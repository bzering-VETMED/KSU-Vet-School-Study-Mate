"""Practical 3 strict audit (made by Claude): every bold term must be the ANSWER of an IMAGE card inside a page
linked from the hub's ⭐ section (concept/text cards and fact mentions don't count).
  python3 tools/p3audit.py 16 17 18 19 21 22 23 24 25"""
import sys,re,os
sys.path.insert(0,'tools')
from bs4 import BeautifulSoup
_src=open('tools/p3split.py').read(); exec(_src[:_src.index('for n in map')])   # norm, has, terms, items, item_bold, answer_text
def main_pages(n):
    h=open(f'gross-anatomy-lab{n}-images.html').read()
    m=re.search(r'<div class="sec main">(.*?)</div>',h,re.S)
    return [f for f in re.findall(r'href="([^"?]+)',m.group(1)) if os.path.exists(f)] if m else []
out={}
for n in map(int,sys.argv[1:]):
    T=terms(n); got=set()
    for f in main_pages(n):
        s=BeautifulSoup(open(f).read(),'html.parser')
        for c in s.select('section.card'):
            if not c.select_one('.pic img'): continue
            its=items(answer_text(c))
            for ti,als in enumerate(T):
                if ti not in got and any(item_bold(x,[als]) for x in its): got.add(ti)
    miss=[T[i][0] for i in range(len(T)) if i not in got]; out[n]=miss
    print(f'Lab {n}: {len(T)-len(miss)}/{len(T)} with image in ⭐ · MISSING: {miss}')
