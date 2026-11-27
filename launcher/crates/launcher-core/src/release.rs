// SPDX-License-Identifier: MIT OR Apache-2.0
//! A release of an app, as the release contract writes it.
//!
//! The contract is open-source-core's `docs/app-releases.md`. What the launcher relies on, from
//! its last section:
//!
//! - the newest release is the newest by version among those that are neither a draft nor a
//!   pre-release, and its tag is `vX.Y.Z`;
//! - the file for a system is found by its name alone: `<id>-<version>-<system><kind>`;
//! - a file is opened only after its SHA-256 checksum has been compared with its line in the
//!   release's `SHA256SUMS.txt`; a file with no line, or with two different ones, is not
//!   installed.
//!
//! Every address a file is fetched from is built here from the app's repository, the tag and
//! the name, never taken from a server's answer. GitHub sends a download on to its own file
//! store; that is followed, and the file is checked against its checksum afterwards.

use std::fmt;

use serde::Deserialize;

use crate::catalog::{AppInfo, System};

/// The name of the checksum file of a release.
pub const SUMS: &str = "SHA256SUMS.txt";

/// A version: three numbers and nothing after them.
#[derive(Clone, Copy, Debug, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub struct Version {
    /// The first number.
    pub major: u64,
    /// The second.
    pub minor: u64,
    /// The third.
    pub patch: u64,
}

impl Version {
    /// A version from its three numbers.
    pub const fn new(major: u64, minor: u64, patch: u64) -> Version {
        Version { major, minor, patch }
    }

    /// `X.Y.Z`, each a plain number. Anything else (`1.2`, `1.2.3-rc.1`, `01.2.3`) is no version.
    pub fn parse(text: &str) -> Option<Version> {
        let mut parts = text.split('.');
        let mut number = || {
            let part = parts.next()?;
            let plain = !part.is_empty() && part.len() <= 9 && part.bytes().all(|b| b.is_ascii_digit()) && (part == "0" || !part.starts_with('0'));
            if plain { part.parse::<u64>().ok() } else { None }
        };
        let version = Version { major: number()?, minor: number()?, patch: number()? };
        parts.next().is_none().then_some(version)
    }

    /// The version a release tag names: `vX.Y.Z`.
    pub fn from_tag(tag: &str) -> Option<Version> {
        Version::parse(tag.strip_prefix('v')?)
    }

    /// Whether this version is before 1.0.0: a preview.
    pub fn is_preview(self) -> bool {
        self.major == 0
    }
}

impl fmt::Display for Version {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}.{}.{}", self.major, self.minor, self.patch)
    }
}

/// One public release of an app.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Release {
    /// Its version.
    pub version: Version,
    /// The day it was published, `YYYY-MM-DD`, when GitHub said so.
    pub date: Option<String>,
    /// What GitHub's API said about its files, when the release was read from the API.
    pub files: Vec<FileFact>,
}

/// What GitHub's API says about one file of a release.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct FileFact {
    /// The file's name.
    pub name: String,
    /// Its size in bytes.
    pub size: Option<u64>,
    /// Its SHA-256 checksum as 64 lower-case hexadecimal digits, when the API gives one.
    pub sha256: Option<String>,
}

impl Release {
    /// A release known by its version alone (found without the API).
    pub fn of(version: Version) -> Release {
        Release { version, date: None, files: Vec::new() }
    }

    /// The release's tag.
    pub fn tag(&self) -> String {
        format!("v{}", self.version)
    }

    /// The release's page, for its notes.
    pub fn page(&self, app: &AppInfo) -> String {
        format!("https://github.com/{}/releases/tag/{}", app.repo, self.tag())
    }

    /// The name of the release file for a system: `<id>-<version>-<system><kind>`.
    pub fn file_name(&self, app: &AppInfo, system: System) -> String {
        format!("{}{}", self.stem(app, system), system.suffix())
    }

    /// The name of the one folder inside a Linux or Windows package: the file's name without
    /// its kind.
    pub fn stem(&self, app: &AppInfo, system: System) -> String {
        format!("{}-{}-{}", app.id, self.version, system.token())
    }

