const { i18n } = require('./next-i18next.config');
const buildWithDocker = process.env.DOCKER === 'true';
/** @type {import('next').NextConfig} */
const nextConfig = {
  i18n,
  reactStrictMode: false,

  webpack(config, { isServer, dev }) {
    config.experiments = {
      asyncWebAssembly: true,
      layers: true,
    };

    return config;
  },
  output: buildWithDocker ? 'standalone' : undefined,
};

module.exports = nextConfig;
