import type { Metadata } from "next";
import { Inter, Playfair_Display } from "next/font/google";
import "./globals.css";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
  display: "swap",
});

const playfair = Playfair_Display({
  subsets: ["latin"],
  variable: "--font-playfair",
  display: "swap",
});

export const metadata: Metadata = {
  title: {
    template: "%s | Bella Barr — Bring Her Home",
    default: "Bring Bella Home | Neveyah-RosaBella Barr",
  },
  description:
    "Neveyah-RosaBella Barr — wrongfully taken. Fighting to return. Public advocacy for Case 21DP0705A. Evidence transparency. Justice.",
  openGraph: {
    type: "website",
    siteName: "Bring Bella Home",
    title: "Bring Bella Home | Justice for Neveyah-RosaBella Barr",
    description:
      "A father's fight to reunite with his daughter. Case 21DP0705A. Evidence. Truth. Justice.",
  },
  twitter: {
    card: "summary_large_image",
    title: "Bring Bella Home",
    description: "Help bring Neveyah-RosaBella Barr home.",
  },
  keywords: [
    "Bella Barr",
    "Neveyah-RosaBella Barr",
    "bring bella home",
    "Case 21DP0705A",
    "Jason Barr",
    "justice for bella",
    "foster care accountability",
    "ICWA",
  ],
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      className={`${inter.variable} ${playfair.variable} h-full antialiased`}
    >
      <body className="min-h-full flex flex-col font-sans">
        {/* Urgency Banner */}
        <div className="urgency-bar">
          ⚠️ URGENT: Adoption finalization threatened —{" "}
          <strong>September 16, 2026</strong>. Act now.
        </div>

        <Navbar />
        <main className="flex-1">{children}</main>
        <Footer />
      </body>
    </html>
  );
}
