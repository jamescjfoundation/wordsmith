#!/usr/bin/env python3
"""Writes the Wordsmith website's HTML pages. The header, the footer and all page text are here.

    python3 website/tools/build.py            rewrite the pages in website/
    python3 website/tools/build.py FOLDER     write them into FOLDER instead
    python3 website/tools/build.py --check    write them into a temporary folder, and fail when a
                                              page in website/ is not what this script writes
    python3 website/tools/build.py FOLDER --releases FILE
                                              take each app's latest release from FILE (the deploy
                                              does this, with what releases.py just read from GitHub)

What the pages say about an app's state comes from two places, never from words typed here:
website/data/apps/<app>.json (the app's name, what it is for, its platforms and the wording for
each state) and a releases file (the version, the date and the download links of the app's latest
public release). Without --releases that file is website/data/releases.json, the last known
answer, so this script never uses the network and --check gives the same result everywhere.
"""
import argparse, difflib, json, pathlib, re, shutil, sys, tempfile

import releases as rel

WEBSITE = pathlib.Path(__file__).resolve().parent.parent
ARGS = argparse.ArgumentParser(description="Write the website's pages.")
ARGS.add_argument("folder", nargs="?", help="write the pages here instead of website/")
ARGS.add_argument("--check", action="store_true", help="fail when a page in website/ is not what this script writes")
ARGS.add_argument("--releases", help="the releases file to build from (default: website/data/releases.json)")
ARGS = ARGS.parse_args()
CHECK = ARGS.check
if CHECK and (ARGS.folder or ARGS.releases):
    sys.exit("build.py: --check compares the pages in website/ with website/data/releases.json; it takes no folder and no --releases.")
if CHECK:
    OUT = pathlib.Path(tempfile.mkdtemp(prefix="wordsmith-pages-"))
else:
    OUT = pathlib.Path(ARGS.folder) if ARGS.folder else WEBSITE
APPS = {app["slug"]: app for app in rel.read_apps()}
PLATFORMS = {platform["id"]: platform for platform in rel.read_platforms()}
RELEASES = rel.read_kept(ARGS.releases or rel.KEPT)["apps"]
ORG = "https://github.com/jamescjfoundation"
FOUNDATION = "https://jamescj.org"
B = "assets/brand/"
IMG = "assets/img/"
SITE = "https://wordsmithand.ink/"

GH = '<svg viewBox="0 0 16 16" aria-hidden="true" fill="currentColor"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/></svg>'
ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
DOWN = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 5v14M6 13l6 6 6-6"/></svg>'

# Simple line icons drawn for this site (24 px grid). Not brand marks.
ICONS = {
    "keys": '<rect x="2.5" y="6" width="19" height="12" rx="2"/><path d="M6.5 10h.01M10 10h.01M14 10h.01M17.5 10h.01M7.5 14h9"/>',
    "page": '<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5M9 13h6M9 17h4"/>',
    "type": '<path d="M4 7V5h16v2M12 5v14M9 19h6"/>',
    "cards": '<rect x="3" y="4" width="8" height="7" rx="1.2"/><rect x="13" y="4" width="8" height="7" rx="1.2"/><rect x="3" y="13" width="8" height="7" rx="1.2"/><rect x="13" y="13" width="8" height="7" rx="1.2"/>',
    "flag": '<path d="M5 21V4M5 4h11l-2 4 2 4H5"/>',
    "chart": '<path d="M3 20h18M6 16v-5M11 16V6M16 16v-8"/>',
    "layers": '<path d="M12 3 3 8l9 5 9-5z"/><path d="m3 13 9 5 9-5"/>',
    "code": '<path d="m8 8-4 4 4 4M16 8l4 4-4 4M14 5l-4 14"/>',
    "terminal": '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="m7 9 3 3-3 3M13 15h4"/>',
    "list": '<path d="M9 6h11M9 12h11M9 18h11M4.5 6h.01M4.5 12h.01M4.5 18h.01"/>',
    "people": '<circle cx="9" cy="8" r="3.5"/><path d="M3 20c0-3.3 2.7-6 6-6s6 2.7 6 6M16 4.5a3.5 3.5 0 0 1 0 7M18 14c2 .7 3 2.8 3 6"/>',
    "history": '<path d="M3 12a9 9 0 1 0 3-6.7"/><path d="M3 4v5h5M12 8v4l3 2"/>',
    "target": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1"/>',
    "timeline": '<path d="M3 12h18M7 8v8M12 6v12M17 9v6"/>',
    "books": '<path d="M5 4h4v16H5zM11 4h4v16h-4zM17 5l3.5.9-3.2 13.6-3.4-.9"/>',
    "pen": '<path d="M4 20h4L19 9l-4-4L4 16z"/><path d="m13 7 4 4"/>',
    "import": '<path d="M12 3v12M7 10l5 5 5-5M5 21h14"/>',
    "letters": '<path d="m3 19 5-14 5 14M5 14h6"/><circle cx="17.5" cy="16.5" r="2.5"/><path d="M20 12v7"/>',
    "print": '<path d="M6 9V3h12v6M6 18H4a1 1 0 0 1-1-1v-6a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v6a1 1 0 0 1-1 1h-2"/><path d="M6 14h12v7H6z"/>',
    "tablet": '<rect x="5" y="2" width="14" height="20" rx="2"/><path d="M11 18h2"/>',
    "check": '<circle cx="12" cy="12" r="9"/><path d="m8 12 3 3 5-6"/>',
    "open-book": '<path d="M2 5h6a4 4 0 0 1 4 4v11a3 3 0 0 0-3-3H2zM22 5h-6a4 4 0 0 0-4 4v11a3 3 0 0 1 3-3h7z"/>',
    "copies": '<rect x="8" y="8" width="12" height="12" rx="2"/><path d="M16 8V6a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2v8a2 2 0 0 0 2 2h2"/>',
    "shield": '<path d="M12 3l8 3v6c0 4.5-3.4 8.3-8 9-4.6-.7-8-4.5-8-9V6z"/>',
    "refresh": '<path d="M20 11a8 8 0 1 0-2.3 5.7"/><path d="M20 4v7h-7"/>',
    "plus": '<path d="M12 5v14M5 12h14"/>',
    "heart": '<path d="M12 20s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.6-7 10-7 10z"/>',
    "eye-off": '<path d="m3 3 18 18M10.6 6.1A9.8 9.8 0 0 1 12 6c5 0 9 6 9 6a15 15 0 0 1-2.6 3.2M6.6 6.6C4.3 8.1 3 12 3 12s4 6 9 6c1.6 0 3-.4 4.3-1.1M9.9 9.9a3 3 0 0 0 4.2 4.2"/>',
    "folder": '<path d="M3 6a2 2 0 0 1 2-2h4l2 2h8a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>',
    "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/>',
    "star": '<path d="m12 3 2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1-4.4-4.3 6.1-.9z"/>',
    "chat": '<path d="M4 5h16v11H9l-5 4z"/>',
    "megaphone": '<path d="M3 11v2a1 1 0 0 0 1 1h3l6 4V6l-6 4H4a1 1 0 0 0-1 1zM17 9a4 4 0 0 1 0 6"/>',
}


def icon(name):
    return (f'<svg class="i" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>')


