//
//  Transcript.swift
//  EvidenceNexus
//
//  SwiftData model for audio/video transcripts
//

import Foundation
import SwiftData

@Model
final class Transcript {
    var id: UUID
    var text: String
    var speaker: String?
    var audioURL: URL?
    var videoURL: URL?
    var createdAt: Date
    var confidence: Double
    var segments: [TranscriptSegment]
    var language: String
    var duration: TimeInterval

    init(
        text: String,
        speaker: String? = nil,
        audioURL: URL? = nil,
        videoURL: URL? = nil,
        confidence: Double = 0.0,
        segments: [TranscriptSegment] = [],
        language: String = "en-US",
        duration: TimeInterval = 0
    ) {
        self.id = UUID()
        self.text = text
        self.speaker = speaker
        self.audioURL = audioURL
        self.videoURL = videoURL
        self.createdAt = Date()
        self.confidence = confidence
        self.segments = segments
        self.language = language
        self.duration = duration
    }
}

// MARK: - Transcript Segment
struct TranscriptSegment: Codable {
    var text: String
    var timestamp: TimeInterval
    var confidence: Double
    var speaker: String?
}

// MARK: - Audit Log Entry
@Model
final class AuditLogEntry {
    var id: UUID
    var action: AuditAction
    var evidenceID: String?
    var userID: String
    var timestamp: Date
    var details: String
    var ipAddress: String?
    var deviceInfo: String

    init(
        action: AuditAction,
        evidenceID: String? = nil,
        userID: String = "primary_user",
        details: String = "",
        ipAddress: String? = nil
    ) {
        self.id = UUID()
        self.action = action
        self.evidenceID = evidenceID
        self.userID = userID
        self.timestamp = Date()
        self.details = details
        self.ipAddress = ipAddress
        self.deviceInfo = "\(UIDevice.current.model) - iOS \(UIDevice.current.systemVersion)"
    }
}

// MARK: - Audit Action
enum AuditAction: String, Codable {
    case appLaunched = "App Launched"
    case appUnlocked = "App Unlocked"
    case evidenceImported = "Evidence Imported"
    case evidenceViewed = "Evidence Viewed"
    case evidenceModified = "Evidence Modified"
    case evidenceExported = "Evidence Exported"
    case evidenceDeleted = "Evidence Deleted"
    case accountConnected = "Account Connected"
    case accountDisconnected = "Account Disconnected"
    case patternDetected = "Pattern Detected"
    case patternVerified = "Pattern Verified"
    case searchPerformed = "Search Performed"
    case reportGenerated = "Report Generated"
}
