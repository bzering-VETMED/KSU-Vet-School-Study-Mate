"""Practical 4 · skull + teeth cards from course decks (made by Claude, Nov 8).
  • 'Canine and Feline Skull Interactive Quiz' (Dr. Sparks): one structure highlighted YELLOW on real dog + cat skulls → title = answer.
  • 'AL Skull' quiz (Dr. Sparks): 'Identify the X' slide → its 'Correct!' slide (2 later) shows X in yellow.
  • Dr. Diehl 'Digestive Components of the Head 2' teeth slides (surfaces photo, tooth diagram with labels → pink numbers).
Slide text is whited out (titles = answers); highlight fills + leader lines stay.  PDFs rendered by LibreOffice in /home/claude/new."""
import sys,re,html,subprocess
sys.path.insert(0,'tools')
import pymupdf as fz
from PIL import Image,ImageDraw,ImageFont
import p4lab26 as B
E=html.escape; W='/home/claude/new/'
KEEP=re.compile(r'^(canine skull|feline skull|©.*)$',re.I)
def _crop(p,out,keep_caps=True,icons=True):
    r=p.rect; ims=[fz.Rect(m['bbox'])&r for m in p.get_image_info()]
    big=[x for x in ims if 0.04*r.width*r.height<x.width*x.height<0.8*r.width*r.height]
    for b in p.get_text('blocks'):
        t=' '.join(b[4].split())
        if keep_caps and KEEP.match(t): continue
        p.add_redact_annot(fz.Rect(b[:4]),fill=None)
    for x in ims if icons else []:                  # small KSU seal / button images
        if x.width*x.height<0.02*r.width*r.height: p.add_redact_annot(x,fill=(0.53,0.76,0.91))
    p.apply_redactions(images=fz.PDF_REDACT_IMAGE_NONE,graphics=fz.PDF_REDACT_LINE_ART_NONE,text=fz.PDF_REDACT_TEXT_REMOVE)
    if icons: p.draw_rect(fz.Rect(r.width*0.845,0,r.width,r.height*0.23),color=None,fill=(0.53,0.76,0.91))   # home button (vector)
    u=big[0]
    for x in big[1:]: u|=x
    u=fz.Rect(u.x0-6,u.y0-6,u.x1+6,u.y1+18)&r
    pm=p.get_pixmap(clip=u,dpi=220); Image.frombytes('RGB',(pm.width,pm.height),pm.samples).save(out,quality=90); return out
def _blocks(p): return [(' '.join(b[4].split()),b) for b in p.get_text('blocks') if b[4].strip()]
ADD={'sphenoid':['basisphenoid','presphenoid'],'cheek teeth':['premolars','molars','superior shearing tooth'],'musculotubal':['musculotubal canal','foramen lacerum'],
     'palatine bone':['major palatine foramen','minor palatine foramen'],'hypoglossal':['hypoglossal canal']}
def skull_quiz(lab=28):
    d=fz.open(W+'skq.pdf'); out=[]
    for i in range(2,len(d)):
        p=d[i]; bl=_blocks(p); txt=' '.join(t for t,_ in bl)
        if 'Click on a region' in txt or 'Select a view' in txt or not p.get_image_info(): continue
        sp=[s for b in p.get_text('dict')['blocks'] for l in b.get('lines',[]) for s in l['spans'] if s['text'].strip()]
        tl=[s for s in sp if s['bbox'][0]<p.rect.width*0.33 and s['bbox'][1]<p.rect.height*0.25 and not KEEP.match(s['text'].strip())]
        if not tl: continue
        mx=max(s['size'] for s in tl); tl=[s for s in tl if s['size']>=mx-0.6]
        title=re.sub(r'\s+',' ',' '.join(s['text'] for s in sorted(tl,key=lambda s:(round(s['bbox'][1]),s['bbox'][0])))).strip()
        title=re.sub(r'\s*\(\s*(FL|MT)?\s*\)',' ',title); title=re.sub(r'\s+',' ',title).strip()
        if 'View' in title: continue
        tt={t for t,_ in bl if t in title or title in t}
        notes=[t for t,b in bl if t not in tt and not KEEP.match(t) and 'HERE' not in t and 'Triadan' not in t and len(t)>3]
        terms=B.terms_in(title,lab)
        for k,extra in ADD.items():
            if k in title.lower(): terms+= [x for x in extra if x not in terms]
        if any('pterygopalatine fossa' in n for n in notes) and 'pterygopalatine fossa' not in terms: terms.append('pterygopalatine fossa')
        fn=f'assets/p4skq_{i+1}.jpg'; _crop(p,fn)
        facts=[('📝 Slide note:',' '.join(notes))] if notes else []
        out.append(dict(name=title,terms=terms,html=B.card('Identify the structure highlighted in yellow (dog skull left, cat skull right).',f'📚 course slide · Dr. Sparks skull quiz #{i+1}',fn,f'<div class="nm">{E(title)}</div>',facts)))
    return out
