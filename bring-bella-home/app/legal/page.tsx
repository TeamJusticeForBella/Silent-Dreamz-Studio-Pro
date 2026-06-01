import type { Metadata } from "next";
import Link from "next/link";
import {
  Scale,
  AlertTriangle,
  FileText,
  Shield,
  ChevronRight,
  Download,
} from "lucide-react";

export const metadata: Metadata = {
  title: "Legal Action",
  description:
    "Active litigation in Bella's case: federal §1983 complaint, Habeas Corpus petition, TRO motion, and late appeal. Pro se litigant Jason R. Barr.",
};

const litigationItems = [
  {
    id: "1983",
    title: "42 U.S.C. §1983 Federal Civil Rights Complaint",
    court: "U.S. District Court",
    status: "Active",
    statusColor: "var(--color-gold)",
    filed: "March 5, 2025",
    lastUpdate: "May 2025 — Initial briefing schedule set",
    nextDeadline: "August 1, 2026 — Opposition response due",
    summary:
      "Federal civil rights complaint alleging violations of constitutional due process, equal protection, and rights under the Indian Child Welfare Act (ICWA). Names state actors who participated in the wrongful removal and TPR process.",
    grounds: [
      "Fourteenth Amendment due process violations",
      "Failure to provide active efforts as required by ICWA §1912(d)",
      "Suppression of exculpatory evidence in TPR proceedings",
      "Equal protection violations based on Native heritage",
    ],
    relief: "Declaratory relief, injunctive relief, damages",
  },
  {
    id: "habeas",
    title: "Petition for Writ of Habeas Corpus",
    court: "U.S. District Court",
    status: "Filed",
    statusColor: "var(--color-rose)",
    filed: "April 12, 2025",
    lastUpdate: "May 2025 — Respondent served",
    nextDeadline: "September 1, 2026 — Hearing requested before adoption deadline",
    summary:
      "Habeas petition challenging the unlawful separation of Bella from her father and the constitutionally deficient proceedings that led to TPR. Grounded in federal constitutional violations that cannot be adequately remedied in state court.",
    grounds: [
      "Unconstitutional deprivation of liberty interest in family unity",
      "State court proceedings infected by due process violations",
      "ICWA mandates not met — federal law preempts state action",
      "Newly discovered evidence not available at time of TPR",
    ],
    relief: "Immediate reunification or supervised contact pending hearing",
  },
  {
    id: "tro",
    title: "Motion for TRO / Preliminary Injunction",
    court: "U.S. District Court",
    status: "Pending",
    statusColor: "var(--color-crimson)",
    filed: "June 20, 2025",
    lastUpdate: "Filing acknowledged — awaiting scheduling",
    nextDeadline: "CRITICAL: Must be heard before September 16, 2026",
    summary:
      "Emergency motion to halt adoption finalization proceedings pending resolution of federal civil rights claims. Argues irreparable harm if adoption proceeds before constitutional violations are adjudicated.",
    grounds: [
      "Irreparable harm — adoption cannot be undone once finalized",
      "Substantial likelihood of success on §1983 merits",
      "Balance of equities favors injunctive relief",
      "Public interest in constitutional compliance by state agencies",
    ],
    relief: "Stay of adoption proceedings pending federal case resolution",
  },
  {
    id: "appeal",
    title: "Late Appeal — State TPR Order",
    court: "State Court of Appeals",
    status: "Filed",
    statusColor: "var(--color-rose)",
    filed: "January 2025",
    lastUpdate: "Motion for leave to file late appeal submitted",
    nextDeadline: "July 2026 — Court ruling on leave motion expected",
    summary:
      "Motion for leave to file late appeal of the TPR order based on newly discovered evidence (the authenticated November 27, 2023 recording) and ineffective assistance of counsel in the underlying proceedings.",
    grounds: [
      "Newly discovered evidence not available at time of original appeal deadline",
      "Ineffective assistance of counsel — failure to present key evidence",
      "Fraud on the court — misrepresentation of service completion record",
      "Constitutional violations apparent on the face of the record",
    ],
    relief: "Reversal and remand for new TPR proceedings",
  },
];

