// SPDX-License-Identifier: MIT OR Apache-2.0
//! `cargo xtask screenshots`: the launcher draws its own window into `docs/images/`.
//!
//! The pictures are drawn offscreen by the launcher's own code, never taken from a real desktop.
//! The window is shown with the three apps a release after their first: one installed at the
//! first and with the update to take, one not installed, one up to date. Nothing is read from this computer and nothing is asked of the network: the
//! rows are filled in here, and the folders named in the picture are made up.

#![forbid(unsafe_code)]
#![deny(clippy::unwrap_used, clippy::expect_used, clippy::panic, clippy::unimplemented, clippy::todo, clippy::unreachable)]

use std::path::{Path, PathBuf};
use std::process::ExitCode;

use jcj_shell::desktop::Window;
use jcj_shell::egui;
use jcj_shell::theme::Mode;
use wordsmith_launcher::window::{Launcher, Newest};
use wordsmith_launcher::{DESKTOP, Setup};
use wordsmith_launcher_core::{Installed, Places, Release, System, Version};

/// The first release of the three apps, and the one after it.
const FIRST: Version = Version::new(0, 9, 0);
const NEXT: Version = Version::new(0, 9, 1);
const PUBLISHED: &str = "2026-11-27";

fn draw(out: &Path) -> Result<(), String> {
    std::fs::create_dir_all(out).map_err(|e| format!("{}: {e}", out.display()))?;
    for (name, mode) in [("window", Mode::Light), ("window-dark", Mode::Dark)] {
        let ctx = egui::Context::default();
        let places = Places { data: PathBuf::from("/home/you/.config/wordsmith-launcher"), apps: PathBuf::from("/home/you/.local") };
        let setup = Setup { system: Some(System::Linux), places: Ok(places) };
        // No settings folder: this run keeps nothing.
        let mut window = Window::start(&DESKTOP, &ctx, None, Vec::new(), |start| Launcher::new(start, setup, false));
        window.shell.mode = mode;
        for (row, installed) in window.app.rows.iter_mut().zip([Some(FIRST), None, Some(NEXT)]) {
            row.newest = Newest::Found(Release { date: Some(PUBLISHED.to_owned()), ..Release::of(NEXT) });
            row.installed = Some(match installed {
                Some(version) => Installed::Yes { version: Some(version), by_launcher: true },
                None => Installed::No,
            });
        }
        let picture = jcj_shell::snapshot::render(&ctx, egui::vec2(1040.0, 480.0), 2.0, Vec::new(), 3, |ui| window.ui_offscreen(ui));
        let file = out.join(format!("{name}.png"));
        std::fs::write(&file, picture.to_png()).map_err(|e| format!("{}: {e}", file.display()))?;
        println!("drew {}", file.display());
        window.exit();
    }
    Ok(())
}

fn main() -> ExitCode {
    let Some(out) = std::env::args_os().nth(1).map(PathBuf::from) else {
        eprintln!("usage: screenshots <folder>");
        return ExitCode::from(2);
    };
    match draw(&out) {
        Ok(()) => ExitCode::SUCCESS,
        Err(problem) => {
            eprintln!("screenshots: {problem}");
            ExitCode::FAILURE
        }
    }
}
