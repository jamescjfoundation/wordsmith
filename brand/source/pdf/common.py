import os, json, html
HERE=os.path.dirname(os.path.abspath(__file__))
K=os.environ.get('WORDSMITH_BRAND',os.path.abspath(os.path.join(HERE,'..','..')))   # the brand/ folder the pages show
S=os.environ.get('WORDSMITH_PDF_OUT',os.path.join(K,'build','pdf'))                 # where the HTML (and PDFs) go
F=os.environ.get('WORDSMITH_FONT_DIR',os.path.join(HERE,'..','fonts'))
os.makedirs(S,exist_ok=True)
def ff(n):
    """font file by name, .ttf or .otf"""
    t=os.path.join(F,n+'.ttf'); return t if os.path.exists(t) else os.path.join(F,n+'.otf')
# the kit's drive folder names, as they are named in this repository
DIRS={'00. PDFs':'pdfs','01. Wordsmith & Ink':'wordsmith-and-ink','02. Wordsmith Script':'wordsmith-script',
      '03. Wordsmith Manuscript':'wordsmith-manuscript','04. Wordsmith Book':'wordsmith-book','05. Suite':'suite',
      'Logo':'logo','App icon':'app-icon','Lockups':'lockups','Palette':'palette'}
INK='#1C2340'; PAPER='#FAFAF7'; NIGHT='#12162B'; SLATE='#5A6080'; BLUE='#3B4FA8'
APPS={'script':dict(dir='02. Wordsmith Script',name='Wordsmith Script',short='Script',color='#B8862B',cname='Brad Brass',text='#8A6418',letter='S',
        what='Screenplays',cursor='A solid brass bar, as tall as the capitals and 0.15 em wide, sitting on the baseline. It comes from the brass brads that bind a script. It may blink in motion pieces (530 ms on, 530 ms off, no fades); everywhere else it is solid.',
        product=['The script page is Courier Prime 12 pt, 10 characters and 6 lines to the inch.','The in-app text cursor is brass.','Revision colors tint revised pages and margins; story-board beats reuse them.'],
        mark='wordsmith-mark'),
      'manuscript':dict(dir='03. Wordsmith Manuscript',name='Wordsmith Manuscript',short='Manuscript',color='#D24B3E',cname='Card Red',text='#A8322A',letter='M',
        what='Novels and long work',cursor='A stack of three sheets: the front sheet is the usual bar, two more step back behind it, each 0.095 em right and 0.05 em higher. On light grounds the back sheets fade toward the ground; on dark grounds and in the icon they deepen. In one color they become slivers with a small gap. It never blinks.',
        product=['The in-app text cursor is a normal thin bar in Card Red; the page stack is for the logo, icon and brand moments.','The writing page defaults to standard manuscript format: Courier Prime 12 pt, double-spaced, 1-inch margins.','The corkboard puts white index cards on cork. Card Red marks a card\'s rule line, label dots and status stamps, never errors.'],
        mark='wordsmith-manuscript-mark'),
      'book':dict(dir='04. Wordsmith Book',name='Wordsmith Book',short='Book',color='#2E9473',cname='Ribbon Green',text='#1F7358',letter='B',
        what='Print books and ebooks',cursor='A ribbon bookmark: a bar 0.15 em wide that starts at the height of the capitals and drops 0.30 em below the baseline, ending in a V notch. The writing is finished; keep your place. It never blinks; it may drop into place once (300 ms) when an export finishes.',
        product=['Brand fonts stay in the app\'s chrome. Book previews always use the fonts of the chosen book design, never Courier Prime or Inter.','Print previews show the page on white or cream stock, fixed in both themes.','Green also marks a passed preflight check, always with text and a check icon.'],
        mark='wordsmith-book-mark')}
