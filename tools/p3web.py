"""Practical 3 · 🌐 extra DOG photos Bethany found (journal perineum figures + pre-lab vulva photo) → added INSIDE the
⭐ bold-terms section of the Lab 24 + Lab 25 hubs as their own block (nothing removed or replaced).  Made by Claude.
The journal photos already carry small printed numbers, so the photo is the question and the caption is the answer
(caption names translated to exam names). Idempotent; run AFTER p3best/p3dedupe/p3check/p3ours:
  python3 tools/p3web.py <attachments dir>"""
import sys,os,re,time,html
sys.path.insert(0,'tools')
from PIL import Image
from deck import page,img_card_facts
A=sys.argv[1]; V=str(int(time.time()))
TAG='🌐 web photo (dog) · journal figure, sent by Bethany'
def crop(src,box,out):
    Image.open(f'{A}/{src}').convert('RGB').crop(box).save(f'assets/{out}',quality=92); return f'assets/{out}?v={V}'
F6=crop('0305875b-image.jpg',(150,38,836,872),'p3web_f6.jpg')
F7=crop('692a465f-image.jpg',(217,30,1119,834),'p3web_f7.jpg')
F8=crop('6a3495e1-image.jpg',(165,34,1167,766),'p3web_f8.jpg')
F11a=crop('5d89f6c8-image.jpg',(116,32,705,546),'p3web_f11a.jpg')
F11b=crop('5d89f6c8-image.jpg',(716,32,1364,546),'p3web_f11b.jpg')
VUL=crop('4282ad39-image.jpg',(130,275,1062,962),'p3web_vulva_pin.jpg')
C={25:[],24:[]}
C[25].append(img_card_facts('Perineal region, caudal view (anus at top). Name 2, 5, 6, 7.',F6,
 '#2 External anal sphincter muscle · #5 Retractor penis muscle (penile part) · #6 Ischiocavernosus muscle · #7 Bulbospongiosus muscle',
 'Other numbers: 1 lateral coccygeus m. · 3 ischial tuberosity · 4 Colle\'s fascia · 8 scrotal septum · 9 deep penile fascia · 10 superficial penile fascia (not bold terms)','',
 [('💪 Ischiocavernosus','Ischiatic tuberosity → covers the crus of the penis'),('💪 Bulbospongiosus','Covers the bulb of the penis, between the ischiocavernosus muscles')],TAG))
C[25].append(img_card_facts('Right ischiorectal fossa, deep dissection. What does the BLACK arrow point to? Also name 5, 6, 7, 9.',F7,
 'Black arrow = Ischiourethralis muscle (under the deep perineal fascia) · #5 Ischiocavernosus muscle · #6 Bulbospongiosus muscle · #7 Retractor penis muscle (penile part) · #9 Pelvic part of the urethra',
 'Others: 1 external anal sphincter · 2 ischiococcygeus (= coccygeus) · 3 pubococcygeus (part of levator ani) · 4 lateral coccygeus · 8 perineal m. · 10 deep perineal fascia · 11 ischial tuberosity · 12 internal obturator','',
 [('💪 Ischiourethralis','Small muscle: ischiatic tuberosity → ring around the dorsal vein of the penis (hard to find in lab)')],TAG))
C[25].append(img_card_facts('Perineal region, left half of the pelvis removed (cranial left). Name 4, 5, 7, 8.',F8,
 '#4 Retractor penis muscle (vertebral part) · #5 External anal sphincter muscle · #7 Bulbospongiosus muscle · #8 Crus of the penis (left)',
 'Others: 1 iliococcygeus + 2 pubococcygeus = levator ani muscle · 3 ischiococcygeus = coccygeus muscle · 6 perineal m.','',
 [('🧩 Levator ani','Iliococcygeus + pubococcygeus parts (medial) · coccygeus = ischiococcygeus (lateral)')],TAG))
for img,lab in ((F11a,'11a'),(F11b,'11b')):
    C[25].append(img_card_facts(f'Suspensory apparatus of the anus (Fig {lab}, cranial left). Name the muscle at the BLACK arrow and its parts.',img,
     'Black arrow = Retractor penis muscle · blue = rectal part · green = penile part · red = anal part'+(' · #2 Rectococcygeus muscle · #4 External anal sphincter muscle · #7 Bulbospongiosus muscle' if lab=='11a' else ''),
     'Pre-lab video: the retractor penis arises from the rectococcygeus and blends with the external anal sphincter',
     '',[],TAG))
C[25].append(img_card_facts('Vulva (pre-lab 25 photo). Name the pinned structure of the labia.',VUL,'Ventral commissure',
 'The labia meet above and below the rima pudendi: dorsal commissure (ventral to the pelvic symphysis level) and ventral commissure (directed caudoventrally)','',
 [('🔎 Dorsal commissure','The OPPOSITE end of the rima pudendi from the pin'),('⚠️ Note','Pin answer = your pre-lab answer; confirm when graded')],'📷 pre-lab 25 photo (dog)'))
C[24]=[C[25][1],C[25][2],C[25][3]]   # levator ani parts, coccygeus, external anal sphincter, rectococcygeus also Lab 24 terms
css=re.search(r'<style>(.*?)</style>',open('gross-anatomy-lab22-best1.html').read(),re.S).group(1)
for n,cs in C.items():
    fn=f'gross-anatomy-lab{n}-web1.html'; hubf=f'gross-anatomy-lab{n}-images.html'
    pg=page(f'Lab {n} · 🌐 Extra dog photos',f'Perineum + vulva photos Bethany found · {len(cs)} cards',''.join(cs).replace('class="card"','class="card on"',1),back=f'{hubf}?v={V}')
    open(fn,'w').write(re.sub(r'<style>.*?</style>',lambda _:f'<style>{css}</style>',pg,count=1,flags=re.S))
    h=open(hubf).read(); h=re.sub(r'<!--web-->.*?<!--/web-->','',h,flags=re.S)
    link=f'<!--web--><a href="{fn}?v={V}">🌐 Extra dog photos · perineum{" + vulva" if n==25 else ""}<span>{len(cs)} cards</span></a><!--/web-->'
    m=re.search(r'(<div class="sec main">.*?)(</div>)',h,re.S)
    h=h[:m.end(1)]+link+h[m.end(1):]; open(hubf,'w').write(h); print(n,len(cs))
