# Wordsmith brand kit

Brand and product assets for Wordsmith & Ink and the three Wordsmith apps, free and open-source writing tools from The James C. J. Foundation. Kit version 1.0, 24 November 2026.

This folder is the source of truth for the brand inside the code. It started as a copy of the kit in the Foundation's shared drive (`10. Open Source / 01. Wordsmith`), with folder names lowercased and hyphenated so they're easy to use in paths. Filenames are unchanged. The logos, icons, palettes and guideline PDFs are now rebuilt here from [`source/`](source/).

Start with **[`suite/BRAND_GUIDE.md`](suite/BRAND_GUIDE.md)** for the ideas and rules. The PDFs in [`pdfs/`](pdfs/) show the same ideas laid out as pages.

## Folders

| Folder | Drive folder | What's in it |
| --- | --- | --- |
| [`pdfs/`](pdfs/) | `00. PDFs` | **Wordsmith & Ink - Brand Guidelines** (the parent brand and how the apps sit under it), **Wordsmith Apps - Product Assets** (each app's logos, icons, colors and files), **Wordsmith - An Introduction** |
| [`wordsmith-and-ink/`](wordsmith-and-ink/) | `01. Wordsmith & Ink` | The parent brand: `logo/`, `app-icon/`, `lockups/` (family and endorsed app logos), `palette/`, `tokens.json` |
| [`wordsmith-script/`](wordsmith-script/) | `02. Wordsmith Script` | Screenplays: `production/`, `logo/`, `app-icon/`, `palette/`, `tokens.json` |
| [`wordsmith-manuscript/`](wordsmith-manuscript/) | `03. Wordsmith Manuscript` | Novels and long work: same layout as Script |
| [`wordsmith-book/`](wordsmith-book/) | `04. Wordsmith Book` | Print books and ebooks: same layout as Script |
| [`suite/`](suite/) | `05. Suite` | The suite brand guide and the three-app overview image |
| [`source/`](source/) | each `Source/` | The scripts that build all of the above (see [Rebuilding](#rebuilding)) |

The drive's `Wordsmith Brand Kit.zip` isn't copied here because it holds the same files. Each app's `Source/` folder on the drive held the same shared scripts, so they're kept once in `source/`.

## Using the files

- **Logos** are outlined SVG paths, so no font is needed. Use `-ink` versions on light backgrounds and `-paper` versions on dark backgrounds. `-mono` versions are single-color.
- **App icons:** each `app-icon/` folder has SVG masters (normal, `-small` for tiny sizes, `-macos` on the 824 px macOS grid), PNGs from 16 to 1024 px, a Windows `.ico` and a `favicon.svg`.
- **Colors:** each `tokens.json` holds that brand's design tokens. Each `palette/` folder has the palette as CSS, JSON, GIMP (`.gpl`) and Adobe (`.ase`) swatches, plus a reference card.
- **Ready-made sets:** each app's `production/` folder is a ready-to-use set of that app's key files and the parent brand's, with a README that explains each one. When an app repository needs brand files, copy them from here.
- **Copy, don't edit.** Other parts of this repo (such as `website/assets/brand/`) and the app repositories copy files from here unchanged. To change a logo, icon, palette or PDF, change the script in `source/` and rebuild. Don't edit the output by hand.

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
- Hand-written files are never touched: the READMEs, `suite/BRAND_GUIDE.md`, the apps' `tokens.json`, `suite/wordsmith-suite-overview.png` and `pdfs/Wordsmith - An Introduction.pdf`. Update them by hand when something they describe changes.
- The `.ico` files are made with ImageMagick when it's installed, otherwise with Pillow.
- [`source/explorations/`](source/explorations/) holds the logo-concept scripts from the kit's design rounds. They're kept for reference, aren't part of the build, and don't run as they are.

## Names and licenses

The apps' code is open source. The names Wordsmith, Wordsmith & Ink, Wordsmith Script, Wordsmith Manuscript and Wordsmith Book, and their logos, are trademarks of The James C. J. Foundation. You may use them unchanged to refer to the project, but not for forks or other products. All names are working names until the trademark check is done. Courier Prime and Inter are under the SIL Open Font License 1.1, which allows using their letters in a logo.
