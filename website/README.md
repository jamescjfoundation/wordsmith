# Wordsmith website

The public site for the Wordsmith apps (Script, Manuscript, Book and the planned Launcher), from Wordsmith & Ink, a project of The James C. J. Foundation.

Plain HTML and CSS, so GitHub Pages can serve the pages as they are. To preview it locally, run `python3 website/tools/serve.py` from the repository root and visit http://localhost:8000. It works like `python3 -m http.server`, but serves `/about` from `about.html` the way Pages does.

## Files

| Path | What it is |
| --- | --- |
| `index.html` | Home: the suite, the three apps, how they fit, the Foundation |
| `script.html`, `manuscript.html`, `book.html` | One page per app |
| `launcher.html` | The planned Wordsmith Launcher |
| `about.html` | The Foundation, James, principles, Wordsmith & Ink |
| `open-source.html` | Each app's latest release and where its plans are kept, how to help, privacy, licenses |
| `404.html` | Page not found |
| `tools/build.py` | Writes every page: the shared header and footer and all the page text. Not published |
| `tools/releases.py` | Reads each app's latest public release from GitHub, for the pages' versions and download links. Not published |
| `tools/serve.py` | Local preview server that serves `/about` from `about.html`, like Pages. Not published |
| `assets/css/site.css` | All styles. Colors are the brand kit's tokens, with a dark theme that follows the system |
| `assets/js/site.js` | The menu button on small screens (the site works without it) |
| `assets/brand/` | Logos and icons copied unchanged from the brand kit in `brand/` by `npm run brand` in `wiki/` (`npm run brand:check` fails when one differs), and `og-image.png` for link previews, which is not a kit file. `favicon.svg`, beside the pages, is a kit copy too |
| `assets/img/` | Screenshots drawn by the apps, carried from each app's repository (`docs/images/`) by `npm run guide` in `wiki/` and written as WebP. Never copied or edited by hand: `npm run guide:check` fails on a file there the tool did not write |
| `data/` | What the pages say about each app's state: `apps/<app>.json` (name, repository, platforms, the words for each state, the screenshots carried here), `platforms.json`, and `releases.json`, the last known release of each app. Not published; the release data a deploy was built from is published as `/releases.json` |
| `assets/fonts/` | Courier Prime and Inter (SIL Open Font License 1.1, license files included), served from here so no visitor data goes to a font service |
| `.nojekyll` | Tells GitHub Pages to serve the files as they are |
| `wiki/` | The wiki, a separate Fumadocs project published at `/wiki/`. See [`wiki/README.md`](wiki/README.md) |

Every picture of an app is a screenshot the app drew itself, carried here by Route G of the [project map](../project/README.md#route-g). Two pictures are drawn in `build.py` and are not screenshots: the stack of three books on the home page, which is decoration, and the sketch on the launcher's page, whose caption says nothing of the launcher is built.

## Editing

The shared header, footer and page text live in `tools/build.py`. Edit it and run `python3 website/tools/build.py` from the repository root to rewrite the HTML pages, then commit the script and the pages together. Never edit a page by hand: `python3 website/tools/build.py --check` fails when a page is not what the script writes, and it runs on every pull request and push. Styles are in `assets/css/site.css`.

The words of the site are under CC BY 4.0, the code that builds it under MIT OR Apache-2.0, and the logos and icons in `assets/brand/` are not open source: [`LICENSES.md`](../LICENSES.md) has the list.

## Publishing on GitHub Pages

The workflow in `.github/workflows/pages.yml` publishes this folder whenever a push to `main` changes it (or run it by hand from the Actions tab). It also runs every day and publishes when an app has a newer release than the live site shows. Every deploy reads the apps' releases from GitHub first and builds the pages from that, so the versions and download links follow the apps without an edit here ([project decision 0006](../project/decisions/0006-the-site-reads-the-apps-releases.md)). It first runs every check a pull request gets (`.github/workflows/checks.yml`): the pages against `build.py`, the brand copies against the kit, and the wiki's lint, type check and build. If one fails, nothing is published. The wiki's static export is published at `/wiki/` in place of the wiki's source, and `tools/`, `data/` and this README are left out. Everything else in this folder is published as it is. Pages is enabled with Source set to "GitHub Actions", and the site is live at https://wordsmithand.ink, a custom domain set in the repository's Pages settings (DNS is on Cloudflare). The deploy doesn't need a `CNAME` file.

All links between pages are relative and leave off `.html` (`about`, not `about.html`). GitHub Pages serves `/about` from `about.html`, and old `.html` addresses still work.
