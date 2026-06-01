"use client";

import { useState } from "react";
import Link from "next/link";
import {
  Users,
  Heart,
  AlertTriangle,
  ChevronRight,
  Shield,
} from "lucide-react";

const campaigns = [
  {
    title: "Sign the Petition",
    desc: "We have an active petition to the state governor demanding an independent review of Case 21DP0705A and immediate suspension of adoption proceedings.",
    count: "14,823 signatures",
    action: "Sign Now",
    color: "var(--color-gold)",
    urgent: true,
  },
  {
    title: "Call Your Representative",
    desc: "Contact your state and federal representatives about ICWA violations and child welfare accountability. We provide a call script and direct phone numbers.",
    count: "Calls make a difference",
    action: "Get Call Script",
    color: "var(--color-rose)",
    urgent: false,
  },
  {
    title: "Share on Social Media",
    desc: "Every share reaches people who haven't heard Bella's story. We have ready-to-post graphics, captions, and hashtags for all platforms.",
    count: "#BringBellaHome",
    action: "Get Share Kit",
    color: "var(--color-navy)",
    urgent: false,
  },
  {
    title: "Attend the Rally",
    desc: "In-person presence sends an unmistakable message. See our upcoming events for times, locations, and details.",
    count: "Next: August 2026",
    action: "View Events",
    color: "var(--color-crimson)",
    urgent: false,
  },
];

const events = [
  {
    date: "July 19, 2026",
    time: "11:00 AM – 2:00 PM",
    title: "Awareness Rally — State Capitol Steps",
    location: "State Capitol Building, Main Entrance",
    desc: "Community rally demanding accountability. Speakers, community testimony, live stream. Family-friendly.",
    rsvp: true,
  },
  {
    date: "August 9, 2026",
    time: "2:00 PM – 4:00 PM",
    title: "Community Briefing — Bella's Case Update",
    location: "Virtual (Zoom) — Link sent on RSVP",
    desc: "Jason will provide a live case update, answer questions, and share next steps for the advocacy community.",
    rsvp: true,
  },
  {
    date: "September 5, 2026",
    time: "9:00 AM – 12:00 PM",
    title: "Emergency Action Day — Last Push Before Deadline",
    location: "Federal Courthouse Plaza + Virtual",
    desc: "Final mobilization before the September 16 deadline. In-person presence and coordinated social media action.",
    rsvp: true,
  },
];

const merch = [
  {
    name: "Bring Bella Home T-Shirt",
    price: "$28",
    desc: "Navy unisex tee with gold Bella text. All proceeds to campaign.",
    emoji: "👕",
  },
  {
    name: "Bella's Army Hoodie",
    price: "$48",
    desc: "Navy pullover hoodie. Warm, powerful message.",
    emoji: "🧥",
  },
  {
    name: "Advocacy Sticker Pack",
    price: "$8",
    desc: "6 vinyl stickers — case details, slogans, QR code.",
    emoji: "🏷️",
  },
  {
    name: "Solidarity Bracelet",
    price: "$12",
    desc: "Gold silicone with embossed #BringBellaHome.",
    emoji: "📿",
  },
  {
    name: "Enamel Pin",
    price: "$10",
    desc: "Gold scales of justice with Bella's initial. 1.5\".",
    emoji: "📌",
  },
  {
    name: "Advocate Baseball Cap",
    price: "$24",
    desc: "Navy cap with gold embroidery. Adjustable.",
    emoji: "🧢",
  },
];

