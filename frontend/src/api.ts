const API_BASE = "/api";

export async function createSession(): Promise<string> {
  const res = await fetch(`${API_BASE}/session`, { method: "POST" });
  const data = await res.json();
  return data.session_id;
}

export async function fullChat(
  audio: Blob,
  sessionId: string
): Promise<{
  transcript: string;
  response: string;
  audio_base64: string;
  session_id: string;
  emotion?: { emotion: string; intensity: number; summary: string };
}> {
  const form = new FormData();
  form.append("audio", audio, "recording.webm");
  form.append("session_id", sessionId);

  const res = await fetch(`${API_BASE}/chat`, {
    method: "POST",
    body: form,
  });

  const contentType = res.headers.get("content-type") || "";
  const isJson = contentType.includes("application/json");
  const body = isJson ? await res.json() : await res.text();

  if (!res.ok) {
    const detail =
      typeof body === "string"
        ? body
        : body?.detail || body?.error || "Request failed";
    throw new Error(detail);
  }

  if (!isJson) {
    throw new Error("Unexpected server response format");
  }

  return body;
}