def features(items):
    """A grid of features: (icon, title, text)."""
    cells = "\n".join(f'          <div class="feature"><span class="ficon">{icon(i)}</span><h3>{t}</h3><p>{p}</p></div>'
                      for i, t, p in items)
    return f'<div class="features">\n{cells}\n        </div>'


def logo(name, alt, cls=""):
    """A logo that switches to its paper version in dark mode."""
    c = f' class="{cls}"' if cls else ""
    return (f'<picture><source srcset="{B}{name}-paper.svg" media="(prefers-color-scheme: dark)">'
            f'<img{c} src="{B}{name}-ink.svg" alt="{alt}"></picture>')


# The screenshots are drawn by the apps and carried here by website/wiki/scripts/guide.mjs, which
# records each one's size in its lock file. Which ones are carried: "screenshots" in data/apps/<app>.json.
SHOTS = {copy["file"].removeprefix("website/"): copy
         for entry in json.loads((WEBSITE / "wiki" / "guides.lock.json").read_text(encoding="utf-8"))["apps"].values()
         for image in entry["images"] for copy in image["copies"]}


def shot(app, name, alt, lazy=True):
    """An app's screenshot, with the size the carried file has."""
    file = f"{IMG}{app}-{name}.webp"
    if file not in SHOTS:
        sys.exit(f'build.py: no screenshot {file}. Name "{name}" under "screenshots" in website/data/apps/{app}.json '
                 "and run `npm run guide` in website/wiki.")
    size = SHOTS[file]
    return (f'<img src="{file}" alt="{alt}" width="{size["width"]}" height="{size["height"]}"'
            f'{' loading="lazy"' if lazy else ""}>')


# ---------------------------------------------------------------- An app's state, from the data files
def repo(slug):
    return f"https://github.com/{APPS[slug]['repository']}"


def state(slug):
    """The app's words for where it stands: "chip", "line" and "download", with the version and date filled in."""
    return rel.state_words(APPS[slug], RELEASES.get(slug))


def chip(slug):
    """The small label beside an app's name: its version once it has a release, nothing before."""
    words = state(slug)["chip"]
    kind = "pre" if rel.state_of(RELEASES.get(slug)) == "preview" else "ok"
    return f'<span class="chip {kind}">{words}</span>' if words else ""


def systems(slug, last=" and "):
    names = [PLATFORMS[platform]["name"] for platform in APPS[slug]["platforms"]]
    return ", ".join(names[:-1]) + last + names[-1]


def download(slug, sunken=False):
    """The download area of an app's page.

    Before the app has a release: its systems, each with a link to the releases page. Once it has
    one: the release's files for each system. The words above them are the app's own, from its
    data file.
    """
    app, release = APPS[slug], RELEASES.get(slug)
    cards = []
    for platform in (PLATFORMS[one] for one in app["platforms"]):
        files = rel.files_for(release, platform)
        if files:
            links = "".join(f'<a class="btn btn-primary" href="{file["url"]}">{DOWN} Download</a>'
                            f'<p class="dl-file">{file["name"]} &middot; {rel.size_words(file["size"])}</p>' for file in files)
        elif release:
            links = (f'<a class="btn btn-ghost" href="{release["url"]}">Open the release {ARROW}</a>'
                     f'<p class="dl-file">Version {release["version"]} has no file for this system.</p>')
        else:
            links = f'<a class="btn btn-ghost" href="{repo(slug)}/releases">Releases page {ARROW}</a>'
        cards.append(f'          <div class="dl"><h3>{platform["name"]}</h3><p class="dl-for">{platform["detail"]}</p>{links}</div>')
    sums = " and their checksums" if release and rel.has_checksums(release) else ""
    all_files = (f'<a href="{release["url"]}">Every file of version {release["version"]}{sums}</a>' if release
                 else f'<a href="{repo(slug)}/releases">{app["name"]} releases on GitHub</a>')
    return f"""
    <section class="section{' sunken' if sunken else ''}" id="download">
      <div class="wrap">
        <div class="section-head">
          <p class="eyebrow">Download</p>
          <h2>Get {app["name"]}.</h2>
          <p class="lede">{state(slug)["download"]}</p>
        </div>
        <div class="downloads">
{chr(10).join(cards)}
        </div>
        <div class="dl-notes">
          <div>
            <h3>The first time you open it</h3>
            <p>The apps are not signed with a paid developer certificate, so macOS and Windows ask before they
              open one for the first time.</p>
            <ul>
              <li><b>macOS:</b> open the app once and close the notice. Then open System Settings, choose
                Privacy &amp; Security, and click Open Anyway.</li>
              <li><b>Windows:</b> on the &ldquo;Windows protected your PC&rdquo; notice, click More info, then Run anyway.</li>
            </ul>
            <p><a href="wiki/start/install">Installing, step by step</a></p>
          </div>
          <div>
            <h3>Free, and yours to check</h3>
            <p>{app["name"]} costs nothing and needs no account. Downloads come only from the app's own
              releases on GitHub. {all_files}.</p>
            <p>The code is open source. To build the app yourself, follow the
              <a href="{repo(slug)}#readme">README in its repository</a>.</p>
          </div>
        </div>
      </div>
    </section>"""


NAV = [[("script", "Script", "n-script"), ("manuscript", "Manuscript", "n-manuscript"), ("book", "Book", "n-book")],
       [("launcher", "Launcher", ""), ("wiki/", "Wiki", ""), ("open-source", "Open source", ""), ("about", "About", "")]]


def page(file, title, desc, body, cls=""):
    # Pages are written as name.html, but links leave off ".html" (GitHub Pages serves /name from name.html).
    groups = []
    for g in NAV:
        links = "".join(
            f'<a href="{h}"{f' class="{c}"' if c else ""}{' aria-current="page"' if h == file.removesuffix(".html") else ""}>{t}</a>' for h, t, c in g)
        groups.append(f'          <div class="nav-group">{links}</div>')
    nav = "\n".join(groups)
    full_title = title if file == "index.html" else f"{title} · Wordsmith"
    url = SITE if file == "index.html" else SITE + file.removesuffix(".html")
    canonical = "" if file == "404.html" else f'\n  <link rel="canonical" href="{url}">\n  <meta property="og:url" content="{url}">'
    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{full_title}</title>
  <meta name="description" content="{desc}">
  <meta property="og:title" content="{full_title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:type" content="website">
  <meta property="og:image" content="{SITE}{B}og-image.png">{canonical}
  <meta name="twitter:card" content="summary_large_image">
  <meta name="theme-color" content="#FAFAF7" media="(prefers-color-scheme: light)">
  <meta name="theme-color" content="#12162B" media="(prefers-color-scheme: dark)">
  <link rel="icon" href="favicon.svg" type="image/svg+xml">
  <link rel="apple-touch-icon" href="{B}wordsmith-and-ink-icon-512.png">
  <link rel="preload" href="assets/fonts/courier-prime-latin-700-normal.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="assets/fonts/inter-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="assets/css/site.css">
  <script>document.documentElement.classList.add("js")</script>
