#!/usr/bin/env python3
"""Writes the Wordsmith website's HTML pages (python3 website/tools/build.py). Header and footer are shared here."""
import pathlib, re, sys

OUT = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parent.parent
ORG = "https://github.com/jamescjfoundation"
FOUNDATION = "https://jamescj.org"
B = "assets/brand/"

GH = '<svg viewBox="0 0 16 16" aria-hidden="true" fill="currentColor"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/></svg>'
ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'


def logo(name, alt, cls="", h=None):
    """A logo that switches to its paper version in dark mode."""
    c = f' class="{cls}"' if cls else ""
    return (f'<picture><source srcset="{B}{name}-paper.svg" media="(prefers-color-scheme: dark)">'
            f'<img{c} src="{B}{name}-ink.svg" alt="{alt}"></picture>')


NAV = [[("index.html", "Home", ""), ("about.html", "About", "")],
       [("script.html", "Script", "n-script"), ("manuscript.html", "Manuscript", "n-manuscript"), ("book.html", "Book", "n-book")],
       [("launcher.html", "Launcher", ""), ("open-source.html", "Open source", "")]]


def page(file, title, desc, body, cls=""):
    groups = []
    for g in NAV:
        links = "".join(
            f'<a href="{h}"{f' class="{c}"' if c else ""}{' aria-current="page"' if h == file else ""}>{t}</a>' for h, t, c in g)
        groups.append(f'        <div class="nav-group">{links}</div>')
    nav = '\n        <span class="nav-sep" aria-hidden="true"></span>\n'.join(groups)
    full_title = title if file == "index.html" else f"{title} · Wordsmith"
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
  <meta property="og:image" content="{B}og-image.png">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="theme-color" content="#FAFAF7" media="(prefers-color-scheme: light)">
  <meta name="theme-color" content="#12162B" media="(prefers-color-scheme: dark)">
  <link rel="icon" href="favicon.svg" type="image/svg+xml">
  <link rel="apple-touch-icon" href="{B}wordsmith-and-ink-icon-512.png">
  <link rel="preload" href="assets/fonts/courier-prime-latin-700-normal.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="assets/fonts/inter-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="assets/css/site.css">
</head>
<body class="{cls}">
  <a class="skip" href="#main">Skip to content</a>
  <header class="site-header">
    <div class="wrap">
      <a class="brand-link" href="index.html" aria-label="Wordsmith home">
        {logo("wordsmith-and-ink-wordmark", "Wordsmith &amp; Ink")}
      </a>
      <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav">Menu</button>
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
        </div>
        <div>
          <h4>Apps</h4>
          <ul>
            <li><a href="script.html">Wordsmith Script</a></li>
            <li><a href="manuscript.html">Wordsmith Manuscript</a></li>
            <li><a href="book.html">Wordsmith Book</a></li>
            <li><a href="launcher.html">Wordsmith Launcher</a></li>
          </ul>
        </div>
        <div>
          <h4>Project</h4>
          <ul>
            <li><a href="about.html">About</a></li>
            <li><a href="open-source.html">Open source</a></li>
            <li><a href="open-source.html#roadmap">Road to 1.0</a></li>
            <li><a href="open-source.html#get-involved">Get involved</a></li>
            <li><a href="open-source.html#privacy">Privacy</a></li>
          </ul>
        </div>
        <div>
          <h4>Elsewhere</h4>
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
    (OUT / file).write_text(html, encoding="utf-8")


# ---------------------------------------------------------------- Home and About
DOWN = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 5v14M6 13l6 6 6-6"/></svg>'

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

