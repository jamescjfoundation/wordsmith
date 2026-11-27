// SPDX-License-Identifier: MIT OR Apache-2.0
//! The requests the launcher makes.
//!
//! Two hosts are asked, and only for the repositories in the catalog: `api.github.com` for the
//! list of an app's releases, and `github.com` for the release's files (and, when the API's
//! allowance is used up, for the newest release's tag). GitHub answers a download with a
//! redirect to its own file store, which is followed. Every request is HTTPS, checked against
//! the system's certificates, and carries the launcher's name and version and nothing else: no
//! token, no cookie, nothing about the user or the computer.

use std::io::{Read, Write};
use std::path::Path;
use std::time::Duration;

use sha2::{Digest, Sha256};
use ureq::ResponseExt;
use ureq::tls::{RootCerts, TlsConfig};

use crate::catalog::AppInfo;
use crate::release::{self, Release, SUMS};

/// The most a list of releases or a checksum file may hold. Both are small.
const TEXT_LIMIT: u64 = 4 * 1024 * 1024;
/// The most a release file may hold. The apps' are about 60 MB.
pub const FILE_LIMIT: u64 = 1024 * 1024 * 1024;

/// The launcher's connection to GitHub.
#[derive(Clone, Debug)]
pub struct Client {
    /// For short answers: a time limit on the whole request.
    quick: ureq::Agent,
    /// For a release file: a time limit on connecting and on the whole download.
    slow: ureq::Agent,
}

fn agent(version: &str, whole: Duration) -> ureq::Agent {
    ureq::Agent::config_builder()
        .https_only(true)
        .max_redirects(5)
        .user_agent(format!("WordsmithLauncher/{version}"))
        .tls_config(TlsConfig::builder().root_certs(RootCerts::PlatformVerifier).build())
        .timeout_connect(Some(Duration::from_secs(30)))
        .timeout_global(Some(whole))
        .build()
        .new_agent()
}

/// Why a request failed, for a person.
fn problem(what: &str, error: &ureq::Error) -> String {
    match error {
        ureq::Error::StatusCode(code) => format!("{what}: GitHub answered {code}"),
        other => format!("{what}: {other}"),
    }
}

impl Client {
    /// A connection that says it is the launcher at `version`.
    pub fn new(version: &str) -> Client {
        Client { quick: agent(version, Duration::from_secs(60)), slow: agent(version, Duration::from_secs(60 * 60)) }
    }

    /// The text at `address`, when it is short.
    fn text(&self, address: &str, accept: &str, what: &str) -> Result<String, String> {
        let mut response = self.quick.get(address).header("Accept", accept).call().map_err(|e| problem(what, &e))?;
        response.body_mut().with_config().limit(TEXT_LIMIT).read_to_string().map_err(|e| problem(what, &e))
    }

    /// The newest public release of `app`; `None` when it has none yet.
    ///
    /// GitHub's API is asked first. It allows a computer sixty requests an hour without a
    /// token; when it does not answer, the address of the newest release's page is followed
    /// instead, which names the version, and the files are then found by their names.
    pub fn latest(&self, app: &AppInfo) -> Result<Option<Release>, String> {
        let what = format!("the releases of {}", app.name);
        let listed = self.text(&format!("https://api.github.com/repos/{}/releases?per_page=30", app.repo), "application/vnd.github+json", &what);
        match listed {
            Ok(json) => release::newest(&json),
            Err(api_problem) => self.latest_without_the_api(app).map_err(|e| format!("{api_problem}; and {e}")),
        }
    }

    /// The newest release by the address `releases/latest` leads to.
    pub fn latest_without_the_api(&self, app: &AppInfo) -> Result<Option<Release>, String> {
        let what = format!("the newest release of {}", app.name);
        let response = self.quick.get(&format!("https://github.com/{}/releases/latest", app.repo)).call().map_err(|e| problem(&what, &e))?;
        let landed = response.get_uri().to_string();
        Ok(release::version_of_latest(app, &landed)?.map(Release::of))
    }

