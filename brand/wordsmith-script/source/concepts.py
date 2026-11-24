import sys; sys.path.insert(0,'.')
OUTC='outc'
from build import *  # rebuilds into out (cheap)
from text import text_path
def icon_A(): return icon_full()
def icon_B(S=1024):
    b=f'<rect width="{S}" height="{S}" rx="{S*0.225}" fill="#E9EAF2"/>'
    b+=f'<rect x="250" y="150" width="560" height="740" rx="18" fill="#C9CCDA"/>'
    b+=f'<rect x="222" y="132" width="560" height="740" rx="18" fill="{PAPER}" stroke="#C9CCDA" stroke-width="4"/>'
    b+=brad(300,132+740*0.19,34)+brad(300,132+740*0.81,34)
    # courier-like lines: scene heading, action, character, dialogue
    rows=[(380,300,330,26),(380,370,340,14),(380,405,300,14),(380,440,250,14),(520,520,140,18),(450,565,250,14),(450,600,230,14),(450,635,190,14)]
    for x,y,w,h in rows: b+=f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="{INK}"/>'
    return b
def icon_C(S=1024):
    b=f'<rect width="{S}" height="{S}" rx="{S*0.225}" fill="{INK}"/>'
    d,a=text_path('W','CourierPrime-700.ttf',720,0,0)
    x=(S-a-120)/2; d,a=text_path('W','CourierPrime-700.ttf',720,x,690)
    b+=f'<path fill="{PAPER}" d="{d}"/><rect x="{x+a+10}" y="300" width="110" height="400" fill="{BRASS}"/>'
    return b
def lock_A():
    w,h,b=horizontal(INK,BRASS_D); return w,h,b
def lock_B():
    d,a=text_path('wordsmith script','CourierPrime-700.ttf',64,0,60)
    return a,80,f'<path fill="{INK}" d="{d}"/>'
def lock_C():
    d,a=text_path('Wordsmith Script','CourierPrime-700.ttf',60,0,60)
    return a+50,80,f'<path fill="{INK}" d="{d}"/><rect x="{a+12}" y="16" width="30" height="50" fill="{BRASS}"/>'
cols=[('A  Twin nib','The W is two pen nibs joined. Extends to every Wordsmith product.',icon_A,lock_A),
      ('B  Bound page','A typed script page held by two brass brads. Most literal.',icon_B,lock_B),
      ('C  Typewriter  (chosen)','A Courier W with a brass cursor. Simple, technical.',icon_C,lock_C)]
CW=520; body=f'<rect width="{CW*3}" height="760" fill="#FFFFFF"/>'
for i,(t,sub,ic,lk) in enumerate(cols):
    x0=i*CW+40
    body+=f'<g transform="translate({x0+80} 40) scale({280/1024})">{ic()}</g>'
    w,h,b=lk(); s=min(420/w,1.0)
    body+=f'<g transform="translate({x0} {380}) scale({s})">{b}</g>'
    d,_=text_path(t,'Inter-600.ttf',24,x0,600); body+=f'<path fill="{INK}" d="{d}"/>'
    words=sub.split(); line='';yy=640
    lines=[]
    for wd in words:
        if len(line+' '+wd)>44: lines.append(line); line=wd
        else: line=(line+' '+wd).strip()
    lines.append(line)
    for ln in lines:
        d,_=text_path(ln,'Inter-400.ttf',18,x0,yy); body+=f'<path fill="#4A5070" d="{d}"/>'; yy+=26
open(OUTC+'/concepts/logo-directions.svg','w').write(svg(CW*3,760,body,'Wordsmith Script logo directions'))
cairosvg.svg2png(url=OUTC+'/concepts/logo-directions.svg',write_to=OUTC+'/concepts/logo-directions.png',output_width=1560)
