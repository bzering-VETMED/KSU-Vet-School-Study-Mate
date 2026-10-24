"""Practical 3 · gap fill-ins (made by Claude): lab-guide drawings + Bethany's web photo for bold terms with no real photo.
- Lab-guide figures (Lab 24 lab guide PDF: Fig 4-38, 4-40, 4-41B): PDF text labels removed; labels that are a Practical 3
  bold term get pink numbered badges, the rest are erased. Reveal = the labeled original.
- web photo (cat, male inguinal region): typed labels inpainted → badges.
Writes gross-anatomy-lab{21,24}-gapfill1.html, registered as sources so p3best.py can place them.
Run after p3cross.py, before p3best.py:  python3 tools/p3gapimg.py <Lab_24_lab_guide.pdf> <web_photo.jpg>"""
import sys,os,re,time,html
sys.path.insert(0,'tools')
import pymupdf,cv2,numpy as np
from PIL import Image,ImageDraw,ImageFont
from deck import page,img_card_facts,text_card2
import p3bold
_src=open('tools/p3split.py').read(); exec(_src[:_src.index('for n in map')])
LG,WEB=sys.argv[1],sys.argv[2]; V=str(int(time.time())); E=html.escape
F=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',36)
ALL=[[t]+al for n in (21,22,23,24,25) for t,al,_ in p3bold.P3BOLD[n]]
def badge(d,cx,cy,n,r=26):
    d.ellipse([cx-r,cy-r,cx+r,cy+r],fill=(224,95,168),outline='white',width=5); d.text((cx,cy),str(n),font=F,fill='white',anchor='mm')
def fig(pg,rect,name,want):
    doc=pymupdf.open(LG); p=doc[pg-1]; R=pymupdf.Rect(rect); M=pymupdf.Matrix(3,3)
    a=p.get_pixmap(matrix=M,clip=R); A=Image.frombytes('RGB',(a.w,a.h),a.samples)
    lines=[]
    for b in p.get_text('dict')['blocks']:
        for l in b.get('lines',[]):
            t=' '.join(sp['text'] for sp in l['spans']).strip(); r=pymupdf.Rect(l['bbox'])
            if t and r.intersects(R): lines.append([r,re.sub(r'\s+',' ',t)])
    lines.sort(key=lambda x:(x[0].y0,x[0].x0)); blocks=[]
    for r,t in lines:            # two-line labels: previous line ends in a connector or this one starts lowercase
        pr=next((b for b in reversed(blocks) if 0<=r.y0-b[0].y1<4 and abs(r.x0-b[0].x0)<40),None)
        if pr and (re.search(r'\b(of|the|and|to|with)$|,$',pr[1]) or t[:1].islower()): pr[0]|=r; pr[1]+=' '+t
        else: blocks.append([r,t])
    for w in p.get_text('words'):
        if pymupdf.Rect(w[:4]).intersects(R): p.add_redact_annot(pymupdf.Rect(w[:4])+(-1,-1,1,1),fill=False)
    p.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE,graphics=pymupdf.PDF_REDACT_LINE_ART_NONE,text=pymupdf.PDF_REDACT_TEXT_REMOVE)
    q=p.get_pixmap(matrix=M,clip=R); Q=Image.frombytes('RGB',(q.w,q.h),q.samples); d=ImageDraw.Draw(Q); out=[]
    for r,t in sorted(blocks,key=lambda x:(x[0].y0,x[0].x0)):
        if not re.search(want,t,re.I): continue
        out.append(t); badge(d,(r.x0+r.x1)/2*3-R.x0*3,(r.y0+r.y1)/2*3-R.y0*3,len(out))
    qf,af=f'assets/p3lg_{name}_q.jpg',f'assets/p3lg_{name}_a.jpg'; Q.save(qf,quality=90); A.save(af,quality=90)
    return qf,af,out
