# Contributing

Thank you for helping. This repository is public: everything you commit, push, or write in an issue, pull request or review can be read by anyone and stays in the history for good.

This repository holds what belongs to Wordsmith as a whole: the project map, the brand kit, the website and the wiki. The apps are in their own repositories, each with its own `CONTRIBUTING.md`. [`AGENTS.md`](AGENTS.md) has this repository's rules in full, for people and for coding agents; this page is the short way in.

## The quickest way to help

Fix a wiki page. Every page of [the wiki](https://wordsmithand.ink/wiki/) has an "Edit on GitHub" link, which opens the file the page is made from.

- A page about one app is that app's own guide, kept in the app's repository under `docs/guide/`: the link takes you there, and the wiki follows the guide ([project decision 0005](project/decisions/0005-one-guide-per-app.md)). The copies in `website/wiki/content/docs/<app>/` are written by a tool and never edited.
- The pages about the project as a whole are written here, in `website/wiki/content/docs/start/` and `website/wiki/content/docs/index.mdx`.
- Write for writers, in plain, short sentences.
- Describe only what the app does today. Check it in the app before you write it.
- Mark anything not built yet as planned.

## Building and checking

There is no Cargo here. The tools need Python 3 and nothing else. The wiki needs Node.js 22 or later.

```sh
python3 -m unittest discover -s project   # the tools' own tests
python3 project/privacy.py                # nothing personal, no secret, no-reply commit addresses
python3 project/check_links.py            # the links between the Markdown files
python3 project/carry.py                  # the text carried from and to the other repositories

python3 website/tools/build.py            # rewrite the website's pages from the generator
python3 website/tools/build.py --check    # the pages in website/ are what the generator writes
python3 website/tools/serve.py            # preview the website at http://localhost:8000

cd website/wiki
npm ci                                    # once
npm run dev                               # the wiki at http://localhost:3000/wiki/
npm run brand:check                       # the brand copies match the kit
npm test                                  # the wiki's tools' own tests
npm run guide                             # build each app's section again from the app's guide
npm run guide:check                       # each app's section is what its recorded commit gives
npm run lint
npm run types:check
npm run build                             # the static export, as the deploy builds it
```

The "Checks" workflow runs every check above on each pull request and each push to `main`. `carry.py` has its own workflow, which compares the carried text with what the other repositories have published, and so has `npm run guide:behind`, which reports an app's guide that has changed since the wiki was built from it. Run the checks for the folder you changed before you push; `AGENTS.md` lists them by folder.

## Where things are

| Path | What it is |
| --- | --- |
| `project/README.md` | The project map: every Wordsmith repository, how they depend on each other, and where each kind of change goes |
| `project/decisions/` | Why the project-wide rules are the way they are |
| `project/*.py` | The tools: `carry.py` (carried text), `check_links.py` (Markdown links), `privacy.py` (personal details and secrets), each with its tests |
| `brand/` | The brand kit: the source of every logo, icon and brand color. Its files are rebuilt by `brand/source/build.py`, never edited by hand |
| `website/tools/build.py` | The website's generator: the header, the footer and all page text |
| `website/*.html` | The generated pages. Never edited by hand |
| `website/assets/` | Styles, the menu script, fonts, pictures, and copies of brand files |
| `website/wiki/content/docs/` | The wiki's pages: `start/` and `index.mdx`, written here, and one folder per app, built from the app's own guide by `website/wiki/scripts/guide.mjs` |
| `website/data/apps/` | One small file per app: its name, repository and what the tools carry from it |
| `website/wiki/` (the rest) | The wiki's own code: Fumadocs on Next.js, exported as static files |
| `launcher/` | Wordsmith Launcher. Planned, not started |
| `.github/workflows/` | `checks.yml` (every check), `pages.yml` (the deploy), `carried.yml` (the carried text, against what is published), `guides.yml` (the apps' guides, against what the wiki was built from) |
| `LICENSES.md` | Which license covers which folder |

<!-- BEGIN open-source-core: contributing -->
<!-- Owned by open-source-core (template/CONTRIBUTING.md). Change it there, never in a copy: its tooling rewrites the copies. -->
## Rules for a public repository

### Personal information

Never commit, or paste into an issue or pull request: anyone's name, email address or account
(other than your commit author line); local paths, user names, host names or machine details;
files from a real machine (preferences, recovery, auto-save or backup files, logs, desktop
screenshots); anyone's private writing; passwords, tokens or keys. Test fixtures are
public-domain texts or written for the test. The repository's privacy check
(`cargo xtask privacy` where it has `cargo xtask`) checks files and commit identities.

### Security problems

Follow `SECURITY.md`: report privately and keep the problem out of public places until a release
fixes it.

### Private working notes

Reviews, audits and working notes go in `.private/` (ignored by Git). One is published only when
a maintainer says so, under `docs/history/` where the repository has a `docs/` folder, with a
first line saying it is history
([core decision 0012](https://github.com/jamescjfoundation/open-source-core/blob/main/docs/decisions/0012-working-in-the-open.md)).
Write the public part as a decision record or changelog entry, giving the reason itself rather
than "as discussed".

## Commits, pushes and pull requests

- While no app built on the core has a public release, a push to `main` is allowed once the
  repository's gate passes (`cargo xtask ci` where it has `cargo xtask`). A pull request is
  optional; its author may merge it once its checks pass
  ([core decision 0013](https://github.com/jamescjfoundation/open-source-core/blob/main/docs/decisions/0013-app-and-core.md)).
- A release is cut, and in the core an upstream pin is moved, only on a commit whose full gate
  has passed; a person or an agent may do either (core decisions
  [0004](https://github.com/jamescjfoundation/open-source-core/blob/main/docs/decisions/0004-follow-hold-own.md)
  and
  [0011](https://github.com/jamescjfoundation/open-source-core/blob/main/docs/decisions/0011-releases-and-versioning.md)).
- Contributions are licensed as the repository's license files say (MIT OR Apache-2.0 for
  code), with no extra terms. No CLA.
- Use your GitHub no-reply address (`git config user.email <id>+<login>@users.noreply.github.com`).
- One concern per commit or pull request; say what changed, why, and how you checked it.
- A pull request opened by Dependabot is merged by anyone with write access once its checks
  pass.
- Update the changelog and the decision records, where the repository keeps them, when behavior
  changes. A core change that apps must act on says so under "What apps must do".
- AI-assisted contributions are welcome; you are responsible for every line.
<!-- END open-source-core: contributing -->

## This repository's own rules

The rules above are carried word for word from open-source-core and are written for a repository with Cargo. Read them here as follows.

- **The checks.** There is no `cargo xtask`. `python3 project/privacy.py` does the job of `cargo xtask privacy`, and the checks under "Building and checking" stand where the rules say `cargo xtask ci`: a push to `main` is allowed once the ones for the folders you changed pass.
- **Licenses.** A contribution takes the license of the folder it is made in, and [`LICENSES.md`](LICENSES.md) has the list: code is MIT OR Apache-2.0, and the words of the website and the wiki are CC BY 4.0. The brand files are not open source. Do not send a changed logo or icon: open an issue that says what should change.
- **No releases, no changelog.** Nothing is released from here and there is no `CHANGELOG.md`. The website and the wiki are published from `main` by the deploy. A change that follows a change in an app links it ([Route L](project/README.md#route-l) of the project map).
- **Say only what exists.** The website and the wiki describe what an app does today. Check the app's repository before you write a claim.
- **The Foundation's name** is always "The James C. J. Foundation".
- **Generated files.** Website pages come from `website/tools/build.py` and brand files from `brand/source/build.py`. Change the script, run it, and commit what it writes.
- **No third-party requests.** The site and the wiki load nothing from another site: no CDN, font service, analytics or embed.

## Conduct

Follow [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md).
