"""Practical 4 · Lab 26 hub (pelvic limb vessels).  Made by Claude.
Sources
  ⭐  Lab 26 lab-slide PDF (Dr. Stueve, plain + green-highlight slide pairs) → one 'Identify the highlighted
      structure' card per highlighted slide; slide note in the reveal.  Rendered at the photo's native dpi.
  📚  'Pelvic limb vv nn' lecture-photo PDF: labels are vector text → redacted (photo pixels untouched:
      images=NONE), label box + leader line kept, pink numbered badge on the box; labeled original in the reveal.
      Only slides naming a Lab 26 bold term (nerve-only slides are held for the nerves lab).
  🧠  Bold terms with no photo yet → text cards (photograph them at lab).
Run from repo root:  python3 tools/p4lab26.py <lab26_slides.pdf> <pelvic_limb_vv_nn.pdf>
Reusable for later Practical 4 labs: slide_cards(), label_cards(), write_deck(), write_hub()."""
import sys,os,re,html,time,io
sys.path.insert(0,'tools')
import pymupdf as fz
from PIL import Image,ImageDraw,ImageFont
from p4bold import P4BOLD
E=html.escape; V=str(int(time.time()))
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
TPL=open('gross-anatomy-lab22-best1.html').read()
SIMPLE_CSS='.ans .nm{font-size:clamp(19px,2.2vw,26px);font-weight:900;text-align:center;margin:2px 0 6px}.ans .fx{font-size:15px;font-weight:650;margin:4px 0;text-align:left}.ans .fx b{color:#67338d}.ans img{margin-top:8px}'

def norm(s): return re.sub(r'[^a-z ]','',re.sub(r'\s+',' ',s.lower())).strip()
def terms_in(name,lab):
    n=' '+norm(name)+' '; out=[]
    for t,al,_ in P4BOLD[lab]:
        if any(' '+norm(a)+' ' in n or norm(a)==norm(name) for a in al): out.append(t)
    return out

def card(q,tag,img,name,facts=(),aimg=None):
    fx=''.join(f'<div class="fx"><b>{E(k)}</b> {E(v)}</div>' for k,v in facts if v)
    ai=f'<img src="{aimg}?v={V}" loading="lazy">' if aimg else ''
    return (f'<section class="card"><div class="q">{E(q)}<span class="tagline">{E(tag)}</span></div>'
            f'<div class="pic"><img src="{img}?v={V}" loading="lazy"></div>'
            f'<div class="stg ans"><div class="pr">❓ Name it (complete + specific)</div><div class="an">{name}{fx}{ai}</div></div>'
            f'<div class="rev">💗 TAP TO REVEAL</div></section>')

# ---------- ⭐ highlighted lab slides ----------
FULL={'external iliac arteries':'External iliac artery (paired: right + left)',
      'lateral saphenous vein cranial branch':'Cranial branch of the lateral saphenous vein',
      'lateral saphenous vein caudal branch':'Caudal branch of the lateral saphenous vein',
      'deep branch of medial circumflex femoral artery':'Deep branch of the medial circumflex femoral artery',
      'transverse branch of medial circumflex femoral artery':'Transverse branch of the medial circumflex femoral artery',
      'cranial branch of saphenous artery':'Cranial branch of the saphenous artery',
      'caudal branch of saphenous artery':'Caudal branch of the saphenous artery'}
def slide_cards(pdf,lab,tag,prefix,src_label):
    d=fz.open(pdf); out=[]
    for i,p in enumerate(d):
        ims=p.get_image_info(); dr=[x for x in p.get_drawings() if x.get('fill') and x['fill']!=(1.0,1.0,1.0)]
        if not ims or not dr: continue                      # keep only the highlighted copy of each pair
        t=p.get_text(); title=re.sub(r'\s+',' ',t.split('Note:')[0]).strip()
        note=re.sub(r'\s+',' ',t.split('Note:')[1].split('Dissection:')[0]).strip() if 'Note:' in t else ''
        im=max(ims,key=lambda m:(m['bbox'][2]-m['bbox'][0])*(m['bbox'][3]-m['bbox'][1]))
        r=fz.Rect(im['bbox'])&p.rect
        dpi=int(min(300,max(150,im['width']/fz.Rect(im['bbox']).width*72)))
        pm=p.get_pixmap(clip=r,dpi=dpi); fn=f'assets/{prefix}_{i+1}.jpg'
        Image.frombytes('RGB',(pm.width,pm.height),pm.samples).save(fn,quality=90)
        name=FULL.get(title.lower(),title[0].upper()+title[1:])
        out.append(dict(name=name,terms=terms_in(name,lab),html=card('Identify the highlighted structure.',f'📚 course slide · {src_label} #{i+1}',fn,
                   f'<div class="nm">{E(name)}</div>',[('📝 Slide note (professor):',note)])))
    return out

