"""Isolate ONE label on a vector-labeled PDF figure/photo (made by Claude for Bethany, Nov 16).
Renders the page with ALL vector labels/lines removed (raster art kept), then redraws only the target label
(its text + the circle/leader line/arrowhead chain touching it)."""
import pymupdf as fz, math
def _pts(dr):
    P=[]
    for it in dr['items']:
        for v in it[1:]:
            if isinstance(v,fz.Point): P.append(v)
            elif isinstance(v,fz.Rect): P+= [v.tl,v.tr,v.bl,v.br]
            elif isinstance(v,fz.Quad): P+= [v.ul,v.ur,v.ll,v.lr]
    return P
def _near(a,b,tol):
    ra,rb=a['rect']+(-tol,-tol,tol,tol),b['rect']
    if not ra.intersects(rb): return False
    pa,pb=_pts(a),_pts(b)
    small=lambda d:d['rect'].width<14 and d['rect'].height<14
    if small(a) and any(p in b['rect']+(-tol,-tol,tol,tol) for p in pb[:0]+pa): pass
    for p in pa:
        for q in pb:
            if abs(p.x-q.x)<tol and abs(p.y-q.y)<tol: return True
    # endpoint of a inside small shape b (arrowhead/circle) or vice versa
    if small(b) and any(p in rb+(-tol,-tol,tol,tol) for p in pa): return True
    if small(a) and any(q in a['rect']+(-tol,-tol,tol,tol) for q in pb): return True
    return False
def find_words(p,phrase,clip):
    kw=[w.lower() for w in phrase.split()]
    W=[w for w in p.get_text('words') if fz.Rect(w[:4]).intersects(clip)]
    for i in range(len(W)):
        if [x[4].lower() for x in W[i:i+len(kw)]]==kw or [x[4].lower().strip(',.') for x in W[i:i+len(kw)]]==[k.strip(',.') for k in kw]:
            return W[i:i+len(kw)]
    raise ValueError(f'label not found: {phrase}')