</head>
<body class="{cls}">
  <a class="skip" href="#main">Skip to content</a>
  <header class="site-header">
    <div class="header-inner">
      <a class="brand-link" href="./" aria-label="Wordsmith home">
        {logo("wordsmith-and-ink-wordmark", "Wordsmith &amp; Ink")}
      </a>
      <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav"><span class="bars" aria-hidden="true"></span>Menu</button>
      <nav class="nav" id="site-nav" aria-label="Main">
        <div class="nav-links">
{nav}
        </div>
        <div class="nav-actions">
          <a class="btn btn-ghost btn-sm" href="{ORG}">{GH} GitHub</a>
          <a class="btn btn-primary btn-sm" href="{FOUNDATION}">Foundation</a>
        </div>
      </nav>
    </div>
  </header>

  <main id="main">
{body}
  </main>

  <footer class="site-footer">
    <div class="wrap">
      <div class="foot-grid">
        <div class="foot-brand">
          <img src="{B}wordsmith-and-ink-wordmark-paper.svg" alt="Wordsmith &amp; Ink">
          <p>Free, open-source writing apps for screenwriters, novelists and authors. A project of
            <a href="{FOUNDATION}">The James C. J. Foundation</a>.</p>
          <div class="foot-icons">
            <a href="script" aria-label="Wordsmith Script"><img src="{B}wordsmith-script-icon.svg" alt="" width="36" height="36"></a>
            <a href="manuscript" aria-label="Wordsmith Manuscript"><img src="{B}wordsmith-manuscript-icon.svg" alt="" width="36" height="36"></a>
            <a href="book" aria-label="Wordsmith Book"><img src="{B}wordsmith-book-icon.svg" alt="" width="36" height="36"></a>
          </div>
        </div>
        <div>
          <h2>Apps</h2>
          <ul>
            <li><a href="script">Wordsmith Script</a></li>
            <li><a href="manuscript">Wordsmith Manuscript</a></li>
            <li><a href="book">Wordsmith Book</a></li>
            <li><a href="launcher">Wordsmith Launcher</a></li>
          </ul>
        </div>
        <div>
          <h2>Project</h2>
          <ul>
            <li><a href="wiki/">Wiki</a></li>
            <li><a href="about">About</a></li>
            <li><a href="open-source">Open source</a></li>
            <li><a href="open-source#releases">Releases and plans</a></li>
            <li><a href="open-source#get-involved">Get involved</a></li>
            <li><a href="open-source#privacy">Privacy</a></li>
          </ul>
        </div>
        <div>
          <h2>Elsewhere</h2>
          <ul>
            <li><a href="{ORG}">GitHub</a></li>
            <li><a href="{FOUNDATION}">The James C. J. Foundation</a></li>
          </ul>
        </div>
      </div>
      <div class="foot-legal">
        <span>The apps' code is open source under MIT or Apache-2.0. The words of this site are under <a href="{ORG}/wordsmith/blob/main/LICENSES.md">CC BY 4.0</a>. Wordsmith, Wordsmith &amp; Ink and the app names and logos are trademarks of The James C. J. Foundation.</span>
        <span>Set in Courier Prime and Inter.</span>
      </div>
    </div>
  </footer>
  <script src="assets/js/site.js" defer></script>
</body>
</html>
"""
    html = re.sub(r'<a ([^>]*?)href="(https?://[^"]+)"', lambda m: f'<a {m.group(1)}href="{m.group(2)}" target="_blank" rel="noopener"', html)
    if file == "404.html":
        # GitHub Pages serves this page at any missing address, even inside a folder (/foo/bar),
        # where relative links would point into that folder. Make its local links start at the site root.
        html = html.replace('href="./"', 'href="/"')
        html = re.sub(r'\b(href|src|srcset)="(?![#/]|[a-z]+:)', r'\1="/', html)
    (OUT / file).write_text(html, encoding="utf-8")


# ---------------------------------------------------------------- Shared illustrations
# A stack of three books, seen from the spine, one per app. Drawn here, not a logo.
BOOKS = """<svg class="books-art" viewBox="0 0 560 330" role="img" aria-label="A stack of three books: Script, Manuscript and Book">
  <defs>
    <pattern id="pages" width="6" height="4" patternUnits="userSpaceOnUse"><rect width="6" height="4" fill="#E9E4D6"/><rect y="3" width="6" height="1" fill="#C9C2B0"/></pattern>
  </defs>
  <ellipse cx="290" cy="306" rx="250" ry="12" fill="#0C0F1F"/>
  <g>
    <rect x="44" y="222" width="470" height="78" rx="8" fill="#1C2340" stroke="#3A4270" stroke-width="2"/>
    <rect x="490" y="230" width="18" height="62" fill="url(#pages)"/>
    <rect x="44" y="222" width="22" height="78" rx="6" fill="#2E9473"/>
    <rect x="400" y="222" width="10" height="78" fill="#2E9473"/>
    <text x="92" y="271" fill="#FAFAF7" font-family="Courier Prime, Courier, monospace" font-weight="700" font-size="28">Book</text>
  </g>
  <g transform="rotate(-2.2 280 180)">
    <rect x="86" y="140" width="400" height="80" rx="8" fill="#1C2340" stroke="#3A4270" stroke-width="2"/>
    <rect x="462" y="148" width="18" height="64" fill="url(#pages)"/>
    <rect x="86" y="140" width="22" height="80" rx="6" fill="#D24B3E"/>
    <rect x="380" y="140" width="10" height="80" fill="#D24B3E"/>
    <text x="134" y="190" fill="#FAFAF7" font-family="Courier Prime, Courier, monospace" font-weight="700" font-size="28">Manuscript</text>
  </g>
  <g transform="rotate(1.6 300 100)">
    <rect x="120" y="62" width="330" height="74" rx="8" fill="#1C2340" stroke="#3A4270" stroke-width="2"/>
    <rect x="426" y="70" width="18" height="58" fill="url(#pages)"/>
    <rect x="120" y="62" width="22" height="74" rx="6" fill="#B8862B"/>
    <rect x="350" y="62" width="10" height="74" fill="#B8862B"/>
    <text x="168" y="109" fill="#FAFAF7" font-family="Courier Prime, Courier, monospace" font-weight="700" font-size="28">Script</text>
  </g>
</svg>"""

# Where the apps' pictures come from: each app draws its own, from a public-domain text.
DRAWN = {
    "script": 'Pictures are drawn by the app from "Everybody\'s Girl" (1918), a public-domain photoplay.',
    "manuscript": ("Pictures are drawn by the app from the first chapters of <i>Pride and Prejudice</i> (1813), in the public domain. "
                   "The chapter titles, synopses and bible entries were written for the pictures."),
    "book": "Pictures are drawn by the app from <i>Gulliver's Travels</i> (1726), in the public domain.",
}

# The home page's "desk": one real screenshot of each app, laid over each other.
DESK = f"""<div class="desk" role="img" aria-label="Three screenshots: a screenplay page in Wordsmith Script, with Wordsmith Manuscript's corkboard and Wordsmith Book's print preview laid over it">
          <div class="desk-shot">{shot("script", "page-view", "", lazy=False)}</div>
          <div class="desk-inset desk-a"><img class="badge" src="{B}wordsmith-manuscript-icon.svg" alt="" width="40" height="40">{shot("manuscript", "corkboard", "", lazy=False)}</div>
          <div class="desk-inset desk-b"><img class="badge" src="{B}wordsmith-book-icon.svg" alt="" width="40" height="40">{shot("book", "print-preview", "", lazy=False)}</div>
          <img class="badge badge-shot" src="{B}wordsmith-script-icon.svg" alt="" width="40" height="40">
        </div>"""


def gallery(app, shots):
    """A grid of an app's screenshots: (name, alt, caption)."""
    figures = "\n".join(f'          <figure><div class="shot">{shot(app, name, alt)}</div><figcaption>{caption}</figcaption></figure>'
                        for name, alt, caption in shots)
    return f'<div class="gallery">\n{figures}\n        </div>'


