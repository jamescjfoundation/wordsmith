// Every copy of a brand kit file, made and checked by one tool. The kit is the repository's
// brand/ folder; a logo, an icon or a palette card is never edited in a copy. It uses Node.js
// alone, so it runs before `npm install`.
//
// The copies in this repository:
//   npm run brand            write the wiki's copies (website/wiki/public/brand/, the kit's folder
//                            names), the website's (website/assets/brand/ and website/favicon.svg,
//                            flat, some renamed) and brand/apps.json, the list of what each app carries
//   npm run brand:check      fail if one of those is missing or differs from brand/, or if a copy
//                            folder holds a file this script does not make (the checks workflow runs it)
//
// The copies in an app's repository (its assets/brand/ folder):
//   npm run brand -- --app script
//                            write the kit's files for that app into the checkout beside this
//                            repository (../wordsmith-script), with a record of the kit commit they
//                            came from, and say what changed. A path works in place of the name.
//   npm run brand:check -- --app script
//                            compare that checkout with the kit, and change nothing
//
// It never removes a file from an app, and never touches the files that are the app's own.
import { execFileSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { copyFileSync, existsSync, mkdirSync, readFileSync, readdirSync, writeFileSync } from 'node:fs';
import { dirname, isAbsolute, join, relative, resolve } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const wiki = join(dirname(fileURLToPath(import.meta.url)), '..');
const repositoryRoot = join(wiki, '..', '..');
const apps = ['wordsmith-script', 'wordsmith-manuscript', 'wordsmith-book'];
const sha256 = (data) => createHash('sha256').update(data).digest('hex');

// ---------------------------------------------------------------- the copies in this repository

// Every copy, as [file in brand/, copy from the repository root].
export const copies = [];

// The wiki: the kit's own folder layout.
for (const name of ['wordsmith-and-ink', ...apps]) {
  for (const file of [
    `${name}/logo/${name}-wordmark-ink.svg`,
    `${name}/logo/${name}-wordmark-paper.svg`,
    `${name}/app-icon/${name}-icon.svg`,
    `${name}/app-icon/${name}-icon-small.svg`,
    `${name}/app-icon/favicon.svg`,
  ]) {
    copies.push([file, `website/wiki/public/brand/${file}`]);
  }
}

// The website: one flat folder, so the parent brand's 512 px icon takes a longer name.
const site = 'website/assets/brand';
const parent = 'wordsmith-and-ink';
for (const tone of ['ink', 'paper']) {
  copies.push(
    [`${parent}/logo/${parent}-wordmark-${tone}.svg`, `${site}/${parent}-wordmark-${tone}.svg`],
    [`${parent}/logo/${parent}-foundation-${tone}.svg`, `${site}/${parent}-foundation-${tone}.svg`],
    [`${parent}/lockups/${parent}-family-${tone}.svg`, `${site}/${parent}-family-${tone}.svg`],
  );
  for (const app of apps) {
    copies.push([`${app}/logo/${app}-wordmark-${tone}.svg`, `${site}/${app}-wordmark-${tone}.svg`]);
  }
}
for (const name of [parent, ...apps]) {
  copies.push([`${name}/app-icon/${name}-icon.svg`, `${site}/${name}-icon.svg`]);
}
copies.push(
  [`${parent}/app-icon/icon-512.png`, `${site}/${parent}-icon-512.png`],
  [`${parent}/app-icon/favicon.svg`, 'website/favicon.svg'],
);

// Files in the copy folders that are not kit files. No script makes them.
const notFromKit = new Set([`${site}/og-image.png`]); // the picture in link previews

function filesUnder(root, folder) {
  const start = join(root, folder);
  if (!existsSync(start)) return [];
  const found = [];
  for (const entry of readdirSync(start, { withFileTypes: true })) {
    const path = `${folder}/${entry.name}`;
    if (entry.isDirectory()) found.push(...filesUnder(root, path));
    else found.push(path);
  }
  return found;
}

// ---------------------------------------------------------------- the copies in the apps

/*
 * What each app's repository keeps in assets/brand/. Three kinds of file:
 *
 * - carried: a kit file, unchanged. Every file of the app's production/ set here (but its README)
 *   is carried under its own name; `icons` adds files from the app's app-icon/ folder, as
 *   { name in the app: name in app-icon/ }.
 * - own: the app writes it. The kit never touches it.
 * - derived: the app makes it from a carried file with its own tool, and makes it again when
 *   that file changes.
 *
 * `theme` is the app's interface theme file, in the token format of open-source-core. It is the
 * app's own; only its seven palette colors must be the kit's.
 */
export const APPS = {
  script: {
    repository: 'jamescjfoundation/wordsmith-script',
    theme: 'script/tokens.json',
    appColor: ['brand-brass', 'brass-text'],
    icons: { 'icon-256.png': 'icon-256.png', 'icon-512.png': 'icon-512.png' },
    own: {
      'README.md': "What the app's brand files are for, and the rules for using them",
      'script/tokens.json': "The app's interface theme, in the token format of open-source-core",
    },
    derived: {
      'mark-mask.png': { from: ['wordsmith-mark-ink.svg'], by: null },
      'wordmark-mask.png': { from: ['wordsmith-script-wordmark-ink.svg'], by: null },
    },
  },
  manuscript: {
    repository: 'jamescjfoundation/wordsmith-manuscript',
    theme: 'tokens.json',
    appColor: ['brand-red', 'red-text'],
    icons: { 'icon-32.png': 'icon-32.png', 'icon-256.png': 'icon-256.png', 'icon-512.png': 'icon-512.png', 'icon.ico': 'wordsmith-manuscript.ico' },
    own: {
      'README.md': "What the app's brand files are for, and the rules for using them",
      'tokens.json': "The app's interface theme, in the token format of open-source-core",
    },
    derived: {},
  },
  book: {
    repository: 'jamescjfoundation/wordsmith-book',
    theme: 'tokens.json',
    appColor: ['brand-green', 'green-text'],
    icons: {
      'icon-32.png': 'icon-32.png',
      'icon-256.png': 'icon-256.png',
      'icon-512.png': 'icon-512.png',
      'icon-macos-1024.png': 'icon-macos-1024.png',
      'icon.ico': 'wordsmith-book.ico',
    },
    own: {
      'README.md': "What the app's brand files are for, and the rules for using them",
      'tokens.json': "The app's interface theme, in the token format of open-source-core",
    },
    derived: {
      'mark-mask.png': { from: ['wordsmith-book-mark-ink.svg'], by: 'tools/brand-mask.py' },
    },
  },
};

export const APP_FOLDER = 'assets/brand';
// The record the tool leaves in an app's folder: the kit commit its copies came from, and the list.
export const RECORD = 'kit.json';
export const LIST = 'brand/apps.json';

/** The seven palette colors of an app, from the kit's tokens.json. */
export function palette(root, slug) {
  const tokens = JSON.parse(readFileSync(join(root, 'brand', `wordsmith-${slug}`, 'tokens.json'), 'utf8')).color.tokens;
  const value = (name, theme) => {
    const token = tokens.find((one) => one.name === name);
    if (!token) throw new Error(`brand/wordsmith-${slug}/tokens.json has no color "${name}"`);
    return token.value[theme].toUpperCase();
  };
  const [color, text] = APPS[slug].appColor;
  return {
    ink: value('brand-ink', 'light'),
    paper: value('brand-paper', 'light'),
    'app-color': value(color, 'light'),
    'app-color-text': value(text, 'light'),
    'margin-blue': value('accent', 'light'),
    slate: value('ink-muted', 'light'),
    night: value('surface-page', 'dark'),
  };
}

/** One app's entry of brand/apps.json: every file its assets/brand/ holds, by kind. */
export function appEntry(root, slug) {
  const app = APPS[slug];
  const kit = `brand/wordsmith-${slug}`;
  const carried = [];
  for (const name of readdirSync(join(root, kit, 'production')).sort()) {
    if (name !== 'README.md') carried.push({ file: name, from: `${kit}/production/${name}` });
  }
  for (const [file, source] of Object.entries(app.icons)) carried.push({ file, from: `${kit}/app-icon/${source}` });
  carried.sort((a, b) => (a.file < b.file ? -1 : 1));
  for (const one of carried) one.sha256 = sha256(readFileSync(join(root, one.from)));
  return {
    repository: app.repository,
    folder: APP_FOLDER,
    record: RECORD,
    carried,
    own: Object.entries(app.own).map(([file, what]) => ({ file, what })),
    derived: Object.entries(app.derived).map(([file, how]) => ({ file, ...how })),
    theme: app.theme,
    palette: palette(root, slug),
  };
}

/** The text of brand/apps.json. */
export function listText(root) {
  const note =
    'What each app keeps in its assets/brand/ folder. "carried" files are kit files, unchanged, with their SHA-256. ' +
    '"own" files are the app\'s. "derived" files are made by the app from the carried files named in "from", with the tool in "by" ' +
    '(null: no tool yet). "palette" is the seven colors the app\'s theme file ("theme") must hold. ' +
    'Written by `npm run brand` in website/wiki (scripts/brand.mjs); never edit it.';
  const entries = Object.fromEntries(Object.keys(APPS).map((slug) => [slug, appEntry(root, slug)]));
  return `${JSON.stringify({ note, apps: entries }, null, 2)}\n`;
}

/** The colors a theme file names in its "palette", upper case, sorted. */
function themeColors(text) {
  const colors = Object.values(JSON.parse(text).palette ?? {});
  return colors.map((color) => String(color).toUpperCase()).sort();
}

/**
 * Compares an app checkout's assets/brand/ with the kit. Returns { problems, notes }: what is
 * wrong, and what is worth knowing.
 */
export function checkApp(root, slug, checkout) {
  const entry = appEntry(root, slug);
  const folder = join(checkout, APP_FOLDER);
  const problems = [];
  const notes = [];
  if (!existsSync(folder)) return { problems: [`${checkout} has no ${APP_FOLDER}/ folder`], notes };
  for (const one of entry.carried) {
    const path = join(folder, one.file);
    if (!existsSync(path)) problems.push(`${one.file}: missing (the kit's ${one.from})`);
    else if (sha256(readFileSync(path)) !== one.sha256) problems.push(`${one.file}: differs from the kit's ${one.from}`);
  }
  for (const one of entry.own) {
    if (!existsSync(join(folder, one.file))) problems.push(`${one.file}: missing (the app's own: ${one.what})`);
  }
  for (const one of entry.derived) {
    if (!existsSync(join(folder, one.file))) problems.push(`${one.file}: missing (the app makes it from ${one.from.join(', ')}${one.by ? ` with ${one.by}` : ''})`);
  }
  const theme = join(folder, entry.theme);
  if (existsSync(theme)) {
    const wanted = Object.values(entry.palette).sort();
    let found;
    try {
      found = themeColors(readFileSync(theme, 'utf8'));
    } catch {
      found = null;
    }
    if (!found) problems.push(`${entry.theme}: cannot be read as a theme file`);
    else if (found.join(' ') !== wanted.join(' ')) problems.push(`${entry.theme}: its palette is ${found.join(' ')}; the kit's seven colors are ${wanted.join(' ')}`);
  }
  const known = new Set([...entry.carried, ...entry.own, ...entry.derived].map((one) => one.file).concat(RECORD));
  for (const file of filesUnder(checkout, APP_FOLDER).map((path) => path.slice(APP_FOLDER.length + 1))) {
    if (!known.has(file)) problems.push(`${file}: in ${APP_FOLDER}/, and not in the kit's list for this app (${LIST})`);
  }
  const record = join(folder, RECORD);
  if (!existsSync(record)) {
    notes.push(`${RECORD}: not there yet. \`npm run brand -- --app ${slug}\` writes it, with the kit commit the copies came from.`);
  } else {
    const kept = JSON.parse(readFileSync(record, 'utf8'));
    const { kit, ...list } = kept;
    if (JSON.stringify(list.app) !== JSON.stringify(entry)) problems.push(`${RECORD}: records another list than the kit has now (it was written at kit commit ${String(kit?.commit).slice(0, 7)})`);
    else notes.push(`${RECORD}: the copies were taken at kit commit ${String(kit?.commit).slice(0, 7)}, and the kit's list is the same now.`);
  }
  return { problems, notes };
}

/** Writes the kit's files for an app into a checkout. Returns { changed, same, notes }. */
export function writeApp(root, slug, checkout, commit) {
  const entry = appEntry(root, slug);
  const folder = join(checkout, APP_FOLDER);
  if (!existsSync(folder)) throw new Error(`${checkout} has no ${APP_FOLDER}/ folder. Is it the app's repository?`);
  const changed = [];
  let same = 0;
  const put = (file, data, what) => {
    const path = join(folder, file);
    if (existsSync(path) && readFileSync(path).equals(data)) {
      same += 1;
      return;
    }
    changed.push(`${existsSync(path) ? 'updated' : 'added'}: ${file}${what ? ` (${what})` : ''}`);
    mkdirSync(dirname(path), { recursive: true });
    writeFileSync(path, data);
  };
  const touched = new Set();
  for (const one of entry.carried) {
    const before = changed.length;
    put(one.file, readFileSync(join(root, one.from)), `from ${one.from}`);
    if (changed.length > before) touched.add(one.file);
  }
  const record = { note: `The kit files in this folder, and the commit of jamescjfoundation/wordsmith they were taken at. Written by the kit's tool (\`npm run brand -- --app ${slug}\` in website/wiki there); never edit it.`, kit: { repository: 'jamescjfoundation/wordsmith', commit }, app: entry };
  // A record that differs only in its commit is left alone: nothing the app holds changed.
  const recordPath = join(folder, RECORD);
  const kept = existsSync(recordPath) ? JSON.parse(readFileSync(recordPath, 'utf8')) : null;
  if (!kept || changed.length > 0 || JSON.stringify(kept.app) !== JSON.stringify(entry)) {
    put(RECORD, Buffer.from(`${JSON.stringify(record, null, 2)}\n`), 'the record of what was taken');
  }
  const notes = [];
  for (const one of entry.derived) {
    if (one.from.some((source) => touched.has(source))) {
      notes.push(`${one.file} is made from ${one.from.join(', ')}, which changed: make it again${one.by ? ` (${one.by})` : ' (the app has no tool for it yet)'}.`);
    }
  }
  return { changed, same, notes };
}

// ---------------------------------------------------------------- the command line

function checkHere(root) {
  const stale = [];
  for (const [from, to] of copies) {
    const copy = join(root, to);
    if (!existsSync(copy) || !readFileSync(join(root, 'brand', from)).equals(readFileSync(copy))) stale.push(`${to}  (from brand/${from})`);
  }
  const made = new Set(copies.map(([, to]) => to));
  const strays = ['website/wiki/public/brand', site]
    .flatMap((folder) => filesUnder(root, folder))
    .filter((file) => !made.has(file) && !notFromKit.has(file));
  const problems = [];
  if (stale.length) {
    problems.push(`These copies are missing or differ from brand/:\n  ${stale.join('\n  ')}\nRun "npm run brand" in ${relative(root, wiki)}.`);
  }
  if (strays.length) {
    problems.push(
      `These files are in a folder of brand copies, and this script does not make them:\n  ${strays.join('\n  ')}\n` +
        'Add each to scripts/brand.mjs (a kit file under "copies", anything else under "notFromKit"), or remove it.',
    );
  }
  const list = join(root, LIST);
  if (!existsSync(list) || readFileSync(list, 'utf8') !== listText(root)) {
    problems.push(`${LIST} is not what the kit gives now: the list of what each app carries, with each file's checksum.\nRun "npm run brand" in ${relative(root, wiki)}.`);
  }
  return problems;
}

function main(argv) {
  const root = repositoryRoot;
  const check = argv.includes('--check');
  const named = argv.includes('--app') ? argv[argv.indexOf('--app') + 1] : undefined;

  if (named !== undefined) {
    // an app by name is the checkout beside this repository; anything else is a path
    const slug = Object.keys(APPS).find((one) => one === named || `wordsmith-${one}` === named) ?? Object.keys(APPS).find((one) => resolve(named).endsWith(`wordsmith-${one}`));
    if (!slug) throw new Error(`"${named}" is not script, manuscript or book, and not a path that ends in an app's repository name. Name the app: --app book.`);
    const checkout = named === slug || named === `wordsmith-${slug}` ? join(root, '..', `wordsmith-${slug}`) : isAbsolute(named) ? named : resolve(named);
    if (check) {
      const { problems, notes } = checkApp(root, slug, checkout);
      for (const note of notes) console.log(note);
      if (problems.length) {
        console.error(`${checkout}/${APP_FOLDER} is not what the kit gives for ${slug}:\n  ${problems.join('\n  ')}\nTo take the kit's files: npm run brand -- --app ${slug}`);
        process.exit(1);
      }
      console.log(`${checkout}/${APP_FOLDER} holds the kit's files for ${slug}, unchanged.`);
      return;
    }
    const dirty = execFileSync('git', ['-C', root, 'status', '--porcelain', '--', 'brand'], { encoding: 'utf8' }).trim();
    if (dirty) throw new Error(`brand/ has changes that are not committed:\n${dirty}\nCommit and push the kit first: the app records the kit commit its copies came from.`);
    const commit = execFileSync('git', ['-C', root, 'rev-parse', 'HEAD'], { encoding: 'utf8' }).trim();
    const { changed, same, notes } = writeApp(root, slug, checkout, commit);
    for (const line of changed) console.log(line);
    for (const note of notes) console.log(note);
    console.log(`${changed.length} file(s) written and ${same} already the kit's, in ${checkout}/${APP_FOLDER}. Nothing is committed: the change is the app's.`);
    const { problems } = checkApp(root, slug, checkout);
    if (problems.length) console.log(`Still to do in the app:\n  ${problems.join('\n  ')}`);
    return;
  }

  if (check) {
    const problems = checkHere(root);
    if (problems.length) {
      console.error(problems.join('\n\n'));
      process.exit(1);
    }
    console.log(`${copies.length} brand copies match brand/, and ${LIST} lists what each app carries.`);
    return;
  }
  for (const [from, to] of copies) {
    mkdirSync(dirname(join(root, to)), { recursive: true });
    copyFileSync(join(root, 'brand', from), join(root, to));
  }
  writeFileSync(join(root, LIST), listText(root));
  console.log(`Copied ${copies.length} brand files from brand/, and wrote ${LIST}.`);
  const strays = checkHere(root);
  if (strays.length) {
    console.error(strays.join('\n\n'));
    process.exit(1);
  }
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  try {
    main(process.argv.slice(2));
  } catch (error) {
    console.error(error.message);
    process.exit(1);
  }
}
