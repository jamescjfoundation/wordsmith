// SPDX-License-Identifier: MIT OR Apache-2.0
//! Unpacking a release file into a folder.
//!
//! A release file is checked against its checksum before it comes here, so what is unpacked is
//! what the app's release workflow built. The bounds below are a second line: nothing is written
//! outside the folder named, nothing but files and folders is made, and an archive cannot ask
//! for more files or more room than a release could hold.

use std::fs::File;
use std::io::{BufReader, Read, Write};
use std::path::{Component, Path, PathBuf};

/// The most files and folders an archive may hold.
pub const MAX_ENTRIES: usize = 20_000;
/// The most room an archive may take once unpacked.
pub const MAX_BYTES: u64 = 2 * 1024 * 1024 * 1024;

/// What an archive has used of its bounds so far.
#[derive(Default)]
struct Used {
    entries: usize,
    bytes: u64,
}

impl Used {
    fn entry(&mut self, name: &Path) -> Result<(), String> {
        self.entries += 1;
        if self.entries > MAX_ENTRIES { Err(format!("the archive holds more than {MAX_ENTRIES} files ({})", name.display())) } else { Ok(()) }
    }
}

/// `into` joined with `name`, when `name` is a plain path down from a folder: no root, no
/// drive, no `..`.
fn inside(into: &Path, name: &Path) -> Result<PathBuf, String> {
    let plain = name.components().all(|part| matches!(part, Component::Normal(_) | Component::CurDir));
    let down: PathBuf = name.components().filter(|part| matches!(part, Component::Normal(_))).collect();
    if !plain || down.as_os_str().is_empty() {
        return Err(format!("the archive names {}, which is not a place inside it", name.display()));
    }
    Ok(into.join(down))
}

/// Copy one file of an archive to `to`, counting its bytes against the bound.
fn write_file(from: &mut dyn Read, to: &Path, used: &mut Used) -> Result<(), String> {
    if let Some(dir) = to.parent() {
        std::fs::create_dir_all(dir).map_err(|e| format!("{}: {e}", dir.display()))?;
    }
    let mut file = File::create(to).map_err(|e| format!("{}: {e}", to.display()))?;
    let mut buffer = vec![0u8; 256 * 1024];
    loop {
        let read = from.read(&mut buffer).map_err(|e| format!("{}: the archive is damaged ({e})", to.display()))?;
        let Some(chunk) = buffer.get(..read).filter(|chunk| !chunk.is_empty()) else { return Ok(()) };
        used.bytes += chunk.len() as u64;
        if used.bytes > MAX_BYTES {
            return Err("the archive unpacks to more than a release can hold".to_owned());
        }
        file.write_all(chunk).map_err(|e| format!("{}: {e}", to.display()))?;
    }
}

/// Make a file a program, where the system has such a mark.
#[cfg(unix)]
fn mark_program(path: &Path, mode: u32) -> Result<(), String> {
    use std::os::unix::fs::PermissionsExt;
    let mode = if mode & 0o111 != 0 { 0o755 } else { 0o644 };
    std::fs::set_permissions(path, std::fs::Permissions::from_mode(mode)).map_err(|e| format!("{}: {e}", path.display()))
}

#[cfg(not(unix))]
fn mark_program(_path: &Path, _mode: u32) -> Result<(), String> {
    Ok(())
}

/// Unpack a gzip-compressed tar archive into the folder `into`, which is made. Only files and
/// folders are taken: an archive that holds a link or a device is refused.
pub fn tar_gz(archive: &Path, into: &Path) -> Result<(), String> {
    let file = File::open(archive).map_err(|e| format!("{}: {e}", archive.display()))?;
    let mut tar = tar::Archive::new(flate2::read::GzDecoder::new(BufReader::new(file)));
    std::fs::create_dir_all(into).map_err(|e| format!("{}: {e}", into.display()))?;
    let mut used = Used::default();
    let damaged = |e: std::io::Error| format!("{}: the archive is damaged ({e})", archive.display());
    for entry in tar.entries().map_err(damaged)? {
        let mut entry = entry.map_err(damaged)?;
        let name = entry.path().map_err(damaged)?.into_owned();
        used.entry(&name)?;
        let to = inside(into, &name)?;
        let kind = entry.header().entry_type();
        if kind.is_dir() {
            std::fs::create_dir_all(&to).map_err(|e| format!("{}: {e}", to.display()))?;
        } else if kind.is_file() {
            let mode = entry.header().mode().unwrap_or(0o644);
            write_file(&mut entry, &to, &mut used)?;
            mark_program(&to, mode)?;
        } else {
            return Err(format!("the archive holds {}, which is neither a file nor a folder", name.display()));
        }
    }
    Ok(())
}