# ---------------------------------------------------------------- Home
def app_row(slug, text, ticks, visual):
    items = "".join(f"<li>{t}</li>" for t in ticks)
    name = slug.capitalize()
    return f"""
        <article class="app-row p-{slug}">
          <div class="app-copy">
            <div class="app-head"><img src="{B}wordsmith-{slug}-icon.svg" alt="" width="64" height="64">{chip(slug)}</div>
            {logo(f"wordsmith-{slug}-wordmark", f"Wordsmith {name}", "wordmark")}
            <p class="app-for">{APPS[slug]["for"]}</p>
            <p class="app-text">{text}</p>
            <ul class="ticks">{items}</ul>
            <a class="btn btn-ghost" href="{slug}">Explore {name} {ARROW}</a>
          </div>
          <div class="app-visual stage">
            {visual}
          </div>
        </article>"""


home = f"""
    <section class="hero">
      <div class="wrap hero-grid">
        <div class="hero-copy">
          <p class="kicker"><span>Free and open source, for {systems("script")}</span></p>
          <h1>Free writing tools, from first page to finished book.</h1>
          <p class="lede">A family of open-source apps for screenwriters, novelists and authors. Write a screenplay,
            draft a novel, and turn it into a print book and an ebook.</p>
          <div class="actions">
            <a class="btn btn-primary" href="#apps">Meet the apps {DOWN}</a>
            <a class="btn btn-ghost" href="wiki/">Read the guides</a>
          </div>
          <ul class="hero-apps" aria-label="The Wordsmith apps">
            <li><a href="script" class="n-script"><img src="{B}wordsmith-script-icon.svg" alt="" width="48" height="48"><span><b>Script</b><small>Screenplays</small></span></a></li>
            <li><a href="manuscript" class="n-manuscript"><img src="{B}wordsmith-manuscript-icon.svg" alt="" width="48" height="48"><span><b>Manuscript</b><small>Novels</small></span></a></li>
            <li><a href="book" class="n-book"><img src="{B}wordsmith-book-icon.svg" alt="" width="48" height="48"><span><b>Book</b><small>Print and ebook</small></span></a></li>
          </ul>
        </div>
        {DESK}
      </div>
    </section>

    <section class="promises" aria-label="What we promise">
      <div class="wrap">
        <ul class="promise-list">
          <li>{icon("heart")}<div><b>Free, for good</b><span>No price, no subscription, no premium tier.</span></div></li>
          <li>{icon("folder")}<div><b>Your files are yours</b><span>Plain, open files on your own computer.</span></div></li>
          <li>{icon("eye-off")}<div><b>No tracking</b><span>No accounts, no telemetry, no ads.</span></div></li>
          <li>{icon("code")}<div><b>Open source</b><span>Anyone can read, fix and translate the code.</span></div></li>
        </ul>
      </div>
    </section>

    <section class="section" id="apps">
      <div class="wrap">
        <div class="section-head center">
          <p class="eyebrow">The apps</p>
          <h2>One family, three desks.</h2>
          <p class="lede">Each app does one job well, and they work together. All three run on {systems("script")},
            and keep your work as plain files on your own computer.</p>
        </div>
        <div class="app-rows">{app_row("script",
        "Write screenplays, TV episodes and stage plays, formatted as you type and ready for production.",
        ["Return and Tab do the formatting", "Pages, PDFs and printouts that match the screen", "Revision colors, scene numbers and locked pages"],
        f'<div class="shot">{shot("script", "index-cards", "Wordsmith Script showing index cards, one per scene")}</div>')}
{app_row("manuscript",
        "Plan, draft and revise novels and other long work, with your story bible beside the text.",
        ["Parts, chapters and scenes in one binder", "A corkboard, an outline and a story bible", "Drafts and snapshots you can compare"],
        f'<div class="shot">{shot("manuscript", "corkboard", "Wordsmith Manuscript showing the corkboard, one card per chapter with its synopsis")}</div>')}
{app_row("book",
        "Design and typeset a finished manuscript as a print-ready book and an ebook for the stores.",
        ["Thirteen book designs, or your own", "A print-ready PDF and an accessible EPUB, every word checked", "Preflight before you export"],
        f'<div class="shot">{shot("book", "print-preview", "Wordsmith Book showing a chapter and its print pages as spreads")}</div>')}
        </div>
      </div>
    </section>

    <section class="section sunken">
      <div class="wrap">
        <div class="section-head center">
          <p class="eyebrow">How it works</p>
          <h2>Write <span class="arr">&rarr;</span> Finish <span class="arr">&rarr;</span> Publish.</h2>
          <p class="lede">One shared foundation means the apps look alike, work alike and pass your work along without
            copying and pasting.</p>
        </div>
        <ol class="flow">
          <li><a class="step n-script" href="script"><span class="step-num">1</span><img src="{B}wordsmith-script-icon.svg" alt="" width="72" height="72"><h3>Script</h3><p>Write the screenplay, and keep it in your novel's project too.</p></a></li>
          <li><a class="step n-manuscript" href="manuscript"><span class="step-num">2</span><img src="{B}wordsmith-manuscript-icon.svg" alt="" width="72" height="72"><h3>Manuscript</h3><p>Draft and revise the story, with characters and places in one bible.</p></a></li>
          <li><a class="step n-book" href="book"><span class="step-num">3</span><img src="{B}wordsmith-book-icon.svg" alt="" width="72" height="72"><h3>Book</h3><p>Turn the finished manuscript into a print book and an ebook.</p></a></li>
        </ol>
        <p class="flow-note">The <a href="launcher">Wordsmith Launcher</a>, which is planned, will bring all three together in one download.</p>
      </div>
    </section>

    <section class="section band">
      <div class="wrap split">
        <div>
          <p class="eyebrow">The Foundation</p>
          <h2>For writers, in James&rsquo; name.</h2>
          <p class="lede">The James C. J. Foundation is building free, open tools to support writers and their work.
            Wordsmith is the first of them.</p>
          <div class="actions">
            <a class="btn btn-primary" href="{FOUNDATION}">Visit the Foundation</a>
            <a class="btn btn-ghost" href="about">About the project</a>
          </div>
        </div>
        <div>{BOOKS}</div>
      </div>
    </section>

    <section class="section">
      <div class="wrap">
        <div class="cta-panel">
          <div class="cta-copy">
            <p class="eyebrow">Open source</p>
            <h2>Built in the open. Come and help.</h2>
            <p class="lede">Every line is public: the code, the plans and the decisions. If you write, code, design
              or translate, there's a place for you.</p>
            <div class="actions">
              <a class="btn btn-primary" href="open-source#get-involved">Get involved</a>
              <a class="btn btn-ghost" href="{ORG}">{GH} jamescjfoundation on GitHub</a>
            </div>
          </div>
          <ul class="ticks boxed">
            <li>Write something real in an app, and report what gets in your way</li>
            <li>Fix a page of a guide: every wiki page links to its source</li>
            <li>Translate: Manuscript and Book already come in English and Spanish</li>
            <li>Write code: the apps are in Rust, on one shared base</li>
          </ul>
        </div>
      </div>
    </section>
"""

