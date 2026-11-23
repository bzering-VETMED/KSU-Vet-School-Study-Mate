"""Index the labeled-photo notes PDFs (Gross_Anatomy_1*.pdf): OCR'd handwritten label lines -> bold terms (made by Claude, Nov 23)."""
import sys,re,difflib,json
sys.path.insert(0,'/home/claude/repo/tools')
import pymupdf as fz
from p4bold import P4BOLD
FILES=['/mnt/user-data/uploads/Gross_Anatomy_1.pdf','/mnt/user-data/uploads/Gross_Anatomy_1_2.pdf']
def norm(s): return re.sub(r'[^a-z ]','',s.lower().replace('—',' ')).strip()
TERMS={}
for L,lst in P4BOLD.items():
    for t,_,_ in lst:
        TERMS.setdefault(norm(re.sub(r'\(.*?\)','',t)),[]).append((L,t))
def fix(s):  # handwriting OCR: s->c swaps etc.
    s=norm(s)
    for a,b in [('sranial','cranial'),('sandal','caudal'),('bransh','branch'),('sutaneous','cutaneous'),('sirsumflex','circumflex'),('oscipital','occipital'),('sana','canal'),('tossa','fossa'),('buzzal','buccal'),('buzcal','buccal'),('restus','rectus'),('inqual','lingual'),('lingval','lingual'),('slerd','sclera'),('lusidum','lucidum'),('corned','cornea'),('ured','uvea'),('saz','sac'),('sarotid','carotid'),('trockled','trochlea'),('duccal','buccal'),('duccinator','buccinator'),('chande','choanae'),('ingval','lingual')]:
        s=s.replace(a,b)
    return s
def match(s):
    s=fix(s)
    if len(s)<4: return None
    best=max(TERMS,key=lambda k:difflib.SequenceMatcher(None,s,k).ratio())
    r=difflib.SequenceMatcher(None,s,best).ratio()
    return (best,r) if r>=0.8 else None
def index():
    out=[]
    for fi,f in enumerate(FILES):
        d=fz.open(f)
        for pi,p in enumerate(d):
            lines=[]
            for b in p.get_text('dict')['blocks']:
                for ln in b.get('lines',[]):
                    tx=' '.join(s['text'] for s in ln['spans']).strip()
                    if tx: lines.append((tx,fz.Rect(ln['bbox'])))
            used=set()
            for i,(tx,r) in enumerate(lines):
                cands=[(tx,[r])]
                if i+1<len(lines): cands.append((tx+' '+lines[i+1][0],[r,lines[i+1][1]]))
                best=None
                for c,rs in cands:
                    m=match(c)
                    if m and (best is None or m[1]>best[0][1]+0.02 or (abs(m[1]-best[0][1])<0.02 and len(rs)>len(best[1]))): best=(m,rs)
                if best:
                    for L,t in TERMS[best[0][0]]: out.append(dict(file=fi,page=pi+1,L=L,term=t,ocr=tx,score=round(best[0][1],2),rects=[list(x) for x in best[1]]))
    return out
if __name__=='__main__':
    ix=index(); json.dump(ix,open('/home/claude/studysheets/ganotes.json','w'))
    got={(e['L'],e['term']) for e in ix}
    for L in range(26,33):
        miss=[t for t,_,_ in P4BOLD[L] if (L,t) not in got]
        print(L,len(P4BOLD[L])-len(miss),'/',len(P4BOLD[L]),'missing:',miss)
