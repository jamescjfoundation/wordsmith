import type { Metadata } from 'next';
import { Provider } from '@/components/provider';
import { appName, siteUrl } from '@/lib/shared';
import { brandUrl } from '@/lib/brand';
import './global.css';

export const metadata: Metadata = {
  metadataBase: new URL(`${siteUrl}/wiki/`),
  title: { default: appName, template: `%s · ${appName}` },
  description: 'Guides for Wordsmith Script, Manuscript and Book: free, open-source writing apps from The James C. J. Foundation.',
  icons: { icon: brandUrl.favicon('wordsmith-and-ink') },
  openGraph: { siteName: appName, images: `${siteUrl}/assets/brand/og-image.png` },
};

export default function Layout({ children }: LayoutProps<'/'>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className="flex flex-col min-h-screen">
        <Provider>{children}</Provider>
      </body>
    </html>
  );
}
