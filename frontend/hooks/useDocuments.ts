"use client";

import { useState, useEffect, useCallback } from "react";
import {
  listDocuments,
  uploadDocument,
  deleteDocument,
  type DocumentStats,
} from "@/lib/api";

export function useDocuments() {
  const [documents, setDocuments] = useState<DocumentStats[]>([]);
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState<string | null>(null);

  const refresh = useCallback(async () => {
    setLoading(true);
    try {
      const data = await listDocuments();
      setDocuments(data.documents);
    } catch {
      // silently fail if backend not running
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    refresh();
  }, [refresh]);

  const upload = useCallback(
    async (file: File) => {
      setStatus(`正在索引 ${file.name}...`);
      try {
        const result = await uploadDocument(file);
        if (result.status === "ok") {
          setStatus(result.message);
          await refresh();
        } else {
          setStatus(result.message);
        }
      } catch (e: unknown) {
        const msg = e instanceof Error ? e.message : "上传失败";
        setStatus(msg);
      }
    },
    [refresh]
  );

  const remove = useCallback(
    async (filename: string) => {
      setStatus(`正在删除 ${filename}...`);
      try {
        await deleteDocument(filename);
        setDocuments((prev) => prev.filter((d) => d.filename !== filename));
        setStatus(null);
      } catch (e: unknown) {
        const msg = e instanceof Error ? e.message : "删除失败";
        setStatus(msg);
      }
    },
    []
  );

  return { documents, loading, status, refresh, upload, remove, setStatus };
}
