# Wordsmith website

The marketing site for the Wordsmith apps (Script, Manuscript, Book and the planned Launcher), from Wordsmith & Ink, a project of The James C. J. Foundation.

Plain HTML and CSS with no build step, so GitHub Pages can serve this folder as it is. Open `index.html` in a browser to preview it locally, or run `python3 -m http.server` in this folder and visit http://localhost:8000.

## Files

| Path | What it is |
| --- | --- |
| `index.html` | Home: the suite, the three apps, how they fit, the Foundation |
| `script.html`, `manuscript.html`, `book.html` | One page per app |
| `launcher.html` | The planned Wordsmith Launcher |
| `about.html` | The Foundation, James, principles, Wordsmith & Ink |
| `open-source.html` | The road to 1.0, status, how to help, privacy, licenses |
| `404.html` | Page not found |
| `assets/css/site.css` | All styles. Colors are the brand kit's tokens, with a dark theme that follows the system |
| `assets/js/site.js` | The menu button on small screens (the site works without it) |
| `assets/brand/` | Logos and icons copied unchanged from the brand kit, and `og-image.png` for link previews |
| `assets/img/` | Wordsmith Script screenshots from the app's repository (`docs/images`), with the title bar cropped off |
| `assets/fonts/` | Courier Prime and Inter (SIL Open Font License 1.1, license files included), served from here so no visitor data goes to a font service |
| `.nojekyll` | Tells GitHub Pages to serve the files as they are |

The Manuscript, Book and Launcher pictures are HTML illustrations, not screenshots, and say so in their captions. Replace them with real screenshots once each app can draw its own.

## Editing

The shared header, footer and page text live in `tools/build.py`. Edit it and run `python3 website/tools/build.py` from the repository root to rewrite the HTML pages. Styles are in `assets/css/site.css`.

## Publishing on GitHub Pages

The workflow in `.github/workflows/pages.yml` publishes this folder whenever a push to `main` changes it (or run it by hand from the Actions tab). Pages is enabled with Source set to "GitHub Actions", and the site is live at https://wordsmithand.ink, a custom domain set in the repository's Pages settings (DNS is on Cloudflare). The deploy doesn't need a `CNAME` file.

Still to do:

1. For a custom domain, set it in Settings > Pages, add a `CNAME` file with the domain to this folder, and set the DNS records GitHub lists.
2. Once the final address is known, make the `og:image` URL in each page absolute (for example `https://<domain>/assets/brand/og-image.png`, set in `tools/build.py`), because link previews need a full URL.

All links between pages are relative, so the site works at a domain root or under a repository path.
