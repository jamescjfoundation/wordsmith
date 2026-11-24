from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
import os
# Courier Prime and Inter (both SIL OFL 1.1). fetch_fonts.py puts the exact versions the kit was drawn with here.
FD=os.environ.get('WORDSMITH_FONT_DIR', os.path.join(os.path.dirname(os.path.abspath(__file__)),'fonts'))+'/'
_c={}
def font(n):
    """n is a name like 'Inter-500.ttf'; a .otf with the same stem is used when there is no .ttf."""
    if n not in _c:
        path=FD+n
        if not os.path.exists(path) and os.path.exists(os.path.splitext(path)[0]+'.otf'): path=os.path.splitext(path)[0]+'.otf'
        if not os.path.exists(path): raise SystemExit(f'Font {n} not found in {FD}. Run: python3 brand/source/fetch_fonts.py')
        _c[n]=TTFont(path)
    return _c[n]
def text_path(s, fname, size, x=0, y=0, tracking=0.0):
    """returns (d, advance_width). y = baseline. tracking in em."""
    f=font(fname); gs=f.getGlyphSet(); cmap=f.getBestCmap(); upm=f['head'].unitsPerEm
    sc=size/upm; pen=SVGPathPen(gs); cx=0
    kern={}
    for i,ch in enumerate(s):
        gn=cmap[ord(ch)]
        tp=TransformPen(pen,(sc,0,0,-sc,x+cx,y))
        gs[gn].draw(tp)
        cx+=gs[gn].width*sc + (tracking*size if i<len(s)-1 else 0)
    return pen.getCommands(), cx
def metrics(fname,size):
    f=font(fname); upm=f['head'].unitsPerEm; os2=f['OS/2']
    return os2.sCapHeight*size/upm, os2.sxHeight*size/upm

def fit_svg(path, scale=8):
    """Set a logo SVG's viewBox to the real ink bounds of everything in it.
    Letters with ascenders (d, h, i, k, t), the ampersand and the cursors reach past
    the capital height, so a box built from the capital height crops them."""
    import re, io, cairosvg, numpy as np
    from PIL import Image
    s=open(path).read()
    m=re.match(r'(<svg[^>]*?)viewBox="([^"]+)" width="[^"]+" height="[^"]+"(.*?>)(.*)</svg>\s*$',s,re.S)
    head,vb,rest,inner=m.groups(); x0,y0,w,h=map(float,vb.split())
    px,py=w*0.5,h*0.5   # render with a generous margin round the old box
    probe=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0-px} {y0-py} {w+2*px} {h+2*py}">{inner}</svg>'
    W=int((w+2*px)*scale); H=int((h+2*py)*scale)
    a=np.array(Image.open(io.BytesIO(cairosvg.svg2png(bytestring=probe.encode(),output_width=W,output_height=H))))[:,:,3]
    ys,xs=np.nonzero(a>0)
    nx0=x0-px+xs.min()/scale; nx1=x0-px+(xs.max()+1)/scale
    ny0=y0-py+ys.min()/scale; ny1=y0-py+(ys.max()+1)/scale
    # union with the old box, so the spacing the builder set (descender room, cursor edge) stays
    nx0=min(nx0,x0); ny0=min(ny0,y0); nx1=max(nx1,x0+w); ny1=max(ny1,y0+h)
    nw,nh=nx1-nx0,ny1-ny0
    out=f'{head}viewBox="{nx0:.2f} {ny0:.2f} {nw:.2f} {nh:.2f}" width="{nw:.0f}" height="{nh:.0f}"{rest}{inner}</svg>\n'
    open(path,'w').write(out)

def make_ico(folder, name, sizes=(16,32,48,64,128,256)):
    """Windows icon from the icon-<size>.png files in folder. Uses ImageMagick when it is installed
    (as the kit was made), otherwise Pillow."""
    import shutil, subprocess
    pngs=[f'icon-{s}.png' for s in sizes]
    tool=shutil.which('magick') or shutil.which('convert')
    if tool:
        subprocess.run([tool,*pngs,name],cwd=folder,check=True); return
    from PIL import Image
    imgs=[Image.open(os.path.join(folder,p)).convert('RGBA') for p in pngs]
    imgs[-1].save(os.path.join(folder,name),format='ICO',sizes=[i.size for i in imgs],append_images=imgs[:-1])
