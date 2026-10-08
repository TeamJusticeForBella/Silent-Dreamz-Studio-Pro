"use client";

import { useState } from "react";
import Link from "next/link";
import { apiFetch } from "@/lib/api";

interface SearchResult {
  kind: string;
  id: string;
  score: number;
  snippet: string | null;
}

export default function SearchPage() {
  const [query, setQuery] = useState("");
  const [mode, setMode] = useState<"hybrid" | "fulltext" | "semantic">("hybrid");
  const [results, setResults] = useState<SearchResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [searched, setSearched] = useState(false);

  const handleSearch = async () => {
    if (!query.trim()) return;
    setLoading(true);
    setSearched(true);
    try {
      const data = await apiFetch<{ results: SearchResult[] }>(
        `/search?q=${encodeURIComponent(query)}&mode=${mode}`
      );
      setResults(data.results);
    } catch {
      setResults([]);
    } finally {
      setLoading(false);
    }
  };

  const kindColors: Record<string, string> = {
    evidence: "bg-blue-100 text-blue-800",
    incident: "bg-red-100 text-red-800",
    draft: "bg-purple-100 text-purple-800",
    packet: "bg-green-100 text-green-800",
  };

  return (
    <div className="max-w-6xl mx-auto px-6 py-8">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold text-bcc-900">Search</h1>
        <Link href="/" className="text-sm text-bcc-600 hover:underline">
          Back to Dashboard
        </Link>
      </div>

      <div className="flex gap-3 mb-6">
        <input
          type="text"
          placeholder="Search evidence, incidents, drafts, packets..."
          className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-bcc-500"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSearch()}
        />
        <select
          className="px-3 py-2 border border-gray-300 rounded-lg text-sm"
          value={mode}
          onChange={(e) => setMode(e.target.value as typeof mode)}
        >
          <option value="hybrid">Hybrid</option>
          <option value="fulltext">Fulltext</option>
          <option value="semantic">Semantic</option>
        </select>
        <button
          onClick={handleSearch}
          className="px-6 py-2 bg-bcc-600 text-white rounded-lg hover:bg-bcc-700 transition-colors"
        >
          Search
        </button>
      </div>

      {loading ? (
        <p className="text-gray-500">Searching...</p>
      ) : searched && results.length === 0 ? (
        <p className="text-gray-500">No results found.</p>
      ) : (
        <div className="space-y-3">
          {results.map((result, idx) => (
            <div
              key={`${result.kind}-${result.id}-${idx}`}
              className="p-4 bg-white rounded-lg border border-gray-200"
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-1">
                    <span className={`px-2 py-0.5 rounded text-xs font-medium ${kindColors[result.kind] || "bg-gray-100"}`}>
                      {result.kind}
                    </span>
                    <span className="text-xs text-gray-400">
                      Score: {result.score.toFixed(3)}
                    </span>
                  </div>
                  <p className="text-sm text-gray-600 font-mono">{result.id}</p>
                  {result.snippet && (
                    <p
                      className="text-sm text-gray-700 mt-2 line-clamp-3"
                      dangerouslySetInnerHTML={{ __html: result.snippet }}
                    />
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
