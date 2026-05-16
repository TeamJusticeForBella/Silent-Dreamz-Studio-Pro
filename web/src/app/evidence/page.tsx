"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { apiFetch } from "@/lib/api";

interface EvidenceItem {
  id: string;
  title: string;
  evidence_type: string;
  sha256: string;
  uploaded_at: string;
  is_key_evidence: boolean;
  tags: string[];
}

export default function EvidenceListPage() {
  const [items, setItems] = useState<EvidenceItem[]>([]);
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const params = query ? `?q=${encodeURIComponent(query)}` : "";
    apiFetch<{ items: EvidenceItem[] }>(`/evidence${params}`)
      .then((data) => setItems(data.items))
      .catch(() => setItems([]))
      .finally(() => setLoading(false));
  }, [query]);

  return (
    <div className="max-w-6xl mx-auto px-6 py-8">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold text-bcc-900">Evidence</h1>
        <Link
          href="/"
          className="text-sm text-bcc-600 hover:underline"
        >
          Back to Dashboard
        </Link>
      </div>

      <input
        type="text"
        placeholder="Search evidence..."
        className="w-full px-4 py-2 border border-gray-300 rounded-lg mb-6 focus:outline-none focus:ring-2 focus:ring-bcc-500"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />

      {loading ? (
        <p className="text-gray-500">Loading...</p>
      ) : items.length === 0 ? (
        <p className="text-gray-500">No evidence items found. Upload your first piece of evidence to get started.</p>
      ) : (
        <div className="space-y-3">
          {items.map((item) => (
            <div
              key={item.id}
              className="p-4 bg-white rounded-lg border border-gray-200 hover:border-bcc-500 transition-colors"
            >
              <div className="flex items-start justify-between">
                <div>
                  <h3 className="font-semibold text-gray-900">{item.title}</h3>
                  <p className="text-sm text-gray-500 mt-1">
                    {item.evidence_type.toUpperCase()} &middot; {new Date(item.uploaded_at).toLocaleDateString()}
                    &middot; SHA: {item.sha256.slice(0, 12)}...
                  </p>
                  {item.tags.length > 0 && (
                    <div className="flex gap-1 mt-2">
                      {item.tags.map((tag) => (
                        <span key={tag} className="px-2 py-0.5 bg-bcc-50 text-bcc-700 rounded text-xs">
                          {tag}
                        </span>
                      ))}
                    </div>
                  )}
                </div>
                {item.is_key_evidence && (
                  <span className="px-2 py-1 bg-yellow-100 text-yellow-800 rounded text-xs font-medium">
                    KEY
                  </span>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
