"""Practical 4 · 🌐 UMN Carnivore Dissection screenshots → ⭐ Bold-terms cards (made by Claude).
UMN numbered pointers stay (numbers never give the answer); caption + browser bar are cropped off.
The question asks only for the numbers that are YOUR bold terms; the reveal also lists the other labeled numbers.
A photo goes to every Practical 4 lab whose bold terms it shows.  Originals: tools/umn_src_p4/IMG_NNNN.jpg
  merge(lab, school_star, extra) → (best, extra): UMN first, school slides only for terms UMN doesn't cover.
Add new screenshots by appending to SPEC: (img id, UMN lab/image note, caption-top y, {number: full name}, view-level terms)."""
import os,re,html,sys
from PIL import Image
import numpy as np
sys.path.insert(0,'tools')
import p4lab26 as B
from p4bold import P4BOLD
E=html.escape; SRC='tools/umn_src_p4'
SPEC=[
 ('4906','UMN Lab 20 · corrosion cast, dorsal pelvis',1322,{'1':'Caudal gluteal artery','2':'Internal pudendal artery','3':'Cranial gluteal artery','4':'Iliolumbar artery','5':'Sacrum','6':'Ischiatic tuberosity','*':'Greater trochanter of the femur'},[]),
 ('4908','UMN Lab 20 · gluteal + perineal region',1339,{'1':'Caudal gluteal artery','2':'Sciatic nerve','3':'Lateral caudal artery','4':'Dorsal perineal artery','5':'Caudal cutaneous femoral nerve','6':'Perineal nerves (branches of the pudendal nerve)','7':'Pudendal nerve','8':'Deep gluteal muscle','9':'Middle gluteal muscle','10':'Superficial gluteal muscle','*':'Sacrotuberous ligament','11':'Anus','12':'Vulva'},[]),
 ('4909','UMN Lab 20 · lateral rump',1057,{'1':'Caudal gluteal artery','2':'Lateral caudal artery','3':'Perineal nerves (branches of the pudendal nerve)','4':'Caudal cutaneous femoral nerve','5':'Cranial gluteal nerve','6':'Tensor fasciae latae muscle','7':'Middle gluteal muscle','8':'Deep gluteal muscle','9':'Vulva'},[]),
 ('4910','UMN Lab 21 · gluteal dissection (cat)',1359,{'1':'Lumbosacral trunk','2':'Cranial gluteal nerve','3':'Caudal gluteal nerve','4':'Sciatic nerve','5':'Caudal gluteal artery','6':'Cranial gluteal artery','7':'Iliolumbar artery','8':'Superficial gluteal muscle','9':'Middle gluteal muscle','10':'Deep gluteal muscle','11':'Tensor fasciae latae muscle','12':'Quadriceps femoris muscle','13':'Caudofemoralis muscle','14':'Biceps femoris muscle','15':'Tail'},[]),
 ('4911','UMN Lab 20 · femoral triangle',875,{'1':'Femoral artery and vein','2':'Sartorius muscle','3':'Pectineus muscle','4':'Vascular lacuna','5':'Proximal caudal femoral artery (vessels)','6':'Adductor muscle','7':'Gracilis muscle','8':'External pudendal vessels','9':'Inguinal canal'},['femoral triangle']),
 ('4912','UMN Lab 20 · external iliac → femoral branches',1014,{'1':'Vascular lacuna','2':'External iliac artery (vessels)','3':'Deep femoral artery (vessels)','4':'Pudendoepigastric trunk','5':'Medial circumflex femoral artery (vessels)','6':'Adductor muscle','7':'Transverse branch of the medial circumflex femoral artery','8':'Deep branch of the medial circumflex femoral artery','9':'Femoral artery','10':'Superficial circumflex iliac artery','11':'Lateral circumflex femoral artery','12':'Proximal caudal femoral artery','13':'Saphenous artery','*':'Saphenous nerve'},[]),
 ('4913','UMN Lab 20 · branches of the femoral artery',985,{'1':'Femoral artery','2':'Common trunk of the superficial circumflex iliac + lateral circumflex femoral arteries','3':'Proximal caudal femoral artery','4':'Middle caudal femoral artery','5':'Distal caudal femoral artery','6':'Saphenous artery','7':'Saphenous nerve','8':'Descending genicular artery','9':'Tibial nerve','10':'Medial circumflex femoral artery','11':'Gracilis muscle','12':'Pectineus muscle'},[]),
 ('4914','UMN Lab 20 · caudal view, gastrocnemius reflected',1032,{'1':'Medial head of the gastrocnemius muscle (cut + reflected)','2':'Femoral artery','3':'Proximal caudal femoral artery','4':'Middle caudal femoral artery','5':'Distal caudal femoral artery','6':'Popliteal artery','7':'Saphenous artery','8':'Saphenous nerve','9':'Cranial branch of the saphenous artery','10':'Caudal branch of the saphenous artery'},[]),
 ('4915','UMN Lab 21 · corrosion casts, crus + pes',1366,{'1':'Cranial tibial artery','2':'Dorsal pedal artery','3':'Arcuate artery','4':'Dorsal metatarsal artery II','5':'Perforating branch of dorsal metatarsal artery II','6':'Saphenous artery'},[]),
 ('4916','UMN Lab 21 · cranial crus + pes',1471,{'1':'Cranial tibial artery','2':'Cranial tibial muscle','3':'Fibularis longus muscle','4':'Superficial fibular nerve (superficial branch of the common fibular nerve)','5':'Deep fibular nerve (deep branch of the common fibular nerve)','6':'Common fibular nerve','7':'Cranial + caudal branches of the medial saphenous vein','8':'Long digital extensor muscle','9':'Dorsal pedal artery','10':'Arcuate artery','11':'Perforating branch of dorsal metatarsal artery II'},[]),
 ('4928','UMN Lab 21 · arterial cast, crus + pes',1633,{'1':'Popliteal artery','2':'Cranial tibial artery','3':'Caudal tibial artery','4':'Dorsal pedal artery','5':'Arcuate artery','6':'Perforating branch of dorsal metatarsal artery II','7':'Saphenous artery','8':'Tibia','9':'Fibula','10':'Calcaneus','*':'Metatarsal bones'},[]),
 ('4919','UMN Lab 20 · medial limb (cat)',959,{'1':'Medial saphenous vein','2':'Saphenous artery and saphenous nerve','3':'Proximal caudal femoral artery','4':'Medial circumflex femoral artery','5':'Lateral circumflex femoral artery','6':'External iliac artery','7':'Internal iliac artery','8':'Umbilical artery','9':'Deep circumflex iliac artery','10':'Caudal mesenteric artery','11':'Testicular artery','12':'Femoral nerve'},[]),
 ('4920','UMN Lab 20 · medial saphenous vein (cat)',871,{'1':'Medial saphenous vein','2':'Cranial branch of the medial saphenous vein','3':'Caudal branch of the medial saphenous vein'},[]),
 ('4921','UMN Lab 20 · lateral saphenous vein (dog)',746,{'1':'Lateral saphenous vein','2':'Caudal branch of the lateral saphenous vein','3':'Cranial branch of the lateral saphenous vein'},[]),
 ('4922','UMN Lab 21 · lumbosacral plexus (cat)',1372,{'1':'S1 ventral branch','2':'S2 ventral branch','3':'S3 ventral branch','6':'L6 ventral branch','7':'L7 ventral branch','10':'Femoral nerve','11':'Obturator nerve','12':'Lumbosacral trunk','13':'Pudendal nerve','14':'Pelvic nerve','→':'Saphenous nerve (unnumbered arrow)','*':'Internal obturator muscle'},['lumbosacral plexus']),
 ('4923','UMN Lab 21 · lumbosacral plexus (dog)',705,{'1':'L4 ventral branch','2':'S1 ventral branch','3':'S3 ventral branch','4':'Lateral cutaneous femoral nerve','5':'Femoral nerve','6':'Saphenous nerve','7':'Obturator nerve','8':'Lumbosacral trunk (entering the greater ischiatic notch)','9':'Pelvic nerve','10':'Femoral vessels','11':'Caudal gluteal artery'},['lumbosacral plexus']),
 ('4924','UMN Lab 21 · medial thigh nerves',986,{'1':'Saphenous nerve','2':'Femoral artery','3':'Saphenous artery','4':'Femoral nerve','5':'Obturator nerve','6':'Tibial nerve','7':'Gracilis muscle','8':'Adductor muscle','9':'Pectineus muscle','10':'Sartorius muscle'},[]),
 ('4925','UMN Lab 21 · lateral rump, gluteals reflected',1168,{'1':'Superficial gluteal muscle','2':'Middle gluteal muscle','3':'Deep gluteal muscle','4':'Sciatic nerve','5':'Caudal gluteal artery','6':'Branches of the sciatic nerve to the hamstrings','7':'Biceps femoris muscle','8':'Cranial gluteal nerve (branches)','9':'Tensor fasciae latae muscle','10':'Sacrotuberous ligament','11':'External anal sphincter muscle'},[]),
 ('4926','UMN Lab 21 · sciatic division (cat)',1091,{'1':'Biceps femoris muscle (reflected)','2':'Sciatic nerve','3':'Branches of the sciatic nerve to the hamstrings','4':'Common fibular nerve','5':'Tibial nerve','6':'Soleus + lateral head of the gastrocnemius (reflected)','7':'Tibial nerve branches to the caudal crus muscles','8':'Quadriceps femoris muscle','9':'Adductor muscle','10':'Semimembranosus muscle','11':'Semitendinosus muscle','12':'Popliteal artery'},[]),
 ('4927','UMN Lab 21 · caudal thigh (dog)',798,{'1':'Biceps femoris muscle (reflected)','2':'Semitendinosus muscle (reflected)','3':'Sciatic nerve','4':'Caudal gluteal artery','5':'Greater trochanter','6':'Branches of the sciatic nerve to the hamstrings','7':'Common fibular nerve','8':'Tibial nerve','9':'Caudal cutaneous sural nerve','10':'Tensor fasciae latae muscle','11':'Quadriceps femoris muscle','12':'Semimembranosus muscle','13':'Lateral head of the gastrocnemius muscle'},[]),
]
TOP={'4928':110}   # Safari status bar overlaid on the photo
NOT_BOLD={'Femoral artery and vein':'femoral artery'}   # label → bold term it still counts for

