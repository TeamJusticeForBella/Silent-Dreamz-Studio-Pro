import type { Metadata } from "next";
import Link from "next/link";
import {
  Heart,
  AlertTriangle,
  FileText,
  Shield,
  Scale,
  ChevronRight,
} from "lucide-react";

export const metadata: Metadata = {
  title: "Bella's Story",
  description:
    "The full story of Neveyah-RosaBella Barr — wrongful removal, ICWA violations, abuse in foster care, and a father's unrelenting fight for justice.",
};

const chapters = [
  {
    id: "beginning",
    number: "01",
    title: "The Beginning",
    subtitle: "A Family Before the State Intervened",
    content: [
      "Jason R. Barr is a father. That is the most important fact in this entire case — a fact that every court filing, every caseworker report, and every procedural maneuver has attempted to obscure. Before the state arrived, there was a family: Jason and his daughter Neveyah-RosaBella, called Bella, a child who laughed easily and held onto her father's hand.",
      "Jason was an active, present, and loving parent. He attended medical appointments, participated in school activities, and maintained a stable home environment. The record of that time — photographs, communications, witness accounts — is preserved in the evidence vault and available for any journalist or legal observer who seeks the truth.",
      "The initial contact with child protective services arose from a disputed complaint filed in 2019. What followed would reveal not a child welfare system working to protect a family, but one operating with institutional momentum toward removal regardless of the actual safety circumstances on the ground.",
    ],
    pullQuote: null,
  },
  {
    id: "removal",
    number: "02",
    title: "The Removal",
    subtitle: "How a Father Lost His Daughter to the System",
    content: [
      "In 2019, Neveyah-RosaBella was removed from Jason's care. The removal was swift, traumatic, and — as subsequent evidence would demonstrate — procedurally flawed from the outset. Jason was not given adequate notice. The emergency removal order was issued without sufficient evidentiary basis, and the initial placement decision failed to consider family preservation alternatives required by federal law.",
      "The Indian Child Welfare Act (ICWA) — a federal statute enacted specifically to prevent the unnecessary removal of Native American children from their families and tribal communities — was triggered by Bella's heritage. The obligations it imposes on state agencies are not suggestions; they are federal mandates. The state's failure to comply with ICWA from the first days of this case represents one of the most significant legal violations in the entire record.",
      "Jason responded immediately. He hired counsel, filed objections, and began documenting every contact, every communication, and every procedural event. He participated in every requested service. He passed every evaluation. He showed up, every single time — and was denied reunification at every turn.",
    ],
    pullQuote:
      "He passed every evaluation. He showed up, every single time — and was denied reunification at every turn.",
  },
  {
    id: "abuse-reports",
    number: "03",
    title: "The Abuse Reports",
    subtitle: "What Jason Documented — and What Was Ignored",
    content: [
      "Beginning in 2020 and continuing through 2023, Jason filed multiple formal reports documenting indicators of abuse occurring in Bella's foster placement. These were not vague concerns or unsubstantiated allegations — they were specific, timestamped, documented complaints submitted through official channels and supported by observable evidence.",
      "Each report was either dismissed without investigation or met with the bureaucratic equivalent of silence. The caseworkers who were statutorily obligated to investigate did not conduct meaningful inquiries. Court-appointed representatives who should have been Bella's voice failed to pursue the documented concerns. The institutional incentive — to close cases and finalize placements — overrode the legal obligation to protect a child in state care.",
      "The record of these reports, their filing dates, the responses received (or not received), and the subsequent evidence of what was occurring in the foster home forms a devastating paper trail. It is preserved in full in the evidence vault. Every document has been SHA-256 authenticated and is available for review by any court, journalist, or legal observer.",
    ],
    pullQuote:
      "The institutional incentive — to close cases and finalize placements — overrode the legal obligation to protect a child in state care.",
  },
  {
    id: "november-2023",
    number: "04",
    title: "November 27, 2023",
    subtitle: "The Incident That Changed Everything",
    content: [
      "On November 27, 2023, an incident occurred that crystallized everything Jason had been reporting for years. It was documented in real time via audio recording — a recording that has since been authenticated, preserved with a SHA-256 cryptographic hash, and submitted to the court record. The recording exists. It cannot be unheard.",
      "The details of what that recording contains are documented in the evidence vault. What matters for this narrative is what happened after: the system did not respond with urgency. There was no emergency protective action on Bella's behalf. The incident was minimized, reframed, and folded back into a narrative that continued pointing toward termination of Jason's parental rights rather than protection of his daughter.",
      "This is the moment that defines the systemic failure at the heart of Case 21DP0705A. A child was in demonstrable danger in state custody. Her father had documented it. The documentation is unambiguous. And the system's response was to continue the course toward permanent family separation.",
    ],
    pullQuote:
      "The recording exists. It cannot be unheard.",
  },
  {
    id: "icwa-failure",
    number: "05",
    title: "ICWA Failure",
    subtitle: "Federal Law Violated at Every Step",
    content: [
      "The Indian Child Welfare Act was signed into law in 1978 specifically because Congress recognized that state child welfare agencies were removing Native American children from their families at catastrophically disproportionate rates. The Act establishes specific procedural protections, evidentiary standards, and placement preferences designed to keep Native children connected to their families and tribal communities.",
      "In Case 21DP0705A, ICWA violations are not incidental — they are structural. Active efforts to prevent family breakup, as required by 25 U.S.C. § 1912(d), were not made in good faith. The heightened evidentiary standard for termination of parental rights — 'beyond a reasonable doubt' for certain findings — was not met. The placement preference hierarchy established by the Act was not followed.",
      "These are not technical procedural objections. They are the core of what makes this case a federal civil rights matter, not merely a state family court dispute. Jason has raised ICWA violations in every available forum. The federal complaints currently pending incorporate these violations as grounds for relief. A child's tribal heritage is not a technicality — it is a federally protected right.",
    ],
    pullQuote: null,
  },
  {
    id: "wrongful-tpr",
    number: "06",
    title: "Wrongful Termination of Parental Rights",
    subtitle: "A Legal Conclusion Built on a Compromised Process",
    content: [
      "The Termination of Parental Rights (TPR) in this case was not the product of a fair and impartial process. It was the endpoint of a proceeding in which critical evidence was withheld from the court, in which Jason's documented compliance with every service requirement was minimized, and in which the abuse reports he had filed were never properly adjudicated.",
      "A TPR is supposed to be a last resort — a recognition that no other outcome can serve the child's best interests. In this case, it was a first resort dressed up in procedural clothing. The standard for terminating a parent's rights is constitutionally significant: the Supreme Court has long recognized that parents have a fundamental liberty interest in the care and custody of their children. That interest requires due process. That due process was not provided.",
      "The record Jason has compiled — the communications, the court filings, the evidence submissions, the abuse reports, the compliance documentation — tells a different story than the one that was presented to the terminating court. That record is the foundation of every federal filing now pending. It is the reason this fight is not over.",
    ],
    pullQuote:
      "A TPR is supposed to be a last resort. In this case, it was a first resort dressed up in procedural clothing.",
  },
  {
    id: "fight-today",
    number: "07",
    title: "The Fight Today",
    subtitle: "Pro Se, Federal Courts, and a Deadline That Cannot Be Ignored",
    content: [
      "Jason R. Barr is currently litigating pro se in federal court. Without an attorney — because the legal fees associated with this case have been exhausted, because the state has unlimited resources and he does not — he is drafting and filing his own federal complaints, researching case law, and preparing motions that require the expertise of experienced civil rights counsel.",
      "The active litigation includes a 42 U.S.C. § 1983 civil rights complaint alleging constitutional violations, a Habeas Corpus petition challenging the unlawful detention of Bella from her father, and a TRO/Injunction motion seeking emergency relief before the September 16, 2026 adoption finalization deadline. These are not frivolous filings — they are grounded in documented evidence and established constitutional doctrine.",
      "September 16, 2026 is the critical date. Once adoption is finalized, the practical legal pathways for reversal narrow dramatically. This campaign exists to ensure that date does not arrive without maximum public attention, legal support, and pressure on every accountable party in this case.",
    ],
    pullQuote: null,
  },
  {
    id: "how-you-can-help",
    number: "08",
    title: "How You Can Help",
    subtitle: "Every Voice, Every Dollar, Every Share Matters",
    content: [
      "This case needs three things: resources, visibility, and legal support. On resources: Jason is fighting without institutional backing against a system with a budget and staff attorneys. Donations go directly to legal filing fees, document preparation, travel to court hearings, and the operational costs of maintaining this evidence-based advocacy campaign.",
      "On visibility: media attention changes the calculus for every actor in this case. When judges, caseworkers, and officials know that the public is watching — that every decision will be scrutinized — the accountability pressure increases. Share this campaign. Write about it. Post about it. Contact your representatives.",
      "On legal support: if you are an attorney licensed in the relevant jurisdiction — particularly one with experience in civil rights, ICWA, family law, or federal habeas practice — please reach out through the contact page. Pro bono representation or legal guidance could make the difference between a fight that is won and one that is lost for want of technical expertise. Bella is counting on the best of what this community can offer.",
    ],
    pullQuote:
      "Bella is counting on the best of what this community can offer.",
  },
];

