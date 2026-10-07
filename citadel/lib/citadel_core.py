"""
Citadel Intake V1.1 — shared core library.

Stdlib-only (no pip installs, no Homebrew). Everything here is designed to
run identically in a test sandbox and on the target Mac: all paths are
parameterized through CitadelConfig / --root, nothing hardcodes
/Users/graveddiessd.

V1.1 changelog (independent-review remediation; see docs/README.md for
the full writeup of each item):
  1. Evidence-ID minting and the evidence row INSERT now happen inside the
     *same* BEGIN IMMEDIATE transaction (reserve_evidence()), closing the
     race window where two concurrent intakes could mint the same ID.
  2. open_db_readonly() opens the DB with SQLite's `mode=ro` URI flag and
     raises FileNotFoundError if the DB file doesn't exist yet — used only
     by citadel-status, which must make zero filesystem/DB mutations.
  3. The intake sidecar (<id>.intake.json) is written once, chmod 0o444,
     and write_intake_sidecar() refuses to overwrite it. Verification
     results go to separate verification/<id>.VERIFY-<ts>.json records.
  4. citadel-intake takes a --min-free-gib override so the real CLI gate
     (not just the core function) can be driven from a test.
  5. The evidence table carries an explicit intake_state column
     (RESERVED/COPYING/HASHING/ORIGINAL_VERIFIED/WORKING_COPY_CREATED/
     INDEXED/QUEUED/COMPLETE/FAILED) and citadel-intake stages the original
     through a .tmp-<id> file, promoted to its final name only via an
     atomic os.replace() after the copy's hash is verified. A finalized
     original is never deleted by any failure path.
  6. Source-mutation detection: size+mtime (and a full hash) are captured
     before the acquisition window and re-checked after the copy; a
     mismatch aborts as SOURCE_CHANGED_DURING_INTAKE rather than
     certifying an ambiguous acquisition.
  7. sanitize_filename()/assert_within_root() harden on-disk paths against
     unicode/length/separator abuse while the full original filename is
     still preserved verbatim in the sidecar/DB for provenance.
  8. open_db() sets documented PRAGMAs (see below).
  9. The JSONL intake log is now a hash chain (previous_entry_hash /
     entry_hash per line), verified by bin/citadel-audit-verify. This is
     tamper-evident, not tamper-proof — see that script's docstring.

SQLite PRAGMA choices (open_db(), read-write connections only):
  - foreign_keys = ON       : audit_log/hashes/events/processing_jobs rows
                               can't dangle from a nonexistent evidence_id.
  - journal_mode = WAL      : lets citadel-status's read-only connections
                               run concurrently with an in-progress intake
                               write, instead of blocking on it.
  - synchronous = FULL      : intake volume is low and human-paced (one
                               phone upload at a time); we trade write
                               throughput for the strongest durability
                               guarantee against power loss / crash
                               corruption, since this is evidence data.
  - busy_timeout = 5000     : a second writer waits up to 5s for the first
                               writer's BEGIN IMMEDIATE to commit instead of
                               failing immediately with "database is locked".

Integrity model:
  - Originals are hashed immediately on intake and NEVER edited afterward.
  - A working copy is a separate file; only it may ever be modified.
  - chmod 0o444 on an original (and on the frozen intake sidecar) is a
    speed bump, not real immutability — anyone with write access to the
    containing directory (or root) can still remove/replace it. True
    immutability would need something like a separate read-only volume,
    an append-only filesystem attribute, or object-lock storage, none of
    which this V1.1 sets up.
  - Any hash mismatch on verify becomes INTEGRITY_ALERT and is recorded;
    nothing is ever silently repaired or replaced.
"""

import errno
import fcntl
import hashlib
import json
import mimetypes
import os
import re
import shutil
import socket
import sqlite3
import sys
import time
import unicodedata
from contextlib import contextmanager
from datetime import datetime, timezone
from urllib.parse import quote

SCHEMA_VERSION = 2
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

