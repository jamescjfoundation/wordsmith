# 0006: The site reads each app's releases itself

Date: 2026-11-26. Status: accepted.

## Context

What the website and the wiki said about an app's state was typed into them: "no downloads yet", "pre-release", "in development", in about sixty lines of the page generator and seventeen wiki pages. Nothing in an app's release reached this repository, so the first release of any app would have needed dozens of edits here, by someone the release never told, and every later release a new version number and new links by hand.

## Decision

The pages show an app's version, date and download links from the app's own public releases on GitHub. Nobody types them.

- **One small data file per app**, `website/data/apps/<app>.json`: its name, its repository, what it is for, its platforms, and its own words for each state it can be in (no release, a preview before 1.0.0, released). The website's generator and the wiki read it. Wording about an app's state is changed there and nowhere else.
- **One releases file**: for each app, its latest public release (version, date, address, files) or nothing. `website/tools/releases.py` reads it from GitHub's public API. The newest full release is shown; a pre-release only while no full release exists; a draft never.
- **Every deploy reads GitHub.** The deploy builds the pages and the wiki from what GitHub answers at that moment, and publishes that answer with the site as `releases.json`. So a deploy for any other reason never puts older release data back.
- **A daily run** asks GitHub again and deploys only when the answer differs from the `releases.json` the live site was built from. It can also be started by hand. It commits nothing.
- **The file in the repository**, `website/data/releases.json`, is the last known answer. The pages in the repository are built from it, and `build.py --check` compares against it, so the check gives the same result everywhere and a release never turns it red. Anyone may refresh it with `python3 website/tools/releases.py --write` and commit the pages with it; nothing depends on that.
- **When GitHub cannot be read** for an app (no network, the request allowance used up), the build keeps the last known release for that app, from the file the live site was built from and then from the file in the repository, and says so. It never guesses.
- **No secret.** The data is public and the tool works without a token. In a workflow it sends the token GitHub gives every run, because requests without one share a small hourly allowance with every other runner at the same address.

Which file belongs to which system is decided by the file's name, with one pattern per platform in `website/data/platforms.json`. A release with no file for a system says so and links to the release.

## Consequences

- An app's release changes the site by itself, within a day, or at once when the deploy is started by hand. Route J no longer has a step in this repository for it.
- The pages in the repository can show an older release than the live site. That is by design: the live site is the fresh one.
- The download area depends on the names of the release files. The patterns accept the spellings the three apps use today; a new naming scheme needs a look at `platforms.json`.
- A scheduled workflow stops after sixty days without a commit to the repository, and nothing reports that it stopped.
- The wiki has the same rules written a second time, in JavaScript, with the same test cases as the Python ones.

## Revisit when

The launcher exists and needs the same data (it should read the same source), an app publishes for a system the three patterns do not cover, or the daily run is too slow for a release that must show at once.
