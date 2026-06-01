"use client";

import { useState } from "react";
import Link from "next/link";
import {
  Shield,
  FileText,
  Play,
  Download,
  Search,
  AlertTriangle,
  ChevronRight,
} from "lucide-react";

const evidenceItems = [
  {
    id: "audio-nov-2023",
    type: "Audio",
    title: "November 27, 2023 — Incident Recording",
    date: "2023-11-27",
    format: "MP3 / WAV",
    sha256: "a3f9c27d4e8b2f1c6a0d3e9b5f8c1a4d7e2b6f9c3a8d1e4b7f2c5a0d8e3b6f9",
    description:
      "Primary incident documentation audio. Submitted to court record. Directly contradicts foster care agent statements.",
    featured: true,
    category: "Audio",
  },
  {
    id: "abuse-report-2020-01",
    type: "Document",
    title: "Formal Abuse Report #1 — Filed 2020",
    date: "2020-03-14",
    format: "PDF",
    sha256: "b4e8d3c7a1f5e9b2d6c0a4f8e2b5d9c3a7f1e5b8d2c6a0f4e8b1d5c9a3f7e1b4",
    description:
      "First formal abuse report filed with CPS. Documents specific observed indicators. Official response: case closed without investigation.",
    featured: false,
    category: "Documents",
  },
  {
    id: "abuse-report-2020-02",
    type: "Document",
    title: "Formal Abuse Report #2 — Filed 2020",
    date: "2020-08-22",
    format: "PDF",
    sha256: "c5f9e4d8b2a6f0c3e7b1d5a9f3b7e0c4a8f2d6b0e4c8a2f6d0b4e8c2a6f0d4b8",
    description:
      "Second formal abuse report filed after continued observations. Includes documented communications with caseworker.",
    featured: false,
    category: "Documents",
  },
  {
    id: "abuse-report-2021-01",
    type: "Document",
    title: "Formal Abuse Report #3 — Filed 2021",
    date: "2021-02-09",
    format: "PDF",
    sha256: "d6a0f5e9c3b7d1a5f9e2c6b0d4a8f2c6b0e4d8a2f6c0b4e8d2a6f0c4b8e2a6f0",
    description:
      "Third documented abuse report. Escalated to supervisor level. Response: no findings.",
    featured: false,
    category: "Documents",
  },
  {
    id: "icwa-violation-memo",
    type: "Legal",
    title: "ICWA Violation Documentation — Procedural Analysis",
    date: "2022-06-15",
    format: "PDF",
    sha256: "e7b1d6f0a4c8e2b6f0a4d8b2e6a0c4f8d2b6a0e4c8f2b6d0a4e8b2c6f0a4d8b2",
    description:
      "Detailed analysis of ICWA violations throughout the case. Identifies 7 specific statutory violations with citations.",
    featured: true,
    category: "Legal",
  },
  {
    id: "tpr-objection-filing",
    type: "Legal",
    title: "TPR Objection and Protest Filing",
    date: "2024-01-18",
    format: "PDF",
    sha256: "f8c2e7a1d5b9f3c7a1e5d9b3f7a1e5c9b3d7f1a5c9b3e7d1f5a9c3b7e1d5f9a3",
    description:
      "Formal objection to TPR filed by Jason R. Barr. Documents compliance with all service requirements and procedural violations.",
    featured: false,
    category: "Legal",
  },
  {
    id: "federal-1983-complaint",
    type: "Legal",
    title: "42 U.S.C. §1983 Federal Civil Rights Complaint",
    date: "2025-03-05",
    format: "PDF",
    sha256: "a1d5f9b3e7c1d5a9f3b7e1c5d9a3f7b1e5d9c3a7f1b5e9d3c7a1f5d9b3e7a1c5",
    description:
      "Federal civil rights complaint filed in District Court. Alleges constitutional violations including due process and ICWA rights.",
    featured: true,
    category: "Legal",
  },
  {
    id: "habeas-petition",
    type: "Legal",
    title: "Habeas Corpus Petition",
    date: "2025-04-12",
    format: "PDF",
    sha256: "b2e6a0c4f8b2e6a0c4f8b2e6a0c4f8b2e6a0c4f8b2e6a0c4f8b2e6a0c4f8b2e6",
    description:
      "Petition for writ of habeas corpus challenging unlawful detention/separation. Grounds include ICWA violations and due process.",
    featured: false,
    category: "Legal",
  },
  {
    id: "audio-visitation-2022",
    type: "Audio",
    title: "Supervised Visitation Recording — 2022",
    date: "2022-11-03",
    format: "MP3",
    sha256: "c3f7b1d5a9e3c7b1d5a9f3c7b1d5e9a3f7b1c5d9e3a7f1b5c9d3e7a1f5b9c3d7",
    description:
      "Recording of supervised visitation session. Demonstrates quality of father-daughter relationship and Bella's emotional state.",
    featured: false,
    category: "Audio",
  },
  {
    id: "caseworker-communications",
    type: "Document",
    title: "Caseworker Communications — Compiled 2019–2024",
    date: "2024-06-01",
    format: "PDF",
    sha256: "d4a8e2c6f0d4a8e2c6f0d4a8e2c6f0d4a8e2c6f0d4a8e2c6f0d4a8e2c6f0d4a8",
    description:
      "Compiled record of all written communications with assigned caseworkers. Documents inconsistencies in official statements.",
    featured: false,
    category: "Documents",
  },
  {
    id: "medical-records-concerns",
    type: "Medical",
    title: "Medical Examination Findings — 2023",
    date: "2023-09-14",
    format: "PDF",
    sha256: "e5b9f3d7a1e5b9f3d7a1e5b9f3d7a1e5b9f3d7a1e5b9f3d7a1e5b9f3d7a1e5b9",
    description:
      "Medical examination findings documenting physical condition. Requested by Jason as part of abuse reporting process.",
    featured: false,
    category: "Medical",
  },
  {
    id: "tro-motion-2025",
    type: "Legal",
    title: "TRO / Injunction Motion — Adoption Stay",
    date: "2025-06-20",
    format: "PDF",
    sha256: "f6c0d4a8b2f6c0d4a8b2f6c0d4a8b2f6c0d4a8b2f6c0d4a8b2f6c0d4a8b2f6c0",
    description:
      "Motion for Temporary Restraining Order and Preliminary Injunction to halt adoption finalization pending federal case resolution.",
    featured: false,
    category: "Legal",
  },
];