def al_quiz(lab=28):
    d=fz.open(W+'alsk2.pdf'); out=[]; seen=set()
    for i in range(len(d)-2):
        t=' '.join(d[i].get_text().split()); m=re.match(r'Identify (?:the )?(.+?)\.?$',t)
        if not m or 'Correct!' not in d[i+2].get_text(): continue
        name=re.sub(r'\s+',' ',m.group(1)).strip(); name=name[0].upper()+name[1:]
        fn=f'assets/p4alsk_{i+1}.jpg'; _crop(d[i+2],fn,False)
        out.append(dict(name=name,terms=B.terms_in(name,lab),html=B.card('Identify the structure highlighted in yellow.',f'📚 course slide · Dr. Sparks skull quiz (AL) #{i+1}',fn,f'<div class="nm">{E(name)}</div>',[])))
    return out
KNOWN={"enamel","gingiva","dentin","pulp","cavity","root","canal","cementum","periodontal","ligaments","dental","alveolus","crown","neck"}
def _ocr_number(src,out,box):
    """white-out label words (tesseract) inside box=(x0,y0,x1,y1) fraction → pink numbers; returns [(n,text)] top→bottom, left→right."""
    im=Image.open(src).convert('RGB'); w,h=im.size
    tsv=subprocess.run(['tesseract',src,'-','--psm','11','tsv'],capture_output=True,text=True).stdout.splitlines()[1:]
    words=[]
    for l in tsv:
        f=l.split('\t')
        if len(f)<12 or not f[11].strip() or float(f[10])<50 or not re.match(r'^[A-Za-z]{3,}$',f[11].strip()): continue
        if KNOWN and f[11].strip().lower() not in KNOWN: continue
        x,y,ww,hh=map(int,f[6:10]); words.append((x,y,ww,hh,f[11]))
    words.sort(key=lambda a:(a[1],a[0])); lines=[]
    for wd in words:
        for L in lines:
            if abs(L['y']-wd[1])<max(wd[3],L['h'])*0.9 and (wd[0]-L['x1'])<w*0.04 and wd[0]>=L['x0']-5:
                L['t']+=' '+wd[4]; L['x1']=wd[0]+wd[2]; L['h']=max(L['h'],wd[3]); L['y1']=max(L['y1'],wd[1]+wd[3]); break
        else: lines.append(dict(x0=wd[0],y=wd[1],x1=wd[0]+wd[2],y1=wd[1]+wd[3],h=wd[3],t=wd[4]))
    dr=ImageDraw.Draw(im); F=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',max(14,int(h*0.03))); res=[]
    lines=sorted(lines,key=lambda L:(L['x0']>w/2,L['y']))
    m=[]
    for L in lines:                                  # 'Periodontal' + 'ligaments' on two rows = one label
        if m and m[-1]['t'].lower().endswith('periodontal') and L['t'].lower().startswith('ligament'):
            P=m[-1]; P['t']+=' '+L['t']; P['x0']=min(P['x0'],L['x0']); P['x1']=max(P['x1'],L['x1']); P['y1']=L['y1']
        else: m.append(L)
    lines=m
    for k,L in enumerate(lines,1):
        dr.rectangle([L['x0']-3,L['y']-3,L['x1']+3,L['y1']+3],fill='white')
        cx=L['x0']+8 if L['x0']<w/2 else L['x1']-8; cy=(L['y']+L['y1'])//2; r=int(h*0.022)
        dr.ellipse([cx-r,cy-r,cx+r,cy+r],fill='#D94F7F'); dr.text((cx,cy),str(k),fill='white',font=F,anchor='mm'); res.append((k,L['t']))
    im.save(out,quality=92); return res
