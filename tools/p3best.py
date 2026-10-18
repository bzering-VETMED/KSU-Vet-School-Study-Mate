"""Practical 3 hubs: ⭐ "Best pictures" = EVERY bold term in one place.
One best REAL photo per bold term (no drawings), mostly UMN, in bold-list order, blocks of ≤12;
bold terms with no real photo yet → a final 🧠 block of term cards inside ⭐.
Every other bold-term deck → "📚 More practice". Idempotent.
Rank: 🌐 UMN > 📷 my photo > 📚 course slide (single highlight > numbered); fewer labels breaks ties.
Pipeline: p3labs → umn → lab16me → lab16draw → p3simplify → p3split → p3best → p3check
  python3 tools/p3best.py 16 17 18 19 21 22 23 24"""
import sys,os,re,time,html
sys.path.insert(0,'tools')
from bs4 import BeautifulSoup
from deck import page
_src=open('tools/p3split.py').read(); exec(_src[:_src.index('for n in map')])   # norm, has, terms, items, item_bold, answer_text
V=str(int(time.time())); E=html.escape
def score(card,nitems):
    t=card.get_text(' ')[:600]; q=card.select_one('.q').get_text(' ') if card.select_one('.q') else ''
    if '✏️' in t or '📖' in t or 'lab guide' in t or 'Diagram' in t: return None      # drawings never count
    if '🌐' in t or 'UMN' in t: s=60
    elif '📷' in t: s=55
    elif 'course slide' in t: s=50 if 'highlighted' in q else 44
    else: s=40
    if 'find + point' in q.lower() or 'No labels' in q: s-=8
    return s-0.3*min(nitems,12)
def write(fn,title,sub,cards_html,css,hubf):
    hh=''.join(cards_html).replace('class="card on"','class="card"').replace('class="card"','class="card on"',1)
    pg=page(title,sub,hh,back=f'{hubf}?v={V}')
    open(fn,'w').write(re.sub(r'<style>.*?</style>',lambda _:f'<style>{css}</style>',pg,count=1,flags=re.S))
