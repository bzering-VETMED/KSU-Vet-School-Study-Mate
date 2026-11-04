"""Clean look (Bethany, Nov 3): strip the 'extra junk' from every page —
⚠️ precision-traps boxes, orange source-disagreement / flag boxes, legend lines, ★-reason lines.
Cards themselves are never touched. Idempotent. Run from repo root after ANY build:  python3 tools/clean.py"""
import glob,re
from bs4 import BeautifulSoup
SEL=['.traps','.trap','.flag','.legend','.why']
WORDS=re.compile(r'precision trap|source disagreement|open items?\b',re.I)
n=0
for f in glob.glob('*.html'):
    raw=open(f).read()
    if not any(k in raw for k in ('traps','trap"','flag','legend','class="why"','Precision trap','Source disagreement','Open item')): continue
    s=BeautifulSoup(raw,'html.parser'); hit=0
    for sel in SEL:
        for el in s.select(sel):
            if el.name=='section' and 'card' in (el.get('class') or []): continue
            el.decompose(); hit+=1
    for h in s.find_all(['h2','h3','summary','b','strong']):
        if h.decomposed if hasattr(h,'decomposed') else False: continue
        if WORDS.search(h.get_text()):
            box=h.find_parent(['div','details','aside'])
            if box and not box.find_parent('section',class_='card') and 'wrap' not in (box.get('class') or []):
                box.decompose(); hit+=1
    if hit: open(f,'w').write(str(s)); n+=1
print('pages cleaned:',n)
