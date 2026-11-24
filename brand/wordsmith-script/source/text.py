from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
import os
FD=os.environ.get('WORDSMITH_FONT_DIR', os.path.join(os.path.dirname(os.path.abspath(__file__)),'fonts'))+'/'  # Courier Prime, Inter TTFs (OFL) from Google Fonts
_c={}
def font(n):
    if n not in _c: _c[n]=TTFont(FD+n)
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
