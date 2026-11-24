import { createMDX } from 'fumadocs-mdx/next';

const withMDX = createMDX();

/**
 * The wiki is a static export served at /wiki/ on the main site (wordsmithand.ink/wiki/).
 * The Pages workflow copies `out/` into the published site's `wiki/` folder.
 * @type {import('next').NextConfig}
 */
const config = {
  output: 'export',
  basePath: '/wiki',
  trailingSlash: true,
  images: { unoptimized: true },
  reactStrictMode: true,
  // the local preview at https://wordwiki.test proxies to `next dev`
  allowedDevOrigins: ['wordwiki.test'],
};

export default withMDX(config);
