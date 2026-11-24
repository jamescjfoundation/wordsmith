import { source } from '@/lib/source';
import { DocsLayout } from 'fumadocs-ui/layouts/docs';
import { baseOptions } from '@/lib/layout.shared';
import { AppIcon, appForSection, apps, Wordmark } from '@/lib/brand';

export default function Layout({ children }: LayoutProps<'/'>) {
  return (
    <DocsLayout
      tree={source.getPageTree()}
      {...baseOptions()}
      // The tab switcher shows each app as its wordmark. The shared tab has no wordmark of its
      // own (the Wordsmith & Ink one is already in the header), so it shows its icon and name.
      tabs={{
        transform(tab) {
          const app = appForSection(tab.url.split('/').filter(Boolean)[0]);
          if (!app) return { ...tab, icon: <AppIcon app="wordsmith-and-ink" size={24} /> };
          return {
            ...tab,
            icon: undefined,
            title: <Wordmark brand={app} label={apps[app].name} className={`ws-tab-wordmark ws-tab-${app}`} />,
          };
        },
      }}
    >
      {children}
    </DocsLayout>
  );
}
