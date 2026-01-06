//
//  PatternDetectionEngine.swift
//  EvidenceNexus
//
//  On-device pattern detection using NaturalLanguage framework
//

import Foundation
import NaturalLanguage
import SwiftData

class PatternDetectionEngine {
    static let shared = PatternDetectionEngine()

    private init() {}

    // MARK: - Pattern Detection Keywords
    private let deceptionKeywords = [
        "honestly", "to be honest", "to tell you the truth", "believe me",
        "I think", "maybe", "possibly", "I don't recall", "as far as I know"
    ]

    private let crimeKeywords = [
        "falsified", "forged", "fabricated", "lied", "deceived",
        "trafficking", "exploitation", "abuse", "neglect", "assault",
        "kidnapping", "endangerment", "maltreatment"
    ]

    private let obstructionKeywords = [
        "redacted", "withheld", "concealed", "hidden", "destroyed",
        "delayed", "refused", "denied access", "blocked", "prevented"
    ]

    private let neglectKeywords = [
        "infection", "untreated", "malnourished", "unsupervised",
        "unsafe conditions", "medical neglect", "failure to provide",
        "abandoned", "inadequate care"
    ]

    private let misconductKeywords = [
        "attorney misconduct", "failure to disclose", "conflict of interest",
        "ethical violation", "professional misconduct", "breach of duty"
    ]

    // MARK: - Analyze Text
    func analyzeText(_ text: String, evidenceID: String, modelContext: ModelContext) async {
        let lowercasedText = text.lowercased()

        // Detect deception patterns
        if let deceptionFlag = detectDeception(in: lowercasedText, evidenceID: evidenceID) {
            modelContext.insert(deceptionFlag)
        }

        // Detect crime indicators
        if let crimeFlag = detectCrime(in: lowercasedText, evidenceID: evidenceID) {
            modelContext.insert(crimeFlag)
        }

        // Detect obstruction
        if let obstructionFlag = detectObstruction(in: lowercasedText, evidenceID: evidenceID) {
            modelContext.insert(obstructionFlag)
        }

        // Detect neglect
        if let neglectFlag = detectNeglect(in: lowercasedText, evidenceID: evidenceID) {
            modelContext.insert(neglectFlag)
        }

        // Detect attorney misconduct
        if let misconductFlag = detectMisconduct(in: lowercasedText, evidenceID: evidenceID) {
            modelContext.insert(misconductFlag)
        }

        // Sentiment analysis
        analyzeSentiment(text)
    }

    // MARK: - Deception Detection
    private func detectDeception(in text: String, evidenceID: String) -> PatternFlag? {
        var matchedKeywords: [String] = []
        var score = 0.0

        for keyword in deceptionKeywords {
            if text.contains(keyword) {
                matchedKeywords.append(keyword)
                score += 0.1
            }
        }

        // Check for hedging language patterns
        let hedgingPatterns = ["I believe", "I think", "maybe", "possibly", "I guess"]
        for pattern in hedgingPatterns {
            if text.contains(pattern) {
                score += 0.15
            }
        }

        guard score > 0.3 else { return nil }

        return PatternFlag(
            type: .deception,
            confidence: min(score, 1.0),
            evidenceIDs: [evidenceID],
            explanation: "Detected hedging language and deception indicators: \(matchedKeywords.joined(separator: ", "))",
            keywords: matchedKeywords,
            severity: score > 0.7 ? .high : .medium
        )
    }

    // MARK: - Crime Detection
    private func detectCrime(in text: String, evidenceID: String) -> PatternFlag? {
        var matchedKeywords: [String] = []

        for keyword in crimeKeywords {
            if text.contains(keyword) {
                matchedKeywords.append(keyword)
            }
        }

        guard !matchedKeywords.isEmpty else { return nil }

        let confidence = min(Double(matchedKeywords.count) * 0.3, 1.0)

        return PatternFlag(
            type: .crime,
            confidence: confidence,
            evidenceIDs: [evidenceID],
            explanation: "Detected criminal activity indicators related to foster care abuse and neglect",
            keywords: matchedKeywords,
            severity: .critical
        )
    }

    // MARK: - Obstruction Detection
    private func detectObstruction(in text: String, evidenceID: String) -> PatternFlag? {
        var matchedKeywords: [String] = []

        for keyword in obstructionKeywords {
            if text.contains(keyword) {
                matchedKeywords.append(keyword)
            }
        }

        guard !matchedKeywords.isEmpty else { return nil }

        let confidence = min(Double(matchedKeywords.count) * 0.25, 1.0)

        return PatternFlag(
            type: .obstruction,
            confidence: confidence,
            evidenceIDs: [evidenceID],
            explanation: "Evidence of obstruction of justice or document manipulation",
            keywords: matchedKeywords,
            severity: .high
        )
    }

    // MARK: - Neglect Detection
    private func detectNeglect(in text: String, evidenceID: String) -> PatternFlag? {
        var matchedKeywords: [String] = []

        for keyword in neglectKeywords {
            if text.contains(keyword) {
                matchedKeywords.append(keyword)
            }
        }

        guard !matchedKeywords.isEmpty else { return nil }

        let confidence = min(Double(matchedKeywords.count) * 0.35, 1.0)

        return PatternFlag(
            type: .neglect,
            confidence: confidence,
            evidenceIDs: [evidenceID],
            explanation: "Indicators of child neglect and inadequate care in foster placement",
            keywords: matchedKeywords,
            severity: .critical
        )
    }

    // MARK: - Misconduct Detection
    private func detectMisconduct(in text: String, evidenceID: String) -> PatternFlag? {
        var matchedKeywords: [String] = []

        for keyword in misconductKeywords {
            if text.contains(keyword) {
                matchedKeywords.append(keyword)
            }
        }

        guard !matchedKeywords.isEmpty else { return nil }

        let confidence = min(Double(matchedKeywords.count) * 0.4, 1.0)

        return PatternFlag(
            type: .misconduct,
            confidence: confidence,
            evidenceIDs: [evidenceID],
            explanation: "Potential attorney or professional misconduct",
            keywords: matchedKeywords,
            severity: .high
        )
    }

    // MARK: - Sentiment Analysis
    private func analyzeSentiment(_ text: String) {
        let tagger = NLTagger(tagSchemes: [.sentimentScore])
        tagger.string = text

        let (sentiment, _) = tagger.tag(at: text.startIndex, unit: .paragraph, scheme: .sentimentScore)

        if let sentimentScore = sentiment {
            print("Sentiment: \(sentimentScore.rawValue)")
        }
    }

    // MARK: - Timeline Inconsistency Detection
    func detectTimelineInconsistencies(evidence: [EvidenceItem], modelContext: ModelContext) {
        // Group by dates
        let sortedEvidence = evidence.sorted { $0.date < $1.date }

        for i in 0..<sortedEvidence.count - 1 {
            let current = sortedEvidence[i]
            let next = sortedEvidence[i + 1]

            let timeDiff = next.date.timeIntervalSince(current.date)

            // Check for suspicious gaps (e.g., more than 90 days)
            if timeDiff > 90 * 24 * 60 * 60 {
                let flag = PatternFlag(
                    type: .inconsistency,
                    confidence: 0.7,
                    evidenceIDs: [current.id.uuidString, next.id.uuidString],
                    explanation: "Significant time gap detected: \(Int(timeDiff / (24 * 60 * 60))) days between evidence items",
                    keywords: ["timeline gap"],
                    severity: .medium
                )

                modelContext.insert(flag)
            }
        }
    }
}
