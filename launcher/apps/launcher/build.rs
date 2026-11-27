// SPDX-License-Identifier: MIT OR Apache-2.0
//! On Windows, embed the launcher's icon (`assets/brand/icon.ico`) and the program's name in
//! the executable, so Explorer and the taskbar show the brand. Does nothing for any other
//! target.
//!
//! This file holds no data of the launcher's: the names come from
//! `[package.metadata.winresource]` in this package's `Cargo.toml`.

#![forbid(unsafe_code)]
#![deny(clippy::unwrap_used, clippy::expect_used, clippy::panic, clippy::unimplemented, clippy::todo, clippy::unreachable)]

const ICON: &str = "../../assets/brand/icon.ico";

fn main() -> std::io::Result<()> {
    println!("cargo:rerun-if-changed=build.rs");
    println!("cargo:rerun-if-changed=Cargo.toml");
    println!("cargo:rerun-if-changed={ICON}");
    // The target, not the machine running the build script.
    if std::env::var("CARGO_CFG_TARGET_OS").as_deref() != Ok("windows") {
        return Ok(());
    }
    let mut resource = winresource::WindowsResource::new();
    resource.set_icon(ICON);
    resource.compile()
}
