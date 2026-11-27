// SPDX-License-Identifier: MIT OR Apache-2.0
//! What Wordsmith Launcher does, without its window.
//!
//! The launcher lists the Wordsmith apps, reads each one's newest public release from its own
//! GitHub repository, installs the release file for this system after checking it, starts an
//! installed app, and removes one. This crate is all of that; the window (`apps/launcher`) only
//! shows it and asks for it.
//!
//! - [`catalog`]: the apps, and the systems a release has a file for.
//! - [`release`]: a release as the core's contract writes it (`docs/app-releases.md` in
//!   open-source-core): versions, file names, `SHA256SUMS.txt`, and which checksum a file must
//!   have before it is opened.
//! - [`net`]: the requests. Only `api.github.com` and `github.com` are asked, only for the
//!   repositories in the catalog, and nothing about the user is sent.
//! - [`unpack`]: a `.tar.gz` or a `.zip` unpacked into a folder, with bounds, and never outside it.
//! - [`install`]: where things go on each system, and the steps of installing, starting and
//!   removing.
//!
//! Nothing here needs more rights than the user has: every folder is the user's own.

#![forbid(unsafe_code)]
#![deny(clippy::unwrap_used, clippy::expect_used, clippy::panic, clippy::unimplemented, clippy::todo, clippy::unreachable)]

pub mod catalog;
pub mod install;
pub mod net;
pub mod release;
pub mod unpack;

pub use catalog::{APPS, AppInfo, System};
pub use install::{Installed, Places, Step};
pub use net::Client;
pub use release::{Release, Version};