# ---------- 📚 vector-labeled lecture photos ----------
AB=[(r'\bCr\. branch, ','cranial branch of the '),(r'\bCd\. branch, ','caudal branch of the '),(r'\bext\.','external'),
    (r'\ba\. & n\.','artery and nerve'),(r'\ba\.','artery'),(r'\bn\.','nerve'),(r'\bv\.','vein'),(r'\bm\.','muscle')]
def expand(s):
    for a,b in AB: s=re.sub(a,b,s,flags=re.I)
    s=re.sub(r'\s+',' ',s).strip().lower(); return s[0].upper()+s[1:]
def groups(p):
    """one group per white label box (spans assigned to the smallest drawn rect containing them);
    spans outside any box → merged by proximity"""
    rects=[x['rect'] for x in p.get_drawings() if x['rect'].width>20 and x['rect'].height>8 and x['rect'].width<p.rect.width*0.6]
    spans=[]
    for b in p.get_text('dict')['blocks']:
        for l in b.get('lines',[]):
            for sp in l['spans']:
                if sp['text'].strip(): spans.append((fz.Rect(sp['bbox']),sp['text'].strip()))
    gs={}
    for r,t in sorted(spans,key=lambda x:(x[0].y0,x[0].x0)):
        inner=fz.Rect(r.x0+1,r.y0+1,r.x1-1,r.y1-1)
        cont=[R for R in rects if R.contains(inner)]
        key=min(cont,key=lambda R:R.get_area()) if cont else None
        if key is None:
            for k,g in gs.items():
                if g['free'] and 0<=r.y0-g['r'].y1<12 and min(r.x1,g['r'].x1)-max(r.x0,g['r'].x0)>5: key=k; break
            else: key=('free',len(gs))
        k=tuple(key) if not isinstance(key,tuple) else key
        g=gs.setdefault(k,{'r':fz.Rect(r),'t':[],'spans':[],'free':cont==[],'box':key if cont else None})
        g['r']|=r; g['t'].append(t); g['spans'].append(r)
    out=sorted(gs.values(),key=lambda g:g['r'].y0)
    i=0
    while i<len(out):        # a label split across a broken box ("Cd. branch, lateral" / "saphenous vein") → merge down
        a=out[i]; last=a['t'][-1].rstrip()
        if not re.search(r'(\.|\)|vein|artery|nerve)$',last,re.I):
            nb=[b for b in out if b is not a and 0<=b['r'].y0-a['r'].y1<16 and min(b['r'].x1,a['r'].x1)-max(b['r'].x0,a['r'].x0)>5]
            if nb:
                b=nb[0]; a['t']+=b['t']; a['spans']+=b['spans']; a['r']|=b['r']; out.remove(b); continue
        i+=1
    for g in out:
        full=re.sub(r'\s+',' ',' '.join(g['t'])); m=re.match(r'^(.*?)\s*(\(.*\))?$',full)
        g['name']=expand(m.group(1)); g['more']=expand(m.group(2).strip('()')) if m.group(2) else ''
        g['box']=g['box'] or g['r']
    return out