# ---------------------------------------------------------------- About
about = f"""
    <section class="p-hero">
      <div class="wrap split">
        <div>
          <p class="eyebrow">About</p>
          <h1>Built for writers, in James&rsquo; name.</h1>
          <p class="lede">Wordsmith is made by Wordsmith &amp; Ink, a project of
            <a href="{FOUNDATION}">The James C. J. Foundation</a>. Its goal is simple: give creatives the tools they need
            to create, free, on any computer, for good.</p>
        </div>
        <div class="about-mark">{logo("wordsmith-and-ink-foundation", "Wordsmith &amp; Ink, a project of The James C. J. Foundation")}</div>
      </div>
    </section>

    <section class="section">
      <div class="wrap split top">
        <div>
          <p class="eyebrow">James</p>
          <h2>A writer with a world of stories.</h2>
        </div>
        <div class="prose">
          <p class="big">James C. J. wrote novels, plays, screenplays, TV pilots, songs and poems, and built whole worlds behind them.
            The James C. J. Foundation keeps his work alive and is being built to support emerging writers in his name.</p>
          <p class="muted">Wordsmith is one way the Foundation does that. Writing software is often expensive, closed, or
            tied to one kind of computer. These apps are none of those things, and because they're open source, they can't
            be taken away.</p>
          <div class="actions"><a class="btn btn-primary" href="{FOUNDATION}">Visit jamescj.org</a></div>
        </div>
      </div>
    </section>

    <section class="section sunken">
      <div class="wrap">
        <div class="section-head">
          <p class="eyebrow">What we believe</p>
          <h2>Tools that belong to the writer.</h2>
        </div>
        <div class="principles">
          <div><span class="ficon">{icon("heart")}</span><span class="num">01</span><h3>Free, for good</h3><p>No price, no subscription, no premium tier. Every feature is for every writer.</p></div>
          <div><span class="ficon">{icon("folder")}</span><span class="num">02</span><h3>Your files are yours</h3><p>Plain, open file formats you can read in any text editor, saved on your own computer.</p></div>
          <div><span class="ficon">{icon("eye-off")}</span><span class="num">03</span><h3>No tracking</h3><p>No accounts, no telemetry, no ads. Your words never leave your computer unless you send them.</p></div>
          <div><span class="ficon">{icon("code")}</span><span class="num">04</span><h3>Open source</h3><p>Anyone can read the code, fix it, translate it and help decide where it goes next.</p></div>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="wrap split">
        <div>
          <p class="eyebrow">Wordsmith &amp; Ink</p>
          <h2>The house behind the apps.</h2>
          <p class="muted">Wordsmith &amp; Ink is the name the Foundation makes its writing tools under. Each app types its
            own name in Courier Prime with a cursor of its own: a brass bar for Script, a stack of pages for Manuscript, a
            ribbon bookmark for Book. The house itself is one color, ink on paper, with a drop of ink falling from its
            cursor.</p>
          <div class="actions"><a class="btn btn-ghost" href="open-source">How the project works</a></div>
        </div>
        <div class="stage family">{logo("wordsmith-and-ink-family", "Wordsmith &amp; Ink and its three apps: Script, Manuscript and Book")}</div>
      </div>
    </section>
"""


# ---------------------------------------------------------------- App page parts
def hero_meta(slug):
    """Under an app's first buttons: its version once it has one, its systems, and its state's one line."""
    return f'{chip(slug)}<span>{systems(slug, ", ")}</span><span>{state(slug)["line"]}</span>'


def app_hero(slug, h1, lede, picture, alt, caption):
    """The top of an app's page: its name, what it is, the download and guide buttons, and one screenshot."""
    name = APPS[slug]["name"]
    return f"""
    <section class="p-hero app-hero">
      <div class="wrap">
        <div class="app-hero-copy">
          <div class="app-id">
            <img class="icon" src="{B}wordsmith-{slug}-icon.svg" alt="" width="72" height="72">
            <div>
              {logo(f"wordsmith-{slug}-wordmark", name, "wordmark")}
              <p class="endorse">a Wordsmith &amp; Ink app</p>
            </div>
          </div>
          <h1>{h1}</h1>
          <p class="lede">{lede}</p>
          <div class="actions">
            <a class="btn btn-primary" href="#download">{DOWN} Download</a>
            <a class="btn btn-ghost" href="wiki/{slug}/">Read the guide</a>
          </div>
          <div class="meta">{hero_meta(slug)}</div>
        </div>
        <figure class="visual">
          <div class="stage"><div class="shot">{shot(slug, picture, alt, lazy=False)}</div></div>
          <figcaption>{caption} {DRAWN[slug]}</figcaption>
        </figure>
      </div>
    </section>"""


# ---------------------------------------------------------------- Script
script = app_hero(
    "script", "Write the screenplay. The page takes care of itself.",
    """A free, open-source screenwriting app. Type with two keys doing the formatting, see every page
          as it will print, and take the script into production with revision colors, locked pages and scene numbers.""",
    "page-view", "Wordsmith Script showing a screenplay page, the list of scenes on the left and the scene inspector on the right",
    "The page view, with the scenes on the left and the scene at the caret on the right.",
) + f"""

    <section class="section sunken">
      <div class="wrap">
        <div class="section-head">
          <p class="eyebrow">What it does</p>
          <h2>Everything a script needs, from first draft to shooting script.</h2>
        </div>
        {features([
    ("keys", "Formatting on two keys", "Return and Tab move between scene headings, action, characters, parentheticals, dialogue and transitions. The status bar always says what comes next."),
    ("page", "Industry pages", "Courier Prime on standard margins, with (MORE) and (CONT'D), scene continueds, a title page, and PDFs and printouts that match the screen."),
    ("type", "Autocomplete that waits", "Character names, places and times offered as you type, never typed for you. Spelling, find and replace, and notes on any text."),
    ("cards", "Structure", "Index cards and a scene view that reorder the script, story boards of beats, an outline in lanes, scene colors and a structure strip."),
    ("flag", "Production", "Revision mode on the standard color cycle with margin marks, scene numbers with A-scenes and omitted scenes, locked pages, tracked changes and revised-pages-only printing."),
    ("chart", "Reports", "Scenes, locations, cast and single characters, scene lengths in eighths, a representation report, and writing statistics with goals and a sprint timer."),
    ("layers", "Templates", "Screenplays, TV episodes, sitcoms, stage plays and audio dramas, your own templates, and dual dialogue when two people talk at once."),
    ("code", "Open files", "A plain-text native format that reads well in version control. Fountain both ways, import from text, RTF and PDF, export to PDF, RTF, text, HTML and CSV."),
    ("terminal", "Command line", "Convert, export and report from a terminal or a build script, and let tools you choose drive the app."),
])}
      </div>
    </section>

    <section class="section">
      <div class="wrap">
        <div class="section-head">
          <p class="eyebrow">A closer look</p>
          <h2>Plan it, write it, shoot it.</h2>
        </div>
        {gallery("script", [
    ("index-cards", "Index cards, one per scene, with scene summaries", "Index cards: drag a card and the scene moves in the script."),
    ("story-board", "The story board with beats arranged in acts", "The story board: plan beats before you write them."),
    ("ribbon-production", "The Production tab with revision tools", "Production: revisions, scene numbers and locked pages."),
    ("draft-view-dark", "The draft view in the dark theme", "The draft view, in the dark theme."),
])}
      </div>
    </section>

    <section class="section sunken">
      <div class="wrap split">
        <div>
          <p class="eyebrow">Familiar from day one</p>
          <h2>Works the way screenwriters already work.</h2>
          <p class="muted">Wordsmith Script follows the conventions the industry has used for decades, so the pages
            look the way readers and crews expect. The ribbon is named for screenplay work: Write, Insert, Plan,
            Production, Review and View.</p>
        </div>
        <ul class="ticks boxed">
          <li>Plain-text scripts you can read, back up and compare anywhere</li>
          <li>Auto-save and timestamped backups, every file saved safely</li>
          <li>No telemetry. The only request it makes is an update check you can turn off</li>
          <li>Screen readers supported through the system's accessibility tools</li>
          <li>MIT or Apache-2.0 licensed: free to use, study and improve</li>
        </ul>
      </div>
    </section>
{download("script")}
"""

