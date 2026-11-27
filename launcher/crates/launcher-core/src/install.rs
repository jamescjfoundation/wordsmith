// SPDX-License-Identifier: MIT OR Apache-2.0
//! Installing, starting and removing an app.
//!
//! Each system's release file is installed the way that file is meant to be, into folders that
//! are the user's own, so no step asks for more rights (the core's `docs/app-releases.md` says
//! what each file holds):
//!
//! | System | The file | Where the app goes | How |
//! | --- | --- | --- | --- |
//! | Linux | `.tar.gz` | `~/.local` (`bin/<id>`, the menu entry, icons, file types) | The package's own `install.sh`, with `PREFIX` set |
//! | Windows | `-portable.zip` | `%LOCALAPPDATA%\Programs\<name>\` | The package's one folder, moved there; then its `register-file-types.cmd` |
//! | macOS | `.dmg` | `~/Applications/<name>.app` | The app copied off the disk image |
//!
//! So an app the launcher installed on Linux is the one a person installs by hand from the same
//! file, in the same place: the launcher finds a copy installed by hand, and the app's own
//! update check keeps working. The launcher keeps a small record of what it installed in its own
//! folder, and removes only that.
//!
//! The installed version is asked of the program itself (`<program> --version`), because an app
//! updates itself in place and the launcher's record would then be behind.

use std::path::{Path, PathBuf};
use std::process::{Child, Command, Stdio};
use std::time::{Duration, Instant};

use serde::{Deserialize, Serialize};

use crate::catalog::{AppInfo, System};
use crate::net::{self, Client};
use crate::release::{self, Release, Version};
use crate::unpack;

/// The folders the launcher works in.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Places {
    /// The launcher's own folder: the records of what it installed, and a download while it is
    /// checked and unpacked.
    pub data: PathBuf,
    /// Where apps go: on Linux the prefix `install.sh` fills, on Windows the folder that holds
    /// one folder for each app, on macOS the folder that holds the apps.
    pub apps: PathBuf,
}

impl Places {
    /// The user's own places: records in `data`, apps where the system keeps a user's own
    /// programs. An error when the system does not say where that is.
    pub fn for_user(data: &Path, system: System) -> Result<Places, String> {
        let home = || std::env::home_dir().filter(|dir| dir.is_absolute()).ok_or("this account has no home folder");
        let apps = match system {
            System::Linux => home()?.join(".local"),
            System::Macos => home()?.join("Applications"),
            System::Windows => {
                let local = std::env::var_os("LOCALAPPDATA").map(PathBuf::from).filter(|dir| dir.is_absolute());
                local.ok_or("Windows did not say where this account's programs go (LOCALAPPDATA)")?.join("Programs")
            }
        };
        Ok(Places { data: data.to_path_buf(), apps })
    }

    /// Every place inside one folder: for a run kept apart from the user's own (a test, a
    /// second profile).
    pub fn inside(root: &Path) -> Places {
        Places { data: root.join("launcher"), apps: root.join("apps") }
    }

    fn record(&self, app: &AppInfo) -> PathBuf {
        self.data.join("installed").join(format!("{}.json", app.id))
    }

    fn uninstaller(&self, app: &AppInfo) -> PathBuf {
        self.data.join("installed").join(format!("{}-uninstall.sh", app.id))
    }

    fn scratch(&self, app: &AppInfo) -> PathBuf {
        self.data.join("downloads").join(app.id)
    }
}

/// A step of an installation, for whoever shows it.
#[derive(Clone, Debug, PartialEq, Eq)]
pub enum Step {
    /// Reading the release's checksums.
    Reading,
    /// Downloading: bytes so far, and the size when it is known.
    Downloading {
        /// Bytes written so far.
        done: u64,
        /// The file's size.
        total: Option<u64>,
    },
    /// Comparing the download with its checksum.
    Checking,
    /// Unpacking the release file.
    Unpacking,
    /// Putting the app in its place.
    Installing,
    /// Something worth saying that did not stop the installation.
    Note(String),
}

