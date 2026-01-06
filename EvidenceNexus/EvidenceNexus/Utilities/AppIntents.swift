//
//  AppIntents.swift
//  EvidenceNexus
//
//  Siri Shortcuts and App Intents integration
//

import Foundation
import AppIntents
import SwiftData

// MARK: - Search Evidence Intent
struct SearchEvidenceIntent: AppIntent {
    static var title: LocalizedStringResource = "Search Evidence"
    static var description = IntentDescription("Search for evidence in EvidenceNexus")

    @Parameter(title: "Search Query")
    var query: String

    func perform() async throws -> some IntentResult & ProvidesDialog {
        // In production, would query SwiftData and return results
        let message = "Searching for evidence matching '\(query)'"

        return .result(dialog: IntentDialog(message))
    }
}

// MARK: - Get Pattern Summary Intent
struct GetPatternSummaryIntent: AppIntent {
    static var title: LocalizedStringResource = "Get Pattern Summary"
    static var description = IntentDescription("Get a summary of detected patterns")

    func perform() async throws -> some IntentResult & ProvidesDialog {
        // In production, would query PatternFlag data
        let message = "Found multiple patterns requiring attention"

        return .result(dialog: IntentDialog(message))
    }
}

// MARK: - Add Voice Note Intent
struct AddVoiceNoteIntent: AppIntent {
    static var title: LocalizedStringResource = "Add Voice Note"
    static var description = IntentDescription("Record a voice note as evidence")

    @Parameter(title: "Note Title")
    var title: String

    func perform() async throws -> some IntentResult & ProvidesDialog {
        // In production, would trigger voice recording
        let message = "Recording voice note: \(title)"

        return .result(dialog: IntentDialog(message))
    }
}

// MARK: - Quick Import Intent
struct QuickImportIntent: AppIntent {
    static var title: LocalizedStringResource = "Quick Import"
    static var description = IntentDescription("Quickly import evidence from Photos or Files")

    func perform() async throws -> some IntentResult & OpensIntent {
        // Opens the app to the Imports tab
        return .result()
    }
}

// MARK: - App Shortcuts Provider
struct EvidenceNexusShortcuts: AppShortcutsProvider {
    static var appShortcuts: [AppShortcut] {
        AppShortcut(
            intent: SearchEvidenceIntent(),
            phrases: [
                "Search \(.applicationName)",
                "Find evidence in \(.applicationName)",
                "Search my evidence"
            ],
            shortTitle: "Search Evidence",
            systemImageName: "magnifyingglass"
        )

        AppShortcut(
            intent: GetPatternSummaryIntent(),
            phrases: [
                "Get pattern summary from \(.applicationName)",
                "Show detected patterns",
                "What patterns were found"
            ],
            shortTitle: "Pattern Summary",
            systemImageName: "waveform.path.ecg"
        )

        AppShortcut(
            intent: AddVoiceNoteIntent(),
            phrases: [
                "Add voice note to \(.applicationName)",
                "Record evidence note",
                "New voice note"
            ],
            shortTitle: "Voice Note",
            systemImageName: "mic.fill"
        )

        AppShortcut(
            intent: QuickImportIntent(),
            phrases: [
                "Import to \(.applicationName)",
                "Add evidence",
                "Quick import"
            ],
            shortTitle: "Quick Import",
            systemImageName: "square.and.arrow.down"
        )
    }
}
