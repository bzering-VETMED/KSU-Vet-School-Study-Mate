"""University of Minnesota Carnivore Dissection Labs screenshots → 🌐 UMN cards in each Practical 3 lab hub.
Rules: numbered pointers for BOLD terms stay (numbers never give the answer); labels/arrows for NON-bold
terms are inpainted away on both sides. Caption text is cropped off. One tap = full answer (p3simplify.py).
A photo with bold terms from several labs is added to EVERY one of those labs.
Run: python3 tools/umn.py   (originals live in tools/umn_src/NNNN.jpg)   then python3 tools/p3simplify.py
Add new screenshots by appending to SPEC (crop box, erase list, labs, question, answer, facts)."""
import sys,os,re,time,html,cv2,numpy as np
sys.path.insert(0,'tools'); from deck import *
SRC=sys.argv[1] if len(sys.argv)>1 else 'tools/umn_src'
V=str(int(time.time())); E=html.escape; TAG='🌐 UMN dissection site (vanat.ahc.umn.edu)'
# erase items: ('b',x,y,r) badge circle · ('l',x1,y1,x2,y2) arrow (head at x2,y2) · ('r',x1,y1,x2,y2) box
SPEC=[
 dict(id='4505',umn=9,crop=(65,29,1264,492),labs=[16],
  erase=[('l',320,500,395,420),('l',430,500,518,410),('l',632,500,632,408),('l',795,500,795,386),('l',1060,470,965,373),('l',1265,470,1168,368)],
  q='Right side, skin reflected. Name 1 and 2.',
  a='1 · great auricular nerve (ventral cutaneous branch of the second cervical spinal nerve) · 2 · fifth cervical spinal nerve (its ventral cutaneous branch)',
  f=[('📍 Great auricular n. from?','Ventral branch of C2; runs toward the ear'),('🧭 Dorsal vs ventral cutaneous?','Dorsal cutaneous nn. emerge along the dorsal midline; ventral ones come up on the side of the neck')]),
 dict(id='4507',umn=9,crop=(86,26,1189,1031),labs=[16],
  erase=[('b',806,492,22),('l',790,500,688,582),('r',196,862,246,912)],
  q='Neck, caudolateral view (head to the right). Name 1, 2, and the two unnumbered arrows.',
  a='1 · accessory nerve (cranial nerve XI) · 2 · great auricular nerve · arrows · third cervical spinal nerve (cranial arrow) and fifth cervical spinal nerve (caudal arrow)',
  f=[('🎯 Accessory n. ends in?','Trapezius; runs lengthwise down the neck to reach it'),('🌿 C2 ventral branch splits into?','Great auricular n. + transverse cervical n.')]),
 dict(id='4508',umn=9,crop=(44,26,1243,973),labs=[16],
  erase=[('b',884,650,22),('l',866,650,760,650)],
  q='Neck, lateral view (head to the right). Name 1, 2, and the three unnumbered arrows.',
  a='1 · accessory nerve (cranial nerve XI) · 2 · great auricular nerve · arrows, cranial → caudal · third, fourth, fifth cervical spinal nerves (ventral branches)',
  f=[('📍 Key landmark?','C2–C5 ventral branches all surface under the omotransversarius'),('🔢 Order?','Numbered cranial → caudal; the fifth is the most caudal (toward the shoulder)')]),
 dict(id='4509',umn=9,crop=(34,29,1433,808),labs=[16,17,18],
  erase=[('b',868,245,22),('l',852,262,758,344),('b',318,288,22),('l',334,304,440,408),('b',895,401,22),('b',1048,530,22)],
  q='Neck, LEFT lateral view, deep (head to the right). Name 1, 2, 3, and the asterisks.',
  a='1 · vagosympathetic trunk · 2 · left common carotid artery · 3 · left recurrent laryngeal nerve (on the trachea) · asterisks · brachial plexus',
  f=[('📍 Vagosympathetic trunk?','In the carotid sheath, bound to the common carotid artery'),('🔁 Recurrent laryngeal n.?','Branch of the vagus; runs back up the neck on the trachea to the larynx'),('🧪 Labs','Lab 16: vagosympathetic trunk · Lab 17: left common carotid a. · Lab 18: left recurrent laryngeal n., brachial plexus')]),
 # ---- UMN Lab 10 (thoracic wall, pleura, lungs) ----
 dict(id='4510',umn=10,crop=(62,16,1261,765),labs=[16],
  erase=[('b',533,46,20),('l',515,62,432,128),('b',325,255,20),('l',342,272,398,325),('b',838,367,20),('l',822,352,776,312),('l',822,382,776,418),('b',962,680,20)],
  q='Left lateral thorax, skin reflected (head to the right). Name 5 (both arrows).',
  a='5 · lateral thoracic nerve',
  f=[('🎯 Supplies?','Cutaneous trunci (motor); this is the panniculus reflex nerve'),('🧬 From?','Brachial plexus (C8 + T1); emerges from the axilla')]),
 dict(id='4516',umn=10,crop=(40,31,1239,870),labs=[16,18],
  erase=[('b',402,264,20),('b',287,175,20),('b',527,183,20),('b',828,290,20),('l',810,302,712,372),('r',950,795,995,845)],
  q='Deep (pleural) surface of the thoracic wall; probe lifts one bundle. Name 4 and 5.',
  a='4 · dorsal intercostal artery · 5 · intercostal nerve',
  f=[('📍 Where do they run?','Along the CAUDAL border of each rib (vein, artery, nerve)'),('🫁 The shiny lining here?','Costal pleura (parietal pleura on the ribs)')]),
 dict(id='4511',umn=10,crop=(42,30,1241,691),labs=[17,18],
  erase=[('b',880,133,20),('b',316,355,20)],
  q='Cat, ventral view; deep pectoral reflected cranially, rectus abdominis reflected caudally. Name 3 and 4.',
  a='3 · cranial epigastric artery (deep surface of the rectus abdominis) · 4 · brachial plexus nerves + axillary vessels',
  f=[('🩸 Cranial epigastric a. from?','Continuation of the internal thoracic artery')]),
 dict(id='4512',umn=10,crop=(35,29,1234,862),labs=[17,18],erase=[],
  q='Cat, ventral view; thoracic wall cut. Name 1, 2, 3, and 4.',
  a='1 · cranial epigastric artery · 2 · internal thoracic artery · 3 · cranial superficial epigastric artery · 4 · brachial plexus nerves + axillary vessels',
  f=[('🔗 Chain?','Internal thoracic a. → cranial epigastric a. → gives off the cranial superficial epigastric a. (cutaneous)'),('⚠️ Trap','Superficial = cutaneous branch; the plain cranial epigastric stays on the deep rectus surface')]),
 dict(id='4513',umn=10,crop=(29,25,1228,692),labs=[18],
  erase=[('b',377,597,20),('b',746,600,20),('b',718,178,20),('l',222,480,330,480),('l',965,474,858,474)],
  q='Dog, ventrolateral thorax; serratus ventralis detached. Name 3.',
  a='3 · brachial plexus',
  f=[('🧬 Roots?','Ventral branches of C6, C7, C8, T1 (T2 small)')]),
 dict(id='4514',umn=10,crop=(32,35,1231,946),labs=[17,18],
  erase=[('l',375,390,480,390),('l',357,518,462,518),('l',375,630,480,630),('l',442,768,548,768),('l',656,718,656,612),('l',680,700,680,598),('l',771,658,771,555),('l',796,642,796,537),('l',878,598,878,492),('l',908,585,908,482)],
  q='Cat, sternum elevated, left thoracic wall reflected. Name 1, 2, 3, and the asterisk.',
  a='1 · heart · 2 · left lung · 3 · internal thoracic artery · asterisk · ventral mediastinum (sternopericardial ligament)',
  f=[('🧭 Mediastinum?','Midline partition between the two pleural cavities; ventral part attaches to the sternum')]),
 dict(id='4515',umn=10,crop=(36,34,1235,1115),labs=[17,18],erase=[],
  q='Cat, RIGHT pleural cavity, right lung reflected. Name 1–9 and the asterisks (1–3 = which pleura covers it).',
  a='1 · costal pleura (on thoracic wall) · 2 · diaphragmatic pleura (on diaphragm) · 3 · mediastinal pleura (over the heart) · 4 · right caudal lobe · 5 · right middle lobe · 6 · right cranial lobe · 7 · phrenic nerve · 8 · right azygos vein · 9 · internal thoracic artery · asterisks · thymus',
  f=[('🫁 Lungs are covered by?','Pulmonary (visceral) pleura'),('🧪 Labs','Lab 17: pleurae, lobes, azygos, internal thoracic, thymus · Lab 18: phrenic nerve, heart')]),
 dict(id='4517',umn=10,crop=(26,20,1225,1277),labs=[17,18],
  erase=[('b',457,510,20)],
  q='Left thorax, left lung reflected. Name 1–7 and 9 (5 + 6: name the pleura covering each).',
  a='1 · cranial part of the left cranial lobe · 2 · caudal part of the left cranial lobe · 3 · left caudal lobe · 4 · pulmonary ligament · 5 · mediastinal pleura (over the heart) · 6 · diaphragmatic pleura (on the diaphragm) · 7 · root of the lung (cut) · 9 · phrenic nerve',
  f=[('🔗 Pulmonary ligament?','Fold connecting pulmonary (visceral) pleura to mediastinal (parietal) pleura, caudal to the root'),('🎯 Phrenic n.?','Motor to the diaphragm (C5, C6, C7)')]),
 dict(id='4518',umn=10,crop=(131,20,1120,637),labs=[17],
  erase=[('b',355,45,20),('l',372,62,462,150),('b',455,312,20),('b',542,312,20),('l',455,292,455,215),('l',542,292,542,215),('b',710,80,20),('l',692,98,612,158),('l',657,295,568,205)],
  q='Isolated LEFT lung, medial view. Name 1, 2, 3, 4, and 6.',
  a='1 · cranial part of the left cranial lobe · 2 · caudal part of the left cranial lobe · 3 · left caudal lobe · 4 · pulmonary ligament · 6 · lobar bronchi',
  f=[('🌳 Bronchial tree?','Principal bronchus → lobar bronchi (one per lobe) → segmental bronchi'),('🧭 Left lung lobes?','Cranial (cranial + caudal parts) and caudal; no middle or accessory lobe on the left')]),
]
def erase(im,items,crop):
    """Region = generous zone around each guessed label; inside it, only label-like pixels (near-black
    arrow/number strokes, near-white badge fill) are masked, dilated, then inpainted. Anatomy stays."""
    x0,y0=crop[0],crop[1]; R=np.zeros(im.shape[:2],np.uint8)
    for it in items:
        k=it[0]; c=[int(v-(x0 if i%2==0 else y0)) for i,v in enumerate(it[1:5 if k!='b' else 3])]
        if k=='b': cv2.circle(R,(c[0],c[1]),it[3]+16,255,-1)
        elif k=='r': cv2.rectangle(R,(c[0],c[1]),(c[2],c[3]),255,-1)
        else:
            v=np.array([c[2]-c[0],c[3]-c[1]],float); v/=max(np.linalg.norm(v),1)
            hx,hy=int(c[2]+v[0]*22),int(c[3]+v[1]*22)
            cv2.line(R,(c[0],c[1]),(hx,hy),255,34); cv2.circle(R,(c[2],c[3]),30,255,-1)
    g=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY); mn=im.min(2)
    m=(((g<95)|(mn>205))&(R>0)).astype(np.uint8)*255
    m=cv2.dilate(m,np.ones((7,7),np.uint8))&R
    return cv2.inpaint(im,m,9,cv2.INPAINT_TELEA)
