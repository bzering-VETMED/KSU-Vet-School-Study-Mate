"""Lab 16 · original drawn diagrams (made by Claude) for bold terms with no lab-guide figure:
annulus fibrosus / intervertebral disc, cranial + caudal costal foveae. Numbered (question) + labeled (answer) SVGs.
Run from repo root AFTER p3ppt.py/p3diagrams.py, BEFORE p3simplify.py:  python3 tools/lab16draw.py"""
import sys,re,time
sys.path.insert(0,'tools'); import deck; deck.PRACTICAL=3
from deck import img_card_facts,page
V=str(int(time.time()))
BONE='#f1e3c9';BONE_S='#8b6b4a';DISC='#e6d6f3';DISC_S='#7b42a0';NUC='#f6c3dc';PINK='#e05fa8';INK='#34213f';SOFT='#8a6b99'
def svg(body,w=820,h=520): return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" font-family="Arial,Helvetica,sans-serif"><rect width="{w}" height="{h}" fill="#fff"/>{body}</svg>'
def tag(x,y,txt): return f'<g><rect x="{x-46}" y="{y-13}" width="92" height="26" rx="13" fill="#fff" stroke="{SOFT}" stroke-width="1.5"/><text x="{x}" y="{y+5}" font-size="14" font-weight="700" fill="{SOFT}" text-anchor="middle">{txt}</text></g>'
def ptr(n,lx,ly,tx,ty,name,labeled,anchor='middle'):
    line=f'<line x1="{lx}" y1="{ly}" x2="{tx}" y2="{ty}" stroke="{INK}" stroke-width="2.2"/><circle cx="{tx}" cy="{ty}" r="4" fill="{INK}"/>'
    if labeled:
        wbox=len(name)*8.6+20; x0=lx-wbox/2 if anchor=='middle' else (lx if anchor=='start' else lx-wbox)
        return line+f'<rect x="{x0}" y="{ly-16}" width="{wbox}" height="30" rx="8" fill="#fff" stroke="{DISC_S}" stroke-width="2"/><text x="{x0+wbox/2}" y="{ly+5}" font-size="16" font-weight="700" fill="#5d347e" text-anchor="middle">{name}</text>'
    return line+f'<circle cx="{lx}" cy="{ly}" r="17" fill="{PINK}" stroke="#fff" stroke-width="3"/><text x="{lx}" y="{ly+6}" font-size="17" font-weight="800" fill="#fff" text-anchor="middle">{n}</text>'
def disc(labeled):
    b=''
    # side view: two vertebral bodies + disc (cranial left)
    b+=f'<rect x="40" y="200" width="185" height="130" rx="18" fill="{BONE}" stroke="{BONE_S}" stroke-width="2.5"/>'
    b+=f'<rect x="265" y="200" width="185" height="130" rx="18" fill="{BONE}" stroke="{BONE_S}" stroke-width="2.5"/>'
    b+=f'<rect x="222" y="206" width="46" height="118" rx="8" fill="{DISC}" stroke="{DISC_S}" stroke-width="2.5"/>'
    b+=f'<ellipse cx="245" cy="258" rx="12" ry="26" fill="{NUC}" stroke="{PINK}" stroke-width="1.5"/>'
    b+=f'<text x="245" y="112" font-size="15" fill="{SOFT}" text-anchor="middle" font-weight="700">Side view (two vertebral bodies)</text>'
    b+=tag(90,160,'Cranial')+tag(400,160,'Caudal')
    # cross-section: annulus rings thinner dorsally
    cx=630
    for i,(ry,rx,cy) in enumerate([(108,140,268),(96,126,262),(84,112,256),(72,98,250)]):
        b+=f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{DISC if i==0 else "none"}" stroke="{DISC_S}" stroke-width="{2.5 if i==0 else 1.4}"/>'
    b+=f'<ellipse cx="{cx}" cy="226" rx="54" ry="40" fill="{NUC}" stroke="{PINK}" stroke-width="2"/>'
    b+=f'<text x="{cx}" y="410" font-size="15" fill="{SOFT}" text-anchor="middle" font-weight="700">Disc in cross-section</text>'
    b+=tag(cx-95,138,'Dorsal')+tag(cx,446,'Ventral')
    b+=ptr(1,780,330,735,318,'Annulus fibrosus',labeled,'end')
    b+=ptr(2,cx+95,62,cx+20,226,'Nucleus pulposus',labeled)
    b+=ptr(3,245,470,245,320,'Intervertebral disc',labeled)
    return svg(b)
