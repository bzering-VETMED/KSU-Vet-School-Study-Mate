"""Practical 3 · Lab 25 · Male + female reproductive (Lecture 23 Male, Lecture 24 Female course slides).  Made by Claude.
Figures on these slides are textbook drawings with labels BAKED INTO the image, so labels are found with
OCR (tesseract) and erased by inpainting ONLY the letter strokes (no boxes, no blur); a pink numbered badge
marks where each label was. Reveal = the original labeled figure + the slide's own bullet text.
Drawings → 📖 Diagram images (Bethany: best-picture blocks are real photos only).
Cross-lab: male decks also listed on the Lab 21 hub, female decks on the Lab 22 hub (📖 section).
Run from repo root:  python3 tools/p3repro.py <Lecture_23_Male.pdf> <Lecture_24_Female.pdf>"""
import sys,os,re,time,html
sys.path.insert(0,'tools')
import pymupdf,cv2,numpy as np,pytesseract
from PIL import Image,ImageDraw,ImageFont
import deck; deck.PRACTICAL=3
from deck import img_card_facts,text_card2,page,HUBCSS,E
MALE,FEM=sys.argv[1],sys.argv[2]
V=str(int(time.time()))
for f in os.listdir('assets'):
    if f.startswith('p3rep_'): os.remove('assets/'+f)
FONT=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',30)
def figrect(p):
    W,H=p.rect.width,p.rect.height; R=pymupdf.Rect()
    for x in p.get_image_info():
        r=pymupdf.Rect(x['bbox'])&p.rect
        if r.width>W*0.9 or r.x1<50 or r.width<40 or r.height<40: continue      # slide template, purple bar, logo
        if r.y0>H*0.85 and r.x0>W*0.75: continue                                 # K-State wordmark
        R|=r
    return R
def slide_text(p,R):
    t=[];title=''
    for b in p.get_text('blocks'):
        r=pymupdf.Rect(b[:4]); s=re.sub(r'\s+',' ',b[4]).strip()
        if not s or 'KANSAS' in s.upper(): continue
        if not title and r.y1<70: title=s; continue
        t.append(s)
    return title,' '.join(t)
