"""Practical 4 · Labs 30–32 hubs from Dr. Stueve's lab .pptx decks (rendered to PDF by LibreOffice).  Made by Claude.
Each title = plain slide + highlighted copy (green/teal/purple fill or black arrow). Keep the highlighted copy (else the
single slide); crop to the photo(s) at native dpi; title = answer (bold-list wording); 'Note:' text in the reveal.
Slides whose photo has labels BAKED IN (Dr. Sparks / NCSU images) → 📚 Extra as labeled reference.
Title groups with no photo → 🧠 concept card (slide note).  Wilhite 'Canine head + eye' deck → p4wil (⭐ only for gaps).
  python3 tools/p4pptlab.py 30 /path/l30.pdf 'Lab 30 · Larynx, ear, tongue + hyoid muscles'"""
import sys,os,re,html
sys.path.insert(0,'tools')
import pymupdf as fz
from PIL import Image
import p4lab26 as B
from p4bold import P4BOLD
E=html.escape
BAKED={31:{18,20,97,102,103,104,105}}          # labels printed inside the photo
SKIP={'antihelix','removing the zygomatic arch','dissection','extrinsic muscles of the eye'}
FIX={'rima glottis':'rima glottidis','cricoartenoideus dorsalis':'cricoarytenoideus dorsalis','cricoartenoideus lateralis':'cricoarytenoideus lateralis',
     'thyroartenoideus':'thyroarytenoideus','auricolotemporal nerve':'auriculotemporal nerve','pharyngoesophage al limen':'pharyngoesophageal limen'}
def is_hl(p):
    return any(x.get('fill') and tuple(round(c,2) for c in x['fill'])!=(1.0,1.0,1.0) and x['fill']!=(1.0,1.0,0.0) for x in p.get_drawings())
def info(p):
    t=p.get_text(); title=re.sub(r'\s+',' ',t.split('Note:')[0]).strip()
    title=re.split(r'\s(?=The |This |You )',title)[0]           # 'Vestibular fold The vestibular fold extends…'
    note=re.sub(r'\s+',' ',t.split('Note:',1)[1]).strip() if 'Note:' in t else ''
    note=re.sub(r'Image (is )?property of .*?(Medicine|Sparks)\.?','',note).strip()
    return title,note
def crop(p,fn):
    ims=[fz.Rect(m['bbox'])&p.rect for m in p.get_image_info()]
    ims=[r for r in ims if r.width*r.height>3000]
    r=ims[0]
    for x in ims[1:]: r|=x
    if len(ims)>1:                                   # union box can take in slide text → white it out (photos untouched)
        for b in p.get_text('blocks'):
            br=fz.Rect(b[:4])
            if br.intersects(r) and not any(br in x for x in ims): p.add_redact_annot(br,fill=(1,1,1))
        p.apply_redactions(images=fz.PDF_REDACT_IMAGE_NONE,graphics=fz.PDF_REDACT_LINE_ART_NONE)
    dpi=int(min(300,max(150,max(m['width']/max(1,fz.Rect(m['bbox']).width)*72 for m in p.get_image_info()))))
    pm=p.get_pixmap(clip=r,dpi=dpi); Image.frombytes('RGB',(pm.width,pm.height),pm.samples).save(fn,quality=90)
def build(lab,pdf):
    d=fz.open(pdf); grp=[]
    for i,p in enumerate(d):
        if i==0: continue
        title,note=info(p); key=B.norm(title)
        if grp and grp[-1]['key']==key: grp[-1]['pages'].append(i)
        else: grp.append(dict(key=key,title=title,pages=[i],note=note))
        if note and len(note)>len(grp[-1]['note']): grp[-1]['note']=note
    best=[];extra=[];concept=[]
    for g in grp:
        title=FIX.get(g['title'].lower(),g['title']);
        if B.norm(title) in SKIP: continue
        terms=B.terms_in(title,lab)
        name=terms[0] if len(terms)==1 else title
        NAME=name[0].upper()+name[1:]
        pg=[i for i in g['pages'] if d[i].get_image_info()]
        if not pg:
            if terms: concept.append(dict(name=NAME,terms=terms,html=(f'<section class="card"><div class="q">🧠 {E(NAME)}<span class="tagline">❗ no photo on the slides · concept</span></div>'
                f'<div class="stg ans"><div class="pr">❓ What is it / where is it?</div><div class="an"><div class="nm">{E(NAME)}</div><div class="fx">{E(g["note"])}</div></div></div><div class="rev">💗 TAP TO REVEAL</div></section>')))
            continue
        hl=[i for i in pg if is_hl(d[i])]; i=(hl or pg)[-1]
        fn=f'assets/p4_l{lab}s_{i+1}.jpg'; crop(d[i],fn)
        baked=(i+1) in BAKED.get(lab,set())
        q=('📖 Labeled slide — cover the labels, name them' if baked else
           'Identify the highlighted structure.' if hl else 'Identify the structure at the arrow / probe.')
        c=dict(name=NAME,terms=terms,html=B.card(q,f'📚 course slide · Lab {lab} slides #{i+1}',fn,f'<div class="nm">{E(NAME)}</div>',[('📝 Slide note (professor):',g['note'])]))
        (extra if baked or not terms else best).append(c)
    return best,extra,concept

GROUP={'rectus muscles':['dorsal rectus','medial rectus','ventral rectus','lateral rectus'],'obliquus muscles':['dorsal oblique','ventral oblique'],
       'uvea':['middle vascular coat'],'internal coat':['retina'],'buccal branches':['dorsal buccal branch','ventral buccal branch']}
def group_terms(lab,cs):
    for c in cs:
        for g,mem in GROUP.items():
            if any(t in g for t in []) : pass
            if g in [t for t,_,_ in P4BOLD[lab]] and set(mem)&set(c['terms']) and g not in c['terms']: c['terms'].append(g)
if __name__=='__main__':
    lab=int(sys.argv[1]); pdf=sys.argv[2]; title=sys.argv[3]
    best,extra,concept=build(lab,pdf)
    group_terms(lab,best+extra)
    import p4wil
    wb,wx=p4wil.cards(lab)
    have={t for c in best for t in c['terms']}
    for c in sorted(wb,key=lambda c:-len(set(c['terms'])-have)):
        new=set(c['terms'])-have
        (best if new else extra).append(c); have|=new
    extra+=wx; group_terms(lab,best+extra)
    # labeled-reference slides fill a gap only if nothing else shows the term
    for c in list(extra):
        if '📖 Labeled slide' in c['html'][:200] and set(c['terms'])-have: pass
    concept=[c for c in concept if set(c['terms'])-have]
    got=B.two_area_hub(lab,title,'Two decks. One tap = full answer. 🐾',best+concept,extra,'lab slides, in your list order')
    print(lab,'best',len(best),'extra',len(extra),'concept',len(concept),'covered',got,'/',len(P4BOLD[lab]))
    miss=[t for t,_,_ in P4BOLD[lab] if t not in {x for c in best+extra for x in c['terms']}]
    print('no photo:',miss)
