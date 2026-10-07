"""
Citadel Intake V1 — shared core library.

Stdlib-only (no pip installs, no Homebrew). Everything here is designed to
run identically in a test sandbox and on the target Mac: all paths are
parameterized through CitadelConfig / --root, nothing hardcodes
/Users/graveddiessd.

Integrity model:
  - Originals are hashed immediately on intake and NEVER edited afterward.
  - A working copy is a separate file; only it may ever be modified.
  - chmod 0o444 on an original is a speed bump, not real immutability —
    anyone with write access to the containing directory (or root) can
    still remove/replace it. True immutability would need something like
    a separate read-only volume, an append-only attribute, or object-lock
    storage, none of which this V1 sets up.
  - Any hash mismatch on verify becomes INTEGRITY_ALERT and is recorded;
    nothing is ever silently repaired or replaced.
"""

import hashlib
import json
import mimetypes
import os
import shutil
import socket
import sqlite3
import sys
import time
from contextlib import contextmanager
from datetime import datetime, timezone

SCHEMA_VERSION = 1
MIN_FREE_GIB_DEFAULT = 5.0
EVIDENCE_TYPES = {
    "photo", "video", "audio", "document", "screenshot", "text", "other",
}
EVENT_DATE_PRECISIONS = {"exact", "day", "month", "year", "unknown"}

ADAPTER_TYPES = [
    "IMAGE_OCR",
    "PDF_OCR",
    "AUDIO_TRANSCRIPTION",
    "VIDEO_TRANSCRIPTION",
    "METADATA_EXTRACTION",
]

# mime-type prefix/exact matches -> adapters that apply to this evidence
ADAPTER_ROUTING = {
    "IMAGE_OCR": lambda mime: mime.startswith("image/"),
    "PDF_OCR": lambda mime: mime == "application/pdf",
    "AUDIO_TRANSCRIPTION": lambda mime: mime.startswith("audio/"),
    "VIDEO_TRANSCRIPTION": lambda mime: mime.startswith("video/"),
    "METADATA_EXTRACTION": lambda mime: True,  # always applicable
}


def utcnow_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


class IntegrityAlert(Exception):
    """Raised when a hash mismatch is detected. Never caught-and-repaired."""


class CitadelConfig:
    """
    Resolves the Citadel root directory and tunable settings.

    Resolution order: --root CLI flag > $CITADEL_ROOT env var >
    config/config.json 'root' key > ~/Citadel default.

    This file deliberately does NOT create storage directories as a side
    effect of import — directory creation only happens inside
    ensure_layout(), which is itself gated by the live disk-space check.
    """

    def __init__(self, root=None, config_path=None):
        self.repo_config_dir = os.path.dirname(os.path.abspath(__file__)).replace(
            "/lib", "/config"
        )
        self.config_path = config_path or os.path.join(
            self.repo_config_dir, "config.json"
        )
        self._file_config = self._load_file_config()

        self.root = os.path.abspath(
            os.path.expanduser(
                root
                or os.environ.get("CITADEL_ROOT")
                or self._file_config.get("root")
                or "~/Citadel"
            )
        )
        self.min_free_gib = float(
            self._file_config.get("min_free_gib", MIN_FREE_GIB_DEFAULT)
        )

    def _load_file_config(self):
        if os.path.exists(self.config_path):
            with open(self.config_path, "r") as f:
                return json.load(f)
        return {}

    # Subdirectories per the CITADEL INTAKE V1 architecture spec.
    SUBDIRS = [
        "bin",
        "config",
        "tests",
        "docs",
        "00_INBOX",
        "01_ORIGINALS",
        "02_WORKING_COPIES",
        "03_METADATA",
        "04_PROCESSING_QUEUE",
        "05_INDEX",
        "06_LOGS",
    ]

    STORAGE_SUBDIRS = [
        "00_INBOX",
        "01_ORIGINALS",
        "02_WORKING_COPIES",
        "03_METADATA",
        "04_PROCESSING_QUEUE",
        "05_INDEX",
        "06_LOGS",
    ]

    def path(self, *parts):
        return os.path.join(self.root, *parts)

    @property
    def db_path(self):
        return self.path("05_INDEX", "citadel.db")

    @property
    def intake_log_path(self):
        return self.path("06_LOGS", "intake.log")


def free_space_gib(path):
    """Free space (GiB) on the filesystem containing `path`.

    Walks up to an existing ancestor directory if `path` itself doesn't
    exist yet, so this can be called before the Citadel root is created.
    """
    probe = path
    while not os.path.exists(probe):
        parent = os.path.dirname(probe)
        if parent == probe:
            break
        probe = parent
    usage = shutil.disk_usage(probe)
    return usage.free / (1024 ** 3)


def check_disk_safety_gate(config: CitadelConfig):
    """
    HARD SAFETY GATE: refuse to proceed with anything that creates working
    copies, processes evidence, or copies large files if free space on the
    Citadel root's filesystem is below the configured minimum (default 5
    GiB). Returns (ok: bool, free_gib: float, min_gib: float).
    """
    free_gib = free_space_gib(config.root)
    return free_gib >= config.min_free_gib, free_gib, config.min_free_gib


