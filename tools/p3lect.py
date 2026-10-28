"""Practical 3 · thorax LECTURE slide pictures (Lectures 12–14 Thorax 1–3, tagged PDFs) → numbered image cards (made by Claude).
- vector text labels on a figure are removed and replaced with pink numbered badges (only bold-relevant ones kept)
- raster figures with printed numbers keep their numbers; the slide legend is the answer
- highlighted / color-coded figures ask for the colored structure
- Miller's veins figure: printed labels found by OCR (tesseract), erased (white), bold ones badged
Cards go to gross-anatomy-lab{17,18}-lect1.html, linked INSIDE the ⭐ section (<!--lect-->). Idempotent; run after p3best/p3web/p3fill:
  python3 tools/p3lect.py <L12.pdf> <L13.pdf> <L14.pdf>"""
import sys,re,os,time,html
sys.path.insert(0,'tools')
import pymupdf,pytesseract
from PIL import Image,ImageDraw,ImageFont
from deck import page,img_card_facts
_src=open('tools/p3split.py').read(); exec(_src[:_src.index('for n in map')])
P={12:sys.argv[1],13:sys.argv[2],14:sys.argv[3]}; V=str(int(time.time())); Z=3
F=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',34)
def badge(d,x,y,n,r=27):
    d.ellipse([x-r,y-r,x+r,y+r],fill=(224,95,168),outline='white',width=5); d.text((x,y),str(n),font=F,fill='white',anchor='mm')
def render(L,pn,R,redact=False):
    doc=pymupdf.open(P[L]); p=doc[pn-1]; R=pymupdf.Rect(R); words=[]
    if redact:
        for w in p.get_text('words'):
            r=pymupdf.Rect(w[:4])
            if r.intersects(R): words.append((r,w[4])); p.add_redact_annot(r+(-1,-1,1,1),fill=False)
        lines=[]
        for b in p.get_text('dict')['blocks']:
            for l in b.get('lines',[]):
                t=' '.join(s['text'] for s in l['spans']).strip(); r=pymupdf.Rect(l['bbox'])
                if t and r.intersects(R): lines.append((r,re.sub(r'\s+',' ',t)))
        p.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE,graphics=pymupdf.PDF_REDACT_LINE_ART_NONE,text=pymupdf.PDF_REDACT_TEXT_REMOVE)
    else: lines=[]
    pm=p.get_pixmap(matrix=pymupdf.Matrix(Z,Z),clip=R); im=Image.frombytes('RGB',(pm.w,pm.h),pm.samples)
    return im,[((r.x0+r.x1)/2*Z-R.x0*Z,(r.y0+r.y1)/2*Z-R.y0*Z,t) for r,t in lines]
def pct(im,x,y): return im.width*x/100,im.height*y/100
C={17:[],18:[]}; N=[0]
def save(im,lab):
    N[0]+=1; f=f'assets/p3lect_{N[0]}.jpg'; im.save(f,quality=91); return f'{f}?v={V}'
def add(lab,q,im,ans,clue,src,facts=()):
    C[lab].append(img_card_facts(q,save(im,lab),ans,clue,'',list(facts),f'📚 course slide · Lecture {src}'))
def manual(L,pn,R,marks,lab,q,clue='',facts=()):
    im,_=render(L,pn,R); d=ImageDraw.Draw(im); ans=[]
    for i,(x,y,name) in enumerate(marks,1): badge(d,*pct(im,x,y),i); ans.append(f'#{i} {name}')
    add(lab,q,im,' · '.join(ans),clue,f'{L} Thorax {L-11} slide {pn}',facts)
def vector(L,pn,R,want,lab,q,clue='',facts=()):
    im,lines=render(L,pn,R,True); d=ImageDraw.Draw(im); ans=[]
    for x,y,t in sorted(lines,key=lambda z:(z[1],z[0])):
        k=next((v for k2,v in want if re.search(k2,t,re.I)),None)
        if k and k not in [a.split(' ',1)[1] for a in ans]: ans.append(f'#{len(ans)+1} {k}'); badge(d,x,y,len(ans))
    add(lab,q,im,' · '.join(ans),clue,f'{L} Thorax {L-11} slide {pn}',facts)
