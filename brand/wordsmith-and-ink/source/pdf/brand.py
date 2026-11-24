from common import *
P='01. Wordsmith & Ink'; FOOT='Wordsmith &amp; Ink · Brand guidelines · v1.0 · November 2026'
L=lambda f:p(P,'Logo',f); I=lambda f:p(P,'App icon',f); X=lambda f:p(P,'Lockups',f)
pg=[]
pg.append(page(f'''<div class="kick">Brand guidelines · v1.0</div>
<div style="margin:auto 0;">{img(L("wordsmith-and-ink-wordmark-paper.svg"),w="200mm")}
<p style="font-size:12pt;margin-top:12mm;max-width:190mm">The house of the Wordsmith writing apps and a home for published writing. A project of The J. C. J. Foundation.</p></div>''','dark',FOOT))
pg.append(page(f'''<div class="kick">The idea</div><h2>A cursor, and a drop of ink</h2>
<div class="cols c2"><div>
<p>Every Wordsmith app types its own name in Courier Prime Bold and ends it with a cursor in its own color: brass for Script, red for Manuscript, green for Book.</p>
<p>Wordsmith &amp; Ink is the house they live in, and may become a publisher of finished books. It types its name the same way, and its cursor lets fall a single drop of ink. That drop is where the writing turns into something that lasts: ink on a page.</p>
<p>The house has no color of its own. It is ink on paper, or paper on ink, and nothing else. The apps bring the color; the house is what they have in common. So the parent mark prints in one color on a spine, a title page or a letterhead, and a new app joins the family without the parent changing.</p>
<h3 style="margin-top:5mm">In one line</h3><p style="font:700 12pt 'Courier Prime';color:{INK}">The apps add the color. The house is ink.</p></div>
<div style="display:flex;flex-direction:column;gap:5mm"><div class="tile l" style="flex:1">{img(L("wordsmith-and-ink-wordmark-ink.svg"),w="92%")}</div>
<div class="tile d" style="flex:1">{img(L("wordsmith-and-ink-wordmark-paper.svg"),w="92%")}</div></div></div>''','',FOOT))
pg.append(page(f'''<div class="kick">The mark</div><h2>How it is built</h2>
<div class="cols" style="grid-template-columns:1.3fr 1fr"><div class="tile l" style="padding:10mm">{img(L("wordsmith-and-ink-mark-ink.svg"),h="105mm")}</div>
<div><table><tr><th>Part</th><th>Rule</th></tr>
<tr><td>Name</td><td>"Wordsmith &amp; Ink" in Courier Prime Bold, normal spacing, with the ampersand. In running text you may write "Wordsmith and Ink"; in the logo it is always "&amp;".</td></tr>
<tr><td>Cursor bar</td><td>Right after the last letter, 0.03 em away. As tall as the capitals, 0.153 em wide, on the baseline. The same bar every Wordsmith app uses.</td></tr>
<tr><td>Drop</td><td>Centred under the bar, 0.08 em below the baseline. A teardrop, point up, round below: 0.18 em wide, its centre 0.20 em below its point.</td></tr>
<tr><td>Color</td><td>One color only. Iron Gall Ink #1C2340 on light grounds, Page White #FAFAF7 on dark. Never in a product color, never two colors.</td></tr>
<tr><td>Motion</td><td>In motion pieces the bar may blink (530 ms on, 530 ms off) and the drop may fall once and settle. Everywhere else it is still.</td></tr>
<tr><td>Icon</td><td>A paper ampersand with the drop cursor, centred as one group on an Iron Gall Ink tile with a 22.5% corner radius.</td></tr></table></div></div>''','',FOOT))
def t(f,cls,cap,h=None,w="90%"): return f'<div><div class="tile {cls}" style="height:30mm">{img(L(f),h=h,w=None if h else w)}</div><div class="cap">{cap}</div></div>'
pg.append(page(f'''<div class="kick">Logo versions</div><h2>Logo set</h2>
<div class="cols c3" style="grid-template-rows:auto auto auto;gap:5mm;flex:none">
{t("wordsmith-and-ink-wordmark-ink.svg","l","wordmark-ink.svg · primary, light grounds")}
{t("wordsmith-and-ink-wordmark-paper.svg","d","wordmark-paper.svg · dark grounds")}
{t("wordsmith-and-ink-foundation-ink.svg","l","foundation-ink.svg · with the Foundation line",w="88%")}
{t("wordsmith-and-ink-stacked-ink.svg","l","stacked-ink.svg · narrow and square spaces",h="22mm")}
{t("wordsmith-and-ink-imprint-ink.svg","l","imprint-ink.svg · title pages, centred",h="22mm")}
{t("wordsmith-and-ink-imprint-paper.svg","d","imprint-paper.svg",h="22mm")}
{t("wordsmith-and-ink-mark-ink.svg","l","mark-ink.svg · avatars, spines, watermarks",h="22mm")}
{t("wordsmith-and-ink-mark-paper.svg","d","mark-paper.svg",h="22mm")}
{t("wordsmith-and-ink-foundation-paper.svg","d","foundation-paper.svg",w="88%")}
</div><p style="margin-top:5mm;font-size:8.5pt;color:{SLATE}">The mark is already one color, so there are no separate mono files: the ink and paper versions are the mono versions. All logos are outlined SVG paths in <code>Logo/</code>; no font needed. The Foundation line is set in Inter under the logo and is never merged into it.</p>''','',FOOT))
sizes=''.join(f'<div style="text-align:center">{img(I(f"icon-{s}.png"),h=f"{max(s/1024*55,4.2):.1f}mm")}<div class="cap">{s}</div></div>' for s in [1024,512,256,128,64,48,32,16])
pg.append(page(f'''<div class="kick">Icon, clear space and size</div><h2>The icon</h2>
<div style="display:flex;gap:7mm;align-items:flex-end">{sizes}<div style="text-align:center;margin-left:4mm">{img(I("icon-macos-1024.png"),h="55mm")}<div class="cap">macOS grid</div></div></div>
<div class="cols c3" style="margin-top:9mm;flex:none"><div><h3>Clear space</h3><p>Keep the height of the capitals clear on every side of the logo. The drop counts as part of the logo.</p></div>
<div><h3>Minimum size</h3><p>Wordmark 150 px wide on screen or 38 mm in print. Below that, use the mark (ampersand and drop) down to 16 px, and the small icon under 48 px.</p></div>
<div><h3>Files</h3><p><code>App icon/</code>: master SVG and PNGs 1024 to 64, a small-size SVG for 48, 32 and 16, a macOS SVG and PNG on the 824 px grid, a Windows .ico and a favicon.</p></div></div>''','',FOOT))
D=lambda inner,cap:f'<div><div class="dont">{inner}</div><div class="cap">{cap}</div></div>'
wm=L("wordsmith-and-ink-wordmark-ink.svg")
pg.append(page(f'''<div class="kick">Use it well</div><h2>Don't</h2>
<div class="cols c4" style="flex:none;gap:5mm">
{D(f'<span style="font:700 15pt Georgia">Wordsmith &amp; Ink</span>','Retype the name in another font')}
{D(f'<span style="font:700 13pt Courier Prime;letter-spacing:.2em">WORDSMITH &amp; INK</span>','Change its case or spacing')}
{D(f'<img src="{wm}" style="width:85%;filter:invert(48%) sepia(60%) saturate(500%) hue-rotate(5deg)">','Color it in a product color')}
{D(f'<img src="{wm}" style="width:85%;transform:scaleX(1.35)">','Stretch, squash or rotate it')}
{D(f'<span style="font:700 14pt Courier Prime;color:{INK}"><span style="display:inline-block;width:2mm;height:4mm;background:{INK};vertical-align:-.5mm"></span> Wordsmith &amp; Ink</span>','Move the cursor or drop')}
{D(f'<img src="{wm}" style="width:85%;filter:drop-shadow(1mm 1mm 1mm rgba(0,0,0,.5))">','Add shadows, outlines or gradients')}
{D(f'<span style="font:700 13pt Courier Prime">Wordsmith Script</span><img src="{p(P,"Logo","wordsmith-and-ink-mark-ink.svg")}" style="height:6mm;margin-left:1mm">','Put the drop on an app name')}
{D(f'<div style="background:linear-gradient(90deg,#8a7f6a,#4a5568);width:100%;height:100%;display:flex;align-items:center;justify-content:center"><img src="{wm}" style="width:85%"></div>','Put the ink logo on a busy or mid-tone ground')}
</div>
<p style="margin-top:7mm">Write the name as Wordsmith &amp; Ink, or Wordsmith and Ink in running text. Never "W&amp;I", "WordSmith" or in capitals. The house talks like the apps do: plain, warm and short, a writer helping another writer.</p>''','',FOOT))
pg.append(page(f'''<div class="kick">Color</div><h2>Ink and paper, and the apps' colors</h2>{swatches(f"{K}/{P}/Palette/wordsmith-and-ink.json")}
<div class="cols c2" style="margin-top:7mm;flex:none"><div><h3>The house</h3><p>Iron Gall Ink and Page White are the whole of the parent brand. Night is for dark grounds and the website's dark theme, Slate for secondary text and endorsement lines, Margin Blue for links, buttons and focus.</p></div>
<div><h3>The family</h3><p>Brad Brass, Card Red and Ribbon Green belong to Script, Manuscript and Book. On a Wordsmith &amp; Ink page they appear only with their own app, as its cursor or a small mark, never on the parent logo. Palette files are in <code>Palette/</code> (.ase, .gpl, .css, .json) and the tokens in <code>tokens.json</code>.</p></div></div>
<div class="tile n" style="flex:1;margin:6mm 0 5mm;padding:0;overflow:hidden">{img(X("wordsmith-and-ink-family-paper.png"),h="100%")}</div>''','',FOOT))
pg.append(page(f'''<div class="kick">Typography</div><h2>Two typefaces</h2><div class="cols c2"><div>
<div style="font:700 46pt/1 'Courier Prime'">Aa &amp;</div><h3 style="margin-top:4mm">Courier Prime Bold · display</h3><p>The logo, title pages, headings of a few words in sentence case. SIL OFL 1.1.</p>
<div style="font:700 15pt 'Courier Prime';margin-top:6mm">The apps add the color.<br>The house is ink.</div></div>
<div><div style="font:500 46pt/1 Inter">Aa</div><h3 style="margin-top:4mm">Inter 400, 500, 600 · everything else</h3><p>Body copy, the website, documents, endorsement lines and the Foundation line. SIL OFL 1.1.</p>
<p style="margin-top:6mm;font-size:11pt">Wordsmith &amp; Ink makes free, open-source tools for writers, and may one day publish the books they help to finish.</p></div></div>
<div style="margin-top:8mm;font:700 17pt/1.5 'Courier Prime';color:{INK}">ABCDEFGHIJKLMNOPQRSTUVWXYZ &amp;<br>abcdefghijklmnopqrstuvwxyz 0123456789</div>
<div style="margin-top:3mm;font:400 13pt/1.5 Inter;color:{SLATE}">ABCDEFGHIJKLMNOPQRSTUVWXYZ abcdefghijklmnopqrstuvwxyz 0123456789</div>
<p style="margin-top:auto;margin-bottom:6mm">Books published under the imprint keep their own book design; the brand fonts appear only on the imprint page, the spine mark and the colophon.</p>''','',FOOT))
endo=''.join(f'<div><div class="tile l" style="height:26mm">{img(p(a["dir"],"Logo",a["name"].lower().replace(" ","-")+"-endorsed-ink.svg"),w="88%")}</div></div>' for a in APPS.values())
pg.append(page(f'''<div class="kick">Brand architecture</div><h2>The house and its apps</h2>
<div class="cols" style="grid-template-columns:1.15fr 1fr;flex:none"><div class="tile l" style="padding:0;overflow:hidden">{img(X("wordsmith-and-ink-family-ink.png"),w="100%")}</div>
<div><p><b>Wordsmith &amp; Ink</b> is the parent: the house that makes the apps and, later, publishes books. Each app is a <b>branded product</b> with its own name, letter, cursor and color, all from the same system.</p>
<ul style="margin-top:3mm"><li>The parent is one color; each app owns one color.</li><li>Every name is typed in Courier Prime Bold and ends in a cursor. Only the parent's cursor drops ink.</li><li>Apps say they belong to the house with a line of text, never by merging logos.</li><li>The Foundation is credited in text: "A project of The J. C. J. Foundation".</li></ul></div></div>
<h3 style="margin-top:6mm">Endorsed app logos</h3><div class="cols c3" style="flex:none;gap:5mm">{endo}</div>
<p style="font-size:8.5pt;color:{SLATE};margin-top:2mm">Files <code>-endorsed-ink.svg</code> and <code>-paper.svg</code> in each app's <code>Logo/</code> folder and in <code>Lockups/</code>. Use them on the website, in stores and in About boxes; the app icon itself stays as it is.</p>''','',FOOT))
spine=f'''<div style="width:15mm;height:120mm;background:{INK};border-radius:1mm;display:flex;flex-direction:column;align-items:center;justify-content:space-between;padding:6mm 0">
<div style="writing-mode:vertical-rl;font:400 10pt Georgia,serif;color:{PAPER}">The Title of the Book</div><img src="{L("wordsmith-and-ink-mark-paper.svg")}" style="width:7mm"></div>'''
title=f'''<div style="width:85mm;height:120mm;background:#fff;box-shadow:0 1mm 4mm rgba(0,0,0,.15);display:flex;flex-direction:column;align-items:center;padding:16mm 10mm 12mm">
<div style="font:400 17pt Georgia,serif;text-align:center">The Title<br>of the Book</div><div style="font:400 9pt Georgia,serif;margin-top:5mm;color:{SLATE}">The Author</div>
<img src="{L("wordsmith-and-ink-imprint-ink.svg")}" style="width:34mm;margin-top:auto"></div>'''
colo=f'''<div style="width:85mm;height:120mm;background:#fff;box-shadow:0 1mm 4mm rgba(0,0,0,.15);padding:14mm 10mm;font:400 7.5pt/1.6 Georgia,serif;color:#333;display:flex;flex-direction:column">
<div style="margin-top:auto">First published by Wordsmith &amp; Ink, a project of The J. C. J. Foundation.<br><br>Typeset in the book's own typeface with Wordsmith Book.</div>
<img src="{L("wordsmith-and-ink-mark-ink.svg")}" style="width:8mm;margin-top:6mm"></div>'''
pg.append(page(f'''<div class="kick">As a publisher</div><h2>On books</h2>
<div style="display:flex;gap:12mm;align-items:flex-end;justify-content:center;flex:1">
<div style="text-align:center">{spine}<div class="cap">Spine: the mark at the foot</div></div>
<div style="text-align:center">{title}<div class="cap">Title page: the imprint lockup</div></div>
<div style="text-align:center">{colo}<div class="cap">Copyright page: the mark and a line of text</div></div></div>
<p style="margin-top:6mm;margin-bottom:5mm">The book's own design rules its interior; the imprint only signs it. The publishing name is a working name until the trademark check is done.</p>''','',FOOT))
pg.append(page(f'''<div class="kick">Growing the family</div><h2>Adding an app, and the files</h2><div class="cols c2"><div>
<p>A new Wordsmith app types its own name the same way, takes its first letter for the icon, and picks a cursor color that is at least 3:1 on both ink and paper and differs from the others in lightness as well as hue. If it helps, it gets a cursor shape from its own world, like the page stack or the ribbon. The parent does not change.</p>
<p>Something that is not a writing app (a newsletter, a podcast, an event) uses the Wordsmith &amp; Ink mark with a line of text, rather than a new cursor.</p>
<h3 style="margin-top:5mm">Licensing</h3><p>The apps' code is open source. The names and logos are trademarks of The J. C. J. Foundation and may be used unmodified to refer to the project, not for forks or other products. Courier Prime and Inter are under the SIL Open Font License 1.1.</p></div>
<div><table><tr><th>In <code>01. Wordsmith &amp; Ink</code></th><th></th></tr>
<tr><td><code>Logo/</code></td><td>Wordmark, stacked, imprint, mark and Foundation-line versions, ink and paper</td></tr>
<tr><td><code>App icon/</code></td><td>SVG masters, PNGs 16 to 1024, macOS, .ico, favicon</td></tr>
<tr><td><code>Lockups/</code></td><td>The family lockup, and each app endorsed by the house</td></tr>
<tr><td><code>Palette/</code></td><td>.ase, .gpl, .css, .json and a swatch card</td></tr>
<tr><td><code>tokens.json</code></td><td>Colors, type and mark measurements</td></tr>

<tr><td><code>Source/</code></td><td><code>buildink.py</code> rebuilds everything; it uses the app builder in each app's <code>Source/</code> and the two OFL fonts</td></tr></table>
<p style="margin-top:4mm">Open item: trademark check on "Wordsmith &amp; Ink" and the app names.</p></div></div>''','',FOOT))
open(S+'/pdf/brand.html','w').write(doc('Wordsmith & Ink brand guidelines',pg))
