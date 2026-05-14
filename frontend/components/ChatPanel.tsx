"use client";

import type { ChatMessage } from "@/hooks/useChat";
import ChatInput from "./ChatInput";
import SourceBadge from "./SourceBadge";
import type { ReactNode } from "react";

interface Props {
  messages: ChatMessage[];
  loading: boolean;
  error: string | null;
  onSend: (text: string) => void;
  title?: string;
}

function renderContent(content: string): ReactNode {
  const lines = content.split("\n");
  let inCode = false;
  const result: ReactNode[] = [];
  let codeLines: string[] = [];

  const flushCode = () => {
    if (codeLines.length > 0) {
      result.push(
        <pre
          key={`code-${result.length}`}
          style={{
            background: "var(--code-bg)",
            border: "1px solid var(--code-border)",
            padding: "10px 14px",
            borderRadius: 8,
            fontSize: 12,
            overflow: "auto",
            margin: "8px 0",
          }}
        >
          <code>{codeLines.join("\n")}</code>
        </pre>
      );
      codeLines = [];
    }
  };

  for (const line of lines) {
    if (line.trim().startsWith("```")) {
      if (inCode) flushCode();
      inCode = !inCode;
      continue;
    }
    if (inCode) {
      codeLines.push(line);
    } else {
      flushCode();
      if (line.trim()) {
        result.push(
          <p key={`p-${result.length}`} style={{ margin: "4px 0" }}>
            {line}
          </p>
        );
      } else {
        result.push(<div key={`br-${result.length}`} style={{ height: 4 }} />);
      }
    }
  }
  flushCode();
  return result;
}

export default function ChatPanel({
  messages,
  loading,
  error,
  onSend,
  title,
}: Props) {
  return (
    <div
      style={{ flex: 1, display: "flex", flexDirection: "column", minWidth: 0 }}
    >
      <div
        style={{
          padding: "14px 20px",
          borderBottom: "1px solid var(--border-light)",
          fontSize: 14,
          color: "var(--text-secondary)",
          fontWeight: 500,
        }}
      >
        {title || "新对话"}
      </div>

      <div
        style={{
          flex: 1,
          overflowY: "auto",
          padding: "24px 28px",
          background: "var(--bg-chat)",
        }}
      >
        {messages.length === 0 && !loading && (
          <div
            style={{
              textAlign: "center",
              color: "var(--text-muted)",
              marginTop: 120,
              fontSize: 15,
            }}
          >
            输入你的嵌入式问题开始查询
          </div>
        )}

        {messages.map((msg) => (
          <div
            key={msg.id}
            style={{
              marginBottom: 24,
              display: "flex",
              justifyContent:
                msg.role === "user" ? "flex-end" : "flex-start",
            }}
          >
            <div
              style={{ maxWidth: msg.role === "user" ? "75%" : "90%" }}
            >
              <div
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: 6,
                  justifyContent:
                    msg.role === "user" ? "flex-end" : "flex-start",
                  marginBottom: 4,
                }}
              >
                <span
                  style={{
                    width: 20,
                    height: 20,
                    borderRadius: "50%",
                    background:
                      msg.role === "user"
                        ? "var(--accent)"
                        : "var(--success)",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    color: "#fff",
                    fontSize: 10,
                    fontWeight: 700,
                  }}
                >
                  {msg.role === "user" ? "Y" : "AI"}
                </span>
                <span style={{ fontSize: 11, color: "var(--text-muted)" }}>
                  {msg.role === "user" ? "你" : "DeepSeek"}
                </span>
              </div>
              <div
                style={{
                  background:
                    msg.role === "user"
                      ? "var(--bubble-user)"
                      : "var(--bubble-ai-bg)",
                  border:
                    msg.role === "user"
                      ? "none"
                      : "1px solid var(--bubble-ai-border)",
                  padding: "12px 16px",
                  borderRadius:
                    msg.role === "user"
                      ? "12px 4px 12px 12px"
                      : "4px 12px 12px 12px",
                  fontSize: 14,
                  lineHeight: 1.7,
                  color: "var(--text-primary)",
                }}
              >
                {renderContent(msg.content)}

                {msg.sources && msg.sources.length > 0 && (
                  <div
                    style={{
                      marginTop: 12,
                      display: "flex",
                      gap: 6,
                      flexWrap: "wrap",
                    }}
                  >
                    {msg.sources.map((s, i) => (
                      <SourceBadge key={i} source={s} />
                    ))}
                  </div>
                )}
              </div>
            </div>
          </div>
        ))}

        {loading && (
          <div
            style={{
              display: "flex",
              gap: 8,
              alignItems: "center",
              padding: "8px 0",
            }}
          >
            <span
              style={{
                width: 8,
                height: 8,
                background: "var(--accent)",
                borderRadius: "50%",
                animation: "pulse 1s infinite",
              }}
            />
            <span style={{ fontSize: 13, color: "var(--text-muted)" }}>
              查询文档中...
            </span>
          </div>
        )}

        {error && (
          <div
            style={{
              padding: 12,
              background: "#fff0f0",
              border: "1px solid #ffcccc",
              borderRadius: 8,
              color: "#cc0000",
              fontSize: 13,
            }}
          >
            {error}
          </div>
        )}
      </div>

      <ChatInput onSend={onSend} disabled={loading} />
    </div>
  );
}
