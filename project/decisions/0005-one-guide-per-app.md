# 0005: One user guide per app, kept in the app

Date: 2026-11-26. Status: accepted.

## Context

Each app had two user guides: `docs/guide/` in its own repository, and a section of the wiki in this one, written separately by hand. Neither was named the source. A change to an app asked for the guide page at most, so the wiki fell behind within a day: it said Wordsmith Book could not export while Book exported, and it said an app made no network request while the app checked for updates. The website sent readers to one guide and its menu to the other.

## Decision

The guide in the app's repository is the only one. The wiki shows it.

- An app's `docs/guide/` is the source of its user guide. It is written and changed there, with the change it describes.
- The wiki's section for an app, `website/wiki/content/docs/<app>/`, is built from that guide by a tool here, `website/wiki/scripts/guide.mjs`, at one commit of the app's repository. The commit is recorded in `website/wiki/guides.lock.json`, and each page says under its text which guide and which commit it came from. A page in an app's section is never edited here.
- The screenshots go the same way. The app draws them into `docs/images/`; the tool carries the ones a guide page shows, and the ones the website names, and writes them as WebP.
- What stays written by hand in the wiki is what belongs to no single app: the home page (`content/docs/index.mdx`) and the pages in `content/docs/start/` (the apps and how they fit together, installing, your files, moving between the apps, getting help, questions and answers, privacy). A page about one app's features does not go there.
- When the wiki should say something about an app that its guide does not say, the guide gets the page: open an issue in the app's repository. Nobody writes a second copy here.
- The website's "Read the guide" buttons lead to the wiki.

Two checks hold it. The checks workflow fails when a page here is not exactly what the recorded commit gives. A second workflow, on a schedule, fails while an app's guide on `main` has changed since the recorded commit, until someone runs the tool and lands the result.

The steps are Routes C, D and G in the [project map](../README.md#route-c).

## Consequences

- A change users will see needs one guide edit, in the app, beside the code. The wiki follows by a command, not by a rewrite.
- The wiki can say only what a guide says. A guide that is thin makes a thin section; the fix is in the guide.
- The wiki's page addresses follow the guide's file names. Renaming a guide page changes its address on the site.
- Guide pages are plain Markdown. The wiki's own components (callouts, tabs, status marks) are for the hand-written pages only.
- The apps' repositories are read at a commit over git, with no token, so the check works on a pull request from a fork.

## Revisit when

An app publishes releases often enough that the wiki should show the guide of the released version and not of `main` (the tool already takes a tag: `npm run guide -- --app <app> --ref v1.0.0`), or the guides need something Markdown cannot say.
