# Wordsmith Wiki

The user guides for Wordsmith Script, Manuscript and Book, and the pages about the project as a whole, published at https://wordsmithand.ink/wiki/.

Built with [Fumadocs](https://fumadocs.dev) on Next.js and exported as static files. It's its own project, separate from the main site's plain HTML, and shares only the domain and the fonts.

## Two kinds of page

Pages are MDX (Markdown with a few components) in `content/docs/`:

| Folder | Sidebar tab | Who writes it |
| --- | --- | --- |
| `index.mdx` | The wiki's home page, shown first in the Wordsmith apps tab as "Getting started" (`start/meta.json` lists it as `../index`) | Written here |
| `start/` | The Wordsmith apps tab: the apps and how they fit together, installing, files, moving between apps, help, questions, privacy | Written here |
| `script/`, `manuscript/`, `book/` | One tab per app: the app's user guide | Built by `npm run guide` from the guide in the app's repository. Never edited |

### An app's pages: built from the app's guide

Each app keeps its user guide in its own repository, as Markdown in `docs/guide/`. That guide is the source ([project decision 0005](../../project/decisions/0005-one-guide-per-app.md)). `npm run guide` (`scripts/guide.mjs`) reads it at one commit and writes the app's folder here:

- each guide page becomes a wiki page with the same file name (`views.md` is `views.mdx`; the guide's `README.md` is the section's first page, `index.mdx`);
- the page's first heading becomes its title, and the line after its link in the guide's `README.md`, when there is one, its description;
- a link to another guide page leads to that wiki page, and a link to any other file of the app's repository becomes a full link to that file at the commit;
- a picture the page shows is taken from the app's repository (its screenshots are in `docs/images/`), scaled to 1600 pixels wide and written as WebP into the section's `images/` folder;
- the section's `meta.json` lists the pages in the order of the guide's `README.md`;
- text that MDX would read as code (`{`, `<`, a line that starts with `import` or `export`) is written so it shows as text. Code spans and code blocks are never changed.

The commit is recorded in `guides.lock.json`, with every file the tool wrote, and each page says under its text which guide and commit it came from. Its "Edit on GitHub" link opens the guide page in the app's repository.

```sh
npm run guide                          # every app, from the head of its main branch on GitHub
npm run guide -- --app script          # one app
npm run guide -- --app book --ref v1.0.0    # at a branch, a tag or a full commit id
npm run guide:check                    # the folders are what the recorded commits give, and no link between pages is broken
npm run guide:behind                   # has an app's guide on main changed since the recorded commit?
npm test                               # the tool's own tests
```

The tool reads the apps' repositories with git and needs no token: a checkout beside this repository when that checkout already has the commit, a small temporary fetch from GitHub otherwise. It takes what is published on GitHub, never a working tree, so a recorded commit is one everybody can read. It prints what it wrote and anything a person should look at, such as a guide link to a file that does not exist: that is fixed in the guide.

The same tool carries the screenshots the main site shows, into `website/assets/img/`: the ones named under `screenshots` in `website/data/apps/<app>.json`.

To change what an app's page says: change the guide in the app's repository and land it there, then run `npm run guide` here and land what it writes. If the wiki should say something an app's guide does not, open an issue in the app's repository for the guide page; do not write the page here.

### The project's pages: written here

- Each page starts with frontmatter: `title`, a one-line `description`, and optionally `icon` (a [Lucide](https://lucide.dev/icons) icon name) and `navTitle` (a different label for the sidebar; the home page uses it to show as "Getting started").
- Each folder's `meta.json` sets the page order (`pages`) and, for the tabs, `"root": true`.
- Link to other pages by their file: `[Views](../script/views.mdx)` or `<Card title="Views" href="../script/views.mdx" />`. `npm run guide:check` fails on a link to a page or a heading that is not there. An app's pages take their names from the app's guide, so a link into one can break when the guide changes.
- Give a page or folder an app's icon with `icon: brand:wordsmith-script` (or `-manuscript`, `-book`, `-and-ink`).
- Components you can use without an import: `Callout`, `Cards`/`Card`, `Steps`/`Step`, `Tabs`/`Tab`, `Accordions`/`Accordion`, `Files`/`Folder`/`File`, `Kbd` (`<Kbd>Ctrl</Kbd>+<Kbd>S</Kbd>`), `AppIcon` (`<AppIcon app="wordsmith-book" />`), `Wordmark` and `Status` (`<Status value="available|in-progress|planned" />`). They're registered in `components/mdx.tsx`.
- An app's version and downloads are never typed into a page. `<AppRelease app="script" />` shows the app's latest release (or a link to its releases page before it has one) and `<Downloads app="book" />` its downloads for each system. Both read `website/data/` (`lib/releases.mjs`), the files the main site reads, so a page follows an app's release without an edit ([project decision 0006](../../project/decisions/0006-the-site-reads-the-apps-releases.md)).
- Don't put `<Status>` or other components inside a heading: the page fails with "Status is not defined". Put it on the line under the heading.
- Write for writers, in plain, short sentences. Only describe what an app does today, and mark the rest as planned. The rules are in the repository's `AGENTS.md`.
- These pages are about the project as a whole. What one app does belongs in that app's guide.

## Brand

The wiki follows `brand/suite/BRAND_GUIDE.md`:

- **Logos and icons** are the kit's own files, copied unchanged into `public/brand/` (same folder names as `brand/`) by `npm run brand`. Never edit the copies. If the kit changes, run `npm run brand` again and commit the result. `npm run brand:check` fails if a copy is missing or out of date, and it runs on every pull request and push. To use another kit file, add it to `scripts/brand.mjs`. The same script makes and checks the main site's copies in `website/assets/brand/`, writes `brand/apps.json` (what each app's repository carries from the kit), and writes or checks an app's copies in a checkout beside this repository: `npm run brand -- --app book`, `npm run brand:check -- --app book`. Route F of the [project map](../../project/README.md#route-f) has the steps.
- **Colors** are the kit's tokens, set in `app/global.css`: ink, paper and Margin Blue everywhere, and each app's own color (Brad Brass, Card Red, Ribbon Green) in its own section only, used sparingly: the sidebar's current page and the section switcher.
- **Each app's home page** is titled with its wordmark, and each section uses the app's favicon.
- **Fonts** (Courier Prime for headings, Inter for text) are the main site's self-hosted files in `/assets/fonts/`.

## Running it

Needs Node.js 22 or later.

```sh
cd website/wiki
npm ci
npm run dev          # http://localhost:3000/wiki/ (without the fonts: they come from the main site)
npm run brand:check  # the wiki's and the main site's brand copies match brand/
npm test             # the tools' own tests
npm run guide:check  # each app's section is what the app's guide gives at its recorded commit
npm run lint
npm run types:check
npm run build        # static export into out/, the same as the deploy
```

The checks workflow (`.github/workflows/checks.yml`) runs `npm ci`, `npm run brand:check`, `npm test`, `npm run guide:check`, `npm run lint`, `npm run types:check` and `npm run build` on every pull request and every push to `main`. `npm run guide:behind` has its own workflow (`.github/workflows/guides.yml`), every day: it is red while an app's guide has changed since the wiki was built from it. The deploy (`.github/workflows/pages.yml`) runs the same checks and publishes `out/` at `/wiki/` next to the main site. Run them before you push all the same: a failed check after a push to `main` means the site was not updated.

### Preview with the main site

The wiki takes its fonts from the main site, so it only looks as deployed when both are served together. Put the site together the way the deploy does, in a folder outside the repository, and serve that. From the repository root, after `npm run build`:

```sh
site="$(mktemp -d)"
rsync -a --exclude /wiki --exclude /tools --exclude /data --exclude /README.md website/ "$site"/
cp -R website/wiki/out "$site"/wiki
python3 website/tools/serve.py 8000 "$site"   # http://localhost:8000/wiki/
```

This is a built copy: build and copy again to see a change. Use `npm run dev` while writing.

`npm run dev` writes an `AGENTS.md` into this folder: Next.js generates it, with a note for coding agents about its own documentation. Git ignores it. The rules for this folder are in the repository's `AGENTS.md`.

`npm run dev` answers `http://localhost:3000` as it is. If you reach the dev server under another host name (a proxy on your own machine), Next.js wants that name allowed. Put it in an untracked `.env.local` in this folder, as `WIKI_DEV_ORIGINS=<host>` (several: comma-separated), never in `next.config.mjs`: a host name of one machine does not belong in a public repository.
