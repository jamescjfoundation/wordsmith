// Tests for the brand tool's app side (scripts/brand.mjs): what each app carries from the kit,
// writing it into a checkout and comparing. The kit is this repository's own brand/ folder,
// read only; the app checkout is a temporary folder.
import assert from 'node:assert/strict';
import { existsSync, mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import { test } from 'node:test';
import { fileURLToPath } from 'node:url';
import { APPS, APP_FOLDER, LIST, RECORD, appEntry, checkApp, copies, listText, palette, writeApp } from './brand.mjs';

const root = join(dirname(fileURLToPath(import.meta.url)), '..', '..', '..');
const COMMIT = '0123456789abcdef0123456789abcdef01234567';

/** A made-up checkout of an app with the files that are the app's own. */
function checkout(slug, colors = Object.values(palette(root, slug))) {
  const folder = mkdtempSync(join(tmpdir(), `brand-${slug}-`));
  const entry = appEntry(root, slug);
  const put = (file, text) => {
    mkdirSync(dirname(join(folder, APP_FOLDER, file)), { recursive: true });
    writeFileSync(join(folder, APP_FOLDER, file), text);
  };
  for (const own of entry.own) put(own.file, own.file === entry.theme ? JSON.stringify({ name: slug, palette: Object.fromEntries(colors.map((color, at) => [`c${at}`, color])) }) : 'the app wrote this');
  for (const derived of entry.derived) put(derived.file, 'made by the app');
  return folder;
}

test('the list in the kit is what the tool writes', () => {
  assert.equal(readFileSync(join(root, LIST), 'utf8'), listText(root));
});

test('every app carries its production set and its icons, and no file twice', () => {
  for (const slug of Object.keys(APPS)) {
    const entry = appEntry(root, slug);
    const files = [...entry.carried, ...entry.own, ...entry.derived].map((one) => one.file);
    assert.equal(new Set(files).size, files.length, `${slug} names a file twice`);
    assert.ok(entry.carried.some((one) => one.file === 'favicon.svg'), slug);
    assert.ok(entry.carried.some((one) => one.file === `wordsmith-${slug}-wordmark-ink.svg`), slug);
    assert.ok(!entry.carried.some((one) => one.file === 'README.md'), `${slug}: the README is the app's own`);
    assert.ok(entry.own.some((one) => one.file === entry.theme), `${slug}: the theme file is the app's own`);
    for (const one of entry.carried) {
      assert.ok(existsSync(join(root, one.from)), one.from);
      assert.match(one.sha256, /^[0-9a-f]{64}$/);
    }
    for (const derived of entry.derived) for (const source of derived.from) assert.ok(entry.carried.some((one) => one.file === source), `${slug}: ${derived.file} is made from ${source}, which is not carried`);
  }
});

test('the seven palette colors: five shared, two the app\'s own', () => {
  const all = Object.keys(APPS).map((slug) => palette(root, slug));
  for (const colors of all) {
    assert.equal(Object.keys(colors).length, 7);
    for (const color of Object.values(colors)) assert.match(color, /^#[0-9A-F]{6}$/);
  }
  for (const name of ['ink', 'paper', 'margin-blue', 'slate', 'night']) assert.equal(new Set(all.map((colors) => colors[name])).size, 1, name);
  assert.equal(new Set(all.map((colors) => colors['app-color'])).size, 3);
});

test('writing takes the kit\'s files, leaves the app\'s own alone, and records the commit', () => {
  const folder = checkout('book');
  try {
    const before = readFileSync(join(folder, APP_FOLDER, 'tokens.json'), 'utf8');
    const first = writeApp(root, 'book', folder, COMMIT);
    const entry = appEntry(root, 'book');
    assert.equal(first.changed.length, entry.carried.length + 1); // every carried file, and the record
    assert.ok(first.changed.every((line) => line.startsWith('added: ')));
    assert.match(first.notes.join('\n'), /mark-mask\.png is made from wordsmith-book-mark-ink\.svg, which changed: make it again \(tools\/brand-mask\.py\)/);
    assert.equal(readFileSync(join(folder, APP_FOLDER, 'tokens.json'), 'utf8'), before);
    assert.equal(readFileSync(join(folder, APP_FOLDER, 'mark-mask.png'), 'utf8'), 'made by the app');
    const record = JSON.parse(readFileSync(join(folder, APP_FOLDER, RECORD), 'utf8'));
    assert.deepEqual(record.kit, { repository: 'jamescjfoundation/wordsmith', commit: COMMIT });
    assert.deepEqual(record.app, entry);

    const { problems, notes } = checkApp(root, 'book', folder);
    assert.deepEqual(problems, []);
    assert.match(notes.join('\n'), /taken at kit commit 0123456/);

    // a second run changes nothing, and does not move the recorded commit
    const again = writeApp(root, 'book', folder, 'f'.repeat(40));
    assert.deepEqual(again.changed, []);
    assert.equal(again.same, entry.carried.length);
    assert.equal(JSON.parse(readFileSync(join(folder, APP_FOLDER, RECORD), 'utf8')).kit.commit, COMMIT);
  } finally {
    rmSync(folder, { recursive: true });
  }
});

test('the check names a changed copy, a missing one, a stray file and a wrong palette', () => {
  const folder = checkout('script');
  try {
    writeApp(root, 'script', folder, COMMIT);
    const brand = join(folder, APP_FOLDER);
    writeFileSync(join(brand, 'favicon.svg'), '<svg/>');
    rmSync(join(brand, 'icon-512.png'));
    writeFileSync(join(brand, 'logo-recolored.svg'), '<svg/>');
    writeFileSync(join(brand, 'script', 'tokens.json'), JSON.stringify({ palette: { ink: '#000000' } }));
    rmSync(join(brand, 'wordmark-mask.png'));
    const found = checkApp(root, 'script', folder).problems.join('\n');
    assert.match(found, /favicon\.svg: differs from the kit's brand\/wordsmith-script\/production\/favicon\.svg/);
    assert.match(found, /icon-512\.png: missing/);
    assert.match(found, /logo-recolored\.svg: in assets\/brand\/, and not in the kit's list/);
    assert.match(found, /script\/tokens\.json: its palette is #000000; the kit's seven colors are/);
    assert.match(found, /wordmark-mask\.png: missing \(the app makes it from wordsmith-script-wordmark-ink\.svg\)/);

    // taking the kit's files again repairs the copies, and only them
    const repaired = writeApp(root, 'script', folder, COMMIT);
    assert.deepEqual(repaired.changed.map((line) => line.split(' (')[0]).sort(), ['added: icon-512.png', 'updated: favicon.svg']);
    assert.ok(existsSync(join(brand, 'logo-recolored.svg')), 'the tool removes nothing from an app');
  } finally {
    rmSync(folder, { recursive: true });
  }
});

test('a folder that is not an app is refused', () => {
  const folder = mkdtempSync(join(tmpdir(), 'brand-none-'));
  try {
    assert.throws(() => writeApp(root, 'book', folder, COMMIT), /no assets\/brand\/ folder/);
    assert.match(checkApp(root, 'book', folder).problems.join('\n'), /no assets\/brand\/ folder/);
  } finally {
    rmSync(folder, { recursive: true });
  }
});

test('the copies in this repository name kit files that exist', () => {
  assert.ok(copies.length > 30);
  for (const [from] of copies) assert.ok(existsSync(join(root, 'brand', from)), from);
});
