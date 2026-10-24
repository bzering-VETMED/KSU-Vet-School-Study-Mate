"""Practical 3 · 🔗 cross-lab links (made by Claude). Idempotent.
For each lab, any bold term with no labeled photo in its OWN decks gets copied cards from OTHER labs' photo decks
(any practical) where that term is a NUMBERED / highlighted answer (not just mentioned in a fact).
Writes gross-anatomy-lab{n}-cross1.html and registers it in the hub's <!--p3src--> list so p3best.py uses it for ⭐ gaps.
Also builds the Lab 25 rima pudendi card from the Lab 25 vulva slide.
Run after p3ppt2.py, before p3best.py:   python3 tools/p3cross.py 21 22 23 24 25"""
import sys,os,re,glob,time,html
sys.path.insert(0,'tools')
from bs4 import BeautifulSoup
from PIL import Image,ImageDraw,ImageFont
from deck import page,img_card_facts
_src=open('tools/p3split.py').read(); exec(_src[:_src.index('for n in map')])   # norm, has, terms, items, item_bold, answer_text
V=str(int(time.time())); E=html.escape
LABS=list(map(int,sys.argv[1:]))
SKIP=re.compile(r'-(best|more|cross)\d*\.html$|-terms|-functions|-diag|-lec|mock|games')
def photo_cards(f):
    s=BeautifulSoup(open(f).read(),'html.parser')
    for c in s.select('section.card'):
        if not c.select_one('.pic img'): continue
        t=c.get_text(' ')[:600]
        if '📖' in t or 'Diagram' in t or 'lab guide' in t: continue
        yield c
def own_named(n,T):
    hub=open(f'gross-anatomy-lab{n}-images.html').read(); got=set()
    m=re.search(r'<!--p3src:(.*?)-->',hub); files=[p.split('::')[1] for p in m.group(1).split('|')] if m else []
    files+=[f for f in glob.glob(f'gross-anatomy-lab{n}-*.html') if re.search(r'-(umn\d*|ours\d+|ppt\d+|main\d+)\.html$',f)]
    for f in set(files):
        if not os.path.exists(f) or '-cross' in f: continue
        for c in photo_cards(f):
            its=items(answer_text(c))
            for ti,als in enumerate(T):
                if any(item_bold(x,[als]) for x in its): got.add(ti)
    return got
# Lab 25 · rima pudendi badge card from the vulva slide
EXTRA={}
if os.path.exists('assets/p3x_l25_75q.jpg'):
    im=Image.open('assets/p3x_l25_75q.jpg').convert('RGB'); d=ImageDraw.Draw(im)
    F=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',34)
    d.line([(255,560),(515,560)],fill='white',width=5); d.ellipse([215,520,295,600],fill=(224,95,168),outline='white',width=5); d.text((255,560),'1',font=F,fill='white',anchor='mm')
    im.save('assets/p3x_l25_75rima.jpg',quality=90)
    EXTRA[25]=[img_card_facts('Vulva, caudal view (green = labia). Name 1.',f'assets/p3x_l25_75rima.jpg?v={V}','Rima pudendi','',f'assets/p3x_l25_75q.jpg?v={V}',
        [('🧩 Vulva =','The two labia + the opening they bound (rima pudendi)'),('🔝 Commissures','Labia fuse above + below the rima → dorsal + ventral commissures; ventral commissure points caudoventrally')],'📚 course slide · Lab 25 slides #75 (badge added)')]
pool=[f for f in glob.glob('gross-anatomy-*.html') if not SKIP.search(f) and 'section class="card' in open(f).read()]
for n in LABS:
    T=terms(n); own=own_named(n,T); out=list(EXTRA.get(n,[])); seen=set(); found=[]
    for ti,als in enumerate(T):
        if ti in own: continue
        for f in sorted(pool):
            m=re.match(r'gross-anatomy-lab(\d+)',f)
            if not m or int(m.group(1))==n: continue
            for c in photo_cards(f):
                src=c.select_one('.pic img')['src'].split('?')[0]
                if src in seen or not any(item_bold(x,[als]) for x in items(answer_text(c))): continue
                seen.add(src); found.append(als[0])
                tg=c.select_one('.tagline')
                if tg: tg.string=(tg.get_text()+f' · 🔗 from Lab {m.group(1)}')
                out.append(str(c))
    fn=f'gross-anatomy-lab{n}-cross1.html'; hubf=f'gross-anatomy-lab{n}-images.html'; h=open(hubf).read()
    mk=re.search(r'<!--p3src:(.*?)-->',h)
    parts=[p for p in (mk.group(1).split('|') if mk else []) if '-cross' not in p]
    if out:
        css=re.search(r'<style>(.*?)</style>',open('gross-anatomy-lab22-best1.html').read(),re.S).group(1)
        pg=page(f'Lab {n} · 🔗 From other labs',f'Photos from other labs that show this lab\'s bold terms · {len(out)} cards',''.join(out).replace('class="card"','class="card on"',1),back=f'{hubf}?v={V}')
        open(fn,'w').write(re.sub(r'<style>.*?</style>',lambda _:f'<style>{css}</style>',pg,count=1,flags=re.S))
        parts.append(f'more::{fn}::🔗 From other labs')
    elif os.path.exists(fn): os.remove(fn)
    if mk: h=h.replace(mk.group(0),'<!--p3src:'+'|'.join(parts)+'-->'); open(hubf,'w').write(h)
    print(n,'cross cards',len(out),'for',sorted(set(found)))