    /// Where a file of this release is downloaded from. `None` for a name that is not a plain
    /// file name, which no release file has.
    pub fn file_url(&self, app: &AppInfo, name: &str) -> Option<String> {
        plain_name(name).then(|| format!("https://github.com/{}/releases/download/{}/{name}", app.repo, self.tag()))
    }

    /// What the API said about the file `name`, if it said anything.
    pub fn fact(&self, name: &str) -> Option<&FileFact> {
        self.files.iter().find(|f| f.name == name)
    }
}

/// Whether `name` holds only what a release file's name may hold: letters, digits, `.`, `-` and
/// `_`, and is not a way out of a folder.
pub fn plain_name(name: &str) -> bool {
    !name.is_empty()
        && name.len() <= 200
        && !name.starts_with('.')
        && name.bytes().all(|b| b.is_ascii_alphanumeric() || matches!(b, b'.' | b'-' | b'_'))
}

#[derive(Deserialize)]
struct ApiRelease {
    tag_name: String,
    #[serde(default)]
    draft: bool,
    #[serde(default)]
    prerelease: bool,
    #[serde(default)]
    published_at: Option<String>,
    #[serde(default)]
    assets: Vec<ApiAsset>,
}

#[derive(Deserialize)]
struct ApiAsset {
    name: String,
    #[serde(default)]
    size: Option<u64>,
    #[serde(default)]
    digest: Option<String>,
}

/// The day of a GitHub time stamp (`2026-11-27T06:19:36Z`), when it is shaped like one.
fn day_of(stamp: &str) -> Option<String> {
    let day = stamp.get(..10)?;
    let shaped = day.bytes().enumerate().all(|(i, b)| if i == 4 || i == 7 { b == b'-' } else { b.is_ascii_digit() });
    shaped.then(|| day.to_owned())
}

/// 64 hexadecimal digits, lower case.
fn checksum(text: &str) -> Option<String> {
    (text.len() == 64 && text.bytes().all(|b| b.is_ascii_digit() || (b'a'..=b'f').contains(&b))).then(|| text.to_owned())
}

/// The newest release in GitHub's answer to `GET /repos/<owner>/<app>/releases`: the newest by
/// version among those that are neither a draft nor a pre-release and whose tag is `vX.Y.Z`.
/// `None` when there is none yet.
pub fn newest(api_json: &str) -> Result<Option<Release>, String> {
    let listed: Vec<ApiRelease> = serde_json::from_str(api_json).map_err(|e| format!("GitHub's list of releases could not be read ({e})"))?;
    let newest = listed
        .into_iter()
        .filter(|r| !r.draft && !r.prerelease)
        .filter_map(|r| Version::from_tag(&r.tag_name).map(|version| (version, r)))
        .max_by_key(|(version, _)| *version);
    Ok(newest.map(|(version, r)| Release {
        version,
        date: r.published_at.as_deref().and_then(day_of),
        files: r
            .assets
            .into_iter()
            .map(|a| FileFact { sha256: a.digest.as_deref().and_then(|d| d.strip_prefix("sha256:")).and_then(checksum), name: a.name, size: a.size })
            .collect(),
    }))
}

/// The version named by the address `https://github.com/<repo>/releases/latest` leads to:
/// `.../releases/tag/vX.Y.Z`. `Ok(None)` when it leads to the list of releases, which is where
/// GitHub sends a repository that has none. Any other address is an error.
pub fn version_of_latest(app: &AppInfo, address: &str) -> Result<Option<Version>, String> {
    let releases = format!("https://github.com/{}/releases", app.repo);
    let rest =
        address.strip_prefix(&releases).ok_or_else(|| format!("{releases}/latest led to {address}, which is not a release of {}", app.name))?;
    match rest.strip_prefix("/tag/") {
        Some(tag) => {
            Version::from_tag(tag).map(Some).ok_or_else(|| format!("the newest release of {} is tagged {tag}, which is not a version", app.name))
        }
        None if rest.is_empty() || rest == "/" => Ok(None),
        None => Err(format!("{releases}/latest led to {address}, which is not a release of {}", app.name)),
    }
}

