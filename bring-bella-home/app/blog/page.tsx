import type { Metadata } from "next";
import Link from "next/link";
import { ChevronRight, FileText } from "lucide-react";

export const metadata: Metadata = {
  title: "Blog",
  description:
    "Case updates, legal analysis, personal reflections, and advocacy resources from the Bring Bella Home campaign.",
};

const categories = [
  "Case Updates",
  "Legal Analysis",
  "Personal",
  "Media",
  "Advocacy",
];

const posts = [
  {
    slug: "federal-tro-motion-filed",
    title: "Federal TRO Motion Filed: What It Means and What Happens Next",
    date: "June 20, 2025",
    category: "Case Updates",
    categoryColor: "var(--color-crimson)",
    excerpt:
      "On June 20, 2025, Jason filed a Motion for Temporary Restraining Order and Preliminary Injunction in federal court. This is arguably the most critical legal filing to date — here's what it means for Bella's case.",
    featured: true,
    readTime: "8 min read",
  },
  {
    slug: "icwa-what-you-need-to-know",
    title: "ICWA: What the Indian Child Welfare Act Actually Requires (And Why It Matters Here)",
    date: "May 12, 2025",
    category: "Legal Analysis",
    categoryColor: "var(--color-gold)",
    excerpt:
      "The Indian Child Welfare Act is not a technicality. It is a federal law with real teeth — and in Case 21DP0705A, it was violated at nearly every step. Here is what the law requires and what happened instead.",
    featured: false,
    readTime: "12 min read",
  },
  {
    slug: "six-years-what-i-know",
    title: "Six Years In: What I Know Now That I Didn't Know Then",
    date: "April 3, 2025",
    category: "Personal",
    categoryColor: "var(--color-rose)",
    excerpt:
      "A personal reflection from Jason R. Barr on six years of fighting the system as a pro se litigant — what he's learned, what he wished he'd known, and why he will not stop.",
    featured: false,
    readTime: "6 min read",
  },
  {
    slug: "evidence-authentication-explainer",
    title: "How We Authenticate Evidence: SHA-256 and Why It Matters",
    date: "March 15, 2025",
    category: "Legal Analysis",
    categoryColor: "var(--color-gold)",
    excerpt:
      "Every piece of evidence in this case is SHA-256 authenticated. Here's an accessible explanation of what that means, why it matters, and how it protects the integrity of the record.",
    featured: false,
    readTime: "5 min read",
  },
  {
    slug: "nov-27-2023-the-recording",
    title: "November 27, 2023: What the Recording Shows",
    date: "February 8, 2025",
    category: "Case Updates",
    categoryColor: "var(--color-crimson)",
    excerpt:
      "The audio recording from November 27, 2023 is central to this case. This post explains the context, what the recording documents, and why it directly contradicts the official narrative.",
    featured: false,
    readTime: "7 min read",
  },
  {
    slug: "how-to-support-a-pro-se-litigant",
    title: "How to Support a Pro Se Litigant Fighting Child Welfare Courts",
    date: "January 20, 2025",
    category: "Advocacy",
    categoryColor: "var(--color-navy)",
    excerpt:
      "Pro se litigants — people representing themselves in court — face enormous disadvantages against state agencies. Here's a practical guide for advocates who want to help.",
    featured: false,
    readTime: "9 min read",
  },
];

const recentPosts = posts.slice(0, 4);

