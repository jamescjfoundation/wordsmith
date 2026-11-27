# Attribution

What Wordsmith Launcher carries that is not its own code, each with its terms. Code dependencies
are listed by `cargo xtask third-party-licenses`; their licenses are checked by
`cargo xtask licenses` and `cargo deny` (open-source-core decision 0001).

## Brand files

Copies of files of the Wordsmith brand kit, the `brand/` folder at the top of this repository.
They are made and checked by the kit's tool (`npm run brand` and `npm run brand:check` in
`website/wiki`), never edited here. They are not open source.

| Path | What | Terms |
| --- | --- | --- |
| `assets/brand/icon-32.png` | The icon of the parent brand, Wordsmith & Ink, 32 px | Trademark of The James C. J. Foundation; use unmodified (`assets/brand/README.md`) |
| `assets/brand/icon-256.png` | The same, 256 px: the window's icon | Trademark of The James C. J. Foundation; use unmodified (`assets/brand/README.md`) |
| `assets/brand/icon-512.png` | The same, 512 px | Trademark of The James C. J. Foundation; use unmodified (`assets/brand/README.md`) |
| `assets/brand/icon-1024.png` | The same, 1024 px | Trademark of The James C. J. Foundation; use unmodified (`assets/brand/README.md`) |
| `assets/brand/icon-macos-1024.png` | The same, drawn for macOS's icon grid, 1024 px | Trademark of The James C. J. Foundation; use unmodified (`assets/brand/README.md`) |
| `assets/brand/icon.ico` | The same, for the Windows program (16 to 256 px) | Trademark of The James C. J. Foundation; use unmodified (`assets/brand/README.md`) |
| `assets/brand/wordsmith-script-icon-128.png` | Wordsmith Script's icon, 128 px, for the list of apps | Trademark of The James C. J. Foundation; use unmodified (`assets/brand/README.md`) |
| `assets/brand/wordsmith-manuscript-icon-128.png` | Wordsmith Manuscript's icon, 128 px, for the list of apps | Trademark of The James C. J. Foundation; use unmodified (`assets/brand/README.md`) |
| `assets/brand/wordsmith-book-icon-128.png` | Wordsmith Book's icon, 128 px, for the list of apps | Trademark of The James C. J. Foundation; use unmodified (`assets/brand/README.md`) |

## Our own assets

| Path | What | License |
| --- | --- | --- |
| `assets/brand/tokens.json` | The launcher's interface theme, in the brand kit's colors | MIT OR Apache-2.0 (this project) |
| `assets/brand/README.md` | What the brand files are and where they come from | MIT OR Apache-2.0 (this project) |

## Fonts

The launcher bundles no font of its own. The interface fonts are built in by open-source-core,
and their license texts are carried in every release package under `licenses/assets/fonts/`.

## Other work

The idea of what a launcher does, and the order of its steps, was learned from ArtCraft Launcher
(<https://github.com/storytold/craft-launcher>, MIT OR Apache-2.0). No code, text or picture of
it was copied.
