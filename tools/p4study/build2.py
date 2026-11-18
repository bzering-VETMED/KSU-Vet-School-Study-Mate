"""Bold Term Study Photos v2 (made by Claude, Nov 16): ONE label per photo (all other labels + arrows removed),
that label blurred; one tap reveals label + term + study sentence. Dr. Wilhite's deck photos first for Labs 29–32."""
import sys,os,re,html,json,hashlib,io,base64
sys.path.insert(0,'/home/claude/repo/tools'); sys.path.insert(0,'/home/claude/studysheets')
import pymupdf as fz
from PIL import Image,ImageOps,ImageDraw
import build, p4lab26 as B, pptdeck as P, p4wil
from p4bold import P4BOLD
from iso import isolate
E=html.escape; R='/home/claude/repo/'; OUT='/home/claude/studysheets/single/'; os.makedirs(OUT,exist_ok=True)
DECKS=[('/mnt/user-data/uploads/Canine_Head_and_eye_Dissection.pptx','/home/claude/p4wil/a.pdf','📚 Dr. Wilhite head + eye deck #'),
       ('/home/claude/new/eye.pptx','/home/claude/p4eye/a.pdf','📚 Dr. Malreddy eye lecture #'),
       ('/home/claude/new/diehl1.pptx','/home/claude/p4dh1/a.pdf','📚 Dr. Diehl Digestive Head 1 #')]
_DI=None
def deck_index():
    global _DI
    if _DI is not None: return _DI
    _DI={}
    for src,apdf,tag in DECKS:
        if not (os.path.exists(src) and os.path.exists(apdf)): continue
        for d in P.analyze(src):
            if not d['pics']: continue
            for l in d['labels']:
                nm=p4wil.full((l['name']+' '+l['more']).strip())
                import p4umn
                for L in range(26,33):
                    for t in set(p4umn.strict_terms(nm,L)+p4umn.strict_terms(re.sub(r'\s+(artery|vein|nerve|muscle|lymph node)$','',nm)+' '+nm.split()[-1],L)):
                        _DI.setdefault((L,t),[]).append((apdf,d['i'],[v*72 for v in l['box']],[[v*72 for v in pc['box']] for pc in d['pics']],tag+str(d['i']+1)))
    return _DI
def deck_img(L,t):
    for apdf,i,box,pics,tag in deck_index().get((L,t),[]):
        lr=fz.Rect(box); clip=fz.Rect(lr)
        for pb in pics: clip|=fz.Rect(pb)
        page=fz.open(apdf)[i]; clip=(clip+(-8,-8,8,8))&page.rect
        out=f'{OUT}w_{os.path.basename(os.path.dirname(apdf))}_{i}_{re.sub(r"[^a-z0-9]+","_",t)}.jpg'
        try:
            n=isolate(apdf,i+1,[lr],clip,out.replace('.jpg','.png'),dpi=150)
        except Exception as e: continue
        Image.open(out.replace('.jpg','.png')).convert('RGB').save(out,quality=88)
        return dict(img=out,boxes=isolate.boxes,cue='the one label on the photo (blurred)',tag=tag)
    return None
def kind(c):
    q=c['q']
    if 'highlight' in q: return 'hl'
    if '🎥' in c['tag'] or 'probe tip' in q: return 'video'
    if q.startswith('Identify the structure at the arrow'): return 'arrow'
    if 'UMN' in c['tag']: return 'umn'
    if '📖' in c['tag']: return 'guide'
    if 'p4skull' in (c['imgs'][0] if c['imgs'] else ''): return 'skull'
    return 'other'
def cands(L,t,cs):
    out=[]
    for c in cs:
        if not c['imgs']: continue
        for ln in c['lines']:
            part=re.sub(r'^(#\S+|Right \d+|Top-left \d+|Bottom-left \d+)\s*·?\s*','',ln)
            if t in B.terms_in(part,L) or t in B.terms_in(ln,L):
                m=re.match(r'(#\d+[a-z]?)',ln.strip()); out.append((kind(c),c,m.group(1) if m else None)); break
    return out
