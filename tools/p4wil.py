"""Practical 4 · Dr. Wilhite 'Canine head and eye dissection' .pptx (text-box labels) → numbered cards.  Made by Claude.
Labels → 1, 2, 3 … (box + leader line kept); captions ('Canine right eye', 'Deep vessels of the head') stay as text.
Every number is answered on ONE card. Each slide goes to the lab (29–32) whose bold terms it shows most.
cards(lab) → (gap_candidates, extra): p4pptlab/p4stub put a card in ⭐ only when it adds an uncovered bold term."""
import sys,os,re,html,time
sys.path.insert(0,'tools')
import pptdeck as P, p4lab26 as B
from p4bold import P4BOLD
E=html.escape; V=str(int(time.time()))
SRC='/mnt/user-data/uploads/Canine_Head_and_eye_Dissection.pptx'; WD='/home/claude/p4wil'
CAP=re.compile(r'^(canine|bovine|equine|deep (vessels|nerves)|superficial (veins|nerves)|cherry eye|\*$)',re.I)
FULL=[(r'\bext\.','external'),(r'\ba\.$','artery'),(r'\bA\.$','artery'),(r'\bv\.$','vein'),(r'\bn\s?\.$','nerve'),(r'\bm\.$','muscle'),(r'\blnn?\.$','lymph node'),
      (r'\bbr\.','branch'),(r'Maxilary','Maxillary'),(r'Plapebrum','palpebra'),(r'Orra','Ora'),(r'Cilliary','Ciliary')]
def full(s):
    for a,b in FULL: s=re.sub(a,b,s)
    return s[0].upper()+s[1:] if s else s
def _all():
    info=P.analyze(SRC); out=[]; numbering={}
    for d in info:
        if not d['pics']: continue
        labs=[l for l in d['labels'] if not CAP.match(l['name'].strip())]
        if not labs: continue
        labs=sorted(labs,key=lambda l:(round(l['box'][1]/0.35),l['box'][0]))
        d['num']=[(k+1,l) for k,l in enumerate(labs)]
        numbering[d['i']]={(l['shape'],l['paras'][0]):k for k,l in d['num']}
        out.append(d)
    os.makedirs(WD,exist_ok=True)
    if not os.path.exists(f'{WD}/q.pdf'): P.make_versions(SRC,WD,numbering,keep=True)
    return out
_C=None
def cards(lab):
    global _C
    if _C is None:
        _C={}
        for d in _all():
            names=[(n,full((l['name']+' '+l['more']).strip())) for n,l in d['num']]
            hits={L:sorted({t for _,nm in names for t in B.terms_in(nm,L)},key=[t for t,_,_ in P4BOLD[L]].index) for L in (29,30,31,32)}
            homes=[L for L in hits if hits[L]]            # Nov 7: a slide goes to EVERY lab whose bold terms it labels
            if not homes: continue
            q=f'assets/p4w_{d["i"]+1}q.jpg'; a=f'assets/p4w_{d["i"]+1}a.jpg'
            P.crop_render(f'{WD}/q.pdf',d['i'],d,q); P.crop_render(f'{WD}/a.pdf',d['i'],d,a)
            ans=''.join(f'<div class="fx"><b>#{n}</b> {E(nm)}</div>' for n,nm in names)
            k=len(names); qq=f'Name #1–#{k}' if k>1 else 'Name #1'
            h=(f'<section class="card"><div class="q">{E(qq)}<span class="tagline">📚 course slide · Dr. Wilhite head + eye deck #{d["i"]+1}</span></div>'
               f'<div class="pic"><img src="{q}?v={V}" loading="lazy"></div><div class="stg ans"><div class="pr">❓ Name every number (complete + specific)</div>'
               f'<div class="an">{ans}<img src="{a}?v={V}" loading="lazy"></div></div><div class="rev">💗 TAP TO REVEAL</div></section>')
            for home in homes: _C.setdefault(home,[]).append(dict(name=' · '.join(nm for _,nm in names),terms=hits[home],html=h))
    cs=_C.get(lab,[])
    return cs,[]
