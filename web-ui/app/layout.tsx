import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "PII Detection Service",
  description: "Secure, local PII detection powered by AI.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased">{children}</body>
    </html>
  );
}