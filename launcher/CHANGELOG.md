# Changelog

What changed in each release of Wordsmith Launcher, newest first, for the people who use it.
`## Unreleased` holds what the next release will bring; when that release is cut, the section
takes its version and date, and the next `## Unreleased` opens above it.

The first public release is 0.9.0, a preview; 1.0.0 follows it, as for the Wordsmith apps.

## Unreleased

The first public release of Wordsmith Launcher: a preview of 1.0.0, for trying the launcher, its
downloads and its update check. The guide is `docs/guide/` in the launcher's folder of the
repository.

### What it does

- **One list of the Wordsmith apps**: Wordsmith Script, Wordsmith Manuscript and Wordsmith Book,
  each with the version that is installed on this computer and the newest version published.
- **Install** the newest release of an app for this system. The download comes from the app's
  own releases on GitHub and is compared with the release's `SHA256SUMS.txt` before it is
  opened; a file that does not match is not installed.
- **Update** an installed app when a newer release exists, with the same steps.
- **Open** an installed app.
- **Remove** an app the launcher installed. Your documents and the app's settings are kept.
- **It updates itself**, through the same update check the apps have.
- **The same work from a terminal**: `wordsmith-launcher list`, `install <app>`, `start <app>`
  and `remove <app>`.

### Where apps go

For your account only; nothing asks for an administrator's password.

- **Linux:** `~/.local`, by the app's own `install.sh`: the program in `~/.local/bin`, with its
  menu entry, icons and file types. An app you installed by hand from the same download is
  found there too.
- **Windows:** `%LOCALAPPDATA%\Programs`, one folder for each app, with its file types
  registered for your account.
- **macOS:** `~/Applications`.

### Getting it

- One download for each system, and a list of their checksums: a `.tar.gz` for Linux (64-bit
  Intel or AMD; needs the C library of Ubuntu 24.04 or newer), a `.dmg` for a Mac with Apple
  silicon (macOS 11 or later), a portable `.zip` for Windows (64-bit), and `SHA256SUMS.txt`.
- **The builds are not signed with a publisher's certificate yet.** macOS and Windows ask
  before they open the launcher the first time.

### Not in this release

- No list of recent documents, no "new document" page and no guides inside the launcher.
- No choice of where apps are installed, and no older version of an app.
- The interface is in English.
- An app is not updated while it is running: close it first.

### Privacy

The launcher asks GitHub for the releases of the three apps and of itself, and downloads what
you install. It sends nothing about you, has no account and no tracking, and the check when it
starts can be turned off (File, then About).
