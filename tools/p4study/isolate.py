"""Keep ONLY one label on a PDF figure/photo page (made by Claude). The page is rebuilt from its parts:
the photo/drawing image(s), then just the kept label's own objects: its text, its circle, its arrow image(s)
and its leader line(s). Each small arrow image / line is given to the label it starts at."""
import pymupdf as fz, math
def _grow(r,t): return fz.Rect(r.x0-t,r.y0-t,r.x1+t,r.y1+t)
def _dist(r,pt):
    dx=max(r.x0-pt.x,0,pt.x-r.x1); dy=max(r.y0-pt.y,0,pt.y-r.y1); return math.hypot(dx,dy)
def _labels(p):
    """label = run of words on one text line with no big gap (so '1 2 3 4' spread along a row = separate labels)"""
    L={}
    for w in p.get_text('words'): L.setdefault((w[5],w[6]),[]).append(w)
    out=[]
    for ws in L.values():
        ws.sort(key=lambda w:w[0]); cur=None
        for w in ws:
            r=fz.Rect(w[:4])
            if cur and r.x0-cur['rect'].x1<=max(4.5,0.45*r.height): cur['rect']|=r; cur['text']+=' '+w[4]
            else: cur=dict(rect=r,text=w[4]); out.append(cur)
    return out
