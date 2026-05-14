"use client";

import { useState, useCallback } from "react";
import { sendMessage, ChatResponse, SourceRef } from "@/lib/api";

export interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  sources: SourceRef[];
}

export function useChat() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [conversationId, setConversationId] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const send = useCallback(
    async (question: string) => {
      setLoading(true);
      setError(null);

      const userMsg: ChatMessage = {
        id: crypto.randomUUID(),
        role: "user",
        content: question,
        sources: [],
      };
      setMessages((prev) => [...prev, userMsg]);

      try {
        const data: ChatResponse = await sendMessage(
          question,
          conversationId || undefined
        );
        if (!conversationId) {
          setConversationId(data.conversation_id);
        }
        const aiMsg: ChatMessage = {
          id: data.message_id,
          role: "assistant",
          content: data.answer,
          sources: data.sources,
        };
        setMessages((prev) => [...prev, aiMsg]);
      } catch (e: unknown) {
        const msg = e instanceof Error ? e.message : "请求失败，请检查后端是否启动";
        setError(msg);
      } finally {
        setLoading(false);
      }
    },
    [conversationId]
  );

  const loadHistory = useCallback(
    (historyMessages: ChatMessage[], convId: string) => {
      setMessages(historyMessages);
      setConversationId(convId);
      setError(null);
    },
    []
  );

  const reset = useCallback(() => {
    setMessages([]);
    setConversationId(null);
    setError(null);
  }, []);

  return { messages, conversationId, loading, error, send, loadHistory, reset };
}
