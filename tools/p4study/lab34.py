from build import build_items
import pymupdf as fz
from isolate import isolate,find_rects,find_phrase
L34='/mnt/user-data/attachments/31594bc3-9d6f-5c02-a55e-32953ff4d455/eacfa4d6-Lab_34.pdf'
def G1(pg,labels,clip,phrase=False):
    within=fz.Rect(clip.x0-90,clip.y0-40,clip.x1+90,clip.y1+40)
    rs=[r for l in labels for r in (find_phrase(L34,pg,l,within) if phrase else find_rects(L34,pg,l,within))[:1]]
    assert len(rs)==len(labels),labels
    out=f'/home/claude/studysheets/iso/l34_{pg}_{"_".join(labels).replace(" ","_")}.png'; isolate(L34,pg,rs,out,clip=clip,dpi=200); return out
F61=fz.Rect(165,406,453,575); F64=fz.Rect(100,64,451,238)
I='/home/claude/studysheets/img34/'
D='📚 course slide · Lab 34 slides #'; G='📖 lab guide · Lab 34 notes, '
F1='Fig. 6-1 (meninges, median plane)'; F4='Fig. 6-4 (cervical vertebral veins)'
H='highlighted on the photo'
items=[
('meninges',G1(2,['5','6','8'],F61),'#5 dura, #6 arachnoid, #8 pia',G+F1,'The <b>3 connective-tissue coverings</b> of the brain and spinal cord, from outside in: <b>dura mater, arachnoid, pia mater</b>.'),
('dura mater',I+'s4.jpg',H,D+'4','The <b>thickest, outermost</b> meninx, fused to the inside of the cranium. Its folds are the falx cerebri and the tentorium cerebelli.'),
('longitudinal cerebral fissure',I+'s6.jpg',H,D+'6','The deep <b>midline groove that separates the left and right cerebral hemispheres</b>. The falx cerebri sits in it.'),
('falx cerebri',I+'s8.jpg',H,D+'8','A <b>dura fold in the longitudinal fissure</b> between the hemispheres. Its attached dorsal edge holds the <b>dorsal sagittal sinus</b>.'),
('pia mater',G1(2,['8'],F61),'#8 (the thin layer on the brain surface)',G+F1,'The <b>innermost</b> meninx, stuck directly to the brain. It follows the brain <b>down into every sulcus</b>.'),
('arachnoid',G1(2,['6'],F61),'#6 (arachnoid + its trabeculae)',G+F1,'The <b>middle</b> meninx, lining the dura. It bridges over the sulci and does not dip into them. Under it is the <b>subarachnoid space</b> full of cerebrospinal fluid (#7).'),
('leptomeninges',I+'s11.jpg','the thin layer the probe is lifting',D+'11','<b>Arachnoid + pia mater</b> together. In embalmed brains they are collapsed onto each other, which is what the probe lifts here.'),
('pachymeninges',I+'s13.jpg',H,D+'13','Another name for the <b>dura mater</b>. Think "pachy = thick."'),
('cerebellomedullary cistern',G1(2,['14'],F61),'#14 (between the cerebellum and the medulla)',G+F1,'The <b>largest subarachnoid cistern</b>, in the angle between the <b>cerebellum and medulla</b>. This is where you do a cisterna magna CSF tap.'),
('basilar artery',I+'s16.jpg',H,D+'16','The single artery on the <b>ventral midline of the brainstem</b>, formed by the <b>vertebral arteries</b> joining. It runs rostrally to the arterial circle.'),
('vertebral arteries',I+'s18.jpg',H,D+'18','Branches of the <b>subclavian</b> that run up the transverse foramina and enter the vertebral canal. They form the <b>basilar artery</b>.'),
('ventral spinal artery',I+'s20.jpg',H,D+'20','Continues <b>caudally from the vertebral/basilar junction</b> along the ventral midline of the spinal cord.'),
('internal carotid arteries',I+'s22.jpg',H,D+'22','The other main blood supply to the brain (besides the vertebrals). They enter the skull and join the <b>arterial circle</b> beside the hypophysis.'),
('caudal communicating arteries',I+'s24.jpg',H,D+'24','They come off the internal carotid and run <b>caudally to join the basilar artery</b>, closing the back half of the circle.'),
('cerebral arterial circle',I+'s26.jpg',H,D+'26','The arterial ring <b>around the hypophysis</b> (circle of Willis): internal carotids + caudal communicating arteries + basilar artery + their branches.'),
('rostral cerebral artery',I+'s28.jpg',H,D+'28','Runs <b>forward into the longitudinal fissure</b> and over the corpus callosum. It supplies the medial cerebrum.'),
('middle cerebral artery',I+'s30.jpg',H,D+'30','Runs <b>laterally, rostral to the piriform lobe</b>, then spreads over the whole <b>lateral cerebrum</b>. It is the biggest branch.'),
('caudal cerebral artery',I+'s32.jpg',H,D+'32','Comes off the <b>caudal communicating artery</b>, <b>rostral to the oculomotor nerve</b>, and dives deep to the <b>caudal cerebrum</b>.'),
('rostral cerebellar artery',I+'s34.jpg',H,D+'34','Leaves the <b>caudal third of the arterial circle, caudal to the oculomotor nerve</b>, and runs along the pons to the cerebellar hemisphere. Watch the spelling: cerebell<b>ar</b> vs cerebr<b>al</b>.'),
('caudal cerebellar artery',I+'s36.jpg',H,D+'36','A branch of the <b>basilar artery</b> going to the <b>caudal cerebellum</b>.'),
('dorsal sagittal sinus',I+'s38.jpg',H,D+'38','The venous sinus in the <b>attached dorsal edge of the falx cerebri</b>. It drains caudally into the <b>transverse sinuses</b>.'),
('transverse sinus',I+'s40.jpg',H,D+'40','Paired sinuses that run <b>transversely in the bony transverse canal</b>. Each one splits into the <b>temporal sinus and the sigmoid sinus</b>.'),
('temporal sinus',I+'s42.jpg',H,D+'42','From the transverse sinus to the <b>retroarticular foramen</b>. There it becomes an emissary vein that joins the <b>maxillary vein</b>.'),
('sigmoid sinus',I+'s44.jpg',H,D+'44','The <b>S-shaped</b> continuation of the transverse sinus. It curves over the <b>petrous temporal bone</b> and passes through the <b>jugular foramen</b> into the tympano-occipital fissure.'),
('cavernous sinus',I+'s48.jpg',H,D+'48','On each side of the <b>floor of the middle cranial fossa</b>, beside the hypophysis. It drains caudally as the <b>ventral petrosal sinus</b>.'),
('ventral petrosal sinus',I+'s46.jpg',H,D+'46','Continues caudally from the <b>cavernous sinus</b> through the petro-occipital canal and joins the <b>sigmoid sinus</b>.'),
('ventral internal vertebral venous plexuses',I+'s50.jpg',H,D+'50','Paired venous channels on the <b>floor of the vertebral canal</b>. They collect blood from the skull sinuses and run down the spine.'),
('intervertebral veins',G1(5,['Intervertebral vein III'],F64,True),'"Intervertebral vein III"',G+F4,'At each <b>intervertebral foramen</b> they connect the internal vertebral plexus to the vertebral vein. Only find them if they are already exposed.'),
]
build_items(34,'Meninges + blood supply',items)
