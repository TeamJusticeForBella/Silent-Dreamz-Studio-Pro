"use client";

import { useState } from "react";
import Link from "next/link";
import {
  Shield,
  Lock,
  Eye,
  EyeOff,
  Upload,
  FileText,
  AlertTriangle,
  CheckCircle,
  Mail,
  Key,
  Fingerprint,
  ChevronRight,
} from "lucide-react";

const portalSections = [
  {
    id: "whistleblower",
    icon: Eye,
    title: "Whistleblower Submissions",
    color: "var(--color-gold)",
    description:
      "Are you a current or former caseworker, court employee, foster care agency staff member, or anyone with direct knowledge of misconduct in Case 21DP0705A? Your information can make a difference.",
    steps: [
      "Use Signal or ProtonMail for initial contact to protect your identity",
      "You do not need to reveal your name — tips can be anonymous",
      "All submissions are encrypted and stored offline",
      "Legal counsel reviews every submission for evidentiary value",
    ],
    cta: "Submit a Tip",
    ctaHref: "/contact#whistleblower",
  },
  {
    id: "evidence",
    icon: Upload,
    title: "Evidence Submission",
    color: "var(--color-crimson)",
    description:
      "Witnesses, concerned citizens, and legal observers can submit documents, recordings, photographs, and other materials directly to the evidence team.",
    steps: [
      "All uploads are SHA-256 hashed at receipt to preserve chain of custody",
      "Submissions are reviewed by the legal team within 72 hours",
      "You will receive a confirmation code to track your submission",
      "Materials may be used in active litigation — you will be notified",
    ],
    cta: "Submit Evidence",
    ctaHref: "/contact",
  },
  {
    id: "attorney",
    icon: FileText,
    title: "Attorney & Legal Observer Access",
    color: "var(--color-success-green)",
    description:
      "Licensed attorneys, legal aid organizations, law school clinics, and credentialed legal observers may request access to the full case record.",
    steps: [
      "Submit bar number and contact information for verification",
      "Access includes all pleadings, declarations, and supporting evidence",
      "Collaboration welcome — pro bono representation actively sought",
      "ICWA specialists, constitutional litigators, and appellate counsel encouraged",
    ],
    cta: "Request Access",
    ctaHref: "/contact",
  },
  {
    id: "media",
    icon: Mail,
    title: "Verified Media Portal",
    color: "var(--color-rose)",
    description:
      "Credentialed journalists and documentary filmmakers can request access to verified case materials, interview scheduling, and press assets.",
    steps: [
      "Submit outlet name, editorial contact, and story scope",
      "Press kit and media package available immediately upon verification",
      "Embargo agreements available for investigative pieces",
      "Jason Barr is available for on-record interviews",
    ],
    cta: "Press Inquiry",
    ctaHref: "/media",
  },
];

const securityFeatures = [
  {
    icon: Lock,
    title: "End-to-End Encryption",
    detail: "All communications routed through encrypted channels. PGP keys available upon request.",
  },
  {
    icon: Fingerprint,
    title: "SHA-256 Evidence Hashing",
    detail: "Every document is cryptographically fingerprinted at receipt. Tampering is detectable.",
  },
  {
    icon: Shield,
    title: "No Metadata Logging",
    detail: "Anonymous submissions do not log IP addresses, browser fingerprints, or device identifiers.",
  },
  {
    icon: Key,
    title: "Air-Gapped Storage",
    detail: "Critical evidence copies are stored offline, isolated from any network-connected system.",
  },
];

