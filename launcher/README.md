# Wordsmith Launcher

One small desktop program for the three Wordsmith apps: Wordsmith Script, Wordsmith Manuscript
and Wordsmith Book. It shows which of them are on your computer and at which version, installs
the ones you want, keeps them up to date, opens them and removes them. It runs on Linux, macOS
and Windows.

> **A note from the founder**
>
> A lot of work has already gone into laying a solid foundation. The apps aren't ready for everyday use yet, but the idea is sound and the pieces are in place. From here, the plan is slow, steady development and testing.
>
> I've been a wannabe developer for years. AI has finally given me the tools to bring an idea like this together, but my time and resources are limited. Ideas, feedback, bug reports, fixes and feature improvements are all welcome. If you care about this as much as we do, we're also open to deeper partnerships.
>
> I'll keep improving the ecosystem where I can while building out the rest of the foundation.
>
> — Dylan J.

- **Install** the newest release of an app for your system, for your account only: nothing asks
  for an administrator's password.
- **Update** an app when a newer release exists.
- **Open** an installed app, and **remove** one the launcher installed. Your documents and the
  app's settings are kept.
- **Checked before it is opened:** every download comes from the app's own releases on GitHub
  and is compared with the release's checksums first.
- **The same promises as the apps:** no account and no tracking. The only requests are to
  GitHub, for the releases, and the ones the launcher makes by itself can be turned off.
- **The same work from a terminal:** `wordsmith-launcher list`, `install <app>`, `start <app>`,
  `remove <app>`.

You do not need the launcher to use the apps: each one can be downloaded and installed by
itself.

## Getting it

Downloads are on the [releases page](https://github.com/jamescjfoundation/wordsmith/releases) of
this repository: a `.tar.gz` for Linux, a `.dmg` for a Mac with Apple silicon and a portable
`.zip` for Windows. [Installing and updating the launcher](docs/guide/installing.md) has the
steps for each system. The first public release is 0.9.0, a preview; `CHANGELOG.md` says what
each release holds.

The user guide is [`docs/guide/`](docs/guide/README.md).

## Building

This folder is a Cargo workspace of its own, inside the wordsmith repository. With Rust installed
(`rust-toolchain.toml` names the version), from this folder:

```sh
cargo run -p wordsmith-launcher            # the launcher
cargo run -p wordsmith-launcher -- list    # the same work without a window
cargo xtask ci                             # every check, clippy and the tests
cargo xtask live                           # with the network: install a real release into a scratch folder, and remove it
```

To try it without touching your own apps, name a folder for everything it keeps and installs:
`WORDSMITH_LAUNCHER_PROFILE=/tmp/launcher-try cargo run -p wordsmith-launcher`.

## How it is made

The launcher is built on [open-source-core](https://github.com/jamescjfoundation/open-source-core),
the shared base of the Wordsmith apps, and is handled like them: it pins one core release,
carries the core's shared files, passes the same gate, and is released by the same contract.
[`AGENTS.md`](AGENTS.md) has the rules for changing it, and [`docs/decisions/`](docs/decisions/README.md)
says why it sits in this folder and what it does and leaves out.

| Path | What it is |
| --- | --- |
| `crates/launcher-core` | What the launcher does, without a window: the apps, their releases, the requests, unpacking, installing, starting and removing |
| `apps/launcher` | The program: the window, its commands, and the command line |
| `assets/brand` | The icons, copied from the brand kit, and the launcher's theme |
| `docs/guide` | The user guide |
| `xtask` | The gate and the release tasks |

## License

The code is MIT OR Apache-2.0, at your option (`LICENSE-MIT`, `LICENSE-APACHE`, `NOTICE`). The
names and the icons are trademarks of The James C. J. Foundation and are not open source
(`ATTRIBUTION.md`).
