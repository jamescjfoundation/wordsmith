#!/usr/bin/env python3
"""Writes the Wordsmith website's HTML pages (python3 website/tools/build.py). Header and footer are shared here."""
import pathlib, re, sys

OUT = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parent.parent
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


def terminal(cmds):
    return (f'<div class="terminal"><div class="terminal-bar" aria-hidden="true"><i></i><i></i><i></i><span>Terminal</span></div>'
            f'<pre><code>{cmds}</code></pre></div>')


NAV = [[("script.html", "Script", "n-script"), ("manuscript.html", "Manuscript", "n-manuscript"), ("book.html", "Book", "n-book")],
       [("launcher.html", "Launcher", ""), ("wiki/", "Wiki", ""), ("open-source.html", "Open source", ""), ("about.html", "About", "")]]


def page(file, title, desc, body, cls=""):
    groups = []
    for g in NAV:
        links = "".join(
            f'<a href="{h}"{f' class="{c}"' if c else ""}{' aria-current="page"' if h == file else ""}>{t}</a>' for h, t, c in g)
        groups.append(f'          <div class="nav-group">{links}</div>')
    nav = "\n".join(groups)
    full_title = title if file == "index.html" else f"{title} · Wordsmith"
    url = SITE if file == "index.html" else SITE + file
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
      <a class="brand-link" href="index.html" aria-label="Wordsmith home">
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
            <a href="script.html" aria-label="Wordsmith Script"><img src="{B}wordsmith-script-icon.svg" alt="" width="36" height="36"></a>
            <a href="manuscript.html" aria-label="Wordsmith Manuscript"><img src="{B}wordsmith-manuscript-icon.svg" alt="" width="36" height="36"></a>
            <a href="book.html" aria-label="Wordsmith Book"><img src="{B}wordsmith-book-icon.svg" alt="" width="36" height="36"></a>
          </div>
        </div>
        <div>
          <h2>Apps</h2>
          <ul>
            <li><a href="script.html">Wordsmith Script</a></li>
            <li><a href="manuscript.html">Wordsmith Manuscript</a></li>
            <li><a href="book.html">Wordsmith Book</a></li>
            <li><a href="launcher.html">Wordsmith Launcher</a></li>
          </ul>
        </div>
        <div>
          <h2>Project</h2>
          <ul>
            <li><a href="wiki/">Wiki</a></li>
            <li><a href="about.html">About</a></li>
            <li><a href="open-source.html">Open source</a></li>
            <li><a href="open-source.html#roadmap">Road to 1.0</a></li>
            <li><a href="open-source.html#get-involved">Get involved</a></li>
            <li><a href="open-source.html#privacy">Privacy</a></li>
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
        <span>The apps' code is open source under MIT or Apache-2.0. Wordsmith, Wordsmith &amp; Ink and the app names and logos are trademarks of The James C. J. Foundation.</span>
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

CORK = """<div class="cork" role="img" aria-label="Illustration of a corkboard with six index cards, one per chapter">
          <div class="icard"><b>Playing Pilgrims</b><span>Christmas Eve by the fire. Mother's letter from the war.</span></div>
          <div class="icard"><b>A Merry Christmas</b><span>The girls give their breakfast away.</span></div>
          <div class="icard"><b>The Laurence Boy</b><span>Jo meets Laurie at the New Year's party.</span></div>
          <div class="icard"><b>Burdens</b><span>Each sister and her own trouble.</span></div>
          <div class="icard"><b>Being Neighborly</b><span>Jo crosses the snow to the big house.</span></div>
          <div class="icard"><b>Beth Finds the Palace Beautiful</b><span>The piano, and Mr. Laurence.</span></div>
        </div>"""


def spread(guides=True):
    g = '<div class="guides" aria-hidden="true"></div>' if guides else ""
    return f"""<div class="spread">
              <div class="leaf left">
                <div class="ch-num" style="margin-top:58%">VOLUME I</div>
                <div class="orn" style="margin-top:1.2em">&#10087;</div>
              </div>
              <div class="leaf right">
                {g}
                <div class="ch-num">CHAPTER I</div>
                <div class="orn" style="margin-top:0.8em">&#10087;</div>
                <p class="first"><span class="sc">It is a truth</span> universally acknowledged, that a single man in possession of a good fortune, must be in want of a wife.</p>
                <p>However little known the feelings or views of such a man may be on his first entering a neighbourhood, this truth is so well fixed in the minds of the surrounding families, that he is considered the rightful property of some one or other of their daughters.</p>
                <p>“My dear Mr. Bennet,” said his lady to him one day, “have you heard that Netherfield Park is let at last?”</p>
                <p>Mr. Bennet replied that he had not.</p>
                <p>“But it is,” returned she; “for Mrs. Long has just been here, and she told me all about it.”</p>
                <div class="folio">1</div>
              </div>
            </div>"""


