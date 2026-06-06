import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Allow images from any domain for company logos / avatars
  images: {
    remotePatterns: [
      { protocol: "https", hostname: "**" },
    ],
  },
  // Proxy /api/* → FastAPI backend in dev
  async rewrites() {
    return [
      {
        source: "/api/:path*",
        destination: `${process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api/v1"}/:path*`,
      },
    ];
  },
};

export default nextConfig;
