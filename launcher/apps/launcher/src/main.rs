// SPDX-License-Identifier: MIT OR Apache-2.0
//! Wordsmith Launcher, the desktop program.
//!
//! `wordsmith-launcher` opens the window. `wordsmith-launcher list`, `install <app>`,
//! `start <app>` and `remove <app>` do the same work without one, and `--version` prints the
//! program's name and version. Everything but this file's `main` is in the library beside it.

#![forbid(unsafe_code)]
#![deny(clippy::unwrap_used, clippy::expect_used, clippy::panic, clippy::unimplemented, clippy::todo, clippy::unreachable)]

use std::ffi::OsString;
use std::process::ExitCode;

use wordsmith_launcher::{DESKTOP, ID, Setup, cli, window};

fn main() -> ExitCode {
    // First of all: on Windows an update is finished by a copy of this program, started with
    // the updater's own arguments. It opens no window and reads no command.
    if let Some(code) = DESKTOP.finish_update() {
        return code;
    }
    let args: Vec<OsString> = std::env::args_os().skip(1).collect();
    match cli::asked(&args) {
        Ok(cli::Asked::Window) => DESKTOP.main(|start| window::Launcher::new(start, Setup::of_this_run(), true)),
        Ok(asked) => cli::run(&asked, &Setup::of_this_run()),
        Err(problem) => {
            eprintln!("{ID}: {problem}\n\n{}", cli::USAGE);
            ExitCode::from(2)
        }
    }
}

#[cfg(test)]
mod tests {
    use wordsmith_launcher::{APP_ID, DESKTOP, ID};

    /// The names a release is found and installed by (the core's `docs/app-releases.md`). The
    /// packaging has the same two ids in `xtask/src/main.rs`, whose own test holds them there:
    /// the xtask cannot read this file, so each side says them and both are tested.
    #[test]
    fn the_program_carries_the_names_a_release_is_found_by() {
        assert_eq!(ID, "wordsmith-launcher");
        assert_eq!(APP_ID, "org.jcjfoundation.launcher");
        // The desktop program is named by the release id, and so is its package.
        assert_eq!(env!("CARGO_BIN_NAME"), ID);
        assert_eq!(env!("CARGO_PKG_NAME"), ID);
        let source = DESKTOP.release_source().unwrap();
        assert_eq!(source.id, ID);
        assert_eq!(source.repo, "jamescjfoundation/wordsmith");
        assert_eq!(source.releases_url(), "https://github.com/jamescjfoundation/wordsmith/releases");
        assert_eq!(source.version, env!("CARGO_PKG_VERSION"));
        assert_eq!(source.developer, "The James C. J. Foundation");
        // An update is installed in place on Linux and Windows; macOS is sent to the release page.
        assert_eq!(source.installs_in_place, !cfg!(target_os = "macos"));
        assert_eq!(DESKTOP.viewport().app_id.as_deref(), Some(APP_ID));
    }
}