def teeth(lab=28):
    d=fz.open(W+'diehl.pdf'); out=[]
    # surfaces photo (slide 21): legend colors
    p=d[20]; fn='assets/p4teeth_surf.jpg'; _crop(p,fn,False,False)
    rows=[('Red','Occlusal surface (biting surface)'),('Purple','Mesial contact surface (toward the first incisor)'),('Blue','Distal surface (away from the first incisor)'),
          ('Green','Lingual surface (faces the tongue)'),('Yellow','Labial surface = vestibular surface facing the lips'),('Pink','Buccal surface = vestibular surface facing the cheeks')]
    out.append(dict(name='Tooth surfaces',terms=['occlusal or masticating surface','contact surfaces','mesial contact surface','distal surface','lingual surface','vestibular surface'],
        html=B.card('Name the tooth surface for each color.','📚 lecture slide · Dr. Diehl Digestive Head 2, slide 21',fn,''.join(f'<div class="fx"><b>{a}:</b> {E(b)}</div>' for a,b in rows),[])))
    # tooth diagram (slide 11): crop the picture, number the printed labels
    p=d[10]; R=p.rect; big=fz.Rect(R.width*0.5,R.height*0.02,R.width*0.995,R.height*0.78)   # cropped picture overhangs the slide; diagram = right half
    raw='/home/claude/new/tooth_raw.png'; p.get_pixmap(clip=big,dpi=300).save(raw)
    fn='assets/p4teeth_tooth.jpg'; labs=_ocr_number(raw,fn,None)
    out.append(dict(name='Parts of a tooth',terms=['crown','root','neck of tooth'],
        html=B.card('Name every number.','📚 lecture slide · Dr. Diehl Digestive Head 2, slide 11',fn,''.join(f'<div class="fx"><b>#{k}</b> {E(t)}</div>' for k,t in labs),[])))
    return out

# ---- Nov 8: Dr. Malreddy eye lecture slides for terms nothing else shows ----
def _redact(p,pat,keep=None):
    for t,b in _blocks(p):
        if re.search(pat,t,re.I) and not (keep and re.search(keep,t,re.I)): p.add_redact_annot(fz.Rect(b[:4]),fill=(1,1,1))
    p.apply_redactions(images=fz.PDF_REDACT_IMAGE_NONE,graphics=fz.PDF_REDACT_LINE_ART_NONE)
def _shot(p,clip,out,dpi=220):
    pm=p.get_pixmap(clip=clip,dpi=dpi); Image.frombytes('RGB',(pm.width,pm.height),pm.samples).save(out,quality=90); return out