ADAPTER_ROUTING = {
    "IMAGE_OCR": lambda mime: mime.startswith("image/"),
    "PDF_OCR": lambda mime: mime == "application/pdf",
    "AUDIO_TRANSCRIPTION": lambda mime: mime.startswith("audio/"),
    "VIDEO_TRANSCRIPTION": lambda mime: mime.startswith("video/"),
    "METADATA_EXTRACTION": lambda mime: True,
}

# Acquisition pipeline states, in order. FAILED can be reached from any of
# them. COMPLETE is the only "safe to trust this evidence" terminal state.
INTAKE_STATES = [
    "RESERVED", "COPYING", "HASHING", "ORIGINAL_VERIFIED",
    "WORKING_COPY_CREATED", "INDEXED", "QUEUED", "COMPLETE", "FAILED",
]

GENESIS_HASH = "0" * 64

# Test-only fault injection. Unset (the default, including real Mac use)
# makes maybe_inject_fault() a complete no-op. Never gate real behavior on
# this — it exists solely so the test suite can exercise failure paths
# (copy failure, disk-full, sidecar write failure, DB write failure)
# without actually filling the disk or corrupting SQLite.
FAULT_ENV_VAR = "CITADEL_TEST_FAULT"


def utcnow_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


def maybe_inject_fault(name, exc=None):
    if os.environ.get(FAULT_ENV_VAR) == name:
        raise exc if exc is not None else RuntimeError(f"INJECTED_TEST_FAULT:{name}")


def disk_full_error():
    return OSError(errno.ENOSPC, "No space left on device (injected test fault)")


class CitadelConfig:
    """
    Resolves the Citadel root directory and tunable settings.

    Resolution order: --root CLI flag > $CITADEL_ROOT env var >
    config/config.json 'root' key > ~/Citadel default.

    Importing/constructing this never creates directories — that only
    happens where the code explicitly needs to (gated by the disk safety
    check in citadel-intake); citadel-status must create nothing at all.
    """

    def __init__(self, root=None, config_path=None, min_free_gib=None):
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
            min_free_gib
            if min_free_gib is not None
            else self._file_config.get("min_free_gib", MIN_FREE_GIB_DEFAULT)
        )

    def _load_file_config(self):
        if os.path.exists(self.config_path):
            with open(self.config_path, "r") as f:
                return json.load(f)
        return {}

    SUBDIRS = [
        "bin", "config", "tests", "docs",
        "00_INBOX", "01_ORIGINALS", "02_WORKING_COPIES", "03_METADATA",
        "04_PROCESSING_QUEUE", "05_INDEX", "06_LOGS",
    ]

    STORAGE_SUBDIRS = [
        "00_INBOX", "01_ORIGINALS", "02_WORKING_COPIES", "03_METADATA",
        "04_PROCESSING_QUEUE", "05_INDEX", "06_LOGS",
    ]

    def path(self, *parts):
        return os.path.join(self.root, *parts)

    @property
    def db_path(self):
        return self.path("05_INDEX", "citadel.db")

    @property
    def intake_log_path(self):
        return self.path("06_LOGS", "intake.log")


def assert_within_root(config: "CitadelConfig", path):
    """Defense in depth: every path we're about to write must resolve
    under the configured root. evidence_id is server-minted and
    sanitize_filename() strips separators, so this should never trip —
    but it's cheap insurance against a future regression."""
    root_real = os.path.realpath(config.root)
    path_real = os.path.realpath(path)
    if os.path.commonpath([root_real, path_real]) != root_real:
        raise ValueError(f"refusing to write outside Citadel root: {path}")
    return path


_UNSAFE_CHARS = re.compile(r"[\x00-\x1f/\\]")