export default function PortalPage() {
  const [activeSection, setActiveSection] = useState<string | null>(null);

  return (
    <div style={{ background: "var(--color-warm)" }}>
      {/* Hero */}
      <section
        style={{ background: "var(--color-navy)", color: "white" }}
        className="section-padding"
      >
        <div style={{ maxWidth: "var(--max-width-content)", margin: "0 auto" }}>
          <div className="flex items-center gap-3 mb-6">
            <Shield size={32} style={{ color: "var(--color-gold)" }} />
            <span
              style={{
                color: "var(--color-gold)",
                fontWeight: 700,
                fontSize: "0.8rem",
                letterSpacing: "0.12em",
                textTransform: "uppercase",
              }}
            >
              Secure Portal
            </span>
          </div>
          <h1
            style={{
              fontFamily: "var(--font-playfair)",
              fontSize: "clamp(2rem, 4vw, 3.5rem)",
              fontWeight: 700,
              lineHeight: 1.2,
              marginBottom: "20px",
            }}
          >
            Submit. Witness. Protect.
          </h1>
          <p
            style={{
              fontSize: "1.125rem",
              color: "rgba(255,255,255,0.75)",
              maxWidth: "640px",
              lineHeight: 1.7,
              marginBottom: "24px",
            }}
          >
            This portal exists because truth requires infrastructure. Whether
            you are a whistleblower, a witness, an attorney, or a journalist —
            your contribution to this record is protected here.
          </p>
          <div
            style={{
              background: "rgba(201,162,39,0.12)",
              border: "1px solid rgba(201,162,39,0.35)",
              borderRadius: "10px",
              padding: "16px 20px",
              display: "inline-flex",
              alignItems: "flex-start",
              gap: "12px",
              maxWidth: "560px",
            }}
          >
            <AlertTriangle
              size={18}
              style={{ color: "var(--color-gold)", flexShrink: 0, marginTop: "2px" }}
            />
            <p style={{ fontSize: "0.85rem", color: "rgba(255,255,255,0.7)", lineHeight: 1.6, margin: 0 }}>
              <strong style={{ color: "var(--color-gold)" }}>Case 21DP0705A</strong> — adoption
              finalization threatened September 16, 2026. Time-sensitive submissions are marked
              urgent and reviewed within 24 hours.
            </p>
          </div>
        </div>
      </section>

      {/* Security Features */}
      <section className="section-padding" style={{ background: "white" }}>
        <div
          style={{ maxWidth: "var(--max-width-content)", margin: "0 auto" }}
          className="px-4"
        >
          <h2
            style={{
              fontFamily: "var(--font-playfair)",
              fontSize: "1.75rem",
              fontWeight: 700,
              marginBottom: "8px",
              color: "var(--color-navy)",
              textAlign: "center",
            }}
          >
            How We Protect You
          </h2>
          <p
            style={{
              textAlign: "center",
              color: "rgba(51,51,51,0.65)",
              marginBottom: "40px",
              fontSize: "0.95rem",
            }}
          >
            Every submission method is designed with your safety in mind.
          </p>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {securityFeatures.map((f) => (
              <div
                key={f.title}
                style={{
                  background: "var(--color-light-gray)",
                  borderRadius: "12px",
                  padding: "24px",
                  border: "1px solid rgba(0,0,0,0.06)",
                }}
              >
                <f.icon
                  size={28}
                  style={{ color: "var(--color-navy)", marginBottom: "12px" }}
                />
                <h3
                  style={{
                    fontWeight: 700,
                    fontSize: "0.95rem",
                    color: "var(--color-navy)",
                    marginBottom: "8px",
                  }}
                >
                  {f.title}
                </h3>
                <p style={{ fontSize: "0.85rem", color: "rgba(51,51,51,0.65)", lineHeight: 1.6 }}>
                  {f.detail}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Portal Sections */}
      <section className="section-padding" style={{ background: "var(--color-warm)" }}>
        <div
          style={{ maxWidth: "var(--max-width-content)", margin: "0 auto" }}
          className="px-4"
        >
          <h2
            style={{
              fontFamily: "var(--font-playfair)",
              fontSize: "1.75rem",
              fontWeight: 700,
              marginBottom: "8px",
              color: "var(--color-navy)",
            }}
          >
            Choose Your Path
          </h2>
          <p
            style={{
              color: "rgba(51,51,51,0.65)",
              marginBottom: "40px",
              fontSize: "0.95rem",
            }}
          >
            Select the submission type that applies to you.
          </p>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {portalSections.map((section) => {
              const isOpen = activeSection === section.id;
              return (
                <div
                  key={section.id}
                  className="card"
                  style={{
                    border: isOpen ? `2px solid ${section.color}` : "2px solid transparent",
                    transition: "border-color 0.2s",
                    cursor: "pointer",
                  }}
                  onClick={() =>
                    setActiveSection(isOpen ? null : section.id)
                  }
                >
                  <div style={{ padding: "28px" }}>
                    <div className="flex items-center gap-3 mb-4">
                      <div
                        style={{
                          background: `${section.color}18`,
                          borderRadius: "8px",
                          padding: "10px",
                          flexShrink: 0,
                        }}
                      >
                        <section.icon size={22} style={{ color: section.color }} />
                      </div>
                      <h3
                        style={{
                          fontWeight: 700,
                          fontSize: "1.1rem",
                          color: "var(--color-navy)",
                        }}
                      >
                        {section.title}
                      </h3>
                      <ChevronRight
                        size={18}
                        style={{
                          color: "rgba(51,51,51,0.35)",
                          marginLeft: "auto",
                          transform: isOpen ? "rotate(90deg)" : "none",
                          transition: "transform 0.2s",
                          flexShrink: 0,
                        }}
                      />
                    </div>
                    <p
                      style={{
                        fontSize: "0.9rem",
                        color: "rgba(51,51,51,0.7)",
                        lineHeight: 1.65,
                        marginBottom: isOpen ? "20px" : 0,
                      }}
                    >
                      {section.description}
                    </p>

                    {isOpen && (
                      <div>
                        <ul style={{ listStyle: "none", padding: 0, margin: "0 0 20px 0" }}>
                          {section.steps.map((step, i) => (
                            <li
                              key={i}
                              className="flex items-start gap-3"
                              style={{ marginBottom: "10px" }}
                            >
                              <CheckCircle
                                size={16}
                                style={{
                                  color: section.color,
                                  flexShrink: 0,
                                  marginTop: "3px",
                                }}
                              />
                              <span
                                style={{
                                  fontSize: "0.875rem",
                                  color: "var(--color-charcoal)",
                                  lineHeight: 1.5,
                                }}
                              >
                                {step}
                              </span>
                            </li>
                          ))}
                        </ul>
                        <Link
                          href={section.ctaHref}
                          className="btn-primary"
                          style={{
                            background: section.color,
                            color:
                              section.color === "var(--color-crimson)" ||
                              section.color === "var(--color-success-green)"
                                ? "white"
                                : "var(--color-navy)",
                            padding: "10px 24px",
                            fontSize: "0.875rem",
                            display: "inline-block",
                          }}
                          onClick={(e) => e.stopPropagation()}
                        >
                          {section.cta} →
                        </Link>
                      </div>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* Secure Contact Methods */}
      <section className="section-padding" style={{ background: "var(--color-navy)" }}>
        <div
          style={{ maxWidth: "640px", margin: "0 auto", textAlign: "center" }}
          className="px-4"
        >
          <Lock size={32} style={{ color: "var(--color-gold)", margin: "0 auto 16px" }} />
          <h2
            style={{
              fontFamily: "var(--font-playfair)",
              fontSize: "1.75rem",
              fontWeight: 700,
              color: "white",
              marginBottom: "16px",
            }}
          >
            Secure Contact Methods
          </h2>
          <p
            style={{
              color: "rgba(255,255,255,0.65)",
              fontSize: "0.95rem",
              lineHeight: 1.7,
              marginBottom: "32px",
            }}
          >
            For the most sensitive information, use end-to-end encrypted channels. Do not send
            confidential case information through unencrypted email or social media.
          </p>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-left">
            {[
              {
                method: "Signal",
                detail: "Preferred for whistleblowers. Disappearing messages supported.",
                note: "Contact via secure form for number",
              },
              {
                method: "ProtonMail",
                detail: "Send to our ProtonMail address for encrypted email.",
                note: "Available via contact page",
              },
              {
                method: "In-Person",
                detail: "Orange County, CA area. Meetings can be arranged for sensitive materials.",
                note: "Arrange via secure form",
              },
            ].map((m) => (
              <div
                key={m.method}
                style={{
                  background: "rgba(255,255,255,0.07)",
                  border: "1px solid rgba(201,162,39,0.2)",
                  borderRadius: "10px",
                  padding: "20px",
                }}
              >
                <h3
                  style={{
                    color: "var(--color-gold)",
                    fontWeight: 700,
                    fontSize: "0.95rem",
                    marginBottom: "8px",
                  }}
                >
                  {m.method}
                </h3>
                <p
                  style={{
                    color: "rgba(255,255,255,0.65)",
                    fontSize: "0.8rem",
                    lineHeight: 1.6,
                    marginBottom: "8px",
                  }}
                >
                  {m.detail}
                </p>
                <span
                  style={{
                    fontSize: "0.75rem",
                    color: "rgba(255,255,255,0.35)",
                    fontStyle: "italic",
                  }}
                >
                  {m.note}
                </span>
              </div>
            ))}
          </div>
          <div style={{ marginTop: "40px" }}>
            <Link href="/contact" className="btn-primary" style={{ marginRight: "12px" }}>
              Go to Contact Page
            </Link>
            <Link href="/evidence" className="btn-secondary">
              View Evidence Vault
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
}
