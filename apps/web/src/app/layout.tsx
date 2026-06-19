import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Learn It",
  description: "A cognitive operating system for deliberate learning.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