home = f"""
    <section class="hero">
      <div class="wrap hero-grid">
        <div>
          <p class="eyebrow">Free &middot; Open source &middot; For writers</p>
          <h1>Free writing tools, from first page to finished book.</h1>
          <p class="lede">A family of open-source apps for screenwriters, novelists and authors. Write a screenplay,
            draft a novel, and turn it into a print book and an ebook.</p>
          <div class="actions">
            <a class="btn btn-primary" href="#apps">Get the apps {DOWN}</a>
            <a class="btn btn-ghost" href="{ORG}">{GH} Follow on GitHub</a>
          </div>
          <p class="hero-note"><span class="chip pre">Early days</span> No downloads yet. <a href="open-source.html#roadmap">See the road to 1.0</a></p>
        </div>
        <div class="icon-stack" aria-label="The Wordsmith apps">
          <a href="script.html" class="n-script"><img src="{B}wordsmith-script-icon.svg" alt="" width="200" height="200"><span>Script</span><small>Screenplays</small></a>
          <a href="manuscript.html" class="n-manuscript"><img src="{B}wordsmith-manuscript-icon.svg" alt="" width="200" height="200"><span>Manuscript</span><small>Novels</small></a>
          <a href="book.html" class="n-book"><img src="{B}wordsmith-book-icon.svg" alt="" width="200" height="200"><span>Book</span><small>Print and ebook</small></a>
        </div>
      </div>
    </section>

    <section class="section" id="apps">
      <div class="wrap">
        <div class="section-head">
          <p class="eyebrow">The apps</p>
          <h2>One family, three desks.</h2>
          <p class="lede">Each app does one job well, and they work together. All three run on macOS, Windows and Linux,
            and keep your work as plain files on your own computer.</p>
        </div>
        <div class="cards">
          <a class="card p-script" href="script.html">
            <div class="card-top"><img src="{B}wordsmith-script-icon.svg" alt="" width="56" height="56"><span class="chip pre">Pre-release</span></div>
            {logo("wordsmith-script-wordmark", "Wordsmith Script", "wordmark")}
            <p>Write screenplays, TV episodes and stage plays, formatted as you type and ready for production.</p>
            <span class="more">Explore Script {ARROW}</span>
          </a>
          <a class="card p-manuscript" href="manuscript.html">
            <div class="card-top"><img src="{B}wordsmith-manuscript-icon.svg" alt="" width="56" height="56"><span class="chip pre">Pre-release</span></div>
            {logo("wordsmith-manuscript-wordmark", "Wordsmith Manuscript", "wordmark")}
            <p>Plan, draft and revise novels and other long work, with your story bible beside the text.</p>
            <span class="more">Explore Manuscript {ARROW}</span>
          </a>
          <a class="card p-book" href="book.html">
            <div class="card-top"><img src="{B}wordsmith-book-icon.svg" alt="" width="56" height="56"><span class="chip dev">In development</span></div>
            {logo("wordsmith-book-wordmark", "Wordsmith Book", "wordmark")}
            <p>Design and typeset a finished manuscript as a print-ready book and an ebook for every store.</p>
            <span class="more">Explore Book {ARROW}</span>
          </a>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="wrap">
        <div class="section-head">
          <p class="eyebrow">How it works</p>
          <h2>Write <span class="arr">&rarr;</span> Finish <span class="arr">&rarr;</span> Publish.</h2>
          <p class="lede">One shared foundation means the apps look alike, work alike and pass your work along without
            copying and pasting.</p>
        </div>
        <div class="flow">
          <a class="step n-script" href="script.html"><img src="{B}wordsmith-script-icon.svg" alt="" width="72" height="72"><h3>Script</h3><p>Write the screenplay, and keep it in your novel's project too.</p></a>
          <div class="arrow">{ARROW}</div>
          <a class="step n-manuscript" href="manuscript.html"><img src="{B}wordsmith-manuscript-icon.svg" alt="" width="72" height="72"><h3>Manuscript</h3><p>Draft and revise the story, with characters and places in one bible.</p></a>
          <div class="arrow">{ARROW}</div>
          <a class="step n-book" href="book.html"><img src="{B}wordsmith-book-icon.svg" alt="" width="72" height="72"><h3>Book</h3><p>Turn the finished manuscript into a print book and an ebook.</p></a>
        </div>
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
        <div class="section-head">
          <p class="eyebrow">Early days</p>
          <h2>Help us get to 1.0.</h2>
          <p class="lede">The apps are young and there are no downloads yet. If you write, code, design or translate,
            there's a place for you. Watch the repositories to hear about the first releases.</p>
          <div class="actions">
            <a class="btn btn-primary" href="open-source.html#get-involved">Get involved</a>
            <a class="btn btn-ghost" href="{ORG}">{GH} jamescjfoundation on GitHub</a>
          </div>
        </div>
      </div>
    </section>
"""

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
        <div class="about-mark">{logo("wordsmith-and-ink-foundation", "Wordsmith &amp; Ink, a project of The J. C. J. Foundation")}</div>
      </div>
    </section>

    <section class="section">
      <div class="wrap split">
        <div>
          <p class="eyebrow">James</p>
          <h2>A writer with a world of stories.</h2>
        </div>
        <div>
          <p>James C. J. wrote novels, plays, screenplays, TV pilots, songs and poems, and built whole worlds behind them.
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
          <div><span class="num">01</span><h3>Free, for good</h3><p>No price, no subscription, no premium tier. Every feature is for every writer.</p></div>
          <div><span class="num">02</span><h3>Your files are yours</h3><p>Plain, open file formats you can read in any text editor, saved on your own computer.</p></div>
          <div><span class="num">03</span><h3>No tracking</h3><p>No accounts, no telemetry, no ads. Your words never leave your computer unless you send them.</p></div>
          <div><span class="num">04</span><h3>Open source</h3><p>Anyone can read the code, fix it, translate it and help decide where it goes next.</p></div>
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
        <div>{logo("wordsmith-and-ink-family", "Wordsmith &amp; Ink and its three apps: Script, Manuscript and Book")}</div>
      </div>
    </section>