# ---------------------------------------------------------------- Manuscript
manuscript = app_hero(
    "manuscript", "The whole novel, in one place.",
    """A free, open-source app for writing novels and other long work. Plan on a corkboard, draft in a
          binder of chapters and scenes, keep your story bible beside the text, and hand the finished manuscript to
          Wordsmith Book.""",
    "editor", "Wordsmith Manuscript showing a scene's text, the binder of chapters and scenes on the left and the inspector on the right",
    "The editor, with the binder on the left and the scene's synopsis, label, status and bible entries on the right.",
) + f"""

    <section class="section sunken">
      <div class="wrap">
        <div class="section-head">
          <p class="eyebrow">What it does</p>
          <h2>Plan it, write it, revise it, finish it.</h2>
        </div>
        {features([
    ("list", "The binder", "Parts, chapters and scenes in one tree, with research and notes beside them. Drag to reorder, and read a chapter, or the whole book, as one continuous text."),
    ("cards", "Corkboard and outline", "Index cards for every scene, a freeform board with lines between ideas, and an outline with your own columns."),
    ("people", "Story bible", "Characters, places and anything else, with your own entry types, relationships read from both sides, and suggested links from the names in a scene."),
    ("layers", "Drafts", "Keep the manuscript as it is and start a new draft. Compare drafts chapter by chapter and choose which one is exported."),
    ("history", "Snapshots", "Keep a scene as it is before a big change, compare it word by word later, and restore it in one click."),
    ("target", "Targets and history", "Word targets for the session and the book with a deadline, and a writing calendar kept on your computer, never in the project."),
    ("timeline", "Threads and timeline", "Lanes for plot threads or points of view, and a timeline of the story's own dates."),
    ("books", "Series", "Several books can share one story bible, so what you learn about a character in book one is there in book three."),
    ("pen", "Revision tools", "Split the editor, leave comments, mark revision passes in color, and turn on grammar hints that run on your own computer."),
])}
      </div>
    </section>

    <section class="section">
      <div class="wrap">
        <div class="section-head">
          <p class="eyebrow">A closer look</p>
          <h2>See the shape of the story.</h2>
          <p class="lede">Every scene is a card. Write a line on it, color it by label, and move it around until the
            story works. The text moves with it.</p>
        </div>
        {gallery("manuscript", [
    ("corkboard", "The corkboard: one card per chapter with its synopsis, label color and status", "The corkboard: one card per chapter, with its synopsis, label and status."),
    ("outline", "The outline: chapters and scenes with label, status, words, target, point of view and scene date", "The outline: sort it, edit it in place, add your own columns."),
    ("bible", "A character's sheet in the story bible", "The story bible: a character's sheet, beside the text."),
    ("stitched-dark", "The whole manuscript as one text, in the dark theme", "The whole manuscript read as one text, in the dark theme."),
])}
      </div>
    </section>

    <section class="section sunken">
      <div class="wrap split">
        <div>
          <p class="eyebrow">Your words, safe</p>
          <h2>Bring everything in. Lose nothing.</h2>
          <p class="muted">Import from Word, OpenDocument, RTF, Markdown, web pages, EPUB and plain text, an outline,
            or a whole folder of documents at once. Chapters and scene breaks are found for you, and every import is
            checked word for word against the source. If a single word doesn't match, the import isn't made.</p>
        </div>
        <ul class="ticks boxed">
          <li>A project is a folder of plain text files, readable in any text editor</li>
          <li>One file per scene, so version control and synced folders work well</li>
          <li>Export a standard manuscript for agents and editors, as DOCX or PDF</li>
          <li>Export to Word, OpenDocument, RTF, Markdown, HTML and EPUB, each one checked</li>
          <li>Hand the book to Wordsmith Book as one package, ready to typeset</li>
          <li>Keep Wordsmith Script screenplays inside the same project</li>
          <li>The interface comes in English and Spanish</li>
        </ul>
      </div>
    </section>

    <section class="section">
      <div class="wrap">
        <div class="callout p-book">
          <img src="{B}wordsmith-book-icon.svg" alt="" width="64" height="64">
          <div><h3>Finished? Make it a book.</h3><p>Wordsmith Book opens your Manuscript project directly and typesets it for print and ebook. If it spots a typo, it offers the fix back instead of changing your words.</p></div>
          <a class="btn btn-ghost" href="book">About Book {ARROW}</a>
        </div>
      </div>
    </section>
{download("manuscript", sunken=True)}
"""

