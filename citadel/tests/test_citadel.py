#!/usr/bin/env python3
"""
Citadel Intake V1 test suite — synthetic fixture only, never touches any
real evidence tree. Every test runs against a fresh tempfile.TemporaryDirectory
used as --root / $CITADEL_ROOT, so nothing here can collide with, or even
see, an operator's actual ~/Citadel.

Run:
    python3 citadel/tests/test_citadel.py
"""
import json
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
BIN = os.path.join(HERE, "..", "bin")
LIB = os.path.join(HERE, "..", "lib")
FIXTURE = os.path.join(HERE, "fixtures", "synthetic_evidence.txt")

sys.path.insert(0, LIB)
import citadel_core as cc  # noqa: E402


def run(cmd, root):
    full = [sys.executable, os.path.join(BIN, cmd[0]), *cmd[1:], "--root", root]
    return subprocess.run(full, capture_output=True, text=True)


class CitadelTestCase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(prefix="citadel-test-")
        self.root = self._tmp.name

    def tearDown(self):
        # Originals are chmod 0o444; TemporaryDirectory cleanup needs write
        # perms on the containing dirs, which it retains, so this is fine.
        self._tmp.cleanup()

    def intake(self, **kwargs):
        args = ["citadel-intake", FIXTURE,
                "--source", kwargs.get("source", "Test Harness"),
                "--evidence-type", kwargs.get("evidence_type", "text"),
                "--event-date", kwargs.get("event_date", "2026-10-01"),
                "--event-date-precision", kwargs.get("event_date_precision", "day"),
                "--notes", kwargs.get("notes", "synthetic test fixture")]
        result = run(args, self.root)
        self.assertEqual(result.returncode, 0, msg=result.stderr + result.stdout)
        return json.loads(result.stdout)


class TestIntake(CitadelTestCase):
    def test_ingest_creates_receipt_with_expected_fields(self):
        receipt = self.intake()
        self.assertIn("evidence_id", receipt)
        self.assertRegex(receipt["evidence_id"], r"^EVD-\d{8}-\d{6}$")
        self.assertEqual(receipt["integrity_status"], "OK")
        self.assertIn("sha256", receipt)
        self.assertEqual(len(receipt["sha256"]), 64)

    def test_hash_matches_known_fixture_content(self):
        import hashlib
        with open(FIXTURE, "rb") as f:
            expected = hashlib.sha256(f.read()).hexdigest()
        receipt = self.intake()
        self.assertEqual(receipt["sha256"], expected)

    def test_original_and_working_copy_both_exist_and_are_byte_identical(self):
        receipt = self.intake()
        config = cc.CitadelConfig(root=self.root)
        with cc.open_db(config) as conn:
            row = conn.execute(
                "SELECT * FROM evidence WHERE evidence_id = ?", (receipt["evidence_id"],)
            ).fetchone()
        self.assertTrue(os.path.isfile(row["original_path"]))
        self.assertTrue(os.path.isfile(row["working_copy_path"]))
        with open(row["original_path"], "rb") as f1, open(row["working_copy_path"], "rb") as f2:
            self.assertEqual(f1.read(), f2.read())

    def test_original_is_chmod_read_only(self):
        receipt = self.intake()
        config = cc.CitadelConfig(root=self.root)
        with cc.open_db(config) as conn:
            row = conn.execute(
                "SELECT original_path FROM evidence WHERE evidence_id = ?", (receipt["evidence_id"],)
            ).fetchone()
        mode = oct(os.stat(row["original_path"]).st_mode & 0o777)
        self.assertEqual(mode, "0o444")


