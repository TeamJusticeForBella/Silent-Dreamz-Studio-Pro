"""Tests for the read-only evidence scanner.

Uses synthetic fixtures only — no real evidence.
Verifies the scanner never modifies the scanned tree.
"""
import hashlib
import json
import os
import stat
import tempfile
from pathlib import Path

import pytest

# Import with -I semantics (scanner is not a package)
import importlib.util
_spec = importlib.util.spec_from_file_location(
    "scan", str(Path(__file__).resolve().parent.parent / "scan.py")
)
scan_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(scan_mod)

scan_path = scan_mod.scan_path
write_csv = scan_mod.write_csv
write_json = scan_mod.write_json
find_duplicates = scan_mod.find_duplicates
main = scan_mod.main
sha256_file = scan_mod.sha256_file


@pytest.fixture
def synthetic_tree(tmp_path):
    """Create a synthetic evidence directory with known contents."""
    (tmp_path / "doc1.pdf").write_bytes(b"synthetic pdf content")
    (tmp_path / "doc2.txt").write_text("synthetic text document")

    sub = tmp_path / "subdir"
    sub.mkdir()
    (sub / "photo.jpg").write_bytes(b"\xff\xd8\xff\xe0synthetic jpeg")
    (sub / "notes.md").write_text("# Case Notes\nSynthetic only.")

    dup = tmp_path / "duplicates"
    dup.mkdir()
    (dup / "copy_a.bin").write_bytes(b"identical content")
    (dup / "copy_b.bin").write_bytes(b"identical content")

    return tmp_path


@pytest.fixture
def snapshot_mtimes(synthetic_tree):
    """Record mtimes before scanning to verify nothing changed."""
    mtimes = {}
    for dirpath, _, filenames in os.walk(synthetic_tree):
        for f in filenames:
            full = os.path.join(dirpath, f)
            mtimes[full] = os.stat(full).st_mtime
    return mtimes


def test_scan_finds_all_files(synthetic_tree):
    entries = scan_path(str(synthetic_tree))
    names = {e["filename"] for e in entries}
    assert names == {"doc1.pdf", "doc2.txt", "photo.jpg", "notes.md", "copy_a.bin", "copy_b.bin"}


def test_scan_computes_sha256(synthetic_tree):
    entries = scan_path(str(synthetic_tree))
    for e in entries:
        assert e["sha256"] is not None
        assert len(e["sha256"]) == 64


def test_sha256_matches_known_value(synthetic_tree):
    expected = hashlib.sha256(b"synthetic pdf content").hexdigest()
    entries = scan_path(str(synthetic_tree))
    pdf = [e for e in entries if e["filename"] == "doc1.pdf"][0]
    assert pdf["sha256"] == expected


def test_scan_records_size(synthetic_tree):
    entries = scan_path(str(synthetic_tree))
    pdf = [e for e in entries if e["filename"] == "doc1.pdf"][0]
    assert pdf["size_bytes"] == len(b"synthetic pdf content")


def test_scan_records_mtime(synthetic_tree):
    entries = scan_path(str(synthetic_tree))
    for e in entries:
        assert e["mtime_utc"] is not None
        assert "T" in e["mtime_utc"]


def test_scan_does_not_modify_files(synthetic_tree, snapshot_mtimes):
    scan_path(str(synthetic_tree))
    for full, original_mtime in snapshot_mtimes.items():
        assert os.stat(full).st_mtime == original_mtime, f"Scanner modified {full}"


def test_scan_does_not_create_files(synthetic_tree):
    before = set()
    for dirpath, _, filenames in os.walk(synthetic_tree):
        for f in filenames:
            before.add(os.path.join(dirpath, f))

    scan_path(str(synthetic_tree))

    after = set()
    for dirpath, _, filenames in os.walk(synthetic_tree):
        for f in filenames:
            after.add(os.path.join(dirpath, f))

    assert after == before, f"Scanner created files: {after - before}"


@pytest.mark.skipif(os.getuid() == 0, reason="root bypasses file permissions")
def test_scan_reports_permission_error(synthetic_tree):
    restricted = synthetic_tree / "restricted.dat"
    restricted.write_bytes(b"secret")
    os.chmod(str(restricted), 0o000)

    try:
        entries = scan_path(str(synthetic_tree))
        restricted_entry = [e for e in entries if e["filename"] == "restricted.dat"][0]
        assert restricted_entry["error"] is not None
        assert "permission" in restricted_entry["error"].lower() or "denied" in restricted_entry["error"].lower()
    finally:
        os.chmod(str(restricted), 0o644)


def test_find_duplicates(synthetic_tree):
    entries = scan_path(str(synthetic_tree))
    dups = find_duplicates(entries)
    assert len(dups) == 1
    dup_names = {e["filename"] for e in dups[0]}
    assert dup_names == {"copy_a.bin", "copy_b.bin"}


def test_csv_output(synthetic_tree):
    import io
    entries = scan_path(str(synthetic_tree))
    buf = io.StringIO()
    write_csv(entries, buf)
    csv_text = buf.getvalue()
    assert "filename" in csv_text
    assert "sha256" in csv_text
    assert "doc1.pdf" in csv_text


def test_json_output(synthetic_tree):
    import io
    entries = scan_path(str(synthetic_tree))
    buf = io.StringIO()
    write_json(entries, buf)
    data = json.loads(buf.getvalue())
    assert "file_count" in data
    assert data["file_count"] == 6
    assert "absolute_path" not in data["files"][0]


def test_output_outside_tree_enforced(synthetic_tree):
    inside_path = str(synthetic_tree / "output.csv")
    result = main([str(synthetic_tree), "-o", inside_path])
    assert result == 1


def test_main_stdout_csv(synthetic_tree, capsys):
    result = main([str(synthetic_tree)])
    assert result == 0
    captured = capsys.readouterr()
    assert "doc1.pdf" in captured.out


def test_main_stdout_json(synthetic_tree, capsys):
    result = main([str(synthetic_tree), "--json"])
    assert result == 0
    captured = capsys.readouterr()
    data = json.loads(captured.out)
    assert data["file_count"] == 6


def test_main_with_output_file(synthetic_tree):
    with tempfile.TemporaryDirectory() as out_dir:
        out = os.path.join(out_dir, "inventory.csv")
        result = main([str(synthetic_tree), "-o", out])
        assert result == 0
        assert os.path.exists(out)
        content = open(out).read()
        assert "doc1.pdf" in content


def test_main_duplicates_flag(synthetic_tree, capsys):
    result = main([str(synthetic_tree), "--duplicates"])
    assert result == 0
    captured = capsys.readouterr()
    assert "duplicate" in captured.err.lower() or "copy_a.bin" in captured.err


def test_empty_directory(tmp_path):
    entries = scan_path(str(tmp_path))
    assert entries == []


def test_nonexistent_directory():
    result = main(["/nonexistent/path/abc123"])
    assert result == 1