/// Whether an app is installed.
#[derive(Clone, Debug, PartialEq, Eq)]
pub enum Installed {
    /// Its program is not in its place.
    No,
    /// Its program is in its place.
    Yes {
        /// The version the program says it is; else the one the launcher recorded.
        version: Option<Version>,
        /// Whether the launcher installed this copy, and so can remove it.
        by_launcher: bool,
    },
}

/// What the launcher writes down about a copy it installed.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
struct Record {
    id: String,
    version: String,
    file: String,
    sha256: String,
}

/// One app, on one system, in the launcher's places.
#[derive(Clone, Copy, Debug)]
pub struct Target<'a> {
    /// The folders.
    pub places: &'a Places,
    /// The system the release file is for.
    pub system: System,
    /// The app.
    pub app: &'a AppInfo,
}

/// An empty folder at `dir`.
fn fresh(dir: &Path) -> Result<(), String> {
    if dir.exists() {
        std::fs::remove_dir_all(dir).map_err(|e| format!("{}: {e}", dir.display()))?;
    }
    std::fs::create_dir_all(dir).map_err(|e| format!("{}: {e}", dir.display()))
}

/// Run a command to its end; an error holds the last of what it said.
fn run(command: &mut Command, what: &str) -> Result<(), String> {
    let out = command.stdin(Stdio::null()).output().map_err(|e| format!("{what} could not be started ({e})"))?;
    if out.status.success() {
        return Ok(());
    }
    let said = String::from_utf8_lossy(&out.stderr);
    let last: Vec<&str> = said.lines().filter(|line| !line.trim().is_empty()).rev().take(3).collect();
    let last: Vec<&str> = last.into_iter().rev().collect();
    Err(format!("{what} failed ({}){}{}", out.status, if last.is_empty() { "" } else { ": " }, last.join(" / ")))
}

/// Copy a folder and everything in it. Only files and folders are copied.
fn copy_folder(from: &Path, to: &Path) -> Result<(), String> {
    std::fs::create_dir_all(to).map_err(|e| format!("{}: {e}", to.display()))?;
    for entry in std::fs::read_dir(from).map_err(|e| format!("{}: {e}", from.display()))? {
        let entry = entry.map_err(|e| format!("{}: {e}", from.display()))?;
        let (source, dest) = (entry.path(), to.join(entry.file_name()));
        let kind = entry.file_type().map_err(|e| format!("{}: {e}", source.display()))?;
        if kind.is_dir() {
            copy_folder(&source, &dest)?;
        } else if kind.is_file() {
            std::fs::copy(&source, &dest).map_err(|e| format!("{}: {e}", dest.display()))?;
        }
    }
    Ok(())
}

/// Move a folder, also to another disk.
fn move_folder(from: &Path, to: &Path) -> Result<(), String> {
    if std::fs::rename(from, to).is_ok() {
        return Ok(());
    }
    copy_folder(from, to)?;
    std::fs::remove_dir_all(from).map_err(|e| format!("{}: {e}", from.display()))
}

/// Put the folder `staged` where `home` is. A copy already at `home` is set aside first and put
/// back if the new one cannot take its place, so a failed update leaves the old version.
fn swap_in(staged: &Path, home: &Path) -> Result<(), String> {
    let mut aside = home.as_os_str().to_owned();
    aside.push(".old");
    let aside = PathBuf::from(aside);
    if aside.exists() {
        std::fs::remove_dir_all(&aside).map_err(|e| format!("{}: {e}", aside.display()))?;
    }
    let had = home.exists();
    if had {
        std::fs::rename(home, &aside)
            .map_err(|e| format!("{} is in use and could not be replaced ({e}). Close the app and try again.", home.display()))?;
    }
    if let Err(e) = std::fs::rename(staged, home) {
        if had {
            let _ = std::fs::rename(&aside, home);
        }
        return Err(format!("{}: {e}", home.display()));
    }
    if had {
        let _ = std::fs::remove_dir_all(&aside);
    }
    Ok(())
}

/// The version in what a program printed for `--version`: the first word of its first line
/// that is a version (`wordsmith-book 0.9.0`, `Wordsmith Script 0.9.0`, `v0.9.0`).
pub fn version_in(printed: &str) -> Option<Version> {
    let line = printed.lines().find(|line| !line.trim().is_empty())?;
    line.split_whitespace().find_map(|word| Version::parse(word.trim_start_matches('v').trim_end_matches([',', ';'])))
}

