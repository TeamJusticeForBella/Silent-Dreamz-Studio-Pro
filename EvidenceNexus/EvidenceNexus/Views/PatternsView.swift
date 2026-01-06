//
//  PatternsView.swift
//  EvidenceNexus
//
//  Display detected patterns and anomalies
//

import SwiftUI
import SwiftData

struct PatternsView: View {
    @Query(sort: \PatternFlag.detectedAt, order: .reverse) private var patterns: [PatternFlag]
    @State private var selectedSeverity: SeverityLevel?
    @State private var selectedType: PatternType?
    @State private var showVerifiedOnly = false

    var filteredPatterns: [PatternFlag] {
        var items = patterns

        if let severity = selectedSeverity {
            items = items.filter { $0.severity == severity }
        }

        if let type = selectedType {
            items = items.filter { $0.type == type }
        }

        if showVerifiedOnly {
            items = items.filter { $0.isUserVerified }
        }

        return items
    }

    var severityCounts: [SeverityLevel: Int] {
        Dictionary(grouping: patterns) { $0.severity }
            .mapValues { $0.count }
    }

    var body: some View {
        NavigationStack {
            VStack(spacing: 0) {
                // Header Stats
                ScrollView(.horizontal, showsIndicators: false) {
                    HStack(spacing: 12) {
                        ForEach(SeverityLevel.allCases, id: \.self) { severity in
                            SeverityCard(
                                severity: severity,
                                count: severityCounts[severity] ?? 0,
                                isSelected: selectedSeverity == severity
                            ) {
                                selectedSeverity = selectedSeverity == severity ? nil : severity
                            }
                        }
                    }
                    .padding()
                }
                .background(Color(.systemBackground))

                // Type Filter
                ScrollView(.horizontal, showsIndicators: false) {
                    HStack(spacing: 8) {
                        FilterChip(title: "All", isSelected: selectedType == nil) {
                            selectedType = nil
                        }

                        ForEach(PatternType.allCases.prefix(8), id: \.self) { type in
                            FilterChip(
                                title: type.rawValue,
                                icon: type.iconName,
                                isSelected: selectedType == type
                            ) {
                                selectedType = selectedType == type ? nil : type
                            }
                        }
                    }
                    .padding(.horizontal)
                    .padding(.vertical, 8)
                }

                Divider()

                // Patterns List
                if filteredPatterns.isEmpty {
                    EmptyPatternsView()
                } else {
                    List(filteredPatterns) { pattern in
                        PatternRow(pattern: pattern)
                    }
                    .listStyle(.plain)
                }
            }
            .navigationTitle("Patterns (\(filteredPatterns.count))")
            .toolbar {
                ToolbarItem(placement: .primaryAction) {
                    Button {
                        showVerifiedOnly.toggle()
                    } label: {
                        Image(systemName: showVerifiedOnly ? "checkmark.circle.fill" : "checkmark.circle")
                    }
                }
            }
        }
    }
}

// MARK: - Severity Card
struct SeverityCard: View {
    let severity: SeverityLevel
    let count: Int
    let isSelected: Bool
    let action: () -> Void

    var body: some View {
        Button(action: action) {
            VStack(spacing: 8) {
                HStack(spacing: 4) {
                    Circle()
                        .fill(Color(severity.color))
                        .frame(width: 8, height: 8)
                    Text(severity.rawValue)
                        .font(.caption.bold())
                }

                Text("\(count)")
                    .font(.title2.bold())
                    .foregroundStyle(isSelected ? .white : .primary)
            }
            .frame(width: 80)
            .padding()
            .background(isSelected ? Color(severity.color) : Color(severity.color).opacity(0.1))
            .cornerRadius(12)
        }
        .buttonStyle(.plain)
    }
}

// MARK: - Pattern Row
struct PatternRow: View {
    let pattern: PatternFlag
    @State private var showingDetail = false
    @Environment(\.modelContext) private var modelContext

    var body: some View {
        Button {
            showingDetail = true
        } label: {
            VStack(alignment: .leading, spacing: 12) {
                HStack {
                    Image(systemName: pattern.type.iconName)
                        .foregroundStyle(Color(pattern.type.color))

                    Text(pattern.type.rawValue)
                        .font(.headline)

                    Spacer()

                    HStack(spacing: 4) {
                        Image(systemName: "sparkles")
                            .font(.caption2)
                        Text(String(format: "%.0f%%", pattern.confidence * 100))
                            .font(.caption)
                    }
                    .foregroundStyle(.secondary)
                }

                Text(pattern.explanation)
                    .font(.subheadline)
                    .foregroundStyle(.secondary)
                    .lineLimit(2)

                HStack {
                    Label("\(pattern.evidenceIDs.count) items", systemImage: "doc.fill")
                        .font(.caption)
                        .foregroundStyle(.secondary)

                    Spacer()

                    HStack(spacing: 4) {
                        Circle()
                            .fill(Color(pattern.severity.color))
                            .frame(width: 6, height: 6)
                        Text(pattern.severity.rawValue)
                            .font(.caption)
                    }

                    if pattern.isUserVerified {
                        Image(systemName: "checkmark.seal.fill")
                            .foregroundStyle(.blue)
                            .font(.caption)
                    }

                    Text(pattern.detectedAt.formatted(date: .abbreviated, time: .omitted))
                        .font(.caption)
                        .foregroundStyle(.secondary)
                }

                if !pattern.keywords.isEmpty {
                    ScrollView(.horizontal, showsIndicators: false) {
                        HStack(spacing: 6) {
                            ForEach(pattern.keywords.prefix(5), id: \.self) { keyword in
                                Text(keyword)
                                    .font(.caption2)
                                    .padding(.horizontal, 6)
                                    .padding(.vertical, 2)
                                    .background(Color.orange.opacity(0.2))
                                    .cornerRadius(4)
                            }
                        }
                    }
                }
            }
            .padding()
            .background(Color(.systemBackground))
            .cornerRadius(12)
        }
        .buttonStyle(.plain)
        .sheet(isPresented: $showingDetail) {
            PatternDetailView(pattern: pattern)
        }
    }
}