for n in map(int,sys.argv[1:]):
    T=terms(n); hubf=f'gross-anatomy-lab{n}-images.html'; hub=open(hubf).read()
    sec=lambda cls: re.search(r'<div class="sec '+cls+r'"[^>]*>(.*?)</div>',hub,re.S)
    pages=[]
    for cls in ('main','more'):
        m=sec(cls)
        if not m: continue
        for href,name in re.findall(r'<a href="([^"?]+)[^"]*">([^<]*)<span>',m.group(1)):
            if '-best' in href or not os.path.exists(href) or href in [p[1] for p in pages]: continue
            pages.append((cls,href,name.strip()))
    extra=[]
    me=sec('extra')
    if me:
        for href,name in re.findall(r'<a href="([^"?]+)[^"]*">([^<]*)<span>',me.group(1)):
            if os.path.exists(href): extra.append(('extra',href,name.strip()))
    cards=[]; css=''
    for cls,href,name in pages+extra:
        s=BeautifulSoup(open(href).read(),'html.parser')
        if not css and s.find('style'): css=s.find('style').string or ''
        for c in s.select('section.card'):
            it=items(answer_text(c)); sc=score(c,len(it))
            if sc is not None: cards.append(dict(html=str(c),items=it,score=sc-(15 if cls=='extra' else 0),nm=answer_text(c).lower(),full=c.get_text(' ').lower(),ex=cls=='extra'))
    chosen=[]; covered=set()
    for ti,als in enumerate(T):
        if ti in covered: continue
        al=[a.lstrip('=').lower() for a in als]
        best=None
        for test in (lambda c:not c['ex'] and any(item_bold(x,[als]) for x in c['items']),      # 1 · named in the answer
                     lambda c:not c['ex'] and any(a in c['nm'] for a in al),                    # 2 · answer text contains it
                     lambda c:any(a in c['full'] for a in al)):                                 # 3 · anywhere on a real-photo card
            best=max((ci for ci,c in enumerate(cards) if test(c)),key=lambda ci:cards[ci]['score'],default=None)
            if best is not None: break
        if best is None: continue
        if best not in chosen: chosen.append(best)
        covered.add(ti)
        for tj,a2 in enumerate(T):
            if any(item_bold(x,[a2]) for x in cards[best]['items']): covered.add(tj)
    nophoto=[]; tf=f'gross-anatomy-lab{n}-terms.html'
    if os.path.exists(tf):
        tcards=BeautifulSoup(open(tf).read(),'html.parser').select('section.card'); tused=set()
        for ti,als in enumerate(T):
            if ti in covered: continue
            for k,c in enumerate(tcards):
                if any(a.lstrip('=').lower() in c.get_text(' ').lower() for a in als):
                    if k not in tused: tused.add(k); nophoto.append(str(c))
                    covered.add(ti); break
    # PHOTO COMING: bold terms with nothing at all yet → placeholder card (function from the Functions page)
    from deck import text_card2
    from p3functions_data import S as FN
    names=[x[0] for x in (p3bold.P3BOLD[n] if n in p3bold.P3BOLD else [])] or [x[0] for x in {16:SH.S16,17:SH.S17,18:SH.S18}[n]]
    for ti,als in enumerate(T):
        if ti in covered: continue
        tn=names[ti]; base=re.sub(r'\s*\(.*?\)','',tn).lower()
        hint=next((a for _,_,rows in FN for q,a in rows if base in q.lower()),'')
        nophoto.append(text_card2(f'📷 No photo yet · {tn}',(hint+' · ' if hint else '')+'Get this one at lab this week',"❗ photo coming"))
        covered.add(ti)
    for f in os.listdir('.'):
        if re.match(rf'gross-anatomy-lab{n}-best\d+\.html$',f): os.remove(f)
    blocks=[chosen[i:i+12] for i in range(0,len(chosen),12)]; links=''
    for bi,blk in enumerate(blocks,1):
        fn=f'gross-anatomy-lab{n}-best{bi}.html'
        write(fn,f'Lab {n} · ⭐ Best pictures {bi}',f'Best real photo per bold term · {len(blk)} cards',[cards[c]['html'] for c in blk],css,hubf)
        links+=f'<a href="{fn}?v={V}">⭐ Best pictures {bi}<span>{len(blk)} cards</span></a>'
    if nophoto:
        fn=f'gross-anatomy-lab{n}-best{len(blocks)+1}.html'
        write(fn,f'Lab {n} · ⭐ Bold terms with no photo yet',f'Concepts + terms without a real photo · {len(nophoto)} cards',nophoto,css,hubf)
        links+=f'<a href="{fn}?v={V}">🧠 Bold terms with no photo yet<span>{len(nophoto)} cards</span></a>'
    morelinks=''.join(f'<a href="{h}?v={V}">{E(nm)}<span>{open(h).read().count("<section class=")} cards</span></a>' for cls,h,nm in pages)
    main=f'<div class="sec main"><h2>⭐ Best pictures · start here</h2><p>Every bold term in one place: the best real photo for each (mostly UMN), in your list order. Terms with no photo yet are in the last block.</p>{links}</div>'
    more=f'<div class="sec more" style="border-left:7px solid #b48ad6"><h2>📚 More practice · same bold terms</h2><p>Every bold term, in small blocks.</p>{morelinks}</div>'
    mo=sec('more'); hub=hub.replace(sec('main').group(0),main,1)
    hub=hub.replace(mo.group(0),more,1) if mo else hub.replace(main,main+more,1)
    hub=re.sub(r'<!--(umn|mine)-->.*?<!--/\1-->','',hub,flags=re.S)   # those decks are already listed in More practice
    open(hubf,'w').write(hub)
    print(n,'terms',len(T),'in ⭐',len(covered),'photos',len(chosen),'no-photo cards',len(nophoto))
