#!/usr/bin/env python3
"""
Review item 4: prove the ACTUAL CLI disk gate, not just the core
function. Runs the real citadel-intake binary with an impossible
--min-free-gib threshold and proves nothing at all gets created.
"""
import json
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
BIN = os.path.join(HERE, "..", "bin")
FIXTURE = os.path.join(HERE, "fixtures", "synthetic_evidence.txt")


def run_intake_with_impossible_gate(root):
    cmd = [
        sys.executable, os.path.join(BIN, "citadel-intake"), FIXTURE,
        "--source", "Test Harness", "--evidence-type", "text",
        "--event-date", "2026-10-01", "--event-date-precision", "day",
        "--notes", "disk gate CLI test",
        "--root", root, "--min-free-gib", "999999999",
    ]
    return subprocess.run(cmd, capture_output=True, text=True)


class TestDiskGateCLI(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(prefix="citadel-gate-test-")
        # Root does not exist yet — citadel-intake must not even create it.
        self.root = os.path.join(self._tmp.name, "citadel_root")

    def tearDown(self):
        self._tmp.cleanup()

    def test_cli_refuses_with_nonzero_exit_and_disk_safety_gate_error(self):
        result = run_intake_with_impossible_gate(self.root)
        self.assertNotEqual(result.returncode, 0)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["error"], "DISK_SAFETY_GATE")
        self.assertIn("free_gib", payload)
        self.assertIn("min_gib", payload)
        self.assertEqual(payload["min_gib"], 999999999)

    def test_cli_creates_absolutely_nothing_on_gate_failure(self):
        run_intake_with_impossible_gate(self.root)

        # The root directory itself must not exist — not even an attempt
        # to mkdir it before bailing out.
        self.assertFalse(os.path.exists(self.root), "root directory was created despite gate failure")

    def test_gate_failure_on_preexisting_empty_root_leaves_it_empty(self):
        os.makedirs(self.root)
        run_intake_with_impossible_gate(self.root)
        self.assertEqual(os.listdir(self.root), [], "gate failure left files/dirs behind in an existing root")


if __name__ == "__main__":
    unittest.main(verbosity=2)