def sanitize_filename(name, max_bytes=180):
    """
    Returns a filesystem-safe version of `name` for use ON DISK ONLY.
    The *real* original filename (any length, any unicode) is still kept
    verbatim in the sidecar/DB for provenance — this function only
    protects the literal path citadel-intake writes to.

    Strips path separators and control characters, replaces empty/"."/".."
    results with "unnamed", normalizes unicode (NFC) so visually-identical
    names don't silently collide or fail differently across filesystems,
    and truncates to fit common filesystem name-length limits while
    preserving the extension where possible.
    """
    name = os.path.basename(name or "")
    name = unicodedata.normalize("NFC", name)
    name = _UNSAFE_CHARS.sub("_", name)
    name = name.strip()
    if name in ("", ".", ".."):
        name = "unnamed"

    encoded = name.encode("utf-8", errors="surrogatepass")
    if len(encoded) > max_bytes:
        root, ext = os.path.splitext(name)
        ext_bytes = ext.encode("utf-8", errors="surrogatepass")
        budget = max(max_bytes - len(ext_bytes), 1)
        root_bytes = root.encode("utf-8", errors="surrogatepass")[:budget]
        root = root_bytes.decode("utf-8", errors="ignore")
        name = (root or "unnamed") + ext
    return name


def free_space_gib(path):
    probe = path
    while not os.path.exists(probe):
        parent = os.path.dirname(probe)
        if parent == probe:
            break
        probe = parent
    usage = shutil.disk_usage(probe)
    return usage.free / (1024 ** 3)


