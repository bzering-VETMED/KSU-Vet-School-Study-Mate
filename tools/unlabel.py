import pdfplumber, cv2, numpy as np
def unlabel(pdf_path,pn,a_path,q_path,S,single=False,yglobal=False):
    pg=pdfplumber.open(pdf_path).pages[pn-1]; ims=[max(pg.images,key=lambda i:(i['x1']-i['x0'])*(i['bottom']-i['top']))] if single else pg.images
    bb=(max(0,min(i['x0'] for i in ims)),max(0,min(i['top'] for i in ims)),min(pg.width,max(i['x1'] for i in ims)),min(pg.height,max(i['bottom'] for i in ims)))
    im=cv2.imread(a_path); H,W=im.shape[:2]; mask=np.zeros((H,W),np.uint8); boxes=[]
    b=im[:,:,0].astype(int);g=im[:,:,1].astype(int);r=im[:,:,2].astype(int)
    red=(r>130)&(r-g>60)&(r-b>60); dark=(r+g+b)<150; yellow=(r>170)&(g>160)&(b<140)
    for w in pg.extract_words():
        if w['x1']>bb[0] and w['x0']<bb[2] and w['bottom']>bb[1] and w['top']<bb[3]:
            x0=max(0,int((w['x0']-bb[0])*S)-6);y0=max(0,int((w['top']-bb[1])*S)-5);x1=min(W,int((w['x1']-bb[0])*S)+6);y1=min(H,int((w['bottom']-bb[1])*S)+5)
            if x1>x0 and y1>y0:
                sub=im[y0:y1,x0:x1].astype(int)
                border=np.concatenate([sub[0],sub[-1],sub[:,0],sub[:,-1]])
                med=np.median(border,axis=0)
                m=(np.abs(sub-med).sum(2)>60)|(red|dark|yellow)[y0:y1,x0:x1]
                if med.min()>215 and np.abs(border-med).sum(1).mean()<40:
                    m=np.ones(m.shape,bool)
                mask[y0:y1,x0:x1]=np.maximum(mask[y0:y1,x0:x1],(m*255).astype(np.uint8)); boxes.append((x0,y0,x1,y1))
    if yglobal:
        ym=((r>180)&(g>170)&(b<110)).astype(np.uint8)*255
        mask=np.maximum(mask,cv2.dilate(ym,np.ones((3,3),np.uint8),iterations=3))
    mask=cv2.dilate(mask,np.ones((3,3),np.uint8),iterations=2)
    out=cv2.inpaint(im,mask,7,cv2.INPAINT_TELEA)
    cv2.imwrite(q_path,out,[cv2.IMWRITE_JPEG_QUALITY,85])
