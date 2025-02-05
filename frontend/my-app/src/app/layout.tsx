import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "CV Crafter",
  description: "App that auto generates CV and cover letter for a given position description using AI.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className="h-screen flex items-center justify-center"
      >
        {children}
      </body>
    </html>
  );
}
