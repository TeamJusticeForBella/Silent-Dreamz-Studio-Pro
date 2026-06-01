//
//  ImportManager.swift
//  EvidenceNexus
//
//  Manages evidence imports from all sources
//

import Foundation
import SwiftUI
import SwiftData
import Photos
import AVFoundation

class ImportManager: ObservableObject {
    @Published var recentImports: [EvidenceItem] = []
    @Published var showFilePicker = false

    private let fileManager = FileManager.default
    private let securityManager = SecurityManager()

    // Get app's evidence storage directory
    private var evidenceDirectory: URL {
        let documentsURL = fileManager.urls(for: .documentDirectory, in: .userDomainMask)[0]
        let evidenceURL = documentsURL.appendingPathComponent("Evidence", isDirectory: true)

        if !fileManager.fileExists(atPath: evidenceURL.path) {
            try? fileManager.createDirectory(at: evidenceURL, withIntermediateDirectories: true)
        }

        return evidenceURL
    }

    // MARK: - File Import
    func importFiles(urls: [URL], modelContext: ModelContext) {
        for url in urls {
            do {
                // Copy file to secure storage
                let fileName = url.lastPathComponent
                let destination = evidenceDirectory.appendingPathComponent(fileName)

                // Read original file data
                let data = try Data(contentsOf: url)

                // Calculate SHA-256 hash for integrity
                let hash = SecurityManager.sha256(data: data)

                // Copy (never move) to evidence directory
                try data.write(to: destination)

                // Determine type
                let type = determineEvidenceType(from: url)

                // Create evidence item
                let item = EvidenceItem(
                    title: fileName,
                    description: "Imported from Files",
                    date: Date(),
                    type: type,
                    fileURL: destination,
                    originalSource: "Files App"
                )
                item.sha256Hash = hash

                // Process with AI
                Task {
                    await processWithAI(item: item, fileURL: destination)
                }

                modelContext.insert(item)
                recentImports.insert(item, at: 0)

                AuditLogger.shared.log(.evidenceImported, evidenceID: item.id.uuidString, details: fileName)

            } catch {
                print("Failed to import file: \(error)")
            }
        }
    }

    // MARK: - Photos Library
    func importFromPhotos(modelContext: ModelContext, appState: AppState) {
        PHPhotoLibrary.requestAuthorization(for: .readWrite) { status in
            guard status == .authorized else {
                DispatchQueue.main.async {
                    appState.showError("Photos access denied")
                }
                return
            }

            DispatchQueue.main.async {
                // In production, would show photo picker
                appState.showProcessing("Importing photos...")
            }
        }
    }

    // MARK: - Voice Recording
    func startVoiceRecording(modelContext: ModelContext, appState: AppState) {
        AVAudioSession.sharedInstance().requestRecordPermission { granted in
            DispatchQueue.main.async {
                if granted {
                    // In production, would start audio recording
                    appState.showProcessing("Recording voice note...")
                } else {
                    appState.showError("Microphone access denied")
                }
            }
        }
    }

    // MARK: - Gmail
    func connectGmail(appState: AppState) {
        appState.showProcessing("Connecting to Gmail...")

        DispatchQueue.main.asyncAfter(deadline: .now() + 1) {
            appState.hideProcessing()
            appState.showError("Gmail integration requires GoogleSignIn SDK. See Package.swift.")
        }
    }

    // MARK: - Outlook
    func connectOutlook(appState: AppState) {
        appState.showProcessing("Connecting to Outlook...")

        DispatchQueue.main.asyncAfter(deadline: .now() + 1) {
            appState.hideProcessing()
            appState.showError("Outlook integration requires MSAL SDK. See Package.swift.")
        }
    }

    // MARK: - Facebook
    func connectFacebook(appState: AppState) {
        appState.showProcessing("Connecting to Facebook...")

        DispatchQueue.main.asyncAfter(deadline: .now() + 1) {
            appState.hideProcessing()
            appState.showError("Facebook integration requires Facebook SDK. See Package.swift.")
        }
    }

    // MARK: - Instagram
    func connectInstagram(appState: AppState) {
        appState.showProcessing("Connecting to Instagram...")

        DispatchQueue.main.asyncAfter(deadline: .now() + 1) {
            appState.hideProcessing()
            appState.showError("Instagram integration requires Meta Graph API. See Package.swift.")
        }
    }

    // MARK: - YouTube
    func importFromYouTube(urlString: String, title: String, notes: String, modelContext: ModelContext, appState: AppState) {
        let trimmed = urlString.trimmingCharacters(in: .whitespacesAndNewlines)
        guard let url = URL(string: trimmed),
              trimmed.contains("youtube.com") || trimmed.contains("youtu.be") else {
            appState.showError("Invalid YouTube URL. Please enter a valid youtube.com or youtu.be link.")
            return
        }

        let item = EvidenceItem(
            title: title.isEmpty ? "YouTube Video" : title,
            description: notes.isEmpty ? "Imported from YouTube" : notes,
            date: Date(),
            type: .video,
            fileURL: url,
            originalSource: "YouTube"
        )
        item.metadata["youtubeURL"] = trimmed
        item.metadata["platform"] = "YouTube"

        modelContext.insert(item)
        recentImports.insert(item, at: 0)

        AuditLogger.shared.log(.evidenceImported, evidenceID: item.id.uuidString, details: trimmed)
    }

    // MARK: - AI Processing
    private func processWithAI(item: EvidenceItem, fileURL: URL) async {
        // OCR for images and PDFs
        if item.type == .photo || item.type == .document {
            if let text = await OCRService.shared.extractText(from: fileURL) {
                item.ocrText = text
            }
        }

        // Transcription for audio/video
        if item.type == .audio || item.type == .video {
            if let transcript = await TranscriptionService.shared.transcribe(fileURL: fileURL) {
                item.ocrText = transcript
            }
        }

        // Generate thumbnail
        if let thumbnailData = await ThumbnailService.shared.generateThumbnail(for: fileURL, type: item.type) {
            item.thumbnailData = thumbnailData
        }

        // Facial recognition for photos/videos
        if item.type == .photo || item.type == .video {
            await FacialRecognitionService.shared.processFaces(in: fileURL)
        }
    }

    // MARK: - Helper Methods
    private func determineEvidenceType(from url: URL) -> EvidenceType {
        let ext = url.pathExtension.lowercased()

        switch ext {
        case "jpg", "jpeg", "png", "heic", "gif":
            return .photo
        case "mp4", "mov", "m4v", "avi":
            return .video
        case "mp3", "m4a", "wav", "aac":
            return .audio
        case "pdf", "doc", "docx", "txt", "rtf":
            return .document
        case "eml", "msg":
            return .email
        default:
            return .document
        }
    }
}
