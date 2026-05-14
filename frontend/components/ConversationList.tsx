"use client";

import type { Conversation } from "@/lib/api";

interface Props {
  conversations: Conversation[];
  activeId: string | null;
  onSelect: (id: string) => void;
  onDelete: (id: string) => void;
  onNew: () => void;
}

export default function ConversationList({
  conversations,
  activeId,
  onSelect,
  onDelete,
  onNew,
}: Props) {
  return (
    <div
      style={{
        width: 240,
        background: "var(--bg-sidebar)",
        borderRight: "1px solid var(--border)",
        display: "flex",
        flexDirection: "column",
        height: "100vh",
      }}
    >
      <div style={{ padding: "18px 14px" }}>
        <div
          style={{
            fontWeight: 700,
            color: "var(--text-primary)",
            fontSize: 14,
          }}
        >
          STM32H5 Helper
        </div>
        <div style={{ color: "var(--accent)", fontSize: 10, marginTop: 3 }}>
          嵌入式文档 AI 助手
        </div>
      </div>

      <div style={{ padding: "0 10px 10px" }}>
        <button
          onClick={onNew}
          style={{
            width: "100%",
            padding: "9px 0",
            border: "1px solid var(--border)",
            borderRadius: 8,
            background: "var(--bg-primary)",
            cursor: "pointer",
            fontSize: 13,
            color: "var(--text-primary)",
            fontWeight: 500,
            boxShadow: "var(--shadow-sm)",
          }}
        >
          + 新对话
        </button>
      </div>

      <div style={{ flex: 1, overflowY: "auto", padding: "0 8px" }}>
        {conversations.map((conv) => (
          <div
            key={conv.id}
            onClick={() => onSelect(conv.id)}
            style={{
              padding: "10px 12px",
              borderRadius: 8,
              marginBottom: 2,
              fontSize: 13,
              color:
                activeId === conv.id
                  ? "var(--accent)"
                  : "var(--text-secondary)",
              fontWeight: activeId === conv.id ? 600 : 400,
              background:
                activeId === conv.id ? "var(--bubble-user)" : "transparent",
              cursor: "pointer",
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
            }}
          >
            <span
              style={{
                overflow: "hidden",
                textOverflow: "ellipsis",
                whiteSpace: "nowrap",
                flex: 1,
              }}
            >
              {conv.title || "新对话"}
            </span>
            <button
              onClick={(e) => {
                e.stopPropagation();
                onDelete(conv.id);
              }}
              style={{
                background: "none",
                border: "none",
                color: "var(--text-muted)",
                cursor: "pointer",
                fontSize: 14,
                padding: "0 2px",
                opacity: 0.5,
                flexShrink: 0,
              }}
              title="删除对话"
            >
              ×
            </button>
          </div>
        ))}
        {conversations.length === 0 && (
          <div
            style={{
              fontSize: 12,
              color: "var(--text-muted)",
              textAlign: "center",
              marginTop: 24,
            }}
          >
            暂无对话
          </div>
        )}
      </div>

      <div
        style={{
          padding: "12px 14px",
          borderTop: "1px solid var(--border)",
          fontSize: 10,
          color: "var(--text-muted)",
        }}
      >
        STM32H5 HAL 手册
      </div>
    </div>
  );
}
