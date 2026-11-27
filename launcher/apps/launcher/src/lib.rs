// SPDX-License-Identifier: MIT OR Apache-2.0
//! Wordsmith Launcher: one window that lists the Wordsmith apps, installs the ones a writer
//! wants, keeps them up to date, starts them and removes them.
//!
//! The start-up is the core's (`jcj_shell::desktop`): this crate gives the launcher's data
//! ([`DESKTOP`]), its window ([`window`]) and its command line ([`cli`]). What the launcher
//! does is in the `wordsmith-launcher-core` crate; the window shows it and asks for it. The
//! launcher updates itself through the core's update check, from the releases of the repository
//! it is built in.
//!
//! The program is `src/main.rs`. This library exists so that the program's parts can be used
//! without it: by the `screenshots` example, which draws the pictures in `docs/images/`.

#![forbid(unsafe_code)]
#![deny(clippy::unwrap_used, clippy::expect_used, clippy::panic, clippy::unimplemented, clippy::todo, clippy::unreachable)]

pub mod cli;
pub mod window;

use std::path::PathBuf;

use jcj_shell::desktop::{Desktop, Releases};
use jcj_shell::theme::Brand;
use wordsmith_launcher_core::{Places, System};

/// The release id: the stem of every release file, the program's name, and the name of the
/// settings folder on Linux. `xtask/src/main.rs` gives the packaging the same id.
pub const ID: &str = "wordsmith-launcher";

/// The id the window is given. A Linux desktop joins the window to its menu entry and icon by
/// it, and the macOS app carries it; `xtask/src/main.rs` gives the packaging the same id.
pub const APP_ID: &str = "org.jcjfoundation.launcher";

/// The product's name.
pub const NAME: &str = "Wordsmith Launcher";

/// A variable that names one folder for everything a run keeps and installs: its preferences,
/// its records, and the apps themselves. For a run kept apart from the user's own.
pub const PROFILE_ENV: &str = "WORDSMITH_LAUNCHER_PROFILE";

/// The launcher's theme and its window icon. The icon is the parent brand's: the kit has none
/// of the launcher's own yet.
pub const BRAND: Brand = Brand::new(include_str!("../../../assets/brand/tokens.json"), include_bytes!("../../../assets/brand/icon-256.png"));

/// The launcher's data for its start-up.
pub const DESKTOP: Desktop = Desktop {
    brand: BRAND,
    // The launcher is released from the repository it is built in.
    releases: Some(Releases {
        repo: "jamescjfoundation/wordsmith",
        tagline: "Install, update and open the Wordsmith apps",
        developer: "The James C. J. Foundation",
    }),
    profile_env: Some(PROFILE_ENV),
    window_size: Some([820.0, 700.0]),
    ..Desktop::new(NAME, ID, APP_ID, env!("CARGO_PKG_VERSION"))
};

/// Where this run works, and for which system.
#[derive(Clone, Debug)]
pub struct Setup {
    /// The system release files are picked for; `None` when the apps have none for this one.
    pub system: Option<System>,
    /// The folders, or why there are none.
    pub places: Result<Places, String>,
}

impl Setup {
    /// The setup of this run: everything inside the folder [`PROFILE_ENV`] names when it is
    /// set, else the user's own places, with the launcher's records in its settings folder.
    pub fn of_this_run() -> Setup {
        let profile = std::env::var_os(PROFILE_ENV).filter(|dir| !dir.is_empty()).map(PathBuf::from);
        Setup::with(System::host(), profile, DESKTOP.settings_dir())
    }

    /// The setup for a system, a profile folder and a settings folder.
    pub fn with(system: Option<System>, profile: Option<PathBuf>, settings: Option<PathBuf>) -> Setup {
        let places = match (profile, settings, system) {
            (Some(profile), _, _) => Ok(Places::inside(&profile)),
            (None, Some(settings), Some(system)) => Places::for_user(&settings, system),
            (None, Some(settings), None) => Ok(Places { apps: settings.join("apps"), data: settings }),
            (None, None, _) => Err("this system gives the launcher no settings folder to keep its records in".to_owned()),
        };
        Setup { system, places }
    }
}

#[cfg(test)]
mod tests {
    use std::ffi::OsString;

    use super::*;

    #[test]
    fn an_ordinary_start_is_not_an_updates_helper() {
        assert!(DESKTOP.finish_update_with(&[]).is_none());
        assert!(DESKTOP.finish_update_with(&[OsString::from("list")]).is_none());
        assert!(DESKTOP.finish_update_with(&[OsString::from("--version")]).is_none());
        // The updater's own first argument is never read as a command.
        assert!(DESKTOP.finish_update_with(&[OsString::from(jcj_shell::updates::desktop::FINISH_FLAG)]).is_some());
    }

    #[test]
    fn the_brand_files_read_and_the_theme_holds_the_kits_colors() {
        let tokens = BRAND.read_tokens().unwrap();
        assert!(BRAND.icon().is_some_and(|icon| icon.width == 256 && icon.height == 256));
        // The palette is the parent brand's, and each app's mark is that app's color: all of
        // them the kit's, read from its own file at the top of this repository.
        let kit = std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("../../../brand/wordsmith-and-ink/tokens.json");
        let kit = std::fs::read_to_string(&kit).unwrap().to_uppercase();
        let ours = include_str!("../../../assets/brand/tokens.json");
        let palette: std::collections::BTreeMap<String, String> = BRAND.section("palette").unwrap();
        assert_eq!(palette.keys().map(String::as_str).collect::<Vec<_>>(), ["ink", "margin-blue", "night", "paper", "slate"]);
        let marks: std::collections::BTreeMap<String, String> = BRAND.section("launcher").unwrap();
        assert_eq!(marks.len(), 3);
        for (name, color) in palette.iter().chain(&marks) {
            assert!(kit.contains(&format!("\"{}\"", color.to_uppercase())), "{name} ({color}) is not a color of the kit");
        }
        for app in &wordsmith_launcher_core::APPS {
            assert!(marks.contains_key(app.id), "{}", app.id);
        }
        assert!(ours.contains("\"name\": \"wordsmith-launcher\""));
        // Text can be read on every surface in every theme (WCAG AA for body text).
        for mode in [jcj_shell::theme::Mode::Light, jcj_shell::theme::Mode::Dark, jcj_shell::theme::Mode::ExtraDark] {
            let theme = tokens.theme(mode);
            for surface in [theme.canvas, theme.surface, theme.surface_high] {
                assert!(jcj_shell::theme::brand::contrast(theme.text, surface) >= 4.5, "{mode:?}");
                assert!(jcj_shell::theme::brand::contrast(theme.text_dim, surface) >= 4.5, "{mode:?} dim");
            }
        }
    }

    #[test]
    fn a_profile_folder_holds_everything_a_run_keeps_and_installs() {
        let profile = PathBuf::from("/scratch/profile");
        let setup = Setup::with(Some(System::Linux), Some(profile.clone()), Some(PathBuf::from("/home/user/.config/wordsmith-launcher")));
        let places = setup.places.unwrap();
        assert!(places.data.starts_with(&profile) && places.apps.starts_with(&profile));
        // Without one, the records are in the settings folder.
        let setup = Setup::with(None, None, Some(PathBuf::from("/settings")));
        assert_eq!(setup.places.unwrap().data, PathBuf::from("/settings"));
        assert!(Setup::with(Some(System::Linux), None, None).places.is_err());
    }
}