def ocr_erase(img):
    """img: RGB np array. Several OCR passes (union) → erase letter strokes only; returns erased copy + label groups"""
    H,W=img.shape[:2]; boxes=[]
    for fx in (1,2):
        big=cv2.resize(img,None,fx=fx,fy=fx,interpolation=cv2.INTER_CUBIC) if fx>1 else img
        for psm in (11,12):
            d=pytesseract.image_to_data(Image.fromarray(big),config=f'--psm {psm}',output_type=pytesseract.Output.DICT)
            for i,w in enumerate(d['text']):
                w=w.strip(); c=float(d['conf'][i])
                if c<30 or len(w)<2 or not re.search(r'[A-Za-z]{2}',w): continue
                x,y,ww,hh=[v//fx for v in (d['left'][i],d['top'][i],d['width'][i],d['height'][i])]
                if hh>45 or hh<6 or ww>W*0.6: continue
                sub=img[max(0,y-3):y+hh+3,max(0,x-3):x+ww+3].astype(int)
                if sub.size==0: continue
                border=np.concatenate([sub[0],sub[-1],sub[:,0],sub[:,-1]])
                if np.median(border,axis=0).min()<185 and c<85: continue
                if (sub.sum(2)<450).mean()>0.45: continue                       # mostly dark = drawing, not a label          # keep busy anatomy untouched
                boxes.append([x,y,x+ww,y+hh])
    mask=np.zeros((H,W),np.uint8)
    for x0,y0,x1,y1 in boxes:
        x0=max(0,x0-3);y0=max(0,y0-3);x1=min(W,x1+3);y1=min(H,y1+3)
        sub=img[y0:y1,x0:x1].astype(int); border=np.concatenate([sub[0],sub[-1],sub[:,0],sub[:,-1]]); med=np.median(border,axis=0)
        m=(np.abs(sub-med).sum(2)>70) if med.min()<=200 else (sub.sum(2)<620)
        mask[y0:y1,x0:x1]=np.maximum(mask[y0:y1,x0:x1],(m*255).astype(np.uint8))
    mask=cv2.dilate(mask,np.ones((3,3),np.uint8),iterations=2)
    out=cv2.inpaint(img,mask,5,cv2.INPAINT_TELEA)
    # merge overlapping boxes, words on a line, then stacked lines of one label
    def near(a,b):
        h=min(a[3]-a[1],b[3]-b[1],40)
        vo=min(a[3],b[3])-max(a[1],b[1]); gap=max(a[0],b[0])-min(a[2],b[2])
        if vo>0.5*min(a[3]-a[1],b[3]-b[1]) and gap<1.0*h: return True     # same line, word gap
        vgap=max(a[1],b[1])-min(a[3],b[3])
        if -2<vgap<0.55*h and (abs(a[0]-b[0])<1.5*h or abs(a[2]-b[2])<1.5*h or abs((a[0]+a[2])-(b[0]+b[2]))<2*h): return True   # stacked line of one label
        return False
    G=[list(b) for b in boxes]; ch=True
    while ch:
        ch=False
        for i in range(len(G)):
            for j in range(i+1,len(G)):
                if near(G[i],G[j]):
                    G[i]=[min(G[i][0],G[j][0]),min(G[i][1],G[j][1]),max(G[i][2],G[j][2]),max(G[i][3],G[j][3])]; G.pop(j); ch=True; break
            if ch: break
    return out,G
def render(pdf,pg,name):
    d=pymupdf.open(pdf); p=d[pg-1]; R=figrect(p)
    title,txt=slide_text(p,R)
    if R.is_empty: return None
    R=(R+(-2,-2,2,2))&p.rect
    # render figure only (drop overlapping PDF text such as figure legends)
    a0=p.get_pixmap(matrix=pymupdf.Matrix(3,3),clip=R)
    A=np.array(Image.frombytes('RGB',(a0.w,a0.h),a0.samples))
    for w in p.get_text('words'):
        if pymupdf.Rect(w[:4]).intersects(R): p.add_redact_annot(pymupdf.Rect(w[:4])+(-1,-1,1,1),fill=False)
    p.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE,graphics=pymupdf.PDF_REDACT_LINE_ART_NONE,text=pymupdf.PDF_REDACT_TEXT_REMOVE)
    q0=p.get_pixmap(matrix=pymupdf.Matrix(3,3),clip=R); Q=np.array(Image.frombytes('RGB',(q0.w,q0.h),q0.samples))
    Q,groups=ocr_erase(Q)
    qi=Image.fromarray(Q); dr=ImageDraw.Draw(qi)
    for k,(x0,y0,x1,y1,*_) in enumerate(sorted(groups,key=lambda g:(g[1],g[0])),1):
        cx,cy=(x0+x1)/2,(y0+y1)/2; r=19
        dr.ellipse((cx-r,cy-r,cx+r,cy+r),fill=(217,79,127),outline='white',width=3); dr.text((cx,cy),str(k),fill='white',font=FONT,anchor='mm')
    fq=f'assets/p3rep_{name}_q.jpg'; fa=f'assets/p3rep_{name}_a.jpg'
    qi.save(fq,quality=90); Image.fromarray(A).save(fa,quality=90)
    return f'{fq}?v={V}',f'{fa}?v={V}',re.sub(r'^LO\d:\s*','',title),txt,len(groups)
TAG={'m':'📖 course slide · Lecture 23 Male reproductive','f':'📖 course slide · Lecture 24 Female reproductive'}
DECKS={
 'm':[('Scrotum + testis',[6,8,9,10]),('Epididymis + ductus deferens',[11,12,13,14]),('Penis',[19,20,21,22,24,25,26,27,28]),('Prostate + blood supply',[29,30,31,32,33,34,35,37])],
 'f':[('Broad ligament + ovary',[4,5,6,7,8,9]),('Uterus, vagina + vestibule',[13,14,15]),('External genitalia + blood supply',[16,17,19,20])],
}
cards={}
for sx,pdf in (('m',MALE),('f',FEM)):
    for name,pgs in DECKS[sx]:
        cs=[]
        for pg in pgs:
            r=render(pdf,pg,f'{sx}{pg}')
            if not r: continue
            qi,ai,title,txt,n=r
            clue=txt if len(txt)<480 else txt[:460].rsplit(' ',1)[0]+'…'
            q=f'{title} · name each numbered label.' if n else f'{title} · identify what is shown.'
            cs.append(img_card_facts(q,qi,title,clue,ai,[],TAG[sx]+f' · slide {pg}'))
        cards[(sx,name)]=cs
# photo cards (real specimens; labels are PDF text → handled by render too)
PHOTO=[(MALE,'m',15,'Identify the structure held up by the forceps.','Spermatic cord','Begins at the vaginal ring; passes through the inguinal canal (descent of the testis).'),
       (FEM,'f',8,'Identify the organ (two specimens).','Ovary','Smooth before estrus; rough + nodular in multiparous bitches. Lies caudal to the kidney.')]
