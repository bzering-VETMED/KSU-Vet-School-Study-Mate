import sys; sys.path.insert(0,'.')
import deck; deck.PRACTICAL=3          # Lab 14 belongs to Practical 3
from deck import *; from oia_thoracic import OIA
# Source images (re-create in a sandbox): D = native-res crops.
#  d{pn}.jpg  = Lab 14 Dissection Images PDF page pn, photo only (highlight kept, orientation tags kept, no name labels)
#  t{pn}a.jpg = Trunk muscles slide pn (labeled) · t{pn}q.jpg = same with labels inpainted by unlabel(keep=KEEP_ORIENT),
#               pointer-line boxes numbered on slides 3 + 18
#  q1.jpg, q5.jpg = Pre-lab 14 quiz images
D='/home/claude/l14/'; Q='/home/claude/img/'
SD='📚 course slide · Lab 14 Dissection Images'; ST='📚 course slide · Trunk muscles'; SP='📚 course slide · Pre-lab 14 quiz'
O14={'Serratus ventralis':OIA['Serratus ventralis']}   # only Lab 14 muscle on the professor's thoracic OIA list
IDQ='Identify the highlighted structure.'
def put(src,dst):
    from PIL import Image
    save_img(src,f'site/assets/{dst}',Image.open(src).width)   # native resolution
    return f'assets/{dst}'

def dcard(pn,name,facts,q=IDQ,clue='',oia=False):
    qi=put(D+f'd{pn}.jpg',f'lab14_d{pn}.jpg')
    if oia: return img_card2(q,qi,name,clue,'',['Serratus ventralis'],O14,SD)
    return img_card_facts(q,qi,name,clue,'',facts,SD)
def tcard(pn,q,name,facts=(),clue='',oia=False):
    qi=put(D+f't{pn}q.jpg',f'lab14_t{pn}q.jpg'); ai=put(D+f't{pn}a.jpg',f'lab14_t{pn}a.jpg')
    if oia: return img_card2(q,qi,name,clue,ai,['Serratus ventralis'],O14,ST)
    return img_card_facts(q,qi,name,clue,ai,list(facts),ST)

