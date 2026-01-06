//
//  SecurityManager.swift
//  EvidenceNexus
//
//  Biometric authentication and encryption management
//

import Foundation
import LocalAuthentication
import SwiftUI
import CryptoKit

class SecurityManager: ObservableObject {
    @Published var isAuthenticated = false
    @Published var authenticationError: String?

    private let context = LAContext()
    private let keychain = KeychainManager.shared

    init() {
        // Check if biometrics are available
        var error: NSError?
        guard context.canEvaluatePolicy(.deviceOwnerAuthenticationWithBiometrics, error: &error) else {
            authenticationError = error?.localizedDescription ?? "Biometric authentication not available"
            return
        }
    }

    func authenticate() {
        let reason = "Unlock EvidenceNexus to access your secure evidence vault"

        context.evaluatePolicy(.deviceOwnerAuthenticationWithBiometrics, localizedReason: reason) { [weak self] success, error in
            DispatchQueue.main.async {
                if success {
                    self?.isAuthenticated = true
                    self?.authenticationError = nil
                    AuditLogger.shared.log(.appUnlocked)
                } else {
                    self?.isAuthenticated = false
                    self?.authenticationError = error?.localizedDescription ?? "Authentication failed"
                }
            }
        }
    }

    func lock() {
        isAuthenticated = false
    }

    // Encrypt data using AES-GCM
    func encrypt(data: Data) throws -> Data {
        let key = try getOrCreateEncryptionKey()
        let sealedBox = try AES.GCM.seal(data, using: key)
        return sealedBox.combined!
    }

    // Decrypt data
    func decrypt(data: Data) throws -> Data {
        let key = try getOrCreateEncryptionKey()
        let sealedBox = try AES.GCM.SealedBox(combined: data)
        return try AES.GCM.open(sealedBox, using: key)
    }

    // Generate SHA-256 hash for file integrity
    static func sha256(data: Data) -> String {
        let hash = SHA256.hash(data: data)
        return hash.compactMap { String(format: "%02x", $0) }.joined()
    }

    private func getOrCreateEncryptionKey() throws -> SymmetricKey {
        let keyIdentifier = "com.evidencenexus.encryption.key"

        if let keyData = keychain.get(key: keyIdentifier) {
            return SymmetricKey(data: keyData)
        }

        // Generate new key
        let key = SymmetricKey(size: .bits256)
        let keyData = key.withUnsafeBytes { Data($0) }
        try keychain.set(key: keyIdentifier, value: keyData)
        return key
    }
}

// MARK: - Keychain Manager
class KeychainManager {
    static let shared = KeychainManager()

    private init() {}

    func set(key: String, value: Data) throws {
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrAccount as String: key,
            kSecValueData as String: value,
            kSecAttrAccessible as String: kSecAttrAccessibleWhenUnlockedThisDeviceOnly
        ]

        SecItemDelete(query as CFDictionary)

        let status = SecItemAdd(query as CFDictionary, nil)
        guard status == errSecSuccess else {
            throw KeychainError.unableToStore
        }
    }

    func get(key: String) -> Data? {
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrAccount as String: key,
            kSecReturnData as String: true,
            kSecMatchLimit as String: kSecMatchLimitOne
        ]

        var result: AnyObject?
        let status = SecItemCopyMatching(query as CFDictionary, &result)

        guard status == errSecSuccess else {
            return nil
        }

        return result as? Data
    }

    func delete(key: String) throws {
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrAccount as String: key
        ]

        let status = SecItemDelete(query as CFDictionary)
        guard status == errSecSuccess || status == errSecItemNotFound else {
            throw KeychainError.unableToDelete
        }
    }
}

enum KeychainError: Error {
    case unableToStore
    case unableToDelete
    case notFound
}

// MARK: - Audit Logger
class AuditLogger {
    static let shared = AuditLogger()

    private init() {}

    func log(_ action: AuditAction, evidenceID: String? = nil, details: String = "") {
        // In a real implementation, this would write to SwiftData
        let entry = AuditLogEntry(
            action: action,
            evidenceID: evidenceID,
            details: details
        )
        print("AUDIT: [\(entry.timestamp)] \(action.rawValue) - \(details)")
    }
}
