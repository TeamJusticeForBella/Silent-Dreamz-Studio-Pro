//
//  EvidenceItem.swift
//  EvidenceNexus
//
//  SwiftData model for evidence items
//

import Foundation
import SwiftData

@Model
final class EvidenceItem {
    var id: UUID
    var title: String
    var itemDescription: String
    var date: Date
    var type: EvidenceType
    var tags: [String]
    var notes: String
    var fileURL: URL?
    var sourceAccount: String?
    var thumbnailData: Data?
    var ocrText: String?
    var metadata: [String: String]
    var createdAt: Date
    var modifiedAt: Date

    // Chain of custody
    var originalSource: String
    var importedAt: Date
    var sha256Hash: String?

    init(
        title: String,
        description: String,
        date: Date,
        type: EvidenceType,
        tags: [String] = [],
        notes: String = "",
        fileURL: URL? = nil,
        sourceAccount: String? = nil,
        originalSource: String
    ) {
        self.id = UUID()
        self.title = title
        self.itemDescription = description
        self.date = date
        self.type = type
        self.tags = tags
        self.notes = notes
        self.fileURL = fileURL
        self.sourceAccount = sourceAccount
        self.metadata = [:]
        self.createdAt = Date()
        self.modifiedAt = Date()
        self.originalSource = originalSource
        self.importedAt = Date()
    }
}

// MARK: - Evidence Type
enum EvidenceType: String, Codable, CaseIterable {
    case email = "Email"
    case text = "Text Message"
    case photo = "Photo"
    case video = "Video"
    case document = "Document"
    case audio = "Audio"
    case voiceNote = "Voice Note"
    case socialPost = "Social Media Post"
    case webpage = "Webpage"

    var iconName: String {
        switch self {
        case .email: return "envelope.fill"
        case .text: return "message.fill"
        case .photo: return "photo.fill"
        case .video: return "video.fill"
        case .document: return "doc.fill"
        case .audio: return "waveform"
        case .voiceNote: return "mic.fill"
        case .socialPost: return "bubble.left.and.bubble.right.fill"
        case .webpage: return "globe"
        }
    }

    var color: String {
        switch self {
        case .email: return "blue"
        case .text: return "green"
        case .photo: return "purple"
        case .video: return "red"
        case .document: return "orange"
        case .audio: return "pink"
        case .voiceNote: return "mint"
        case .socialPost: return "indigo"
        case .webpage: return "cyan"
        }
    }
}
