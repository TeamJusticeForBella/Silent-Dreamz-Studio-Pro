const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "/api";

export async function apiFetch<T>(
  path: string,
  options: RequestInit = {},
  workspaceId = "00000000-0000-0000-0000-000000000001"
): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      "X-Workspace-Id": workspaceId,
      ...options.headers,
    },
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`API ${res.status}: ${text}`);
  }
  return res.json();
}