const timelineEvents = [
  { year: "2019", event: "Initial removal — ICWA protections not invoked", type: "critical" },
  { year: "2019–2020", event: "Jason completes all required services, files objections, begins documentation", type: "action" },
  { year: "2020", event: "First formal abuse reports filed with CPS — no investigation", type: "warning" },
  { year: "2021", event: "Additional abuse reports filed — dismissed without adequate inquiry", type: "warning" },
  { year: "2021–2022", event: "ICWA violation raised in state court proceedings — not addressed", type: "critical" },
  { year: "2022", event: "TPR proceedings initiated despite lack of active reunification efforts", type: "critical" },
  { year: "Nov 27, 2023", event: "Incident documented via authenticated audio recording (SHA-256 preserved)", type: "critical" },
  { year: "2023–2024", event: "Court proceedings continue — audio evidence submitted to record", type: "action" },
  { year: "2024", event: "Wrongful TPR finalized — due process violations documented", type: "critical" },
  { year: "2025", event: "Federal §1983 complaint filed; Habeas Corpus petition filed; TRO motion filed", type: "action" },
  { year: "2025–2026", event: "Public advocacy campaign launched — evidence vault published", type: "action" },
  { year: "Sep 16, 2026", event: "CRITICAL DEADLINE — adoption finalization threatened", type: "deadline" },
];

