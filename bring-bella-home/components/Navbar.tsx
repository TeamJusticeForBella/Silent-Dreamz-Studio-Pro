"use client";

import Link from "next/link";
import { useState } from "react";
import { Menu, X, Scale } from "lucide-react";

const navLinks = [
  { href: "/story", label: "The Story" },
  { href: "/evidence", label: "Evidence" },
  { href: "/legal", label: "Legal Action" },
  { href: "/media", label: "Media" },
  { href: "/army", label: "Bella's Army" },
  { href: "/blog", label: "Blog" },
  { href: "/contact", label: "Contact" },
];

export default function Navbar() {
  const [open, setOpen] = useState(false);

  return (
    <nav
      style={{
        background: "var(--color-navy)",
        borderBottom: "2px solid var(--color-gold)",
        position: "sticky",
        top: "42px",
        zIndex: 50,
      }}
    >
      <div
        style={{ maxWidth: "var(--max-width-content)", margin: "0 auto" }}
        className="px-4 py-3 flex items-center justify-between"
      >
        {/* Logo */}
        <Link
          href="/"
          className="flex items-center gap-2 no-underline"
          onClick={() => setOpen(false)}
        >
          <Scale
            size={28}
            style={{ color: "var(--color-gold)", flexShrink: 0 }}
          />
          <span
            style={{
              fontFamily: "var(--font-playfair)",
              fontSize: "1.25rem",
              fontWeight: 700,
              color: "var(--color-gold)",
              letterSpacing: "0.01em",
            }}
          >
            Bring Bella Home
          </span>
        </Link>

        {/* Desktop Nav */}
        <div className="hidden md:flex items-center gap-1">
          {navLinks.map((link) => (
            <Link
              key={link.href}
              href={link.href}
              style={{
                color: "rgba(255,255,255,0.85)",
                fontSize: "0.875rem",
                fontWeight: 500,
                padding: "6px 12px",
                borderRadius: "6px",
                transition: "color 0.15s, background 0.15s",
                textDecoration: "none",
              }}
              className="hover:text-white"
              onMouseEnter={(e) =>
                (e.currentTarget.style.background = "rgba(201,162,39,0.15)")
              }
              onMouseLeave={(e) =>
                (e.currentTarget.style.background = "transparent")
              }
            >
              {link.label}
            </Link>
          ))}
          <Link
            href="/donate"
            className="btn-primary"
            style={{ marginLeft: "8px", padding: "8px 20px", fontSize: "0.875rem" }}
          >
            Donate
          </Link>
        </div>

        {/* Mobile Toggle */}
        <button
          className="md:hidden"
          onClick={() => setOpen(!open)}
          style={{ color: "var(--color-gold)", background: "none", border: "none", cursor: "pointer" }}
          aria-label="Toggle menu"
        >
          {open ? <X size={28} /> : <Menu size={28} />}
        </button>
      </div>

      {/* Mobile Menu */}
      {open && (
        <div
          style={{ background: "var(--color-navy)", borderTop: "1px solid rgba(201,162,39,0.3)" }}
          className="md:hidden px-4 pb-4"
        >
          {navLinks.map((link) => (
            <Link
              key={link.href}
              href={link.href}
              onClick={() => setOpen(false)}
              style={{
                display: "block",
                color: "rgba(255,255,255,0.85)",
                padding: "10px 0",
                borderBottom: "1px solid rgba(255,255,255,0.08)",
                textDecoration: "none",
                fontWeight: 500,
              }}
            >
              {link.label}
            </Link>
          ))}
          <Link
            href="/donate"
            onClick={() => setOpen(false)}
            className="btn-primary"
            style={{ marginTop: "16px", display: "block", textAlign: "center" }}
          >
            Donate Now
          </Link>
        </div>
      )}
    </nav>
  );
}