    /// The text of the release's `SHA256SUMS.txt`.
    pub fn sums(&self, app: &AppInfo, release: &Release) -> Result<String, String> {
        let address = release.file_url(app, SUMS).ok_or("the checksum file has no address")?;
        self.text(&address, "*/*", &format!("the checksums of {} {}", app.name, release.version))
    }

    /// Download the release file `name` into `to`, and give its SHA-256 checksum as 64
    /// lower-case hexadecimal digits. `progress` is told the bytes written so far and the size
    /// GitHub announced. A file larger than [`FILE_LIMIT`] is refused.
    pub fn download(
        &self,
        app: &AppInfo,
        release: &Release,
        name: &str,
        to: &Path,
        progress: &mut dyn FnMut(u64, Option<u64>),
    ) -> Result<String, String> {
        let what = name;
        let address = release.file_url(app, name).ok_or_else(|| format!("{name} is not a release file's name"))?;
        let mut response = self.slow.get(&address).header("Accept", "application/octet-stream").call().map_err(|e| problem(what, &e))?;
        let total = response.body().content_length().or_else(|| release.fact(name).and_then(|fact| fact.size));
        if total.is_some_and(|size| size > FILE_LIMIT) {
            return Err(format!("{name} is larger than a release file can be"));
        }
        let mut file = std::fs::File::create(to).map_err(|e| format!("{}: {e}", to.display()))?;
        let mut reader = response.body_mut().with_config().limit(FILE_LIMIT).reader();
        let mut hash = Sha256::new();
        let mut buffer = vec![0u8; 256 * 1024];
        let mut done = 0u64;
        loop {
            let read = reader.read(&mut buffer).map_err(|e| format!("{what}: the download stopped ({e})"))?;
            let Some(chunk) = buffer.get(..read).filter(|chunk| !chunk.is_empty()) else { break };
            file.write_all(chunk).map_err(|e| format!("{}: {e}", to.display()))?;
            hash.update(chunk);
            done += chunk.len() as u64;
            progress(done, total);
        }
        file.sync_all().map_err(|e| format!("{}: {e}", to.display()))?;
        if total.is_some_and(|size| size != done) {
            return Err(format!("{what}: the download ended early ({done} bytes of {})", total.unwrap_or_default()));
        }
        Ok(hex(&hash.finalize()))
    }
}

/// Bytes as lower-case hexadecimal digits.
pub fn hex(bytes: &[u8]) -> String {
    use std::fmt::Write as _;
    let mut out = String::with_capacity(bytes.len() * 2);
    for byte in bytes {
        let _ = write!(out, "{byte:02x}");
    }
    out
}

/// The SHA-256 checksum of a file, as 64 lower-case hexadecimal digits.
pub fn sha256_of(path: &Path) -> Result<String, String> {
    let mut file = std::fs::File::open(path).map_err(|e| format!("{}: {e}", path.display()))?;
    let mut hash = Sha256::new();
    let mut buffer = vec![0u8; 256 * 1024];
    loop {
        let read = file.read(&mut buffer).map_err(|e| format!("{}: {e}", path.display()))?;
        let Some(chunk) = buffer.get(..read).filter(|chunk| !chunk.is_empty()) else { break };
        hash.update(chunk);
    }
    Ok(hex(&hash.finalize()))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn a_checksum_is_the_standards() {
        let dir = std::env::temp_dir().join(format!("wordsmith-launcher-net-{}", std::process::id()));
        std::fs::create_dir_all(&dir).unwrap();
        let file = dir.join("abc");
        std::fs::write(&file, b"abc").unwrap();
        // The example of FIPS 180-2 for the message "abc".
        assert_eq!(sha256_of(&file).unwrap(), "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad");
        std::fs::write(&file, b"").unwrap();
        assert_eq!(sha256_of(&file).unwrap(), "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855");
        assert!(sha256_of(&dir.join("missing")).is_err());
        std::fs::remove_dir_all(&dir).unwrap();
        assert_eq!(hex(&[0, 15, 255]), "000fff");
    }
}
