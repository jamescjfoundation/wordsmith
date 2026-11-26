# Wordsmith brand kit

Brand and product assets for Wordsmith & Ink and the three Wordsmith apps, free and open-source writing tools from The James C. J. Foundation. Kit version 1.0, 24 November 2026.

This folder is the source of every logo, icon and brand color. It started as a copy of the Foundation's brand kit, with folder names lowercased and hyphenated so they're easy to use in paths. Filenames are the kit's. The logos, icons, palettes and guideline PDFs are now rebuilt here from [`source/`](source/).

Start with **[`suite/BRAND_GUIDE.md`](suite/BRAND_GUIDE.md)** for the ideas and rules. The PDFs in [`pdfs/`](pdfs/) show the same ideas laid out as pages.

## Folders

| Folder | What's in it |
| --- | --- |
| [`pdfs/`](pdfs/) | **Wordsmith & Ink - Brand Guidelines** (the parent brand and how the apps sit under it), **Wordsmith Apps - Product Assets** (each app's logos, icons, colors and files), **Wordsmith - An Introduction** |
| [`wordsmith-and-ink/`](wordsmith-and-ink/) | The parent brand: `logo/`, `app-icon/`, `lockups/` (family and endorsed app logos), `palette/`, `tokens.json` |
| [`wordsmith-script/`](wordsmith-script/) | Screenplays: `production/`, `logo/`, `app-icon/`, `palette/`, `tokens.json` |
| [`wordsmith-manuscript/`](wordsmith-manuscript/) | Novels and long work: same layout as Script |
| [`wordsmith-book/`](wordsmith-book/) | Print books and ebooks: same layout as Script |
| [`suite/`](suite/) | The suite brand guide and the three-app overview image |
| [`source/`](source/) | The scripts that build all of the above (see [Rebuilding](#rebuilding)) |
| [`apps.json`](apps.json) | What each app's repository carries from the kit: every file with its checksum, the files that are the app's own, and the seven palette colors. Written by `npm run brand`; never edited |
| [`LICENSE.md`](LICENSE.md) | How the names and logos may be used |

The original kit kept the same build scripts once per app; here they're kept once, in `source/`.

## Using the files

- **Logos** are outlined SVG paths, so no font is needed. Use `-ink` versions on light backgrounds and `-paper` versions on dark backgrounds. `-mono` versions are single-color.
- **App icons:** each `app-icon/` folder has SVG masters (normal, `-small` for tiny sizes, `-macos` on the 824 px macOS grid), PNGs from 16 to 1024 px, a Windows `.ico` and a `favicon.svg`.
- **Colors:** each `tokens.json` holds that brand's design tokens. Each `palette/` folder has the palette as CSS, JSON, GIMP (`.gpl`) and Adobe (`.ase`) swatches, plus a reference card.
- **Ready-made sets:** each app's `production/` folder is a ready-to-use set of that app's key files and the parent brand's, with a README that explains each one. An app's repository carries this set, and the icons it uses from `app-icon/`.
- **Copy by the tool, don't edit.** The website (`website/assets/brand/`), the wiki (`website/wiki/public/brand/`) and the app repositories (`assets/brand/` in each) hold files from here unchanged, written by one tool. To change a logo, icon, palette or PDF, change the script in `source/` and rebuild. Don't edit the output by hand, here or in a copy.
- **After a change, update the copies.** One tool makes and checks every copy, `website/wiki/scripts/brand.mjs`. `npm run brand` in `website/wiki` writes the website's and the wiki's copies and `apps.json`, and `npm run brand:check` fails when one is missing or differs; it runs on every pull request and every push. For an app, `npm run brand -- --app script` (or `manuscript`, `book`) writes the kit's files into the app's checkout beside this repository and says what changed, and `npm run brand:check -- --app script` compares without writing. The repository's [`AGENTS.md`](../AGENTS.md#brand) lists the copies, and Route F of the [project map](../project/README.md#route-f) has the steps.
- **What is an app's own.** Each app's interface theme file is the app's, in the token format of open-source-core; it is not a copy of the `tokens.json` here, and only its seven palette colors must match. [`apps.json`](apps.json) names it, and the files an app derives from a kit file with its own tool.

## Rebuilding

Nothing runs automatically; rebuild only when a name, color or shape changes. You need Python 3.10+; for the PDFs you also need Node.js.

```sh
pip install -r brand/source/requirements.txt   # fonttools, cairosvg, numpy, pillow (cairosvg needs the system cairo library)
python3 brand/source/fetch_fonts.py            # once: the exact Courier Prime and Inter files, checked by SHA-256
python3 brand/source/build.py                  # builds into brand/build/ and lists what differs from brand/
python3 brand/source/build.py --write          # also writes the changed files into brand/
```

For the two guideline PDFs, add `--pdf` (with `--write` to replace them in `pdfs/`). It renders with Playwright's Chromium, installed once:

```sh
cd brand/source && npm install && npx playwright install chromium
```

What the build does and doesn't cover:

- `build.py` runs `buildink.py` (the parent brand and its lockups), `buildp.py` (Manuscript and Book) and `buildc.py` (Script, which keeps its own builder). It then writes Script's palette and copies the endorsed lockups and `production/` sets into place.
- It only changes files whose content changed. SVGs are compared without the C2PA "content credentials" metadata that the kit's export tool added, PNGs by their pixels and `.ico` files by their images. A fresh build matches every committed logo, icon and palette.
- The fonts matter: other versions of Courier Prime or Inter change the letter outlines slightly. `fetch_fonts.py` gets Courier Prime from Google Fonts and Inter 4.0 (OTF) from its official release.
- Hand-written files are never touched: the READMEs, `suite/BRAND_GUIDE.md`, each brand's `tokens.json`, `suite/wordsmith-suite-overview.png` and `pdfs/Wordsmith - An Introduction.pdf`. Update them by hand when something they describe changes.
- The `.ico` files are made with ImageMagick when it's installed, otherwise with Pillow.
- [`source/explorations/`](source/explorations/) holds the logo-concept scripts from the kit's design rounds. They're kept for reference, aren't part of the build, and don't run as they are.

## Names and licenses

The apps' code is open source. The brand files are not: all rights in them are reserved. The names Wordsmith, Wordsmith & Ink, Wordsmith Script, Wordsmith Manuscript, Wordsmith Book and Wordsmith Launcher, and their logos, are trademarks of The James C. J. Foundation. You may use them unchanged to refer to the project, but not for forks or other products. **[`LICENSE.md`](LICENSE.md)** says what is fine without asking and what is not. All names are working names until the trademark check is done. Courier Prime and Inter are under the SIL Open Font License 1.1, which allows using their letters in a logo.
