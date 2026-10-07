# Citadel Intake V1.1

A minimal, local-first evidence intake system. Stdlib-only Python 3 — no
`pip install`, no Homebrew, no cloud services, no AI/model APIs. Everything
runs on the operator's own machine against the operator's own filesystem.

**Status: hardening complete, independent review items addressed. Still
not approved for real evidence** — see READY_FOR_REAL_EVIDENCE at the
bottom of this file and in the session's own report for the current call.

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

## V1.1 changelog (independent-review remediation)

An independent review of the V1 build found five classes of issue before
real evidence should touch it. All five are addressed here; see each
numbered section below for the detail, and `tests/` for the test that
proves it:

1. **Evidence-ID race condition** → `citadel_core.reserve_evidence()` now
   mints the ID, derives its on-disk paths, and inserts the evidence row
   all inside one `BEGIN IMMEDIATE` transaction. `tests/test_concurrency.py`.
2. **`citadel-status` wasn't really read-only** → it now opens the DB with
   `mode=ro&immutable=1` and never calls `os.makedirs`/`CREATE TABLE`/
   `INSERT`; a missing DB reports `NOT_INITIALIZED`.
   `tests/test_readonly_status.py`.
3. **Sidecars could be overwritten** → the intake sidecar
   (`<id>.intake.json`) is written once, chmod 0o444, and refuses to be
   rewritten. Verification results go to separate
   `03_METADATA/verification/<id>.VERIFY-<ts>-<rand>.json` records.
   `tests/test_sidecar_immutability.py`.
4. **The disk-gate test didn't test the CLI** → `citadel-intake` now takes
   `--min-free-gib`, and a test drives the real binary with an impossible
   threshold and checks nothing at all got created.
   `tests/test_disk_gate_cli.py`.
5. **No concurrency/crash/path/mutation coverage** → see the Acquisition
   pipeline, Source-mutation detection, and Audit chain sections below,
   plus `tests/test_atomicity.py`, `tests/test_source_mutation.py`,
   `tests/test_path_hardening.py`.

A sixth, self-found issue surfaced while stress-testing item 1: running
the full suite repeatedly (not just once) turned up a real flake —
`PRAGMA journal_mode = WAL` can raise "database is locked" immediately,
ignoring `busy_timeout`, when several processes race to flip a brand-new
database into WAL mode for the first time simultaneously (exactly what 6–8
concurrent `citadel-intake` runs do). Fixed by setting `busy_timeout`
before any other PRAGMA and wrapping the WAL switch itself in a bounded
retry (`citadel_core._set_wal_mode_with_retry()`). Confirmed with 12
consecutive full-suite runs and 10 consecutive targeted runs of the two
concurrency-heaviest test files after the fix, all clean — see the
session's own test-run report for the exact numbers. This is the kind of
thing a single green run hides and only repetition surfaces, which is
why "ran once, passed" is not the same claim as "ran repeatedly under
load, passed."

## Layout

```
citadel/
  bin/      citadel-intake, citadel-verify, citadel-status,
            citadel-audit-verify (executable, stdlib-only)
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
  00_INBOX/              (reserved for future drop-folder watching; unused by V1.1)
  01_ORIGINALS/          <evidence_id>_<filename> — chmod 0o444, never edited
                         .tmp-<evidence_id> staging files during COPYING (never a finalized original)
  02_WORKING_COPIES/     <evidence_id>_<filename> — mutable, used by processing
  03_METADATA/           <evidence_id>.intake.json — frozen sidecar, chmod 0o444
    verification/        <evidence_id>.VERIFY-<timestamp>-<rand>.json — one per citadel-verify run
  04_PROCESSING_QUEUE/   (reserved; job state currently lives in the DB)
  05_INDEX/              citadel.db (SQLite, WAL mode: also citadel.db-wal / citadel.db-shm)
  06_LOGS/               intake.log (hash-chained, append-only JSONL) + intake.log.lock
```

These directories are **not** created until the first successful
`citadel-intake` run clears the disk safety gate — nothing is pre-created
speculatively, so a low-disk machine never gets a half-built evidence tree.

## The disk safety gate