def plain(L,pn,R,lab,q,ans,clue='',facts=()):
    im,_=render(L,pn,R); add(lab,q,im,ans,clue,f'{L} Thorax {L-11} slide {pn}',facts)
# ---------------- Lab 17 (pleura, lungs, thoracic vessels)
plain(12,46,(114,76,375,344),17,'Name the RED-highlighted double fold of pleura (left lung lifted).','Pulmonary ligament','Connecting pleura: joins the caudal lobe to the mediastinum, caudal to the hilus')
plain(12,46,(401,76,657,344),17,'Name the RED-highlighted fold (right side, head to the right).','Plica venae cavae','Connecting pleura: fold that holds the caudal vena cava; the accessory lobe sits in the pocket it makes')
manual(12,50,(339,80,693,313),[(30,42,'Cranial part of the left cranial lobe'),(47,55,'Caudal part of the left cranial lobe'),(72,42,'Left caudal lobe')],17,'Left lung, left lateral view (cranial left). Name the lobes / parts.','Left lung = 2 lobes: cranial lobe (cranial + caudal parts) and caudal lobe')
manual(12,53,(333,84,705,332),[(80,40,'Right cranial lobe'),(60,60,'Right middle lobe'),(14,48,'Right caudal lobe'),(57,74,'Cardiac notch (heart shows through)')],17,'Right lung, right lateral view (cranial right). Name 1–4.','Right lung = 4 lobes (cranial, middle, caudal, accessory — accessory not visible here). Cardiac notch: low in the right 4th–5th intercostal space (needle access to the heart without hitting lung)')
vector(12,56,(0,0,720,405),[(r'Bronchoesophageal','Bronchoesophageal artery')],17,'Name the vessel at the arrow (off the descending aorta).','Nutritional blood supply of the lungs: from the right 5th intercostal artery area / aorta')
# Miller's veins figure, OCR
doc=pymupdf.open(P[13]); R=pymupdf.Rect(322,6,715,399); pm=doc[27].get_pixmap(matrix=pymupdf.Matrix(4,4),clip=R); im=Image.frombytes('RGB',(pm.w,pm.h),pm.samples)
D=pytesseract.image_to_data(im,output_type=pytesseract.Output.DICT,config='--psm 11')
from collections import defaultdict
rows=defaultdict(list)
for i,w in enumerate(D['text']):
    if w.strip() and int(float(D['conf'][i]))>30: rows[(D['block_num'][i],D['par_num'][i],D['line_num'][i])].append((D['left'][i],D['top'][i],D['width'][i],D['height'][i],w))
WANT=[(r'cranial vena cava','Cranial vena cava'),(r'caudal vena cava','Caudal vena cava'),(r'right external jugular','Right external jugular vein'),(r'subclavian vein','Subclavian vein'),(r'right brachiocephalic vein','Right brachiocephalic vein'),(r'left brachiocephalic vein','Left brachiocephalic vein'),(r'internal thoracic vein','Internal thoracic vein'),(r'costocervical vein','Costocervical vein'),(r'thoracic duct','Thoracic duct'),(r'ligamentum arteriosum','Ligamentum arteriosum'),(r'pulmonary trunk','Pulmonary trunk'),(r'brachiocephalic trunk','Brachiocephalic trunk'),(r'left subclavian artery','Left subclavian artery'),(r'costocervical trunk','Costocervical trunk'),(r'aortic arch','Aortic arch'),(r'left tracheal','Left tracheal trunk'),(r'paraconal','Paraconal interventricular branch'),(r'right auricle','Right auricle'),(r'left auricle','Left auricle'),(r'vertebral artery','Vertebral artery'),(r'superficial cervical artery','Superficial cervical artery'),(r'internal thoracic artery','Internal thoracic artery')]
import numpy as np
from scipy import ndimage
a=np.asarray(im).astype(int); blue=(a[:,:,2]>150)&(a[:,:,0]<90)&(a[:,:,1]>80)&(a[:,:,1]<170)
lab_,nl=ndimage.label(ndimage.binary_dilation(blue,iterations=2))
boxes=[]
for sl in ndimage.find_objects(lab_):
    h_=sl[0].stop-sl[0].start; w_=sl[1].stop-sl[1].start
    if 40<h_<120 and w_>200: boxes.append((sl[1].start,sl[0].start,sl[1].stop,sl[0].stop))