const contradictions = [
  {
    claim:
      "Foster care agency stated no abuse reports were filed by biological parent",
    evidence: "Abuse Reports #1, #2, #3 (2020–2021)",
    contradiction:
      "Three formal reports filed and date-stamped. Official response records confirm receipt.",
    source: "Evidence IDs: abuse-report-2020-01, -02, -03",
  },
  {
    claim:
      "Caseworker testified biological father did not complete required services",
    evidence: "Service completion certificates, compliance documentation",
    contradiction:
      "Independent verification shows all required services completed. Certificates on file.",
    source: "Evidence ID: caseworker-communications",
  },
  {
    claim:
      "Agency stated November 27, 2023 incident was not significant or documented",
    evidence: "Authenticated audio recording (SHA-256: a3f9c2...8b4e17)",
    contradiction:
      "Recording directly documents the incident in real time. Submitted to court record.",
    source: "Evidence ID: audio-nov-2023",
  },
  {
    claim: "ICWA did not apply to this case or active efforts were made",
    evidence: "ICWA Violation Analysis Memo, federal complaint",
    contradiction:
      "Legal analysis identifies 7 specific violations. Active efforts requirement was not met per §1912(d).",
    source: "Evidence IDs: icwa-violation-memo, federal-1983-complaint",
  },
];

const categories = ["All", "Audio", "Video", "Documents", "Legal", "Medical"];