Before copying anything, `citadel-intake` calls
`citadel_core.check_disk_safety_gate()`, which checks free space on the
filesystem containing the configured root. If free space is below
`min_free_gib` (default 5 GiB, set in `config/config.json` or overridden
per-run with `--min-free-gib`), intake refuses immediately — no
directories created, no files copied, no DB writes, nothing. It prints a
JSON error with the actual free/required numbers instead.

V1 only unit-tested the underlying `check_disk_safety_gate()` function.
V1.1 also drives the real `citadel-intake` binary with an impossible
`--min-free-gib` and proves the root directory is never even created
(`tests/test_disk_gate_cli.py`) — including when the root directory
already existed (it's left exactly as empty as it was found).

This gate does **not** try to free space, delete anything, or prompt for
cleanup. That is a human decision.

## Evidence ID format

`EVD-YYYYMMDD-NNNNNN` — date of intake, then a 6-digit sequence scoped to
that day. Minting and reservation are now atomic (see next section) —
this is the fix for the V1 race where two concurrent intakes could compute
the same next-sequence number.

## Acquisition pipeline (intake_state)

Each evidence item moves through an explicit `intake_state`, visible in
`evidence.intake_state` and as one `audit_log` row per transition:

```
RESERVED -> COPYING -> HASHING -> ORIGINAL_VERIFIED -> WORKING_COPY_CREATED
         -> INDEXED -> QUEUED -> COMPLETE
               (any of the above) -> FAILED
```

- **RESERVED**: `reserve_evidence()` mints the evidence_id, derives its
  on-disk paths, and INSERTs the row — all inside one `BEGIN IMMEDIATE`
  SQLite transaction. A second intake process blocked on `BEGIN IMMEDIATE`
  always sees the first one's committed row before computing its own next
  ID, so two concurrent intakes can never collide
  (`tests/test_concurrency.py` runs 8 real subprocesses at once and checks
  for exactly 8 unique IDs).
- **COPYING**: the source is copied to a staging file,
  `01_ORIGINALS/.tmp-<evidence_id>` — never directly to the final name.
  A half-written copy can therefore never be mistaken for a finalized
  original.
- Immediately after the copy, a **source-mutation check** compares the
  source file's size+mtime against what was captured before the copy
  started (see next section). A mismatch aborts as
  `SOURCE_CHANGED_DURING_INTAKE`.
- **HASHING**: the staged copy is rehashed and compared to the hash taken
  before the copy began. A mismatch here is `INTEGRITY_ALERT` (copy-stage
  corruption, distinct from source mutation).
- **ORIGINAL_VERIFIED**: only now is the staging file promoted to its real,
  permanent name via `os.replace()` — an atomic rename — then chmod
  0o444'd. **From this point on, no failure path in this codebase ever
  deletes that file.** A failure after this point (sidecar write failure,
  DB write failure, etc.) leaves the original and intake_state=`FAILED` on
  disk for inspection, per the "never silently delete an already-created
  original" rule.
- **WORKING_COPY_CREATED**, **INDEXED** (sidecar written and frozen),
  **QUEUED** (hashes/events/processing_jobs rows inserted), **COMPLETE**.

`tests/test_atomicity.py` uses a test-only fault-injection hook
(`CITADEL_TEST_FAULT`, see below) to force a failure at each of these
points and checks the expected survivor state every time: copy failure
and disk-full leave no original at all; sidecar-write and DB-write
failures leave the already-finalized original and working copy alone.

### Test-only fault injection

`citadel_core.maybe_inject_fault(name)` raises a controlled exception if
the environment variable `CITADEL_TEST_FAULT` is set to `name`, and is a
complete no-op otherwise — which is always true in real/Mac use, since
nothing in this codebase ever sets that variable itself.
`tests/test_atomicity.py::TestNoFaultControlCase` is the sanity check for
that claim: with the variable unset, intake succeeds exactly as if the
hook didn't exist. Recognized values: `copy_failure`, `disk_full`,
`working_copy_failure`, `sidecar_write_failure`, `db_write_failure`, and
(source-mutation-specific) `mutate_source_after_copy`.

## Source-mutation detection

The source file's size and mtime (nanosecond precision) are captured
before the copy starts and re-checked immediately after it finishes. If
either changed, citadel-intake refuses to certify the acquisition —
`SOURCE_CHANGED_DURING_INTAKE` — rather than index bytes that may not be
what the operator thinks they sent. On a clean intake, both snapshots are
recorded in the sidecar (`source_size_before/after`,
`source_mtime_before_ns/after_ns`) as a matter of record even though they
matched.

`tests/test_source_mutation.py` proves this two ways:
- **Deterministic** (`CITADEL_TEST_FAULT=mutate_source_after_copy`):
  citadel-intake itself appends a byte to the source right after copying
  it, before the post-copy stat check — this is inert unless that env var
  is set, exercises the real check every time with no timing dependency,
  and is what the test suite actually relies on for this guarantee.
- **Best-effort real concurrency**: a background thread races a real
  mutation against the subprocess. This is inherently timing-dependent
  against a near-instant copy of a tiny synthetic file and is **not**
  relied on for the guarantee above — see Remaining risks.

## Integrity model (read this before trusting any "protected" claim)

- The original is hashed (SHA-256) **before** it is copied, then rehashed
  **immediately after** the copy. If those two hashes don't match, the
  intake aborts, the evidence row is marked `INTEGRITY_ALERT` /
  `intake_state=FAILED`, and nothing is silently retried or repaired.
- A separate working copy is made from the original. Only the working copy
  is ever touched by OCR/transcription/etc. The original is never opened
  for writing again by this toolchain.
- `citadel-verify` rehashes the original and compares against the hash
  recorded at intake. A mismatch becomes `INTEGRITY_ALERT` — recorded in
  the `evidence` table and `audit_log`, and in a new verification record
  (see Sidecar section). **Nothing is ever auto-repaired or
  auto-replaced.** A human has to look at it.
- **`chmod 0o444` on an original (and on the frozen sidecar) is NOT true
  immutability.** It's a speed bump against accidental overwrites by this
  toolchain and ordinary non-root processes. Anyone with write access to
  the containing directory, or root, can still delete or replace the
  file; chmod does not survive a `cp --preserve` style overwrite of the
  parent dir, and it offers no protection at all against disk failure,
  filesystem corruption, or a malicious actor with sufficient privilege.
  If you need real immutability, that means a separate read-only volume,
  an append-only/immutable filesystem attribute (e.g. macOS `chflags
  uchg`, which *is* stronger than chmod but still root-overridable), or
  object-lock storage — none of which V1.1 sets up, and all of which are
  a deliberate, separate decision to make later.
- Duplicate detection is by content hash, not filename: a second intake of
  bytes identical to an existing evidence item still gets its own new
  `evidence_id` (so chain-of-custody for *that specific submission event* is
  preserved — who sent it, when, with what notes) but is flagged
  `duplicate_of: <earlier evidence_id>` rather than silently merged or
  rejected.

## SQLite schema

Five tables, all in `05_INDEX/citadel.db`:

- **evidence** — one row per intake; the sidecar JSON's fields plus
  `intake_state`, `duplicate_of`, and `created_at`.
- **hashes** — every hash ever computed for an evidence item, tagged
  `stage` (`intake` or `verify`), so the full hash history survives even
  across repeated verifications.
- **events** — the real-world event metadata (event_date/precision/notes)
  tied to each evidence item; separate from `audit_log`, which is system
  actions, not case facts.
- **processing_jobs** — one row per adapter type that applies to a given
  evidence item's MIME type, carrying `status` and `adapter_status`
  (`CONNECTED`/`NOT_CONNECTED`).
- **audit_log** — append-via-INSERT-only; every state transition and every
  other state-changing operation (`VERIFY_OK`, `INTEGRITY_ALERT`,
  `DUPLICATE_DETECTED`, ...) writes one row here. Nothing in this codebase
  issues `UPDATE` or `DELETE` against `audit_log`.

### SQLite PRAGMA choices (read-write connections — `citadel_core.open_db()`)

| PRAGMA | Value | Why |
|---|---|---|
| `foreign_keys` | `ON` | `audit_log`/`hashes`/`events`/`processing_jobs` rows can't dangle from a nonexistent `evidence_id`. |
| `journal_mode` | `WAL` | Lets a read-only `citadel-status` connection run concurrently with an in-progress intake write instead of blocking on it. |
| `synchronous` | `FULL` | Intake volume is low and human-paced — one phone upload at a time — so we trade write throughput for the strongest durability guarantee against power-loss/crash corruption, since this is evidence data. |
| `busy_timeout` | `5000` (ms) | A second writer waits up to 5s for the first writer's `BEGIN IMMEDIATE` to commit instead of failing immediately with "database is locked" — this is what makes the concurrency test pass cleanly rather than needing retry logic. |

These were chosen deliberately, not left at SQLite's defaults; see
`citadel_core.py`'s module docstring for the same table inline.

### Read-only access and the WAL/`immutable` trade-off

`citadel-status` opens the DB via `citadel_core.open_db_readonly()`, which
uses the URI flags `mode=ro&immutable=1`. `mode=ro` alone turns out not to
be enough: a plain read-only connection to a WAL-mode database still has
to create a `-shm` shared-memory index file the first time it opens (WAL
readers need it to locate valid frames) and, being read-only, can't
checkpoint-and-clean it up on close either. That's exactly the kind of
mutation `citadel-status` must never cause. `immutable=1` tells SQLite to
skip the WAL/locking machinery entirely and read only the main `.db`
file's last-checkpointed contents — at the cost of possibly showing a
view that's a moment stale if a write is genuinely uncheckpointed at the
instant `citadel-status` runs. For a read-only dashboard tool, a stale
count is an acceptable trade for an absolute guarantee that running it
never writes a single byte anywhere. `tests/test_readonly_status.py`
snapshots every file's size+mtime before and after a `citadel-status` run
(including the "DB doesn't exist yet" case, which must create nothing at
all and report `NOT_INITIALIZED`) and asserts the snapshots are identical.

There is also `06_LOGS/intake.log` — an independent, hash-chained,
append-only JSONL log, described next.

## Chained audit log (`06_LOGS/intake.log`)

Each line carries `previous_entry_hash` (the prior line's `entry_hash`, or
64 zeros for the first line) and `entry_hash` (SHA-256 of that line's own
canonical JSON). Appends are serialized across concurrent processes with
an `flock()` on a sibling `.lock` file, so concurrent intakes can't fork
the chain (`tests/test_audit_chain.py::test_concurrent_appends_do_not_fork_the_chain`
runs 6 real concurrent intakes and checks the resulting chain is one
valid sequence).

`citadel-audit-verify` walks the whole chain, recomputes every hash and
link, and reports either `OK` or the exact line number and reason the
chain first breaks (`BROKEN`, `previous_hash_mismatch` or
`entry_hash_mismatch`).

**This is tamper-evident, not tamper-proof.** Read
`bin/citadel-audit-verify`'s own docstring (it's deliberately long) before
relying on it for anything like a chain-of-custody argument. Short
version: there is no external anchor — no timestamping authority, no
separate ledger, no write-once media — so anyone with filesystem write
access to `intake.log`, including the same user account that runs
`citadel-intake` and including root, can regenerate a brand-new,
perfectly self-consistent chain from scratch. It catches accidental
corruption and naive tampering (hand-editing one line without
recomputing everything after it); it does not stop a determined local
attacker who is willing to rewrite the whole file.

