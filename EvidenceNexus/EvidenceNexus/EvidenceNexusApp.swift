//
//  EvidenceNexusApp.swift
//  EvidenceNexus
//
//  Created for Team Justice For Bella
//  iOS 18+ | iPhone 17 Pro Max Optimized
//

import SwiftUI
import SwiftData

@main
struct EvidenceNexusApp: App {
    @StateObject private var securityManager = SecurityManager()
    @StateObject private var appState = AppState()

    var sharedModelContainer: ModelContainer = {
        let schema = Schema([
            EvidenceItem.self,
            Person.self,
            PatternFlag.self,
            Transcript.self,
            AuditLogEntry.self
        ])

        let modelConfiguration = ModelConfiguration(
            schema: schema,
            isStoredInMemoryOnly: false,
            allowsSave: true
        )

        do {
            return try ModelContainer(for: schema, configurations: [modelConfiguration])
        } catch {
            fatalError("Could not create ModelContainer: \(error)")
        }
    }()

    var body: some Scene {
        WindowGroup {
            ContentView()
                .modelContainer(sharedModelContainer)
                .environmentObject(securityManager)
                .environmentObject(appState)
                .onAppear {
                    securityManager.authenticate()
                }
        }
    }
}

// MARK: - App State
class AppState: ObservableObject {
    @Published var selectedTab: Int = 0
    @Published var searchText: String = ""
    @Published var isProcessing: Bool = false
    @Published var processingMessage: String = ""
    @Published var showAlert: Bool = false
    @Published var alertMessage: String = ""

    func showProcessing(_ message: String) {
        isProcessing = true
        processingMessage = message
    }

    func hideProcessing() {
        isProcessing = false
        processingMessage = ""
    }

    func showError(_ message: String) {
        alertMessage = message
        showAlert = true
    }
}
