import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "AI Decision Flow - FlyRank BE-09",
  description: "Visual AI workflow system with React Flow + Inngest",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-gray-50">{children}</body>
    </html>
  );
}