const pillars = [
  {
    title: "Constitutional Due Process",
    desc: "Every parent has a fundamental liberty interest in the care and custody of their child. That interest requires meaningful process before termination — process that was denied here.",
    icon: <Scale size={28} style={{ color: "var(--color-gold)" }} />,
  },
  {
    title: "ICWA Federal Protections",
    desc: "The Indian Child Welfare Act is federal law. Its active efforts requirement, heightened evidentiary standards, and placement preferences are mandatory — not optional guidelines for state agencies.",
    icon: <Shield size={28} style={{ color: "var(--color-gold)" }} />,
  },
  {
    title: "Evidence Suppression",
    desc: "A court cannot make a fair determination on the basis of a partial record. The suppression of abuse documentation and the exclusion of authenticated audio evidence from full consideration is a structural due process failure.",
    icon: <FileText size={28} style={{ color: "var(--color-gold)" }} />,
  },
  {
    title: "Reunification as the Goal",
    desc: "The goal of child welfare law is family preservation and reunification, not permanent separation. Every procedural avenue that was cut short represented a failure to fulfill the statutory mandate.",
    icon: <AlertTriangle size={28} style={{ color: "var(--color-gold)" }} />,
  },
];

const resources = [
  { title: "42 U.S.C. §1983 Complaint (Full)", format: "PDF", size: "2.4 MB" },
  { title: "Habeas Corpus Petition", format: "PDF", size: "1.8 MB" },
  { title: "TRO/Injunction Motion Brief", format: "PDF", size: "3.1 MB" },
  { title: "ICWA Violation Analysis Memo", format: "PDF", size: "890 KB" },
  { title: "Legal Timeline Summary", format: "PDF", size: "450 KB" },
  { title: "Pro Se Motion Templates Used", format: "PDF", size: "1.2 MB" },
];

const caseTimeline = [
  { date: "2019", event: "Removal — ICWA protections not applied", status: "past" },
  { date: "2020–2021", event: "Service compliance — all requirements met by Jason", status: "past" },
  { date: "2022", event: "TPR proceedings initiated — ICWA violations raised", status: "past" },
  { date: "2024", event: "Wrongful TPR finalized — due process violations documented", status: "past" },
  { date: "Jan 2025", event: "Late appeal filed in state court", status: "active" },
  { date: "Mar 2025", event: "§1983 federal complaint filed", status: "active" },
  { date: "Apr 2025", event: "Habeas corpus petition filed", status: "active" },
  { date: "Jun 2025", event: "TRO/Injunction motion filed", status: "active" },
  { date: "Sep 16, 2026", event: "CRITICAL: Adoption finalization deadline", status: "deadline" },
];

