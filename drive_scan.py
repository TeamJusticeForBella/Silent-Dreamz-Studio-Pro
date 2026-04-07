import os
import shutil
import stat
from datetime import datetime
from pathlib import Path
import sys

# Safe defaults—don't touch these unless you're sure
EXCLUDE_DIRS = {
    '/System', '/private', '/Library', '/usr', '/bin', '/sbin',
    '/Applications', '/Volumes', '/.Trash', '/.Spotlight-V100',
    '/.fseventsd', '/var', '/tmp', '/dev', '/Network'
}

LOG_DIR = Path.home() / "drive_scan_logs"
BACKUP_DIR = Path.home() / "drive_scan_backups"
LOG_DIR.mkdir(parents=True, exist_ok=True)
BACKUP_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOG_DIR / f"scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"


def log(msg: str) -> None:
    print(msg)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(msg + "\n")


def is_excluded(path: str) -> bool:
    abs_path = os.path.abspath(path)
    return any(
        abs_path == excluded or abs_path.startswith(excluded + os.sep)
        for excluded in EXCLUDE_DIRS
    )


def make_readable(path: str) -> bool:
    try:
        current_mode = os.stat(path).st_mode
        os.chmod(path, current_mode | stat.S_IRUSR)
        return True
    except Exception as e:
        log(f"[!] Could not chmod {path}: {e}")
        return False


def backup_file(src_path: str) -> None:
    try:
        src = Path(src_path)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        dest = BACKUP_DIR / f"{timestamp}_{src.name}"
        shutil.copy2(src, dest)
        log(f"[+] Backed up: {src_path} -> {dest}")
    except Exception as e:
        log(f"[!] Backup failed for {src_path}: {e}")


def test_file_read(path: str) -> tuple[bool, str | None]:
    try:
        with open(path, "rb") as f:
            f.read(1024)
        return True, None
    except Exception as e:
        return False, str(e)


def scan_drive(path: str, try_fix_permissions: bool = False, backup_bad_files: bool = False) -> list[str]:
    issues: list[str] = []
    abs_root = os.path.abspath(path)

    if is_excluded(abs_root):
        msg = f"[!] Refusing to scan excluded path: {abs_root}"
        log(msg)
        return [msg]

    log(f"[+] Scanning: {abs_root}")

    for root, dirs, files in os.walk(abs_root, topdown=True, onerror=None):
        # prune excluded dirs before descending
        dirs[:] = [d for d in dirs if not is_excluded(os.path.join(root, d))]

        for name in files + dirs:
            full = os.path.join(root, name)

            if is_excluded(full):
                log(f"[-] Skipping excluded path: {full}")
                continue

            try:
                try:
                    os.stat(full)
                except Exception as e:
                    msg = f"Stat error: {full} -> {e}"
                    issues.append(msg)
                    log(f"[!] {msg}")
                    continue

                if not os.access(full, os.R_OK):
                    msg = f"Permission denied: {full}"
                    issues.append(msg)
                    log(f"[!] {msg}")

                    if try_fix_permissions:
                        if make_readable(full):
                            log(f"[+] Added user-read permission: {full}")

                if os.path.isfile(full):
                    ok, err = test_file_read(full)
                    if not ok:
                        msg = f"Read error on {full}: {err}"
                        issues.append(msg)
                        log(f"[!] {msg}")

                        if backup_bad_files:
                            backup_file(full)

            except Exception as e:
                msg = f"Unexpected error on {full}: {e}"
                issues.append(msg)
                log(f"[!] {msg}")

    log(f"[+] Scan complete. Total issues: {len(issues)}")
    log(f"[+] Log written to: {LOG_FILE}")
    return issues


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python drive_scan.py /path/to/scan [--fix] [--backup]")
        return 1

    target = sys.argv[1]
    try_fix = "--fix" in sys.argv
    do_backup = "--backup" in sys.argv

    if not os.path.exists(target):
        print(f"[!] Path does not exist: {target}")
        return 1

    issues = scan_drive(
        target,
        try_fix_permissions=try_fix,
        backup_bad_files=do_backup
    )

    print("\n--- SUMMARY ---")
    print(f"Issues found: {len(issues)}")
    print(f"Log file: {LOG_FILE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
