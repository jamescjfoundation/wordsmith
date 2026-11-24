"""Wordsmith suite product brand builder. Usage: python3 buildp.py <product> <outdir>
Products share: brand-ink tile, Courier Prime Bold wordmark, a cursor after the name.
Each product owns its cursor color, icon letter and cursor shape."""
import sys, os, struct, json
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from text import text_path, fit_svg
import cairosvg
INK='#1C2340'; PAPER='#FAFAF7'; GROUND='dark'  # set by build(): which ground the art sits on
STACK_TONES={'dark':['#D24B3E','#9C3A3A','#6B2F3C'],'light':['#D24B3E','#E8968A','#F4CBC3']}
F="CourierPrime-700.ttf"; CAP=1187/2048
PRODUCTS={
 'script':    dict(name='Wordsmith Script',    lines=['Wordsmith','Script'],    letter='S', cursor='#B8862B', shape='bar'),
 'manuscript':dict(name='Wordsmith Manuscript',lines=['Wordsmith','Manuscript'],letter='M', cursor='#D24B3E', shape='stack'),
 'book':      dict(name='Wordsmith Book',      lines=['Wordsmith','Book'],      letter='B', cursor='#2E9473', shape='ribbon'),
}
def svg(w,h,body,title):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.1f} {h:.1f}" width="{w:.0f}" height="{h:.0f}" role="img" aria-label="{title}"><title>{title}</title>{body}</svg>\n'
def cursor_shape(shape,x,base,size,col):
    cw=size*0.153; top=base-size*CAP
    if shape=='bar':
        return f'<rect fill="{col}" x="{x:.2f}" y="{top:.2f}" width="{cw:.2f}" height="{size*CAP+size*0.02:.2f}"/>', cw, 0
    if shape=='card':   # upright index card with its header rule cut out
        h=size*CAP+size*0.02; w=cw*2.4
        d=f'M{x:.2f},{top:.2f}h{w:.2f}v{h:.2f}h{-w:.2f}Z M{x+w*0.16:.2f},{top+h*0.20:.2f}h{w*0.68:.2f}v{h*0.07:.2f}h{-w*0.68:.2f}Z'
        return f'<path fill="{col}" fill-rule="evenodd" d="{d}"/>', w, 0
    if shape=='stack':  # three sheets stepping back; back sheets fade toward the ground
        h=size*CAP+size*0.02; step=cw*0.62
        out=''
        if col.upper()=='#D24B3E':
            tones=STACK_TONES[GROUND]
            for i in (2,1,0):
                out+=f'<rect fill="{tones[i]}" x="{x+i*step:.2f}" y="{top-i*step*0.55:.2f}" width="{cw:.2f}" height="{h:.2f}"/>'
        else:  # one-color: back sheets become slivers separated by a gap
            gap=cw*0.18
            out+=f'<rect fill="{col}" x="{x:.2f}" y="{top:.2f}" width="{cw:.2f}" height="{h:.2f}"/>'
            for i in (1,2):
                x0=x+(i-1)*step+cw+gap; x1=x+i*step+cw
                out+=f'<rect fill="{col}" x="{x0:.2f}" y="{top-i*step*0.55:.2f}" width="{x1-x0:.2f}" height="{h:.2f}"/>'
        return out, cw+2*step, 0
    if shape=='drafts': # two bars: drafts side by side
        h=size*CAP+size*0.02; g=cw*0.55
        return (f'<rect fill="{col}" x="{x:.2f}" y="{top:.2f}" width="{cw:.2f}" height="{h:.2f}"/>'
                f'<rect fill="{col}" x="{x+cw+g:.2f}" y="{top:.2f}" width="{cw:.2f}" height="{h:.2f}"/>'), 2*cw+g, 0
    # ribbon bookmark: bar from cap height down past the baseline, ending in a V notch
    drop=size*0.30; notch=cw*0.55; bot=base+drop
    d=f'M{x:.2f},{top:.2f}H{x+cw:.2f}V{bot:.2f}L{x+cw/2:.2f},{bot-notch:.2f}L{x:.2f},{bot:.2f}Z'
    return f'<path fill="{col}" d="{d}"/>', cw, drop
def typed(s,size,x,base,fg,cur,shape,cursor=True):
    d,a=text_path(s,F,size,x,base); body=f'<path fill="{fg}" d="{d}"/>'; right=x+a; drop=0
    if cursor:
        cx=x+a+size*0.03; b,cw,drop=cursor_shape(shape,cx,base,size,cur); body+=b; right=cx+cw
    return body,right,drop
def block(lines,size,fg,cur,shape,lead=1.05,center=False):
    asc=size*CAP; widths=[]
    for i,l in enumerate(lines):
        _,r,_=typed(l,size,0,0,fg,cur,shape,i==len(lines)-1); widths.append(r)
    W=max(widths); body=''; drop=0
    for i,l in enumerate(lines):
        base=asc+i*size*lead; x=(W-widths[i])/2 if center else 0
        b,_,dr=typed(l,size,x,base,fg,cur,shape,i==len(lines)-1); body+=b; drop=dr
    H=asc+(len(lines)-1)*size*lead+max(size*0.22,drop)
    return W,H,body
def icon(p,S=1024,glyph=640):
    _,r,drop=typed(p['letter'],glyph,0,0,PAPER,p['cursor'],p['shape'])
    x=(S-r)/2; h=glyph*CAP+drop; base=S/2-h/2+glyph*CAP
    b,_,_=typed(p['letter'],glyph,x,base,PAPER,p['cursor'],p['shape'])
    return f'<rect width="{S}" height="{S}" rx="{S*0.225:.1f}" fill="{INK}"/>'+b

