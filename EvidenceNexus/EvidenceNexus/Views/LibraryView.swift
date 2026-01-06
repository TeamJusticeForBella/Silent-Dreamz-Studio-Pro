//
//  LibraryView.swift
//  EvidenceNexus
//
//  Browse and search all evidence
//

import SwiftUI
import SwiftData

struct LibraryView: View {
    @Environment(\.modelContext) private var modelContext
    @Query(sort: \EvidenceItem.date, order: .reverse) private var allEvidence: [EvidenceItem]

    @State private var searchText = ""
    @State private var selectedType: EvidenceType?
    @State private var selectedTag: String?
    @State private var viewMode: ViewMode = .grid
    @State private var selectedItem: EvidenceItem?

    enum ViewMode {
        case grid, list
    }

    var filteredEvidence: [EvidenceItem] {
        var items = allEvidence

        if !searchText.isEmpty {
            items = items.filter {
                $0.title.localizedCaseInsensitiveContains(searchText) ||
                $0.itemDescription.localizedCaseInsensitiveContains(searchText) ||
                $0.tags.contains { $0.localizedCaseInsensitiveContains(searchText) } ||
                ($0.ocrText?.localizedCaseInsensitiveContains(searchText) ?? false)
            }
        }

        if let type = selectedType {
            items = items.filter { $0.type == type }
        }

        if let tag = selectedTag {
            items = items.filter { $0.tags.contains(tag) }
        }

        return items
    }

    var body: some View {
        NavigationStack {
            VStack(spacing: 0) {
                // Filters
                ScrollView(.horizontal, showsIndicators: false) {
                    HStack(spacing: 12) {
                        FilterChip(
                            title: "All",
                            isSelected: selectedType == nil
                        ) {
                            selectedType = nil
                        }

                        ForEach(EvidenceType.allCases, id: \.self) { type in
                            FilterChip(
                                title: type.rawValue,
                                icon: type.iconName,
                                isSelected: selectedType == type
                            ) {
                                selectedType = selectedType == type ? nil : type
                            }
                        }
                    }
                    .padding()
                }
                .background(Color(.systemBackground))

                // Content
                if filteredEvidence.isEmpty {
                    EmptyLibraryView()
                } else {
                    Group {
                        if viewMode == .grid {
                            GridView(items: filteredEvidence, selectedItem: $selectedItem)
                        } else {
                            ListView(items: filteredEvidence, selectedItem: $selectedItem)
                        }
                    }
                }
            }
            .navigationTitle("Library (\(filteredEvidence.count))")
            .searchable(text: $searchText, prompt: "Search evidence...")
            .toolbar {
                ToolbarItem(placement: .primaryAction) {
                    Button {
                        withAnimation {
                            viewMode = viewMode == .grid ? .list : .grid
                        }
                    } label: {
                        Image(systemName: viewMode == .grid ? "list.bullet" : "square.grid.2x2")
                    }
                }
            }
            .sheet(item: $selectedItem) { item in
                EvidenceDetailView(item: item)
            }
        }
    }
}

// MARK: - Grid View
struct GridView: View {
    let items: [EvidenceItem]
    @Binding var selectedItem: EvidenceItem?

    let columns = [
        GridItem(.flexible()),
        GridItem(.flexible())
    ]

    var body: some View {
        ScrollView {
            LazyVGrid(columns: columns, spacing: 16) {
                ForEach(items) { item in
                    EvidenceCard(item: item)
                        .onTapGesture {
                            selectedItem = item
                            AuditLogger.shared.log(.evidenceViewed, evidenceID: item.id.uuidString)
                        }
                }
            }
            .padding()
        }
    }
}

// MARK: - List View
struct ListView: View {
    let items: [EvidenceItem]
    @Binding var selectedItem: EvidenceItem?

    var body: some View {
        List(items) { item in
            Button {
                selectedItem = item
                AuditLogger.shared.log(.evidenceViewed, evidenceID: item.id.uuidString)
            } label: {
                EvidenceListRow(item: item)
            }
            .buttonStyle(.plain)
        }
        .listStyle(.plain)
    }
}

