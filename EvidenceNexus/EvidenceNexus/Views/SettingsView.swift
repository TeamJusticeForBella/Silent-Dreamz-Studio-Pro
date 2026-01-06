//
//  SettingsView.swift
//  EvidenceNexus
//
//  App settings and account management
//

import SwiftUI
import SwiftData

struct SettingsView: View {
    @Environment(\.modelContext) private var modelContext
    @EnvironmentObject var securityManager: SecurityManager
    @Query private var auditLog: [AuditLogEntry]

    @State private var connectedAccounts: [ConnectedAccount] = []
    @State private var showingAuditLog = false
    @State private var showingAbout = false

    var body: some View {
        NavigationStack {
            List {
                // Connected Accounts
                Section("Connected Accounts") {
                    ForEach(connectedAccounts) { account in
                        AccountRow(account: account)
                    }

                    Button {
                        // Add new account
                    } label: {
                        Label("Connect New Account", systemImage: "plus.circle.fill")
                    }
                }

                // Security
                Section("Security") {
                    NavigationLink {
                        SecuritySettingsView()
                    } label: {
                        Label("Security Settings", systemImage: "lock.shield.fill")
                    }

                    Button {
                        showingAuditLog = true
                    } label: {
                        Label("Audit Log (\(auditLog.count))", systemImage: "list.bullet.clipboard.fill")
                            .foregroundStyle(.primary)
                    }
                }

                // Data Management
                Section("Data Management") {
                    NavigationLink {
                        StorageView()
                    } label: {
                        Label("Storage & Backup", systemImage: "internaldrive.fill")
                    }

                    Button(role: .destructive) {
                        // Export all data
                    } label: {
                        Label("Export All Data", systemImage: "square.and.arrow.up")
                    }
                }

                // Preset Tags
                Section("Quick Tags") {
                    NavigationLink {
                        PresetTagsView()
                    } label: {
                        Label("Manage Preset Tags", systemImage: "tag.fill")
                    }
                }

                // About
                Section {
                    Button {
                        showingAbout = true
                    } label: {
                        Label("About EvidenceNexus", systemImage: "info.circle.fill")
                            .foregroundStyle(.primary)
                    }

                    Link(destination: URL(string: "https://github.com/TeamJusticeForBella")!) {
                        Label("Team Justice For Bella", systemImage: "heart.fill")
                    }

                    Text("Version 1.0.0 (Build 1)")
                        .font(.caption)
                        .foregroundStyle(.secondary)
                }
            }
            .navigationTitle("Settings")
            .sheet(isPresented: $showingAuditLog) {
                AuditLogView(entries: auditLog)
            }
            .sheet(isPresented: $showingAbout) {
                AboutView()
            }
        }
    }
}

// MARK: - Connected Account
struct ConnectedAccount: Identifiable {
    let id = UUID()
    let type: String
    let email: String
    let isActive: Bool
}

// MARK: - Account Row
struct AccountRow: View {
    let account: ConnectedAccount

    var body: some View {
        HStack {
            Image(systemName: iconForAccountType(account.type))
                .foregroundStyle(colorForAccountType(account.type))

            VStack(alignment: .leading, spacing: 4) {
                Text(account.type)
                    .font(.headline)
                Text(account.email)
                    .font(.caption)
                    .foregroundStyle(.secondary)
            }

            Spacer()

            Circle()
                .fill(account.isActive ? Color.green : Color.gray)
                .frame(width: 8, height: 8)
        }
    }

    private func iconForAccountType(_ type: String) -> String {
        switch type {
        case "Gmail": return "envelope.fill"
        case "Outlook": return "envelope.badge.fill"
        case "Facebook": return "f.square.fill"
        case "Instagram": return "camera.fill"
        default: return "person.circle.fill"
        }
    }

    private func colorForAccountType(_ type: String) -> Color {
        switch type {
        case "Gmail": return .red
        case "Outlook": return .blue
        case "Facebook": return .indigo
        case "Instagram": return .pink
        default: return .gray
        }
    }
}

// MARK: - Security Settings View
struct SecuritySettingsView: View {
    @EnvironmentObject var securityManager: SecurityManager
    @State private var requireBiometrics = true
    @State private var autoLockMinutes = 5.0

    var body: some View {
        List {
            Section("Authentication") {
                Toggle("Require Face ID", isOn: $requireBiometrics)

                VStack(alignment: .leading, spacing: 8) {
                    Text("Auto-Lock After")
                        .font(.subheadline)

                    Slider(value: $autoLockMinutes, in: 1...30, step: 1)

                    Text("\(Int(autoLockMinutes)) minutes")
                        .font(.caption)
                        .foregroundStyle(.secondary)
                }
            }

            Section("Encryption") {
                HStack {
                    Text("Storage Encryption")
                    Spacer()
                    Image(systemName: "checkmark.circle.fill")
                        .foregroundStyle(.green)
                    Text("Active")
                        .font(.caption)
                        .foregroundStyle(.green)
                }
            }

            Section {
                Button("Lock App Now") {
                    securityManager.lock()
                }
            }
        }
        .navigationTitle("Security")
    }
}

