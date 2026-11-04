"""Practical 4 · Lab 28 📷 Bethany's lab photos of the color-coded skull model → numbered cards (made by Claude).
Labels are Claude's reads of the painted bones + big landmarks only (no tiny foramina) — tagged so she can check them.
One card per photo, ALL numbers answered on one tap.  Originals: tools/skull_src_p4/IMG_NNNN.jpg
SPEC: (id, view, crop box (x0,y0,x1,y1) in the upright original, [(x, y, name), ...])"""
import sys,html
sys.path.insert(0,'tools')
from PIL import Image,ImageOps,ImageDraw,ImageFont
import p4lab26 as B
E=html.escape; FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
SPEC=[
 ('8546','Dorsal view',(300,80,1220,1900),[(640,300,'Parietal bone'),(760,620,'Frontal bone'),(750,1150,'Nasal bone'),(560,1150,'Maxilla'),(740,1740,'Incisive bone'),(420,900,'Zygomatic arch'),(380,640,'Zygomatic process (temporal bone)')]),
 ('8548','Left lateral view, caudal half',(0,330,1420,1200),[(650,470,'Frontal bone'),(1100,620,'Parietal bone'),(1000,950,'Temporal bone (squamous part)'),(560,1010,'Zygomatic arch'),(450,870,'Orbit'),(110,820,'Maxilla')]),
 ('8547','Left lateral view, rostral half',(0,150,1512,1340),[(110,850,'Incisive bone'),(560,650,'Nasal bone'),(620,820,'Maxilla'),(1010,960,'Zygomatic bone (part of the zygomatic arch)'),(95,1110,'Canine tooth'),(640,1190,'Premolars (cheek teeth)')]),
 ('8550','Caudal (back) view',(200,100,1260,1180),[(470,600,'Parietal bone'),(725,600,'External sagittal crest'),(700,170,'Frontal bone'),(250,620,'Zygomatic arch'),(330,820,'Zygomatic process (temporal bone)')]),
 ('8557','Ventral view (hard palate)',(150,140,1260,2000),[(688,515,'Palatine fissure'),(735,370,'Incisive bone'),(620,870,'Hard palate'),(470,470,'Canine tooth'),(640,215,'Incisor teeth'),(470,830,'Premolars'),(320,1180,'Superior shearing tooth (upper fourth premolar)'),(430,1330,'Molars'),(240,1520,'Zygomatic arch')]),
 ('8556','Ventral view, caudal skull',(160,0,1360,1650),[(470,1040,'Tympanic bulla'),(720,500,'Choanae'),(640,230,'Hard palate'),(355,600,'Zygomatic arch'),(700,1250,'Occipital bone')]),
]
def build():
    out=[]; font=ImageFont.truetype(FONT,52)
    for img_id,view,box,pts in SPEC:
        im=ImageOps.exif_transpose(Image.open(f'tools/skull_src_p4/IMG_{img_id}.jpg')).convert('RGB'); d=ImageDraw.Draw(im)
        for k,(x,y,_) in enumerate(pts,1):
            R=40; d.ellipse([x-R,y-R,x+R,y+R],fill='#e05fa8',outline='white',width=6); d.text((x,y),str(k),fill='white',font=font,anchor='mm')
        fn=f'assets/p4skull_{img_id}.jpg'; im.crop(box).save(fn,quality=90)
        nums=', '.join(f'#{k}' for k in range(1,len(pts)+1))
        nm=''.join(f'<div class="nm">#{k} · {E(n)}</div>' for k,(_,_,n) in enumerate(pts,1))
        terms=list(dict.fromkeys(t for _,_,n in pts for t in B.terms_in(n,28)))
        out.append(dict(name=view,terms=terms,html=B.card(f'Name {nums}',f'📷 my lab photo · skull model · {view} · labels by Claude — check with TA',fn,nm,[])))
    return out