# The home page's "desk": a real Script screenshot with an index card and a book page laid over it.
DESK = f"""<div class="desk" role="img" aria-label="A Wordsmith Script screenplay page, with an index card and a typeset book page laid on top: the three apps on one desk">
          <div class="desk-shot"><img src="{IMG}script-page-view.webp" alt="" width="1600" height="983"></div>
          <div class="desk-card">
            <img class="badge" src="{B}wordsmith-manuscript-icon.svg" alt="" width="40" height="40">
            <b>Playing Pilgrims</b>
            <span>Christmas Eve by the fire. The four sisters wish for presents, and Mother's letter comes from the war.</span>
          </div>
          <div class="desk-leaf">
            <img class="badge" src="{B}wordsmith-book-icon.svg" alt="" width="40" height="40">
            <div class="ch-num">CHAPTER I</div>
            <div class="orn">&#10087;</div>
            <p class="first"><span class="sc">It is a truth</span> universally acknowledged, that a single man in possession of a good fortune, must be in want of a wife.</p>
            <p>However little known the feelings or views of such a man may be on his first entering a neighbourhood, this truth is so well fixed in the minds of the surrounding families.</p>
          </div>
          <img class="badge badge-shot" src="{B}wordsmith-script-icon.svg" alt="" width="40" height="40">
        </div>"""


# ---------------------------------------------------------------- Home
def app_row(cls, slug, chip, chip_cls, for_, text, ticks, visual, ticks_label=""):
    items = "".join(f"<li>{t}</li>" for t in ticks)
    label = f'<p class="ticks-label">{ticks_label}</p>' if ticks_label else ""
    name = slug.capitalize()
    return f"""
        <article class="app-row {cls}">
          <div class="app-copy">
            <div class="app-head"><img src="{B}wordsmith-{slug}-icon.svg" alt="" width="64" height="64"><span class="chip {chip_cls}">{chip}</span></div>
            {logo(f"wordsmith-{slug}-wordmark", f"Wordsmith {name}", "wordmark")}
            <p class="app-for">{for_}</p>
            <p class="app-text">{text}</p>
            {label}<ul class="ticks">{items}</ul>
            <a class="btn btn-ghost" href="{slug}.html">Explore {name} {ARROW}</a>
          </div>
          <div class="app-visual stage">
            {visual}
          </div>
        </article>"""


