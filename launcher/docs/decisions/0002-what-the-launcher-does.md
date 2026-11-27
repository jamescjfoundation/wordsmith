# 0002: What the launcher does, where it installs, and what it leaves out

Date: 2026-11-27 · Status: accepted

## Context

The three Wordsmith apps each publish releases by one contract (core decision 0019): a tag
`vX.Y.Z`, one file for each of three systems named by a fixed pattern, and `SHA256SUMS.txt`.
The contract's last section says what a launcher may rely on. Each app has had its first
release, 0.9.0.

A writer who wants the apps today finds each one's release page, picks the file for the
computer, unpacks it and runs an install step, three times, and again for every update that the
app's own update check cannot install in place.

The reference for what a launcher does is ArtCraft Launcher
(<https://github.com/storytold/craft-launcher>), which serves a suite of nineteen apps. It was
read for behavior and shape. Its licenses (MIT OR Apache-2.0) would allow copying with credit;
nothing was copied, and the interface's names and text here are our own (project decision 0003).

## Decision

### Identity

| | |
| --- | --- |
| Product name | Wordsmith Launcher |
| Program, release id, settings folder | `wordsmith-launcher` |
| App id | `org.jcjfoundation.launcher` |
| Releases | `jamescjfoundation/wordsmith` (decision 0001) |
| Icon | The icon of the parent brand, Wordsmith & Ink, until the kit has one of the launcher's own |

The program is `wordsmith-launcher`, not `wordsmith`. The release id is the stem of every
release file, the name in a process list and the name of the settings folder, and the three
apps are `wordsmith-script`, `wordsmith-manuscript` and `wordsmith-book`: a fourth name of the
same shape says what the program is, and a file named `wordsmith-0.9.0-linux-x86_64.tar.gz`
would not say which Wordsmith it holds. The bare name `wordsmith` stays free.

### What it does

1. **Lists the three apps**, from a catalog compiled in: each app's release id, name and
   repository.
2. **Reads each app's newest release** from GitHub's public API, with no token: the newest by
   version among the releases that are neither a draft nor a pre-release. When the API does not
   answer (its allowance without a token is sixty requests an hour), it follows
   `https://github.com/<owner>/<app>/releases/latest`, whose address names the version, and
   finds the files by their names. Both ways are the contract's.
3. **Installs** the file for this system: reads the release's `SHA256SUMS.txt`, downloads the
   file, compares its SHA-256 checksum with its line, and only then unpacks it. A file with no
   line, with two different ones, or with a line that differs from the checksum GitHub's API
   gives for the same file, is not installed.
4. **Starts** an installed app.
5. **Updates** an app when the newest release is newer than the installed version, by the same
   steps as an installation.
6. **Removes** an app it installed. Settings and documents are left alone.
7. **Updates itself** through the core's update check (`jcj_shell::desktop`), like every app.

The same work is offered without a window, as commands of the one program
(`wordsmith-launcher list`, `install`, `start`, `remove`), so it can be scripted and checked on
a computer with no screen. The apps ship a separate command-line program each; the launcher is
small enough for one.

### Where an app goes

Folders of the user's own. No step asks for an administrator.

| System | Where | How |
| --- | --- | --- |
| Linux | `~/.local` | The package's own `install.sh`, with `PREFIX` set: `bin/<id>`, the menu entry, the icons, the file types, the license texts. The package's `uninstall.sh` is kept, and removing runs it |
| Windows | `%LOCALAPPDATA%\Programs\<name>\` | The package's one folder, moved there; then its `register-file-types.cmd`. Removing runs `unregister-file-types.cmd` and deletes the folder |
| macOS | `~/Applications/<name>.app` | The app copied off the disk image with the system's `ditto`. Removing deletes it |

On Linux this is the place and the way a person installs the same file by hand, so the launcher
finds a copy installed by hand, an app installed by the launcher has its menu entry and file
types, and the app's own update check replaces it in place as the contract describes.

The launcher keeps a record of each copy it installed in its settings folder, and removes only
those. The installed version is asked of the program itself (`<program> --version`), because an
app updates itself in place and a record would then be behind.

`WORDSMITH_LAUNCHER_PROFILE` names one folder for everything a run keeps and installs: its
preferences, its records and the apps. It is for a test and for trying the launcher without
touching one's own apps.

### What it sends

Requests to `api.github.com` and `github.com`, for the four repositories only, with the
launcher's name and version and nothing else. One switch, the shell's "Check for updates when
the app starts", covers every request the launcher makes unasked: its own update check and the
apps' releases. With it off, the launcher asks when "Check Now" is pressed.

### What the reference does that the launcher leaves out

| Left out | Why |
| --- | --- |
| A tray or menu-bar icon, starting at login, notifications | A window opened when wanted is enough for three apps |
| A choice of install folder, installs for the whole computer, system packages (`.deb`, `.rpm`, `.msi`, Flatpak, AppImage) | The apps publish three kinds of file; each has one per-user place |
| Older versions, rolling back, pinning a version, nightly builds | The contract has full releases only, and the newest is the one supported |
| A queue of downloads, pausing and resuming, a proxy setting | Three files of about 55 MB; a failed download is started again |
| A grid and a table view, sorting, search, details pages with pictures | Three rows |
| A fonts page | Not a launcher's job here |
| A web version | The website already links the downloads |
| Interface translations | English for now; the shell's translations are there to be used |
| Signature checks on downloads | The apps' builds are unsigned (core decision 0019). The checksum, and the attestation a person can verify, are what there is |
| Only one launcher running at a time | A second window is allowed. One window refuses a second task on an app that is busy; two windows are not held apart |
| A hosted catalog of apps | The catalog is three lines in the program; a new app is a new launcher release |

Planned in the launcher's first description and not in this release: a list of recent documents
from every app, a "new document" page, and guides inside the launcher. The apps would have to
tell the launcher about their documents first; that is a request to each app, not written yet.

## Consequences

- The launcher runs a script from a release package on Linux and Windows. The package was
  checked against the release's checksum first, and the same package holds the program the user
  is about to run.
- On Linux an app's files join the user's `~/.local`. An older version's file that the newer
  package no longer has stays there until the app is removed and installed again.
- An app is not replaced while it runs. Linux and Windows say that a program is running; macOS
  does not, so there the launcher cannot refuse.
- The quick-access row of the shell names a document and says whether it is saved, so the
  launcher switches it off, and with it the box that searches commands (the command palette
  still opens with its keys). A shell option for an app without a document is asked of the core
  ([open-source-core#51](https://github.com/jamescjfoundation/open-source-core/issues/51)).
- The code that reads a release by the contract is the launcher's own. The same reading exists
  in the core's update check, for an app's own releases, behind an interface that does not
  offer it for another app's. If a second program needs to read another app's releases, it
  belongs in the core.
- The window icon is the parent brand's until the kit draws the launcher's
  ([wordsmith#25](https://github.com/jamescjfoundation/wordsmith/issues/25)).

## Revisit when

The apps tell a launcher about their documents; a fourth app is added; the apps' builds are
signed; a system gains a second kind of release file; or 1.0.0 is planned.