CARDS={21:[],24:[]}
TAG='📖 lab guide drawing · gap fill (no real photo exists)'
qf,af,o=fig(8,(55,368,560,668),'f441b',r'epididym|vaginal tunic|ductus deferens|testicular|cremaster|vaginal ring')
CARDS[21].append(img_card_facts('Fig 4-41B · male, median section (cranial to the right). Name each number.',f'{qf}?v={V}',' · '.join(f'#{i} {t}' for i,t in enumerate(o,1)),'Visceral vaginal tunic = peritoneum fused onto the testis + epididymis · parietal vaginal tunic = outer layer · ligament of the tail of the epididymis anchors the tail to the vaginal tunic + spermatic fascia',f'{af}?v={V}',[],TAG+' · Lab 24 lab guide p187'))
for pg,rect,nm,cap in ((6,(40,55,470,366),'f438','Fig 4-38 · female pelvic arteries, right lateral view.'),(7,(60,356,565,739),'f440','Fig 4-40 · vessels of the penis + prepuce.')):
    qf,af,o=fig(pg,rect,nm,r'caudal rectal|internal pudendal|ventral perineal|artery of the (penis|bulb|clitoris)|deep artery|dorsal artery')
    o=[t if re.search(r'artery|vein',t,re.I) else t+' artery' for t in o]
    CARDS[24].append(img_card_facts(cap+' Name each number.',f'{qf}?v={V}',' · '.join(f'#{i} {t}' for i,t in enumerate(o,1)),'Caudal rectal artery = branch of the ventral perineal artery (internal pudendal) → rectum + anus; also supplies the external anal sphincter',f'{af}?v={V}',[],TAG+f' · Lab 24 lab guide p{pg+179}'))
# Bethany's web photo (cat): erase typed labels, badge the bold ones
im=cv2.imread(WEB); H,W=im.shape[:2]
# (box, mode, answer): mode b = label sits on fur/background → inpaint the whole box · w/k = white/dark letter strokes on tissue
LAB=[((538,300,640,370),'b','Head and tail of the epididymis'),((358,316,517,344),'b','Spermatic cord'),((465,276,487,300),'b','Ductus deferens'),
     ((593,220,610,247),'k','Testis'),((360,76,429,104),'b','Penis'),((330,48,429,74),'b','Prepuce'),
     ((248,106,277,132),'w',None),((573,120,592,147),'b',None),((666,220,687,245),'k',None)]
mask=np.zeros((H,W),np.uint8)
for (x0,y0,x1,y1),md,_ in LAB:
    sub=im[y0:y1,x0:x1].astype(int)
    m=np.ones(sub.shape[:2],bool) if md=='b' else ((sub.min(2)>175) if md=='w' else (sub.max(2)<110))
    mask[y0:y1,x0:x1]=np.maximum(mask[y0:y1,x0:x1],(m*255).astype(np.uint8))
mask=cv2.dilate(mask,np.ones((3,3),np.uint8),iterations=2); out=cv2.inpaint(im,mask,9,cv2.INPAINT_TELEA)
Q=Image.fromarray(out[:,:,::-1]); d=ImageDraw.Draw(Q); names=[]
for (x0,y0,x1,y1),_m,a in LAB:
    if a: names.append(a); badge(d,(x0+x1)/2,(y0+y1)/2,len(names),r=17)
Q.save('assets/p3web_cat_inguinal_q.jpg',quality=92); Image.open(WEB).convert('RGB').save('assets/p3web_cat_inguinal_a.jpg',quality=92)
CARDS[21].insert(0,img_card_facts('Male inguinal region, ventral view (cranial left). Name 1–6.',f'assets/p3web_cat_inguinal_q.jpg?v={V}',' · '.join(f'#{i} {t}' for i,t in enumerate(names,1)),'⚠️ This specimen is a CAT (penis points caudally, testes near the tail) · same structures as the dog',f'assets/p3web_cat_inguinal_a.jpg?v={V}',[],'🌐 web photo (cat) · sent by Bethany'))
CARDS[21].append(text_card2('🧅 Layers around the testis, outside → in (where are the spermatic fascia + visceral vaginal tunic?)','Skin + scrotum (tunica dartos) → spermatic fascia (reflect it to see the vaginal tunic; cremaster muscle runs in it) → parietal vaginal tunic → vaginal cavity (continuous with the peritoneal cavity) → visceral vaginal tunic (fused onto the testis, epididymis + ductus deferens; can\'t be peeled off) → tunica albuginea → testis','🧠 concept · gap fill · Lab 21 lab guide p153–154'))
CARDS[21].append(text_card2('🔗 Head, body, tail of the epididymis + its two ligaments?','Head = cranial end (joins the testis) · body = along the lateral side of the testis · tail = caudal end, continues as the ductus deferens · proper ligament of the testis: tail of the epididymis → testis · ligament of the tail of the epididymis: tail → vaginal tunic + spermatic fascia (both = gubernaculum remnants)','🧠 concept · gap fill · Lab 21 lab guide p154'))

