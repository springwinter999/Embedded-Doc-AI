"use client";

import { useState, type KeyboardEvent } from "react";

interface Props {
  onSend: (text: string) => void;
  disabled: boolean;
}

export default function ChatInput({ onSend, disabled }: Props) {
  const [text, setText] = useState("");

  const handleSend = () => {
    const trimmed = text.trim();
    if (!trimmed || disabled) return;
    onSend(trimmed);
    setText("");
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div
      style={{
        padding: "14px 20px",
        borderTop: "1px solid var(--border-light)",
        background: "var(--bg-primary)",
      }}
    >
      <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
        <input
          value={text}
          onChange={(e) => setText(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="输入你的嵌入式问题..."
          disabled={disabled}
          style={{
            flex: 1,
            padding: "10px 16px",
            border: "1px solid var(--border)",
            borderRadius: 10,
            fontSize: 14,
            outline: "none",
            color: "var(--text-primary)",
            background: "var(--bg-chat)",
          }}
        />
        <button
          onClick={handleSend}
          disabled={disabled || !text.trim()}
          style={{
            padding: "10px 22px",
            background: disabled || !text.trim() ? "#ccc" : "var(--accent)",
            color: "#fff",
            border: "none",
            borderRadius: 10,
            fontSize: 13,
            fontWeight: 600,
            cursor: disabled || !text.trim() ? "not-allowed" : "pointer",
          }}
        >
          发送
        </button>
      </div>
      <div
        style={{
          fontSize: 11,
          color: "var(--text-muted)",
          textAlign: "center",
          marginTop: 6,
        }}
      >
        答案基于文档生成，请以官方手册为准
      </div>
    </div>
  );
}
