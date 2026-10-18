"""Practical 3 · 🩻 Abdominal radiology hub (Dr. McHaney).  Made by Claude.
Sources: 'Normal Radiographic Anatomy of the Abdomen Student 2026 - Tagged.pdf' (lecture, LEC)
         'Lecture 25 Abdominal Anatomy Lab 2026.pdf' (radiology lab questions, LAB).
Each card = the slide's radiographs only (title + bullets cropped off, PDF text labels erased by redaction;
arrows/circles/overlays kept), ONE tap reveals the answer + the labeled original.
The lab PDF has NO answer key: answers there are Claude's read, tagged with a confidence level.
Run from repo root:  python3 tools/p3rad.py <LEC.pdf> <LAB.pdf>"""
import sys,os,re,time,html
sys.path.insert(0,'tools')
import pymupdf
from PIL import Image,ImageFilter
import deck; deck.PRACTICAL=3
from deck import img_card_facts,text_card2,page,HUBCSS,E
LEC,LAB=sys.argv[1],sys.argv[2]
V=str(int(time.time())); P='rad'
for f in os.listdir('assets'):
    if f.startswith('p3rad_'): os.remove('assets/'+f)

def crop(pdf,pg,name,extra=()):
    """render the radiograph area of a slide twice: q = text labels removed, a = as shown in class"""
    d=pymupdf.open(pdf); p=d[pg-1]; W,H=p.rect.width,p.rect.height
    ims=[(pymupdf.Rect(x['bbox']),x) for x in p.get_image_info(xrefs=True)]
    ims=[(r,x) for r,x in ims if r.width<W*0.98 or r.height<H*0.98]
    R=pymupdf.Rect(); zoom=2.0
    for r,x in ims:
        if r.width<25 or r.height<25: continue
        R|=r
        try: zoom=max(zoom,min(4,x['width']/max(r.width,1)))
        except Exception: pass
    for dr in p.get_drawings():
        if any(dr['rect'].intersects(r) for r,_ in ims) and dr['rect'].width<W*0.9: R|=dr['rect']
    for e in extra: R|=pymupdf.Rect(e)
    R=(R+(-4,-4,4,4))&p.rect
    M=pymupdf.Matrix(zoom,zoom)
    a=p.get_pixmap(matrix=M,clip=R); A=Image.frombytes('RGB',(a.w,a.h),a.samples)
    for w in p.get_text('words'):
        r=pymupdf.Rect(w[:4])
        if r.intersects(R): p.add_redact_annot(r+(-1,-1,1,1),fill=False)
    p.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE,graphics=pymupdf.PDF_REDACT_LINE_ART_NONE,text=pymupdf.PDF_REDACT_TEXT_REMOVE)
    q=p.get_pixmap(matrix=M,clip=R); Q=Image.frombytes('RGB',(q.w,q.h),q.samples)
    out=[]
    for tag,im in (('q',Q),('a',A)):
        if im.width>2200: im=im.resize((2200,int(im.height*2200/im.width)),Image.LANCZOS)
        fn=f'assets/p3rad_{name}_{tag}.jpg'; im.save(fn,quality=90); out.append(f'{fn}?v={V}')
    return out

