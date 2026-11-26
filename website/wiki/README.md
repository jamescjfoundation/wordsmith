# Wordsmith Wiki

User guides for Wordsmith Script, Manuscript and Book, published at https://wordsmithand.ink/wiki/.

Built with [Fumadocs](https://fumadocs.dev) on Next.js and exported as static files. It's its own project, separate from the main site's plain HTML, and shares only the domain and the fonts.

## Writing pages

Pages are MDX (Markdown with a few components) in `content/docs/`:

| Folder | Sidebar tab |
| --- | --- |
| `index.mdx` | The wiki's home page, shown first in the Wordsmith apps tab as "Getting started" (`start/meta.json` lists it as `../index`) |
| `start/` | The Wordsmith apps tab: the suite, installing, files, moving between apps, help, privacy |
| `script/`, `manuscript/`, `book/` | One tab per app |

- Each page starts with frontmatter: `title`, a one-line `description`, and optionally `icon` (a [Lucide](https://lucide.dev/icons) icon name) and `navTitle` (a different label for the sidebar; the home page uses it to show as "Getting started").
- Each folder's `meta.json` sets the page order (`pages`) and, for the tabs, `"root": true`.
- Link to other pages by their file: `[Views](./views.mdx)` or `<Card title="Views" href="./views.mdx" />`.
- Put pictures next to the pages (`script/images/…`) and link them relatively: `![The page view](./images/page-view.webp)`.
- Give a page or folder an app's icon with `icon: brand:wordsmith-script` (or `-manuscript`, `-book`, `-and-ink`).
- Components you can use without an import: `Callout`, `Cards`/`Card`, `Steps`/`Step`, `Tabs`/`Tab`, `Accordions`/`Accordion`, `Files`/`Folder`/`File`, `Kbd` (`<Kbd>Ctrl</Kbd>+<Kbd>S</Kbd>`), `AppIcon` (`<AppIcon app="wordsmith-book" />`), `Wordmark` and `Status` (`<Status value="available|in-progress|planned" />`). They're registered in `components/mdx.tsx`.
- Don't put `<Status>` or other components inside a heading: the page fails with "Status is not defined". Put it on the line under the heading.
- Write for writers, in plain, short sentences. Only describe what an app does today, and mark the rest as planned. The rules are in the repository's `AGENTS.md`.

## Brand

The wiki follows `brand/suite/BRAND_GUIDE.md`:

- **Logos and icons** are the kit's own files, copied unchanged into `public/brand/` (same folder names as `brand/`) by `npm run brand`. Never edit the copies. If the kit changes, run `npm run brand` again and commit the result. `npm run brand:check` fails if a copy is missing or out of date, and the deploy runs it. To use another kit file, add it to `scripts/brand.mjs`.
- **Colors** are the kit's tokens, set in `app/global.css`: ink, paper and Margin Blue everywhere, and each app's own color (Brad Brass, Card Red, Ribbon Green) in its own section only, used sparingly: the sidebar's current page and the section switcher.
- **Each app's home page** is titled with its wordmark, and each section uses the app's favicon.
- **Fonts** (Courier Prime for headings, Inter for text) are the main site's self-hosted files in `/assets/fonts/`.

## Running it

Needs Node.js 22 or later.

```sh
cd website/wiki
npm install
npm run dev          # http://localhost:3000/wiki/ (without the fonts: they come from the main site)
npm run brand:check  # the copies in public/brand/ match brand/
npm run lint
npm run types:check
npm run build        # static export into out/, the same as the deploy
```

The deploy (`.github/workflows/pages.yml`) runs `npm ci`, `npm run brand:check` and `npm run build`, and publishes `out/` at `/wiki/` next to the main site. `npm run lint` and `npm run types:check` run nowhere but on your machine, so run them before you push.

### Preview with the main site

The wiki takes its fonts from the main site, so it only looks as deployed when both are served together. Put the site together the way the deploy does, in a folder outside the repository, and serve that. From the repository root, after `npm run build`:

```sh
site="$(mktemp -d)"
rsync -a --exclude /wiki website/ "$site"/
cp -R website/wiki/out "$site"/wiki
python3 "$site"/tools/serve.py       # http://localhost:8000/wiki/
```

This is a built copy: build and copy again to see a change. Use `npm run dev` while writing.

`npm run dev` writes an `AGENTS.md` into this folder: Next.js generates it, with a note for coding agents about its own documentation. It is not tracked; leave it out of your commit.
