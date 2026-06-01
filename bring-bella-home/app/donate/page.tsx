"use client";

import { useState } from "react";
import Link from "next/link";
import { Heart, Shield, AlertTriangle, ChevronRight } from "lucide-react";

const tiers = [
  {
    amount: 25,
    label: "$25",
    impact: "Covers one court filing fee",
    popular: false,
  },
  {
    amount: 50,
    label: "$50",
    impact: "Funds one day of document preparation",
    popular: false,
  },
  {
    amount: 100,
    label: "$100",
    impact: "Covers travel to one court hearing",
    popular: true,
  },
  {
    amount: 250,
    label: "$250",
    impact: "Funds a week of legal research materials",
    popular: false,
  },
  {
    amount: 500,
    label: "$500",
    impact: "Supports a full month of campaign operations",
    popular: false,
  },
];

const fundUsage = [
  { label: "Legal filing fees and court costs", pct: 40 },
  { label: "Document preparation and printing", pct: 20 },
  { label: "Travel to hearings and court appearances", pct: 15 },
  { label: "Website and evidence vault hosting", pct: 10 },
  { label: "Campaign outreach and advocacy", pct: 10 },
  { label: "Operational reserve", pct: 5 },
];

const GOAL = 50000;
const RAISED = 12450;

export default function DonatePage() {
  const [selectedAmount, setSelectedAmount] = useState<number | null>(100);
  const [customAmount, setCustomAmount] = useState("");
  const [isMonthly, setIsMonthly] = useState(false);

  const displayAmount =
    customAmount !== "" ? parseFloat(customAmount) || 0 : selectedAmount || 0;
  const pct = Math.round((RAISED / GOAL) * 100);

  return (
    <div style={{ background: "var(--color-warm)" }}>
      {/* ── HEADER ── */}
      <section
        style={{ background: "var(--color-navy)", padding: "64px 16px" }}
      >
        <div
          style={{ maxWidth: "760px", margin: "0 auto" }}
          className="text-center"
        >
          <Heart
            size={40}
            style={{ color: "var(--color-rose)", margin: "0 auto 16px" }}
          />
          <h1
            style={{
              fontFamily: "var(--font-serif)",
              fontSize: "clamp(2rem, 4vw, 3rem)",
              color: "var(--color-gold)",
              fontWeight: 900,
              marginBottom: "16px",
            }}
          >
            Fund Bella&apos;s Fight
          </h1>
          <p
            style={{
              color: "rgba(255,255,255,0.75)",
              fontSize: "1.05rem",
              lineHeight: 1.7,
              marginBottom: "8px",
            }}
          >
            Jason R. Barr is fighting pro se — without an attorney, without
            institutional backing — against a state system with unlimited
            resources. Every dollar donated goes directly to the legal fight
            to bring Bella home before September 16, 2026.
          </p>
        </div>
      </section>

      {/* ── FUND THERMOMETER ── */}
      <section
        style={{
          background: "var(--color-light-gray)",
          padding: "40px 16px",
        }}
      >
        <div style={{ maxWidth: "600px", margin: "0 auto" }}>
          <div className="flex justify-between items-end mb-3">
            <div>
              <span
                style={{
                  fontFamily: "var(--font-serif)",
                  fontSize: "2rem",
                  fontWeight: 900,
                  color: "var(--color-navy)",
                }}
              >
                ${RAISED.toLocaleString()}
              </span>
              <span
                style={{
                  color: "var(--color-charcoal)",
                  fontSize: "0.9rem",
                  marginLeft: "8px",
                  opacity: 0.7,
                }}
              >
                raised
              </span>
            </div>
            <div style={{ textAlign: "right" }}>
              <span
                style={{
                  color: "var(--color-charcoal)",
                  fontSize: "0.9rem",
                  opacity: 0.7,
                }}
              >
                of ${GOAL.toLocaleString()} goal
              </span>
            </div>
          </div>

          <div
            style={{
              height: "20px",
              background: "rgba(0,0,0,0.08)",
              borderRadius: "100px",
              overflow: "hidden",
            }}
          >
            <div
              style={{
                height: "100%",
                width: `${pct}%`,
                background: `linear-gradient(90deg, var(--color-gold) 0%, #e8b84b 100%)`,
                borderRadius: "100px",
                transition: "width 0.8s ease",
              }}
            />
          </div>

          <div className="flex justify-between mt-2">
            <span
              style={{
                color: "var(--color-gold)",
                fontSize: "0.85rem",
                fontWeight: 700,
              }}
            >
              {pct}% funded
            </span>
            <span
              style={{
                color: "var(--color-crimson)",
                fontSize: "0.85rem",
                fontWeight: 600,
              }}
            >
              ${(GOAL - RAISED).toLocaleString()} remaining
            </span>
          </div>
        </div>
      </section>

      {/* ── DONATION FORM ── */}
      <section className="section-padding">
        <div
          style={{ maxWidth: "var(--max-width-content)", margin: "0 auto" }}
          className="px-4"
        >
          <div className="flex flex-col md:flex-row gap-12">
            {/* Left: Form */}
            <div className="flex-1">
              <div
                className="card"
                style={{ padding: "36px" }}
              >
                {/* Monthly toggle */}
                <div className="flex items-center gap-3 mb-8">
                  <button
                    onClick={() => setIsMonthly(false)}
                    style={{
                      flex: 1,
                      padding: "10px",
                      borderRadius: "8px",
                      border: `2px solid ${!isMonthly ? "var(--color-gold)" : "var(--color-light-gray)"}`,
                      background: !isMonthly ? "var(--color-gold)" : "transparent",
                      color: !isMonthly ? "var(--color-navy)" : "var(--color-charcoal)",
                      fontWeight: 700,
                      fontSize: "0.9rem",
                      cursor: "pointer",
                    }}
                  >
                    One-Time
                  </button>
                  <button
                    onClick={() => setIsMonthly(true)}
                    style={{
                      flex: 1,
                      padding: "10px",
                      borderRadius: "8px",
                      border: `2px solid ${isMonthly ? "var(--color-gold)" : "var(--color-light-gray)"}`,
                      background: isMonthly ? "var(--color-gold)" : "transparent",
                      color: isMonthly ? "var(--color-navy)" : "var(--color-charcoal)",
                      fontWeight: 700,
                      fontSize: "0.9rem",
                      cursor: "pointer",
                    }}
                  >
                    Monthly
                  </button>
                </div>

                {isMonthly && (
                  <div
                    style={{
                      background: "rgba(201,162,39,0.08)",
                      border: "1px solid rgba(201,162,39,0.3)",
                      borderRadius: "8px",
                      padding: "12px 16px",
                      marginBottom: "20px",
                      fontSize: "0.85rem",
                      color: "var(--color-navy)",
                    }}
                  >
                    Monthly donors provide sustained support for the duration
                    of the legal fight. Cancel anytime.
                  </div>
                )}

                {/* Amount Buttons */}
                <div className="grid grid-cols-3 gap-3 mb-4">
                  {tiers.map((tier) => (
                    <button
                      key={tier.amount}
                      onClick={() => {
                        setSelectedAmount(tier.amount);
                        setCustomAmount("");
                      }}
                      style={{
                        padding: "14px 8px",
                        borderRadius: "8px",
                        border: `2px solid ${selectedAmount === tier.amount && customAmount === "" ? "var(--color-gold)" : "var(--color-light-gray)"}`,
                        background:
                          selectedAmount === tier.amount && customAmount === ""
                            ? "var(--color-gold)"
                            : "white",
                        color:
                          selectedAmount === tier.amount && customAmount === ""
                            ? "var(--color-navy)"
                            : "var(--color-charcoal)",
                        fontWeight: 700,
                        fontSize: "1rem",
                        cursor: "pointer",
                        position: "relative",
                      }}
                    >
                      {tier.label}
                      {tier.popular && (
                        <span
                          style={{
                            position: "absolute",
                            top: "-8px",
                            left: "50%",
                            transform: "translateX(-50%)",
                            background: "var(--color-crimson)",
                            color: "white",
                            fontSize: "0.6rem",
                            fontWeight: 700,
                            padding: "2px 6px",
                            borderRadius: "100px",
                            whiteSpace: "nowrap",
                          }}
                        >
                          POPULAR
                        </span>
                      )}
                    </button>
                  ))}

                  {/* Custom */}
                  <div
                    style={{
                      gridColumn: "span 3",
                      display: "flex",
                      alignItems: "center",
                      border: `2px solid ${customAmount !== "" ? "var(--color-gold)" : "var(--color-light-gray)"}`,
                      borderRadius: "8px",
                      overflow: "hidden",
                    }}
                  >
                    <span
                      style={{
                        padding: "0 12px",
                        color: "var(--color-charcoal)",
                        fontWeight: 700,
                        fontSize: "1.1rem",
                        background: "var(--color-light-gray)",
                        alignSelf: "stretch",
                        display: "flex",
                        alignItems: "center",
                      }}
                    >
                      $
                    </span>
                    <input
                      type="number"
                      placeholder="Custom amount"
                      value={customAmount}
                      onChange={(e) => {
                        setCustomAmount(e.target.value);
                        setSelectedAmount(null);
                      }}
                      style={{
                        flex: 1,
                        padding: "14px 16px",
                        border: "none",
                        outline: "none",
                        fontSize: "1rem",
                        background: "white",
                      }}
                    />
                  </div>
                </div>

                {/* Impact message */}
                {displayAmount > 0 && (
                  <div
                    style={{
                      background: "rgba(201,162,39,0.08)",
                      borderRadius: "8px",
                      padding: "12px 16px",
                      marginBottom: "20px",
                      fontSize: "0.85rem",
                      color: "var(--color-navy)",
                    }}
                  >
                    {customAmount !== ""
                      ? `Your gift of $${displayAmount} makes a real difference in Bella's case.`
                      : tiers.find((t) => t.amount === selectedAmount)?.impact ||
                        ""}
                    {isMonthly && " (monthly)"}
                  </div>
                )}

                {/* Payment CTA */}
                <div
                  style={{
                    background: "var(--color-gold)",
                    color: "var(--color-navy)",
                    borderRadius: "10px",
                    padding: "18px",
                    textAlign: "center",
                    fontWeight: 700,
                    fontSize: "1.1rem",
                    cursor: "pointer",
                    marginBottom: "12px",
                  }}
                >
                  Donate{" "}
                  {displayAmount > 0 ? `$${displayAmount}` : ""}
                  {isMonthly ? "/month" : ""} — Secure Payment
                </div>

                {/* Payment Methods */}
                <div className="grid grid-cols-2 gap-3">
                  {[
                    { label: "Cash App", handle: "$BellaBarr", color: "#00D64F" },
                    { label: "Zelle", handle: "bringbellahome@email.com", color: "#6D1ED4" },
                    { label: "PayPal", handle: "@BellaFightFund", color: "#003087" },
                    { label: "Venmo", handle: "@BellaBarrFund", color: "#3D95CE" },
                  ].map((method) => (
                    <div
                      key={method.label}
                      style={{
                        border: "1px solid var(--color-light-gray)",
                        borderRadius: "8px",
                        padding: "12px",
                        textAlign: "center",
                      }}
                    >
                      <p
                        style={{
                          fontWeight: 700,
                          fontSize: "0.85rem",
                          color: method.color,
                          marginBottom: "4px",
                        }}
                      >
                        {method.label}
                      </p>
                      <p
                        style={{
                          fontSize: "0.78rem",
                          color: "var(--color-charcoal)",
                          opacity: 0.7,
                        }}
                      >
                        {method.handle}
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* Right: Transparency */}
            <div style={{ flexShrink: 0, width: "340px", maxWidth: "100%" }}>
              <div
                style={{
                  background: "var(--color-navy)",
                  borderRadius: "16px",
                  padding: "28px",
                  marginBottom: "16px",
                }}
              >
                <h3
                  style={{
                    fontFamily: "var(--font-serif)",
                    fontSize: "1.1rem",
                    color: "var(--color-gold)",
                    fontWeight: 700,
                    marginBottom: "20px",
                  }}
                >
                  Where Your Money Goes
                </h3>
                {fundUsage.map((item) => (
                  <div key={item.label} style={{ marginBottom: "14px" }}>
                    <div className="flex justify-between mb-1">
                      <span
                        style={{
                          color: "rgba(255,255,255,0.75)",
                          fontSize: "0.82rem",
                        }}
                      >
                        {item.label}
                      </span>
                      <span
                        style={{
                          color: "var(--color-gold)",
                          fontSize: "0.82rem",
                          fontWeight: 700,
                        }}
                      >
                        {item.pct}%
                      </span>
                    </div>
                    <div
                      style={{
                        height: "6px",
                        background: "rgba(255,255,255,0.1)",
                        borderRadius: "100px",
                      }}
                    >
                      <div
                        style={{
                          height: "100%",
                          width: `${item.pct}%`,
                          background: "var(--color-gold)",
                          borderRadius: "100px",
                        }}
                      />
                    </div>
                  </div>
                ))}
              </div>

              {/* Trust badges */}
              <div className="flex flex-col gap-3">
                {[
                  {
                    icon: <Shield size={18} style={{ color: "var(--color-gold)" }} />,
                    text: "Secure SSL-encrypted donations",
                  },
                  {
                    icon: <Heart size={18} style={{ color: "var(--color-rose)" }} />,
                    text: "100% goes to Bella's legal fight",
                  },
                  {
                    icon: <AlertTriangle size={18} style={{ color: "var(--color-crimson)" }} />,
                    text: "Deadline: September 16, 2026",
                  },
                ].map((badge, idx) => (
                  <div
                    key={idx}
                    className="flex items-center gap-3"
                    style={{
                      background: "white",
                      border: "1px solid var(--color-light-gray)",
                      borderRadius: "8px",
                      padding: "12px 16px",
                    }}
                  >
                    {badge.icon}
                    <span
                      style={{
                        color: "var(--color-charcoal)",
                        fontSize: "0.85rem",
                        fontWeight: 500,
                      }}
                    >
                      {badge.text}
                    </span>
                  </div>
                ))}
              </div>

              <div
                style={{
                  background: "var(--color-light-gray)",
                  borderRadius: "10px",
                  padding: "16px",
                  marginTop: "16px",
                }}
              >
                <p
                  style={{
                    color: "var(--color-charcoal)",
                    fontSize: "0.82rem",
                    lineHeight: 1.6,
                    opacity: 0.8,
                  }}
                >
                  Can&apos;t donate right now? You can still help by{" "}
                  <Link
                    href="/army"
                    style={{ color: "var(--color-gold)", fontWeight: 600 }}
                  >
                    joining Bella&apos;s Army
                  </Link>
                  {" "}or sharing this campaign with your network.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ── CTA ── */}
      <section
        style={{ background: "var(--color-crimson)", padding: "60px 16px" }}
      >
        <div
          style={{ maxWidth: "600px", margin: "0 auto" }}
          className="text-center"
        >
          <h2
            style={{
              fontFamily: "var(--font-serif)",
              fontSize: "clamp(1.5rem, 3vw, 2rem)",
              color: "white",
              fontWeight: 800,
              marginBottom: "12px",
            }}
          >
            Every Dollar Counts Before September 16, 2026
          </h2>
          <p
            style={{
              color: "rgba(255,255,255,0.85)",
              lineHeight: 1.7,
              marginBottom: "24px",
              fontSize: "0.95rem",
            }}
          >
            The legal system was not built for the kind of fight Jason is
            waging alone. Your contribution levels that playing field.
          </p>
          <Link
            href="/story"
            style={{
              display: "inline-flex",
              alignItems: "center",
              gap: "6px",
              border: "2px solid white",
              color: "white",
              fontWeight: 700,
              padding: "12px 28px",
              borderRadius: "8px",
              textDecoration: "none",
              fontSize: "0.9rem",
            }}
          >
            Read Bella&apos;s Story First
            <ChevronRight size={16} />
          </Link>
        </div>
      </section>
    </div>
  );
}
