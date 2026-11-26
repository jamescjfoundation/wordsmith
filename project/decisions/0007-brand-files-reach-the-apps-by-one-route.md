# 0007: Brand files reach the apps by one route

Date: 2026-11-26. Status: accepted.

## Context

The brand kit here is the source of every logo and icon, and each app keeps copies in its `assets/brand/`. The copies were made by hand, three different ways, and nothing compared them with the kit. Two apps had drifted: one held icons scaled by a tool of its own and SVG files with their metadata stripped, another a palette card from an older kit. The kit's `tokens.json` and an app's `tokens.json` shared a name and not a format, so it was not clear which decided an interface color. The brand guide described an app copy route nobody used.

## Decision

- **The kit owns the seven palette colors and every logo and icon.** An app never edits, recolors, rescales or redraws one, and never makes an icon size of its own: the kit has every size.
- **An app owns its interface theme file** (`assets/brand/tokens.json`; in Script, `assets/brand/script/tokens.json`). It is in the token format of open-source-core, it is not a copy of the kit's `tokens.json`, and the app decides every interface color in it. Only the seven palette colors it names must be the kit's.
- **Three kinds of file in an app's `assets/brand/`**, and nothing else:
  - *carried*: a kit file, byte for byte: the app's `production/` set and the icons it uses from `app-icon/`;
  - *own*: the theme file and the folder's README;
  - *derived*: a file the app makes from a carried file with a tool of its own (the mask the window paints the mark from), and makes again when that file changes.
- **One list.** `brand/apps.json` says, for each app, every carried file with the kit file it comes from and its SHA-256, the files that are the app's own, the derived files with their source and tool, and the seven colors. A tool writes it from the kit and the check fails when it is stale, so it cannot disagree with the kit.
- **One tool, on the kit's side.** `npm run brand -- --app <app>` in `website/wiki` writes the kit's files for that app into the app's checkout, leaves the app's own files alone, removes nothing, and says what changed and which derived files to make again. It also writes `assets/brand/kit.json`: the kit commit the copies were taken at, and the app's part of the list. `npm run brand:check -- --app <app>` compares and changes nothing. The change it makes is committed in the app, by whoever works there.
- **The check that fails in the app is the app's.** With `kit.json` an app can check its copies in its own gate without the network, and compare `kit.json` with `brand/apps.json` on this repository's `main` to learn that the kit has moved. A kit change then shows as a failing check in each app until the app takes its copies.

The steps are Route F in the [project map](../README.md#route-f).

## Consequences

- A kit change is finished in wordsmith first, with `npm run brand`, which also rewrites the list. The apps follow by one command each.
- Manuscript stops scaling its own icons, and its tool for them goes. Script needs a tool for its two mask files, which today no tool makes.
- An app that wants another kit file asks for it here: the file is added to the app's entry in `website/wiki/scripts/brand.mjs`, and the list follows.
- The kit's `tokens.json` stays a design reference for the brand. No app reads it.
- Until each app has its own check, a drifted copy is found only when someone runs the kit's check on that app's checkout.

## Revisit when

The apps' checks exist in all three (the "Today" lines of Route F then go), or a fourth product needs brand files.