import single
def skull_img(c,t,L):
    import p4skull
    m=re.search(r'p4skull_(\w+)\.jpg',c['imgs'][0]); sid=m.group(1)
    for img_id,view,box,pts in p4skull.SPEC:
        if img_id!=sid: continue
        for x,y,name in pts:
            if t in B.terms_in(name,L):
                im=ImageOps.exif_transpose(Image.open(f'{R}tools/skull_src_p4/IMG_{img_id}.jpg')).convert('RGB'); d=ImageDraw.Draw(im)
                r=34; d.ellipse([x-r,y-r,x+r,y+r],fill='#e05fa8',outline='white',width=7)
                im=im.crop(box); out=f'{OUT}sk_{sid}_{re.sub(r"[^a-z0-9]+","_",t)}.jpg'; im.save(out,quality=88)
                return dict(img=out,boxes=[],cue='at the pink dot',tag='📷 my lab photo · skull model · '+view)
    return None
import umnclean
def umn_img(c,where,t):
    if not where: return None
    src=R+c['imgs'][0]; out=f'{OUT}u_{os.path.basename(src)[:-4]}_{where[1:]}.jpg'
    found,labs=umnclean.clean(src,where[1:],out)
    if found>=1: return dict(img=out,boxes=[],cue=f'{where} (the only number left on the photo)',tag=c['tag'])
    return None
SPECIAL={(28,'tympanic part (temporal bone)'):('assets/p4g28_5q.jpg',['tympanic bulla'],'the bulla under the blurred label: the tympanic part forms it'),
         (28,'ossicles'):('assets/p4g28_8q.jpg',['malleus','incus','stapes'],'the 3 blurred labels together'),
         (28,'hyoid apparatus'):('assets/p4g28_12q.jpg',[],'the whole set of hyoid bones in this drawing')}
DECKSPECIAL={(31,'buccal branches'):(21,['Dorsal Buccal','Ventral Buccal'])}
def deck_multi(L,t):
    i,keys=DECKSPECIAL[(L,t)]; apdf=DECKS[0][1]
    for d in P.analyze(DECKS[0][0]):
        if d['i']!=i: continue
        rects=[fz.Rect([v*72 for v in l['box']]) for l in d['labels'] if any(l['name'].lower().startswith(k.lower()) for k in keys)]
        clip=fz.Rect()
        for pc in d['pics']: clip|=fz.Rect([v*72 for v in pc['box']])
        for r in rects: clip|=r
        page=fz.open(apdf)[i]; clip=(clip+(-8,-8,8,8))&page.rect
        out=f'{OUT}dm_{re.sub(r"[^a-z0-9]+","_",t)}.png'; isolate(apdf,i+1,rects,clip,out,dpi=150)
        return dict(img=out,boxes=isolate.boxes,cue='the 2 blurred labels together',tag=DECKS[0][2]+str(i+1),src_kind='special')
def special(L,t):
    if (L,t) in DECKSPECIAL: return deck_multi(L,t)
    if (L,t)==(31,'trigeminal (fifth cranial) nerve') and os.path.exists('/home/claude/studysheets/iso/l33_3_V.png'):
        return dict(img='/home/claude/studysheets/iso/l33_3_V.png',boxes=[],cue='"V" on the drawing (the big nerve on the side of the pons)',tag='📖 lab guide · Lab 33 notes, Fig. 5-53 (brain, ventral view)',src_kind='special')
    sp=SPECIAL.get((L,t))
    if not sp: return None
    img,terms,cue=sp; m=re.match(r'assets/(p4g\d+[a-z]?)_(\d+)[qa]\.jpg',img)
    import guidefigs as G, p4guide
    pdf,lab=single.GPDF[m.group(1)]
    if pdf not in single._G: single._G[pdf]=G.run(pdf)
    f=single._G[pdf][int(m.group(2))]
    rects=[fz.Rect(l['rect']) for l in f['labels'] if p4guide.term_for(l['text'],lab) in terms]
    out=f'{OUT}sp_{re.sub(r"[^a-z0-9]+","_",t)}.png'
    isolate(pdf,f['page']+1,rects,fz.Rect(f['box']),out,dpi=200)
    return dict(img=out,boxes=isolate.boxes,cue=cue,tag='📖 lab guide · '+f['caption'][:60],src_kind='special')
