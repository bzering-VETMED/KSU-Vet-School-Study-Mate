"""Erase every UMN number pointer except the target (white disk + digits + its black arrow), inpaint (made by Claude)."""
import cv2, numpy as np, pytesseract, math
def disks(img):
    g=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY); hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    cand=[]
    c=cv2.HoughCircles(cv2.medianBlur(g,3),cv2.HOUGH_GRADIENT,dp=1,minDist=25,param1=120,param2=20,minRadius=11,maxRadius=42)
    for x,y,r in (c[0] if c is not None else []): cand.append((int(x),int(y),int(r)))
    white=((hsv[...,1]<45)&(hsv[...,2]>205)).astype(np.uint8)*255
    n,lab,st,cen=cv2.connectedComponentsWithStats(cv2.morphologyEx(white,cv2.MORPH_CLOSE,np.ones((5,5),np.uint8)))
    for i in range(1,n):
        x,y,w,h,a=st[i]
        if 20<=w<=88 and 20<=h<=88 and 0.75<w/h<1.33: cand.append((x+w//2,y+h//2,max(w,h)//2))
    out=[]
    for x,y,r in cand:
        m=np.zeros(g.shape,np.uint8); cv2.circle(m,(x,y),max(3,int(r*0.85)),1,-1)
        wh=((hsv[...,1]<45)&(hsv[...,2]>200))[m>0].mean(); dk=(g<100)[m>0].mean()
        if wh>0.5 and 0.03<dk<0.45 and not any(math.hypot(x-a,y-b)<max(r,c)*0.8 for a,b,c in out): out.append((x,y,r))
    return out
def read(img,d):
    x,y,r=d; g=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    roi=g[max(0,y-r):y+r,max(0,x-r):x+r].copy(); mm=np.zeros(roi.shape,np.uint8); cv2.circle(mm,(roi.shape[1]//2,roi.shape[0]//2),int(r*0.82),255,-1)
    roi[mm==0]=255
    best=''
    for th in (110,140,170):
        b=cv2.threshold(cv2.resize(roi,None,fx=5,fy=5,interpolation=cv2.INTER_CUBIC),th,255,cv2.THRESH_BINARY)[1]
        b=cv2.copyMakeBorder(b,30,30,30,30,cv2.BORDER_CONSTANT,value=255)
        for psm in (8,10,7):
            t=pytesseract.image_to_string(b,config=f'--psm {psm} -c tessedit_char_whitelist=0123456789').strip()
            if t: return t
    return best
def arrow(img,d):
    x,y,r=d; g=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY); H,W=g.shape
    best=None
    for ang in range(0,360,2):
        dx,dy=math.cos(math.radians(ang)),math.sin(math.radians(ang)); run=0; gap=0; start=None; end=None
        for s in range(int(r)+1,int(r)+420):
            px,py=int(x+dx*s),int(y+dy*s)
            if not(0<=px<W and 0<=py<H): break
            dark=g[py,px]<85
            if dark:
                if start is None:
                    if s>r+9: break
                    start=s
                run+=1; gap=0; end=s
            elif start is not None:
                gap+=1
                if gap>3: break
            elif s>r+9: break
        if start is not None and run>18 and (best is None or run>best[0]): best=(run,ang,end)
    m=np.zeros(g.shape,np.uint8)
    if best:
        run,ang,end=best; dx,dy=math.cos(math.radians(ang)),math.sin(math.radians(ang))
        p1=(int(x+dx*r),int(y+dy*r)); p2=(int(x+dx*end),int(y+dy*end))
        cv2.line(m,p1,p2,255,11)
        p3=(int(x+dx*(end+26)),int(y+dy*(end+26))); p0=(int(x+dx*(end-30)),int(y+dy*(end-30)))
        cv2.line(m,p0,p3,255,30)
    return m
def clean(path,keep,out,expect=None):
    img=cv2.imread(path); ds=disks(img); found=0; mask=np.zeros(img.shape[:2],np.uint8); labels=[]
    reads=[read(img,d) for d in ds]
    if keep=='1' and reads.count('1')==0 and reads.count('')==1: reads=['1' if r=='' else r for r in reads]
    for d,t in zip(ds,reads):
        labels.append(t)
        if t==keep: found+=1; continue
        x,y,r=d; cv2.circle(mask,(x,y),r+5,255,-1); mask|=arrow(img,d)
    res=cv2.inpaint(img,mask,6,cv2.INPAINT_TELEA); cv2.imwrite(out,res,[cv2.IMWRITE_JPEG_QUALITY,90])
    return found,labels
