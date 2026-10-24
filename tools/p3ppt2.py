"""Practical 3 · course-slide .pptx decks for Labs 22, 24, 25 (Lab 22 full deck, Lab 25 deck, Pelvic Cavity deck).  Made by Claude.
Each slide pair = plain photo + the same photo with a colored highlight; we keep the highlighted one (title removed
from the image, shown in the reveal). Slides with text-box labels become numbered cards (labels → 1, 2, 3 …).
Pages: gross-anatomy-lab{n}-ppt{k}.html (≤15 cards), registered in the hub's <!--p3src--> list so p3best.py can use
them to fill ⭐ gaps.  Then run: p3best → p3dedupe → p3check → p3ours → p3abdfix.
  python3 tools/p3ppt2.py <dir with l22.pptx l25.pptx pc.pptx>"""
import sys,os,re,html,time
sys.path.insert(0,'tools')
import pptdeck as P, deck
from deck import page,stg
SRC=sys.argv[1]; V=str(int(time.time())); E=html.escape
WORK='/home/claude/p3work2'; os.makedirs(WORK,exist_ok=True)
# (file, short name, slide-number → lab)
DECKS=[('l22.pptx','Lab 22 slides',lambda i:22),('l25.pptx','Lab 25 slides',lambda i:25),('pc.pptx','Pelvic cavity slides',lambda i:24 if i<=10 else 25)]
def select(info):
    sel=[];i=0
    while i<len(info):
        d=info[i];j=i
        if d['title']:
            while j+1<len(info) and info[j+1]['title']==d['title']: j+=1
        run=info[i:j+1]; byimg={}
        for x in run: byimg.setdefault(x['pics'][0]['hash'] if x['pics'] else None,[]).append(x)
        for g in byimg.values(): sel.append(max(g,key=lambda x:(len(x['labels'])>0,x['hl'],-x['i'])))
        i=j+1
    return sel
def clean(t): return re.sub(r'\s+',' ',t).strip()
def card(d,src):
    notes=' '.join(d['notes']).replace('Note:','').strip()
    S=[]          # Bethany: no "orient first" stage, one tap = full answer
    if d['kind']=='num':
        q=f"Name #1–#{len(d['num'])}" if len(d['num'])>1 else 'Name #1'
        for n,lb in d['num']:
            more=f' <span style="font-weight:600">({E(lb["more"])})</span>' if lb['more'] else ''
            S.append(stg(f'❓ <b>#{n}</b> — name it (complete + specific)',E(lb['name'])+more,True))
    else:
        q='Identify the highlighted structure.' if d['kind']=='hl' else f"📍 Find + point to: {d['title']}"
        if d['kind']=='hl': S.append(stg('❓ Name it (complete + specific)',E(d['title']),True))
    if d['desc']: S.append(stg('💡 On-slide hint',E(' · '.join(clean(x) for x in d['desc']))))
    if notes: S.append(stg('📝 Slide note (professor)',E(notes)))
    if d.get('a'): S.append(stg('📖 Labeled slide',f'<img src="{d["a"]}?v={V}" loading="lazy">'))
    return f'<section class="card"><div class="q">{E(q)}<span class="tagline">{E(src)}</span></div><div class="pic"><img src="{d["q"]}?v={V}" loading="lazy"></div>{"".join(S)}<div class="rev">💗 TAP TO REVEAL</div></section>'
bylab={}
for fn,short,home in DECKS:
    path=f'{SRC}/{fn}'; info=P.analyze(path); sel=[d for d in select(info) if d['pics']]
    numbering={}
    for d in sel:
        labs=sorted(d['labels'],key=lambda l:(round(l['box'][1]/0.35),l['box'][0]))
        d['num']=[(k+1,l) for k,l in enumerate(labs)]
        numbering[d['i']]={(l['shape'],l['paras'][0]):k for k,l in d['num']}
        d['kind']='num' if labs else ('hl' if d['hl'] else 'find')
        if not d['title'] and d['kind']!='num': continue
    wd=f'{WORK}/{fn[:-5]}'; os.makedirs(wd,exist_ok=True)
    if not (os.path.exists(f'{wd}/q.pdf') and os.path.exists(f'{wd}/a.pdf')): P.make_versions(path,wd,numbering)
    tag=fn[:-5]
    for d in sel:
        if not d['title'] and d['kind']!='num': continue
        out=f'assets/p3x_{tag}_{d["i"]+1}q.jpg'; P.crop_render(f'{wd}/q.pdf',d['i'],d,out); d['q']=out; d['a']=None
        if d['kind']=='num': o2=f'assets/p3x_{tag}_{d["i"]+1}a.jpg'; P.crop_render(f'{wd}/a.pdf',d['i'],d,o2); d['a']=o2
        d['title']=clean(d['title']) or ' · '.join(l['name'] for _,l in d['num'])
        bylab.setdefault(home(d['i']+1),[]).append((short,d,card(d,f"📚 course slide · {short} #{d['i']+1}")))
for lab,items in bylab.items():
    hubf=f'gross-anatomy-lab{lab}-images.html'
    css=re.search(r'<style>(.*?)</style>',open(f'gross-anatomy-lab22-best1.html').read(),re.S).group(1)
    for f in os.listdir('.'):
        if re.match(rf'gross-anatomy-lab{lab}-ppt\d+\.html$',f): os.remove(f)
    regs=[]
    for k in range(0,len(items),15):
        blk=items[k:k+15]; fn=f'gross-anatomy-lab{lab}-ppt{k//15+1}.html'
        nm=f"{blk[0][0]} · {blk[0][1]['title'][:22]} → {blk[-1][1]['title'][:22]}"
        hh=''.join(c for _,_,c in blk).replace('class="card"','class="card on"',1)
        pg=page(f'Lab {lab} · {nm}',f'📚 Course slide photos · {len(blk)} cards',hh,back=f'{hubf}?v={V}')
        open(fn,'w').write(re.sub(r'<style>.*?</style>',lambda _:f'<style>{css}</style>',pg,count=1,flags=re.S))
        regs.append(f'more::{fn}::{nm}')
    h=open(hubf).read(); m=re.search(r'<!--p3src:(.*?)-->',h)
    if m:
        parts=[p for p in m.group(1).split('|') if '-ppt' not in p.split('::')[1]]+regs
        h=h.replace(m.group(0),'<!--p3src:'+'|'.join(parts)+'-->'); open(hubf,'w').write(h)
    print(lab,len(items),'cards',len(regs),'pages', 'registered' if m else 'NO p3src in hub')
