"""Practical 3 (Labs 16-18) image decks from the COURSE SLIDE .pptx files; bold terms = screenshots only.
cd tools && python3 p3ppt.py /path/to/pptx_dir   (repo root needs: ln -s . site)"""
import sys,os,re,html,json,time,shutil
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import pptdeck as P, p3shots as SH, p3data as PD
import deck; deck.PRACTICAL=3
from deck import *
SRC=sys.argv[1]; os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
WORK='/home/claude/p3work'; os.makedirs(WORK,exist_ok=True)
E=html.escape
DECKS=[('Lab_15_Neck__Thorax_and_Thoracic_Limb-2.pptx','Lab 16 slides',lambda i:16,[(29,'Neck'),(99,'Thoracic wall + axilla')]),
 ('Neck_Thorax.pptx','Neck/Thorax slides',lambda i:16 if i<=5 else 17,[(5,'Neck'),(10,'Thoracic wall'),(99,'Lungs + thymus')]),
 ('Lab_17_Deep_vessels_of_the_thorax__lungs.pptx','Lab 17 slides',lambda i:17,[(7,'Thoracic wall'),(30,'Pleura + mediastinum'),(53,'Lungs + bronchi'),(66,'Veins + lymph'),(99,'Arteries')]),
 ('Lab_18_ANS_structures__Heart.pptx','Lab 18 slides',lambda i:18,[(29,'Arteries + phrenic n.'),(59,'Autonomic nerves'),(82,'Pericardium + heart surfaces'),(136,'Heart chambers + valves'),(999,'Coronary vessels')]),
 ('ANS_structures.pptx','ANS slides',lambda i:18,[(7,'Arteries + phrenic n.'),(99,'Autonomic nerves')]),
 ('Heart.pptx','Heart slides',lambda i:18,[(7,'Pericardium + heart surfaces'),(15,'Heart chambers + valves'),(99,'Coronary vessels')])]
REG_ORDER=['Neck','Thoracic wall','Thoracic wall + axilla','Pleura + mediastinum','Lungs + bronchi','Lungs + thymus','Veins + lymph','Arteries','Arteries + phrenic n.','Autonomic nerves','Pericardium + heart surfaces','Heart chambers + valves','Coronary vessels']
TITLEFIX={('Lab_17_Deep_vessels_of_the_thorax__lungs.pptx',12):'Costal pleura (green = parietal pleura lining the ribs)',('Lab_17_Deep_vessels_of_the_thorax__lungs.pptx',13):'Green: costal pleura · Blue: diaphragmatic pleura',('Lab_17_Deep_vessels_of_the_thorax__lungs.pptx',15):'Mediastinal pleura (red)'}
FIXNAME={'Caudal part Caudal Lobe':'Caudal part of the left cranial lobe (slide typo says "Caudal part Caudal Lobe")','Cranial part Cranial Lobe':'Cranial part of the left cranial lobe'}
AB={'a':'artery','aa':'arteries','v':'vein','vv':'veins','n':'nerve','nn':'nerves','m':'muscle','mm':'muscles','lig':'ligament','rt':'right','lt':'left','cr':'cranial','cd':'caudal','azygous':'azygos','br':'branch'}
def norm(t):
    t=t.lower(); toks=re.findall(r'[a-z0-9]+',t); out=[]
    for w in toks:
        w=AB.get(w,w)
        if len(w)>4 and w.endswith('s') and not w.endswith(('ss','us','is')): w=w[:-1]
        if w=='arterie': w='artery'
        if w in('the','of','and'): continue
        out.append(w)
    return out
def has(h,n): return bool(n) and any(h[i:i+len(n)]==n for i in range(len(h)-len(n)+1))
def match(name,terms):
    L=norm(name); hits=[]
    for ti,(t,al) in enumerate(terms):
        for a in ([] if t in SH.EXACT else [t])+al:
            ex=a.startswith('='); A=norm(a.lstrip('='))
            if (L==A) if ex else has(L,A):
                # a branch/vein OF a structure is not the structure
                if not ex and L!=A and (set(L)-set(A))&{'branch','vein','artery','nerve','ganglion'} and not (set(A)&{'branch','vein','artery','nerve','ganglion','arteries','veins','nerves'}): continue
                hits.append(ti); break
    return hits
FX={}
for lst in (PD.L16,PD.L17,PD.L18):
    for t,al,f in lst:
        for k in [t]+al:
            if f and ' '.join(norm(k.lstrip('='))) not in FX: FX[' '.join(norm(k.lstrip('=')))]=f