/// Unpack a zip archive into the folder `into`, which is made. Only files and folders are taken.
pub fn zip(archive: &Path, into: &Path) -> Result<(), String> {
    let file = File::open(archive).map_err(|e| format!("{}: {e}", archive.display()))?;
    let damaged = |e: ::zip::result::ZipError| format!("{}: the archive is damaged ({e})", archive.display());
    let mut zip = ::zip::ZipArchive::new(BufReader::new(file)).map_err(damaged)?;
    std::fs::create_dir_all(into).map_err(|e| format!("{}: {e}", into.display()))?;
    let mut used = Used::default();
    for index in 0..zip.len() {
        let mut entry = zip.by_index(index).map_err(damaged)?;
        let Some(name) = entry.enclosed_name() else {
            return Err(format!("file {} of the archive is named for a place outside it", index + 1));
        };
        used.entry(&name)?;
        let to = inside(into, &name)?;
        if entry.is_dir() {
            std::fs::create_dir_all(&to).map_err(|e| format!("{}: {e}", to.display()))?;
        } else if entry.is_file() {
            let mode = entry.unix_mode().unwrap_or(0o644);
            write_file(&mut entry, &to, &mut used)?;
            mark_program(&to, mode)?;
        } else {
            return Err(format!("the archive holds {}, which is neither a file nor a folder", name.display()));
        }
    }
    Ok(())
}