def check_disk_safety_gate(config: CitadelConfig):
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
        {"status": "CONNECTED", "detail": f"ffmpeg+whisper at {ffmpeg_bin}, {whisper_bin}"}
        if (ffmpeg_bin and whisper_bin)
        else {
            "status": "NOT_CONNECTED",
            "detail": "needs both ffmpeg and whisper; missing: "
            + ", ".join(n for n, v in (("ffmpeg", ffmpeg_bin), ("whisper", whisper_bin)) if not v),
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
    intake_state             TEXT NOT NULL DEFAULT 'RESERVED',
    duplicate_of             TEXT,
    created_at                TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS hashes (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    evidence_id   TEXT NOT NULL REFERENCES evidence(evidence_id),
    sha256        TEXT NOT NULL,
    algo          TEXT NOT NULL DEFAULT 'sha256',
    stage         TEXT NOT NULL,
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
    job_type        TEXT NOT NULL,
    status          TEXT NOT NULL,
    adapter_status  TEXT NOT NULL,
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


def _set_wal_mode_with_retry(conn, attempts=50, delay=0.05):
    """
    PRAGMA journal_mode=WAL switches the database's on-disk journal
    format and needs exclusive access to do so. On some platforms this
    can raise "database is locked" immediately rather than honoring
    busy_timeout, particularly when several processes race to flip a
    brand-new database into WAL mode for the first time — exactly what
    happens when several citadel-intake processes start concurrently
    against a --root that doesn't have a DB yet. Rather than fail an
    entire intake over a one-time mode switch every process is trying to
    set to the same value anyway, retry briefly.
    """
    last_exc = None
    for _ in range(attempts):
        try:
            conn.execute("PRAGMA journal_mode = WAL;")
            return
        except sqlite3.OperationalError as e:
            if "locked" not in str(e).lower():
                raise
            last_exc = e
            time.sleep(delay)
    raise last_exc


@contextmanager
def open_db(config: CitadelConfig):
    """Read-write connection. See module docstring for the PRAGMA choices."""
    os.makedirs(os.path.dirname(config.db_path), exist_ok=True)
    conn = sqlite3.connect(config.db_path, isolation_level=None, timeout=5.0)
    conn.row_factory = sqlite3.Row
    # busy_timeout FIRST: every statement after this — including the WAL
    # mode switch below — gets SQLite's busy-retry behavior instead of
    # failing instantly on "database is locked".
    conn.execute("PRAGMA busy_timeout = 5000;")
    conn.execute("PRAGMA foreign_keys = ON;")
    _set_wal_mode_with_retry(conn)
    conn.execute("PRAGMA synchronous = FULL;")
    try:
        yield conn
    finally:
        conn.close()


@contextmanager
def open_db_readonly(config: CitadelConfig):
    """
    Strictly read-only connection for citadel-status. Never creates the DB,
    never creates 05_INDEX/, never runs DDL, and — because it's opened
    with `immutable=1` in addition to `mode=ro` — never creates or
    touches a WAL database's `-shm`/`-wal` companion files either.
    Raises FileNotFoundError if the DB doesn't exist yet so the caller
    can report NOT_INITIALIZED instead of silently provisioning one.

    Why `immutable=1` specifically: open_db() runs in WAL mode (see its
    docstring) precisely so a read-only connection doesn't block on a
    concurrent writer. But a *plain* `mode=ro` connection to a WAL
    database still has to create a `-shm` shared-memory index file the
    first time it opens — WAL readers need it to safely locate valid
    frames — and, having opened read-only, it can't check pointing-clean
    it up on close either (checkpointing is itself a write). That's
    exactly the mutation citadel-status must never cause. `immutable=1`
    tells SQLite to skip the WAL/locking machinery entirely and read only
    the main .db file's last-checkpointed contents, at the cost of
    possibly showing a view that's a moment stale if a write is
    mid-transaction (uncheckpointed) at the exact instant citadel-status
    runs. For a read-only status/dashboard tool that's the right
    trade — a stale count is harmless; a status check that creates files
    or blocks a writer is not.
    """
    if not os.path.exists(config.db_path):
        raise FileNotFoundError(config.db_path)
    uri = f"file:{quote(config.db_path, safe='/')}?mode=ro&immutable=1"
    conn = sqlite3.connect(uri, uri=True, timeout=5.0)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def init_db(config: CitadelConfig):
    """Creates the schema if needed. Never call this from citadel-status."""
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


def _mint_id_locked(conn, when=None):
    """
    Computes the next EVD-YYYYMMDD-NNNNNN id. MUST be called with the
    connection already inside a `BEGIN IMMEDIATE` transaction, and the
    caller MUST INSERT the evidence row before committing that same
    transaction — that's what makes allocation atomic. This function
    does not open or close any transaction itself.
    """
    when = when or datetime.now(timezone.utc)
    date_part = when.strftime("%Y%m%d")
    prefix = f"EVD-{date_part}-"
    row = conn.execute(
        "SELECT evidence_id FROM evidence WHERE evidence_id LIKE ? ORDER BY evidence_id DESC LIMIT 1",
        (prefix + "%",),
    ).fetchone()
    seq = 1 if row is None else int(row["evidence_id"].rsplit("-", 1)[-1]) + 1
    return f"{prefix}{seq:06d}"


def reserve_evidence(conn, config: "CitadelConfig", fs_safe_filename, fields: dict):
    """
    Atomically mints a fresh evidence_id, derives its on-disk paths, and
    inserts the initial evidence row (intake_state='RESERVED') — all in a
    single BEGIN IMMEDIATE transaction. This is the fix for the V1 race:
    previously the ID was minted and committed *before* the row existed,
    leaving a window where two concurrent intakes could compute the same
    next-sequence number (and, had it existed, a second window where the
    row existed with placeholder paths). Now minting, path derivation,
    and the INSERT that claims them all happen under the same write lock,
    so a second writer blocked on BEGIN IMMEDIATE always sees the first
    writer's committed row before computing its own next id — there is no
    gap in which an id or a path exists without its row, or vice versa.

    `fields` must contain every evidence column except evidence_id,
    intake_state, original_path, and working_copy_path (computed here).
    Returns (evidence_id, duplicate_of, original_path, working_copy_path).
    """
    conn.execute("BEGIN IMMEDIATE")
    try:
        dup_row = conn.execute(
            "SELECT evidence_id FROM evidence WHERE sha256 = ? ORDER BY created_at ASC LIMIT 1",
            (fields["sha256"],),
        ).fetchone()
        duplicate_of = dup_row["evidence_id"] if dup_row else None

        evidence_id = _mint_id_locked(conn)
        original_path = config.path("01_ORIGINALS", f"{evidence_id}_{fs_safe_filename}")
        working_copy_path = config.path("02_WORKING_COPIES", f"{evidence_id}_{fs_safe_filename}")
        assert_within_root(config, original_path)
        assert_within_root(config, working_copy_path)

        conn.execute(
            """INSERT INTO evidence (
                evidence_id, original_filename, source, evidence_type, event_date,
                event_date_precision, acquired_at, sha256, byte_size, mime_type,
                original_path, working_copy_path, processing_status, ocr_status,
                transcription_status, notes, integrity_status, intake_state,
                duplicate_of, created_at
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (
                evidence_id, fields["original_filename"], fields["source"], fields["evidence_type"],
                fields["event_date"], fields["event_date_precision"], fields["acquired_at"],
                fields["sha256"], fields["byte_size"], fields["mime_type"],
                original_path, working_copy_path,
                "RESERVED", "NOT_STARTED", "NOT_STARTED", fields["notes"],
                "PENDING", "RESERVED", duplicate_of, fields["acquired_at"],
            ),
        )
        audit(conn, evidence_id, "RESERVED", fields.get("actor", "citadel-intake"),
              {"duplicate_of": duplicate_of})
        conn.execute("COMMIT")
        return evidence_id, duplicate_of, original_path, working_copy_path
    except Exception:
        conn.execute("ROLLBACK")
        raise


def advance_state(config: CitadelConfig, evidence_id, state, actor, extra_columns=None, detail=None):
    """Opens its own short-lived autocommit connection, updates
    intake_state (plus any extra_columns), and writes one audit_log row
    whose action is the state name. Each call is its own transaction so a
    crash between states leaves the last successfully-reached state
    visible rather than an all-or-nothing blob."""
    if state not in INTAKE_STATES:
        raise ValueError(f"unknown intake state: {state}")
    with open_db(config) as conn:
        set_clauses = ["intake_state = ?"]
        params = [state]
        for col, val in (extra_columns or {}).items():
            set_clauses.append(f"{col} = ?")
            params.append(val)
        params.append(evidence_id)
        conn.execute(
            f"UPDATE evidence SET {', '.join(set_clauses)} WHERE evidence_id = ?",
            params,
        )
        audit(conn, evidence_id, state, actor, detail)


# ---------------------------------------------------------------------------
# Sidecar JSON (frozen at intake) + separate verification records
# ---------------------------------------------------------------------------

SIDECAR_FIELDS = [
    "evidence_id", "original_filename", "source", "evidence_type", "event_date",
    "event_date_precision", "acquired_at", "sha256", "byte_size", "mime_type",
    "original_path", "working_copy_path", "processing_status", "ocr_status",
    "transcription_status", "notes", "integrity_status",
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


def intake_sidecar_path(config: CitadelConfig, evidence_id):
    return config.path("03_METADATA", f"{evidence_id}.intake.json")


def write_intake_sidecar(config: CitadelConfig, evidence_id, data: dict):
    """
    Writes the ONE sidecar for this evidence item. This is historical
    provenance, frozen at intake time: refuses to run if the file already
    exists, and chmod 0o444s it afterward. citadel-verify must never call
    this — use write_verification_record() for verification results.
    """
    validate_sidecar(data)
    path = intake_sidecar_path(config, evidence_id)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if os.path.exists(path):
        raise FileExistsError(f"intake sidecar already exists and is frozen: {path}")
    with open(path, "w") as f:
        json.dump(data, f, indent=2, sort_keys=True)
        f.write("\n")
    try:
        os.chmod(path, 0o444)
    except OSError:
        pass
    return path


def read_intake_sidecar(config: CitadelConfig, evidence_id):
    with open(intake_sidecar_path(config, evidence_id), "r") as f:
        return json.load(f)


def write_verification_record(config: CitadelConfig, evidence_id, record: dict):
    """Appends a new, separate verification-result file; never touches
    the intake sidecar. Filenames include microsecond precision plus a
    short random suffix so rapid repeated verifies (as in a tight test
    loop) can never collide and silently overwrite one another."""
    vdir = config.path("03_METADATA", "verification")
    os.makedirs(vdir, exist_ok=True)
    ts = record.get("verified_at", utcnow_iso())
    ts_safe = ts.replace(":", "").replace(".", "")
    suffix = os.urandom(4).hex()
    path = os.path.join(vdir, f"{evidence_id}.VERIFY-{ts_safe}-{suffix}.json")
    with open(path, "w") as f:
        json.dump(record, f, indent=2, sort_keys=True)
        f.write("\n")
    return path


# ---------------------------------------------------------------------------
# Chained, append-only intake log
# ---------------------------------------------------------------------------

def _canonical_json(d: dict) -> bytes:
    return json.dumps(d, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _read_last_entry_hash(log_path):
    if not os.path.exists(log_path):
        return GENESIS_HASH
    last = None
    with open(log_path, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                last = line
    if last is None:
        return GENESIS_HASH
    rec = json.loads(last)
    return rec.get("entry_hash", GENESIS_HASH)


def append_chained_log(config: CitadelConfig, record: dict):
    """
    Appends one hash-chained line to 06_LOGS/intake.log.

    Each record gets `previous_entry_hash` (the prior line's entry_hash,
    or GENESIS_HASH for the first line) and `entry_hash` = SHA-256 of the
    canonical JSON of the record (including previous_entry_hash, excluding
    entry_hash itself). An flock() on a sibling .lock file serializes the
    read-last-hash + append-new-line sequence across concurrent processes,
    so concurrent intakes can't fork the chain.

    This is tamper-EVIDENT, not tamper-proof: anyone with filesystem write
    access to intake.log (including this same user account, including
    root) can rewrite the entire file from scratch with a fresh,
    internally-consistent chain. There's no external anchor (timestamping
    authority, separate ledger, write-once media) and no protection
    against an attacker who rewrites entries before anyone ever runs
    citadel-audit-verify. It only catches accidental or naive tampering —
    see bin/citadel-audit-verify's own docstring for the same caveat in
    the place an operator is most likely to read it.
    """
    os.makedirs(os.path.dirname(config.intake_log_path), exist_ok=True)
    lock_path = config.intake_log_path + ".lock"
    lock_fd = os.open(lock_path, os.O_CREAT | os.O_RDWR, 0o644)
    try:
        fcntl.flock(lock_fd, fcntl.LOCK_EX)
        try:
            prev_hash = _read_last_entry_hash(config.intake_log_path)
            record = dict(record)
            record["previous_entry_hash"] = prev_hash
            entry_hash = hashlib.sha256(_canonical_json(record)).hexdigest()
            record["entry_hash"] = entry_hash
            line = json.dumps(record, sort_keys=True) + "\n"
            fd = os.open(config.intake_log_path, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o644)
            try:
                os.write(fd, line.encode("utf-8"))
            finally:
                os.close(fd)
            return entry_hash
        finally:
            fcntl.flock(lock_fd, fcntl.LOCK_UN)
    finally:
        os.close(lock_fd)


def verify_chain(log_path):
    """
    Walks the chained log and recomputes/validates every entry_hash and
    previous_entry_hash link. Returns a dict:
      {"status": "NO_LOG"} — file doesn't exist (nothing to verify)
      {"status": "OK", "entries": N}
      {"status": "BROKEN", "broken_at_line": i, "reason": ..., "evidence_id": ...}
    Stops at the FIRST broken record — does not try to resynchronize.
    """
    if not os.path.exists(log_path):
        return {"status": "NO_LOG", "entries": 0}

    prev = GENESIS_HASH
    idx = 0
    with open(log_path, "r") as f:
        for raw_line in f:
            raw_line = raw_line.strip()
            if not raw_line:
                continue
            idx += 1
            try:
                rec = json.loads(raw_line)
            except json.JSONDecodeError:
                return {"status": "BROKEN", "broken_at_line": idx, "reason": "invalid_json", "evidence_id": None}

            claimed_entry_hash = rec.get("entry_hash")
            claimed_prev = rec.get("previous_entry_hash")
            check_rec = dict(rec)
            check_rec.pop("entry_hash", None)
            recomputed = hashlib.sha256(_canonical_json(check_rec)).hexdigest()

            if claimed_prev != prev:
                return {
                    "status": "BROKEN", "broken_at_line": idx, "reason": "previous_hash_mismatch",
                    "evidence_id": rec.get("evidence_id"),
                    "expected_previous": prev, "found_previous": claimed_prev,
                }
            if claimed_entry_hash != recomputed:
                return {
                    "status": "BROKEN", "broken_at_line": idx, "reason": "entry_hash_mismatch",
                    "evidence_id": rec.get("evidence_id"),
                }
            prev = claimed_entry_hash

    return {"status": "OK", "entries": idx}
