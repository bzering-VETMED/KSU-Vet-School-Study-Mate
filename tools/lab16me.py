"""Lab 16 · Bethany's dissection photos (notebook pages 13-16) → 📷 my-photo cards.
Run AFTER p3ppt.py + p3diagrams.py (they rewrite the hub), then p3simplify.py. From repo root: python3 tools/lab16me.py <dir with a-000.jpg …>
Question = the photo alone (no labels on it). Reveal = name + facts + the notebook strip with her labels."""
import sys,os,re,time,html
sys.path.insert(0,'tools'); import deck; from deck import *
from PIL import Image
D=sys.argv[1] if len(sys.argv)>1 else '/home/claude/l16p'; V=str(int(time.time())); E=html.escape
Y='📷 my photo · Lab 16 dissection'
def crop(page,box,lab_box,k):
    im=Image.open(f'{D}/{page}.jpg').convert('RGB')
    im.crop(box).save(f'assets/lab16_me_{k}q.jpg',quality=90)
    im.save(f'assets/lab16_me_{k}a.jpg',quality=90)
    return f'assets/lab16_me_{k}q.jpg?v={V}',f'assets/lab16_me_{k}a.jpg?v={V}'
def card(k,page,box,lab_box,q,name,facts,clue=''):
    qi,ai=crop(page,box,lab_box,k); return img_card_facts(q,qi,name,clue,ai,facts,Y)
O=('🧭 Orient first?','Say it: view, recumbency, cranial/caudal, dorsal/ventral. Then name it.')
C=[
card('c2','a-000',(34,74,367,518),(34,74,990,518),'Name the probed nerves (4 structures).',
 'Second cervical spinal nerve · its ventral branch → great auricular nerve · transverse cervical nerve · accessory nerve (cranial nerve XI)',
 [O,('📍 Where does C2 emerge?','Between cleidomastoideus + omotransversarius, near the caudoventral border of the platysma'),
  ('🌿 Ventral branch of C2 gives?','Great auricular n. (ear, back of head) + transverse cervical n. (ventral neck skin)'),
  ('📍 Accessory n. (CN XI): where + supplies?','Deep to the sternocephalicus · motor to trapezius (sole supply), omotransversarius, cleidocephalicus, sternocephalicus')],
 'Your note: accessory n. found under the sternocephalicus'),
card('c35a','a-000',(34,586,367,1030),(34,586,650,1030),'Name the segmental cervical nerves in this view.',
 'Third, fourth + fifth cervical spinal nerves (ventral branches)',
 [O,('📍 Found where?','Ventral border of the omotransversarius, ventral to the accessory n. + dorsal to the external jugular v.'),
  ('🔢 Order?','Sequential cranial → caudal; fifth is the most caudal')],'Your note: C2–C5 found under the omotransversarius'),

]
C=[c for c in C if c]
C.append(card('veins','a-001',(35,48,375,500),(35,48,990,500),'Name the 2 veins + the gland they wrap around.',
 'Linguofacial vein · maxillary vein · mandibular salivary gland',
 [O,('🩸 They join to form?','External jugular vein (at the caudal pole of the mandibular salivary gland)'),
  ('🧭 Which goes where?','Maxillary v. = dorsal/caudal toward the ear · linguofacial v. = ventral/rostral along the jaw')]))
C.append(card('phr','a-001',(35,550,401,1037),(35,550,990,1037),'Which spinal nerve is shown branching, and what does its deep branch form?',
 'Fifth cervical spinal nerve · deep branch = a root of the phrenic nerve',
 [O,('🧬 Phrenic nerve roots?','Ventral branches of C5, C6, C7 (C5 deep branch on the scalenus = most cranial root)'),
  ('🎯 Phrenic n. supplies?','Diaphragm (motor)')],'⚠️ Your note also says "splenic n." here; there is no splenic nerve in the neck, so check with your lab partner what that branch was'))