/// Ask a program its version. `None` when it does not answer within a few seconds or says
/// nothing that is a version; a program that is still running then is stopped.
pub fn version_of(program: &Path) -> Option<Version> {
    let mut child = Command::new(program).arg("--version").stdin(Stdio::null()).stdout(Stdio::piped()).stderr(Stdio::null()).spawn().ok()?;
    let started = Instant::now();
    loop {
        match child.try_wait() {
            Ok(Some(_)) => break,
            Ok(None) if started.elapsed() < Duration::from_secs(8) => std::thread::sleep(Duration::from_millis(40)),
            _ => {
                let _ = child.kill();
                let _ = child.wait();
                return None;
            }
        }
    }
    let out = child.wait_with_output().ok()?;
    version_in(&String::from_utf8_lossy(&out.stdout))
}

impl Target<'_> {
    /// Where the app's desktop program is, once it is installed.
    pub fn program(&self) -> PathBuf {
        match self.system {
            System::Linux => self.places.apps.join("bin").join(self.app.id),
            System::Windows => self.home().join(format!("{}.exe", self.app.id)),
            System::Macos => self.home().join("Contents").join("MacOS").join(self.app.id),
        }
    }

    /// The folder that is the whole app on Windows and macOS. On Linux the app is spread over
    /// the prefix, and this is the prefix.
    pub fn home(&self) -> PathBuf {
        match self.system {
            System::Linux => self.places.apps.clone(),
            System::Windows => self.places.apps.join(self.app.name),
            System::Macos => self.places.apps.join(format!("{}.app", self.app.name)),
        }
    }

    fn read_record(&self) -> Option<Record> {
        let text = std::fs::read_to_string(self.places.record(self.app)).ok()?;
        serde_json::from_str::<Record>(&text).ok().filter(|record| record.id == self.app.id)
    }

    /// Whether the app is installed, and at which version. This starts the program to ask it.
    pub fn installed(&self) -> Installed {
        let program = self.program();
        if !program.is_file() {
            return Installed::No;
        }
        let record = self.read_record();
        let recorded = record.as_ref().and_then(|r| Version::parse(&r.version));
        Installed::Yes { version: version_of(&program).or(recorded), by_launcher: record.is_some() }
    }

    /// Whether the installed program is running, as far as the system tells: on Linux and
    /// Windows a program that runs cannot be opened for writing. macOS does not say.
    pub fn in_use(&self) -> bool {
        if self.system == System::Macos {
            return false;
        }
        match std::fs::OpenOptions::new().write(true).open(self.program()) {
            Ok(_) => false,
            Err(e) => e.kind() != std::io::ErrorKind::NotFound,
        }
    }

    /// Download the release file for this system, check it and install it.
    pub fn install(&self, client: &Client, release: &Release, report: &mut dyn FnMut(Step)) -> Result<(), String> {
        if self.in_use() {
            return Err(format!("{} is running. Close it and try again.", self.app.name));
        }
        let scratch = self.places.scratch(self.app);
        fresh(&scratch)?;
        let done = self.fetch_and_install(client, release, &scratch, report);
        let _ = std::fs::remove_dir_all(&scratch);
        done
    }

    fn fetch_and_install(&self, client: &Client, release: &Release, scratch: &Path, report: &mut dyn FnMut(Step)) -> Result<(), String> {
        let name = release.file_name(self.app, self.system);
        report(Step::Reading);
        let expected = release::expected_checksum(release, &client.sums(self.app, release)?, &name)?;
        let file = scratch.join(&name);
        let got = client.download(self.app, release, &name, &file, &mut |done, total| report(Step::Downloading { done, total }))?;
        report(Step::Checking);
        if got != expected {
            return Err(format!(
                "{name} is not the file the release lists: its checksum is {got}, and the release's is {expected}. Nothing was installed."
            ));
        }
        self.install_file(release, &file, &expected, report)
    }

    /// Install a release file that is already on disk. Its checksum is compared with
    /// `expected` first, here too: nothing is unpacked that was not checked.
    pub fn install_file(&self, release: &Release, file: &Path, expected: &str, report: &mut dyn FnMut(Step)) -> Result<(), String> {
        let name = release.file_name(self.app, self.system);
        let got = net::sha256_of(file)?;
        if got != expected {
            return Err(format!(
                "{name} is not the file the release lists: its checksum is {got}, and the release's is {expected}. Nothing was installed."
            ));
        }
        let work = self.places.scratch(self.app).join("unpacked");
        fresh(&work)?;
        let stem = release.stem(self.app, self.system);
        let done = match self.system {
            System::Linux => self.install_linux(&stem, file, &work, report),
            System::Windows => self.install_windows(&stem, file, &work, report),
            System::Macos => self.install_macos(file, &work, report),
        };
        let _ = std::fs::remove_dir_all(&work);
        done?;
        if !self.program().is_file() {
            return Err(format!("{} was installed, but its program is not at {}", self.app.name, self.program().display()));
        }
        let record = Record { id: self.app.id.to_owned(), version: release.version.to_string(), file: name, sha256: expected.to_owned() };
        let path = self.places.record(self.app);
        if let Some(dir) = path.parent() {
            std::fs::create_dir_all(dir).map_err(|e| format!("{}: {e}", dir.display()))?;
        }
        let text = serde_json::to_string_pretty(&record).map_err(|e| e.to_string())?;
        std::fs::write(&path, text + "\n").map_err(|e| format!("{}: {e}", path.display()))
    }

    fn install_linux(&self, stem: &str, file: &Path, work: &Path, report: &mut dyn FnMut(Step)) -> Result<(), String> {
        report(Step::Unpacking);
        unpack::tar_gz(file, work)?;
        let top = unpack::top_folder(work, stem)?;
        let (install, uninstall) = (top.join("install.sh"), top.join("uninstall.sh"));
        for needed in [&top.join("bin").join(self.app.id), &install, &uninstall] {
            if !needed.is_file() {
                return Err(format!(
                    "the package has no {}: it is not laid out as a release is",
                    needed.strip_prefix(&top).unwrap_or(needed).display()
                ));
            }
        }
        report(Step::Installing);
        std::fs::create_dir_all(&self.places.apps).map_err(|e| format!("{}: {e}", self.places.apps.display()))?;
        run(Command::new("sh").arg(&install).env("PREFIX", &self.places.apps), "the package's install.sh")?;
        // Kept, so that the launcher can take away exactly what this package put there.
        let kept = self.places.uninstaller(self.app);
        if let Some(dir) = kept.parent() {
            std::fs::create_dir_all(dir).map_err(|e| format!("{}: {e}", dir.display()))?;
        }
        std::fs::copy(&uninstall, &kept).map(|_| ()).map_err(|e| format!("{}: {e}", kept.display()))
    }

    fn install_windows(&self, stem: &str, file: &Path, work: &Path, report: &mut dyn FnMut(Step)) -> Result<(), String> {
        report(Step::Unpacking);
        unpack::zip(file, work)?;
        let top = unpack::top_folder(work, stem)?;
        if !top.join(format!("{}.exe", self.app.id)).is_file() {
            return Err(format!("the package has no {}.exe: it is not laid out as a release is", self.app.id));
        }
        report(Step::Installing);
        let home = self.home();
        std::fs::create_dir_all(&self.places.apps).map_err(|e| format!("{}: {e}", self.places.apps.display()))?;
        let mut staged = home.as_os_str().to_owned();
        staged.push(".new");
        let staged = PathBuf::from(staged);
        if staged.exists() {
            std::fs::remove_dir_all(&staged).map_err(|e| format!("{}: {e}", staged.display()))?;
        }
        move_folder(&top, &staged)?;
        swap_in(&staged, &home)?;
        // The package's own script: the app's file types, for this user.
        let register = home.join("register-file-types.cmd");
        if register.is_file() && run(Command::new("cmd").arg("/C").arg(&register).current_dir(&home), "register-file-types.cmd").is_err() {
            report(Step::Note(format!("{} is installed, but its file types could not be registered.", self.app.name)));
        }
        Ok(())
    }

    fn install_macos(&self, file: &Path, work: &Path, report: &mut dyn FnMut(Step)) -> Result<(), String> {
        report(Step::Unpacking);
        let volume = work.join("volume");
        std::fs::create_dir_all(&volume).map_err(|e| format!("{}: {e}", volume.display()))?;
        run(
            Command::new("hdiutil").args(["attach", "-nobrowse", "-readonly", "-noautoopen", "-mountpoint"]).arg(&volume).arg(file),
            "opening the disk image",
        )?;
        let done = self.copy_off_the_volume(&volume, report);
        let _ = run(Command::new("hdiutil").arg("detach").arg(&volume).arg("-force"), "closing the disk image");
        done
    }

    fn copy_off_the_volume(&self, volume: &Path, report: &mut dyn FnMut(Step)) -> Result<(), String> {
        let bundle = format!("{}.app", self.app.name);
        let from = volume.join(&bundle);
        if !from.join("Contents").join("MacOS").join(self.app.id).is_file() {
            return Err(format!("the disk image has no {bundle} with the program {}: it is not laid out as a release is", self.app.id));
        }
        report(Step::Installing);
        std::fs::create_dir_all(&self.places.apps).map_err(|e| format!("{}: {e}", self.places.apps.display()))?;
        let home = self.home();
        let mut staged = home.as_os_str().to_owned();
        staged.push(".new");
        let staged = PathBuf::from(staged);
        if staged.exists() {
            std::fs::remove_dir_all(&staged).map_err(|e| format!("{}: {e}", staged.display()))?;
        }
        // The system's own copy, which keeps an app whole (its signature, its links).
        run(Command::new("ditto").arg(&from).arg(&staged), "copying the app")?;
        swap_in(&staged, &home)
    }

    /// Remove a copy the launcher installed. Settings and documents are left alone.
    pub fn remove(&self) -> Result<(), String> {
        if self.read_record().is_none() {
            return Err(format!("The launcher did not install this copy of {}, so it leaves it alone.", self.app.name));
        }
        if self.in_use() {
            return Err(format!("{} is running. Close it and try again.", self.app.name));
        }
        match self.system {
            System::Linux => {
                let kept = self.places.uninstaller(self.app);
                run(Command::new("sh").arg(&kept).env("PREFIX", &self.places.apps), "the package's uninstall.sh")?;
                let _ = std::fs::remove_file(&kept);
            }
            System::Windows => {
                let home = self.home();
                let unregister = home.join("unregister-file-types.cmd");
                if unregister.is_file() {
                    let _ = run(Command::new("cmd").arg("/C").arg(&unregister).current_dir(&home), "unregister-file-types.cmd");
                }
                std::fs::remove_dir_all(&home).map_err(|e| format!("{}: {e}", home.display()))?;
            }
            System::Macos => {
                let home = self.home();
                std::fs::remove_dir_all(&home).map_err(|e| format!("{}: {e}", home.display()))?;
            }
        }
        let record = self.places.record(self.app);
        std::fs::remove_file(&record).map_err(|e| format!("{}: {e}", record.display()))
    }

    /// Start the installed app. On macOS the system starts it and nothing is returned to wait
    /// for; elsewhere the running program is returned.
    pub fn start(&self) -> Result<Option<Child>, String> {
        let program = self.program();
        if !program.is_file() {
            return Err(format!("{} is not installed.", self.app.name));
        }
        if self.system == System::Macos {
            return run(Command::new("open").arg(self.home()), &format!("opening {}", self.app.name)).map(|()| None);
        }
        let child = Command::new(&program).stdin(Stdio::null()).stdout(Stdio::null()).stderr(Stdio::null()).spawn();
        child.map(Some).map_err(|e| format!("{} could not be started ({e})", self.app.name))
    }
}

