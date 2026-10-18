"""Practical 3 hubs: ⭐ "Best pictures" = ONE best card per bold term, in bold-list order, blocks of ≤12.
Every other bold-term deck moves to "📚 More practice" (same terms, more pictures). Idempotent.
Rank: 📷 my photo > 📚 course slide (single highlight) > course slide (numbered) > ✏️/📖 diagram > 🌐 UMN; fewer labels wins.
Pipeline: p3labs → umn → lab16draw → p3simplify → p3split → p3best → p3check
  python3 tools/p3best.py 16 17 18 19 21 22 23 24"""
import sys,os,re,time,html
sys.path.insert(0,'tools')
from bs4 import BeautifulSoup
from deck import page
src=open('tools/p3split.py').read(); exec(src[:src.index('for n in map')])   # norm, has, terms, items, item_bold, answer_text
V=str(int(time.time())); E=html.escape
def score(card,txt,nitems):
    t=card.get_text(' ')[:600]; q=(card.select_one('.q').get_text(' ') if card.select_one('.q') else '')
    if '📷' in t: s=60
    elif '📚 course slide' in t or 'course slides' in t: s=50 if 'highlighted' in q else 42
    elif '✏️' in t or 'Diagram' in t or '📖' in t: s=34
    elif '🌐' in t or 'UMN' in t: s=30
    else: s=25
    if 'find + point' in q.lower() or 'No labels' in q: s-=6
    return s-min(nitems,12)
for n in map(int,sys.argv[1:]):
    T=terms(n); hubf=f'gross-anatomy-lab{n}-images.html'; hub=open(hubf).read()
    # current decks: main (non-best) + more + diag
    def sec(cls):
        m=re.search(r'<div class="sec '+cls+r'"[^>]*>(.*?)</div>',hub,re.S); return m
    pages=[]
    for cls in ('main','more','diag'):
        m=sec(cls)
        if not m: continue
        for href,name in re.findall(r'<a href="([^"?]+)[^"]*">([^<]*)<span>',m.group(1)):
            if '-best' in href or not os.path.exists(href): continue
            if href not in [p[1] for p in pages]: pages.append((cls,href,name.strip()))
    cards=[]; css=''
    for cls,href,name in pages:
        s=BeautifulSoup(open(href).read(),'html.parser')
        if not css and s.find('style'): css=s.find('style').string or ''
        for c in s.select('section.card'):
            txt=answer_text(c); it=items(txt)
            cards.append(dict(html=str(c),items=it,score=score(c,txt,len(it)),src=name))
    chosen=[]; used=set(); covered=set()
    for ti,als in enumerate(T):
        if ti in covered: continue
        best=None
        for ci,c in enumerate(cards):
            if not any(item_bold(x,[als]) for x in c['items']): continue
            if best is None or c['score']>cards[best]['score']: best=ci
        if best is None: continue
        if best not in used:
            used.add(best); chosen.append(best)
        for tj,a2 in enumerate(T):     # anything else that card names is covered too
            if any(item_bold(x,[a2]) for x in cards[best]['items']): covered.add(tj)
    # write best decks (≤12 per block)
    for f in os.listdir('.'):
        if re.match(rf'gross-anatomy-lab{n}-best\d+\.html$',f): os.remove(f)
    blocks=[chosen[i:i+12] for i in range(0,len(chosen),12)]
    links=''
    for bi,blk in enumerate(blocks,1):
        hh=''.join(cards[c]['html'] for c in blk).replace('class="card on"','class="card"').replace('class="card"','class="card on"',1)
        fn=f'gross-anatomy-lab{n}-best{bi}.html'
        pg=page(f'Lab {n} · ⭐ Best pictures {bi}',f'One best picture per bold term · {len(blk)} cards',hh,back=f'{hubf}?v={V}')
        pg=re.sub(r'<style>.*?</style>',lambda _:f'<style>{css}</style>',pg,count=1,flags=re.S)
        open(fn,'w').write(pg)
        links+=f'<a href="{fn}?v={V}">⭐ Best pictures {bi}<span>{len(blk)} cards</span></a>'
    # rebuild sections: main = best only · more = every other bold-term deck
    morelinks=''.join(f'<a href="{h}?v={V}">{E(nm)}<span>{open(h).read().count("<section class=")} cards</span></a>' for cls,h,nm in pages if cls in('main','more'))
    keep=re.findall(r'<!--(?:umn|mine)-->.*?<!--/(?:umn|mine)-->',sec('main').group(1)+(sec('more').group(1) if sec('more') else ''),re.S)
    main=f'<div class="sec main"><h2>⭐ Best pictures · start here</h2><p>One best picture for every bold term, in your list order. Do these first.</p>{links}</div>'
    more=f'<div class="sec more" style="border-left:7px solid #b48ad6"><h2>📚 More practice · same bold terms</h2><p>Every bold term, in small blocks.</p>{morelinks}</div>'
    hub=hub.replace(sec('main').group(0),main,1)
    if sec('more'): hub=hub.replace(sec('more').group(0),more,1)
    else: hub=hub.replace(main,main+more,1)
    # 🔁 markers: future umn.py / lab16me.py runs insert after '<p>Every bold term, in small blocks.</p>' (now in More practice);
    # strip the duplicate decks those markers would add (they're already listed in morelinks)
    hub=re.sub(r'<!--(umn|mine)-->.*?<!--/\1-->','',hub,flags=re.S)
    open(hubf,'w').write(hub)
    print(n,'bold terms',len(T),'covered by best',len(covered),'best cards',len(chosen),'blocks',len(blocks))