def path(*a): return os.path.join(K,*[DIRS.get(x,x) for x in a])
def p(*a): return 'file://'+path(*a)
CSS=f'''
@font-face{{font-family:"Courier Prime";font-weight:700;src:url(file://{ff('CourierPrime-700')})}}
@font-face{{font-family:"Courier Prime";font-weight:400;src:url(file://{ff('CourierPrime-400')})}}
@font-face{{font-family:"Inter";font-weight:400;src:url(file://{ff('Inter-400')})}}
@font-face{{font-family:"Inter";font-weight:500;src:url(file://{ff('Inter-500')})}}
@font-face{{font-family:"Inter";font-weight:600;src:url(file://{ff('Inter-600')})}}
@page{{size:297mm 210mm;margin:0}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:Inter;color:{INK};-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.pg{{width:297mm;height:210mm;padding:16mm 18mm 14mm;position:relative;overflow:hidden;background:{PAPER};page-break-after:always;display:flex;flex-direction:column}}
.pg.dark{{background:{INK};color:{PAPER}}} .pg.night{{background:{NIGHT}}}
.foot{{position:absolute;left:18mm;right:18mm;bottom:8mm;display:flex;justify-content:space-between;font-size:7.5pt;color:{SLATE}}}
.dark .foot{{color:#9EA3BD}}
.kick{{font:600 8pt Inter;letter-spacing:.12em;text-transform:uppercase;color:{SLATE};margin-bottom:3mm}}
.dark .kick{{color:#9EA3BD}}
h1{{font:700 30pt/1.1 "Courier Prime";margin-bottom:5mm}}
h2{{font:700 21pt/1.15 "Courier Prime";margin-bottom:4mm}}
h3{{font:600 10.5pt Inter;margin:0 0 1.5mm}}
p,li{{font-size:9.5pt;line-height:1.5;color:#2C3352}}
.dark p,.dark li{{color:#D6D8E4}}
p+p{{margin-top:2mm}} ul{{padding-left:4.5mm}} li{{margin-bottom:1mm}}
.cols{{display:grid;gap:8mm;flex:1;min-height:0}}
.c2{{grid-template-columns:1fr 1fr}} .c3{{grid-template-columns:1fr 1fr 1fr}} .c4{{grid-template-columns:repeat(4,1fr)}}
.tile{{border-radius:3mm;display:flex;align-items:center;justify-content:center;padding:6mm;position:relative}}
.tile.l{{background:#FFFFFF;border:.3mm solid #E4E5EC}} .tile.d{{background:{INK}}} .tile.n{{background:{NIGHT}}}
.cap{{font-size:7.5pt;color:{SLATE};margin-top:1.5mm;font-family:"Courier Prime"}}
.dark .cap{{color:#9EA3BD}}
.sw{{border-radius:2mm;overflow:hidden;border:.3mm solid #E4E5EC;background:#fff}}
.sw .chip{{height:22mm}} .sw .t{{padding:2.5mm 3mm;font-size:7.5pt;line-height:1.45}} .sw b{{font:700 9pt "Courier Prime";display:block}}
table{{border-collapse:collapse;width:100%;font-size:8.5pt}} td,th{{text-align:left;padding:1.6mm 2mm;border-bottom:.25mm solid #E4E5EC;vertical-align:top}} th{{font-weight:600;color:{SLATE};font-size:7.5pt;text-transform:uppercase;letter-spacing:.06em}}
code{{font-family:"Courier Prime";font-size:8.5pt}}
.dont{{border:.3mm solid #E4E5EC;border-radius:2mm;background:#fff;height:26mm;display:flex;align-items:center;justify-content:center;position:relative;overflow:hidden}}
.dont:after{{content:"";position:absolute;inset:0;background:linear-gradient(to top right,transparent calc(50% - .4mm),#B3261E calc(50% - .4mm),#B3261E calc(50% + .4mm),transparent calc(50% + .4mm));opacity:.85}}
'''
def page(body,cls='',foot=''): return f'<section class="pg {cls}">{body}<div class="foot"><span>{foot}</span><span class="pn"></span></div></section>'
def doc(title,pages):
    return f'<!doctype html><html><head><meta charset="utf-8"><title>{html.escape(title)}</title><style>{CSS}</style></head><body>{"".join(pages)}</body></html>'
def swatches(jsonpath,cols=None):
    C=json.load(open(jsonpath)); n=cols or len(C)
    return f'<div class="cols" style="grid-template-columns:repeat({n},1fr);flex:none;gap:4mm">'+''.join(
        f'<div class="sw"><div class="chip" style="background:{c["hex"]}"></div><div class="t"><b>{html.escape(c["name"])}</b>{c["hex"]} · RGB {" ".join(map(str,c["rgb"]))}<br><span style="color:{SLATE}">{html.escape(c["use"])}</span></div></div>' for c in C)+'</div>'
def img(src,h=None,w=None,style=''):
    st=(f'height:{h};' if h else '')+(f'width:{w};' if w else '')+'object-fit:contain;'+style
    return f'<img src="{src}" style="{st}">'
