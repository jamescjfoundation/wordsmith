# Security

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

## What counts here

This repository holds no app. It holds what the project publishes about itself: the website, the wiki, the brand kit, and the project map with its tools. A security problem here is anything that lets someone change what the project publishes, or that breaks a promise the site makes to its visitors. For example:

- **The website and the wiki.** A page of [wordsmithand.ink](https://wordsmithand.ink/) that loads something from another site (a script, a font, a tracker), or a way to make a page run someone else's script. A link on the site or the wiki that offers an app from anywhere but the project's own repositories and their GitHub releases.
- **The deploy.** A way to change what is published without a commit on `main`: a workflow that runs text it was given as a command, an action that is not pinned to a commit, a token with more rights than its job needs.
- **The brand files.** A logo, icon or PDF in `brand/` that holds more than the picture: a script, a link that is fetched when the file is opened, or details of the machine that made it.
- **The tools.** A script here (`project/`, `website/tools/`, `brand/source/`, `website/wiki/scripts/`) that writes outside the folder it was given, or that fetches something and uses it unchecked.
- **Anything private.** A secret or a person's details in a tracked file or in the history.

A wrong sentence on the site or the wiki is not a security problem, unless it tells a writer something false about what an app sends or stores. Open an [issue](https://github.com/jamescjfoundation/wordsmith/issues) for the first kind and report the second kind privately.

A problem in an app is reported in that app's repository: [wordsmith-script](https://github.com/jamescjfoundation/wordsmith-script/security), [wordsmith-manuscript](https://github.com/jamescjfoundation/wordsmith-manuscript/security), [wordsmith-book](https://github.com/jamescjfoundation/wordsmith-book/security).

## Where this repository differs from the text above

The text between the two marker lines is carried word for word from open-source-core and is written for a repository that releases an app.

- Nothing is released from here and there is no `CHANGELOG.md`. A fix ships when it is on `main` and the deploy that follows is green. The public record of a fixed problem is the advisory.
- What is supported is the site as it is published today, and `main`.
- Someone working in a checkout, an agent included, does not file a report: keep the problem in `.private/`, which Git ignores, and tell the maintainer you are working for ([Route H](project/README.md#route-h) of the project map).
