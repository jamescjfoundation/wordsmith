import { createMDX } from 'fumadocs-mdx/next';

const withMDX = createMDX();

// `next dev` answers http://localhost:3000 as it is. A machine that reaches the dev server under
// another host name (a local proxy) names that host in WIKI_DEV_ORIGINS, comma-separated, in its
// own untracked .env.local. A host name of one machine is never written in this file.
const devOrigins = (process.env.WIKI_DEV_ORIGINS ?? '')
  .split(',')
  .map((origin) => origin.trim())
  .filter(Boolean);

/**
 * The wiki is a static export served at /wiki/ on the main site (wordsmithand.ink/wiki/).
 * The checks workflow puts `out/` into the site's `wiki/` folder, and the Pages workflow publishes it.
 * @type {import('next').NextConfig}
 */
const config = {
  output: 'export',
  basePath: '/wiki',
  trailingSlash: true,
  images: { unoptimized: true },
  reactStrictMode: true,
  ...(devOrigins.length > 0 ? { allowedDevOrigins: devOrigins } : {}),
};

export default withMDX(config);
