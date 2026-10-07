#!/usr/bin/env python3
"""
Review item 3: the intake sidecar is frozen historical provenance.
citadel-verify must never rewrite it; verification results go to
separate 03_METADATA/verification/*.json records instead.
"""
import hashlib
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


class TestSidecarImmutability(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(prefix="citadel-sidecar-test-")
        self.root = self._tmp.name
        result = run(["citadel-intake", FIXTURE,
                      "--source", "Test Harness", "--evidence-type", "text",
                      "--event-date", "2026-10-01", "--event-date-precision", "day",
                      "--notes", "sidecar immutability test"], self.root)
        assert result.returncode == 0, result.stderr + result.stdout
        self.receipt = json.loads(result.stdout)
        self.config = cc.CitadelConfig(root=self.root)
        self.sidecar_path = cc.intake_sidecar_path(self.config, self.receipt["evidence_id"])

    def tearDown(self):
        self._tmp.cleanup()

    def _sidecar_bytes_and_hash(self):
        with open(self.sidecar_path, "rb") as f:
            data = f.read()
        return data, hashlib.sha256(data).hexdigest()

    def test_sidecar_bytes_unchanged_after_one_verify(self):
        before_bytes, before_hash = self._sidecar_bytes_and_hash()

        result = run(["citadel-verify", "--evidence-id", self.receipt["evidence_id"]], self.root)
        self.assertEqual(result.returncode, 0, msg=result.stderr)

        after_bytes, after_hash = self._sidecar_bytes_and_hash()
        self.assertEqual(before_bytes, after_bytes)
        self.assertEqual(before_hash, after_hash)

    def test_sidecar_bytes_unchanged_after_many_verifies_including_one_that_finds_an_alert(self):
        before_bytes, before_hash = self._sidecar_bytes_and_hash()

        for _ in range(3):
            run(["citadel-verify", "--evidence-id", self.receipt["evidence_id"]], self.root)

        # Now force an INTEGRITY_ALERT (by simulating loss, not tampering
        # with bytes) and verify again — even a verify run that *finds*
        # a problem must not touch the sidecar.
        with cc.open_db(self.config) as conn:
            row = conn.execute(
                "SELECT original_path FROM evidence WHERE evidence_id = ?", (self.receipt["evidence_id"],)
            ).fetchone()
        os.chmod(row["original_path"], 0o644)
        os.remove(row["original_path"])
        run(["citadel-verify", "--evidence-id", self.receipt["evidence_id"]], self.root)

        after_bytes, after_hash = self._sidecar_bytes_and_hash()
        self.assertEqual(before_bytes, after_bytes)
        self.assertEqual(before_hash, after_hash)

    def test_sidecar_is_chmod_read_only(self):
        mode = oct(os.stat(self.sidecar_path).st_mode & 0o777)
        self.assertEqual(mode, "0o444")

    def test_write_intake_sidecar_refuses_to_overwrite_existing(self):
        sidecar = cc.read_intake_sidecar(self.config, self.receipt["evidence_id"])
        with self.assertRaises(FileExistsError):
            cc.write_intake_sidecar(self.config, self.receipt["evidence_id"], sidecar)

    def test_verification_records_land_in_separate_directory(self):
        run(["citadel-verify", "--evidence-id", self.receipt["evidence_id"]], self.root)
        vdir = self.config.path("03_METADATA", "verification")
        self.assertTrue(os.path.isdir(vdir))
        files = os.listdir(vdir)
        self.assertEqual(len(files), 1)
        self.assertIn(self.receipt["evidence_id"], files[0])
        self.assertIn("VERIFY-", files[0])

    def test_multiple_verifies_produce_multiple_verification_records(self):
        for _ in range(3):
            run(["citadel-verify", "--evidence-id", self.receipt["evidence_id"]], self.root)
        vdir = self.config.path("03_METADATA", "verification")
        files = os.listdir(vdir)
        self.assertEqual(len(files), 3)


if __name__ == "__main__":
    unittest.main(verbosity=2)
