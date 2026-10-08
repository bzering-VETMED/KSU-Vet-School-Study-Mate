"""Practical 3 decks: ONE tap shows the whole answer. Drops the 'Orient first' stage and merges every
remaining stage (names, facts, labeled image) into a single reveal. Idempotent.
Run LAST, after p3ppt.py / p3diagrams.py / lab16me.py:  python3 tools/p3simplify.py"""
import glob,re,sys
from bs4 import BeautifulSoup
CSS='.ans .nm{font-size:clamp(19px,2.2vw,26px);font-weight:900;text-align:center;margin:2px 0 6px}.ans .fx{font-size:15px;font-weight:650;margin:4px 0;text-align:left}.ans .fx b{color:#67338d}.ans img{margin-top:8px}'
n=0
for f in sorted(glob.glob('gross-anatomy-lab1[6-9]-*.html')+glob.glob('gross-anatomy-lab2[0-6]*-*.html')):
    if f.endswith('-images.html'): continue
    s=BeautifulSoup(open(f).read(),'html.parser'); ch=False
    for card in s.select('section.card'):
        st=card.select('.stg')
        if len(st)<=1 and not any('Orient' in g.select_one('.pr').get_text() for g in st): continue
        names=[];facts=[];imgs=[]
        for g in st:
            pr=g.select_one('.pr'); an=g.select_one('.an'); p=pr.get_text(' ',strip=True)
            if 'Orient' in p: continue
            for im in an.find_all('img'): imgs.append(str(im.extract()))
            a=an.decode_contents().strip()
            if not BeautifulSoup(a,'html.parser').get_text(strip=True): continue
            if '❓' in p:
                num=re.search(r'#\d+[a-z]?',p); names.append(f'<div class="nm">{(num.group(0)+" · ") if num else ""}{a}</div>')
            else:
                facts.append(f'<div class="fx"><b>{p.replace("❓","").strip()}</b> {a}</div>')
        q=card.select_one('.q'); qt=q.find(string=True,recursive=False) if q else ''
        new=BeautifulSoup(f'<div class="stg ans"><div class="pr">❓ {str(qt).strip() if qt else "Name it"}</div><div class="an">{"".join(names)}{"".join(facts)}{"".join(imgs)}</div></div>','html.parser')
        st[0].insert_before(new)
        for g in st: g.decompose()
        ch=True
    if ch:
        if CSS not in str(s):
            sty=s.find('style'); sty.string=(sty.string or '')+CSS
        open(f,'w').write(str(s)); n+=1
print('pages simplified:',n)
