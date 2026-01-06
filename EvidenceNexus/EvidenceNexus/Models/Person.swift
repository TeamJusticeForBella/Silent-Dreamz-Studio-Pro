//
//  Person.swift
//  EvidenceNexus
//
//  SwiftData model for people (facial recognition)
//

import Foundation
import SwiftData
import Vision

@Model
final class Person {
    var id: UUID
    var name: String
    var faceIDData: Data? // Serialized VNFaceObservation data
    var faceClusterID: String?
    var notes: String
    var tags: [String]
    var firstSeen: Date
    var lastSeen: Date
    var photoCount: Int
    var role: PersonRole?

    init(
        name: String,
        faceIDData: Data? = nil,
        notes: String = "",
        tags: [String] = [],
        role: PersonRole? = nil
    ) {
        self.id = UUID()
        self.name = name
        self.faceIDData = faceIDData
        self.notes = notes
        self.tags = tags
        self.firstSeen = Date()
        self.lastSeen = Date()
        self.photoCount = 0
        self.role = role
    }
}

// MARK: - Person Role
enum PersonRole: String, Codable, CaseIterable {
    case victim = "Victim"
    case defendant = "Defendant"
    case witness = "Witness"
    case attorney = "Attorney"
    case socialWorker = "Social Worker"
    case fosterParent = "Foster Parent"
    case judge = "Judge"
    case expert = "Expert"
    case family = "Family Member"
    case other = "Other"

    var color: String {
        switch self {
        case .victim: return "red"
        case .defendant: return "orange"
        case .witness: return "blue"
        case .attorney: return "purple"
        case .socialWorker: return "green"
        case .fosterParent: return "yellow"
        case .judge: return "indigo"
        case .expert: return "cyan"
        case .family: return "pink"
        case .other: return "gray"
        }
    }
}

// MARK: - Preset Key People
extension Person {
    static let presetDefendants = [
        ("Koohanim", PersonRole.defendant),
        ("Forrey-Baker", PersonRole.defendant),
        ("Davis", PersonRole.defendant)
    ]
}