# ---------------------------------------------------------------- Book
book = app_hero(
    "book", "From manuscript to a book you'd be proud to sell.",
    """A free, open-source app for designing and typesetting books. Bring a finished manuscript, choose
          a design, set the trim size and the front and back matter, and export a print-ready PDF and an accessible
          ebook, with every word checked against your source.""",
    "print-preview", "Wordsmith Book showing a chapter's text, the book's outline on the left and its print pages as spreads on the right",
    "A chapter open from the Outline, with its print pages as spreads in the Print Preview.",
) + f"""

    <section class="section sunken">
      <div class="wrap">
        <div class="section-head">
          <p class="eyebrow">What it does</p>
          <h2>Beautiful by default. Ready to print and to sell.</h2>
          <p class="lede">For independent authors and small presses: a typeset book and a clean ebook from the same
            manuscript, without learning typesetting.</p>
        </div>
        {features([
    ("import", "Bring the manuscript", "Link a Wordsmith Manuscript project, which Book reads and never changes, or import Word, OpenDocument, RTF, Markdown, plain text or EPUB. Chapters, parts and scene breaks are found for you, and you review them first."),
    ("letters", "Book designs", "Thirteen designs, from Classic and Literary to Fantasy, Poetry and Large Print, each previewed with your own first chapter. Mix parts of two designs, save your own, and share it as a file."),
    ("page", "Front and back matter", "A half title, title page, copyright page and contents made from your book's details, and a dedication, epigraph, about the author, \"also by\" and more, each put where convention has it."),
    ("print", "Print-ready PDF", "Eighteen trim sizes, mirrored margins with a gutter that grows with the page count, paperback and hardcover profiles, bleed, footnotes on the page, and a large-print edition of any design."),
    ("tablet", "Ebooks", "EPUB 3.3 with a table of contents, accessibility metadata and alternative text for pictures, embedded fonts where their licenses allow, pop-up notes and the print edition's page numbers."),
    ("check", "Preflight", "Builds an edition and reads the file back: page size and margins, embedded fonts, picture resolution, the cover, ISBNs and every word against the source. Each finding links to its page or setting."),
    ("open-book", "Cover template", "The full-wrap cover template for your page count and paper, with the spine, bleed, safe areas and barcode area marked, and a check of the cover you bring."),
    ("copies", "Editions", "A paperback, a hardcover, a large-print edition and an ebook from one book, each with its own ISBN. Add an ebook edition per store, each carrying only its own links."),
    ("shield", "Your words, untouched", "Typographic cleanup (curly quotes, dashes, ellipses) is shown change by change and can be undone. A fix to a linked manuscript is offered back to the writer, never written into it."),
])}
      </div>
    </section>

    <section class="section">
      <div class="wrap">
        <div class="section-head">
          <p class="eyebrow">A closer look</p>
          <h2>Choose, preview, check, export.</h2>
        </div>
        {gallery("book", [
    ("designs", "The design chooser: genres and moods, and a sample chapter opening for each design", "The design chooser: filter by genre and mood, and see each design on your own chapter."),
    ("ebook", "The Ebook Preview on a phone, with the chapter's opening in small capitals", "The ebook preview: a phone, an e-ink reader or a tablet."),
    ("preflight", "Preflight on the paperback: nothing blocks export, and each note has a button to its page or setting", "Preflight: what blocks export, what to look at, and where."),
    ("details", "Details: the book's metadata, what it still needs and its editions with their ISBNs", "Details: the book's metadata, what a store would miss, and the editions."),
])}
      </div>
    </section>

    <section class="section sunken">
      <div class="wrap split">
        <div>
          <p class="eyebrow">For a small press too</p>
          <h2>One author or a whole catalogue.</h2>
          <p class="muted">A press keeps its imprints, its series and the ISBNs it owns in one house file. An imprint
            or a series can lock its design, so every book matches, and builds run from the command line, the same
            way every time.</p>
        </div>
        <ul class="ticks boxed">
          <li>Title and copyright pages from the imprint, with its logo and wording</li>
          <li>A series line, an "Also by" list in order, and box sets with one contents</li>
          <li>Each ISBN checked and given once, and an ONIX 3.0 record for distributors</li>
          <li>The same project gives the same files, byte for byte, every time</li>
          <li>A command line that builds, checks and verifies without the window</li>
          <li>The interface comes in English and Spanish</li>
        </ul>
      </div>
    </section>
{download("book")}
"""

# ---------------------------------------------------------------- Launcher
launcher = f"""
    <section class="p-hero app-hero">
      <div class="wrap split">
        <div>
          <div class="app-id">
            <img class="icon" src="{B}wordsmith-and-ink-icon.svg" alt="" width="72" height="72">
            <div><p class="eyebrow flat">Wordsmith Launcher</p></div>
          </div>
          <h1>One download for the whole desk.</h1>
          <p class="lede">The Wordsmith Launcher is planned, and not started. It will be the front door to the suite: a
            small app that installs the Wordsmith apps you want, keeps them up to date, and opens your recent work
            from any of them.</p>
          <div class="meta"><span class="chip planned">Planned</span><span>Not started</span><span>Until it exists, each app is its own download</span></div>
        </div>
        <figure class="launch">
          <div class="mock" role="img" aria-label="Sketch of the planned launcher: the three apps with their status, and a list of recent projects">
            <div class="mock-bar"><i></i><i></i><i></i><span class="title">Wordsmith</span></div>
            <div class="mock-body">
              <div class="launch-apps">
                <div><img src="{B}wordsmith-script-icon.svg" alt="">Script<small>Up to date</small></div>
                <div><img src="{B}wordsmith-manuscript-icon.svg" alt="">Manuscript<small>Update ready</small></div>
                <div><img src="{B}wordsmith-book-icon.svg" alt="">Book<small>Install</small></div>
              </div>
              <div class="launch-recent">
                <h4>Recent</h4>
                <div class="r"><img src="{B}wordsmith-manuscript-icon.svg" alt=""><span>Little Women</span><small>Today</small></div>
                <div class="r"><img src="{B}wordsmith-script-icon.svg" alt=""><span>Everybody's Girl</span><small>Yesterday</small></div>
                <div class="r"><img src="{B}wordsmith-book-icon.svg" alt=""><span>Pride and Prejudice</span><small>Last week</small></div>
              </div>
            </div>
          </div>
          <figcaption>A sketch of the idea, not a design. Nothing of the launcher is built yet.</figcaption>
        </figure>
      </div>
    </section>

    <section class="section sunken">
      <div class="wrap">
        <div class="section-head">
          <p class="eyebrow">The plan</p>
          <h2>What the launcher will be for.</h2>
        </div>
        {features([
    ("import", "Install what you need", "Pick the apps you want. A screenwriter may only need Script; a novelist may want Manuscript and Book."),
    ("refresh", "Stay up to date", "One place to see and install updates, downloaded only from the project's official releases and checked before they run."),
    ("folder", "All your work", "Recent screenplays, novels and books in one list, each opened in the right app."),
    ("plus", "Start something new", "Choose a screenplay, a stage play, a novel or a book, and the right app opens with the right template."),
    ("open-book", "Learn the tools", "Guides and getting-started help for every app, in one place."),
    ("shield", "Same promises", "No account, no tracking. Update checks can be turned off."),
])}
      </div>
    </section>

    <section class="section">
      <div class="wrap">
        <div class="callout">
          <img src="{B}wordsmith-and-ink-icon.svg" alt="" width="64" height="64">
          <div><h3>Have ideas for the launcher?</h3><p>It hasn't been built yet, so now is the best time to shape it. Its plan is an open issue: tell us there what would help you.</p></div>
          <a class="btn btn-ghost" href="{ORG}/wordsmith/issues/10">{GH} The plan on GitHub</a>
        </div>
      </div>
    </section>
"""


# ---------------------------------------------------------------- Open source
def status_rows():
    """One row per app: its latest release, from the releases file, or a link to where releases appear."""
    rows = []
    for slug, app in APPS.items():
        release = RELEASES.get(slug)
        latest = (f'<a href="{release["url"]}">{release["version"]}</a>, {rel.long_date(release["date"])}' if release
                  else f'<a href="{repo(slug)}/releases">Releases page</a>')
        name = app["repository"].split("/")[1]
        rows.append(f'              <tr class="p-{slug}"><td><img src="{B}wordsmith-{slug}-icon.svg" alt="" width="28" height="28">{app["name"]}</td>'
                    f'<td>{latest}</td><td>{app["for"]}</td><td><a href="{repo(slug)}">{name}</a></td></tr>')
    return "\n".join(rows)


