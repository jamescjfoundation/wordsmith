# AGENTS.md

Guidance for anyone, human or agent, changing this repository.

## What this repository is

The pieces of Wordsmith that belong to the project as a whole. The apps (Wordsmith Script, Wordsmith Manuscript, Wordsmith Book) and their shared base (`open-source-core`) live in their own repositories under `jamescjfoundation`; never copy their code here. Each top-level folder is its own small project with its own tooling:

| Folder | Stack | Owns |
| --- | --- | --- |
| `project/` | Markdown, three Python 3 scripts, no dependencies | The project map: every Wordsmith repository, how they depend on each other, the route for each kind of change, and the project-wide decisions; `carry.py`, which writes and checks the text the repositories carry word for word; `check_links.py`, which checks the links between this repository's Markdown files; and `privacy.py`, which looks for personal details and secrets in the files and the commits |
| `brand/` | SVG, PNG, ICO, JSON tokens, PDFs, Python 3 build scripts | The brand kit: the source of every logo, icon and brand color, and the list of what each app carries from it |
| `website/` | Plain HTML/CSS/JS, a Python 3 page generator and release reader, no dependencies | The public site, [wordsmithand.ink](https://wordsmithand.ink/), and the data files that say what each app is and where it stands |
| `website/wiki/` | Fumadocs (Next.js, MDX), static export, Node.js scripts | The wiki, at `/wiki/`: each app's user guide, built from the guide in the app's own repository, and the pages about the project as a whole |
| `launcher/` | Rust (planned) | Wordsmith Launcher, a desktop app. Not started |
| `.github/` | GitHub Actions, Markdown | `workflows/checks.yml` (every check, on each pull request and each push to `main`), `workflows/pages.yml` (runs the same checks, then deploys the website and the wiki: on a push, and every day when an app has published a release), `workflows/carried.yml` (compares the carried text with what the other repositories have published), `workflows/guides.yml` (compares each app's guide on `main` with the commit the wiki was built from), and the pull request template |

At the root: `LICENSES.md` says which license covers which folder, with the license texts beside it (`LICENSE-MIT`, `LICENSE-APACHE`, `LICENSE-CC-BY-4.0`; the brand terms are `brand/LICENSE.md`). `SECURITY.md`, `CONTRIBUTING.md` and `CODE_OF_CONDUCT.md` are for people arriving from outside; each carries text from `open-source-core` ([`project/`](#project) says how).

Keep a change inside one folder where you can. A change that spans folders (for example, launcher status on the website) says so in its commit message.

## Start with the map

**[`project/README.md`](project/README.md) is the project map.** Read it when a task touches another repository, or when you are not sure where a change belongs. It lists the five repositories and two forks and gives the steps for each route: a change users will see in an app and its guide (Route C), a wiki page (Route D), website text (Route E), a brand change that must reach the apps (Route F), screenshots (Route G), a fix that belongs in `open-source-core` (Route A).

The map's [Project rules](project/README.md#project-rules) hold in every Wordsmith repository, this one included: how changes land, what is public, naming, licensing, privacy, the product names and the writing style. They are not repeated here. Two of them are broken most often in this repository:

- **The Foundation's name** is always "The James C. J. Foundation", never a shorter form.
- **Say only what exists.** The website and the wiki describe what an app does today. Check the app's repository (code, `docs/guide/`, `CHANGELOG.md`, releases page) before you write a claim, and mark planned things as planned.

The block below is carried word for word from `open-source-core` and is not edited here ([`project/`](#project) says how it is updated).

<!-- BEGIN open-source-core: public -->
<!-- Owned by open-source-core (template/AGENTS.md). Change it there, never in a copy: its tooling rewrites the copies. -->
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

The Foundation's name is always written "The James C. J. Foundation", with its capital "The"
wherever it stands in a sentence, never in a shorter form.
<!-- END open-source-core: public -->

Where the block and this repository differ:

- There is no `cargo xtask` here. `python3 project/privacy.py` does the job of `cargo xtask privacy`: it reads every tracked text file for email addresses, home folders, private network addresses and host names, and things shaped like secrets, and it reads the author and committer address of every commit. The checks workflow runs it on every pull request and push. No hook runs it for you: run it before you push.
- A pattern cannot find a person's name, something said in a conversation or an open security problem. Read your own diff and commit message for those.
- In a fresh clone, set a GitHub no-reply address with `git config user.email` before the first commit.
- A line that must keep something the check finds (an example in a test) ends with the marker `privacy:allow`. Use it for made-up examples only, never to keep a real detail.

## project/

- `project/README.md` is the map and `project/decisions/` holds the project-wide decisions, numbered from 0001. A new route gets the next free letter and an `<a id="route-x">` anchor; a new decision gets a row in `project/decisions/README.md`. `project/` is not part of the website and is never published with it.
- Some text is carried word for word in several repositories, between a `BEGIN` and an `END` marker line. The block marked in `project/README.md` is carried in each app's `AGENTS.md`. This repository carries four pieces from open-source-core: the `public` block above, the `security` block in `SECURITY.md`, the `contributing` block in `CONTRIBUTING.md`, and the whole of `CODE_OF_CONDUCT.md`. A copy is never edited: change the owner's text, then run `python3 project/carry.py --write` with the repositories side by side. It changes files and commits nothing. [Route N](project/README.md#route-n) has the steps.
- The carried text is written for a repository with Cargo and releases. Where a sentence of it does not fit here, the file says so in its own part, outside the marker lines (`SECURITY.md`: "Where this repository differs"; `CONTRIBUTING.md`: "This repository's own rules"). Keep those parts true when the carried text changes.
- `python3 project/carry.py` with no flag checks without writing. It reads the sibling folders where they exist; `--remote` reads what is published on GitHub: each app's `main` and the core's newest release. `--write --remote` writes this repository's copies from that release, for when the core's sibling folder is ahead of it.
- `python3 project/check_links.py` checks every tracked Markdown file here: each link to a file in this repository names one that exists, and each `#anchor` names a heading or an `id` that exists. It makes no network request, so it does not check links to other sites or repositories, and it does not read the wiki's `.mdx` pages. In the apps, `cargo xtask docs` does this job from core v0.1.18.
- `python3 project/privacy.py` is described under [What is public](#what-is-public). Its rules follow the core's `template/xtask/src/privacy.rs`; keep the two in step when one gains a rule.
- Check before pushing: `python3 project/privacy.py` and `python3 project/check_links.py` pass; `python3 -m unittest discover -s project` passes when a tool changed (it runs `test_carry.py`, `test_check_links.py` and `test_privacy.py`); and after a change to a carried block, `python3 project/carry.py` passes against the sibling folders. Each route in the map ends with a "Held by:" line; keep it true when a check is added or a step changes.

## brand/

`brand/` is the source of every logo, icon and brand color. A brand file is never edited, recolored or redrawn anywhere else, and not by hand here either. Read `brand/suite/BRAND_GUIDE.md` before any visual work.

- **Generated files** (logos, icons, lockups, palettes, the `production/` sets, the Brand Guidelines and Product Assets PDFs) come from `brand/source/build.py`. To change one, edit the script in `brand/source/`, run `python3 brand/source/build.py` to see what changes, then run it again with `--write` (add `--pdf` for the PDFs). `brand/README.md` has the setup. The fonts must come from `brand/source/fetch_fonts.py`, because other versions change the outlines.
- **Hand-written files** (the READMEs, `suite/BRAND_GUIDE.md`, each brand's `tokens.json` in the kit, `suite/wordsmith-suite-overview.png`, the Introduction PDF) are edited directly and kept in step with the generated files.
- Never commit `brand/build/`, `brand/source/fonts/` or `brand/source/node_modules/` (Git ignores them).
- Use the `-ink` versions on light backgrounds and the `-paper` versions on dark backgrounds.

The copies of kit files, and what keeps each in step:

| Copy | Made by | Checked by |
| --- | --- | --- |
| `website/wiki/public/brand/` | `npm run brand` in `website/wiki` | `npm run brand:check`, which the checks workflow runs on every pull request and push |
| `website/assets/brand/` and `website/favicon.svg` | The same `npm run brand`: from the kit's `logo/`, `lockups/` and `app-icon/` folders into one flat folder, some renamed (`app-icon/icon-512.png` is `wordsmith-and-ink-icon-512.png` there) | The same `npm run brand:check` |
| Each app's `assets/brand/`, in the app's repository | `npm run brand -- --app <app>` in `website/wiki`, which writes the kit's files into the app's checkout beside this repository: the app's `production/` set and the icons it uses from `app-icon/`, with `kit.json`, the record of the kit commit they came from. The change is committed in the app | `npm run brand:check -- --app <app>` here, by hand. The check that fails in the app is the app's own, from `kit.json` and `brand/apps.json` ([Route F](project/README.md#route-f)) |

- One script makes and checks every copy: `website/wiki/scripts/brand.mjs`. It needs Node.js and nothing installed. To use another kit file on the website or in the wiki, add it to the script's list and run `npm run brand`; never copy one by hand. `brand:check` also fails on a file in either folder of copies that the script does not make.
- `brand/apps.json` is the list of what each app carries from the kit: every carried file with the kit file it comes from and its SHA-256, the files in the app's `assets/brand/` that are the app's own, the files the app derives from a kit file and the tool that makes each, and the seven palette colors. `npm run brand` writes it from the table `APPS` in the script and from the kit's files, and `brand:check` fails when it is stale. Never edit it. To have an app carry another kit file, change the app's entry in `APPS` and run `npm run brand`. `npm test` runs the tool's tests (`scripts/brand.test.mjs`).
- `website/assets/brand/og-image.png` (the picture in link previews) is not a kit file, and no script here makes it. It is the one file the check lets stay.
- The brand files are not open source, and their copies are under the same terms: [`brand/LICENSE.md`](brand/LICENSE.md). Keep it, `brand/README.md`, `brand/suite/BRAND_GUIDE.md` and the website's "Open source" page saying the same thing.
- The kit owns the seven palette colors and every logo and icon; an app owns its interface theme file, which is in the core's token format and is not a copy of the kit's `tokens.json`, and the files it derives from a kit file with its own tool ([project decision 0007](project/decisions/0007-brand-files-reach-the-apps-by-one-route.md)). The tool for an app never touches those, and never removes a file from an app. [Route F](project/README.md#route-f) has the steps for a change that must reach the copies.
- A change under `brand/` runs the checks workflow like any other change, and `brand:check` fails there while a copy is behind the kit. It starts no deploy, because the site publishes the copies, not `brand/`. After a rebuild, run `npm run brand` in the same piece of work; that change touches `website/` and deploys. Then each app takes its copies ([Route F](project/README.md#route-f)). The kit's own build (`python3 brand/source/build.py`) runs nowhere on GitHub.

## website/

- Pages are generated. The shared header, footer and all page text are in `website/tools/build.py`. Edit that, run `python3 website/tools/build.py` from the repository root, and commit the regenerated `.html` files with it. Never hand-edit the `.html` pages; the next build overwrites them, and `python3 website/tools/build.py --check` (run by the checks workflow) fails on a page that is not what the script writes.
- Styles: `website/assets/css/site.css` (brand color tokens; the dark theme follows the system). JS: `website/assets/js/site.js`; the site must work with JS off.
- **An app's state is never typed into a page** ([project decision 0006](project/decisions/0006-the-site-reads-the-apps-releases.md)). Two kinds of file hold it, and `build.py` and the wiki both read them:
  - `website/data/apps/<app>.json`, one small file per app: its name, its repository, what it is for, its platforms (named in `website/data/platforms.json`), its words for each state (`none`: no release; `preview`: a release before 1.0.0, or one marked a pre-release; `released`), and which of its screenshots the website shows. To change what a page says about an app's state, change the words there; `{version}` and `{date}` are filled in.
  - A releases file: each app's latest public release, with its version, date and files. `python3 website/tools/releases.py` reads it from GitHub. `website/data/releases.json` is the last known answer: the pages in the repository are built from it, so `build.py` never uses the network. Refresh it with `python3 website/tools/releases.py --write`, then run `build.py` and commit both; nothing depends on doing so.
- In `build.py`, use `chip(app)`, `state(app)`, `systems(app)` and `download(app)` for anything about a version, a state or a download. Do not write a version number, "no downloads yet" or a download link into the page text.
- The published site is built with fresh release data: every deploy runs `releases.py` first and builds the pages and the wiki from its answer, and a daily run of `pages.yml` deploys when an app has published a release since the last deploy. The file the site was built from is published as `releases.json`. `website/data/` itself is not published.
- The screenshots in `website/assets/img/` are drawn by the apps and carried here by `npm run guide` in `website/wiki` ([website/wiki/](#websitewiki)), never copied or edited by hand. To show another one, add its name to `screenshots` in the app's data file, run `npm run guide`, and use it in `build.py` with `shot(app, name, alt)`, which takes the picture's size from the tool's lock file.
- **No third-party requests.** No CDN, font service, analytics or embed: the site promises this to its visitors. The fonts are served from `website/assets/fonts/`, with their license files beside them.
- Links between pages stay relative and leave off `.html` (`about`, not `about.html`): GitHub Pages serves `/about` from `about.html`, and old `.html` links still work. `build.py` writes them that way; keep new links in the same form, in this repository's other files too. The home page link is `./`. The site is served at `https://wordsmithand.ink/`; the only absolute URLs are the canonical, `og:url` and `og:image` tags, built from `SITE` in `build.py`. The 404 page is the exception: `build.py` makes its local links start at `/`, because Pages shows it at any missing address, including ones inside folders.
- Preview: `python3 website/tools/serve.py`, then http://localhost:8000 (a port number as its argument changes the port, and a folder after the port serves that folder instead of `website/`). Plain `python3 -m http.server` cannot follow links without `.html`.
- Deploy: `.github/workflows/pages.yml` runs on every push to `main` that touches `website/`, every day (it deploys then only when an app's latest release differs from what the live site shows), and by hand (`gh workflow run pages.yml`). It runs every check first (it calls `checks.yml`), then publishes the site that run put together: `website/` with the wiki's static export in place of `website/wiki/`, and without `website/tools/`, `website/data/` and `website/README.md`, which are for people working on the site. Everything else under `website/` is published as it is: put nothing there that should not be public. A new file or folder that should stay out of the site is added to the "Put the site together" step of `checks.yml`. Pages uses the "GitHub Actions" source, with the custom domain `wordsmithand.ink` set in the repository's Pages settings.
- Check before pushing: `python3 website/tools/build.py --check` passes, `python3 -m unittest discover -s website/tools` passes when `releases.py` changed, and `git status` shows only the pages you meant to change; no broken relative links or missing assets; images have `alt` text; the page reads well at phone width and in dark mode.

## website/wiki/

- A separate project from the main site: Fumadocs on Next.js, exported as static files with `basePath: '/wiki'`, published at `https://wordsmithand.ink/wiki/` by the same Pages workflow (one repository has one Pages site). `website/wiki/README.md` has the commands.
- Pages are MDX in `website/wiki/content/docs/`: `start/` (the shared "Wordsmith apps" tab, which also holds the home page) and one folder per app (`script/`, `manuscript/`, `book/`), each a sidebar tab (`root: true` in its `meta.json`). `meta.json` sets the page order.
- **An app's folder is built, never written.** `npm run guide` in `website/wiki` (`scripts/guide.mjs`) reads the guide in the app's own repository, `docs/guide/`, at one commit, and writes the folder from it: each guide page as a wiki page, the folder's `meta.json` in the order of the guide's `README.md`, and the pictures the pages show. It records the commit in `website/wiki/guides.lock.json`, and the page footer shows it. To change what an app's page says, change the guide in the app's repository, land it there, then run `npm run guide` here and land what it writes ([Route C](project/README.md#route-c)). [Project decision 0005](project/decisions/0005-one-guide-per-app.md) has the reasons.
- **Written here by hand:** `content/docs/index.mdx` and the pages in `content/docs/start/`, which are about the project as a whole: the apps and how they fit together, installing, your files, moving between the apps, getting help, questions and answers, privacy. A page about one app's features does not belong there: it belongs in that app's guide. If the wiki should say something an app's guide does not say, open an issue in the app's repository for the guide page.
- `npm run guide` reads each app's `main` on GitHub with git: a checkout beside this repository when it already has the commit, a small temporary fetch otherwise. It never reads a working tree, so the recorded commit is always a published one. `npm run guide -- --app book --ref <branch, tag or commit>` builds one app at another place.
- `npm run guide:check` fails when a page, a picture or the lock file is not what the recorded commits give, when an app's folder or `website/assets/img/` holds a file the tool does not make, and when a link from one wiki page to another, or to a heading of it, leads nowhere. `npm run guide:behind` fails when an app's guide on `main` has changed since the recorded commit. `npm test` runs the tool's tests (`scripts/guide.test.mjs`).
- Its logos, app icons and favicons are the copies in `website/wiki/public/brand/` (see [brand/](#brand)). Never edit them. Each app's section uses that app's color only for small marks; links stay Margin Blue.
- The fonts come from the main site's `/assets/fonts/`, so `npm run dev` shows the wiki without them. To see it as deployed, build it and serve it with the main site; `website/wiki/README.md` has the steps.
- Content rules for the hand-written pages: write for writers, document only what the apps do today, and check claims against the apps' repositories (code, `docs/guide/`, `CHANGELOG.md`). Mark anything not built with `<Status value="planned" />` or `"in-progress"`. Never use an app repository's `.private/` notes or reviews as content.
- `npm run dev` writes an `AGENTS.md` into `website/wiki`: Next.js makes it, with a note about its own documentation. Git ignores it. This file has the rules for the wiki.
- A host name of your own machine never goes into `next.config.mjs`. If you reach the dev server under another name than `localhost`, name it in `WIKI_DEV_ORIGINS` in an untracked `website/wiki/.env.local`.
- Check before pushing: `npm run brand:check`, `npm test`, `npm run guide:check`, `npm run lint`, `npm run types:check` and `npm run build` in `website/wiki` all pass, and every page you touched loads.

## launcher/

Not started. When it is:

- A Rust crate (or Cargo workspace) rooted at `launcher/`, so `cargo` commands run from there: `cargo fmt --check`, `cargo clippy --all-targets -- -D warnings`, `cargo test`.
- Match the apps' choices where it makes sense (egui for the interface, `open-source-core` if it fits) so the suite looks and behaves as one.
- Downloads come only from the project's official GitHub releases and are verified before anything runs. Update checks can be turned off. No accounts, no telemetry.
- Targets macOS, Windows and Linux.
- Add a `launcher.yml` workflow scoped to `paths: ["launcher/**"]` when there is code to check.
- Keep the website's launcher page (`website/launcher.html`, written by `build.py`) in step with what the launcher actually does.

## Before you push

Run the checks for each folder you changed; they are the "Check before pushing" line of its section above. All of them at once, from the repository root:

```sh
python3 -m unittest discover -s project
python3 -m unittest discover -s website/tools
python3 project/privacy.py
python3 project/check_links.py
python3 website/tools/build.py --check
(cd website/wiki && npm ci && npm run brand:check && npm test && npm run guide:check && npm run lint && npm run types:check && npm run build)
```

What runs on GitHub, and what does not:

| Check | Where it runs |
| --- | --- |
| The tools' tests (`python3 -m unittest discover -s project` and `-s website/tools`), `python3 project/privacy.py`, `python3 project/check_links.py`, `python3 website/tools/build.py --check` | `checks.yml`, job "repository": on every pull request and every push to `main`, whatever changed; and by hand |
| `npm run brand:check`, `npm test`, `npm run guide:check`, `npm run lint`, `npm run types:check` and `npm run build` in `website/wiki`, then the site put together as it is published | `checks.yml`, job "wiki and site": the same. `guide:check` reads each app's public repository at its recorded commit, so this job needs the network, as `npm ci` does |
| All of the above again, before the deploy | `pages.yml`: on a push to `main` that touches `website/` or either workflow, every day when an app's latest release has changed, and by hand. It calls `checks.yml` and publishes only when every job passed. A failure there means the site was not updated |
| The pages the deploy builds from fresh release data | Nowhere: they are written by the checked `build.py` from what GitHub answered, after the pages in the repository passed `--check`. Look at the live page after an app's release |
| `python3 project/carry.py --check --remote` | `carried.yml`: on a push to `main` or a pull request that touches `project/README.md`, `project/carry.py`, `AGENTS.md`, `SECURITY.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md` or the workflow; weekly; and by hand. It is red while a published copy is behind its source |
| `npm run guide:behind`: an app's guide on `main` is still the one the wiki was built from | `guides.yml`: every day, by hand, and on a push to `main` that touches the lock file, the tool or an app's data file. It is red while an app's guide has moved on, until `npm run guide` is run and its result landed |
| `python3 brand/source/build.py` matches the committed kit | Locally only |
| A claim on the website or in a hand-written wiki page is true of the app; a link in a website page leads somewhere; a link to another site works | Nowhere: check it yourself |

Every workflow uses GitHub's own actions only, each pinned to a full commit hash with its version in a comment (the organisation allows no others). To move one to a newer version, look the tag's commit up (`gh api repos/actions/<name>/git/ref/tags/<tag>`; for an annotated tag, follow it to the commit) and change the hash and the comment together, in every workflow that uses the action.

`.github/pull_request_template.md` lists what to confirm; a change pushed straight to `main` follows the same list. After a push, watch the "Checks" run; after one that touches `website/`, watch the "Deploy website and wiki to GitHub Pages" run too and open the live page.

## Git

- `main` is the default branch and deploys the website. A change may be pushed straight to `main` once the checks for its folder pass; a pull request is optional and its author merges it ([decision 0002](project/decisions/0002-how-changes-land-and-who-releases.md)).
- History on `main` is not rewritten: GitHub refuses a force-push to `main`, its deletion, and a moved or deleted `v*` tag. Fix a mistake with a new commit.
- Working notes, reviews and anything private go in `.private/`, which Git ignores. Never commit them.
- Keep commits focused, with a short imperative subject.
- Commit the generated website pages with the change that regenerates them. Commit no other build output: not `out/`, `.next/`, `node_modules/`, `target/` or editor files.
- A new folder, or a new kind of file, gets a row in [`LICENSES.md`](LICENSES.md) when none of its rows fits.