home = f"""
    <section class="hero">
      <div class="wrap hero-grid">
        <div class="hero-copy">
          <p class="kicker"><span class="chip pre">Early days</span><span>No downloads yet. <a href="open-source.html#roadmap">See the road to 1.0</a></span></p>
          <h1>Free writing tools, from first page to finished book.</h1>
          <p class="lede">A family of open-source apps for screenwriters, novelists and authors. Write a screenplay,
            draft a novel, and turn it into a print book and an ebook.</p>
          <div class="actions">
            <a class="btn btn-primary" href="#apps">Meet the apps {DOWN}</a>
            <a class="btn btn-ghost" href="{ORG}">{GH} Follow on GitHub</a>
          </div>
          <ul class="hero-apps" aria-label="The Wordsmith apps">
            <li><a href="script.html" class="n-script"><img src="{B}wordsmith-script-icon.svg" alt="" width="48" height="48"><span><b>Script</b><small>Screenplays</small></span></a></li>
            <li><a href="manuscript.html" class="n-manuscript"><img src="{B}wordsmith-manuscript-icon.svg" alt="" width="48" height="48"><span><b>Manuscript</b><small>Novels</small></span></a></li>
            <li><a href="book.html" class="n-book"><img src="{B}wordsmith-book-icon.svg" alt="" width="48" height="48"><span><b>Book</b><small>Print and ebook</small></span></a></li>
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
          <p class="lede">Each app does one job well, and they work together. All three run on macOS, Windows and Linux,
            and keep your work as plain files on your own computer.</p>
        </div>
        <div class="app-rows">{app_row("p-script", "script", "Pre-release", "pre", "Screenplays, TV and stage plays",
        "Write screenplays, TV episodes and stage plays, formatted as you type and ready for production.",
        ["Return and Tab do the formatting", "Pages, PDFs and printouts that match the screen", "Revision colors, scene numbers and locked pages"],
        f'<div class="shot"><img src="{IMG}script-index-cards.webp" alt="Wordsmith Script showing index cards, one per scene" width="1600" height="983" loading="lazy"></div>')}
{app_row("p-manuscript", "manuscript", "Pre-release", "pre", "Novels and long work",
        "Plan, draft and revise novels and other long work, with your story bible beside the text.",
        ["Parts, chapters and scenes in one binder", "A corkboard, an outline and a story bible", "Drafts and snapshots you can compare"],
        CORK)}
{app_row("p-book", "book", "In development", "dev", "Print books and ebooks",
        "Design and typeset a finished manuscript as a print-ready book and an ebook for every store.",
        ["Book designs with chapter openings and drop caps", "A print-ready PDF and an accessible EPUB 3", "Preflight checks before you upload"],
        f'<div role="img" aria-label="Illustration of a typeset two-page book spread">{spread(False)}</div>',
        "What it will do")}
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
          <li><a class="step n-script" href="script.html"><span class="step-num">1</span><img src="{B}wordsmith-script-icon.svg" alt="" width="72" height="72"><h3>Script</h3><p>Write the screenplay, and keep it in your novel's project too.</p></a></li>
          <li><a class="step n-manuscript" href="manuscript.html"><span class="step-num">2</span><img src="{B}wordsmith-manuscript-icon.svg" alt="" width="72" height="72"><h3>Manuscript</h3><p>Draft and revise the story, with characters and places in one bible.</p></a></li>
          <li><a class="step n-book" href="book.html"><span class="step-num">3</span><img src="{B}wordsmith-book-icon.svg" alt="" width="72" height="72"><h3>Book</h3><p>Turn the finished manuscript into a print book and an ebook.</p></a></li>
        </ol>
        <p class="flow-note">The planned <a href="launcher.html">Wordsmith Launcher</a> will bring all three together in one download.</p>
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
            <a class="btn btn-ghost" href="about.html">About the project</a>
          </div>
        </div>
        <div>{BOOKS}</div>
      </div>
    </section>

    <section class="section">
      <div class="wrap">
        <div class="cta-panel">
          <div class="cta-copy">
            <p class="eyebrow">Early days</p>
            <h2>Help us get to 1.0.</h2>
            <p class="lede">The apps are young and there are no downloads yet. If you write, code, design or translate,
              there's a place for you. Watch the repositories to hear about the first releases.</p>
            <div class="actions">
              <a class="btn btn-primary" href="open-source.html#get-involved">Get involved</a>
              <a class="btn btn-ghost" href="{ORG}">{GH} jamescjfoundation on GitHub</a>
            </div>
          </div>
          <ol class="mini-road" aria-label="The road to 1.0">
            <li class="now"><b>Now</b><span>Building the base</span></li>
            <li><b>Next</b><span>First releases</span></li>
            <li><b>1.0</b><span>Ready for real work</span></li>
            <li><b>Beyond</b><span>Growing together</span></li>
          </ol>
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
          <div class="actions"><a class="btn btn-ghost" href="open-source.html">How the project works</a></div>
        </div>
        <div class="stage family">{logo("wordsmith-and-ink-family", "Wordsmith &amp; Ink and its three apps: Script, Manuscript and Book")}</div>
      </div>
    </section>
"""


