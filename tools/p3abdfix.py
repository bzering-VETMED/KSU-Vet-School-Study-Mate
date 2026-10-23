"""Practical 3 · fix labels BAKED into the Abdomen.pdf kidney slide (p33): 'Cortex' + 'Medulla' are part of the
photo, so p3abd.py's PDF-text redaction left them visible. Erase the white letter strokes (inpaint), add pink
badges 2 + 3, and update every card that uses p3s_abd_33q.jpg.  Made by Claude.  Idempotent.
Run from repo root after p3labs/p3best:  python3 tools/p3abdfix.py"""
import re,glob,time,cv2,numpy as np,shutil,os
from PIL import Image,ImageDraw,ImageFont
Q='assets/p3s_abd_33q.jpg'; ORIG='tools/umn_src/p3s_abd_33q_orig.jpg'
if not os.path.exists(ORIG): shutil.copy(Q,ORIG)          # keep the untouched render for reruns
img=cv2.imread(ORIG); H,W=img.shape[:2]
BOX={'2':(395,360,520,515),'3':(535,415,675,605)}          # Cortex, Medulla (rotated white text) in the 1800-px render
mask=np.zeros((H,W),np.uint8)
for x0,y0,x1,y1 in BOX.values():
    sub=img[y0:y1,x0:x1].astype(int); m=(sub.min(2)>185)&((sub.max(2)-sub.min(2))<45)
    mask[y0:y1,x0:x1]=np.maximum(mask[y0:y1,x0:x1],(m*255).astype(np.uint8))
mask=cv2.dilate(mask,np.ones((3,3),np.uint8),iterations=3)
out=cv2.inpaint(img,mask,7,cv2.INPAINT_TELEA)
im=Image.fromarray(out[:,:,::-1]); d=ImageDraw.Draw(im); F=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',30)
for n,(x0,y0,x1,y1) in BOX.items():
    cx,cy=(x0+x1)/2,(y0+y1)/2; r=26
    d.ellipse([cx-r,cy-r,cx+r,cy+r],fill=(224,95,168),outline='white',width=4); d.text((cx,cy),n,font=F,fill='white',anchor='mm')
im.save(Q,quality=90)
V=str(int(time.time())); n=0
for f in glob.glob('gross-anatomy-*.html'):
    h=open(f).read()
    if 'p3s_abd_33q.jpg' not in h: continue
    h2=re.sub(r'(<section class="card[^"]*"><div class="q">)Name #1(<span[^>]*>[^<]*</span></div><div class="pic"><img[^>]*p3s_abd_33q\.jpg)[^"]*"',lambda m:m.group(1)+'Name #1, #2 and #3'+m.group(2)+f'?v={V}"',h)
    h2=h2.replace('<div class="pr">❓ Name #1</div><div class="an big">#1 Renal pelvis<img','<div class="pr">❓ Name #1, #2 and #3</div><div class="an big">#1 Renal pelvis · #2 Renal cortex · #3 Renal medulla<img')
    if h2!=h: open(f,'w').write(h2); n+=1
print('patched',n,'pages')