def isolate(pdf,pg,keep_rects,out,clip=None,dpi=170,pad=8,big_frac=0.2,reach=7):
    src=fz.open(pdf); p=src[pg-1]
    imgs=[(im[0],im[1],r) for im in p.get_images(full=True) for r in p.get_image_rects(im[0])]
    art=fz.Rect()
    for *_,r in imgs: art|=r
    A=max(1,art.width*art.height)
    big=[x for x in imgs if x[2].width*x[2].height>big_frac*A]; small=[x for x in imgs if x not in big]
    labs=_labels(p); keepR=[fz.Rect(r) for r in keep_rects]
    for l in labs: l['keep']=any(l['rect'].intersects(k) for k in keepR)
    # circles/ovals = drawings that contain a label's text; owner = that label
    drw=[d for d in p.get_drawings() if fz.Rect(d['rect']).width*fz.Rect(d['rect']).height<0.2*A]
    owner={}
    def nearest(pts,lim):
        """owner = label whose circle/text has the MOST of this object's points within lim (ties → closest)"""
        best=None
        for i,l in enumerate(labs):
            R=l['circ'] if 'circ' in l else l['rect']
            ds=[_dist(R,pt) for pt in pts]; n=sum(d<=lim for d in ds)
            if n and (best is None or (n,-min(ds))>best[0]): best=((n,-min(ds)),i)
        return best and best[1]
    circles=set()
    def circ_assign(key,dr):
        ins=[i for i,l in enumerate(labs) if dr.contains(fz.Point((l['rect'].x0+l['rect'].x1)/2,(l['rect'].y0+l['rect'].y1)/2)) and dr.width<l['rect'].width*4+40 and dr.height<l['rect'].height*4+30]
        if not ins: return False
        owner[key]=ins[0]; circles.add(key)
        for i in ins: labs[i]['circ']=labs[i].get('circ',fz.Rect(dr))|dr; labs[i]['grp']=ins
        return True
    for j,d in enumerate(drw): circ_assign(('d',j),fz.Rect(d['rect']))
    for j,(x,sm,r) in enumerate(small): circ_assign(('i',j),r)
    for j,d in enumerate(drw):
        if ('d',j) in owner: continue
        pts=[]
        for it in d['items']:
            pts+=[q for q in it[1:] if isinstance(q,fz.Point)]
            if it[0]=='re': r=it[1]; pts+=[r.tl,r.br,r.tr,r.bl]
            if it[0]=='qu': pts+=[it[1].ul,it[1].ur,it[1].ll,it[1].lr]
        i=nearest(pts,reach)
        if i is not None: owner[('d',j)]=i
    import numpy as np
    for j,(x,sm,r) in enumerate(small):
        if ('i',j) in owner: continue
        # opaque pixels of the arrow image, in page coordinates
        pts=[]
        try:
            mp=fz.Pixmap(src,sm) if sm else None
            if mp is not None:
                a=np.frombuffer(mp.samples,np.uint8).reshape(mp.height,mp.width,mp.n)[...,0]
                ys,xs=np.nonzero(a>128); step=max(1,len(xs)//400)
                pts=[fz.Point(r.x0+(xx+.5)/mp.width*r.width,r.y0+(yy+.5)/mp.height*r.height) for xx,yy in zip(xs[::step],ys[::step])]
        except Exception: pts=[]
        if not pts: pts=[r.tl,r.tr,r.bl,r.br]
        i=nearest(pts,reach)
        if i is not None: owner[('i',j)]=i
    for l in labs:
        if l['keep']:
            for g in l.get('grp',[]): labs[g]['keep']=True
    kept={k for k,i in owner.items() if labs[i]['keep']}
    # second hop: lines/arrows that start on a kept object (e.g. bracket → stem)
    for _ in range(2):
        kr=[fz.Rect(drw[k[1]]['rect']) if k[0]=='d' else small[k[1]][2] for k in kept if k not in circles]
        for j,d in enumerate(drw):
            if ('d',j) not in owner and ('d',j) not in kept and any(_grow(fz.Rect(d['rect']),1.5).intersects(r) for r in kr): kept.add(('d',j))
    box=fz.Rect(clip) if clip else fz.Rect(art)
    for l in labs:
        if l['keep']: box|=l['rect']; box|=l.get('circ',l['rect'])
    for k in kept: box|=fz.Rect(drw[k[1]]['rect']) if k[0]=='d' else small[k[1]][2]
    box=_grow(box,pad)&p.rect
    nd=fz.open(); q=nd.new_page(width=p.rect.width,height=p.rect.height)
    def put(x,sm,r):
        e=src.extract_image(x); kw={'mask':src.extract_image(sm)['image']} if sm else {}
        q.insert_image(r,stream=e['image'],keep_proportion=False,**kw)
    for x,sm,r in big: put(x,sm,r)
    for k in sorted(k for k in kept if k[0]=='i'): put(*small[k[1]])
    sh=q.new_shape()
    for k in sorted(k for k in kept if k[0]=='d'):
        d=drw[k[1]]
        for it in d['items']:
            if it[0]=='l': sh.draw_line(it[1],it[2])
            elif it[0]=='c': sh.draw_bezier(it[1],it[2],it[3],it[4])
            elif it[0]=='re': sh.draw_rect(it[1])
            elif it[0]=='qu': sh.draw_quad(it[1])
        sh.finish(color=d.get('color'),fill=d.get('fill'),width=d.get('width') or 1,closePath=d.get('closePath',False),even_odd=d.get('even_odd',False),fill_opacity=d.get('fill_opacity') or 1,stroke_opacity=d.get('stroke_opacity') or 1)
    sh.commit()
    for l in labs:
        if l['keep']: q.show_pdf_page(_grow(l['rect'],0.8),src,pg-1,clip=_grow(l['rect'],0.8))
    q.get_pixmap(dpi=dpi,clip=box).save(out)
    import json; json.dump({'box':list(box),'keep':[list(fz.Rect(r)) for r in keep_rects]},open(out+'.json','w'))
    return len(kept)
def find_rects(pdf,pg,text,within=None):
    p=fz.open(pdf)[pg-1]
    return [fz.Rect(w[:4]) for w in p.get_text('words') if w[4]==text and (within is None or fz.Rect(w[:4]).intersects(within))]
def find_phrase(pdf,pg,phrase,within=None):
    p=fz.open(pdf)[pg-1]
    return [r for r in p.search_for(phrase) if within is None or r.intersects(within)]
