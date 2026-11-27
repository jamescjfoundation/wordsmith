// SPDX-License-Identifier: MIT OR Apache-2.0
//! The launcher without its window: the same work as commands, for a terminal and for scripts.
//!
//! Every command prints what it did on standard output and a problem on standard error, and
//! ends with 0 when it worked, 1 when it did not, and 2 when the command line was not
//! understood.

use std::ffi::OsString;
use std::process::ExitCode;

use wordsmith_launcher_core::install::Target;
use wordsmith_launcher_core::{APPS, AppInfo, Client, Installed, Step, System};

use crate::{ID, Setup};

/// What `--help` prints.
pub const USAGE: &str = "\
usage: wordsmith-launcher [command]

  (no command)       open the window
  list               the Wordsmith apps: what is installed, and the newest release of each
  install <app>      install the newest release of an app, or update it to the newest
  start <app>        start an installed app
  remove <app>       remove an app the launcher installed (settings and documents are kept)
  --version, -V      print the launcher's name and version
  --help, -h         print this

<app> is script, manuscript or book.";

/// What the command line asks for.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Asked {
    /// Open the window.
    Window,
    /// Print the version line.
    Version,
    /// Print [`USAGE`].
    Help,
    /// List the apps.
    List,
    /// Install or update an app.
    Install(&'static AppInfo),
    /// Start an app.
    Start(&'static AppInfo),
    /// Remove an app.
    Remove(&'static AppInfo),
}

/// The app named `name`: by its short name (`book`) or its release id (`wordsmith-book`).
fn app_named(name: &str) -> Option<&'static AppInfo> {
    APPS.iter().find(|app| app.id == name || app.id.strip_prefix("wordsmith-") == Some(name))
}

/// Read the arguments (without the program's name).
pub fn asked(args: &[OsString]) -> Result<Asked, String> {
    let words: Vec<&str> = args.iter().map(|arg| arg.to_str().unwrap_or("\u{fffd}")).collect();
    let app = |name: Option<&&str>, command: &str| match name {
        Some(name) => app_named(name).ok_or_else(|| format!("'{name}' is not a Wordsmith app (script, manuscript or book)")),
        None => Err(format!("{command} needs an app: script, manuscript or book")),
    };
    let only = |count: usize, asked: Asked| if words.len() == count { Ok(asked) } else { Err(format!("'{}' takes no more words", words.join(" "))) };
    match words.first().copied() {
        None => Ok(Asked::Window),
        Some("--version" | "-V") => only(1, Asked::Version),
        Some("--help" | "-h" | "help") => only(1, Asked::Help),
        Some("list") => only(1, Asked::List),
        Some("install" | "update") => only(2, Asked::Install(app(words.get(1), "install")?)),
        Some("start") => only(2, Asked::Start(app(words.get(1), "start")?)),
        Some("remove") => only(2, Asked::Remove(app(words.get(1), "remove")?)),
        Some(other) => Err(format!("'{other}' is not a command")),
    }
}

/// The line `--version` prints: the program's name and its version.
pub fn version_line() -> String {
    format!("{ID} {}", env!("CARGO_PKG_VERSION"))
}

/// One step of an installation, in words. `None` for a step not worth a line of its own.
pub fn words_for(step: &Step) -> String {
    match step {
        Step::Reading => "Reading the release…".to_owned(),
        Step::Downloading { done, total: Some(total) } if *total > 0 => {
            format!("Downloading… {:.0} of {:.0} MB", *done as f64 / 1_048_576.0, *total as f64 / 1_048_576.0)
        }
        Step::Downloading { done, .. } => format!("Downloading… {:.0} MB", *done as f64 / 1_048_576.0),
        Step::Checking => "Checking the download…".to_owned(),
        Step::Unpacking => "Unpacking…".to_owned(),
        Step::Installing => "Installing…".to_owned(),
        Step::Note(note) => note.clone(),
    }
}

fn list(setup: &Setup, client: &Client) -> Result<(), String> {
    let places = setup.places.as_ref().ok();
    let mut failed = None;
    for app in &APPS {
        let installed = match (places, setup.system) {
            (Some(places), Some(system)) => Target { places, system, app }.installed(),
            _ => Installed::No,
        };
        let have = match installed {
            Installed::No => "not installed".to_owned(),
            Installed::Yes { version: Some(version), .. } => format!("installed {version}"),
            Installed::Yes { version: None, .. } => "installed".to_owned(),
        };
        let newest = match client.latest(app) {
            Ok(Some(release)) => format!("newest {}", release.version),
            Ok(None) => "no release yet".to_owned(),
            Err(problem) => {
                failed = Some(problem);
                "newest release unknown".to_owned()
            }
        };
        println!("{:<22} {have:<18} {newest}", app.id);
    }
    failed.map_or(Ok(()), Err)
}

fn install(target: &Target<'_>, client: &Client) -> Result<(), String> {
    let app = target.app;
    let release = client.latest(app)?.ok_or_else(|| format!("{} has no release yet", app.name))?;
    if let Installed::Yes { version: Some(version), .. } = target.installed()
        && version >= release.version
    {
        println!("{} {version} is installed, and it is the newest.", app.name);
        return Ok(());
    }
    let mut last = String::new();
    target.install(client, &release, &mut |step| {
        // One line for the download, not one for every piece of it.
        let words = if matches!(step, Step::Downloading { .. }) { "Downloading…".to_owned() } else { words_for(&step) };
        if words != last {
            println!("{words}");
            last = words;
        }
    })?;
    println!("{} {} is installed: {}", app.name, release.version, target.program().display());
    Ok(())
}

/// Run a command that needs no window.
pub fn run(asked: &Asked, setup: &Setup) -> ExitCode {
    let client = Client::new(env!("CARGO_PKG_VERSION"));
    let target = |app: &'static AppInfo| -> Result<(&wordsmith_launcher_core::Places, System, &'static AppInfo), String> {
        let system = setup.system.ok_or("no release file of the Wordsmith apps is built for this system")?;
        Ok((setup.places.as_ref().map_err(Clone::clone)?, system, app))
    };
    let done = match *asked {
        Asked::Window => Ok(()),
        Asked::Version => {
            println!("{}", version_line());
            Ok(())
        }
        Asked::Help => {
            println!("{USAGE}");
            Ok(())
        }
        Asked::List => list(setup, &client),
        Asked::Install(app) => target(app).and_then(|(places, system, app)| install(&Target { places, system, app }, &client)),
        Asked::Start(app) => {
            target(app).and_then(|(places, system, app)| Target { places, system, app }.start()).map(|_| println!("{} is started.", app.name))
        }
        Asked::Remove(app) => {
            target(app).and_then(|(places, system, app)| Target { places, system, app }.remove()).map(|()| println!("{} is removed.", app.name))
        }
    };
    match done {
        Ok(()) => ExitCode::SUCCESS,
        Err(problem) => {
            eprintln!("{ID}: {problem}");
            ExitCode::FAILURE
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn args(words: &[&str]) -> Vec<OsString> {
        words.iter().map(OsString::from).collect()
    }

    #[test]
    fn the_command_line_is_a_command_or_the_window() {
        assert_eq!(asked(&[]), Ok(Asked::Window));
        assert_eq!(asked(&args(&["--version"])), Ok(Asked::Version));
        assert_eq!(asked(&args(&["-V"])), Ok(Asked::Version));
        assert_eq!(asked(&args(&["--help"])), Ok(Asked::Help));
        assert_eq!(asked(&args(&["list"])), Ok(Asked::List));
        assert_eq!(asked(&args(&["install", "book"])), Ok(Asked::Install(&APPS[2])));
        assert_eq!(asked(&args(&["update", "wordsmith-script"])), Ok(Asked::Install(&APPS[0])));
        assert_eq!(asked(&args(&["start", "manuscript"])), Ok(Asked::Start(&APPS[1])));
        assert_eq!(asked(&args(&["remove", "script"])), Ok(Asked::Remove(&APPS[0])));
        for wrong in
            [&["install"][..], &["install", "word"], &["install", "book", "now"], &["list", "all"], &["open"], &["--verbose"], &["novel.wsm"]]
        {
            assert!(asked(&args(wrong)).is_err(), "{wrong:?}");
        }
        assert_eq!(version_line(), concat!("wordsmith-launcher ", env!("CARGO_PKG_VERSION")));
        // Every command the usage text names is one the program reads.
        for command in ["list", "install", "start", "remove", "--version", "--help"] {
            assert!(USAGE.contains(command), "{command}");
        }
    }

    #[test]
    fn a_step_is_said_in_words() {
        assert_eq!(words_for(&Step::Downloading { done: 26_214_400, total: Some(52_428_800) }), "Downloading… 25 of 50 MB");
        assert_eq!(words_for(&Step::Downloading { done: 1_048_576, total: None }), "Downloading… 1 MB");
        assert_eq!(words_for(&Step::Checking), "Checking the download…");
        assert_eq!(words_for(&Step::Note("a note".into())), "a note");
    }
}