export default function BellaStoryPage() {
  return (
    <div style={{ background: "var(--color-warm)" }}>
      {/* ── HEADER ── */}
      <section
        style={{
          background: "var(--color-navy)",
          padding: "80px 16px",
        }}
      >
        <div
          style={{ maxWidth: "var(--max-width-content)", margin: "0 auto" }}
          className="text-center"
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
            Case 21DP0705A
          </span>
          <h1
            style={{
              fontFamily: "var(--font-serif)",
              fontSize: "clamp(2.5rem, 5vw, 4rem)",
              color: "var(--color-gold)",
              fontWeight: 900,
              marginTop: "12px",
              marginBottom: "16px",
              lineHeight: 1.1,
            }}
          >
            Bella&apos;s Story
          </h1>
          <p
            style={{
              color: "rgba(255,255,255,0.75)",
              fontSize: "1.15rem",
              maxWidth: "600px",
              margin: "0 auto 32px",
              lineHeight: 1.7,
            }}
          >
            A complete account of what happened — from the removal through the
            wrongful TPR to the ongoing federal fight for justice. Read it.
            Share it. Do not let it be forgotten.
          </p>
          <div className="flex flex-col sm:flex-row gap-3 justify-center">
            <Link href="/evidence" className="btn-primary">
              View Evidence Vault
            </Link>
            <Link href="/legal" className="btn-secondary">
              Legal Actions
            </Link>
          </div>
        </div>
      </section>

      {/* ── CHAPTER NAVIGATION ── */}
      <div
        style={{
          background: "var(--color-light-gray)",
          borderBottom: "1px solid rgba(201,162,39,0.2)",
          overflowX: "auto",
        }}
      >
        <div
          style={{ maxWidth: "var(--max-width-content)", margin: "0 auto" }}
          className="px-4 py-3 flex gap-2"
        >
          {chapters.map((ch) => (
            <a
              key={ch.id}
              href={`#${ch.id}`}
              style={{
                color: "var(--color-navy)",
                fontSize: "0.8rem",
                fontWeight: 600,
                padding: "6px 14px",
                borderRadius: "100px",
                textDecoration: "none",
                whiteSpace: "nowrap",
                border: "1px solid rgba(26,26,46,0.15)",
                transition: "background 0.15s",
              }}
            >
              {ch.number}. {ch.title}
            </a>
          ))}
        </div>
      </div>

      {/* ── CHAPTERS ── */}
      <div style={{ maxWidth: "860px", margin: "0 auto" }} className="px-4">
        {chapters.map((ch, idx) => (
          <section
            key={ch.id}
            id={ch.id}
            style={{
              paddingTop: "80px",
              paddingBottom: "60px",
              borderBottom:
                idx < chapters.length - 1
                  ? "1px solid rgba(201,162,39,0.15)"
                  : "none",
            }}
          >
            <div className="flex items-start gap-6 mb-6">
              <span
                style={{
                  fontFamily: "var(--font-serif)",
                  fontSize: "3rem",
                  fontWeight: 900,
                  color: "rgba(201,162,39,0.2)",
                  lineHeight: 1,
                  flexShrink: 0,
                }}
              >
                {ch.number}
              </span>
              <div>
                <span
                  style={{
                    color: "var(--color-gold)",
                    fontSize: "0.8rem",
                    fontWeight: 700,
                    letterSpacing: "0.1em",
                    textTransform: "uppercase",
                    display: "block",
                    marginBottom: "4px",
                  }}
                >
                  {ch.subtitle}
                </span>
                <h2
                  style={{
                    fontFamily: "var(--font-serif)",
                    fontSize: "clamp(1.5rem, 3vw, 2rem)",
                    color: "var(--color-navy)",
                    fontWeight: 800,
                    lineHeight: 1.2,
                  }}
                >
                  {ch.title}
                </h2>
              </div>
            </div>

            {ch.content.map((para, pIdx) => (
              <p
                key={pIdx}
                style={{
                  color: "var(--color-charcoal)",
                  lineHeight: 1.85,
                  fontSize: "1.05rem",
                  marginBottom: "20px",
                }}
              >
                {para}
              </p>
            ))}

            {ch.pullQuote && (
              <blockquote className="pull-quote">{ch.pullQuote}</blockquote>
            )}

            {ch.id === "abuse-reports" && (
              <div
                style={{
                  background: "rgba(201,162,39,0.06)",
                  border: "1px solid rgba(201,162,39,0.25)",
                  borderRadius: "10px",
                  padding: "20px 24px",
                  marginTop: "24px",
                }}
              >
                <p
                  style={{
                    color: "var(--color-navy)",
                    fontSize: "0.9rem",
                    fontWeight: 600,
                    marginBottom: "8px",
                  }}
                >
                  <FileText
                    size={14}
                    style={{
                      display: "inline",
                      marginRight: "6px",
                      verticalAlign: "middle",
                    }}
                  />
                  Evidence Reference
                </p>
                <p
                  style={{
                    color: "var(--color-charcoal)",
                    fontSize: "0.875rem",
                    lineHeight: 1.6,
                  }}
                >
                  All abuse reports, filing dates, and official responses are
                  documented in the Evidence Vault.{" "}
                  <Link
                    href="/evidence#abuse-reports"
                    style={{
                      color: "var(--color-gold)",
                      textDecoration: "none",
                      fontWeight: 600,
                    }}
                  >
                    View abuse report documentation →
                  </Link>
                </p>
              </div>
            )}

            {ch.id === "november-2023" && (
              <div
                style={{
                  background: "rgba(220,38,38,0.06)",
                  border: "1px solid rgba(220,38,38,0.2)",
                  borderRadius: "10px",
                  padding: "20px 24px",
                  marginTop: "24px",
                }}
              >
                <p
                  style={{
                    color: "var(--color-crimson)",
                    fontSize: "0.9rem",
                    fontWeight: 600,
                    marginBottom: "8px",
                  }}
                >
                  <Shield
                    size={14}
                    style={{
                      display: "inline",
                      marginRight: "6px",
                      verticalAlign: "middle",
                    }}
                  />
                  Authenticated Evidence
                </p>
                <p
                  style={{
                    color: "var(--color-charcoal)",
                    fontSize: "0.875rem",
                    lineHeight: 1.6,
                  }}
                >
                  The November 27, 2023 audio recording is preserved in the
                  Evidence Vault with full SHA-256 authentication.{" "}
                  <Link
                    href="/evidence#nov-2023"
                    style={{
                      color: "var(--color-crimson)",
                      textDecoration: "none",
                      fontWeight: 600,
                    }}
                  >
                    Review this evidence →
                  </Link>
                </p>
              </div>
            )}

            {ch.id === "icwa-failure" && (
              <div
                style={{
                  background: "rgba(26,26,46,0.04)",
                  border: "1px solid rgba(26,26,46,0.12)",
                  borderRadius: "10px",
                  padding: "20px 24px",
                  marginTop: "24px",
                }}
              >
                <p
                  style={{
                    color: "var(--color-navy)",
                    fontSize: "0.9rem",
                    fontWeight: 600,
                    marginBottom: "8px",
                  }}
                >
                  <Scale
                    size={14}
                    style={{
                      display: "inline",
                      marginRight: "6px",
                      verticalAlign: "middle",
                    }}
                  />
                  Legal Reference
                </p>
                <p
                  style={{
                    color: "var(--color-charcoal)",
                    fontSize: "0.875rem",
                    lineHeight: 1.6,
                  }}
                >
                  ICWA violations documented in the legal filings.{" "}
                  <Link
                    href="/legal#icwa"
                    style={{
                      color: "var(--color-gold)",
                      textDecoration: "none",
                      fontWeight: 600,
                    }}
                  >
                    View legal action →
                  </Link>
                </p>
              </div>
            )}

            {ch.id === "how-you-can-help" && (
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-8">
                {[
                  {
                    href: "/donate",
                    label: "Donate",
                    desc: "Fund the legal fight",
                    color: "var(--color-gold)",
                  },
                  {
                    href: "/army",
                    label: "Join the Army",
                    desc: "Amplify the campaign",
                    color: "var(--color-rose)",
                  },
                  {
                    href: "/contact",
                    label: "Legal Support",
                    desc: "Attorneys needed",
                    color: "var(--color-crimson)",
                  },
                ].map((action) => (
                  <Link
                    key={action.href}
                    href={action.href}
                    style={{
                      display: "block",
                      background: "white",
                      border: `2px solid ${action.color}`,
                      borderRadius: "10px",
                      padding: "20px",
                      textDecoration: "none",
                      textAlign: "center",
                    }}
                  >
                    <div
                      style={{
                        color: action.color,
                        fontWeight: 700,
                        fontSize: "1rem",
                        marginBottom: "4px",
                      }}
                    >
                      {action.label}
                    </div>
                    <div
                      style={{
                        color: "var(--color-charcoal)",
                        fontSize: "0.85rem",
                      }}
                    >
                      {action.desc}
                    </div>
                  </Link>
                ))}
              </div>
            )}
          </section>
        ))}
      </div>

      {/* ── FULL TIMELINE ── */}
      <section
        id="timeline"
        className="section-padding"
        style={{ background: "var(--color-navy)" }}
      >
        <div
          style={{ maxWidth: "800px", margin: "0 auto" }}
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
              Interactive Timeline
            </span>
            <h2
              style={{
                fontFamily: "var(--font-serif)",
                fontSize: "clamp(1.75rem, 3vw, 2.25rem)",
                color: "white",
                fontWeight: 800,
                marginTop: "8px",
              }}
            >
              The Complete Record
            </h2>
          </div>

          <div>
            {timelineEvents.map((evt, idx) => (
              <div key={idx} className="flex gap-6 mb-6">
                <div
                  className="flex flex-col items-center"
                  style={{ flexShrink: 0 }}
                >
                  <div
                    style={{
                      width: "14px",
                      height: "14px",
                      borderRadius: "50%",
                      background:
                        evt.type === "deadline"
                          ? "var(--color-crimson)"
                          : evt.type === "critical"
                          ? "var(--color-crimson)"
                          : evt.type === "warning"
                          ? "var(--color-rose)"
                          : "var(--color-gold)",
                      marginTop: "4px",
                      border: "2px solid rgba(255,255,255,0.2)",
                      flexShrink: 0,
                    }}
                  />
                  {idx < timelineEvents.length - 1 && (
                    <div
                      style={{
                        width: "2px",
                        flex: 1,
                        background: "rgba(201,162,39,0.3)",
                        marginTop: "4px",
                        minHeight: "32px",
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
                      letterSpacing: "0.05em",
                    }}
                  >
                    {evt.year}
                  </span>
                  <p
                    style={{
                      color:
                        evt.type === "deadline"
                          ? "var(--color-crimson)"
                          : "rgba(255,255,255,0.85)",
                      fontSize: "0.95rem",
                      marginTop: "4px",
                      lineHeight: 1.5,
                      fontWeight: evt.type === "deadline" ? 700 : 400,
                    }}
                  >
                    {evt.event}
                  </p>
                </div>
              </div>
            ))}
          </div>

          <div
            style={{
              background: "rgba(220,38,38,0.15)",
              border: "1px solid var(--color-crimson)",
              borderRadius: "10px",
              padding: "24px",
              marginTop: "40px",
              textAlign: "center",
            }}
          >
            <AlertTriangle
              size={32}
              style={{ color: "var(--color-crimson)", margin: "0 auto 12px" }}
            />
            <h3
              style={{
                fontFamily: "var(--font-serif)",
                fontSize: "1.3rem",
                color: "white",
                fontWeight: 700,
                marginBottom: "8px",
              }}
            >
              September 16, 2026 — The Deadline
            </h3>
            <p
              style={{
                color: "rgba(255,255,255,0.75)",
                fontSize: "0.95rem",
                lineHeight: 1.6,
                marginBottom: "20px",
              }}
            >
              This is not an abstract date. It is the day that changes what is
              legally possible. Every action taken before this deadline
              matters. Every action delayed costs something that cannot be
              recovered.
            </p>
            <Link href="/donate" className="btn-crimson">
              Take Action Now
            </Link>
          </div>
        </div>
      </section>

      {/* ── NEXT STEPS CTA ── */}
      <section className="section-padding">
        <div
          style={{ maxWidth: "var(--max-width-content)", margin: "0 auto" }}
          className="px-4"
        >
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div
              className="card"
              style={{ padding: "32px" }}
            >
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
                  marginBottom: "20px",
                  fontSize: "0.9rem",
                }}
              >
                Every document, recording, and filing referenced in this story
                is available in the Evidence Vault with full authentication
                records.
              </p>
              <Link
                href="/evidence"
                className="btn-primary inline-flex items-center gap-2"
                style={{ fontSize: "0.9rem" }}
              >
                Open Evidence Vault <ChevronRight size={14} />
              </Link>
            </div>

            <div
              className="card"
              style={{ padding: "32px" }}
            >
              <h3
                style={{
                  fontFamily: "var(--font-serif)",
                  fontSize: "1.3rem",
                  color: "var(--color-navy)",
                  fontWeight: 700,
                  marginBottom: "12px",
                }}
              >
                Understand the Legal Fight
              </h3>
              <p
                style={{
                  color: "var(--color-charcoal)",
                  lineHeight: 1.7,
                  marginBottom: "20px",
                  fontSize: "0.9rem",
                }}
              >
                Four active federal cases, each targeting a different dimension
                of the constitutional violations. See what&apos;s filed and
                what&apos;s pending.
              </p>
              <Link
                href="/legal"
                className="btn-secondary inline-flex items-center gap-2"
                style={{ fontSize: "0.9rem" }}
              >
                View Legal Actions <ChevronRight size={14} />
              </Link>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
