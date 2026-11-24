import sys,os
S=os.environ['S']; sys.path.insert(0,S+'/work/src'); os.environ['WORDSMITH_FONT_DIR']=S+'/fonts'
import buildp as B, cairosvg
from text import text_path
INK,PAPER=B.INK,B.PAPER; CAP=B.CAP
def drop(x,base,size,col,gap=0.06):
    # the usual bar, and below it a falling drop of ink: point up, round below
    cw=size*0.153; top=base-size*CAP; h=size*CAP+size*0.02
    r=size*0.092; cx=x+cw/2; tip=base+size*0.02+size*gap; cy=tip+size*0.20
    k=0.5523*r
    d=(f'M{cx:.2f},{tip:.2f}C{cx+r*0.15:.2f},{tip+size*0.06:.2f} {cx+r:.2f},{cy-r*1.05:.2f} {cx+r:.2f},{cy:.2f}'
       f'C{cx+r:.2f},{cy+k:.2f} {cx+k:.2f},{cy+r:.2f} {cx:.2f},{cy+r:.2f}'
       f'C{cx-k:.2f},{cy+r:.2f} {cx-r:.2f},{cy+k:.2f} {cx-r:.2f},{cy:.2f}'
       f'C{cx-r:.2f},{cy-r*1.05:.2f} {cx-r*0.15:.2f},{tip+size*0.06:.2f} {cx:.2f},{tip:.2f}Z')
    return f'<rect fill="{col}" x="{x:.2f}" y="{top:.2f}" width="{cw:.2f}" height="{h:.2f}"/><path fill="{col}" d="{d}"/>', cw, cy+r-base
def tri(x,base,size,col):
    cw=size*0.075; g=size*0.03; top=base-size*CAP; h=size*CAP+size*0.02; o=''
    for i,c in enumerate(['#B8862B','#D24B3E','#2E9473']):
        o+=f'<rect fill="{c}" x="{x+i*(cw+g):.2f}" y="{top:.2f}" width="{cw:.2f}" height="{h:.2f}"/>'
    return o, 3*cw+2*g, 0
def block(x,base,size,col):
    cw=size*0.6; top=base-size*CAP; h=size*CAP+size*0.02
    return f'<rect fill="{col}" x="{x:.2f}" y="{top:.2f}" width="{cw:.2f}" height="{h:.2f}"/>', cw, 0
SH={'drop':drop,'tri':tri,'block':block}
def typed(s,size,x,base,fg,cur,shape):
    d,a=text_path(s,B.F,size,x,base); body=f'<path fill="{fg}" d="{d}"/>'
    if shape is None: return body,x+a,0
    b,cw,dr=SH[shape](x+a+size*0.03,base,size,cur); return body+b, x+a+size*0.03+cw, dr
def icon(letter,shape,cur,S=1024,glyph=600,fg=PAPER):
    _,r,dr=typed(letter,glyph,0,0,fg,cur,shape); x=(S-r)/2; h=glyph*CAP+dr; base=S/2-h/2+glyph*CAP
    b,_,_=typed(letter,glyph,x,base,fg,cur,shape)
    return f'<rect width="{S}" height="{S}" rx="{S*0.225:.1f}" fill="{INK}"/>'+b
if __name__=='__main__':
    W=1800; rows=[('A','Ink drop (recommended)','drop',INK,PAPER,'&','The cursor lets fall a drop of ink. One color, pure ink: the products add color, the house does not.'),
                  ('B','Family cursor','tri',None,None,'&','Three slim cursors in Brass, Card Red and Ribbon Green: the house of the three apps. Ties it to today\'s three products.'),
                  ('C','Typewriter block','block',INK,PAPER,'W&I','The full-width block cursor of an old terminal, after a typed W&I monogram. Strong on a book spine, less of a link to the apps.')]
    body=f'<rect width="{W}" height="{len(rows)*420+60}" fill="#FFFFFF"/>'
    for i,(k,t,sh,c1,c2,ic,desc) in enumerate(rows):
        y=i*420+40
        body+=f'<rect x="40" y="{y}" width="{W-80}" height="380" rx="16" fill="{PAPER}" stroke="#E4E5EC"/>'
        d,_=text_path(f'{k}. {t}','Inter-600.ttf',30,80,y+60); body+=f'<path fill="{INK}" d="{d}"/>'
        d,_=text_path(desc,'Inter-400.ttf',20,80,y+96); body+=f'<path fill="#5A6080" d="{d}"/>'
        b,_,_=typed('Wordsmith & Ink',84,80,y+230,INK,c1 or INK,sh); body+=b
        body+=f'<g transform="translate({W-760},{y+120})"><rect width="420" height="200" rx="12" fill="{INK}"/></g>'
        b,_,_=typed('Wordsmith & Ink',40,W-740,y+232,PAPER,c2 or PAPER,sh); body+=b
        body+=f'<g transform="translate({W-300},{y+40}) scale(0.125)"></g><g transform="translate({W-220},{y+150}) scale(0.125)">{icon(ic,sh,c2 or PAPER,glyph=640 if len(ic)==1 else 340)}</g>'
    sv=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {len(rows)*420+60}" width="{W}" height="{len(rows)*420+60}">{body}</svg>'
    open('concepts.svg','w').write(sv); cairosvg.svg2png(bytestring=sv.encode(),write_to='concepts.png',output_width=W)