LT='📚 course slide · Dr. McHaney radiology lecture'
QT='🩻 radiology lab · Lecture 25'
# ---------- 1 · Radiology LAB questions (no key in the PDF → confidence tags) ----------
HI,MD,LO='✅ high confidence','⚠️ moderate confidence — confirm in lab','❓ low confidence — ask Dr. McHaney'
LABQ=[
 (3,'Q4–5 films · Name all three views.','Right lateral (top left) · left lateral (bottom) · ventrodorsal (VD, right)','The three standard abdominal views. Markers (RIGHT / LEFT) tell you which lateral = which side is DOWN.',HI),
 (7,'Q6 · Right lateral or left lateral? How do you know?','Left lateral','Gas rises to the NON-dependent part of the stomach. Here the gas pocket is ventral = the pylorus (right side is up) → left lateral. In a right lateral, gas fills the fundus (dorsal).',MD),
 (8,'Q7 · Identify the indicated structure.','Cecum','C-shaped, compartmentalized, gas-filled, right mid abdomen on the VD (dog).',HI),
 (9,'Q8 · Which lymph nodes, not normally seen, sit in the circled region?','Medial iliac (iliosacral / sublumbar) lymph nodes','Ventral to L6–L7, dorsal to the descending colon. Drain the pelvic limbs + perineal region.',HI),
 (10,'Q9 · Identify the indicated vascular structure (can mimic a ureteral stone or enlarged lymph node).','Deep circumflex iliac artery','Seen end-on as a small round soft-tissue opacity ventral to the caudal lumbar spine.',HI),
 (11,'Q10 · The patient ate a sock (arrow). Which GI segment holds it?','Descending duodenum (best read)','Tubular, right side of the VD, running caudally along the right body wall toward the caudal flexure (~L5–L6). Alternative to rule out with the key: ascending colon (much shorter, near the cecum).',LO),
 (12,'Q11 · Identify the indicated structure.','Liver · right side, caudolateral margin (best read)','Arrow tip sits at the right cranial abdomen just inside the costal arch, where the liver margin borders the body wall. Check the key: right kidney (cranial pole) is the other candidate.',LO),
 (13,'Q12 · Right lateral or left lateral? How do you know?','Left lateral (best read)','Gas outlines the pylorus + proximal duodenum (ventral → curving dorsally) — those are UP in left lateral recumbency. Right lateral would put gas in the dorsal fundus.',MD),
 (14,'Q13 · Sick dog, ↑ liver enzymes, circled abnormality. Which two organs could it be?','Liver and gallbladder','Ventral + right cranial abdomen (circled on both views) = liver; the gallbladder sits ventral and on the right aspect of the liver. Mineral foci here = possible choleliths / biliary mineralization.',MD),
 (15,'Q14 · Identify the specific region of the stomach indicated (right + left laterals).','Fundus','Dorsal + cranial part of the stomach, right under the diaphragm on both laterals.',MD),
 (16,'Q15 · Which lymph nodes, not normally seen, sit in the circled region?','Mesenteric lymph nodes','Central (mid) abdomen; drain the abdominal viscera; when big they push small intestine peripherally.',HI),
 (17,'Q16 · Identify the indicated structure (seen sometimes, especially in obese cats).','Left lobe (left limb) of the pancreas','Runs along the greater curvature of the stomach, caudal to it on the left. Lecture: "left limb sometimes visible in obese cats."',HI),
 (18,'Q17 · Identify the indicated structure.','Prostate (enlarged)','Round soft tissue at the pelvic inlet, caudodorsal to the bladder, ventral to the rectum, dorsal to the pubis. Visible = intact male (benign prostatic hyperplasia).',MD),
 (19,'Q18 · Abnormal urinary tract (cat). Identify the abnormal opacities in the indicated kidney.','Mineral opacities = nephroliths (renal calculi)','Small mineral-opaque foci inside the kidney silhouette; the mineral just caudoventral to it suggests ureteroliths too.',MD),
 (20,'Q19 · Same cat, VD. Which kidney is indicated?','Right kidney (best read)','On a standard VD the patient\'s right is on the viewer\'s left (no marker visible on this crop). Also the more cranial of the two.',MD),
 (21,'Q20 · Identify the indicated structure. Be specific.','Urinary bladder · apex (best read)','Soft-tissue opacity in the caudoventral abdomen cranial to the pubis. "Be specific" = name the REGION: apex (cranial), body, neck/trigone.',LO),
 (22,'Q21 · Which liver lobe is indicated in this cat?','Right lateral liver lobe','Cats: the caudoventral liver margin = right lateral lobe (dogs = left lateral lobe).',HI),
 (23,'Q22 · Identify the specific region of the stomach indicated.','Pylorus','Ventral part of the stomach; gas-filled on the LEFT lateral (right side up).',HI),
]
labcards=[]
for pg,q,name,why,conf in LABQ:
    qi,ai=crop(LAB,pg,f'lab{pg}')
    labcards.append(img_card_facts(q,qi,name,f'{why} · {conf}',ai,[],QT+(' · '+conf.split(' ')[0])))