os.makedirs('assets',exist_ok=True)
for f in os.listdir('assets'):
    if f.startswith('umn_'): os.remove('assets/'+f)
bylab={}
for s in SPEC:
    im=cv2.imread(f"{SRC}/{s['id']}.jpg"); x0,y0,x1,y1=s['crop']; im=im[y0:y1+1,x0:x1+1]
    im=erase(im,s['erase'],s['crop']); out=f"assets/umn_{s['id']}.jpg"; cv2.imwrite(out,im,[cv2.IMWRITE_JPEG_QUALITY,93])
    tag=f"{TAG} · UMN Lab {s['umn']}"
    c=img_card_facts(s['q'],f'{out}?v={V}',s['a'],'',f'{out}?v={V}',s['f'],tag)
    for L in s['labs']: bylab.setdefault(L,[]).append(c)
for L,cs in bylab.items():
    cs=list(cs); cs[0]=cs[0].replace('class="card"','class="card on"',1)
    fn=f'gross-anatomy-lab{L}-umn.html'
    open(fn,'w').write(page(f'Lab {L} · 🌐 UMN dissection photos',f'⭐ Bold terms · {len(cs)} cards',''.join(cs),back=f'gross-anatomy-lab{L}-images.html?v={V}'))
    hub=f'gross-anatomy-lab{L}-images.html'; h=open(hub).read()
    h=re.sub(r'<!--umn-->.*?<!--/umn-->','',h,flags=re.S)
    h=h.replace('<p>Every bold term, in small blocks.</p>',f'<p>Every bold term, in small blocks.</p><!--umn--><a href="{fn}?v={V}">🌐 UMN dissection photos<span>{len(cs)} cards</span></a><!--/umn-->',1)
    open(hub,'w').write(h)
p=open('gross-anatomy-practical3.html').read()
for L in bylab: p=re.sub(rf'gross-anatomy-lab{L}-images\.html\?v=\d+',f'gross-anatomy-lab{L}-images.html?v={V}',p)
open('gross-anatomy-practical3.html','w').write(p)
print({L:len(c) for L,c in bylab.items()})