# ---------------------------------------------------------------- App page parts
def app_hero(slug, name, h1, lede, actions, meta, visual):
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
            {actions}
          </div>
          <div class="meta">{meta}</div>
        </div>
        <figure class="visual">
          {visual}
        </figure>
      </div>
    </section>"""


# ---------------------------------------------------------------- Script
script = app_hero(
    "script", "Wordsmith Script", "Write the screenplay. The page takes care of itself.",
    """A free, open-source screenwriting app. Type with two keys doing the formatting, see every page
          as it will print, and take the script into production with revision colors, locked pages and scene numbers.""",
    f"""<a class="btn btn-primary" href="{ORG}/wordsmith-script">{GH} View on GitHub</a>
            <a class="btn btn-ghost" href="{ORG}/wordsmith-script/blob/main/docs/guide/README.md">Read the guide</a>""",
    '<span class="chip pre">Pre-release</span><span>macOS, Windows, Linux</span><span>No downloads yet: build from source</span>',
    f"""<div class="stage"><div class="shot"><img src="{IMG}script-page-view.webp" alt="Wordsmith Script showing a screenplay page, the list of scenes on the left and the scene inspector on the right" width="1600" height="983"></div></div>
          <figcaption>The page view, with the scenes on the left and the scene at the caret on the right. Pictures are drawn by the app from "Everybody's Girl" (1918), a public-domain photoplay.</figcaption>""",
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
    ("cards", "Structure", "Index cards and a scene view that reorder the script, a story board of beats, an outline in lanes, scene colors and a structure strip."),
    ("flag", "Production", "Revision mode on the standard color cycle with margin marks, scene numbers with A-scenes and omitted scenes, locked pages and revised-pages-only printing."),
    ("chart", "Reports", "Scene lengths in eighths, a character report, a representation report and writing statistics, with goals and a sprint timer."),
    ("layers", "Templates", "Feature screenplays, TV episodes, stage plays and more, with dual dialogue when two people talk at once."),
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
        <div class="gallery">
          <figure><div class="shot"><img src="{IMG}script-index-cards.webp" alt="Index cards, one per scene, with scene summaries" width="1600" height="983" loading="lazy"></div><figcaption>Index cards: drag a card and the scene moves in the script.</figcaption></figure>
          <figure><div class="shot"><img src="{IMG}script-story-board.webp" alt="The story board with beats arranged in acts" width="1600" height="983" loading="lazy"></div><figcaption>The story board: plan beats before you write them.</figcaption></figure>
          <figure><div class="shot"><img src="{IMG}script-ribbon-production.webp" alt="The Production tab with revision tools" width="1600" height="983" loading="lazy"></div><figcaption>Production: revisions, scene numbers and locked pages.</figcaption></figure>
          <figure><div class="shot"><img src="{IMG}script-draft-view-dark.webp" alt="The draft view in the dark theme" width="1600" height="983" loading="lazy"></div><figcaption>The draft view, in the dark theme.</figcaption></figure>
        </div>
      </div>
    </section>

    <section class="section sunken">
      <div class="wrap split">
        <div>
          <p class="eyebrow">Familiar from day one</p>
          <h2>Works the way screenwriters already work.</h2>
          <p class="muted">Wordsmith Script follows the conventions the industry has used for decades, so you can move
            between it and other screenwriting software without relearning anything. The ribbon is named for screenplay
            work: Write, Insert, Plan, Production, Review and View.</p>
        </div>
        <ul class="ticks boxed">
          <li>Plain-text scripts you can read, back up and compare anywhere</li>
          <li>Auto-save and timestamped backups, every file saved safely</li>
          <li>No telemetry. The only request it makes is an update check you can turn off</li>
          <li>Screen readers supported through the platform's accessibility tools</li>
          <li>MIT or Apache-2.0 licensed: free to use, study and improve</li>
        </ul>
      </div>
    </section>

    <section class="section">
      <div class="wrap split">
        <div>
          <p class="eyebrow">Try it today</p>
          <h2>Build it from source.</h2>
          <p class="muted">There are no installers yet. If you're comfortable with a terminal and have
            <a href="https://rustup.rs">Rust</a> installed, you can run the current version now. Installers for macOS,
            Windows and Linux come with the first release.</p>
        </div>
        {terminal(f'''git clone {ORG}/wordsmith-script
cd wordsmith-script
cargo run --release -p wordsmith''')}
      </div>
    </section>
"""