d=ImageDraw.Draw(im); ans=[]; spots=[]
for x0,y0,x1,y1 in boxes:
    t=pytesseract.image_to_string(im.crop((x0+6,y0+6,x1-6,y1-6)),config='--psm 7').strip()
    d.rectangle([x0,y0,x1,y1],fill='white'); spots.append(((x0+x1)/2,(y0+y1)/2,t))
for k,ws in rows.items():
    t=' '.join(w[4] for w in ws); x0=min(w[0] for w in ws); y0=min(w[1] for w in ws); x1=max(w[0]+w[2] for w in ws); y1=max(w[1]+w[3] for w in ws)
    if not (x0>0.585*im.width or x1<0.36*im.width or (y0+y1)/2<0.075*im.height): continue   # inside the drawing: never paint over anatomy
    d.rectangle([x0-3,y0-3,x1+3,y1+3],fill='white'); spots.append(((x0+x1)/2,(y0+y1)/2,t))
for x,y,t in sorted(spots,key=lambda z:(z[1],z[0])):
    k=next((v for p2,v in WANT if re.search(p2,t,re.I)),None)
    if k and k not in [a.split(' ',1)[1] for a in ans]: ans.append(f'#{len(ans)+1} {k}'); badge(d,x,y,len(ans),r=30)