C.append(card('vst','b-000',(44,558,392,1023),(44,558,990,1023),'Identify the probed structure in the carotid sheath.',
 'Vagosympathetic trunk',[O,('📍 Where?','Carotid sheath, bound to the medial side of the common carotid artery'),
  ('🧩 Contains?','Vagus nerve + cervical sympathetic trunk in one sheath')]))
C.append(card('mrln','b-001',(23,47,375,534),(23,47,990,534),'Identify the structure at the probe.',
 'Medial retropharyngeal lymph node',[O,('📍 Where?','Opposite the larynx, ventrolateral to the carotid sheath'),
  ('🎯 Drains?','Main collecting node of the head + cranial neck → left/right tracheal trunk')]))
C.append(card('lat','b-001',(23,584,375,1044),(23,584,990,1044),'Name the vessels + nerve at the probe (3 structures).',
 'Lateral thoracic artery · lateral thoracic vein · lateral thoracic nerve',
 [O,('📍 Emerge from?','The axilla, between the latissimus dorsi and the deep pectoral'),
  ('🧬 Lateral thoracic nerve?','C8 + T1 · motor to the cutaneous trunci (panniculus reflex)'),
  ('🩸 Artery from / vein to?','Axillary artery / axillary vein')]))
EX=[card('neck','b-000',(44,45,392,510),(44,45,990,510),'Name the deep neck structures exposed (5) + the 2 reflected muscles.',
 'Trachea · larynx · thyroid gland · esophagus · carotid sheath · reflected: cleidocephalicus (mastoid part) + sternocephalicus',[O])]
cs=list(C); cs[0]=cs[0].replace('class="card"','class="card on"',1)
open('gross-anatomy-lab16-mine1.html','w').write(page('Lab 16 · 📷 My dissection photos','⭐ Bold terms · '+str(len(cs))+' cards',''.join(cs),back=f'gross-anatomy-lab16-images.html?v={V}'))
ex=list(EX); ex[0]=ex[0].replace('class="card"','class="card on"',1)
open('gross-anatomy-lab16-mine2.html','w').write(page('Lab 16 · 📷 My photos · deep neck','📚 Extra · non-bold structures',''.join(ex),back=f'gross-anatomy-lab16-images.html?v={V}'))
h=open('gross-anatomy-lab16-images.html').read()
h=re.sub(r'<!--mine-->.*?<!--/mine-->','',h,flags=re.S)
h=h.replace('<p>Every bold term, in small blocks.</p>',f'<p>Every bold term, in small blocks.</p><!--mine--><a href="gross-anatomy-lab16-mine1.html?v={V}">📷 My dissection photos<span>{len(C)} cards</span></a><!--/mine-->',1)
h=h.replace('Optional reps.</p>' if 'Optional reps.</p>' in h else 'fair game.&quot;</p>',(('Optional reps.</p>' if 'Optional reps.</p>' in h else 'fair game.&quot;</p>'))+f'<!--mine--><a href="gross-anatomy-lab16-mine2.html?v={V}">📷 My photos · deep neck<span>1 cards</span></a><!--/mine-->',1)
GOT=['Second cervical spinal nerve','Great auricular nerve','Accessory nerve (cranial nerve XI)','Third cervical spinal nerve','Fifth cervical spinal nerve','External jugular vein','Linguofacial vein','Mandibular salivary gland','Vagosympathetic trunk','Lateral thoracic nerve','Lateral thoracic artery']
for t in GOT:
    h=re.sub(r'(<tr><td>'+re.escape(E(t))+r'</td><td>)(?!📷)',r'\1📷 My photos · ',h)
open('gross-anatomy-lab16-images.html','w').write(h)
p=open('gross-anatomy-practical3.html').read(); p=re.sub(r'gross-anatomy-lab16-images\.html\?v=\d+',f'gross-anatomy-lab16-images.html?v={V}',p); open('gross-anatomy-practical3.html','w').write(p)
print(len(C),'main +',len(EX),'extra')
