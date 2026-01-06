# EvidenceNexus

**Secure, Private, On-Device Evidence Management for iOS**

---

## Overview

**EvidenceNexus** is a production-ready iOS application designed for high-stakes legal cases involving foster care agencies, attorney misconduct, and family rights. Built with Swift, SwiftUI, and SwiftData, it provides a comprehensive evidence vault with on-device AI analysis, pattern detection, and multi-source import capabilities.

**For Justice, For Bella. 🤍**

---

## Features

### 🔒 Security & Privacy
- **Face ID / Touch ID** biometric authentication
- **AES-256 encryption** for all stored data
- **On-device processing** - no cloud uploads, ever
- **Tamper-evident audit logs** for chain of custody
- **SHA-256 hashing** for file integrity verification
- **Copy-only imports** - original sources never modified

### 📥 Multi-Source Import
- **Gmail** - Import emails via OAuth (Google Sign-In SDK)
- **Outlook** - Import emails via Microsoft Graph API (MSAL)
- **Facebook** - Import posts and messages (Facebook SDK)
- **Instagram** - Import media (Meta Graph API)
- **Photos** - Import photos/videos with facial recognition
- **Files** - Drag-and-drop document import
- **Voice Notes** - Record and transcribe audio notes

### 🤖 On-Device AI Intelligence
- **Facial Recognition** - Vision framework clustering and identification
- **Speech Transcription** - Accurate on-device speech-to-text
- **OCR Text Extraction** - Extract text from images and PDFs
- **Pattern Detection** - Identify:
  - Deception (hedging language, inconsistencies)
  - Crimes (neglect, abuse, trafficking, exploitation)
  - Obstruction (redaction, delay, concealment)
  - Attorney misconduct
  - Timeline anomalies
- **Sentiment Analysis** - Analyze emotional tone in text
- **Adaptive Learning** - On-device ML classifier improves with use

### 📊 Organization & Analysis
- **Library** - Grid/list views with full-text search
- **Timeline** - Chronological view with anomaly highlights
- **Patterns** - Flagged items with confidence scores
- **AI Hub** - Generate summaries, export reports
- **Settings** - Account management, audit logs

### 🔗 AI Team Coordination
- **Siri Shortcuts** - Voice commands for quick access
- **Custom URL Scheme** - `evidencenexus://query?search=...`
- **Share Extension** - Export data to external AI tools (Claude, Grok)
- **Timestamped Exports** - PDF/JSON bundles

---

## Requirements

- **iOS 18.0+**
- **Xcode 16.0+**
- **Swift 5.9+**
- **iPhone with Face ID / Touch ID** (optimized for iPhone 17 Pro Max)

