"use client";

import { useRef } from "react";
import { useDocuments } from "@/hooks/useDocuments";

export default function DocumentManager() {
  const { documents, loading, status, upload, remove, setStatus } =
    useDocuments();
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      upload(file);
    }
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  return (
    <div
      style={{
        borderTop: "1px solid var(--border)",
        display: "flex",
        flexDirection: "column",
        minHeight: 0,
      }}
    >
      <div
        style={{
          padding: "8px 14px",
          fontSize: 11,
          fontWeight: 600,
          color: "var(--text-muted)",
          textTransform: "uppercase",
          letterSpacing: "0.5px",
        }}
      >
        文档管理
      </div>

      <div style={{ padding: "0 10px 6px" }}>
        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf"
          onChange={handleSelect}
          style={{ display: "none" }}
        />
        <button
          onClick={() => fileInputRef.current?.click()}
          style={{
            width: "100%",
            padding: "7px 0",
            border: "1px dashed var(--border)",
            borderRadius: 8,
            background: "var(--bg-primary)",
            cursor: "pointer",
            fontSize: 12,
            color: "var(--accent)",
          }}
        >
          + 添加 PDF
        </button>
      </div>

      {status && (
        <div
          style={{
            padding: "4px 14px",
            fontSize: 11,
            color: status.includes("失败") || status.includes("error")
              ? "#ef4444"
              : "var(--text-muted)",
            whiteSpace: "normal",
            wordBreak: "break-all",
          }}
        >
          {status}
          {status.includes("成功") && (
            <button
              onClick={() => setStatus(null)}
              style={{
                background: "none",
                border: "none",
                color: "var(--text-muted)",
                cursor: "pointer",
                fontSize: 14,
                padding: "0 4px",
                lineHeight: 1,
              }}
            >
              ×
            </button>
          )}
        </div>
      )}

      <div
        style={{
          overflowY: "auto",
          padding: "0 8px 8px",
          maxHeight: 160,
          minHeight: 0,
        }}
      >
        {loading && documents.length === 0 && (
          <div
            style={{
              fontSize: 11,
              color: "var(--text-muted)",
              textAlign: "center",
              padding: "12px 0",
            }}
          >
            加载中...
          </div>
        )}
        {documents.map((doc) => (
          <div
            key={doc.filename}
            style={{
              padding: "6px 10px",
              borderRadius: 6,
              marginBottom: 2,
              fontSize: 11,
              color: "var(--text-secondary)",
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              gap: 4,
            }}
          >
            <span
              style={{
                overflow: "hidden",
                textOverflow: "ellipsis",
                whiteSpace: "nowrap",
                flex: 1,
              }}
              title={doc.filename}
            >
              {doc.filename}
              <span
                style={{
                  color: "var(--text-muted)",
                  fontSize: 10,
                  marginLeft: 4,
                }}
              >
                ({doc.chunk_count})
              </span>
            </span>
            <button
              onClick={() => remove(doc.filename)}
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
              title="删除文档索引"
            >
              ×
            </button>
          </div>
        ))}
        {!loading && documents.length === 0 && (
          <div
            style={{
              fontSize: 11,
              color: "var(--text-muted)",
              textAlign: "center",
              padding: "8px 0",
            }}
          >
            暂无索引文档
          </div>
        )}
      </div>
    </div>
  );
}
