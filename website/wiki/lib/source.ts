import { createElement } from 'react';
import { llms, loader, type LoaderPlugin } from 'fumadocs-core/source';
import { lucideIconsPlugin } from 'fumadocs-core/source/lucide-icons';
import { docsRoute } from './shared';
import { AppIcon, type Brand } from './brand';
import { defineDocs } from 'fumadocs-mdx/macro';
import { metaSchema, pageSchema } from 'fumadocs-core/source/schema';

const docs = defineDocs({
  dir: 'content/docs',
  docs: {
    // navTitle: a shorter or different label for the page in the sidebar; the page keeps its title
    schema: pageSchema.extend({ navTitle: pageSchema.shape.title.optional() }),
    postprocess: {
      includeProcessedMarkdown: true,
    },
  },
  meta: {
    schema: metaSchema,
  },
});

/* `icon: brand:wordsmith-script` (or -manuscript, -book, -and-ink) shows the brand kit's app icon */
function brandIconsPlugin(): LoaderPlugin {
  function replace<T extends { icon?: unknown }>(node: T): T {
    if (typeof node.icon === 'string' && node.icon.startsWith('brand:')) {
      node.icon = createElement(AppIcon, { app: node.icon.slice('brand:'.length) as Brand, size: 16 });
    }
    return node;
  }
  return { name: 'wordsmith:brand-icons', transformPageTree: { file: replace, folder: replace } };
}

/* `navTitle` in a page's frontmatter replaces its title in the sidebar */
function navTitlePlugin(): LoaderPlugin {
  return {
    name: 'wordsmith:nav-title',
    transformPageTree: {
      file(node, filePath) {
        const file = filePath ? this.storage.read(filePath) : undefined;
        const navTitle = file?.format === 'page' ? (file.data as { navTitle?: string }).navTitle : undefined;
        if (navTitle) node.name = navTitle;
        return node;
      },
    },
  };
}

// See https://fumadocs.dev/docs/headless/source-api
export const source = loader({
  baseUrl: docsRoute,
  source: docs.toFumadocsSource(),
  // `icon` in frontmatter and meta.json: "brand:<app>" for an app icon, or a Lucide icon name such as "Compass"
  plugins: [navTitlePlugin(), brandIconsPlugin(), lucideIconsPlugin()],
});

export const docsLlms = llms(source, {
  renderPage: async (page) => `# ${page.data.title} (${page.url})

${await page.data.getText('processed')}`,
});
