"use client";

import { useState, useCallback, useEffect } from "react";
import {
  listConversations,
  deleteConversation,
  Conversation,
} from "@/lib/api";

export function useConversations() {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [loading, setLoading] = useState(false);

  const refresh = useCallback(async () => {
    setLoading(true);
    try {
      const data = await listConversations();
      setConversations(data.conversations);
    } catch {
      // silently fail — backend might not be running yet
    } finally {
      setLoading(false);
    }
  }, []);

  const remove = useCallback(async (id: string) => {
    await deleteConversation(id);
    setConversations((prev) => prev.filter((c) => c.id !== id));
  }, []);

  useEffect(() => {
    refresh();
  }, [refresh]);

  return { conversations, loading, refresh, remove };
}
