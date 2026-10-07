#!/usr/bin/env python3
"""
Review item 2: citadel-status must make ZERO filesystem/DB mutations.
Covers both the "DB doesn't exist yet" case (must report
NOT_INITIALIZED and create nothing) and the "DB already has data" case
(a full directory snapshot before/after must be byte-for-byte identical,
including every file's mtime).
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


def snapshot(root):
    """Maps every file path (relative to root) to (size, mtime_ns).
    Returns an empty dict if root doesn't exist."""
    out = {}
    if not os.path.exists(root):
        return out
    for dirpath, _dirnames, filenames in os.walk(root):
        for name in filenames:
            full = os.path.join(dirpath, name)
            rel = os.path.relpath(full, root)
            st = os.stat(full)
            out[rel] = (st.st_size, st.st_mtime_ns)
    return out


class TestReadonlyStatusOnMissingDB(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(prefix="citadel-ro-test-")
        self.root = os.path.join(self._tmp.name, "citadel_root")  # does not exist

    def tearDown(self):
        self._tmp.cleanup()

    def test_reports_not_initialized_and_creates_nothing(self):
        self.assertFalse(os.path.exists(self.root))
        result = run(["citadel-status", "--json"], self.root)
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["db_status"], "NOT_INITIALIZED")
        self.assertFalse(report["root_exists"])
        # The real test: did it actually create the directory it just
        # reported as not existing?
        self.assertFalse(os.path.exists(self.root), "citadel-status created the root it reported as missing")

    def test_running_status_twice_on_missing_db_stays_idempotent(self):
        run(["citadel-status", "--json"], self.root)
        run(["citadel-status", "--json"], self.root)
        self.assertFalse(os.path.exists(self.root))


class TestReadonlyStatusWithExistingData(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(prefix="citadel-ro-test-")
        self.root = self._tmp.name
        intake_cmd = [
            "citadel-intake", FIXTURE,
            "--source", "Test Harness", "--evidence-type", "text",
            "--event-date", "2026-10-01", "--event-date-precision", "day",
            "--notes", "readonly status test",
        ]
        result = run(intake_cmd, self.root)
        assert result.returncode == 0, result.stderr + result.stdout

    def tearDown(self):
        self._tmp.cleanup()

    def test_status_run_changes_no_file_bytes_or_mtimes(self):
        before = snapshot(self.root)
        self.assertGreater(len(before), 0, "setUp's intake didn't create any files?")

        result = run(["citadel-status", "--json"], self.root)
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["db_status"], "OK")
        self.assertEqual(report["evidence"]["total"], 1)

        after = snapshot(self.root)
        self.assertEqual(before, after, "citadel-status mutated file contents, sizes, or mtimes")

    def test_status_creates_no_new_files(self):
        before = set(snapshot(self.root).keys())
        run(["citadel-status", "--json"], self.root)
        after = set(snapshot(self.root).keys())
        self.assertEqual(before, after, "citadel-status created or removed files")

    def test_status_human_output_mode_is_also_read_only(self):
        before = snapshot(self.root)
        result = run(["citadel-status"], self.root)  # no --json
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        after = snapshot(self.root)
        self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main(verbosity=2)
