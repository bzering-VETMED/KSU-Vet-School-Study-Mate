"""Practical 3 · each photo is studied ONCE across Labs 16–24 (made by Claude).
A photo that sits in several labs' decks is OWNED by the lab whose bold terms it shows most (tie → earlier lab).
Other labs: in ⭐ the card becomes a small "📍 Seen in Lab X" card (names this lab's bold terms on it + link);
in 📚 More practice the repeat is removed. Run after p3best.py (all labs), before p3check.py.
  python3 tools/p3dedupe.py 16 17 18 19 21 22 23 24"""
import sys,os,re,time,html,collections
sys.path.insert(0,'tools')
from bs4 import BeautifulSoup
_src=open('tools/p3split.py').read(); exec(_src[:_src.index('for n in map')])   # terms, items, item_bold, answer_text
V=str(int(time.time())); E=html.escape
LABS=list(map(int,sys.argv[1:]))
def key(card):
    im=card.select_one('.pic img'); return im['src'].split('?')[0] if im else None
pages={}   # file -> (lab, section, soup)
for n in LABS:
    hub=open(f'gross-anatomy-lab{n}-images.html').read()
    for cls in ('main','more'):
        m=re.search(r'<div class="sec '+cls+r'"[^>]*>(.*?)</div>',hub,re.S)
        if not m: continue
        for href in re.findall(r'<a href="([^"?]+)',m.group(1)):
            if os.path.exists(href) and href not in pages: pages[href]=(n,cls,BeautifulSoup(open(href).read(),'html.parser'))
T={n:terms(n) for n in LABS}
def bold_here(card,n):
    it=items(answer_text(card)); out=[]
    for als in T[n]:
        if any(item_bold(x,[als]) for x in it): out.append(als[0].lstrip('='))
    return out
occ=collections.defaultdict(list)     # image -> [(lab, cls, file, card)]
for f,(n,cls,s) in pages.items():
    for c in s.select('section.card'):
        k=key(c)
        if k: occ[k].append((n,cls,f,c))
owner={}
for k,lst in occ.items():
    labs=sorted({n for n,_,_,_ in lst})
    if len(labs)<2: continue
    cnt={n:max(len(bold_here(c,n)) for m,_,_,c in lst if m==n) for n in labs}
    owner[k]=max(labs,key=lambda n:(cnt[n],-n))
def best_page(n,k):
    for m,cls,f,c in occ[k]:
        if m==n and cls=='main': return f
    return f'gross-anatomy-lab{n}-images.html'
stubbed=removed=0; changed=set()
for k,o in owner.items():
    for n,cls,f,c in occ[k]:
        if n==o: continue
        if cls=='main':
            names=bold_here(c,n) or ['(see photo)']
            tgt=best_page(o,k)
            stub=BeautifulSoup(f'<section class="card"><div class="q textq">📍 Seen in Lab {o}<span class="tagline">studied once · Lab {o} ⭐</span></div>'
                f'<div class="stg ans"><div class="pr">❓ Lab {n} bold terms on that photo</div><div class="an"><div class="nm">{E(" · ".join(names))}</div>'
                f'<div class="fx"><a href="{tgt}?v={V}" style="color:#7b42a0;font-weight:800">Open it in Lab {o} →</a></div></div></div><div class="rev">💗 TAP TO REVEAL</div></section>','html.parser')
            c.replace_with(stub); stubbed+=1
        else:
            c.decompose(); removed+=1
        changed.add(f)
for f in changed:
    n,cls,s=pages[f]; cs=s.select('section.card')
    for c in cs: c['class']=['card']
    if cs: cs[0]['class']=['card','on']
    open(f,'w').write(str(s))
# hub link counts (drop empty More-practice decks)
for n in LABS:
    hf=f'gross-anatomy-lab{n}-images.html'; hub=open(hf).read()
    def fix(m):
        href=m.group(1)
        if href in pages and href in changed:
            k=len(pages[href][2].select('section.card'))
            return '' if k==0 else re.sub(r'<span>\d+ cards</span>',f'<span>{k} cards</span>',m.group(0))
        return m.group(0)
    hub=re.sub(r'<a href="([^"?]+)[^"]*">[^<]*<span>\d+ cards</span></a>',fix,hub)
    open(hf,'w').write(hub)
print('shared photos',len(owner),'· ⭐ repeats → 📍 stubs',stubbed,'· More-practice repeats removed',removed)
print('owners:',dict(collections.Counter(owner.values())))
