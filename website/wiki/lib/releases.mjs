// Each app's state for the wiki's pages: the app's own words from website/data/apps/<app>.json
// and its latest public release from a releases file. The website's build.py reads the same
// files (website/tools/releases.py); the rules here are the same ones, and
// scripts/releases.test.mjs holds the cases they share.
//
// The releases file is website/data/releases.json, the last known answer, unless
// WORDSMITH_RELEASES names another one: the deploy sets it to what it has just read from GitHub.
import { readFileSync, readdirSync } from 'node:fs';
import { join } from 'node:path';

// the wiki is built from website/wiki; the data files are beside it, in website/data
const data = join(process.cwd(), '..', 'data');
const readJson = (file) => JSON.parse(readFileSync(file, 'utf8'));

/** Orders versions: 1.0.0 after 0.9.0 and after 1.0.0-rc.1 */
export function versionKey(version) {
  const found = /^v?(\d+)\.(\d+)\.(\d+)(?:-([0-9A-Za-z.-]+))?(?:\+.*)?$/.exec(version.trim());
  return found ? [Number(found[1]), Number(found[2]), Number(found[3])] : [-1, 0, 0];
}

/** "none" (nothing published), "preview" (before 1.0.0, or marked a pre-release) or "released" */
export function stateOf(release) {
  if (!release) return 'none';
  return release.prerelease || versionKey(release.version)[0] < 1 ? 'preview' : 'released';
}

const MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];

/** 2026-12-01 → 1 December 2026 */
export function longDate(day) {
  const [year, month, date] = day.split('-').map(Number);
  return `${date} ${MONTHS[month - 1]} ${year}`;
}

/** Bytes as a reader says them: 48 MB, 1.2 GB, 310 KB */
export function sizeWords(size) {
  const halfUp = (number) => Math.floor(number + 0.5); // website/tools/releases.py rounds the same way
  if (size >= 1024 ** 3) return `${(halfUp((size * 10) / 1024 ** 3) / 10).toFixed(1)} GB`;
  if (size >= 1024 ** 2) return `${halfUp(size / 1024 ** 2)} MB`;
  return `${Math.max(1, halfUp(size / 1024))} KB`;
}

/** The app's words for its state, with the release's version and date filled in */
export function stateWords(app, release) {
  const fill = release ? { version: release.version, date: longDate(release.date) } : {};
  return Object.fromEntries(
    Object.entries(app.state[stateOf(release)]).map(([key, text]) => [key, text.replace(/\{(\w+)\}/g, (_, name) => fill[name])]),
  );
}

// files that are about a download, not a download: checksum lists, signatures, update manifests
const BESIDE = /(sha256|sha512|checksums?|\.sig$|\.asc$|\.minisig$|\.sbom|\.json$|\.txt$|\.yml$|\.yaml$)/i;

/** The release's files for one platform, by the platform's file-name pattern */
export function filesFor(release, platform) {
  if (!release) return [];
  const pattern = new RegExp(platform.files, 'i');
  return release.files.filter((file) => pattern.test(file.name) && !BESIDE.test(file.name));
}

/** Everything a page shows about one app ("script", "manuscript", "book") */
export function appState(slug) {
  const app = readdirSync(join(data, 'apps'))
    .filter((name) => name.endsWith('.json'))
    .map((name) => readJson(join(data, 'apps', name)))
    .find((one) => one.slug === slug);
  if (!app) throw new Error(`No app "${slug}" in website/data/apps/.`);
  const platforms = readJson(join(data, 'platforms.json'));
  const releases = readJson(process.env.WORDSMITH_RELEASES || join(data, 'releases.json')).apps;
  const release = releases[slug] ?? null;
  return {
    app,
    release,
    state: stateOf(release),
    words: stateWords(app, release),
    releasesUrl: `https://github.com/${app.repository}/releases`,
    platforms: app.platforms.map((id) => {
      const platform = platforms.find((one) => one.id === id);
      return { ...platform, files: filesFor(release, platform) };
    }),
  };
}
