"""Wordsmith & Ink parent brand builder. Usage: python3 buildink.py <outdir>
Needs the product builder (buildp.py, text.py) beside it and the fonts (see text.py).
Usually run through build.py. The parent mark is one color: the name
typed in Courier Prime Bold, and a cursor that lets fall a drop of ink."""
import sys, os, json
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import buildp as B
from text import text_path, fit_svg, make_ico
import cairosvg
from xml.sax.saxutils import escape
_svg=B.svg
B.svg=lambda w,h,body,title:_svg(w,h,body,escape(title,{'"':'&quot;'}))
INK,PAPER,CAP=B.INK,B.PAPER,B.CAP
SLATE='#5A6080'; SLATE_DARK='#9EA3BD'
NAME='Wordsmith & Ink'
def drop_cursor(x,base,size,col,gap=0.06):
    """the usual bar (cap height, 0.153 em), and under it a falling drop: point up, round below"""
    cw=size*0.153; top=base-size*CAP; h=size*CAP+size*0.02
    r=size*0.092; cx=x+cw/2; tip=base+size*0.02+size*gap; cy=tip+size*0.20; k=0.5523*r
    d=(f'M{cx:.2f},{tip:.2f}C{cx+r*0.15:.2f},{tip+size*0.06:.2f} {cx+r:.2f},{cy-r*1.05:.2f} {cx+r:.2f},{cy:.2f}'
       f'C{cx+r:.2f},{cy+k:.2f} {cx+k:.2f},{cy+r:.2f} {cx:.2f},{cy+r:.2f}'
       f'C{cx-k:.2f},{cy+r:.2f} {cx-r:.2f},{cy+k:.2f} {cx-r:.2f},{cy:.2f}'
       f'C{cx-r:.2f},{cy-r*1.05:.2f} {cx-r*0.15:.2f},{tip+size*0.06:.2f} {cx:.2f},{tip:.2f}Z')
    return f'<rect fill="{col}" x="{x:.2f}" y="{top:.2f}" width="{cw:.2f}" height="{h:.2f}"/><path fill="{col}" d="{d}"/>', cw, cy+r-base
def typed(s,size,x,base,fg,cursor=True,font=B.F):
    d,a=text_path(s,font,size,x,base); body=f'<path fill="{fg}" d="{d}"/>'
    if not cursor: return body,x+a,0
    b,cw,dr=drop_cursor(x+a+size*0.03,base,size,fg); return body+b,x+a+size*0.03+cw,dr
def block(lines,size,fg,lead=1.05,center=False):
    asc=size*CAP; ws=[typed(l,size,0,0,fg,i==len(lines)-1)[1] for i,l in enumerate(lines)]
    W=max(ws); body=''; drop=0
    for i,l in enumerate(lines):
        b,_,dr=typed(l,size,(W-ws[i])/2 if center else 0,asc+i*size*lead,fg,i==len(lines)-1); body+=b; drop=dr
    return W,asc+(len(lines)-1)*size*lead+drop,body
def icon(S=1024,glyph=640):
    _,r,dr=typed('&',glyph,0,0,PAPER); x=(S-r)/2; h=glyph*CAP+dr; base=S/2-h/2+glyph*CAP
    return f'<rect width="{S}" height="{S}" rx="{S*0.225:.1f}" fill="{INK}"/>'+typed('&',glyph,x,base,PAPER)[0]
def line(s,size,x,base,col,font='Inter-500.ttf'):
    d,a=text_path(s,font,size,x,base); return f'<path fill="{col}" d="{d}"/>',a
PALETTE=[("Iron Gall Ink","#1C2340","The mark, icon tile, spines, title pages"),("Page White","#FAFAF7","Pages, reversed mark"),
 ("Night","#12162B","Dark grounds, website dark theme"),("Slate","#5A6080","Secondary text, endorsement lines"),("Margin Blue","#3B4FA8","Links, buttons, focus"),
 ("Brad Brass","#B8862B","Wordsmith Script"),("Card Red","#D24B3E","Wordsmith Manuscript"),("Ribbon Green","#2E9473","Wordsmith Book")]
