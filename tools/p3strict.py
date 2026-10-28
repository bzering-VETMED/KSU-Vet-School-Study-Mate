"""Stricter audit (made by Claude): a bold term counts only when it is a SHORT named answer (a label, ≤8 words)
on an image card in ⭐ — not a phrase buried in a long slide note.
  python3 tools/p3strict.py 16 17 ...   (add --all to search every deck for fixes)"""
import sys,re,os,glob
sys.path.insert(0,'tools')
from bs4 import BeautifulSoup
_src=open('tools/p3split.py').read(); exec(_src[:_src.index('for n in map')])
def short_items(c):
    out=[]
    for x in items(answer_text(c)):
        y=re.sub(r'\(.*?\)','',x)
        out.append(x if len(norm(y))<=8 else ' '.join(y.split()[:6]))   # long note → only its title words count
    return out
def main_pages(n):
    h=open(f'gross-anatomy-lab{n}-images.html').read()
    m=re.search(r'<div class="sec main">(.*?)</div>',h,re.S)
    return [f for f in re.findall(r'href="([^"?]+)',m.group(1)) if os.path.exists(f)] if m else []
ALL='--all' in sys.argv
CACHE=[]
if ALL:
    for f in sorted(glob.glob('gross-anatomy-lab*.html')):
        if 'images' in f or 'star1' in f: continue
        for k,c in enumerate(BeautifulSoup(open(f).read(),'html.parser').select('section.card')):
            im=c.select_one('.pic img')
            if im:
                tg=c.select_one('.tagline')
                CACHE.append((f,k+1,im['src'].split('?')[0].split('/')[-1],tg.get_text()[:45] if tg else '',short_items(c)))
for n in [int(a) for a in sys.argv[1:] if a.isdigit()]:
    T=terms(n); got=set()
    for f in main_pages(n):
        for c in BeautifulSoup(open(f).read(),'html.parser').select('section.card'):
            if not c.select_one('.pic img'): continue
            its=short_items(c)
            for ti,als in enumerate(T):
                if any(item_bold(x,[als]) for x in its): got.add(ti)
    miss=[i for i in range(len(T)) if i not in got]
    print(f'Lab {n}: {len(T)-len(miss)}/{len(T)} · WEAK: {[T[i][0] for i in miss]}')
    if ALL:
        for i in miss:
            hits=[f"{f}#{k} {src} [{tg}]" for f,k,src,tg,its in CACHE if any(item_bold(x,[T[i]]) for x in its)]
            print('   ',T[i][0],'→',hits[:6] or 'NONE')
