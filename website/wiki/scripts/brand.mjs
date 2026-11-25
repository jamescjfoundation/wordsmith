// Copies the brand files the wiki uses from the repository's brand/ kit into public/brand/,
// unchanged and with the kit's folder names. Never edit the copies: change brand/ and run this again.
//
//   npm run brand          copy the files
//   npm run brand:check    fail if a copy is missing or differs from brand/ (run by the deploy)
import { copyFileSync, mkdirSync, readFileSync, existsSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const wiki = join(dirname(fileURLToPath(import.meta.url)), '..');
const kit = join(wiki, '..', '..', 'brand');
const out = join(wiki, 'public', 'brand');

const files = [];
for (const name of ['wordsmith-and-ink', 'wordsmith-script', 'wordsmith-manuscript', 'wordsmith-book']) {
  files.push(
    `${name}/logo/${name}-wordmark-ink.svg`,
    `${name}/logo/${name}-wordmark-paper.svg`,
    `${name}/app-icon/${name}-icon.svg`,
    `${name}/app-icon/${name}-icon-small.svg`,
    `${name}/app-icon/favicon.svg`,
  );
}

const check = process.argv.includes('--check');
const stale = [];
for (const file of files) {
  const from = join(kit, file);
  const to = join(out, file);
  if (check) {
    if (!existsSync(to) || !readFileSync(from).equals(readFileSync(to))) stale.push(file);
  } else {
    mkdirSync(dirname(to), { recursive: true });
    copyFileSync(from, to);
  }
}

if (stale.length) {
  console.error(`These brand files in public/brand/ are missing or differ from brand/:\n  ${stale.join('\n  ')}\nRun "npm run brand" in website/wiki.`);
  process.exit(1);
}
console.log(check ? `${files.length} brand files match brand/.` : `Copied ${files.length} brand files into public/brand/.`);