## Sidecar JSON (frozen at intake) and verification records

One `<evidence_id>.intake.json` per item in `03_METADATA/`, written once,
chmod 0o444, with exactly these required fields (see
`citadel_core.SIDECAR_FIELDS` / `validate_sidecar()`) plus extra
source-mutation-evidence fields:

```
evidence_id, original_filename, source, evidence_type, event_date,
event_date_precision, acquired_at, sha256, byte_size, mime_type,
original_path, working_copy_path, processing_status, ocr_status,
transcription_status, notes, integrity_status
  (+ source_size_before, source_size_after,
     source_mtime_before_ns, source_mtime_after_ns, duplicate_of)
```

**This file is historical provenance and is never rewritten.**
`write_intake_sidecar()` raises `FileExistsError` if called twice for the
same evidence_id. `citadel-verify` never touches it — each verification
run instead writes a new, separate record to
`03_METADATA/verification/<evidence_id>.VERIFY-<timestamp>-<random>.json`
(the random suffix exists so a tight loop of verifies, as in the test
suite, can never collide and silently overwrite one of its own prior
records). `tests/test_sidecar_immutability.py` hashes the sidecar file
before and after several verify runs — including one that finds a
real `INTEGRITY_ALERT` — and checks the bytes never change.

The DB's `evidence.integrity_status` column is a different thing from the
sidecar's frozen snapshot: it's live, current knowledge, and `citadel-verify`
does update it (that's the point of verification) — just never the sidecar
file on disk.

## Path and filename hardening

`original_filename` as given (any length, any unicode) is always
preserved verbatim in the DB and sidecar for provenance.
`citadel_core.sanitize_filename()` produces a *separate*,
filesystem-safe name used only for the actual on-disk path: it strips
path separators and control characters, NFC-normalizes unicode, replaces
`""`/`"."`/`".."` with `"unnamed"`, and truncates to fit common filesystem
name-length limits while trying to preserve the extension.
`assert_within_root()` is a defense-in-depth check that every path
citadel-intake is about to write resolves under the configured root —
belt-and-suspenders, since `evidence_id` is server-minted and filenames
are already sanitized, so this should never actually trip.
`tests/test_path_hardening.py` covers spaces, quotes, unicode, leading
dots, very long names, duplicate original filenames across different
evidence (no on-disk collision, since paths are prefixed by the unique
evidence_id), unexpected extensions (falls back to
`application/octet-stream`), and a 20MB file to exercise chunked
hashing/copying on something bigger than a few bytes. True multi-GB files
are not tested here — see Remaining risks.

## Processing queue adapters (V1.1: interfaces only, nothing executes)

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
transcription is ever actually run against real evidence by V1.1 — these
are queue placeholders for a future phase.

## Privacy

No evidence leaves the machine this runs on. No OpenAI/Anthropic/Gemini
API calls, no Dropbox/Google Drive/iCloud, no telemetry, no public server.
Everything is local files + a local SQLite database.

## JASON GATE

This toolchain never deletes, overwrites, publishes, exposes, moves,
renames, or modifies an existing evidence file without explicit human
approval. `citadel-intake` only ever *creates* new files under fresh
`evidence_id`s and never deletes a finalized original on any failure
path (see Acquisition pipeline); `citadel-verify` only ever *reads*
originals and *updates status fields / writes new verification records*
(never original file bytes, never the frozen sidecar); nothing here has a
delete/move/rename code path for anything in `01_ORIGINALS/`.

## CLI reference

```
citadel-intake <file> --source "..." --evidence-type {photo,video,audio,document,screenshot,text,other} \
    [--event-date YYYY-MM-DD] [--event-date-precision {exact,day,month,year,unknown}] \
    [--notes "..."] [--root /path] [--min-free-gib N]
  -> prints JSON receipt: {evidence_id, sha256, integrity_status, queue_status, duplicate_of}
  -> on failure: {error, message, evidence_id, ...} with a non-zero exit code
     (error is one of DISK_SAFETY_GATE, NO_SUCH_FILE, ORIGINAL_PATH_COLLISION,
     SOURCE_CHANGED_DURING_INTAKE, INTEGRITY_ALERT, INTAKE_FAILED)

citadel-verify --evidence-id EVD-... | --all [--root /path]
  -> prints JSON array of {evidence_id, integrity_status, sha256}
  -> exit code 1 if any item comes back INTEGRITY_ALERT
  -> writes a new 03_METADATA/verification/*.json record per item; never
     touches the frozen intake sidecar

citadel-status [--json] [--root /path]
  -> read-only: disk safety gate state, adapter connectivity, evidence
     counts by type/integrity_status/intake_state, recent audit log,
     audit-chain status, whether port 22 is listening on *this* host
  -> db_status: "NOT_INITIALIZED" if citadel.db doesn't exist yet (and
     nothing is created to check)

citadel-audit-verify [--json] [--root /path]
  -> walks 06_LOGS/intake.log, recomputes/validates every hash and link
  -> exit 0 (chain OK, or no log yet) / 1 (chain broken — prints the
     first broken line number and reason)
  -> read this tool's own docstring for exactly what it does and does
     NOT prove (tamper-evident, not tamper-proof)
```

## Running the tests

```
python3 -m unittest discover -s citadel/tests -p "test_*.py" -v
```

63 tests across 9 files. Every test runs against a fresh
`tempfile.TemporaryDirectory()` used as `--root`; nothing in the test
suite can touch a real `~/Citadel` tree. Input is always either
`tests/fixtures/synthetic_evidence.txt`
(`CITADEL SYNTHETIC TEST / NOT REAL EVIDENCE`), a file the test itself
generates (unicode names, a 20MB random blob, distinct per-slot
concurrency fixtures), or `os.urandom()` content — never anything real.
Per the assignment's own rule, no test intentionally corrupts a protected
*original's bytes* — integrity-failure paths are exercised by removing an
original (simulating loss) or via the `CITADEL_TEST_FAULT` hook (which is
a complete no-op unless a test explicitly sets it), and separately by
proving that tampering with a *working copy* leaves the original's
verification untouched.

| File | Covers |
|---|---|
| `test_citadel.py` | core intake/verify/status/index/sidecar/audit behavior |
| `test_concurrency.py` | review item 1 — unique IDs under real concurrent intakes |
| `test_disk_gate_cli.py` | review item 4 — the real CLI gate, not just the primitive |
| `test_readonly_status.py` | review item 2 — zero mutation, `NOT_INITIALIZED` |
| `test_sidecar_immutability.py` | review item 3 — frozen sidecar, separate verification records |
| `test_atomicity.py` | review item 5 — fault injection at each pipeline stage |
| `test_source_mutation.py` | review item 6 — source changing mid-acquisition |
| `test_path_hardening.py` | review item 7 — unicode/length/duplicate/escape handling |
| `test_audit_chain.py` | review item 9 — hash-chain validity and tamper detection |

## Known gaps / Remaining risks

- No OCR/transcription actually runs — adapters report connectivity only.
- No drop-folder watcher for `00_INBOX/` yet.
- No real SSH/SCP receiver for the iPhone side — see
  `IPHONE_SHORTCUT_SPEC.md`. Not started, per the review's explicit
  instruction not to begin iPhone transport yet.
- `chmod 0o444` is the only original-protection mechanism; see the
  Integrity model section for exactly what that does and doesn't
  guarantee.
- The source-mutation real-concurrency test
  (`test_source_mutation.py::TestSourceMutationBestEffortRace`) is
  inherently timing-dependent and not relied on for the core guarantee —
  the deterministic fault-injection test is. A genuinely adversarial
  concurrent-mutation scenario (an attacker, not an accident) is not
  specifically modeled.
- True multi-GB files are untested; only a 20MB synthetic blob was used,
  to avoid burning sandbox disk. Chunked hashing/copying should scale,
  but this hasn't been empirically confirmed at real evidence-file sizes
  (large video exports, for instance).
- The SQLite schema changed in V1.1 (`intake_state` column added) with no
  migration script. That's fine — nothing has been deployed with real
  evidence yet — but a *future* schema change after real deployment would
  need a migration path this codebase does not provide.
- `advance_state()` opens a short-lived connection per state transition.
  If the DB file itself becomes fully inaccessible (disk unmounted,
  permissions revoked) partway through a failure handler's own attempt to
  record `FAILED`, that write can itself fail silently (caught and
  swallowed) — the evidence row is then stuck at whatever `intake_state`
  it last reached, recoverable only by manual inspection, not
  automatically. This is an inherent limit of the current design, not
  tested directly (would require simulating total DB inaccessibility).
  No test for this specific "DB has died" compound scenario.
- The chained audit log's concurrency guard (`flock`) only serializes
  processes on the *same host*. If `06_LOGS/intake.log` is ever placed on
  a network filesystem shared across machines, `flock` semantics are not
  guaranteed — not a concern for the current single-Mac design.
- Preflight items specific to the real Mac (live disk space right now,
  whether port 22 is open on `iMac.lan`, whether `whisper`/`tesseract` are
  installed there) could not be checked from this cloud sandbox — run
  `citadel-status` on the Mac itself to get those for real.

## READY_FOR_REAL_EVIDENCE

See the session's own remediation report for the authoritative answer at
the time V1.1 was delivered. This file will not independently assert
"YES" — that call belongs in the explicit test-run report each round of
review produces, not buried in documentation that can drift out of sync
with what was actually last verified.
