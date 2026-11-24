"""Wordsmith Script logo and icon builder. Usage: python3 buildc.py <outdir>
Script keeps its own builder: its mark is boxed to the capital height. Its palette is written by build.py."""
import sys, os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from text import text_path, fit_svg, make_ico
import cairosvg
INK='#1C2340'; PAPER='#FAFAF7'; BRASS='#B8862B'
F='CourierPrime-700.ttf'; CAP=1187/2048
OUT=sys.argv[1]
for d in ('logo','app-icon'): os.makedirs(f'{OUT}/{d}',exist_ok=True)
def svg(w,h,body,title):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.1f} {h:.1f}" width="{w:.0f}" height="{h:.0f}" role="img" aria-label="{title}"><title>{title}</title>{body}</svg>\n'
def save(n,s):
    open(f'{OUT}/{n}','w').write(s)
    if n.startswith('logo/'): fit_svg(f'{OUT}/{n}')

def typed(s, size, x, base, fg, cur, cursor=True):
    """text + brass cursor. returns body, right edge"""
    d,a=text_path(s,F,size,x,base)
    body=f'<path fill="{fg}" d="{d}"/>'
    right=x+a
    if cursor:
        cw=size*0.153; gap=size*0.03
        cx=x+a+gap; top=base-size*CAP
        body+=f'<rect fill="{cur}" x="{cx:.2f}" y="{top:.2f}" width="{cw:.2f}" height="{size*CAP+size*0.02:.2f}"/>'
        right=cx+cw
    return body,right

def block(lines, size, fg, cur, pad=0, lead=1.05, center=False):
    # lines: list of strings; cursor on last
    asc=size*CAP; widths=[]
    for i,l in enumerate(lines):
        _,r=typed(l,size,0,0,fg,cur,cursor=(i==len(lines)-1)); widths.append(r)
    W=max(widths); body=''
    for i,l in enumerate(lines):
        base=pad+asc+i*size*lead
        x=pad+((W-widths[i])/2 if center else 0)
        b,_=typed(l,size,x,base,fg,cur,cursor=(i==len(lines)-1)); body+=b
    H=asc+(len(lines)-1)*size*lead+size*0.22  # room for descenders (p in Script)
    return pad*2+W, pad*2+H, body

variants=[('ink',INK,BRASS),('paper',PAPER,BRASS),('mono-ink',INK,INK),('mono-paper',PAPER,PAPER)]
for nm,fg,cur in variants:
    w,h,b=block(['Wordsmith Script'],100,fg,cur); save(f'logo/wordsmith-script-wordmark-{nm}.svg',svg(w,h,b,'Wordsmith Script'))
for nm,fg,cur in variants[:2]:
    w,h,b=block(['Wordsmith','Script'],100,fg,cur); save(f'logo/wordsmith-script-stacked-{nm}.svg',svg(w,h,b,'Wordsmith Script'))
    w,h,b=block(['S'],400,fg,cur); save(f'logo/wordsmith-mark-{nm}.svg',svg(w,400*CAP+8,b,'Wordsmith mark'))

def icon(S=1024, glyph=640):
    _,r=typed('S',glyph,0,0,PAPER,BRASS)
    x=(S-r)/2; base=S/2+glyph*CAP/2
    b,_=typed('S',glyph,x,base,PAPER,BRASS)
    return f'<rect width="{S}" height="{S}" rx="{S*0.225:.1f}" fill="{INK}"/>'+b
save('app-icon/wordsmith-script-icon.svg',svg(1024,1024,icon(),'Wordsmith Script app icon'))
save('app-icon/wordsmith-script-icon-small.svg',svg(1024,1024,icon(glyph=720),'Wordsmith Script app icon, small sizes'))
save('app-icon/favicon.svg',svg(1024,1024,icon(glyph=720),'Wordsmith Script'))
save('app-icon/wordsmith-script-icon-macos.svg',svg(1024,1024,f'<g transform="translate(100 100) scale({824/1024})">{icon()}</g>','Wordsmith Script app icon (macOS grid)'))
for s in [1024,512,256,128,64]:
    cairosvg.svg2png(url=f'{OUT}/app-icon/wordsmith-script-icon.svg',write_to=f'{OUT}/app-icon/icon-{s}.png',output_width=s,output_height=s)
for s in [48,32,16]:
    cairosvg.svg2png(url=f'{OUT}/app-icon/wordsmith-script-icon-small.svg',write_to=f'{OUT}/app-icon/icon-{s}.png',output_width=s,output_height=s)
cairosvg.svg2png(url=f'{OUT}/app-icon/wordsmith-script-icon-macos.svg',write_to=f'{OUT}/app-icon/icon-macos-1024.png',output_width=1024,output_height=1024)
make_ico(f'{OUT}/app-icon','wordsmith-script.ico')
