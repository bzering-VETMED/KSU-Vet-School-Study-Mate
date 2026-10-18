"""Practical 3 hubs (Labs 16-24): ⭐ blocks keep ONLY cards built around THAT lab's bold terms
(slides: ≥1 bold item; UMN photos: ≥2 bold items or ≥40% of the numbered items).
Every other card moves to a twin page '<page>s.html' listed under 📚 Supplemental in the hub.
Run after p3labs.py / umn.py / lab16me.py AND p3simplify.py, then p3check.py:
  python3 tools/p3split.py 16 17 18 19 21 22 23 24"""
import sys,os,re,time,html
sys.path.insert(0,'tools')
from bs4 import BeautifulSoup
import p3shots as SH,p3bold
from deck import page
V=str(int(time.time())); E=html.escape
AB={'a':'artery','aa':'arteries','v':'vein','vv':'veins','n':'nerve','nn':'nerves','m':'muscle','mm':'muscles','lig':'ligament','gb':'gallbladder','br':'branch','rt':'right','lt':'left','cr':'cranial','cd':'caudal','azygous':'azygos'}
def norm(t):
    out=[]
    for w in re.findall(r'[a-z0-9]+',t.lower()):
        w=AB.get(w,w)
        if len(w)>4 and w.endswith('s') and not w.endswith(('ss','us','is')): w=w[:-1]
        if w=='arterie': w='artery'
        if w in('the','of','and'): continue
        out.append(w)
    return out
def has(h,n): return bool(n) and any(h[i:i+len(n)]==n for i in range(len(h)-len(n)+1))
def terms(n):
    if n in(16,17,18):
        T=[]
        for t,al in {16:SH.S16,17:SH.S17,18:SH.S18}[n]:
            T.append([('='+t) if t in SH.EXACT else t]+al)
        return T
    return [[t]+al for t,al,_ in p3bold.P3BOLD[n]]
def items(a):
    a=re.sub(r'#(\d+)\s',r'\1 · ',a)
    parts=[p.strip(' ·') for p in re.split(r'\s·\s',a) if p.strip(' ·')]
    out=[];i=0
    while i<len(parts):
        if re.fullmatch(r'(\d+[a-z]?|(double |long |short |white |unnumbered )?arrows?(head)?|(double )?asterisks?|probe|forceps)',parts[i].lower()) and i+1<len(parts):
            out.append(parts[i+1]); i+=2
        else: out.append(parts[i]); i+=1
    return out
def item_bold(item,T):
    forms=[norm(re.sub(r'\(.*?\)','',item)),norm(item)]
    forms+=[[('artery' if t=='vessel' else t) for t in f] for f in forms]+[[('vein' if t=='vessel' else t) for t in f] for f in forms]
    for als in T:
        for a in als:
            for A in (norm(a.lstrip('=')),norm(re.sub(r'\(.*?\)','',a.lstrip('=')))):
                if not A: continue
                for w in forms:
                    if not w: continue
                    if w==A or (len(A)>=2 and has(w,A)): return True
                    if len(A)==1 and not a.startswith('=') and (w[:1]==A or (A[0] in w and len(w)<=3)): return True
    return False
def is_star(card,T):
    it=items(answer_text(card)); b=sum(item_bold(x,T) for x in it)
    umn='🌐' in card.get_text()[:400] or 'UMN' in (card.select_one('.tagline').get_text() if card.select_one('.tagline') else '')
    if umn: return b>=1 and (b>=2 or b/max(len(it),1)>=0.4)
    return b>=1
def answer_text(card):
    nm=card.select('.nm')
    if nm: return ' · '.join(x.get_text(' ',strip=True) for x in nm)
    an=card.select('.an')
    return an[0].get_text(' ',strip=True) if an else card.get_text(' ',strip=True)
for n in map(int,sys.argv[1:]):
    T=terms(n); hubf=f'gross-anatomy-lab{n}-images.html'; hub=open(hubf).read()
    m=re.search(r'<div class="sec more"[^>]*>(.*?)</div>',hub,re.S) or re.search(r'<div class="sec main">(.*?)</div>',hub,re.S)   # after p3best the decks live in 📚 More practice
    links=re.findall(r'<a href="([^"?]+)[^"]*">([^<]*)<span>[^<]*</span></a>',m.group(1))
    supp=[]; newmain=m.group(1); moved=kept=0
    for href,name in links:
        if not os.path.exists(href): continue
        s=BeautifulSoup(open(href).read(),'html.parser'); cards=s.select('section.card')
        bad=[c for c in cards if not is_star(c,T)]
        if not bad:
            kept+=len(cards); tw=href.replace('.html','s.html')
            if os.path.exists(tw):   # moved on an earlier run (page not rebuilt since) → keep listing it
                supp.append((tw,f'{name.strip()} · supplemental',open(tw).read().count('<section class="card')))
            continue
        good=[c for c in cards if c not in bad]; moved+=len(bad); kept+=len(good)
        twin=href.replace('.html','s.html')
        bh=''.join(str(c) for c in bad).replace('class="card on"','class="card"')
        bh=bh.replace('class="card"','class="card on"',1)
        css=s.find('style').string or ''
        title=f'Lab {n} · {name.strip()} · 📚 supplemental'
        pg=page(title,f'📚 Supplemental (no bold terms) · {len(bad)} cards',bh,back=f'{hubf}?v={V}')
        pg=re.sub(r'<style>.*?</style>',lambda _:f'<style>{css}</style>',pg,count=1,flags=re.S)
        open(twin,'w').write(pg)
        supp.append((twin,f'{name.strip()} · supplemental',len(bad)))
        for c in bad: c.decompose()
        lnk=re.search(r'<a href="'+re.escape(href)+r'[^"]*">[^<]*<span>[^<]*</span></a>',newmain).group(0)
        if good:
            for c in s.select('section.card'): c['class']=['card']
            s.select('section.card')[0]['class']=['card','on']
            h1=s.find(class_='hero')
            if h1 and h1.p: h1.p.string=re.sub(r'\d+ cards',f'{len(good)} cards',h1.p.get_text())
            open(href,'w').write(str(s))
            newmain=newmain.replace(lnk,re.sub(r'<span>\d+ cards',f'<span>{len(good)} cards',re.sub(r'\?v=\d+',f'?v={V}',lnk)))
        else:
            newmain=newmain.replace(lnk,'')
    hub=hub.replace(m.group(1),newmain,1)
    hub=re.sub(r'<!--supp-->.*?<!--/supp-->','',hub,flags=re.S)
    if supp:
        sl='<!--supp-->'+''.join(f'<a href="{f}?v={V}">{E(t)}<span>{k} cards</span></a>' for f,t,k in supp)+'<!--/supp-->'
        if '<div class="sec extra">' in hub:
            hub=re.sub(r'<div class="sec extra"><h2>[^<]*</h2><p>[^<]*</p>',lambda x:x.group(0)+sl,hub,count=1)
        else:
            hub=hub.replace('<div class="sec terms">',f'<div class="sec extra"><h2>📚 Supplemental</h2><p></p>{sl}</div><div class="sec terms">',1)
        hub=re.sub(r'<div class="sec extra"><h2>[^<]*</h2><p>[^<]*</p>','<div class="sec extra"><h2>📚 Supplemental · extra study</h2><p>No bold terms here. Optional extra views + other structures.</p>',hub,count=1)
    open(hubf,'w').write(hub)
    print(n,'kept ⭐',kept,'moved 📚',moved,'supp pages',len(supp))