# practice films: systematic read (no key)
SYS='Systematic read: 1 extra-abdominal (soft tissues, body wall, diaphragm, skeleton, thorax) → 2 serosal detail + contour → 3 liver + spleen → 4 kidneys, bladder, reproductive → 5 stomach, small intestine, colon. Name what you ALWAYS see, SOMETIMES see, NEVER normally see.'
prac=[]
for i,pg in enumerate(range(25,35),1):
    qi,ai=crop(LAB,pg,f'lab{pg}')
    prac.append(img_card_facts(f'Practice film {pg-24} · Name the view, then read it systematically.',qi,'Your read',SYS,ai,[],QT+' · extra normal film (no key)'))

# ---------- 2 · Lecture radiographs ----------
L=lambda pg,q,a,c='':(pg,q,a,c)
LECQ={
'Views + technique':[
 L(7,'Name each standard view.','Left lateral · right lateral · ventrodorsal (VD)','Take BOTH laterals: gas/fluid shift shows different parts of the stomach.'),
 L(9,'What additional view is this, and what do c / u / b mark?','Compression view · c = colon · u = uterus · b = urinary bladder','Compression reduces superimposition over an area of interest.'),
 L(11,'Which additional view is this?','Pneumocolonogram (negative contrast: air in the colon)','Pneumogastrogram = air in the stomach. Both outline GI position.'),
 L(12,'Which additional view is this, and why take it?','Lateral with pelvic limbs pulled forward (perineal view)','Shows the region of the urethra · evaluation of urinary stones.'),
 L(13,'What view is this, and what does the arrow show?','Horizontal beam · free gas','Horizontal beam highlights free (peritoneal) gas, which rises to the top.'),
 L(61,'Positive or negative contrast in each film?','Left = positive contrast (barium) · right = negative contrast (air)','Both outline the GI tract.'),
],
'Extra-abdominal + serosal detail':[
 L(17,'What do the arrows / dotted outline show?','External structures: nipples / prepuce','Surrounded by air → easily seen. Don\'t call them abdominal masses.'),
 L(20,'What do the dashed lines trace?','Lumbar musculature margins','Epaxial = dorsal to the transverse processes · hypaxial = ventral. They can create confusing lines.'),
 L(23,'Vomiting dog, pneumonia on the VD. Which lung lobe? (arrow)','Right middle lung lobe (best read · ⚠️ confirm)','Aspiration pneumonia classically hits the right middle lobe (dependent, straight bronchus).'),
 L(25,'What do the dashed lines outline?','Diaphragm: cupola (dome) + right and left crura','Only the THORACIC surface is visible: the abdominal side border-effaces with the liver.'),
 L(26,'Why is the abdominal surface of the diaphragm visible in each film?','Left: falciform fat · right: free peritoneal gas (ruptured bowel)','The 2 exceptions to "only the thoracic surface is visible."'),
 L(28,'What do the dashed lines mark?','Body wall','Ventral + lateral abdominal wall margins.'),
 L(33,'Why is serosal detail poor here?','Emaciation','Too little fat = less natural contrast.'),
 L(34,'Why is serosal detail poor here?','Young age','Brown fat = higher water content → less contrast.'),
 L(35,'Which film has peritoneal effusion?','Top = moderate effusion · bottom = normal','Fluid erases serosal margins.'),
 L(36,'Why is serosal detail lost?','Severe peritoneal effusion',''),
 L(37,'Why is serosal detail poor here?','Serosal disease (peritonitis, carcinomatosis)',''),
 L(38,'Why is serosal detail poor here?','Mass effect / organomegaly',''),
 L(39,'Why is serosal detail poor here?','Radiographic technique / patient factors','Large dogs scatter the x-ray beam more.'),
],
'Liver + spleen':[
 L(42,'Dog: which liver lobe forms the caudoventral margin?','Left lateral liver lobe','Caudoventral margin = easiest liver edge to see.'),
 L(43,'Cat: which liver lobe forms the caudoventral margin?','Right lateral liver lobe',''),
 L(44,'What do the blue lines show, and the 3 liver-size indicators?','Gastric axis · shape of the margins · caudal extent','Normal gastric axis: perpendicular to the spine / parallel to the ribs.'),
 L(45,'Top vs bottom: hepatomegaly or microhepatica?','Top = hepatomegaly · bottom = microhepatica','Big liver pushes the gastric axis caudally; small liver tips it cranially.'),
 L(46,'What is inside the blue boxes?','Spleen · head (left cranial abdomen, VD) + tail (ventral, lateral)','Head immobile, tail mobile. Dogs: usually seen ventrally on the lateral; cats: usually NOT.'),
 L(48,'The splenic head is attached to the stomach. By what?','Gastrosplenic ligament',''),
],
'Urogenital':[
 L(50,'Which film is the cat, which is the dog?','Top = feline (rounder kidneys) · bottom = canine (elongate)','Kidneys: cranial + dorsal, retroperitoneal; left is more caudal ("left is left behind").'),
 L(51,'What is outlined in blue?','Kidneys (superimposed on the lateral)','Cranial pole of the RIGHT kidney is hidden by superimposition on the lateral.'),
 L(53,'How do you size a kidney here?','VD · dog 2.5–3.5 × length of L2 · cat 2–3 × L2',''),
 L(56,'Identify the arrowed structure.','Aorta','Retroperitoneal vessel, occasionally seen.'),
 L(57,'Identify the arrowed structure.','Deep circumflex iliac artery','Seen end-on; can be mistaken for a ureteral stone or lymph node.'),
 L(58,'Name the 3 colored regions.','Urinary bladder: apex · body · neck/trigone','Bladder extends cranially from the pelvic canal; rounds up as it fills.'),
 L(59,'What is the dashed outline on the VD?','Urinary bladder','Harder to see on the VD: superimposed pelvis, spine, colon.'),
 L(83,'What is outlined by contrast?','Ureters (excretory study)','Only seen with contrast unless massively distended; sometimes ureteral stones are visible.'),
 L(85,'Contrast study: name the 3 parts of the male urethra.','Prostatic · membranous (pelvic) · penile','Urethra needs contrast; perineal view (limbs pulled forward) shows the region best.'),
 L(87,'Name c / u / b.','c = colon · u = uterus · b = urinary bladder','Uterus: dorsal to the bladder, ventral to the colon; tubular, soft-tissue opaque.'),
 L(88,'What do the arrows show?','Uteromegaly (enlarged uterus)',''),
 L(89,'What do you see, and when does it show?','Gravid uterus · enlargement 25–30 days · fetal mineralization: cats 35–39 d, dogs 42–45 d',''),
 L(90,'Identify the soft tissue at the pelvic inlet (intact male).','Prostate','Ventral to rectum, dorsal to pubis; normal < 70% of pelvic-inlet height. Not seen in neutered males or cats.'),
 L(91,'What is the orange triangle, and why does it matter?','Triangle of fat','Separates the prostate from the bladder + ventral body wall. Important landmark!'),
 L(92,'What is outlined (dashed)?','Medial iliac (iliosacral / sublumbar) lymph nodes · enlarged','Ventral to L6–L7, dorsal to the descending colon; drain pelvic limbs + perineum.'),
 L(93,'What do the arrows show?','Mesenteric lymph nodes (enlarged)','Central abdomen; push small intestine peripherally.'),
],
'GI tract':[
 L(64,'What is outlined in each film?','Stomach (empty vs distended)','Size varies with the degree of distension.'),
 L(65,'Name the four lettered regions (VD + lateral, barium).','C = cardia · F = fundus · B = body · P = pylorus',''),
 L(66,'Name F / D / P.','F = fundus · D = duodenum · P = pylorus',''),
 L(67,'Which film is the right lateral and which is the left lateral? How do you know?','Left image = right lateral (gas in the fundus) · right image = left lateral (gas in the pylorus + duodenum)','Gas rises to the non-dependent part.'),
 L(68,'Barium: which is the right lateral and which is the left lateral?','Left image = right lateral (barium pools in the dependent pylorus) · right image = left lateral (barium in the fundus)','Fluid/barium pools in the dependent part.'),
 L(69,'Which is the DV and which is the VD?','Left = DV (barium in pylorus + body, gas in fundus) · right = VD (barium pools in the dorsal fundus)',''),
 L(71,'Dog or cat? What does normal small intestine look like?','Top = dog · bottom = cat','Tubular, uniform diameter, gas/fluid/mixed, smooth serosa. You CANNOT judge wall thickness on radiographs.'),
 L(74,'What do the red lines compare?','Small intestinal diameter vs the narrowest height of L5','Dog: < 1.6 × L5 height · cat: < 12 mm or < 2 × body of L4.'),
 L(75,'Barium enema: name CC, IC and Tip.','CC = cecocolic junction · IC = ileocolic junction · Tip = cecum (apex)','Abbreviation expansion is Claude\'s (not on the slide) — confirm.'),
 L(76,'What is circled?','Cecum (dog)','C-shaped, compartmentalized, usually gas-filled, right mid abdomen. Don\'t call it abnormal small intestine.'),
 L(77,'What is bracketed?','Cecum (cat)','Cone-shaped; rarely seen without barium.'),
 L(78,'What do the red lines compare?','Colon diameter vs L7 length','Dog: < length of L7 · cat: < 1.3 × length of L5.'),
 L(80,'What is the mineral opacity?','Gallbladder (mineralized)','Usually border-effaced with the liver; ventral + right aspect of the liver.'),
 L(82,'What is in the blue box (obese cat)?','Left limb (left lobe) of the pancreas','Body = pyloroduodenal angle · right lobe = descending duodenum (bigger in dogs) · left lobe = greater curvature (bigger in cats).'),
]}
lec={}
for grp,rows in LECQ.items():
    lec[grp]=[]
    for pg,q,a,c in rows:
        qi,ai=crop(LEC,pg,f'lec{pg}')
        lec[grp].append(img_card_facts(q,qi,a,c,ai,[],LT+f' · slide {pg}'))

