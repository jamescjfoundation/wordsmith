// SPDX-License-Identifier: MIT OR Apache-2.0
//! The launcher's code against GitHub and a real release: `cargo xtask live`.
//!
//! Not part of the gate: it needs the network, and it downloads one whole release file. It
//! reads the newest release of each app, checks that every system's file has a checksum the
//! launcher would accept, then installs one app for this system into a scratch folder, asks the
//! installed program its version, and removes it again. `WORDSMITH_LAUNCHER_LIVE_APP` names the
//! app to install (`wordsmith-manuscript` when unset).

use wordsmith_launcher_core::install::Target;
use wordsmith_launcher_core::release;
use wordsmith_launcher_core::{APPS, Client, Installed, Places, Step, System, Version, catalog};

#[test]
#[ignore = "needs the network and downloads a release file: run it with `cargo xtask live`"]
fn a_real_release_is_read_installed_started_and_removed() {
    let client = Client::new(env!("CARGO_PKG_VERSION"));
    for app in &APPS {
        let newest = client.latest(app).unwrap().unwrap_or_else(|| panic!("{} has no release", app.name));
        assert!(newest.version >= Version::new(0, 9, 0), "{}: {}", app.id, newest.version);
        // The way that needs no API allowance finds the same release.
        let by_page = client.latest_without_the_api(app).unwrap().unwrap();
        assert_eq!(by_page.version, newest.version, "{}", app.id);
        let sums = client.sums(app, &newest).unwrap();
        for system in System::ALL {
            let name = newest.file_name(app, system);
            let sum = release::expected_checksum(&newest, &sums, &name).unwrap();
            assert_eq!(release::expected_checksum(&by_page, &sums, &name).unwrap(), sum);
            println!("{} {}: {name} {sum}", app.name, newest.version);
        }
    }

    let Some(system) = System::host() else {
        println!("no release file is built for this system: nothing is installed");
        return;
    };
    let id = std::env::var("WORDSMITH_LAUNCHER_LIVE_APP").unwrap_or_else(|_| "wordsmith-manuscript".to_owned());
    let app = catalog::app(&id).unwrap_or_else(|| panic!("{id} is not a Wordsmith app"));
    let root = std::env::temp_dir().join(format!("wordsmith-launcher-live-{}", std::process::id()));
    let _ = std::fs::remove_dir_all(&root);
    let places = Places::inside(&root);
    let target = Target { places: &places, system, app };
    assert_eq!(target.installed(), Installed::No);

    let newest = client.latest(app).unwrap().unwrap();
    let mut last = String::new();
    target
        .install(&client, &newest, &mut |step| {
            let words = match &step {
                Step::Downloading { .. } => "downloading".to_owned(),
                other => format!("{other:?}"),
            };
            if words != last {
                println!("{}: {words}", app.name);
                last = words;
            }
        })
        .unwrap();
    let program = target.program();
    assert!(program.starts_with(&root) && program.is_file(), "{}", program.display());
    // The installed program starts and says it is the release that was asked for.
    assert_eq!(target.installed(), Installed::Yes { version: Some(newest.version), by_launcher: true });
    println!("{} {} is installed at {} and answers with its version", app.name, newest.version, program.display());
    assert!(!places.data.join("downloads").join(app.id).exists(), "the download is not kept");

    target.remove().unwrap();
    assert_eq!(target.installed(), Installed::No);
    assert!(!program.exists());
    println!("{} is removed again", app.name);
    std::fs::remove_dir_all(&root).unwrap();
}