#[cfg(test)]
mod tests {
    use std::io::Write as _;

    use super::*;
    use crate::catalog::APPS;

    fn scratch(tag: &str) -> PathBuf {
        let dir = std::env::temp_dir().join(format!("wordsmith-launcher-install-{tag}-{}", std::process::id()));
        let _ = std::fs::remove_dir_all(&dir);
        std::fs::create_dir_all(&dir).unwrap();
        dir
    }

    #[test]
    fn the_version_is_read_from_what_a_program_prints() {
        assert_eq!(version_in("wordsmith-book 0.9.0\n"), Some(Version::new(0, 9, 0)));
        assert_eq!(version_in("\nWordsmith Script 1.2.3\nBased on other work 9.9.9\n"), Some(Version::new(1, 2, 3)));
        assert_eq!(version_in("app v2.0.1, built today"), Some(Version::new(2, 0, 1)));
        assert_eq!(version_in("usage: app [file]"), None);
        assert_eq!(version_in(""), None);
        // A program that is not there, or is no program, has no version.
        assert_eq!(version_of(Path::new("/nonexistent/program")), None);
    }

    #[test]
    fn every_place_is_inside_the_folder_a_separate_run_names() {
        let root = Path::new("/scratch/run");
        let places = Places::inside(root);
        for system in System::ALL {
            for app in &APPS {
                let target = Target { places: &places, system, app };
                assert!(target.program().starts_with(root), "{system:?} {}", app.id);
                assert!(target.home().starts_with(root));
            }
        }
        let script = Target { places: &places, system: System::Linux, app: &APPS[0] };
        assert_eq!(script.program(), root.join("apps/bin/wordsmith-script"));
        let script = Target { places: &places, system: System::Windows, app: &APPS[0] };
        assert_eq!(script.program(), root.join("apps").join("Wordsmith Script").join("wordsmith-script.exe"));
        let script = Target { places: &places, system: System::Macos, app: &APPS[0] };
        assert_eq!(script.program(), root.join("apps/Wordsmith Script.app/Contents/MacOS/wordsmith-script"));
        assert!(places.record(&APPS[0]).starts_with(root) && places.scratch(&APPS[0]).starts_with(root));
    }

