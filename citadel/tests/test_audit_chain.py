#!/usr/bin/env python3
"""
Review item 9: chained audit hashes. Every line in 06_LOGS/intake.log
carries previous_entry_hash/entry_hash; citadel-audit-verify must
confirm an untouched chain and pinpoint the first broken record after
tampering.
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


def intake(root, notes="chain test"):
    result = run(["citadel-intake", FIXTURE,
                  "--source", "Chain Test", "--evidence-type", "text",
                  "--event-date", "2026-10-07", "--event-date-precision", "day",
                  "--notes", notes], root)
    assert result.returncode == 0, result.stderr + result.stdout
    return json.loads(result.stdout)


class TestAuditChain(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(prefix="citadel-chain-test-")
        self.root = self._tmp.name
        self.config = cc.CitadelConfig(root=self.root)

    def tearDown(self):
        self._tmp.cleanup()

    def test_no_log_yet_reports_no_log_and_exit_zero(self):
        result = run(["citadel-audit-verify", "--json"], self.root)
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "NO_LOG")

    def test_chain_verifies_ok_after_several_intakes(self):
        for i in range(5):
            intake(self.root, notes=f"entry {i}")
        result = run(["citadel-audit-verify", "--json"], self.root)
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "OK")
        self.assertEqual(payload["entries"], 5)

    def test_every_line_carries_previous_and_entry_hash(self):
        intake(self.root)
        intake(self.root)
        with open(self.config.intake_log_path) as f:
            lines = [json.loads(l) for l in f if l.strip()]
        self.assertEqual(len(lines), 2)
        self.assertEqual(lines[0]["previous_entry_hash"], cc.GENESIS_HASH)
        self.assertEqual(lines[1]["previous_entry_hash"], lines[0]["entry_hash"])
        for line in lines:
            self.assertEqual(len(line["entry_hash"]), 64)

    def test_tampering_with_a_field_breaks_the_chain_at_that_line(self):
        for i in range(4):
            intake(self.root, notes=f"entry {i}")

        with open(self.config.intake_log_path) as f:
            lines = [json.loads(l) for l in f if l.strip()]
        # Tamper with line 3 (1-indexed) without recomputing its hash —
        # the naive tampering this tool is designed to catch.
        lines[2]["notes_tampered"] = True
        with open(self.config.intake_log_path, "w") as f:
            for line in lines:
                f.write(json.dumps(line, sort_keys=True) + "\n")

        result = run(["citadel-audit-verify", "--json"], self.root)
        self.assertEqual(result.returncode, 1)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "BROKEN")
        self.assertEqual(payload["broken_at_line"], 3)

    def test_deleting_a_line_breaks_the_link_at_the_following_line(self):
        for i in range(4):
            intake(self.root, notes=f"entry {i}")
        with open(self.config.intake_log_path) as f:
            lines = [json.loads(l) for l in f if l.strip()]
        del lines[1]  # remove the second entry entirely
        with open(self.config.intake_log_path, "w") as f:
            for line in lines:
                f.write(json.dumps(line, sort_keys=True) + "\n")

        result = run(["citadel-audit-verify", "--json"], self.root)
        self.assertEqual(result.returncode, 1)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "BROKEN")
        self.assertEqual(payload["broken_at_line"], 2)
        self.assertEqual(payload["reason"], "previous_hash_mismatch")

    def test_concurrent_appends_do_not_fork_the_chain(self):
        """Uses the same locking path exercised by test_concurrency.py's
        real concurrent intakes; here we just confirm the resulting chain
        (built from several concurrent citadel-intake processes) is a
        single, valid sequence rather than forked or corrupted."""
        import concurrent.futures

        def do_intake(i):
            src = os.path.join(self._tmp.name, f"chain_src_{i}.txt")
            with open(src, "w") as f:
                f.write(f"CITADEL SYNTHETIC TEST\nNOT REAL EVIDENCE\nslot-{i}\n")
            cmd = [
                sys.executable, os.path.join(BIN, "citadel-intake"), src,
                "--source", "Chain Concurrency Test", "--evidence-type", "text",
                "--event-date", "2026-10-07", "--event-date-precision", "day",
                "--notes", f"chain concurrency {i}", "--root", self.root,
            ]
            return subprocess.run(cmd, capture_output=True, text=True)

        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
            results = list(pool.map(do_intake, range(6)))

        for r in results:
            self.assertEqual(r.returncode, 0, msg=r.stderr + r.stdout)

        result = run(["citadel-audit-verify", "--json"], self.root)
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "OK")
        self.assertEqual(payload["entries"], 6)


if __name__ == "__main__":
    unittest.main(verbosity=2)
