"""Abdomen.pdf (labeled course slides): remove PDF-text labels, drop numbered tags in their place.
Non-bold labels: text + touching box/arrow removed, no number. Orientation tags kept.
python3 tools/p3abd.py <Abdomen.pdf> <outdir>  -> outdir/abd.json"""
import sys,re,json,pymupdf
from PIL import Image,ImageDraw,ImageFont,ImageFilter
ORIENT={'cranial','caudal','dorsal','ventral','left','right','medial','lateral','rostral'}
def labels(p):
    bl=[b for b in p.get_text('dict')['blocks'] if 'lines' in b]
    L=[]
    for ln in [l for b in bl for l in b['lines']]:
        t=' '.join(s['text'] for s in ln['spans']).strip()
        if not t: continue
        r=pymupdf.Rect(ln['bbox'])
        for g in L:
            if abs(r.y0-g['r'].y1)<9 and min(r.x1,g['r'].x1)-max(r.x0,g['r'].x0)>0 and (t[0].islower() or (g['t'].startswith(('•','*')) is False and g['t'].count('•')>0) or t[0]=='(' or g['t'].rstrip().endswith((' of',' Of',' the',','))):
                g['r']|=r; g['t']+=' '+t; break
        else: L.append(dict(r=r,t=t))
    for g in L: g['t']=re.sub(r'\s+',' ',g['t']).strip()
    return L
def run(pdf,out,keep):
    """keep(page_no, label_text) -> True if bold"""
    d=pymupdf.open(pdf); items=[]
    for i in range(len(d)):
        p=d[i]; z=2.5; M=pymupdf.Matrix(z,z)
        a=p.get_pixmap(matrix=M); a.save(f'{out}/abd_{i+1}a.png')
        L=labels(p); tags=[]; notes=[]
        for g in L:
            if g['t'].lower().strip(' .') in ORIENT: continue
            if len(g['t'])>70 or g['t'].startswith('•') or g['t'].startswith('*'): notes.append(g['t']); kind='note'
            else: kind='b' if keep(i+1,g['t']) else 'x'
            p.add_redact_annot(g['r']+(-1,-1,1,1),fill=False)
            g['k']=kind
        p.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE,graphics=pymupdf.PDF_REDACT_LINE_ART_NONE,text=pymupdf.PDF_REDACT_TEXT_REMOVE)
        # remove white boxes of non-bold/note labels by repainting from... simpler: draw over with image pixels is not possible; leave box blank
        im=Image.frombytes('RGB',(p.get_pixmap(matrix=M).w,p.get_pixmap(matrix=M).h),p.get_pixmap(matrix=M).samples)
        dr=ImageDraw.Draw(im); n=0
        try: F=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',44)
        except: F=ImageFont.load_default()
        for g in L:
            if g.get('k')!='b': continue
            n+=1; cx=(g['r'].x0+g['r'].x1)/2*z; cy=(g['r'].y0+g['r'].y1)/2*z; R=34
            dr.ellipse((cx-R,cy-R,cx+R,cy+R),fill=(217,79,127),outline='white',width=4)
            dr.text((cx,cy),str(n),fill='white',font=F,anchor='mm'); tags.append((n,g['t']))
        im=im.filter(ImageFilter.UnsharpMask(2,50,3)); im.save(f'{out}/abd_{i+1}q.jpg',quality=88)
        Image.open(f'{out}/abd_{i+1}a.png').convert('RGB').filter(ImageFilter.UnsharpMask(2,50,3)).save(f'{out}/abd_{i+1}a.jpg',quality=88)
        items.append(dict(page=i+1,tags=tags,notes=notes,skipped=[g['t'] for g in L if g.get('k')=='x']))
    json.dump(items,open(f'{out}/abd.json','w'),indent=0)
    return items
if __name__=='__main__':
    for x in run(sys.argv[1],sys.argv[2],lambda pg,t:True): print(x)
