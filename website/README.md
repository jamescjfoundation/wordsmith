# Wordsmith website

The marketing site for the Wordsmith apps (Script, Manuscript, Book and the planned Launcher), from Wordsmith & Ink, a project of The James C. J. Foundation.

Plain HTML and CSS, so GitHub Pages can serve this folder as it is. To preview it locally, run `python3 website/tools/serve.py` from the repository root and visit http://localhost:8000. It works like `python3 -m http.server`, but serves `/about` from `about.html` the way Pages does.

## Files

| Path | What it is |
| --- | --- |
| `index.html` | Home: the suite, the three apps, how they fit, the Foundation |
| `script.html`, `manuscript.html`, `book.html` | One page per app |
| `launcher.html` | The planned Wordsmith Launcher |
| `about.html` | The Foundation, James, principles, Wordsmith & Ink |
| `open-source.html` | The road to 1.0, status, how to help, privacy, licenses |
| `404.html` | Page not found |
| `tools/build.py` | Writes every page: the shared header and footer and all the page text |
| `tools/serve.py` | Local preview server that serves `/about` from `about.html`, like Pages |
| `assets/css/site.css` | All styles. Colors are the brand kit's tokens, with a dark theme that follows the system |
| `assets/js/site.js` | The menu button on small screens (the site works without it) |
| `assets/brand/` | Logos and icons copied by hand, unchanged, from the brand kit in `brand/` (nothing checks the copies), and `og-image.png` for link previews, which is not a kit file |
| `assets/img/` | Wordsmith Script screenshots from the app's repository (`docs/images`), with the title bar cropped off |
| `assets/fonts/` | Courier Prime and Inter (SIL Open Font License 1.1, license files included), served from here so no visitor data goes to a font service |
| `.nojekyll` | Tells GitHub Pages to serve the files as they are |
| `wiki/` | The wiki, a separate Fumadocs project published at `/wiki/`. See [`wiki/README.md`](wiki/README.md) |

The Manuscript, Book and Launcher pictures are HTML illustrations, not screenshots, and say so in their captions. Manuscript and Book can now draw their own pictures; replacing the illustrations follows Route G of the [project map](../project/README.md#route-g).

## Editing

The shared header, footer and page text live in `tools/build.py`. Edit it and run `python3 website/tools/build.py` from the repository root to rewrite the HTML pages. Styles are in `assets/css/site.css`.

## Publishing on GitHub Pages

The workflow in `.github/workflows/pages.yml` publishes this folder whenever a push to `main` changes it (or run it by hand from the Actions tab). It builds the wiki first and publishes its static export at `/wiki/` in place of the wiki's source. Everything else in this folder is published as it is, `tools/` and this README included. Pages is enabled with Source set to "GitHub Actions", and the site is live at https://wordsmithand.ink, a custom domain set in the repository's Pages settings (DNS is on Cloudflare). The deploy doesn't need a `CNAME` file.

All links between pages are relative and leave off `.html` (`about`, not `about.html`). GitHub Pages serves `/about` from `about.html`, and old `.html` addresses still work.
