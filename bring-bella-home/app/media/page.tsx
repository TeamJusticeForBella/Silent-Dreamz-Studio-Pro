"use client";

import { useState } from "react";
import Link from "next/link";
import { FileText, Download, Play, AlertTriangle, Scale } from "lucide-react";

const pressKitItems = [
  { title: "Press Kit — Full Package", size: "18 MB", format: "ZIP" },
  { title: "Official Case Summary (1-page)", size: "450 KB", format: "PDF" },
  { title: "High-Res Campaign Graphics", size: "12 MB", format: "ZIP" },
  { title: "Timeline Infographic", size: "2.1 MB", format: "PDF" },
  { title: "Verified Facts Sheet", size: "380 KB", format: "PDF" },
];

const coverage = [
  {
    outlet: "Independent Journalist Investigation",
    title: "A Father's Six-Year Fight: The Evidence Behind Case 21DP0705A",
    type: "Article",
    date: "April 2025",
    desc: "In-depth investigative report examining the documented evidence, ICWA violations, and systemic failures in this case.",
    featured: true,
  },
  {
    outlet: "Child Welfare Reform Podcast",
    title: "Episode 84: When the System Fails — The Barr Case",
    type: "Podcast",
    date: "March 2025",
    desc: "Jason R. Barr speaks directly about six years of fighting the system, the evidence vault, and what advocacy looks like from the inside.",
    featured: false,
  },
  {
    outlet: "ICWA Advocates Network",
    title: "Case Study: Systematic ICWA Non-Compliance in Family Court",
    type: "Article",
    date: "February 2025",
    desc: "Legal advocacy organization's analysis of ICWA violations documented in Case 21DP0705A.",
    featured: false,
  },
  {
    outlet: "Community Justice Report",
    title: "Pro Se vs. the State: One Father's Federal Fight",
    type: "Article",
    date: "January 2025",
    desc: "Profile of Jason R. Barr and the strategic legal filings he has made without counsel in federal court.",
    featured: false,
  },
  {
    outlet: "Advocacy Documentary Series",
    title: "Bring Bella Home — Short Documentary",
    type: "Video",
    date: "December 2024",
    desc: "Short-form documentary on the case, the evidence, and the community that has mobilized around Bella's return.",
    featured: true,
  },
  {
    outlet: "Family Law Observer",
    title: "Due Process and the TPR: A Case Study in Constitutional Failure",
    type: "Article",
    date: "November 2024",
    desc: "Analysis of the procedural and constitutional issues raised by the termination of parental rights in this case.",
    featured: false,
  },
];

const statements = [
  {
    date: "June 20, 2025",
    title: "Statement on Filing of Federal TRO Motion",
    excerpt:
      "Today I filed a motion for temporary restraining order in federal court. I am asking a federal judge to stop the adoption proceedings while my constitutional claims are heard. This is not a delay tactic — it is the only remaining avenue to prevent an irreversible harm from occurring before the courts have had a chance to evaluate six years of documented evidence.",
  },
  {
    date: "April 12, 2025",
    title: "Statement on Habeas Corpus Filing",
    excerpt:
      "The Habeas Corpus petition is a statement that my daughter's separation from her father is not simply a state family court matter. It is a federal constitutional question. Due process was denied. ICWA was violated. I am bringing these claims to a federal court and asking them to act.",
  },
  {
    date: "March 5, 2025",
    title: "Statement on §1983 Federal Complaint",
    excerpt:
      "Filing this federal civil rights complaint is not an act of desperation — it is an act of documentation. Every violation in this case is on the record. Every misrepresentation, every suppressed report, every procedural shortcut is documented. I am asking a federal court to look at what the state did and call it what it is.",
  },
];

