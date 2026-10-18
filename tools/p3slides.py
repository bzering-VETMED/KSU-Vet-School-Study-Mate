"""Extract 'Title / Note:' course-slide PDFs (Labs 19-24) into highlight/clean pairs.
python3 tools/p3slides.py <pdf> <tag> <outdir>  -> outdir/<tag>.json + PNGs"""
import sys,os,json,re
import pymupdf,numpy as np
from PIL import Image,ImageFilter
def title_note(p):
    d=p.get_text('dict'); spans=[]
    for b in d['blocks']:
        for l in b.get('lines',[]):
            for s in l['spans']:
                if s['text'].strip(): spans.append(s)
    if not spans: return '',''
    big=max(s['size'] for s in spans)
    title=' '.join(s['text'].strip() for s in spans if s['size']>=big-0.6)
    txt=p.get_text()
    note=txt.split('Note:',1)[1] if 'Note:' in txt else ''
    note=re.sub(r'\s+',' ',note).strip()
    return re.sub(r'\s+',' ',title).strip(),note
def render(p,bbox,w):
    r=pymupdf.Rect(bbox)&p.rect; z=max(1,w/r.width)
    pm=p.get_pixmap(matrix=pymupdf.Matrix(z,z),clip=r)
    return np.frombuffer(pm.samples,np.uint8).reshape(pm.h,pm.w,pm.n)[:,:,:3].copy()
def sat(a):
    a=a.astype(int); mx=a.max(2); mn=a.min(2); return ((mx-mn)>90)&(mx>120)
def run(pdf,tag,out):
    d=pymupdf.open(pdf); pages=[]
    for i,p in enumerate(d):
        t,n=title_note(p); info=p.get_image_info()
        pages.append(dict(i=i,title=t,note=n,img=(max(info,key=lambda b:(b['bbox'][2]-b['bbox'][0])*(b['bbox'][3]-b['bbox'][1])) if info else None),nd=len(p.get_drawings())))
    groups=[]
    for pg in pages:
        if groups and groups[-1][0]['title']==pg['title'] and pg['img'] and groups[-1][0]['img'] and groups[-1][0]['img']['bbox']==pg['img']['bbox']: groups[-1].append(pg)
        else: groups.append([pg])
    items=[]
    for g in groups:
        t=g[0]['title']; note=max((x['note'] for x in g),key=len)
        if not g[0]['img']:
            items.append(dict(src=tag,page=g[0]['i']+1,title=t,note=note,clean=None,hl=[])); continue
        bb=g[0]['img']['bbox']; w=min(1800,max(g[0]['img']['width'],1000))
        arr=[render(d[x['i']],bb,w) for x in g]
        if len(g)==1:
            items.append(dict(src=tag,page=g[0]['i']+1,title=t,note=note,clean=None,hl=[save(arr[0],f'{out}/{tag}_{g[0]["i"]+1}.jpg')])); continue
        # clean = page whose render diff from the rest is lowest drawings count
        ci=min(range(len(g)),key=lambda k:(g[k]['nd'],sat(arr[k]).sum()))
        hl=[]
        for k in range(len(g)):
            if k==ci: continue
            if (np.abs(arr[k].astype(int)-arr[ci].astype(int)).max(2)>40).mean()<0.00005: continue
            hl.append(save(arr[k],f'{out}/{tag}_{g[k]["i"]+1}.jpg'))
        items.append(dict(src=tag,page=g[ci]['i']+1,title=t,note=note,clean=save(arr[ci],f'{out}/{tag}_{g[ci]["i"]+1}c.jpg'),hl=hl))
    json.dump(items,open(f'{out}/{tag}.json','w'),indent=0)
    print(tag,len(items),'items',sum(len(x['hl']) for x in items),'hl')
def save(a,fn):
    im=Image.fromarray(a).filter(ImageFilter.UnsharpMask(radius=2,percent=60,threshold=3))
    im.save(fn,quality=88); return fn
if __name__=='__main__': run(sys.argv[1],sys.argv[2],sys.argv[3])
