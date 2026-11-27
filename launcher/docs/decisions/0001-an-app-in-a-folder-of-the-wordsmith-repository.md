# 0001: An app in a folder of the wordsmith repository

Date: 2026-11-27 · Status: accepted

## Context

Wordsmith Launcher is a Rust desktop program and is to be handled like the three Wordsmith apps:
built on open-source-core at a release tag, carrying the core's shared files through
`cargo xtask sync`, passing the shared gate (`cargo xtask ci`), and released by the core's
release contract (core decision 0019, `docs/app-releases.md` there).

The three apps are each a repository. The launcher is not: it belongs to the project as a
whole, and the wordsmith repository holds such things (project decision 0001). That repository
also holds the project map, the brand kit, the website and the wiki, none of which is Rust.

Everything the core gives an app assumes that the app's folder is the root of a repository.
Read at core v0.1.22:

| What | What it assumes | In a folder |
| --- | --- | --- |
| `cargo xtask sync` and `sync --check` | Nothing: they work on the workspace's folder | Work |
| The gate's other checks (`fmt`, `lint-roots`, `core-pin`, `layers`, `app-layers`, `assets`, `release-data`, `privacy`, `licenses`) | Git commands run in the workspace's folder, which lists only that folder's files | Work. `privacy` also reads every commit of the repository |
| The gate's `docs` check | A relative link in Markdown stays inside the workspace's folder | A link to a file of the repository outside `launcher/` is refused. Such links are written as full GitHub addresses |
| `cargo xtask ci --changed`, `cargo xtask affected` | The changed files Git names are paths from the workspace's folder | Wrong: Git names them from the repository's root, no package's folder matches, and the answer is "nothing changed". Clippy and the tests are then skipped |
| `cargo xtask install-hooks`, the two hooks | The hooks are in `hooks/` at the repository's root, and run there | Wrong: the path it sets leads nowhere from a folder, and a hook runs at the root, where there is no Cargo |
| `shared-ci.yml`, `shared-release.yml`, `shared-core-pin.yml` | `Cargo.toml`, `Cargo.lock`, `rust-toolchain.toml`, `.cargo/config.toml`, `target/` and `dist/` at the root; every step runs there | Cannot be called: they have no input for a folder |
| `.github/workflows/*.yml`, `.github/pull_request_template.md`, `.github/dependabot.yml` | GitHub reads them at the root | GitHub does not read them in a folder |
| A release | The tag `vX.Y.Z` and the GitHub release of the app's own repository | The repository's, whatever folder the app is in |

## Decision

- **The workspace is `launcher/`.** Its own `Cargo.toml`, `Cargo.lock`, `.cargo/`, `xtask/`,
  `rust-toolchain.toml` and `target/`. Every `cargo` command runs there. The rest of the
  repository stays without Cargo: no manifest at the root, so the website and the wiki are not
  a Rust project and their checks need no Rust.
- **The launcher carries everything an app carries**, written by `cargo xtask sync` from the
  pinned core release into `launcher/`, and held by `sync --check` in its gate: the settings
  files, the shared xtask modules and the shared gate (`gate::main`), the marked blocks in
  `AGENTS.md`, `SECURITY.md`, `CONTRIBUTING.md`, `Cargo.toml`, `.cargo/config.toml`,
  `.gitignore` and `.gitattributes`, the code of conduct, the hooks, and the files under
  `.github/`. Nothing of the core's is edited or left out.
- **The carried files under `launcher/.github/` and `launcher/hooks/` do not run.** They are
  kept because the core's check wants them. A `README.md` beside them says so.
- **The workflows that run are the launcher's own, at the repository's root**, written to do
  what the core's shared workflows do, step for step, from the folder:

  | At the root | Does what | In place of |
  | --- | --- | --- |
  | `.github/workflows/launcher.yml` | The gate in three jobs (checks, cargo-deny, clippy and tests), on every push to `main` and every pull request that touches `launcher/`; and the live check, each app on Linux, macOS and Windows | The core's `shared-ci.yml` |
  | `.github/workflows/release.yml` | The release, and its dry run: the release commit checked, the whole gate on three systems, the package of each system, `SHA256SUMS.txt`, the attestation, then the tag and the published release | The core's `shared-release.yml` |
  | `.github/workflows/launcher-core-pin.yml` | The weekly look at how far behind the core pin is, and the issue | The core's `shared-core-pin.yml` |

  They build and test everything on every run and never use `--changed`. The launcher is two
  small packages, so that costs little.