def port_listening(host="127.0.0.1", port=22, timeout=0.5):
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


def which_any(*names):
    for n in names:
        p = shutil.which(n)
        if p:
            return p
    return None


def detect_adapters():
    """
    Returns {adapter_type: {"status": "CONNECTED"|"NOT_CONNECTED", "detail": str}}.

    V1 never installs anything; it only reports what's already present.
    METADATA_EXTRACTION is CONNECTED using only Python's stdlib (size,
    mtime, mime-type guess) — rich EXIF/GPS extraction via exiftool or
    macOS mdls is a separate, optional upgrade noted in `detail`.
    """
    results = {}

    tesseract = which_any("tesseract")
    pdftoppm = which_any("pdftoppm")
    ocrmypdf = which_any("ocrmypdf")
    whisper_bin = which_any("whisper", "whisper-cli", "whisper.cpp", "main")
    ffmpeg_bin = which_any("ffmpeg")
    exiftool = which_any("exiftool")
    mdls = which_any("mdls")

    results["IMAGE_OCR"] = (
        {"status": "CONNECTED", "detail": f"tesseract at {tesseract}"}
        if tesseract
        else {"status": "NOT_CONNECTED", "detail": "tesseract not found on PATH"}
    )

    if ocrmypdf:
        results["PDF_OCR"] = {"status": "CONNECTED", "detail": f"ocrmypdf at {ocrmypdf}"}
    elif tesseract and pdftoppm:
        results["PDF_OCR"] = {
            "status": "CONNECTED",
            "detail": f"tesseract+pdftoppm at {tesseract}, {pdftoppm}",
        }
    else:
        results["PDF_OCR"] = {
            "status": "NOT_CONNECTED",
            "detail": "need ocrmypdf, or tesseract+pdftoppm; neither found",
        }

    results["AUDIO_TRANSCRIPTION"] = (
        {"status": "CONNECTED", "detail": f"whisper at {whisper_bin}"}
        if whisper_bin
        else {"status": "NOT_CONNECTED", "detail": "whisper / whisper.cpp not found on PATH"}
    )

    results["VIDEO_TRANSCRIPTION"] = (
        {
            "status": "CONNECTED",
            "detail": f"ffmpeg+whisper at {ffmpeg_bin}, {whisper_bin}",
        }
        if (ffmpeg_bin and whisper_bin)
        else {
            "status": "NOT_CONNECTED",
            "detail": "needs both ffmpeg and whisper; missing: "
            + ", ".join(
                n for n, v in (("ffmpeg", ffmpeg_bin), ("whisper", whisper_bin)) if not v
            ),
        }
    )

    extra = []
    if exiftool:
        extra.append(f"exiftool at {exiftool}")
    if mdls:
        extra.append(f"mdls at {mdls}")
    results["METADATA_EXTRACTION"] = {
        "status": "CONNECTED",
        "detail": "stdlib stat/mimetypes always available"
        + (f"; also: {', '.join(extra)}" if extra else "; exiftool/mdls not found (optional, richer metadata)"),
    }

    return results


def sha256_file(path, chunk_size=1024 * 1024):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def guess_mime(path):
    mime, _ = mimetypes.guess_type(path)
    return mime or "application/octet-stream"


