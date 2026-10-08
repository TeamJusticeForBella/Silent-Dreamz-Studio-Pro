# Read-Only Evidence Scanner

## Purpose

A local, non-deploying CLI tool that inventories files in a directory tree without modifying, copying, renaming, or deleting anything.

**This tool is strictly read-only.** It opens files with `os.O_RDONLY`, never creates output inside the scanned tree, and never alters timestamps.

## What it produces

For each file in the scanned directory:

| Field | Description |
|-------|-------------|
| `filename` | Base filename |
| `relative_path` | Path relative to scan root |
| `size_bytes` | File size |
| `mtime_utc` | Last modification time (UTC ISO-8601) |
| `sha256` | SHA-256 hash of file contents |
| `error` | Access error (permission denied, etc.) or null |

## Usage

```bash
# Scan a directory, output CSV to stdout
python -I scanner/scan.py /path/to/evidence

# Save CSV to a file (must be outside the scanned tree)
python -I scanner/scan.py /path/to/evidence -o /tmp/inventory.csv

# Output JSON instead
python -I scanner/scan.py /path/to/evidence --json -o /tmp/inventory.json

# Show duplicate hash groups
python -I scanner/scan.py /path/to/evidence --duplicates

# Scan multiple directories
python -I scanner/scan.py /path/to/dir1 /path/to/dir2
```

## Safety guarantees

1. All file handles opened read-only (`os.O_RDONLY`)
2. Output path is validated to be **outside** all scanned trees
3. Scanner never creates, modifies, or deletes files in the scanned tree
4. Tests verify mtimes and file counts are unchanged after scanning
5. Permission errors are reported, never bypassed

## Running tests

```bash
python -m pytest scanner/tests/ -v
```

All tests use synthetic fixtures — no real evidence data is referenced.

## Deployment

This branch does **not** deploy. It has no Vercel configuration, no web server, and no public endpoints. The scanner runs locally only.