class TestIndex(CitadelTestCase):
    def test_db_created_with_all_required_tables(self):
        self.intake()
        config = cc.CitadelConfig(root=self.root)
        with cc.open_db(config) as conn:
            tables = {
                r["name"] for r in conn.execute(
                    "SELECT name FROM sqlite_master WHERE type='table'"
                )
            }
        for required in ("evidence", "hashes", "events", "processing_jobs", "audit_log"):
            self.assertIn(required, tables)

    def test_processing_jobs_queued_for_text_evidence_metadata_adapter(self):
        receipt = self.intake(evidence_type="text")
        config = cc.CitadelConfig(root=self.root)
        with cc.open_db(config) as conn:
            jobs = conn.execute(
                "SELECT job_type, status, adapter_status FROM processing_jobs WHERE evidence_id = ?",
                (receipt["evidence_id"],),
            ).fetchall()
        job_types = {j["job_type"] for j in jobs}
        # text/plain only routes to METADATA_EXTRACTION per ADAPTER_ROUTING
        self.assertIn("METADATA_EXTRACTION", job_types)
        meta_job = next(j for j in jobs if j["job_type"] == "METADATA_EXTRACTION")
        self.assertEqual(meta_job["adapter_status"], "CONNECTED")


class TestVerify(CitadelTestCase):
    def test_verify_all_reports_ok_immediately_after_intake(self):
        self.intake()
        result = run(["citadel-verify", "--all"], self.root)
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        results = json.loads(result.stdout)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["integrity_status"], "OK")

    def test_modifying_working_copy_does_not_break_original_verification(self):
        """
        Proves the integrity model: mutating the WORKING COPY must never
        affect the ORIGINAL's verification. We deliberately do NOT touch
        the original — that would violate the no-intentional-corruption
        rule for this test suite.
        """
        receipt = self.intake()
        config = cc.CitadelConfig(root=self.root)
        with cc.open_db(config) as conn:
            row = conn.execute(
                "SELECT working_copy_path FROM evidence WHERE evidence_id = ?",
                (receipt["evidence_id"],),
            ).fetchone()

        with open(row["working_copy_path"], "a") as f:
            f.write("TAMPERED WORKING COPY — SHOULD NOT AFFECT ORIGINAL\n")

        result = run(["citadel-verify", "--evidence-id", receipt["evidence_id"]], self.root)
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        results = json.loads(result.stdout)
        self.assertEqual(results[0]["integrity_status"], "OK")
        self.assertEqual(results[0]["sha256"], receipt["sha256"])

    def test_verify_reports_integrity_alert_if_original_file_removed(self):
        """
        We never corrupt an original to test this (per the assignment's
        rule). Simulating *loss* of the original (not tampering with its
        bytes) is an acceptable, distinct failure mode to exercise, since
        no evidentiary bytes are altered — the file is simply absent.
        """
        receipt = self.intake()
        config = cc.CitadelConfig(root=self.root)
        with cc.open_db(config) as conn:
            row = conn.execute(
                "SELECT original_path FROM evidence WHERE evidence_id = ?",
                (receipt["evidence_id"],),
            ).fetchone()
        os.chmod(row["original_path"], 0o644)
        os.remove(row["original_path"])

        result = run(["citadel-verify", "--evidence-id", receipt["evidence_id"]], self.root)
        self.assertEqual(result.returncode, 1)
        results = json.loads(result.stdout)
        self.assertEqual(results[0]["integrity_status"], "INTEGRITY_ALERT")


class TestDuplicateDetection(CitadelTestCase):
    def test_second_intake_of_identical_bytes_is_flagged_duplicate(self):
        first = self.intake()
        second = self.intake()
        self.assertNotEqual(first["evidence_id"], second["evidence_id"])
        self.assertEqual(second["duplicate_of"], first["evidence_id"])
        self.assertIsNone(first["duplicate_of"])


