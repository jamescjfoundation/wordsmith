// Builds each app's section of the wiki from the app's own guide. The guide in the app's
// repository (docs/guide/, Markdown) is the source: this script reads it at one commit, turns
// each page into a wiki page, carries the pictures the pages show, and records the commit in
// guides.lock.json. The pages it writes are never edited by hand.
//
//   npm run guide                      every app, from the head of its main branch on GitHub
//   npm run guide -- --app script      one app
//   npm run guide -- --app script --ref v1.0.0     at a branch, a tag or a full commit id
//   npm run guide:check                fail if a page, a picture or the lock file is not what
//                                      the recorded commits give, or a link from one wiki page
//                                      to another leads nowhere (the checks workflow runs it)
//   npm run guide:behind               fail if an app's guide on main has changed since the
//                                      recorded commit (guides.yml runs it on a schedule)
//
// What it owns: website/wiki/content/docs/<app>/ (every file in it), website/assets/img/ (the
// screenshots the website shows, named in each app's file under website/data/apps/) and
// website/wiki/guides.lock.json.
//
// It reads a repository with git: a checkout beside this repository when that checkout already
// has the commit, and otherwise a small temporary fetch from GitHub (the commit's folders and
// only the files needed). No GitHub API, no token. Pictures are scaled to 1600 pixels wide and
// written as WebP with sharp, which the wiki's build already installs; a picture whose source
// has not changed is not written again, so the check never depends on the encoder.
import { execFileSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { existsSync, mkdirSync, mkdtempSync, readFileSync, readdirSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { convertPage, imagePath, pagePath, readIndex, sectionMeta } from './guide-pages.mjs';

const wiki = join(dirname(fileURLToPath(import.meta.url)), '..');
const repositoryRoot = join(wiki, '..', '..');

export const LOCK = 'website/wiki/guides.lock.json';
export const SECTIONS = 'website/wiki/content/docs';
export const SITE_IMAGES = 'website/assets/img';
export const APPS = 'website/data/apps';
const IMAGE_WIDTH = 1600;

const sha256 = (data) => createHash('sha256').update(data).digest('hex');
/** The id git gives a file's content, so a file can be matched to a commit without git. */
export const blobId = (data) => createHash('sha1').update(`blob ${data.length}\0`).update(data).digest('hex');

/** The apps, from website/data/apps/<slug>.json, in their `order`. */
export function readApps(root) {
  const folder = join(root, APPS);
  return readdirSync(folder)
    .filter((name) => name.endsWith('.json'))
    .map((name) => JSON.parse(readFileSync(join(folder, name), 'utf8')))
    .sort((a, b) => a.order - b.order);
}

export function readLock(root) {
  const file = join(root, LOCK);
  return existsSync(file) ? JSON.parse(readFileSync(file, 'utf8')) : { apps: {} };
}

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

// ---------------------------------------------------------------- reading a repository with git

function git(args, options = {}) {
  return execFileSync('git', args, {
    maxBuffer: 256 * 1024 * 1024,
    stdio: ['pipe', 'pipe', 'pipe'],
    env: { ...process.env, GIT_TERMINAL_PROMPT: '0' },
    ...options,
  });
}

const repositoryUrl = (repository) => `https://github.com/${repository}`;

/** The commit a branch or tag of the repository on GitHub points at. A full commit id is returned as it is. */
export function resolveRef(repository, ref) {
  if (/^[0-9a-f]{40}$/.test(ref)) return ref;
  const lines = git(['ls-remote', repositoryUrl(repository), ref, `${ref}^{}`], { encoding: 'utf8' })
    .split('\n')
    .filter(Boolean)
    .map((line) => line.split('\t'));
  const wanted = [`refs/tags/${ref}^{}`, `refs/heads/${ref}`, `refs/tags/${ref}`];
  for (const name of wanted) {
    const hit = lines.find(([, found]) => found === name);
    if (hit) return hit[0];
  }
  throw new Error(`${repository} has no branch or tag "${ref}" on GitHub`);
}

/**
 * Opens a repository at one commit. Returns { files: Map(path → blob id), date, read(paths) →
 * Map(path → Buffer), close() }. `date` is the day the commit was made (UTC).
 */
export function openRepository(repository, commit, root = repositoryRoot) {
  const sibling = join(root, '..', repository.split('/')[1]);
  let folder = null;
  let temporary = false;
  if (existsSync(sibling)) {
    try {
      git(['-C', sibling, 'cat-file', '-e', `${commit}^{commit}`]);
      folder = sibling;
    } catch {
      // the checkout does not have this commit yet
    }
  }
  if (!folder) {
    folder = mkdtempSync(join(tmpdir(), 'wordsmith-guide-'));
    temporary = true;
    git(['init', '-q', folder]);
    git(['-C', folder, 'remote', 'add', 'origin', repositoryUrl(repository)]);
    // the commit and its folders, without any file's content
    git(['-C', folder, 'fetch', '-q', '--depth', '1', '--filter=blob:none', '--no-tags', 'origin', commit]);
  }
  const files = new Map();
  for (const line of git(['-C', folder, 'ls-tree', '-r', '-z', commit], { encoding: 'utf8' }).split('\0')) {
    const found = /^\d+ blob ([0-9a-f]{40})\t(.+)$/.exec(line);
    if (found) files.set(found[2], found[1]);
  }
  const seconds = Number(git(['-C', folder, 'show', '-s', '--format=%ct', commit], { encoding: 'utf8' }).trim());
  return {
    files,
    date: new Date(seconds * 1000).toISOString().slice(0, 10),
    read(paths) {
      const wanted = paths.filter((path) => files.has(path));
      if (temporary && wanted.length) {
        // one request for every file still missing, instead of one request per file
        git(
          ['-C', folder, '-c', 'fetch.negotiationAlgorithm=noop', 'fetch', '-q', 'origin', '--no-tags', '--no-write-fetch-head',
            '--recurse-submodules=no', '--filter=blob:none', '--stdin'],
          { input: [...new Set(wanted.map((path) => files.get(path)))].join('\n') },
        );
      }
      return new Map(wanted.map((path) => [path, git(['-C', folder, 'cat-file', 'blob', files.get(path)])]));
    },
    close() {
      if (temporary) rmSync(folder, { recursive: true, force: true });
    },
  };
}

// ---------------------------------------------------------------- building one app's section

/**
 * Everything one app's section holds at one commit, built in memory.
 * Returns { pages: [{ source, blob, file, text }], meta: { file, text }, images: [{ source, blob,
 * copies: [file] }], warnings }.
 */
export function buildApp(app, commit, repo) {
  const guideDir = app.guide;
  const sources = [...repo.files.keys()].filter((path) => path.startsWith(`${guideDir}/`) && path.endsWith('.md')).sort();
  if (!sources.length) throw new Error(`${app.repository} has no Markdown pages in ${guideDir}/ at ${commit.slice(0, 7)}`);
  const pages = new Set(sources);
  const files = new Set(repo.files.keys());
  const texts = repo.read(sources);
  const section = `${SECTIONS}/${app.slug}`;
  const readme = sources.find((path) => pagePath(path, guideDir) === 'index.mdx');
  if (!readme) throw new Error(`${app.repository} has no ${guideDir}/README.md at ${commit.slice(0, 7)}: the section needs a first page`);
  const index = readIndex(texts.get(readme).toString('utf8'), readme, pages);

  const built = [];
  const warnings = [];
  const shown = new Map(); // picture in the repository → the files it becomes here
  for (const source of sources) {
    // the first page takes the app's one line from its data file; its own first paragraph stays in its text
    const description = source === readme ? app.description : (index.descriptions.get(source) ?? '');
    // the section's first page starts with the app's downloads, which the wiki draws from website/data/
    const lead = source === readme ? `<Downloads app="${app.slug}" />` : '';
    const page = convertPage({ text: texts.get(source).toString('utf8'), source, guideDir, pages, files, repository: app.repository, commit, description, lead });
    warnings.push(...page.warnings);
    built.push({ source, blob: repo.files.get(source), file: `${section}/${pagePath(source, guideDir)}`, text: page.mdx });
    for (const image of page.images) shown.set(image, [`${section}/${imagePath(image)}`]);
  }
  // the screenshots the website shows, whether or not a guide page shows them
  for (const name of app.screenshots ?? []) {
    const source = `${app.images}/${name}.png`;
    if (!repo.files.has(source)) throw new Error(`${app.repository} has no ${source} at ${commit.slice(0, 7)} (named in ${APPS}/${app.slug}.json)`);
    shown.set(source, [...(shown.get(source) ?? []), `${SITE_IMAGES}/${app.slug}-${name}.webp`]);
  }
  const images = [...shown.keys()].sort().map((source) => ({ source, blob: repo.files.get(source), copies: shown.get(source) }));
  const meta = { file: `${section}/meta.json`, text: sectionMeta(app, pages, guideDir, index.order) };
  return { pages: built, meta, images, warnings };
}

async function encode(png) {
  let sharp;
  try {
    ({ default: sharp } = await import('sharp'));
  } catch {
    throw new Error('A picture has to be written and sharp is not installed. Run `npm ci` in website/wiki first.');
  }
  const { data, info } = await sharp(png)
    .resize({ width: IMAGE_WIDTH, withoutEnlargement: true })
    .webp({ quality: 82 })
    .toBuffer({ resolveWithObject: true });
  return { data, width: info.width, height: info.height };
}

/** Writes one app's section and returns its entry for the lock file, with what changed. */
export async function writeApp(root, app, commit, repo, before, convert = encode) {
  const built = buildApp(app, commit, repo);
  const changed = [];
  const put = (file, data) => {
    const path = join(root, file);
    const same = existsSync(path) && readFileSync(path).equals(Buffer.from(data));
    if (!same) {
      mkdirSync(dirname(path), { recursive: true });
      writeFileSync(path, data);
      changed.push(file);
    }
  };
  const entry = { repository: app.repository, commit, date: repo.date, pages: [], meta: null, images: [] };
  for (const page of built.pages) {
    put(page.file, page.text);
    entry.pages.push({ source: page.source, blob: page.blob, file: page.file, sha256: sha256(page.text) });
  }
  put(built.meta.file, built.meta.text);
  entry.meta = { file: built.meta.file, sha256: sha256(built.meta.text) };

  // A picture is written again only when its source changed, or its copy is missing or altered.
  const known = new Map((before?.images ?? []).map((image) => [image.source, image]));
  const todo = built.images.filter((image) => {
    const old = known.get(image.source);
    if (!old || old.blob !== image.blob) return true;
    return image.copies.some((file) => {
      const copy = old.copies.find((one) => one.file === file);
      return !copy || !existsSync(join(root, file)) || sha256(readFileSync(join(root, file))) !== copy.sha256;
    });
  });
  const sources = repo.read(todo.map((image) => image.source));
  for (const image of built.images) {
    if (todo.includes(image)) {
      const made = await convert(sources.get(image.source));
      const copies = image.copies.map((file) => {
        put(file, made.data);
        return { file, sha256: sha256(made.data), width: made.width, height: made.height };
      });
      entry.images.push({ source: image.source, blob: image.blob, copies });
    } else {
      const old = known.get(image.source);
      entry.images.push({ source: image.source, blob: image.blob, copies: image.copies.map((file) => old.copies.find((one) => one.file === file)) });
    }
  }
  return { entry, changed, warnings: built.warnings };
}

/** The files the tool owns that no lock entry names. */
export function strays(root, apps, lock) {
  const named = new Set();
  for (const entry of Object.values(lock.apps)) {
    for (const page of entry.pages) named.add(page.file);
    if (entry.meta) named.add(entry.meta.file);
    for (const image of entry.images) for (const copy of image.copies) named.add(copy.file);
  }
  const owned = [...apps.flatMap((app) => filesUnder(root, `${SECTIONS}/${app.slug}`)), ...filesUnder(root, SITE_IMAGES)];
  return owned.filter((file) => !named.has(file)).sort();
}

/** Compares one app's section with what its recorded commit gives. Returns the problems found. */
export function checkApp(root, app, entry, repo) {
  const problems = [];
  const onDisk = (file) => (existsSync(join(root, file)) ? readFileSync(join(root, file)) : null);
  const built = buildApp(app, entry.commit, repo);
  if (entry.repository !== app.repository) problems.push(`${LOCK}: ${app.slug} is recorded from ${entry.repository}, and ${APPS}/${app.slug}.json names ${app.repository}`);
  if (entry.date !== repo.date) problems.push(`${LOCK}: ${app.slug} records the date ${entry.date}; the commit was made on ${repo.date}`);

  const texts = [...built.pages.map((page) => [page.file, page.text]), [built.meta.file, built.meta.text]];
  const recorded = new Map([...entry.pages, entry.meta].filter(Boolean).map((one) => [one.file, one.sha256]));
  for (const [file, text] of texts) {
    const kept = onDisk(file);
    if (kept === null) problems.push(`${file}: missing`);
    else if (kept.toString('utf8') !== text) problems.push(`${file}: differs from what the guide gives at ${entry.commit.slice(0, 7)}`);
    if (recorded.get(file) !== sha256(text)) problems.push(`${LOCK}: the entry for ${file} is missing or out of date`);
    recorded.delete(file);
  }
  for (const file of recorded.keys()) problems.push(`${LOCK}: names ${file}, which the guide at ${entry.commit.slice(0, 7)} does not give`);

  const images = new Map(entry.images.map((image) => [image.source, image]));
  for (const image of built.images) {
    const kept = images.get(image.source);
    images.delete(image.source);
    if (!kept) {
      problems.push(`${LOCK}: no entry for the picture ${image.source}`);
      continue;
    }
    if (kept.blob !== image.blob) problems.push(`${LOCK}: ${image.source} is recorded as another file than the one at ${entry.commit.slice(0, 7)}`);
    const files = kept.copies.map((copy) => copy.file);
    if (files.join('\n') !== image.copies.join('\n')) problems.push(`${LOCK}: the copies of ${image.source} are not ${image.copies.join(', ')}`);
    for (const copy of kept.copies) {
      const data = onDisk(copy.file);
      if (data === null) problems.push(`${copy.file}: missing`);
      else if (sha256(data) !== copy.sha256) problems.push(`${copy.file}: is not the picture this tool wrote from ${image.source}`);
    }
  }
  for (const source of images.keys()) problems.push(`${LOCK}: names the picture ${source}, which no page and no data file uses`);
  return { problems, warnings: built.warnings };
}

/** What changed in an app's guide between its recorded commit and another commit's files. */
export function behind(app, entry, files) {
  const now = new Map([...files].filter(([path]) => path.startsWith(`${app.guide}/`) && path.endsWith('.md')));
  const changes = [];
  for (const page of entry.pages) {
    if (!now.has(page.source)) changes.push(`removed: ${page.source}`);
    else if (now.get(page.source) !== page.blob) changes.push(`changed: ${page.source}`);
    now.delete(page.source);
  }
  for (const path of [...now.keys()].sort()) changes.push(`added: ${path}`);
  for (const image of entry.images) {
    if (!files.has(image.source)) changes.push(`removed: ${image.source}`);
    else if (files.get(image.source) !== image.blob) changes.push(`changed: ${image.source}`);
  }
  return changes;
}

// ---------------------------------------------------------------- links between the wiki's pages

/** The anchor a heading gets on its page: lower case, punctuation dropped, spaces to hyphens. */
export function headingAnchor(text) {
  return text
    .toLowerCase()
    .replace(/[^\p{L}\p{M}\p{N}\p{Pc}\- ]/gu, '')
    .replace(/ /g, '-');
}

function anchorsOf(mdx) {
  const anchors = new Set();
  const seen = new Map();
  let fence = null;
  for (const line of mdx.split('\n')) {
    const mark = /^\s*(`{3,}|~{3,})/.exec(line);
    if (mark) {
      if (fence === null) fence = mark[1][0];
      else if (mark[1][0] === fence) fence = null;
      continue;
    }
    if (fence !== null) continue;
    const heading = /^#{1,6}[ \t]+(.+?)[ \t]*#*[ \t]*$/.exec(line);
    if (heading) {
      const base = headingAnchor(heading[1].replace(/!?\[((?:\\.|[^\]\\])*)\]\([^)]*\)/g, '$1').replace(/[`*]/g, '').replace(/\\(.)/g, '$1').trim());
      const count = seen.get(base) ?? 0;
      seen.set(base, count + 1);
      anchors.add(count ? `${base}-${count}` : base);
    }
    for (const id of line.matchAll(/\bid="([^"]+)"/g)) anchors.add(id[1]);
  }
  return anchors;
}