- **The repository gets a `hooks/` folder at its root**, which is where
  `cargo xtask install-hooks` points Git. Its pre-commit runs the launcher's format, privacy and
  dev-link checks, and its pre-push the launcher's whole gate, each only when the change touches
  `launcher/`.
- **The core is asked to carry an app in a folder**, in
  [open-source-core#50](https://github.com/jamescjfoundation/open-source-core/issues/50):
  a folder input to the three shared workflows, changed files read from the workspace's folder,
  hooks that work from a folder, and a `docs` check bounded by the repository. Nothing in the core is changed from here. When the core
  has it, the three root workflows become the short callers the apps have, and the root hooks
  call the carried ones.
- **The wordsmith repository's releases are the launcher's.** The repository released nothing
  before, so a tag `vX.Y.Z` there names a version of the launcher, the launcher's update check
  reads `jamescjfoundation/wordsmith`, and the website reads the launcher's release as it reads
  an app's. The repository's rule that a `v*` tag is never moved or deleted already holds.
- **The release workflow is named `release.yml`**, as in every app, so the contract's commands
  work as written. The gate's workflow is `launcher.yml`, because `ci.yml` beside the
  repository's own `checks.yml` would not say whose it is.
- **Two tools carry the core's text into this repository, and they do not meet.**
  `cargo xtask sync` writes the launcher's copies, in `launcher/`, from the core release the
  launcher pins. `python3 project/carry.py` writes the repository's own copies, at the root,
  from the core's newest release. Each checks only its own. The launcher's `AGENTS.md` carries
  no project block: the project map is in the same repository, and the file points at it.
- **The repository's own checks read the launcher's files** as they read every tracked file:
  `python3 project/privacy.py` and `python3 project/check_links.py`. They need no Rust. The
  launcher's gate does not run the repository's checks, and `checks.yml` does not run the
  launcher's gate: a change to the website starts no Rust build, and a change to the launcher
  starts both workflows.
- **The brand files are copies made by the kit's tool**, in `launcher/assets/brand/`, listed
  with the website's and the wiki's copies in `website/wiki/scripts/brand.mjs`. The kit is in
  the same repository, so the copies are compared with it on every push (`npm run brand:check`
  in `checks.yml`) and need no record file.

## Consequences

- Three workflow files at the root repeat what the core's shared workflows hold. A fix to the
  core's workflows does not reach them by itself: whoever moves the launcher to a newer core
  compares the root files with the core's. The versions of cargo-deny and cargo-nextest and
  their checksums are written in them a second time.
- `cargo xtask ci --changed` is wrong in the launcher until the core reads changed files from
  the workspace's folder. It is not used by any workflow or hook here, and `AGENTS.md` says not
  to use it.
- The build provenance attestation of a launcher release is signed by this repository's own
  workflow, so it is verified with `--repo jamescjfoundation/wordsmith` alone. An app's is
  signed by the core's shared workflow.
- The wordsmith repository now has Rust in one folder, a `hooks/` folder, a weekly dry run of
  the release, and a weekly look at the core pin.
- The repository has no Dependabot settings. The carried `launcher/.github/dependabot.yml` is
  not read, so nothing proposes newer versions of the actions the root workflows use.

## What was considered and not chosen

- **A repository of its own.** It would make the launcher exactly like the apps, at the price
  of a sixth repository for one small program, and of taking it out of the repository that
  holds the other things that belong to the project as a whole.
- **A Cargo workspace at the repository's root**, with the launcher's packages as members. The
  shared workflows could then be called as they are. But the root would gain a dozen files that
  are the launcher's alone (`Cargo.toml`, `Cargo.lock`, `rust-toolchain.toml`, `deny.toml`,
  `xtask/`, a second `AGENTS.md` block set), `sync` would write the core's blocks into the
  repository's own `AGENTS.md`, `SECURITY.md` and `CONTRIBUTING.md`, where `carry.py` already
  writes some of them from another release, and every push to the website would start a Rust
  build.
- **Changing the core from here.** The core is changed in the core, by its own route.

## Revisit when

The core's shared workflows take a folder (the root workflows become callers), the launcher
grows enough to want a repository of its own, or a second Rust program is added to this
repository.
