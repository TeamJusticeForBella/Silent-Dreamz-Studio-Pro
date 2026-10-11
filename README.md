# Silent-Dreamz-Studio-Pro — Team Justice For Bella Workspace

This repository is the private workspace ("the Citadel") for **Team Justice For
Bella**. It is proprietary and case-related — it is **not** the public
TeamJusticeForBellaFoundation.org website, and nothing here is intended for
public distribution.

For Justice. For Bella. 🤍

## Contents

```
.
├── EvidenceNexus/      Private, on-device iOS evidence-vault app (Swift/SwiftUI/SwiftData)
├── docs/               Internal tooling documentation (not case evidence)
├── CITADEL_MAP.md      Repository organization, status, and open items
├── LICENSE             Proprietary notice (see below)
└── README.md           This file
```

- **[`EvidenceNexus/`](EvidenceNexus/README.md)** — the evidence-management
  application: biometric-locked storage, on-device OCR/transcription/facial
  recognition, pattern detection, and chain-of-custody logging. See its own
  README and `PROJECT_STRUCTURE.md` for architecture details.
- **[`docs/`](docs/)** — documentation for internal tooling (e.g. the drive
  scan utility) that is separate from any case evidence.
- **[`CITADEL_MAP.md`](CITADEL_MAP.md)** — the organizational map of this
  repository: what lives here, what deliberately does not, and the current
  status of the separate public-website effort.

## Public website

The public advocacy site (TeamJusticeForBellaFoundation.org) is a **separate
effort in a separate repository**, pending Codex's discovery report. It must
never share a codebase, branch, or commit history with this repository. See
`CITADEL_MAP.md` for the current status.

## Privacy firewall

This repository may contain or reference sensitive case material. Anyone —
human or AI agent — working here must:

- Never copy evidence, case files, or private data into any public-facing
  location, fixture, or source file.
- Never commit secrets, credentials, or private API endpoints.
- Never expose EXIF/location data or local filesystem paths.
- Treat `EvidenceNexus/` as evidence-adjacent: preserve chain of custody,
  never modify original sources, copy-only imports.

## License

See [`LICENSE`](LICENSE). This project is proprietary to Team Justice For
Bella; it is not open-source software.
