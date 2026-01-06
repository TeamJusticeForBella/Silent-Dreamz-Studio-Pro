//
//  ContentView.swift
//  EvidenceNexus
//
//  Main navigation container
//

import SwiftUI
import SwiftData

struct ContentView: View {
    @EnvironmentObject var securityManager: SecurityManager
    @EnvironmentObject var appState: AppState
    @State private var selectedTab = 0

    var body: some View {
        if securityManager.isAuthenticated {
            TabView(selection: $selectedTab) {
                ImportsView()
                    .tabItem {
                        Label("Import", systemImage: "square.and.arrow.down")
                    }
                    .tag(0)

                LibraryView()
                    .tabItem {
                        Label("Library", systemImage: "folder.fill")
                    }
                    .tag(1)

                TimelineView()
                    .tabItem {
                        Label("Timeline", systemImage: "calendar")
                    }
                    .tag(2)

                PatternsView()
                    .tabItem {
                        Label("Patterns", systemImage: "waveform.path.ecg")
                    }
                    .tag(3)

                AIHubView()
                    .tabItem {
                        Label("AI Hub", systemImage: "sparkles")
                    }
                    .tag(4)

                SettingsView()
                    .tabItem {
                        Label("Settings", systemImage: "gear")
                    }
                    .tag(5)
            }
            .overlay {
                if appState.isProcessing {
                    ProcessingOverlay(message: appState.processingMessage)
                }
            }
            .alert("Error", isPresented: $appState.showAlert) {
                Button("OK", role: .cancel) {}
            } message: {
                Text(appState.alertMessage)
            }
        } else {
            LockScreen()
        }
    }
}

// MARK: - Lock Screen
struct LockScreen: View {
    @EnvironmentObject var securityManager: SecurityManager

    var body: some View {
        ZStack {
            LinearGradient(
                colors: [.blue, .purple],
                startPoint: .topLeading,
                endPoint: .bottomTrailing
            )
            .ignoresSafeArea()

            VStack(spacing: 30) {
                Image(systemName: "lock.shield.fill")
                    .font(.system(size: 100))
                    .foregroundStyle(.white)

                Text("EvidenceNexus")
                    .font(.system(size: 36, weight: .bold))
                    .foregroundStyle(.white)

                Text("Secure Evidence Management")
                    .font(.headline)
                    .foregroundStyle(.white.opacity(0.8))

                Button {
                    securityManager.authenticate()
                } label: {
                    Label("Unlock with Face ID", systemImage: "faceid")
                        .font(.headline)
                        .foregroundStyle(.blue)
                        .padding()
                        .frame(maxWidth: .infinity)
                        .background(.white)
                        .cornerRadius(12)
                }
                .padding(.horizontal, 40)
                .padding(.top, 40)

                if let error = securityManager.authenticationError {
                    Text(error)
                        .font(.caption)
                        .foregroundStyle(.red)
                        .padding()
                        .background(.white.opacity(0.9))
                        .cornerRadius(8)
                }
            }
            .padding()
        }
    }
}

// MARK: - Processing Overlay
struct ProcessingOverlay: View {
    let message: String

    var body: some View {
        ZStack {
            Color.black.opacity(0.4)
                .ignoresSafeArea()

            VStack(spacing: 20) {
                ProgressView()
                    .scaleEffect(1.5)
                    .tint(.white)

                Text(message)
                    .font(.headline)
                    .foregroundStyle(.white)
            }
            .padding(30)
            .background(.ultraThinMaterial)
            .cornerRadius(16)
        }
    }
}