opensource = f"""
    <section class="p-hero">
      <div class="wrap">
        <p class="eyebrow">Open source</p>
        <h1>Built in the open, for every writer.</h1>
        <p class="lede">Every line of Wordsmith is public: the code, the plans and the decisions. Here is where each
          app's releases are, where its plans are kept, and how you can help.</p>
      </div>
    </section>

    <section class="section" id="releases">
      <div class="wrap">
        <div class="section-head">
          <p class="eyebrow">Where things stand</p>
          <h2>Releases and plans.</h2>
          <p class="lede">Each app is released from its own repository, and this page reads its latest release from
            there. What comes next is not written here: it is kept as issues, where anyone can read it and add to it.</p>
        </div>
        <div class="table-scroll">
          <table class="status">
            <thead><tr><th>App</th><th>Latest release</th><th>For</th><th>Code</th></tr></thead>
            <tbody>
{status_rows()}
              <tr><td><img src="{B}wordsmith-and-ink-icon.svg" alt="" width="28" height="28">Wordsmith Launcher</td><td><span class="chip planned">Planned</span></td><td>Installing and opening the apps</td><td class="muted">Not started</td></tr>
              <tr><td><span class="core-dot" aria-hidden="true"></span>open-source-core</td><td><a href="{ORG}/open-source-core/releases">Releases page</a></td><td>The shared base every app is built on</td><td><a href="{ORG}/open-source-core">open-source-core</a></td></tr>
            </tbody>
          </table>
        </div>
        <p class="after-table">What is planned: the open issues of
          <a href="{repo("script")}/issues">Script</a>, <a href="{repo("manuscript")}/issues">Manuscript</a> and
          <a href="{repo("book")}/issues">Book</a>, and for this website, the wiki and the launcher, the
          <a href="{ORG}/wordsmith/milestone/1">v1 milestone</a>. What changed in a release is in each repository's changelog.</p>
      </div>
    </section>

    <section class="section sunken" id="get-involved">
      <div class="wrap">
        <div class="section-head">
          <p class="eyebrow">Get involved</p>
          <h2>There's a place for you.</h2>
          <p class="lede">You don't need to write code to help. Everything happens in the open on GitHub.</p>
        </div>
        {features([
    ("star", "Watch and star", "Watch a repository to hear about its releases. Stars help other writers find the project."),
    ("chat", "Try it and tell us", "Write something real in an app, and open an issue for anything that gets in your way."),
    ("code", "Write code", "The apps are written in Rust. Each repository's contributing guide explains how changes are made and checked."),
    ("globe", "Translate", "Help bring the apps to writers in your language. Manuscript and Book already come in English and Spanish."),
    ("letters", "Design", "Book designs, templates and the guides all need people with an eye for detail."),
    ("megaphone", "Spread the word", "Tell a writer who could use free tools. That's how a community starts."),
])}
        <div class="actions"><a class="btn btn-primary" href="{ORG}">{GH} jamescjfoundation on GitHub</a></div>
      </div>
    </section>

    <section class="section">
      <div class="wrap split top">
        <div class="panel">
          <span class="ficon">{icon("heart")}</span>
          <p class="eyebrow">Standing on shoulders</p>
          <h2>Built on great open-source work.</h2>
          <p class="muted">The apps share one base, open-source-core, which is based on WordCraft by the ArtCraft team and
            uses craft-libs, egui, HarfRust, Vello and many other open-source projects. Every app credits what it uses in
            its README and NOTICE files, and fixes we make to those projects are offered back.</p>
        </div>
        <div class="panel" id="privacy">
          <span class="ficon">{icon("eye-off")}</span>
          <p class="eyebrow">Privacy</p>
          <h2>Your writing stays with you.</h2>
          <p class="muted">The apps have no accounts and send no telemetry: no usage reports, no crash reports. Your
            writing, notes and file names are never sent anywhere.</p>
          <p class="muted">One request leaves your computer by itself: the update check. When an app starts, it asks
            GitHub for the list of that app's releases. GitHub sees your IP address and the app's name and version,
            and nothing else. Turn it off in File &rsaquo; Preferences. An update is downloaded only when you choose
            to install it. <a href="wiki/start/privacy">Privacy, in full</a>.</p>
        </div>
      </div>
    </section>

    <section class="section sunken">
      <div class="wrap split top">
        <div>
          <p class="eyebrow">Licenses and names</p>
          <h2>Free to use, study and change.</h2>
        </div>
        <div class="prose">
          <p>The apps' code is licensed under the MIT license or the Apache License 2.0, at your option, and so is
            each app's guide, which the wiki shows. The fonts are under the SIL Open Font License.</p>
          <p>The words of this website and of the wiki's own pages are under the Creative Commons Attribution 4.0
            license. Copy them, translate them and build on them, and give credit to the Wordsmith contributors.
            <a href="{ORG}/wordsmith/blob/main/LICENSES.md">Which license covers what</a>.</p>
          <p class="muted">The names Wordsmith, Wordsmith &amp; Ink, Wordsmith Script, Wordsmith Manuscript, Wordsmith
            Book and Wordsmith Launcher, and their logos, are trademarks of The James C. J. Foundation, and the logo
            and icon files are not open source. You may use them unchanged to refer to the project, but not for forks
            or other products. <a href="{ORG}/wordsmith/blob/main/brand/LICENSE.md">Using the names and logos</a>.</p>
        </div>
      </div>
    </section>
"""

notfound = """
    <section class="section notfound">
      <div class="wrap">
        <div class="sheet" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i><i></i></div>
        <p class="eyebrow">Page not found</p>
        <h1>This page is still a blank sheet.</h1>
        <p class="lede">The page you were looking for isn't here.</p>
        <div class="actions"><a class="btn btn-primary" href="./">Back to the start</a><a class="btn btn-ghost" href="wiki/">Open the wiki</a></div>
      </div>
    </section>
"""

page("index.html", "Wordsmith: free, open-source writing apps",
     "Wordsmith is a family of free, open-source apps for screenwriters, novelists and authors, from The James C. J. Foundation.", home)
page("script.html", "Wordsmith Script", "A free, open-source screenwriting app for macOS, Windows and Linux.", script, "p-script")
page("manuscript.html", "Wordsmith Manuscript", "A free, open-source app for writing novels and other long work.", manuscript, "p-manuscript")
page("book.html", "Wordsmith Book", "A free, open-source app for designing and typesetting print books and ebooks.", book, "p-book")
page("launcher.html", "Wordsmith Launcher", "The planned Wordsmith Launcher: one download to install, update and open the Wordsmith apps.", launcher)
page("about.html", "About", "Wordsmith is made by Wordsmith & Ink, a project of The James C. J. Foundation, to give writers free, open tools.", about)
page("open-source.html", "Open source", "Wordsmith is an open-source project of The James C. J. Foundation. Read where each app's releases and plans are, and how to help.", opensource)
page("404.html", "Page not found", "This page could not be found.", notfound)

if CHECK:
    stale = 0
    names = sorted({p.name for p in OUT.glob("*.html")} | {p.name for p in WEBSITE.glob("*.html")})
    for name in names:
        built, kept = OUT / name, WEBSITE / name
        if not built.exists():
            print(f"website/{name}: build.py does not write this page. Delete it, or add it to build.py.")
        elif not kept.exists():
            print(f"website/{name}: build.py writes this page, and it is not in website/.")
        elif built.read_text(encoding="utf-8") != kept.read_text(encoding="utf-8"):
            sys.stdout.writelines(difflib.unified_diff(
                kept.read_text(encoding="utf-8").splitlines(keepends=True), built.read_text(encoding="utf-8").splitlines(keepends=True),
                f"website/{name}", f"website/{name} as build.py writes it", n=1))
        else:
            continue
        stale += 1
    shutil.rmtree(OUT)
    if stale:
        sys.exit(f"{stale} of {len(names)} pages in website/ differ from what build.py writes. "
                 "Run `python3 website/tools/build.py` and commit the pages; never edit a page by hand.")
    print(f"ok: the {len(names)} pages in website/ are what build.py writes")
else:
    print("ok")
