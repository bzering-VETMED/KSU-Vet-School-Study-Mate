"""Practical 3 hubs · ⭐ "Bold-term labeled photos" (made by Claude). Idempotent.
  1 · CORE = every UMN labeled photo that names a bold term of this lab (deck order)
  2 · GAPS = for bold terms UMN doesn't show: best of my photos (📷) > course-slide photos (📚); never drawings
  3 · 🧠 "Bold terms with no photo yet" = its OWN section (concepts, drawings-only terms, photo-coming placeholders)
All other bold-term decks → 📚 More practice.
Pipeline: p3labs → umn → lab16me → lab16draw → p3simplify → p3split → p3best → p3dedupe → p3check
  python3 tools/p3best.py 16 17 18 19 21 22 23 24"""
import sys,os,re,time,html
sys.path.insert(0,'tools')
from bs4 import BeautifulSoup
from deck import page,text_card2
import p3bold,p3shots as SH
from p3functions_data import S as FN
_src=open('tools/p3split.py').read(); exec(_src[:_src.index('for n in map')])   # norm, has, terms, items, item_bold, answer_text
V=str(int(time.time())); E=html.escape
def kind(card):
    t=card.get_text(' ')[:600]; q=card.select_one('.q').get_text(' ') if card.select_one('.q') else ''
    if 'web photo' in t: return 'mine',54
    if 'gap fill' in t: return 'draw',20                                                    # drawings only when no photo exists
    if '✏️' in t or '📖' in t or 'lab guide' in t or 'Diagram' in t: return None,0          # other drawings never count
    find='No labels' in q or 'find-it' in t.lower() or 'find + point' in q.lower()
    if '🌐' in t or 'UMN' in t: return 'umn',(0 if find else 60)
    if '📷' in t: return 'mine',55
    if 'course slide' in t: return 'slide',(50 if 'highlighted' in q else 44)-(8 if find else 0)
    return 'other',40
from PIL import Image
import numpy as np
_FP={}
def fp(card):
    im=card.select_one('.pic img')
    if not im: return None
    p=im['src'].split('?')[0]
    if p not in _FP:
        try: a=np.array(Image.open(p).convert('L').resize((24,24))).astype(int); _FP[p]=(a>a.mean()).flatten()
        except Exception: _FP[p]=None
    return _FP[p]
def same(a,b): return a['fp'] is not None and b['fp'] is not None and a['nm']==b['nm'] and a['nm'].strip()!='' and (a['fp']!=b['fp']).sum()<=6
def write(fn,title,sub,cards_html,css,hubf):
    hh=''.join(cards_html).replace('class="card on"','class="card"').replace('class="card"','class="card on"',1)
    pg=page(title,sub,hh,back=f'{hubf}?v={V}')
    open(fn,'w').write(re.sub(r'<style>.*?</style>',lambda _:f'<style>{css}</style>',pg,count=1,flags=re.S))