---

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/TeamJusticeForBella/EvidenceNexus.git
cd EvidenceNexus
```

### 2. Open in Xcode
```bash
open EvidenceNexus.xcodeproj
```

### 3. Configure Signing & Capabilities
1. Select the **EvidenceNexus** target
2. Go to **Signing & Capabilities**
3. Select your development team
4. Ensure these capabilities are enabled:
   - Face ID
   - Keychain Sharing
   - Background Modes (Audio, Processing)

### 4. Add External SDK Dependencies (Optional)
To enable Gmail, Outlook, Facebook, and Instagram connectors, uncomment the dependencies in `Package.swift`:

```swift
dependencies: [
    .package(url: "https://github.com/google/GoogleSignIn-iOS", from: "7.0.0"),
    .package(url: "https://github.com/AzureAD/microsoft-authentication-library-for-objc", from: "1.3.0"),
    .package(url: "https://github.com/facebook/facebook-ios-sdk", from: "16.0.0"),
],
```

Then update the target dependencies accordingly.

### 5. Build and Run
1. Select your target device (iPhone 17 Pro Max or similar)
2. Press **Cmd+R** to build and run

---

## Architecture

### SwiftData Models
- **EvidenceItem** - Core evidence with metadata, tags, OCR text
- **Person** - Facial recognition data and roles
- **PatternFlag** - AI-detected patterns with confidence scores
- **Transcript** - Speech-to-text with timestamps
- **AuditLogEntry** - Tamper-evident activity log

### Services
- **ImportManager** - Handles all evidence imports
- **SecurityManager** - Biometric auth, encryption, keychain
- **FacialRecognitionService** - Vision-based face clustering
- **TranscriptionService** - On-device speech-to-text
- **OCRService** - Text extraction from images/PDFs
- **PatternDetectionEngine** - NaturalLanguage-based pattern detection

### Views (SwiftUI)
- **ContentView** - Main TabView navigation
- **ImportsView** - Multi-source import interface
- **LibraryView** - Grid/list browsing with search
- **TimelineView** - Chronological evidence timeline
- **PatternsView** - Detected pattern flags
- **AIHubView** - AI analysis and export tools
- **SettingsView** - Account and security settings

---

## Usage

### Importing Evidence
1. Open the **Import** tab
2. Select a connector (Gmail, Outlook, Photos, Files, etc.)
3. Authenticate (OAuth for email/social connectors)
4. Select evidence to import
5. Files are **copied** (never moved) to secure storage
6. AI processing runs automatically (OCR, transcription, facial recognition)

### Searching Evidence
- Use the **Library** tab search bar
- Full-text search across titles, descriptions, tags, and OCR text
- Filter by type, tag, or source

### Reviewing Patterns
1. Open the **Patterns** tab
2. Review flagged items by severity (Critical, High, Medium, Low)
3. Tap a pattern to see:
   - Explanation
   - Related evidence
   - Keywords detected
   - Confidence score
4. Verify patterns to mark them as reviewed

### Exporting Reports
1. Open the **AI Hub** tab
2. Tap **Generate Case Summary** for an AI-powered overview
3. Tap **Export Evidence Bundle** to create:
   - PDF reports
   - JSON data exports
   - Timeline documents
   - Complaint drafts

### Siri Integration
Use voice commands:
- *"Search EvidenceNexus for [query]"*
- *"Show detected patterns"*
- *"Add voice note to EvidenceNexus"*
- *"Quick import to EvidenceNexus"*

### External AI Coordination
Use the custom URL scheme to query from other apps:
```
evidencenexus://query?search=obstruction
evidencenexus://export?format=json
```

---

## Preset Tags & Defendants

The app includes preset tags for quick evidence tagging:

**Key Defendants:**
- Koohanim
- Forrey-Baker
- Davis

**Common Themes:**
- Obstruction
- Redaction
- Foster Neglect
- False Statement
- Timeline Issue
- Missing Evidence

---

## Privacy & Legal Integrity

### Chain of Custody
- All imports are **copied**, never moved
- SHA-256 hashes verify file integrity
- Audit log tracks every access and modification
- Timestamps are immutable

### Data Protection
- **No cloud storage** - everything stays on device
- **No analytics** - no tracking, no telemetry
- **No network access** except for user-initiated OAuth
- **Encrypted at rest** using iOS Data Protection APIs

### Permissions
The app requests minimal permissions:
- Photos: To import evidence
- Microphone: To record voice notes
- Speech Recognition: For transcription (on-device only)
- Face ID: For authentication
- Camera: To capture photos/videos

---

## Development Roadmap

### Phase 1: Core Features ✅
- SwiftData models
- Security & encryption
- Import manager
- Main views (Library, Timeline, Patterns, AI Hub)

### Phase 2: AI Integration 🚧
- Advanced pattern detection
- Create ML classifier training
- Enhanced sentiment analysis
- Speaker diarization

### Phase 3: External Connectors 📅
- Gmail integration
- Outlook integration
- Facebook/Instagram integration
- iCloud sync (encrypted)

### Phase 4: Advanced Features 📅
- PDF report generation
- Timeline visualization graphs
- Network analysis (relationship mapping)
- Witness statement comparison

---

## Contributing

This project is built for **Team Justice For Bella**. Contributions aligned with the mission of protecting children and ensuring legal accountability are welcome.

### Guidelines
1. Maintain privacy-first architecture
2. Never add cloud dependencies
3. Keep all AI processing on-device
4. Follow Swift/SwiftUI best practices
5. Document all changes thoroughly

---

## License

**Proprietary - Team Justice For Bella**

This software is developed for specific legal case purposes. Unauthorized use, reproduction, or distribution is prohibited.

---

## Support & Contact

For questions, bug reports, or feature requests:
- **GitHub Issues**: [TeamJusticeForBella/EvidenceNexus/issues](https://github.com/TeamJusticeForBella/EvidenceNexus/issues)
- **Project Lead**: Team Justice For Bella

---

## Acknowledgments

Built with:
- Swift
- SwiftUI
- SwiftData
- Vision Framework
- Speech Framework
- NaturalLanguage Framework
- CryptoKit
- AVFoundation

**For Justice. For Bella. For every child who deserves protection. 🤍**

---

## Disclaimer

This software is provided as-is for evidence management purposes. All findings and AI-generated insights should be reviewed by qualified legal professionals. The developers assume no liability for legal decisions made based on this software's output.

---

**Version 1.0.0** | Built 2026-01-06 | iOS 18+
