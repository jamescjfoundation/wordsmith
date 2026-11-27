// Turns one page of an app's guide (Markdown, as the app's repository keeps it in docs/guide/)
// into a wiki page (MDX with front matter). No file or network access here: guide.mjs reads the
// app's repository and writes the results. Everything in this file is covered by guide.test.mjs.
import { posix } from 'node:path';

const IMAGE = /\.(png|jpe?g|webp)$/i;

/** docs/guide/README.md → index.mdx, docs/guide/a/b.md → a/b.mdx (paths inside the app's wiki section) */
export function pagePath(source, guideDir) {
  const inside = posix.relative(guideDir, source);
  const folder = posix.dirname(inside);
  const name = posix.basename(inside, '.md');
  const file = name.toLowerCase() === 'readme' ? 'index.mdx' : `${name}.mdx`;
  return folder === '.' ? file : `${folder}/${file}`;
}

/** docs/images/page-view.png → images/page-view.webp (inside the app's wiki section) */
export function imagePath(source) {
  return `images/${posix.basename(source).replace(IMAGE, '')}.webp`;
}

function relativeLink(fromPage, to) {
  const link = posix.relative(posix.dirname(fromPage), to);
  return link.startsWith('.') ? link : `./${link}`;
}

/* Code spans are set aside before anything else is changed, and put back at the end. A span
   opens with a run of backticks and closes with a run of the same length in the same block. */
function setCodeAside(text, kept) {
  let out = '';
  let i = 0;
  while (i < text.length) {
    const ch = text[i];
    if (ch === '\\' && i + 1 < text.length) {
      out += text.slice(i, i + 2);
      i += 2;
      continue;
    }
    if (ch !== '`') {
      out += ch;
      i += 1;
      continue;
    }
    let run = 1;
    while (text[i + run] === '`') run += 1;
    let close = -1;
    let j = i + run;
    while (j < text.length) {
      if (text[j] === '`') {
        let other = 1;
        while (text[j + other] === '`') other += 1;
        if (other === run) {
          close = j;
          break;
        }
        j += other;
      } else if (text[j] === '\n' && /^[ \t]*(\n|$)/.test(text.slice(j + 1))) {
        break; // a blank line ends the block
      } else {
        j += 1;
      }
    }
    if (close < 0) {
      out += text.slice(i, i + run);
      i += run;
      continue;
    }
    out += keep(kept, text.slice(i, close + run));
    i = close + run;
  }
  return out;
}

function keep(kept, text) {
  kept.push(text);
  return `\u0000${kept.length - 1}\u0000`;
}

function putBack(text, kept) {
  let out = text;
  // kept pieces can hold other kept pieces (a link whose text is code), so repeat until none is left
  while (/\u0000\d+\u0000/.test(out)) out = out.replace(/\u0000(\d+)\u0000/g, (_, n) => kept[Number(n)]);
  return out;
}

/**
 * Converts one guide page.
 *
 * page: {
 *   text         the Markdown source
 *   source       its path in the app's repository, e.g. docs/guide/views.md
 *   guideDir     the guide's folder, e.g. docs/guide
 *   pages        Set of every guide page's path in the repository
 *   files        Set of every file's path in the repository at that commit
 *   repository   e.g. jamescjfoundation/wordsmith-script
 *   commit       the full commit id the page is read at
 *   description  the page's one-line description, or '' for none
 *   lead         text put at the top of the page's body, or '' (the tool's own, not from the guide)
 * }
 *
 * Returns { mdx, title, images, warnings }: the page, its title, the repository paths of the
 * pictures it shows, and what a person should look at.
 */