# ---------------------------------------------------------------- Manuscript
manuscript = app_hero(
    "manuscript", "Wordsmith Manuscript", "The whole novel, in one place.",
    """A free, open-source app for writing novels and other long work. Plan on a corkboard, draft in a
          binder of chapters and scenes, keep your story bible beside the text, and hand the finished manuscript to
          Wordsmith Book.""",
    f"""<a class="btn btn-primary" href="{ORG}/wordsmith-manuscript">{GH} View on GitHub</a>
            <a class="btn btn-ghost" href="{ORG}/wordsmith-manuscript/blob/main/docs/guide/README.md">Read the guide</a>""",
    '<span class="chip pre">Pre-release</span><span>macOS, Windows, Linux</span><span>No downloads yet: build from source</span>',
    """<div class="stage"><div class="mock" role="img" aria-label="Illustration of Wordsmith Manuscript: a binder of chapters, the text of a scene, and the inspector with the scene's synopsis and label">
            <div class="mock-bar"><i></i><i></i><i></i><span class="title">Little Women</span><span>· Draft 2</span></div>
            <div class="mock-body">
              <div class="mock-side">
                <h4>Manuscript</h4>
                <div class="row">Part One</div>
                <div class="row in">1. Playing Pilgrims</div>
                <div class="row in sel">&nbsp;&nbsp;The four sisters</div>
                <div class="row in">&nbsp;&nbsp;Mother's letter</div>
                <div class="row in">2. A Merry Christmas</div>
                <div class="row in">3. The Laurence Boy</div>
                <div class="row in">4. Burdens</div>
                <h4 class="gap">Story bible</h4>
                <div class="row"><span class="dot"></span>Jo March</div>
                <div class="row"><span class="dot"></span>Meg March</div>
                <div class="row"><span class="dot muted-dot"></span>Orchard House</div>
                <h4 class="gap">Research</h4>
                <div class="row">Pilgrim's Progress notes</div>
              </div>
              <div class="mock-page">
                <h5>CHAPTER ONE</h5>
                <p>"Christmas won't be Christmas without any presents," grumbled Jo, lying on the rug.</p>
                <p>"It's so dreadful to be poor!" sighed Meg, looking down at her old dress.</p>
                <p>"I don't think it's fair for some girls to have plenty of pretty things, and other girls nothing at all," added little Amy, with an injured sniff.</p>
                <p>"We've got Father and Mother, and each other," said Beth contentedly from her corner.<span class="caret"></span></p>
              </div>
              <div class="mock-side right">
                <h4>Inspector</h4>
                <div class="field"><b>Synopsis</b><span>The sisters by the fire on Christmas Eve, wishing for presents.</span></div>
                <div class="field"><b>Label</b><span><span class="dot"></span>Jo's thread</span></div>
                <div class="field"><b>Status</b><span>Second draft</span></div>
                <div class="field"><b>In this scene</b><span>Jo, Meg, Amy, Beth</span></div>
              </div>
            </div>
            <div class="mock-foot"><span>Scene: 412 words</span><span>Session 1,240 of 1,800 <span class="target"><b></b></span></span></div>
          </div></div>
          <figcaption>An illustration of the main window, not a screenshot. The text is from <i>Little Women</i> (1868), in the public domain.</figcaption>""",
) + f"""

    <section class="section sunken">
      <div class="wrap">
        <div class="section-head">
          <p class="eyebrow">What it does</p>
          <h2>Plan it, write it, revise it, finish it.</h2>
        </div>
        {features([
    ("list", "The binder", "Parts, chapters and scenes in one list. Drag to reorder, split and merge, and read any run of scenes as one continuous text."),
    ("cards", "Corkboard and outline", "Index cards for every scene, a freeform board with lines between ideas, and an outline with your own columns."),
    ("people", "Story bible", "Characters, places and anything else, with your own templates, relationships read from both sides, and suggested links from the names in a scene."),
    ("layers", "Drafts", "Keep the manuscript as it is and start a new draft. Compare drafts chapter by chapter and choose which one goes to print."),
    ("history", "Snapshots", "Save a scene before a big change and compare it word by word later. Restore it in one click."),
    ("target", "Targets and history", "Word targets for the session and the book, a writing calendar kept on your computer, and progress you can see."),
    ("timeline", "Threads and timeline", "Lanes for plot threads or points of view, and a timeline of the story's own dates."),
    ("books", "Series", "Several books can share one story bible, so what you learn about a character in book one is there in book three."),
    ("pen", "Revision tools", "Split the editor, leave comments, mark revision passes in color, and turn on offline grammar hints if you want them."),
])}
      </div>
    </section>

    <section class="section">
      <div class="wrap split wide-visual">
        <div>
          <p class="eyebrow">Planning</p>
          <h2>See the shape of the story.</h2>
          <p class="muted">Every scene is a card. Write a line on it, color it by thread or point of view, and move it
            around until the story works. The text moves with it.</p>
        </div>
        <div class="stage">{CORK}</div>
      </div>
    </section>

    <section class="section sunken">
      <div class="wrap split">
        <div>
          <p class="eyebrow">Your words, safe</p>
          <h2>Bring everything in. Lose nothing.</h2>
          <p class="muted">Import from Word, OpenDocument, RTF, Markdown, web pages, EPUB and plain text, or a whole
            folder of documents at once. Chapters and scene breaks are found for you, and every import is checked word
            for word against the source. If a single word doesn't match, the import isn't made.</p>
        </div>
        <ul class="ticks boxed">
          <li>A project is a folder of plain text files, readable in any text editor</li>
          <li>One file per scene, so version control and synced folders work well</li>
          <li>Export a standard manuscript for agents and editors, as DOCX or PDF</li>
          <li>Export to Word, OpenDocument, RTF, Markdown, HTML and EPUB, each one checked</li>
          <li>Hand the book to Wordsmith Book as one package, ready to typeset</li>
          <li>Keep Wordsmith Script screenplays inside the same project</li>
        </ul>
      </div>
    </section>

    <section class="section">
      <div class="wrap">
        <div class="callout p-book">
          <img src="{B}wordsmith-book-icon.svg" alt="" width="64" height="64">
          <div><h3>Finished? Make it a book.</h3><p>Wordsmith Book opens your Manuscript project directly and typesets it for print and ebook. If it spots a typo, it offers the fix back instead of changing your words.</p></div>
          <a class="btn btn-ghost" href="book.html">About Book {ARROW}</a>
        </div>
      </div>
    </section>

    <section class="section sunken">
      <div class="wrap split">
        <div>
          <p class="eyebrow">Try it today</p>
          <h2>Build it from source.</h2>
          <p class="muted">There are no installers yet. With <a href="https://rustup.rs">Rust</a> installed you can run
            the current version now. The interface is in English and Spanish so far, and more languages can be added.</p>
        </div>
        {terminal(f'''git clone {ORG}/wordsmith-manuscript
cd wordsmith-manuscript
cargo run -p wordsmith-manuscript''')}
      </div>
    </section>
"""