/// The lines of a `SHA256SUMS.txt`: (checksum, file name) for each.
///
/// A line is 64 lower-case hexadecimal digits, two spaces and a bare file name. A file that
/// holds any other line is refused whole: it is not the file the contract describes, so nothing
/// in it is trusted.
pub fn parse_sums(text: &str) -> Result<Vec<(String, String)>, String> {
    let mut lines = Vec::new();
    for (n, line) in text.split('\n').enumerate() {
        if line.is_empty() && n + 1 == text.split('\n').count() {
            continue; // the line feed that ends the last line
        }
        let line = line.strip_suffix('\r').unwrap_or(line);
        let entry = line.split_once("  ").and_then(|(sum, name)| Some((checksum(sum)?, name))).filter(|(_, name)| plain_name(name));
        match entry {
            Some((sum, name)) => lines.push((sum, name.to_owned())),
            None => return Err(format!("line {} of {SUMS} is not a checksum, two spaces and a file name", n + 1)),
        }
    }
    if lines.is_empty() {
        return Err(format!("{SUMS} lists no file"));
    }
    Ok(lines)
}

/// The checksum the file `name` of `release` must have: its line in the release's
/// `SHA256SUMS.txt`. A file with no line, or with two different ones, has none, and so has one
/// whose line differs from the checksum GitHub's API gives for the same file.
pub fn expected_checksum(release: &Release, sums_text: &str, name: &str) -> Result<String, String> {
    let sums = parse_sums(sums_text)?;
    let mut found = sums.iter().filter(|(_, listed)| listed == name).map(|(sum, _)| sum.as_str());
    let Some(sum) = found.next() else { return Err(format!("{SUMS} of {} has no line for {name}", release.tag())) };
    if found.any(|other| other != sum) {
        return Err(format!("{SUMS} of {} gives two different checksums for {name}", release.tag()));
    }
    if let Some(api) = release.fact(name).and_then(|fact| fact.sha256.as_deref())
        && api != sum
    {
        return Err(format!("{SUMS} of {} and GitHub give different checksums for {name}", release.tag()));
    }
    Ok(sum.to_owned())
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::catalog::APPS;

    const SUM_A: &str = "3b7e0c1f5a9d2e486f0b1c7d9a3e5f2048c6b1d7e9f3a5c20b4d6e8f1a3c5e79";
    const SUM_B: &str = "9f2c4e6a8b0d1f3e5a7c9b1d3f5e7a9c0b2d4f6e8a1c3e5b7d9f0a2c4e6b8d1f";

    #[test]
    fn a_version_is_three_plain_numbers() {
        assert_eq!(Version::parse("0.9.0"), Some(Version::new(0, 9, 0)));
        assert_eq!(Version::parse("12.0.345"), Some(Version::new(12, 0, 345)));
        for wrong in ["", "1", "1.2", "1.2.3.4", "1.2.x", "1.2.3-rc.1", "1.2.3+5", "01.2.3", "1..3", " 1.2.3", "1.2.3 ", "v1.2.3", "1.2.-3"] {
            assert_eq!(Version::parse(wrong), None, "{wrong:?}");
        }
        assert_eq!(Version::from_tag("v1.0.0"), Some(Version::new(1, 0, 0)));
        assert_eq!(Version::from_tag("1.0.0"), None);
        assert_eq!(Version::from_tag("book-view-1.7"), None);
        // Compared as numbers, not as text.
        assert!(Version::new(0, 10, 0) > Version::new(0, 9, 9));
        assert!(Version::new(1, 0, 0) > Version::new(0, 99, 99));
        assert_eq!(Version::new(0, 9, 0).to_string(), "0.9.0");
        assert!(Version::new(0, 9, 0).is_preview() && !Version::new(1, 0, 0).is_preview());
    }

    #[test]
    fn the_files_of_a_release_are_named_as_the_contract_names_them() {
        let release = Release::of(Version::new(1, 2, 3));
        let script = &APPS[0];
        assert_eq!(release.tag(), "v1.2.3");
        assert_eq!(release.file_name(script, System::Linux), "wordsmith-script-1.2.3-linux-x86_64.tar.gz");
        assert_eq!(release.file_name(script, System::Macos), "wordsmith-script-1.2.3-macos-aarch64.dmg");
        assert_eq!(release.file_name(script, System::Windows), "wordsmith-script-1.2.3-windows-x64-portable.zip");
        assert_eq!(release.stem(script, System::Windows), "wordsmith-script-1.2.3-windows-x64");
        assert_eq!(release.page(script), "https://github.com/jamescjfoundation/wordsmith-script/releases/tag/v1.2.3");
        assert_eq!(
            release.file_url(script, SUMS).as_deref(),
            Some("https://github.com/jamescjfoundation/wordsmith-script/releases/download/v1.2.3/SHA256SUMS.txt")
        );
        // A name that could lead elsewhere gets no address.
        for wrong in ["", "../x", "a/b", "a b", ".hidden", "a?b", "a#b", "a%2Fb"] {
            assert_eq!(release.file_url(script, wrong), None, "{wrong:?}");
        }
    }

    #[test]
    fn the_newest_release_is_the_newest_full_one_by_version() {
        let json = r#"[
            {"tag_name": "v0.9.1", "draft": false, "prerelease": false, "published_at": "2026-12-02T10:00:00Z",
             "assets": [{"name": "SHA256SUMS.txt", "size": 330, "digest": "sha256:3b7e0c1f5a9d2e486f0b1c7d9a3e5f2048c6b1d7e9f3a5c20b4d6e8f1a3c5e79"},
                        {"name": "odd", "digest": "md5:abc"}, {"name": "bare"}]},
            {"tag_name": "v0.10.0", "draft": false, "prerelease": false, "published_at": "2026-12-01T10:00:00Z"},
            {"tag_name": "v2.0.0", "draft": true, "prerelease": false},
            {"tag_name": "v1.5.0", "draft": false, "prerelease": true},
            {"tag_name": "book-view-1.7", "draft": false, "prerelease": false},
            {"tag_name": "v1.0.0-rc.1", "draft": false, "prerelease": false}
        ]"#;
        let newest = newest(json).unwrap().unwrap();
        assert_eq!(newest.version, Version::new(0, 10, 0));
        assert_eq!(newest.date.as_deref(), Some("2026-12-01"));
        // Listed first is not newest: the versions decide.
        let older = r#"[{"tag_name": "v0.9.1", "published_at": "not a date",
            "assets": [{"name": "SHA256SUMS.txt", "size": 330, "digest": "sha256:3b7e0c1f5a9d2e486f0b1c7d9a3e5f2048c6b1d7e9f3a5c20b4d6e8f1a3c5e79"},
                       {"name": "odd", "digest": "md5:abc"}, {"name": "upper", "digest": "sha256:3B7E0C1F5A9D2E486F0B1C7D9A3E5F2048C6B1D7E9F3A5C20B4D6E8F1A3C5E79"}]}]"#;
        let only = super::newest(older).unwrap().unwrap();
        assert_eq!(only.date, None);
        assert_eq!(only.fact(SUMS), Some(&FileFact { name: SUMS.into(), size: Some(330), sha256: Some(SUM_A.into()) }));
        // A checksum of another kind, or written another way, is not taken for one.
        assert_eq!(only.fact("odd").unwrap().sha256, None);
        assert_eq!(only.fact("upper").unwrap().sha256, None);
        assert_eq!(super::newest("[]"), Ok(None));
        assert_eq!(super::newest(r#"[{"tag_name": "v1.0.0", "draft": true}]"#), Ok(None));
        assert!(super::newest(r#"{"message": "API rate limit exceeded"}"#).is_err());
        assert!(super::newest("<html>").is_err());
    }

    #[test]
    fn the_address_latest_leads_to_names_the_version() {
        let book = &APPS[2];
        let at = |rest: &str| format!("https://github.com/jamescjfoundation/wordsmith-book/releases{rest}");
        assert_eq!(version_of_latest(book, &at("/tag/v0.9.0")), Ok(Some(Version::new(0, 9, 0))));
        // A repository with no release is sent to its empty list.
        assert_eq!(version_of_latest(book, &at("")), Ok(None));
        assert!(version_of_latest(book, &at("/tag/nightly")).is_err());
        assert!(version_of_latest(book, &at("/tag/v0.9.0/../../x")).is_err());
        assert!(version_of_latest(book, "https://github.com/someone-else/wordsmith-book/releases/tag/v9.9.9").is_err());
        assert!(version_of_latest(book, "https://example.com/login").is_err());
    }

    #[test]
    fn a_checksum_file_is_read_whole_or_not_at_all() {
        let good = format!("{SUM_A}  a-1.0.0-linux-x86_64.tar.gz\n{SUM_B}  a-1.0.0-macos-aarch64.dmg\n");
        assert_eq!(
            parse_sums(&good).unwrap(),
            [(SUM_A.to_owned(), "a-1.0.0-linux-x86_64.tar.gz".to_owned()), (SUM_B.to_owned(), "a-1.0.0-macos-aarch64.dmg".to_owned())]
        );
        // Without the last line feed, and with carriage returns, the lines are the same.
        assert_eq!(parse_sums(good.trim_end()).unwrap().len(), 2);
        assert_eq!(parse_sums(&good.replace('\n', "\r\n")).unwrap().len(), 2);
        let wrong = [
            String::new(),
            "\n".to_owned(),
            format!("{SUM_A} a.tar.gz\n"),           // one space
            format!("{SUM_A}  ./a.tar.gz\n"),        // a path
            format!("{SUM_A} *a.tar.gz\n"),          // binary mode
            format!("{}  a.tar.gz\n", &SUM_A[..63]), // too short
            format!("{}  a.tar.gz\n", SUM_A.to_uppercase()),
            format!("{SUM_A}  a.tar.gz\n\n{SUM_B}  b.dmg\n"), // a blank line
            format!("# sums\n{SUM_A}  a.tar.gz\n"),
            format!("{SUM_A}  ../a.tar.gz\n"),
        ];
        for text in wrong {
            assert!(parse_sums(&text).is_err(), "{text:?}");
        }
    }

    #[test]
    fn a_file_has_a_checksum_only_when_one_line_names_it_and_github_agrees() {
        let mut release = Release::of(Version::new(1, 0, 0));
        let sums = format!("{SUM_A}  a.tar.gz\n{SUM_B}  b.dmg\n");
        assert_eq!(expected_checksum(&release, &sums, "a.tar.gz").as_deref(), Ok(SUM_A));
        assert!(expected_checksum(&release, &sums, "c.zip").unwrap_err().contains("no line for c.zip"));
        // The same line twice is one answer; two answers are none.
        let twice = format!("{sums}{SUM_A}  a.tar.gz\n");
        assert_eq!(expected_checksum(&release, &twice, "a.tar.gz").as_deref(), Ok(SUM_A));
        let two = format!("{sums}{SUM_B}  a.tar.gz\n");
        assert!(expected_checksum(&release, &two, "a.tar.gz").unwrap_err().contains("two different checksums"));
        // What the API says about the file must be the same.
        release.files.push(FileFact { name: "a.tar.gz".into(), size: None, sha256: Some(SUM_A.into()) });
        assert_eq!(expected_checksum(&release, &sums, "a.tar.gz").as_deref(), Ok(SUM_A));
        release.files[0].sha256 = Some(SUM_B.into());
        assert!(expected_checksum(&release, &sums, "a.tar.gz").unwrap_err().contains("GitHub give different checksums"));
        assert!(expected_checksum(&release, "not sums", "a.tar.gz").is_err());
    }
}