// MARK: - Evidence Card
struct EvidenceCard: View {
    let item: EvidenceItem

    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            // Thumbnail
            ZStack {
                if let thumbnailData = item.thumbnailData,
                   let uiImage = UIImage(data: thumbnailData) {
                    Image(uiImage: uiImage)
                        .resizable()
                        .scaledToFill()
                } else {
                    Image(systemName: item.type.iconName)
                        .font(.system(size: 40))
                        .foregroundStyle(Color(item.type.color))
                }
            }
            .frame(height: 120)
            .frame(maxWidth: .infinity)
            .background(Color(item.type.color).opacity(0.1))
            .clipShape(RoundedRectangle(cornerRadius: 8))

            // Info
            VStack(alignment: .leading, spacing: 4) {
                Text(item.title)
                    .font(.headline)
                    .lineLimit(2)

                Text(item.date.formatted(date: .abbreviated, time: .omitted))
                    .font(.caption)
                    .foregroundStyle(.secondary)

                if !item.tags.isEmpty {
                    ScrollView(.horizontal, showsIndicators: false) {
                        HStack(spacing: 4) {
                            ForEach(item.tags.prefix(3), id: \.self) { tag in
                                Text(tag)
                                    .font(.caption2)
                                    .padding(.horizontal, 6)
                                    .padding(.vertical, 2)
                                    .background(Color.blue.opacity(0.2))
                                    .cornerRadius(4)
                            }
                        }
                    }
                }
            }
        }
        .padding(8)
        .background(Color(.systemBackground))
        .cornerRadius(12)
        .shadow(color: .black.opacity(0.1), radius: 5, y: 2)
    }
}

// MARK: - Evidence List Row
struct EvidenceListRow: View {
    let item: EvidenceItem

    var body: some View {
        HStack(spacing: 12) {
            Image(systemName: item.type.iconName)
                .font(.title2)
                .foregroundStyle(Color(item.type.color))
                .frame(width: 50, height: 50)
                .background(Color(item.type.color).opacity(0.1))
                .cornerRadius(8)

            VStack(alignment: .leading, spacing: 4) {
                Text(item.title)
                    .font(.headline)

                Text(item.itemDescription)
                    .font(.subheadline)
                    .foregroundStyle(.secondary)
                    .lineLimit(1)

                HStack {
                    Text(item.date.formatted(date: .abbreviated, time: .shortened))
                        .font(.caption)
                        .foregroundStyle(.secondary)

                    if let source = item.sourceAccount {
                        Text("•")
                            .foregroundStyle(.secondary)
                        Text(source)
                            .font(.caption)
                            .foregroundStyle(.secondary)
                    }
                }
            }

            Spacer()
        }
        .padding(.vertical, 4)
    }
}

// MARK: - Filter Chip
struct FilterChip: View {
    let title: String
    var icon: String?
    let isSelected: Bool
    let action: () -> Void

    var body: some View {
        Button(action: action) {
            HStack(spacing: 4) {
                if let icon = icon {
                    Image(systemName: icon)
                        .font(.caption)
                }
                Text(title)
                    .font(.subheadline)
            }
            .padding(.horizontal, 12)
            .padding(.vertical, 6)
            .background(isSelected ? Color.blue : Color.gray.opacity(0.2))
            .foregroundStyle(isSelected ? .white : .primary)
            .cornerRadius(16)
        }
    }
}

// MARK: - Empty Library View
struct EmptyLibraryView: View {
    var body: some View {
        VStack(spacing: 16) {
            Image(systemName: "folder")
                .font(.system(size: 80))
                .foregroundStyle(.secondary)

            Text("No Evidence Yet")
                .font(.title2.bold())

            Text("Import evidence from the Import tab to get started")
                .font(.subheadline)
                .foregroundStyle(.secondary)
                .multilineTextAlignment(.center)
        }
        .padding()
        .frame(maxWidth: .infinity, maxHeight: .infinity)
    }
}

// MARK: - Evidence Detail View
struct EvidenceDetailView: View {
    let item: EvidenceItem
    @Environment(\.dismiss) private var dismiss

