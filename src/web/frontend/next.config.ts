import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://localhost:8000/api/:path*',
      },
    ];
  },
  // Configure port for development
  // Note: Next.js doesn't support port config in next.config, use package.json script instead
};

export default nextConfig;