def build(key,OUT,palette):
    p=PRODUCTS[key]; slug=p['name'].lower().replace(' ','-'); mark=f"wordsmith-{key}-mark" if key!='script' else 'wordsmith-mark'
    for d in ('logo','icon','palette'): os.makedirs(f'{OUT}/{d}',exist_ok=True)
    def save(n,s):
        open(f'{OUT}/{n}','w').write(s)
        if n.startswith('logo/'): fit_svg(f'{OUT}/{n}')
    cur=p['cursor']; sh=p['shape']
    V=[('ink',INK,cur),('paper',PAPER,cur),('mono-ink',INK,INK),('mono-paper',PAPER,PAPER)]
    global GROUND
    for nm,fg,c in V:
        GROUND='light' if fg==INK else 'dark'
        w,h,b=block([p['name']],100,fg,c,sh); save(f'logo/{slug}-wordmark-{nm}.svg',svg(w,h,b,p['name']))
    for nm,fg,c in V[:2]:
        GROUND='light' if fg==INK else 'dark'
        w,h,b=block(p['lines'],100,fg,c,sh); save(f'logo/{slug}-stacked-{nm}.svg',svg(w,h,b,p['name']))
        w,h,b=block([p['letter']],400,fg,c,sh); save(f'logo/{mark}-{nm}.svg',svg(w,h,b,p['name']+' mark'))
    GROUND='dark'
    save(f'icon/{slug}-icon.svg',svg(1024,1024,icon(p),p['name']+' app icon'))
    save(f'icon/{slug}-icon-small.svg',svg(1024,1024,icon(p,glyph=720 if sh=='bar' else 660),p['name']+' app icon, small sizes'))
    save('icon/favicon.svg',svg(1024,1024,icon(p,glyph=720 if sh=='bar' else 660),p['name']))
    save(f'icon/{slug}-icon-macos.svg',svg(1024,1024,f'<g transform="translate(100 100) scale({824/1024})">{icon(p)}</g>',p['name']+' app icon (macOS grid)'))
    for s in [1024,512,256,128,64]:
        cairosvg.svg2png(url=f'{OUT}/icon/{slug}-icon.svg',write_to=f'{OUT}/icon/icon-{s}.png',output_width=s,output_height=s)
    for s in [48,32,16]:
        cairosvg.svg2png(url=f'{OUT}/icon/{slug}-icon-small.svg',write_to=f'{OUT}/icon/icon-{s}.png',output_width=s,output_height=s)
    cairosvg.svg2png(url=f'{OUT}/icon/{slug}-icon-macos.svg',write_to=f'{OUT}/icon/icon-macos-1024.png',output_width=1024,output_height=1024)
    os.system(f'cd "{OUT}/icon" && convert icon-16.png icon-32.png icon-48.png icon-64.png icon-128.png icon-256.png {slug}.ico')
    write_palette(p['name'],slug,palette,f'{OUT}/palette/')

rgb=lambda h:tuple(int(h[i:i+2],16) for i in (1,3,5))
def write_palette(title,slug,C,D):
    open(D+f'{slug}.gpl','w').write(f"GIMP Palette\nName: {title}\nColumns: {len(C)}\n#\n"+"".join(f"{r:3d} {g:3d} {b:3d}\t{n}\n" for n,h,_ in C for r,g,b in [rgb(h)]))
    def nm(s):
        s=s+'\0'; return struct.pack('>H',len(s))+s.encode('utf-16-be')
    g=nm(title); blocks=struct.pack('>HI',0xC001,len(g))+g
    for n,h,_ in C:
        body=nm(n)+b'RGB '+struct.pack('>fffH',*[x/255 for x in rgb(h)],2); blocks+=struct.pack('>HI',1,len(body))+body
    blocks+=struct.pack('>HI',0xC002,0)
    open(D+f'{slug}.ase','wb').write(b'ASEF'+struct.pack('>HHI',1,0,len(C)+2)+blocks)
    s=lambda n:n.lower().replace(' ','-')
    open(D+f'{slug}.css','w').write(":root {\n"+"".join(f"  --ws-{s(n)}: {h}; /* {u} */\n" for n,h,u in C)+"}\n")
    json.dump([{"name":n,"hex":h,"rgb":list(rgb(h)),"use":u} for n,h,u in C],open(D+f'{slug}.json','w'),indent=2)
    W=1400; sw=W/len(C); body=f'<rect width="{W}" height="560" fill="#FFFFFF"/>'
    for i,(n,h,u) in enumerate(C):
        x=i*sw; body+=f'<rect x="{x:.1f}" y="0" width="{sw+1:.1f}" height="380" fill="{h}"/>'
        if h in ("#FAFAF7","#FFFFFF"): body+=f'<rect x="{x+.5:.1f}" y=".5" width="{sw-1:.1f}" height="379" fill="none" stroke="#D9DBE6"/>'
        for t,f,sz,y,col in [(n,'CourierPrime-700.ttf',20,425,'#1C2340'),(h,'CourierPrime-400.ttf',20,457,'#1C2340'),("RGB %d %d %d"%rgb(h),'Inter-400.ttf',14,487,'#5A6080')]:
            d,_=text_path(t,f,sz,x+16,y); body+=f'<path fill="{col}" d="{d}"/>'
    sv=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} 560" width="{W}" height="560">{body}</svg>'
    open(D+f'{slug}-palette.svg','w').write(sv); cairosvg.svg2png(bytestring=sv.encode(),write_to=D+f'{slug}-palette.png',output_width=2800)

if __name__=='__main__':
    import palettes
    build(sys.argv[1],sys.argv[2],getattr(palettes,sys.argv[1].upper()))
