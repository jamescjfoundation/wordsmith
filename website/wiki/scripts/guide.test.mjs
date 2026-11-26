// Tests for the guide tool: `npm test` in website/wiki (the checks workflow runs it).
// Nothing here uses the network or another repository: an app's repository is a made-up one.
import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { existsSync, mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import { test } from 'node:test';
import { convertPage, imagePath, pagePath, plain, readIndex, sectionMeta } from './guide-pages.mjs';
import { behind, blobId, buildApp, checkApp, LOCK, strays, writeApp } from './guide.mjs';

const COMMIT = '0123456789abcdef0123456789abcdef01234567';
const app = {
  slug: 'script',
  order: 1,
  name: 'Wordsmith Script',
  repository: 'example/app',
  description: 'An app for the test.',
  guide: 'docs/guide',
  images: 'docs/images',
  screenshots: ['window'],
};

function convert(text, more = {}) {
  const pages = new Set(['docs/guide/README.md', 'docs/guide/views.md', 'docs/guide/files.md', 'docs/guide/deep/inner.md']);
  const files = new Set([...pages, 'docs/format.md', 'docs/images/window.png', 'crates/ui/src/lib.rs', 'README.md']);
  return convertPage({ text, source: 'docs/guide/views.md', guideDir: 'docs/guide', pages, files, repository: 'example/app', commit: COMMIT, description: '', lead: '', ...more });
}
const body = (text, more) => convert(`# T\n\n${text}`, more).mdx.split('---\n').slice(2).join('---\n').replace(/^\n+/, '').trimEnd();

test('paths: the README is the index, pictures become WebP', () => {
  assert.equal(pagePath('docs/guide/README.md', 'docs/guide'), 'index.mdx');
  assert.equal(pagePath('docs/guide/views.md', 'docs/guide'), 'views.mdx');
  assert.equal(pagePath('docs/guide/deep/inner.md', 'docs/guide'), 'deep/inner.mdx');
  assert.equal(pagePath('docs/guide/deep/README.md', 'docs/guide'), 'deep/index.mdx');
  assert.equal(imagePath('docs/images/page-view.png'), 'images/page-view.webp');
});

test('the first heading becomes the title, with a description when one is given', () => {
  const page = convert('# The `window`: "all" of it\n\nText.\n', { description: 'What is where.' });
  assert.equal(page.title, 'The window: "all" of it');
  assert.match(page.mdx, /^---\n# Made by website\/wiki\/scripts\/guide\.mjs from docs\/guide\/views\.md in example\/app\.\n/);
  assert.match(page.mdx, /\ntitle: "The window: \\"all\\" of it"\ndescription: "What is where\."\n---\n\nText\.\n$/);
  assert.doesNotMatch(convert('# T\n\nText.\n').mdx, /description:/);
});

test('a page without a heading is titled from its file name, and says so', () => {
  const page = convert('Just text.\n');
  assert.equal(page.title, 'Views');
  assert.equal(page.warnings.length, 1);
});

test('links between guide pages point at the wiki pages', () => {
  assert.equal(body('See [Files](files.md) and [the start](README.md#top).'), 'See [Files](./files.mdx) and [the start](./index.mdx#top).');
  assert.equal(body('[Inner](deep/inner.md)'), '[Inner](./deep/inner.mdx)');
  const inner = convertPage({ text: '# I\n\n[Up](../views.md) ![w](../../images/window.png)', source: 'docs/guide/deep/inner.md', guideDir: 'docs/guide', pages: new Set(['docs/guide/views.md', 'docs/guide/deep/inner.md']), files: new Set(['docs/images/window.png']), repository: 'example/app', commit: COMMIT, description: '', lead: '' });
  assert.match(inner.mdx, /\[Up\]\(\.\.\/views\.mdx\) !\[w\]\(\.\.\/images\/window\.webp\)/);
});

test('links to other files of the repository become full links at the commit', () => {
  assert.equal(body('The [format](../format.md#version) and the [code](../../crates/ui/src/lib.rs).'),
    `The [format](https://github.com/example/app/blob/${COMMIT}/docs/format.md#version) and the [code](https://github.com/example/app/blob/${COMMIT}/crates/ui/src/lib.rs).`);
  assert.equal(body('[The crates](../../crates/) and [the repository](../..)'),
    `[The crates](https://github.com/example/app/tree/${COMMIT}/crates) and [the repository](https://github.com/example/app/tree/${COMMIT})`);
  assert.equal(body('[ref]\n\n[ref]: ../format.md "The format"'), `[ref]\n\n[ref]: https://github.com/example/app/blob/${COMMIT}/docs/format.md "The format"`);
});

test('a link to a file that is not there is reported', () => {
  const page = convert('# T\n\n[Gone](../gone.md)');
  assert.equal(page.warnings.length, 1);
  assert.match(page.warnings[0], /gone\.md/);
});

test('other links are left alone', () => {
  const text = 'A [site](https://example.org/a.md), [mail](mailto:a@example.org), [here](#part) and [[Name]].'; // privacy:allow
  assert.equal(body(text), text);
});

test('pictures are carried and named', () => {
  const page = convert('# T\n\n![The window](../images/window.png "Title")');
  assert.deepEqual(page.images, ['docs/images/window.png']);
  assert.match(page.mdx, /!\[The window\]\(\.\/images\/window\.webp "Title"\)/);
  assert.throws(() => convert('# T\n\n![x](../images/missing.png)'), /not in the repository/);
  assert.throws(() => convert('# T\n\n![x](../format.md)'), /not a PNG/);
});

test('code is never changed', () => {
  const fenced = '```sh\nexport A={b} <c> [x](files.md)\n```';
  assert.equal(body(fenced), fenced);
  assert.equal(body('Use `{page}` and `<name> [x](files.md)` and ``a ` b``.'), 'Use `{page}` and `<name> [x](files.md)` and ``a ` b``.');
  assert.equal(body('| Key |\n| --- |\n| `Mod+Alt+\\` |'), '| Key |\n| --- |\n| `Mod+Alt+\\` |');
  assert.equal(body('   ```\n   <tag>\n   ```\n\nAfter {x}.'), '   ```\n   <tag>\n   ```\n\nAfter \\{x\\}.');
  assert.equal(body('[`code`](files.md)'), '[`code`](./files.mdx)');
});

test('what MDX would read as code is written as text', () => {
  assert.equal(body('Fields {title} and a < b, kept \\{so\\}.'), 'Fields \\{title\\} and a \\< b, kept \\{so\\}.');
  assert.equal(body('export the file\n\nimport a file\n\nexports stay'), '&#x65;xport the file\n\n&#x69;mport a file\n\nexports stay');
  assert.equal(body('Before <!-- a\nnote --> after.'), 'Before  after.');
  assert.equal(body('See <https://example.org/a>.'), 'See [https://example.org/a](https://example.org/a).');
  const page = convert('# T\n\nA <b>bold</b> word.');
  assert.match(page.mdx, /A \\<b>bold\\<\/b> word\./);
  assert.equal(page.warnings.length, 1);
});

test('an unclosed backtick does not swallow the page', () => {
  assert.equal(body('A ` alone.\n\nThen {x}.'), 'A ` alone.\n\nThen \\{x\\}.');
});

test('plain text of a line', () => {
  assert.equal(plain('**The** `x` and [a link](y.md)\nwrapped'), 'The x and a link wrapped');
});

test('the README gives the order and the descriptions', () => {
  const pages = new Set(['docs/guide/README.md', 'docs/guide/views.md', 'docs/guide/files.md', 'docs/guide/keys.md']);
  const readme = '# Guide\n\nAn app for *long* work,\nin one place.\n\n1. [Files](files.md): the format,\n   and backups\n2. [Views](views.md).\n3. [Elsewhere](https://example.org)\n4. [Files again](files.md)\n\nA closing note.\n';
  const index = readIndex(readme, 'docs/guide/README.md', pages);
  assert.deepEqual(index.order, ['docs/guide/files.md', 'docs/guide/views.md']);
  assert.equal(index.descriptions.get('docs/guide/files.md'), 'The format, and backups.');
  assert.equal(index.descriptions.has('docs/guide/views.md'), false);
  const meta = JSON.parse(sectionMeta(app, pages, 'docs/guide', index.order));
  assert.deepEqual(meta, { title: 'Wordsmith Script', icon: 'brand:wordsmith-script', root: true, pages: ['index', 'files', 'views', 'keys'] });
});

test('blob ids are git\'s', () => {
  assert.equal(blobId(Buffer.from('')), 'e69de29bb2d1d6434b8b29ae775ad8c2e48c5391');
  assert.equal(blobId(Buffer.from('hello\n')), 'ce013625030ba8dba906f756967f9e9ca394464a');
});

// ---------------------------------------------------------------- a made-up repository and a temporary folder

function repository(texts) {
  const data = new Map(Object.entries(texts).map(([path, text]) => [path, Buffer.from(text)]));
  return {
    files: new Map([...data].map(([path, bytes]) => [path, blobId(bytes)])),
    date: '2026-01-02',
    read: (paths) => new Map(paths.filter((path) => data.has(path)).map((path) => [path, data.get(path)])),
    close() {},
  };
}
const GUIDE = {
  'docs/guide/README.md': '# Script guide\n\n1. [Views](views.md): how to look at a script.\n',
  'docs/guide/views.md': '# Views\n\n![The window](../images/window.png)\n\nSee the [format](../format.md).\n',
  'docs/format.md': '# Format\n',
  'docs/images/window.png': 'not really a picture',
  'docs/images/unused.png': 'another',
};
// stands in for the picture encoder, so the tests need no image library
const fakeEncode = async (png) => ({ data: Buffer.from(`webp of ${png.toString()}`), width: 1600, height: 1000 });

async function written() {
  const root = mkdtempSync(join(tmpdir(), 'guide-test-'));
  const repo = repository(GUIDE);
  const result = await writeApp(root, app, COMMIT, repo, undefined, fakeEncode);
  return { root, repo, ...result };
}

test('writing a section gives pages, a meta file, pictures and a lock entry', async () => {
  const { root, entry, changed, warnings } = await written();
  try {
    assert.deepEqual(warnings, []);
    assert.deepEqual(changed.sort(), [
      'website/assets/img/script-window.webp',
      'website/wiki/content/docs/script/images/window.webp',
      'website/wiki/content/docs/script/index.mdx',
      'website/wiki/content/docs/script/meta.json',
      'website/wiki/content/docs/script/views.mdx',
    ]);
    assert.equal(entry.commit, COMMIT);
    assert.equal(entry.date, '2026-01-02');
    assert.deepEqual(entry.pages.map((page) => page.source), ['docs/guide/README.md', 'docs/guide/views.md']);
    assert.deepEqual(entry.images.map((image) => [image.source, image.copies.map((copy) => copy.file)]), [
      ['docs/images/window.png', ['website/wiki/content/docs/script/images/window.webp', 'website/assets/img/script-window.webp']],
    ]);
    const index = readFileSync(join(root, 'website/wiki/content/docs/script/index.mdx'), 'utf8');
    assert.match(index, /description: "An app for the test\."\n---\n\n<Downloads app="script" \/>\n\n1\. \[Views\]/);
    const views = readFileSync(join(root, 'website/wiki/content/docs/script/views.mdx'), 'utf8');
    assert.match(views, /description: "How to look at a script\."/);
    assert.match(views, /!\[The window\]\(\.\/images\/window\.webp\)/);
  } finally {
    rmSync(root, { recursive: true });
  }
});

test('the check passes on what was written, and names each kind of difference', async () => {
  const { root, repo, entry } = await written();
  try {
    assert.deepEqual(checkApp(root, app, entry, repo).problems, []);
    assert.deepEqual(strays(root, [app], { apps: { script: entry } }), []);

    const page = join(root, 'website/wiki/content/docs/script/views.mdx');
    const text = readFileSync(page, 'utf8');
    writeFileSync(page, `${text}\nA line added by hand.\n`);
    assert.match(checkApp(root, app, entry, repo).problems.join('\n'), /views\.mdx: differs/);
    writeFileSync(page, text);

    const picture = join(root, 'website/assets/img/script-window.webp');
    const bytes = readFileSync(picture);
    writeFileSync(picture, 'edited');
    assert.match(checkApp(root, app, entry, repo).problems.join('\n'), /script-window\.webp: is not the picture/);
    writeFileSync(picture, bytes);

    rmSync(join(root, 'website/wiki/content/docs/script/meta.json'));
    assert.match(checkApp(root, app, entry, repo).problems.join('\n'), /meta\.json: missing/);

    // the same lock entry against a repository whose guide and picture are different files
    const other = repository({ ...GUIDE, 'docs/guide/views.md': '# Views\n\nNew words.\n', 'docs/images/window.png': 'redrawn' });
    const found = checkApp(root, app, entry, other).problems.join('\n');
    assert.match(found, /views\.mdx: differs/);
    assert.match(found, /out of date/);

    const hand = join(root, 'website/wiki/content/docs/script/whats-next.mdx');
    writeFileSync(hand, '---\ntitle: By hand\n---\n');
    assert.deepEqual(strays(root, [app], { apps: { script: entry } }), ['website/wiki/content/docs/script/whats-next.mdx']);
  } finally {
    rmSync(root, { recursive: true });
  }
});

test('a picture is written again only when its source changed', async () => {
  const { root, repo, entry } = await written();
  try {
    let calls = 0;
    const counting = async (png) => {
      calls += 1;
      return fakeEncode(png);
    };
    const again = await writeApp(root, app, COMMIT, repo, entry, counting);
    assert.equal(calls, 0);
    assert.deepEqual(again.changed, []);
    assert.deepEqual(again.entry, entry);

    const redrawn = repository({ ...GUIDE, 'docs/images/window.png': 'redrawn' });
    const next = await writeApp(root, app, COMMIT, redrawn, entry, counting);
    assert.equal(calls, 1);
    assert.deepEqual(next.changed.sort(), ['website/assets/img/script-window.webp', 'website/wiki/content/docs/script/images/window.webp']);
  } finally {
    rmSync(root, { recursive: true });
  }
});

test('behind lists what changed in the guide since the recorded commit', async () => {
  const { root, repo, entry } = await written();
  try {
    assert.deepEqual(behind(app, entry, repo.files), []);
    const later = repository({
      'docs/guide/README.md': GUIDE['docs/guide/README.md'],
      'docs/guide/views.md': '# Views\n\nNew words.\n',
      'docs/guide/keys.md': '# Keys\n',
      'docs/images/window.png': 'redrawn',
      'README.md': 'not part of the guide',
    });
    assert.deepEqual(behind(app, entry, later.files), ['changed: docs/guide/views.md', 'added: docs/guide/keys.md', 'changed: docs/images/window.png']);
  } finally {
    rmSync(root, { recursive: true });
  }
});

test('a guide without a README, or a screenshot that is not there, is refused', () => {
  assert.throws(() => buildApp(app, COMMIT, repository({ 'docs/guide/views.md': '# Views\n' })), /README\.md/);
  assert.throws(() => buildApp({ ...app, screenshots: ['nowhere'] }, COMMIT, repository(GUIDE)), /nowhere\.png/);
});

test('this repository: the lock file names files that exist', () => {
  const root = join(dirname(new URL(import.meta.url).pathname), '..', '..', '..');
  const lock = JSON.parse(readFileSync(join(root, LOCK), 'utf8'));
  for (const entry of Object.values(lock.apps)) {
    assert.match(entry.commit, /^[0-9a-f]{40}$/);
    for (const page of entry.pages) assert.ok(existsSync(join(root, page.file)), page.file);
    for (const image of entry.images) for (const copy of image.copies) assert.ok(existsSync(join(root, copy.file)), copy.file);
  }
});

test('reading a real repository with git: the files and one file\'s content', () => {
  // a small repository made here, read the way a checkout beside this one is read
  const base = mkdtempSync(join(tmpdir(), 'guide-git-'));
  try {
    const work = join(base, 'app');
    mkdirSync(join(work, 'docs/guide'), { recursive: true });
    writeFileSync(join(work, 'docs/guide/README.md'), '# Guide\n');
    const git = (...args) => execFileSync('git', ['-C', work, ...args], { encoding: 'utf8' });
    execFileSync('git', ['init', '-q', work]);
    git('add', '.');
    git('-c', 'user.name=test', '-c', 'user.email=test@users.noreply.github.com', 'commit', '-q', '-m', 'guide');
    const commit = git('rev-parse', 'HEAD').trim();
    return import('./guide.mjs').then(({ openRepository }) => {
      const repo = openRepository('example/app', commit, join(base, 'wordsmith'));
      assert.equal(repo.files.get('docs/guide/README.md'), blobId(Buffer.from('# Guide\n')));
      assert.equal(repo.read(['docs/guide/README.md']).get('docs/guide/README.md').toString(), '# Guide\n');
      assert.match(repo.date, /^\d{4}-\d{2}-\d{2}$/);
      repo.close();
      rmSync(base, { recursive: true });
    });
  } catch (error) {
    rmSync(base, { recursive: true });
    throw error;
  }
});

test('headings get the anchors the wiki gives them', async () => {
  const { headingAnchor } = await import('./guide.mjs');
  assert.equal(headingAnchor('Updates and privacy'), 'updates-and-privacy');
  assert.equal(headingAnchor("A project's files: .wsm & more"), 'a-projects-files-wsm--more');
});

test('a link between wiki pages that leads nowhere is found', async () => {
  const { brokenLinks } = await import('./guide.mjs');
  const root = mkdtempSync(join(tmpdir(), 'guide-links-'));
  try {
    const put = (file, text) => {
      mkdirSync(dirname(join(root, file)), { recursive: true });
      writeFileSync(join(root, file), text);
    };
    put('website/wiki/content/docs/start/index.mdx', [
      '---', 'title: Start', '---', '',
      '[Views](../script/views.mdx), [a part](../script/views.mdx#draft-view), [twice](../script/views.mdx#notes-1), [here](#below).',
      '<Card title="Files" href="../script/files.mdx" /> ![w](../script/images/window.webp)',
      '[gone](../script/gone.mdx) and [no part](../script/views.mdx#nowhere) and `[code](./never.mdx)`',
      '```', '[fenced](./never.mdx)', '```', '[site](https://example.org/x.mdx) [root](/wiki/x)', '', '## Below', '',
    ].join('\n'));
    put('website/wiki/content/docs/script/views.mdx', '---\ntitle: Views\n---\n\n## Draft view\n\n## Notes\n\n## Notes\n');
    put('website/wiki/content/docs/script/files.mdx', '---\ntitle: Files\n---\n');
    put('website/wiki/content/docs/script/images/window.webp', 'picture');
    assert.deepEqual(brokenLinks(root), [
      'website/wiki/content/docs/start/index.mdx:7: "../script/gone.mdx" names no file',
      'website/wiki/content/docs/start/index.mdx:7: "../script/views.mdx#nowhere" names no heading of that page',
    ]);
  } finally {
    rmSync(root, { recursive: true });
  }
});