APPS=[('script','Wordsmith Script'),('manuscript','Wordsmith Manuscript'),('book','Wordsmith Book')]
def build(OUT):
    for d in ('logo','app-icon','palette','lockups'): os.makedirs(f'{OUT}/{d}',exist_ok=True)
    def save(n,s):
        open(f'{OUT}/{n}','w').write(s)
        if n.startswith('logo/') or 'endorsed' in n: fit_svg(f'{OUT}/{n}')
    for nm,fg in (('ink',INK),('paper',PAPER)):
        w,h,b=block([NAME],100,fg); save(f'logo/wordsmith-and-ink-wordmark-{nm}.svg',B.svg(w,h,b,NAME))
        w,h,b=block(['Wordsmith','& Ink'],100,fg); save(f'logo/wordsmith-and-ink-stacked-{nm}.svg',B.svg(w,h,b,NAME))
        w,h,b=block(['&'],400,fg); save(f'logo/wordsmith-and-ink-mark-{nm}.svg',B.svg(w,h,b,NAME+' mark'))
        # imprint lockup: stacked, centred, for title pages and spines' foot
        w,h,b=block(['Wordsmith','& Ink'],100,fg,center=True); save(f'logo/wordsmith-and-ink-imprint-{nm}.svg',B.svg(w,h,b,NAME))
        # foundation line in text under the wordmark (never merged into it)
        w,h,b=block([NAME],100,fg); sub=SLATE if fg==INK else SLATE_DARK
        lb,la=line('A project of The James C. J. Foundation',30,0,h+52,sub)
        save(f'logo/wordsmith-and-ink-foundation-{nm}.svg',B.svg(max(w,la),h+60,b+lb,NAME+', a project of The James C. J. Foundation'))
    save('app-icon/wordsmith-and-ink-icon.svg',B.svg(1024,1024,icon(),NAME+' icon'))
    save('app-icon/wordsmith-and-ink-icon-small.svg',B.svg(1024,1024,icon(glyph=700),NAME+' icon, small sizes'))
    save('app-icon/favicon.svg',B.svg(1024,1024,icon(glyph=700),NAME))
    save('app-icon/wordsmith-and-ink-icon-macos.svg',B.svg(1024,1024,f'<g transform="translate(100 100) scale({824/1024})">{icon()}</g>',NAME+' icon (macOS grid)'))
    for s in [1024,512,256,128,64]: cairosvg.svg2png(url=f'{OUT}/app-icon/wordsmith-and-ink-icon.svg',write_to=f'{OUT}/app-icon/icon-{s}.png',output_width=s,output_height=s)
    for s in [48,32,16]: cairosvg.svg2png(url=f'{OUT}/app-icon/wordsmith-and-ink-icon-small.svg',write_to=f'{OUT}/app-icon/icon-{s}.png',output_width=s,output_height=s)
    cairosvg.svg2png(url=f'{OUT}/app-icon/wordsmith-and-ink-icon-macos.svg',write_to=f'{OUT}/app-icon/icon-macos-1024.png',output_width=1024,output_height=1024)
    make_ico(f'{OUT}/app-icon','wordsmith-and-ink.ico')
    B.write_palette(NAME,'wordsmith-and-ink',PALETTE,f'{OUT}/palette/')
    # endorsed product lockups: product wordmark, and under it "a Wordsmith & Ink app" in Inter
    for key,pname in APPS:
        p=B.PRODUCTS[key]
        for nm,fg in (('ink',INK),('paper',PAPER)):
            B.GROUND='light' if fg==INK else 'dark'
            w,h,b=B.block([pname],100,fg,p['cursor'],p['shape']); sub=SLATE if fg==INK else SLATE_DARK
            lb,la=line('a Wordsmith & Ink app',30,0,h+50,sub)
            save(f'lockups/{p["name"].lower().replace(" ","-")}-endorsed-{nm}.svg',B.svg(max(w,la),h+58,b+lb,pname+', a Wordsmith & Ink app'))
    # family lockup: parent wordmark over the three app icons
    B.GROUND='dark'
    for nm,fg,bg in (('ink',INK,PAPER),('paper',PAPER,'#12162B')):
        W=1200; w,h,b=block([NAME],100,fg); x0=(W-w)/2
        body=f'<rect width="{W}" height="520" fill="{bg}"/><g transform="translate({x0:.1f},60)">{b}</g>'
        for i,(key,pname) in enumerate(APPS):
            cx=W/2+(i-1)*300; body+=f'<g transform="translate({cx-90:.1f},250) scale({180/1024})">{B.icon(B.PRODUCTS[key])}</g>'
            lb,la=line(pname.replace('Wordsmith ',''),28,0,0,fg if fg==INK else PAPER,'Inter-600.ttf')
            body+=f'<g transform="translate({cx-la/2:.1f},475)">{lb}</g>'
        save(f'lockups/wordsmith-and-ink-family-{nm}.svg',B.svg(W,520,body,NAME+' and its apps'))
        cairosvg.svg2png(url=f'{OUT}/lockups/wordsmith-and-ink-family-{nm}.svg',write_to=f'{OUT}/lockups/wordsmith-and-ink-family-{nm}.png',output_width=2400)
    tokens={"name":NAME,"version":"1.0","date":"2026-11-24",
      "color":{"brand-ink":{"value":"#1C2340","note":"The mark, icon tile. Fixed in both themes"},"brand-paper":{"value":"#FAFAF7","note":"Pages, reversed mark. Fixed"},
        "surface-page":{"light":"#FAFAF7","dark":"#12162B"},"surface-raised":{"light":"#FFFFFF","dark":"#1C2340"},
        "ink":{"light":"#1C2340","dark":"#E9EAF2"},"ink-muted":{"light":"#5A6080","dark":"#9EA3BD"},"accent":{"light":"#3B4FA8","dark":"#9AABF2"},
        "product":{"script":"#B8862B","manuscript":"#D24B3E","book":"#2E9473"}},
      "type":{"display":"Courier Prime Bold (OFL 1.1)","interface":"Inter 400/500/600 (OFL 1.1)"},
      "mark":{"cursor":"bar 0.153 em wide, cap height; a drop falls below it, 0.06 em gap, 0.20 em tall to its centre, radius 0.092 em","color":"one color only: ink on light grounds, paper on dark"},
      "icon":{"letter":"&","tile":"brand-ink, corner radius 22.5%","glyph":"Page White"}}
    json.dump(tokens,open(f'{OUT}/tokens.json','w'),indent=2)
if __name__=='__main__': build(sys.argv[1])
