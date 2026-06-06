import type { Metadata } from "next";
import { Geist_Mono } from "next/font/google";
import "./globals.css";

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: {
    default: "SkillBridge AI — Career Intelligence Platform",
    template: "%s | SkillBridge AI",
  },
  description:
    "AI-powered career guidance platform that matches students with jobs, internships, mentors and courses using intelligent recommendations.",
  keywords: ["career", "AI", "internship", "jobs", "mentors", "resume", "skill gap"],
  openGraph: {
    title: "SkillBridge AI",
    description: "AI-Powered Career Intelligence Platform for Students",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={`${geistMono.variable} h-full`} suppressHydrationWarning>
      <body className="min-h-full flex flex-col antialiased">{children}</body>
    </html>
  );
}
