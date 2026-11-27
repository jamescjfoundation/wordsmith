// SPDX-License-Identifier: MIT OR Apache-2.0
//! `cargo xtask <task>` for Wordsmith Launcher, built on open-source-core.
//!
//! This file is the launcher's own. It holds only what is the launcher's: its data (`APP`),
//! which includes what a release carries (`package`: the core's `docs/app-releases.md` says what
//! each field is), and its one task of its own, `live`. The gate, the packaging, every shared
//! task and the list of them are in the modules under `shared`, which the core owns and
//! `cargo xtask sync` keeps identical in every app; `cargo xtask help` lists them. The
//! launcher's layers are the table in `AGENTS.md`, which `cargo xtask app-layers` reads.

#![forbid(unsafe_code)]
#![deny(clippy::unwrap_used, clippy::expect_used, clippy::panic, clippy::unimplemented, clippy::todo, clippy::unreachable)]

mod shared;

use std::path::Path;
use std::process::ExitCode;

use shared::gate::{self, App, Task};
use shared::package::Package;
use shared::util::{TaskResult, cargo};

/// What the shared tasks need to know about the launcher.
const APP: App = App {
    product: "Wordsmith Launcher",
    // The package that builds the one program the launcher ships. The program has its
    // package's name.
    shipped: &["wordsmith-launcher"],
    package: Some(Package {
        // Also the `id` of the update check's source and the settings folder's name
        // (`apps/launcher/src/main.rs`, whose tests hold the two places together).
        id: "wordsmith-launcher",
        // Also the app id the window is given.
        app_id: "org.jcjfoundation.launcher",
        summary: "Install, update and open the Wordsmith apps",
        categories: "Office;Utility;",
        // The parent brand's icon: the kit has none of the launcher's own yet.
        icons: &[
            (32, "assets/brand/icon-32.png"),
            (256, "assets/brand/icon-256.png"),
            (512, "assets/brand/icon-512.png"),
            (1024, "assets/brand/icon-1024.png"),
        ],
        // The kit's icon drawn for macOS, with the margin and corners that system expects.
        macos_icons: &[(1024, "assets/brand/icon-macos-1024.png")],
        // `apps/launcher/build.rs` embeds it in the Windows program.
        windows_icon: Some("assets/brand/icon.ico"),
        ..Package::DEFAULT
    }),
    // `cargo xtask screenshots` redraws docs/images with the launcher's own offscreen renderer
    // (`apps/launcher/examples/screenshots.rs`).
    screenshots: Some("wordsmith-launcher"),
    tasks: TASKS,
    ..App::DEFAULT
};

/// The launcher's own task. `live` is no part of the gate, because it needs the network and
/// downloads a whole release file: it installs one real release of a Wordsmith app into a
/// scratch folder with the launcher's own code, asks the installed program its version, and
/// removes it again (`crates/launcher-core/tests/live.rs`).
const TASKS: &[Task] =
    &[Task::other("live", "install a real release of one Wordsmith app into a scratch folder, start it and remove it (network)", live)];

fn live(root: &Path, args: &[String]) -> TaskResult {
    let mut command = vec!["test", "--locked", "--package", "wordsmith-launcher-core", "--test", "live", "--", "--ignored", "--nocapture"];
    command.extend(args.iter().map(String::as_str));
    cargo(root, &command)
}

fn main() -> ExitCode {
    gate::main(&APP)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn the_task_table_is_sound() {
        assert_eq!(gate::table_problems(&APP), Vec::<String>::new());
        let in_gate = gate::gate_names(&APP);
        for check in ["app-layers", "assets", "release-data", "sync"] {
            assert!(in_gate.contains(&check), "{check} is not in ci");
        }
        // The check that needs the network is run by name, never by the gate.
        assert!(!in_gate.contains(&"live"));
    }

    /// The release names every reader of a release relies on (the core's
    /// `docs/app-releases.md`). `apps/launcher/src/main.rs` has the other half: the program
    /// gives the same two ids.
    #[test]
    fn the_release_carries_the_launchers_names() {
        assert_eq!(APP.shipped, ["wordsmith-launcher"]);
        let package = APP.package.as_ref().map(|p| (p.id, p.app_id));
        assert_eq!(package, Some(("wordsmith-launcher", "org.jcjfoundation.launcher")));
        assert_eq!(shared::package::data_problems(&APP), Vec::<String>::new());
    }
}
