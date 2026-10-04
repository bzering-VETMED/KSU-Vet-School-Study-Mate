"""Detect lab-guide figures in a notes PDF, extract labels (vector text) + leader lines."""
import pymupdf as fz, json, sys, re

def is_label_span(s):
    f=s['font']; return ('Helvetica' in f or 'Arial' in f) and s['size']<=9.6

def rect_union(a,b): return fz.Rect(a)|fz.Rect(b)

def page_figs(page):
    imgs=[fz.Rect(i['bbox']) for i in page.get_image_info() if fz.Rect(i['bbox']).width>60 and fz.Rect(i['bbox']).height>60]
    # label lines
    lines=[]
    for b in page.get_text('dict')['blocks']:
        if b['type']: continue
        for l in b['lines']:
            sp=[s for s in l['spans'] if s['text'].strip()]
            if sp and all(is_label_span(s) for s in sp):
                lines.append({'bbox':fz.Rect(l['bbox']),'text':''.join(s['text'] for s in sp).strip()})
    caps=[]
    for b in page.get_text('dict')['blocks']:
        if b['type']: continue
        t=' '.join(''.join(s['text'] for s in l['spans']) for l in b['lines']).strip()
        if re.match(r'Fig\.\s*\d',t): caps.append({'bbox':fz.Rect(b['bbox']),'text':t})
    segs=[]
    for d in page.get_drawings():
        r=fz.Rect(d['rect'])
        if r.y1<50: continue
        for it in d['items']:
            if it[0]=='l': segs.append((it[1],it[2],d.get('color')))
    figs=[]
    used=set()
    for im in imgs:
        box=fz.Rect(im); members=[]
        changed=True
        while changed:
            changed=False
            ex=fz.Rect(box.x0-6,box.y0-6,box.x1+6,box.y1+6)
            for (p1,p2,c) in segs:
                sr=fz.Rect(p1,p2).normalize()
                if sr.width<0.5 and sr.height<0.5: continue
                inside = sr.x0>=box.x0 and sr.y0>=box.y0 and sr.x1<=box.x1 and sr.y1<=box.y1
                if (ex.contains(p1) or ex.contains(p2)) and not inside:
                    box=fz.Rect(min(box.x0,sr.x0),min(box.y0,sr.y0),max(box.x1,sr.x1),max(box.y1,sr.y1)); changed=True
            for i,l in enumerate(lines):
                if i in used: continue
                if ex.intersects(l['bbox']):
                    box|=l['bbox']; used.add(i); members.append(i); changed=True
        figs.append({'box':box,'imgs':[im],'labels':members})
    # merge overlapping figs
    merged=True
    while merged:
        merged=False
        for a in range(len(figs)):
            for b in range(a+1,len(figs)):
                if figs[a]['box'].intersects(figs[b]['box']):
                    figs[a]['box']|=figs[b]['box']; figs[a]['imgs']+=figs[b]['imgs']; figs[a]['labels']+=figs[b]['labels']; figs.pop(b); merged=True; break
            if merged: break
    # caption: nearest caption below (or overlapping)
    for f in figs:
        best=None
        for c in caps:
            if c['bbox'].y0>=f['box'].y1-20 and c['bbox'].x0<f['box'].x1 and c['bbox'].x1>f['box'].x0:
                dy=c['bbox'].y0-f['box'].y1
                if best is None or dy<best[0]: best=(dy,c)
        f['caption']=best[1]['text'] if best and best[0]<60 else ''
        # group label lines into labels
        L=[lines[i] for i in f['labels']]
        L.sort(key=lambda l:(l['bbox'].y0,l['bbox'].x0))
        groups=[]
        for l in L:
            placed=False
            for g in groups:
                last=g[-1]['bbox']
                gap=l['bbox'].y0-last.y1
                xov=min(l['bbox'].x1,last.x1)-max(l['bbox'].x0,last.x0)
                aligned=abs(l['bbox'].x0-last.x0)<4 or abs(l['bbox'].x1-last.x1)<4 or abs((l['bbox'].x0+l['bbox'].x1)/2-(last.x0+last.x1)/2)<4
                if -1<gap<2.5 and xov>0 and aligned:
                    g.append(l); placed=True; break
            if not placed: groups.append([l])
        labs=[]
        for g in groups:
            r=fz.Rect(g[0]['bbox'])
            for l in g[1:]: r|=l['bbox']
            txt=' '.join(x['text'] for x in g)
            txt=re.sub(r'-\s+(?=[a-z])','',txt)  # dehyphenate
            txt=re.sub(r'\s+',' ',txt).strip()
            labs.append({'rect':list(r),'lines':[list(x['bbox']) for x in g],'text':txt})
        f['labs']=labs
    return figs

