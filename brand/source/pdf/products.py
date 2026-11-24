from common import *
import glob
FOOT='Wordsmith apps · Product assets · v1.0 · November 2026'
pg=[]
# cover
icons=''.join(f'<div style="text-align:center">{img(p(a["dir"],"App icon","icon-512.png"),h="46mm")}<div style="font:600 11pt Inter;margin-top:4mm">{a["short"]}</div><div style="font-size:8.5pt;color:#9EA3BD">{a["what"]}</div></div>' for a in APPS.values())
pg.append(page(f'''<div class="kick">Wordsmith &amp; Ink · Product assets</div>
<h1 style="font-size:40pt">The Wordsmith apps</h1><p style="max-width:170mm;font-size:11pt">Three free, open-source writing apps from The James C. J. Foundation: logos, app icons, colors and type for each, and where to find every file.</p>
<div style="display:flex;gap:22mm;justify-content:center;align-items:flex-start;margin-top:auto;margin-bottom:14mm">{icons}</div>''','dark night',FOOT))
# shared system
pg.append(page(f'''<div class="kick">The shared system</div><h2>One idea, three cursors</h2>
<div class="cols c2"><div><p>A writer's whole day is spent next to a blinking cursor, and a screenplay is still typed in a Courier face. So every Wordsmith logo is the app's name typed out in Courier Prime Bold, with a cursor waiting at the end of the line. Each app gives that cursor its own color and shape, taken from the object it works with.</p>
<h3 style="margin-top:5mm">These never change between apps</h3><ul>
<li>The name typed in Courier Prime Bold, normal spacing, title case.</li>
<li>The cursor right after the last letter, 0.03 em away, as tall as the capitals. Never before the text, never on other words.</li>
<li>The icon: a paper letter and the app's cursor, centered as one group on an Iron Gall Ink tile with a 22.5% corner radius.</li>
<li>Ink #1C2340 and Page White #FAFAF7. Inter for the interface, Margin Blue #3B4FA8 for links, focus and buttons.</li></ul>
<p style="margin-top:4mm">The app names are working names until the trademark check is done.</p></div>
<div><table><tr><th></th><th>Script</th><th>Manuscript</th><th>Book</th></tr>
<tr><td>For</td><td>Screenplays</td><td>Novels and long work</td><td>Print books and ebooks</td></tr>
<tr><td>Icon letter</td><td>S</td><td>M</td><td>B</td></tr>
<tr><td>Cursor</td><td>Brass bar</td><td>Red page stack</td><td>Green ribbon bookmark</td></tr>
<tr><td>Color</td>{"".join(f'<td><span style="display:inline-block;width:3mm;height:3mm;border-radius:.6mm;background:{a["color"]};vertical-align:-.3mm"></span> {a["cname"]} {a["color"]}</td>' for a in APPS.values())}</tr>
<tr><td>Text-safe</td>{"".join(f'<td>{a["text"]}</td>' for a in APPS.values())}</tr></table>
<div class="tile l" style="margin-top:6mm;height:60mm">{img(p("05. Suite","wordsmith-suite-overview.png"),h="100%",w="100%")}</div></div></div>''','',FOOT))
for k,a in APPS.items():
    D=a['dir']; slug=a['name'].lower().replace(' ','-')
    # intro page
    pg.append(page(f'''<div class="kick" style="color:{a["color"]}">{a["what"]}</div>
<div style="height:21mm;margin:3mm 0 9mm">{img(p(D,"Logo",f"{slug}-wordmark-ink.svg"),h="100%",style="max-width:100%")}</div>
<div class="cols c2" style="flex:none"><div><h3>The cursor</h3><p>{a["cursor"]}</p></div>
<div><h3>In the product</h3><ul>{"".join(f"<li>{x}</li>" for x in a["product"])}</ul></div></div>
<div style="display:flex;gap:6mm;margin-top:auto;margin-bottom:5mm;height:58mm">
<div class="tile d" style="flex:1;justify-content:flex-start;padding:0 12mm">{img(p(D,"Logo",f"{slug}-stacked-paper.svg"),h="30mm")}</div>
<div style="text-align:center">{img(p(D,"App icon","icon-512.png"),h="56mm")}<div class="cap">App icon</div></div></div>''','',FOOT))
    # logos page
    L=lambda f:p(D,'Logo',f)
    pg.append(page(f'''<div class="kick">{a["name"]} · Logos</div><h2>Logo set</h2>
<div class="cols" style="grid-template-columns:1.6fr 1.6fr 1fr;grid-template-rows:1fr 1fr 1fr;gap:4mm">
<div><div class="tile l" style="height:24mm">{img(L(f"{slug}-wordmark-ink.svg"),w="92%")}</div><div class="cap">{slug}-wordmark-ink.svg · light grounds</div></div>
<div><div class="tile d" style="height:24mm">{img(L(f"{slug}-wordmark-paper.svg"),w="92%")}</div><div class="cap">{slug}-wordmark-paper.svg · dark grounds</div></div>
<div><div class="tile l" style="height:24mm">{img(L(a["mark"]+"-ink.svg"),h="15mm")}</div><div class="cap">{a["mark"]}-ink.svg</div></div>
<div><div class="tile l" style="height:24mm">{img(L(f"{slug}-wordmark-mono-ink.svg"),w="92%")}</div><div class="cap">-wordmark-mono-ink.svg · one color</div></div>
<div><div class="tile d" style="height:24mm">{img(L(f"{slug}-wordmark-mono-paper.svg"),w="92%")}</div><div class="cap">-wordmark-mono-paper.svg</div></div>
<div><div class="tile d" style="height:24mm">{img(L(a["mark"]+"-paper.svg"),h="15mm")}</div><div class="cap">{a["mark"]}-paper.svg</div></div>
<div><div class="tile l" style="height:24mm">{img(L(f"{slug}-stacked-ink.svg"),h="17mm")}</div><div class="cap">-stacked-ink.svg · narrow spaces</div></div>
<div><div class="tile l" style="height:24mm">{img(L(f"{slug}-endorsed-ink.svg"),w="88%")}</div><div class="cap">-endorsed-ink.svg · with the Wordsmith &amp; Ink line</div></div>
<div><div class="tile d" style="height:24mm">{img(L(f"{slug}-stacked-paper.svg"),h="17mm")}</div><div class="cap">-stacked-paper.svg</div></div>
</div><p style="margin-top:3mm;font-size:8.5pt;color:{SLATE}">Clear space: the height of the capitals on every side. Minimum size: wordmark {"160 px / 40 mm" if k=="manuscript" else "140 px / 35 mm"}; below that, use the mark. All logos are outlined SVG paths; no font needed.</p>''','',FOOT))
    # icon + palette page
    I=lambda f:p(D,'App icon',f)
    sizes=''.join(f'<div style="text-align:center">{img(I(f"icon-{s}.png"),h=f"{max(s/1024*40,4.2):.1f}mm")}<div class="cap">{s}</div></div>' for s in [1024,512,256,128,64,48,32,16])
    pg.append(page(f'''<div class="kick">{a["name"]} · App icon and color</div><h2>App icon</h2>
<div style="display:flex;gap:6mm;align-items:flex-end">{sizes}<div style="text-align:center;margin-left:6mm">{img(I("icon-macos-1024.png"),h="40mm")}<div class="cap">macOS grid</div></div></div>
<p style="font-size:8.5pt;color:{SLATE};margin-top:3mm">Master: <code>{slug}-icon.svg</code>, PNGs 1024 to 64. Small sizes (48, 32, 16) use <code>{slug}-icon-small.svg</code> with a larger letter. macOS: <code>{slug}-icon-macos.svg</code> on the 824 px grid; build the .icns from <code>icon-macos-1024.png</code>. Windows: <code>{slug.replace("wordsmith-","wordsmith-")}.ico</code>. Web: <code>favicon.svg</code>.</p>
<h2 style="margin-top:7mm">Palette</h2>{swatches(path(D,"Palette",f"{slug}.json"))}
<p style="font-size:8.5pt;color:{SLATE};margin-top:3mm">{a["cname"]} is a spice: one thing per screen, usually the cursor itself. Use {a["text"]} for text. Palette files for design apps in <code>palette/</code>: .ase, .gpl, .css, .json and a swatch card. Full design tokens with dark values: <code>tokens.json</code>.</p>''','',FOOT))
# typography + files
pg.append(page(f'''<div class="kick">Shared</div><h2>Typography and files</h2><div class="cols c2"><div>
<div style="font:700 26pt 'Courier Prime'">Courier Prime Bold</div><p>Display: logos, title screens, headings of a few words in sentence case. SIL OFL 1.1.</p>
<div style="font:500 26pt Inter;margin-top:6mm">Inter 400, 500, 600</div><p>Interface: menus, panels, buttons, docs, website body copy. SIL OFL 1.1.</p>
<div style="font:400 12pt 'Courier Prime';margin-top:6mm;background:#fff;border:.3mm solid #E4E5EC;padding:5mm;border-radius:2mm">INT. WRITING ROOM - NIGHT<br><br>A cursor blinks at the end of a line.</div>
<p style="margin-top:3mm">Never set long paragraphs in Courier outside a script or manuscript page.</p></div>
<div><table><tr><th>Folder</th><th>What is in it</th></tr>
<tr><td><code>pdfs/</code></td><td>This document and the Wordsmith &amp; Ink brand guidelines</td></tr>
<tr><td><code>wordsmith-and-ink/</code></td><td>The parent brand: logo, app-icon, lockups, palette, tokens.json</td></tr>
<tr><td><code>wordsmith-script/</code></td><td>production (ready-to-use set with README), logo, app-icon, palette, tokens.json</td></tr>
<tr><td><code>wordsmith-manuscript/</code></td><td>production (ready-to-use set with README), logo, app-icon, palette, tokens.json</td></tr>
<tr><td><code>wordsmith-book/</code></td><td>production (ready-to-use set with README), logo, app-icon, palette, tokens.json</td></tr>
<tr><td><code>suite/</code></td><td>The suite brand guide (Markdown) and the overview image</td></tr>
</table>
<p style="margin-top:4mm">Logos, icons and these PDFs are rebuilt by <code>brand/source/build.py</code> if a name changes. They need the Courier Prime and Inter font files (both SIL OFL 1.1).</p>
<p>The apps' code is open source; the names and logos are the Foundation's trademarks. They may be used unmodified to refer to the project, not for forks or other products.</p></div></div>''','',FOOT))
open(os.path.join(S,'products.html'),'w').write(doc('Wordsmith apps: product assets',pg))