/**
 * Every link from one wiki page to another page or to a picture, in Markdown or in a
 * component's href or src, names a file that exists, and its #anchor a heading of that page.
 * The wiki's build does not check this. Returns the broken links.
 */
export function brokenLinks(root) {
  const pages = filesUnder(root, SECTIONS).filter((file) => file.endsWith('.mdx'));
  const texts = new Map(pages.map((file) => [file, readFileSync(join(root, file), 'utf8')]));
  const anchors = new Map();
  const broken = [];
  for (const [file, text] of texts) {
    const body = text.replace(/^---\n[\s\S]*?\n---\n/, (front) => front.replace(/[^\n]/g, ''));
    const lines = body.split('\n');
    let fence = null;
    lines.forEach((line, at) => {
      const mark = /^\s*(`{3,}|~{3,})/.exec(line);
      if (mark) {
        if (fence === null) fence = mark[1][0];
        else if (mark[1][0] === fence) fence = null;
        return;
      }
      if (fence !== null) return;
      const bare = line.replace(/`[^`]*`/g, '');
      const found = [...bare.matchAll(/\]\(\s*<?([^)\s>]+)/g), ...bare.matchAll(/\b(?:href|src)="([^"]+)"/g)].map((one) => one[1]);
      for (const link of found) {
        if (/^[a-z][a-z0-9+.-]*:/i.test(link) || link.startsWith('//') || link.startsWith('/')) continue;
        const [path, anchor] = link.split('#');
        const target = path === '' ? file : posixJoin(file, path);
        if (path !== '' && !existsSync(join(root, target))) {
          broken.push(`${file}:${at + 1}: "${link}" names no file`);
          continue;
        }
        if (anchor && target.endsWith('.mdx')) {
          if (!anchors.has(target)) anchors.set(target, anchorsOf(texts.get(target) ?? readFileSync(join(root, target), 'utf8')));
          if (!anchors.get(target).has(anchor)) broken.push(`${file}:${at + 1}: "${link}" names no heading of that page`);
        }
      }
    });
  }
  return broken;
}

