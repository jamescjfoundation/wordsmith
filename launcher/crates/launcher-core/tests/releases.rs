// SPDX-License-Identifier: MIT OR Apache-2.0
//! The real 0.9.0 release of each Wordsmith app, read through the code that picks a file and
//! decides its checksum. The releases are recorded in `tests/fixtures/`; `tests/live.rs` reads
//! them from GitHub.

use wordsmith_launcher_core::release::{self, SUMS};
use wordsmith_launcher_core::{APPS, AppInfo, Release, System, Version};

fn fixture(name: &str) -> String {
    let path = std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("tests/fixtures").join(name);
    std::fs::read_to_string(&path).unwrap_or_else(|e| panic!("{}: {e}", path.display()))
}

fn recorded(app: &AppInfo) -> (Release, String) {
    let release = release::newest(&fixture(&format!("{}-releases.json", app.id))).unwrap().expect("a release");
    (release, fixture(&format!("{}-SHA256SUMS.txt", app.id)))
}

#[test]
fn each_app_has_a_first_release_with_a_checked_file_for_every_system() {
    for app in &APPS {
        let (release, sums) = recorded(app);
        assert_eq!(release.version, Version::new(0, 9, 0), "{}", app.id);
        assert_eq!(release.date.as_deref(), Some("2026-11-27"), "{}", app.id);
        assert_eq!(release.page(app), format!("https://github.com/{}/releases/tag/v0.9.0", app.repo));
        // Exactly four files, as the contract says: one for each system, and the checksums.
        assert_eq!(release.files.len(), 4, "{}", app.id);
        assert!(release.fact(SUMS).is_some());
        let lines = release::parse_sums(&sums).unwrap();
        assert_eq!(lines.len(), 3, "{}: one line for each package", app.id);
        for system in System::ALL {
            let name = release.file_name(app, system);
            // The file the launcher asks for by its name alone is a file of the release.
            let fact = release.fact(&name).unwrap_or_else(|| panic!("{name} is not in the release"));
            assert!(fact.size.is_some_and(|size| size > 1_000_000), "{name}");
            // Its checksum is its line of the checksum file, which GitHub's own figure matches.
            let sum = release::expected_checksum(&release, &sums, &name).unwrap();
            assert_eq!(fact.sha256.as_deref(), Some(sum.as_str()), "{name}");
            assert_eq!(release.file_url(app, &name).unwrap(), format!("https://github.com/{}/releases/download/v0.9.0/{name}", app.repo));
        }
        // Found without the API, the release has the same names and the same checksums.
        let by_tag = Release::of(release.version);
        for system in System::ALL {
            let name = by_tag.file_name(app, system);
            assert_eq!(release::expected_checksum(&by_tag, &sums, &name), release::expected_checksum(&release, &sums, &name));
        }
    }
}

#[test]
fn a_file_of_another_app_or_another_version_has_no_checksum_here() {
    let (script, script_sums) = recorded(&APPS[0]);
    let (_, book_sums) = recorded(&APPS[2]);
    let name = script.file_name(&APPS[0], System::Linux);
    // The other app's checksum file has no line for it, and its own gives another checksum
    // than GitHub's figure for a different file would.
    assert!(release::expected_checksum(&script, &book_sums, &name).is_err());
    let next = Release::of(Version::new(0, 9, 1));
    assert!(release::expected_checksum(&next, &script_sums, &next.file_name(&APPS[0], System::Linux)).is_err());
    // A checksum file that was changed is not believed over GitHub's figure.
    let changed = script_sums.replacen('7', "8", 1);
    assert_ne!(changed, script_sums);
    assert!(release::expected_checksum(&script, &changed, &name).is_err());
}
