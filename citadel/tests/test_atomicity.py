#!/usr/bin/env python3
"""
Review item 5: crash/failure atomicity. Uses citadel_core's
CITADEL_TEST_FAULT env-var hook (a no-op unless explicitly set — never
active in normal/real use) to inject failures at specific points in the
pipeline, and proves that:
  - the evidence row is marked FAILED, never COMPLETE
  - a finalized original is never deleted once it exists
  - a failure before the original is finalized leaves no original behind
  - diagnostic state (intake_state, audit_log) survives the failure
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


def run_intake(root, fault=None):
    cmd = [
        sys.executable, os.path.join(BIN, "citadel-intake"), FIXTURE,
        "--source", "Fault Injection Test", "--evidence-type", "text",
        "--event-date", "2026-10-07", "--event-date-precision", "day",
        "--notes", f"fault={fault}",
        "--root", root,
    ]
    env = dict(os.environ)
    if fault:
        env["CITADEL_TEST_FAULT"] = fault
    return subprocess.run(cmd, capture_output=True, text=True, env=env)


class AtomicityTestCase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(prefix="citadel-atomicity-test-")
        self.root = self._tmp.name
        self.config = cc.CitadelConfig(root=self.root)

    def tearDown(self):
        self._tmp.cleanup()

    def _row_for_only_evidence(self):
        with cc.open_db(self.config) as conn:
            return conn.execute("SELECT * FROM evidence ORDER BY created_at DESC LIMIT 1").fetchone()

    def _assert_failed_cleanly(self, result, expected_error=None):
        self.assertNotEqual(result.returncode, 0)
        payload = json.loads(result.stdout)
        if expected_error:
            self.assertEqual(payload["error"], expected_error)

        row = self._row_for_only_evidence()
        self.assertIsNotNone(row, "no evidence row at all was reserved")
        self.assertEqual(row["intake_state"], "FAILED")

        with cc.open_db(self.config) as conn:
            actions = [r["action"] for r in conn.execute(
                "SELECT action FROM audit_log WHERE evidence_id = ? ORDER BY id", (row["evidence_id"],)
            )]
        self.assertIn("RESERVED", actions)
        self.assertIn("FAILED", actions)
        return row


class TestCopyFailure(AtomicityTestCase):
    def test_copy_failure_marks_failed_and_creates_no_original(self):
        result = run_intake(self.root, fault="copy_failure")
        row = self._assert_failed_cleanly(result, expected_error="INTAKE_FAILED")
        self.assertFalse(os.path.exists(row["original_path"]), "original exists despite copy failure")
        tmp_path = self.config.path("01_ORIGINALS", f".tmp-{row['evidence_id']}")
        self.assertFalse(os.path.exists(tmp_path), "staging tmp file was left behind after copy failure")


class TestDiskFullDuringCopy(AtomicityTestCase):
    def test_disk_full_marks_failed_and_creates_no_original(self):
        result = run_intake(self.root, fault="disk_full")
        row = self._assert_failed_cleanly(result, expected_error="INTAKE_FAILED")
        self.assertFalse(os.path.exists(row["original_path"]))


class TestSidecarWriteFailure(AtomicityTestCase):
    def test_sidecar_write_failure_preserves_already_finalized_original(self):
        """
        By the time the sidecar is written, the original has already
        been finalized (atomic rename + chmod 0o444) and the working copy
        created. A failure AFTER that point must never delete them —
        this is the "never silently delete an already-created original"
        rule in action.
        """
        result = run_intake(self.root, fault="sidecar_write_failure")
        row = self._assert_failed_cleanly(result, expected_error="INTAKE_FAILED")
        self.assertTrue(os.path.exists(row["original_path"]),
                         "a finalized original was deleted after a later-stage failure")
        self.assertTrue(os.path.exists(row["working_copy_path"]))
        # And the sidecar itself must NOT exist, since write_intake_sidecar
        # never got to (or failed partway through) writing it.
        sidecar_path = cc.intake_sidecar_path(self.config, row["evidence_id"])
        self.assertFalse(os.path.exists(sidecar_path))


class TestDbWriteFailure(AtomicityTestCase):
    def test_db_write_failure_preserves_sidecar_and_original(self):
        """
        By this point the sidecar has already been written (frozen) and
        the original/working copy finalized. The injected failure only
        prevents the hashes/events/processing_jobs inserts — those rows
        should be absent, but nothing already on disk should vanish.
        """
        result = run_intake(self.root, fault="db_write_failure")
        row = self._assert_failed_cleanly(result, expected_error="INTAKE_FAILED")
        self.assertTrue(os.path.exists(row["original_path"]))
        self.assertTrue(os.path.exists(row["working_copy_path"]))
        sidecar_path = cc.intake_sidecar_path(self.config, row["evidence_id"])
        self.assertTrue(os.path.exists(sidecar_path))

        with cc.open_db(self.config) as conn:
            job_count = conn.execute(
                "SELECT COUNT(*) c FROM processing_jobs WHERE evidence_id = ?", (row["evidence_id"],)
            ).fetchone()["c"]
        self.assertEqual(job_count, 0, "processing_jobs rows exist despite injected db_write_failure")


class TestWorkingCopyFailure(AtomicityTestCase):
    def test_working_copy_failure_preserves_finalized_original_but_no_sidecar(self):
        result = run_intake(self.root, fault="working_copy_failure")
        row = self._assert_failed_cleanly(result, expected_error="INTAKE_FAILED")
        self.assertTrue(os.path.exists(row["original_path"]),
                         "a finalized original was deleted after a working-copy-stage failure")
        self.assertFalse(os.path.exists(row["working_copy_path"]))
        sidecar_path = cc.intake_sidecar_path(self.config, row["evidence_id"])
        self.assertFalse(os.path.exists(sidecar_path))


class TestNoFaultControlCase(AtomicityTestCase):
    def test_unset_fault_env_var_never_triggers_anything(self):
        """Sanity check for the hook itself: with no CITADEL_TEST_FAULT
        set, intake must succeed normally. This is what guarantees the
        fault-injection hooks are inert in real/production use."""
        result = run_intake(self.root, fault=None)
        self.assertEqual(result.returncode, 0, msg=result.stderr + result.stdout)
        receipt = json.loads(result.stdout)
        row = self._row_for_only_evidence()
        self.assertEqual(row["evidence_id"], receipt["evidence_id"])
        self.assertEqual(row["intake_state"], "COMPLETE")


if __name__ == "__main__":
    unittest.main(verbosity=2)