/// The one folder at the top of an unpacked package, which must be named `stem` and be alone.
pub fn top_folder(unpacked: &Path, stem: &str) -> Result<PathBuf, String> {
    let mut names = Vec::new();
    for entry in std::fs::read_dir(unpacked).map_err(|e| format!("{}: {e}", unpacked.display()))? {
        names.push(entry.map_err(|e| format!("{}: {e}", unpacked.display()))?.file_name());
    }
    let top = unpacked.join(stem);
    if names.len() == 1 && names.first().is_some_and(|name| name == stem) && top.is_dir() {
        Ok(top)
    } else {
        Err(format!("the package does not hold the one folder {stem}: it is not laid out as a release is"))
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn scratch(tag: &str) -> PathBuf {
        let dir = std::env::temp_dir().join(format!("wordsmith-launcher-unpack-{tag}-{}", std::process::id()));
        let _ = std::fs::remove_dir_all(&dir);
        std::fs::create_dir_all(&dir).unwrap();
        dir
    }

    /// A tar archive from (name, kind, mode, contents, link target). A name is written into the
    /// header as it is given, so a test can make an archive no honest tool would.
    fn tar_of(entries: &[(&str, tar::EntryType, u32, &[u8], &str)]) -> Vec<u8> {
        let mut builder = tar::Builder::new(Vec::new());
        for (name, kind, mode, contents, link) in entries {
            let mut header = tar::Header::new_gnu();
            header.as_gnu_mut().unwrap().name[..name.len()].copy_from_slice(name.as_bytes());
            header.set_entry_type(*kind);
            header.set_mode(*mode);
            header.set_size(contents.len() as u64);
            if !link.is_empty() {
                header.set_link_name(link).unwrap();
            }
            header.set_cksum();
            builder.append(&header, *contents).unwrap();
        }
        builder.into_inner().unwrap()
    }

    fn gz(bytes: &[u8]) -> Vec<u8> {
        let mut encoder = flate2::write::GzEncoder::new(Vec::new(), flate2::Compression::fast());
        encoder.write_all(bytes).unwrap();
        encoder.finish().unwrap()
    }

    #[test]
    fn a_tar_archive_is_unpacked_with_its_folders_and_its_programs() {
        let dir = scratch("tar");
        let file = tar::EntryType::Regular;
        let archive = dir.join("a.tar.gz");
        let bytes = tar_of(&[
            ("app-1.0.0/", tar::EntryType::Directory, 0o755, b"", ""),
            ("app-1.0.0/bin/app", file, 0o755, b"#!/bin/sh\n", ""),
            ("app-1.0.0/share/app/NOTICE", file, 0o644, b"notice", ""),
        ]);
        std::fs::write(&archive, gz(&bytes)).unwrap();
        let out = dir.join("out");
        tar_gz(&archive, &out).unwrap();
        assert_eq!(std::fs::read(out.join("app-1.0.0/share/app/NOTICE")).unwrap(), b"notice");
        #[cfg(unix)]
        {
            use std::os::unix::fs::PermissionsExt;
            assert_eq!(std::fs::metadata(out.join("app-1.0.0/bin/app")).unwrap().permissions().mode() & 0o777, 0o755);
            assert_eq!(std::fs::metadata(out.join("app-1.0.0/share/app/NOTICE")).unwrap().permissions().mode() & 0o777, 0o644);
        }
        assert_eq!(top_folder(&out, "app-1.0.0").unwrap(), out.join("app-1.0.0"));
        assert!(top_folder(&out, "app-2.0.0").is_err());
        std::fs::write(out.join("beside"), b"").unwrap();
        assert!(top_folder(&out, "app-1.0.0").is_err(), "a second thing at the top is not a release's layout");
        std::fs::remove_dir_all(&dir).unwrap();
    }

    #[test]
    fn a_tar_archive_cannot_write_outside_its_folder_or_make_a_link() {
        let dir = scratch("tar-bad");
        let file = tar::EntryType::Regular;
        let bad: [&[(&str, tar::EntryType, u32, &[u8], &str)]; 5] = [
            &[("../escaped", file, 0o644, b"x", "")],
            &[("app/../../escaped", file, 0o644, b"x", "")],
            &[("/escaped-from-root", file, 0o644, b"x", "")],
            &[("app/link", tar::EntryType::Symlink, 0o777, b"", "/etc/passwd")],
            &[("app/hard", tar::EntryType::Link, 0o644, b"", "app/other")],
        ];
        for (n, entries) in bad.iter().enumerate() {
            let archive = dir.join(format!("bad-{n}.tar.gz"));
            std::fs::write(&archive, gz(&tar_of(entries))).unwrap();
            let out = dir.join(format!("out-{n}"));
            assert!(tar_gz(&archive, &out).is_err(), "archive {n} was unpacked");
        }
        assert!(!dir.join("escaped").exists() && !dir.parent().unwrap().join("escaped").exists());
        // Not an archive at all.
        std::fs::write(dir.join("not.tar.gz"), b"plain text").unwrap();
        assert!(tar_gz(&dir.join("not.tar.gz"), &dir.join("out-not")).is_err());
        std::fs::remove_dir_all(&dir).unwrap();
    }

    #[test]
    fn a_zip_archive_is_unpacked_and_cannot_write_outside_its_folder() {
        use ::zip::write::SimpleFileOptions;
        let dir = scratch("zip");
        let make = |entries: &[(&str, &[u8])]| {
            let mut writer = ::zip::ZipWriter::new(std::io::Cursor::new(Vec::new()));
            for (name, contents) in entries {
                if name.ends_with('/') {
                    writer.add_directory(*name, SimpleFileOptions::default()).unwrap();
                } else {
                    writer.start_file(*name, SimpleFileOptions::default()).unwrap();
                    writer.write_all(contents).unwrap();
                }
            }
            writer.finish().unwrap().into_inner()
        };
        let archive = dir.join("a.zip");
        std::fs::write(&archive, make(&[("app-1.0.0/", b""), ("app-1.0.0/app.exe", b"MZ"), ("app-1.0.0/licenses/OFL.txt", b"ofl")])).unwrap();
        let out = dir.join("out");
        zip(&archive, &out).unwrap();
        assert_eq!(std::fs::read(out.join("app-1.0.0/app.exe")).unwrap(), b"MZ");
        assert_eq!(std::fs::read(out.join("app-1.0.0/licenses/OFL.txt")).unwrap(), b"ofl");
        assert_eq!(top_folder(&out, "app-1.0.0").unwrap(), out.join("app-1.0.0"));
        for (n, name) in ["../escaped", "app/../../escaped"].iter().enumerate() {
            let archive = dir.join(format!("bad-{n}.zip"));
            std::fs::write(&archive, make(&[(name, b"x")])).unwrap();
            assert!(zip(&archive, &dir.join(format!("out-{n}"))).is_err(), "{name} was unpacked");
        }
        assert!(!dir.join("escaped").exists() && !dir.parent().unwrap().join("escaped").exists());
        // A name that starts at the root is refused, or lands inside the folder: never at the root.
        let rooted = dir.join("rooted.zip");
        std::fs::write(&rooted, make(&[("/wordsmith-launcher-escaped-from-root", b"x")])).unwrap();
        let out = dir.join("out-rooted");
        if zip(&rooted, &out).is_ok() {
            assert!(out.join("wordsmith-launcher-escaped-from-root").is_file());
        }
        assert!(!Path::new("/wordsmith-launcher-escaped-from-root").exists());
        std::fs::write(dir.join("not.zip"), b"plain text").unwrap();
        assert!(zip(&dir.join("not.zip"), &dir.join("out-not")).is_err());
        std::fs::remove_dir_all(&dir).unwrap();
    }
}
