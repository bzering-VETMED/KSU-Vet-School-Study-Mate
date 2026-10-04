"""Practical 3 builder: Labs 16-18 from the lab-guide figures in the professor's Notes PDFs.
Run from the site root's parent with ./site -> repo:  cd tools && python3 p3build.py <pdfdir>"""
import sys,os,re,json,copy,html,time
sys.path.insert(0,os.path.dirname(__file__))
import pymupdf as fz
import guidefigs as G
import deck; deck.PRACTICAL=3
from deck import *
import p3data as D
PDF=sys.argv[1] if len(sys.argv)>1 else '/mnt/project'
SITE=os.path.join(os.path.dirname(__file__),'..'); os.chdir(SITE); os.makedirs('site',exist_ok=True) if not os.path.exists('site') else None
import p3shots as SH
LABS={16:D.L16,17:D.L17,18:D.L18}; TERMS={16:D.T16,17:D.T17,18:D.T18}
TITLES={16:'Lab 16 · Vertebral joints + superficial neck & thoracic wall',17:'Lab 17 · Deep vessels of the thorax + lungs',18:'Lab 18 · ANS structures + heart'}
E=html.escape
# ---------- normalize ----------
AB={'a':'artery','aa':'arteries','v':'vein','vv':'veins','n':'nerve','nn':'nerves','m':'muscle','mm':'muscles','lig':'ligament','br':'branch','brr':'branches','trk':'trunk','lnn':'lymph nodes','ln':'lymph node'}
def norm(t):
    t=t.lower().replace('’',"'")
    t=re.sub(r'\([^)]*\)',lambda m:' '+m.group(0)[1:-1]+' ',t)
    toks=re.findall(r"[a-z0-9]+",t)
    out=[]
    for w in toks:
        w=AB.get(w,w)
        if w in('the','of','and') : out.append(w); continue
        if len(w)>4 and w.endswith('s') and not w.endswith(('ss','us','is')): w=w[:-1]
        if w=='arterie': w='artery'
        out.append(w)
    return [w for w in out if w not in('the','of')]
def _shots(lst):
    fx={}
    for L in (D.L16,D.L17,D.L18):
        for t,al,f in L:
            for k in [t]+al:
                kk=' '.join(norm(k.lstrip('=')))
                if f and kk not in fx: fx[kk]=f
    out=[]
    for t,al in lst:
        f=[]
        for k in [t]+[a for a in al if not a.startswith('=')]:
            f=fx.get(' '.join(norm(k)),[])
            if f: break
        out.append((t,al,f))
    return out
def contains(hay,needle):
    n=len(needle)
    return any(hay[i:i+n]==needle for i in range(len(hay)-n+1)) if n else False
VESSEL={'artery','vein','nerve','branch','trunk','ganglion','groove'}
def match(label,terms):
    L=norm(label); best=None; exacts=set()
    for ti,(term,al,_) in enumerate(terms):
        for a in ([] if term in SH.EXACT else [term])+al:
            exact=a.startswith('='); A=norm(a.lstrip('='))
            ok = (L==A) if exact else contains(L,A)
            if not ok: continue
            if not exact and (set(L)&VESSEL)-set(A) and L!=A:
                # label is a vessel/branch/nerve of the structure, not the structure itself
                if not (set(L)-set(A))<= {'and','vein','artery','nerve','ventral','branch','right','left'} or 'branch' in set(L)-set(A): continue
            sc=len(A)+(100 if L==A else 0)
            if not best or sc>best[0]: best=(sc,ti)
            if sc>=100: exacts.add(ti)
    if not best: return None
    return best[1]
def match_all(label,terms):
    t=match(label,terms)
    if t is None: return []
    L=norm(label); out=[t]
    for ti,(term,al,_) in enumerate(terms):
        if ti!=t and any(norm(a.lstrip('='))==L for a in [term]+al): out.append(ti)
    return out