    #[test]
    fn a_new_folder_takes_the_place_of_the_old_one() {
        let dir = scratch("swap");
        let (home, staged) = (dir.join("App"), dir.join("App.new"));
        std::fs::create_dir_all(&home).unwrap();
        std::fs::write(home.join("old.txt"), b"old").unwrap();
        std::fs::create_dir_all(staged.join("inner")).unwrap();
        std::fs::write(staged.join("inner/new.txt"), b"new").unwrap();
        swap_in(&staged, &home).unwrap();
        assert!(home.join("inner/new.txt").is_file() && !home.join("old.txt").exists());
        assert!(!staged.exists() && !dir.join("App.old").exists());
        // The first time there is nothing to set aside.
        let (first, staged) = (dir.join("First"), dir.join("First.new"));
        std::fs::create_dir_all(&staged).unwrap();
        swap_in(&staged, &first).unwrap();
        assert!(first.is_dir());
        // A folder is copied whole when it cannot be renamed.
        copy_folder(&home, &dir.join("Copy")).unwrap();
        assert_eq!(std::fs::read(dir.join("Copy/inner/new.txt")).unwrap(), b"new");
        std::fs::remove_dir_all(&dir).unwrap();
    }

    /// A release file made for the test, laid out as the contract lays out a Linux package: one
    /// folder, a program that prints its version, and the two scripts.
    #[cfg(unix)]
    fn linux_package(app: &AppInfo, release: &Release, to: &Path, with_uninstaller: bool) {
        let stem = release.stem(app, System::Linux);
        let program = format!("#!/bin/sh\necho \"{} {}\"\n", app.id, release.version);
        let install = "#!/bin/sh\nset -eu\nhere=$(cd \"$(dirname \"$0\")\" && pwd)\nmkdir -p \"$PREFIX/bin\" \"$PREFIX/share\"\n\
                       cp \"$here\"/bin/* \"$PREFIX/bin/\"\ncp -R \"$here/share/.\" \"$PREFIX/share/\"\n";
        let uninstall = format!("#!/bin/sh\nset -eu\nrm -f \"$PREFIX/bin/{id}\"\nrm -rf \"$PREFIX/share/{id}\"\n", id = app.id);
        let mut files = vec![
            (format!("{stem}/bin/{}", app.id), 0o755, program),
            (format!("{stem}/share/{}/NOTICE", app.id), 0o644, "a notice\n".to_owned()),
            (format!("{stem}/install.sh"), 0o755, install.to_owned()),
        ];
        if with_uninstaller {
            files.push((format!("{stem}/uninstall.sh"), 0o755, uninstall));
        }
        let mut builder = tar::Builder::new(flate2::write::GzEncoder::new(Vec::new(), flate2::Compression::fast()));
        for (name, mode, contents) in files {
            let mut header = tar::Header::new_gnu();
            header.set_mode(mode);
            header.set_size(contents.len() as u64);
            builder.append_data(&mut header, name, contents.as_bytes()).unwrap();
        }
        std::fs::write(to, builder.into_inner().unwrap().finish().unwrap()).unwrap();
    }

