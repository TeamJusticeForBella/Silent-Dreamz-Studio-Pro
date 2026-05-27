# Drive Scan Utility

## Purpose
The `drive_scan.py` tool is a CLI utility designed to safely and recursively scan specified directories or drives, primarily for the purposes of:
- Detecting file access issues without modifying evidence.
- Optionally fixing permissions or backing up files as needed.

### Features:
1. Dry-run mode to ensure no changes are made unless specified.
2. Detects permission issues, file_stat errors, and read failures.
3. Logs timestamped reports to the `~/drive_scan_logs` directory.
4. Defaults to reading files or directories without modification.
5. Verify backups using `hash functionality`.