def crop(img_id,captop):
    out=f'assets/p4umn_{img_id}.jpg'
    im=Image.open(f'{SRC}/IMG_{img_id}.jpg').convert('RGB'); a=np.asarray(im)[:max(10,captop-8)].astype(int)
    nonwhite=(a.min(axis=2)<235)
    rows=np.where(nonwhite.mean(axis=1)>0.35)[0]; rows=rows[rows>=TOP.get(img_id,0)]; cols=np.where(nonwhite[rows.min():rows.max()+1].mean(axis=0)>0.35)[0]
    box=(int(cols.min()),int(rows.min()),int(cols.max())+1,int(rows.max())+1)
    im.crop(box).save(out,quality=92); return out

def strict_terms(name,lab):
    """exact match only (parentheticals dropped; 'X and Y' split) so 'branches of the sciatic nerve' ≠ sciatic nerve"""
    base=re.sub(r'\s*\(.*?\)','',name).strip()
    parts=[base]+([p for p in re.split(r'\s+and\s+',base)] if ' and ' in base else [])
    out=[]
    for t,al,_ in P4BOLD[lab]:
        if any(B.norm(p)==B.norm(a) for p in parts for a in al): out.append(t)
    return out

def cards_for(lab):
    out=[]
    for img_id,src,captop,labels,view in SPEC:
        bold=[];other=[]
        for n,name in labels.items():
            ts=strict_terms(name,lab) or ([NOT_BOLD[name]] if name in NOT_BOLD and NOT_BOLD[name] in [t for t,_,_ in P4BOLD[lab]] else [])
            (bold if ts else other).append((n,name,ts))
        vterms=[t for t in view if t in [x for x,_,_ in P4BOLD[lab]]]
        if not bold and not vterms: continue
        img=crop(img_id,captop)
        nums=', '.join('#'+n if n[0].isdigit() else n for n,_,_ in bold)
        q=(f'Which region/plexus is this? Then name {nums}' if vterms and bold else f'Name {nums}' if bold else 'Which region/plexus is this?')
        nm=''.join(f'<div class="nm">{E(v[0].upper()+v[1:])}</div>' for v in vterms)
        nm+=''.join(f'<div class="nm">{"#"+n if n[0].isdigit() else n} · {E(name)}</div>' for n,name,_ in bold)
        facts=[('Also labeled (not your bold terms):',' · '.join(f'{"#"+n if n[0].isdigit() else n} {name}' for n,name,_ in other))] if other else []
        terms=vterms+[t for _,_,ts in bold for t in ts]
        out.append(dict(name=' | '.join(name for _,name,_ in bold) or vterms[0],terms=list(dict.fromkeys(terms)),umn=True,
            html=B.card(q,f'🌐 UMN · {src}',img,nm,facts)))
    return out