photos=[]
for pdf,sx,pg,q,a,c in PHOTO:
    d=pymupdf.open(pdf); p=d[pg-1]; R=figrect(p)
    if sx=='f': R=pymupdf.Rect(R.x1-90,R.y0,R.x1,R.y0+150)&R
    pm=p.get_pixmap(matrix=pymupdf.Matrix(3,3),clip=R); fn=f'assets/p3rep_photo{sx}{pg}.jpg'
    Image.frombytes('RGB',(pm.w,pm.h),pm.samples).save(fn,quality=90)
    photos.append(img_card_facts(q,f'{fn}?v={V}',a,c,'',[],('📚' if sx else '')+' course slide photo · '+TAG[sx].split('· ')[1]+f' · slide {pg}'))
D=lambda q,a,t:text_card2(q,a,'🧠 '+t)
TERMS=[
 D('Layers around the testis, outside → in.','Scrotal skin · tunica dartos · scrotal septum · external spermatic fascia · parietal layer of vaginal tunic · visceral layer of vaginal tunic · tunica albuginea','Lecture 23'),
 D('Proper ligament of the testis vs ligament of the tail of the epididymis vs scrotal ligament?','Proper ligament of the testis: testis → tail of the epididymis · ligament of the tail of the epididymis: tail of the epididymis → vaginal tunic + spermatic fascia · scrotal ligament: tunica dartos → ligament of the tail of the epididymis (remnants of the gubernaculum testis)','Lecture 23'),
 D('Three parts of the epididymis + where each sits.','Head (caput): cranial medial surface of the testis, twists to the lateral side · body (corpus): dorsolateral surface · tail (cauda): caudal extremity, attached by the proper ligament of the testis','Lecture 23'),
 D('Mesorchium + testicular bursa?','Mesorchium = visceral vaginal tunic attaching the medial edge of the epididymis to the testis; it extends over the lateral surface of the epididymis to form a potential space, the testicular bursa','Lecture 23'),
 D('Anatomical vs surgical/clinical spermatic cord?','Anatomical: ductus deferens + its vessels · mesoductus deferens · testicular artery · testicular veins (pampiniform plexus) · lymphatics · testicular nerve plexus · mesorchium. Surgical adds: cremaster muscle + parietal vaginal tunic','Lecture 23'),
 D('Cryptorchidism timeline?','Most puppies: testes in the scrotum by 6 weeks · cryptorchid if descent not complete by 7 months · unilateral or bilateral · abdominal or inguinal','Lecture 23'),
 D('Three divisions of the penis + their parts.','Root: left + right crura, bulb of the penis · body: two corpora cavernosa (+ corpus spongiosum + urethra, in tunica albuginea) · glans: bulbus glandis + pars longa glandis','Lecture 23'),
 D('Penile muscles: origin + job.','Ischiocavernosus m.: ischiatic tuberosity, encloses the crura · bulbospongiosus m.: surrounds the bulb, from the external anal sphincter · retractor penis m.: mainly smooth, from the first two caudal vertebrae · ischiourethralis m.: ischiatic tuberosity → fibrous ring around the dorsal vein of the penis','Lecture 23'),
 D('Prostate: position + where the ductus deferens open.','Surrounds the urethra at the bladder neck; dorsal surface covered by peritoneum, ventral retroperitoneal; bounded dorsally by the rectum, ventrally by the pubic symphysis + ventral wall; median septum → right + left lobes. Ductus deferens open into the urethra by slits on each side of the colliculus seminalis','Lecture 23'),
 D('Male lymph drainage.','Scrotum → superficial inguinal lymph nodes · testis + epididymis → medial iliac + lumbar aortic lymph nodes · prostate → medial + internal iliac lymph nodes · prepuce + penis → superficial inguinal lymph nodes','Lecture 23'),
 D('Three regions of the broad ligament + what each holds.','Mesovarium → ovary · mesosalpinx → uterine tube · mesometrium → uterine horns + body. Ovarian bursa = pouch formed by mesovarium + mesosalpinx around the ovary','Lecture 24'),
 D('Suspensory vs proper ligament of the ovary vs round ligament of the uterus?','Suspensory: middle + ventral thirds of the 12th/13th rib → ovary · proper: caudal continuation, ovary → uterine horn · round ligament of the uterus: fibrous cord in the free border of the laterally extended mesometrium, ovary region → inguinal canal','Lecture 24'),
 D('Uterine tube parts.','Fimbriae (capture the oocyte) · infundibulum with the abdominal ostium · tubular part (site of fertilization) · uterine ostium into the uterine horn at the tubouterine junction','Lecture 24'),
 D('Cervix: position + canal.','Most caudal part of the uterus; lies obliquely across the uterovaginal junction; cervical canal runs from the internal uterine orifice to the external uterine orifice','Lecture 24'),
 D('Vagina + vestibule key points.','Vagina: very long in dogs, mostly retroperitoneal, longitudinal + transverse folds, vaginal fornix cranial to the cervix · vestibule: urethral tubercle (external urethral orifice) on the cranioventral wall, no mucosal folds, vestibular bulb on each side','Lecture 24'),
 D('Female blood supply.','Ovarian artery → uterine + tubal branches · internal pudendal artery → vaginal artery → uterine artery, artery of the clitoris, artery of the vestibular bulb','Lecture 24'),
 D('Female lymph drainage.','Ovary → lumbar aortic · uterus → lumbar aortic, medial iliac, hypogastric, lateral sacral · vagina → hypogastric, lateral sacral · vestibule → hypogastric, lateral sacral · vulva + clitoris → superficial inguinal','Lecture 24'),
]
CSS=open('tools/p3simplify.py').read().split("CSS='")[1].split("'")[0]
def write(fn,title,sub,cs,back):
    cs=list(cs); cs[0]=cs[0].replace('class="card"','class="card on"',1)
    open(fn,'w').write(page(title,sub,''.join(cs),back=back).replace('</style>',CSS+'</style>',1))
