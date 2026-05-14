"use client";

import { useChat } from "@/hooks/useChat";
import { useConversations } from "@/hooks/useConversations";
import { getChatHistory, type ChatHistoryResponse } from "@/lib/api";
import ConversationList from "@/components/ConversationList";
import ChatPanel from "@/components/ChatPanel";
import DocumentManager from "@/components/DocumentManager";

export default function Home() {
  const chat = useChat();
  const convs = useConversations();

  const handleSelect = async (id: string) => {
    try {
      const data: ChatHistoryResponse = await getChatHistory(id);
      chat.loadHistory(
        data.messages.map((m) => ({
          id: m.id,
          role: m.role,
          content: m.content,
          sources: m.sources,
        })),
        data.conversation_id
      );
    } catch {
      // conversation may have been deleted
    }
  };

  const handleDelete = async (id: string) => {
    await convs.remove(id);
    if (chat.conversationId === id) {
      chat.reset();
    }
  };

  const handleNew = () => {
    chat.reset();
  };

  return (
    <div style={{ display: "flex", height: "100vh" }}>
      <div
        style={{
          width: 240,
          display: "flex",
          flexDirection: "column",
          height: "100vh",
          background: "var(--bg-sidebar)",
          borderRight: "1px solid var(--border)",
        }}
      >
        <ConversationList
          conversations={convs.conversations}
          activeId={chat.conversationId}
          onSelect={handleSelect}
          onDelete={handleDelete}
          onNew={handleNew}
        />
        <DocumentManager />
      </div>
      <ChatPanel
        messages={chat.messages}
        loading={chat.loading}
        error={chat.error}
        onSend={chat.send}
        title={
          convs.conversations.find((c) => c.id === chat.conversationId)?.title
        }
      />
    </div>
  );
}
