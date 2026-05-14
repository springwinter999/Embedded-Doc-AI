"use client";

import { SourceRef } from "@/lib/api";

export default function SourceBadge({ source }: { source: SourceRef }) {
  return (
    <span
      style={{
        display: "inline-flex",
        alignItems: "center",
        gap: 4,
        background: "var(--badge-bg)",
        color: "var(--badge-text)",
        fontSize: 11,
        padding: "3px 10px",
        borderRadius: 14,
        border: "1px solid var(--badge-border)",
        cursor: "default",
        whiteSpace: "nowrap",
      }}
      title={source.snippet}
    >
      {source.filename} p.{source.page}
    </span>
  );
}