for n in map(int,sys.argv[1:]):
    T=terms(n); hubf=f'gross-anatomy-lab{n}-images.html'; hub=open(hubf).read()
    names=[x[0] for x in p3bold.P3BOLD[n]] if n in p3bold.P3BOLD else [x[0] for x in {16:SH.S16,17:SH.S17,18:SH.S18}[n]]
    sec=lambda cls: re.search(r'<div class="sec '+cls+r'"[^>]*>(.*?)</div>',hub,re.S)
    pages=[]; mk=re.search(r'<!--p3src:(.*?)-->',hub)
    if mk:
        for part in mk.group(1).split('|'):
            cls,href,name=part.split('::')
            if os.path.exists(href): pages.append((cls,href,name))
    for cls in ([] if mk else ['main','more']) + ['extra']:
        m=sec(cls)
        if not m: continue
        for href,name in re.findall(r'<a href="([^"?]+)[^"]*">([^<]*)<span>',m.group(1)):
            if '-best' in href or re.search(r'-more\d+\.html$',href) or not os.path.exists(href) or href in [p[1] for p in pages]: continue
            pages.append((cls,href,name.strip()))
    cards=[]; css=''
    for cls,href,name in pages:
        s=BeautifulSoup(open(href).read(),'html.parser')
        if not css and s.find('style'): css=s.find('style').string or ''
        for c in s.select('section.card'):
            k,sc=kind(c)
            if k is None: continue
            cards.append(dict(src=href,name=name,cls=cls,fp=fp(c),html=str(c),items=items(answer_text(c)),nm=answer_text(c).lower(),full=c.get_text(' ').lower(),kind=k,score=sc-(15 if cls=='extra' else 0),ex=cls=='extra'))
    # 📖 diagram-section drawings: used ONLY to fill ⭐ gaps when no photo exists (Bethany: all bold terms in one place)
    for dsec in re.findall(r'<div class="sec diag"[^>]*>(.*?)</div>',hub,re.S):
        for href in re.findall(r'<a href="([^"?]+)',dsec):
            if not os.path.exists(href) or '-best' in href: continue
            for c in BeautifulSoup(open(href).read(),'html.parser').select('section.card'):
                if not c.select_one('.pic img'): continue
                cards.append(dict(src=href,name='📖 diagram',cls='diag',fp=fp(c),html=str(c),items=items(answer_text(c)),nm=answer_text(c).lower(),full=c.get_text(' ').lower(),kind='draw',score=18,ex=False))
    keep=[]
    for c in sorted(cards,key=lambda c:-c['score']):
        if not any(same(c,k) for k in keep): keep.append(c)
    order={id(c):i for i,c in enumerate(cards)}; cards=sorted(keep,key=lambda c:order[id(c)])
    def names_term(c,als,full=False):
        al=[x.lstrip('=').lower() for x in als]
        if any(item_bold(x,[als]) for x in c['items']) or any(x in c['nm'] for x in al): return True
        return full and any(x in c['full'] for x in al)
    covered=set()
    def cover(ci):
        for tj,a2 in enumerate(T):
            if names_term(cards[ci],a2): covered.add(tj)
    core=[]
    for ci,c in enumerate(cards):
        if c['kind']=='umn' and c['score']>0 and not c['ex'] and any(names_term(c,als) for als in T):
            core.append(ci); cover(ci)
    gaps=[]
    for ti,als in enumerate(T):
        if ti in covered: continue
        best=None
        for full in (False,True):
            cand=[ci for ci,c in enumerate(cards) if c['kind'] in('mine','slide','other','draw') and names_term(c,als,full)]
            if not cand: cand=[ci for ci,c in enumerate(cards) if c['kind']=='umn' and c['score']>-10 and ci not in core and names_term(c,als,full)]
            best=max(cand,key=lambda ci:cards[ci]['score'],default=None)
            if best is not None: break
        if best is None: continue
        if best not in gaps: gaps.append(best)
        covered.add(ti); cover(best)
    nophoto=[]; tf=f'gross-anatomy-lab{n}-terms.html'
    if os.path.exists(tf):
        tcards=BeautifulSoup(open(tf).read(),'html.parser').select('section.card'); tused=set()
        for ti,als in enumerate(T):
            if ti in covered: continue
            for k,c in enumerate(tcards):
                if any(a.lstrip('=').lower() in c.get_text(' ').lower() for a in als):
                    if k not in tused: tused.add(k); nophoto.append(str(c))
                    covered.add(ti); break
    for ti,als in enumerate(T):
        if ti in covered: continue
        base=re.sub(r'\s*\(.*?\)','',names[ti]).lower()
        hint=next((a for _,_,rows in FN for q,a in rows if base in q.lower()),'')
        nophoto.append(text_card2(f'📷 No photo yet · {names[ti]}',(hint+' · ' if hint else '')+'Get this one at lab this week','❗ photo coming'))
        covered.add(ti)
    for f in os.listdir('.'):
        if re.match(rf'gross-anatomy-lab{n}-best\d+\.html$',f): os.remove(f)
    links=''; k=0
    for label,group in (('🌐 UMN labeled photos',core),('📷 Filling the gaps · my photos, slides + diagrams',gaps)):
        bl=[group[i:i+12] for i in range(0,len(group),12)]
        for bi,blk in enumerate(bl,1):
            k+=1; fn=f'gross-anatomy-lab{n}-best{k}.html'; nm=label+(f' {bi}' if len(bl)>1 else '')
            write(fn,f'Lab {n} · {nm}',f'⭐ Bold-term labeled photos · {len(blk)} cards',[cards[c]['html'] for c in blk],css,hubf)
            links+=f'<a href="{fn}?v={V}">{E(nm)}<span>{len(blk)} cards</span></a>'
    nplink=''
    if nophoto:
        k+=1; fn=f'gross-anatomy-lab{n}-best{k}.html'
        write(fn,f'Lab {n} · Bold terms with no photo yet',f'Concepts, drawings-only terms + photos still coming · {len(nophoto)} cards',nophoto,css,hubf)
        nplink=f'<a href="{fn}?v={V}">🧠 Concepts + bold terms with no photo<span>{len(nophoto)} cards</span></a>'
    for f in os.listdir('.'):
        if re.match(rf'gross-anatomy-lab{n}-more\d+\.html$',f): os.remove(f)
    inbest=set(core+gaps); morelinks=''; mi=0; groups={}
    for ci,c in enumerate(cards):
        if ci in inbest or c['cls'] not in ('main','more'): continue
        groups.setdefault(c['name'],[]).append(c['html'])
    for nm,hs in groups.items():
        for i in range(0,len(hs),15):
            mi+=1; fn=f'gross-anatomy-lab{n}-more{mi}.html'; part=hs[i:i+15]
            label=nm+(f' ({i//15+1})' if len(hs)>15 else '')
            write(fn,f'Lab {n} · {label}',f'📚 More practice · not repeated in ⭐ · {len(part)} cards',part,css,hubf)
            morelinks+=f'<a href="{fn}?v={V}">{E(label)}<span>{len(part)} cards</span></a>'
    srcmark='<!--p3src:'+'|'.join(f'{cls}::{h}::{nm}' for cls,h,nm in pages if cls in ('main','more'))+'-->'
    main=f'<div class="sec main"><h2>⭐ ALL bold terms · start here</h2><p>Every bold term in one place: cadaver photos first (UMN, then your photos + course slides), then drawings/web photos for the few with no cadaver photo, then concept cards.</p>{links}{nplink}</div>'
    more=f'<div class="sec more" style="border-left:7px solid #b48ad6"><h2>📚 Supplemental · more practice</h2><p>Optional extra views of the same terms. Nothing here repeats ⭐.</p>{morelinks}{srcmark}</div>'
    hub=re.sub(r'<div class="sec nophoto".*?</div>','',hub,flags=re.S)
    mo=sec('more'); hub=hub.replace(sec('main').group(0),main,1)
    hub=hub.replace(mo.group(0),more,1) if mo else hub.replace(main,main+more,1)
    hub=re.sub(r'<!--(umn|mine)-->.*?<!--/\1-->','',hub,flags=re.S)
    open(hubf,'w').write(hub)
    print(n,'terms',len(T),'UMN',len(core),'gap fill',len(gaps),'no-photo',len(nophoto))