export function convertPage(page) {
  const { source, guideDir, pages, files, repository, commit } = page;
  const out = pagePath(source, guideDir);
  const warnings = [];
  const images = [];
  const folders = new Set();
  for (const file of files) {
    let folder = posix.dirname(file);
    while (folder !== '.' && !folders.has(folder)) {
      folders.add(folder);
      folder = posix.dirname(folder);
    }
  }

  function destination(dest, isImage) {
    let target = dest.startsWith('<') && dest.endsWith('>') ? dest.slice(1, -1) : dest;
    if (/^[a-z][a-z0-9+.-]*:/i.test(target) || target.startsWith('//') || target.startsWith('#')) return target;
    let tail = '';
    const cut = target.search(/[?#]/);
    if (cut >= 0) {
      tail = target.slice(cut);
      target = target.slice(0, cut);
    }
    let path;
    try {
      path = decodeURI(target);
    } catch {
      path = target;
    }
    const resolved = posix.normalize(path.startsWith('/') ? path.slice(1) : posix.join(posix.dirname(source), path)).replace(/\/$/, '');
    if (resolved.startsWith('..')) {
      warnings.push(`${source}: the link "${dest}" leaves the repository; left as it is`);
      return dest;
    }
    if (pages.has(resolved)) return relativeLink(out, pagePath(resolved, guideDir)) + tail;
    if (isImage) {
      if (!IMAGE.test(resolved)) throw new Error(`${source}: the picture "${dest}" is not a PNG, JPEG or WebP file`);
      if (!files.has(resolved)) throw new Error(`${source}: the picture "${dest}" is not in the repository at ${commit.slice(0, 7)}`);
      const clash = images.find((other) => other !== resolved && imagePath(other) === imagePath(resolved));
      if (clash) throw new Error(`${source}: the pictures ${clash} and ${resolved} would both be ${imagePath(resolved)}`);
      if (!images.includes(resolved)) images.push(resolved);
      return relativeLink(out, imagePath(resolved));
    }
    const kind = folders.has(resolved) || resolved === '.' ? 'tree' : 'blob';
    if (kind === 'blob' && !files.has(resolved)) {
      warnings.push(`${source}: the link "${dest}" names a file that is not in the repository at ${commit.slice(0, 7)}`);
    }
    const address = resolved === '.' ? '' : `/${encodeURI(resolved)}`;
    return `https://github.com/${repository}/${kind}/${commit}${address}${tail}`;
  }

  function inline(text) {
    const kept = [];
    let work = setCodeAside(text, kept);
    // comments are not Markdown the wiki can show
    work = work.replace(/<!--[\s\S]*?-->/g, '');
    // <https://example.org> is not MDX; write it as a link
    work = work.replace(/<((?:https?|mailto):[^\s<>]+)>/g, (_, url) => keep(kept, `[${url}](${url})`));
    // [text](destination "title") and ![alt](destination)
    work = work.replace(
      /(!?)\[((?:\\.|[^\]\\])*)\]\(\s*(<[^>\n]*>|(?:\\.|[^\s()\\]|\((?:\\.|[^\s()\\])*\))*)(\s+(?:"[^"]*"|'[^']*'))?\s*\)/g,
      (whole, bang, label, dest, title) => {
        if (dest === '') return whole;
        const to = destination(dest, bang === '!');
        const written = /[\s()]/.test(to) ? `<${to}>` : to;
        return `${bang}[${label}]${keep(kept, `(${written}${title ?? ''})`)}`;
      },
    );
    // [label]: destination
    work = work.replace(/^( {0,3}\[[^\]\n]+\]:[ \t]*)(<[^>\n]*>|\S+)(.*)$/gm, (_, head, dest, rest) =>
      keep(kept, `${head}${destination(dest, false)}${rest}`),
    );
    if (/<[A-Za-z/!]/.test(work)) warnings.push(`${source}: HTML in the page is shown as text, not as HTML`);
    // in MDX a bare { or < starts code, and a line that starts with "import " or "export " is code
    work = work.replace(/(?<!\\)([{}<])/g, '\\$1');
    work = work.replace(/^(import|export)(?=\s)/gm, (word) => `&#x${word.charCodeAt(0).toString(16)};${word.slice(1)}`);
    return putBack(work, kept);
  }

  // Split into fenced code (kept as it is) and everything else.
  const lines = page.text.replace(/\r\n?/g, '\n').split('\n');
  const parts = [];
  let fence = null;
  let run = [];
  const flush = (code) => {
    if (run.length) parts.push({ code, text: run.join('\n') });
    run = [];
  };
  for (const line of lines) {
    const mark = /^\s*(`{3,}|~{3,})(.*)$/.exec(line);
    if (fence === null && mark && !(mark[1][0] === '`' && mark[2].includes('`'))) {
      flush(false);
      fence = mark[1];
      run.push(line);
    } else if (fence !== null && mark && mark[1][0] === fence[0] && mark[1].length >= fence.length && mark[2].trim() === '') {
      run.push(line);
      flush(true);
      fence = null;
    } else {
      run.push(line);
    }
  }
  flush(fence !== null);

  // The first heading of the page is its title.
  let title = '';
  for (const part of parts) {
    if (part.code) continue;
    const heading = /^#[ \t]+(.+?)[ \t]*#*[ \t]*$/m.exec(part.text);
    if (heading) {
      title = plain(heading[1]);
      part.text = part.text.slice(0, heading.index) + part.text.slice(heading.index + heading[0].length);
    }
    break;
  }
  if (!title) {
    title = posix.basename(source, '.md').replace(/-/g, ' ');
    title = title[0].toUpperCase() + title.slice(1);
    warnings.push(`${source}: no "# Title" line at the top; the page is titled "${title}"`);
  }

  const body = parts
    .map((part) => (part.code ? part.text : inline(part.text)))
    .join('\n')
    .replace(/\n{3,}/g, '\n\n')
    .replace(/^\n+/, '')
    .trimEnd();

  const front = [
    '---',
    `# Made by website/wiki/scripts/guide.mjs from ${source} in ${repository}.`,
    "# Never edit this page: change the guide in the app's repository, then run `npm run guide`.",
    `title: ${JSON.stringify(title)}`,
  ];
  if (page.description) front.push(`description: ${JSON.stringify(page.description)}`);
  front.push('---', '');
  const lead = page.lead ? `${page.lead.trim()}\n\n` : '';
  return { mdx: `${front.join('\n')}\n${lead}${body}\n`, title, images, warnings };
}

/** Markdown marks taken off a short piece of text: "**The** `x`" → "The x" */
export function plain(text) {
  return text
    .replace(/!?\[((?:\\.|[^\]\\])*)\]\([^)]*\)/g, '$1')
    .replace(/(\*\*|__|\*|`)/g, '')
    .replace(/\\([\\`*_{}[\]()#+\-.!<>|])/g, '$1')
    .replace(/\s+/g, ' ')
    .trim();
}

/**
 * Reads the guide's README: the order of its pages, and each page's one-line description (the
 * text after its link, when there is some).
 *
 * Returns { order: [repository paths], descriptions: Map(path → text) }.
 */
export function readIndex(text, source, pages) {
  const order = [];
  const descriptions = new Map();
  // one list item is its first line and the indented lines after it
  const items = text.replace(/\r\n?/g, '\n').split(/\n(?=[ \t]*(?:[-*+]|\d+[.)])[ \t])/);
  for (const item of items) {
    const found = /^[ \t]*(?:[-*+]|\d+[.)])[ \t]+\[((?:\\.|[^\]\\])*)\]\(([^)\s]+)\)([\s\S]*)$/.exec(item);
    if (!found) continue;
    const target = found[2].replace(/[?#].*$/, '');
    if (/^[a-z][a-z0-9+.-]*:/i.test(target)) continue;
    const path = posix.normalize(posix.join(posix.dirname(source), target));
    if (!pages.has(path) || path === source || order.includes(path)) continue;
    order.push(path);
    let rest = plain(found[3].split(/\n[ \t]*\n/)[0]).replace(/^[:.–—-]+\s*/, '');
    if (rest) {
      rest = rest[0].toUpperCase() + rest.slice(1);
      if (!/[.!?]$/.test(rest)) rest += '.';
      descriptions.set(path, rest);
    }
  }
  return { order, descriptions };
}

/** The section's meta.json: the README first, then its pages in the README's order, then the rest by name. */
export function sectionMeta(app, pages, guideDir, order) {
  const index = [...pages].filter((path) => pagePath(path, guideDir) === 'index.mdx');
  const listed = order.filter((path) => !index.includes(path));
  const rest = [...pages].filter((path) => !index.includes(path) && !listed.includes(path)).sort();
  const names = [...index, ...listed, ...rest].map((path) => pagePath(path, guideDir).replace(/\.mdx$/, ''));
  // the kit's icon for the section: the app's own, or the brand its data file names until it has one
  return `${JSON.stringify({ title: app.name, icon: `brand:${app.brand ?? `wordsmith-${app.slug}`}`, root: true, pages: names }, null, 2)}\n`;
}
