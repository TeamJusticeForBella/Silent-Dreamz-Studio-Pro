//
//  TimelineView.swift
//  EvidenceNexus
//
//  Chronological timeline with anomaly detection
//

import SwiftUI
import SwiftData

struct TimelineView: View {
    @Query(sort: \EvidenceItem.date, order: .reverse) private var allEvidence: [EvidenceItem]
    @Query private var patterns: [PatternFlag]

    @State private var selectedDate: Date?
    @State private var showingAnomaliesOnly = false

    var groupedEvidence: [(Date, [EvidenceItem])] {
        let calendar = Calendar.current
        let grouped = Dictionary(grouping: allEvidence) { item in
            calendar.startOfDay(for: item.date)
        }
        return grouped.sorted { $0.key > $1.key }
    }

    var anomalyDates: Set<Date> {
        let calendar = Calendar.current
        var dates = Set<Date>()

        for pattern in patterns where pattern.type == .inconsistency {
            for evidenceID in pattern.evidenceIDs {
                if let item = allEvidence.first(where: { $0.id.uuidString == evidenceID }) {
                    dates.insert(calendar.startOfDay(for: item.date))
                }
            }
        }

        return dates
    }

    var body: some View {
        NavigationStack {
            ScrollView {
                VStack(spacing: 0) {
                    // Timeline Header
                    HStack {
                        VStack(alignment: .leading, spacing: 4) {
                            Text("Evidence Timeline")
                                .font(.title2.bold())
                            Text("\(allEvidence.count) items across \(groupedEvidence.count) days")
                                .font(.caption)
                                .foregroundStyle(.secondary)
                        }

                        Spacer()

                        Toggle(isOn: $showingAnomaliesOnly) {
                            Label("Anomalies", systemImage: "exclamationmark.triangle.fill")
                                .font(.caption)
                        }
                        .toggleStyle(.button)
                        .tint(.orange)
                    }
                    .padding()

                    // Timeline
                    ForEach(groupedEvidence, id: \.0) { date, items in
                        if !showingAnomaliesOnly || anomalyDates.contains(date) {
                            TimelineDay(
                                date: date,
                                items: items,
                                hasAnomaly: anomalyDates.contains(date)
                            )
                        }
                    }
                }
            }
            .navigationTitle("Timeline")
            .navigationBarTitleDisplayMode(.inline)
        }
    }
}

// MARK: - Timeline Day
struct TimelineDay: View {
    let date: Date
    let items: [EvidenceItem]
    let hasAnomaly: Bool

    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            // Date Header
            HStack {
                Circle()
                    .fill(hasAnomaly ? Color.orange : Color.blue)
                    .frame(width: 12, height: 12)

                Text(date.formatted(date: .complete, time: .omitted))
                    .font(.headline)

                if hasAnomaly {
                    Image(systemName: "exclamationmark.triangle.fill")
                        .foregroundStyle(.orange)
                }

                Spacer()

                Text("\(items.count)")
                    .font(.caption)
                    .foregroundStyle(.secondary)
            }
            .padding(.horizontal)
            .padding(.top, 8)

            // Items
            VStack(spacing: 8) {
                ForEach(items) { item in
                    TimelineItem(item: item)
                }
            }
            .padding(.leading, 30)
            .padding(.trailing)
            .padding(.bottom, 16)

            Divider()
                .padding(.leading, 30)
        }
    }
}

// MARK: - Timeline Item
struct TimelineItem: View {
    let item: EvidenceItem
    @State private var showingDetail = false

    var body: some View {
        Button {
            showingDetail = true
        } label: {
            HStack(spacing: 12) {
                Image(systemName: item.type.iconName)
                    .font(.title3)
                    .foregroundStyle(Color(item.type.color))
                    .frame(width: 40, height: 40)
                    .background(Color(item.type.color).opacity(0.1))
                    .cornerRadius(8)

                VStack(alignment: .leading, spacing: 4) {
                    Text(item.title)
                        .font(.subheadline.bold())
                        .foregroundStyle(.primary)

                    Text(item.date.formatted(date: .omitted, time: .shortened))
                        .font(.caption)
                        .foregroundStyle(.secondary)
                }

                Spacer()

                Image(systemName: "chevron.right")
                    .font(.caption)
                    .foregroundStyle(.secondary)
            }
            .padding(12)
            .background(Color(.systemBackground))
            .cornerRadius(10)
            .shadow(color: .black.opacity(0.05), radius: 3, y: 1)
        }
        .buttonStyle(.plain)
        .sheet(isPresented: $showingDetail) {
            EvidenceDetailView(item: item)
        }
    }
}