# ---------- 3 · No-image concepts ----------
D=lambda q,a:text_card2(q,a,'🧠 radiology lecture')
TERMS=[
 D('Rank the 5 radiographic opacities, least → most opaque.','Gas · fat · soft tissue · mineral · metal'),
 D('When do you take an abdominal radiograph, and what must be in the field?','End of expiration (less motion blur) · pelvic limbs extended · diaphragm to the coxofemoral joints'),
 D('Why take BOTH lateral projections?','Gas rises and fluid pools: each lateral shows a different part of the stomach (right lateral → gas in fundus; left lateral → gas in pylorus/duodenum)'),
 D('4 additional views + why.','Compression (less superimposition) · pneumogastrogram/pneumocolonogram (outline GI) · lateral with pelvic limbs pulled forward = perineal view (urethra, urinary stones) · horizontal beam (free gas)'),
 D('Systematic order for reading the abdomen?','Extra-abdominal (soft tissues, body wall, diaphragm, skeleton, thorax) → serosal detail + contour → liver + spleen → urogenital → GI'),
 D('What gives natural contrast in the abdomen?','Fat (around the serosal margins of organs)'),
 D('Causes of poor serosal detail (6).','Emaciation · young age (brown fat = more water) · peritoneal effusion · serosal disease (peritonitis, carcinomatosis) · mass effect/organomegaly · technique/patient factors (large dogs scatter more)'),
 D('Liver borders?','Cranial: diaphragm · caudal: stomach, right kidney, small intestine · lateral: body wall · ventral: falciform fat'),
 D('Retroperitoneal space: always / sometimes / never seen?','Visible: lumbar muscles, kidneys · occasionally: blood vessels · not normally: ureters, adrenal glands, lymphatic vessels, lymph nodes'),
 D('Kidney size on the VD?','Dog 2.5–3.5 × L2 length · cat 2–3 × L2 length'),
 D('Small intestine size limits?','Dog < 1.6 × narrowest height of L5 body (lateral) · cat < 12 mm or < 2 × body of L4 (lateral). Interpret with caution.'),
 D('Large intestine size limits?','Dog < length of L7 body (lateral) · cat < 1.3 × length of L5 body'),
 D('Stomach position: dog vs cat?','Dog: left body wall → right body wall · cat: J-shaped, mostly left cranial quadrant, pylorus on midline. Caudal to liver, cranial to colon + small bowel.'),
 D('Cecum: dog vs cat?','Dog: right mid abdomen, C-shaped, usually gas-filled · cat: cone-shaped, rarely seen (may need barium)'),
 D('Adrenal gland positions + enlargement sign?','Lateral to the caudal vena cava + aorta · right: medial and slightly cranial to the right kidney · left: relatively more cranial to its kidney · enlargement pushes the kidney caudally + laterally'),
 D('Pancreas: where is each part?','Body: pyloroduodenal angle · right lobe: descending duodenum (larger in dogs) · left lobe: greater curvature of the stomach (larger in cats; left limb sometimes seen in obese cats)'),
 D('Prostate: when visible + size limit?','Intact males (benign prostatic hyperplasia); NOT neutered males or cats; not usually on VD. Ventral to rectum, dorsal to pubis, < 70% of pelvic-inlet height.'),
 D('Gravid uterus timeline?','Enlargement 25–30 days · fetal mineralization cats 35–39 d, dogs 42–45 d'),
 D('Medial iliac vs mesenteric lymph nodes?','Medial iliac (iliosacral/sublumbar): ventral to L6–L7, dorsal to descending colon, drain pelvic limbs + perineum · mesenteric: central, drain abdominal viscera, push small intestine peripherally'),
 D('Cat small left kidney hidden by GI superimposition: what technique helps?','Compression view (reduces superimposition)'),
 D('Gallbladder sits between which two liver lobes?','Quadrate lobe and right medial lobe (standard anatomy · not on the slide)'),
 D('Which DV/VD shows the fundus filled with barium?','VD (dorsal recumbency): barium pools in the dorsal fundus · DV: gas rises into the fundus'),
]
# ---------- write pages + hub ----------
CSS=open('tools/p3simplify.py').read().split("CSS='")[1].split("'")[0]
def write(fn,title,sub,cards):
    cs=list(cards); cs[0]=cs[0].replace('class="card"','class="card on"',1)
    pg=page(title,sub,''.join(cs),back=f'gross-anatomy-rad-abd-images.html')
    open(fn,'w').write(pg.replace('</style>',CSS+'</style>',1))
