# Wordsmith brand kit

Brand and product assets for Wordsmith & Ink and the three Wordsmith apps, free and open-source writing tools from The James C. J. Foundation. Kit version 1.0, 24 November 2026.

This folder is the source of truth for the brand inside the code. The design masters live in the Foundation's shared drive (`10. Open Source / 01. Wordsmith`). This is a byte-for-byte copy of them, with folder names lowercased and hyphenated so they're easy to use in paths. Filenames are unchanged.

Start with **[`suite/BRAND_GUIDE.md`](suite/BRAND_GUIDE.md)** for the ideas and rules. The PDFs in [`pdfs/`](pdfs/) show the same ideas laid out as pages.

## Folders

| Folder | Drive folder | What's in it |
| --- | --- | --- |
| [`pdfs/`](pdfs/) | `00. PDFs` | **Wordsmith & Ink - Brand Guidelines** (the parent brand and how the apps sit under it), **Wordsmith Apps - Product Assets** (each app's logos, icons, colors and files), **Wordsmith - An Introduction** |
| [`wordsmith-and-ink/`](wordsmith-and-ink/) | `01. Wordsmith & Ink` | The parent brand: `logo/`, `app-icon/`, `lockups/` (family and endorsed app logos), `palette/`, `source/`, `tokens.json` |
| [`wordsmith-script/`](wordsmith-script/) | `02. Wordsmith Script` | Screenplays: `production/`, `logo/`, `app-icon/`, `palette/`, `source/`, `tokens.json` |
| [`wordsmith-manuscript/`](wordsmith-manuscript/) | `03. Wordsmith Manuscript` | Novels and long work: same layout as Script |
| [`wordsmith-book/`](wordsmith-book/) | `04. Wordsmith Book` | Print books and ebooks: same layout as Script |
| [`suite/`](suite/) | `05. Suite` | The suite brand guide and the three-app overview image |

The `Wordsmith Brand Kit.zip` on the drive isn't copied here, because it holds the same files.

## Using the files

- **Logos** are outlined SVG paths, so no font is needed. Use `-ink` versions on light backgrounds and `-paper` versions on dark backgrounds. `-mono` versions are single-color.
- **App icons:** each `app-icon/` folder has SVG masters (normal, `-small` for tiny sizes, `-macos` on the 824 px macOS grid), PNGs from 16 to 1024 px, a Windows `.ico` and a `favicon.svg`.
- **Colors:** each `tokens.json` holds that brand's design tokens. Each `palette/` folder has the palette as CSS, JSON, GIMP (`.gpl`) and Adobe (`.ase`) swatches, plus a reference sheet.
- **Ready-made sets:** each app's `production/` folder is a ready-to-use set of that app's key files and the parent brand's, with a README that explains each one. When an app repository needs brand files, copy them from here.
- **Copy, don't edit.** Other parts of this repo (such as `website/assets/brand/`) and the app repositories copy files from here unchanged. To change a logo or icon, change the master in the drive, rebuild, and copy it here again.

## Rebuilding

The `source/` scripts rebuild the logos, icons and palettes, and `wordsmith-and-ink/source/pdf/` rebuilds the PDFs. They need Python with fontTools and cairosvg, plus the Courier Prime and Inter font files (SIL Open Font License 1.1) in a folder named by `WORDSMITH_FONT_DIR`.

The scripts were written for the place the kit was first made: they refer to the drive's folder names and to a fixed kit path (`/mnt/project-files/wordsmith/brand-kit` in `source/pdf/common.py`). Point that at this folder and update the folder names before running them here.

## Names and licenses

The apps' code is open source. The names Wordsmith, Wordsmith & Ink, Wordsmith Script, Wordsmith Manuscript and Wordsmith Book, and their logos, are trademarks of The James C. J. Foundation. You may use them unchanged to refer to the project, but not for forks or other products. All names are working names until the trademark check is done. Courier Prime and Inter are under the SIL Open Font License 1.1, which allows using their letters in a logo.
