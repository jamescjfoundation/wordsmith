// SPDX-License-Identifier: MIT OR Apache-2.0
//! The apps the launcher installs, and the systems a release has a file for.

/// One Wordsmith app.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct AppInfo {
    /// The release id: the stem of every release file and the name of the desktop program.
    pub id: &'static str,
    /// The product's name: the macOS app, and the app's folder on Windows.
    pub name: &'static str,
    /// The GitHub `owner/repository` its releases are read and downloaded from, and only from.
    pub repo: &'static str,
    /// What it is for, in a few words.
    pub summary: &'static str,
}

/// The three apps, in the order the window shows them.
pub const APPS: [AppInfo; 3] = [
    AppInfo {
        id: "wordsmith-script",
        name: "Wordsmith Script",
        repo: "jamescjfoundation/wordsmith-script",
        summary: "Screenplays, TV episodes and stage plays",
    },
    AppInfo {
        id: "wordsmith-manuscript",
        name: "Wordsmith Manuscript",
        repo: "jamescjfoundation/wordsmith-manuscript",
        summary: "Novels and other long work",
    },
    AppInfo {
        id: "wordsmith-book",
        name: "Wordsmith Book",
        repo: "jamescjfoundation/wordsmith-book",
        summary: "Print and ebook editions of a finished book",
    },
];

/// The app with this release id.
pub fn app(id: &str) -> Option<&'static AppInfo> {
    APPS.iter().find(|app| app.id == id)
}

/// A system a release has a file for (the core's `docs/app-releases.md`, "The files").
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum System {
    /// Linux on x86_64: a `.tar.gz`.
    Linux,
    /// macOS on Apple silicon: a `.dmg`.
    Macos,
    /// Windows on x64: a `-portable.zip`.
    Windows,
}

impl System {
    /// Every system, in the order of the file names.
    pub const ALL: [System; 3] = [System::Linux, System::Macos, System::Windows];

    /// The system's part of a release file's name.
    pub fn token(self) -> &'static str {
        match self {
            System::Linux => "linux-x86_64",
            System::Macos => "macos-aarch64",
            System::Windows => "windows-x64",
        }
    }

    /// What follows the token in the file's name: the kind of package.
    pub fn suffix(self) -> &'static str {
        match self {
            System::Linux => ".tar.gz",
            System::Macos => ".dmg",
            System::Windows => "-portable.zip",
        }
    }

    /// The system's name, for people.
    pub fn name(self) -> &'static str {
        match self {
            System::Linux => "Linux (x86_64)",
            System::Macos => "macOS (Apple silicon)",
            System::Windows => "Windows (x64)",
        }
    }

    /// The system of an operating system and a processor, in Rust's names for them.
    pub fn of(os: &str, arch: &str) -> Option<System> {
        match (os, arch) {
            ("linux", "x86_64") => Some(System::Linux),
            ("macos", "aarch64") => Some(System::Macos),
            ("windows", "x86_64") => Some(System::Windows),
            _ => None,
        }
    }

    /// The system this program runs on; `None` when the apps have no release file for it.
    pub fn host() -> Option<System> {
        System::of(std::env::consts::OS, std::env::consts::ARCH)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn the_catalog_holds_the_three_apps_under_their_release_ids() {
        let ids: Vec<&str> = APPS.iter().map(|a| a.id).collect();
        assert_eq!(ids, ["wordsmith-script", "wordsmith-manuscript", "wordsmith-book"]);
        for one in &APPS {
            // An app's releases are its own repository's, under the project's owner.
            assert_eq!(one.repo, format!("jamescjfoundation/{}", one.id));
            assert!(one.name.starts_with("Wordsmith "));
            assert_eq!(app(one.id), Some(one));
        }
        assert_eq!(app("wordsmith-launcher"), None);
    }

    #[test]
    fn a_system_is_named_as_the_release_contract_names_it() {
        assert_eq!(System::of("linux", "x86_64"), Some(System::Linux));
        assert_eq!(System::of("macos", "aarch64"), Some(System::Macos));
        assert_eq!(System::of("windows", "x86_64"), Some(System::Windows));
        // No release file is built for these.
        assert_eq!(System::of("macos", "x86_64"), None);
        assert_eq!(System::of("linux", "aarch64"), None);
        let names: Vec<String> = System::ALL.iter().map(|s| format!("{}{}", s.token(), s.suffix())).collect();
        assert_eq!(names, ["linux-x86_64.tar.gz", "macos-aarch64.dmg", "windows-x64-portable.zip"]);
    }
}
