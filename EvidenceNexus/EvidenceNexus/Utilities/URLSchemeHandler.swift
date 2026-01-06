//
//  URLSchemeHandler.swift
//  EvidenceNexus
//
//  Custom URL scheme for AI team coordination
//  Supports: evidencenexus://query?search=... and evidencenexus://export?format=...
//

import Foundation
import SwiftUI

class URLSchemeHandler: ObservableObject {
    static let shared = URLSchemeHandler()

    private init() {}

    func handle(_ url: URL) {
        guard url.scheme == "evidencenexus" else {
            print("Invalid URL scheme: \(url)")
            return
        }

        let host = url.host ?? ""

        switch host {
        case "query":
            handleQuery(url)
        case "export":
            handleExport(url)
        case "search":
            handleSearch(url)
        case "pattern":
            handlePattern(url)
        default:
            print("Unknown URL host: \(host)")
        }
    }

    private func handleQuery(_ url: URL) {
        guard let components = URLComponents(url: url, resolvingAgainstBaseURL: true),
              let queryItems = components.queryItems,
              let searchQuery = queryItems.first(where: { $0.name == "search" })?.value else {
            return
        }

        print("External query: \(searchQuery)")
        AuditLogger.shared.log(.searchPerformed, details: "External AI query: \(searchQuery)")

        // In production, would:
        // 1. Search evidence database
        // 2. Return results as JSON
        // 3. Use URL callback to respond
    }

    private func handleExport(_ url: URL) {
        guard let components = URLComponents(url: url, resolvingAgainstBaseURL: true),
              let queryItems = components.queryItems,
              let format = queryItems.first(where: { $0.name == "format" })?.value else {
            return
        }

        print("Export request: \(format)")
        AuditLogger.shared.log(.evidenceExported, details: "External export request: \(format)")

        // In production, would generate and return export bundle
    }

    private func handleSearch(_ url: URL) {
        // Open app to search view
        print("Opening search view")
    }

    private func handlePattern(_ url: URL) {
        // Open app to patterns view
        print("Opening patterns view")
    }
}

// MARK: - URL Handling in App
extension EvidenceNexusApp {
    func setupURLHandling() {
        // In ScenePhase, would register URL handler
    }
}
