import type { Metadata } from "next";
import Link from "next/link";
import {
  Heart,
  Shield,
  FileText,
  Users,
  Play,
  AlertTriangle,
  Download,
  Scale,
  ChevronRight,
} from "lucide-react";

export const metadata: Metadata = {
  title: "Bring Bella Home | Justice for Neveyah-RosaBella Barr",
  description:
    "Join the fight to bring Neveyah-RosaBella 'Bella' Barr home to her father. Case 21DP0705A. Evidence. Truth. Justice. September 16, 2026 deadline.",
};

export default function BringBellaHomePage() {
  return (
    <div style={{ background: "var(--color-warm)" }}>
      {/* ── HERO ── */}
      <section
        style={{
          background: "var(--color-navy)",
          position: "relative",
          overflow: "hidden",
        }}
      >
        <div
          style={{
            position: "absolute",
            inset: 0,
            backgroundImage:
              "radial-gradient(ellipse at 70% 50%, rgba(201,162,39,0.08) 0%, transparent 60%)",
            pointerEvents: "none",
          }}
        />
        <div
          style={{ maxWidth: "var(--max-width-content)", margin: "0 auto" }}
          className="section-padding px-4 relative"
        >
          <div className="flex flex-col md:flex-row items-center gap-12">
            <div className="flex-1 text-center md:text-left">
              <div className="inline-flex items-center gap-2 mb-6">
                <span
                  style={{
                    background: "rgba(201,162,39,0.15)",
                    border: "1px solid var(--color-gold)",
                    color: "var(--color-gold)",
                    fontSize: "0.75rem",
                    fontWeight: 700,
                    letterSpacing: "0.12em",
                    padding: "4px 14px",
                    borderRadius: "100px",
                    textTransform: "uppercase",
                  }}
                >
                  Case 21DP0705A
                </span>
                <span
                  style={{
                    background: "var(--color-crimson)",
                    color: "white",
                    fontSize: "0.7rem",
                    fontWeight: 700,
                    letterSpacing: "0.1em",
                    padding: "4px 12px",
                    borderRadius: "100px",
                    textTransform: "uppercase",
                  }}
                >
                  URGENT
                </span>
              </div>

              <h1
                style={{
                  fontFamily: "var(--font-serif)",
                  fontSize: "clamp(2.5rem, 6vw, 4.5rem)",
                  fontWeight: 900,
                  color: "var(--color-gold)",
                  lineHeight: 1.1,
                  marginBottom: "16px",
                  letterSpacing: "-0.02em",
                }}
              >
                BRING
                <br />
                BELLA HOME
              </h1>

              <p
                style={{
                  fontSize: "1.25rem",
                  color: "rgba(255,255,255,0.9)",
                  marginBottom: "8px",
                  fontStyle: "italic",
                  fontFamily: "var(--font-serif)",
                }}
              >
                Neveyah-RosaBella &ldquo;Bella&rdquo; Barr
              </p>

              <p
                style={{
                  fontSize: "1rem",
                  color: "rgba(255,255,255,0.65)",
                  marginBottom: "32px",
                  maxWidth: "520px",
                }}
              >
                A daughter wrongfully removed. A father who never stopped
                fighting. Six years of documented evidence, court violations,
                and systemic failure — all demanding one answer: bring her home.
              </p>

              <div
                style={{
                  background: "rgba(220,38,38,0.15)",
                  border: "1px solid var(--color-crimson)",
                  borderRadius: "10px",
                  padding: "16px 20px",
                  marginBottom: "32px",
                  maxWidth: "480px",
                }}
              >
                <div className="flex items-center gap-3">
                  <AlertTriangle
                    size={20}
                    style={{ color: "var(--color-crimson)", flexShrink: 0 }}
                  />
                  <div>
                    <p
                      style={{
                        color: "var(--color-crimson)",
                        fontWeight: 700,
                        fontSize: "0.875rem",
                        marginBottom: "2px",
                      }}
                    >
                      ADOPTION FINALIZATION DEADLINE
                    </p>
                    <p
                      style={{
                        color: "rgba(255,255,255,0.8)",
                        fontSize: "0.875rem",
                      }}
                    >
                      September 16, 2026 — legal windows closing fast
                    </p>
                  </div>
                </div>
              </div>

              <div className="flex flex-col sm:flex-row gap-3">
                <Link href="/story" className="btn-primary">
                  Read Bella&apos;s Story
                </Link>
                <Link href="/evidence" className="btn-secondary">
                  View Evidence Vault
                </Link>
              </div>
            </div>

            <div style={{ flexShrink: 0 }}>
              <div
                style={{
                  width: "320px",
                  height: "380px",
                  borderRadius: "16px",
                  border: "3px solid var(--color-gold)",
                  background:
                    "linear-gradient(145deg, rgba(201,162,39,0.1) 0%, rgba(26,26,46,0.8) 100%)",
                  display: "flex",
                  flexDirection: "column",
                  alignItems: "center",
                  justifyContent: "center",
                  gap: "12px",
                }}
              >
                <Heart
                  size={64}
                  style={{ color: "var(--color-rose)", opacity: 0.7 }}
                />
                <p
                  style={{
                    color: "var(--color-gold)",
                    fontFamily: "var(--font-serif)",
                    fontSize: "1.1rem",
                    textAlign: "center",
                    padding: "0 24px",
                  }}
                >
                  Neveyah-RosaBella Barr
                </p>
                <p
                  style={{
                    color: "rgba(255,255,255,0.5)",
                    fontSize: "0.8rem",
                    textAlign: "center",
                    padding: "0 24px",
                  }}
                >
                  Photo withheld to protect minor
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ── STATS ROW ── */}
      <section style={{ background: "var(--color-gold)" }}>
        <div
          style={{ maxWidth: "var(--max-width-content)", margin: "0 auto" }}
          className="px-4 py-6"
        >
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-center">
            {[
              { number: "6+", label: "Years Fighting", sub: "Since 2019" },
              { number: "21DP0705A", label: "Case Number", sub: "On the record" },
              { number: "Sep 16, 2026", label: "Critical Deadline", sub: "Act now" },
            ].map((stat) => (
              <div key={stat.label}>
                <div
                  style={{
                    fontFamily: "var(--font-serif)",
                    fontSize: "2rem",
                    fontWeight: 900,
                    color: "var(--color-navy)",
                    lineHeight: 1,
                  }}
                >
                  {stat.number}
                </div>
                <div
                  style={{
                    color: "var(--color-navy)",
                    fontWeight: 700,
                    fontSize: "0.875rem",
                    letterSpacing: "0.08em",
                    textTransform: "uppercase",
                    marginTop: "4px",
                  }}
                >
                  {stat.label}
                </div>
                <div
                  style={{
                    color: "rgba(26,26,46,0.65)",
                    fontSize: "0.8rem",
                    marginTop: "2px",
                  }}
                >
                  {stat.sub}
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── STORY TEASER ── */}
      <section className="section-padding">
        <div
          style={{ maxWidth: "var(--max-width-content)", margin: "0 auto" }}
          className="px-4"
        >
          <div className="flex flex-col md:flex-row gap-12 items-center">
            <div style={{ flexShrink: 0, width: "360px", maxWidth: "100%" }}>
              <div
                style={{
                  width: "100%",
                  aspectRatio: "4/5",
                  borderRadius: "12px",
                  background:
                    "linear-gradient(145deg, var(--color-rose) 0%, var(--color-navy) 100%)",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  boxShadow: "0 24px 64px rgba(26,26,46,0.2)",
                }}
              >
                <div className="text-center p-8">
                  <Heart
                    size={48}
                    style={{ color: "white", opacity: 0.6, marginBottom: "12px" }}
                  />
                  <p
                    style={{
                      color: "white",
                      fontFamily: "var(--font-serif)",
                      fontSize: "1rem",
                      opacity: 0.9,
                    }}
                  >
                    Bella &amp; Jason Barr
                  </p>
                  <p
                    style={{
                      color: "rgba(255,255,255,0.6)",
                      fontSize: "0.75rem",
                      marginTop: "6px",
                    }}
                  >
                    Family photo — identities protected
                  </p>
                </div>
              </div>
            </div>

            <div className="flex-1">
              <span
                style={{
                  color: "var(--color-gold)",
                  fontSize: "0.8rem",
                  fontWeight: 700,
                  letterSpacing: "0.12em",
                  textTransform: "uppercase",
                }}
              >
                The Story
              </span>
              <h2
                style={{
                  fontFamily: "var(--font-serif)",
                  fontSize: "clamp(1.75rem, 3.5vw, 2.5rem)",
                  color: "var(--color-navy)",
                  fontWeight: 800,
                  marginTop: "8px",
                  marginBottom: "20px",
                  lineHeight: 1.2,
                }}
              >
                A Father&apos;s Fight Against
                <br />a Broken System
              </h2>

              <p
                style={{
                  color: "var(--color-charcoal)",
                  lineHeight: 1.8,
                  marginBottom: "16px",
                  fontSize: "1.05rem",
                }}
              >
                In 2019, Jason R. Barr&apos;s daughter Neveyah-RosaBella was
                removed from his care. What followed was not a rescue — it was
                a systematic dismantling of a family by state actors who
                suppressed evidence, ignored abuse reports, and violated the
                Indian Child Welfare Act at every turn.
              </p>

              <p
                style={{
                  color: "var(--color-charcoal)",
                  lineHeight: 1.8,
                  marginBottom: "24px",
                  fontSize: "1.05rem",
                }}
              >
                The November 27, 2023 incident — documented in audio recordings
                that have been authenticated and preserved — shows clearly what
                Bella endured in foster care. Despite multiple abuse reports
                filed by Jason, the state moved toward termination of parental
                rights. The wrongful TPR was finalized against a father who
                never stopped showing up, never stopped documenting, and never
                stopped fighting.
              </p>

              <blockquote className="pull-quote">
                &ldquo;They took my daughter. I took notes. Six years of notes,
                recordings, filings, and the truth is still here — and it will
                not be buried.&rdquo;
                <footer
                  style={{
                    fontSize: "0.85rem",
                    color: "var(--color-charcoal)",
                    marginTop: "8px",
                    fontStyle: "normal",
                    fontFamily: "var(--font-sans)",
                  }}
                >
                  — Jason R. Barr, father, pro se litigant
                </footer>
              </blockquote>

              <Link
                href="/story"
                className="btn-primary inline-flex items-center gap-2"
              >
                Read the Full Story
                <ChevronRight size={16} />
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* ── FEATURED AUDIO EVIDENCE ── */}
      <section
        style={{ background: "var(--color-navy)" }}
        className="section-padding"
      >
        <div
          style={{ maxWidth: "var(--max-width-content)", margin: "0 auto" }}
          className="px-4"
        >
          <div className="text-center mb-12">
            <span
              style={{
                color: "var(--color-gold)",
                fontSize: "0.8rem",
                fontWeight: 700,
                letterSpacing: "0.12em",
                textTransform: "uppercase",
              }}
            >
              Authenticated Evidence
            </span>
            <h2
              style={{
                fontFamily: "var(--font-serif)",
                fontSize: "clamp(1.75rem, 3vw, 2.25rem)",
                color: "white",
                fontWeight: 800,
                marginTop: "8px",
                marginBottom: "12px",
              }}
            >
              Evidence Vault — What the Record Shows
            </h2>
            <p
              style={{
                color: "rgba(255,255,255,0.65)",
                maxWidth: "560px",
                margin: "0 auto",
              }}
            >
              Every piece of evidence has been preserved, hashed, and
              time-stamped. The truth cannot be erased.
            </p>
          </div>

          <div
            style={{
              background: "rgba(255,255,255,0.05)",
              border: "1px solid rgba(201,162,39,0.3)",
              borderRadius: "16px",
              padding: "32px",
              marginBottom: "24px",
            }}
          >
            <div className="flex flex-col md:flex-row gap-8 items-start">
              <div className="flex-1">
                <div className="flex items-center gap-3 mb-4">
                  <span
                    style={{
                      background: "var(--color-crimson)",
                      color: "white",
                      fontSize: "0.7rem",
                      fontWeight: 700,
                      letterSpacing: "0.1em",
                      padding: "3px 10px",
                      borderRadius: "100px",
                      textTransform: "uppercase",
                    }}
                  >
                    FEATURED
                  </span>
                  <span
                    style={{
                      color: "var(--color-gold)",
                      fontSize: "0.8rem",
                      fontWeight: 600,
                    }}
                  >
                    Audio Recording
                  </span>
                </div>

                <h3
                  style={{
                    fontFamily: "var(--font-serif)",
                    fontSize: "1.4rem",
                    color: "white",
                    fontWeight: 700,
                    marginBottom: "8px",
                  }}
                >
                  November 27, 2023 — Incident Documentation
                </h3>

                <p
                  style={{
                    color: "rgba(255,255,255,0.65)",
                    fontSize: "0.9rem",
                    lineHeight: 1.7,
                    marginBottom: "16px",
                  }}
                >
                  Audio recording documenting the incident of November 27, 2023.
                  This recording was submitted to the court and preserved in the
                  evidence vault. It directly contradicts statements made by
                  foster care agents in subsequent court filings.
                </p>

                <div className="waveform mb-4" />

                <div
                  style={{
                    background: "rgba(201,162,39,0.1)",
                    border: "1px solid rgba(201,162,39,0.2)",
                    borderRadius: "8px",
                    padding: "12px 16px",
                    display: "flex",
                    alignItems: "center",
                    gap: "12px",
                    marginBottom: "16px",
                  }}
                >
                  <div
                    style={{
                      background: "var(--color-gold)",
                      borderRadius: "50%",
                      width: "40px",
                      height: "40px",
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                      flexShrink: 0,
                    }}
                  >
                    <Play
                      size={16}
                      style={{
                        color: "var(--color-navy)",
                        marginLeft: "2px",
                        fill: "var(--color-navy)",
                      }}
                    />
                  </div>
                  <div style={{ flex: 1 }}>
                    <div
                      style={{
                        height: "4px",
                        background: "rgba(255,255,255,0.15)",
                        borderRadius: "2px",
                      }}
                    />
                  </div>
                  <span
                    style={{
                      color: "rgba(255,255,255,0.5)",
                      fontSize: "0.8rem",
                      flexShrink: 0,
                    }}
                  >
                    14:32
                  </span>
                </div>

                <div className="flex items-center gap-2 flex-wrap">
                  <Shield
                    size={14}
                    style={{ color: "var(--color-gold)", flexShrink: 0 }}
                  />
                  <span
                    style={{
                      color: "rgba(255,255,255,0.45)",
                      fontSize: "0.75rem",
                    }}
                  >
                    SHA-256:
                  </span>
                  <span className="evidence-badge">a3f9c2...8b4e17</span>
                  <span
                    style={{
                      color: "rgba(255,255,255,0.45)",
                      fontSize: "0.75rem",
                    }}
                  >
                    Authenticated
                  </span>
                </div>
              </div>

              <div style={{ flexShrink: 0 }} className="flex flex-col gap-3">
                <Link
                  href="/evidence"
                  className="btn-secondary flex items-center gap-2"
                  style={{ whiteSpace: "nowrap" }}
                >
                  <FileText size={16} />
                  View Full Vault
                </Link>
                <div
                  style={{
                    display: "flex",
                    alignItems: "center",
                    gap: "8px",
                    border: "1px solid rgba(255,255,255,0.2)",
                    color: "rgba(255,255,255,0.7)",
                    padding: "12px 20px",
                    borderRadius: "8px",
                    fontSize: "0.875rem",
                    fontWeight: 600,
                    whiteSpace: "nowrap",
                  }}
                >
                  <Download size={16} />
                  Download Package
                </div>
              </div>
            </div>
          </div>

          <div className="text-center">
            <Link
              href="/evidence"
              style={{
                color: "var(--color-gold)",
                textDecoration: "none",
                fontSize: "0.9rem",
                fontWeight: 600,
              }}
            >
              View all 47 evidence items in the vault →
            </Link>
          </div>
        </div>
      </section>

      {/* ── TIMELINE TEASER ── */}
      <section
        className="section-padding"
        style={{ background: "var(--color-light-gray)" }}
      >
        <div
          style={{ maxWidth: "var(--max-width-content)", margin: "0 auto" }}
          className="px-4"
        >
          <div className="text-center mb-12">
            <span
              style={{
                color: "var(--color-gold)",
                fontSize: "0.8rem",
                fontWeight: 700,
                letterSpacing: "0.12em",
                textTransform: "uppercase",
              }}
            >
              Timeline
            </span>
            <h2
              style={{
                fontFamily: "var(--font-serif)",
                fontSize: "clamp(1.75rem, 3vw, 2.25rem)",
                color: "var(--color-navy)",
                fontWeight: 800,
                marginTop: "8px",
              }}
            >
              Six Years of Fighting
            </h2>
          </div>

          <div style={{ maxWidth: "700px", margin: "0 auto" }}>
            {(
              [
                {
                  date: "2019",
                  title: "Initial Removal",
                  desc: "Neveyah-RosaBella removed from Jason's care under disputed circumstances. ICWA protections not applied.",
                  type: "critical",
                },
                {
                  date: "2020–2021",
                  title: "Abuse Reports Filed",
                  desc: "Jason files multiple documented reports of abuse occurring in foster placement. Reports are ignored or suppressed.",
                  type: "warning",
                },
                {
                  date: "Nov 27, 2023",
                  title: "The Incident — Audio Documented",
                  desc: "Critical incident documented via authenticated audio recording. Evidence preserved and hashed to SHA-256.",
                  type: "critical",
                },
                {
                  date: "2024",
                  title: "Wrongful TPR Finalized",
                  desc: "Termination of Parental Rights finalized despite pending federal complaints and documented procedural violations.",
                  type: "critical",
                },
                {
                  date: "2025",
                  title: "Federal Complaints Filed",
                  desc: "Jason files §1983 civil rights complaint, Habeas Corpus petition, and TRO motion in federal court. Pro se.",
                  type: "action",
                },
                {
                  date: "Sep 16, 2026",
                  title: "Critical Deadline",
                  desc: "Adoption finalization looms. Every day of inaction narrows the legal windows available.",
                  type: "deadline",
                },
              ] as const
            ).map((event, idx) => (
              <div key={idx} className="flex gap-6 mb-8">
                <div
                  className="flex flex-col items-center"
                  style={{ flexShrink: 0 }}
                >
                  <div
                    style={{
                      width: "16px",
                      height: "16px",
                      borderRadius: "50%",
                      background:
                        event.type === "deadline" || event.type === "critical"
                          ? "var(--color-crimson)"
                          : "var(--color-gold)",
                      flexShrink: 0,
                      marginTop: "4px",
                      border: "3px solid white",
                      boxShadow: "0 0 0 2px var(--color-gold)",
                    }}
                  />
                  {idx < 5 && (
                    <div
                      style={{
                        width: "2px",
                        flex: 1,
                        background: "var(--color-gold)",
                        opacity: 0.4,
                        marginTop: "4px",
                        minHeight: "40px",
                      }}
                    />
                  )}
                </div>

                <div style={{ paddingBottom: "8px" }}>
                  <span
                    style={{
                      color: "var(--color-gold)",
                      fontSize: "0.8rem",
                      fontWeight: 700,
                      letterSpacing: "0.06em",
                    }}
                  >
                    {event.date}
                  </span>
                  <h3
                    style={{
                      fontFamily: "var(--font-serif)",
                      fontSize: "1.1rem",
                      color:
                        event.type === "deadline"
                          ? "var(--color-crimson)"
                          : "var(--color-navy)",
                      fontWeight: 700,
                      marginTop: "2px",
                      marginBottom: "6px",
                    }}
                  >
                    {event.title}
                  </h3>
                  <p
                    style={{
                      color: "var(--color-charcoal)",
                      fontSize: "0.9rem",
                      lineHeight: 1.6,
                    }}
                  >
                    {event.desc}
                  </p>
                </div>
              </div>
            ))}
          </div>

          <div className="text-center mt-8">
            <Link
              href="/story#timeline"
              className="btn-primary inline-flex items-center gap-2"
            >
              View Full Interactive Timeline
              <ChevronRight size={16} />
            </Link>
          </div>
        </div>
      </section>

      {/* ── HOW YOU CAN HELP ── */}
      <section className="section-padding">
        <div
          style={{ maxWidth: "var(--max-width-content)", margin: "0 auto" }}
          className="px-4"
        >
          <div className="text-center mb-12">
            <span
              style={{
                color: "var(--color-gold)",
                fontSize: "0.8rem",
                fontWeight: 700,
                letterSpacing: "0.12em",
                textTransform: "uppercase",
              }}
            >
              Take Action
            </span>
            <h2
              style={{
                fontFamily: "var(--font-serif)",
                fontSize: "clamp(1.75rem, 3vw, 2.25rem)",
                color: "var(--color-navy)",
                fontWeight: 800,
                marginTop: "8px",
                marginBottom: "12px",
              }}
            >
              How You Can Help
            </h2>
            <p
              style={{
                color: "var(--color-charcoal)",
                maxWidth: "480px",
                margin: "0 auto",
              }}
            >
              This fight belongs to all of us who believe in family, in truth,
              and in accountability.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div
              className="card"
              style={{
                padding: "32px",
                borderTop: "4px solid var(--color-gold)",
                textAlign: "center",
              }}
            >
              <div
                style={{
                  width: "56px",
                  height: "56px",
                  background: "rgba(201,162,39,0.1)",
                  borderRadius: "12px",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  margin: "0 auto 20px",
                }}
              >
                <Heart size={28} style={{ color: "var(--color-gold)" }} />
              </div>
              <h3
                style={{
                  fontFamily: "var(--font-serif)",
                  fontSize: "1.3rem",
                  color: "var(--color-navy)",
                  fontWeight: 700,
                  marginBottom: "12px",
                }}
              >
                Donate
              </h3>
              <p
                style={{
                  color: "var(--color-charcoal)",
                  lineHeight: 1.7,
                  marginBottom: "24px",
                  fontSize: "0.9rem",
                }}
              >
                Legal fees, court filing costs, and travel expenses mount
                quickly when fighting a well-funded state system. Every dollar
                goes directly to Bella&apos;s case.
              </p>
              <Link
                href="/donate"
                className="btn-primary"
                style={{ fontSize: "0.9rem" }}
              >
                Donate Now
              </Link>
            </div>

            <div
              className="card"
              style={{
                padding: "32px",
                borderTop: "4px solid var(--color-rose)",
                textAlign: "center",
              }}
            >
              <div
                style={{
                  width: "56px",
                  height: "56px",
                  background: "rgba(232,180,184,0.2)",
                  borderRadius: "12px",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  margin: "0 auto 20px",
                }}
              >
                <Users size={28} style={{ color: "var(--color-rose)" }} />
              </div>
              <h3
                style={{
                  fontFamily: "var(--font-serif)",
                  fontSize: "1.3rem",
                  color: "var(--color-navy)",
                  fontWeight: 700,
                  marginBottom: "12px",
                }}
              >
                Join Bella&apos;s Army
              </h3>
              <p
                style={{
                  color: "var(--color-charcoal)",
                  lineHeight: 1.7,
                  marginBottom: "24px",
                  fontSize: "0.9rem",
                }}
              >
                2,847 supporters and counting. Sign petitions, call
                representatives, attend rallies, and spread the word. Public
                pressure changes outcomes.
              </p>
              <Link
                href="/army"
                className="btn-secondary"
                style={{ fontSize: "0.9rem" }}
              >
                Join the Fight
              </Link>
            </div>

            <div
              className="card"
              style={{
                padding: "32px",
                borderTop: "4px solid var(--color-crimson)",
                textAlign: "center",
              }}
            >
              <div
                style={{
                  width: "56px",
                  height: "56px",
                  background: "rgba(220,38,38,0.08)",
                  borderRadius: "12px",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  margin: "0 auto 20px",
                }}
              >
                <Scale size={28} style={{ color: "var(--color-crimson)" }} />
              </div>
              <h3
                style={{
                  fontFamily: "var(--font-serif)",
                  fontSize: "1.3rem",
                  color: "var(--color-navy)",
                  fontWeight: 700,
                  marginBottom: "12px",
                }}
              >
                Review the Evidence
              </h3>
              <p
                style={{
                  color: "var(--color-charcoal)",
                  lineHeight: 1.7,
                  marginBottom: "24px",
                  fontSize: "0.9rem",
                }}
              >
                Journalists, legal observers, and advocates — the evidence vault
                is fully documented with SHA-256 authentication. Share what you
                find.
              </p>
              <Link
                href="/evidence"
                className="btn-crimson"
                style={{ fontSize: "0.9rem" }}
              >
                Open Evidence Vault
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* ── URGENT CTA ── */}
      <section
        style={{ background: "var(--color-crimson)" }}
        className="section-padding"
      >
        <div
          style={{ maxWidth: "700px", margin: "0 auto" }}
          className="px-4 text-center"
        >
          <AlertTriangle
            size={48}
            style={{ color: "white", margin: "0 auto 16px", opacity: 0.9 }}
          />
          <h2
            style={{
              fontFamily: "var(--font-serif)",
              fontSize: "clamp(1.75rem, 3.5vw, 2.75rem)",
              color: "white",
              fontWeight: 900,
              marginBottom: "16px",
              lineHeight: 1.2,
            }}
          >
            Time Is Running Out
          </h2>
          <p
            style={{
              color: "rgba(255,255,255,0.9)",
              fontSize: "1.1rem",
              lineHeight: 1.7,
              marginBottom: "32px",
            }}
          >
            September 16, 2026 is not a distant deadline — it is an active
            countdown. Once adoption is finalized, the legal pathways narrow
            dramatically. Jason R. Barr is fighting pro se against a system
            with unlimited resources. He needs your voice, your resources, and
            your solidarity — today.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              href="/donate"
              style={{
                background: "white",
                color: "var(--color-crimson)",
                fontWeight: 700,
                padding: "16px 36px",
                borderRadius: "8px",
                textDecoration: "none",
                fontSize: "1rem",
              }}
            >
              Donate Now
            </Link>
            <Link
              href="/legal"
              style={{
                border: "2px solid white",
                color: "white",
                fontWeight: 700,
                padding: "14px 36px",
                borderRadius: "8px",
                textDecoration: "none",
                fontSize: "1rem",
              }}
            >
              View Legal Actions
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
}