def isolate(pdf,pg,phrase,clip,out,dpi=170,tol=3.5,ring=False):
    src=fz.open(pdf); p=src[pg-1]
    phrases=phrase if isinstance(phrase,list) else [phrase]
    Ls=[]
    for ph in phrases:
        if isinstance(ph,fz.Rect): Ls.append(ph); continue
        words=find_words(p,ph,clip); r=fz.Rect(words[0][:4])
        for w in words[1:]: r|=fz.Rect(w[:4])
        Ls.append(r)
    draws=[d for d in p.get_drawings() if d['rect'].width<p.rect.width*0.9]
    # seeds: shapes containing the label (circle/box) or lines starting next to it
    seed=[i for i,d in enumerate(draws) if any((d['rect'].contains(L) and d['rect'].width<80 and d['rect'].height<80) or any(abs(q.x-L.x0)<6 or abs(q.x-L.x1)<6 for q in _pts(d) if L.y0-6<q.y<L.y1+6) or (d['rect'].width<p.rect.width*0.6 and any(q in L+(-14,-10,14,10) for q in _pts(d))) for L in Ls)]
    keep=set(seed); frontier=[(i,0) for i in seed]
    while frontier:
        i,dep=frontier.pop()
        if dep>=2: continue
        a=draws[i]
        for j,d in enumerate(draws):
            if j in keep: continue
            hit=_near(a,d,tol)
            if not hit and a['rect'].width<45 and a['rect'].height<45:      # label circle/box → arrow starting at its edge
                hit=any(q in a['rect']+(-tol,-tol,tol,tol) for q in _pts(d)) and d['rect'].width<p.rect.width*0.5
            if hit: keep.add(j); frontier.append((j,dep+1))
    from PIL import Image
    z=dpi/72; W,H=int(p.rect.width*z),int(p.rect.height*z)
    canvas=Image.new('RGB',(W,H),'white')
    for m in p.get_image_info(xrefs=True):
        if not m['xref'] or fz.Rect(m['bbox']).get_area()<p.rect.get_area()*0.08: continue
        info=src.extract_image(m['xref']); pm=fz.Pixmap(src,m['xref'])
        if pm.alpha: pm=fz.Pixmap(pm,0)
        if pm.n!=3: pm=fz.Pixmap(fz.csRGB,pm)
        im=Image.frombytes('RGB',(pm.width,pm.height),pm.samples)
        if info.get('smask'):
            mk=fz.Pixmap(src,info['smask'])
            if mk.n!=1: mk=fz.Pixmap(fz.csGRAY,mk)
            mi=Image.frombytes('L',(mk.width,mk.height),mk.samples).resize(im.size); im.putalpha(mi)
        b=fz.Rect(m['bbox']); im=im.resize((max(1,int(b.width*z)),max(1,int(b.height*z))))
        canvas.paste(im,(int(b.x0*z),int(b.y0*z)),im if im.mode=='RGBA' else None)
    ov=fz.open(); tp=ov.new_page(width=p.rect.width,height=p.rect.height)
    sh=tp.new_shape()
    for j in sorted(keep, key=lambda j:draws[j].get('seqno',0)):
        d=draws[j]
        for it in d['items']:
            k=it[0]
            if k=='l': sh.draw_line(it[1],it[2])
            elif k=='c': sh.draw_bezier(it[1],it[2],it[3],it[4])
            elif k=='re': sh.draw_rect(it[1])
            elif k=='qu': sh.draw_quad(it[1])
        sh.finish(color=d.get('color'),fill=d.get('fill'),width=d.get('width') or 1,closePath=d.get('closePath',False),
                  fill_opacity=d.get('fill_opacity') or 1,stroke_opacity=d.get('stroke_opacity') or 1,lineCap=max(d.get('lineCap') or (0,)) if isinstance(d.get('lineCap'),tuple) else (d.get('lineCap') or 0),even_odd=d.get('even_odd',False))
    sh.commit()
    for b in p.get_text('dict')['blocks']:
        for ln in b.get('lines',[]):
            for s in ln['spans']:
                if any(fz.Rect(s['bbox']).intersects(L) for L in Ls) and s['text'].strip():
                    c=s['color']; col=((c>>16&255)/255,(c>>8&255)/255,(c&255)/255)
                    tp.insert_text(fz.Point(s['origin']),s['text'],fontsize=s['size'],color=col,fontname='helv')
    opm=tp.get_pixmap(dpi=dpi,alpha=True)
    oi=Image.frombytes('RGBA',(opm.width,opm.height),opm.samples).resize((W,H))
    canvas.paste(oi,(0,0),oi)
    if ring:
        from PIL import ImageDraw
        dr=ImageDraw.Draw(canvas)
        for L in Ls:
            cx,cy=(L.x0+L.x1)/2*z,(L.y0+L.y1)/2*z; rr=max(L.width,L.height)/2*z+14*z/1.8
            for k in range(int(4*z/1.8)+2): dr.ellipse([cx-rr-k,cy-rr-k,cx+rr+k,cy+rr+k],outline=(217,79,127))
    pass
    canvas.crop((int(clip.x0*z),int(clip.y0*z),int(clip.x1*z),int(clip.y1*z))).save(out)
    boxes=[]
    for L in Ls:
        sp=[fz.Rect(s['bbox']) for b in p.get_text('dict')['blocks'] for ln in b.get('lines',[]) for s in ln['spans'] if fz.Rect(s['bbox']).intersects(L) and s['text'].strip()]
        R=fz.Rect(L)
        for r in sp: R|=r
        R=R+(-3,-2,3,2)
        boxes.append(((R.x0-clip.x0)/clip.width,(R.y0-clip.y0)/clip.height,R.width/clip.width,R.height/clip.height))
    isolate.boxes=boxes
    return len(keep)
