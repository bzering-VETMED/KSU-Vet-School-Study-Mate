"""Practical 4 · Lab 27 hub (pelvic limb nerves).  Made by Claude.  Reuses p4lab26 builders.
  ⭐ Lab 27 lab-slide PDF (Dr. Stueve, green-highlight pairs) + slide 34 (yellow text labels → pink numbers)
  🧠 lumbosacral plexus + lumbosacral trunk (concept slides, no photo)
  📚 'Pelvic limb vv nn' nerve-only lecture photos (labels → pink numbers)
  📍 nerve photos already in Lab 26 decks (no repeated photos)
Run from repo root:  python3 tools/p4lab27.py <lab27_slides.pdf> <pelvic_limb_vv_nn.pdf>   (then p4labfn.py)"""
import sys,os,re,html
sys.path.insert(0,'tools')
import pymupdf as fz
from PIL import Image,ImageDraw,ImageFont
import p4lab26 as B
from p4bold import P4BOLD
E=html.escape; LAB=27; HUB=f'gross-anatomy-lab{LAB}-images.html'

def inimage_label_card(pdf,pg,prefix,src_label,zoom=3):
    """slide whose labels are text boxes ON the photo: erase text only, badge on each box"""
    doc=fz.open(pdf); p=doc[pg-1]; im=fz.Rect(max(p.get_image_info(),key=lambda m:fz.Rect(m['bbox']).get_area())['bbox'])&p.rect
    t=p.get_text(); title=re.sub(r'\s+',' ',t.split('Note:')[0]).strip()
    note=re.sub(r'\s+',' ',t.split('Note:')[1]).strip() if 'Note:' in t else ''
    gs=[g for g in B.groups(p) if im.contains(g['r'])]
    for g in gs: note=note.replace(' '.join(g['t']),'').strip()
    gs=sorted(gs,key=lambda g:(round(g['box'].y0/30),g['box'].x0)); M=fz.Matrix(zoom,zoom)
    pa=p.get_pixmap(matrix=M,clip=im); fa=f'assets/{prefix}_{pg}a.jpg'; Image.frombytes('RGB',(pa.width,pa.height),pa.samples).save(fa,quality=90)
    for g in gs:
        for r in g['spans']: p.add_redact_annot(r,fill=False)
    p.apply_redactions(images=fz.PDF_REDACT_IMAGE_NONE,graphics=fz.PDF_REDACT_LINE_ART_NONE)
    pq=p.get_pixmap(matrix=M,clip=im); img=Image.frombytes('RGB',(pq.width,pq.height),pq.samples); dr=ImageDraw.Draw(img)
    font=ImageFont.truetype(B.FONT,int(12*zoom))
    for k,g in enumerate(gs,1):
        c=g['box']; cx=((c.x0+c.x1)/2-im.x0)*zoom; cy=((c.y0+c.y1)/2-im.y0)*zoom; R=11*zoom
        dr.ellipse([cx-R,cy-R,cx+R,cy+R],fill='#e05fa8',outline='white',width=3); dr.text((cx,cy),str(k),fill='white',font=font,anchor='mm')
    fq=f'assets/{prefix}_{pg}q.jpg'; img.save(fq,quality=90)
    FULL={'Perforating branch':'Perforating branch of dorsal metatarsal artery II'}
    names=''.join(f'<div class="nm">#{k} · {E(FULL.get(g["name"],g["name"]))}</div>' for k,g in enumerate(gs,1))
    return dict(name=' | '.join(g['name'] for g in gs),terms=sum((B.terms_in(g['name'],LAB) for g in gs),[]),
                html=B.card(f'Name #1–#{len(gs)}',f'📚 course slide · {src_label} #{pg}',fq,names,[('📝 Slide note (professor):',note)],fa))

def concept(term,text,src):
    return dict(name=term,terms=[term],html=f'<section class="card"><div class="q">🧠 {E(term)}<span class="tagline">🧠 concept · no photo on the slides · {E(src)}</span></div><div class="stg ans"><div class="pr">❓ Define it — what forms it + what comes off it?</div><div class="an"><div class="nm">{E(term)}</div><div class="fx">{E(text)}</div></div></div><div class="rev">💗 TAP TO REVEAL</div></section>')

if __name__=='__main__':
    SL,VN=sys.argv[1],sys.argv[2]
    star=B.slide_cards(SL,LAB,'','p4_l27s','Lab 27 slides')
    star.append(inimage_label_card(SL,34,'p4_l27s','Lab 27 slides'))
    order=[t for t,_,_ in P4BOLD[LAB]]
    star.sort(key=lambda c:min([order.index(t) for t in c['terms']]+[99]))
    vn=B.label_cards(VN,LAB,[18,19,22,23,24,27],'','p4_vvnn','Pelvic limb vv nn')
    np_=[concept('lumbosacral plexus','Ventral branches of the lumbar + sacral spinal nerves (slide: L3–S2). Pelvic-limb sense (notes #1): mainly L4, L5, L6, L7, S1 with small L3 + S2 contributions — like the brachial plexus for the forelimb.','Lab 27 slide 2 · notes #1'),
         concept('lumbosacral trunk','Ventral branches of L6, L7, S1 + part of S2. Gives rise to the cranial gluteal, caudal gluteal + sciatic nerves. Only a SUBSET of the whole lumbosacral plexus.','Lab 27 slide 17 · notes #5')]
    # nerve photos that already live in the Lab 26 decks (no repeated photos)
    seen=[dict(name='Femoral nerve',terms=['femoral nerve']),dict(name='Sciatic nerve',terms=['sciatic nerve']),
          dict(name='Deep fibular nerve',terms=['deep fibular nerve']),dict(name='Cranial gluteal nerve',terms=['cranial gluteal nerve'])]
    seencard=dict(name='Seen in Lab 26',terms=[t for c in seen for t in c['terms']],html='<section class="card"><div class="q">📍 More nerve photos live in Lab 26<span class="tagline">femoral, sciatic + deep fibular nerves · cranial gluteal nerve</span></div><div class="stg ans"><div class="pr">❓ Where?</div><div class="an"><div class="nm"><a href="gross-anatomy-lab26-extra.html">Lab 26 · 📚 Extra bold-term photos</a></div><div class="fx">Numbered lecture photos: femoral nerve, sciatic nerve, deep fibular nerve. Lab 26 ⭐ deck: cranial gluteal nerve slide.</div></div></div><div class="rev">💗 TAP TO REVEAL</div></section>')
    import p4umn
    best,extra,nu=p4umn.merge(LAB,star+np_,vn+[seencard])
    got=B.two_area_hub(LAB,'Lab 27 · Pelvic limb nerves','Two decks. One tap = full answer. 🐾',best,extra,f'{nu} UMN cadaver photos (all numbers on one card) + school slides for the rest')
    print('star',len(star),'more',len(vn),'covered',got,'/',len(P4BOLD[LAB]))
