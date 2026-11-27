# Wordsmith Launcher: brand files

The pictures in this folder are copies of files of the Wordsmith brand kit, the `brand/` folder
at the top of this repository. They are made and checked by the kit's tool, never by hand: in
`website/wiki`, `npm run brand` writes them and `npm run brand:check` fails when one differs from
the kit or when this folder holds a file the tool does not know.

| File | The kit's file | Used for |
| --- | --- | --- |
| `icon-32.png`, `icon-256.png`, `icon-512.png`, `icon-1024.png` | `brand/wordsmith-and-ink/app-icon/` | The window, the Linux menu entry |
| `icon-macos-1024.png` | `brand/wordsmith-and-ink/app-icon/icon-macos-1024.png` | The macOS app |
| `icon.ico` | `brand/wordsmith-and-ink/app-icon/wordsmith-and-ink.ico` | The Windows program |
| `wordsmith-script-icon-128.png`, `wordsmith-manuscript-icon-128.png`, `wordsmith-book-icon-128.png` | Each app's `app-icon/icon-128.png` | The list of apps in the window |

The kit has no icon of the launcher's own yet, so the launcher carries the icon of the parent
brand, Wordsmith & Ink.

`tokens.json` is the launcher's own: its interface theme, in the token format of
open-source-core. Its five palette colors are the parent brand's, and the three colors under
`launcher` are the apps' own colors, each used only for the small mark beside that app. A test
in `apps/launcher` holds all eight to the kit's `brand/wordsmith-and-ink/tokens.json`.

The brand files are not open source: all rights are reserved, and the names and logos are
trademarks of The James C. J. Foundation. [`brand/LICENSE.md`](https://github.com/jamescjfoundation/wordsmith/blob/main/brand/LICENSE.md) says
what may be done with them without asking.
