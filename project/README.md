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
- Each app takes its logos, icons and palette from the brand kit, unchanged, by the kit's tool. Each app's `docs/guide/` is its one user guide: the wiki's pages for the app are built from it. The website and the wiki read each app's latest release from its GitHub releases.

| The change | Where it goes | Route |
| --- | --- | --- |
| A fix in a `jcj-` crate, or something any app would share | open-source-core first, then the app's pin | [A](https://github.com/jamescjfoundation/wordsmith/blob/main/project/README.md#route-a) |
| Something one app needs from another app | An issue in the providing app's repository | [B](https://github.com/jamescjfoundation/wordsmith/blob/main/project/README.md#route-b) |
| A change users will see in an app | The app's `docs/guide/` and `CHANGELOG.md`; then wordsmith builds the wiki's pages from the guide | [C](https://github.com/jamescjfoundation/wordsmith/blob/main/project/README.md#route-c) |
| A wiki page | About one app: that app's `docs/guide/`, never the wiki's copy. About the project: wordsmith, `website/wiki/content/docs/start/` | [D](https://github.com/jamescjfoundation/wordsmith/blob/main/project/README.md#route-d) |
| Website text, or the words for an app's state on the site | wordsmith, `website/tools/build.py` and `website/data/apps/` | [E](https://github.com/jamescjfoundation/wordsmith/blob/main/project/README.md#route-e) |
| A logo, icon or brand color | wordsmith, `brand/source/`; then its tool writes the copies into each app's `assets/brand/` | [F](https://github.com/jamescjfoundation/wordsmith/blob/main/project/README.md#route-f) |
| Screenshots | Drawn in the app into `docs/images/`; wordsmith's tool carries them | [G](https://github.com/jamescjfoundation/wordsmith/blob/main/project/README.md#route-g) |
| A security problem | Never public: `.private/` and a maintainer | [H](https://github.com/jamescjfoundation/wordsmith/blob/main/project/README.md#route-h) |
| A core release, or moving an app to a newer core | open-source-core, then each app | [I](https://github.com/jamescjfoundation/wordsmith/blob/main/project/README.md#route-i) |
| An app release | The app; the website and wiki pick it up by themselves | [J](https://github.com/jamescjfoundation/wordsmith/blob/main/project/README.md#route-j) |
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

Each route ends with a **Held by:** line. It names what checks the route or refuses a wrong step, and says what nothing checks. A task named there (`core-pin`, `sync`, `layers`, `docs`) is a task of `cargo xtask ci`, the gate of each Rust repository and of the launcher in `launcher/` here; "on GitHub" means a setting of the repository there, which refuses the step for everyone.

## The repositories

All are public, under [github.com/jamescjfoundation](https://github.com/jamescjfoundation), with `main` as the default branch.

### wordsmith

[github.com/jamescjfoundation/wordsmith](https://github.com/jamescjfoundation/wordsmith)

- **Owns:** everything that belongs to the project as a whole. `project/` (this map and the project's decisions), `brand/` (the brand kit, the source of every logo, icon and brand color), `website/` (the public site), `website/wiki/` (the wiki), `launcher/` (Wordsmith Launcher, the program that installs, updates, opens and removes the three apps).
- **Stack:** Python 3 scripts for the brand kit and the website pages; Fumadocs on Next.js for the wiki, with Node.js scripts that build its app sections. Rust in one folder: `launcher/` is a Cargo workspace of its own, built on open-source-core like an app, with the program `wordsmith-launcher`. The rest of the repository has no Cargo.
- **Publishes:** [wordsmithand.ink](https://wordsmithand.ink/) and [wordsmithand.ink/wiki/](https://wordsmithand.ink/wiki/), by `.github/workflows/pages.yml` on every push to `main` that touches `website/`, and each day an app has published a release, after every check in `.github/workflows/checks.yml` has passed. And the launcher's release files, on this repository's GitHub releases page: a tag `vX.Y.Z` here is a version of the launcher ([Route J](#route-j)).
- **Licenses:** by folder, in [`LICENSES.md`](../LICENSES.md): code is MIT OR Apache-2.0, the words of the website and the wiki are CC BY 4.0, and the brand files are not open source.
- **Rules:** [`AGENTS.md`](../AGENTS.md); for the launcher, [`launcher/AGENTS.md`](../launcher/AGENTS.md), which carries the core's rules for apps.

### wordsmith-script

[github.com/jamescjfoundation/wordsmith-script](https://github.com/jamescjfoundation/wordsmith-script)

- **Owns:** Wordsmith Script, the app for screenplays, TV and stage plays. The screenplay rules (elements, typing, pagination, Fountain, scene numbers, reports) and the `.wss` file format (`docs/format.md`).
- **Stack:** Rust on open-source-core. Crates `wordsmith-script`, `wordsmith-format`, `wordsmith-ui` in `crates/`; programs `wordsmith`, `wordsmith-cli`, `wordsmith-web` in `apps/`.
- **Publishes:** release files on its GitHub releases page, which the app's update check and the launcher read. Its user guide is `docs/guide/`, the source of its section of the wiki ([Route C](#route-c)).
- **Rules:** its [`AGENTS.md`](https://github.com/jamescjfoundation/wordsmith-script/blob/main/AGENTS.md).

### wordsmith-manuscript

[github.com/jamescjfoundation/wordsmith-manuscript](https://github.com/jamescjfoundation/wordsmith-manuscript)

- **Owns:** Wordsmith Manuscript, the app for novels and long work. The binder, the story bible, import and export, the `.wsm` project folder and its packed form `.wsmz` (`docs/format.md`), and the book view that Wordsmith Book reads (`docs/book-handoff.md`).
- **Stack:** Rust on open-source-core. Crates `manuscript-model`, `manuscript-format`, `manuscript-io`, `manuscript-ui` in `crates/`; programs `manuscript`, `manuscript-cli`, `manuscript-web` in `apps/`.
- **Publishes:** release files on its GitHub releases page, which the app's update check and the launcher read; and the tag Book builds on (`book-view-1.3` today; a new one is cut each time Manuscript moves to a newer core). Its user guide is `docs/guide/`, the source of its section of the wiki ([Route C](#route-c)).
- **Rules:** its [`AGENTS.md`](https://github.com/jamescjfoundation/wordsmith-manuscript/blob/main/AGENTS.md).

### wordsmith-book

[github.com/jamescjfoundation/wordsmith-book](https://github.com/jamescjfoundation/wordsmith-book)

- **Owns:** Wordsmith Book, the app that designs and typesets print books and ebooks. Designs, editions, print typesetting, the ebook writer, preflight, the `.wsbk` project folder and its packed form `.wsbkz` (`docs/format.md`, `docs/design-format.md`).
- **Stack:** Rust on open-source-core, and on Manuscript's `manuscript-model` and `manuscript-format` crates. Crates `book-model`, `book-format`, `book-design`, `book-import`, `book-typeset`, `book-epub`, `book-check`, `book-ui` in `crates/`; programs `book`, `book-cli` in `apps/`.
- **Publishes:** release files on its GitHub releases page, which the app's update check and the launcher read. Its user guide is `docs/guide/`, the source of its section of the wiki ([Route C](#route-c)).
- **Rules:** its [`AGENTS.md`](https://github.com/jamescjfoundation/wordsmith-book/blob/main/AGENTS.md).

### open-source-core

[github.com/jamescjfoundation/open-source-core](https://github.com/jamescjfoundation/open-source-core)

- **Owns:** what every app needs and none should write twice: the `jcj-` crates (document model, layout, engine, output, interchange, proofing, project files, theming, boards, entries, translation, shared features, the shell, agent control), and `template/`, the starting point for a new app and the source of the files every app carries.
- **It is general.** Other projects can build on it, so its code holds no product name, brand, or screenplay, manuscript or book concept. Wordsmith-wide rules live here in `project/`, not in the core.
- **Stack:** Rust. It is the only place that depends on the upstream projects, through `jcj-upstream`.
- **Publishes:** release tags (`v0.1.18` and so on) with a GitHub release each. Apps name a tag. `CHANGELOG.md` says what each release asks of the apps.
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
                   |
           launcher/ in wordsmith               (built on open-source-core; installs the three apps from their releases)
```

| From → to | What crosses | How it is held |
| --- | --- | --- |
| Each app → open-source-core | The `jcj-` crates | A git dependency on every `jcj-` line of the app's root `Cargo.toml`, all at the same release tag. `cargo xtask core-pin` (part of `cargo xtask ci`) fails if two tags are named or the lock file holds two cores |
| Each app → open-source-core | Shared settings and tooling: the toolchain, format and lint settings, `deny.toml`, the shared `xtask/src/` modules, the shared gate behind each app's `xtask/src/main.rs`, `.github/workflows/ci.yml` and `core-pin.yml` (short callers of the core's shared workflows at its tag `workflows-v1`), `.github/dependabot.yml`, `hooks/`, the pull request template, and marked blocks in `Cargo.toml` (patches, lints and profiles), `.cargo/config.toml`, `.gitignore` and `.gitattributes` | `cargo xtask sync` copies them from the pinned core release; `cargo xtask sync --check` (part of `cargo xtask ci`) fails if they differ. They are changed in the core, never in the app |
| Each app → open-source-core | The shared rules: marked blocks in `AGENTS.md`, `SECURITY.md` and `CONTRIBUTING.md`, and the whole `CODE_OF_CONDUCT.md` | The same `cargo xtask sync` and `--check`, from core v0.1.17 on. Their source is the core's `template/` ([Route N](#route-n)) |
| Each app → wordsmith (the map) | The project block at the top of this file | A copy in the app's `AGENTS.md`, written by `python3 project/carry.py --write` here and checked by this repository's `carried.yml` workflow ([Route N](#route-n)) |
| The launcher → open-source-core | The `jcj-` crates, and everything an app carries: the shared settings and tooling, the shared gate, the marked blocks and the code of conduct | In `launcher/` here, as in an app: one release tag on its `jcj-` line, and `cargo xtask sync` with `sync --check` in its gate (`cargo xtask ci`, run by `launcher.yml`). The core's workflow files and hooks are carried and do not run in a folder: the workflows that run are the launcher's own, at this repository's root ([launcher decision 0001](../launcher/docs/decisions/0001-an-app-in-a-folder-of-the-wordsmith-repository.md)) |
| The launcher → each app (releases) | The newest release's version, its file for the user's system, and `SHA256SUMS.txt` | Read from each app's public releases on GitHub, by the core's release contract ([`docs/app-releases.md`](https://github.com/jamescjfoundation/open-source-core/blob/main/docs/app-releases.md), "For a launcher or a website"): the file's name, its line in the checksum file, the place of the program in a package. The launcher's tests read the three apps' recorded 0.9.0 releases, and `cargo xtask live` (in `launcher.yml`) installs a real release on Linux, macOS and Windows |
| wordsmith → open-source-core | The core's `public`, `security` and `contributing` blocks and its code of conduct | Copies in this repository's `AGENTS.md`, `SECURITY.md`, `CONTRIBUTING.md` and `CODE_OF_CONDUCT.md`, written and checked by the same tool against the core's newest release |
| open-source-core → the forks | WordCraft and craft-libs code | The patch block in the core's `Cargo.toml` points the upstream names at our fork's commits; `cargo xtask pins` checks it against `docs/UPSTREAM.md`. Apps never name an upstream crate or type |
| Book → Manuscript (code) | The crates `wordsmith-manuscript-model` and `wordsmith-manuscript-format` | Git dependencies in Book's `Cargo.toml` at a Manuscript tag `book-view-1.N`, cut on the same core release Book pins (Book's `Cargo.toml` names the current one). The contract is Manuscript's [`docs/book-handoff.md`](https://github.com/jamescjfoundation/wordsmith-manuscript/blob/main/docs/book-handoff.md) |
| Book → Manuscript (files) | `.wsm` project folders and `.wsmz` packed projects, read; an offers file written beside the project | Book never writes a Manuscript project. It reads Manuscript's project schema, so a schema change in Manuscript reaches Book |
| Manuscript → Script (files) | `.wss` files kept inside a Manuscript project, shown read-only | Manuscript's own reader, `crates/manuscript-io/src/screenplay.rs`. The format is Script's, in its [`docs/format.md`](https://github.com/jamescjfoundation/wordsmith-script/blob/main/docs/format.md) |
| Each app → wordsmith (brand) | Logos, icons, the palette card, and the seven palette colors of the app's theme file | Copies in the app's `assets/brand/`, written by `npm run brand -- --app <app>` here from the kit, with `kit.json`, the record of the kit commit they came from. `brand/apps.json` here lists every carried file with its checksum ([Route F](#route-f)) |
| wordsmith → each app (the guide) | Each app's section of the wiki, and the screenshots the wiki and the website show | Built by `npm run guide` in `website/wiki` from the app's `docs/guide/` and `docs/images/` at a commit recorded in `website/wiki/guides.lock.json`. `npm run guide:check` (in `checks.yml`) fails when a page here is not what that commit gives; `guides.yml` fails while the app's guide on `main` has moved on ([Route C](#route-c)) |
| wordsmith → each app (releases) | The version, the date and the download links the website and the wiki show | Read from each app's public releases on GitHub by `website/tools/releases.py`, at every deploy and once a day ([Route J](#route-j)). The words around them are in `website/data/apps/<app>.json` |
| wordsmith → each app (facts) | What the website and the wiki's project pages say an app does | Written by hand from the app's `docs/guide/`, `CHANGELOG.md` and code |
| Each app → its GitHub releases | The in-app update check | The only network request an app makes on its own; it reads the app's own published releases and can be turned off |

Book and Manuscript move to a new core together, Manuscript first: Book's graph holds one core release, so the book-view tag Book pins must be cut on the core release Book pins ([Route I](#route-i)).

## Routes

Each route is a list of steps. Follow the repository's own `AGENTS.md` at every step that happens inside it.

<a id="route-a"></a>
### Route A: a core change an app needs

For a bug in a `jcj-` crate found from an app, or a feature that any app would share. The decision tree "Building between an app and the core" in each app's `AGENTS.md` says whether a change belongs in the core.

1. Open an issue in [open-source-core](https://github.com/jamescjfoundation/open-source-core/issues) that describes the general need, not the app's feature.
2. Have the core as a sibling folder of the app (see [Route M](#route-m)). In the app, run `cargo xtask dev-link ../open-source-core`, so the app builds against your core checkout. From core v0.1.20 the link is kept in a folder Git ignores, with its own lock file, so no tracked file changes; `cargo xtask ci --linked` runs the app's gate against the link.
3. Build the general part in the core, with its own tests and a use in `apps/core-testbed`. No product name, color, logo, or screenplay, manuscript or book idea goes into the core.
4. Build the app's use of it in the app. Never change a core interface from the app's side, and never work around a core bug in the app.
5. In the core, run `cargo xtask ci` and land the change. To have GitHub check the app's half before the core is released, pin every `jcj-` line on an app branch to that core commit (`rev = "<the full commit id>"` in place of `tag`): `core-pin` passes on the branch and in its pull request with a warning, and fails on `main`. Then release the core ([Route I](#route-i)).
6. In the app, run `cargo xtask dev-unlink`, move the app to the new core release ([Route I](#route-i), step 5), run `cargo xtask ci`, and land the app's change. Name the core issue in it.

If the general shape is not clear yet, build it in the app first: mark the code `// core-candidate: open-source-core#N` with the number of a core issue labelled `core-candidate`, and move it later. When it moves, delete the app's copy and its marker in the same change. Never copy code from one app repository into another.

**Held by:** the app's gate. `unlinked` refuses a committed dev-link, and from core v0.1.18 the pre-commit hook does too. `layers` refuses a dependency on `jcj-upstream` or an upstream crate. `core-pin` holds every `jcj-` line to one release tag. From core v0.1.18, `docs` fails when a `// core-candidate:` marker names no core issue. An app can name only a core tag that exists, so the core lands and is released first. The pull request template every app carries (from core v0.1.18) asks for the change another repository must make first. Nothing checks that the issue was opened before the work began, that a product idea stays out of the core, or that an app does not work around a core bug.

**Today:**

- An app on a core older than v0.1.20 has the older `dev-link`: it writes the link into the tracked `.cargo/config.toml` and a linked build changes `Cargo.lock`. Move the app to the newest core first ([Route I](#route-i)).
- An app that builds on another app's crates names that app as a provider in its `xtask/src/main.rs` and links it the same way: `cargo xtask dev-link <name>=<folder>`. Book names Manuscript.
- Nothing stops a pull request whose branch pins a core commit from being merged; the warning, and `core-pin` failing on `main` afterwards, are the only guards.
- Each app lists the code it holds that waits for the core in its `docs/core-candidates.md`, with the core issue for each.

<a id="route-b"></a>
### Route B: something one app needs from another

Two pairs exist: Book builds on Manuscript's crates and reads its projects, and Manuscript reads Script's `.wss` files. The rule is the same for any pair ([decision 0004](decisions/0004-apps-that-depend-on-apps.md)).

1. The providing app owns the contract. For Book and Manuscript it is Manuscript's [`docs/book-handoff.md`](https://github.com/jamescjfoundation/wordsmith-manuscript/blob/main/docs/book-handoff.md); for `.wss` it is Script's [`docs/format.md`](https://github.com/jamescjfoundation/wordsmith-script/blob/main/docs/format.md).
2. A need goes in as an issue in the providing app's repository. Say what is needed and why, and name the consuming app. An agent may open it. Book keeps an index of its requests to Manuscript in its `docs/requests-to-manuscript.md`: add the new issue's row there.
3. The change is made in the providing app, as its own change under its own rules. A change in the consuming app never edits the provider's repository.
4. The provider lands first. For Book, Manuscript then cuts a new book-view tag and Book moves its two `wordsmith-manuscript-` lines to it. Then the consumer's change lands ([Route L](#route-l)).
5. When you change a provider, check the consumer before you land:
   - `manuscript-model`, `manuscript-format` or the `.wsm` project schema: Book builds on them. Open a Book issue for any change Book must follow.
   - The `.wss` format: Manuscript reads it. Open a Manuscript issue when the format version changes.
6. If a third app would need the same thing, it belongs in the core: use [Route A](#route-a).

**Held by:** Book's gate. `core-pin` fails while the lock file holds two cores, which it does when the Manuscript tag Book names is on another core release than Book's own, so Manuscript moves and tags first. On GitHub, a `book-view-*` tag in Manuscript cannot be moved or deleted. The apps' pull request template (from core v0.1.18) asks for the change another repository must make first. Nothing in a provider's gate builds its consumer, and nothing checks that a need was filed as an issue.

**Today:**

- The book-view tags are listed under "Tags" in Manuscript's `docs/book-handoff.md`: `book-view-<view version>.<count>`, with a new one cut each time Manuscript moves to a newer core. What else cuts a tag, and which release tag Book may name once Manuscript has a release, is not written yet. A change that breaks Book shows only when Book moves to a new tag.
- Manuscript's `.wss` reader does not check the format version it is given.

<a id="route-c"></a>
### Route C: a change users will see in an app

Each app has one user guide, `docs/guide/` in its own repository. The wiki's section for the app is built from it, so the guide is written once ([decision 0005](decisions/0005-one-guide-per-app.md)).

1. In the app: make the change, update the page in the app's `docs/guide/`, and add a `CHANGELOG.md` line. Manuscript and Book also add a line to `docs/progress.md`. A new guide page gets a line in the guide's `README.md`, which sets the order of the wiki's pages; the words after its link there become the page's description.
2. If screenshots changed, redraw them in the app ([Route G](#route-g)).
3. Land the app's change on its `main`.
4. In wordsmith, in `website/wiki`: run `npm ci` once, then `npm run guide`. It reads each app's `main` on GitHub, writes the app's section of the wiki and its pictures again, records the commit, and prints what changed and anything to look at. Never edit a page it writes.
5. Read what changed. If a page was renamed or removed, a link to it from a hand-written page breaks: `npm run guide:check` names it. Then run the rest of [Route D](#route-d), step 4, and land the change, naming the app's commit ([Route L](#route-l)).
6. If the change also moves what the website or the wiki's project pages say about the app (its feature list, its platforms, how it fits with the other apps), update them ([Route E](#route-e), [Route D](#route-d)).

**Held by:** in wordsmith, `npm run guide:check` (in `checks.yml`, on every pull request and push, and again before the deploy) fails when a page or picture of an app's section is not exactly what the recorded commit of the app gives, so a section cannot be edited by hand or left half built. `guides.yml` runs `npm run guide:behind` every day and is red while an app's guide on `main` differs from the recorded commit, until step 4 is done. In the apps, the pull request template (from core v0.1.18) asks what users will see and whether the guide and `CHANGELOG.md` say it. Nothing checks that a guide page follows a change to the app's code, or that step 6 was done.

**Today:** steps 4 and 5 are done by hand after an app's change lands; the daily run is the reminder. The wiki shows each app's guide as it is on `main`, not as it was at a release.

<a id="route-d"></a>
### Route D: a wiki page

"The wiki" always means the one in this repository, published at [wordsmithand.ink/wiki/](https://wordsmithand.ink/wiki/). It is not the wiki tab on GitHub. It holds two kinds of page.

**A page about one app** (`website/wiki/content/docs/script/`, `manuscript/`, `book/`) is that app's guide. It is changed in the app's repository, in `docs/guide/`, and reaches the wiki by [Route C](#route-c). If the wiki should say something about an app that its guide does not, open an issue in the app's repository for the guide page.

**A page about the project as a whole** (`website/wiki/content/docs/index.mdx` and `start/`: the apps and how they fit together, installing, your files, moving between the apps, getting help, questions and answers, privacy) is written here:

1. Work in the wordsmith repository.
2. Take the facts from the apps' repositories: `docs/guide/`, `CHANGELOG.md` and code. Document only what the apps do today; mark anything not built with `<Status value="planned" />` or `"in-progress"`. Never use an app's `.private/` notes.
3. Add or edit the page, and list a new page in `start/meta.json`, which sets the order. `website/wiki/README.md` has the frontmatter, the components and the picture rules.
4. In `website/wiki`, run `npm ci` once, then `npm run brand:check`, `npm test`, `npm run guide:check`, `npm run lint`, `npm run types:check` and `npm run build`. All must pass.
5. Land it on `main`. The push deploys the site and the wiki together; the page is live when the "Deploy website and wiki to GitHub Pages" run is green. Open the live page to check it.

**Held by:** `checks.yml` runs the commands of step 4 on every pull request and every push to `main`, and puts the site together as it is published. `pages.yml` runs the same checks again before it publishes, and the site is not updated when one fails. `npm run guide:check` fails on a file in an app's section that the tool did not write, so a hand-written page cannot be put there; and it fails on a link from one wiki page to another page, a heading of it or a picture that is not there. `python3 project/check_links.py` checks the links between the other Markdown files of this repository. Nothing checks a link from a wiki page to another site, or a hand-written page's claims against the apps.

**Today:** the checks are not required on `main`: a red run does not stop a merge or a direct push, only the deploy. Watch the "Checks" run of your own push.

<a id="route-e"></a>
### Route E: website text

1. Work in the wordsmith repository. All page text, the header and the footer are in `website/tools/build.py`. Never edit the `.html` pages by hand.
2. What a page says about an app's state is not page text ([decision 0006](decisions/0006-the-site-reads-the-apps-releases.md)). The version, the date and the download links come from the app's releases on GitHub. The words around them ("Preview 0.9.0", the line above the downloads) are in `website/data/apps/<app>.json`, one set for each state: no release, a preview before 1.0.0, released. Change them there. In `build.py`, use `chip`, `state`, `systems` and `download`; never write a version or a download link.
3. Run `python3 website/tools/build.py` from the repository root and commit the regenerated pages with the script and the data files.
4. Preview with `python3 website/tools/serve.py`. Check phone width, dark mode and every link you touched. To see a page as it will look after a release, write a releases file by hand in a folder outside the repository and build into another: `python3 website/tools/build.py <folder> --releases <file>`.
5. Say only what is true of the apps today. Check the app's guide and code before you change what a page says an app does.
6. Land it on `main`; the push deploys it.

**Held by:** `checks.yml` runs `python3 website/tools/build.py --check` on every pull request and every push to `main`: it fails when a page in `website/` is not what `build.py` writes from the data files in the repository, so a page edited by hand or left stale after a change to the script or the data is found before it is published. `pages.yml` runs the same check before the deploy. The tests in `website/tools/test_releases.py` hold the rules for which release is shown and which file belongs to which system, and the wiki's `scripts/releases.test.mjs` holds the same cases for the wiki. The published site leaves out `website/tools/`, `website/data/` and `website/README.md`. Nothing checks that a sentence about what an app does is true (step 5), how a page looks (step 4), or a link to another site.

**Today:** the three apps' data files hold the same words for each state; they are separate so one app's wording can differ.

<a id="route-f"></a>
### Route F: a logo, icon or brand color

The brand kit in `brand/` here is the source. It owns the seven palette colors of each app and every logo and icon; a logo, icon or palette file is never edited, recolored, rescaled or redrawn anywhere else ([decision 0007](decisions/0007-brand-files-reach-the-apps-by-one-route.md)).

In wordsmith:

1. Read `brand/suite/BRAND_GUIDE.md`. Change the script in `brand/source/`, run `python3 brand/source/build.py` to see what changes, then again with `--write` (add `--pdf` for the guideline PDFs). `brand/README.md` has the setup.
2. Update by hand the files the build does not write: the kit's READMEs, `BRAND_GUIDE.md` and each `tokens.json`.
3. In `website/wiki`, run `npm run brand`. It writes the wiki's copies (`website/wiki/public/brand/`), the website's (`website/assets/brand/` and `website/favicon.svg`), the launcher's (`launcher/assets/brand/`) and `brand/apps.json`, the list of what each app carries with each file's checksum; `npm run brand:check` verifies all three. Land the change on `main`.

In each app, as a change in that app's repository that names the wordsmith commit ([Route L](#route-l)):

4. With the app's checkout beside wordsmith ([Route M](#route-m)), run `npm run brand -- --app script` (or `manuscript`, `book`) in wordsmith's `website/wiki`. It writes the kit's files for that app into the app's `assets/brand/`, with `kit.json` (the kit commit they were taken at, and the app's part of the list), and prints what changed. It commits nothing, removes nothing, and never touches the files that are the app's own. `npm run brand:check -- --app script` compares without writing.
5. Make again the files the app derives from a kit file, when the tool says their source changed, and run `cargo xtask ci` (its `assets` check wants every file under `assets/` listed in `ATTRIBUTION.md`).

What an app's `assets/brand/` holds, and nothing else. `brand/apps.json` names every file:

| Kind | Which files | Who changes it |
| --- | --- | --- |
| Carried | The app's `production/` set (the wordmark, stacked logo and mark, the parent brand's logos, the favicon, the 1024 px icon, the palette card) and the icons it uses from `app-icon/` (the smaller sizes, the Windows `.ico`) | The kit, by the tool. Never the app |
| Own | The interface theme file (`assets/brand/tokens.json` in Manuscript and Book, `assets/brand/script/tokens.json` in Script), which is in the core's token format and is not a copy of the kit's `tokens.json`; and the folder's `README.md` | The app. The seven palette colors in the theme file must be the kit's |
| Derived | The masks the window paints the mark from: `mark-mask.png` in Book (made by its `tools/brand-mask.py`), `mark-mask.png` and `wordmark-mask.png` in Script | The app, with its own tool, when the kit file it is made from changes |
| The record | `kit.json` | The tool |

To have an app carry another kit file, change the app's entry in the table `APPS` of `website/wiki/scripts/brand.mjs` here and run `npm run brand`.

**Held by:** `npm run brand:check` for the copies in this repository, the wiki's, the website's and the launcher's, and for `brand/apps.json`: `checks.yml` runs it on every pull request and every push to `main`, a change under `brand/` alone included, and `pages.yml` runs it again before the deploy. It fails when a copy is missing or differs from the kit, when a folder of copies holds a file the tool does not make, and when the list is not what the kit gives. `npm run brand:check -- --app <app>` fails on a carried file that is missing or differs, a file in the app's folder the list does not name, a theme file whose seven palette colors are not the kit's, and a `kit.json` that records another list than the kit has now; it runs by hand. In each app, the gate's `assets` task wants every file under `assets/` listed in `ATTRIBUTION.md`. This repository's pull request template, and the apps' from core v0.1.18, ask about brand files. Nothing on GitHub runs the kit's own build (`python3 brand/source/build.py`), so a kit file edited by hand is not found.

**Today:**

- No app has a check of its own yet, so nothing in an app's gate fails when its copies are behind the kit. Each app has an issue for it: check the folder against `kit.json` in the gate, with no network, and compare `kit.json` with `brand/apps.json` on this repository's `main` on a schedule, so a kit change shows as a failing check until the app takes its copies.
- No app has taken its copies by the tool yet, so none has a `kit.json`. Script's palette card and two icons, and sixteen of Manuscript's files, differ from the kit; Book's are the kit's.
- Manuscript makes its smaller icons and its `.ico` with its own `tools/brand-icons.py`. The kit has every size, and the list names the kit's as the ones Manuscript carries.
- Script's `mark-mask.png` and `wordmark-mask.png` have no tool that makes them.

<a id="route-g"></a>
### Route G: screenshots

1. In the app, run `cargo xtask screenshots`. The app draws its own pictures into `docs/images/`. Never use a screenshot of a real desktop.
2. Land them in the app. A guide page shows one with an ordinary Markdown picture link (`![The window](../images/page-view.png)`).
3. In wordsmith, in `website/wiki`, run `npm run guide` ([Route C](#route-c), step 4). It carries every picture a guide page shows into the app's section of the wiki, and every picture named under `screenshots` in `website/data/apps/<app>.json` into `website/assets/img/` as `<app>-<name>.webp`, each scaled to 1600 pixels wide and written as WebP. A picture is never copied, converted or cropped by hand.
4. To show another screenshot on the website: add its name to `screenshots` in the app's data file, run `npm run guide`, and place it in `website/tools/build.py` with `shot(app, name, alt)` ([Route E](#route-e)).

**Held by:** the app draws the pictures itself, so they cannot show a real desktop. `npm run guide:check` (in `checks.yml`) fails when a picture here is not the file the tool wrote, when its source is not the file at the recorded commit, and when `website/assets/img/` or an app's section holds a picture the tool does not make. `guides.yml` is red while a carried picture has been redrawn on the app's `main`. `build.py` stops when a page asks for a screenshot that is not carried. Nothing checks that a picture still shows what its caption says.

**Today:** only Wordsmith Script's guide shows a picture. The guides of Manuscript and Book show none of the pictures in their `docs/images/`, so their wiki sections have none.

<a id="route-h"></a>
### Route H: a security problem

1. Do not describe it in a commit, branch name, comment, issue, pull request or any tracked file, in any repository.
2. Write it up in `.private/` in the checkout you are working in (ignored by Git in all five repositories) and tell the maintainer you are working for. The maintainer opens a private advisory on the repository's Security tab when the problem needs a private place for the discussion and the fix.
3. A problem in shared code (the window, saving, import and export, updates, agent control) belongs to the core even when you found it from an app. Do not open an app issue or a core issue for it. It is fixed in the core, on a branch with a neutral name, with a test that would have caught it.
4. After the fix: release the core and move every app to it ([Route I](#route-i)). A problem in one app's own code is fixed and released in that app the same way.
5. Disclosure comes after the release: the advisory, and a **Security** entry in the changelog. Each repository's `SECURITY.md` has the details. A problem in the website, the wiki, the deploy or the brand files is fixed in wordsmith, which has no releases: the fix ships with the deploy, and the advisory is the record.

There are two ways in and one handling. Someone outside the project reports through GitHub's private reporting: the repository's Security tab, then "Report a vulnerability". It is on in all five repositories, and only the maintainers see a report. Someone working in a checkout, an agent included, follows step 2 instead of filing a report. Either way the discussion stays in the private advisory, working notes stay in `.private/`, and nothing public names the problem until the fix is released.

**Held by:** on GitHub, private vulnerability reporting is on in the five repositories, and secret scanning with push protection refuses a push that holds a credential it recognises. In the Rust repositories, `cargo xtask privacy` (the pre-commit hook and the gate) looks for personal details and secrets in files and commit identities; in wordsmith, `python3 project/privacy.py` does, in `checks.yml` on every pull request and push. `.private/` is ignored by Git in all five. Nothing can check that a commit message, a branch name or an issue does not describe an open problem: step 1 is kept by whoever writes.

**Today:** private reporting is off in the two forks: a problem found in upstream code is reported to the core. A `.private/` folder inside a worktree goes away with the worktree, so tell the maintainer before the thread ends.

<a id="route-i"></a>
### Route I: a core release, and moving an app to a newer core

Releasing the core:

1. Everything for the release is on the core's `main` and `cargo xtask ci` passes there.
2. Make the release commit: the new version in `Cargo.toml` and `Cargo.lock`, the new tag on the `jcj-` lines of `template/Cargo.toml`, and a `CHANGELOG.md` section with **What apps must do**. While the core is at 0.x, a patch release only adds or fixes; anything that breaks an app is a minor release and says exactly what each app changes.
3. Push the commit. Run the core's Nightly workflow on it by hand (`gh workflow run nightly.yml --ref main`): that is the full gate on Linux, macOS and Windows.
4. When that run is green, push the tag `vX.Y.Z`. The tag starts the Release workflow, which runs the gate again and publishes the GitHub release. No tag goes on a commit whose gate has not passed. A person or an agent may cut the release ([decision 0002](decisions/0002-how-changes-land-and-who-releases.md)).

Moving an app to it:

5. In the app's root `Cargo.toml`, change the tag on every `jcj-` line; they all carry the same tag. Run `cargo metadata --format-version 1 > /dev/null` so `Cargo.lock` follows; do not run a blanket `cargo update`.
6. Run `cargo xtask sync` to take the core-owned files of that release, then `cargo xtask sync --check`. From core v0.1.20 one run is enough; an app coming from an older core runs it again until the check passes.
7. Read **What apps must do** in the core's [`CHANGELOG.md`](https://github.com/jamescjfoundation/open-source-core/blob/main/CHANGELOG.md) for every release between the old tag and the new one, and do it.
8. Run `cargo xtask ci`. A golden file that changes is a deliberate change: review it and record it in the app's `docs/golden.md`.
9. Script also names its core tag in its top-level `UPSTREAM.md`; update that line.

The launcher moves the same way, with every command run in `launcher/` of this repository. One step more: compare `.github/workflows/launcher.yml`, `release.yml` and `launcher-core-pin.yml` here with the core's shared workflows at the new release, and bring over what changed. They are written out here because the core's shared workflows cannot be called for an app in a folder ([launcher decision 0001](../launcher/docs/decisions/0001-an-app-in-a-folder-of-the-wordsmith-repository.md)).

A fix to CI itself does not wait for a release: the apps' CI is the core's shared workflow, called at the core's tag `workflows-v1`, and the fix reaches every app when that tag is moved to a commit of the core's `main` whose own CI passed (the core's `.github/workflows/README.md` has the steps).

When to move: before starting new work on an app and before releasing it. `cargo xtask core-pin --behind` prints how far behind an app is, and a weekly workflow in each app (`core-pin.yml`) opens an issue there when it is more than three releases behind ([decision 0002](decisions/0002-how-changes-land-and-who-releases.md)).

**Held by:** on GitHub, a `v*` tag cannot be moved or deleted in any repository and `main` cannot be force-pushed or deleted, so a release that went out wrong is fixed by the next version. The core's Release workflow runs the full gate on the tag before it publishes the GitHub release. In each app, `core-pin` fails on two tags or two cores and `sync` fails when a core-owned file or block differs from the pinned release; the weekly `core-pin.yml` opens an issue when the app is more than three releases behind (for the launcher: `launcher-core-pin.yml` here). Nothing stops a tag being pushed before the Nightly run is green, and nothing checks that an app did what **What apps must do** asks beyond those two tasks.

**Today:**

- Steps 3 and 4 are kept by whoever cuts the release. A tag cannot be taken back once pushed, and apps can name it even if the Release run fails.
- Nothing builds the real apps against a core change before it is released; the core's own check builds only the template app.
- A fix to the core's shared workflows reaches the three apps when `workflows-v1` is moved, and does not reach the launcher's three workflows: they are compared by hand, at a move to a newer core.
- Moving Book takes two steps by hand: Manuscript moves to the new core and cuts a new book-view tag, then Book moves its core tag and its Manuscript tag in one change. `cargo xtask core-pin` fails in Book until both are done. Before Manuscript's tag exists, Book can already take the release's core-owned files: in a core checkout at that release, run `cargo xtask sync <Book's folder>`.

<a id="route-j"></a>
### Route J: an app release

The three apps and the launcher release the same way, by the core's release contract ([core decision 0019](https://github.com/jamescjfoundation/open-source-core/blob/main/docs/decisions/0019-app-releases.md); the contract is the core's [`docs/app-releases.md`](https://github.com/jamescjfoundation/open-source-core/blob/main/docs/app-releases.md)). An app's release is its own repository's. The launcher's is this repository's, and its commands run in `launcher/`.

1. Move the app to the newest core first ([Route I](#route-i)).
2. In the app: write what the release changes under `## Unreleased` of `CHANGELOG.md`, then run `cargo xtask release X.Y.Z`, which sets the version and gives the changelog section its date. Run `cargo xtask ci`, commit, and push to `main`.
3. To try the packaging without releasing: `gh workflow run release.yml --ref main -f dry-run=true` builds and checks the file of every system and publishes nothing (`-f gate=true` adds the whole gate on the three systems). The same dry run starts by itself every week.
4. Start the release: `gh workflow run release.yml --ref main`. The workflow checks that the commit is a release commit that is not released yet, runs the whole gate on Linux, macOS and Windows, builds and checks each system's file and `SHA256SUMS.txt`, and only then makes the tag `vX.Y.Z` and publishes the release. A red job leaves no tag: fix the cause on `main` and start it again. Never push a `v*` tag or make a release by hand.
5. Check the published release: one file for each system and `SHA256SUMS.txt` are there, and the app's update check finds them.
6. The website and the wiki pick the release up by themselves: every deploy reads each app's latest public release from GitHub, and `pages.yml` runs every day and deploys when an app has published one ([decision 0006](decisions/0006-the-site-reads-the-apps-releases.md)). To show it at once, start the deploy by hand in wordsmith: `gh workflow run pages.yml`. Then open the app's page on the site and its "Installing" entry in the wiki: the version, the date and a download for each system should be there.
7. In wordsmith, when the guide changed with the release: `npm run guide`, so the wiki shows the released app's guide ([Route C](#route-c)).
8. The launcher finds an app's new release by itself: it reads the app's releases when it starts. After a change to the contract, or to what a package holds, run `cargo xtask live` in `launcher/` ([launcher/AGENTS.md](../launcher/AGENTS.md)).

A person or an agent may release an app once its gate passes ([decision 0002](decisions/0002-how-changes-land-and-who-releases.md)).

**Held by:** the release workflow runs the whole gate on three systems before it builds the release files, checks every file's name against the contract, and makes the tag last, so a failed release leaves nothing behind. In an app the workflow is the core's shared one, called at `workflows-v1`; for the launcher it is `release.yml` here, written out step for step from the core's. On GitHub, a `v*` tag cannot be moved or deleted. The gate's `release-data` task (every push) fails when a file the package data names is missing or a program is not named as the contract says. In wordsmith, the daily run of `pages.yml` compares GitHub's releases with the release data the live site was built from and deploys when they differ, through every check of `checks.yml`; a release with no file for one of the app's systems shows that on the page instead of a wrong link. Nothing tells this repository at the moment of a release: the site follows within a day.

**Today:**

- Each of the three apps has published its first release, 0.9.0, a preview; 1.0.0 follows. The site calls a release before 1.0.0 a preview.
- The release files are not signed with a publisher's certificate: the signing steps are in the workflow and wait for the certificates.
- A download is matched to its system by the file's name (`website/data/platforms.json`), and the launcher builds the name from the contract's pattern. Both follow the contract; neither is checked against the other.

<a id="route-k"></a>
### Route K: a change in WordCraft or craft-libs

1. Apps never name WordCraft or craft-libs crates or types. If an app needs something from upstream, it needs it from a `jcj-` interface: use [Route A](#route-a).
2. In the core, the adapters in `jcj-upstream` and the `jcj-` crate that wraps them change first. Most needs end there.
3. If upstream code itself must change, it changes in our fork, on a topic branch, one commit per patch, and is recorded under "Carried patches" in the core's [`docs/UPSTREAM.md`](https://github.com/jamescjfoundation/open-source-core/blob/main/docs/UPSTREAM.md). Nowhere else.
4. Moving to a newer upstream release follows "The two-week train" in that file: move the pins, rebuild the fork's `jcj` branch, run the contract tests, decide follow, hold or own for each source, release the core, move the apps ([Route I](#route-i)). `cargo xtask pins` checks the pins against the file.
5. The patch block reaches each app through `cargo xtask sync`.

**Held by:** the `layers` task: in the core only `jcj-upstream` may depend on an upstream crate, and in an app nothing may. The core's `pins` task fails when the pins, `Cargo.lock` and `docs/UPSTREAM.md` disagree. The patch block is part of each app's `sync` check. On GitHub, in both forks `main` cannot be force-pushed or deleted, `v*` and `jcj-*` tags cannot be moved or deleted, and no workflow runs; in the WordCraft fork the `jcj` and `topic/*` branches cannot be deleted. `layers` reads dependencies, not text, so nothing checks for an upstream type named in an app's documents.

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

**Held by:** where a tag carries the first change, the order holds itself: an app can name only a core tag or a book-view tag that exists, and `core-pin` fails on a mixed state. Both pull request templates ask for the other change's link. Nothing checks the order where no tag is involved (an app and this repository, the brand kit and an app), the branch names, or that each change names the other.

<a id="route-m"></a>
### Route M: working with all the repositories, or with only one

**Side by side.** Clone the repositories as sibling folders with their own names, so `../open-source-core` from an app is the core:

```
wordsmith/  wordsmith-script/  wordsmith-manuscript/  wordsmith-book/  open-source-core/
```

- The folder that holds them is not a repository. Run `git`, `cargo`, `npm` and `gh` inside the repository they belong to.
- Each repository has its own history, branch and gate. Commit each one separately.
- In each Rust repository, run `cargo xtask install-hooks` once per clone: the hooks check formatting and privacy before a commit and run the changed-only gate before a push.
- Before the first commit in a fresh clone, check `git config user.email`. It must be a GitHub no-reply address; if the machine's own setting is another address, set it in the clone with `git config user.email`.
- History on `main` is not rewritten and a release tag is not moved: GitHub refuses a force-push to `main` and a moved or deleted `v*` tag in every repository. A mistake is fixed by a new commit or the next version.

**Worktree threads.** When a tool gives a task its own checkout of every repository on a same-named branch:

- Change only that task's checkouts. Another checkout of the same repository is for reading.
- A new worktree has no `target/` folder, so the first build and the first push are slow.
- `.private/` notes in a worktree are lost with it.

**Only one repository.** The block at the top of this file is carried in each app's `AGENTS.md`, and this repository's `AGENTS.md` starts from this file, so the others can be found from any of them. The core is general and carries no block. When a route needs another repository, clone it beside the one you have (`git clone https://github.com/jamescjfoundation/<repository> ../<repository>`). To read one file, the links in this map go straight to it on GitHub.

**Held by:** in a Rust repository with the hooks installed, the pre-commit hook runs the format and privacy checks (and `unlinked` from core v0.1.18) and the pre-push hook runs the changed-only gate. From core v0.1.18, `cargo xtask ci` warns when a clone's hooks are not installed. `cargo xtask privacy` fails on a commit whose address is not a no-reply one. This repository's hooks (`hooks/`, switched on by `cargo xtask install-hooks` in `launcher/`) run only for a change to `launcher/`. For the rest, `python3 project/privacy.py` checks its files and every commit's address, but only when you run it, or in `checks.yml` after the push or on the pull request. Nothing stops a task editing another task's checkout.

<a id="route-n"></a>
### Route N: a rule or instruction that several repositories carry

Some text is the same, word for word, in several repositories. It sits between a `BEGIN` and an `END` marker line, it has one owner, and a copy is never edited: a tool writes the copies and a check fails when one differs.

| Block | Owner: edit it here | Carried in | Written by | Checked by |
| --- | --- | --- | --- | --- |
| The project block (`wordsmith project block`) | [`project/README.md`](#the-wordsmith-project-map) here | Each app's `AGENTS.md` | `python3 project/carry.py --write`, here | `.github/workflows/carried.yml`, here |
| The core's rules (`open-source-core: public`, `app-and-core`, `app`, `security`, `contributing`) | The core's `template/AGENTS.md`, `template/SECURITY.md`, `template/CONTRIBUTING.md` | Each app's file of the same name; `public`, `security` and `contributing` also in this repository's `AGENTS.md`, `SECURITY.md` and `CONTRIBUTING.md` | `cargo xtask sync` in each app; `python3 project/carry.py --write` here | `cargo xtask sync --check` in each app's gate; `carried.yml` here |
| The code of conduct, a whole file | The core's `template/CODE_OF_CONDUCT.md` | `CODE_OF_CONDUCT.md` in each app and in this repository | The same two tools | The same two checks |

A block owned by the core:

1. In open-source-core, edit the block in the file under `template/`. Keep it general: it is read in every app, and `public`, `security`, `contributing` and the code of conduct in this repository too, which has no Cargo and no releases. So it names no product and nothing only one repository has.
2. Run `cargo xtask template --write`, which copies the blocks into the core's own `AGENTS.md`, `SECURITY.md` and `CONTRIBUTING.md`, then `cargo xtask ci`.
3. Land it and release the core ([Route I](#route-i), steps 1 to 4).
4. Each app moves to that release ([Route I](#route-i), steps 5 to 9). `cargo xtask sync` writes the new block, and the app's gate fails until it has.
5. In wordsmith, run `python3 project/carry.py --write` and land the files it changed. Read the part of each file outside the marker lines (`SECURITY.md`: "Where this repository differs"; `CONTRIBUTING.md`: "This repository's own rules") and keep it true of the new text.

The project block:

1. Edit it in `project/README.md`, between the two marker lines. Keep its links absolute, since it is read in other repositories.
2. With the apps as sibling folders ([Route M](#route-m)), run `python3 project/carry.py --write`. It writes the block into each app's `AGENTS.md`. It commits nothing.
3. Land the wordsmith change first. Then, in each app, commit and push the changed `AGENTS.md`, naming the wordsmith commit ([Route L](#route-l)).
4. The "Check the carried blocks" workflow here goes red at the wordsmith push and green once the last app has landed. Start it by hand with `gh workflow run carried.yml`, or run the same check yourself: `python3 project/carry.py --check --remote`.

`python3 project/carry.py` with no flag checks without writing. It reads the sibling folders where they exist, which can be ahead of or behind what is published; `--remote` reads each app's `main` and the core's newest release from GitHub. With `--write --remote` the tool writes only this repository's copies of the core's text, from that release: use it when the core's sibling folder is ahead of its last release. A file that is to carry a block needs the two marker lines first; the tool never guesses where a block belongs. To have another repository or file carry a block, add the marker lines there and a row to the table at the top of `project/carry.py`; a file carried whole needs only its row.

**Held by:** `cargo xtask sync --check` in each app's gate, for the core's blocks; the core's `template` task, for the core's own copies; `carried.yml` here, for the project block in each app and the core's text here.

**Today:**

- An app's own gate does not check its copy of the project block. A copy edited by hand in an app is found by this repository's workflow, at the next push here or the weekly run, not at the app's push.
- The core's text is written for a repository with Cargo and releases. A few of its sentences do not fit this repository; its `SECURITY.md` and `CONTRIBUTING.md` say which, in their own parts.
- After a core release that changes a block this repository carries, `carried.yml` here is red until step 5 is done.
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
| What the launcher does, and why it is built as it is | `launcher/docs/guide/`, `launcher/CHANGELOG.md` and `launcher/docs/decisions/` here. Outside its folder, write "launcher decision NNNN" |
| What is planned in wordsmith (the website, the wiki, the brand kit, this map, the launcher) | Its issues with the milestone [`v1`](https://github.com/jamescjfoundation/wordsmith/milestone/1). [`ROADMAP.md`](../ROADMAP.md) links there and holds no list |
| What is missing or planned in an app | Script: `docs/gaps.md` and `ROADMAP.md`. Manuscript and Book: `docs/PLAN.md` (both plans are finished) and `docs/progress.md`. **Today:** no repository keeps one live list of what is planned |
| What was done, step by step | Each app's `docs/progress.md`; the core's `CHANGELOG.md` |
| How users do something in an app | The app's `docs/guide/`. The app's section of the wiki, `website/wiki/content/docs/<app>/` here, is built from it and never edited ([Route C](#route-c)) |
| Which commit of an app the wiki shows | `website/wiki/guides.lock.json` here, and the line under each wiki page |
| What the public is told about the apps | `website/tools/build.py` and `website/wiki/content/docs/start/` here |
| An app's name, platforms and the words for its state on the site | `website/data/apps/<app>.json` here. Its version and downloads: its releases page on GitHub, read by `website/tools/releases.py` ([Route J](#route-j)) |
| Brand rules, logos, icons, colors | `brand/suite/BRAND_GUIDE.md` and `brand/README.md` here. What each app carries from the kit: `brand/apps.json` here, and `assets/brand/kit.json` in the app. An app's interface theme: its own `tokens.json`, in the format of the core's [`crates/jcj-theme/TOKENS.md`](https://github.com/jamescjfoundation/open-source-core/blob/main/crates/jcj-theme/TOKENS.md) |
| Test data and reference outputs | Each app's `docs/golden.md`; Manuscript's and Book's `docs/fixtures.md` |
| Credits for assets and dependencies | Each Rust repository's `ATTRIBUTION.md` and `NOTICE`; for the launcher, the two in `launcher/` |
| How to report or handle a security problem | Each repository's `SECURITY.md`; [Route H](#route-h) |
| Which license covers a file | Each Rust repository's `LICENSE-MIT`, `LICENSE-APACHE` and `NOTICE`. In wordsmith, [`LICENSES.md`](../LICENSES.md), by folder; for the names and logos, [`brand/LICENSE.md`](../brand/LICENSE.md) |
| Security notes, reviews, audits, working notes | `.private/` in the repository you are in, never tracked ([Project rules](#project-rules)) |

## Project rules

These hold in every Wordsmith repository. Each repository's `AGENTS.md` adds its own.

- **How changes land.** While no app has been released, a change may be pushed straight to `main`. Run the repository's gate first (`cargo xtask ci` in the Rust repositories; the checks in `AGENTS.md` here). A pull request is optional, and its author merges it once the checks pass. A red `main` is fixed at once by whoever made it red. History on `main` is never rewritten and a release tag is never moved; GitHub refuses both in every repository. [Decision 0002](decisions/0002-how-changes-land-and-who-releases.md).
- **Who releases.** A person or an agent may release the core or an app, once the release's gate passes. [Decision 0002](decisions/0002-how-changes-land-and-who-releases.md).
- **Core pins.** An app moves to the newest core release before new work starts on it and before it is released. An app more than three core releases behind gets an issue. [Decision 0002](decisions/0002-how-changes-land-and-who-releases.md), [Route I](#route-i).
- **Naming other companies, programs and formats.** Code and docs may name them where it is a fact a reader needs: the formats an app opens, what a store or print service expects of a file. Interface names, designs and help text stay our own, and an app never says it replaces or follows another product. Apps never name WordCraft or craft-libs types. People are never named. [Decision 0003](decisions/0003-naming-other-companies-programs-and-formats.md).
- **Apps that depend on apps.** Allowed, under a contract the providing app owns. [Decision 0004](decisions/0004-apps-that-depend-on-apps.md), [Route B](#route-b).
- **Where project-wide things live.** Here, in `project/`. The core holds only what is general to any app built on it. A decision about one app stays in that app. [Decision 0001](decisions/0001-where-project-wide-things-live.md).
- **What is public.** Every repository is public, history included, for good. No commit, branch name, issue, pull request, comment or tracked file holds a person's name or email, an account name, details of a machine (home-folder paths, user or host names, addresses), anything said in a conversation, an open security problem, a secret, a file from a real machine, or anyone's private writing. Commit with a GitHub no-reply address, and set it in a fresh clone before the first commit. Never push with `--all` or `--mirror`. A tool looks for what a pattern can find: `cargo xtask privacy` in the Rust repositories, `python3 project/privacy.py` in wordsmith.
- **Reviews and working notes.** Reviews, audits and working notes stay in `.private/`, which every repository ignores. One is published only when a maintainer says so, and then under `docs/history/`, labelled as history.
- **The Foundation's name** is always "The James C. J. Foundation". **Today:** older text in the core and the apps uses a shorter form; do not copy it into new text.
- **Product names** are "Wordsmith", "Wordsmith & Ink", "Wordsmith Script", "Wordsmith Manuscript", "Wordsmith Book" and "Wordsmith Launcher", written exactly so. They are trademarks.
- **Licensing.** Code is MIT OR Apache-2.0. The words of the website and the wiki are CC BY 4.0. The brand files (logos, icons and their copies in every repository) are not open source: all rights are reserved, and [`brand/LICENSE.md`](../brand/LICENSE.md) says how the names and logos may be used. A new dependency must have a compatible license (the core's license allowlist decides for the Rust repositories) and is credited. Bundled fonts are under the SIL Open Font License.
- **Privacy.** No telemetry, analytics, accounts, trackers or third-party requests, in the apps or on the site. The only network request an app makes on its own is the update check with its GitHub releases, and it can be turned off.
- **Writing.** Plain, short sentences, for writers in user-facing text. Say only what exists; mark planned things as planned.
- **Never** copy code from one app repository into another, and never edit upstream code outside our forks.