def run(pdf):
    d=fz.open(pdf); out=[]
    for pn,p in enumerate(d):
        for i,f in enumerate(page_figs(p)):
            out.append({'page':pn,'box':list(f['box']),'caption':f['caption'],'labels':f['labs']})
    return out

if __name__=='__main__':
    res=run(sys.argv[1])
    for k,f in enumerate(res):
        print(k,'p',f['page'],[round(v) for v in f['box']],f['caption'][:70])
        print('   ',' / '.join(l['text'] for l in f['labels']))
    json.dump(res,open(sys.argv[2],'w'),indent=1)

# ---------- rendering (lab-guide figures with vector labels) ----------
from PIL import Image, ImageDraw, ImageFont
KEEP_RE=re.compile(r'^(dorsal|ventral|cranial|caudal|rostral|medial|lateral|proximal|distal|left|right|[A-Z]|[TCLS]-?\s?\d+|[TCLS]-?I+|LV|RV|\d+[a-z]?|[LR]B\d.*|[LR]PB)$',re.I)
def keep_label(t): return bool(KEEP_RE.match(t.strip().rstrip(':')))
def render(pdf,fig,out_q,out_a,numbered,dpi=300,pad=6):
    """numbered: list of (number,label_index). Erases ALL non-kept label text (letter strokes only,
    via PDF text redaction: images + line art untouched), then draws number badges at the label spots."""
    box=fz.Rect(fig['box']); box=fz.Rect(box.x0-pad,box.y0-pad,box.x1+pad,box.y1+pad)
    d=fz.open(pdf); p=d[fig['page']]; box&=p.rect
    p.get_pixmap(clip=box,dpi=dpi).save(out_a.replace('.jpg','.png'))
    keepset={tuple(round(v) for v in ln) for lab in fig['labels'] if keep_label(lab['text']) and not lab.get('quiz') for ln in lab['lines']}
    for b in p.get_text('dict')['blocks']:
        if b['type']: continue
        for l in b['lines']:
            sp=[s for s in l['spans'] if s['text'].strip()]
            if not sp or not all(is_label_span(s) for s in sp): continue
            r=fz.Rect(l['bbox'])
            if not r.intersects(box) or tuple(round(v) for v in r) in keepset: continue
            if keep_label(''.join(s['text'] for s in sp).strip()) and not any(tuple(round(v) for v in fz.Rect(ln))==tuple(round(v) for v in r) for lab in fig['labels'] if lab.get('quiz') for ln in lab['lines']): continue
            p.add_redact_annot(r,fill=False)
    p.apply_redactions(images=fz.PDF_REDACT_IMAGE_NONE,graphics=fz.PDF_REDACT_LINE_ART_NONE,text=fz.PDF_REDACT_TEXT_REMOVE)
    p.get_pixmap(clip=box,dpi=dpi).save(out_q.replace('.jpg','.png'))
    S=dpi/72
    for src in (out_a,out_q):
        Image.open(src.replace('.jpg','.png')).convert('RGB').save(src,quality=88); os.remove(src.replace('.jpg','.png'))
    im=Image.open(out_q); dr=ImageDraw.Draw(im)
    try: font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',int(11*S))
    except: font=ImageFont.load_default()
    pts=[]
    for dd in fz.open(pdf)[fig['page']].get_drawings():
        for it in dd['items']:
            if it[0]=='l': pts+= [it[1],it[2]]
    def anchor(r):
        best=None
        for q in pts:
            dx=max(r.x0-q.x,0,q.x-r.x1); dy=max(r.y0-q.y,0,q.y-r.y1); dist=(dx*dx+dy*dy)**.5
            if dist<6 and (best is None or dist<best[0]): best=(dist,q)
        if not best: return (r.x0+r.x1)/2,(r.y0+r.y1)/2
        q=best[1]; R0=9.5
        # push badge just outside the line end, toward the label
        cx=min(max(q.x,r.x0+R0),r.x1-R0) if r.width>2*R0 else (r.x0+r.x1)/2
        cy=min(max(q.y,r.y0+R0*0.6),r.y1-R0*0.6) if r.height>1.2*R0 else (r.y0+r.y1)/2
        if q.x<=r.x0+1: cx=r.x0+R0
        elif q.x>=r.x1-1: cx=r.x1-R0
        return cx,cy
    for num,li in numbered:
        r=fz.Rect(fig['labels'][li]['rect']); cx,cy=anchor(r); cx-=box.x0; cy-=box.y0
        cx*=S; cy*=S; R=int(9.5*S)
        dr.ellipse([cx-R,cy-R,cx+R,cy+R],fill=(81,40,136),outline=(255,255,255),width=int(1.2*S))
        dr.text((cx,cy),str(num),fill='white',font=font,anchor='mm')
    im.save(out_q,quality=88)
import os
