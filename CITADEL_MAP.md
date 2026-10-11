# Citadel Map

Organizational reference for the `TeamJusticeForBella/Silent-Dreamz-Studio-Pro`
repository. This is the **private** workspace ("the Citadel") — it is
distinct from the public TeamJusticeForBellaFoundation.org website.

Last organized: 2026-10-11, by Claude Code (frontend/design role), at
Jason Barr's request. No evidence, Swift application logic, or public-site
scaffolding was touched in this pass — see "What this pass did" below.

## Repository layout

```
.
├── EvidenceNexus/           Private iOS evidence-vault app (Swift/SwiftUI/SwiftData)
│   ├── EvidenceNexus/       App source (Models, Views, Services, Security, AI, Utilities)
│   ├── Package.swift        Swift Package Manager manifest
│   ├── README.md            App-level overview, setup, architecture
│   └── PROJECT_STRUCTURE.md Detailed component inventory
├── docs/
│   └── drive_scan.md        Doc for an internal drive-scanning CLI tool
├── CITADEL_MAP.md           This file
├── LICENSE                  Proprietary notice
├── README.md                Top-level orientation
└── .gitignore
```

## What lives here vs. what doesn't

**Belongs in this repo:**
- EvidenceNexus application source code and its own documentation.
- Internal tooling docs/scripts that operate *on* evidence without
  *containing* evidence (e.g. `drive_scan.md`).
- Organizational/process documentation like this file.

**Must never land in this repo:**
- Actual case evidence, exports, scans, or private documents.
- Public website source code (it belongs in a separate, approved repository
  once Codex's discovery is complete — see Architecture Decision 001 below).
- Secrets, credentials, API keys, or OAuth tokens.
- Xcode user-state files (`xcuserdata/`, `*.xcuserstate`, `DerivedData/`) —
  these often embed local filesystem paths. Now excluded via `.gitignore`.

## Status: public website

**On hold pending Codex discovery**, per Architecture Decision 001
(2026-10-11, Jason Barr / Citadel Command):

1. Repository and working tree preserved — no website branches, folders,
   commits, or scaffolding created.
2. EvidenceNexus is isolated and untouched.
3. Waiting on Codex's four discovery documents:
   - `DISCOVERY_REPORT.md`
   - `RECOVERY_MAP.md`
   - `REPOSITORY_MAP.md`
   - `WEBSITE_GAP_ANALYSIS.md`
4. The public site will be developed in a **separate, approved repository**.
5. Once discovery completes, the seven design deliverables
   (`DESIGN_DIRECTION.md`, `DESIGN_TOKENS.md`, `COMPONENT_INVENTORY.md`,
   `PAGE_BLUEPRINTS.md`, `MOBILE_STRATEGY.md`, `ACCESSIBILITY_PLAN.md`,
   `MOTION_SPEC.md`) will be produced there, using synthetic placeholder
   content until Jason explicitly approves public-facing material.

## What this pass did (organizational cleanup only)

1. **`README.md`** — replaced leftover, unrelated boilerplate (it described
   an "AI-powered music production" product, which does not match this
   repo's actual contents) with an accurate orientation to the Citadel,
   EvidenceNexus, and the privacy firewall.
2. **`LICENSE`** — replaced a generic MIT license (attributed to an
   unrelated "SilentDreamzSoundDesignStudio") with a proprietary notice
   consistent with the license EvidenceNexus's own README already claims
   ("Proprietary — Team Justice For Bella"). The two were previously
   contradictory.
3. **`.gitignore`** — added macOS, Xcode/Swift-Package-Manager, and
   evidence-path exclusions. Previously the file was entirely generic
   Node/web-project boilerplate with no protection against committing
   Xcode user-state (which can leak local filesystem paths) or an
   accidental evidence path.
4. **This file** — a standing map so any agent (Claude, Codex, ChatGPT) or
   human opening this repo can immediately see what's here, what isn't,
   and why.

No Swift source files were modified. No commits, pushes, or scaffolding
related to the public website occurred.

## Open items (flagged for Codex / Jason — not acted on here)

These are documentation/code inconsistencies observed in `EvidenceNexus/`,
left for the owning team since Swift application logic is outside this
pass's (frontend/design) scope:

- `PROJECT_STRUCTURE.md` documents an `AuditLogEntry.swift` model and a
  `Resources/` directory; neither currently exists under
  `EvidenceNexus/EvidenceNexus/`.
- The top-level README's install instructions reference opening
  `EvidenceNexus.xcodeproj`, but the project currently only has a
  `Package.swift` (Swift Package Manager) — no `.xcodeproj` is present.
- `docs/drive_scan.md` documents a `drive_scan.py` CLI tool; no such script
  currently exists in the repository.

## Firewall reminder

PUBLIC WEBSITE != PRIVATE CITADEL. Anyone working in this repository —
agent or human — must never copy evidence into a public location, embed
it in source/fixtures, commit it, expose EXIF/location data, expose local
filesystem paths, or expose private API endpoints. Use synthetic
placeholder data for any public-facing work until Jason explicitly
approves real assets.
