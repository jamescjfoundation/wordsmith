# Contributing to Wordsmith Launcher

Thank you for helping. The launcher is a folder of the wordsmith repository, which is public:
everything you commit, push, or write in an issue, pull request or review can be read by anyone
and stays in the history for good. [`../CONTRIBUTING.md`](https://github.com/jamescjfoundation/wordsmith/blob/main/CONTRIBUTING.md) is the way into
the repository as a whole; this page is about the launcher.

## Building and checking

From this folder, with Rust installed (`rust-toolchain.toml` names the version):

```sh
cargo run -p wordsmith-launcher            # the launcher
cargo run -p wordsmith-launcher -- list    # the same work without a window
cargo xtask install-hooks                  # once: the repository's pre-commit and pre-push hooks
cargo xtask ci                             # the full gate (CI runs the same)
cargo xtask docs                           # links, decision references (part of the gate)
cargo xtask live                           # with the network: install a real release into a scratch folder, and remove it
cargo xtask package                        # this computer's release package, in dist/ (nothing is published)
```

`cargo xtask help` lists every task. Do not use `cargo xtask ci --changed` here
([`AGENTS.md`](AGENTS.md#where-the-blocks-and-this-folder-differ) says why).

To try the launcher without touching your own apps, name a folder for everything it keeps and
installs: `WORDSMITH_LAUNCHER_PROFILE=/tmp/launcher-try cargo run -p wordsmith-launcher`.

## Where things are

| Path | What it is |
| --- | --- |
| `crates/launcher-core` | What the launcher does, without a window: the apps, their releases, the requests, unpacking, installing, starting and removing |
| `apps/launcher` | The program: the window, its commands, and the command line |
| `assets/brand` | The icons, copied from the brand kit by its tool, and the launcher's theme |
| `xtask` | The gate and maintenance tasks. `src/main.rs` (the launcher's data and its own task) is the launcher's; the other modules, the gate among them, are the core's |
| `docs/guide` | The user guide: the source of the launcher's pages in the wiki |
| `docs/decisions` | Why things are the way they are |
| `.github`, `hooks` | The core's files, carried here. The ones that run are at the repository's root ([`.github/README.md`](.github/README.md)) |

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

## The launcher's own rules

- [`AGENTS.md`](AGENTS.md) has them in full, with what differs here from an app that is a
  repository of its own.
- A change users will see changes the guide (`docs/guide/`) and `CHANGELOG.md` with it.
- The tests in the gate use no network. A test that needs GitHub goes in
  `crates/launcher-core/tests/live.rs`.