export default function BlogPage() {
  const featured = posts[0];
  const grid = posts.slice(1);

  return (
    <div style={{ background: "var(--color-warm)" }}>
      {/* ── HEADER ── */}
      <section
        style={{ background: "var(--color-navy)", padding: "56px 16px" }}
      >
        <div style={{ maxWidth: "var(--max-width-content)", margin: "0 auto" }}>
          <span
            style={{
              color: "var(--color-gold)",
              fontSize: "0.8rem",
              fontWeight: 700,
              letterSpacing: "0.14em",
              textTransform: "uppercase",
            }}
          >
            Updates &amp; Analysis
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
            The Blog
          </h1>
          <p
            style={{
              color: "rgba(255,255,255,0.65)",
              fontSize: "1rem",
              maxWidth: "520px",
              lineHeight: 1.7,
            }}
          >
            Case updates, legal analysis, personal reflections, and advocacy
            resources from the Bring Bella Home campaign.
          </p>
        </div>
      </section>

      <section className="section-padding">
        <div
          style={{ maxWidth: "var(--max-width-content)", margin: "0 auto" }}
          className="px-4"
        >
          <div className="flex flex-col md:flex-row gap-12">
            {/* Main Content */}
            <div className="flex-1">
              {/* Featured Post */}
              <div
                style={{
                  background: "var(--color-navy)",
                  borderRadius: "16px",
                  overflow: "hidden",
                  marginBottom: "40px",
                }}
              >
                <div style={{ padding: "36px" }}>
                  <div className="flex items-center gap-3 mb-4">
                    <span
                      style={{
                        background: "var(--color-crimson)",
                        color: "white",
                        fontSize: "0.65rem",
                        fontWeight: 700,
                        padding: "3px 10px",
                        borderRadius: "100px",
                        textTransform: "uppercase",
                        letterSpacing: "0.08em",
                      }}
                    >
                      FEATURED
                    </span>
                    <span
                      style={{
                        background: featured.categoryColor,
                        color:
                          featured.categoryColor === "var(--color-gold)"
                            ? "var(--color-navy)"
                            : "white",
                        fontSize: "0.65rem",
                        fontWeight: 700,
                        padding: "3px 10px",
                        borderRadius: "100px",
                      }}
                    >
                      {featured.category}
                    </span>
                  </div>

                  <h2
                    style={{
                      fontFamily: "var(--font-serif)",
                      fontSize: "clamp(1.25rem, 2.5vw, 1.75rem)",
                      color: "white",
                      fontWeight: 800,
                      marginBottom: "12px",
                      lineHeight: 1.3,
                    }}
                  >
                    {featured.title}
                  </h2>

                  <p
                    style={{
                      color: "rgba(255,255,255,0.65)",
                      lineHeight: 1.7,
                      fontSize: "0.95rem",
                      marginBottom: "24px",
                    }}
                  >
                    {featured.excerpt}
                  </p>

                  <div className="flex items-center justify-between flex-wrap gap-3">
                    <div className="flex items-center gap-4">
                      <span
                        style={{
                          color: "var(--color-gold)",
                          fontSize: "0.82rem",
                        }}
                      >
                        {featured.date}
                      </span>
                      <span
                        style={{
                          color: "rgba(255,255,255,0.4)",
                          fontSize: "0.82rem",
                        }}
                      >
                        {featured.readTime}
                      </span>
                    </div>
                    <Link
                      href={`/blog/${featured.slug}`}
                      className="btn-primary inline-flex items-center gap-2"
                      style={{ fontSize: "0.875rem", padding: "10px 24px" }}
                    >
                      Read More
                      <ChevronRight size={14} />
                    </Link>
                  </div>
                </div>
              </div>

              {/* Post Grid */}
              <h3
                style={{
                  fontFamily: "var(--font-serif)",
                  fontSize: "1.2rem",
                  color: "var(--color-navy)",
                  fontWeight: 700,
                  marginBottom: "20px",
                }}
              >
                Recent Posts
              </h3>

              <div className="flex flex-col gap-6">
                {grid.map((post) => (
                  <div
                    key={post.slug}
                    className="card"
                    style={{
                      padding: "24px",
                      borderLeft: `4px solid ${post.categoryColor}`,
                    }}
                  >
                    <div className="flex items-center gap-3 mb-3">
                      <span
                        style={{
                          background: post.categoryColor,
                          color:
                            post.categoryColor === "var(--color-gold)"
                              ? "var(--color-navy)"
                              : "white",
                          fontSize: "0.65rem",
                          fontWeight: 700,
                          padding: "2px 8px",
                          borderRadius: "100px",
                        }}
                      >
                        {post.category}
                      </span>
                      <span
                        style={{
                          color: "var(--color-charcoal)",
                          fontSize: "0.8rem",
                          opacity: 0.6,
                        }}
                      >
                        {post.date} · {post.readTime}
                      </span>
                    </div>

                    <h3
                      style={{
                        fontFamily: "var(--font-serif)",
                        fontSize: "1.1rem",
                        color: "var(--color-navy)",
                        fontWeight: 700,
                        marginBottom: "8px",
                        lineHeight: 1.3,
                      }}
                    >
                      {post.title}
                    </h3>

                    <p
                      style={{
                        color: "var(--color-charcoal)",
                        fontSize: "0.88rem",
                        lineHeight: 1.7,
                        marginBottom: "16px",
                      }}
                    >
                      {post.excerpt}
                    </p>

                    <Link
                      href={`/blog/${post.slug}`}
                      style={{
                        color: "var(--color-gold)",
                        textDecoration: "none",
                        fontSize: "0.85rem",
                        fontWeight: 600,
                        display: "inline-flex",
                        alignItems: "center",
                        gap: "4px",
                      }}
                    >
                      Read More <ChevronRight size={14} />
                    </Link>
                  </div>
                ))}
              </div>
            </div>

            {/* Sidebar */}
            <div
              style={{ flexShrink: 0, width: "280px", maxWidth: "100%" }}
              className="flex flex-col gap-6"
            >
              {/* Categories */}
              <div
                style={{
                  background: "white",
                  border: "1px solid var(--color-light-gray)",
                  borderRadius: "12px",
                  padding: "24px",
                }}
              >
                <h4
                  style={{
                    fontFamily: "var(--font-serif)",
                    fontSize: "1rem",
                    color: "var(--color-navy)",
                    fontWeight: 700,
                    marginBottom: "16px",
                  }}
                >
                  Categories
                </h4>
                <ul style={{ listStyle: "none", padding: 0, margin: 0 }}>
                  {categories.map((cat) => (
                    <li
                      key={cat}
                      style={{
                        borderBottom: "1px solid var(--color-light-gray)",
                        padding: "8px 0",
                        display: "flex",
                        justifyContent: "space-between",
                        alignItems: "center",
                        cursor: "pointer",
                      }}
                    >
                      <span
                        style={{
                          color: "var(--color-charcoal)",
                          fontSize: "0.88rem",
                        }}
                      >
                        {cat}
                      </span>
                      <span
                        style={{
                          color: "var(--color-gold)",
                          fontSize: "0.78rem",
                          fontWeight: 600,
                        }}
                      >
                        {Math.floor(Math.random() * 8) + 1}
                      </span>
                    </li>
                  ))}
                </ul>
              </div>

              {/* Recent Posts */}
              <div
                style={{
                  background: "white",
                  border: "1px solid var(--color-light-gray)",
                  borderRadius: "12px",
                  padding: "24px",
                }}
              >
                <h4
                  style={{
                    fontFamily: "var(--font-serif)",
                    fontSize: "1rem",
                    color: "var(--color-navy)",
                    fontWeight: 700,
                    marginBottom: "16px",
                  }}
                >
                  Recent Posts
                </h4>
                <ul style={{ listStyle: "none", padding: 0, margin: 0 }}>
                  {recentPosts.map((post) => (
                    <li
                      key={post.slug}
                      style={{
                        borderBottom: "1px solid var(--color-light-gray)",
                        padding: "10px 0",
                      }}
                    >
                      <Link
                        href={`/blog/${post.slug}`}
                        style={{ textDecoration: "none" }}
                      >
                        <p
                          style={{
                            color: "var(--color-navy)",
                            fontSize: "0.85rem",
                            fontWeight: 600,
                            lineHeight: 1.4,
                            marginBottom: "4px",
                          }}
                        >
                          {post.title}
                        </p>
                        <p
                          style={{
                            color: "var(--color-gold)",
                            fontSize: "0.75rem",
                          }}
                        >
                          {post.date}
                        </p>
                      </Link>
                    </li>
                  ))}
                </ul>
              </div>

              {/* Newsletter Signup */}
              <div
                style={{
                  background: "var(--color-navy)",
                  borderRadius: "12px",
                  padding: "24px",
                }}
              >
                <FileText
                  size={24}
                  style={{ color: "var(--color-gold)", marginBottom: "12px" }}
                />
                <h4
                  style={{
                    fontFamily: "var(--font-serif)",
                    fontSize: "1rem",
                    color: "var(--color-gold)",
                    fontWeight: 700,
                    marginBottom: "8px",
                  }}
                >
                  Stay Updated
                </h4>
                <p
                  style={{
                    color: "rgba(255,255,255,0.6)",
                    fontSize: "0.82rem",
                    lineHeight: 1.6,
                    marginBottom: "16px",
                  }}
                >
                  Get case updates and new posts delivered directly to your
                  inbox.
                </p>
                <input
                  type="email"
                  placeholder="your@email.com"
                  style={{
                    width: "100%",
                    padding: "10px 14px",
                    borderRadius: "6px",
                    border: "none",
                    fontSize: "0.85rem",
                    marginBottom: "10px",
                    boxSizing: "border-box",
                    outline: "none",
                  }}
                />
                <button
                  style={{
                    width: "100%",
                    background: "var(--color-gold)",
                    color: "var(--color-navy)",
                    border: "none",
                    borderRadius: "6px",
                    padding: "10px",
                    fontSize: "0.88rem",
                    fontWeight: 700,
                    cursor: "pointer",
                  }}
                >
                  Subscribe
                </button>
              </div>

              {/* Urgent CTA */}
              <div
                style={{
                  background: "var(--color-crimson)",
                  borderRadius: "12px",
                  padding: "24px",
                  textAlign: "center",
                }}
              >
                <p
                  style={{
                    color: "white",
                    fontFamily: "var(--font-serif)",
                    fontSize: "1rem",
                    fontWeight: 700,
                    marginBottom: "8px",
                  }}
                >
                  Sep 16, 2026 Deadline
                </p>
                <p
                  style={{
                    color: "rgba(255,255,255,0.8)",
                    fontSize: "0.82rem",
                    marginBottom: "16px",
                    lineHeight: 1.5,
                  }}
                >
                  The deadline to stop adoption finalization is approaching.
                  Act now.
                </p>
                <Link
                  href="/donate"
                  style={{
                    display: "block",
                    background: "white",
                    color: "var(--color-crimson)",
                    fontWeight: 700,
                    padding: "10px",
                    borderRadius: "6px",
                    textDecoration: "none",
                    fontSize: "0.9rem",
                  }}
                >
                  Donate Now
                </Link>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
