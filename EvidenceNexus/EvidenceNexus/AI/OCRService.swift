//
//  OCRService.swift
//  EvidenceNexus
//
//  On-device OCR using Vision framework
//

import Foundation
import Vision
import UIKit
import PDFKit

class OCRService {
    static let shared = OCRService()

    private init() {}

    func extractText(from fileURL: URL) async -> String? {
        let ext = fileURL.pathExtension.lowercased()

        if ext == "pdf" {
            return await extractTextFromPDF(fileURL)
        } else {
            return await extractTextFromImage(fileURL)
        }
    }

    private func extractTextFromImage(_ fileURL: URL) async -> String? {
        guard let image = UIImage(contentsOfFile: fileURL.path),
              let cgImage = image.cgImage else {
            return nil
        }

        let request = VNRecognizeTextRequest()
        request.recognitionLevel = .accurate
        request.usesLanguageCorrection = true
        request.recognitionLanguages = ["en-US"]

        let handler = VNImageRequestHandler(cgImage: cgImage, options: [:])

        do {
            try handler.perform([request])

            guard let observations = request.results else {
                return nil
            }

            let recognizedStrings = observations.compactMap { observation in
                observation.topCandidates(1).first?.string
            }

            let text = recognizedStrings.joined(separator: "\n")
            print("OCR extracted \(text.count) characters")

            return text.isEmpty ? nil : text

        } catch {
            print("OCR error: \(error)")
            return nil
        }
    }

    private func extractTextFromPDF(_ fileURL: URL) async -> String? {
        guard let pdfDocument = PDFDocument(url: fileURL) else {
            return nil
        }

        var fullText = ""

        for pageIndex in 0..<pdfDocument.pageCount {
            if let page = pdfDocument.page(at: pageIndex),
               let pageText = page.string {
                fullText += pageText + "\n"
            }
        }

        return fullText.isEmpty ? nil : fullText
    }
}

// MARK: - Thumbnail Service
class ThumbnailService {
    static let shared = ThumbnailService()

    private init() {}

    func generateThumbnail(for fileURL: URL, type: EvidenceType) async -> Data? {
        switch type {
        case .photo:
            return await generateImageThumbnail(fileURL)
        case .video:
            return await generateVideoThumbnail(fileURL)
        case .document:
            return await generateDocumentThumbnail(fileURL)
        default:
            return nil
        }
    }

    private func generateImageThumbnail(_ fileURL: URL) async -> Data? {
        guard let image = UIImage(contentsOfFile: fileURL.path) else {
            return nil
        }

        let targetSize = CGSize(width: 200, height: 200)
        let thumbnail = image.preparingThumbnail(of: targetSize)

        return thumbnail?.jpegData(compressionQuality: 0.7)
    }

    private func generateVideoThumbnail(_ fileURL: URL) async -> Data? {
        let asset = AVAsset(url: fileURL)
        let imageGenerator = AVAssetImageGenerator(asset: asset)
        imageGenerator.appliesPreferredTrackTransform = true

        let time = CMTime(seconds: 1, preferredTimescale: 60)

        do {
            let cgImage = try imageGenerator.copyCGImage(at: time, actualTime: nil)
            let thumbnail = UIImage(cgImage: cgImage)
            return thumbnail.jpegData(compressionQuality: 0.7)
        } catch {
            print("Video thumbnail error: \(error)")
            return nil
        }
    }

    private func generateDocumentThumbnail(_ fileURL: URL) async -> Data? {
        if fileURL.pathExtension.lowercased() == "pdf" {
            guard let pdfDocument = PDFDocument(url: fileURL),
                  let firstPage = pdfDocument.page(at: 0) else {
                return nil
            }

            let pageRect = firstPage.bounds(for: .mediaBox)
            let renderer = UIGraphicsImageRenderer(size: pageRect.size)

            let thumbnail = renderer.image { ctx in
                UIColor.white.set()
                ctx.fill(pageRect)

                ctx.cgContext.translateBy(x: 0, y: pageRect.size.height)
                ctx.cgContext.scaleBy(x: 1, y: -1)

                firstPage.draw(with: .mediaBox, to: ctx.cgContext)
            }

            return thumbnail.jpegData(compressionQuality: 0.7)
        }

        return nil
    }
}