# ---------------------------------------------------------------------------
# SQLite index
# ---------------------------------------------------------------------------

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS schema_meta (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS evidence (
    evidence_id            TEXT PRIMARY KEY,
    original_filename      TEXT NOT NULL,
    source                 TEXT NOT NULL,
    evidence_type          TEXT NOT NULL,
    event_date             TEXT,
    event_date_precision   TEXT,
    acquired_at            TEXT NOT NULL,
    sha256                 TEXT NOT NULL,
    byte_size               INTEGER NOT NULL,
    mime_type               TEXT NOT NULL,
    original_path           TEXT NOT NULL,
    working_copy_path       TEXT NOT NULL,
    processing_status       TEXT NOT NULL,
    ocr_status               TEXT NOT NULL,
    transcription_status    TEXT NOT NULL,
    notes                    TEXT,
    integrity_status         TEXT NOT NULL,
    duplicate_of             TEXT,
    created_at                TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS hashes (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    evidence_id   TEXT NOT NULL REFERENCES evidence(evidence_id),
    sha256        TEXT NOT NULL,
    algo          TEXT NOT NULL DEFAULT 'sha256',
    stage         TEXT NOT NULL,   -- 'intake' | 'verify'
    computed_at   TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS events (
    id                    INTEGER PRIMARY KEY AUTOINCREMENT,
    evidence_id           TEXT NOT NULL REFERENCES evidence(evidence_id),
    event_date            TEXT,
    event_date_precision  TEXT,
    description           TEXT,
    created_at             TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS processing_jobs (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    evidence_id     TEXT NOT NULL REFERENCES evidence(evidence_id),
    job_type        TEXT NOT NULL,   -- IMAGE_OCR / PDF_OCR / AUDIO_TRANSCRIPTION / VIDEO_TRANSCRIPTION / METADATA_EXTRACTION
    status          TEXT NOT NULL,   -- QUEUED / NOT_CONNECTED / RUNNING / DONE / FAILED
    adapter_status  TEXT NOT NULL,   -- CONNECTED / NOT_CONNECTED
    detail          TEXT,
    created_at       TEXT NOT NULL,
    updated_at       TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS audit_log (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    evidence_id   TEXT REFERENCES evidence(evidence_id),
    action        TEXT NOT NULL,
    actor         TEXT NOT NULL,
    timestamp     TEXT NOT NULL,
    detail        TEXT
);

CREATE INDEX IF NOT EXISTS idx_hashes_evidence ON hashes(evidence_id);
CREATE INDEX IF NOT EXISTS idx_jobs_evidence ON processing_jobs(evidence_id);
CREATE INDEX IF NOT EXISTS idx_audit_evidence ON audit_log(evidence_id);
CREATE INDEX IF NOT EXISTS idx_evidence_sha256 ON evidence(sha256);
"""


@contextmanager
def open_db(config: CitadelConfig):
    os.makedirs(os.path.dirname(config.db_path), exist_ok=True)
    conn = sqlite3.connect(config.db_path, isolation_level=None)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    try:
        yield conn
    finally:
        conn.close()


def init_db(config: CitadelConfig):
    with open_db(config) as conn:
        conn.executescript(SCHEMA_SQL)
        conn.execute(
            "INSERT OR IGNORE INTO schema_meta (key, value) VALUES ('schema_version', ?)",
            (str(SCHEMA_VERSION),),
        )


def audit(conn, evidence_id, action, actor, detail=None):
    conn.execute(
        "INSERT INTO audit_log (evidence_id, action, actor, timestamp, detail) "
        "VALUES (?, ?, ?, ?, ?)",
        (evidence_id, action, actor, utcnow_iso(), json.dumps(detail) if detail is not None else None),
    )


def append_intake_log(config: CitadelConfig, record: dict):
    """Append-only JSONL log, independent of the SQLite DB.

    Opened with O_APPEND so writes cannot overwrite prior lines even under
    concurrent access; this is the durable record if the DB is ever lost
    or corrupted. It is not immune to an operator with shell access
    truncating the file — see docs/README.md's immutability caveat.
    """
    os.makedirs(os.path.dirname(config.intake_log_path), exist_ok=True)
    line = json.dumps(record, sort_keys=True) + "\n"
    fd = os.open(config.intake_log_path, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o644)
    try:
        os.write(fd, line.encode("utf-8"))
    finally:
        os.close(fd)


def next_evidence_id(conn, when=None):
    when = when or datetime.now(timezone.utc)
    date_part = when.strftime("%Y%m%d")
    prefix = f"EVD-{date_part}-"
    conn.execute("BEGIN IMMEDIATE")
    try:
        row = conn.execute(
            "SELECT evidence_id FROM evidence WHERE evidence_id LIKE ? ORDER BY evidence_id DESC LIMIT 1",
            (prefix + "%",),
        ).fetchone()
        if row is None:
            seq = 1
        else:
            seq = int(row["evidence_id"].rsplit("-", 1)[-1]) + 1
        evidence_id = f"{prefix}{seq:06d}"
        conn.execute("COMMIT")
        return evidence_id
    except Exception:
        conn.execute("ROLLBACK")
        raise


# ---------------------------------------------------------------------------
# Sidecar JSON
# ---------------------------------------------------------------------------

SIDECAR_FIELDS = [
    "evidence_id",
    "original_filename",
    "source",
    "evidence_type",
    "event_date",
    "event_date_precision",
    "acquired_at",
    "sha256",
    "byte_size",
    "mime_type",
    "original_path",
    "working_copy_path",
    "processing_status",
    "ocr_status",
    "transcription_status",
    "notes",
    "integrity_status",
]


def validate_sidecar(data: dict):
    missing = [f for f in SIDECAR_FIELDS if f not in data]
    if missing:
        raise ValueError(f"sidecar missing required fields: {missing}")
    if data["evidence_type"] not in EVIDENCE_TYPES:
        raise ValueError(f"invalid evidence_type: {data['evidence_type']!r}")
    if data["event_date_precision"] not in EVENT_DATE_PRECISIONS | {None}:
        raise ValueError(f"invalid event_date_precision: {data['event_date_precision']!r}")
    return True


def write_sidecar(config: CitadelConfig, evidence_id, data: dict):
    validate_sidecar(data)
    path = config.path("03_METADATA", f"{evidence_id}.json")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2, sort_keys=True)
        f.write("\n")
    return path


def read_sidecar(config: CitadelConfig, evidence_id):
    path = config.path("03_METADATA", f"{evidence_id}.json")
    with open(path, "r") as f:
        return json.load(f)
