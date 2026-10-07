#!/usr/bin/env python3
"""
Review item 7: path/filename hardening. Spaces, quotes, unicode, leading
dots, very long names, duplicate names, and unexpected extensions must
all intake cleanly without ever writing outside the Citadel root, while
the real original filename is still preserved verbatim for provenance.
Also: a moderately large (non-huge, sandbox-disk-friendly) file, to
exercise chunked hashing/copying on something bigger than a few bytes.
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

sys.path.insert(0, LIB)
import citadel_core as cc  # noqa: E402


def run_intake(root, source_path, evidence_type="text"):
    cmd = [
        sys.executable, os.path.join(BIN, "citadel-intake"), source_path,
        "--source", "Path Hardening Test", "--evidence-type", evidence_type,
        "--event-date", "2026-10-07", "--event-date-precision", "day",
        "--notes", "path hardening test",
        "--root", root,
    ]
    return subprocess.run(cmd, capture_output=True, text=True)


class TestPathHardening(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(prefix="citadel-path-test-")
        self.root = os.path.join(self._tmp.name, "root")
        self.config = cc.CitadelConfig(root=self.root)

    def tearDown(self):
        self._tmp.cleanup()

    def _intake_named(self, filename, content=b"CITADEL SYNTHETIC TEST\nNOT REAL EVIDENCE\n"):
        src_dir = tempfile.mkdtemp(dir=self._tmp.name)
        src_path = os.path.join(src_dir, filename)
        with open(src_path, "wb") as f:
            f.write(content)
        result = run_intake(self.root, src_path)
        self.assertEqual(result.returncode, 0, msg=f"filename {filename!r}: {result.stderr}{result.stdout}")
        return json.loads(result.stdout), filename

    def _assert_paths_safe_and_filename_preserved(self, receipt, original_filename):
        config = self.config
        with cc.open_db(config) as conn:
            row = conn.execute(
                "SELECT original_path, working_copy_path, original_filename FROM evidence WHERE evidence_id = ?",
                (receipt["evidence_id"],),
            ).fetchone()

        # On-disk paths never escape the root.
        root_real = os.path.realpath(config.root)
        for p in (row["original_path"], row["working_copy_path"]):
            self.assertEqual(os.path.commonpath([root_real, os.path.realpath(p)]), root_real)
            self.assertTrue(os.path.isfile(p))

        # The true original filename is preserved verbatim for provenance,
        # even though the on-disk filename may have been sanitized.
        self.assertEqual(row["original_filename"], original_filename)

        sidecar = cc.read_intake_sidecar(config, receipt["evidence_id"])
        self.assertEqual(sidecar["original_filename"], original_filename)

    def test_filename_with_spaces(self):
        receipt, name = self._intake_named("a file with spaces.txt")
        self._assert_paths_safe_and_filename_preserved(receipt, name)

    def test_filename_with_quotes(self):
        receipt, name = self._intake_named('weird"quoted\'name.txt')
        self._assert_paths_safe_and_filename_preserved(receipt, name)

    def test_filename_with_unicode(self):
        receipt, name = self._intake_named("日本語_émoji_😀_файл.txt")
        self._assert_paths_safe_and_filename_preserved(receipt, name)

    def test_filename_with_leading_dot(self):
        receipt, name = self._intake_named(".hidden_evidence.txt")
        self._assert_paths_safe_and_filename_preserved(receipt, name)

    def test_very_long_filename(self):
        # 220 chars + ".txt" = 224 bytes, which real filesystems (NAME_MAX
        # is commonly 255 bytes) will still let us create as a *source*
        # file — the point of this test is citadel-intake's own
        # truncation of the *on-disk copy's* name (sanitize_filename's
        # 180-byte budget), not whether the OS itself has a limit.
        long_stem = "x" * 220
        receipt, name = self._intake_named(f"{long_stem}.txt")
        self._assert_paths_safe_and_filename_preserved(receipt, name)
        # The on-disk filename must have been truncated to something a
        # real filesystem will accept.
        config = self.config
        with cc.open_db(config) as conn:
            row = conn.execute(
                "SELECT original_path FROM evidence WHERE evidence_id = ?", (receipt["evidence_id"],)
            ).fetchone()
        on_disk_name = os.path.basename(row["original_path"])
        self.assertLess(len(on_disk_name.encode("utf-8")), 255)

    def test_duplicate_filenames_across_different_evidence_do_not_collide(self):
        receipt1, name1 = self._intake_named("same_name.txt", content=b"first content\n")
        receipt2, name2 = self._intake_named("same_name.txt", content=b"second content, different hash\n")
        self.assertNotEqual(receipt1["evidence_id"], receipt2["evidence_id"])

        config = self.config
        with cc.open_db(config) as conn:
            row1 = conn.execute(
                "SELECT original_path FROM evidence WHERE evidence_id = ?", (receipt1["evidence_id"],)
            ).fetchone()
            row2 = conn.execute(
                "SELECT original_path FROM evidence WHERE evidence_id = ?", (receipt2["evidence_id"],)
            ).fetchone()
        self.assertNotEqual(row1["original_path"], row2["original_path"])
        self.assertTrue(os.path.isfile(row1["original_path"]))
        self.assertTrue(os.path.isfile(row2["original_path"]))

    def test_unexpected_extension_falls_back_to_octet_stream_mime(self):
        receipt, name = self._intake_named("data.notarealext123")
        config = self.config
        with cc.open_db(config) as conn:
            row = conn.execute(
                "SELECT mime_type FROM evidence WHERE evidence_id = ?", (receipt["evidence_id"],)
            ).fetchone()
        self.assertEqual(row["mime_type"], "application/octet-stream")

    def test_moderately_large_file_hashes_and_copies_correctly(self):
        """~20MB — big enough to exercise chunked sha256_file()/copy2()
        across multiple read() calls, small enough not to waste sandbox
        disk. True multi-GB files are a documented remaining risk, not
        tested here — see docs/README.md."""
        import hashlib
        content = os.urandom(20 * 1024 * 1024)
        expected_hash = hashlib.sha256(content).hexdigest()
        receipt, name = self._intake_named("large_synthetic_blob.bin", content=content)
        self.assertEqual(receipt["sha256"], expected_hash)
        self._assert_paths_safe_and_filename_preserved(receipt, name)

    def test_sanitize_filename_never_produces_path_separators(self):
        for raw in ("../../etc/passwd", "a/b/c.txt", "a\\b\\c.txt", "", ".", ".."):
            safe = cc.sanitize_filename(raw)
            self.assertNotIn("/", safe)
            self.assertNotIn("\\", safe)
            self.assertTrue(safe)


if __name__ == "__main__":
    unittest.main(verbosity=2)