FXMAP={'Left cranial lobe: cranial and caudal parts':'left lung cranial lobe cranial part','Right cranial lobe':'right lung cranial lobe','Right accessory lobe':'right lung accessory lobe','Right middle lobe':'right lung middle lobe','Left caudal lobe':'left lung caudal lobe','Brachiocephalic veins':'brachiocephalic vein','External jugular veins':'external jugular vein','Vagosympathetic trunk':'vagosympathetic trunk','Pectinate muscles':'pectinate muscle','Subclavian veins':'subclavian vein','Right caudal lobe':'right lung caudal lobe','Transversus thoracis':'transversus thoracis m','Papillary muscles':'papillary muscles','Phrenic nerves':'phrenic nerves','Trabecula septomarginalis (moderator band)':'trabecula septomarginalis','Visceral serous pericardium (epicardium)':'epicardium','Semilunar cusps':'pulmonary valve semilunar cusps','Pulmonary valve':'pulmonary valve semilunar cusps','Circumflex branch':'circumflex branch','Chordae tendineae':'chordae tendineae'}
def facts(term):
    k=' '.join(norm(FXMAP.get(term,term)))
    return FX.get(k,[])
def region(regs,i):
    for hi,n in regs:
        if i<=hi: return n
def orient_ans(d):
    return 'Say it out loud: view, recumbency, cranial/caudal, dorsal/ventral. Then check the orientation tags on the image.'
def stg(p,a,big=False): return deck.stg(p,a,big)
def card(kind,qimg,aimg,title,src,labels,notes,descs,lab,terms,bold_only=False):
    S=[stg('🧭 Orient first',E(orient_ans(None)))]
    if kind in('hl','find'):
        q='Identify the highlighted structure.' if kind=='hl' else f'📍 Find + point to: {title}'
        if kind=='hl':
            S.append(stg('❓ Name it (complete + specific)',E(title),True))
        for ti in match(title,terms):
            for p,a in facts(terms[ti][0]): S.append(stg(E(p),E(a)))
    else:
        q=f'Name #1–#{len(labels)}' if len(labels)>1 else 'Name #1'
        for n,lb in labels:
            nm=FIXNAME.get(lb['name'],lb['name']); more=f' <span style="font-weight:600">({E(lb["more"])})</span>' if lb['more'] else ''
            star=' ⭐' if match(lb['name']+' '+lb['more'],terms) else ''
            S.append(stg(f'❓ <b>#{n}</b>{star} — name it (complete + specific)',E(nm)+more,True))
            for ti in match(lb['name']+' '+lb['more'],terms):
                for p,a in facts(terms[ti][0]): S.append(stg(f'#{n} · {E(p)}',E(a)))
    if descs: S.append(stg('💡 On-slide hint',E(' · '.join(descs))))
    if notes: S.append(stg('📝 Slide note (professor)',E(' '.join(notes)).replace('\n','<br>')))
    if aimg: S.append(stg('📖 Labeled slide',f'<img src="{aimg}" loading="lazy">'))
    return f'<section class="card"><div class="q">{E(q)}<span class="tagline">{E(src)}</span></div><div class="pic"><img src="{qimg}" loading="lazy"></div>{"".join(S)}<div class="rev">💗 TAP TO REVEAL</div></section>'
def textcard(q,a,tag): return text_card2(q,a,tag)
LABS={16:SH.S16,17:SH.S17,18:SH.S18}
TITLE={16:'Lab 16 · Neck + thoracic wall',17:'Lab 17 · Deep vessels of the thorax + lungs',18:'Lab 18 · ANS structures + heart'}
def build():
    allc=[]; textslides=[]
    for fn,short,home,regs in DECKS:
        path=f'{SRC}/{fn}'; info=P.analyze(path)
        # pick one slide per run of same-titled slides (max highlight); untitled slides stand alone
        sel=[]; i=0
        while i<len(info):
            d=info[i]; j=i
            if d['title']:
                while j+1<len(info) and info[j+1]['title']==d['title']: j+=1
            run=info[i:j+1]
            byimg={}
            for x in run: byimg.setdefault(x['pics'][0]['hash'] if x['pics'] else None,[]).append(x)
            for grp in byimg.values():
                mx=max(x['hl'] for x in grp)
                # keep every distinct highlight variant (e.g. costal vs mediastinal pleura); else the single best slide
                hlv=[x for x in grp if x['hl']>0] if (mx>0 and not any(x['labels'] for x in grp)) else [max(grp,key=lambda x:(len(x['labels'])>0,x['hl'],-x['i']))]
                if d['title']=='Veins' or (grp[0]['labels'] and mx>0): hlv=[max(grp,key=lambda x:(x['hl'],-x['i']))]
                sel+=hlv
            i=j+1
        numbering={}; seen=set()
        for d in sel:
            if not d['pics']:
                if d['title'] or d['notes'] or d['desc']: textslides.append((home(d['i']+1),d,short))
                continue
            d['title']=TITLEFIX.get((fn,d['i']+1),d['title'])
            key=(d['pics'][0]['hash'],d['title'],tuple(l['name'] for l in d['labels']),d['hl'] and d['i'])
            if key in seen: continue
            seen.add(key)
            labs=sorted(d['labels'],key=lambda l:(round(l['box'][1]/0.35),l['box'][0]))
            d['num']=[(k+1,l) for k,l in enumerate(labs)]
            numbering[d['i']]={(l['shape'],l['paras'][0]):k for k,l in d['num']}
            d['kind']='num' if labs else ('hl' if d['hl'] else 'find')
            d['deck']=fn; d['short']=short; d['home']=home(d['i']+1); d['region']=region(regs,d['i']+1)
            allc.append(d)
        wd=f'{WORK}/{fn[:-5]}'; os.makedirs(wd,exist_ok=True)
        P.make_versions(path,wd,numbering)
        for d in [c for c in allc if c['deck']==fn]:
            tag=re.sub(r'\W','',fn[:10])+f"_s{d['i']+1}"
            q=P.crop_render(f'{wd}/q.pdf',d['i'],d,f'site/assets/p3s_{tag}q.jpg')
            d['q']=f'assets/p3s_{tag}q.jpg'
            d['a']=None
            if d['kind']=='num':
                P.crop_render(f'{wd}/a.pdf',d['i'],d,f'site/assets/p3s_{tag}a.jpg'); d['a']=f'assets/p3s_{tag}a.jpg'
    return allc,textslides
