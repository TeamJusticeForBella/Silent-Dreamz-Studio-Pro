"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { apiFetch } from "@/lib/api";

interface Packet {
  id: string;
  packet_type: string;
  status: string;
  title: string;
  target_name: string | null;
  created_at: string;
}

const statusColors: Record<string, string> = {
  draft: "bg-gray-100 text-gray-700",
  under_review: "bg-yellow-100 text-yellow-800",
  locked: "bg-blue-100 text-blue-800",
  exported: "bg-green-100 text-green-800",
};

export default function PacketsListPage() {
  const [items, setItems] = useState<Packet[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    apiFetch<{ items: Packet[] }>("/packets")
      .then((data) => setItems(data.items))
      .catch(() => setItems([]))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="max-w-6xl mx-auto px-6 py-8">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold text-bcc-900">Packets</h1>
        <Link href="/" className="text-sm text-bcc-600 hover:underline">
          Back to Dashboard
        </Link>
      </div>

      {loading ? (
        <p className="text-gray-500">Loading...</p>
      ) : items.length === 0 ? (
        <p className="text-gray-500">No packets yet. Create a packet to start building a court-ready bundle.</p>
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
                    Type: {item.packet_type.replace("_", " ")}
                    {item.target_name && <> &middot; Target: {item.target_name}</>}
                  </p>
                </div>
                <span className={`px-2 py-1 rounded text-xs font-medium ${statusColors[item.status] || "bg-gray-100 text-gray-700"}`}>
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
