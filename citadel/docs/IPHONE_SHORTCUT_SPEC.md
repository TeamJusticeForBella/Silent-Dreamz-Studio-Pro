# Citadel Intake — iPhone Shortcuts Spec (for Phase 2)

Nothing in this spec is implemented yet. V1 is the Mac-side CLI only
(`citadel-intake` / `citadel-verify` / `citadel-status`). This document is
the exact recipe for the Shortcut once you're ready to wire up the phone
side, plus the Mac-side prerequisites it depends on.

## Security ground rule

**Do not expose SSH to the public internet.** The Shortcut talks to the Mac
only over a network path you control: the same LAN/Wi-Fi, or a private
mechanism such as a Tailscale/WireGuard tunnel between the phone and the
Mac. Never port-forward 22 on a router to the open internet to make this
"work from anywhere" — that trades convenience for a real attack surface
against evidence that may matter in court. If remote access is ever
needed, that's a separate, deliberate decision (e.g. a VPN mesh), not a
router port-forward.

## Shortcut steps (Apple Shortcuts app)

1. **Receive input from Share Sheet**
   - Shortcut Input Types: `Images`, `Videos`, `Audio`, `Files`, `PDFs`.
   - "Accepts Share Sheet Input" = On, shown in Share Sheet = On.

2. **Ask for Source**
   - Action: *Choose from Menu* or *Ask for Input (Text)*.
   - Suggested menu items: `iPhone / Jason`, `iPhone / [other party name]`,
     `Screenshot`, `Forwarded`, `Other` (free text fallback).
   - Store result as variable `Source`.

3. **Choose Evidence Type**
   - Action: *Choose from Menu*.
   - Items must exactly match `citadel-intake --evidence-type` choices:
     `photo`, `video`, `audio`, `document`, `screenshot`, `text`, `other`.
   - Store as `EvidenceType`.

4. **Ask Event Date**
   - Action: *Ask for Input (Date)*, default = current date, allow "I don't
     know" via a separate *Choose from Menu* step for `EventDatePrecision`
     (`exact`, `day`, `month`, `year`, `unknown`).
   - Format the date as `YYYY-MM-DD` with *Format Date* before sending.
   - Store as `EventDate` / `EventDatePrecision`.

5. **Ask Notes**
   - Action: *Ask for Input (Text)*, multiline, optional (allow empty).
   - Store as `Notes`.

6. **Secure transfer to Mac**
   - V1 has no network receiver — this step needs a small addition on the
     Mac side before it can work: either (a) a `sshd` endpoint reachable
     only on the trusted LAN/VPN with key-based auth (no passwords) and an
     `authorized_keys` entry restricted to a forced command that calls
     `citadel-intake` directly (so the SSH key can *only* ever run intake,
     nothing else), or (b) a tiny local HTTP listener bound to
     `127.0.0.1`/LAN-only that the Shortcut's *Get Contents of URL* action
     POSTs to, which then shells out to `citadel-intake`. Both are Phase 2
     work; V1 deliberately ships neither to avoid opening any network
     listener before the Mac's disk/security posture is confirmed healthy.
   - Shortcut action once that exists: *Get Contents of URL* (HTTPS to a
     LAN address, self-signed cert pinned in the Shortcut) or *Run Script
     Over SSH* (if using a Shortcuts SSH action / an SSH-capable automation
     app), passing the file plus `Source`, `EvidenceType`, `EventDate`,
     `EventDatePrecision`, `Notes` as parameters mapping 1:1 to
     `citadel-intake`'s CLI flags.

7. **Receive JSON receipt**
   - The Mac-side endpoint returns exactly what `citadel-intake` prints to
     stdout: `{"evidence_id": ..., "sha256": ..., "integrity_status": ...,
     "queue_status": {...}, "duplicate_of": ...}`.
   - Action: *Get Dictionary from Input* on the response body.

8. **Display result**
   - Action: *Show Result* (or *Show Notification* for a less intrusive
     confirmation), formatted as:
     ```
     Evidence ID:  <evidence_id>
     SHA-256:      <sha256, first 12 + last 8 chars is enough on a phone screen>
     Integrity:    <integrity_status>
     Queue:        <queue_status, e.g. "METADATA_EXTRACTION: QUEUED">
     ```
   - On any error key in the response (`error`), show that message instead
     and do not claim success.

## What's needed on the Mac before step 6 can be built

- Decide transport: SSH-with-forced-command vs. local-only HTTP listener.
  Either way, nothing binds to `0.0.0.0` on a port reachable from outside
  your LAN/VPN.
- If SSH: create a dedicated key pair for this Shortcut only, restrict its
  `authorized_keys` entry with `command="/path/to/citadel/bin/citadel-intake-wrapper ..."`
  so that key can never get an interactive shell.
- Either way: the wrapper must validate/sanitize every field before
  invoking `citadel-intake` (evidence_type against the fixed enum, dates
  parsed not string-concatenated, filenames never taken from attacker
  input for path construction — `citadel-intake` already derives paths
  from its own minted `evidence_id`, not from the client-supplied filename
  alone, which helps here).
- `citadel-status` should be run on the Mac first to confirm the disk
  safety gate passes and to see which processing adapters are actually
  `CONNECTED` there, before wiring up real intake traffic.