    #[cfg(unix)]
    #[test]
    fn a_linux_package_is_installed_found_started_and_removed() {
        let dir = scratch("linux");
        let places = Places::inside(&dir);
        let app = &APPS[1];
        let target = Target { places: &places, system: System::Linux, app };
        let release = Release::of(Version::new(1, 2, 3));
        let file = dir.join(release.file_name(app, System::Linux));
        linux_package(app, &release, &file, true);
        let sum = net::sha256_of(&file).unwrap();
        assert_eq!(target.installed(), Installed::No);
        assert!(target.start().unwrap_err().contains("is not installed"));

        let mut steps = Vec::new();
        target.install_file(&release, &file, &sum, &mut |step| steps.push(step)).unwrap();
        assert_eq!(steps, [Step::Unpacking, Step::Installing]);
        assert!(dir.join("apps/bin/wordsmith-manuscript").is_file());
        assert!(dir.join("apps/share/wordsmith-manuscript/NOTICE").is_file());
        // The version is the one the program says, and the copy is the launcher's.
        assert_eq!(target.installed(), Installed::Yes { version: Some(Version::new(1, 2, 3)), by_launcher: true });
        assert!(!places.scratch(app).join("unpacked").exists(), "the unpacked package is not kept");
        let mut child = target.start().unwrap().unwrap();
        assert!(child.wait().unwrap().success());

        // A newer release takes the older one's place.
        let newer = Release::of(Version::new(1, 3, 0));
        let file = dir.join(newer.file_name(app, System::Linux));
        linux_package(app, &newer, &file, true);
        target.install_file(&newer, &file, &net::sha256_of(&file).unwrap(), &mut |_| {}).unwrap();
        assert_eq!(target.installed(), Installed::Yes { version: Some(Version::new(1, 3, 0)), by_launcher: true });

        target.remove().unwrap();
        assert_eq!(target.installed(), Installed::No);
        assert!(!dir.join("apps/share/wordsmith-manuscript").exists());
        assert!(!places.record(app).exists() && !places.uninstaller(app).exists());
        assert!(target.remove().unwrap_err().contains("did not install"));
        std::fs::remove_dir_all(&dir).unwrap();
    }

