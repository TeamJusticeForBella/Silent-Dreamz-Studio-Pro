"use client";

import { useState } from "react";
import Link from "next/link";
import { Scale, Shield, AlertTriangle, Heart, FileText } from "lucide-react";

const subjectOptions = [
  "General Inquiry",
  "Media / Press",
  "Legal Support (Attorney)",
  "Whistleblower / Tip",
  "Donation Question",
  "Ambassador Program",
  "Volunteer",
  "Other",
];

export default function ContactPage() {
  const [form, setForm] = useState({
    name: "",
    email: "",
    subject: "",
    message: "",
  });
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitted(true);
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
            Get In Touch
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
            Contact
          </h1>
          <p
            style={{
              color: "rgba(255,255,255,0.7)",
              fontSize: "1rem",
              maxWidth: "560px",
              lineHeight: 1.7,
            }}
          >
            Journalists, attorneys, advocates, supporters — we want to hear
            from you. Every credible tip, every legal offer of assistance, and
            every media inquiry matters.
          </p>
        </div>
      </section>

      <section className="section-padding">
        <div
          style={{ maxWidth: "var(--max-width-content)", margin: "0 auto" }}
          className="px-4"
        >
          <div className="flex flex-col md:flex-row gap-12">
            {/* Main Form */}
            <div className="flex-1">
              <h2
                style={{
                  fontFamily: "var(--font-serif)",
                  fontSize: "1.4rem",
                  color: "var(--color-navy)",
                  fontWeight: 700,
                  marginBottom: "24px",
                }}
              >
                Send a Message
              </h2>

              {submitted ? (
                <div
                  style={{
                    background: "rgba(22,163,74,0.1)",
                    border: "1px solid #16a34a",
                    borderRadius: "12px",
                    padding: "32px",
                    textAlign: "center",
                  }}
                >
                  <p
                    style={{
                      fontFamily: "var(--font-serif)",
                      fontSize: "1.3rem",
                      color: "var(--color-navy)",
                      fontWeight: 700,
                      marginBottom: "8px",
                    }}
                  >
                    Message Received
                  </p>
                  <p
                    style={{
                      color: "var(--color-charcoal)",
                      lineHeight: 1.7,
                      fontSize: "0.9rem",
                    }}
                  >
                    Thank you for reaching out. We review all messages and
                    respond to media and legal inquiries within 24 hours.
                    General inquiries may take 2–3 business days.
                  </p>
                </div>
              ) : (
                <form onSubmit={handleSubmit} className="flex flex-col gap-5">
                  <div className="flex flex-col md:flex-row gap-4">
                    <div style={{ flex: 1 }}>
                      <label
                        style={{
                          display: "block",
                          color: "var(--color-navy)",
                          fontSize: "0.85rem",
                          fontWeight: 600,
                          marginBottom: "6px",
                        }}
                      >
                        Full Name *
                      </label>
                      <input
                        type="text"
                        required
                        value={form.name}
                        onChange={(e) =>
                          setForm({ ...form, name: e.target.value })
                        }
                        placeholder="Your full name"
                        style={{
                          width: "100%",
                          padding: "12px 16px",
                          border: "1px solid var(--color-light-gray)",
                          borderRadius: "8px",
                          fontSize: "0.9rem",
                          outline: "none",
                          boxSizing: "border-box",
                        }}
                      />
                    </div>
                    <div style={{ flex: 1 }}>
                      <label
                        style={{
                          display: "block",
                          color: "var(--color-navy)",
                          fontSize: "0.85rem",
                          fontWeight: 600,
                          marginBottom: "6px",
                        }}
                      >
                        Email Address *
                      </label>
                      <input
                        type="email"
                        required
                        value={form.email}
                        onChange={(e) =>
                          setForm({ ...form, email: e.target.value })
                        }
                        placeholder="your@email.com"
                        style={{
                          width: "100%",
                          padding: "12px 16px",
                          border: "1px solid var(--color-light-gray)",
                          borderRadius: "8px",
                          fontSize: "0.9rem",
                          outline: "none",
                          boxSizing: "border-box",
                        }}
                      />
                    </div>
                  </div>

                  <div>
                    <label
                      style={{
                        display: "block",
                        color: "var(--color-navy)",
                        fontSize: "0.85rem",
                        fontWeight: 600,
                        marginBottom: "6px",
                      }}
                    >
                      Subject *
                    </label>
                    <select
                      required
                      value={form.subject}
                      onChange={(e) =>
                        setForm({ ...form, subject: e.target.value })
                      }
                      style={{
                        width: "100%",
                        padding: "12px 16px",
                        border: "1px solid var(--color-light-gray)",
                        borderRadius: "8px",
                        fontSize: "0.9rem",
                        outline: "none",
                        background: "white",
                        boxSizing: "border-box",
                      }}
                    >
                      <option value="">Select a subject...</option>
                      {subjectOptions.map((opt) => (
                        <option key={opt} value={opt}>
                          {opt}
                        </option>
                      ))}
                    </select>
                  </div>

                  <div>
                    <label
                      style={{
                        display: "block",
                        color: "var(--color-navy)",
                        fontSize: "0.85rem",
                        fontWeight: 600,
                        marginBottom: "6px",
                      }}
                    >
                      Message *
                    </label>
                    <textarea
                      required
                      rows={6}
                      value={form.message}
                      onChange={(e) =>
                        setForm({ ...form, message: e.target.value })
                      }
                      placeholder="Your message..."
                      style={{
                        width: "100%",
                        padding: "12px 16px",
                        border: "1px solid var(--color-light-gray)",
                        borderRadius: "8px",
                        fontSize: "0.9rem",
                        outline: "none",
                        resize: "vertical",
                        boxSizing: "border-box",
                        fontFamily: "var(--font-sans)",
                      }}
                    />
                  </div>

                  {/* File Attachment Placeholder */}
                  <div>
                    <label
                      style={{
                        display: "block",
                        color: "var(--color-navy)",
                        fontSize: "0.85rem",
                        fontWeight: 600,
                        marginBottom: "6px",
                      }}
                    >
                      Attach Files (Optional)
                    </label>
                    <div
                      style={{
                        border: "2px dashed var(--color-light-gray)",
                        borderRadius: "8px",
                        padding: "24px",
                        textAlign: "center",
                        cursor: "pointer",
                      }}
                    >
                      <FileText
                        size={24}
                        style={{
                          color: "var(--color-charcoal)",
                          opacity: 0.4,
                          margin: "0 auto 8px",
                        }}
                      />
                      <p
                        style={{
                          color: "var(--color-charcoal)",
                          fontSize: "0.85rem",
                          opacity: 0.6,
                        }}
                      >
                        Drop files here or click to attach
                      </p>
                      <p
                        style={{
                          color: "var(--color-charcoal)",
                          fontSize: "0.75rem",
                          opacity: 0.45,
                          marginTop: "4px",
                        }}
                      >
                        PDF, DOC, JPG, MP3, MP4 — Max 25MB
                      </p>
                    </div>
                  </div>

                  <button
                    type="submit"
                    className="btn-primary"
                    style={{ fontSize: "1rem", padding: "16px" }}
                  >
                    Send Message
                  </button>
                </form>
              )}
            </div>

            {/* Right: Supplemental Sections */}
            <div
              style={{ flexShrink: 0, width: "320px", maxWidth: "100%" }}
              className="flex flex-col gap-6"
            >
              {/* Resources for Families */}
              <div
                style={{
                  background: "white",
                  border: "1px solid var(--color-light-gray)",
                  borderRadius: "12px",
                  padding: "24px",
                }}
              >
                <div className="flex items-center gap-2 mb-4">
                  <Heart size={20} style={{ color: "var(--color-rose)" }} />
                  <h3
                    style={{
                      fontFamily: "var(--font-serif)",
                      fontSize: "1.05rem",
                      color: "var(--color-navy)",
                      fontWeight: 700,
                    }}
                  >
                    Resources for Families
                  </h3>
                </div>
                <p
                  style={{
                    color: "var(--color-charcoal)",
                    fontSize: "0.85rem",
                    lineHeight: 1.6,
                    marginBottom: "16px",
                  }}
                >
                  If you are a family navigating the child welfare system,
                  these resources may help:
                </p>
                <ul style={{ listStyle: "none", padding: 0, margin: 0 }}>
                  {[
                    "National ICWA Alliance",
                    "Child Welfare Information Gateway",
                    "National Family Preservation Network",
                    "Indian Child Welfare Act Resource Center",
                    "Parents Anonymous National",
                  ].map((r) => (
                    <li
                      key={r}
                      style={{
                        borderBottom: "1px solid var(--color-light-gray)",
                        padding: "8px 0",
                        fontSize: "0.85rem",
                        color: "var(--color-gold)",
                        fontWeight: 500,
                        cursor: "pointer",
                      }}
                    >
                      {r} →
                    </li>
                  ))}
                </ul>
              </div>

              {/* Whistleblower Hotline */}
              <div
                style={{
                  background: "var(--color-navy)",
                  borderRadius: "12px",
                  padding: "24px",
                }}
              >
                <div className="flex items-center gap-2 mb-4">
                  <Shield size={20} style={{ color: "var(--color-gold)" }} />
                  <h3
                    style={{
                      fontFamily: "var(--font-serif)",
                      fontSize: "1.05rem",
                      color: "var(--color-gold)",
                      fontWeight: 700,
                    }}
                  >
                    Anonymous Tip Line
                  </h3>
                </div>
                <p
                  style={{
                    color: "rgba(255,255,255,0.7)",
                    fontSize: "0.85rem",
                    lineHeight: 1.6,
                    marginBottom: "16px",
                  }}
                >
                  If you have information about Case 21DP0705A — including
                  knowledge of misconduct, suppressed evidence, or other
                  relevant facts — you can submit a tip anonymously. We take
                  all credible tips seriously.
                </p>
                <div
                  style={{
                    background: "rgba(201,162,39,0.1)",
                    border: "1px solid rgba(201,162,39,0.3)",
                    borderRadius: "8px",
                    padding: "16px",
                    marginBottom: "12px",
                  }}
                >
                  <p
                    style={{
                      color: "var(--color-gold)",
                      fontWeight: 700,
                      fontSize: "0.85rem",
                      marginBottom: "4px",
                    }}
                  >
                    Your identity is protected
                  </p>
                  <p
                    style={{
                      color: "rgba(255,255,255,0.6)",
                      fontSize: "0.8rem",
                    }}
                  >
                    Use the contact form above and select
                    &ldquo;Whistleblower / Tip&rdquo; as the subject.
                  </p>
                </div>
                <p
                  style={{
                    color: "rgba(255,255,255,0.45)",
                    fontSize: "0.75rem",
                  }}
                >
                  For fully anonymous submissions, consider using a VPN or
                  anonymous email service. We do not log IP addresses.
                </p>
              </div>

              {/* Emergency Contact */}
              <div
                style={{
                  background: "rgba(220,38,38,0.06)",
                  border: "1px solid rgba(220,38,38,0.2)",
                  borderRadius: "12px",
                  padding: "24px",
                }}
              >
                <div className="flex items-center gap-2 mb-3">
                  <AlertTriangle
                    size={18}
                    style={{ color: "var(--color-crimson)" }}
                  />
                  <h3
                    style={{
                      fontFamily: "var(--font-serif)",
                      fontSize: "1rem",
                      color: "var(--color-crimson)",
                      fontWeight: 700,
                    }}
                  >
                    Urgent / Emergency Contact
                  </h3>
                </div>
                <p
                  style={{
                    color: "var(--color-charcoal)",
                    fontSize: "0.85rem",
                    lineHeight: 1.6,
                    marginBottom: "12px",
                  }}
                >
                  For time-sensitive legal matters related to the September 16,
                  2026 deadline — attorneys with emergency injunction
                  experience especially — mark your message URGENT in the
                  subject line.
                </p>
                <p
                  style={{
                    color: "var(--color-crimson)",
                    fontWeight: 700,
                    fontSize: "0.85rem",
                  }}
                >
                  Deadline: Sep 16, 2026
                </p>
                <Link
                  href="/legal"
                  style={{
                    display: "block",
                    marginTop: "8px",
                    color: "var(--color-gold)",
                    textDecoration: "none",
                    fontSize: "0.82rem",
                    fontWeight: 600,
                  }}
                >
                  View active legal cases →
                </Link>
              </div>

              {/* Legal Support */}
              <div
                style={{
                  background: "var(--color-light-gray)",
                  borderRadius: "12px",
                  padding: "24px",
                }}
              >
                <div className="flex items-center gap-2 mb-3">
                  <Scale
                    size={18}
                    style={{ color: "var(--color-navy)" }}
                  />
                  <h3
                    style={{
                      fontFamily: "var(--font-serif)",
                      fontSize: "1rem",
                      color: "var(--color-navy)",
                      fontWeight: 700,
                    }}
                  >
                    Attorneys
                  </h3>
                </div>
                <p
                  style={{
                    color: "var(--color-charcoal)",
                    fontSize: "0.85rem",
                    lineHeight: 1.6,
                  }}
                >
                  Seeking pro bono counsel or consultation in federal civil
                  rights, ICWA, habeas corpus, or family law. Please use the
                  contact form with subject &ldquo;Legal Support (Attorney)&rdquo; and
                  include your bar number and jurisdiction.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