"""

# ---------------------------------------------------------------- Script
script = f"""
    <section class="p-hero">
      <div class="wrap">
        <div class="app-id">
          <img class="icon" src="{B}wordsmith-script-icon.svg" alt="" width="72" height="72">
          {logo("wordsmith-script-wordmark", "Wordsmith Script", "wordmark")}
        </div>
        <p class="endorse">a Wordsmith &amp; Ink app</p>
        <h1>Write the screenplay. The page takes care of itself.</h1>
        <p class="lede">A free, open-source screenwriting app. Type with two keys doing the formatting, see every page
          as it will print, and take the script into production with revision colors, locked pages and scene numbers.</p>
        <div class="actions">
          <a class="btn btn-primary" href="{ORG}/wordsmith-script">{GH} View on GitHub</a>
          <a class="btn btn-ghost" href="{ORG}/wordsmith-script/blob/main/docs/guide/README.md">Read the guide</a>
        </div>
        <div class="meta"><span class="chip pre">Pre-release</span><span>macOS, Windows, Linux</span><span>No downloads yet: build from source</span></div>
        <figure class="visual">
          <div class="shot"><img src="assets/img/script-page-view.webp" alt="Wordsmith Script showing a screenplay page, the list of scenes on the left and the scene inspector on the right" width="1600" height="983"></div>
          <figcaption>The page view, with the scenes on the left and the scene at the caret on the right. Pictures are drawn by the app from "Everybody's Girl" (1918), a public-domain photoplay.</figcaption>
        </figure>
      </div>
    </section>

    <section class="section sunken">
      <div class="wrap">
        <div class="section-head">
          <p class="eyebrow">What it does</p>
          <h2>Everything a script needs, from first draft to shooting script.</h2>
        </div>
        <div class="features">
          <div class="feature"><h3>Formatting on two keys</h3><p>Return and Tab move between scene headings, action, characters, parentheticals, dialogue and transitions. The status bar always says what comes next.</p></div>
          <div class="feature"><h3>Industry pages</h3><p>Courier Prime on standard margins, with (MORE) and (CONT'D), scene continueds, a title page, and PDFs and printouts that match the screen.</p></div>
          <div class="feature"><h3>Autocomplete that waits</h3><p>Character names, places and times offered as you type, never typed for you. Spelling, find and replace, and notes on any text.</p></div>
          <div class="feature"><h3>Structure</h3><p>Index cards and a scene view that reorder the script, a story board of beats, an outline in lanes, scene colors and a structure strip.</p></div>
          <div class="feature"><h3>Production</h3><p>Revision mode on the standard color cycle with margin marks, scene numbers with A-scenes and omitted scenes, locked pages and revised-pages-only printing.</p></div>
          <div class="feature"><h3>Reports</h3><p>Scene lengths in eighths, a character report, a representation report and writing statistics, with goals and a sprint timer.</p></div>
          <div class="feature"><h3>Templates</h3><p>Feature screenplays, TV episodes, stage plays and more, with dual dialogue when two people talk at once.</p></div>
          <div class="feature"><h3>Open files</h3><p>A plain-text native format that reads well in version control. Fountain both ways, import from text, RTF and PDF, export to PDF, RTF, text, HTML and CSV.</p></div>
          <div class="feature"><h3>Command line</h3><p>Convert, export and report from a terminal or a build script, and let tools you choose drive the app.</p></div>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="wrap">
        <div class="gallery">
          <figure><div class="shot"><img src="assets/img/script-index-cards.webp" alt="Index cards, one per scene, with scene summaries" width="1600" height="983" loading="lazy"></div><figcaption>Index cards: drag a card and the scene moves in the script.</figcaption></figure>
          <figure><div class="shot"><img src="assets/img/script-story-board.webp" alt="The story board with beats arranged in acts" width="1600" height="983" loading="lazy"></div><figcaption>The story board: plan beats before you write them.</figcaption></figure>
          <figure><div class="shot"><img src="assets/img/script-ribbon-production.webp" alt="The Production tab with revision tools" width="1600" height="983" loading="lazy"></div><figcaption>Production: revisions, scene numbers and locked pages.</figcaption></figure>
          <figure><div class="shot"><img src="assets/img/script-draft-view-dark.webp" alt="The draft view in the dark theme" width="1600" height="983" loading="lazy"></div><figcaption>The draft view, in the dark theme.</figcaption></figure>
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
        <ul class="ticks">
          <li>Plain-text scripts you can read, back up and compare anywhere</li>
          <li>Auto-save and timestamped backups, every file saved safely</li>
          <li>No telemetry. The only request it makes is an update check you can turn off</li>
          <li>Screen readers supported through the platform's accessibility tools</li>
          <li>MIT or Apache-2.0 licensed: free to use, study and improve</li>
        </ul>
      </div>
    </section>

    <section class="section">
      <div class="wrap">
        <div class="split">
          <div>
            <p class="eyebrow">Try it today</p>
            <h2>Build it from source.</h2>
            <p class="muted">There are no installers yet. If you're comfortable with a terminal and have
              <a href="https://rustup.rs">Rust</a> installed, you can run the current version now. Installers for macOS,
              Windows and Linux come with the first release.</p>
          </div>
          <pre><code>git clone {ORG}/wordsmith-script
cd wordsmith-script
cargo run --release -p wordsmith</code></pre>
        </div>
      </div>
    </section>
"""

# ---------------------------------------------------------------- Manuscript
manuscript = f"""
    <section class="p-hero">
      <div class="wrap">
        <div class="app-id">
          <img class="icon" src="{B}wordsmith-manuscript-icon.svg" alt="" width="72" height="72">
          {logo("wordsmith-manuscript-wordmark", "Wordsmith Manuscript", "wordmark")}
        </div>
        <p class="endorse">a Wordsmith &amp; Ink app</p>
        <h1>The whole novel, in one place.</h1>
        <p class="lede">A free, open-source app for writing novels and other long work. Plan on a corkboard, draft in a
          binder of chapters and scenes, keep your story bible beside the text, and hand the finished manuscript to
          Wordsmith Book.</p>
        <div class="actions">
          <a class="btn btn-primary" href="{ORG}/wordsmith-manuscript">{GH} View on GitHub</a>
          <a class="btn btn-ghost" href="{ORG}/wordsmith-manuscript/blob/main/docs/guide/README.md">Read the guide</a>
        </div>
        <div class="meta"><span class="chip pre">Pre-release</span><span>macOS, Windows, Linux</span><span>No downloads yet: build from source</span></div>

        <figure class="visual">
          <div class="mock" role="img" aria-label="Illustration of Wordsmith Manuscript: a binder of chapters, the text of a scene, and the inspector with the scene's synopsis and label">
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
                <h4 style="margin-top:14px">Story bible</h4>
                <div class="row"><span class="dot"></span>Jo March</div>
                <div class="row"><span class="dot"></span>Meg March</div>
                <div class="row"><span class="dot" style="background:var(--muted)"></span>Orchard House</div>
                <h4 style="margin-top:14px">Research</h4>
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
          </div>
          <figcaption>An illustration of the main window, not a screenshot. The text is from <i>Little Women</i> (1868), in the public domain.</figcaption>
        </figure>
      </div>
    </section>

    <section class="section sunken">
      <div class="wrap">
        <div class="section-head">
          <p class="eyebrow">What it does</p>
          <h2>Plan it, write it, revise it, finish it.</h2>
        </div>
        <div class="features">
          <div class="feature"><h3>The binder</h3><p>Parts, chapters and scenes in one list. Drag to reorder, split and merge, and read any run of scenes as one continuous text.</p></div>
          <div class="feature"><h3>Corkboard and outline</h3><p>Index cards for every scene, a freeform board with lines between ideas, and an outline with your own columns.</p></div>
          <div class="feature"><h3>Story bible</h3><p>Characters, places and anything else, with your own templates, relationships read from both sides, and suggested links from the names in a scene.</p></div>
          <div class="feature"><h3>Drafts</h3><p>Keep the manuscript as it is and start a new draft. Compare drafts chapter by chapter and choose which one goes to print.</p></div>
          <div class="feature"><h3>Snapshots</h3><p>Save a scene before a big change and compare it word by word later. Restore it in one click.</p></div>
          <div class="feature"><h3>Targets and history</h3><p>Word targets for the session and the book, a writing calendar kept on your computer, and progress you can see.</p></div>
          <div class="feature"><h3>Threads and timeline</h3><p>Lanes for plot threads or points of view, and a timeline of the story's own dates.</p></div>
          <div class="feature"><h3>Series</h3><p>Several books can share one story bible, so what you learn about a character in book one is there in book three.</p></div>
          <div class="feature"><h3>Revision tools</h3><p>Split the editor, leave comments, mark revision passes in color, and turn on offline grammar hints if you want them.</p></div>
        </div>
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
        <div class="cork" role="img" aria-label="Illustration of a corkboard with six index cards, one per chapter">
          <div class="icard"><b>Playing Pilgrims</b><span>Christmas Eve by the fire. Mother's letter from the war.</span></div>
          <div class="icard"><b>A Merry Christmas</b><span>The girls give their breakfast away.</span></div>
          <div class="icard"><b>The Laurence Boy</b><span>Jo meets Laurie at the New Year's party.</span></div>
          <div class="icard"><b>Burdens</b><span>Each sister and her own trouble.</span></div>
          <div class="icard"><b>Being Neighborly</b><span>Jo crosses the snow to the big house.</span></div>
          <div class="icard"><b>Beth Finds the Palace Beautiful</b><span>The piano, and Mr. Laurence.</span></div>
        </div>
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
        <ul class="ticks">
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
          <a class="btn btn-ghost" href="book.html">About Book</a>
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
        <pre><code>git clone {ORG}/wordsmith-manuscript
cd wordsmith-manuscript
cargo run -p wordsmith-manuscript</code></pre>
      </div>
    </section>
"""

# ---------------------------------------------------------------- Book
book = f"""
    <section class="p-hero">
      <div class="wrap">
        <div class="app-id">
          <img class="icon" src="{B}wordsmith-book-icon.svg" alt="" width="72" height="72">
          {logo("wordsmith-book-wordmark", "Wordsmith Book", "wordmark")}
        </div>
        <p class="endorse">a Wordsmith &amp; Ink app</p>
        <h1>From manuscript to a book you'd be proud to sell.</h1>
        <p class="lede">A free, open-source app for designing and typesetting books. Bring a finished manuscript, choose
          a design, set the trim size, fonts and chapter openings, and export a print-ready PDF and an accessible ebook,
          with every word checked against your source.</p>
        <div class="actions">
          <a class="btn btn-primary" href="{ORG}/wordsmith-book">{GH} Follow on GitHub</a>
          <a class="btn btn-ghost" href="{ORG}/wordsmith-book/blob/main/docs/PLAN.md">Read the plan</a>
        </div>
        <div class="meta"><span class="chip dev">In development</span><span>macOS, Windows, Linux</span><span>Being built now</span></div>

        <figure class="visual">
          <div class="spread-wrap" role="img" aria-label="Illustration of a typeset two-page book spread: a part page on the left and the opening of chapter one on the right">
            <div class="spread">
              <div class="leaf left">
                <div class="ch-num" style="margin-top:58%">VOLUME I</div>
                <div class="orn" style="margin-top:1.2em">&#10087;</div>
              </div>
              <div class="leaf right">
                <div class="guides" aria-hidden="true"></div>
                <div class="ch-num">CHAPTER I</div>
                <div class="orn" style="margin-top:0.8em">&#10087;</div>
                <p class="first"><span class=“sc”>It is a truth</span> universally acknowledged, that a single man in possession of a good fortune, must be in want of a wife.</p>
                <p>However little known the feelings or views of such a man may be on his first entering a neighbourhood, this truth is so well fixed in the minds of the surrounding families, that he is considered the rightful property of some one or other of their daughters.</p>
                <p>“My dear Mr. Bennet,” said his lady to him one day, “have you heard that Netherfield Park is let at last?”</p>
                <p>Mr. Bennet replied that he had not.</p>
                <p>“But it is,” returned she; “for Mrs. Long has just been here, and she told me all about it.”</p>
                <div class="folio">1</div>
              </div>
            </div>
            <div class="book-ui" aria-hidden="true">
              <span>Trim 5.5 &times; 8.5 in</span><span>Cream paper</span><span>Design: Classic</span><span class="ok">Preflight passed</span><span class="ok">EPUB valid</span>
            </div>
          </div>
          <figcaption>An illustration of a print preview, with the safe-area guide shown on the right page. Not a screenshot: Book is still being built. Text from <i>Pride and Prejudice</i> (1813), in the public domain.</figcaption>
        </figure>
      </div>
    </section>

    <section class="section sunken">
      <div class="wrap">
        <div class="section-head">
          <p class="eyebrow">What it will do</p>
          <h2>Beautiful by default. Ready for every store.</h2>
          <p class="lede">Book is planned to give independent authors and small presses the typesetting quality of a
            traditional publisher, without learning typesetting.</p>
        </div>
        <div class="features">
          <div class="feature"><h3>Import</h3><p>Open a Wordsmith Manuscript project directly, or bring in Word, Google Docs downloads, Markdown or plain text. Chapters and scene breaks are found for you.</p></div>
          <div class="feature"><h3>Book designs</h3><p>Designs for every genre, with chapter openings, drop caps, ornaments and running heads. Mix parts of two designs, and save your own.</p></div>
          <div class="feature"><h3>Front and back matter</h3><p>Title and copyright pages filled in from your book's details, dedication, contents, about the author, "also by" and more.</p></div>
          <div class="feature"><h3>Print-ready PDF</h3><p>Standard trim sizes, margins that grow with the page count, chapters on the right-hand page, and paperback and hardcover settings.</p></div>
          <div class="feature"><h3>Ebooks</h3><p>An accessible EPUB 3 that passes the industry's validator, with a live preview on phone, tablet and e-reader frames.</p></div>
          <div class="feature"><h3>Preflight</h3><p>Checks the store rules before you upload: blank pages, font sizes, image resolution, cover size and more.</p></div>
          <div class="feature"><h3>Cover template</h3><p>The exact full-wrap cover size for your page count and paper, with spine, bleed and safe areas marked.</p></div>
          <div class="feature"><h3>Store editions</h3><p>One book, several editions: the right links and pages for each ebook store, built from one source.</p></div>
          <div class="feature"><h3>Your words, untouched</h3><p>Typographic cleanup (curly quotes, dashes, ellipses) is shown and reversible, never silent. A switch keeps the text exactly as written.</p></div>
        </div>
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
        <ul class="ticks">
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
    <section class="p-hero">
      <div class="wrap split">
        <div>
          <div class="app-id">
            <img class="icon" src="{B}wordsmith-and-ink-icon.svg" alt="" width="72" height="72">
          </div>
          <p class="eyebrow">Wordsmith Launcher</p>
          <h1>One download for the whole desk.</h1>
          <p class="lede">The Wordsmith Launcher is planned as the front door to the suite: a small app that installs the
            Wordsmith apps you want, keeps them up to date, and opens your recent work from any of them.</p>
          <div class="meta"><span class="chip planned">Planned</span><span>Details are still being worked out</span></div>
        </div>
        <div class="launch">
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
          <p class="small muted" style="text-align:center;margin-top:12px">An early sketch, not a design.</p>
        </div>
      </div>
    </section>

    <section class="section sunken">
      <div class="wrap">
        <div class="section-head">
          <p class="eyebrow">The idea</p>
          <h2>What the launcher is for.</h2>
        </div>
        <div class="features">
          <div class="feature"><h3>Install what you need</h3><p>Pick the apps you want. A screenwriter may only need Script; a novelist may want Manuscript and Book.</p></div>
          <div class="feature"><h3>Stay up to date</h3><p>One place to see and install updates, downloaded only from the project's official releases and checked before they run.</p></div>
          <div class="feature"><h3>All your work</h3><p>Recent screenplays, novels and books in one list, each opened in the right app.</p></div>
          <div class="feature"><h3>Start something new</h3><p>Choose a screenplay, a stage play, a novel or a book, and the right app opens with the right template.</p></div>
          <div class="feature"><h3>Learn the tools</h3><p>Guides and getting-started help for every app, in one place.</p></div>
          <div class="feature"><h3>Same promises</h3><p>No account, no tracking. Update checks can be turned off.</p></div>
        </div>
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

        <div class="table-scroll" style="margin-top:56px">
          <table class="status">
            <thead><tr><th>App</th><th>Status</th><th>For</th><th>Code</th></tr></thead>
            <tbody>
              <tr class="p-script"><td>Wordsmith Script</td><td><span class="chip pre">Pre-release</span></td><td>Screenplays, TV and stage plays</td><td><a href="{ORG}/wordsmith-script">wordsmith-script</a></td></tr>
              <tr class="p-manuscript"><td>Wordsmith Manuscript</td><td><span class="chip pre">Pre-release</span></td><td>Novels and long work</td><td><a href="{ORG}/wordsmith-manuscript">wordsmith-manuscript</a></td></tr>
              <tr class="p-book"><td>Wordsmith Book</td><td><span class="chip dev">In development</span></td><td>Print books and ebooks</td><td><a href="{ORG}/wordsmith-book">wordsmith-book</a></td></tr>
              <tr><td>Wordsmith Launcher</td><td><span class="chip planned">Planned</span></td><td>Installing and opening the apps</td><td class="muted">Not started</td></tr>
              <tr><td>open-source-core</td><td><span class="chip pre">Pre-release</span></td><td>The shared base every app is built on</td><td><a href="{ORG}/open-source-core">open-source-core</a></td></tr>
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
        <div class="features">
          <div class="feature"><h3>Watch and star</h3><p>Watch the repositories to hear about the first releases. Stars help other writers find the project.</p></div>
          <div class="feature"><h3>Try it and tell us</h3><p>Build an app from source, write something real in it, and open an issue for anything that gets in your way.</p></div>
          <div class="feature"><h3>Write code</h3><p>The apps are written in Rust. Each repository's contributing guide explains how changes are made and checked.</p></div>
          <div class="feature"><h3>Translate</h3><p>Help bring the apps to writers in your language. Manuscript already speaks English and Spanish.</p></div>
          <div class="feature"><h3>Design</h3><p>Book designs, templates and documentation all need people with an eye for detail.</p></div>
          <div class="feature"><h3>Spread the word</h3><p>Tell a writer who could use free tools. That's how a community starts.</p></div>
        </div>
        <div class="actions"><a class="btn btn-primary" href="{ORG}">{GH} jamescjfoundation on GitHub</a></div>
      </div>
    </section>

    <section class="section">
      <div class="wrap split">
        <div>
          <p class="eyebrow">Standing on shoulders</p>
          <h2>Built on great open-source work.</h2>
          <p class="muted">The apps share one base, open-source-core, which is based on WordCraft by the ArtCraft team and
            uses craft-libs, egui, HarfRust, Vello and many other open-source projects. Every app credits what it uses in
            its README and NOTICE files, and fixes we make to those projects are offered back.</p>
        </div>
        <div id="privacy">
          <p class="eyebrow">Privacy</p>
          <h2>Your writing stays with you.</h2>
          <p class="muted">The apps send no telemetry and have no accounts. Your writing, notes and file names are never
            sent anywhere. The only request an app makes on its own is a check for updates with GitHub, which you can
            turn off.</p>
        </div>
      </div>
    </section>

    <section class="section sunken">
      <div class="wrap split">
        <div>
          <p class="eyebrow">Licenses and names</p>
          <h2>Free to use, study and change.</h2>
        </div>
        <div>
          <p>The apps' code is licensed under the MIT license or the Apache License 2.0, at your option. The fonts are
            under the SIL Open Font License.</p>
          <p class="muted">The names Wordsmith, Wordsmith &amp; Ink, Wordsmith Script, Wordsmith Manuscript and Wordsmith
            Book, and their logos, are trademarks of The James C. J. Foundation. You may use them unchanged to refer to the
            project, but not for forks or other products.</p>
        </div>
      </div>
    </section>
"""

notfound = f"""
    <section class="section">
      <div class="wrap" style="text-align:center">
        <p class="eyebrow">Page not found</p>
        <h1>This page is still a blank sheet.</h1>
        <p class="lede" style="margin:0 auto">The page you were looking for isn't here.</p>
        <div class="actions" style="justify-content:center"><a class="btn btn-primary" href="index.html">Back to the start</a></div>
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
