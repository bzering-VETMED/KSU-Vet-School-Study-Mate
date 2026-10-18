"""Find + erase label words that survived on Practical 3 QUESTION images (made by Claude).
OCR at 0/±45/90° in both polarities (catches white rotated labels like 'Cortex'), keeps orientation tags,
inpaints ONLY the letter strokes inside each word box (no boxes, no blur). Answer images are never touched.
  python3 tools/p3leakfix.py            # scan + fix every image used by Lab 16–25 deck pages
  python3 tools/p3leakfix.py --dry      # report only"""
import sys,glob,re,os,json
from multiprocessing import Pool
import cv2,numpy as np,pytesseract
from PIL import Image
KEEP={'rostral','cranial','caudal','dorsal','ventral','medial','lateral','left','right','proximal','distal','crania','dorsa','nial','ventra','cranial','caud','lateral','medial','anterior','posterior'}
def words(gray):
    H,W=gray.shape; out=[]
    for ang in (0,45,-45,60,-60,90):
        M=cv2.getRotationMatrix2D((W/2,H/2),ang,1.0); c,s=abs(M[0,0]),abs(M[0,1])
        nW,nH=int(H*s+W*c),int(H*c+W*s); M[0,2]+=nW/2-W/2; M[1,2]+=nH/2-H/2
        r=cv2.warpAffine(gray,M,(nW,nH),borderValue=128); Mi=cv2.invertAffineTransform(M)
        for img in (r,255-r):
            d=pytesseract.image_to_data(img,config='--psm 11',output_type=pytesseract.Output.DICT)
            for i,t in enumerate(d['text']):
                t=t.strip()
                if not re.fullmatch(r'[A-Za-z]{4,}',t) or float(d['conf'][i])<80 or t.lower() in KEEP: continue
                x,y,w,h=d['left'][i],d['top'][i],d['width'][i],d['height'][i]
                pts=np.array([[x-4,y-4],[x+w+4,y-4],[x+w+4,y+h+4],[x-4,y+h+4]],float)
                pts=(Mi[:,:2]@pts.T).T+Mi[:,2]
                out.append((t,pts.astype(np.int32)))
    return out
def fix(path,dry=False):
    im=cv2.imread(path)
    if im is None: return path,[]
    scale=1.0; g=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    if max(g.shape)>1500: scale=1500/max(g.shape); g=cv2.resize(g,None,fx=scale,fy=scale)
    ws=words(g)
    if not ws or dry: return path,[w for w,_ in ws]
    mask=np.zeros(im.shape[:2],np.uint8); G=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY).astype(int)
    for _,pts in ws:
        poly=np.zeros_like(mask); cv2.fillPoly(poly,[(pts/scale).astype(np.int32)],255)
        sel=poly>0
        if not sel.any(): continue
        vals=G[sel]; med=np.median(vals)
        # letters = the minority tone in the box (white text on tissue or dark text on light)
        lo,hi=np.percentile(vals,15),np.percentile(vals,85)
        txt=(G>=hi-5) if (hi-med)>(med-lo) else (G<=lo+5)
        mask[sel&txt]=255
    mask=cv2.dilate(mask,np.ones((3,3),np.uint8),iterations=2)
    cv2.imwrite(path,cv2.inpaint(im,mask,5,cv2.INPAINT_TELEA),[cv2.IMWRITE_JPEG_QUALITY,90])
    return path,[w for w,_ in ws]
def question_images():
    from bs4 import BeautifulSoup
    S=set()
    for f in glob.glob('gross-anatomy-lab1[6-9]-*.html')+glob.glob('gross-anatomy-lab2[0-5]-*.html'):
        if f.endswith('-images.html'): continue
        for im in BeautifulSoup(open(f).read(),'html.parser').select('.pic img'):
            p=im['src'].split('?')[0]
            if p.startswith('assets/') and os.path.exists(p): S.add(p)
    return sorted(S)
if __name__=='__main__':
    dry='--dry' in sys.argv
    files=[a for a in sys.argv[1:] if not a.startswith('--')] or question_images()
    from functools import partial
    print(len(files),'images',flush=True)
    with Pool(os.cpu_count()) as P:
        for p,w in P.imap_unordered(partial(fix,dry=dry),files):
            if w: print(p[7:],sorted(set(w)),flush=True)
