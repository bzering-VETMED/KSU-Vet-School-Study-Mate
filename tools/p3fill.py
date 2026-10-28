"""Practical 3 · last-gap fill (made by Claude). For every bold term that is NOT the answer of an image card in its lab's
⭐ section (see p3audit.py), copy the best image card from anywhere in the app (own lab's other decks first, then other
labs), plus any drawn gap cards from tools/p3draw.py (assets/p3draw_*.svg). Writes gross-anatomy-lab{n}-fill1.html and
links it at the end of the hub's ⭐ section (<!--fill-->). Idempotent; run AFTER p3best/p3web:
  python3 tools/p3fill.py 16 17 18 19 21 22 23 24"""
import sys,re,os,glob,time,json
sys.path.insert(0,'tools')
from bs4 import BeautifulSoup
from deck import page
_src=open('tools/p3split.py').read(); exec(_src[:_src.index('for n in map')])
V=str(int(time.time()))
DRAW=json.load(open('tools/p3draw_cards.json')) if os.path.exists('tools/p3draw_cards.json') else {}
SKIP=re.compile(r'mock|games|-terms|-functions|-lec\d|practical|-fill\d|rad-|quiz')
def main_pages(h):   # the curated source decks (best/web/lecture), wherever the hub now lists them
    return [f for f in dict.fromkeys(re.findall(r'href="([^"?]+)',h)) if os.path.exists(f) and re.search(r'-(best|web|lect)\d+\.html$',f)]
cache={}
def cards(f):
    if f not in cache:
        s=BeautifulSoup(open(f).read(),'html.parser')
        cache[f]=[(c,items(answer_text(c))) for c in s.select('section.card') if c.select_one('.pic img')]
    return cache[f]
def score(f,n):
    m=re.match(r'gross-anatomy-lab(\d+)-(\w+?)\d*s?\.html',f); lab,kind=(int(m.group(1)),m.group(2)) if m else (0,'x')
    pr={'umn':0,'best':1,'ours':1,'mine':1,'main':2,'ppt':2,'cross':3,'gapfill':3,'web':3,'more':4,'extra':5,'diag':6}.get(kind,7)
    return (0 if lab==n else 1, pr, f)
pool=sorted(f for f in glob.glob('gross-anatomy-*.html') if not SKIP.search(f))
for n in map(int,sys.argv[1:]):
    hubf=f'gross-anatomy-lab{n}-images.html'; h=open(hubf).read(); T=terms(n); got=set()
    for f in main_pages(h):
        for c,its in cards(f):
            for ti,als in enumerate(T):
                if any(item_bold(x,[als]) for x in its): got.add(ti)
    out=[];seen=set();filled=[];left=[]
    for ti,als in enumerate(T):
        if ti in got: continue
        best=None
        for f in sorted(pool,key=lambda f:score(f,n)):
            for c,its in cards(f):
                src=c.select_one('.pic img')['src'].split('?')[0]
                if src in seen: continue
                if any(item_bold(x,[als]) for x in its): best=(f,c,src); break
            if best: break
        if best:
            f,c,src=best; seen.add(src); c=BeautifulSoup(str(c),'html.parser').section
            tg=c.select_one('.tagline')
            if tg: tg.string=tg.get_text()+f' · 🔗 copied for: {als[0]}'
            out.append(str(c)); filled.append(als[0])
            for tj,a2 in enumerate(T):        # one copied card may cover more missing terms
                if tj not in got and any(item_bold(x,[a2]) for x in items(answer_text(c))): got.add(tj)
        elif str(n) in DRAW and any(als[0].lower() in d['covers'] for d in DRAW[str(n)]): pass
        else: left.append(als[0])
    for d in DRAW.get(str(n),[]): out.append(d['html'].replace('{V}',V))
    fn=f'gross-anatomy-lab{n}-fill1.html'
    h=re.sub(r'<!--fill-->.*?<!--/fill-->','',h,flags=re.S)
    if out:
        css=re.search(r'<style>(.*?)</style>',open('gross-anatomy-lab22-best1.html').read(),re.S).group(1)
        pg=page(f'Lab {n} · ⭐ Last gaps filled',f'Bold terms that had no picture in ⭐ · {len(out)} cards',''.join(out).replace('class="card"','class="card on"',1),back=f'{hubf}?v={V}')
        open(fn,'w').write(re.sub(r'<style>.*?</style>',lambda _:f'<style>{css}</style>',pg,count=1,flags=re.S))
        link=f'<!--fill--><a href="{fn}?v={V}">⭐ Last gaps filled · photos + drawings<span>{len(out)} cards</span></a><!--/fill-->'
        m=re.search(r'(<div class="sec main">.*?)(</div>)',h,re.S); h=h[:m.end(1)]+link+h[m.end(1):]
    open(hubf,'w').write(h)
    print(f'Lab {n}: copied {len(filled)} {filled} · drawn {len(DRAW.get(str(n),[]))} · STILL NONE: {left}')