RANK={L:(['deck','hl','video','arrow','guide','skull','umn','raw'] if L>=29 else ['hl','video','arrow','skull','guide','deck','umn','raw']) for L in range(26,33)}
def pick(L,t,cs,override=None):
    if override: return override
    sp=special(L,t)
    if sp: return sp
    cc=cands(L,t,cs); got={}
    for k in RANK[L]:
        if k=='deck': r=deck_img(L,t)
        elif k in('hl','video','arrow'):
            r=next((dict(img=R+c['imgs'][0],boxes=[],cue={'hl':'highlighted on the photo','video':'at the probe tip','arrow':'at the arrow / probe'}[k],tag=c['tag']) for kk,c,w in cc if kk==k),None)
        elif k=='guide':
            r=None
            for kk,c,w in cc:
                if kk=='guide':
                    g=single.guide(c['imgs'][0],t)
                    if g: r=dict(img=g[0],boxes=single.guide.boxes,cue='the one label on the drawing (blurred)',tag=c['tag']); break
        elif k=='skull': r=next((x for x in (skull_img(c,t,L) for kk,c,w in cc if kk=='skull') if x),None)
        elif k=='umn': r=next((x for x in (umn_img(c,w,t) for kk,c,w in cc if kk=='umn') if x),None)
        else:
            r=next((dict(img=R+c['imgs'][0],boxes=[],cue=(w+' on the photo' if w else 'on the photo'),tag=c['tag']) for kk,c,w in cc),None)
        if r: r['src_kind']=k; return r
    return None

CSS2=build.CSS+build.TODO_CSS+""".ph{position:relative}.ph img{display:block}.bl{position:absolute;backdrop-filter:blur(9px);-webkit-backdrop-filter:blur(9px);border-radius:8px;background:rgba(255,255,255,.01)}
.t{cursor:pointer}.t .ans{display:none}.t.open .ans{display:block}.t.open .bl{display:none}.t.open .tap{display:none}
.tap{text-align:center;color:#D94F7F;font-weight:800;margin-top:8px}.q{font-weight:800;color:#512888;font-size:1.05em}.q span{color:#D94F7F;margin-right:6px}
.ans .n{margin-top:8px}.bar{max-width:760px;margin:0 auto 12px;display:flex;gap:8px}.bar button{flex:1;padding:10px;border-radius:12px;border:1px solid #eadff2;background:#fff;color:#512888;font-weight:800}
details.nav summary{cursor:pointer;color:#512888;font-weight:700}"""
def card(i,t,r,s):
    bl=''.join(f'<span class="bl" style="left:{x*100:.2f}%;top:{y*100:.2f}%;width:{w*100:.2f}%;height:{h*100:.2f}%"></span>' for x,y,w,h in (r or {}).get('boxes',[]))
    img=(f'<div class="ph"><img loading="lazy" src="{build.imgsrc(r["img"])}" alt="">{bl}</div><div class="src">{E(r["tag"])}</div>' if r else '<div class="src">No photo yet.</div>')
    cue=(r or {}).get('cue','')
    return (f'<div class="t" id="t{i}" onclick="this.classList.toggle(\'open\')"><div class="q"><span>{i}.</span>Name it: {E(cue)}</div>{img}'
            f'<div class="ans"><div class="n">{E(t[0].upper()+t[1:])}</div><div class="s">{s}</div></div><div class="tap">💗 TAP TO REVEAL</div></div>')