def eye(lab):
    d=fz.open(W+'eye.pdf'); out=[]; R=d[0].rect
    if lab==28:
        p=d[10]; _redact(p,r'LO2|Osseous|Image from|Margin')
        fn=_shot(p,fz.Rect(R.width*0.13,0,R.width*0.98,R.height*0.48),'assets/p4eye_orbit.jpg')
        out.append(dict(name='Orbital margin',terms=['orbital margin','orbital ligament'],html=B.card('Name the colored rim of the orbit (be specific).','📚 lecture slide · Dr. Malreddy eye lecture, slide 11',fn,
          '<div class="nm">Orbital margin</div>',[('Formed by:','frontal (yellow) + lacrimal (blue) + zygomatic (green) bones'),('Dorsolateral gap:','closed by the orbital ligament (orange)')])))
    if lab==31:
        p=d[28]; _redact(p,r'Pupil|Iris|Choroid|Tapetum|Optic|Fundus|retina|View|LO4|lucidum')
        fn=_shot(p,fz.Rect(R.width*0.1,R.height*0.08,R.width*0.9,R.height*0.82),'assets/p4eye_fundus.jpg')
        out.append(dict(name='Fundus',terms=['fundus','pupil','iris','choroid','tapetum lucidum','optic disk'],html=B.card('Name #1–#5. What is the right-hand view called?','📚 lecture slide · Dr. Malreddy eye lecture, slide 29',fn,
          '<div class="nm">Right view = FUNDUS of the eye (retina removed)</div><div class="fx"><b>#1</b> Pupil</div><div class="fx"><b>#2</b> Iris</div><div class="fx"><b>#3</b> Choroid</div><div class="fx"><b>#4</b> Tapetum lucidum</div><div class="fx"><b>#5</b> Optic disk</div>',[])))
        p=d[37]; mid=fz.Rect(R.width*0.63,R.height*0.44,R.width*0.98,R.height*0.76)   # middle diagram: dilator vs constrictor pupillae
        raw=_shot(p,mid,'/home/claude/new/dil_raw.png',300)
        im=Image.open(raw).convert('RGB'); w,h=im.size; dr=ImageDraw.Draw(im); F=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',max(16,int(h*0.06)))
        tsv=subprocess.run(['tesseract',raw,'-','--psm','11','tsv'],capture_output=True,text=True).stdout.splitlines()[1:]
        groups={'1':[],'2':[]}
        for l in tsv:
            f=l.split('\t')
            if len(f)<12 or not f[11].strip(): continue
            x,y,ww,hh=map(int,f[6:10]); t=f[11].strip().lower()
            if re.search(r'dilat|pupil|muscl|sympath|constrict|parasym|\(',t):
                dr.rectangle([x-3,y-3,x+ww+3,y+hh+3],fill='white'); groups['1' if x<w/2 else '2'].append((x,y,ww,hh))
        for k,g in groups.items():
            if not g: continue
            cx=min(a[0] for a in g)+20; cy=min(a[1] for a in g)+15; r=int(h*0.045)
            dr.ellipse([cx-r,cy-r,cx+r,cy+r],fill='#D94F7F'); dr.text((cx,cy),k,fill='white',font=F,anchor='mm')
        fn='assets/p4eye_pupil.jpg'; im.save(fn,quality=92)
        out.append(dict(name='Pupillary muscles',terms=['dilator pupillae'],html=B.card('Name muscle #1 (radial) and #2 (circular).','📚 lecture slide · Dr. Malreddy eye lecture, slide 38',fn,
          '<div class="nm">#1 · Dilator pupillae (radial) · sympathetic → dilates (mydriasis)</div><div class="nm">#2 · Constrictor (sphincter) pupillae (circular) · oculomotor nerve, parasympathetic → constricts (miosis)</div>',[])))
    return out

# ---- Nov 8: Bethany's pre-lab VIDEO screenshots (Lab 28 skull interior). Label box + subtitle cropped off; probe = pointer ----
VID=[('3d739024','foramen for the dorsal sagittal sinus','Foramen for the dorsal sagittal sinus',[('Where:','midline at the top of the occipital region, on the inside of the dorsal sagittal crest'),('Leads to:','the transverse canals in the transverse groove')]),
     ('5a93c20f','tentorium cerebelli','Tentorium cerebelli',[('What it is:','the DURA MATER fold that attaches to the tentorium osseum'),('Job:','separates the cerebrum from the cerebellum')]),
     ('50a627d0','tentorium osseum','Tentorium osseum',[('What it is:','the BONY part (shelf) the tentorium cerebelli attaches to'),('Trap:','osseum = bone · cerebelli = dura')]),
     ('a88b0d2b','transverse groove','Transverse groove',[('Holds:','the transverse sinus; the transverse canals open in it')]),
     ('c80bc095','transverse canals','Transverse canals',[('Where:','in the transverse groove; continue from the foramen for the dorsal sagittal sinus')]),
     ('6b811dad','rostral cranial fossa','Rostral cranial fossa',[('Extent:','from the cribriform plate back to the optic canal'),('Holds:','olfactory bulbs + frontal lobes')]),
     ('666589af','middle cranial fossa','Middle cranial fossa',[('Extent:','from the orbital fissure/optic canal back to the dorsum sellae'),('Holds:','pituitary (in the sella turcica), temporal lobes')]),
     ('f877a1d5','caudal cranial fossa','Caudal cranial fossa',[('Extent:','from the dorsum sellae back to the foramen magnum'),('Holds:','cerebellum, pons, medulla')]),
     ('9e516b5c','sella turcica','Sella turcica',[('What it is:','hypophyseal fossa + dorsum sellae together ("Turkish saddle")')]),
     ('c1dc3d4c','hypophyseal fossa','Hypophyseal fossa',[('Holds:','the pituitary gland (hypophysis)')]),
     ('b58597aa','dorsum sellae','Dorsum sellae',[('What it is:','the ELEVATED back of the sella turcica; border between middle + caudal cranial fossae')]),
     ('9fc63fdf','canal for the trigeminal nerve','Canal for the trigeminal nerve',[('Carries:','trigeminal nerve (CN V)')]),
     ('be6d89a0','internal acoustic meatus','Internal acoustic meatus',[('Carries:','facial (VII) + vestibulocochlear (VIII) nerves')]),
     ('dd7dcb79','cerebellar fossa','Cerebellar fossa',[('Holds:','the cerebellum (caudal cranial fossa)')]),
     ('e3210512','jugular foramen','Jugular foramen',[('Carries:','glossopharyngeal (IX), vagus (X), accessory (XI) nerves')]),
     ('3d98e1b2','hypoglossal canal','Hypoglossal canal',[('Carries:','hypoglossal nerve (XII)')]),
     ('90080e27','condyloid canal','Condyloid canal',[('Carries:','a vein (venous connection), near the occipital condyle')]),
     ('90c064f5','optic canal','Optic canal',[('Carries:','optic nerve (II)')]),
]
BOX={'3d739024':(0.30,0.12,0.75,0.70),'a88b0d2b':(0.30,0.10,0.75,0.70),'c80bc095':(0.35,0.08,0.80,0.70),
     '5a93c20f':(0.45,0.25,0.90,0.70),'90080e27':(0.50,0.22,0.92,0.92),'50a627d0':(0.45,0.25,0.90,0.70)}
