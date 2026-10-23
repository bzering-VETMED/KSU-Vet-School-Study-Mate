"""Practical 3 · 📷 OUR lab photos (Bethany's lab group, labeled on the phone) → numbered ⭐ cards.  Made by Claude.
The typed labels are erased (letter strokes + annotation highlight only, inpainted) and replaced by pink numbered
badges; the colored pointer lines/circles stay. Reveal = the original labeled photo.
Label boxes are given in the 825-px-wide preview frame and scaled to the original.
Run from repo root AFTER p3best/p3dedupe:  python3 tools/p3ours.py <folder with IMG_08xx.jpg>"""
import sys,os,re,time,html,cv2,numpy as np
sys.path.insert(0,'tools')
from PIL import Image,ImageOps,ImageDraw,ImageFont
from deck import img_card_facts,page
SRC=sys.argv[1]; V=str(int(time.time())); E=html.escape
FONT=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',44)
TAG='📷 our lab photo · 10/22'
# (file, labs, view, [(box x0,y0,x1,y1 in 825-wide frame, kind, answer or None=erase only)], facts)
#   kind: d = dark text · w = white text · h = text on a colored highlight bar (erase bar too)
P=[
 ('IMG_0820',[24],'Left lateral pelvis, tail to the left',[((222,800,422,862),'h','Levator ani muscle'),((408,756,607,802),'h','Coccygeus muscle')],
  [('🧭 Which is lateral?','Coccygeus = lateral, shorter + thicker · levator ani = medial, thinner'),('🧱 Together they form?','The pelvic diaphragm')]),
 ('IMG_0821',[23,24],'Abdomen opened, viscera reflected',[((212,683,630,737),'h','Left hypogastric nerve')],
  [('⚡ Carries?','Sympathetic fibers: caudal mesenteric ganglion → pelvic plexus'),('🔗 Partner?','Right hypogastric nerve on the other side')]),
 ('IMG_0825',[24],'Pelvic cavity, left side opened',[((98,430,320,470),'d','Pelvic nerve'),((4,876,392,937),'d','Pelvic plexus')],
  [('⚡ Pelvic nerve carries?','Sacral PARASYMPATHETIC fibers to the pelvic plexus'),('🕸️ Pelvic plexus gets?','Hypogastric (sympathetic) + pelvic (parasympathetic) nerves')]),
 ('IMG_0826',[24],'Female, caudal abdomen; probe in a peritoneal space',[((445,652,808,788),'d','Rectogenital pouch (labeled "fossa" on the photo)')],
  [('📍 Between?','Rectum (dorsal) and the genital fold/uterus (ventral)'),('⚠️ Name it right','Exam term = rectogenital POUCH')]),
 ('IMG_0827',[24],'Female, bladder retracted cranially',[((404,348,548,390),'w','Urinary bladder'),((205,405,358,437),'d','Body of the uterus'),((316,858,702,1002),'d','Vesicogenital pouch')],
  [('📍 Vesicogenital pouch is between?','Uterus (genital fold) and the urinary bladder'),('🔢 Pouches dorsal → ventral','Pararectal fossa · rectogenital · vesicogenital · pubovesical')]),
 ('IMG_0828',[24],'Female, bladder and ventral body wall',[((55,386,196,427),'d','Urinary bladder'),((440,590,573,619),'d','Peritoneum'),((544,725,742,757),'d','Median ligament of the bladder (labeled "medial" on the photo)'),((209,745,422,830),'d','Pubovesical pouch')],
  [('📍 Pubovesical pouch is between?','Bladder and the pubis / ventral body wall'),('⚠️ Name it right','MEDIAN ligament of the bladder (not "medial")')]),
 ('IMG_0830',[24],'Terminal aorta, ventral view',[((3,226,228,312),'w','External iliac arteries'),((292,246,490,303),'d','Round ligament of the bladder (umbilical artery)'),((119,755,321,784),'d','Common trunk of the internal iliac arteries'),((540,730,675,862),'d','Internal iliac artery')],
  [('➡️ External iliac becomes?','Femoral artery, through the vascular lacuna'),('👶 Round ligament of the bladder is?','Remnant of the fetal umbilical artery (in the lateral ligament of the bladder)')]),
 ('IMG_0831',[24],'Female, bladder retracted to the right',[((75,208,272,267),'d','Round ligament of the bladder (umbilical artery)'),((294,198,395,252),'d','External iliac artery'),((633,303,775,340),'d','Urinary bladder'),((509,628,800,670),'d','Median ligament of the bladder (labeled "medial" on the photo)'),((339,678,621,717),'d','Lateral ligament of the bladder')],
  [('🧩 3 bladder ligaments','Median (ventral, to the body wall) · left + right lateral (contain the round ligament + ureter)'),('⚠️ Name it right','MEDIAN ligament of the bladder')]),
 ('IMG_0832',[24],'Pelvic inlet, left side',[((184,266,492,300),'d','Internal pudendal artery'),((124,318,350,354),'d','External iliac artery'),((582,686,722,724),'d','Urinary bladder'),((480,818,694,854),'d','Internal iliac artery')],
  [('🌿 Internal iliac ends as?','Caudal gluteal + internal pudendal arteries'),('➡️ Internal pudendal first branch?','Vaginal / prostatic artery')]),
]
def erase(img,boxes):
    H,W=img.shape[:2]; s=W/825; mask=np.zeros((H,W),np.uint8)
    for (x0,y0,x1,y1),k,_ in boxes:
        X0,Y0,X1,Y1=[int(v*s) for v in (x0,y0,x1,y1)]; X0=max(0,X0);Y0=max(0,Y0);X1=min(W,X1);Y1=min(H,Y1)
        sub=img[Y0:Y1,X0:X1].astype(int)
        if k=='h': m=np.ones(sub.shape[:2],bool)                    # annotation highlight bar = overlay, not anatomy
        elif k=='w': m=(sub.min(2)>200)
        else: m=(sub.max(2)<95)
        mask[Y0:Y1,X0:X1]=np.maximum(mask[Y0:Y1,X0:X1],(m*255).astype(np.uint8))
    mask=cv2.dilate(mask,np.ones((3,3),np.uint8),iterations=3)
    return cv2.inpaint(img,mask,9,cv2.INPAINT_TELEA)