# ---------------------------------------------------------------- Book
book = app_hero(
    "book", "Wordsmith Book", "From manuscript to a book you'd be proud to sell.",
    """A free, open-source app for designing and typesetting books. Bring a finished manuscript, choose
          a design, set the trim size, fonts and chapter openings, and export a print-ready PDF and an accessible ebook,
          with every word checked against your source.""",
    f"""<a class="btn btn-primary" href="{ORG}/wordsmith-book">{GH} Follow on GitHub</a>
            <a class="btn btn-ghost" href="{ORG}/wordsmith-book/blob/main/docs/PLAN.md">Read the plan</a>""",
    '<span class="chip dev">In development</span><span>macOS, Windows, Linux</span><span>Being built now</span>',
    f"""<div class="spread-wrap" role="img" aria-label="Illustration of a typeset two-page book spread: a part page on the left and the opening of chapter one on the right">
            {spread()}
            <div class="book-ui" aria-hidden="true">
              <span>Trim 5.5 &times; 8.5 in</span><span>Cream paper</span><span>Design: Classic</span><span class="ok">Preflight passed</span><span class="ok">EPUB valid</span>
            </div>
          </div>
          <figcaption>An illustration of a print preview, with the safe-area guide shown on the right page. Not a screenshot: Book is still being built. Text from <i>Pride and Prejudice</i> (1813), in the public domain.</figcaption>""",
) + f"""

    <section class="section sunken">
      <div class="wrap">
        <div class="section-head">
          <p class="eyebrow">What it will do</p>
          <h2>Beautiful by default. Ready for every store.</h2>
          <p class="lede">Book is planned to give independent authors and small presses the typesetting quality of a
            traditional publisher, without learning typesetting.</p>
        </div>
        {features([
    ("import", "Import", "Open a Wordsmith Manuscript project directly, or bring in Word, Google Docs downloads, Markdown or plain text. Chapters and scene breaks are found for you."),
    ("letters", "Book designs", "Designs for every genre, with chapter openings, drop caps, ornaments and running heads. Mix parts of two designs, and save your own."),
    ("page", "Front and back matter", "Title and copyright pages filled in from your book's details, dedication, contents, about the author, \"also by\" and more."),
    ("print", "Print-ready PDF", "Standard trim sizes, margins that grow with the page count, chapters on the right-hand page, and paperback and hardcover settings."),
    ("tablet", "Ebooks", "An accessible EPUB 3 that passes the industry's validator, with a live preview on phone, tablet and e-reader frames."),
    ("check", "Preflight", "Checks the store rules before you upload: blank pages, font sizes, image resolution, cover size and more."),
    ("open-book", "Cover template", "The exact full-wrap cover size for your page count and paper, with spine, bleed and safe areas marked."),
    ("copies", "Store editions", "One book, several editions: the right links and pages for each ebook store, built from one source."),
    ("shield", "Your words, untouched", "Typographic cleanup (curly quotes, dashes, ellipses) is shown and reversible, never silent. A switch keeps the text exactly as written."),
])}
      </div>
    </section>

    <section class="section">
      <div class="wrap split">
        <div>
          <p class="eyebrow">For a small press too</p>
          <h2>One author or a whole catalogue.</h2>
          <p class="muted">House styles lock a design for an imprint or a series, so every book matches. Builds can run
            from the command line, so a press can produce a whole list the same way every time.</p>
        </div>
        <ul class="ticks boxed">
          <li>Designs in an open format that can be shared and versioned</li>
          <li>Series pages and box sets with one master contents</li>
          <li>Reproducible builds from a script</li>
          <li>Built on established open-source typesetting, not reinvented</li>
        </ul>
      </div>
    </section>

    <section class="section sunken">
      <div class="wrap">
        <div class="callout">
          <img src="{B}wordsmith-book-icon.svg" alt="" width="64" height="64">
          <div><h3>Book is being built in the open.</h3><p>Watch the repository to follow along, or read the plan and tell us what your books need.</p></div>
          <a class="btn btn-primary" href="{ORG}/wordsmith-book">{GH} Watch on GitHub</a>
        </div>
      </div>
    </section>
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
          <p class="lede">The Wordsmith Launcher is planned as the front door to the suite: a small app that installs the
            Wordsmith apps you want, keeps them up to date, and opens your recent work from any of them.</p>
          <div class="meta"><span class="chip planned">Planned</span><span>Details are still being worked out</span></div>
        </div>
        <figure class="launch">
          <div class="mock" role="img" aria-label="Illustration of the planned launcher: the three apps with their status, and a list of recent projects">
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
          <figcaption>An early sketch, not a design.</figcaption>
        </figure>
      </div>
    </section>

    <section class="section sunken">
      <div class="wrap">
        <div class="section-head">
          <p class="eyebrow">The idea</p>
          <h2>What the launcher is for.</h2>
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
          <div><h3>Have ideas for the launcher?</h3><p>It hasn't been built yet, so now is the best time to shape it. Tell us what would help you.</p></div>
          <a class="btn btn-ghost" href="open-source.html#get-involved">Get involved</a>
        </div>
      </div>
    </section>
"""