def merge(lab,school,extra):
    """UMN first; a school card stays in ⭐ only if it shows a bold term no UMN photo covers; the rest → 📚 extra."""
    umn=cards_for(lab); covered={t for c in umn for t in c['terms']}
    best=list(umn); moved=[]
    for c in school:
        (best if (not c['terms'] or set(c['terms'])-covered) else moved).append(c)
    return best,moved+extra,len(umn)

def per_term(lab,school,extra):
    """Bethany (Nov 3): EVERY bold term gets its OWN ⭐ card, in list order.
    Pick: UMN photo where the term is a numbered label ('Name #7') → else a school slide that shows ONLY/mainly that term
    → else a concept card. All multi-number UMN cards + every other photo go to 📚 Extra."""
    order=[t for t,_,_ in P4BOLD[lab]]; best=[]; used_school=set(); nu=0
    def umn_hit(term):
        for img_id,src,captop,labels,view in SPEC:
            if term in view: return img_id,src,captop,None,labels
            for n,name in labels.items():
                ts=strict_terms(name,lab) or ([NOT_BOLD[name]] if name in NOT_BOLD else [])
                if term in ts: return img_id,src,captop,(n,name),labels
        return None
    for term in order:
        h=umn_hit(term); TERM=term[0].upper()+term[1:]
        if h:
            img_id,src,captop,lab_,labels=h; img=crop(img_id,captop); nu+=1
            if lab_:
                n,name=lab_; tag='#'+n if n[0].isdigit() else ('the ' +('asterisk' if n=='*' else 'unnumbered arrow'))
                q=f'Name {tag}'
                nm=f'<div class="nm">{E(TERM)}</div>'+('' if B.norm(name)==B.norm(term) else f'<div class="fx" style="text-align:center">label: {E(name)}</div>')
            else:
                q='Name the whole structure shown in this view.'; nm=f'<div class="nm">{E(TERM)}</div>'
            best.append(dict(name=term,terms=[term],html=B.card(q,f'🌐 UMN · {src}',img,nm,[])))
            continue
        pick=None
        for i,c in enumerate(school):
            if term in c['terms'] and i not in used_school and len(c['terms'])==1: pick=i; break
        if pick is None:
            for i,c in enumerate(school):
                if term in c['terms']: pick=i; break
        if pick is not None:
            used_school.add(pick); c=dict(school[pick]); c['terms']=[term]; best.append(c)
        else:
            best.append(dict(name=term,terms=[term],html=f'<section class="card"><div class="q">🧠 {E(TERM)}<span class="tagline">❗ no photo yet</span></div><div class="stg ans"><div class="pr">❓ Where is it?</div><div class="an"><div class="nm">{E(TERM)}</div></div></div><div class="rev">💗 TAP TO REVEAL</div></section>'))
    rest=cards_for(lab)+[c for i,c in enumerate(school) if i not in used_school and '🧠' not in c['html'][:300]]+extra
    return best,rest,nu
