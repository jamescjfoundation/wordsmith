# Wordsmith

Shared pieces of the [Wordsmith](https://wordsmithand.ink) project: free, open-source writing apps for screenwriters, novelists and authors, from The James C. J. Foundation.

> **A note from the founder**
>
> A lot of work has already gone into laying a solid foundation. The apps aren't ready for everyday use yet, but the idea is sound and the pieces are in place. From here, the plan is slow, steady development and testing.
>
> I've been a wannabe developer for years. AI has finally given me the tools to bring an idea like this together, but my time and resources are limited. Ideas, feedback, bug reports, fixes and feature improvements are all welcome. If you care about this as much as we do, we're also open to deeper partnerships.
>
> I'll keep improving the ecosystem where I can while building out the rest of the foundation.
>
> — Dylan J.

The apps themselves live in their own repositories. This repository is a small monorepo for everything that belongs to the project as a whole.

## What's here

| Folder | What it is | Status |
| --- | --- | --- |
| [`project/`](project/) | The project map: the repositories, how they depend on each other, where each kind of change goes, and the project-wide decisions | Current |
| [`brand/`](brand/) | The brand kit: logos, app icons, palettes, tokens and brand guidelines | v1.0 |
| [`website/`](website/) | The public website, plain HTML and CSS, published with GitHub Pages | Live |
| [`website/wiki/`](website/wiki/) | The wiki (Fumadocs), at wordsmithand.ink/wiki/: each app's user guide, built from the guide in the app's own repository, and the pages about the project as a whole | Live |
| [`launcher/`](launcher/) | Wordsmith Launcher, a small Rust program that installs, updates, opens and removes the Wordsmith apps. Its downloads are this repository's [releases](https://github.com/jamescjfoundation/wordsmith/releases) | Its first release is 0.9.0, a preview ([changelog](launcher/CHANGELOG.md)) |

## The Wordsmith repositories

| Repository | What it is |
| --- | --- |
| [wordsmith-script](https://github.com/jamescjfoundation/wordsmith-script) | Wordsmith Script: screenplays, TV and stage plays |
| [wordsmith-manuscript](https://github.com/jamescjfoundation/wordsmith-manuscript) | Wordsmith Manuscript: novels and long work |
| [wordsmith-book](https://github.com/jamescjfoundation/wordsmith-book) | Wordsmith Book: print books and ebooks |
| [open-source-core](https://github.com/jamescjfoundation/open-source-core) | The shared base every app is built on |
| wordsmith (this one) | Project map, brand kit, website, wiki, launcher |
| [wordcraft](https://github.com/jamescjfoundation/wordcraft), [craft-libs](https://github.com/jamescjfoundation/craft-libs) | Our forks of the upstream projects the shared base builds on |

![How the Wordsmith repositories fit together: the upstream projects are forked into our wordcraft and craft-libs forks, which open-source-core builds on. The core feeds Wordsmith Script, Wordsmith Manuscript and Wordsmith Book. Manuscript reads Script's .wss files and Book builds on Manuscript's model and format. The wordsmith repository sends brand files to each app and writes up each app's guide, changelog and releases in the wiki and on the website; it also holds the project map and rules, the brand kit, the website, the wiki and the launcher.](project/repositories.svg)

How they fit together, and where each kind of change goes, is in the [project map](project/README.md).

## Working on it

Each folder has its own README with how to build, preview and publish it.

- **Project map:** [`project/README.md`](project/README.md). `python3 project/carry.py` checks the text that other repositories carry from it, and the text this one carries from the shared base.
- **Brand kit:** [`brand/README.md`](brand/README.md). Logos, icons and palettes are rebuilt from `brand/source/`, never edited by hand.
- **Website:** `python3 website/tools/build.py` rewrites the pages; preview with `python3 website/tools/serve.py`, then http://localhost:8000. Every push to `main` that touches `website/` deploys it, wiki included.
- **Wiki:** `npm ci && npm run dev` in `website/wiki`; see [`website/wiki/README.md`](website/wiki/README.md). It deploys with the website.
- **Launcher:** a Cargo workspace of its own, built on the shared base like an app. `cargo xtask ci` in `launcher/` is its gate; see [`launcher/README.md`](launcher/README.md) and [`launcher/AGENTS.md`](launcher/AGENTS.md).

Every pull request and every push to `main` runs the "Checks" workflow: the tools' tests, the privacy and link checks, the website's pages, the brand copies, and the wiki's lint, type check and build. A change under `launcher/` also runs the "Launcher" workflow, the launcher's own gate.

What is planned is in [`ROADMAP.md`](ROADMAP.md): open work is an issue in the [v1 milestone](https://github.com/jamescjfoundation/wordsmith/milestone/1).

To help, start with [`CONTRIBUTING.md`](CONTRIBUTING.md). Coding agents, and anyone changing more than a page, read [`AGENTS.md`](AGENTS.md) first. To report a security problem, follow [`SECURITY.md`](SECURITY.md). Everyone taking part follows the [code of conduct](CODE_OF_CONDUCT.md).

## Licenses and names

Each kind of thing here has its own terms. [`LICENSES.md`](LICENSES.md) lists them by folder:

- **Code**, and everything not named below, is under the MIT license or the Apache License 2.0, at your option ([`LICENSE-MIT`](LICENSE-MIT), [`LICENSE-APACHE`](LICENSE-APACHE)).
- **The words of the website and the wiki** are under Creative Commons Attribution 4.0 ([`LICENSE-CC-BY-4.0`](LICENSE-CC-BY-4.0)).
- **The brand files** in `brand/`, and their copies, are not open source: all rights reserved. The names Wordsmith, Wordsmith & Ink, Wordsmith Script, Wordsmith Manuscript, Wordsmith Book and Wordsmith Launcher, and their logos, are trademarks of The James C. J. Foundation. You may use them unchanged to refer to the project, but not for forks or other products; [`brand/LICENSE.md`](brand/LICENSE.md) says what is fine without asking.
- **The fonts** are under the SIL Open Font License, with their license files beside them in `website/assets/fonts/`.