# fetal pig testis (SCB209 Lab 11 p6, sent by Bethany): white labels on black background → inpaint the boxes
pim=cv2.imread('tools/umn_src/scb209_l11_p6.png'); pm=np.zeros(pim.shape[:2],np.uint8)
PL=[((920,112,1165,165),'Ductus deferens'),((765,582,890,636),'Testis'),((960,582,1290,636),'Head of the epididymis'),((395,582,605,636),None)]
for (x0,y0,x1,y1),_ in PL: pm[y0:y1,x0:x1]=255
pq=Image.fromarray(cv2.inpaint(pim,pm,7,cv2.INPAINT_TELEA)[:,:,::-1]); d=ImageDraw.Draw(pq); k=0
for (x0,y0,x1,y1),a in PL:
    if a: k+=1; badge(d,(x0+x1)/2,(y0+y1)/2,k,r=30)
pq.crop((0,30,1500,1125)).save('assets/p3web_pig_testis_q.jpg',quality=90); Image.open('tools/umn_src/scb209_l11_p6.png').convert('RGB').crop((0,30,1500,1125)).save('assets/p3web_pig_testis_a.jpg',quality=90)
CARDS[21].insert(1,img_card_facts('Isolated testis, medial view (top) + lateral view (bottom). Name 1–3.',f'assets/p3web_pig_testis_q.jpg?v={V}','#1 Ductus deferens · #2 Testis · #3 Head of the epididymis','⚠️ FETAL PIG specimen · head = cranial end of the epididymis where it joins the testis; body runs along the testis; tail = caudal end → ductus deferens',f'assets/p3web_pig_testis_a.jpg?v={V}',[],'🌐 web photo (fetal pig) · SCB209 Lab 11 · sent by Bethany'))

# Lecture 23 drawings (already OCR-erased + numbered by p3repro.py) → Lab 21 gap fill-ins, answers spelled out
LEC=[('m10','Testis attachments, lateral view. Name each number.','Ductus deferens · Cremaster muscle · Parietal vaginal tunic · Ligament of the tail of the epididymis · Proper ligament of the testis','Proper ligament: tail of the epididymis → testis · ligament of the tail: tail → vaginal tunic + spermatic fascia (gubernaculum remnants)'),
     ('m11','Testis + epididymis (A lateral, B medial). Name each number.','Head of the epididymis · Body of the epididymis · Tail of the epididymis · Testis · Pampiniform plexus · Testicular bursa · Cremaster muscle · Ductus deferens · Parietal vaginal tunic · Ligament of the tail of the epididymis · Proper ligament of the testis','Head = cranial end · body = along the testis · tail = caudal end, continues as the ductus deferens'),
     ('m12','Cross section of the spermatic cord. Name each number.','Spermatic fascia · Parietal vaginal tunic · Visceral vaginal tunic · Vaginal cavity · Mesorchium · Mesoductus deferens · Testicular artery and vein · Ductus deferens · Deferent artery · Deferent vein · Cremaster muscle','Deferent artery + vein ride with the ductus deferens in the mesoductus deferens; testicular vessels sit in the mesorchium')]
for nm,q,a,c in LEC:
    CARDS[21].append(img_card_facts(q,f'assets/p3rep_{nm}_q.jpg?v={V}',a,c,f'assets/p3rep_{nm}_a.jpg?v={V}',[],'📖 lecture drawing · gap fill (no real photo exists) · Lecture 23 Male reproductive'))
css=re.search(r'<style>(.*?)</style>',open('gross-anatomy-lab22-best1.html').read(),re.S).group(1)
for n,cs in CARDS.items():
    fn=f'gross-anatomy-lab{n}-gapfill1.html'; hubf=f'gross-anatomy-lab{n}-images.html'
    pg=page(f'Lab {n} · Gap fill-ins',f'Drawings + web photos for bold terms with no real photo · {len(cs)} cards',''.join(cs).replace('class="card"','class="card on"',1),back=f'{hubf}?v={V}')
    open(fn,'w').write(re.sub(r'<style>.*?</style>',lambda _:f'<style>{css}</style>',pg,count=1,flags=re.S))
    h=open(hubf).read(); mk=re.search(r'<!--p3src:(.*?)-->',h)
    parts=[x for x in mk.group(1).split('|') if '-gapfill' not in x]+[f'more::{fn}::🩹 Gap fill-ins (drawings + web photos)']
    open(hubf,'w').write(h.replace(mk.group(0),'<!--p3src:'+'|'.join(parts)+'-->')); print(n,len(cs),'cards')
