import Link from "next/link";
import { Scale, Globe, ExternalLink, Share2, Rss } from "lucide-react";

const footerSections = [
  {
    title: "About",
    links: [
      { href: "/story", label: "Bella's Story" },
      { href: "/legal", label: "Legal Action" },
      { href: "/evidence", label: "Evidence Vault" },
      { href: "/blog", label: "Blog & Updates" },
    ],
  },
  {
    title: "Get Involved",
    links: [
      { href: "/army", label: "Join Bella's Army" },
      { href: "/donate", label: "Donate" },
      { href: "/army#merch", label: "Merch Store" },
      { href: "/army#events", label: "Events" },
    ],
  },
  {
    title: "Legal",
    links: [
      { href: "/legal#case", label: "Case 21DP0705A" },
      { href: "/legal#filings", label: "Court Filings" },
      { href: "/legal#resources", label: "Legal Resources" },
      { href: "/contact", label: "Contact Us" },
    ],
  },
  {
    title: "Connect",
    links: [
      { href: "/media", label: "Press & Media" },
      { href: "/contact#whistleblower", label: "Whistleblower Hotline" },
      { href: "/contact#resources", label: "Family Resources" },
      { href: "/portal", label: "Secure Portal" },
    ],
  },
];

const socialLinks = [
  { href: "https://x.com/BellasArmy2026", icon: Globe, label: "X / Twitter" },
  { href: "https://instagram.com/bringbellahome", icon: ExternalLink, label: "Instagram" },
  { href: "https://facebook.com/BringBellaHome", icon: Share2, label: "Facebook" },
  { href: "https://youtube.com/BringBellaHome", icon: Rss, label: "YouTube" },
];

export default function Footer() {
  return (
    <footer style={{ background: "var(--color-navy)", color: "rgba(255,255,255,0.8)" }}>
      <div
        style={{ maxWidth: "var(--max-width-content)", margin: "0 auto" }}
        className="px-4 py-16"
      >
        {/* Top: Logo + tagline */}
        <div className="flex flex-col md:flex-row justify-between gap-10 mb-12">
          <div className="max-w-xs">
            <div className="flex items-center gap-2 mb-3">
              <Scale size={24} style={{ color: "var(--color-gold)" }} />
              <span
                style={{
                  fontFamily: "var(--font-playfair)",
                  fontSize: "1.25rem",
                  fontWeight: 700,
                  color: "var(--color-gold)",
                }}
              >
                Bring Bella Home
              </span>
            </div>
            <p style={{ fontSize: "0.875rem", lineHeight: 1.6 }}>
              A father's fight to bring his daughter home. Advocating for
              Neveyah-RosaBella "Bella" Barr — Case 21DP0705A.
            </p>
            <div className="flex gap-4 mt-5">
              {socialLinks.map((s) => (
                <a
                  key={s.label}
                  href={s.href}
                  aria-label={s.label}
                  target="_blank"
                  rel="noopener noreferrer"
                  style={{ color: "var(--color-gold)", transition: "opacity 0.15s" }}
                  className="hover:opacity-70"
                >
                  <s.icon size={20} />
                </a>
              ))}
            </div>
          </div>

          {/* Links grid */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            {footerSections.map((section) => (
              <div key={section.title}>
                <h3
                  style={{
                    color: "var(--color-gold)",
                    fontWeight: 700,
                    fontSize: "0.875rem",
                    textTransform: "uppercase",
                    letterSpacing: "0.08em",
                    marginBottom: "12px",
                  }}
                >
                  {section.title}
                </h3>
                <ul style={{ listStyle: "none", padding: 0, margin: 0 }}>
                  {section.links.map((link) => (
                    <li key={link.href} style={{ marginBottom: "8px" }}>
                      <Link
                        href={link.href}
                        style={{
                          color: "rgba(255,255,255,0.7)",
                          fontSize: "0.875rem",
                          textDecoration: "none",
                          transition: "color 0.15s",
                        }}
                        className="hover:text-white"
                      >
                        {link.label}
                      </Link>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>

        {/* Divider */}
        <div style={{ borderTop: "1px solid rgba(201,162,39,0.25)", paddingTop: "24px" }}>
          <div className="flex flex-col md:flex-row justify-between gap-4 items-center">
            <p style={{ fontSize: "0.8rem", color: "rgba(255,255,255,0.5)" }}>
              © 2026 Jason R. Barr. All rights reserved.
            </p>
            <p style={{ fontSize: "0.8rem", color: "rgba(255,255,255,0.4)", textAlign: "center" }}>
              This is a personal advocacy website. Not legal advice. All evidence is SHA-256 verified.
            </p>
          </div>
        </div>
      </div>
    </footer>
  );
}