    #[cfg(unix)]
    #[test]
    fn a_file_that_is_not_the_releases_is_not_installed() {
        let dir = scratch("refused");
        let places = Places::inside(&dir);
        let app = &APPS[0];
        let target = Target { places: &places, system: System::Linux, app };
        let release = Release::of(Version::new(1, 0, 0));
        let file = dir.join(release.file_name(app, System::Linux));
        linux_package(app, &release, &file, true);
        let sum = net::sha256_of(&file).unwrap();
        // One byte more than the release lists: the checksum differs, and nothing is unpacked.
        std::fs::OpenOptions::new().append(true).open(&file).unwrap().write_all(b"\n").unwrap();
        let refused = target.install_file(&release, &file, &sum, &mut |_| {}).unwrap_err();
        assert!(refused.contains("is not the file the release lists"), "{refused}");
        assert!(!dir.join("apps").exists() && !places.record(app).exists());

        // A package under another version's name, and one without its scripts, are not a release's.
        let other = Release::of(Version::new(2, 0, 0));
        linux_package(app, &other, &file, true);
        let refused = target.install_file(&release, &file, &net::sha256_of(&file).unwrap(), &mut |_| {}).unwrap_err();
        assert!(refused.contains("does not hold the one folder"), "{refused}");
        linux_package(app, &release, &file, false);
        let refused = target.install_file(&release, &file, &net::sha256_of(&file).unwrap(), &mut |_| {}).unwrap_err();
        assert!(refused.contains("has no uninstall.sh"), "{refused}");
        assert_eq!(target.installed(), Installed::No);
        std::fs::remove_dir_all(&dir).unwrap();
    }