    var body: some View {
        NavigationStack {
            ScrollView {
                VStack(alignment: .leading, spacing: 20) {
                    // Preview
                    if let fileURL = item.fileURL {
                        FilePreview(url: fileURL, type: item.type)
                    }

                    // Metadata
                    VStack(alignment: .leading, spacing: 12) {
                        Text(item.title)
                            .font(.title2.bold())

                        Text(item.itemDescription)
                            .font(.body)
                            .foregroundStyle(.secondary)

                        Divider()

                        MetadataRow(label: "Date", value: item.date.formatted(date: .long, time: .shortened))
                        MetadataRow(label: "Type", value: item.type.rawValue)
                        if let source = item.sourceAccount {
                            MetadataRow(label: "Source", value: source)
                        }
                        MetadataRow(label: "Imported", value: item.importedAt.formatted(date: .long, time: .shortened))

                        if !item.tags.isEmpty {
                            VStack(alignment: .leading, spacing: 8) {
                                Text("Tags")
                                    .font(.subheadline.bold())
                                    .foregroundStyle(.secondary)

                                FlowLayout(spacing: 8) {
                                    ForEach(item.tags, id: \.self) { tag in
                                        Text(tag)
                                            .font(.caption)
                                            .padding(.horizontal, 10)
                                            .padding(.vertical, 5)
                                            .background(Color.blue.opacity(0.2))
                                            .cornerRadius(8)
                                    }
                                }
                            }
                        }

                        if !item.notes.isEmpty {
                            Divider()

                            VStack(alignment: .leading, spacing: 8) {
                                Text("Notes")
                                    .font(.subheadline.bold())

                                Text(item.notes)
                                    .font(.body)
                            }
                        }

                        if let ocrText = item.ocrText, !ocrText.isEmpty {
                            Divider()

                            VStack(alignment: .leading, spacing: 8) {
                                Text("Extracted Text")
                                    .font(.subheadline.bold())

                                Text(ocrText)
                                    .font(.caption)
                                    .foregroundStyle(.secondary)
                            }
                        }
                    }
                    .padding()
                }
            }
            .navigationTitle("Evidence Details")
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

// MARK: - Metadata Row
struct MetadataRow: View {
    let label: String
    let value: String

    var body: some View {
        HStack {
            Text(label)
                .font(.subheadline.bold())
                .foregroundStyle(.secondary)
            Spacer()
            Text(value)
                .font(.subheadline)
        }
    }
}

// MARK: - File Preview
struct FilePreview: View {
    let url: URL
    let type: EvidenceType

    var body: some View {
        ZStack {
            Color.gray.opacity(0.1)

            Image(systemName: type.iconName)
                .font(.system(size: 60))
                .foregroundStyle(Color(type.color))
        }
        .frame(height: 200)
        .cornerRadius(12)
        .padding()
    }
}

// MARK: - Flow Layout
struct FlowLayout: Layout {
    var spacing: CGFloat = 8

    func sizeThatFits(proposal: ProposedViewSize, subviews: Subviews, cache: inout ()) -> CGSize {
        let sizes = subviews.map { $0.sizeThatFits(.unspecified) }
        var totalHeight: CGFloat = 0
        var totalWidth: CGFloat = 0
        var lineWidth: CGFloat = 0
        var lineHeight: CGFloat = 0

        for size in sizes {
            if lineWidth + size.width > proposal.width ?? 0 {
                totalHeight += lineHeight + spacing
                lineWidth = size.width
                lineHeight = size.height
            } else {
                lineWidth += size.width + spacing
                lineHeight = max(lineHeight, size.height)
            }
            totalWidth = max(totalWidth, lineWidth)
        }

        totalHeight += lineHeight
        return CGSize(width: totalWidth, height: totalHeight)
    }

    func placeSubviews(in bounds: CGRect, proposal: ProposedViewSize, subviews: Subviews, cache: inout ()) {
        var lineX = bounds.minX
        var lineY = bounds.minY
        var lineHeight: CGFloat = 0

        for subview in subviews {
            let size = subview.sizeThatFits(.unspecified)
            if lineX + size.width > bounds.maxX {
                lineX = bounds.minX
                lineY += lineHeight + spacing
                lineHeight = 0
            }

            subview.place(at: CGPoint(x: lineX, y: lineY), proposal: .unspecified)
            lineX += size.width + spacing
            lineHeight = max(lineHeight, size.height)
        }
    }
}