function posixJoin(file, link) {
  const parts = file.split('/').slice(0, -1);
  for (const part of decodeURI(link).split('/')) {
    if (part === '..') parts.pop();
    else if (part !== '.' && part !== '') parts.push(part);
  }
  return parts.join('/');
}

// ---------------------------------------------------------------- the command line

function writeLock(root, lock) {
  writeFileSync(join(root, LOCK), `${JSON.stringify(lock, null, 2)}\n`);
}

async function main(argv) {
  const flag = (name) => argv.includes(name);
  const value = (name) => (argv.includes(name) ? argv[argv.indexOf(name) + 1] : undefined);
  const root = repositoryRoot;
  const apps = readApps(root);
  const only = value('--app');
  const chosen = only ? apps.filter((app) => app.slug === only) : apps;
  if (!chosen.length) throw new Error(`No app "${only}" in ${APPS}/.`);
  const lock = readLock(root);

  if (flag('--behind')) {
    let late = 0;
    for (const app of chosen) {
      const entry = lock.apps[app.slug];
      if (!entry) throw new Error(`${LOCK} has no entry for ${app.slug}. Run \`npm run guide\`.`);
      const head = resolveRef(app.repository, value('--ref') ?? 'main');
      if (head === entry.commit) {
        console.log(`${app.name}: recorded at ${entry.commit.slice(0, 7)}, the head of main.`);
        continue;
      }
      const repo = openRepository(app.repository, head, root);
      const changes = behind(app, entry, repo.files);
      repo.close();
      if (changes.length) {
        late += 1;
        console.error(`${app.name}: the guide changed between ${entry.commit.slice(0, 7)} (recorded) and ${head.slice(0, 7)} (main):\n  ${changes.join('\n  ')}`);
      } else {
        console.log(`${app.name}: recorded at ${entry.commit.slice(0, 7)}; main is at ${head.slice(0, 7)} and the guide is the same.`);
      }
    }
    if (late) {
      console.error('\nRun `npm run guide` in website/wiki, read what changed, and land the pages it writes.');
      process.exit(1);
    }
    return;
  }

  if (flag('--check')) {
    const problems = [];
    for (const app of apps) {
      const entry = lock.apps[app.slug];
      if (!entry) {
        problems.push(`${LOCK}: no entry for ${app.slug}`);
        continue;
      }
      const repo = openRepository(app.repository, entry.commit, root);
      try {
        const result = checkApp(root, app, entry, repo);
        problems.push(...result.problems);
      } finally {
        repo.close();
      }
    }
    for (const slug of Object.keys(lock.apps)) if (!apps.some((app) => app.slug === slug)) problems.push(`${LOCK}: an entry for "${slug}", which has no file in ${APPS}/`);
    for (const file of strays(root, apps, lock)) problems.push(`${file}: this tool does not make it. An app's pages come from the app's guide; a hand-written page belongs in ${SECTIONS}/start/.`);
    if (problems.length) {
      console.error(`${problems.join('\n')}\n\nRun \`npm run guide\` in website/wiki to write the sections again. To change a page, change the guide in the app's repository.`);
      process.exit(1);
    }
    const broken = brokenLinks(root);
    if (broken.length) {
      console.error(`${broken.join('\n')}\n\nThese links between wiki pages lead nowhere. In a page under ${SECTIONS}/start/ or in index.mdx, fix the link. In an app's page, the link is wrong in the app's guide: fix it there.`);
      process.exit(1);
    }
    const pages = Object.values(lock.apps).reduce((sum, entry) => sum + entry.pages.length, 0);
    console.log(`${pages} guide pages and their pictures are what the recorded commits give: ${apps.map((app) => `${app.slug} ${lock.apps[app.slug].commit.slice(0, 7)}`).join(', ')}.`);
    return;
  }

  for (const app of chosen) {
    const commit = resolveRef(app.repository, value('--ref') ?? 'main');
    const repo = openRepository(app.repository, commit, root);
    try {
      const before = lock.apps[app.slug];
      const { entry, changed, warnings } = await writeApp(root, app, commit, repo, before);
      lock.apps[app.slug] = entry;
      const was = before ? ` (was ${before.commit.slice(0, 7)})` : '';
      console.log(`${app.name}: ${entry.pages.length} pages and ${entry.images.length} pictures from ${app.repository} at ${commit.slice(0, 7)}${was}.`);
      for (const file of changed) console.log(`  wrote ${file}`);
      for (const warning of warnings) console.log(`  look at: ${warning}`);
    } finally {
      repo.close();
    }
  }
  for (const file of strays(root, apps, lock)) {
    rmSync(join(root, file));
    console.log(`  removed ${file}`);
  }
  // keep the apps in their order, so the file changes only where an app changed
  lock.apps = Object.fromEntries(apps.filter((app) => lock.apps[app.slug]).map((app) => [app.slug, lock.apps[app.slug]]));
  writeLock(root, { note: 'Written by website/wiki/scripts/guide.mjs. Never edit it: run `npm run guide`.', apps: lock.apps });
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  main(process.argv.slice(2)).catch((error) => {
    console.error(error.message);
    process.exit(1);
  });
}