im=im.resize((im.width*3//4,im.height*3//4))
add(17,'Great vessels at the heart base, ventral view (Miller\'s figure). Name each number.',im,' · '.join(ans),'Boxed in the lecture = veins of the "venous angle" (where the external jugular + subclavian meet → brachiocephalic → cranial vena cava)','13 Thorax 2 slide 28')
# ---------------- Lab 18 (heart)
plain(13,7,(0,0,720,405),18,'Thorax opened, heart in situ (head left). What sac surrounds the heart here?','Pericardium (pericardial sac)','Pericardial sac = fibrous pericardium + parietal serous pericardium; attached to the diaphragm by the phrenicopericardial ligament')
plain(13,11,(330,59,710,392),18,'Heart, LEFT view. Name 1–4 (printed numbers).','#1 Left auricle · #2 Pulmonary trunk · #3 Right ventricle · #4 Left ventricle','Auricular surface = left side (auricles show). Base = dorsal (great vessels), apex = ventral/caudal tip')
plain(13,12,(324,62,708,365),18,'Heart, RIGHT view. Name 1–4 (printed numbers).','#1 Right atrium · #2 Caudal vena cava · #3 Aorta · #4 Right azygous vein','Atrial surface = right side')
plain(13,14,(339,0,720,406),18,'Heart, left view. Name the YELLOW line and the RED line.','Yellow = Coronary groove · Red = Paraconal interventricular groove','Coronary groove = atria vs ventricles. Paraconal groove = right vs left ventricle on the LEFT side')
plain(13,15,(323,0,719,406),18,'Heart, right view. Name the YELLOW line and the GREEN line.','Yellow = Coronary groove · Green = Subsinuosal interventricular groove','Subsinuosal groove = right vs left ventricle on the RIGHT side')
manual(13,19,(404,49,719,370),[(48,36,'Chordae tendineae')],18,'Right ventricle opened. Name the cords at #1.','Chordae tendineae run from the papillary muscles to the atrioventricular valve cusps (stop eversion: "parachute cords")')
plain(13,22,(329,11,712,404),18,'Transverse section through the ventricles. Name 2, 3, 4 (printed numbers).','#1 Most cranial point · #2 Right ventricle · #3 Interventricular septum · #4 Left ventricle','Left ventricle wall is much thicker than the right')
manual(13,23,(338,39,712,396),[(38,33,'Left coronary artery (orange)'),(13,55,'Circumflex branch (green)'),(61,92,'Subsinuosal interventricular branch (purple)'),(16,31,'Paraconal interventricular branch (red)'),(35,29,'Septal branch (light blue)'),(91,55,'Right coronary artery (pink)')],18,'Heart base, atria removed (P, A, LAV, RAV = valves). Name each colored vessel 1–6.','In the dog the LEFT coronary artery gives circumflex → subsinuosal interventricular branch, paraconal interventricular branch and septal branch. P = pulmonary valve, A = aortic, LAV / RAV = left / right atrioventricular valves')
plain(13,24,(458,0,720,406),18,'Heart, right view (Miller\'s). Name 1′, 3, 5 (printed numbers).',"#1′ Subsinuosal interventricular branch (continuation of the left coronary artery) · #3 Coronary sinus · #5 Middle cardiac vein",'Great cardiac vein (4) + middle cardiac vein (5) drain into the coronary sinus → right atrium')
plain(14,13,(408,52,714,406),18,'Conduction system. Name 1–6 (printed numbers).','#1 Sinoatrial node · #2 Atrioventricular node · #3 Atrioventricular bundle · #4 Left limb · #5 Right limb · #6 Branch of the right limb in the trabecula septomarginalis','Trabecula septomarginalis (moderator band) carries Purkinje fibers across the right ventricle')
vector(14,16,(184,75,503,386),[(r'^P$','Pulmonary valve'),(r'^A$','Aortic valve'),(r'^LAV$','Left atrioventricular valve (mitral)'),(r'^RAV$','Right atrioventricular valve (tricuspid)')],18,'Heart base, atria removed (cranial up, left on the left). Name 1–4.','Pulmonic + aortic valves = 3 cusps each')
vector(14,22,(110,0,620,405),[(r'foramen ovale','Foramen ovale'),(r'ductus arteriosus','Ductus arteriosus'),(r'umbilical vein','Umbilical vein'),(r'ductus venosus','Ductus venosus'),(r'umbilical$|^arteries$','Umbilical arteries')],18,'FETAL circulation. Name 1–5.','Foramen ovale: right → left atrium · ductus arteriosus: pulmonary trunk → aorta (both bypass the lungs)')
vector(14,24,(110,0,620,405),[(r'^ligamentum arteriosum','Ligamentum arteriosum'),(r'fossa ovalis','Fossa ovalis'),(r'round lig\. of liver','Round ligament of the liver'),(r'^ligamentum venosum','Ligamentum venosum'),(r'urinary bladder','Round ligament of the urinary bladder')],18,'ADULT remnants of the fetal shunts. Name 1–5.','Ductus arteriosus → ligamentum arteriosum · foramen ovale → fossa ovalis · umbilical vein → round ligament of the liver · ductus venosus → ligamentum venosum · umbilical arteries → round ligaments of the bladder')
css=re.search(r'<style>(.*?)</style>',open('gross-anatomy-lab22-best1.html').read(),re.S).group(1)
for n,cs in C.items():
    fn=f'gross-anatomy-lab{n}-lect1.html'; hubf=f'gross-anatomy-lab{n}-images.html'
    pg=page(f'Lab {n} · 📚 Thorax lecture pictures',f'Heart, lungs + vessels from Lectures 12–14 · {len(cs)} cards',''.join(cs).replace('class="card"','class="card on"',1),back=f'{hubf}?v={V}')
    open(fn,'w').write(re.sub(r'<style>.*?</style>',lambda _:f'<style>{css}</style>',pg,count=1,flags=re.S))
    h=open(hubf).read(); h=re.sub(r'<!--lect-->.*?<!--/lect-->','',h,flags=re.S)
    link=f'<!--lect--><a href="{fn}?v={V}">📚 Thorax lecture pictures (heart, lungs, vessels)<span>{len(cs)} cards</span></a><!--/lect-->'
    m=re.search(r'(<div class="sec main">.*?)(</div>)',h,re.S); h=h[:m.end(1)]+link+h[m.end(1):]; open(hubf,'w').write(h)
    print(n,len(cs))