# ---------- figures ----------
def load():
    figs=[]
    for lab in (16,17,18):
        pdf=f'{PDF}/Lab_{lab}.pdf'
        for f in G.run(pdf):
            f['pdf']=pdf; f['lab']=lab; figs.append(f)
    out=[]; seen=set()
    for f in figs:
        b=fz.Rect(f['box'])
        if b.height>600: continue                       # chapter-opener art
        # caption fixes
        for l in list(f['labels']):
            if l['text'].startswith('B,'): f['caption']='Fig. 3-15 '+l['text']; f['labels'].remove(l)
        key=(f['caption'][:40],round(b.x0),round(b.y0))
        if f['caption'].startswith('Fig. 3-14, cont'):
            if 'cont' in seen: continue
            seen.add('cont')
        out.append(f)
    return out
def split_multi(f):
    """split a figure holding two stacked images (Fig. 3-22 A/B) into two cards"""
    d=fz.open(f['pdf']); p=d[f['page']]
    ims=[fz.Rect(i['bbox']) for i in p.get_image_info() if fz.Rect(i['bbox']).intersects(fz.Rect(f['box'])) and fz.Rect(i['bbox']).width>60]
    ims.sort(key=lambda r:r.y0)
    if len(ims)<2 or ims[0].y1>ims[1].y0+5: return [f]
    parts=[]
    for k,im in enumerate(ims):
        g=copy.deepcopy(f); lo=(ims[k-1].y1+2) if k else -1; hi=(ims[k+1].y0 if k+1<len(ims) else 9999)-2
        g['labels']=[l for l in f['labels'] if lo<= (l['rect'][1]+l['rect'][3])/2 <=hi]
        bx=fz.Rect(im)
        for l in g['labels']: bx|=fz.Rect(l['rect'])
        g['box']=list(bx); g['part']='AB'[k]; parts.append(g)
    return parts
CAPFIX={(17,3,0):'Fig. 3-8 A, Schematic transverse section of thorax through cranial mediastinum, caudal view.',
        (17,4,0):'Fig. 3-9 A, Schematic transverse section of thorax through heart, caudal view.'}
LEG={ (17,3,1):('Fig. 3-8 B, CT image, cranial thorax (caudal view; L/R marked).',['Longus colli muscle','Trachea','Cranial vena cava','Right cranial lobe','Cranial mediastinum','Cranial part of left cranial lobe','Brachiocephalic trunk','Left subclavian artery']),
      (17,4,1):('Fig. 3-9 B, CT image, midthorax (caudal view; L/R marked).',['Esophagus','Right principal bronchus','Carina of trachea','Ventral mediastinum-phrenicopericardial ligament','Heart','Left pulmonary artery','Aorta']),
      (17,4,2):('Fig. 3-9 C, CT image, caudal thorax (caudal view; L/R marked).',['Right caudal lobe','Caudal vena cava','Accessory lobe','Plica venae cavae','Heart','Caudal mediastinum','Left caudal lobe','Esophagus','Aorta'])}
L320=['Vertebral artery and nerve','Communicating rami from cervicothoracic ganglion to ventral branches of cervical and thoracic nerves','Left cervicothoracic ganglion','Ansa subclavia','Left subclavian artery','Left vagus nerve','Left recurrent laryngeal nerve','Left tracheobronchial lymph node','Sympathetic trunk ganglion','Sympathetic trunk','Ramus communicans','Aorta','Dorsal intercostal artery (12a)','Dorsal branch of vagus nerve','Esophagus','Ventral trunk of vagus nerve','Accessory lobe of lung','Phrenic nerve to diaphragm','Paraconal interventricular a., v., and groove','Pulmonary trunk','Internal thoracic artery and vein','Brachiocephalic trunk','Cardiac autonomic nerves','Thymus','Cranial vena cava','Middle cervical ganglion','Left subclavian vein','Costocervical trunk','External jugular vein','Vagosympathetic trunk','Common carotid artery','Longus colli muscle']
NUM320=[str(i) for i in range(1,13)]+['12a']+[str(i) for i in range(13,32)]
def side_fix(text,cap,x,box):
    t=text; c=cap.lower(); low=t.lower()
    if 'left lung, medial' in c and re.match(r'(caudal lobe|cranial part|caudal part)',low): t='Left lung, '+t
    if 'left lateral' in c and low.startswith('lung,'): t='Left '+t[0].lower()+t[1:]
    if 'right lateral' in c and low.startswith('lung,'): t='Right '+t[0].lower()+t[1:]
    if 'left lateral' in c and low in('common carotid artery','internal thoracic artery'): t='Left '+low
    if 'right lateral' in c and low in('common carotid artery','internal thoracic artery'): t='Right '+low
    if 'transverse section' in c and low in('caudal lobe',):  # caudal view: viewer's left = dog's left
        t=('Left ' if x<(box[0]+box[2])/2 else 'Right ')+low
    if c.startswith('fig. 3-15 a') and not re.search(r'vein|veins|gland|cartilage|node|arch|branch|esophagus|trachea|trunk|vena',low): t=t+' vein'
    if (c.startswith('fig. 3-18') or c.startswith('fig. 3-19')) and not re.search(r'trunk|aorta|arch|sternum|artery',low): t=t+' artery'
    if c.startswith('fig. 3-19') and low=='subclavian': t='Right subclavian artery'
    return t