class TestSidecarValidation(CitadelTestCase):
    def test_sidecar_written_and_has_all_required_fields(self):
        receipt = self.intake()
        config = cc.CitadelConfig(root=self.root)
        sidecar = cc.read_sidecar(config, receipt["evidence_id"])
        cc.validate_sidecar(sidecar)  # raises on failure
        for field in cc.SIDECAR_FIELDS:
            self.assertIn(field, sidecar)
        self.assertEqual(sidecar["evidence_id"], receipt["evidence_id"])
        self.assertEqual(sidecar["sha256"], receipt["sha256"])

    def test_sidecar_rejects_bad_evidence_type(self):
        bad = {f: "x" for f in cc.SIDECAR_FIELDS}
        bad["evidence_type"] = "not-a-real-type"
        bad["event_date_precision"] = "day"
        with self.assertRaises(ValueError):
            cc.validate_sidecar(bad)

    def test_sidecar_rejects_missing_field(self):
        incomplete = {f: "x" for f in cc.SIDECAR_FIELDS[:-1]}
        with self.assertRaises(ValueError):
            cc.validate_sidecar(incomplete)


class TestAuditLog(CitadelTestCase):
    def test_every_intake_produces_audit_trail(self):
        receipt = self.intake()
        config = cc.CitadelConfig(root=self.root)
        with cc.open_db(config) as conn:
            actions = [
                r["action"] for r in conn.execute(
                    "SELECT action FROM audit_log WHERE evidence_id = ? ORDER BY id",
                    (receipt["evidence_id"],),
                )
            ]
        for expected in ("ORIGINAL_COPIED", "HASH_ORIGINAL", "WORKING_COPY_CREATED",
                          "SIDECAR_WRITTEN", "PROCESSING_JOBS_QUEUED"):
            self.assertIn(expected, actions)

    def test_verify_appends_to_audit_log_without_erasing_history(self):
        receipt = self.intake()
        config = cc.CitadelConfig(root=self.root)
        with cc.open_db(config) as conn:
            before = conn.execute(
                "SELECT COUNT(*) c FROM audit_log WHERE evidence_id = ?", (receipt["evidence_id"],)
            ).fetchone()["c"]

        run(["citadel-verify", "--evidence-id", receipt["evidence_id"]], self.root)

        with cc.open_db(config) as conn:
            after = conn.execute(
                "SELECT COUNT(*) c FROM audit_log WHERE evidence_id = ?", (receipt["evidence_id"],)
            ).fetchone()["c"]
        self.assertGreater(after, before)

    def test_intake_log_jsonl_is_append_only_and_parseable(self):
        r1 = self.intake()
        r2 = self.intake()
        config = cc.CitadelConfig(root=self.root)
        with open(config.intake_log_path) as f:
            lines = [json.loads(line) for line in f if line.strip()]
        ids = {l["evidence_id"] for l in lines}
        self.assertIn(r1["evidence_id"], ids)
        self.assertIn(r2["evidence_id"], ids)


class TestDiskSafetyGate(CitadelTestCase):
    def test_gate_blocks_intake_when_min_free_gib_is_absurdly_high(self):
        config_path = os.path.join(self.root, "config.json")
        with open(config_path, "w") as f:
            json.dump({"min_free_gib": 999999}, f)
        # citadel-intake reads config.json from the repo's own config/ dir,
        # not --root, so we simulate the gate directly via citadel_core
        # with an overridden config object instead of the CLI.
        cfg = cc.CitadelConfig(root=self.root)
        cfg.min_free_gib = 999999
        ok, free_gib, min_gib = cc.check_disk_safety_gate(cfg)
        self.assertFalse(ok)
        self.assertEqual(min_gib, 999999)


class TestStatus(CitadelTestCase):
    def test_status_json_reports_expected_shape(self):
        self.intake()
        result = run(["citadel-status", "--json"], self.root)
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        report = json.loads(result.stdout)
        for key in ("citadel_root", "disk", "adapters", "evidence", "recent_audit"):
            self.assertIn(key, report)
        self.assertEqual(report["evidence"]["total"], 1)
        for adapter in cc.ADAPTER_TYPES:
            self.assertIn(adapter, report["adapters"])
            self.assertIn(report["adapters"][adapter]["status"], ("CONNECTED", "NOT_CONNECTED"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