export default function MediaPressPage() {
  const [pressFormSubmitted, setPressFormSubmitted] = useState(false);
  const [pressEmail, setPressEmail] = useState("");
  const [pressName, setPressName] = useState("");
  const [pressOutlet, setPressOutlet] = useState("");

  const handlePressSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setPressFormSubmitted(true);
  };

  return (
    <div style={{ background: "var(--color-warm)" }}>
      {/* ── HEADER ── */}
      <section
        style={{ background: "var(--color-navy)", padding: "64px 16px" }}
      >
        <div
          style={{ maxWidth: "var(--max-width-content)", margin: "0 auto" }}
        >
          <span
            style={{
              color: "var(--color-gold)",
              fontSize: "0.8rem",
              fontWeight: 700,
              letterSpacing: "0.14em",
              textTransform: "uppercase",
            }}
          >
            Media &amp; Press
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
            Media &amp; Press Room
          </h1>
          <p
            style={{
              color: "rgba(255,255,255,0.7)",
              fontSize: "1rem",
              maxWidth: "560px",
              lineHeight: 1.7,
              marginBottom: "24px",
            }}
          >
            Journalists, documentarians, and media professionals — we welcome
            responsible coverage of this case. Everything you need for accurate
            reporting is here.
          </p>
          <div className="flex flex-col sm:flex-row gap-3">
            <a
              href="#press-kit"
              className="btn-primary inline-flex items-center gap-2"
            >
              <Download size={16} />
              Download Press Kit
            </a>
            <a
              href="#press-contact"
              className="btn-secondary inline-flex items-center gap-2"
            >
              Contact Press Team
            </a>
          </div>
        </div>
      </section>

      {/* ── PRESS KIT ── */}
      <section id="press-kit" className="section-padding">
        <div
          style={{ maxWidth: "var(--max-width-content)", margin: "0 auto" }}
          className="px-4"
        >
          <h2
            style={{
              fontFamily: "var(--font-serif)",
              fontSize: "1.6rem",
              color: "var(--color-navy)",
              fontWeight: 700,
              marginBottom: "8px",
            }}
          >
            Press Kit Downloads
          </h2>
          <p
            style={{
              color: "var(--color-charcoal)",
              fontSize: "0.9rem",
              marginBottom: "24px",
              opacity: 0.8,
            }}
          >
            All materials are free to use with attribution. Please contact us
            before publishing to ensure accuracy.
          </p>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-16">
            {pressKitItems.map((item) => (
              <div
                key={item.title}
                style={{
                  background: "white",
                  border: "1px solid var(--color-light-gray)",
                  borderRadius: "10px",
                  padding: "18px 20px",
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "center",
                }}
              >
                <div className="flex items-center gap-3">
                  <div
                    style={{
                      width: "40px",
                      height: "40px",
                      background: "rgba(201,162,39,0.1)",
                      borderRadius: "8px",
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                      flexShrink: 0,
                    }}
                  >
                    <FileText
                      size={18}
                      style={{ color: "var(--color-gold)" }}
                    />
                  </div>
                  <div>
                    <p
                      style={{
                        fontWeight: 600,
                        fontSize: "0.9rem",
                        color: "var(--color-navy)",
                        marginBottom: "3px",
                      }}
                    >
                      {item.title}
                    </p>
                    <p
                      style={{
                        color: "var(--color-charcoal)",
                        fontSize: "0.78rem",
                        opacity: 0.6,
                      }}
                    >
                      {item.format} — {item.size}
                    </p>
                  </div>
                </div>
                <button
                  style={{
                    background: "var(--color-gold)",
                    color: "var(--color-navy)",
                    border: "none",
                    borderRadius: "6px",
                    padding: "8px 16px",
                    fontSize: "0.8rem",
                    fontWeight: 700,
                    cursor: "pointer",
                    display: "flex",
                    alignItems: "center",
                    gap: "6px",
                    flexShrink: 0,
                    marginLeft: "12px",
                  }}
                >
                  <Download size={14} />
                  Download
                </button>
              </div>
            ))}
          </div>

          {/* ── MEDIA COVERAGE ── */}
          <h2
            style={{
              fontFamily: "var(--font-serif)",
              fontSize: "1.6rem",
              color: "var(--color-navy)",
              fontWeight: 700,
              marginBottom: "24px",
            }}
          >
            Media Coverage
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-16">
            {coverage.map((item, idx) => (
              <div
                key={idx}
                className="card"
                style={{
                  padding: "24px",
                  borderTop: item.featured
                    ? "4px solid var(--color-gold)"
                    : "4px solid var(--color-light-gray)",
                }}
              >
                <div className="flex items-center gap-2 mb-3 flex-wrap">
                  {item.featured && (
                    <span
                      style={{
                        background: "var(--color-gold)",
                        color: "var(--color-navy)",
                        fontSize: "0.65rem",
                        fontWeight: 700,
                        padding: "2px 8px",
                        borderRadius: "100px",
                      }}
                    >
                      FEATURED
                    </span>
                  )}
                  <span
                    style={{
                      background:
                        item.type === "Video"
                          ? "rgba(220,38,38,0.1)"
                          : "var(--color-light-gray)",
                      color:
                        item.type === "Video"
                          ? "var(--color-crimson)"
                          : "var(--color-navy)",
                      fontSize: "0.65rem",
                      fontWeight: 700,
                      padding: "2px 8px",
                      borderRadius: "100px",
                    }}
                  >
                    {item.type}
                  </span>
                  <span
                    style={{
                      color: "var(--color-charcoal)",
                      fontSize: "0.75rem",
                      opacity: 0.6,
                    }}
                  >
                    {item.date}
                  </span>
                </div>

                {item.type === "Video" && (
                  <div
                    style={{
                      height: "80px",
                      background: "var(--color-navy)",
                      borderRadius: "8px",
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                      marginBottom: "14px",
                    }}
                  >
                    <div
                      style={{
                        width: "40px",
                        height: "40px",
                        background: "var(--color-gold)",
                        borderRadius: "50%",
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "center",
                      }}
                    >
                      <Play
                        size={16}
                        style={{
                          color: "var(--color-navy)",
                          fill: "var(--color-navy)",
                          marginLeft: "2px",
                        }}
                      />
                    </div>
                  </div>
                )}

                <p
                  style={{
                    color: "var(--color-gold)",
                    fontSize: "0.78rem",
                    fontWeight: 600,
                    marginBottom: "6px",
                  }}
                >
                  {item.outlet}
                </p>

                <h4
                  style={{
                    fontFamily: "var(--font-serif)",
                    fontSize: "1rem",
                    color: "var(--color-navy)",
                    fontWeight: 700,
                    lineHeight: 1.3,
                    marginBottom: "8px",
                  }}
                >
                  {item.title}
                </h4>

                <p
                  style={{
                    color: "var(--color-charcoal)",
                    fontSize: "0.85rem",
                    lineHeight: 1.6,
                    marginBottom: "12px",
                  }}
                >
                  {item.desc}
                </p>

                <button
                  style={{
                    background: "transparent",
                    border: "1px solid var(--color-light-gray)",
                    borderRadius: "6px",
                    padding: "6px 14px",
                    fontSize: "0.8rem",
                    fontWeight: 600,
                    cursor: "pointer",
                    color: "var(--color-navy)",
                    display: "inline-flex",
                    alignItems: "center",
                    gap: "4px",
                  }}
                >
                  {item.type === "Video" ? (
                    <><Play size={12} /> Watch</>
                  ) : (
                    <><FileText size={12} /> Read</>
                  )}
                </button>
              </div>
            ))}
          </div>

          {/* ── OFFICIAL STATEMENTS ── */}
          <h2
            style={{
              fontFamily: "var(--font-serif)",
              fontSize: "1.6rem",
              color: "var(--color-navy)",
              fontWeight: 700,
              marginBottom: "24px",
            }}
          >
            Official Statements
          </h2>
          <p
            style={{
              color: "var(--color-charcoal)",
              fontSize: "0.9rem",
              marginBottom: "24px",
              opacity: 0.8,
            }}
          >
            Statements from Jason R. Barr regarding major case developments.
            These statements may be quoted with attribution.
          </p>

          <div className="flex flex-col gap-6 mb-16">
            {statements.map((stmt, idx) => (
              <div
                key={idx}
                style={{
                  background: "white",
                  border: "1px solid var(--color-light-gray)",
                  borderRadius: "12px",
                  padding: "28px",
                  borderLeft: "4px solid var(--color-gold)",
                }}
              >
                <div className="flex justify-between items-start flex-wrap gap-3 mb-4">
                  <div>
                    <p
                      style={{
                        color: "var(--color-gold)",
                        fontSize: "0.8rem",
                        fontWeight: 700,
                        marginBottom: "4px",
                      }}
                    >
                      {stmt.date}
                    </p>
                    <h4
                      style={{
                        fontFamily: "var(--font-serif)",
                        fontSize: "1.05rem",
                        color: "var(--color-navy)",
                        fontWeight: 700,
                        lineHeight: 1.3,
                      }}
                    >
                      {stmt.title}
                    </h4>
                  </div>
                  <button
                    style={{
                      background: "var(--color-light-gray)",
                      border: "none",
                      borderRadius: "6px",
                      padding: "6px 14px",
                      fontSize: "0.78rem",
                      fontWeight: 600,
                      cursor: "pointer",
                      color: "var(--color-navy)",
                      display: "flex",
                      alignItems: "center",
                      gap: "4px",
                      flexShrink: 0,
                    }}
                  >
                    <Download size={12} />
                    PDF
                  </button>
                </div>

                <blockquote
                  style={{
                    borderLeft: "3px solid rgba(201,162,39,0.3)",
                    paddingLeft: "16px",
                    margin: 0,
                    fontStyle: "italic",
                    color: "var(--color-charcoal)",
                    fontSize: "0.9rem",
                    lineHeight: 1.7,
                  }}
                >
                  &ldquo;{stmt.excerpt}&rdquo;
                </blockquote>

                <p
                  style={{
                    marginTop: "12px",
                    color: "var(--color-charcoal)",
                    fontSize: "0.8rem",
                    opacity: 0.6,
                    fontStyle: "normal",
                  }}
                >
                  — Jason R. Barr, father and pro se litigant, Case 21DP0705A
                </p>
              </div>
            ))}
          </div>

          {/* ── PRESS CONTACT FORM ── */}
          <div
            id="press-contact"
            style={{
              background: "var(--color-navy)",
              borderRadius: "16px",
              padding: "40px",
            }}
          >
            <div className="flex flex-col md:flex-row gap-12">
              <div className="flex-1">
                <Scale
                  size={32}
                  style={{ color: "var(--color-gold)", marginBottom: "16px" }}
                />
                <h2
                  style={{
                    fontFamily: "var(--font-serif)",
                    fontSize: "1.5rem",
                    color: "var(--color-gold)",
                    fontWeight: 700,
                    marginBottom: "12px",
                  }}
                >
                  Press Contact
                </h2>
                <p
                  style={{
                    color: "rgba(255,255,255,0.65)",
                    fontSize: "0.9rem",
                    lineHeight: 1.7,
                    marginBottom: "20px",
                  }}
                >
                  We respond to media inquiries within 24 hours. Please include
                  your outlet, deadline, and specific questions for the fastest
                  response.
                </p>

                <div className="flex flex-col gap-3">
                  <div
                    style={{
                      display: "flex",
                      alignItems: "center",
                      gap: "8px",
                      color: "rgba(255,255,255,0.7)",
                      fontSize: "0.88rem",
                    }}
                  >
                    <AlertTriangle
                      size={14}
                      style={{ color: "var(--color-crimson)" }}
                    />
                    Urgency: September 16, 2026 deadline — time-sensitive stories
                    prioritized
                  </div>
                  <div
                    style={{
                      display: "flex",
                      alignItems: "center",
                      gap: "8px",
                      color: "rgba(255,255,255,0.7)",
                      fontSize: "0.88rem",
                    }}
                  >
                    <FileText
                      size={14}
                      style={{ color: "var(--color-gold)" }}
                    />
                    Press embargoes honored on request
                  </div>
                </div>
              </div>

              <div className="flex-1">
                {pressFormSubmitted ? (
                  <div
                    style={{
                      background: "rgba(22,163,74,0.15)",
                      border: "1px solid #16a34a",
                      borderRadius: "10px",
                      padding: "24px",
                      textAlign: "center",
                      color: "white",
                    }}
                  >
                    <p style={{ fontWeight: 700, marginBottom: "8px" }}>
                      Press inquiry received
                    </p>
                    <p style={{ fontSize: "0.88rem", opacity: 0.8 }}>
                      We&apos;ll respond within 24 hours.
                    </p>
                  </div>
                ) : (
                  <form onSubmit={handlePressSubmit} className="flex flex-col gap-4">
                    <input
                      type="text"
                      required
                      value={pressName}
                      onChange={(e) => setPressName(e.target.value)}
                      placeholder="Your name"
                      style={{
                        padding: "12px 16px",
                        borderRadius: "8px",
                        border: "none",
                        fontSize: "0.9rem",
                        outline: "none",
                      }}
                    />
                    <input
                      type="email"
                      required
                      value={pressEmail}
                      onChange={(e) => setPressEmail(e.target.value)}
                      placeholder="Press email address"
                      style={{
                        padding: "12px 16px",
                        borderRadius: "8px",
                        border: "none",
                        fontSize: "0.9rem",
                        outline: "none",
                      }}
                    />
                    <input
                      type="text"
                      value={pressOutlet}
                      onChange={(e) => setPressOutlet(e.target.value)}
                      placeholder="Media outlet / publication"
                      style={{
                        padding: "12px 16px",
                        borderRadius: "8px",
                        border: "none",
                        fontSize: "0.9rem",
                        outline: "none",
                      }}
                    />
                    <textarea
                      rows={4}
                      placeholder="Your inquiry, including deadline if applicable..."
                      style={{
                        padding: "12px 16px",
                        borderRadius: "8px",
                        border: "none",
                        fontSize: "0.9rem",
                        outline: "none",
                        resize: "vertical",
                        fontFamily: "var(--font-sans)",
                      }}
                    />
                    <button
                      type="submit"
                      style={{
                        background: "var(--color-gold)",
                        color: "var(--color-navy)",
                        border: "none",
                        borderRadius: "8px",
                        padding: "14px",
                        fontSize: "0.95rem",
                        fontWeight: 700,
                        cursor: "pointer",
                      }}
                    >
                      Send Press Inquiry
                    </button>
                  </form>
                )}
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