def page(L,title,cards,n,todo=None):
    nav='<details class="nav"><summary>Term list (spoilers)</summary>'+' '.join(f'<a href="#t{i}">{E(t)}</a>' for i,t in n)+(' <a href="#todo">📷 Photograph at lab</a>' if todo else '')+'</details>'
    bar='<div class="bar"><button onclick="document.querySelectorAll(\'.t\').forEach(e=>e.classList.add(\'open\'))">Show all answers</button><button onclick="document.querySelectorAll(\'.t\').forEach(e=>e.classList.remove(\'open\'))">Hide all</button></div>'
    out=(build.APPDIR+f'lab{L}.html') if build.APP else f'/home/claude/studysheets/VAP806_Lab{L}_BoldTerms.html'
    doc=(f'<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Lab {L} Bold Terms</title><style>{CSS2}</style></head><body>{build.BACK if build.APP else ""}'
         f'<h1>Lab {L}: {E(title)}</h1><div class="sub">{len(cards)} bold terms · one label per photo (blurred) · tap a card to reveal</div><div class="nav">{nav}</div>{bar}{"".join(cards)}{build.todo_html(L,todo)}<footer>🎀 Bethany · K-State CVM Class of 2030</footer></body></html>')
    import fixlist; doc=fixlist.inject(doc)
    open(out,'w').write(build.dedupe(doc)); print(out,os.path.getsize(out)//1024,'KB')
def build_v2(L,title,sent,override={},todo=None):
    cs=build.cards(f'gross-anatomy-lab{L}-bold.html')+build.cards(f'gross-anatomy-lab{L}-extra.html')
    cards=[];names=[];log=[]
    for i,(t,_,_) in enumerate(P4BOLD[L],1):
        o=override.get(t)
        r=ov(o,t) if o else pick(L,t,cs)
        log.append((t,r and r['src_kind'])); cards.append(card(i,t,r,sent.get(t,''))); names.append((i,t))
    page(L,title,cards,names,todo)
    import collections; print(' sources:',dict(collections.Counter(k for _,k in log)),' none:',[t for t,k in log if not k],' raw:',[t for t,k in log if k=='raw'])
def ov(o,t):
    m=re.match(r'assets/(p4g\d+[a-z]?)_(\d+)a\.jpg',o['img'])
    if m and m.group(1) in single.GPDF:
        import guidefigs as G
        pdf,lab=single.GPDF[m.group(1)]
        if pdf not in single._G: single._G[pdf]=G.run(pdf)
        f=single._G[pdf][int(m.group(2))]; out=f'{OUT}bare_{m.group(1)}_{m.group(2)}.png'
        isolate(pdf,f['page']+1,[],fz.Rect(f['box']),out,dpi=200)
        return dict(img=out,boxes=[],cue=o['cue'],tag=o['tag'],src_kind='override')
    return dict(img=R+o['img'],boxes=[],cue=o['cue'],tag=o['tag'],src_kind='override')
def build_items_v2(L,title,items,todo=None):
    """items: (term, img, cue, src, sentence, boxes)"""
    cards=[card(i,t,dict(img=img,boxes=bx,cue=cue,tag=src) if img else None,s) for i,(t,img,cue,src,s,bx) in enumerate(items,1)]
    page(L,title,cards,[(i,it[0]) for i,it in enumerate(items,1)],todo)

# ---- Labs 33–35: convert their items to one-label images ----
PDF33=single.A+'5536940a-Lab_33.pdf'; PDF34=single.A+'eacfa4d6-Lab_34.pdf'; PDF35=single.A+'f54bb4ad-Lab_35.pdf'
def _clipfig(pdf,pg,k):
    p=fz.open(pdf)[pg-1]; r=fz.Rect(p.get_image_info()[k]['bbox']); Rr=fz.Rect(r)
    for b in p.get_text('blocks'):
        br=fz.Rect(b[:4]); tx=b[4].strip()
        if br.y1>r.y0-30 and br.y0<r.y1+30 and len(tx)<60 and not tx.startswith('Fig'): Rr|=br
    return fz.Rect(Rr.x0-4,Rr.y0-4,Rr.x1+4,Rr.y1+4)&p.rect
def _clip35(pg):
    p=fz.open(PDF35)[pg-1]; Rr=fz.Rect()
    for m in p.get_image_info():
        if fz.Rect(m['bbox']).get_area()>p.rect.get_area()*0.08: Rr|=fz.Rect(m['bbox'])
    R0=fz.Rect(Rr)
    for w in p.get_text('words'):
        wr=fz.Rect(w[:4])
        if len(w[4])<=6 and wr.x1>R0.x0-60 and wr.x0<R0.x1+60 and wr.y1>R0.y0-40 and wr.y0<R0.y1+40: Rr|=wr
    return fz.Rect(Rr.x0-6,Rr.y0-6,Rr.x1+6,Rr.y1+6)&p.rect
def _labelrect(pdf,pg,clip,key):
    p=fz.open(pdf)[pg-1]
    for b in p.get_text('dict')['blocks']:
        for ln in b.get('lines',[]):
            tx=''.join(s['text'] for s in ln['spans']).strip()
            if fz.Rect(ln['bbox']).intersects(clip) and tx.lower().startswith(key.lower()): return fz.Rect(ln['bbox'])
    raise ValueError(key)
def convert(L,items):
    out=[]
    for t,img,cue,src,s in items:
        bx=[]; m=re.search(r'img(33|34)/g(\d+)_(\d+)\.png$',img or '')
        m35=re.search(r'img35/p(\d+)_(.+)\.jpg$',img or '')
        try:
            if m:
                pdf=PDF33 if m.group(1)=='33' else PDF34; pg,k=int(m.group(2)),int(m.group(3)); clip=_clipfig(pdf,pg,k)
                q=re.findall(r'"([^"]+)"',cue); nums=re.findall(r'#(\d+)',cue)
                if q: rects=[_labelrect(pdf,pg,clip,q[0])]; newcue='the one label on the drawing (blurred)'; blur=True
                elif nums: rects=[fz.Rect(w[:4]) for n in nums for w in fz.open(pdf)[pg-1].get_text('words') if w[4]==n and fz.Rect(w[:4]).intersects(clip)][:len(nums)]; newcue=' + '.join('#'+n for n in nums)+' on the drawing'; blur=False
                else: rects=[]; newcue=cue; blur=False
                if 'not drawn' in cue or 'not visible' in cue or 'inside the jugular' in cue: rects=[]; newcue='not visible here: it sits inside the jugular foramen'; blur=False
                o=f'{OUT}L{L}_{re.sub(r"[^a-z0-9]+","_",t)}.png'; isolate(pdf,pg,rects,clip,o,dpi=190)
                bx=isolate.boxes if blur else []; img,cue=o,newcue
            elif m35:
                pg=int(m35.group(1)); labs=m35.group(2).split('_'); clip=_clip35(pg)
                p=fz.open(PDF35)[pg-1]; W=p.get_text('words')
                rects=[fz.Rect(w[:4]) for l in labs for w in W if w[4].strip('*,')==l and fz.Rect(w[:4]).intersects(clip)][:len(labs)]
                o=f'{OUT}L35_{re.sub(r"[^a-z0-9]+","_",t)}.png'; isolate(PDF35,pg,rects,clip,o,dpi=150,ring=True)
                img=o; cue=re.sub(r'\s*\(circled in pink\)','',cue)
        except Exception as e: print('  keep original for',t,'·',e)
        out.append((t,img,cue,src,s,bx))
    return out

import isolate as ISO
CL33={'3':fz.Rect(177,319,365,713),'4a':fz.Rect(165,109,477,362),'4b':fz.Rect(152,488,393,683),'5':fz.Rect(207,64,400,405)}
CL34={2:fz.Rect(165,406,453,575),5:fz.Rect(100,64,451,238)}
def convert(L,items):
    out=[]
    for t,img,cue,src,s in items:
        bx=[]; img=img or ''
        j=img+'.json'
        lbl=re.search(r'/iso/l3[345]_[0-9][ab]?_(.+)\.png$',img)
        label=lbl.group(1).replace('_',' ') if lbl else ''
        named=bool(label) and not re.fullmatch(r'[IVX]+\*?|[\d ]+',label)
        if os.path.exists(j) and named:
            d=json.load(open(j)); B=fz.Rect(d['box'])
            for r in d['keep']:
                r=fz.Rect(r)+(-3,-2,3,2); bx.append(((r.x0-B.x0)/B.width,(r.y0-B.y0)/B.height,r.width/B.width,r.height/B.height))
            cue='the one label on the drawing (blurred)'
        elif label and re.fullmatch(r'[IVX]+\*?',label): cue=f'"{label}" on the drawing'
        elif label and re.fullmatch(r'[\d ]+',label): cue=' + '.join('#'+x for x in label.split())+' on the drawing'
        elif '"' in cue: cue='the one label on the photo (blurred)'
        out.append((t,img,cue,src,s,bx))
    return out