// MARK: - Storage View
struct StorageView: View {
    var body: some View {
        List {
            Section("Usage") {
                HStack {
                    Text("Evidence Files")
                    Spacer()
                    Text("0 MB")
                        .foregroundStyle(.secondary)
                }

                HStack {
                    Text("Database")
                    Spacer()
                    Text("0 MB")
                        .foregroundStyle(.secondary)
                }

                HStack {
                    Text("Total")
                    Spacer()
                    Text("0 MB")
                        .font(.headline)
                }
            }

            Section("Backup") {
                Button {
                    // Create backup
                } label: {
                    Label("Create Backup", systemImage: "arrow.clockwise.circle.fill")
                }

                Button {
                    // Restore from backup
                } label: {
                    Label("Restore from Backup", systemImage: "arrow.counterclockwise.circle.fill")
                }
            }
        }
        .navigationTitle("Storage")
    }
}

// MARK: - Preset Tags View
struct PresetTagsView: View {
    @State private var presetTags = [
        "Koohanim", "Forrey-Baker", "Davis",
        "Obstruction", "Redaction", "Foster Neglect",
        "False Statement", "Timeline Issue", "Missing Evidence"
    ]

    var body: some View {
        List {
            Section("Key Defendants") {
                ForEach(["Koohanim", "Forrey-Baker", "Davis"], id: \.self) { tag in
                    TagRow(tag: tag)
                }
            }

            Section("Common Themes") {
                ForEach(["Obstruction", "Redaction", "Foster Neglect", "False Statement", "Timeline Issue", "Missing Evidence"], id: \.self) { tag in
                    TagRow(tag: tag)
                }
            }

            Section {
                Button {
                    // Add new tag
                } label: {
                    Label("Add Custom Tag", systemImage: "plus.circle.fill")
                }
            }
        }
        .navigationTitle("Preset Tags")
    }
}

struct TagRow: View {
    let tag: String

    var body: some View {
        HStack {
            Text(tag)
            Spacer()
            Image(systemName: "tag.fill")
                .foregroundStyle(.blue)
        }
    }
}

// MARK: - Audit Log View
struct AuditLogView: View {
    let entries: [AuditLogEntry]
    @Environment(\.dismiss) private var dismiss

    var body: some View {
        NavigationStack {
            List(entries.sorted { $0.timestamp > $1.timestamp }) { entry in
                VStack(alignment: .leading, spacing: 6) {
                    HStack {
                        Text(entry.action.rawValue)
                            .font(.headline)

                        Spacer()

                        Text(entry.timestamp.formatted(date: .omitted, time: .shortened))
                            .font(.caption)
                            .foregroundStyle(.secondary)
                    }

                    if !entry.details.isEmpty {
                        Text(entry.details)
                            .font(.caption)
                            .foregroundStyle(.secondary)
                    }

                    Text(entry.deviceInfo)
                        .font(.caption2)
                        .foregroundStyle(.tertiary)
                }
                .padding(.vertical, 4)
            }
            .navigationTitle("Audit Log")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .confirmationAction) {
                    Button("Done") {
                        dismiss()
                    }
                }

                ToolbarItem(placement: .primaryAction) {
                    Button {
                        exportAuditLog()
                    } label: {
                        Image(systemName: "square.and.arrow.up")
                    }
                }
            }
        }
    }

    private func exportAuditLog() {
        AuditLogger.shared.log(.evidenceExported, details: "Audit Log")
    }
}

// MARK: - About View
struct AboutView: View {
    @Environment(\.dismiss) private var dismiss

    var body: some View {
        NavigationStack {
            ScrollView {
                VStack(spacing: 24) {
                    Image(systemName: "shield.checkered")
                        .font(.system(size: 80))
                        .foregroundStyle(
                            LinearGradient(
                                colors: [.blue, .purple],
                                startPoint: .topLeading,
                                endPoint: .bottomTrailing
                            )
                        )

                    Text("EvidenceNexus")
                        .font(.largeTitle.bold())

                    Text("Version 1.0.0")
                        .font(.subheadline)
                        .foregroundStyle(.secondary)

                    Divider()
                        .padding(.horizontal)

                    VStack(alignment: .leading, spacing: 16) {
                        Text("About")
                            .font(.headline)

                        Text("EvidenceNexus is a secure, private, on-device evidence management system designed for high-stakes legal cases. Built with privacy, integrity, and justice in mind.")
                            .font(.body)
                            .foregroundStyle(.secondary)

                        Text("For Justice, For Bella")
                            .font(.headline)
                            .foregroundStyle(.blue)
                            .padding(.top)
                    }
                    .padding(.horizontal)

                    Divider()
                        .padding(.horizontal)

                    VStack(spacing: 12) {
                        Text("Built with")
                            .font(.caption)
                            .foregroundStyle(.secondary)

                        HStack(spacing: 8) {
                            TechBadge(text: "Swift")
                            TechBadge(text: "SwiftUI")
                            TechBadge(text: "SwiftData")
                            TechBadge(text: "Vision")
                            TechBadge(text: "Core ML")
                        }
                    }
                }
                .padding()
            }
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .confirmationAction) {
                    Button("Done") {
                        dismiss()
                    }
                }
            }
        }
    }
}

struct TechBadge: View {
    let text: String

    var body: some View {
        Text(text)
            .font(.caption2)
            .padding(.horizontal, 8)
            .padding(.vertical, 4)
            .background(Color.blue.opacity(0.2))
            .cornerRadius(4)
    }
}
