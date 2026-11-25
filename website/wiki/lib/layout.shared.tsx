import type { BaseLayoutProps } from 'fumadocs-ui/layouts/shared';
import { Globe } from 'lucide-react';
import { gitConfig, siteUrl } from './shared';
import { Wordmark } from './brand';

function Logo() {
  return (
    <span className="ws-logo">
      <Wordmark brand="wordsmith-and-ink" label="Wordsmith &amp; Ink" />
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
    // an icon link sits in the sidebar's footer, next to GitHub
    links: [
      { type: 'icon', text: 'Website', label: 'Wordsmith website', icon: <Globe />, url: siteUrl, external: true },
    ],
    githubUrl: `https://github.com/${gitConfig.user}`,
  };
}