def write(allc,textslides):
    rep={}
    for lab,terms in LABS.items():
        main={};extra={};hits={}
        for d in allc:
            names=[d['title']] if d['kind']!='num' else [l['name']+' '+l['more'] for _,l in d['num']]
            m=set()
            for nm in names: m|=set(match(nm,terms))
            src=f"📚 course slide · {d['short']} #{d['i']+1}"
            if m:
                for t in m: hits.setdefault(t,[]).append(d['region'])
                main.setdefault(d['region'],[]).append(card(d['kind'],d['q'],d['a'],d['title'],src,d['num'],d['notes'],d['desc'],lab,terms))
            elif d['home']==lab:
                extra.setdefault(d['region'],[]).append(card(d['kind'],d['q'],d['a'],d['title'],src,d['num'],d['notes'],d['desc'],lab,terms))
        TT=[]; ttxt=''
        for hl,d,short in textslides:
            if hl!=lab and not set(match(d['title'],terms)): continue
            body=' '.join(d['notes']+d['desc']).replace('Note:','').strip()
            if not d['title'] or not body: continue
            TT.append(textcard(f"{d['title']}?",body,f'🧠 Course slide · {short} #{d["i"]+1}')); ttxt+=' '+d['title'].lower()
            for t in match(d['title'],terms): hits.setdefault(t,[]).append('🧠')
        for ti,(t,al) in enumerate(terms):
            if ti in hits: continue
            a=SH.CONCEPT.get(t) or ' · '.join(f'{p} {x}' for p,x in facts(t))
            if a: TT.append(textcard(f'{t}?',a,'🧠 Bold term · no slide photo')); hits.setdefault(ti,[]).append('🧠')
        TT[0]=TT[0].replace('class="card"','class="card on"',1)
        open(f'site/gross-anatomy-lab{lab}-terms.html','w').write(page(f'Lab {lab} · No-Image Terms',f'{len(TT)} cards · course-slide text + bold terms without a slide photo',''.join(TT),back=f'gross-anatomy-lab{lab}-images.html'))
        def blocks(dct):
            out=[]
            for r in REG_ORDER:
                cs=dct.get(r,[])
                for k in range(0,len(cs),15): out.append((r+(f' ({k//15+1})' if len(cs)>15 else ''),cs[k:k+15]))
            return out
        mb,eb=blocks(main),blocks(extra)
        rows=[];got=0
        for ti,(t,al) in enumerate(terms):
            h=hits.get(ti,[]); photo=[x for x in h if x!='🧠']
            if photo: cell='⭐ '+E(', '.join(dict.fromkeys(photo))); got+=1
            elif h: cell='🧠 No-image terms · ❗ no photo yet'; got+=1
            else: cell='❗ not in decks yet'
            if t in SH.NOTE: cell=E(SH.NOTE[t])
            rows.append(f'<tr><td>{E(t)}</td><td>{cell}</td></tr>')
        n=len([t for t in terms if t[0] not in SH.NOTE])
        chk=f'<details class="sec chk"><summary>✅ Bold-term checklist · {got}/{n} covered</summary><p>Same order as your screenshot. ⭐ = bold-term block (course-slide photo) · 🧠 = no-image terms deck · ❗ = no photo yet.</p><div class="tw"><table>{"".join(rows)}</table></div></details>'
        deck.checklist=lambda *a,_c=chk:_c
        deck.EXTRA_DESC='Non-bold structures from the same course slides. "All portions are fair game."'
        write_lab(lab,TITLE[lab],mb,eb,len(TT))
        rep[lab]=(sum(len(c) for _,c in mb),sum(len(c) for _,c in eb),len(TT),got,n,[t for ti,(t,_) in enumerate(terms) if not [x for x in hits.get(ti,[]) if x!='🧠']])
    return rep
if __name__=='__main__':
    a,t=build(); r=write(a,t)
    for k,v in r.items(): print(k,'main',v[0],'extra',v[1],'terms',v[2],'covered',v[3],'/',v[4],'\n   no photo:',v[5])
