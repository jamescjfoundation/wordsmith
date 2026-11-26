# Wordsmith Launcher

The front door to the Wordsmith suite: a small desktop app, written in Rust, that installs the Wordsmith apps you want, keeps them up to date, and opens your recent work from any of them.

**Status:** planned, not started. See the [launcher page](https://wordsmithand.ink/launcher) for the idea, and [issue 10](https://github.com/jamescjfoundation/wordsmith/issues/10) for what it needs before it can start.

## What it should do

- **Install what you need:** pick which apps to install.
- **Stay up to date:** see and install updates, downloaded only from the project's official GitHub releases and verified before they run.
- **All your work:** recent screenplays, novels and books in one list, each opened in the right app.
- **Start something new:** choose a screenplay, stage play, novel or book, and the right app opens with the right template.
- **Learn the tools:** guides and getting-started help for every app.
- **Same promises:** no account, no tracking, and update checks can be turned off.

Runs on macOS, Windows and Linux.

## Building

Nothing to build yet. Once the crate exists, from this folder:

```sh
cargo run
cargo fmt --check
cargo clippy --all-targets -- -D warnings
cargo test
```
