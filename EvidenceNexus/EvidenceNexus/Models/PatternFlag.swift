//
//  PatternFlag.swift
//  EvidenceNexus
//
//  SwiftData model for pattern detection flags
//

import Foundation
import SwiftData

@Model
final class PatternFlag {
    var id: UUID
    var type: PatternType
    var confidence: Double // 0.0 to 1.0
    var evidenceIDs: [String]
    var notes: String
    var detectedAt: Date
    var isUserVerified: Bool
    var explanation: String
    var keywords: [String]
    var severity: SeverityLevel

    init(
        type: PatternType,
        confidence: Double,
        evidenceIDs: [String],
        notes: String = "",
        explanation: String = "",
        keywords: [String] = [],
        severity: SeverityLevel = .medium
    ) {
        self.id = UUID()
        self.type = type
        self.confidence = confidence
        self.evidenceIDs = evidenceIDs
        self.notes = notes
        self.detectedAt = Date()
        self.isUserVerified = false
        self.explanation = explanation
        self.keywords = keywords
        self.severity = severity
    }
}

// MARK: - Pattern Type
enum PatternType: String, Codable, CaseIterable {
    case deception = "Deception"
    case crime = "Criminal Activity"
    case obstruction = "Obstruction of Justice"
    case neglect = "Neglect"
    case abuse = "Abuse"
    case falsification = "Falsification"
    case redaction = "Improper Redaction"
    case delay = "Improper Delay"
    case misconduct = "Attorney Misconduct"
    case trafficking = "Trafficking"
    case exploitation = "Exploitation"
    case inconsistency = "Timeline Inconsistency"

    var iconName: String {
        switch self {
        case .deception: return "exclamationmark.triangle.fill"
        case .crime: return "xmark.octagon.fill"
        case .obstruction: return "hand.raised.fill"
        case .neglect: return "heart.slash.fill"
        case .abuse: return "bolt.fill"
        case .falsification: return "doc.text.fill.badge.ellipsis"
        case .redaction: return "eye.slash.fill"
        case .delay: return "clock.fill"
        case .misconduct: return "person.fill.xmark"
        case .trafficking: return "arrow.triangle.2.circlepath"
        case .exploitation: return "dollarsign.circle.fill"
        case .inconsistency: return "calendar.badge.exclamationmark"
        }
    }

    var color: String {
        switch self {
        case .deception: return "orange"
        case .crime: return "red"
        case .obstruction: return "purple"
        case .neglect: return "yellow"
        case .abuse: return "red"
        case .falsification: return "orange"
        case .redaction: return "blue"
        case .delay: return "cyan"
        case .misconduct: return "purple"
        case .trafficking: return "red"
        case .exploitation: return "red"
        case .inconsistency: return "yellow"
        }
    }
}

// MARK: - Severity Level
enum SeverityLevel: String, Codable, CaseIterable {
    case low = "Low"
    case medium = "Medium"
    case high = "High"
    case critical = "Critical"

    var color: String {
        switch self {
        case .low: return "green"
        case .medium: return "yellow"
        case .high: return "orange"
        case .critical: return "red"
        }
    }
}