for f in os.listdir('.'):
    if re.match(r'gross-anatomy-lab25-',f): os.remove(f)
links={'m':[],'f':[]}; k=0
for (sx,name),cs in cards.items():
    k+=1; fn=f'gross-anatomy-lab25-diag{k}.html'
    write(fn,f'Lab 25 · {name}',f'📖 Diagram images · labels erased + numbered · {len(cs)} cards',cs,'gross-anatomy-lab25-images.html')
    links[sx].append((fn,('♂ ' if sx=='m' else '♀ ')+name,len(cs)))
write('gross-anatomy-lab25-best1.html','Lab 25 · Course slide photos','⭐ real specimens · 2 cards',photos,'gross-anatomy-lab25-images.html')
write('gross-anatomy-lab25-terms.html','Lab 25 · 🧠 No-image terms',f'{len(TERMS)} cards',TERMS,'gross-anatomy-lab25-images.html')
a=lambda rows:''.join(f'<a href="{fn}?v={V}">{E(nm)}<span>{n} cards</span></a>' for fn,nm,n in rows)
hub=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><title>Lab 25</title><style>{HUBCSS}</style></head><body><div class="wrap"><a class="back" href="gross-anatomy-practical3.html?v={V}">← Back to Practical 3</a><div class="hero"><h1>Lab 25 · Male + female reproductive</h1><p>From Lectures 23 + 24. Small decks, one tap = full answer. 🐾</p></div>
<details class="sec chk"><summary>✅ Bold-term checklist · waiting on your list</summary><p>Send your Lab 25 Canvas bold-term screenshots and this becomes a full checklist (same order as your list), plus ⭐ photo blocks from your dissection photos.</p></details>
<div class="sec main"><h2>⭐ Real photos · start here</h2><p>Only 2 specimen photos are in the lecture slides so far. Your lab photos go here.</p>{a([('gross-anatomy-lab25-best1.html','Course slide photos',len(photos))])}</div>
<div class="sec diag" style="border-left:7px solid #4f8fc0"><h2>📖 Diagram images</h2><p>Lecture drawings. Labels erased + numbered; reveal shows the labeled original + the slide text.</p>{a(links['m']+links['f'])}</div>
<div class="sec terms"><h2>🧠 No-image terms</h2>{a([('gross-anatomy-lab25-terms.html','Concepts + integration',len(TERMS))])}</div></div></body></html>'''
open('gross-anatomy-lab25-images.html','w').write(hub)
# cross-lab: male → Lab 21 hub, female → Lab 22 hub (📖 section, marked so reruns replace it)
for n,sx,lbl in ((21,'m','♂ Lecture 23 male reproductive'),(22,'f','♀ Lecture 24 female reproductive')):
    hf=f'gross-anatomy-lab{n}-images.html'; h=open(hf).read()
    h=re.sub(r'<div class="sec diag" data-src="repro".*?</div>','',h,flags=re.S)
    blk=f'<div class="sec diag" data-src="repro" style="border-left:7px solid #4f8fc0"><h2>📖 Diagram images · {lbl}</h2><p>Lecture drawings that show this lab&#39;s bold terms (also on the Lab 25 hub). Labels erased + numbered.</p>{a(links[sx])}</div>'
    h=h.replace('<div class="sec more"',blk+'<div class="sec more"',1)
    open(hf,'w').write(h)
print({k:len(v) for k,v in cards.items()},'photos',len(photos),'terms',len(TERMS))