REGION=[(r'^Fig\. 2-',"Vertebral joints + ribs"),(r'^Fig\. 3-[1-3]\b',"Neck"),(r'^Fig\. 3-[4-7]\b',"Thoracic wall"),(r'^Fig\. 3-(8|9|10|11|12|13)\b',"Pleura, mediastinum + lungs"),(r'^Fig\. 3-1[4-9]',"Great vessels"),(r'^Fig\. 3-2[01]\b',"Autonomic nerves"),(r'^Fig\. 3-2[2-5]',"Heart")]
def region(cap):
    for rx,n in REGION:
        if re.match(rx,cap): return n
    return 'Other'
def figno(cap):
    m=re.match(r'Fig\.\s*([\d-]+)(?:,\s*cont.d)?\s*([A-C])?',cap); return (m.group(1)+(' cont.' if 'cont' in cap[:20] else '')) if m else '?'
# ---------- cards ----------
def stg(p,a,big=False): return deck.stg(p,a,big)
def fig_card(qimg,aimg,cap,src,nums,facts_on=True,lab=None):
    """nums: list of (n, display_name, facts)"""
    S=[stg('🧭 Orient first: view, recumbency, cranial/caudal, dorsal/ventral?',E(cap),False)]
    for n,name,facts in nums:
        S.append(stg(f'❓ <b>#{n}</b> — name it (complete + specific)',E(name),True))
        if facts_on:
            for pr,an in facts: S.append(stg(f'#{n} · {E(pr)}',E(an)))
    if aimg: S.append(stg('📖 Labeled figure',f'<img src="{aimg}" loading="lazy">'))
    q=f'Name {"#1" if len(nums)==1 else "#1–#"+str(len(nums))}'
    return f'<section class="card"><div class="q">{E(q)}<span class="tagline">{E(src)}</span></div><div class="pic"><img src="{qimg}" loading="lazy"></div>{"".join(S)}<div class="rev">💗 TAP TO REVEAL</div></section>'
def legend_card(qimg,cap,src,items,star):
    S=[stg('🧭 Orient first: which plane/view? Which side is the dog\'s left?',E(cap))]
    for n,name in items:
        S.append(stg(f'❓ <b>#{n}</b>{" ⭐" if n in star else ""} — name it',E(name),True))
    return f'<section class="card"><div class="q">Name the numbered structures<span class="tagline">{E(src)}</span></div><div class="pic"><img src="{qimg}" loading="lazy"></div>{"".join(S)}<div class="rev">💗 TAP TO REVEAL</div></section>'