export default function LegalActionPage() {
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
                Legal Action
              </h1>
              <p
                style={{
                  color: "rgba(255,255,255,0.7)",
                  fontSize: "1rem",
                  maxWidth: "560px",
                  lineHeight: 1.7,
                }}
              >
                Four active legal proceedings, each targeting documented
                violations. Jason R. Barr is proceeding pro se — without
                institutional support, against a system with unlimited
                resources.
              </p>
            </div>

            {/* Pro Se Banner */}
            <div
              style={{
                background: "rgba(201,162,39,0.1)",
                border: "1px solid rgba(201,162,39,0.35)",
                borderRadius: "12px",
                padding: "20px 24px",
                maxWidth: "280px",
                flexShrink: 0,
              }}
            >
              <Scale
                size={24}
                style={{ color: "var(--color-gold)", marginBottom: "10px" }}
              />
              <h3
                style={{
                  color: "var(--color-gold)",
                  fontWeight: 700,
                  fontSize: "0.9rem",
                  marginBottom: "8px",
                  fontFamily: "var(--font-serif)",
                }}
              >
                Pro Se Litigant
              </h3>
              <p
                style={{
                  color: "rgba(255,255,255,0.65)",
                  fontSize: "0.82rem",
                  lineHeight: 1.6,
                }}
              >
                Jason R. Barr is representing himself in all federal
                proceedings. Pro bono legal assistance urgently needed.
              </p>
              <Link
                href="/contact"
                style={{
                  display: "block",
                  marginTop: "12px",
                  color: "var(--color-gold)",
                  textDecoration: "none",
                  fontSize: "0.82rem",
                  fontWeight: 700,
                }}
              >
                Contact for legal support →
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* ── LITIGATION STATUS CARDS ── */}
      <section className="section-padding">
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
              marginBottom: "24px",
            }}
          >
            Active Litigation
          </h2>

          <div className="flex flex-col gap-6">
            {litigationItems.map((item) => (
              <div
                key={item.id}
                id={item.id}
                className="card"
                style={{
                  borderLeft: `4px solid ${item.statusColor}`,
                  padding: "28px",
                }}
              >
                <div className="flex flex-col md:flex-row justify-between gap-4 mb-4">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2 flex-wrap">
                      <span
                        style={{
                          background: item.statusColor,
                          color:
                            item.statusColor === "var(--color-gold)"
                              ? "var(--color-navy)"
                              : "white",
                          fontSize: "0.7rem",
                          fontWeight: 700,
                          letterSpacing: "0.08em",
                          padding: "3px 12px",
                          borderRadius: "100px",
                          textTransform: "uppercase",
                        }}
                      >
                        {item.status}
                      </span>
                      <span
                        style={{
                          color: "var(--color-charcoal)",
                          fontSize: "0.8rem",
                          opacity: 0.7,
                        }}
                      >
                        {item.court}
                      </span>
                    </div>
                    <h3
                      style={{
                        fontFamily: "var(--font-serif)",
                        fontSize: "1.2rem",
                        color: "var(--color-navy)",
                        fontWeight: 700,
                        lineHeight: 1.3,
                        marginBottom: "4px",
                      }}
                    >
                      {item.title}
                    </h3>
                    <p
                      style={{
                        color: "var(--color-charcoal)",
                        fontSize: "0.85rem",
                        opacity: 0.7,
                      }}
                    >
                      Filed: {item.filed}
                    </p>
                  </div>

                  <div
                    style={{
                      flexShrink: 0,
                      minWidth: "200px",
                    }}
                  >
                    <div
                      style={{
                        background: "var(--color-light-gray)",
                        borderRadius: "8px",
                        padding: "12px 16px",
                        fontSize: "0.82rem",
                      }}
                    >
                      <p
                        style={{
                          color: "var(--color-charcoal)",
                          opacity: 0.7,
                          marginBottom: "4px",
                        }}
                      >
                        Last Update
                      </p>
                      <p
                        style={{
                          color: "var(--color-navy)",
                          fontWeight: 600,
                          marginBottom: "10px",
                        }}
                      >
                        {item.lastUpdate}
                      </p>
                      <p
                        style={{
                          color: "var(--color-crimson)",
                          opacity: 0.8,
                          marginBottom: "4px",
                          fontSize: "0.78rem",
                        }}
                      >
                        Next Deadline
                      </p>
                      <p
                        style={{
                          color: "var(--color-crimson)",
                          fontWeight: 700,
                          fontSize: "0.82rem",
                        }}
                      >
                        {item.nextDeadline}
                      </p>
                    </div>
                  </div>
                </div>

                <p
                  style={{
                    color: "var(--color-charcoal)",
                    lineHeight: 1.7,
                    marginBottom: "16px",
                    fontSize: "0.9rem",
                  }}
                >
                  {item.summary}
                </p>

                <div className="flex flex-col md:flex-row gap-6">
                  <div className="flex-1">
                    <p
                      style={{
                        color: "var(--color-navy)",
                        fontSize: "0.8rem",
                        fontWeight: 700,
                        letterSpacing: "0.06em",
                        textTransform: "uppercase",
                        marginBottom: "8px",
                      }}
                    >
                      Legal Grounds
                    </p>
                    <ul style={{ listStyle: "none", padding: 0, margin: 0 }}>
                      {item.grounds.map((g, i) => (
                        <li
                          key={i}
                          style={{
                            color: "var(--color-charcoal)",
                            fontSize: "0.85rem",
                            lineHeight: 1.5,
                            padding: "3px 0",
                            paddingLeft: "16px",
                            position: "relative",
                          }}
                        >
                          <span
                            style={{
                              position: "absolute",
                              left: 0,
                              color: "var(--color-gold)",
                            }}
                          >
                            ›
                          </span>
                          {g}
                        </li>
                      ))}
                    </ul>
                  </div>
                  <div style={{ flexShrink: 0 }}>
                    <p
                      style={{
                        color: "var(--color-navy)",
                        fontSize: "0.8rem",
                        fontWeight: 700,
                        letterSpacing: "0.06em",
                        textTransform: "uppercase",
                        marginBottom: "8px",
                      }}
                    >
                      Relief Sought
                    </p>
                    <p
                      style={{
                        color: "var(--color-charcoal)",
                        fontSize: "0.85rem",
                        lineHeight: 1.5,
                        maxWidth: "240px",
                      }}
                    >
                      {item.relief}
                    </p>
                  </div>
                </div>

                <div
                  style={{
                    marginTop: "16px",
                    paddingTop: "16px",
                    borderTop: "1px solid var(--color-light-gray)",
                    display: "flex",
                    gap: "8px",
                  }}
                >
                  <Link
                    href={`/evidence#${item.id}`}
                    style={{
                      display: "inline-flex",
                      alignItems: "center",
                      gap: "6px",
                      color: "var(--color-gold)",
                      textDecoration: "none",
                      fontSize: "0.82rem",
                      fontWeight: 600,
                    }}
                  >
                    <FileText size={14} />
                    View Filing
                  </Link>
                  <span style={{ color: "var(--color-light-gray)" }}>|</span>
                  <button
                    style={{
                      display: "inline-flex",
                      alignItems: "center",
                      gap: "6px",
                      color: "var(--color-charcoal)",
                      background: "none",
                      border: "none",
                      cursor: "pointer",
                      fontSize: "0.82rem",
                      fontWeight: 600,
                      opacity: 0.7,
                    }}
                  >
                    <Download size={14} />
                    Download PDF
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── CASE TRACKER TIMELINE ── */}
      <section
        style={{ background: "var(--color-light-gray)" }}
        className="section-padding"
      >
        <div
          style={{ maxWidth: "800px", margin: "0 auto" }}
          className="px-4"
        >
          <h2
            style={{
              fontFamily: "var(--font-serif)",
              fontSize: "1.6rem",
              color: "var(--color-navy)",
              fontWeight: 700,
              marginBottom: "32px",
            }}
          >
            Case Tracker
          </h2>

          <div>
            {caseTimeline.map((evt, idx) => (
              <div key={idx} className="flex gap-5 mb-5">
                <div className="flex flex-col items-center" style={{ flexShrink: 0 }}>
                  <div
                    style={{
                      width: "14px",
                      height: "14px",
                      borderRadius: "50%",
                      background:
                        evt.status === "deadline"
                          ? "var(--color-crimson)"
                          : evt.status === "active"
                          ? "var(--color-gold)"
                          : "rgba(51,51,51,0.3)",
                      marginTop: "4px",
                      flexShrink: 0,
                      border:
                        evt.status === "active"
                          ? "3px solid rgba(201,162,39,0.3)"
                          : "none",
                    }}
                  />
                  {idx < caseTimeline.length - 1 && (
                    <div
                      style={{
                        width: "2px",
                        flex: 1,
                        background:
                          evt.status === "active"
                            ? "var(--color-gold)"
                            : "rgba(51,51,51,0.15)",
                        marginTop: "4px",
                        minHeight: "30px",
                      }}
                    />
                  )}
                </div>
                <div style={{ paddingBottom: "6px" }}>
                  <span
                    style={{
                      color:
                        evt.status === "active"
                          ? "var(--color-gold)"
                          : evt.status === "deadline"
                          ? "var(--color-crimson)"
                          : "var(--color-charcoal)",
                      fontSize: "0.8rem",
                      fontWeight: 700,
                    }}
                  >
                    {evt.date}
                  </span>
                  <p
                    style={{
                      color:
                        evt.status === "deadline"
                          ? "var(--color-crimson)"
                          : evt.status === "active"
                          ? "var(--color-navy)"
                          : "rgba(51,51,51,0.65)",
                      fontSize: "0.9rem",
                      marginTop: "3px",
                      fontWeight: evt.status === "active" ? 600 : 400,
                    }}
                  >
                    {evt.event}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── WHAT WE'RE FIGHTING FOR ── */}
      <section className="section-padding">
        <div
          style={{ maxWidth: "var(--max-width-content)", margin: "0 auto" }}
          className="px-4"
        >
          <div className="text-center mb-12">
            <h2
              style={{
                fontFamily: "var(--font-serif)",
                fontSize: "clamp(1.75rem, 3vw, 2.25rem)",
                color: "var(--color-navy)",
                fontWeight: 800,
              }}
            >
              What We&apos;re Fighting For
            </h2>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {pillars.map((p, idx) => (
              <div
                key={idx}
                className="card"
                style={{ padding: "28px" }}
              >
                <div
                  style={{
                    width: "52px",
                    height: "52px",
                    background: "rgba(201,162,39,0.08)",
                    borderRadius: "12px",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    marginBottom: "16px",
                  }}
                >
                  {p.icon}
                </div>
                <h3
                  style={{
                    fontFamily: "var(--font-serif)",
                    fontSize: "1.1rem",
                    color: "var(--color-navy)",
                    fontWeight: 700,
                    marginBottom: "10px",
                  }}
                >
                  {p.title}
                </h3>
                <p
                  style={{
                    color: "var(--color-charcoal)",
                    lineHeight: 1.7,
                    fontSize: "0.9rem",
                  }}
                >
                  {p.desc}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── LEGAL RESOURCES ── */}
      <section
        style={{ background: "var(--color-navy)" }}
        className="section-padding"
      >
        <div
          style={{ maxWidth: "var(--max-width-content)", margin: "0 auto" }}
          className="px-4"
        >
          <h2
            style={{
              fontFamily: "var(--font-serif)",
              fontSize: "1.6rem",
              color: "var(--color-gold)",
              fontWeight: 700,
              marginBottom: "8px",
            }}
          >
            Legal Document Downloads
          </h2>
          <p
            style={{
              color: "rgba(255,255,255,0.65)",
              fontSize: "0.9rem",
              marginBottom: "24px",
            }}
          >
            All filings are public record and available for download.
          </p>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {resources.map((r) => (
              <div
                key={r.title}
                style={{
                  background: "rgba(255,255,255,0.05)",
                  border: "1px solid rgba(201,162,39,0.2)",
                  borderRadius: "10px",
                  padding: "16px 20px",
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "center",
                }}
              >
                <div>
                  <p
                    style={{
                      color: "white",
                      fontWeight: 600,
                      fontSize: "0.9rem",
                      marginBottom: "4px",
                    }}
                  >
                    {r.title}
                  </p>
                  <p
                    style={{
                      color: "rgba(255,255,255,0.45)",
                      fontSize: "0.78rem",
                    }}
                  >
                    {r.format} — {r.size}
                  </p>
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
                  PDF
                </button>
              </div>
            ))}
          </div>

          <div
            style={{
              marginTop: "40px",
              background: "rgba(220,38,38,0.15)",
              border: "1px solid var(--color-crimson)",
              borderRadius: "12px",
              padding: "24px",
            }}
          >
            <div className="flex flex-col md:flex-row items-start gap-4">
              <AlertTriangle
                size={28}
                style={{ color: "var(--color-crimson)", flexShrink: 0 }}
              />
              <div className="flex-1">
                <h3
                  style={{
                    color: "white",
                    fontFamily: "var(--font-serif)",
                    fontSize: "1.1rem",
                    fontWeight: 700,
                    marginBottom: "8px",
                  }}
                >
                  Attorneys: Pro Bono Assistance Needed
                </h3>
                <p
                  style={{
                    color: "rgba(255,255,255,0.75)",
                    fontSize: "0.9rem",
                    lineHeight: 1.6,
                    marginBottom: "16px",
                  }}
                >
                  Jason is proceeding pro se against a system with institutional
                  resources. If you are an attorney with experience in federal
                  civil rights, ICWA, family law, or habeas practice —
                  especially in the relevant jurisdiction — your assistance
                  could be decisive.
                </p>
                <Link href="/contact" className="btn-crimson" style={{ fontSize: "0.9rem" }}>
                  Contact About Legal Support
                  <ChevronRight size={14} style={{ display: "inline", marginLeft: "4px" }} />
                </Link>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
