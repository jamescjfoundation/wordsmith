// The wiki's rules for an app's state (lib/releases.mjs). They are the same rules as the
// website's (website/tools/releases.py, tested in website/tools/test_releases.py): keep the
// cases here and there the same.
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { test } from 'node:test';
import { fileURLToPath } from 'node:url';
import { filesFor, longDate, sizeWords, stateOf, stateWords, versionKey } from '../lib/releases.mjs';

const data = join(dirname(fileURLToPath(import.meta.url)), '..', '..', 'data');
const platforms = Object.fromEntries(JSON.parse(readFileSync(join(data, 'platforms.json'), 'utf8')).map((one) => [one.id, one]));
const app = {
  state: {
    none: { chip: '', line: 'Free' },
    preview: { chip: 'Preview {version}', line: 'Preview, {date}' },
    released: { chip: 'Version {version}', line: 'Released {date}' },
  },
};
const release = (version, more = {}) => ({ version, date: '2026-12-01', prerelease: false, files: [], ...more });
const file = (name) => ({ name, url: 'u', size: 1 });

test('where an app stands', () => {
  assert.equal(stateOf(null), 'none');
  assert.equal(stateOf(release('0.9.0')), 'preview');
  assert.equal(stateOf(release('1.0.0')), 'released');
  assert.equal(stateOf(release('1.1.0-beta.1', { prerelease: true })), 'preview');
  assert.deepEqual(versionKey('v1.10.2'), [1, 10, 2]);
});

test('dates and sizes', () => {
  assert.equal(longDate('2026-12-01'), '1 December 2026');
  assert.equal(sizeWords(50 * 1024 ** 2), '50 MB');
  assert.equal(sizeWords(300), '1 KB');
  assert.equal(sizeWords(Math.floor(1.25 * 1024 ** 3)), '1.3 GB');
  assert.equal(sizeWords(Math.floor(2.5 * 1024 ** 2)), '3 MB');
});

test('the words for each state', () => {
  assert.deepEqual(stateWords(app, null), { chip: '', line: 'Free' });
  assert.deepEqual(stateWords(app, release('0.9.0')), { chip: 'Preview 0.9.0', line: 'Preview, 1 December 2026' });
  assert.deepEqual(stateWords(app, release('1.0.0')), { chip: 'Version 1.0.0', line: 'Released 1 December 2026' });
});

test('every platform finds its file and no other', () => {
  const files = ['app-0.9.0-macos-aarch64.dmg', 'app-0.9.0-macos-aarch64.dmg.sha256', 'app-0.9.0-windows-x64-portable.zip', 'app-0.9.0-linux-x86_64.tar.gz', 'SHA256SUMS.txt'].map(file);
  const found = Object.fromEntries(Object.values(platforms).map((one) => [one.id, filesFor(release('0.9.0', { files }), one).map((each) => each.name)]));
  assert.deepEqual(found, {
    'macos-arm64': ['app-0.9.0-macos-aarch64.dmg'],
    'windows-x64': ['app-0.9.0-windows-x64-portable.zip'],
    'linux-x64': ['app-0.9.0-linux-x86_64.tar.gz'],
  });
  assert.equal(filesFor(release('1.0.0', { files: [file('wordsmith-book-1.0.0-macos-arm64.dmg')] }), platforms['macos-arm64']).length, 1);
  assert.equal(filesFor(release('1.0.0', { files: [file('wordsmith-manuscript-1.0.0-windows-x86_64.zip')] }), platforms['windows-x64']).length, 1);
  assert.equal(filesFor(release('1.0.0', { files: [file('wordsmith-script-1.0.0-macos-x86_64.dmg')] }), platforms['macos-arm64']).length, 0);
  assert.equal(filesFor(release('1.0.0', { files: [file('wordsmith-script-1.0.0-linux-aarch64.tar.gz')] }), platforms['linux-x64']).length, 0);
  assert.deepEqual(filesFor(null, platforms['linux-x64']), []);
});
