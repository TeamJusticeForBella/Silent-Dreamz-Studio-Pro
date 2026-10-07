#!/usr/bin/env python3
"""
Review item 6: source-mutation detection during acquisition.

citadel-intake records the source file's size+mtime before copying and
re-checks them immediately after. Two tests:

  1. Deterministic (the real guarantee): CITADEL_TEST_FAULT=
     mutate_source_after_copy makes citadel-intake itself append a byte
     to the source file right after the copy completes but before the
     post-copy stat check runs. This exercises the exact code path every
     time, with no timing dependency, and is what actually proves the
     detection logic works.
  2. Best-effort real concurrency (documented as racy): a background
     thread tries to mutate the source while the real subprocess is
     running. Included because it's the most honest version of this test
     when it lands inside the window, but a tiny synthetic file copies
     near-instantly, so this is NOT relied on for the core guarantee —
     see REMAINING RISKS in docs/README.md. It only fails if a THIRD,
     actually-wrong thing happens (intake certifies bytes that don't
     match what it hashed).
"""
import json
import os
import subprocess
import sys
import tempfile
import threading
import time
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
BIN = os.path.join(HERE, "..", "bin")
LIB = os.path.join(HERE, "..", "lib")

sys.path.insert(0, LIB)
import citadel_core as cc  # noqa: E402


def run_intake(root, source_path, fault=None):
    cmd = [
        sys.executable, os.path.join(BIN, "citadel-intake"), source_path,
        "--source", "Source Mutation Test", "--evidence-type", "text",
        "--event-date", "2026-10-07", "--event-date-precision", "day",
        "--notes", "source mutation test",
        "--root", root,
    ]
    env = dict(os.environ)
    if fault:
        env["CITADEL_TEST_FAULT"] = fault
    return subprocess.run(cmd, capture_output=True, text=True, env=env)


class TestSourceMutationDeterministic(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(prefix="citadel-sourcemut-test-")
        self.root = os.path.join(self._tmp.name, "root")
        self.source_path = os.path.join(self._tmp.name, "source.txt")
        with open(self.source_path, "w") as f:
            f.write("CITADEL SYNTHETIC TEST\nNOT REAL EVIDENCE\n")

    def tearDown(self):
        self._tmp.cleanup()

    def test_mutation_during_acquisition_is_always_caught_and_refused(self):
        result = run_intake(self.root, self.source_path, fault="mutate_source_after_copy")
        self.assertNotEqual(result.returncode, 0)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["error"], "SOURCE_CHANGED_DURING_INTAKE")
        self.assertIn("size_before", payload)
        self.assertIn("size_after", payload)
        self.assertNotEqual(payload["size_before"], payload["size_after"])

        # No original should have been finalized — the tmp file is
        # cleaned up and the real original path never created.
        config = cc.CitadelConfig(root=self.root)
        with cc.open_db(config) as conn:
            row = conn.execute(
                "SELECT original_path, intake_state FROM evidence WHERE evidence_id = ?",
                (payload["evidence_id"],),
            ).fetchone()
        self.assertEqual(row["intake_state"], "FAILED")
        self.assertFalse(os.path.exists(row["original_path"]))
        tmp_path = config.path("01_ORIGINALS", f".tmp-{payload['evidence_id']}")
        self.assertFalse(os.path.exists(tmp_path))

    def test_without_the_fault_hook_the_same_source_intakes_cleanly(self):
        """Control case: proves the hook (and only the hook) is what
        causes the failure above — an unmutated source succeeds."""
        result = run_intake(self.root, self.source_path, fault=None)
        self.assertEqual(result.returncode, 0, msg=result.stderr + result.stdout)


class TestSourceMutationBestEffortRace(unittest.TestCase):
    """Racy by nature; see module docstring. Only fails on a genuinely
    wrong outcome, never on 'missed the window'."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(prefix="citadel-sourcemut-race-")
        self.root = os.path.join(self._tmp.name, "root")
        self.source_path = os.path.join(self._tmp.name, "source.txt")
        with open(self.source_path, "w") as f:
            f.write("CITADEL SYNTHETIC TEST\nNOT REAL EVIDENCE\n")

    def tearDown(self):
        self._tmp.cleanup()

    def test_best_effort_concurrent_mutation_never_certifies_mismatched_bytes(self):
        def mutate_soon():
            time.sleep(0.001)
            try:
                with open(self.source_path, "a") as f:
                    f.write("MUTATED-BY-BACKGROUND-THREAD\n")
            except OSError:
                pass

        t = threading.Thread(target=mutate_soon)
        t.start()
        result = run_intake(self.root, self.source_path, fault=None)
        t.join(timeout=2)

        if result.returncode == 0:
            receipt = json.loads(result.stdout)
            config = cc.CitadelConfig(root=self.root)
            with cc.open_db(config) as conn:
                row = conn.execute(
                    "SELECT original_path, sha256 FROM evidence WHERE evidence_id = ?",
                    (receipt["evidence_id"],),
                ).fetchone()
            self.assertEqual(cc.sha256_file(row["original_path"]), row["sha256"])
        else:
            payload = json.loads(result.stdout)
            self.assertIn(payload["error"], ("SOURCE_CHANGED_DURING_INTAKE", "INTEGRITY_ALERT"))


class TestSourceMutationFieldsRecordedOnSuccess(unittest.TestCase):
    """Even when nothing changes, the before/after stat fields must be
    present in the sidecar as a matter of record."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(prefix="citadel-sourcemut-fields-")
        self.root = self._tmp.name
        self.source_path = os.path.join(self._tmp.name, "source.txt")
        with open(self.source_path, "w") as f:
            f.write("CITADEL SYNTHETIC TEST\nNOT REAL EVIDENCE\n")

    def tearDown(self):
        self._tmp.cleanup()

    def test_sidecar_records_matching_before_after_stats_on_clean_intake(self):
        result = run_intake(self.root, self.source_path, fault=None)
        self.assertEqual(result.returncode, 0, msg=result.stderr + result.stdout)
        receipt = json.loads(result.stdout)
        config = cc.CitadelConfig(root=self.root)
        sidecar = cc.read_intake_sidecar(config, receipt["evidence_id"])
        self.assertEqual(sidecar["source_size_before"], sidecar["source_size_after"])
        self.assertEqual(sidecar["source_mtime_before_ns"], sidecar["source_mtime_after_ns"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
