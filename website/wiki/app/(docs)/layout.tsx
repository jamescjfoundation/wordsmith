import Link from 'next/link';
import { source } from '@/lib/source';
import { DocsLayout } from 'fumadocs-ui/layouts/docs';
import { getLayoutTabs } from 'fumadocs-ui/layouts/shared';
import { SidebarTabsDropdown } from 'fumadocs-ui/components/sidebar/tabs/dropdown';
import { baseOptions } from '@/lib/layout.shared';
import { AppIcon, appForSection, apps, programForSection, Wordmark } from '@/lib/brand';

export default function Layout({ children }: LayoutProps<'/'>) {
  const tree = source.getPageTree();

  // The switcher lists only the apps, each as its wordmark, and the launcher, which has no
  // wordmark yet, by its name. The shared pages (start/) are a tab too, so their sidebar shows
  // only them, but they're reached from "Getting started" at the bottom of the sidebar instead.
  const appTabs = getLayoutTabs(tree, {
    transform(tab) {
      const section = tab.url.split('/').filter(Boolean)[0];
      const app = appForSection(section);
      const program = programForSection(section);
      if (program) {
        return { ...tab, icon: <AppIcon app={program.brand} size={20} />, title: <span className="ws-tab-placeholder">{program.name}</span> };
      }
      if (!app) return null;
      return {
        ...tab,
        icon: undefined,
        title: <Wordmark brand={app} label={apps[app].name} className={`ws-tab-wordmark ws-tab-${app}`} />,
      };
    },
  });

  return (
    <DocsLayout
      tree={tree}
      {...baseOptions()}
      tabs={false}
      sidebar={{
        banner: <SidebarTabsDropdown options={appTabs} placeholder={<span className="ws-tab-placeholder">Choose an app</span>} />,
        footer: (
          <Link href="/" className="ws-start-link">
            <AppIcon app="wordsmith-and-ink" size={20} />
            Getting started
          </Link>
        ),
      }}
    >
      {children}
    </DocsLayout>
  );
}
