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
# batch 2 (Oct 26): journal Figs 2, 3, 4 (perineum + pelvic pouches)
if os.path.exists(f'{A}/a1fe5a13-image.jpg'):
    G2ab=crop('a1fe5a13-image.jpg',(155,42,818,592),'p3web_g2ab.jpg'); G2c=crop('a1fe5a13-image.jpg',(836,42,1154,592),'p3web_g2c.jpg')
    G3a=crop('426d6e65-image.jpg',(175,50,677,635),'p3web_g3a.jpg'); G3b=crop('426d6e65-image.jpg',(697,50,1173,633),'p3web_g3b.jpg')
    G4a=crop('0e0de78a-image.jpg',(349,5,905,525),'p3web_g4a.jpg'); G4b=crop('0e0de78a-image.jpg',(349,538,905,1000),'p3web_g4b.jpg')
    g2ab=img_card_facts('Lateral view of the perineum, skin + superficial fascia (a) then deeper (b). Name 3 and 4.',G2ab,
     '#3 Rectococcygeus muscle · #4 Anus','Others: 1 superficial perineal fascia · 2 deep perineal fascia · 5 external fascia of the pelvic diaphragm (not bold terms)','',
     [('💪 Rectococcygeus','Smooth muscle from the rectum → ventral tail vertebrae; the retractor penis/clitoridis arises from it')],TAG)
    g2c=img_card_facts('Caudal view of the perineum (tail at top). Name 4, 7, 8, 9.',G2c,
     '#4 Anus · #7 External anal sphincter muscle · #8 Levator ani muscle · #9 Coccygeus muscle','#6 = internal fascia of the pelvic diaphragm (not bold)','',
     [('🧩 Pelvic diaphragm','Levator ani (medial) + coccygeus (lateral) + their fasciae')],TAG)
    g3a=img_card_facts('MALE perineum, caudal view (T = testes). Name 5, 6, 10, 12, 20, 21, 23, 27.',G3a,
     '#5 Ischiourethralis muscle · #6 Ischiocavernosus muscle · #10 External anal sphincter muscle · #12 Coccygeus muscle · #20 Bulbospongiosus muscle · #21 Retractor penis muscle · #23 Rectococcygeus muscle · #27 Anus',
     'Nerves 13–19, 22 (pudendal, caudal rectal, perineal, dorsal nerve of the penis) are not on your bold list · 24 = ischiorectal fossa · 1 superficial gluteal · 2 internal obturator · 3 semimembranosus · 4 semitendinosus · 25 gracilis','',[],TAG)
    g3b=img_card_facts('FEMALE perineum, caudal view (VL = vulvar lips). Name 7, 10, 11, 12, 23, 27.',G3b,
     '#7 Retractor clitoridis muscle (reflected) · #10 External anal sphincter muscle · #11 Levator ani muscle · #12 Coccygeus muscle · #23 Rectococcygeus muscle · #27 Anus · VL = labia of the vulva',
     '8 constrictor vestibuli + 9 constrictor vulvae + 5 ischiourethralis + 6 ischiocavernosus also shown (constrictors not bold) · nerves 13–19 not bold','',[],TAG)
    g4a=img_card_facts('MALE pelvis, right side (cranial right). Name 2, 3, 4, 5, 6, 7, 8 + R, P, U, U.B.',G4a,
     '#2 Pararectal fossa · #3 Rectogenital pouch · #4 Vesicogenital pouch · #5 Pubovesical pouch · #6 Internal anal sphincter muscle · #7 Paranal sinus (right anal sac) · #8 External anal sphincter muscle · R Rectum · P Prostate gland · U Urethra (pelvic part) · U.B Urinary bladder',
     'Pouch order dorsal → ventral: pararectal fossa → rectogenital → vesicogenital → pubovesical · 9 = ampulla of the rectum · L.dd / R.dd = ductus deferens','',
     [('⚠️ Exam word','Paper says "paranal sac" → write paranal sinus; say pouch, not fossa (except pararectal fossa)')],TAG)
    g4b=img_card_facts('FEMALE pelvis, right side (cranial right). Name 2, 3, 4, 5, 10 + R, ut.c, V, VV, U, U.B.',G4b,
     '#2 Pararectal fossa · #3 Rectogenital pouch · #4 Vesicogenital pouch · #5 Pubovesical pouch · #10 Round ligament of the bladder · R Rectum · ut.c Cervix · V Vagina · VV Vestibule · U Urethra · U.B Urinary bladder',
     '6 internal + 8 external anal sphincter muscles · 7 paranal sinus · 11 constrictor vulvae · 12 constrictor vestibuli (not bold)','',
     [('🧩 Female pouches','Rectogenital = between rectum + uterus/vagina; vesicogenital = between genital tract + bladder')],TAG)
    C[24]+= [g2ab,g2c,g4a,g4b,g3a,g3b]; C[25]+= [g3a,g3b,g4a,g4b]
# batch 3: vulva drawing (labels erased + badges made earlier into assets/p3web_vulva_draw.jpg)
if os.path.exists('assets/p3web_vulva_draw.jpg'):
    C[25].insert(0,img_card_facts('Female dog, caudal view (drawing). Name 1–6.',f'assets/p3web_vulva_draw.jpg?v={V}',
     '#1 Anus · #2 Dorsal commissure · #3 Rima pudendi · #4 Ventral commissure · #5 Labia (of the vulva) · #6 Vulva',
     'Drawing labels say "dorsal/ventral labial commissure" and "vulvar cleft" → exam words: dorsal commissure, ventral commissure, rima pudendi','',
     [('🧩 Vulva','= two labia + the rima pudendi between them'),('🔝 Commissures','Dorsal = top end of the rima (toward the anus) · ventral = bottom end, points caudoventrally')],'🌐 web drawing (dog) · sent by Bethany'))
css=re.search(r'<style>(.*?)</style>',open('gross-anatomy-lab22-best1.html').read(),re.S).group(1)
for n,cs in C.items():
    fn=f'gross-anatomy-lab{n}-web1.html'; hubf=f'gross-anatomy-lab{n}-images.html'
    pg=page(f'Lab {n} · 🌐 Extra dog photos',f'Perineum + vulva photos Bethany found · {len(cs)} cards',''.join(cs).replace('class="card"','class="card on"',1),back=f'{hubf}?v={V}')
    open(fn,'w').write(re.sub(r'<style>.*?</style>',lambda _:f'<style>{css}</style>',pg,count=1,flags=re.S))
    h=open(hubf).read(); h=re.sub(r'<!--web-->.*?<!--/web-->','',h,flags=re.S)
    link=f'<!--web--><a href="{fn}?v={V}">🌐 Extra dog photos · perineum{" + vulva" if n==25 else ""}<span>{len(cs)} cards</span></a><!--/web-->'
    m=re.search(r'(<div class="sec main">.*?)(</div>)',h,re.S)
    h=h[:m.end(1)]+link+h[m.end(1):]; open(hubf,'w').write(h); print(n,len(cs))