FD='↘️ Fiber direction?'; FU='↗️ Fiber direction?'
d={
5:dcard(5,'Longus capitis',[("📍 Where?","Lateral surface of the cervical vertebrae"),("⚠️ Dissection caution?","Carotid sheath is nearby; protect its vessels + nerves")]),
7:dcard(7,'Longus colli',[("📍 Where?","Ventral surface of the cervical vertebral bodies, deep to the trachea + esophagus"),("⭐ Why reflect it?","To expose the cervical intervertebral discs")]),
9:dcard(9,'Scalenus',[("⚙️ Function?","Muscle of inspiration"),("🔪 To see it?","Reflect latissimus dorsi dorsally")]),
11:dcard(11,'Serratus ventralis, cervical part (serratus ventralis cervicis)',None,clue='Fully visible now that the limb is removed',oia=True),
12:dcard(12,'Serratus ventralis, thoracic part (serratus ventralis thoracis)',None,clue='Slips on the ribs converge on the serrated face of the scapula',oia=True),
14:dcard(14,'Serratus dorsalis cranialis',[(FD,"Caudoventral"),("🔪 To see it?","Reflect latissimus dorsi dorsally + serratus ventralis ventrally"),("⭐ Origin type?","Aponeurotic, from the thoracolumbar fascia")]),
15:dcard(15,'Serratus dorsalis caudalis',[(FU,"Cranioventral"),("🔪 What covers it?","Thick thoracolumbar fascia; remove it to find the borders")]),
17:dcard(17,'External intercostal muscle',[(FD,"Caudoventral"),("📍 Layer?","Superficial of the two intercostal muscles")]),
18:dcard(18,'Internal intercostal muscle',[(FU,"Cranioventral"),("📍 Layer?","Deep to the external intercostal (one external is reflected here)")]),
20:dcard(20,'External abdominal oblique',[(FD,"Caudoventral"),("📍 Arises from?","Costal part of the last ribs + thoracolumbar fascia"),("🎯 Its aponeurosis inserts on?","Linea alba")]),
22:dcard(22,'Internal abdominal oblique',[(FU,"Cranioventral"),("⭐ Its caudal border forms?","Cranial border of the inguinal canal; the cremaster arises here in males")]),
24:dcard(24,'Rectus abdominis',[("📍 Where?","Beside the ventral midline; the linea alba splits the pair"),("⭐ Its sheath is formed by?","The fused aponeuroses of the abdominal muscles")]),
26:dcard(26,'Transversus abdominis',[("↔️ Fiber direction?","Transverse"),("📍 Layer?","Deepest abdominal muscle; spinal nerves run with its fibers")]),
29:dcard(29,'Superficial inguinal ring',[("📍 Formed by?","An opening in the aponeurosis of the external abdominal oblique"),("⭐ What passes through?","Male: vaginal tunic + spermatic cord · Female: vaginal process")],q='Identify the structure marked in green.'),
31:dcard(31,'Vaginal process (female; in the male = vaginal tunic)',[("📍 What is it?","Blind extension of peritoneum through the inguinal canal"),("⭐ What does it envelop?","Female: round ligament of the uterus · Male (vaginal tunic): spermatic cord"),("⭐ Also through the canal in both sexes?","External pudendal artery and vein + genitofemoral nerve")]),
33:dcard(33,'Inguinal ligament',[("📍 What is it?","Caudal border of the aponeurosis of the external abdominal oblique"),("⭐ Its ventral part lies between?","Superficial inguinal ring and vascular lacuna")],q='Identify the structure the blue lines point to.'),
35:dcard(35,'Vascular lacuna',[("📍 What is it?","Opening in the body wall where the femoral artery + vein first appear; base of the femoral triangle")],q='Identify the structure marked in green.'),
38:dcard(38,'Deep inguinal ring',[("📍 Formed by?","Ventral end of the inguinal ligament + caudal border of the internal abdominal oblique + lateral border of the rectus abdominis"),("⭐ Which side of the wall?","Inside: the internal entrance to the inguinal canal")],q='Identify the structure marked in green.'),
41:dcard(41,'Iliocostalis system',[("📍 Position?","Most ventral epaxial column"),("📏 Span?","Ilium to ribs 4-5")]),
43:dcard(43,'Longissimus system',[("📍 Position?","Middle epaxial column; partly covered by transversospinalis"),("📏 Span?","Ilium to the head")]),
45:dcard(45,'Transversospinalis system',[("📍 Position?","Most dorsal epaxial column"),("📏 Span?","Sacrum to the head")]),
47:dcard(47,'Splenius',[("📍 Deep to?","Rhomboideus + serratus dorsalis, in the cervical neck"),("🔪 Then?","Reflect it dorsally to reach semispinalis capitis")]),
49:dcard(49,'Semispinalis capitis',[("⭐ Made of which two muscles?","Biventer cervicis (dorsal) + complexus (ventral)"),("📍 Deep to?","Splenius")]),
51:dcard(51,'Biventer cervicis',[("📍 Position?","Dorsal part of semispinalis capitis")]),
53:dcard(53,'Complexus',[("📍 Position?","Ventral part of semispinalis capitis")]),
55:dcard(55,'Nuchal ligament',[("📍 Where?","Deep, between biventer cervicis and complexus; large + yellow"),("⭐ Continues caudally as?","Supraspinous ligament (T1 spinous process → caudal vertebrae)")]),
}
main=[('Neck + thorax',[d[k] for k in [5,7,9,11,12,14,15,17,18]]),
      ('Abdominal wall + inguinal region',[d[k] for k in [20,22,24,26,29,31,33,35,38]]),
      ('Epaxial muscles + dorsal neck',[d[k] for k in [41,43,45,47,49,51,53,55]])]

t=[tcard(1,'Identify the red structure.','Longus capitis'),
   tcard(2,'Identify the red AND green structures.','Red: longus capitis · Green: longus colli'),
   tcard(3,'Identify the red structure and the structure at marker 1.','Red: scalenus · 1: rectus thoracis',clue='Rectus thoracis is not a bold term'),
   tcard(4,'Identify the red structure.','Serratus ventralis',oia=True),
   tcard(5,'Identify the red structure.','Serratus dorsalis cranialis',[(FD,"Caudoventral")]),
   tcard(6,'Identify the red structure.','Serratus dorsalis caudalis',[(FU,"Cranioventral")],clue='Damaged during dissection'),
   tcard(7,'Name both muscle layers between the ribs and their fiber directions.','External intercostal muscles: caudoventral (superficial) · Internal intercostal muscles: cranioventral (deep)'),
   tcard(8,'Identify the red structure.','External abdominal oblique',[(FD,"Caudoventral")]),
   tcard(9,'Identify the structure at the black marker.','Superficial inguinal ring'),
   tcard(10,'Identify the red structure.','Internal abdominal oblique',[(FU,"Cranioventral")],clue='External abdominal oblique is reflected'),
   tcard(11,'Identify the red structure.','Transversus abdominis',[("↔️ Fiber direction?","Transverse")]),
   tcard(12,'Identify the red structure.','Rectus abdominis'),
   tcard(13,'Identify the red, green, AND gray columns.','Red: iliocostalis system · Green: longissimus system · Gray: transversospinalis system'),
   tcard(14,'Identify the red structure.','Iliocostalis thoracis (iliocostalis system)',clue='Inserts on the transverse process of C7'),
   tcard(15,'Identify the green structure.','Longissimus thoracis and cervicis (longissimus system)'),
   tcard(16,'Identify the red structure.','Splenius'),
   tcard(17,'Identify the red, green, AND gray columns.','Red: iliocostalis system · Green: longissimus system · Gray: transversospinalis system'),
   tcard(18,'Identify the structures at markers 1, 2, and 3.','1: longissimus capitis · 2: complexus · 3: biventer cervicis'),
   tcard(19,'Identify the yellow structure.','Nuchal ligament')]
