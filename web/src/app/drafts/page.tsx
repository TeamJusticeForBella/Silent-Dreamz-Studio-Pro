"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { apiFetch } from "@/lib/api";

interface Draft {
  id: string;
  draft_type: string;
  status: string;
  title: string;
  incident_id: string | null;
  packet_id: string | null;
  created_at: string;
  updated_at: string;
}

const statusColors: Record<string, string> = {
  needs_review: "bg-yellow-100 text-yellow-800",
  approved: "bg-green-100 text-green-800",
  rejected: "bg-red-100 text-red-800",
  needs_evidence: "bg-orange-100 text-orange-800",
  in_progress: "bg-blue-100 text-blue-800",
};

export default function DraftsQueuePage() {
  const [items, setItems] = useState<Draft[]>([]);
  const [loading, setLoading] = useState(true);
  const [filterStatus, setFilterStatus] = useState<string>("");

  useEffect(() => {
    const params = filterStatus ? `?status=${filterStatus}` : "";
    apiFetch<{ items: Draft[] }>(`/drafts${params}`)
      .then((data) => setItems(data.items))
      .catch(() => setItems([]))
      .finally(() => setLoading(false));
  }, [filterStatus]);

  return (
    <div className="max-w-6xl mx-auto px-6 py-8">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold text-bcc-900">Draft Queue</h1>
        <Link href="/" className="text-sm text-bcc-600 hover:underline">
          Back to Dashboard
        </Link>
      </div>

      <div className="flex gap-2 mb-6">
        {["", "needs_review", "approved", "rejected", "needs_evidence"].map((s) => (
          <button
            key={s}
            onClick={() => setFilterStatus(s)}
            className={`px-3 py-1 rounded-full text-sm ${
              filterStatus === s
                ? "bg-bcc-600 text-white"
                : "bg-gray-100 text-gray-600 hover:bg-gray-200"
            }`}
          >
            {s === "" ? "All" : s.replace("_", " ")}
          </button>
        ))}
      </div>

      {loading ? (
        <p className="text-gray-500">Loading...</p>
      ) : items.length === 0 ? (
        <p className="text-gray-500">No drafts in queue. Generate a draft from an incident or packet.</p>
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
                    Type: {item.draft_type.replace("_", " ")} &middot;
                    Updated: {new Date(item.updated_at).toLocaleDateString()}
                  </p>
                </div>
                <span className={`px-2 py-1 rounded text-xs font-medium ${statusColors[item.status] || "bg-gray-100"}`}>
                  {item.status.replace("_", " ").toUpperCase()}
                </span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