V=str(int(time.time()))
def build():
    figs=[]
    for f in load(): figs+=split_multi(f)
    # per-page index for fixes
    cnt={}
    for f in figs:
        k=(f['lab'],f['page']); f['idx']=cnt.get(k,0); cnt[k]=f['idx']+1
        f['caption']=CAPFIX.get((f['lab'],f['page'],f['idx']),f['caption'])
        if f.get('part')=='B' and 'Fig. 3-22' in f['caption']: f['caption']='Fig. 3-22 B, Dorsal aspect of heart.'
        elif f.get('part')=='A' and 'Fig. 3-22' in f['caption']: f['caption']='Fig. 3-22 A, Interior of right atrium, right lateral aspect.'
        if f['caption'].startswith('Fig. 3-4') and f['idx']==1: f['caption']='Fig. 3-4 B, Transverse section of the thoracic wall (13th rib level).'
        if f['caption'].startswith('Fig. 3-4') and f['idx']==0: f['caption']='Fig. 3-4 A, Schematic transection of thoracic wall: distribution of an intercostal artery.'
        for l in f['labels']: l['fix']=side_fix(l['text'],f['caption'],(l['rect'][0]+l['rect'][2])/2,f['box'])
    os.makedirs('site/assets',exist_ok=True)
    rendered={}
    def img(f,tag,numbered,erase=True):
        key=f"p3_l{f['lab']}p{f['page']}f{f['idx']}{f.get('part','')}_{tag}"
        q=f'site/assets/{key}q.jpg'; a=f'site/assets/{key}a.jpg'
        if key not in rendered:
            if erase: G.render(f['pdf'],f,q,a,numbered)
            else:
                d=fz.open(f['pdf']); p=d[f['page']]; b=fz.Rect(f['box'])
                p.get_pixmap(clip=b,dpi=300).save(q.replace('.jpg','.png'))
                from PIL import Image; Image.open(q.replace('.jpg','.png')).convert('RGB').save(q,quality=88); os.remove(q.replace('.jpg','.png')); a=None
            rendered[key]=1
        return f'assets/{key}q.jpg', (f'assets/{key}a.jpg' if erase else None)
    labs={}
    for lab,terms in LABS.items():
        main={}; extra={}; hits={}
        for f in figs:
            cap=f['caption']; src=f"📖 lab guide · {figno(cap)}{(' '+f['part']) if f.get('part') else ''}" + ('' if f['lab']==lab else f' (from Lab {f["lab"]} notes)')
            leg=LEG.get((f['lab'],f['page'],f['idx']))
            is320=cap.startswith('Fig. 3-20')
            if leg or is320:
                cap2,items=(leg if leg else (cap,L320))
                nums=list(range(1,len(items)+1)) if leg else NUM320
                star=set(); mi=[]
                for n,it in zip(nums,items):
                    t=match(it,terms)
                    if t is not None: star.add(n); mi.append((n,it,t))
                if not mi: continue
                qi,_=img(f,'leg',[],erase=False)
                for n,it,t in mi:
                    for tt in match_all(it,terms): hits.setdefault(tt,[]).append(region(cap2))
                main.setdefault(region(cap2),[]).append(legend_card(qi,cap2,src,[(n,it) for n,it,_ in mi],star))
                extra.setdefault(region(cap2),[]).append(legend_card(qi,cap2,src,list(zip(nums,items)),star))
                continue
            labs_=f['labels']; m=[]
            for i,l in enumerate(labs_):
                if G.keep_label(l['text']) and match(l['fix'],terms) is None: continue
                ts=match_all(l['fix'],terms)
                if ts: m.append((i,ts))
            for i,ts in m: labs_[i]['quiz']=True
            erasable=[i for i,l in enumerate(labs_) if not G.keep_label(l['text']) or match(l['fix'],terms) is not None]
            # spatial order (top→bottom, left→right)
            key=lambda i:(round(labs_[i]['rect'][1]/25),labs_[i]['rect'][0])
            if m:
                m.sort(key=lambda x:key(x[0]))
                # one number per structure-term (dupes share the card, numbered separately)
                for c0 in range(0,len(m),8):
                    ch=m[c0:c0+8]
                    qi,ai=img(f,f'm{lab}_{c0}',[(k+1,i) for k,(i,t) in enumerate(ch)])
                    nums=[]
                    for k,(i,ts) in enumerate(ch):
                        facts=[]
                        for t in ts:
                            term,al,fc=terms[t]; facts+=[((term+' · '+p) if len(ts)>1 else p,a) for p,a in fc]
                            hits.setdefault(t,[]).append(region(cap))
                        lab_t=labs_[i]['fix']
                        disp=terms[ts[0]][0] if len(norm(lab_t))<len(norm(terms[ts[0]][0])) and set(norm(lab_t))<=set(norm(terms[ts[0]][0])) else lab_t
                        nums.append((k+1,disp,facts))
                    main.setdefault(region(cap),[]).append(fig_card(qi,ai,cap,src+(f' · part {c0//8+1}' if len(m)>8 else ''),nums))
            if False and f['lab']==lab and erasable:
                er=sorted(erasable,key=key)
                qi,ai=img(f,'all',[(k+1,i) for k,i in enumerate(er)])
                nums=[(k+1,labs_[i]['fix'],[]) for k,i in enumerate(er)]
                extra.setdefault(region(cap),[]).append(fig_card(qi,ai,cap,src+' · ALL labels',nums,facts_on=False))
        labs[lab]=(main,extra,hits)
    return labs