// MARK: - Pattern Detail View
struct PatternDetailView: View {
    let pattern: PatternFlag
    @Environment(\.dismiss) private var dismiss
    @Environment(\.modelContext) private var modelContext
    @Query private var allEvidence: [EvidenceItem]

    var relatedEvidence: [EvidenceItem] {
        allEvidence.filter { pattern.evidenceIDs.contains($0.id.uuidString) }
    }

    var body: some View {
        NavigationStack {
            ScrollView {
                VStack(alignment: .leading, spacing: 20) {
                    // Header
                    HStack {
                        Image(systemName: pattern.type.iconName)
                            .font(.largeTitle)
                            .foregroundStyle(Color(pattern.type.color))

                        VStack(alignment: .leading, spacing: 4) {
                            Text(pattern.type.rawValue)
                                .font(.title2.bold())

                            HStack {
                                Circle()
                                    .fill(Color(pattern.severity.color))
                                    .frame(width: 8, height: 8)
                                Text(pattern.severity.rawValue)
                                    .font(.subheadline)
                                    .foregroundStyle(.secondary)
                            }
                        }

                        Spacer()

                        VStack(alignment: .trailing, spacing: 4) {
                            Text(String(format: "%.0f%%", pattern.confidence * 100))
                                .font(.title3.bold())
                                .foregroundStyle(.blue)
                            Text("Confidence")
                                .font(.caption)
                                .foregroundStyle(.secondary)
                        }
                    }
                    .padding()

                    Divider()

                    // Explanation
                    VStack(alignment: .leading, spacing: 8) {
                        Text("Explanation")
                            .font(.headline)
                        Text(pattern.explanation)
                            .font(.body)
                            .foregroundStyle(.secondary)
                    }
                    .padding(.horizontal)

                    // Keywords
                    if !pattern.keywords.isEmpty {
                        VStack(alignment: .leading, spacing: 8) {
                            Text("Keywords Detected")
                                .font(.headline)

                            FlowLayout(spacing: 8) {
                                ForEach(pattern.keywords, id: \.self) { keyword in
                                    Text(keyword)
                                        .font(.subheadline)
                                        .padding(.horizontal, 12)
                                        .padding(.vertical, 6)
                                        .background(Color.orange.opacity(0.2))
                                        .cornerRadius(8)
                                }
                            }
                        }
                        .padding(.horizontal)
                    }

                    // Related Evidence
                    VStack(alignment: .leading, spacing: 12) {
                        Text("Related Evidence (\(relatedEvidence.count))")
                            .font(.headline)
                            .padding(.horizontal)

                        ForEach(relatedEvidence) { item in
                            EvidenceListRow(item: item)
                                .padding(.horizontal)
                        }
                    }

                    // Notes
                    if !pattern.notes.isEmpty {
                        VStack(alignment: .leading, spacing: 8) {
                            Text("Notes")
                                .font(.headline)
                            Text(pattern.notes)
                                .font(.body)
                                .foregroundStyle(.secondary)
                        }
                        .padding(.horizontal)
                    }

                    // Metadata
                    VStack(alignment: .leading, spacing: 8) {
                        Text("Detection Info")
                            .font(.headline)

                        MetadataRow(label: "Detected", value: pattern.detectedAt.formatted(date: .long, time: .shortened))
                        MetadataRow(label: "Status", value: pattern.isUserVerified ? "Verified" : "Pending Review")
                    }
                    .padding(.horizontal)
                }
                .padding(.bottom)
            }
            .navigationTitle("Pattern Details")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button("Close") {
                        dismiss()
                    }
                }

                ToolbarItem(placement: .primaryAction) {
                    Button {
                        toggleVerification()
                    } label: {
                        Image(systemName: pattern.isUserVerified ? "checkmark.circle.fill" : "checkmark.circle")
                    }
                }
            }
        }
    }

    private func toggleVerification() {
        pattern.isUserVerified.toggle()
        AuditLogger.shared.log(.patternVerified, details: pattern.type.rawValue)
        dismiss()
    }
}

// MARK: - Empty Patterns View
struct EmptyPatternsView: View {
    var body: some View {
        VStack(spacing: 16) {
            Image(systemName: "sparkles")
                .font(.system(size: 80))
                .foregroundStyle(.secondary)

            Text("No Patterns Detected")
                .font(.title2.bold())

            Text("AI analysis will detect patterns as you import more evidence")
                .font(.subheadline)
                .foregroundStyle(.secondary)
                .multilineTextAlignment(.center)
        }
        .padding()
        .frame(maxWidth: .infinity, maxHeight: .infinity)
    }
}