# ---------------------------------------------------------------- Open source
opensource = f"""
    <section class="p-hero">
      <div class="wrap">
        <p class="eyebrow">Open source</p>
        <h1>Built in the open, for every writer.</h1>
        <p class="lede">Every line of Wordsmith is public: the code, the plans and the decisions. Here is where the
          project stands, where it's going, and how you can help it get there.</p>
      </div>
    </section>

    <section class="section" id="roadmap">
      <div class="wrap">
        <div class="section-head">
          <p class="eyebrow">Early days</p>
          <h2>The road to 1.0.</h2>
          <p class="lede">We're at the start. The apps work, but they're young: no installers yet, and plenty still to
            build. The hope is to reach a solid 1.0 for each app, and to grow a community that carries the work
            forward from there.</p>
        </div>
        <ol class="road">
          <li class="now"><span class="when">Now</span><h3>Building the base</h3>
            <ul><li>Script and Manuscript rebuilt on one shared core</li><li>Book's first steps</li><li>Code, plans and decisions public</li></ul></li>
          <li><span class="when">Next</span><h3>First releases</h3>
            <ul><li>Installers for macOS, Windows and Linux</li><li>Verified downloads from GitHub</li><li>The launcher</li></ul></li>
          <li><span class="when">1.0</span><h3>Ready for real work</h3>
            <ul><li>Each app complete for daily writing</li><li>Script to Manuscript to Book, end to end</li><li>Stable file formats</li></ul></li>
          <li><span class="when">Beyond</span><h3>Growing together</h3>
            <ul><li>More languages</li><li>Templates and book designs from the community</li><li>Whatever writers ask for</li></ul></li>
        </ol>

        <div class="table-scroll">
          <table class="status">
            <thead><tr><th>App</th><th>Status</th><th>For</th><th>Code</th></tr></thead>
            <tbody>
              <tr class="p-script"><td><img src="{B}wordsmith-script-icon.svg" alt="" width="28" height="28">Wordsmith Script</td><td><span class="chip pre">Pre-release</span></td><td>Screenplays, TV and stage plays</td><td><a href="{ORG}/wordsmith-script">wordsmith-script</a></td></tr>
              <tr class="p-manuscript"><td><img src="{B}wordsmith-manuscript-icon.svg" alt="" width="28" height="28">Wordsmith Manuscript</td><td><span class="chip pre">Pre-release</span></td><td>Novels and long work</td><td><a href="{ORG}/wordsmith-manuscript">wordsmith-manuscript</a></td></tr>
              <tr class="p-book"><td><img src="{B}wordsmith-book-icon.svg" alt="" width="28" height="28">Wordsmith Book</td><td><span class="chip dev">In development</span></td><td>Print books and ebooks</td><td><a href="{ORG}/wordsmith-book">wordsmith-book</a></td></tr>
              <tr><td><img src="{B}wordsmith-and-ink-icon.svg" alt="" width="28" height="28">Wordsmith Launcher</td><td><span class="chip planned">Planned</span></td><td>Installing and opening the apps</td><td class="muted">Not started</td></tr>
              <tr><td><span class="core-dot" aria-hidden="true"></span>open-source-core</td><td><span class="chip pre">Pre-release</span></td><td>The shared base every app is built on</td><td><a href="{ORG}/open-source-core">open-source-core</a></td></tr>
            </tbody>
          </table>
        </div>
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
    ("star", "Watch and star", "Watch the repositories to hear about the first releases. Stars help other writers find the project."),
    ("chat", "Try it and tell us", "Build an app from source, write something real in it, and open an issue for anything that gets in your way."),
    ("code", "Write code", "The apps are written in Rust. Each repository's contributing guide explains how changes are made and checked."),
    ("globe", "Translate", "Help bring the apps to writers in your language. Manuscript already speaks English and Spanish."),
    ("letters", "Design", "Book designs, templates and documentation all need people with an eye for detail."),
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
          <p class="muted">The apps send no telemetry and have no accounts. Your writing, notes and file names are never
            sent anywhere. The only request an app makes on its own is a check for updates with GitHub, which you can
            turn off.</p>
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
          <p>The apps' code is licensed under the MIT license or the Apache License 2.0, at your option. The fonts are
            under the SIL Open Font License.</p>
          <p class="muted">The names Wordsmith, Wordsmith &amp; Ink, Wordsmith Script, Wordsmith Manuscript and Wordsmith
            Book, and their logos, are trademarks of The James C. J. Foundation. You may use them unchanged to refer to the
            project, but not for forks or other products.</p>
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
        <div class="actions"><a class="btn btn-primary" href="index.html">Back to the start</a><a class="btn btn-ghost" href="wiki/">Open the wiki</a></div>
      </div>
    </section>
"""

page("index.html", "Wordsmith: free, open-source writing apps",
     "Wordsmith is a family of free, open-source apps for screenwriters, novelists and authors, from The James C. J. Foundation.", home)
page("script.html", "Wordsmith Script", "A free, open-source screenwriting app for macOS, Windows and Linux.", script, "p-script")
page("manuscript.html", "Wordsmith Manuscript", "A free, open-source app for writing novels and other long work.", manuscript, "p-manuscript")
page("book.html", "Wordsmith Book", "A free, open-source app for designing and typesetting print books and ebooks.", book, "p-book")
page("launcher.html", "Wordsmith Launcher", "One download to install, update and open the Wordsmith apps.", launcher)
page("about.html", "About", "Wordsmith is made by Wordsmith & Ink, a project of The James C. J. Foundation, to give writers free, open tools.", about)
page("open-source.html", "Open source", "Wordsmith is an open-source project of The James C. J. Foundation. Read about the project, the road to 1.0 and how to help.", opensource)
page("404.html", "Page not found", "This page could not be found.", notfound)
print("ok")
