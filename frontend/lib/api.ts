const BASE_URL = "http://localhost:8000/api";

export interface SourceRef {
  page: number;
  filename: string;
  snippet: string;
  chunk_id: string;
}

export interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  sources: SourceRef[];
  created_at: string;
}

export interface Conversation {
  id: string;
  title: string;
  created_at: string;
  updated_at: string;
  message_count: number;
}

export interface ChatResponse {
  answer: string;
  conversation_id: string;
  sources: SourceRef[];
  message_id: string;
}

export interface ChatHistoryResponse {
  conversation_id: string;
  title: string;
  messages: Message[];
}

export interface DocumentStats {
  filename: string;
  chunk_count: number;
}

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) {
    const body = await res.text();
    throw new Error(body || `HTTP ${res.status}`);
  }
  return res.json();
}

export function sendMessage(
  question: string,
  conversationId?: string
): Promise<ChatResponse> {
  return request<ChatResponse>("/chat", {
    method: "POST",
    body: JSON.stringify({
      question,
      conversation_id: conversationId || undefined,
    }),
  });
}

export function getChatHistory(
  conversationId: string
): Promise<ChatHistoryResponse> {
  return request<ChatHistoryResponse>(`/chat/${conversationId}`);
}

export function listConversations(): Promise<{
  conversations: Conversation[];
}> {
  return request<{ conversations: Conversation[] }>("/conversations");
}

export function deleteConversation(id: string): Promise<{ status: string }> {
  return request<{ status: string }>(`/conversations/${id}`, {
    method: "DELETE",
  });
}

export function indexDocuments(): Promise<{
  status: string;
  message: string;
  files_processed: number;
  total_chunks: number;
}> {
  return request("/documents/index", { method: "POST" });
}

export function listDocuments(): Promise<{ documents: DocumentStats[] }> {
  return request<{ documents: DocumentStats[] }>("/documents");
}

export async function uploadDocument(file: File): Promise<{
  status: string;
  filename: string;
  total_chunks: number;
  message: string;
}> {
  const formData = new FormData();
  formData.append("file", file);
  const res = await fetch(`${BASE_URL}/documents/upload`, {
    method: "POST",
    body: formData,
  });
  if (!res.ok) {
    const body = await res.text();
    throw new Error(body || `HTTP ${res.status}`);
  }
  return res.json();
}

export async function deleteDocument(filename: string): Promise<{
  status: string;
  filename: string;
  removed_chunks: number;
  message: string;
}> {
  return request(`/documents/${encodeURIComponent(filename)}`, {
    method: "DELETE",
  });
}
