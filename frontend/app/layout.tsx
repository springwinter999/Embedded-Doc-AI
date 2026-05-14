import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Embedded Doc AI",
  description: "AI辅助嵌入式文档查询系统",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="zh-CN">
      <body>{children}</body>
    </html>
  );
}
