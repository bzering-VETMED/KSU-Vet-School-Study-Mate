"""One-label image from the labeled-photo notes PDFs (made by Claude, Nov 23)."""
import sys,re,os; sys.path.insert(0,'/home/claude/studysheets')
import pymupdf as fz
from iso import isolate
from gamap import M,NOTE
FILES=['/mnt/user-data/uploads/Gross_Anatomy_1.pdf','/mnt/user-data/uploads/Gross_Anatomy_1_2.pdf']
OUT='/home/claude/studysheets/single/ga/'; os.makedirs(OUT,exist_ok=True)
def lines(p):
    """OCR lines; rect = union of real word boxes only (drops '-', '~', '>' strokes the OCR glued on)."""
    by={}
    for w in p.get_text('words'):
        by.setdefault((w[5],w[6]),[]).append(w)
    out=[]
    for k,ws in sorted(by.items()):
        tx=' '.join(w[4] for w in ws)
        good=[w for w in ws if sum(ch.isalpha() for ch in w[4])>=2]
        if not good: continue
        r=fz.Rect(good[0][:4])
        for w in good[1:]: r|=fz.Rect(w[:4])
        out.append((tx,r))
    return out
def rects_for(p,anchors):
    ls=lines(p); rs=[]
    for a in anchors:
        for tx,r in ls:
            t=re.sub(r'\s+',' ',tx.lower()); a2=re.sub(r'\s+',' ',a.lower())
            if (a2.startswith('=') and t.strip(' -') == a2[1:].strip(' -')) or (not a2.startswith('=') and a2 in t):
                if r not in rs: rs.append(r)
                break
    return rs
def make(fi,pg,term,anchors):
    pdf=FILES[fi]; d=fz.open(pdf); p=d[pg-1]
    rs=rects_for(p,anchors)
    if not rs: return None
    tmp=OUT+'_probe.png'
    isolate(pdf,pg,rs,p.rect,tmp,dpi=20,draw_text=False,grow=0,seed_pad=12,ink=True)
    kr=isolate.keep_rect
    photos=[fz.Rect(m['bbox']) for m in p.get_image_info() if fz.Rect(m['bbox']).get_area()>p.rect.get_area()*0.08]
    if not photos: return None
    lines_r=fz.Rect()
    for b in [kr]: lines_r|=b
    def score(b):
        if b.intersects(kr): return (b&kr).get_area()
        cx,cy=(kr.x0+kr.x1)/2,(kr.y0+kr.y1)/2; bx,by=(b.x0+b.x1)/2,(b.y0+b.y1)/2
        return -((cx-bx)**2+(cy-by)**2)
    ph=max(photos,key=score)
    if isolate.n_lines==0 and not (ph+(-15,-15,15,15)).intersects(kr): return None   # label floating with no pointer -> don't use
    clip=(ph|kr)+(-4,-4,4,4); clip&=p.rect
    out=f'{OUT}F{fi}p{pg}_{re.sub(r"[^a-z0-9]+","_",term)}.png'
    isolate(pdf,pg,rs,clip,out,dpi=260,draw_text=False,grow=0,seed_pad=12,ink=True)
    return dict(img=out,boxes=isolate.boxes,cue='the one handwritten label on the photo (blurred)',tag='📷 labeled lab photo · Gross Anatomy notes'+(' 2' if fi else '')+f' p{pg}',note=NOTE.get(term))
def available():
    out={}
    for (fi,pg),items in M.items():
        for term,anch in items: out.setdefault(term,[]).append((fi,pg,anch))
    return out
