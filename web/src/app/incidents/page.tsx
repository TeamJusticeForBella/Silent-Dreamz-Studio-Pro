"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { apiFetch } from "@/lib/api";

interface Incident {
  id: string;
  title: string;
  status: string;
  allegation_tags: string[];
  created_at: string;
  updated_at: string;
}

export default function IncidentsListPage() {
  const [items, setItems] = useState<Incident[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    apiFetch<{ items: Incident[] }>("/incidents")
      .then((data) => setItems(data.items))
      .catch(() => setItems([]))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="max-w-6xl mx-auto px-6 py-8">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold text-bcc-900">Incidents</h1>
        <Link href="/" className="text-sm text-bcc-600 hover:underline">
          Back to Dashboard
        </Link>
      </div>

      {loading ? (
        <p className="text-gray-500">Loading...</p>
      ) : items.length === 0 ? (
        <p className="text-gray-500">No incidents yet. Create your first incident to start building your case.</p>
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
                    Status: {item.status} &middot; Created: {new Date(item.created_at).toLocaleDateString()}
                  </p>
                  {item.allegation_tags.length > 0 && (
                    <div className="flex gap-1 mt-2">
                      {item.allegation_tags.map((tag) => (
                        <span key={tag} className="px-2 py-0.5 bg-red-50 text-red-700 rounded text-xs">
                          {tag}
                        </span>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
