//
//  AIHubView.swift
//  EvidenceNexus
//
//  AI-powered analysis and export tools
//

import SwiftUI
import SwiftData

struct AIHubView: View {
    @Query private var allEvidence: [EvidenceItem]
    @Query private var patterns: [PatternFlag]
    @State private var generatedSummary = ""
    @State private var isGenerating = false
    @State private var selectedExportFormat: ExportFormat = .pdf
    @State private var showingExportSheet = false

    enum ExportFormat: String, CaseIterable {
        case pdf = "PDF Report"
        case json = "JSON Data"
        case timeline = "Timeline Document"
        case complaint = "Complaint Draft"
    }

    var body: some View {
        NavigationStack {
            ScrollView {
                VStack(spacing: 24) {
                    // Header
                    VStack(spacing: 8) {
                        Image(systemName: "sparkles")
                            .font(.system(size: 60))
                            .foregroundStyle(
                                LinearGradient(
                                    colors: [.blue, .purple],
                                    startPoint: .topLeading,
                                    endPoint: .bottomTrailing
                                )
                            )

                        Text("AI Hub")
                            .font(.title.bold())

                        Text("Generate insights and export evidence bundles")
                            .font(.caption)
                            .foregroundStyle(.secondary)
                            .multilineTextAlignment(.center)
                    }
                    .padding(.top)

                    // Statistics
                    HStack(spacing: 16) {
                        StatCard(title: "Evidence Items", value: "\(allEvidence.count)", color: .blue)
                        StatCard(title: "Patterns Found", value: "\(patterns.count)", color: .purple)
                        StatCard(title: "Critical Flags", value: "\(patterns.filter { $0.severity == .critical }.count)", color: .red)
                    }
                    .padding(.horizontal)

                    Divider()
                        .padding(.horizontal)

                    // Quick Actions
                    VStack(alignment: .leading, spacing: 16) {
                        Text("Quick Actions")
                            .font(.headline)
                            .padding(.horizontal)

                        AIActionButton(
                            title: "Generate Case Summary",
                            subtitle: "AI-powered overview of all evidence",
                            icon: "doc.text.fill",
                            color: .blue
                        ) {
                            generateSummary()
                        }

                        AIActionButton(
                            title: "Detect New Patterns",
                            subtitle: "Scan for deception, crimes, and inconsistencies",
                            icon: "waveform.path.ecg",
                            color: .purple
                        ) {
                            runPatternDetection()
                        }

                        AIActionButton(
                            title: "Timeline Analysis",
                            subtitle: "Find gaps and inconsistencies",
                            icon: "calendar.badge.clock",
                            color: .orange
                        ) {
                            analyzeTimeline()
                        }

                        AIActionButton(
                            title: "Export Evidence Bundle",
                            subtitle: "Create timestamped report",
                            icon: "square.and.arrow.up.fill",
                            color: .green
                        ) {
                            showingExportSheet = true
                        }
                    }

                    // Generated Summary
                    if !generatedSummary.isEmpty {
                        VStack(alignment: .leading, spacing: 12) {
                            HStack {
                                Text("Generated Summary")
                                    .font(.headline)

                                Spacer()

                                Button {
                                    UIPasteboard.general.string = generatedSummary
                                } label: {
                                    Image(systemName: "doc.on.doc")
                                        .font(.subheadline)
                                }
                            }

                            Text(generatedSummary)
                                .font(.body)
                                .foregroundStyle(.secondary)
                                .padding()
                                .background(Color(.systemGray6))
                                .cornerRadius(12)
                        }
                        .padding(.horizontal)
                    }

                    // AI Coordination
                    VStack(alignment: .leading, spacing: 12) {
                        Text("AI Team Coordination")
                            .font(.headline)
                            .padding(.horizontal)

                        AICoordinationCard(
                            title: "Siri Shortcuts",
                            subtitle: "Voice commands for quick evidence lookup",
                            icon: "mic.fill",
                            status: "Active"
                        )

                        AICoordinationCard(
                            title: "External AI Access",
                            subtitle: "Share with Claude, Grok via URL scheme",
                            icon: "link.circle.fill",
                            status: "Available"
                        )
                    }
                }
                .padding(.bottom)
            }
            .navigationTitle("AI Hub")
            .navigationBarTitleDisplayMode(.inline)
            .overlay {
                if isGenerating {
                    ProcessingOverlay(message: "Generating insights...")
                }
            }
            .sheet(isPresented: $showingExportSheet) {
                ExportSheet(format: $selectedExportFormat)
            }
        }
    }

