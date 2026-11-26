/* Which pages come from an app's own guide, and at which commit. scripts/guide.mjs writes
   guides.lock.json when it builds an app's section from the guide in the app's repository. */
import lock from '@/guides.lock.json';
import { apps } from './brand';

const docs = 'website/wiki/content/docs/';

export type GuideSource = {
  /** e.g. "Wordsmith Script" */
  app: string;
  /** the commit the page was built from, shortened */
  commit: string;
  /** the day that commit was made */
  date: string;
  /** the guide page in the app's repository, at that commit */
  sourceUrl: string;
  /** where the guide page is edited */
  editUrl: string;
};

/** The guide page a wiki page was built from, or undefined for a page written in this repository. */
export function guideSource(pagePath: string): GuideSource | undefined {
  const file = docs + pagePath;
  for (const [slug, entry] of Object.entries(lock.apps)) {
    const page = entry.pages.find((one) => one.file === file);
    if (!page) continue;
    const name = apps[`wordsmith-${slug}` as keyof typeof apps]?.name ?? slug;
    const repository = `https://github.com/${entry.repository}`;
    return {
      app: name,
      commit: entry.commit.slice(0, 7),
      date: entry.date,
      sourceUrl: `${repository}/blob/${entry.commit}/${page.source}`,
      editUrl: `${repository}/edit/main/${page.source}`,
    };
  }
  return undefined;
}
