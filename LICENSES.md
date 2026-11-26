# Licenses

This repository holds four kinds of thing, and each has its own terms. Find the path in the table; the first row that fits is the one that applies.

| What | Paths | Terms |
| --- | --- | --- |
| **Brand files and names**: the logos, icons, palettes, guides and PDFs of the brand kit, the scripts that draw them, and the copies of kit files kept for the website and the wiki | `brand/`, `website/assets/brand/`, `website/favicon.svg`, `website/wiki/public/brand/` | Not open source. All rights reserved; the names and logos are trademarks of The James C. J. Foundation. [`brand/LICENSE.md`](brand/LICENSE.md) says what you may do without asking |
| **Fonts**: Courier Prime and Inter | `website/assets/fonts/` | SIL Open Font License 1.1, each font's own: [`OFL-CourierPrime.txt`](website/assets/fonts/OFL-CourierPrime.txt), [`OFL-Inter.txt`](website/assets/fonts/OFL-Inter.txt) |
| **Words of the website and the wiki**: the text people read on [wordsmithand.ink](https://wordsmithand.ink/) | The wiki pages written here (`website/wiki/content/docs/index.mdx` and `website/wiki/content/docs/start/`), the text of the generated pages `website/*.html`, and the same text where it is written, inside `website/tools/build.py` and `website/data/` | Creative Commons Attribution 4.0 International (CC BY 4.0): [`LICENSE-CC-BY-4.0`](LICENSE-CC-BY-4.0) |
| **Code, and everything else**: the tools, the website's generator, styles and script, the wiki's own code, the workflows, the launcher when it exists, the project map, the decisions and this repository's other documents | `project/`, `website/tools/`, `website/assets/css/`, `website/assets/js/`, `website/wiki/` outside `content/` and `public/brand/`, `.github/`, `launcher/`, and every file no row above names | MIT OR Apache-2.0, at your option: [`LICENSE-MIT`](LICENSE-MIT), [`LICENSE-APACHE`](LICENSE-APACHE) |

Copyright in the code and in the words is held by the Wordsmith contributors.

## Notes

- **Screenshots.** The pictures of the apps in `website/assets/img/` and beside the wiki's pages (`website/wiki/content/docs/<app>/images/`) are drawn by the apps and copied from each app's repository. They keep that repository's terms, MIT OR Apache-2.0. A logo or icon that shows in one stays under the brand terms.
- **The apps' guides.** The wiki pages in `website/wiki/content/docs/script/`, `manuscript/` and `book/` are built from the guide in each app's repository (`docs/guide/`) and are that guide's text. They keep that repository's terms, MIT OR Apache-2.0, as the screenshots do.
- **Reusing the words.** CC BY 4.0 lets you copy, translate and change the text of the website and the wiki, for any purpose, when you give credit. A credit that works: "From the Wordsmith wiki, by the Wordsmith contributors, CC BY 4.0", with a link to the page. Say if you changed the text.
- **The license does not cover the names.** None of the licenses above gives a right to the Wordsmith names or logos. You may reuse the code and the words; a fork, a changed build or another product needs its own name and its own icon ([`brand/LICENSE.md`](brand/LICENSE.md)).
- **The apps** have their own repositories and their own license files. Their code is MIT OR Apache-2.0 too.
- **What a contribution is licensed as.** A change you send takes the terms of the folder it is made in, by the table above ([`CONTRIBUTING.md`](CONTRIBUTING.md)).