    private func generateSummary() {
        isGenerating = true

        DispatchQueue.main.asyncAfter(deadline: .now() + 2) {
            generatedSummary = """
            CASE SUMMARY - EvidenceNexus
            Generated: \(Date().formatted(date: .long, time: .shortened))

            Total Evidence Items: \(allEvidence.count)
            Date Range: \(allEvidence.first?.date.formatted(date: .abbreviated, time: .omitted) ?? "N/A") to \(allEvidence.last?.date.formatted(date: .abbreviated, time: .omitted) ?? "N/A")

            PATTERN ANALYSIS:
            - Critical Flags: \(patterns.filter { $0.severity == .critical }.count)
            - High Priority: \(patterns.filter { $0.severity == .high }.count)
            - Deception Indicators: \(patterns.filter { $0.type == .deception }.count)
            - Obstruction Markers: \(patterns.filter { $0.type == .obstruction }.count)

            KEY FINDINGS:
            This analysis has identified multiple patterns of concern requiring immediate attention. Evidence suggests systematic issues warranting further investigation.

            RECOMMENDED ACTIONS:
            1. Review all critical-severity patterns
            2. Verify timeline inconsistencies
            3. Cross-reference with external documentation
            4. Consult with legal counsel

            This summary was generated by EvidenceNexus AI analysis. All findings should be reviewed by qualified legal professionals.
            """

            isGenerating = false
            AuditLogger.shared.log(.reportGenerated, details: "Case Summary")
        }
    }

    private func runPatternDetection() {
        isGenerating = true

        DispatchQueue.main.asyncAfter(deadline: .now() + 3) {
            // In real implementation, this would call PatternDetectionEngine
            isGenerating = false
        }
    }

    private func analyzeTimeline() {
        isGenerating = true

        DispatchQueue.main.asyncAfter(deadline: .now() + 2) {
            isGenerating = false
        }
    }
}

// MARK: - Stat Card
struct StatCard: View {
    let title: String
    let value: String
    let color: Color

    var body: some View {
        VStack(spacing: 8) {
            Text(value)
                .font(.title.bold())
                .foregroundStyle(color)

            Text(title)
                .font(.caption)
                .foregroundStyle(.secondary)
                .multilineTextAlignment(.center)
        }
        .frame(maxWidth: .infinity)
        .padding()
        .background(color.opacity(0.1))
        .cornerRadius(12)
    }
}

// MARK: - AI Action Button
struct AIActionButton: View {
    let title: String
    let subtitle: String
    let icon: String
    let color: Color
    let action: () -> Void

    var body: some View {
        Button(action: action) {
            HStack(spacing: 16) {
                Image(systemName: icon)
                    .font(.title2)
                    .foregroundStyle(color)
                    .frame(width: 50, height: 50)
                    .background(color.opacity(0.1))
                    .cornerRadius(10)

                VStack(alignment: .leading, spacing: 4) {
                    Text(title)
                        .font(.headline)
                        .foregroundStyle(.primary)

                    Text(subtitle)
                        .font(.caption)
                        .foregroundStyle(.secondary)
                }

                Spacer()

                Image(systemName: "chevron.right")
                    .foregroundStyle(.secondary)
            }
            .padding()
            .background(Color(.systemBackground))
            .cornerRadius(12)
            .shadow(color: .black.opacity(0.05), radius: 5, y: 2)
        }
        .buttonStyle(.plain)
        .padding(.horizontal)
    }
}

// MARK: - AI Coordination Card
struct AICoordinationCard: View {
    let title: String
    let subtitle: String
    let icon: String
    let status: String

    var body: some View {
        HStack(spacing: 16) {
            Image(systemName: icon)
                .font(.title3)
                .foregroundStyle(.blue)
                .frame(width: 44, height: 44)
                .background(Color.blue.opacity(0.1))
                .cornerRadius(8)

            VStack(alignment: .leading, spacing: 4) {
                Text(title)
                    .font(.subheadline.bold())

                Text(subtitle)
                    .font(.caption)
                    .foregroundStyle(.secondary)
            }

            Spacer()

            Text(status)
                .font(.caption)
                .padding(.horizontal, 8)
                .padding(.vertical, 4)
                .background(Color.green.opacity(0.2))
                .foregroundStyle(.green)
                .cornerRadius(6)
        }
        .padding()
        .background(Color(.systemBackground))
        .cornerRadius(12)
        .shadow(color: .black.opacity(0.05), radius: 5, y: 2)
        .padding(.horizontal)
    }
}

// MARK: - Export Sheet
struct ExportSheet: View {
    @Binding var format: AIHubView.ExportFormat
    @Environment(\.dismiss) private var dismiss

    var body: some View {
        NavigationStack {
            List {
                Section("Export Format") {
                    ForEach(AIHubView.ExportFormat.allCases, id: \.self) { exportFormat in
                        Button {
                            format = exportFormat
                        } label: {
                            HStack {
                                Text(exportFormat.rawValue)
                                Spacer()
                                if format == exportFormat {
                                    Image(systemName: "checkmark")
                                        .foregroundStyle(.blue)
                                }
                            }
                        }
                        .foregroundStyle(.primary)
                    }
                }

                Section("Options") {
                    Toggle("Include Patterns", isOn: .constant(true))
                    Toggle("Include Audit Log", isOn: .constant(false))
                    Toggle("Redact Sensitive Info", isOn: .constant(false))
                }
            }
            .navigationTitle("Export Evidence")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button("Cancel") {
                        dismiss()
                    }
                }

                ToolbarItem(placement: .confirmationAction) {
                    Button("Export") {
                        exportEvidence()
                        dismiss()
                    }
                }
            }
        }
    }

    private func exportEvidence() {
        AuditLogger.shared.log(.evidenceExported, details: format.rawValue)
        // In real implementation, would generate and share the export
    }
}
