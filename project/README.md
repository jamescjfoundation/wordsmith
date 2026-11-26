# The Wordsmith project map

How the Wordsmith repositories fit together, where each kind of change goes, and the rules that hold in all of them. This folder owns the map: change it here, never in a copy.

The block between the two marker lines below is carried, word for word, in the `AGENTS.md` of each app repository. It is changed only here. `python3 project/carry.py --write` copies it into the apps, and the "Check the carried blocks" workflow in this repository fails while a published copy differs ([Route N](#route-n)).

<!-- BEGIN wordsmith project block -->
## The Wordsmith project

Wordsmith is five repositories and two forks, all under [jamescjfoundation](https://github.com/jamescjfoundation). The full map, the steps of every route and the project's rules are in the [project map](https://github.com/jamescjfoundation/wordsmith/blob/main/project/README.md), which the wordsmith repository owns.

| Repository | Owns |
| --- | --- |
| [wordsmith](https://github.com/jamescjfoundation/wordsmith) | The project map and rules (`project/`), the brand kit (`brand/`), the website (`website/`), the wiki (`website/wiki/`), the launcher (planned) |
| [wordsmith-script](https://github.com/jamescjfoundation/wordsmith-script) | Wordsmith Script, the screenplay app, and the `.wss` file format |
| [wordsmith-manuscript](https://github.com/jamescjfoundation/wordsmith-manuscript) | Wordsmith Manuscript, the novel and long-form app, the `.wsm` project format, and the book view that Book reads |
| [wordsmith-book](https://github.com/jamescjfoundation/wordsmith-book) | Wordsmith Book, the book design and typesetting app, and the `.wsbk` project format |
| [open-source-core](https://github.com/jamescjfoundation/open-source-core) | The shared base: the `jcj-` crates and the settings and tooling every app carries. It is general and names no product |
| [wordcraft](https://github.com/jamescjfoundation/wordcraft), [craft-libs](https://github.com/jamescjfoundation/craft-libs) | Our forks of the upstream projects the core builds on |

- Each app builds on open-source-core at one release tag and carries its shared files (`cargo xtask sync`). Only the core reaches the forks.
- Wordsmith Book also builds on Wordsmith Manuscript's model and format crates, at a book-view tag. Wordsmith Manuscript reads Wordsmith Script's `.wss` files.
- Each app takes its logos, icons and palette from the brand kit, unchanged. The wiki and the website describe the apps from each app's guide, changelog and releases.

| The change | Where it goes | Route |
| --- | --- | --- |
| A fix in a `jcj-` crate, or something any app would share | open-source-core first, then the app's pin | [A](https://github.com/jamescjfoundation/wordsmith/blob/main/project/README.md#route-a) |
| Something one app needs from another app | An issue in the providing app's repository | [B](https://github.com/jamescjfoundation/wordsmith/blob/main/project/README.md#route-b) |
| A change users will see in an app | The app's `docs/guide/` and `CHANGELOG.md`, then the wiki and website | [C](https://github.com/jamescjfoundation/wordsmith/blob/main/project/README.md#route-c) |
| A wiki page | wordsmith, `website/wiki/content/docs/<app>/` | [D](https://github.com/jamescjfoundation/wordsmith/blob/main/project/README.md#route-d) |
| Website text, or an app's status on the site | wordsmith, `website/tools/build.py` | [E](https://github.com/jamescjfoundation/wordsmith/blob/main/project/README.md#route-e) |
| A logo, icon or brand color | wordsmith, `brand/source/`, then the copies | [F](https://github.com/jamescjfoundation/wordsmith/blob/main/project/README.md#route-f) |
| Screenshots | Drawn in the app, then copied to wordsmith | [G](https://github.com/jamescjfoundation/wordsmith/blob/main/project/README.md#route-g) |
| A security problem | Never public: `.private/` and a maintainer | [H](https://github.com/jamescjfoundation/wordsmith/blob/main/project/README.md#route-h) |
| A core release, or moving an app to a newer core | open-source-core, then each app | [I](https://github.com/jamescjfoundation/wordsmith/blob/main/project/README.md#route-i) |
| An app release | The app, then the website and wiki | [J](https://github.com/jamescjfoundation/wordsmith/blob/main/project/README.md#route-j) |
| A change in WordCraft or craft-libs | Our fork, then the core | [K](https://github.com/jamescjfoundation/wordsmith/blob/main/project/README.md#route-k) |
| A change that spans two repositories | The provider first; each change names the other | [L](https://github.com/jamescjfoundation/wordsmith/blob/main/project/README.md#route-l) |
| Working with all the repositories, or with only one | Side by side as sibling folders | [M](https://github.com/jamescjfoundation/wordsmith/blob/main/project/README.md#route-m) |
| A rule or instruction that several repositories carry | The block's owner: the core's `template/`, or the project map for this block | [N](https://github.com/jamescjfoundation/wordsmith/blob/main/project/README.md#route-n) |

Before changing a repository, read its own `AGENTS.md`. Its rules apply inside it; this block applies in all of them. The block is owned by the project map and copied from it by a tool: it is never edited in a copy.
<!-- END wordsmith project block -->

## Contents

- [The repositories](#the-repositories)
- [How they depend on each other](#how-they-depend-on-each-other)
- [Routes](#routes): A to N
- [Where to look, where to write](#where-to-look-where-to-write)
- [Project rules](#project-rules)
- [Decisions](decisions/README.md)

Lines that start with **Today:** describe a gap as it stands: a tool that does not exist yet or a choice not yet made. They say what is safe to do now. They are not promises.

## The repositories

All are public, under [github.com/jamescjfoundation](https://github.com/jamescjfoundation), with `main` as the default branch.

### wordsmith

[github.com/jamescjfoundation/wordsmith](https://github.com/jamescjfoundation/wordsmith)

- **Owns:** everything that belongs to the project as a whole. `project/` (this map and the project's decisions), `brand/` (the brand kit, the source of every logo, icon and brand color), `website/` (the public site), `website/wiki/` (the wiki), `launcher/` (planned, not started).
- **Stack:** Python 3 scripts for the brand kit and the website pages; Fumadocs on Next.js for the wiki. No Rust yet.
- **Publishes:** [wordsmithand.ink](https://wordsmithand.ink/) and [wordsmithand.ink/wiki/](https://wordsmithand.ink/wiki/), by `.github/workflows/pages.yml` on every push to `main` that touches `website/`.
- **Rules:** [`AGENTS.md`](../AGENTS.md).

### wordsmith-script

[github.com/jamescjfoundation/wordsmith-script](https://github.com/jamescjfoundation/wordsmith-script)

- **Owns:** Wordsmith Script, the app for screenplays, TV and stage plays. The screenplay rules (elements, typing, pagination, Fountain, scene numbers, reports) and the `.wss` file format (`docs/format.md`).
- **Stack:** Rust on open-source-core. Crates `wordsmith-script`, `wordsmith-format`, `wordsmith-ui` in `crates/`; programs `wordsmith`, `wordsmith-cli`, `wordsmith-web` in `apps/`.
- **Publishes:** release files on its GitHub releases page (none yet), which the app's update check reads. Its user guide is `docs/guide/`.
- **Rules:** its [`AGENTS.md`](https://github.com/jamescjfoundation/wordsmith-script/blob/main/AGENTS.md).

### wordsmith-manuscript

[github.com/jamescjfoundation/wordsmith-manuscript](https://github.com/jamescjfoundation/wordsmith-manuscript)

- **Owns:** Wordsmith Manuscript, the app for novels and long work. The binder, the story bible, import and export, the `.wsm` project folder and its packed form `.wsmz` (`docs/format.md`), and the book view that Wordsmith Book reads (`docs/book-handoff.md`).
- **Stack:** Rust on open-source-core. Crates `manuscript-model`, `manuscript-format`, `manuscript-io`, `manuscript-ui` in `crates/`; programs `manuscript`, `manuscript-cli`, `manuscript-web` in `apps/`.
- **Publishes:** release files on its GitHub releases page (none yet), which the app's update check reads; and the tag Book builds on (`book-view-1.2` today; a new one is cut each time Manuscript moves to a newer core). Its user guide is `docs/guide/`.
- **Rules:** its [`AGENTS.md`](https://github.com/jamescjfoundation/wordsmith-manuscript/blob/main/AGENTS.md).

### wordsmith-book

[github.com/jamescjfoundation/wordsmith-book](https://github.com/jamescjfoundation/wordsmith-book)

- **Owns:** Wordsmith Book, the app that designs and typesets print books and ebooks. Designs, editions, print typesetting, the ebook writer, preflight, the `.wsbk` project folder and its packed form `.wsbkz` (`docs/format.md`, `docs/design-format.md`).
- **Stack:** Rust on open-source-core, and on Manuscript's `manuscript-model` and `manuscript-format` crates. Crates `book-model`, `book-format`, `book-design`, `book-import`, `book-typeset`, `book-epub`, `book-check`, `book-ui` in `crates/`; programs `book`, `book-cli` in `apps/`.
- **Publishes:** release files on its GitHub releases page (none yet), which the app's update check reads. Its user guide is `docs/guide/`.
- **Rules:** its [`AGENTS.md`](https://github.com/jamescjfoundation/wordsmith-book/blob/main/AGENTS.md).

### open-source-core

[github.com/jamescjfoundation/open-source-core](https://github.com/jamescjfoundation/open-source-core)

- **Owns:** what every app needs and none should write twice: the `jcj-` crates (document model, layout, engine, output, interchange, proofing, project files, theming, boards, entries, translation, shared features, the shell, agent control), and `template/`, the starting point for a new app and the source of the files every app carries.
- **It is general.** Other projects can build on it, so its code holds no product name, brand, or screenplay, manuscript or book concept. Wordsmith-wide rules live here in `project/`, not in the core.
- **Stack:** Rust. It is the only place that depends on the upstream projects, through `jcj-upstream`.
- **Publishes:** release tags (`v0.1.17` and so on) with a GitHub release each. Apps name a tag. `CHANGELOG.md` says what each release asks of the apps.
- **Rules:** its [`AGENTS.md`](https://github.com/jamescjfoundation/open-source-core/blob/main/AGENTS.md).

### The forks: wordcraft and craft-libs

[github.com/jamescjfoundation/wordcraft](https://github.com/jamescjfoundation/wordcraft) and [github.com/jamescjfoundation/craft-libs](https://github.com/jamescjfoundation/craft-libs)

- **Own:** our copies of the two upstream projects the core builds on, forked from `storytold/wordcraft` and `storytold/craft-libs`. The `jcj` branch of the WordCraft fork is the pinned upstream release plus our patches, one commit each; each patch also has a topic branch.
- **Publish:** the commits the core's patch block points at. Nothing else builds from them.
- **Rules:** upstream code is edited only on a fork's topic branch, and only as the core's [`docs/UPSTREAM.md`](https://github.com/jamescjfoundation/open-source-core/blob/main/docs/UPSTREAM.md) describes.

## How they depend on each other

```
 storytold/wordcraft, storytold/craft-libs      (upstream, not ours)
                 |  forked
     wordcraft, craft-libs                      (our forks)
                 |  the patch block in Cargo.toml
          open-source-core                      (jcj- crates, template/)
          /        |         \   one release tag on every jcj- line, plus `cargo xtask sync`
   Script     Manuscript  -->  Book             (Book builds on Manuscript's model and format crates)
      \________.wss__/                          (Manuscript reads Script's files)
          \        |         /   brand files in, guide + changelog + releases out
               wordsmith                        (brand kit, website, wiki, this map)
```

| From → to | What crosses | How it is held |
| --- | --- | --- |
| Each app → open-source-core | The `jcj-` crates | A git dependency on every `jcj-` line of the app's root `Cargo.toml`, all at the same release tag. `cargo xtask core-pin` (part of `cargo xtask ci`) fails if two tags are named or the lock file holds two cores |
| Each app → open-source-core | Shared settings and tooling: the toolchain, format and lint settings, `deny.toml`, the shared `xtask/src/` modules, `.github/workflows/ci.yml` and `core-pin.yml`, `hooks/`, the patch block in `Cargo.toml` | `cargo xtask sync` copies them from the pinned core release; `cargo xtask sync --check` (part of `cargo xtask ci`) fails if they differ. They are changed in the core, never in the app |
| Each app → open-source-core | The shared rules: marked blocks in `AGENTS.md`, `SECURITY.md` and `CONTRIBUTING.md`, and the whole `CODE_OF_CONDUCT.md` | The same `cargo xtask sync` and `--check`, from core v0.1.17 on. Their source is the core's `template/` ([Route N](#route-n)) |
| Each app → wordsmith (the map) | The project block at the top of this file | A copy in the app's `AGENTS.md`, written by `python3 project/carry.py --write` here and checked by this repository's `carried.yml` workflow ([Route N](#route-n)) |
| wordsmith → open-source-core | The core's `public` block ("What is public") | A copy in this repository's `AGENTS.md`, written and checked by the same tool against the core's newest release |
| open-source-core → the forks | WordCraft and craft-libs code | The patch block in the core's `Cargo.toml` points the upstream names at our fork's commits; `cargo xtask pins` checks it against `docs/UPSTREAM.md`. Apps never name an upstream crate or type |
| Book → Manuscript (code) | The crates `wordsmith-manuscript-model` and `wordsmith-manuscript-format` | Git dependencies in Book's `Cargo.toml` at a Manuscript tag `book-view-1.N`, cut on the same core release Book pins (Book's `Cargo.toml` names the current one). The contract is Manuscript's [`docs/book-handoff.md`](https://github.com/jamescjfoundation/wordsmith-manuscript/blob/main/docs/book-handoff.md) |
| Book → Manuscript (files) | `.wsm` project folders and `.wsmz` packed projects, read; an offers file written beside the project | Book never writes a Manuscript project. It reads Manuscript's project schema, so a schema change in Manuscript reaches Book |
| Manuscript → Script (files) | `.wss` files kept inside a Manuscript project, shown read-only | Manuscript's own reader, `crates/manuscript-io/src/screenplay.rs`. The format is Script's, in its [`docs/format.md`](https://github.com/jamescjfoundation/wordsmith-script/blob/main/docs/format.md) |
| Each app → wordsmith (brand) | Logos, icons, the palette card | Copies in the app's `assets/brand/`, taken from `brand/wordsmith-<app>/production/` here |
| wordsmith → each app (facts) | What the wiki and the website say about an app | Written by hand from the app's `docs/guide/`, `CHANGELOG.md` and releases |
| Each app → its GitHub releases | The in-app update check | The only network request an app makes on its own; it reads the app's own published releases and can be turned off |

Book and Manuscript move to a new core together, Manuscript first: Book's graph holds one core release, so the book-view tag Book pins must be cut on the core release Book pins ([Route I](#route-i)).

## Routes

Each route is a list of steps. Follow the repository's own `AGENTS.md` at every step that happens inside it.

<a id="route-a"></a>
### Route A: a core change an app needs

For a bug in a `jcj-` crate found from an app, or a feature that any app would share. The decision tree "Building between an app and the core" in each app's `AGENTS.md` says whether a change belongs in the core.

1. Open an issue in [open-source-core](https://github.com/jamescjfoundation/open-source-core/issues) that describes the general need, not the app's feature.
2. Have the core as a sibling folder of the app (see [Route M](#route-m)). In the app, run `cargo xtask dev-link ../open-source-core`, so the app builds against your core checkout.
3. Build the general part in the core, with its own tests and a use in `apps/core-testbed`. No product name, color, logo, or screenplay, manuscript or book idea goes into the core.
4. Build the app's use of it in the app. Never change a core interface from the app's side, and never work around a core bug in the app.
5. In the core, run `cargo xtask ci`, land the change, and release the core ([Route I](#route-i)).
6. In the app, run `cargo xtask dev-unlink`, move the app to the new core release ([Route I](#route-i), step 5), run `cargo xtask ci`, and land the app's change. Name the core issue in it.

If the general shape is not clear yet, build it in the app first: mark the code `// core-candidate: open-source-core#N` with the number of a core issue labelled `core-candidate`, and move it later. When it moves, delete the app's copy and its marker in the same change. Never copy code from one app repository into another.

**Today:**

- `dev-link` writes the link, with the full path of your core checkout, into the app's tracked `.cargo/config.toml`, and a build while linked changes `Cargo.lock`. Commit neither. After `dev-unlink`, run `git restore Cargo.lock` before the gate, or its `--locked` checks fail.
- `dev-link` links only the core. It cannot link Manuscript into Book.
- An app's CI builds only against a released core tag, so the app's half of a change is checked in CI only after the core release exists.
- Book lists what it needs from the core in its `docs/core-candidates.md`. Script and Manuscript have no such list; their markers and the core's issues are the record.

<a id="route-b"></a>
### Route B: something one app needs from another

Two pairs exist: Book builds on Manuscript's crates and reads its projects, and Manuscript reads Script's `.wss` files. The rule is the same for any pair ([decision 0004](decisions/0004-apps-that-depend-on-apps.md)).

1. The providing app owns the contract. For Book and Manuscript it is Manuscript's [`docs/book-handoff.md`](https://github.com/jamescjfoundation/wordsmith-manuscript/blob/main/docs/book-handoff.md); for `.wss` it is Script's [`docs/format.md`](https://github.com/jamescjfoundation/wordsmith-script/blob/main/docs/format.md).
2. A need goes in as an issue in the providing app's repository. Say what is needed and why, and name the consuming app. An agent may open it.
3. The change is made in the providing app, as its own change under its own rules. A change in the consuming app never edits the provider's repository.
4. The provider lands first. For Book, Manuscript then cuts a new book-view tag and Book moves its two `wordsmith-manuscript-` lines to it. Then the consumer's change lands ([Route L](#route-l)).
5. When you change a provider, check the consumer before you land:
   - `manuscript-model`, `manuscript-format` or the `.wsm` project schema: Book builds on them. Open a Book issue for any change Book must follow.
   - The `.wss` format: Manuscript reads it. Open a Manuscript issue when the format version changes.
6. If a third app would need the same thing, it belongs in the core: use [Route A](#route-a).

**Today:**

- Book's needs from Manuscript are listed in Book's `docs/requests-to-manuscript.md` and have not been filed as Manuscript issues yet. File a new need as an issue and add its link to that file.
- The book-view tag has no written scheme yet. `book-view-1.2` is the view's version (1), then a count of tags cut for it. Nothing in Manuscript's CI builds Book. A breaking change shows only when Book moves to a new tag.
- Manuscript's `.wss` reader does not check the format version it is given.

<a id="route-c"></a>
### Route C: a change users will see in an app

1. In the app: make the change, update the page in the app's `docs/guide/`, and add a `CHANGELOG.md` line. Manuscript and Book also add a line to `docs/progress.md`.
2. If screenshots changed, redraw them ([Route G](#route-g)).
3. In wordsmith: update the app's wiki pages ([Route D](#route-d)). If the change finishes something the wiki marks as planned, change its `<Status>` mark and the app's `whats-next.mdx`.
4. In wordsmith: if the app's status, feature list or platforms changed, update the website text ([Route E](#route-e)).
5. Land the app's change first, then the wordsmith change, which names the app's commit or pull request ([Route L](#route-l)).

**Today:** each app has two user guides, `docs/guide/` in its own repository and its section of the wiki, written separately. Neither is declared the source, so update both. The website's "Read the guide" buttons point at the app's `docs/guide/`.

<a id="route-d"></a>
### Route D: a wiki page

"The wiki" always means the one in this repository, published at [wordsmithand.ink/wiki/](https://wordsmithand.ink/wiki/). It is not the app's `docs/guide/` and not the wiki tab on GitHub.

1. Work in the wordsmith repository. Pages are MDX in `website/wiki/content/docs/`: `script/`, `manuscript/`, `book/`, and `start/` for what the apps share.
2. Take the facts from the app's repository: its `docs/guide/`, `CHANGELOG.md` and code. Document only what the app does today; mark anything not built with `<Status value="planned" />` or `"in-progress"`. Never use an app's `.private/` notes.
3. Add or edit the page, and list a new page in the folder's `meta.json`, which sets the order. `website/wiki/README.md` has the frontmatter, the components and the picture rules.
4. In `website/wiki`, run `npm install` once, then `npm run brand:check`, `npm run lint` and `npm run build`. All three must pass.
5. Land it on `main`. The push deploys the site and the wiki together; the page is live when the "Deploy website and wiki to GitHub Pages" run is green. Open the live page to check it.

**Today:** a pull request in this repository gets no automatic check, so step 4 is the only check before the deploy.

<a id="route-e"></a>
### Route E: website text

1. Work in the wordsmith repository. All page text, the header and the footer are in `website/tools/build.py`. Never edit the `.html` pages by hand.
2. Run `python3 website/tools/build.py` from the repository root and commit the regenerated pages with the script.
3. Preview with `python3 website/tools/serve.py`. Check phone width, dark mode and every link you touched.
4. Say only what is true of the apps today. Check the app's repository and its releases page before you change a status word.
5. Land it on `main`; the push deploys it.

**Today:** each app's status ("no downloads yet", "in development") is written out in `build.py` and across the wiki pages, not read from one place. When an app's status changes, search both for the old words.

<a id="route-f"></a>
### Route F: a logo, icon or brand color

The brand kit in `brand/` here is the source. A logo, icon or palette file is never edited, recolored or redrawn anywhere else.

1. Read `brand/suite/BRAND_GUIDE.md`. Change the script in `brand/source/`, run `python3 brand/source/build.py` to see what changes, then again with `--write` (add `--pdf` for the guideline PDFs). `brand/README.md` has the setup.
2. Update by hand the files the build does not write: the kit's READMEs, `BRAND_GUIDE.md` and each `tokens.json`.
3. Copies in this repository: run `npm run brand` in `website/wiki` (it writes `website/wiki/public/brand/`; `npm run brand:check` verifies it), and copy the changed files into `website/assets/brand/` by hand.
4. Copies in each app: copy the changed files from `brand/wordsmith-<app>/production/` and `app-icon/` into the app's `assets/brand/`, unchanged, as a change in that app's repository that names the wordsmith commit.
5. In each app, remake the files the app derives from the kit, and run `cargo xtask ci` (its `assets` check wants every file under `assets/` listed in `ATTRIBUTION.md`).

What an app owns and may edit: its interface theme file (`assets/brand/tokens.json` in Manuscript and Book, `assets/brand/script/tokens.json` in Script), which is in the core's token format and is not a copy of the kit's `tokens.json`; and the files it derives from the kit with its own tool (Manuscript's `tools/brand-icons.py`, Book's `tools/brand-mask.py`). The seven palette colors in a theme file must match the kit.

**Today:** only the wiki's copies are checked. The copies in `website/assets/brand/` and in the apps are made by hand, and nothing reports one that is out of date, so step 4 is easy to miss. Script's `mark-mask.png` and `wordmark-mask.png` have no tool that makes them.

<a id="route-g"></a>
### Route G: screenshots

1. In the app, run `cargo xtask screenshots`. The app draws its own pictures into `docs/images/`. Never use a screenshot of a real desktop.
2. Land them in the app.
3. In wordsmith, replace the WebP copies: `website/wiki/content/docs/<app>/images/` for the wiki, and `website/assets/img/` for the website. Keep the file names the pages already use.

**Today:** the copies are converted to WebP and cropped by hand (the title bar is cut off); no script does it. Book has no pictures in the wiki yet, and the website still shows drawn illustrations for Manuscript and Book.

<a id="route-h"></a>
### Route H: a security problem

1. Do not describe it in a commit, branch name, comment, issue, pull request or any tracked file, in any repository.
2. Write it up in `.private/` in the checkout you are working in (ignored by Git in all five repositories) and tell the maintainer you are working for.
3. A problem in shared code (the window, saving, import and export, updates, agent control) belongs to the core even when you found it from an app. Do not open an app issue or a core issue for it. It is fixed in the core, on a branch with a neutral name, with a test that would have caught it.
4. After the fix: release the core and move every app to it ([Route I](#route-i)). A problem in one app's own code is fixed and released in that app the same way.
5. Disclosure comes after the release: the advisory, and a **Security** entry in the changelog. Each Rust repository's `SECURITY.md` has the details.

**Today:** each `SECURITY.md` sends outside reporters to GitHub's private reporting on the repository's Security tab. Check that the tab offers "Report a vulnerability" before you send anyone there. The wordsmith repository has no `SECURITY.md` yet. A `.private/` folder inside a worktree goes away with the worktree, so tell the maintainer before the thread ends.

<a id="route-i"></a>
### Route I: a core release, and moving an app to a newer core

Releasing the core:

1. Everything for the release is on the core's `main` and `cargo xtask ci` passes there.
2. Make the release commit: the new version in `Cargo.toml` and `Cargo.lock`, the new tag on the `jcj-` lines of `template/Cargo.toml`, and a `CHANGELOG.md` section with **What apps must do**. While the core is at 0.x, a patch release only adds or fixes; anything that breaks an app is a minor release and says exactly what each app changes.
3. Push the commit. Run the core's Nightly workflow on it by hand (`gh workflow run nightly.yml --ref main`): that is the full gate on Linux, macOS and Windows.
4. When that run is green, push the tag `vX.Y.Z`. The tag starts the Release workflow, which runs the gate again and publishes the GitHub release. No tag goes on a commit whose gate has not passed. A person or an agent may cut the release ([decision 0002](decisions/0002-how-changes-land-and-who-releases.md)).

Moving an app to it:

5. In the app's root `Cargo.toml`, change the tag on every `jcj-` line; they all carry the same tag. Run `cargo metadata --format-version 1 > /dev/null` so `Cargo.lock` follows; do not run a blanket `cargo update`.
6. Run `cargo xtask sync` to take the core-owned files of that release, and again until `cargo xtask sync --check` passes: a release that adds core-owned files needs two runs.
7. Read **What apps must do** in the core's [`CHANGELOG.md`](https://github.com/jamescjfoundation/open-source-core/blob/main/CHANGELOG.md) for every release between the old tag and the new one, and do it.
8. Run `cargo xtask ci`. A golden file that changes is a deliberate change: review it and record it in the app's `docs/golden.md`.
9. Script also names its core tag in its top-level `UPSTREAM.md`; update that line.

When to move: before starting new work on an app and before releasing it. `cargo xtask core-pin --behind` prints how far behind an app is, and a weekly workflow in each app (`core-pin.yml`) opens an issue there when it is more than three releases behind ([decision 0002](decisions/0002-how-changes-land-and-who-releases.md)).

**Today:**

- Nothing stops a tag being pushed before the gate has run; steps 3 and 4 are kept by whoever cuts the release.
- Nothing builds the real apps against a core change before it is released; the core's own check builds only the template app.
- Moving Book takes two steps by hand: Manuscript moves to the new core and cuts a new book-view tag, then Book moves its core tag and its Manuscript tag in one change. `cargo xtask core-pin` fails in Book until both are done.

<a id="route-j"></a>
### Route J: an app release

1. Move the app to the newest core first ([Route I](#route-i)).
2. In the app: set the version, finish the `CHANGELOG.md` section, and run `cargo xtask ci`.
3. Start the app's release workflow, the way that app's `.github/workflows/release.yml` says:
   - Script: push to the `release` branch. The workflow builds a draft release; it is published by hand on GitHub, or by starting the workflow on that branch with "publish" ticked.
   - Manuscript and Book: push a tag `vX.Y.Z`. The workflow publishes the release.
4. Check the published release: the files for each platform are there, and the app's update check finds them.
5. In wordsmith, the same day: the app's status and download words on the website ([Route E](#route-e)), and in the wiki the `<Status>` marks, the app's `whats-next.mdx` and `start/install.mdx` ([Route D](#route-d)).

A person or an agent may release an app once its gate passes ([decision 0002](decisions/0002-how-changes-land-and-who-releases.md)).

**Today:**

- No app has published a release, so none of the three workflows has run. Treat the first release of each app as a test of its workflow, and read the workflow before starting it.
- The three workflows differ in trigger, platforms, file names and checksum files. There is no shared release contract yet.
- Nothing in an app's release tells this repository. Step 5 is done by hand.

<a id="route-k"></a>
### Route K: a change in WordCraft or craft-libs

1. Apps never name WordCraft or craft-libs crates or types. If an app needs something from upstream, it needs it from a `jcj-` interface: use [Route A](#route-a).
2. In the core, the adapters in `jcj-upstream` and the `jcj-` crate that wraps them change first. Most needs end there.
3. If upstream code itself must change, it changes in our fork, on a topic branch, one commit per patch, and is recorded under "Carried patches" in the core's [`docs/UPSTREAM.md`](https://github.com/jamescjfoundation/open-source-core/blob/main/docs/UPSTREAM.md). Nowhere else.
4. Moving to a newer upstream release follows "The two-week train" in that file: move the pins, rebuild the fork's `jcj` branch, run the contract tests, decide follow, hold or own for each source, release the core, move the apps ([Route I](#route-i)). `cargo xtask pins` checks the pins against the file.
5. The patch block reaches each app through `cargo xtask sync`.

<a id="route-l"></a>
### Route L: a change that spans two repositories

1. Split it into one change per repository. Each must pass its own repository's gate.
2. Use the same branch name in each repository, one that says what the change is (`shell/tree-drag`, `wiki/book-export`). No names of people or machines.
3. The provider lands first:

   | Pair | First | Then |
   | --- | --- | --- |
   | Core and an app | The core, and its release | The app's pin and the app's change |
   | Manuscript and Book | Manuscript, and a new book-view tag | Book |
   | Script and Manuscript (`.wss`) | Script | Manuscript |
   | An app and wordsmith (wiki, website) | The app | wordsmith |
   | wordsmith (brand) and an app | wordsmith | The app's copies |

4. Each change names the other in full, as `jamescjfoundation/<repository>#<number>` for an issue or pull request, or the commit's address. The second change says which first change it needs.
5. Do not land the second change until the first is on `main` and, where a release or tag carries it, released.

<a id="route-m"></a>
### Route M: working with all the repositories, or with only one

**Side by side.** Clone the repositories as sibling folders with their own names, so `../open-source-core` from an app is the core:

```
wordsmith/  wordsmith-script/  wordsmith-manuscript/  wordsmith-book/  open-source-core/
```

- The folder that holds them is not a repository. Run `git`, `cargo`, `npm` and `gh` inside the repository they belong to.
- Each repository has its own history, branch and gate. Commit each one separately.
- In each Rust repository, run `cargo xtask install-hooks` once per clone: the hooks check formatting and privacy before a commit and run the changed-only gate before a push.

**Worktree threads.** When a tool gives a task its own checkout of every repository on a same-named branch:

- Change only that task's checkouts. Another checkout of the same repository is for reading.
- A new worktree has no `target/` folder, so the first build and the first push are slow.
- `.private/` notes in a worktree are lost with it.

**Only one repository.** The block at the top of this file is carried in each app's `AGENTS.md`, and this repository's `AGENTS.md` starts from this file, so the others can be found from any of them. The core is general and carries no block. When a route needs another repository, clone it beside the one you have (`git clone https://github.com/jamescjfoundation/<repository> ../<repository>`). To read one file, the links in this map go straight to it on GitHub.

<a id="route-n"></a>
### Route N: a rule or instruction that several repositories carry

Some text is the same, word for word, in several repositories. It sits between a `BEGIN` and an `END` marker line, it has one owner, and a copy is never edited: a tool writes the copies and a check fails when one differs.

| Block | Owner: edit it here | Carried in | Written by | Checked by |
| --- | --- | --- | --- | --- |
| The project block (`wordsmith project block`) | [`project/README.md`](#the-wordsmith-project-map) here | Each app's `AGENTS.md` | `python3 project/carry.py --write`, here | `.github/workflows/carried.yml`, here |
| The core's rules (`open-source-core: public`, `app-and-core`, `app`, `security`, `contributing`) | The core's `template/AGENTS.md`, `template/SECURITY.md`, `template/CONTRIBUTING.md` | Each app's file of the same name; `public` also in this repository's `AGENTS.md` | `cargo xtask sync` in each app; `python3 project/carry.py --write` here | `cargo xtask sync --check` in each app's gate; `carried.yml` here |

A block owned by the core:

1. In open-source-core, edit the block in the file under `template/`. Keep it general: it is read in every app, and `public` in this repository too, so it names no product and nothing only one repository has.
2. Run `cargo xtask template --write`, which copies the blocks into the core's own `AGENTS.md`, `SECURITY.md` and `CONTRIBUTING.md`, then `cargo xtask ci`.
3. Land it and release the core ([Route I](#route-i), steps 1 to 4).
4. Each app moves to that release ([Route I](#route-i), steps 5 to 9). `cargo xtask sync` writes the new block, and the app's gate fails until it has.
5. In wordsmith, run `python3 project/carry.py --write` and land the changed `AGENTS.md`.

The project block:

1. Edit it in `project/README.md`, between the two marker lines. Keep its links absolute, since it is read in other repositories.
2. With the apps as sibling folders ([Route M](#route-m)), run `python3 project/carry.py --write`. It writes the block into each app's `AGENTS.md`. It commits nothing.
3. Land the wordsmith change first. Then, in each app, commit and push the changed `AGENTS.md`, naming the wordsmith commit ([Route L](#route-l)).
4. The "Check the carried blocks" workflow here goes red at the wordsmith push and green once the last app has landed. Start it by hand with `gh workflow run carried.yml`, or run the same check yourself: `python3 project/carry.py --check --remote`.

`python3 project/carry.py` with no flag checks without writing. It reads the sibling folders where they exist, which can be ahead of or behind what is published; `--remote` reads each app's `main` and the core's newest release from GitHub. A file that is to carry a block needs the two marker lines first; the tool never guesses where a block belongs. To have another repository or file carry a block, add the marker lines there and a row to the table at the top of `project/carry.py`.

**Today:**

- An app's own gate does not check its copy of the project block. A copy edited by hand in an app is found by this repository's workflow, at the next push here or the weekly run, not at the app's push.
- This repository carries only `public`. It has no `SECURITY.md` or `CONTRIBUTING.md` yet, so `security` and `contributing` are not carried here.
- open-source-core carries no project block, because it names no product.

## Where to look, where to write

Paths are inside the repository named. Links go to `main`.

| Question or record | Where |
| --- | --- |
| How the repositories connect, and every route | This file |
| A rule or instruction that several repositories carry word for word | Its owner's file: the core's `template/` or the block at the top of this file ([Route N](#route-n)). Never a copy |
| A rule for the whole project, and why | [`project/decisions/`](decisions/README.md) here |
| What a `jcj-` crate does | The core's [`README.md`](https://github.com/jamescjfoundation/open-source-core/blob/main/README.md) crate table, then the crate's own docs |
| Why a shared interface, the upstream rule or the tooling is as it is | The core's [`docs/decisions/`](https://github.com/jamescjfoundation/open-source-core/tree/main/docs/decisions). Outside the core, write "core decision NNNN": the apps and this folder number their own decisions from 0001 too |
| Why one app behaves as it does | That app's `docs/decisions/` |
| An app's behavior, as specified | That app's `docs/SPEC.md` (Script also has `docs/SPEC-2.md`) |
| A file format | Script: [`docs/format.md`](https://github.com/jamescjfoundation/wordsmith-script/blob/main/docs/format.md) (`.wss`). Manuscript: [`docs/format.md`](https://github.com/jamescjfoundation/wordsmith-manuscript/blob/main/docs/format.md) (`.wsm`, `.wsmz`). Book: [`docs/format.md`](https://github.com/jamescjfoundation/wordsmith-book/blob/main/docs/format.md) and [`docs/design-format.md`](https://github.com/jamescjfoundation/wordsmith-book/blob/main/docs/design-format.md) (`.wsbk`, `.wsbkz`). The core's container: [`crates/jcj-project/FORMAT.md`](https://github.com/jamescjfoundation/open-source-core/blob/main/crates/jcj-project/FORMAT.md) |
| What Manuscript gives Book | Manuscript's [`docs/book-handoff.md`](https://github.com/jamescjfoundation/wordsmith-manuscript/blob/main/docs/book-handoff.md). Book's side: [`docs/handoff-review.md`](https://github.com/jamescjfoundation/wordsmith-book/blob/main/docs/handoff-review.md) and [`docs/requests-to-manuscript.md`](https://github.com/jamescjfoundation/wordsmith-book/blob/main/docs/requests-to-manuscript.md) |
| A need one app has of another | An issue in the providing app's repository ([Route B](#route-b)) |
| A need an app has of the core | A core [issue](https://github.com/jamescjfoundation/open-source-core/issues), labelled `core-candidate` when the code starts in the app. Book also lists its own in [`docs/core-candidates.md`](https://github.com/jamescjfoundation/wordsmith-book/blob/main/docs/core-candidates.md) |
| What a core release changed, and what apps must do | The core's [`CHANGELOG.md`](https://github.com/jamescjfoundation/open-source-core/blob/main/CHANGELOG.md) |
| What an app release changed | That app's `CHANGELOG.md` |
| Upstream pins, carried patches, follow / hold / own | The core's [`docs/UPSTREAM.md`](https://github.com/jamescjfoundation/open-source-core/blob/main/docs/UPSTREAM.md) |
| What is missing or planned in an app | Script: `docs/gaps.md` and `ROADMAP.md`. Manuscript and Book: `docs/PLAN.md` (both plans are finished) and `docs/progress.md`. **Today:** no repository keeps one live list of what is planned |
| What was done, step by step | Each app's `docs/progress.md`; the core's `CHANGELOG.md` |
| How users do something in an app | The app's `docs/guide/`, and the app's section of the wiki, `website/wiki/content/docs/<app>/` here ([Route C](#route-c)) |
| What the public is told about the apps | `website/tools/build.py` and `website/wiki/content/docs/start/` here |
| Brand rules, logos, icons, colors | `brand/suite/BRAND_GUIDE.md` and `brand/README.md` here. An app's interface theme: its own `tokens.json`, in the format of the core's [`crates/jcj-theme/TOKENS.md`](https://github.com/jamescjfoundation/open-source-core/blob/main/crates/jcj-theme/TOKENS.md) |
| Test data and reference outputs | Each app's `docs/golden.md`; Manuscript's and Book's `docs/fixtures.md` |
| Credits for assets and dependencies | Each Rust repository's `ATTRIBUTION.md` and `NOTICE` |
| How to report or handle a security problem | Each Rust repository's `SECURITY.md`; [Route H](#route-h) |
| Security notes, reviews, audits, working notes | `.private/` in the repository you are in, never tracked ([Project rules](#project-rules)) |

## Project rules

These hold in every Wordsmith repository. Each repository's `AGENTS.md` adds its own.

- **How changes land.** While no app has been released, a change may be pushed straight to `main`. Run the repository's gate first (`cargo xtask ci` in the Rust repositories; the checks in `AGENTS.md` here). A pull request is optional, and its author merges it once the checks pass. A red `main` is fixed at once by whoever made it red. [Decision 0002](decisions/0002-how-changes-land-and-who-releases.md).
- **Who releases.** A person or an agent may release the core or an app, once the release's gate passes. [Decision 0002](decisions/0002-how-changes-land-and-who-releases.md).
- **Core pins.** An app moves to the newest core release before new work starts on it and before it is released. An app more than three core releases behind gets an issue. [Decision 0002](decisions/0002-how-changes-land-and-who-releases.md), [Route I](#route-i).
- **Naming other companies, programs and formats.** Code and docs may name them where it is a fact a reader needs: the formats an app opens, what a store or print service expects of a file. Interface names, designs and help text stay our own, and an app never says it replaces or follows another product. Apps never name WordCraft or craft-libs types. People are never named. [Decision 0003](decisions/0003-naming-other-companies-programs-and-formats.md).
- **Apps that depend on apps.** Allowed, under a contract the providing app owns. [Decision 0004](decisions/0004-apps-that-depend-on-apps.md), [Route B](#route-b).
- **Where project-wide things live.** Here, in `project/`. The core holds only what is general to any app built on it. A decision about one app stays in that app. [Decision 0001](decisions/0001-where-project-wide-things-live.md).
- **What is public.** Every repository is public, history included, for good. No commit, branch name, issue, pull request, comment or tracked file holds a person's name or email, an account name, details of a machine (home-folder paths, user or host names, addresses), anything said in a conversation, an open security problem, a secret, a file from a real machine, or anyone's private writing. Commit with a GitHub no-reply address. Never push with `--all` or `--mirror`.
- **Reviews and working notes.** Reviews, audits and working notes stay in `.private/`, which every repository ignores. One is published only when a maintainer says so, and then under `docs/history/`, labelled as history.
- **The Foundation's name** is always "The James C. J. Foundation". **Today:** older text in the core and the apps uses a shorter form; do not copy it into new text.
- **Product names** are "Wordsmith", "Wordsmith & Ink", "Wordsmith Script", "Wordsmith Manuscript", "Wordsmith Book" and "Wordsmith Launcher", written exactly so. They are trademarks.
- **Licensing.** Code is MIT OR Apache-2.0. A new dependency must have a compatible license (the core's license allowlist decides for the Rust repositories) and is credited. Bundled fonts are under the SIL Open Font License.
- **Privacy.** No telemetry, analytics, accounts, trackers or third-party requests, in the apps or on the site. The only network request an app makes on its own is the update check with its GitHub releases, and it can be turned off.
- **Writing.** Plain, short sentences, for writers in user-facing text. Say only what exists; mark planned things as planned.
- **Never** copy code from one app repository into another, and never edit upstream code outside our forks.
