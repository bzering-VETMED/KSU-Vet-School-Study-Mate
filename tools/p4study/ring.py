import pymupdf as fz
from PIL import Image,ImageDraw
D=fz.open('/mnt/user-data/attachments/31594bc3-9d6f-5c02-a55e-32953ff4d455/f54bb4ad-Lab_35.pdf')
def ring(pg,labels,out,dpi=130):
    p=D[pg-1]; R=fz.Rect()
    for m in p.get_image_info(): R|=fz.Rect(m['bbox'])
    R0=fz.Rect(R)
    for w in p.get_text('words'):
        wr=fz.Rect(w[:4])
        if len(w[4])<=6 and wr.x1>R0.x0-60 and wr.x0<R0.x1+60 and wr.y1>R0.y0-40 and wr.y0<R0.y1+40: R|=wr
    R=fz.Rect(R.x0-6,R.y0-6,R.x1+6,R.y1+6)&p.rect; z=dpi/72
    pm=p.get_pixmap(dpi=dpi,clip=R); im=Image.frombytes('RGB',(pm.width,pm.height),pm.samples); dr=ImageDraw.Draw(im)
    found=0
    for w in p.get_text('words'):
        if w[4] in labels and fz.Rect(w[:4]).intersects(R):
            x0,y0,x1,y1=[(v-o)*z for v,o in zip(w[:4],(R.x0,R.y0,R.x0,R.y0))]
            cx,cy=(x0+x1)/2,(y0+y1)/2; r=max(x1-x0,y1-y0)/2+14
            for k in range(10): dr.ellipse([cx-r-k,cy-r-k,cx+r+k,cy+r+k],outline=(217,79,127))
            found+=1
    im.save(out,quality=88); return found
