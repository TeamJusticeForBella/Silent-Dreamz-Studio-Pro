// swift-tools-version: 5.9
// The swift-tools-version declares the minimum version of Swift required to build this package.

import PackageDescription

let package = Package(
    name: "EvidenceNexus",
    platforms: [
        .iOS(.v18)
    ],
    products: [
        .library(
            name: "EvidenceNexus",
            targets: ["EvidenceNexus"])
    ],
    dependencies: [
        // Google Sign-In for Gmail integration
        // Uncomment when ready to add:
        // .package(url: "https://github.com/google/GoogleSignIn-iOS", from: "7.0.0"),

        // Microsoft Authentication Library for Outlook integration
        // Uncomment when ready to add:
        // .package(url: "https://github.com/AzureAD/microsoft-authentication-library-for-objc", from: "1.3.0"),

        // Facebook SDK for Facebook/Instagram integration
        // Uncomment when ready to add:
        // .package(url: "https://github.com/facebook/facebook-ios-sdk", from: "16.0.0"),
    ],
    targets: [
        .target(
            name: "EvidenceNexus",
            dependencies: [
                // Uncomment when adding dependencies:
                // .product(name: "GoogleSignIn", package: "GoogleSignIn-iOS"),
                // .product(name: "MSAL", package: "microsoft-authentication-library-for-objc"),
                // .product(name: "FacebookLogin", package: "facebook-ios-sdk"),
                // .product(name: "FacebookCore", package: "facebook-ios-sdk"),
            ]
        )
    ]
)