export default function EvidenceVaultPage() {
  const [search, setSearch] = useState("");
  const [activeCategory, setActiveCategory] = useState("All");

  const filtered = evidenceItems.filter((item) => {
    const matchSearch =
      search === "" ||
      item.title.toLowerCase().includes(search.toLowerCase()) ||
      item.description.toLowerCase().includes(search.toLowerCase()) ||
      item.type.toLowerCase().includes(search.toLowerCase());
    const matchCat =
      activeCategory === "All" || item.category === activeCategory;
    return matchSearch && matchCat;
  });

  const featured = evidenceItems.filter((i) => i.featured);

  return (
    <div style={{ background: "var(--color-warm)" }}>
      {/* ── HEADER ── */}
      <section
        style={{ background: "var(--color-navy)", padding: "64px 16px" }}
      >
        <div
          style={{ maxWidth: "var(--max-width-content)", margin: "0 auto" }}
        >
          <div className="flex flex-col md:flex-row justify-between items-start gap-8">
            <div>
              <span
                style={{
                  color: "var(--color-gold)",
                  fontSize: "0.8rem",
                  fontWeight: 700,
                  letterSpacing: "0.14em",
                  textTransform: "uppercase",
                }}
              >
                Case 21DP0705A
              </span>
              <h1
                style={{
                  fontFamily: "var(--font-serif)",
                  fontSize: "clamp(2rem, 4vw, 3rem)",
                  color: "var(--color-gold)",
                  fontWeight: 900,
                  marginTop: "8px",
                  marginBottom: "12px",
                }}
              >
                Evidence Vault
              </h1>
              <p
                style={{
                  color: "rgba(255,255,255,0.7)",
                  fontSize: "1rem",
                  maxWidth: "520px",
                  lineHeight: 1.7,
                }}
              >
                Every document, recording, and filing preserved with SHA-256
                cryptographic authentication. The truth cannot be altered.
              </p>
            </div>
            <div className="flex flex-col gap-3">
              <div
                style={{
                  background: "rgba(201,162,39,0.1)",
                  border: "1px solid rgba(201,162,39,0.3)",
                  borderRadius: "10px",
                  padding: "16px 20px",
                  textAlign: "center",
                }}
              >
                <div
                  style={{
                    fontFamily: "var(--font-serif)",
                    fontSize: "2rem",
                    fontWeight: 900,
                    color: "var(--color-gold)",
                    lineHeight: 1,
                  }}
                >
                  47
                </div>
                <div
                  style={{
                    color: "rgba(255,255,255,0.7)",
                    fontSize: "0.8rem",
                    marginTop: "4px",
                  }}
                >
                  Evidence Items
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ── FEATURED EVIDENCE ── */}
      <section className="section-padding">
        <div
          style={{ maxWidth: "var(--max-width-content)", margin: "0 auto" }}
          className="px-4"
        >
          <h2
            style={{
              fontFamily: "var(--font-serif)",
              fontSize: "1.5rem",
              color: "var(--color-navy)",
              fontWeight: 700,
              marginBottom: "24px",
            }}
          >
            Featured Evidence
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
            {featured.map((item) => (
              <div
                key={item.id}
                className="card"
                style={{ borderTop: "4px solid var(--color-gold)" }}
              >
                <div style={{ padding: "24px" }}>
                  <div className="flex items-center gap-2 mb-3">
                    <span
                      style={{
                        background: "var(--color-crimson)",
                        color: "white",
                        fontSize: "0.65rem",
                        fontWeight: 700,
                        padding: "2px 8px",
                        borderRadius: "100px",
                        textTransform: "uppercase",
                        letterSpacing: "0.08em",
                      }}
                    >
                      FEATURED
                    </span>
                    <span
                      style={{
                        background: "var(--color-light-gray)",
                        color: "var(--color-navy)",
                        fontSize: "0.7rem",
                        fontWeight: 600,
                        padding: "2px 8px",
                        borderRadius: "100px",
                      }}
                    >
                      {item.type}
                    </span>
                  </div>

                  {item.type === "Audio" && (
                    <div className="waveform mb-3" style={{ opacity: 0.6 }} />
                  )}

                  {item.type === "Legal" && (
                    <div
                      style={{
                        height: "48px",
                        background: "var(--color-light-gray)",
                        borderRadius: "6px",
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "center",
                        marginBottom: "12px",
                      }}
                    >
                      <FileText
                        size={24}
                        style={{ color: "var(--color-navy)", opacity: 0.4 }}
                      />
                    </div>
                  )}

                  <h3
                    style={{
                      fontFamily: "var(--font-serif)",
                      fontSize: "1rem",
                      color: "var(--color-navy)",
                      fontWeight: 700,
                      marginBottom: "8px",
                      lineHeight: 1.3,
                    }}
                  >
                    {item.title}
                  </h3>

                  <p
                    style={{
                      color: "var(--color-charcoal)",
                      fontSize: "0.82rem",
                      lineHeight: 1.6,
                      marginBottom: "12px",
                    }}
                  >
                    {item.description}
                  </p>

                  <div className="flex items-center gap-2 mb-12px flex-wrap">
                    <Shield
                      size={12}
                      style={{ color: "var(--color-gold)", flexShrink: 0 }}
                    />
                    <span className="evidence-badge">
                      {item.sha256.substring(0, 16)}...
                    </span>
                  </div>

                  <div
                    className="flex gap-2 mt-3"
                    style={{ marginTop: "12px" }}
                  >
                    <button
                      style={{
                        flex: 1,
                        background: "var(--color-navy)",
                        color: "var(--color-gold)",
                        border: "none",
                        borderRadius: "6px",
                        padding: "8px",
                        fontSize: "0.8rem",
                        fontWeight: 600,
                        cursor: "pointer",
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "center",
                        gap: "4px",
                      }}
                    >
                      {item.type === "Audio" ? (
                        <Play size={12} />
                      ) : (
                        <FileText size={12} />
                      )}
                      View
                    </button>
                    <button
                      style={{
                        flex: 1,
                        background: "transparent",
                        color: "var(--color-charcoal)",
                        border: "1px solid var(--color-light-gray)",
                        borderRadius: "6px",
                        padding: "8px",
                        fontSize: "0.8rem",
                        fontWeight: 600,
                        cursor: "pointer",
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "center",
                        gap: "4px",
                      }}
                    >
                      <Download size={12} />
                      Download
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>

          {/* ── SEARCH + FILTER ── */}
          <div
            style={{
              background: "white",
              border: "1px solid var(--color-light-gray)",
              borderRadius: "12px",
              padding: "24px",
              marginBottom: "24px",
            }}
          >
            <div className="flex flex-col md:flex-row gap-4 items-start">
              <div style={{ flex: 1, position: "relative" }}>
                <Search
                  size={18}
                  style={{
                    position: "absolute",
                    left: "12px",
                    top: "50%",
                    transform: "translateY(-50%)",
                    color: "var(--color-charcoal)",
                    opacity: 0.5,
                  }}
                />
                <input
                  type="text"
                  value={search}
                  onChange={(e) => setSearch(e.target.value)}
                  placeholder="Search evidence by title, type, or description..."
                  style={{
                    width: "100%",
                    paddingLeft: "40px",
                    paddingRight: "16px",
                    paddingTop: "12px",
                    paddingBottom: "12px",
                    border: "1px solid var(--color-light-gray)",
                    borderRadius: "8px",
                    fontSize: "0.9rem",
                    outline: "none",
                    boxSizing: "border-box",
                  }}
                />
              </div>
              <div className="flex gap-2 flex-wrap">
                {categories.map((cat) => (
                  <button
                    key={cat}
                    onClick={() => setActiveCategory(cat)}
                    style={{
                      padding: "8px 16px",
                      borderRadius: "100px",
                      border: "1px solid",
                      borderColor:
                        activeCategory === cat
                          ? "var(--color-gold)"
                          : "var(--color-light-gray)",
                      background:
                        activeCategory === cat
                          ? "var(--color-gold)"
                          : "transparent",
                      color:
                        activeCategory === cat
                          ? "var(--color-navy)"
                          : "var(--color-charcoal)",
                      fontSize: "0.82rem",
                      fontWeight: 600,
                      cursor: "pointer",
                    }}
                  >
                    {cat}
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* ── EVIDENCE GRID ── */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-16">
            {filtered.map((item) => (
              <div
                key={item.id}
                className="card"
                style={{ padding: "20px" }}
              >
                <div className="flex items-start gap-4">
                  <div
                    style={{
                      width: "44px",
                      height: "44px",
                      borderRadius: "10px",
                      background:
                        item.type === "Audio"
                          ? "rgba(201,162,39,0.1)"
                          : item.type === "Legal"
                          ? "rgba(26,26,46,0.08)"
                          : item.type === "Medical"
                          ? "rgba(232,180,184,0.2)"
                          : "rgba(26,26,46,0.06)",
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                      flexShrink: 0,
                    }}
                  >
                    {item.type === "Audio" ? (
                      <Play size={20} style={{ color: "var(--color-gold)" }} />
                    ) : (
                      <FileText
                        size={20}
                        style={{ color: "var(--color-navy)" }}
                      />
                    )}
                  </div>

                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-1 flex-wrap">
                      <span
                        style={{
                          background: "var(--color-light-gray)",
                          color: "var(--color-navy)",
                          fontSize: "0.68rem",
                          fontWeight: 600,
                          padding: "2px 8px",
                          borderRadius: "100px",
                        }}
                      >
                        {item.type}
                      </span>
                      <span
                        style={{
                          color: "var(--color-gold)",
                          fontSize: "0.75rem",
                        }}
                      >
                        {item.date}
                      </span>
                    </div>

                    <h4
                      style={{
                        fontFamily: "var(--font-serif)",
                        fontSize: "0.95rem",
                        color: "var(--color-navy)",
                        fontWeight: 700,
                        marginBottom: "6px",
                        lineHeight: 1.3,
                      }}
                    >
                      {item.title}
                    </h4>

                    <p
                      style={{
                        color: "var(--color-charcoal)",
                        fontSize: "0.8rem",
                        lineHeight: 1.5,
                        marginBottom: "10px",
                      }}
                    >
                      {item.description}
                    </p>

                    <div className="flex items-center gap-2 mb-3">
                      <span className="evidence-badge">
                        {item.sha256.substring(0, 12)}...
                      </span>
                      <span
                        style={{
                          color: "var(--color-charcoal)",
                          fontSize: "0.7rem",
                          opacity: 0.6,
                        }}
                      >
                        {item.format}
                      </span>
                    </div>

                    <div className="flex gap-2">
                      <button
                        style={{
                          background: "var(--color-navy)",
                          color: "var(--color-gold)",
                          border: "none",
                          borderRadius: "6px",
                          padding: "6px 14px",
                          fontSize: "0.78rem",
                          fontWeight: 600,
                          cursor: "pointer",
                        }}
                      >
                        View Details
                      </button>
                      <button
                        style={{
                          background: "transparent",
                          color: "var(--color-charcoal)",
                          border: "1px solid var(--color-light-gray)",
                          borderRadius: "6px",
                          padding: "6px 14px",
                          fontSize: "0.78rem",
                          fontWeight: 600,
                          cursor: "pointer",
                          display: "flex",
                          alignItems: "center",
                          gap: "4px",
                        }}
                      >
                        <Download size={12} />
                        Download
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>

          {/* ── CONTRADICTIONS TRACKER ── */}
          <div id="contradictions" style={{ marginBottom: "64px" }}>
            <div className="flex items-center gap-3 mb-6">
              <AlertTriangle
                size={24}
                style={{ color: "var(--color-crimson)" }}
              />
              <h2
                style={{
                  fontFamily: "var(--font-serif)",
                  fontSize: "1.5rem",
                  color: "var(--color-navy)",
                  fontWeight: 700,
                }}
              >
                Contradictions Tracker
              </h2>
            </div>
            <p
              style={{
                color: "var(--color-charcoal)",
                fontSize: "0.9rem",
                marginBottom: "20px",
                lineHeight: 1.6,
              }}
            >
              Official claims made by state actors versus what the authenticated
              evidence actually shows.
            </p>

            <div
              style={{
                overflowX: "auto",
                borderRadius: "12px",
                border: "1px solid var(--color-light-gray)",
              }}
            >
              <table style={{ width: "100%", borderCollapse: "collapse" }}>
                <thead>
                  <tr
                    style={{ background: "var(--color-navy)" }}
                  >
                    {["Official Claim", "Evidence", "Contradiction", "Source"].map(
                      (h) => (
                        <th
                          key={h}
                          style={{
                            color: "var(--color-gold)",
                            fontSize: "0.78rem",
                            fontWeight: 700,
                            letterSpacing: "0.08em",
                            textTransform: "uppercase",
                            padding: "14px 16px",
                            textAlign: "left",
                            whiteSpace: "nowrap",
                          }}
                        >
                          {h}
                        </th>
                      )
                    )}
                  </tr>
                </thead>
                <tbody>
                  {contradictions.map((row, idx) => (
                    <tr
                      key={idx}
                      style={{
                        background: idx % 2 === 0 ? "white" : "var(--color-light-gray)",
                        borderBottom: "1px solid rgba(0,0,0,0.05)",
                      }}
                    >
                      <td
                        style={{
                          padding: "14px 16px",
                          fontSize: "0.85rem",
                          color: "var(--color-charcoal)",
                          maxWidth: "200px",
                          lineHeight: 1.5,
                        }}
                      >
                        <span
                          style={{
                            color: "var(--color-crimson)",
                            fontWeight: 600,
                            fontSize: "0.75rem",
                            display: "block",
                            marginBottom: "4px",
                          }}
                        >
                          ✗ CLAIM
                        </span>
                        {row.claim}
                      </td>
                      <td
                        style={{
                          padding: "14px 16px",
                          fontSize: "0.85rem",
                          color: "var(--color-charcoal)",
                          maxWidth: "160px",
                          lineHeight: 1.5,
                        }}
                      >
                        <span className="evidence-badge">{row.evidence}</span>
                      </td>
                      <td
                        style={{
                          padding: "14px 16px",
                          fontSize: "0.85rem",
                          color: "var(--color-charcoal)",
                          maxWidth: "240px",
                          lineHeight: 1.5,
                        }}
                      >
                        <span
                          style={{
                            color: "var(--color-success-green)",
                            fontWeight: 600,
                            fontSize: "0.75rem",
                            display: "block",
                            marginBottom: "4px",
                          }}
                        >
                          ✓ DOCUMENTED
                        </span>
                        {row.contradiction}
                      </td>
                      <td
                        style={{
                          padding: "14px 16px",
                          fontSize: "0.78rem",
                          color: "var(--color-charcoal)",
                          opacity: 0.7,
                          maxWidth: "140px",
                        }}
                      >
                        {row.source}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* ── DOWNLOAD CENTER ── */}
          <div
            style={{
              background: "var(--color-navy)",
              borderRadius: "16px",
              padding: "40px",
            }}
          >
            <h2
              style={{
                fontFamily: "var(--font-serif)",
                fontSize: "1.5rem",
                color: "var(--color-gold)",
                fontWeight: 700,
                marginBottom: "8px",
              }}
            >
              Download Center
            </h2>
            <p
              style={{
                color: "rgba(255,255,255,0.65)",
                fontSize: "0.9rem",
                marginBottom: "24px",
                lineHeight: 1.6,
              }}
            >
              Packaged evidence bundles for journalists, legal researchers, and
              advocates. All files include SHA-256 manifest for verification.
            </p>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {[
                {
                  title: "Full Evidence Package",
                  size: "847 MB",
                  files: "47 files",
                  desc: "Complete vault — all evidence",
                },
                {
                  title: "Legal Filings Bundle",
                  size: "124 MB",
                  files: "12 files",
                  desc: "All federal court filings",
                },
                {
                  title: "Abuse Documentation",
                  size: "89 MB",
                  files: "8 files",
                  desc: "Reports and responses",
                },
              ].map((pkg) => (
                <div
                  key={pkg.title}
                  style={{
                    background: "rgba(255,255,255,0.06)",
                    border: "1px solid rgba(201,162,39,0.25)",
                    borderRadius: "10px",
                    padding: "20px",
                  }}
                >
                  <h4
                    style={{
                      color: "white",
                      fontWeight: 700,
                      fontSize: "0.95rem",
                      marginBottom: "4px",
                    }}
                  >
                    {pkg.title}
                  </h4>
                  <p
                    style={{
                      color: "rgba(255,255,255,0.5)",
                      fontSize: "0.8rem",
                      marginBottom: "12px",
                    }}
                  >
                    {pkg.desc} — {pkg.files} — {pkg.size}
                  </p>
                  <button
                    style={{
                      width: "100%",
                      background: "var(--color-gold)",
                      color: "var(--color-navy)",
                      border: "none",
                      borderRadius: "6px",
                      padding: "10px",
                      fontSize: "0.85rem",
                      fontWeight: 700,
                      cursor: "pointer",
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                      gap: "6px",
                    }}
                  >
                    <Download size={14} />
                    Download ZIP
                  </button>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
