"""Practical 3 · ONE bold-term section per lab (made by Claude, Bethany's rule Oct 27):
  ⭐ = the single best picture for every bold term (one deck, bold-list order)
  📚 Extra = EVERYTHING else (old best/fill/web/lecture pages, UMN sets, slides, diagrams, terms + functions)
Picks from every image card the hub links (any section). Quality: cadaver photo (UMN / my / lab / classmate) >
course slide or dog web photo > video > lab-guide/lecture drawing or other species > Claude drawing.
Ties → the card that covers the most still-uncovered bold terms. Idempotent. Run LAST, then p3check:
  python3 tools/p3one.py 16 17 18 19 21 22 23 24 25 && python3 tools/p3check.py 16 17 18 19 21 22 23 24 25"""
import sys,re,os,time
sys.path.insert(0,'tools')
from bs4 import BeautifulSoup
from deck import page
_src=open('tools/p3split.py').read(); exec(_src[:_src.index('for n in map')])
V=str(int(time.time()))
def qual(tag,q):
    t=(tag or '').lower()
    if 'lab review video' in t: return 0   # professor/TA's own pin = most trusted
    if 'unlabeled' in t or q.lower().startswith(('📍','find')): return 6
    if '✏️' in tag or 'drawing by claude' in t or 'drawn diagram' in t: return 4
    if '🧠' in tag: return 5
    if 'umn' in t or '📷' in tag or 'our lab photo' in t or 'classmate photo' in t or 'my photo' in t: return 0
    if 'web photo (dog' in t or ('course slide' in t and 'lecture' not in t) or 'course slides' in t: return 1
    if '🎥' in tag: return 2
    if 'course slide photo' in t: return 1
    return 3
SEC=re.compile(r'<div class="sec (?!chk)([a-z]+)"[^>]*>.*?</div>(?=<div class="sec |<details|</div></body>)',re.S)
for n in map(int,sys.argv[1:]):
    hubf=f'gross-anatomy-lab{n}-images.html'; h=open(hubf).read(); T=terms(n)
    # every link in every section (+ marker blocks), minus our own star pages
    secs=list(SEC.finditer(h))
    links=[];seen=set()
    for m in secs:
        for a in re.findall(r'(?:<!--\w+-->)?<a href="[^"]+">.*?</a>(?:<!--/\w+-->)?',m.group(0),re.S):
            f=re.search(r'href="([^"?]+)',a).group(1)
            if f in seen or re.search(rf'lab{n}-star\d+\.html',f): continue
            seen.add(f); links.append((f,a,m.group(1)))
    cands=[]
    for f,a,sec in links:
        if not os.path.exists(f) or re.search(r'-terms|-functions|mock|games',f): continue
        s=BeautifulSoup(open(f).read(),'html.parser')
        for c in s.select('section.card'):
            im=c.select_one('.pic img')
            if not im: continue
            its=items(answer_text(c)); cov={ti for ti,als in enumerate(T) if any(item_bold(x,[als]) for x in its)}
            if not cov: continue
            tg=c.select_one('.tagline'); q=c.select_one('.q')
            cands.append(dict(c=c,cov=cov,q=qual(tg.get_text() if tg else '',q.get_text() if q else ''),src=im['src'].split('?')[0],f=f))
    got=set(); pick=[]; used=set()
    for ti in range(len(T)):
        if ti in got: continue
        opts=[k for k in cands if ti in k['cov'] and k['src'] not in used]
        if not opts: continue
        best=min(opts,key=lambda k:(k['q'],-len(k['cov']-got),len(k['cov'])))
        pick.append((ti,best)); used.add(best['src']); got|=best['cov']
    miss=[T[i][0] for i in range(len(T)) if i not in got]
    # write star pages
    for f in os.listdir('.'):
        if re.match(rf'gross-anatomy-lab{n}-star\d+\.html$',f): os.remove(f)
    css=re.search(r'<style>(.*?)</style>',open('gross-anatomy-lab22-best1.html').read(),re.S).group(1)
    blocks=[]
    for k in range(0,len(pick),1000):
        blk=pick[k:k+1000]; fn=f'gross-anatomy-lab{n}-star{k//15+1}.html'
        cards=[]
        for ti,b in blk:
            c=BeautifulSoup(str(b['c']),'html.parser').section
            for x in c.select('img'):
                if x.get('src') and '?' not in x['src']: x['src']+=f'?v={V}'
            cards.append(str(c))
        nm=f'All bold terms · {len(blk)} cards'
        pg=page(f'Lab {n} · ⭐ {nm}',f'Best picture for each bold term · {len(blk)} cards',''.join(cards).replace('class="card"','class="card on"',1),back=f'{hubf}?v={V}')
        open(fn,'w').write(re.sub(r'<style>.*?</style>',lambda _:f'<style>{css}</style>',pg,count=1,flags=re.S))
        blocks.append(f'<a href="{fn}?v={V}">⭐ {nm}<span>{len(blk)} cards</span></a>')
    main=(f'<div class="sec main"><h2>⭐ Bold terms · start here</h2><p>One best picture for every bold term · {len(pick)} cards cover {len(got)}/{len(T)} terms, in your bold-list order. Everything else is in 📚 Extra.</p>'+''.join(blocks)+'</div>')
    # extra: functions/terms first, then every other old link
    fnl=[a for f,a,s in links if re.search(r'-functions|-terms',f)]
    oth=[a.replace('>⭐ ','>') for f,a,s in links if not re.search(r'-functions|-terms',f)]
    extra=(f'<div class="sec more"><h2>📚 Extra · everything else</h2><p>Functions, concepts, extra angles, other dogs, diagrams, lecture slides, full photo sets.</p>'+''.join(fnl+oth)+'</div>')
    a0=secs[0].start(); a1=secs[-1].end()
    h=h[:a0]+main+extra+h[a1:]
    open(hubf,'w').write(h)
    print(f'Lab {n}: {len(pick)} cards · {len(got)}/{len(T)} terms · extra links {len(fnl)+len(oth)}' + (f' · NO PICTURE: {miss}' if miss else ''))
