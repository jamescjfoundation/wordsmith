# AGENTS.md

Guidance for anyone, human or agent, changing this repository.

## What this repository is

A monorepo for the shared, project-wide pieces of Wordsmith. The apps (Script, Manuscript, Book) and their shared base (`open-source-core`) live in their own repositories under `jamescjfoundation`; don't copy their code here. Each top-level folder is an independent project with its own tooling:

| Folder | Stack | Owns |
| --- | --- | --- |
| `project/` | Markdown, one Python 3 script, no dependencies | The project map: every Wordsmith repository, how they depend on each other, the route for each kind of change, and the project-wide decisions; and `carry.py`, which writes and checks the text the repositories carry word for word |
| `brand/` | SVG, PNG, ICO, JSON tokens, PDFs | The brand kit: logos, icons, palettes, guidelines |
| `website/` | Plain HTML/CSS/JS, a Python 3 page generator, no dependencies | The public site |
| `website/wiki/` | Fumadocs (Next.js, MDX), static export | The wiki: user guides for the apps, at `/wiki/` |
| `launcher/` | Rust (planned) | Wordsmith Launcher desktop app |
| `.github/workflows/` | GitHub Actions | CI and deploys, one workflow per folder |

**Start with [`project/README.md`](project/README.md)** when a task touches another repository, or when you are not sure where a change belongs. It lists the five repositories and two forks, and gives the steps for each route: a wiki page for an app, a brand change that must reach the apps, website text after an app release, a fix that belongs in `open-source-core`. This repository owns that map and the rules in `project/decisions/`; the app repositories carry a copy of its top block in their `AGENTS.md`. Change the block here, never in a copy, and carry it out with `project/carry.py` (see [project/](#project) below). `project/` is not part of the website and is never published with it.

Keep changes inside one folder where you can. A change that spans folders (for example, launcher status on the website) should say so in the commit message.

## Project-wide rules

These come from the project's public promises on the website. Don't break them.

- **Privacy:** no telemetry, analytics, accounts, trackers or third-party requests. The website self-hosts its fonts for this reason; no CDNs, Google Fonts or embeds. The only network request any app makes on its own is the update check with GitHub, and it can be turned off.
- **Licensing:** code is MIT OR Apache-2.0. Only add dependencies with compatible licenses, and credit them (README/NOTICE).
- **Names:** "Wordsmith", "Wordsmith & Ink", "Wordsmith Script", "Wordsmith Manuscript", "Wordsmith Book" are trademarks. Use them exactly as written. The launcher is "Wordsmith Launcher".
- **Brand assets:** `brand/` is the brand kit and the source for every logo, icon, color and font choice. Read `brand/suite/BRAND_GUIDE.md` before any visual work. Copies elsewhere (`website/assets/brand/`, `website/wiki/public/brand/`, the app repos) are taken from `brand/` unchanged. Never edit, recolor or redraw a brand file by hand. Logos, icons, palettes and the guideline PDFs change only through `brand/source/` and a rebuild.
- **The Foundation's name** is always "The James C. J. Foundation", never "The J. C. J. Foundation".
- **Writing style:** plain, short, friendly sentences for writers, not developers. No marketing superlatives. Don't claim a feature exists before it does; mark planned things as planned.

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

## project/

- `project/README.md` is the map and `project/decisions/` holds the project-wide decisions, numbered from 0001. A new route gets the next free letter and an `<a id="route-x">` anchor; a new decision gets a row in `project/decisions/README.md`.
- Some text is carried word for word in several repositories, between a `BEGIN` and an `END` marker line. The block marked in `project/README.md` is carried in each app's `AGENTS.md`; this file carries the block above from open-source-core. A copy is never edited: change the owner's text, then run `python3 project/carry.py --write` with the repositories side by side. It changes files and commits nothing. Route N in the map has the steps.
- `.github/workflows/carried.yml` runs `python3 project/carry.py --check --remote`, which compares every published copy with its source. It is red while a copy is behind.
- Check before committing: `python3 project/test_carry.py` passes; every link and anchor you touched resolves; and after a change to the block, `python3 project/carry.py` passes against the sibling folders.

## brand/

- Started from the kit in the Foundation's shared drive (`10. Open Source / 01. Wordsmith`), with folder names lowercased and hyphenated. Filenames stay as the kit names them. `brand/README.md` maps each folder to its drive folder and explains the build.
- Generated files (logos, icons, lockups, palettes, `production/` sets, the Brand Guidelines and Product Assets PDFs) come from `brand/source/build.py`. To change one, edit the script in `brand/source/`, run `python3 brand/source/build.py` to see what changes, then rerun it with `--write` (add `--pdf` for the PDFs). Nothing runs in CI. The fonts must come from `brand/source/fetch_fonts.py`, because other versions change the outlines.
- Hand-written files (READMEs, `suite/BRAND_GUIDE.md`, the apps' `tokens.json`, the Introduction PDF) are edited directly, and must be kept in step with the generated files.
- Never commit `brand/build/`, `brand/source/fonts/` or `brand/source/node_modules/`.
- Use the `-ink` versions on light backgrounds and `-paper` versions on dark backgrounds. Each app's `production/` folder is the ready-made set to copy into that app's repo.

## website/

- Pages are generated. The shared header, footer and all page text are in `website/tools/build.py`. Edit that, then run `python3 website/tools/build.py` from the repo root and commit the regenerated `.html` files with it. Don't hand-edit the `.html` pages; the next build overwrites them.
- Styles: `website/assets/css/site.css` (brand color tokens, dark theme follows the system). JS: `website/assets/js/site.js`; the site must work with JS off.
- Links between pages stay relative and leave off `.html` (`about`, not `about.html`): GitHub Pages serves `/about` from `about.html`, and old `.html` links still work. `build.py` writes them that way; keep new links in the same form. The home page link is `./`. It is served at `https://wordsmithand.ink/`; the only absolute URLs are the canonical, `og:url` and `og:image` tags, built from `SITE` in `build.py`. The 404 page is the exception: `build.py` makes its local links start at `/`, because Pages shows it at any missing address, including ones inside folders.
- Preview: `python3 website/tools/serve.py` then http://localhost:8000. Plain `python3 -m http.server` can't follow links without `.html`.
- Deploy: `.github/workflows/pages.yml` runs on every push to `main` that touches `website/`. It builds the wiki, then publishes `website/` with the wiki's static export in place of `website/wiki/`, so the wiki's source is never published. Pages is set to the "GitHub Actions" source, with the custom domain `wordsmithand.ink` set in the repository's Pages settings.
- Check before committing: every page builds, no broken relative links or missing assets, images have `alt` text, and the page reads well at phone width and in dark mode.

## website/wiki/

- A separate project from the main site: Fumadocs on Next.js, exported as static files with `basePath: '/wiki'`, published at `https://wordsmithand.ink/wiki/` by the same Pages workflow (one repository has one Pages site). `website/wiki/README.md` has the commands.
- Pages are MDX in `website/wiki/content/docs/`: `start/` (the shared "Wordsmith apps" tab, which also holds the home page) and one folder per app (`script/`, `manuscript/`, `book/`), each a sidebar tab (`root: true` in its `meta.json`). `meta.json` sets the page order.
- Its logos, app icons and favicons are copies of `brand/` files in `website/wiki/public/brand/`, made by `npm run brand` and checked by `npm run brand:check` (the deploy runs it). Never edit the copies. Each app's section uses that app's color only for small marks; links stay Margin Blue. The fonts come from the main site's `/assets/fonts/`, so the wiki only looks right when served with the main site (the deploy, or the local preview at `https://wordwiki.test`).
- Content rules: write for writers, document only what the app does today, and check claims against the app's repo (code, CHANGELOG, progress notes). Mark anything not built with `<Status value="planned" />` or `"in-progress"`. Never use an app repo's `.private/` notes or internal reviews as content.
- Check before committing: `npm run brand:check`, `npm run lint` and `npm run build` in `website/wiki` pass, and every page and internal link loads.

## launcher/

Not started. When it is:

- A Rust crate (or Cargo workspace) rooted at `launcher/`, so `cargo` commands run from there: `cargo fmt --check`, `cargo clippy --all-targets -- -D warnings`, `cargo test`.
- Match the apps' choices where it makes sense (egui for UI, `open-source-core` if it fits) so the suite looks and behaves as one.
- Downloads come only from the project's official GitHub releases and are verified before anything runs. Update checks can be turned off. No accounts, no telemetry.
- Targets macOS, Windows and Linux.
- Add a `launcher.yml` workflow scoped to `paths: ["launcher/**"]` when there is code to check.
- Keep `website/launcher.html` (via `build.py`) in step with what the launcher actually does.

## Git

- `main` is the default branch and deploys the website. A change may be pushed straight to `main` once the checks for its folder pass; a pull request is optional and its author merges it (`project/decisions/0002-how-changes-land-and-who-releases.md`).
- Working notes, reviews and anything private go in `.private/`, which Git ignores. Never commit them.
- Keep commits focused, with a short imperative subject.
- Don't commit build output other than the generated website pages, or `target/`, `node_modules/` or editor files.