    #[cfg(unix)]
    #[test]
    fn a_copy_installed_by_hand_is_found_and_left_alone() {
        let dir = scratch("by-hand");
        let places = Places::inside(&dir);
        let target = Target { places: &places, system: System::Linux, app: &APPS[2] };
        std::fs::create_dir_all(dir.join("apps/bin")).unwrap();
        let program = dir.join("apps/bin/wordsmith-book");
        std::fs::write(&program, "#!/bin/sh\necho 'wordsmith-book 0.9.0'\n").unwrap();
        {
            use std::os::unix::fs::PermissionsExt;
            std::fs::set_permissions(&program, std::fs::Permissions::from_mode(0o755)).unwrap();
        }
        assert_eq!(target.installed(), Installed::Yes { version: Some(Version::new(0, 9, 0)), by_launcher: false });
        assert!(target.remove().unwrap_err().contains("did not install"));
        assert!(program.is_file());
        std::fs::remove_dir_all(&dir).unwrap();
    }

    /// The Windows package is a folder that is moved into place, so its steps run on any system.
    #[test]
    fn a_windows_package_is_moved_into_its_folder_and_removed() {
        use zip::write::SimpleFileOptions;
        let dir = scratch("windows");
        let places = Places::inside(&dir);
        let app = &APPS[0];
        let target = Target { places: &places, system: System::Windows, app };
        let package = |release: &Release, mark: &[u8]| {
            let stem = release.stem(app, System::Windows);
            let mut writer = zip::ZipWriter::new(std::io::Cursor::new(Vec::new()));
            writer.add_directory(format!("{stem}/"), SimpleFileOptions::default()).unwrap();
            for (name, contents) in [("wordsmith-script.exe", mark), ("NOTICE", b"a notice".as_slice())] {
                writer.start_file(format!("{stem}/{name}"), SimpleFileOptions::default()).unwrap();
                writer.write_all(contents).unwrap();
            }
            let file = dir.join(release.file_name(app, System::Windows));
            std::fs::write(&file, writer.finish().unwrap().into_inner()).unwrap();
            file
        };
        let first = Release::of(Version::new(1, 0, 0));
        let file = package(&first, b"one");
        target.install_file(&first, &file, &net::sha256_of(&file).unwrap(), &mut |_| {}).unwrap();
        let home = dir.join("apps").join("Wordsmith Script");
        assert_eq!(std::fs::read(home.join("wordsmith-script.exe")).unwrap(), b"one");
        // The made-up program cannot be asked, so the version is the launcher's record of it.
        assert_eq!(target.installed(), Installed::Yes { version: Some(Version::new(1, 0, 0)), by_launcher: true });

        let second = Release::of(Version::new(1, 1, 0));
        let file = package(&second, b"two");
        target.install_file(&second, &file, &net::sha256_of(&file).unwrap(), &mut |_| {}).unwrap();
        assert_eq!(std::fs::read(home.join("wordsmith-script.exe")).unwrap(), b"two");
        assert_eq!(target.installed(), Installed::Yes { version: Some(Version::new(1, 1, 0)), by_launcher: true });
        let beside: Vec<_> = std::fs::read_dir(dir.join("apps")).unwrap().map(|e| e.unwrap().file_name()).collect();
        assert_eq!(beside, ["Wordsmith Script"], "nothing is left beside the app");

        target.remove().unwrap();
        assert!(!home.exists());
        assert_eq!(target.installed(), Installed::No);
        std::fs::remove_dir_all(&dir).unwrap();
    }
}
