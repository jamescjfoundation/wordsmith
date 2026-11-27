# Security

How to report a security problem in Wordsmith Launcher, and what counts as one.

<!-- BEGIN open-source-core: security -->
<!-- Owned by open-source-core (template/SECURITY.md). Change it there, never in a copy: its tooling rewrites the copies. -->
## Reporting a problem

Report security problems privately, not in a public issue, pull request or discussion. Use
GitHub's private reporting: the **Security** tab of this repository, then **Report a
vulnerability**. Only the maintainers see the report.

Include what you ran, what happened and what you expected. If you attach a file to show the
problem, remove anything personal from it first; a small made-up example is best.

We aim to reply within seven days, tell you when a fix is ready, and credit you in the advisory
and the changelog unless you ask us not to.

A problem in the parts every app shares (the window, saving and backups, format import and
export, agent tools, updates) is fixed in
[open-source-core](https://github.com/jamescjfoundation/open-source-core). Report it there or in
the repository where you found it; we move the report to where the fix belongs.

## How we handle a report

1. **Keep it private until the fix ships.** Not in a public issue, pull request, commit message,
   branch name, code comment or file in the repository. Discuss it in the private advisory;
   working notes go in `.private/` (ignored by Git).
2. **Fix it in the open, quietly.** The change says what the code now does, not how the old code
   could be abused, and adds a test that would have caught it.
3. **Release the fix.** A fix in the core is released there first, and every app then moves to
   that release and releases in turn. A repository that publishes without releases (a website,
   say) publishes the fix.
4. **Disclose:** publish the advisory and, where the repository keeps a changelog, add a
   **Security** entry to it.

If a problem is already public or being exploited, go straight to a fix and an advisory.
<!-- END open-source-core: security -->

## Where this folder differs

The launcher has no repository of its own: it is the `launcher/` folder of
[jamescjfoundation/wordsmith](https://github.com/jamescjfoundation/wordsmith). "This repository"
above is that one: report on its **Security** tab. A fix is released as a new version of the
launcher, from that repository, and the changelog here gets the **Security** entry.

## What counts

Anything that lets a file, a server or another program on the computer make the launcher do more
than its user asked for. The launcher's own cases:

- **What it fetches.** It asks `api.github.com` and `github.com` for the releases of the three
  Wordsmith apps and of itself, and downloads release files from them. A way to make it fetch
  from anywhere else, or to send anything about the user, is a problem.
- **What it installs.** A release file is installed only when its SHA-256 checksum is its line
  in the release's `SHA256SUMS.txt`. A way to have a file installed that does not match, or to
  have an archive write outside the folder it is unpacked into, is a problem.
- **What it runs.** It runs the installed apps, and on Linux and Windows the scripts inside a
  checked release package (`install.sh`, `uninstall.sh`, `register-file-types.cmd`). A way to
  have it run anything else is a problem.
- **Where it writes.** Only folders of the user's own. A way to have it write, replace or
  remove anything outside the app it was asked about is a problem.

The checksum file comes from the same release as the file it lists, so it shows that a download
is the file the release holds, not who built it. The release files are not signed with a
publisher's certificate yet; each has a build attestation on GitHub
(`docs/guide/checking-a-download.md`).

Only the latest release is supported.
