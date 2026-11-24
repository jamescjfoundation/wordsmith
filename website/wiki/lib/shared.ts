import { createGetUrl } from 'fumadocs-core/source';

export const appName = 'Wordsmith Wiki';
export const siteUrl = 'https://wordsmithand.ink';
export const docsRoute = '/';
export const docsContentRoute = '/llms.mdx/docs';

export const gitConfig = {
  user: 'jamescjfoundation',
  repo: 'wordsmith',
  branch: 'main',
  contentDir: 'website/wiki/content/docs',
};

const getContentUrl = createGetUrl(docsContentRoute);

export function getPageMarkdownUrl(page: { slugs: string[]; locale?: string }) {
  const segments = [...page.slugs, 'content.md'];

  return { segments, url: getContentUrl(segments, page.locale) };
}