export default function BellasArmyPage() {
  const [email, setEmail] = useState("");
  const [submitted, setSubmitted] = useState(false);

  const handleSignup = (e: React.FormEvent) => {
    e.preventDefault();
    if (email) {
      setSubmitted(true);
    }
  };

  return (
    <div style={{ background: "var(--color-warm)" }}>
      {/* ── HEADER ── */}
      <section
        style={{
          background: "var(--color-navy)",
          padding: "64px 16px",
          textAlign: "center",
        }}
      >
        <div style={{ maxWidth: "700px", margin: "0 auto" }}>
          <Users
            size={48}
            style={{ color: "var(--color-rose)", margin: "0 auto 16px" }}
          />
          <h1
            style={{
              fontFamily: "var(--font-serif)",
              fontSize: "clamp(2rem, 4vw, 3.5rem)",
              color: "var(--color-gold)",
              fontWeight: 900,
              marginBottom: "16px",
            }}
          >
            Bella&apos;s Army
          </h1>
          <p
            style={{
              color: "rgba(255,255,255,0.75)",
              fontSize: "1.1rem",
              lineHeight: 1.7,
              marginBottom: "32px",
            }}
          >
            A community of 2,847 supporters demanding justice, transparency,
            and the safe return of Neveyah-RosaBella Barr to her father.
          </p>

          {/* Community Counter */}
          <div
            style={{
              display: "inline-flex",
              alignItems: "center",
              gap: "16px",
              background: "rgba(201,162,39,0.1)",
              border: "1px solid rgba(201,162,39,0.3)",
              borderRadius: "12px",
              padding: "20px 32px",
              marginBottom: "32px",
            }}
          >
            <div
              style={{
                fontFamily: "var(--font-serif)",
                fontSize: "3rem",
                fontWeight: 900,
                color: "var(--color-gold)",
                lineHeight: 1,
              }}
            >
              2,847
            </div>
            <div style={{ textAlign: "left" }}>
              <p
                style={{
                  color: "white",
                  fontWeight: 700,
                  fontSize: "1rem",
                }}
              >
                Supporters Worldwide
              </p>
              <p
                style={{
                  color: "rgba(255,255,255,0.55)",
                  fontSize: "0.8rem",
                }}
              >
                Growing every day
              </p>
            </div>
          </div>

          {/* Email Signup */}
          {!submitted ? (
            <form onSubmit={handleSignup} className="flex flex-col sm:flex-row gap-3 max-w-md mx-auto">
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="Your email address"
                required
                style={{
                  flex: 1,
                  padding: "14px 16px",
                  borderRadius: "8px",
                  border: "none",
                  fontSize: "0.9rem",
                  outline: "none",
                }}
              />
              <button
                type="submit"
                className="btn-primary"
                style={{ whiteSpace: "nowrap" }}
              >
                Join the Army
              </button>
            </form>
          ) : (
            <div
              style={{
                background: "rgba(22,163,74,0.15)",
                border: "1px solid #16a34a",
                borderRadius: "8px",
                padding: "16px 24px",
                color: "white",
                fontSize: "0.95rem",
                maxWidth: "400px",
                margin: "0 auto",
              }}
            >
              You&apos;re in! Welcome to Bella&apos;s Army. We&apos;ll send updates to{" "}
              <strong>{email}</strong>.
            </div>
          )}
        </div>
      </section>

      {/* ── ACTION CENTER ── */}
      <section className="section-padding">
        <div
          style={{ maxWidth: "var(--max-width-content)", margin: "0 auto" }}
          className="px-4"
        >
          <div className="text-center mb-10">
            <span
              style={{
                color: "var(--color-gold)",
                fontSize: "0.8rem",
                fontWeight: 700,
                letterSpacing: "0.12em",
                textTransform: "uppercase",
              }}
            >
              Take Action Now
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
              Current Campaigns
            </h2>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {campaigns.map((c) => (
              <div
                key={c.title}
                className="card"
                style={{
                  padding: "28px",
                  borderTop: `4px solid ${c.color}`,
                  position: "relative",
                }}
              >
                {c.urgent && (
                  <span
                    style={{
                      position: "absolute",
                      top: "16px",
                      right: "16px",
                      background: "var(--color-crimson)",
                      color: "white",
                      fontSize: "0.65rem",
                      fontWeight: 700,
                      padding: "3px 10px",
                      borderRadius: "100px",
                      letterSpacing: "0.08em",
                    }}
                  >
                    URGENT
                  </span>
                )}
                <h3
                  style={{
                    fontFamily: "var(--font-serif)",
                    fontSize: "1.15rem",
                    color: "var(--color-navy)",
                    fontWeight: 700,
                    marginBottom: "10px",
                  }}
                >
                  {c.title}
                </h3>
                <p
                  style={{
                    color: "var(--color-charcoal)",
                    fontSize: "0.9rem",
                    lineHeight: 1.7,
                    marginBottom: "16px",
                  }}
                >
                  {c.desc}
                </p>
                <div className="flex justify-between items-center">
                  <span
                    style={{
                      color: c.color,
                      fontSize: "0.82rem",
                      fontWeight: 700,
                    }}
                  >
                    {c.count}
                  </span>
                  <button
                    style={{
                      background: c.color,
                      color:
                        c.color === "var(--color-gold)"
                          ? "var(--color-navy)"
                          : "white",
                      border: "none",
                      borderRadius: "6px",
                      padding: "8px 20px",
                      fontSize: "0.85rem",
                      fontWeight: 700,
                      cursor: "pointer",
                      display: "flex",
                      alignItems: "center",
                      gap: "4px",
                    }}
                  >
                    {c.action}
                    <ChevronRight size={14} />
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── EVENTS CALENDAR ── */}
      <section
        style={{ background: "var(--color-light-gray)" }}
        className="section-padding"
      >
        <div
          style={{ maxWidth: "var(--max-width-content)", margin: "0 auto" }}
          className="px-4"
        >
          <div className="text-center mb-10">
            <span
              style={{
                color: "var(--color-gold)",
                fontSize: "0.8rem",
                fontWeight: 700,
                letterSpacing: "0.12em",
                textTransform: "uppercase",
              }}
            >
              Upcoming Events
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
              Join Us in Person &amp; Online
            </h2>
          </div>

          <div className="flex flex-col gap-6">
            {events.map((evt, idx) => (
              <div
                key={idx}
                className="card"
                style={{ padding: "0", overflow: "hidden" }}
              >
                <div className="flex flex-col md:flex-row">
                  <div
                    style={{
                      background: idx === 2 ? "var(--color-crimson)" : "var(--color-navy)",
                      padding: "24px",
                      minWidth: "140px",
                      display: "flex",
                      flexDirection: "column",
                      alignItems: "center",
                      justifyContent: "center",
                      textAlign: "center",
                    }}
                  >
                    <p
                      style={{
                        color: "var(--color-gold)",
                        fontSize: "0.75rem",
                        fontWeight: 700,
                        letterSpacing: "0.08em",
                        textTransform: "uppercase",
                        marginBottom: "4px",
                      }}
                    >
                      {evt.date.split(",")[0].split(" ")[0]}
                    </p>
                    <p
                      style={{
                        fontFamily: "var(--font-serif)",
                        color: "white",
                        fontSize: "2.5rem",
                        fontWeight: 900,
                        lineHeight: 1,
                      }}
                    >
                      {evt.date.split(" ")[1].replace(",", "")}
                    </p>
                    <p
                      style={{
                        color: "rgba(255,255,255,0.6)",
                        fontSize: "0.8rem",
                        marginTop: "4px",
                      }}
                    >
                      {evt.date.split(", ")[1]}
                    </p>
                  </div>

                  <div style={{ padding: "24px 28px", flex: 1 }}>
                    <h3
                      style={{
                        fontFamily: "var(--font-serif)",
                        fontSize: "1.1rem",
                        color: "var(--color-navy)",
                        fontWeight: 700,
                        marginBottom: "6px",
                      }}
                    >
                      {evt.title}
                      {idx === 2 && (
                        <span
                          style={{
                            background: "var(--color-crimson)",
                            color: "white",
                            fontSize: "0.65rem",
                            fontWeight: 700,
                            padding: "2px 8px",
                            borderRadius: "100px",
                            marginLeft: "8px",
                            verticalAlign: "middle",
                          }}
                        >
                          CRITICAL
                        </span>
                      )}
                    </h3>
                    <p
                      style={{
                        color: "var(--color-gold)",
                        fontSize: "0.82rem",
                        fontWeight: 600,
                        marginBottom: "4px",
                      }}
                    >
                      {evt.time} — {evt.location}
                    </p>
                    <p
                      style={{
                        color: "var(--color-charcoal)",
                        fontSize: "0.88rem",
                        lineHeight: 1.6,
                        marginBottom: "12px",
                      }}
                    >
                      {evt.desc}
                    </p>
                    <button
                      style={{
                        background: idx === 2 ? "var(--color-crimson)" : "var(--color-gold)",
                        color: idx === 2 ? "white" : "var(--color-navy)",
                        border: "none",
                        borderRadius: "6px",
                        padding: "10px 24px",
                        fontSize: "0.85rem",
                        fontWeight: 700,
                        cursor: "pointer",
                      }}
                    >
                      RSVP Now
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── MERCH STORE ── */}
      <section className="section-padding">
        <div
          style={{ maxWidth: "var(--max-width-content)", margin: "0 auto" }}
          className="px-4"
        >
          <div className="text-center mb-10">
            <span
              style={{
                color: "var(--color-gold)",
                fontSize: "0.8rem",
                fontWeight: 700,
                letterSpacing: "0.12em",
                textTransform: "uppercase",
              }}
            >
              Merch Store
            </span>
            <h2
              style={{
                fontFamily: "var(--font-serif)",
                fontSize: "clamp(1.75rem, 3vw, 2.25rem)",
                color: "var(--color-navy)",
                fontWeight: 800,
                marginTop: "8px",
                marginBottom: "8px",
              }}
            >
              Wear the Cause
            </h2>
            <p style={{ color: "var(--color-charcoal)", fontSize: "0.9rem" }}>
              All proceeds go directly to Bella&apos;s legal fund.
            </p>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
            {merch.map((item) => (
              <div
                key={item.name}
                className="card"
                style={{ padding: "20px", textAlign: "center" }}
              >
                <div
                  style={{
                    fontSize: "2.5rem",
                    marginBottom: "12px",
                  }}
                >
                  {item.emoji}
                </div>
                <h4
                  style={{
                    fontFamily: "var(--font-serif)",
                    fontSize: "0.95rem",
                    color: "var(--color-navy)",
                    fontWeight: 700,
                    marginBottom: "6px",
                  }}
                >
                  {item.name}
                </h4>
                <p
                  style={{
                    color: "var(--color-charcoal)",
                    fontSize: "0.8rem",
                    lineHeight: 1.5,
                    marginBottom: "12px",
                  }}
                >
                  {item.desc}
                </p>
                <div className="flex items-center justify-between">
                  <span
                    style={{
                      color: "var(--color-gold)",
                      fontWeight: 900,
                      fontSize: "1.1rem",
                      fontFamily: "var(--font-serif)",
                    }}
                  >
                    {item.price}
                  </span>
                  <button
                    style={{
                      background: "var(--color-navy)",
                      color: "white",
                      border: "none",
                      borderRadius: "6px",
                      padding: "6px 14px",
                      fontSize: "0.8rem",
                      fontWeight: 600,
                      cursor: "pointer",
                    }}
                  >
                    Order
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── AMBASSADOR PROGRAM ── */}
      <section
        style={{ background: "var(--color-navy)" }}
        className="section-padding"
      >
        <div
          style={{ maxWidth: "700px", margin: "0 auto" }}
          className="px-4 text-center"
        >
          <Shield
            size={40}
            style={{ color: "var(--color-gold)", margin: "0 auto 16px" }}
          />
          <h2
            style={{
              fontFamily: "var(--font-serif)",
              fontSize: "clamp(1.5rem, 3vw, 2rem)",
              color: "var(--color-gold)",
              fontWeight: 800,
              marginBottom: "12px",
            }}
          >
            Become an Ambassador
          </h2>
          <p
            style={{
              color: "rgba(255,255,255,0.75)",
              lineHeight: 1.7,
              marginBottom: "24px",
              fontSize: "0.95rem",
            }}
          >
            Ambassadors take this campaign to their communities — churches,
            schools, social groups, local media. We provide materials, talking
            points, and support. You provide the network.
          </p>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-left mb-8">
            {[
              "Official ambassador digital kit",
              "Printable flyers and posters",
              "Presentation slides",
              "Social media content pack",
              "Direct line to Jason for Q&A",
              "Ambassador recognition on site",
            ].map((benefit) => (
              <div
                key={benefit}
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: "8px",
                  color: "rgba(255,255,255,0.8)",
                  fontSize: "0.85rem",
                }}
              >
                <span style={{ color: "var(--color-gold)" }}>✓</span>
                {benefit}
              </div>
            ))}
          </div>
          <Link href="/contact" className="btn-primary">
            Apply as Ambassador
          </Link>
        </div>
      </section>

      {/* ── SOCIAL HUB ── */}
      <section className="section-padding">
        <div
          style={{ maxWidth: "var(--max-width-content)", margin: "0 auto" }}
          className="px-4"
        >
          <div className="text-center mb-10">
            <h2
              style={{
                fontFamily: "var(--font-serif)",
                fontSize: "clamp(1.5rem, 3vw, 2rem)",
                color: "var(--color-navy)",
                fontWeight: 800,
                marginBottom: "8px",
              }}
            >
              Follow &amp; Share
            </h2>
            <p style={{ color: "var(--color-charcoal)", fontSize: "0.9rem" }}>
              Use #BringBellaHome across all platforms
            </p>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {[
              { platform: "Facebook", handle: "/BringBellaHome", color: "#1877F2" },
              { platform: "X / Twitter", handle: "@BellasArmy2026", color: "#000000" },
              { platform: "Instagram", handle: "@bringbellahome", color: "#E1306C" },
              { platform: "TikTok", handle: "@bellasfight2026", color: "#010101" },
            ].map((s) => (
              <div
                key={s.platform}
                style={{
                  background: "white",
                  border: "1px solid var(--color-light-gray)",
                  borderRadius: "10px",
                  padding: "20px",
                  textAlign: "center",
                  borderTop: `4px solid ${s.color}`,
                }}
              >
                <p
                  style={{
                    fontWeight: 700,
                    fontSize: "0.9rem",
                    color: "var(--color-navy)",
                    marginBottom: "6px",
                  }}
                >
                  {s.platform}
                </p>
                <p
                  style={{
                    color: s.color,
                    fontSize: "0.82rem",
                    fontWeight: 600,
                    marginBottom: "12px",
                  }}
                >
                  {s.handle}
                </p>
                <button
                  style={{
                    background: s.color,
                    color: "white",
                    border: "none",
                    borderRadius: "6px",
                    padding: "6px 16px",
                    fontSize: "0.78rem",
                    fontWeight: 600,
                    cursor: "pointer",
                    width: "100%",
                  }}
                >
                  Follow
                </button>
              </div>
            ))}
          </div>

          <div
            style={{
              background: "var(--color-light-gray)",
              borderRadius: "12px",
              padding: "24px",
              marginTop: "24px",
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
              Hashtag: <span style={{ color: "var(--color-gold)" }}>#BringBellaHome</span>
            </p>
            <p
              style={{
                color: "var(--color-charcoal)",
                fontSize: "0.9rem",
              }}
            >
              Post your support, your rally photos, your calls with reps — use the
              hashtag so the community can find and amplify your voice.
            </p>
          </div>
        </div>
      </section>

      {/* Urgent CTA */}
      <section
        style={{
          background: "var(--color-crimson)",
          padding: "48px 16px",
          textAlign: "center",
        }}
      >
        <div style={{ maxWidth: "560px", margin: "0 auto" }}>
          <AlertTriangle
            size={36}
            style={{ color: "white", margin: "0 auto 12px", opacity: 0.9 }}
          />
          <h2
            style={{
              fontFamily: "var(--font-serif)",
              fontSize: "1.75rem",
              color: "white",
              fontWeight: 800,
              marginBottom: "12px",
            }}
          >
            September 16, 2026 — We Have 107 Days
          </h2>
          <p
            style={{
              color: "rgba(255,255,255,0.85)",
              fontSize: "0.95rem",
              lineHeight: 1.7,
              marginBottom: "20px",
            }}
          >
            The deadline is real. Join the army, donate, share, show up. Every
            person in this network is part of Bella&apos;s path home.
          </p>
          <div className="flex flex-col sm:flex-row gap-3 justify-center">
            <Link href="/donate" className="btn-primary">
              Donate Now
            </Link>
            <Link
              href="/story"
              style={{
                border: "2px solid white",
                color: "white",
                fontWeight: 700,
                padding: "14px 28px",
                borderRadius: "8px",
                textDecoration: "none",
                fontSize: "0.9rem",
                display: "inline-flex",
                alignItems: "center",
                gap: "4px",
              }}
            >
              Read the Story
              <Heart size={14} />
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
}
