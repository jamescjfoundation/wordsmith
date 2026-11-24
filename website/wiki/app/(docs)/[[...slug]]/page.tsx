import { source } from '@/lib/source';
import {
  DocsBody,
  DocsDescription,
  DocsPage,
  DocsTitle,
  EditOnGitHub,
  MarkdownCopyButton,
  ViewOptionsPopover,
} from 'fumadocs-ui/layouts/docs/page';
import { notFound } from 'next/navigation';
import { getMDXComponents } from '@/components/mdx';
import type { Metadata } from 'next';
import { createRelativeLink } from 'fumadocs-ui/mdx';
import { Card } from 'fumadocs-ui/components/card';
import { getPageMarkdownUrl, gitConfig } from '@/lib/shared';
import { appForSection, apps, brandUrl, Wordmark } from '@/lib/brand';

export default async function Page(props: PageProps<'/[[...slug]]'>) {
  const params = await props.params;
  const page = source.getPage(params.slug);
  if (!page) notFound();

  const MDX = page.data.body;
  const markdownUrl = getPageMarkdownUrl(page).url;
  const filePath = `${gitConfig.user}/${gitConfig.repo}/blob/${gitConfig.branch}/${gitConfig.contentDir}/${encodeURI(page.path)}`;
  const githubUrl = `https://github.com/${filePath}`;
  const editUrl = `https://github.com/${filePath.replace('/blob/', '/edit/')}`;
  // an app's section takes that app's color (see .ws-app-* in global.css), and its home page its wordmark
  const app = appForSection(page.slugs[0]);
  const isAppHome = app !== undefined && page.slugs.length === 1;

  return (
    <DocsPage toc={page.data.toc} full={page.data.full}>
      {app && <span data-ws-app={app} hidden />}
      {isAppHome ? (
        <DocsTitle className="ws-app-title">
          <Wordmark brand={app} label={apps[app].name} />
        </DocsTitle>
      ) : (
        <DocsTitle>{page.data.title}</DocsTitle>
      )}
      <DocsDescription className="mb-0">{page.data.description}</DocsDescription>
      <div className="flex flex-row gap-2 items-center border-b pb-6">
        <MarkdownCopyButton markdownUrl={markdownUrl} />
        <ViewOptionsPopover markdownUrl={markdownUrl} githubUrl={githubUrl} />
      </div>
      <DocsBody>
        <MDX
          components={getMDXComponents({
            // link to other pages with relative file paths, e.g. [Views](./views.mdx) or <Card href="./views.mdx">
            a: createRelativeLink(source, page),
            Card: createRelativeLink(source, page, Card as never) as unknown as typeof Card,
          })}
        />
      </DocsBody>
      <EditOnGitHub href={editUrl} />
    </DocsPage>
  );
}

export async function generateStaticParams() {
  return source.generateParams();
}

export async function generateMetadata(props: PageProps<'/[[...slug]]'>): Promise<Metadata> {
  const params = await props.params;
  const page = source.getPage(params.slug);
  if (!page) notFound();

  const app = appForSection(page.slugs[0]);
  return {
    title: page.data.title,
    description: page.data.description,
    icons: { icon: brandUrl.favicon(app ?? 'wordsmith-and-ink') },
  };
}
