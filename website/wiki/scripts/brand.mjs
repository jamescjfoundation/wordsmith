// Copies the brand files the wiki and the website use from the repository's brand/ kit, unchanged:
// into website/wiki/public/brand/ (with the kit's folder names) and into website/assets/brand/
// and website/favicon.svg (flat, some renamed). Never edit the copies: change brand/ and run
// this again. It uses Node.js alone, so it runs before `npm install`.
//
//   npm run brand          copy the files
//   npm run brand:check    fail if a copy is missing or differs from brand/, or if a copy folder
//                          holds a file this script does not make (the checks workflow runs it)
import { copyFileSync, mkdirSync, readFileSync, readdirSync, existsSync } from 'node:fs';
import { dirname, join, relative } from 'node:path';
import { fileURLToPath } from 'node:url';

const wiki = join(dirname(fileURLToPath(import.meta.url)), '..');
const root = join(wiki, '..', '..');
const kit = join(root, 'brand');
const apps = ['wordsmith-script', 'wordsmith-manuscript', 'wordsmith-book'];

// Every copy, as [file in brand/, copy from the repository root].
const copies = [];

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

function filesUnder(folder) {
  const found = [];
  for (const entry of readdirSync(join(root, folder), { withFileTypes: true })) {
    const path = `${folder}/${entry.name}`;
    if (entry.isDirectory()) found.push(...filesUnder(path));
    else found.push(path);
  }
  return found;
}

const check = process.argv.includes('--check');
const stale = [];
for (const [from, to] of copies) {
  const source = join(kit, from);
  const copy = join(root, to);
  if (check) {
    if (!existsSync(copy) || !readFileSync(source).equals(readFileSync(copy))) stale.push(`${to}  (from brand/${from})`);
  } else {
    mkdirSync(dirname(copy), { recursive: true });
    copyFileSync(source, copy);
  }
}

const made = new Set(copies.map(([, to]) => to));
const strays = ['website/wiki/public/brand', site]
  .flatMap(filesUnder)
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
if (problems.length) {
  console.error(problems.join('\n\n'));
  process.exit(1);
}
console.log(check ? `${copies.length} brand copies match brand/.` : `Copied ${copies.length} brand files from brand/.`);