def video(lab=28):
    out=[]
    for fid,term,name,facts in VID:
        im=Image.open(f'tools/vid_src_p4/{fid}-image.jpg').convert('RGB'); w,h=im.size
        x0,y0,x1,y1=BOX.get(fid,(0.30,0.04,0.90,0.775))      # Nov 8: zoom on the skull + probe tip
        fn=f'assets/p4vid_{fid}.jpg'; im.crop((int(w*x0),int(h*y0),int(w*x1),int(h*y1))).save(fn,quality=92)
        out.append(dict(name=name,terms=[term],html=B.card('Identify the structure at the probe tip.','🎥 pre-lab video · skull interior',fn,f'<div class="nm">{E(name)}</div>',facts)))
    return out

# ---- Nov 9: 'Lecture 30 Eye - Tagged' PDF (same lecture) → extra real-photo cards for Lab 31 ----
TAG='/mnt/user-data/attachments/31594bc3-9d6f-5c02-a55e-32953ff4d455/3a3afce7-Lecture_30_Eye_-_Tagged.pdf'
def eye_tagged():
    import os
    if not os.path.exists(TAG): return []
    d=fz.open(TAG); R=d[0].rect; out=[]
    p=d[12]; ims=[fz.Rect(m['bbox'])&R for m in p.get_image_info()]; big=max(ims,key=lambda x:x.width*x.height)
    fn=_shot(p,big,'assets/p4tag_periorbita.jpg')
    out.append(dict(name='Periorbita',terms=['periorbita'],html=B.card('Identify the structure at the star.','📚 lecture slide · Eye lecture (tagged), slide 13',fn,
        '<div class="nm">Periorbita</div>',[('What it is:','cone-shaped sheath of connective tissue + smooth muscle enclosing the orbital contents')])))
    p=d[31]; ims=[fz.Rect(m['bbox'])&R for m in p.get_image_info()]; big=max(ims,key=lambda x:x.width*x.height)
    fn=_shot(p,big,'assets/p4tag_retina.jpg')
    out.append(dict(name='Retina',terms=['retina','pars optica retinae'],html=B.card('Name the gray sheet peeling off inside this opened eye.','📚 lecture slide · Eye lecture (tagged), slide 32',fn,
        '<div class="nm">Retina (pars optica retinae)</div>',[('Why it peels:','in embalmed eyes the nervous layer separates from the pigmented epithelium, which stays on the choroid')])))
    return out
