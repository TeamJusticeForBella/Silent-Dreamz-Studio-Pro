//
//  TranscriptionService.swift
//  EvidenceNexus
//
//  On-device speech-to-text using Speech framework
//

import Foundation
import Speech
import AVFoundation

class TranscriptionService {
    static let shared = TranscriptionService()

    private let speechRecognizer = SFSpeechRecognizer(locale: Locale(identifier: "en-US"))

    private init() {}

    func transcribe(fileURL: URL) async -> String? {
        // Request authorization
        let authStatus = await requestAuthorization()
        guard authStatus == .authorized else {
            print("Speech recognition not authorized")
            return nil
        }

        // Create recognition request
        let request = SFSpeechURLRecognitionRequest(url: fileURL)
        request.shouldReportPartialResults = false
        request.requiresOnDeviceRecognition = true // Privacy: on-device only!

        return await withCheckedContinuation { continuation in
            speechRecognizer?.recognitionTask(with: request) { result, error in
                if let error = error {
                    print("Transcription error: \(error)")
                    continuation.resume(returning: nil)
                    return
                }

                if let result = result, result.isFinal {
                    let transcript = result.bestTranscription.formattedString
                    print("Transcription complete: \(transcript.prefix(100))...")
                    continuation.resume(returning: transcript)
                }
            }
        }
    }

    func transcribeWithSegments(fileURL: URL) async -> [TranscriptSegment]? {
        let authStatus = await requestAuthorization()
        guard authStatus == .authorized else { return nil }

        let request = SFSpeechURLRecognitionRequest(url: fileURL)
        request.shouldReportPartialResults = true
        request.requiresOnDeviceRecognition = true

        var segments: [TranscriptSegment] = []

        return await withCheckedContinuation { continuation in
            speechRecognizer?.recognitionTask(with: request) { result, error in
                if let error = error {
                    print("Transcription error: \(error)")
                    continuation.resume(returning: nil)
                    return
                }

                if let result = result {
                    for segment in result.bestTranscription.segments {
                        let transcriptSegment = TranscriptSegment(
                            text: segment.substring,
                            timestamp: segment.timestamp,
                            confidence: Double(segment.confidence),
                            speaker: nil // Speaker diarization requires additional processing
                        )
                        segments.append(transcriptSegment)
                    }

                    if result.isFinal {
                        continuation.resume(returning: segments)
                    }
                }
            }
        }
    }

    private func requestAuthorization() async -> SFSpeechRecognizerAuthorizationStatus {
        return await withCheckedContinuation { continuation in
            SFSpeechRecognizer.requestAuthorization { status in
                continuation.resume(returning: status)
            }
        }
    }

    func analyzeSentiment(text: String) -> String {
        // In production, would use NaturalLanguage framework
        // to analyze sentiment and emotional tone

        return "Neutral"
    }
}
