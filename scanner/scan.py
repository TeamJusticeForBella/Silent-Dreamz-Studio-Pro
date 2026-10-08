#!/usr/bin/env python3
"""Read-only evidence scanner.

Walks one or more directories and produces an inventory of every file:
filename, relative path, size in bytes, mtime, SHA-256 hash, and any
access errors encountered.

GUARANTEES
- Never modifies, copies, renames, or deletes any file.
- Never writes inside the scanned directory tree.
- Output goes to stdout (CSV) or a caller-specified path outside the tree.
- All file handles are opened read-only with os.O_RDONLY.

Usage:
    python -I scanner/scan.py /path/to/evidence
    python -I scanner/scan.py /path/to/evidence -o /tmp/inventory.csv
    python -I scanner/scan.py /path/to/evidence --json -o /tmp/inventory.json
"""
import argparse
import csv
import hashlib
import io
import json
import os
import stat
import sys
from datetime import datetime, timezone
from pathlib import Path


def sha256_file(path: str, block_size: int = 1 << 16) -> str:
    h = hashlib.sha256()
    fd = os.open(path, os.O_RDONLY)
    try:
        while True:
            chunk = os.read(fd, block_size)
            if not chunk:
                break
            h.update(chunk)
    finally:
        os.close(fd)
    return h.hexdigest()


def scan_path(root: str) -> list[dict]:
    root = os.path.abspath(root)
    entries = []

    for dirpath, _dirnames, filenames in os.walk(root):
        for fname in sorted(filenames):
            full = os.path.join(dirpath, fname)
            rel = os.path.relpath(full, root)
            entry = {
                "filename": fname,
                "relative_path": rel,
                "absolute_path": full,
                "size_bytes": None,
                "mtime_utc": None,
                "sha256": None,
                "error": None,
            }
            try:
                st = os.stat(full)
                entry["size_bytes"] = st.st_size
                entry["mtime_utc"] = datetime.fromtimestamp(
                    st.st_mtime, tz=timezone.utc
                ).isoformat()

                if stat.S_ISREG(st.st_mode):
                    entry["sha256"] = sha256_file(full)
                else:
                    entry["error"] = f"not a regular file (mode={oct(st.st_mode)})"
            except PermissionError:
                entry["error"] = "permission denied"
            except OSError as exc:
                entry["error"] = str(exc)

            entries.append(entry)

    return entries


def write_csv(entries: list[dict], out: io.TextIOBase) -> None:
    fields = [
        "filename", "relative_path", "size_bytes",
        "mtime_utc", "sha256", "error",
    ]
    writer = csv.DictWriter(out, fieldnames=fields, extrasaction="ignore")
    writer.writeheader()
    writer.writerows(entries)


def write_json(entries: list[dict], out: io.TextIOBase) -> None:
    clean = []
    for e in entries:
        clean.append({k: v for k, v in e.items() if k != "absolute_path"})
    json.dump({"scan_time_utc": datetime.now(timezone.utc).isoformat(),
               "file_count": len(clean),
               "files": clean}, out, indent=2)
    out.write("\n")


def find_duplicates(entries: list[dict]) -> list[list[dict]]:
    by_hash: dict[str, list[dict]] = {}
    for e in entries:
        h = e.get("sha256")
        if h:
            by_hash.setdefault(h, []).append(e)
    return [group for group in by_hash.values() if len(group) > 1]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Read-only evidence file scanner",
    )
    parser.add_argument(
        "paths", nargs="+",
        help="Directories to scan (read-only)",
    )
    parser.add_argument(
        "-o", "--output",
        help="Output file path (must be outside scanned trees). Default: stdout",
    )
    parser.add_argument(
        "--json", action="store_true", dest="use_json",
        help="Output JSON instead of CSV",
    )
    parser.add_argument(
        "--duplicates", action="store_true",
        help="After scanning, print groups of files sharing a SHA-256",
    )
    args = parser.parse_args(argv)

    all_entries = []
    for p in args.paths:
        p = os.path.abspath(p)
        if not os.path.isdir(p):
            print(f"ERROR: {p} is not a directory", file=sys.stderr)
            return 1
        all_entries.extend(scan_path(p))

    if args.output:
        out_abs = os.path.abspath(args.output)
        for p in args.paths:
            scanned = os.path.abspath(p)
            if out_abs.startswith(scanned + os.sep) or out_abs == scanned:
                print(
                    f"ERROR: output path {args.output} is inside scanned tree {p}",
                    file=sys.stderr,
                )
                return 1
        with open(out_abs, "w", newline="") as f:
            if args.use_json:
                write_json(all_entries, f)
            else:
                write_csv(all_entries, f)
        print(f"Wrote {len(all_entries)} entries to {out_abs}", file=sys.stderr)
    else:
        if args.use_json:
            write_json(all_entries, sys.stdout)
        else:
            write_csv(all_entries, sys.stdout)

    errors = [e for e in all_entries if e["error"]]
    if errors:
        print(f"\n{len(errors)} access error(s):", file=sys.stderr)
        for e in errors:
            print(f"  {e['relative_path']}: {e['error']}", file=sys.stderr)

    if args.duplicates:
        dups = find_duplicates(all_entries)
        if dups:
            print(f"\n{len(dups)} duplicate hash group(s):", file=sys.stderr)
            for group in dups:
                print(f"  SHA-256: {group[0]['sha256']}", file=sys.stderr)
                for e in group:
                    print(f"    {e['relative_path']} ({e['size_bytes']} bytes)", file=sys.stderr)
        else:
            print("\nNo duplicate hashes found.", file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main())