pq=[img_card_facts('Identify the indicated (darker) muscle.',put(Q+'q1.jpg','lab14_pq1.jpg'),'Scalenus','',None,[("⚙️ Function?","Muscle of inspiration")],SP),
    img_card_facts('Identify the muscle in yellow at the arrow.',put(Q+'q5.jpg','lab14_pq5.jpg'),'Iliocostalis system (iliocostalis lumborum)','Green above it = longissimus',None,[("📍 Position?","Most ventral epaxial column")],SP)]
extra=[('Trunk slides · neck, thorax, abdomen',t[0:12]),('Trunk slides · epaxial + neck',t[12:19]),('Pre-lab 14 quiz images',pq)]

C=[("Axial muscles = ?","Muscles of the trunk and neck; divided into hypaxial and epaxial"),
("Epaxial muscles: where + main function?","Dorsal to the transverse processes of the vertebrae; mainly extend the vertebral column"),
("Hypaxial muscles = ?","All other trunk muscles: ventral to the transverse processes"),
("Superficial fascia of the trunk?","Covers the thorax + abdomen subcutaneously"),
("Deep fascia of the trunk is also called?","Thoracolumbar fascia; attaches to the ends of the spinous + transverse processes (thoracic + lumbar)"),
("Linea alba: what + where?","Midventral raphe of fused thoracolumbar fascia + abdominal aponeuroses; xiphoid process → symphysis pelvis"),
("Cremaster: where does it form?","From the caudal border of the internal abdominal oblique; runs with the vaginal tunic (males)"),
("Spermatic cord: where + covered by?","Runs through the inguinal canal in males, enveloped by the vaginal tunic"),
("Which structures pass through the inguinal canal in BOTH sexes?","External pudendal artery and vein + genitofemoral nerve"),
("Supraspinous ligament?","Caudal continuation of the nuchal ligament: spinous process of T1 → caudal vertebrae"),
("Male vs female: what passes through the superficial inguinal ring?","Male: vaginal tunic + spermatic cord · Female: vaginal process (around the round ligament of the uterus)"),
("Fiber direction: which run CAUDOVENTRAL?","External intercostals · external abdominal oblique · serratus dorsalis cranialis"),
("Fiber direction: which run CRANIOVENTRAL?","Internal intercostals · internal abdominal oblique · serratus dorsalis caudalis"),
("Epaxial columns from the spines toward the lateral wall?","Transversospinalis → longissimus → iliocostalis (I Love Tacos = ventral → dorsal)"),
("Which muscle forms the internal lamina of the rectus sheath at the umbilicus?","Transversus abdominis (origin includes lumbar transverse processes via the deep leaf of the thoracolumbar fascia)"),
("Serratus ventralis vs serratus dorsalis on a photo?","Slips converge on the scapula = ventralis · aponeurosis toward the dorsal midline = dorsalis"),
("Deep inguinal ring: 3 boundaries?","Ventral end of the inguinal ligament · caudal border of the internal abdominal oblique · lateral border of the rectus abdominis")]
TT=[text_card2(q,a,'🧠 Concept') for q,a in C]; TT[0]=TT[0].replace('class="card"','class="card on"',1)
open('site/gross-anatomy-lab14-terms.html','w').write(page('Lab 14 · No-Image Terms',f'{len(TT)} cards · definitions, male-only structures + integration',''.join(TT)))
write_lab(14,'Lab 14 · Trunk + Neck',main,extra,len(TT))
print(sum(len(g) for _,g in main),sum(len(g) for _,g in extra),len(TT))
