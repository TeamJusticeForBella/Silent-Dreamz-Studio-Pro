//
//  ImportsView.swift
//  EvidenceNexus
//
//  Import evidence from various sources
//

import SwiftUI
import SwiftData
import UniformTypeIdentifiers

struct ImportsView: View {
    @Environment(\.modelContext) private var modelContext
    @EnvironmentObject var appState: AppState
    @StateObject private var importManager = ImportManager()

    let connectors: [(String, String, String, Color)] = [
        ("Gmail", "envelope.fill", "Import from Gmail", .red),
        ("Outlook", "envelope.badge.fill", "Import from Outlook", .blue),
        ("Facebook", "f.square.fill", "Import from Facebook", .indigo),
        ("Instagram", "camera.fill", "Import from Instagram", .pink),
        ("Photos", "photo.on.rectangle", "Import from Photos", .purple),
        ("Files", "folder.fill", "Import documents", .orange),
        ("Voice Note", "mic.circle.fill", "Record voice note", .mint)
    ]

    var body: some View {
        NavigationStack {
            ScrollView {
                VStack(spacing: 24) {
                    // Header
                    VStack(spacing: 8) {
                        Image(systemName: "square.and.arrow.down.on.square")
                            .font(.system(size: 60))
                            .foregroundStyle(.blue)

                        Text("Import Evidence")
                            .font(.title.bold())

                        Text("All imports are copied, never moved. Original sources remain intact.")
                            .font(.caption)
                            .foregroundStyle(.secondary)
                            .multilineTextAlignment(.center)
                            .padding(.horizontal)
                    }
                    .padding(.top)

                    // Connectors Grid
                    LazyVGrid(columns: [
                        GridItem(.flexible()),
                        GridItem(.flexible())
                    ], spacing: 16) {
                        ForEach(connectors, id: \.0) { connector in
                            ConnectorButton(
                                title: connector.0,
                                icon: connector.1,
                                subtitle: connector.2,
                                color: connector.3
                            ) {
                                handleConnectorTap(connector.0)
                            }
                        }
                    }
                    .padding(.horizontal)

                    // Drag and Drop Zone
                    DropZone { urls in
                        importManager.importFiles(urls: urls, modelContext: modelContext)
                    }
                    .padding(.horizontal)

                    // Recent Imports
                    if !importManager.recentImports.isEmpty {
                        VStack(alignment: .leading, spacing: 12) {
                            Text("Recent Imports")
                                .font(.headline)
                                .padding(.horizontal)

                            ForEach(importManager.recentImports) { item in
                                RecentImportRow(item: item)
                            }
                        }
                        .padding(.top)
                    }
                }
                .padding(.bottom)
            }
            .navigationTitle("Import")
            .navigationBarTitleDisplayMode(.inline)
        }
    }

    private func handleConnectorTap(_ connector: String) {
        switch connector {
        case "Gmail":
            importManager.connectGmail(appState: appState)
        case "Outlook":
            importManager.connectOutlook(appState: appState)
        case "Facebook":
            importManager.connectFacebook(appState: appState)
        case "Instagram":
            importManager.connectInstagram(appState: appState)
        case "Photos":
            importManager.importFromPhotos(modelContext: modelContext, appState: appState)
        case "Files":
            importManager.showFilePicker = true
        case "Voice Note":
            importManager.startVoiceRecording(modelContext: modelContext, appState: appState)
        default:
            break
        }
    }
}

// MARK: - Connector Button
struct ConnectorButton: View {
    let title: String
    let icon: String
    let subtitle: String
    let color: Color
    let action: () -> Void

    var body: some View {
        Button(action: action) {
            VStack(spacing: 12) {
                Image(systemName: icon)
                    .font(.system(size: 40))
                    .foregroundStyle(color)

                VStack(spacing: 4) {
                    Text(title)
                        .font(.headline)
                        .foregroundStyle(.primary)

                    Text(subtitle)
                        .font(.caption2)
                        .foregroundStyle(.secondary)
                        .multilineTextAlignment(.center)
                }
            }
            .frame(maxWidth: .infinity)
            .padding()
            .background(color.opacity(0.1))
            .cornerRadius(12)
        }
        .buttonStyle(.plain)
    }
}

// MARK: - Drop Zone
struct DropZone: View {
    let onDrop: ([URL]) -> Void
    @State private var isTargeted = false

    var body: some View {
        VStack(spacing: 16) {
            Image(systemName: "arrow.down.doc.fill")
                .font(.system(size: 50))
                .foregroundStyle(isTargeted ? .blue : .secondary)

            Text("Drag & Drop Files Here")
                .font(.headline)
                .foregroundStyle(isTargeted ? .blue : .primary)

            Text("Documents, photos, videos, and audio files")
                .font(.caption)
                .foregroundStyle(.secondary)
        }
        .frame(maxWidth: .infinity)
        .frame(height: 150)
        .background(
            RoundedRectangle(cornerRadius: 16)
                .strokeBorder(
                    isTargeted ? Color.blue : Color.gray.opacity(0.3),
                    style: StrokeStyle(lineWidth: 2, dash: [10])
                )
        )
        .background(
            RoundedRectangle(cornerRadius: 16)
                .fill(isTargeted ? Color.blue.opacity(0.1) : Color.clear)
        )
        .onDrop(of: [.fileURL], isTargeted: $isTargeted) { providers in
            handleDrop(providers: providers)
            return true
        }
    }

    private func handleDrop(providers: [NSItemProvider]) {
        var urls: [URL] = []

        let group = DispatchGroup()

        for provider in providers {
            group.enter()
            _ = provider.loadObject(ofClass: URL.self) { url, error in
                if let url = url {
                    urls.append(url)
                }
                group.leave()
            }
        }

        group.notify(queue: .main) {
            if !urls.isEmpty {
                onDrop(urls)
            }
        }
    }
}

// MARK: - Recent Import Row
struct RecentImportRow: View {
    let item: EvidenceItem

    var body: some View {
        HStack(spacing: 12) {
            Image(systemName: item.type.iconName)
                .font(.title2)
                .foregroundStyle(Color(item.type.color))
                .frame(width: 44, height: 44)
                .background(Color(item.type.color).opacity(0.1))
                .cornerRadius(8)

            VStack(alignment: .leading, spacing: 4) {
                Text(item.title)
                    .font(.headline)
                    .lineLimit(1)

                Text(item.date.formatted(date: .abbreviated, time: .shortened))
                    .font(.caption)
                    .foregroundStyle(.secondary)
            }

            Spacer()

            Image(systemName: "checkmark.circle.fill")
                .foregroundStyle(.green)
        }
        .padding()
        .background(Color(.systemBackground))
        .cornerRadius(12)
        .shadow(color: .black.opacity(0.05), radius: 5, y: 2)
        .padding(.horizontal)
    }
}