def blocks(name,cards,key):
    out=[];n=(len(cards)+11)//12
    for i in range(n):
        part=cards[i*len(cards)//n:(i+1)*len(cards)//n]; fn=f'gross-anatomy-rad-abd-{key}{i+1}.html'
        nm=name+(f' {i+1}' if n>1 else ''); write(fn,f'🩻 {nm}',f'{len(part)} cards',part); out.append((fn,nm,len(part)))
    return out
for f in os.listdir('.'):
    if f.startswith('gross-anatomy-rad-abd-') and f!='gross-anatomy-rad-abd-images.html': os.remove(f)
L1=blocks('Radiology lab questions',labcards,'lab')
L2=[]
for i,(g,cs) in enumerate(lec.items(),1): L2+=blocks(g,cs,f'lec{i}-')
L3=blocks('Extra normal films',prac,'prac')
L4=blocks('Concepts + numbers',TERMS,'terms')
a=lambda rows:''.join(f'<a href="{fn}?v={V}">{E(nm)}<span>{k} cards</span></a>' for fn,nm,k in rows)
hub=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><title>Abdominal radiology</title><style>{HUBCSS}</style></head><body><div class="wrap"><a class="back" href="gross-anatomy-practical3.html?v={V}">← Back to Practical 3</a><div class="hero"><h1>🩻 Abdominal radiology</h1><p>Dr. McHaney · radiograph ID for the practical. Small decks, one tap = full answer. 🐾</p></div>
<div class="sec main"><h2>⭐ Radiology lab questions · start here</h2><p>The 18 lab questions (Lecture 25 PDF). Official answer sheet comes AFTER lab. Until then these are best reads, tagged ✅ high · ⚠️ moderate · ❓ low confidence.</p>{a(L1)}</div>
<div class="sec more" style="border-left:7px solid #b48ad6"><h2>📚 Lecture radiographs · by system</h2><p>Slide labels hidden; arrows, circles + colored overlays kept. Reveal shows the slide as taught.</p>{a(L2)}</div>
<div class="sec extra"><h2>📚 Supplemental · extra normal films</h2><p>The "additional normal radiographs for practice." No key: name the view, then do a systematic read.</p>{a(L3)}</div>
<div class="sec terms"><h2>🧠 No-image terms</h2>{a(L4)}</div></div></body></html>'''
open('gross-anatomy-rad-abd-images.html','w').write(hub)
print('lab',len(labcards),'lecture',sum(len(v) for v in lec.values()),'practice',len(prac),'terms',len(TERMS))
