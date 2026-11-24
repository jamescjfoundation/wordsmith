# Wordsmith

Shared pieces of the [Wordsmith](https://wordsmithand.ink) project: free, open-source writing apps for screenwriters, novelists and authors, from The James C. J. Foundation.

The apps themselves live in their own repositories. This repository is a small monorepo for everything that belongs to the project as a whole.

## What's here

| Folder | What it is | Status |
| --- | --- | --- |
| [`brand/`](brand/) | The brand kit: logos, app icons, palettes, tokens and brand guidelines | v1.0 |
| [`website/`](website/) | The public website, plain HTML and CSS, published with GitHub Pages | Draft, live |
| [`wiki/`](wiki/) | User and contributor documentation for the whole suite | Not started |
| [`launcher/`](launcher/) | Wordsmith Launcher, a Rust app that installs, updates and opens the Wordsmith apps | Not started |

## The Wordsmith repositories

| Repository | What it is |
| --- | --- |
| [wordsmith-script](https://github.com/jamescjfoundation/wordsmith-script) | Wordsmith Script: screenplays, TV and stage plays |
| [wordsmith-manuscript](https://github.com/jamescjfoundation/wordsmith-manuscript) | Wordsmith Manuscript: novels and long work |
| [wordsmith-book](https://github.com/jamescjfoundation/wordsmith-book) | Wordsmith Book: print books and ebooks |
| [open-source-core](https://github.com/jamescjfoundation/open-source-core) | The shared base every app is built on |
| wordsmith (this one) | Website, wiki, launcher |

## Working on it

Each folder has its own README with how to build, preview and publish it.

- **Website:** `python3 website/tools/build.py` rewrites the pages; preview with `python3 -m http.server -d website`. Every push to `main` that touches `website/` deploys it.
- **Wiki:** see [`wiki/README.md`](wiki/README.md).
- **Launcher:** see [`launcher/README.md`](launcher/README.md).

Contributors and coding agents: read [`AGENTS.md`](AGENTS.md) first.

## Licenses and names

Code is licensed under the MIT license or the Apache License 2.0, at your option. Fonts are under the SIL Open Font License. The names Wordsmith, Wordsmith & Ink, Wordsmith Script, Wordsmith Manuscript and Wordsmith Book, and their logos, are trademarks of The James C. J. Foundation.
