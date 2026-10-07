# Citadel Intake V1

A minimal, local-first evidence intake system. Stdlib-only Python 3 — no
`pip install`, no Homebrew, no cloud services, no AI/model APIs. Everything
runs on the operator's own machine against the operator's own filesystem.

## Important: where this was built vs. where it runs

This code was authored and tested in a cloud Linux sandbox attached to this
git repository — **not** on the target Mac (`iMac.lan`, `/Users/graveddiessd`)
described in the original assignment. That sandbox has no network path to
the real machine, so none of the "inspect this Mac" preflight steps could be
run for real from there. Instead, every host-specific check (free disk
space, port 22, OCR/whisper tool availability) is implemented *inside the
tool itself* (`citadel-status`, and the safety gate inside `citadel-intake`)
so it reports accurately wherever it is actually executed. Pull this onto
the real Mac and run `citadel-status` there to get the real numbers.

## Layout

```
citadel/
  bin/      citadel-intake, citadel-verify, citadel-status (executable, stdlib-only)
  lib/      citadel_core.py — shared schema, hashing, config, adapters
  config/   config.json — root path + min_free_gib threshold
  tests/    unittest suite + synthetic fixture (no real evidence, ever)
  docs/     this file + the iPhone Shortcuts spec
```

At runtime, `citadel-intake` creates the evidence-storage tree under the
configured root (default `~/Citadel`, override with `--root` or
`$CITADEL_ROOT`):

```
<root>/
  00_INBOX/              (reserved for future drop-folder watching; unused by V1)
  01_ORIGINALS/          <evidence_id>_<filename> — chmod 0o444, never edited
  02_WORKING_COPIES/     <evidence_id>_<filename> — mutable, used by processing
  03_METADATA/           <evidence_id>.json sidecars
  04_PROCESSING_QUEUE/   (reserved; job state currently lives in the DB)
  05_INDEX/              citadel.db (SQLite)
  06_LOGS/               intake.log (append-only JSONL)
```

These directories are **not** created until the first successful
`citadel-intake` run clears the disk safety gate — nothing is pre-created
speculatively, so a low-disk machine never gets a half-built evidence tree.

## The disk safety gate

Before copying anything, `citadel-intake` calls
`citadel_core.check_disk_safety_gate()`, which checks free space on the
filesystem containing the configured root. If free space is below
`min_free_gib` (default 5 GiB, set in `config/config.json`), intake refuses
immediately — no directories created, no files copied, no DB writes. It
prints a JSON error with the actual free/required numbers instead.

This gate does **not** try to free space, delete anything, or prompt for
cleanup. That is a human decision.

## Evidence ID format

`EVD-YYYYMMDD-NNNNNN` — date of intake, then a 6-digit sequence scoped to
that day, minted inside a `BEGIN IMMEDIATE` SQLite transaction so concurrent
intakes can't collide.

## Integrity model (read this before trusting any "protected" claim)

- The original is hashed (SHA-256) **before** it is copied, then rehashed
  **immediately after** the copy. If those two hashes don't match, the
  intake aborts, the evidence row is marked `INTEGRITY_ALERT` /
  `processing_status=FAILED`, and nothing is silently retried or repaired.
- A separate working copy is made from the original. Only the working copy
  is ever touched by OCR/transcription/etc. The original is never opened
  for writing again by this toolchain.
- `citadel-verify` rehashes the original and compares against the hash
  recorded at intake. A mismatch becomes `INTEGRITY_ALERT` — recorded in
  the `evidence` table, the sidecar JSON, and `audit_log`. **Nothing is ever
  auto-repaired or auto-replaced.** A human has to look at it.
- **`chmod 0o444` on an original is NOT true immutability.** It's a speed
  bump against accidental overwrites by this toolchain and ordinary
  non-root processes. Anyone with write access to the containing directory,
  or root, can still delete or replace the file; chmod does not survive a
  `cp --preserve` style overwrite of the parent dir, and it offers no
  protection at all against disk failure, filesystem corruption, or a
  malicious actor with sufficient privilege. If you need real immutability,
  that means a separate read-only volume, an append-only/immutable
  filesystem attribute (e.g. macOS `chflags uchg`, which *is* stronger than
  chmod but still root-overridable), or object-lock storage — none of which
  V1 sets up, and all of which are a deliberate, separate decision to make
  later.
- Duplicate detection is by content hash, not filename: a second intake of
  bytes identical to an existing evidence item still gets its own new
  `evidence_id` (so chain-of-custody for *that specific submission event* is
  preserved — who sent it, when, with what notes) but is flagged
  `duplicate_of: <earlier evidence_id>` rather than silently merged or
  rejected.

## SQLite schema

Five tables, all in `05_INDEX/citadel.db`:

- **evidence** — one row per intake; the sidecar JSON's fields plus
  `duplicate_of` and `created_at`.
- **hashes** — every hash ever computed for an evidence item, tagged
  `stage` (`intake` or `verify`), so the full hash history survives even
  across repeated verifications.
- **events** — the real-world event metadata (event_date/precision/notes)
  tied to each evidence item; separate from `audit_log`, which is system
  actions, not case facts.
- **processing_jobs** — one row per adapter type that applies to a given
  evidence item's MIME type, carrying `status` and `adapter_status`
  (`CONNECTED`/`NOT_CONNECTED`).