def label_cards(pdf,lab,keep_pages,tag,prefix,src_label,zoom=2):
    out=[]; font=ImageFont.truetype(FONT,int(18*zoom))
    for i in keep_pages:
        doc=fz.open(pdf); p=doc[i-1]; gs=groups(p)
        if not any(terms_in(g['name'],lab) for g in gs): continue
        gs=sorted(gs,key=lambda g:(round(g['box'].y0/40),g['box'].x0))
        ims=p.get_image_info(); clip=fz.Rect(ims[0]['bbox']) if ims else p.rect
        for x in p.get_drawings(): clip|=x['rect']
        clip&=p.rect; M=fz.Matrix(zoom,zoom)
        pa=p.get_pixmap(matrix=M,clip=clip); fa=f'assets/{prefix}_{i}a.jpg'
        Image.frombytes('RGB',(pa.width,pa.height),pa.samples).save(fa,quality=90)
        for g in gs:
            for r in g['spans']: p.add_redact_annot(r,fill=False)
        p.apply_redactions(images=fz.PDF_REDACT_IMAGE_NONE,graphics=fz.PDF_REDACT_LINE_ART_NONE)
        pq=p.get_pixmap(matrix=M,clip=clip); img=Image.frombytes('RGB',(pq.width,pq.height),pq.samples)
        dr=ImageDraw.Draw(img)
        for k,g in enumerate(gs,1):
            c=g['box']; cx=(c.x0+c.x1)/2*zoom-clip.x0*zoom; cy=(c.y0+c.y1)/2*zoom-clip.y0*zoom; R=16*zoom
            dr.ellipse([cx-R,cy-R,cx+R,cy+R],fill='#e05fa8',outline='white',width=3)
            dr.text((cx,cy),str(k),fill='white',font=font,anchor='mm')
        fq=f'assets/{prefix}_{i}q.jpg'; img.save(fq,quality=90)
        names=''.join(f'<div class="nm">#{k} · {E(g["name"])}'+(f' <span style="font-weight:600">({E(g["more"])})</span>' if g['more'] else '')+'</div>' for k,g in enumerate(gs,1))
        q=f'Name #1–#{len(gs)}' if len(gs)>1 else 'Name #1'
        allnames=' | '.join(g['name'] for g in gs)
        out.append(dict(name=allnames,terms=sum((terms_in(g['name'],lab) for g in gs),[]),
                        html=card(q,f'📚 course slide · {src_label} #{i}',fq,names,[],fa)))
    return out

# ---------- pages ----------
def write_deck(fn,title,sub,cards,back):
    hh=''.join(c['html'] for c in cards).replace('class="card"','class="card on"',1)
    t=TPL
    t=re.sub(r'<title>.*?</title>',f'<title>{E(title)}</title>',t,count=1)
    t=re.sub(r'<a class="back" href="[^"]*">[^<]*</a>',f'<a class="back" href="{back}?v={V}">← Back to Lab hub</a>',t,count=1)
    t=re.sub(r'<div class="hero">.*?</div>',f'<div class="hero"><h1>{E(title)}</h1><p>{E(sub)}</p></div>',t,count=1,flags=re.S)
    i=t.index('<section class="card'); j=t.rindex('</section>')+len('</section>')
    t=t[:i]+hh+t[j:]
    if SIMPLE_CSS not in t: t=t.replace('</style>',SIMPLE_CSS+'</style>',1)
    open(fn,'w').write(t)
