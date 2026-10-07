#!/usr/bin/env python3
"""
Review item 1: evidence-ID concurrency. Launches several real
citadel-intake subprocesses at once against the same --root and proves
every evidence_id is unique and every row is correctly indexed — i.e.
reserve_evidence()'s single BEGIN IMMEDIATE transaction (mint + insert
together) actually closes the race that existed in V1, where the id was
minted and committed *before* the row was inserted.
"""
import concurrent.futures
import json
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
BIN = os.path.join(HERE, "..", "bin")
LIB = os.path.join(HERE, "..", "lib")

sys.path.insert(0, LIB)
import citadel_core as cc  # noqa: E402

N_CONCURRENT = 8


def make_distinct_fixture(tmp_dir, index):
    path = os.path.join(tmp_dir, f"concurrent_fixture_{index}.txt")
    with open(path, "w") as f:
        f.write(f"CITADEL SYNTHETIC TEST\nNOT REAL EVIDENCE\nconcurrency-slot-{index}\n")
    return path


def intake_once(root, source_file, index):
    cmd = [
        sys.executable, os.path.join(BIN, "citadel-intake"), source_file,
        "--source", f"Concurrency Test {index}", "--evidence-type", "text",
        "--event-date", "2026-10-07", "--event-date-precision", "day",
        "--notes", f"concurrency slot {index}",
        "--root", root,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return index, result


class TestConcurrentIntake(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(prefix="citadel-concurrency-test-")
        self.root = self._tmp.name

    def tearDown(self):
        self._tmp.cleanup()

    def test_simultaneous_intakes_all_get_unique_evidence_ids(self):
        fixtures = [make_distinct_fixture(self._tmp.name, i) for i in range(N_CONCURRENT)]

        with concurrent.futures.ThreadPoolExecutor(max_workers=N_CONCURRENT) as pool:
            futures = [pool.submit(intake_once, self.root, fixtures[i], i) for i in range(N_CONCURRENT)]
            outcomes = [f.result() for f in futures]

        evidence_ids = []
        for index, result in outcomes:
            self.assertEqual(result.returncode, 0,
                              msg=f"slot {index} failed: {result.stderr}{result.stdout}")
            receipt = json.loads(result.stdout)
            evidence_ids.append(receipt["evidence_id"])

        self.assertEqual(len(evidence_ids), N_CONCURRENT)
        self.assertEqual(len(set(evidence_ids)), N_CONCURRENT,
                          f"duplicate evidence_id minted under concurrency: {evidence_ids}")

    def test_simultaneous_intakes_all_land_as_rows_in_the_db(self):
        fixtures = [make_distinct_fixture(self._tmp.name, i) for i in range(N_CONCURRENT)]

        with concurrent.futures.ThreadPoolExecutor(max_workers=N_CONCURRENT) as pool:
            futures = [pool.submit(intake_once, self.root, fixtures[i], i) for i in range(N_CONCURRENT)]
            outcomes = [f.result() for f in futures]

        for index, result in outcomes:
            self.assertEqual(result.returncode, 0, msg=f"slot {index}: {result.stderr}{result.stdout}")

        config = cc.CitadelConfig(root=self.root)
        with cc.open_db(config) as conn:
            count = conn.execute("SELECT COUNT(*) c FROM evidence").fetchone()["c"]
            distinct_ids = conn.execute("SELECT COUNT(DISTINCT evidence_id) c FROM evidence").fetchone()["c"]
            complete_count = conn.execute(
                "SELECT COUNT(*) c FROM evidence WHERE intake_state = 'COMPLETE'"
            ).fetchone()["c"]

        self.assertEqual(count, N_CONCURRENT)
        self.assertEqual(distinct_ids, N_CONCURRENT)
        self.assertEqual(complete_count, N_CONCURRENT)


if __name__ == "__main__":
    unittest.main(verbosity=2)