def blocks(d,label):
    out=[]
    for reg in [n for _,n in REGION]+['Other']:
        cs=d.get(reg,[])
        for i in range(0,len(cs),15):
            out.append((reg+(f' ({i//15+1})' if len(cs)>15 else ''),cs[i:i+15]))
    return out
def checklist_html(lab,hits,terms_text):
    rows=[];got=0
    for ti,(term,al,_) in enumerate(LABS[lab]):
        if ti in hits: cell='⭐ '+E(', '.join(dict.fromkeys(hits[ti]))); got+=1
        elif term.lower().split(' (')[0].split(':')[0] in terms_text or any(a.lstrip('=') in terms_text for a in al if len(a)>4):
            cell='🧠 No-image terms · ❗ no photo yet'; got+=1
        else: cell='❗ not in decks yet'; pass
        rows.append(f'<tr><td>{E(term)}</td><td>{cell}</td></tr>')
    return f'<details class="sec chk"><summary>✅ Bold-term checklist · {got}/{len(LABS[lab])} covered</summary><p>Order = professor\'s bold-print list in the Lab {lab} notes. ⭐ = bold-term block (lab-guide figure) · 🧠 = no-image terms deck · ❗ no photo yet = upload a dissection photo to add one.</p><div class="tw"><table>{"".join(rows)}</table></div></details>',got
def write(labs):
    """Diagram images = lab-guide figures, numbered bold labels (professor's notes lists).
    Written as labN-diagK.html and injected into the existing course-slide hub (built by p3ppt.py)."""
    import glob
    out={}
    for lab,(main,extra,hits) in labs.items():
        for f in glob.glob(f'site/gross-anatomy-lab{lab}-diag*.html'): os.remove(f)
        links=[]
        for k,(name,cards) in enumerate(blocks(main,'main'),1):
            cs=list(cards); cs[0]=cs[0].replace('class="card"','class="card on"',1)
            fn=f'gross-anatomy-lab{lab}-diag{k}.html'
            open(f'site/{fn}','w').write(page(f'Lab {lab} · Diagrams · {name}',f'📖 Lab-guide diagram images · {len(cs)} cards',''.join(cs),back=f'gross-anatomy-lab{lab}-images.html'))
            links.append(f'<a href="{fn}?v={V}">{E(name)}<span>{len(cs)} cards</span></a>')
        sec=f'<!--diag--><div class="sec diag" style="border-left:7px solid #4f8fc0"><h2>📖 Diagram images</h2><p>Lab-guide drawings + CT images (not your course slides). Labels numbered; optional extra reps.</p>{"".join(links)}</div><!--/diag-->'
        hub=f'site/gross-anatomy-lab{lab}-images.html'; h=open(hub).read()
        h=re.sub(r'<!--diag-->.*?<!--/diag-->','',h,flags=re.S)
        k=h.find('<div class="sec terms">'); h=h[:k]+sec+h[k:]
        for ti,(t,_,_) in enumerate(LABS[lab]):
            if ti in hits:
                regs=E(', '.join(dict.fromkeys(hits[ti])))
                h=h.replace(f'<tr><td>{E(t)}</td><td>🧠 No-image terms · ❗ no photo yet</td></tr>',f'<tr><td>{E(t)}</td><td>📖 Diagram images: {regs} · 🧠 terms (no course-slide photo)</td></tr>')
        open(hub,'w').write(h); out[lab]=sum(len(c) for _,c in blocks(main,'main'))
    return out
LABS={16:_shots(SH.S16),17:_shots(SH.S17),18:_shots(SH.S18)}
if __name__=='__main__':
    print(write(build()))
