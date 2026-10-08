"""Lab 16 · Bethany's ORIGINAL dissection photos → 📷 my-photo cards (one tap = full answer).
String/tag colors match her notebook highlights, so answers give a color key.
Run AFTER p3ppt.py + p3diagrams.py, then p3simplify.py.  python3 tools/lab16me.py <photo dir> <notebook page dir>"""
import sys,os,re,time,html
sys.path.insert(0,'tools'); from deck import *
from PIL import Image
P=sys.argv[1] if len(sys.argv)>1 else '/home/claude/l16o'; N=sys.argv[2] if len(sys.argv)>2 else '/home/claude/l16p'
V=str(int(time.time())); E=html.escape; Y='📷 my photo · Lab 16 dissection'
PAGE={'c2':'a-000','c35':'a-000','acc':'a-000','veins':'a-001','phr':'a-001','neck':'b-000','vst':'b-000','mrln':'b-001','lat':'b-001'}
for f in os.listdir('assets'):
    if f.startswith('lab16_me_'): os.remove('assets/'+f)
def card(k,q,name,facts,clue=''):
    im=Image.open(f'{P}/{k}.jpg').convert('RGB'); im.thumbnail((1800,1800)); im.save(f'assets/lab16_me_{k}.jpg',quality=88)
    Image.open(f'{N}/{PAGE[k]}.jpg').convert('RGB').save(f'assets/lab16_me_{k}n.jpg',quality=90)
    return img_card_facts(q,f'assets/lab16_me_{k}.jpg?v={V}',name,clue,f'assets/lab16_me_{k}n.jpg?v={V}',facts,Y)
C=[
card('c2','Name each strung structure (by string color).',
 'Green: second cervical spinal nerve · blue: great auricular nerve (ventral branch of C2) · red/pink: accessory nerve (cranial nerve XI)',
 [('📍 C2 emerges?','Between cleidomastoideus + omotransversarius, near the caudoventral border of the platysma'),
  ('🌿 Ventral branch of C2 gives?','Great auricular n. (ear, back of head) + transverse cervical n. (ventral neck skin)')]),
card('acc','Identify the strung (pink) nerve.',
 'Accessory nerve (cranial nerve XI)',
 [('📍 Found?','Deep to the sternocephalicus; crosses C2; ends in the thoracic trapezius'),
  ('🎯 Supplies?','Trapezius (sole supply), omotransversarius, cleidocephalicus, sternocephalicus')]),
card('c35','Name the 3 strung nerves by color (muscle lifted = omotransversarius).',
 'Orange: third cervical spinal nerve · yellow-green: fourth cervical spinal nerve · teal: fifth cervical spinal nerve',
 [('📍 Key landmark?','C2–C5 ventral branches all lie under the omotransversarius'),
  ('🔢 Order?','Sequential cranial → caudal; fifth is the most caudal')]),
card('veins','Name the 2 highlighted veins + the highlighted gland.',
 'Purple (ventral): linguofacial vein · pink (dorsal): maxillary vein · round mauve: mandibular salivary gland',
 [('🩸 They join to form?','External jugular vein, at the caudal pole of the mandibular salivary gland'),
  ('🧭 Which goes where?','Maxillary v. = dorsal/caudal toward the ear · linguofacial v. = ventral/rostral along the jaw')]),
card('phr','Which spinal nerve is strung here, and what does its deep branch form?',
 'Fifth cervical spinal nerve · deep branch = a root of the phrenic nerve',
 [('🧬 Phrenic nerve roots?','Ventral branches of C5, C6, C7 (C5 deep branch on the scalenus = most cranial root)'),
  ('🎯 Phrenic n. supplies?','Diaphragm (motor)')],
 '⚠️ Your note also says "splenic n." here; there is no splenic nerve in the neck, so check what that branch was'),
card('vst','Identify the structure on the blue probe/string.',
 'Vagosympathetic trunk',
 [('📍 Where?','Carotid sheath, bound to the medial side of the common carotid artery'),
  ('🧩 Contains?','Vagus nerve + cervical sympathetic trunk in one sheath')]),
card('mrln','Identify the purple-dyed structure at the probe.',
 'Medial retropharyngeal lymph node',
 [('📍 Where?','Opposite the larynx, ventrolateral to the carotid sheath'),
  ('🎯 Drains?','Main collecting node of the head + cranial neck → tracheal trunk')]),
card('lat','Name the 3 strung structures by color.',
 'Orange: lateral thoracic artery · yellow-green: lateral thoracic vein · teal: lateral thoracic nerve',
 [('📍 Emerge from?','The axilla, between the latissimus dorsi and the deep pectoral'),
  ('🧬 Lateral thoracic nerve?','C8 + T1 · motor to the cutaneous trunci (panniculus reflex)'),
  ('🩸 Artery from / vein to?','Axillary artery / axillary vein')]),
]
EX=[card('neck','Name the deep neck structures exposed (5) + the 2 reflected muscles.',
 'Trachea · larynx · thyroid gland · esophagus · carotid sheath · reflected: cleidocephalicus (mastoid part) + sternocephalicus',[])]
cs=list(C); cs[0]=cs[0].replace('class="card"','class="card on"',1)
open('gross-anatomy-lab16-mine1.html','w').write(page('Lab 16 · 📷 My dissection photos',f'⭐ Bold terms · {len(cs)} cards',''.join(cs),back=f'gross-anatomy-lab16-images.html?v={V}'))
ex=list(EX); ex[0]=ex[0].replace('class="card"','class="card on"',1)
open('gross-anatomy-lab16-mine2.html','w').write(page('Lab 16 · 📷 My photos · deep neck','📚 Extra · non-bold structures',''.join(ex),back=f'gross-anatomy-lab16-images.html?v={V}'))
h=open('gross-anatomy-lab16-images.html').read()
h=re.sub(r'<!--mine-->.*?<!--/mine-->','',h,flags=re.S)
h=h.replace('<p>Every bold term, in small blocks.</p>',f'<p>Every bold term, in small blocks.</p><!--mine--><a href="gross-anatomy-lab16-mine1.html?v={V}">📷 My dissection photos<span>{len(C)} cards</span></a><!--/mine-->',1)
anchor='fair game.&quot;</p>' if 'fair game.&quot;</p>' in h else 'Optional reps.</p>'
h=h.replace(anchor,anchor+f'<!--mine--><a href="gross-anatomy-lab16-mine2.html?v={V}">📷 My photos · deep neck<span>1 cards</span></a><!--/mine-->',1)
GOT=['Second cervical spinal nerve','Great auricular nerve','Accessory nerve (cranial nerve XI)','Third cervical spinal nerve','Fifth cervical spinal nerve','Linguofacial vein','Mandibular salivary gland','Vagosympathetic trunk','Lateral thoracic nerve','Lateral thoracic artery']
for t in GOT: h=re.sub(r'(<tr><td>'+re.escape(E(t))+r'</td><td>)(?!📷)',r'\1📷 My photos · ',h)
open('gross-anatomy-lab16-images.html','w').write(h)
p=open('gross-anatomy-practical3.html').read(); p=re.sub(r'gross-anatomy-lab16-images\.html\?v=\d+',f'gross-anatomy-lab16-images.html?v={V}',p); open('gross-anatomy-practical3.html','w').write(p)
print(len(C),'main +',len(EX),'extra')
