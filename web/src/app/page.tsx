import Link from "next/link";

const navItems = [
  { href: "/evidence", label: "Evidence", desc: "Ingest, view, and manage evidence items" },
  { href: "/incidents", label: "Incidents", desc: "Document incidents with linked evidence" },
  { href: "/packets", label: "Packets", desc: "Build court-ready document bundles" },
  { href: "/drafts", label: "Draft Queue", desc: "Review and approve AI-generated drafts" },
  { href: "/search", label: "Search", desc: "Fulltext + semantic search across everything" },
];

export default function HomePage() {
  return (
    <main className="max-w-5xl mx-auto px-6 py-12">
      <div className="mb-12 text-center">
        <h1 className="text-4xl font-bold text-bcc-900 mb-2">
          Bella Command Center
        </h1>
        <p className="text-lg text-gray-600">
          Evidence management, incident documentation, and court-ready exports.
        </p>
        <p className="text-sm text-gray-400 mt-1">For Justice. For Bella.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {navItems.map((item) => (
          <Link
            key={item.href}
            href={item.href}
            className="block p-6 bg-white rounded-xl shadow-sm border border-gray-200 hover:border-bcc-500 hover:shadow-md transition-all"
          >
            <h2 className="text-xl font-semibold text-bcc-700 mb-2">
              {item.label}
            </h2>
            <p className="text-gray-500 text-sm">{item.desc}</p>
          </Link>
        ))}
      </div>
    </main>
  );
}