def blocks(cards,n):
    k=max(1,-(-len(cards)//n)); size=-(-len(cards)//k); return [cards[i:i+size] for i in range(0,len(cards),size)]
HUBCSS=re.search(r'<style>(.*?)</style>',open('gross-anatomy-lab25-images.html').read(),re.S).group(1)
def write_hub(lab,title,sub,secs,practical=4):
    """secs = list of (cls, h2, p, [(fn,label,cards)], icon)"""
    where={}
    for cls,h2,pp,links,icon in secs:
        for fn,label,cards in links:
            for c in cards:
                for t in c['terms']: where.setdefault(t,(icon,label))
    rows=[];got=0
    for t,_,note in P4BOLD[lab]:
        w=where.get(t)
        if w and w[0]!='🧠': got+=1
        cell=f'{w[0]} {E(w[1])}' if w else '❗ not in decks yet'
        if w and w[0]=='🧠': cell+=' · ❗ no photo yet — photograph at lab'
        rows.append(f'<tr><td>{E(t)}</td><td>{cell}</td></tr>')
    h=(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><title>Lab {lab}</title><style>{HUBCSS}</style></head><body><div class="wrap">'
       f'<a class="back" href="gross-anatomy-practical{practical}.html?v={V}">← Back to Practical {practical}</a><div class="hero"><h1>{E(title)}</h1><p>{E(sub)}</p></div>'
       f'<details class="sec chk"><summary>✅ Bold-term checklist · {got}/{len(P4BOLD[lab])} with a photo</summary><p>Same order as your bold-term list. ⭐ = start-here photos · 📚 = more practice · 🧠 = no photo yet. ❗ = waiting on a photo.</p><div class="tw"><table>{"".join(rows)}</table></div></details>')
    for cls,h2,pp,links,icon in secs:
        if not links: h+=f'<div class="sec {cls}"><h2>{E(h2)}</h2><p>None 🎉 every bold term has a photo.</p></div>'; continue
        h+=f'<div class="sec {cls}"><h2>{E(h2)}</h2><p>{E(pp)}</p>'+''.join(f'<a href="{fn}?v={V}">{E(label)}<span>{len(cards)} cards</span></a>' for fn,label,cards in links)+'</div>'
    open(f'gross-anatomy-lab{lab}-images.html','w').write(h+'</div></body></html>')
    return got

if __name__=='__main__':
    SL,VN=sys.argv[1],sys.argv[2]; LAB=26; hub=f'gross-anatomy-lab{LAB}-images.html'
    star=slide_cards(SL,LAB,'','p4_l26s','Lab 26 slides')
    vn=label_cards(VN,LAB,list(range(1,28)),'','p4_vvnn','Pelvic limb vv nn')
    nophoto=[t for t,_,_ in P4BOLD[LAB] if not any(t in c['terms'] for c in star+vn)]
    NP={'cranial branch (medial saphenous vein)':'Runs with the cranial branch of the saphenous artery (medial side of the crus). The medial saphenous vein satellites the saphenous artery; it is the most common venipuncture site in the CAT hind limb. (Lab 26 slide 42 note)',
        'caudal branch (medial saphenous vein)':'Runs with the caudal branch of the saphenous artery (medial side of the crus, toward the tarsus). (Lab 26 slide 42 note)'}
    npc=[dict(name=t,terms=[t],html=f'<section class="card"><div class="q">🧠 {E(t)}<span class="tagline">❗ no photo yet · photograph at lab</span></div><div class="stg ans"><div class="pr">❓ Where is it + what does it travel with?</div><div class="an"><div class="nm">{E(t)}</div><div class="fx">{E(NP.get(t,""))}</div></div></div><div class="rev">💗 TAP TO REVEAL</div></section>') for t in nophoto]
    for f in os.listdir('.'):
        if re.match(rf'gross-anatomy-lab{LAB}-(best|more|nophoto)\d+\.html$',f): os.remove(f)
    links_star=[];links_more=[];links_np=[]
    for k,b in enumerate(blocks(star,12),1):
        fn=f'gross-anatomy-lab{LAB}-best{k}.html'; lab_=f'Lab 26 slides {k} · {b[0]["name"]} → {b[-1]["name"]}'
        write_deck(fn,f'Lab {LAB} · Lab slides {k}',f'⭐ Highlighted bold terms · {len(b)} cards',b,hub); links_star.append((fn,lab_,b))
    for k,b in enumerate(blocks(vn,12),1):
        fn=f'gross-anatomy-lab{LAB}-more{k}.html'; lab_=f'🔢 Numbered lecture photos {k}'
        write_deck(fn,f'Lab {LAB} · Numbered lecture photos {k}',f'📚 More practice · {len(b)} cards',b,hub); links_more.append((fn,lab_,b))
    if npc:
        fn=f'gross-anatomy-lab{LAB}-nophoto1.html'; write_deck(fn,f'Lab {LAB} · Bold terms with no photo yet','🧠 Photograph these at lab',npc,hub); links_np.append((fn,'🧠 Bold terms with no photo yet',npc))
    got=write_hub(LAB,'Lab 26 · Pelvic limb vessels','Lab slides (Dr. Stueve) + lecture photos. Small decks, one tap = full answer. 🐾',[
        ('main','⭐ Bold-term labeled photos · start here','Every bold term highlighted on the lab-slide photos, in list order.',links_star,'⭐'),
        ('terms','🧠 Bold terms with no photo yet','Not on any slide photo — photograph these at lab.',links_np,'🧠'),
        ('extra','📚 More practice','Lecture photos (Pelvic limb vv nn): labels erased → pink numbers. Different photos, same bold terms.',links_more,'📚')])
    print('star',len(star),'more',len(vn),'nophoto',nophoto,'covered',got,'/',len(P4BOLD[LAB]))