def foveae(labeled):
    b=''
    # two thoracic vertebrae, lateral view, cranial left; arch + spinous process
    for x0 in (60,410):
        b+=f'<path d="M{x0+40} 230 L{x0+40} 170 Q{x0+40} 150 {x0+70} 150 L{x0+250} 150 Q{x0+280} 150 {x0+280} 170 L{x0+280} 230 Z" fill="{BONE}" stroke="{BONE_S}" stroke-width="2.5"/>'
        b+=f'<path d="M{x0+120} 152 L{x0+175} 40 L{x0+215} 46 L{x0+205} 152 Z" fill="{BONE}" stroke="{BONE_S}" stroke-width="2.5"/>'
        b+=f'<rect x="{x0}" y="228" width="330" height="120" rx="16" fill="{BONE}" stroke="{BONE_S}" stroke-width="2.5"/>'
    b+=f'<rect x="388" y="234" width="24" height="108" rx="6" fill="{DISC}" stroke="{DISC_S}" stroke-width="2.5"/>'
    # caudal fovea on cranial vertebra (its caudodorsal corner) + cranial fovea on caudal vertebra
    b+=f'<path d="M390 234 A26 26 0 0 0 364 260 A26 26 0 0 0 390 286 Z" fill="#d79ac1" stroke="{PINK}" stroke-width="2"/>'
    b+=f'<path d="M410 234 A26 26 0 0 1 436 260 A26 26 0 0 1 410 286 Z" fill="#d79ac1" stroke="{PINK}" stroke-width="2"/>'
    b+=f'<circle cx="400" cy="260" r="36" fill="none" stroke="{INK}" stroke-width="2" stroke-dasharray="7 6"/>'
    b+=f'<text x="410" y="22" font-size="15" fill="{SOFT}" text-anchor="middle" font-weight="700">Dashed circle = where the head of the rib sits (spans both foveae + the disc)</text>'
    b+=tag(110,470,'Cranial')+tag(690,470,'Caudal')+tag(770,90,'Dorsal')
    b+=ptr(1,250,450,372,268,'Caudal costal fovea',labeled)
    b+=ptr(2,560,450,428,268,'Cranial costal fovea',labeled)
    b+=ptr(3,520,110,404,300,'Intervertebral disc',labeled,'start')
    return svg(b)
for k,f in (('disc',disc),('fov',foveae)):
    open(f'assets/lab16_draw_{k}_q.svg','w').write(f(False)); open(f'assets/lab16_draw_{k}_a.svg','w').write(f(True))
TAG='✏️ drawn diagram (Claude) · schematic, not to scale'
C=[img_card_facts('Name #1–#3.',f'assets/lab16_draw_disc_q.svg?v={V}','#1 Annulus fibrosus · #2 Nucleus pulposus · #3 Intervertebral disc','',f'assets/lab16_draw_disc_a.svg?v={V}',
   [('⚠️ Why does a disc herniate dorsally?','The annulus fibrosus is THINNER dorsally, so the nucleus pulposus pushes up into the vertebral canal (onto the spinal cord)'),
    ('🧩 Disc = ?','Fibrocartilage between vertebral bodies: annulus fibrosus (outer rings) + nucleus pulposus (gel core)')],TAG),
   img_card_facts('Name #1–#3.',f'assets/lab16_draw_fov_q.svg?v={V}','#1 Caudal costal fovea (on the cranial vertebra) · #2 Cranial costal fovea (on the caudal vertebra) · #3 Intervertebral disc','',f'assets/lab16_draw_fov_a.svg?v={V}',
   [('🦴 What fits here?','The head of the rib: it spans two vertebrae + the disc between them'),
    ('🔄 Naming trap','Each fovea is named for its position on ITS OWN vertebra: the caudal fovea sits at the caudal end of the cranial vertebra')],TAG)]
cs=list(C); cs[0]=cs[0].replace('class="card"','class="card on"',1)
open('gross-anatomy-lab16-diag6.html','w').write(page('Lab 16 · ✏️ Drawn: disc + costal foveae',f'📖 Diagrams · {len(cs)} cards',''.join(cs),back=f'gross-anatomy-lab16-images.html?v={V}'))
h=open('gross-anatomy-lab16-images.html').read()
h=re.sub(r'<!--draw-->.*?<!--/draw-->','',h,flags=re.S)
h=re.sub(r'(<div class="sec diag"[^>]*><h2>[^<]*</h2><p>[^<]*</p>)',lambda m:m.group(1)+f'<!--draw--><a href="gross-anatomy-lab16-diag6.html?v={V}">✏️ Drawn: disc + costal foveae<span>{len(cs)} cards</span></a><!--/draw-->',h,count=1)
open('gross-anatomy-lab16-images.html','w').write(h)
print('ok')