def badges(img,boxes):
    im=Image.fromarray(img); d=ImageDraw.Draw(im); s=im.width/825; n=0; out=[]
    for (x0,y0,x1,y1),k,ans in boxes:
        if ans is None: continue
        n+=1; cx,cy=(x0+x1)/2*s,(y0+y1)/2*s; r=38
        d.ellipse([cx-r,cy-r,cx+r,cy+r],fill=(224,95,168),outline=(255,255,255),width=5)
        d.text((cx,cy),str(n),font=FONT,fill='white',anchor='mm'); out.append((n,ans))
    return im,out
CROP={'IMG_0830':925}
cards={}
os.makedirs('assets',exist_ok=True)
for f,labs,view,boxes,facts in P:
    o=ImageOps.exif_transpose(Image.open(f'{SRC}/{f}.jpg')).convert('RGB')
    if f in CROP: o=o.crop((0,0,o.width,int(CROP[f]*o.width/825)))      # drop a typed caption bar (its fact is in the reveal)
    A=np.array(o)
    Q,items=badges(erase(cv2.cvtColor(A,cv2.COLOR_RGB2BGR)[:,:,::-1].copy(),boxes),boxes)
    qp=f'assets/ours_{f.lower()}_q.jpg'; ap=f'assets/ours_{f.lower()}_a.jpg'
    Q.save(qp,quality=88); o.save(ap,quality=88)
    nums=', '.join(str(n) for n,_ in items)
    q=f'{view}. Name {nums}.' if len(items)>1 else f'{view}. Name 1.'
    name=' · '.join(f'{n} · {a}' for n,a in items)
    for L in labs: cards.setdefault(L,[]).append(img_card_facts(q,f'{qp}?v={V}',name,'',f'{ap}?v={V}',facts,TAG))
for L,cs in cards.items():
    hub=f'gross-anatomy-lab{L}-images.html'; fn=f'gross-anatomy-lab{L}-ours1.html'
    css=re.search(r'<style>(.*?)</style>',open(f'gross-anatomy-lab{L}-best1.html').read(),re.S).group(1)
    hh=''.join(cs).replace('class="card"','class="card on"',1)
    pg=page(f'Lab {L} · 📷 Our lab photos',f'Labeled at lab 10/22 · labels erased + numbered · {len(cs)} cards',hh,back=f'{hub}?v={V}')
    open(fn,'w').write(re.sub(r'<style>.*?</style>',lambda _:f'<style>{css}</style>',pg,count=1,flags=re.S))
    h=open(hub).read(); h=re.sub(r'<!--ours-->.*?<!--/ours-->','',h,flags=re.S)
    link=f'<!--ours--><a href="{fn}?v={V}">📷 Our lab photos · 10/22<span>{len(cs)} cards</span></a><!--/ours-->'
    m=re.search(r'(<div class="sec main"><h2>[^<]*</h2><p>.*?</p>)',h,re.S)
    h=h.replace(m.group(1),m.group(1)+link,1); open(hub,'w').write(h)
    print(L,fn,len(cs))
