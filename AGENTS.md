# AGENTS.md

Guidance for anyone, human or agent, changing this repository.

## What this repository is

The pieces of Wordsmith that belong to the project as a whole. The apps (Wordsmith Script, Wordsmith Manuscript, Wordsmith Book) and their shared base (`open-source-core`) live in their own repositories under `jamescjfoundation`; never copy their code here. Each top-level folder is its own small project with its own tooling:

| Folder | Stack | Owns |
| --- | --- | --- |
| `project/` | Markdown, one Python 3 script, no dependencies | The project map: every Wordsmith repository, how they depend on each other, the route for each kind of change, and the project-wide decisions; and `carry.py`, which writes and checks the text the repositories carry word for word |
| `brand/` | SVG, PNG, ICO, JSON tokens, PDFs, Python 3 build scripts | The brand kit: the source of every logo, icon and brand color |
| `website/` | Plain HTML/CSS/JS, a Python 3 page generator, no dependencies | The public site, [wordsmithand.ink](https://wordsmithand.ink/) |
| `website/wiki/` | Fumadocs (Next.js, MDX), static export | The wiki: user guides for the apps, at `/wiki/` |
| `launcher/` | Rust (planned) | Wordsmith Launcher, a desktop app. Not started |
| `.github/workflows/` | GitHub Actions | `pages.yml` (deploys the website and the wiki) and `carried.yml` (checks the carried text) |

Keep a change inside one folder where you can. A change that spans folders (for example, launcher status on the website) says so in its commit message.

## Start with the map

**[`project/README.md`](project/README.md) is the project map.** Read it when a task touches another repository, or when you are not sure where a change belongs. It lists the five repositories and two forks and gives the steps for each route: a wiki page for an app (Route D), website text (Route E), a brand change that must reach the apps (Route F), screenshots (Route G), a fix that belongs in `open-source-core` (Route A).

The map's [Project rules](project/README.md#project-rules) hold in every Wordsmith repository, this one included: how changes land, what is public, naming, licensing, privacy, the product names and the writing style. They are not repeated here. Two of them are broken most often in this repository:

- **The Foundation's name** is always "The James C. J. Foundation", never a shorter form.
- **Say only what exists.** The website and the wiki describe what an app does today. Check the app's repository (code, `CHANGELOG.md`, releases page) before you write a claim, and mark planned things as planned.

The block below is carried word for word from `open-source-core` and is not edited here ([`project/`](#project) says how it is updated).

<!-- BEGIN open-source-core: public -->
<!-- Owned by open-source-core (template/AGENTS.md). Change it there, never in a copy: `cargo xtask sync` rewrites the copies. -->
## What is public

This repository is public, history included, forever
([core decision 0012](https://github.com/jamescjfoundation/open-source-core/blob/main/docs/decisions/0012-working-in-the-open.md)).
Before you write a commit, branch name, issue, pull request or comment, check it holds none of:

- anyone's name, email, account names, or details of their machine (local paths such as a home
  folder, user names, host names, IP addresses);
- what the user told you in conversation, quoted or summarised; write the reason for a change as
  its own argument;
- an open security problem (follow `SECURITY.md`: keep it in `.private/` and tell the user);
- secrets, or files from a real machine (preferences, recovery, auto-save, backups, logs,
  screenshots of a desktop);
- anyone's private writing, even as test data. Fixtures are public-domain or written for the test.

Commit with a GitHub no-reply address or a foundation bot identity. Where a repository has
`cargo xtask`, `cargo xtask privacy` checks its files and every commit. Never push with `--all`
or `--mirror`.
<!-- END open-source-core: public -->

Where the block and this repository differ **today**:

- There is no `SECURITY.md` here yet. For a security problem, follow [Route H](project/README.md#route-h) in the map: keep it in `.private/` and tell the user.
- There is no `cargo xtask` here, so no tool checks files or commits for personal details. Read your own diff and commit message before you push, and check the author address: `git log -1 --format=%ae` must be a GitHub no-reply address.

## project/

- `project/README.md` is the map and `project/decisions/` holds the project-wide decisions, numbered from 0001. A new route gets the next free letter and an `<a id="route-x">` anchor; a new decision gets a row in `project/decisions/README.md`. `project/` is not part of the website and is never published with it.
- Some text is carried word for word in several repositories, between a `BEGIN` and an `END` marker line. The block marked in `project/README.md` is carried in each app's `AGENTS.md`; this file carries the `public` block above from open-source-core. A copy is never edited: change the owner's text, then run `python3 project/carry.py --write` with the repositories side by side. It changes files and commits nothing. [Route N](project/README.md#route-n) has the steps.
- `python3 project/carry.py` with no flag checks without writing. It reads the sibling folders where they exist; `--remote` reads what is published on GitHub.
- Check before pushing: `python3 project/test_carry.py` passes; every link and anchor you touched resolves; and after a change to a carried block, `python3 project/carry.py` passes against the sibling folders.

## brand/

`brand/` is the source of every logo, icon and brand color. A brand file is never edited, recolored or redrawn anywhere else, and not by hand here either. Read `brand/suite/BRAND_GUIDE.md` before any visual work.

- **Generated files** (logos, icons, lockups, palettes, the `production/` sets, the Brand Guidelines and Product Assets PDFs) come from `brand/source/build.py`. To change one, edit the script in `brand/source/`, run `python3 brand/source/build.py` to see what changes, then run it again with `--write` (add `--pdf` for the PDFs). `brand/README.md` has the setup. The fonts must come from `brand/source/fetch_fonts.py`, because other versions change the outlines.
- **Hand-written files** (the READMEs, `suite/BRAND_GUIDE.md`, each brand's `tokens.json` in the kit, `suite/wordsmith-suite-overview.png`, the Introduction PDF) are edited directly and kept in step with the generated files.
- Never commit `brand/build/`, `brand/source/fonts/` or `brand/source/node_modules/` (Git ignores them).
- Use the `-ink` versions on light backgrounds and the `-paper` versions on dark backgrounds.

The copies of kit files, and what keeps each in step:

| Copy | Made by | Checked by |
| --- | --- | --- |
| `website/wiki/public/brand/` | `npm run brand` in `website/wiki` | `npm run brand:check`, which the deploy also runs |
| `website/assets/brand/` and `website/favicon.svg` | Hand: copied from the kit's `logo/`, `lockups/` and `app-icon/` folders, some renamed (`app-icon/icon-512.png` is `wordsmith-and-ink-icon-512.png` there) | Nothing |
| Each app's `assets/brand/`, in the app's repository | Hand: copied from `brand/wordsmith-<app>/production/` and `app-icon/`, unchanged | Nothing |

- `website/assets/brand/og-image.png` (the picture in link previews) is not a kit file, and no script here makes it.
- An app owns two kinds of file in its own `assets/brand/`: its interface theme `tokens.json`, which is in the core's token format and is not a copy of the kit's `tokens.json`, and the files it derives from the kit with its own tool. [Route F](project/README.md#route-f) names them and has the steps for a change that must reach the copies.
- Nothing in `brand/` runs on GitHub, and a change under `brand/` alone starts no workflow. After a rebuild, update the copies in the same piece of work, or the next website deploy fails on `brand:check`.

## website/

- Pages are generated. The shared header, footer and all page text are in `website/tools/build.py`. Edit that, run `python3 website/tools/build.py` from the repository root, and commit the regenerated `.html` files with it. Never hand-edit the `.html` pages; the next build overwrites them.
- Styles: `website/assets/css/site.css` (brand color tokens; the dark theme follows the system). JS: `website/assets/js/site.js`; the site must work with JS off.
- **No third-party requests.** No CDN, font service, analytics or embed: the site promises this to its visitors. The fonts are served from `website/assets/fonts/`, with their license files beside them.
- Links between pages stay relative and leave off `.html` (`about`, not `about.html`): GitHub Pages serves `/about` from `about.html`, and old `.html` links still work. `build.py` writes them that way; keep new links in the same form, in this repository's other files too. The home page link is `./`. The site is served at `https://wordsmithand.ink/`; the only absolute URLs are the canonical, `og:url` and `og:image` tags, built from `SITE` in `build.py`. The 404 page is the exception: `build.py` makes its local links start at `/`, because Pages shows it at any missing address, including ones inside folders.
- Preview: `python3 website/tools/serve.py`, then http://localhost:8000 (a port number as its argument changes the port). Plain `python3 -m http.server` cannot follow links without `.html`.
- Deploy: `.github/workflows/pages.yml` runs on every push to `main` that touches `website/`. It builds the wiki, then publishes `website/` with the wiki's static export in place of `website/wiki/`, so the wiki's source is never published. Everything else under `website/` is published as it is, `tools/` and `README.md` included: put nothing there that should not be public. Pages uses the "GitHub Actions" source, with the custom domain `wordsmithand.ink` set in the repository's Pages settings.
- Check before pushing: `python3 website/tools/build.py` leaves `git status` showing only the pages you meant to change; no broken relative links or missing assets; images have `alt` text; the page reads well at phone width and in dark mode.

## website/wiki/

- A separate project from the main site: Fumadocs on Next.js, exported as static files with `basePath: '/wiki'`, published at `https://wordsmithand.ink/wiki/` by the same Pages workflow (one repository has one Pages site). `website/wiki/README.md` has the commands.
- Pages are MDX in `website/wiki/content/docs/`: `start/` (the shared "Wordsmith apps" tab, which also holds the home page) and one folder per app (`script/`, `manuscript/`, `book/`), each a sidebar tab (`root: true` in its `meta.json`). `meta.json` sets the page order.
- Its logos, app icons and favicons are the copies in `website/wiki/public/brand/` (see [brand/](#brand)). Never edit them. Each app's section uses that app's color only for small marks; links stay Margin Blue.
- The fonts come from the main site's `/assets/fonts/`, so `npm run dev` shows the wiki without them. To see it as deployed, build it and serve it with the main site; `website/wiki/README.md` has the steps.
- Content rules: write for writers, document only what the app does today, and check claims against the app's repository (code, `CHANGELOG.md`, `docs/guide/`). Mark anything not built with `<Status value="planned" />` or `"in-progress"`. Never use an app repository's `.private/` notes or reviews as content.
- Check before pushing: `npm run brand:check`, `npm run lint` and `npm run build` in `website/wiki` all pass, and every page and internal link you touched loads.

## launcher/

Not started. When it is:

- A Rust crate (or Cargo workspace) rooted at `launcher/`, so `cargo` commands run from there: `cargo fmt --check`, `cargo clippy --all-targets -- -D warnings`, `cargo test`.
- Match the apps' choices where it makes sense (egui for the interface, `open-source-core` if it fits) so the suite looks and behaves as one.
- Downloads come only from the project's official GitHub releases and are verified before anything runs. Update checks can be turned off. No accounts, no telemetry.
- Targets macOS, Windows and Linux.
- Add a `launcher.yml` workflow scoped to `paths: ["launcher/**"]` when there is code to check.
- Keep the website's launcher page (`website/launcher.html`, written by `build.py`) in step with what the launcher actually does.

## Before you push

Run the checks for each folder you changed; they are the "Check before pushing" line of its section above. What runs on GitHub, and what does not:

| Check | Where it runs |
| --- | --- |
| `python3 project/test_carry.py` and `python3 project/carry.py --check --remote` | `carried.yml`: on a push to `main` or a pull request that touches `project/README.md`, `project/carry.py`, `project/test_carry.py`, `AGENTS.md` or the workflow; weekly; and by hand. It is red while a published copy is behind its source |
| `npm run brand:check` and `npm run build` in `website/wiki` | `pages.yml`: on a push to `main` that touches `website/`, as part of the deploy. A failure there means the site was not updated |
| `npm run lint` and `npm run types:check` in `website/wiki` | Locally only |
| `python3 website/tools/build.py` matches the committed pages | Locally only |
| `python3 brand/source/build.py` matches the committed kit | Locally only |

A pull request gets no check from `pages.yml`, and nothing checks a change under `brand/` alone. After a push that touches `website/`, watch the "Deploy website and wiki to GitHub Pages" run and open the live page.

## Git

- `main` is the default branch and deploys the website. A change may be pushed straight to `main` once the checks for its folder pass; a pull request is optional and its author merges it ([decision 0002](project/decisions/0002-how-changes-land-and-who-releases.md)).
- Working notes, reviews and anything private go in `.private/`, which Git ignores. Never commit them.
- Keep commits focused, with a short imperative subject.
- Commit the generated website pages with the change that regenerates them. Commit no other build output: not `out/`, `.next/`, `node_modules/`, `target/` or editor files.
