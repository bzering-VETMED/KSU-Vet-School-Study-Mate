import sys,re,html,glob
sys.path.insert(0,'.')
import pymupdf as fz, gaiso
from iso import isolate
def letter_box(p,L,W=None):
    rs=[]
    for d in p.get_drawings():
        r=d['rect']; c=fz.Point((r.x0+r.x1)/2,(r.y0+r.y1)/2)
        if c in L and r.width<L.width+4 and r.height<L.height+5:
            if r.width>25 and r.width>3*max(r.height,1): continue      # pointer line, not a letter
            rs.append(r)
    if not rs: return None
    cys=[(r.y0+r.y1)/2 for r in rs]
    band=(W.y0+W.y1)/2 if W else max(cys,key=lambda c:sum(1 for y in cys if abs(y-c)<=9))
    import statistics
    mh=statistics.median([r.height for r in rs]) if rs else 0
    keep=[(r,cy) for r,cy in zip(rs,cys) if r.height<=max(1.8*mh,10)]
    rs=[r for r,_ in keep]; cys=[c for _,c in keep]
    if not rs: return None
    rs=[r for r,cy in zip(rs,cys) if abs(cy-band)<=11]
    rs.sort(key=lambda r:r.x0); cl=[[rs[0]]]
    for r in rs[1:]:
        if r.x0-max(x.x1 for x in cl[-1])>14: cl.append([r])
        else: cl[-1].append(r)
    def u(c):
        b=fz.Rect(c[0])
        for x in c[1:]: b|=x
        return b
    best=max(cl,key=lambda c:sum(x.width*x.height for x in c)+len(c)*10)
    # keep neighbouring clusters that are words of the same label (gap <= 14 already merged); also merge clusters within 30pt of best
    b=u(best)
    for c in cl:
        if c is best: continue
        cb=u(c)
        if cb.x1<b.x0 and b.x0-cb.x1<30 or cb.x0>b.x1 and cb.x0-b.x1<30: b|=cb
    return b
def boxes(fi,pg,term,anch):
    pdf=gaiso.FILES[fi]; p=fz.open(pdf)[pg-1]
    rs=gaiso.rects_for(p,anch)
    if not rs: return None
    isolate(pdf,pg,rs,p.rect,'/tmp/claude-0/-home-claude/31594bc3-9d6f-5c02-a55e-32953ff4d455/scratchpad/fb/_p.png',dpi=20,draw_text=False,grow=0,seed_pad=12,ink=True)
    kr=isolate.keep_rect
    photos=[fz.Rect(m['bbox']) for m in p.get_image_info() if fz.Rect(m['bbox']).get_area()>p.rect.get_area()*0.08]
    def score(b):
        if b.intersects(kr): return (b&kr).get_area()
        cx,cy=(kr.x0+kr.x1)/2,(kr.y0+kr.y1)/2; bx,by=(b.x0+b.x1)/2,(b.y0+b.y1)/2
        return -((cx-bx)**2+(cy-by)**2)
    ph=max(photos,key=score); clip=((ph|kr)+(-4,-4,4,4))&p.rect
    out=[]
    toks=[t for a in anch for t in re.findall(r'[a-z]{4,}',a.lower())]
    for L in rs:
        W=None; best=0
        for w in p.get_text('words'):
            wr=fz.Rect(w[:4]); wl=w[4].lower().strip('-~>Ss')
            if not wr.intersects(L): continue
            sc=max([len(t) for t in toks if t==w[4].lower().strip('-~>') or t in w[4].lower()]+[0])
            if sc>best or (sc==best and sc and W is not None and wr.height<W.height): best=sc; W=wr
        b=letter_box(p,L,W) or W or L
        b=b+(-3,-3,3,3)
        out.append(((b.x0-clip.x0)/clip.width,(b.y0-clip.y0)/clip.height,b.width/clip.width,b.height/clip.height))
    return out
# map term -> (fi,pg,anch) first entry (same order gaiso used)
first={}
for (fi,pg),items in gaiso.M.items():
    for t,a in items: first.setdefault(t,[]).append((fi,pg,a))
tot=0
for L in range(26,33):
    f=f'/home/claude/repo/p4-study-photos/lab{L}.html'; s=open(f).read()
    def fix(m):
        global tot
        card=m.group(0)
        if 'Gross Anatomy notes' not in card: return card
        name=html.unescape(re.search(r'<div class="n">(.*?)</div>',card).group(1)); term=name[0].lower()+name[1:]
        pg=int(re.search(r'Gross Anatomy notes( 2)? p(\d+)',card).group(2)); fi=1 if re.search(r'Gross Anatomy notes 2 p',card) else 0
        cand=[x for x in first.get(term,[]) if x[0]==fi and x[1]==pg]
        if not cand: print('?',L,term); return card
        bx=boxes(*cand[0][:2],term,cand[0][2])
        if not bx: print('nobox',term); return card
        spans=''.join(f'<span class="bl" style="left:{x*100:.2f}%;top:{y*100:.2f}%;width:{w*100:.2f}%;height:{h*100:.2f}%"></span>' for x,y,w,h in bx)
        tot+=1
        return re.sub(r'(<span class="bl"[^>]*></span>)+',spans,card,count=1) if '<span class="bl"' in card else card
    s=re.sub(r'<div class="t" id="t\d+".*?<div class="tap">',fix,s,flags=re.S)
    open(f,'w').write(s)
print('fixed',tot)
