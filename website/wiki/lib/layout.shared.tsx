import type { BaseLayoutProps } from 'fumadocs-ui/layouts/shared';
import { gitConfig, siteUrl } from './shared';

/* Brand files are the main site's own (website/assets/brand), served from the site root,
   so the wiki uses them without keeping copies. Plain <img>: next/image would add the /wiki base path. */
/* eslint-disable @next/next/no-img-element */
function Logo() {
  return (
    <span className="ws-logo">
      <img className="ws-logo-ink" src="/assets/brand/wordsmith-and-ink-wordmark-ink.svg" alt="Wordsmith &amp; Ink" />
      <img className="ws-logo-paper" src="/assets/brand/wordsmith-and-ink-wordmark-paper.svg" alt="" aria-hidden="true" />
      <span className="ws-logo-label">Wiki</span>
    </span>
  );
}

export function baseOptions(): BaseLayoutProps {
  return {
    nav: {
      title: <Logo />,
      url: '/',
    },
    links: [
      { text: 'Website', url: siteUrl, external: true },
    ],
    githubUrl: `https://github.com/${gitConfig.user}`,
  };
}