- **audit_log** — append-via-INSERT-only; every state-changing operation
  (`ORIGINAL_COPIED`, `HASH_ORIGINAL`, `WORKING_COPY_CREATED`,
  `SIDECAR_WRITTEN`, `PROCESSING_JOBS_QUEUED`, `VERIFY_OK`,
  `INTEGRITY_ALERT`, `DUPLICATE_DETECTED`, ...) writes one row here.
  Nothing in this codebase issues `UPDATE` or `DELETE` against `audit_log`.

There is also `06_LOGS/intake.log` — an independent, append-only JSONL log
(file opened with `O_APPEND`) of every intake, so the record survives even
if `citadel.db` is ever lost or corrupted. It is not immune to an operator
with shell access truncating the file; it's a second line of defense, not a
cryptographic ledger.

## Sidecar JSON

One `<evidence_id>.json` per item in `03_METADATA/`, with exactly these
fields (see `citadel_core.SIDECAR_FIELDS` / `validate_sidecar()`):

```
evidence_id, original_filename, source, evidence_type, event_date,
event_date_precision, acquired_at, sha256, byte_size, mime_type,
original_path, working_copy_path, processing_status, ocr_status,
transcription_status, notes, integrity_status
```

## Processing queue adapters (V1: interfaces only, nothing executes)

`citadel_core.detect_adapters()` checks for already-installed tools on
`PATH` and reports `CONNECTED` or `NOT_CONNECTED` — **it never installs
anything**:

| Adapter | Needs | 
|---|---|
| `IMAGE_OCR` | `tesseract` |
| `PDF_OCR` | `ocrmypdf`, or `tesseract` + `pdftoppm` |
| `AUDIO_TRANSCRIPTION` | `whisper` or `whisper.cpp` binary |
| `VIDEO_TRANSCRIPTION` | `ffmpeg` + a whisper binary |
| `METADATA_EXTRACTION` | nothing extra — Python stdlib (`os.stat`, `mimetypes`) always covers basic size/mtime/mime; `exiftool`/macOS `mdls` are optional upgrades for rich EXIF/GPS data |

`citadel-intake` queues a `processing_jobs` row per applicable adapter for
each new evidence item (routed by MIME type), with `status=QUEUED` if the
adapter is connected or `status=NOT_CONNECTED` if not. No OCR or
transcription is ever actually run against real evidence by V1 — these are
queue placeholders for a future phase.

## Privacy

No evidence leaves the machine this runs on. No OpenAI/Anthropic/Gemini
API calls, no Dropbox/Google Drive/iCloud, no telemetry, no public server.
Everything is local files + a local SQLite database.

## JASON GATE

This toolchain never deletes, overwrites, publishes, exposes, moves,
renames, or modifies an existing evidence file without explicit human
approval. `citadel-intake` only ever *creates* new files under fresh
`evidence_id`s; `citadel-verify` only ever *reads* originals and *updates
status fields* (never file bytes); nothing here has a delete/move/rename
code path for anything in `01_ORIGINALS/`.

## CLI reference

```
citadel-intake <file> --source "..." --evidence-type {photo,video,audio,document,screenshot,text,other} \
    [--event-date YYYY-MM-DD] [--event-date-precision {exact,day,month,year,unknown}] \
    [--notes "..."] [--root /path]
  -> prints JSON receipt: {evidence_id, sha256, integrity_status, queue_status, duplicate_of}

citadel-verify --evidence-id EVD-... | --all [--root /path]
  -> prints JSON array of {evidence_id, integrity_status, sha256}
  -> exit code 1 if any item comes back INTEGRITY_ALERT

citadel-status [--json] [--root /path]
  -> disk safety gate state, adapter connectivity, evidence counts,
     recent audit log, whether port 22 is listening on *this* host
```

## Running the tests

```
python3 citadel/tests/test_citadel.py
```

Every test runs against a fresh `tempfile.TemporaryDirectory()` used as
`--root`; nothing in the test suite can touch a real `~/Citadel` tree. The
only input file is `tests/fixtures/synthetic_evidence.txt`
(`CITADEL SYNTHETIC TEST / NOT REAL EVIDENCE`). Per the assignment's own
rule, no test intentionally corrupts a protected *original* — the
integrity-failure path is exercised by removing an original (simulating
loss, not tampering with its bytes) and, separately, by proving that
tampering with a *working copy* leaves the original's verification
untouched.

## Known gaps / what V1 deliberately does not do

- No OCR/transcription actually runs — adapters report connectivity only.
- No drop-folder watcher for `00_INBOX/` yet.
- No real SSH/SCP receiver for the iPhone side — see
  `IPHONE_SHORTCUT_SPEC.md` for the intended transport and what's needed to
  stand it up safely (and not publicly) on the Mac.
- `chmod 0o444` is the only original-protection mechanism; see the
  Integrity model section above for exactly what that does and doesn't
  guarantee.
- Preflight items specific to the real Mac (live disk space right now,
  whether port 22 is open on `iMac.lan`, whether `whisper`/`tesseract` are
  installed there) could not be checked from this cloud sandbox — run
  `citadel-status` on the Mac itself to get those for real.
