"""Practical 4 · functions-page data per lab (made by Claude). Rows = (item, function/supply, starred).
Star = professor emphasis (pre-lab video transcript, Lab N notes PDF, quiz/Kahoot)."""
LABS={
26:{'title':'Lab 26 · Pelvic limb vessels','src':'Pre-lab video · Lab 26 notes · Dr. Stueve lab slides',
 'traps':['Supply ≠ course: the transverse branch of the medial circumflex femoral supplies the adductor but ENDS in the semimembranosus.',
          'Lateral circumflex femoral = biggest single supply to the coxal (hip) joint capsule — not the medial circumflex femoral.',
          'Main blood to the pes = cranial tibial → dorsal pedal → dorsal metatarsal artery II → perforating branch → deep plantar arch → plantar metatarsals. The saphenous branches are collateral routes.',
          'Cranial gluteal NERVE supplies middle + deep gluteals AND continues to the tensor fasciae latae.'],
 'flags':[('⚠️ Source disagreement · femoral branch order','Slide 26 lists: superficial circumflex "femoral" (typo for iliac), proximal caudal femoral, saphenous, descending genicular, middle caudal femoral, distal caudal femoral (no lateral circumflex femoral). Slide 50: descending genicular arises DISTAL to the saphenous. The video names the descending genicular before the saphenous. Learn the slide order; confirm in lab.'),
          ('⚠️ Source disagreement · lateral saphenous venipuncture','Slides 44–48 + video: the CRANIAL BRANCH is the most common site. Lab 26 notes #8: the straight section PROXIMAL to where the cranial + caudal branches join is best for larger needles or fluid volume (it may contain valves).'),
          ('⚠️ Variation · dorsal perineal artery','Not in the lab-guide figure. Size is inversely related to the ventral perineal; it usually comes off the caudal gluteal just distal to the lateral caudal artery and can reinforce or replace the caudal rectal artery (Lab 26 notes #2).')],
 'secs':[
  ('🔴 Gluteal region',[
   ('Internal pudendal artery','Pelvic viscera (smaller terminal branch of the internal iliac)',1),
   ('Caudal gluteal artery','Larger terminal branch of the internal iliac → gluteal region + caudal thigh; gives the iliolumbar + cranial gluteal arteries',1),
   ('Iliolumbar artery','Deep surface of the cranial end of the middle gluteal muscle (ilium region)',0),
   ('Cranial gluteal artery','Middle + deep gluteal muscles',0),
   ('Cranial gluteal nerve','Motor → middle gluteal, deep gluteal + tensor fasciae latae',1),
   ('Umbilical artery','Runs in the lateral ligament of the bladder',0)]),
  ('🟣 Deep femoral system',[
   ('Deep femoral artery','Only branch of the external iliac → pudendoepigastric trunk, then continues as the medial circumflex femoral',1),
   ('Pudendoepigastric trunk','Short common trunk → external pudendal + caudal epigastric arteries',1),
   ('External pudendal artery','Leaves the abdomen via the inguinal canal (superficial inguinal ring) → inguinal region',0),
   ('Caudal epigastric artery','Caudal half of the rectus abdominis + central parts of the oblique + transverse abdominal muscles',0),
   ('Medial circumflex femoral artery','Adductor region, medial + caudal thigh muscles (via deep + transverse branches)',1),
   ('Deep branch (medial circumflex femoral)','Descends between the adductor + vastus medialis → deep thigh muscles',0),
   ('Transverse branch (medial circumflex femoral)','Supplies the adductor; terminates in the semimembranosus',0)]),
  ('🟢 Femoral artery branches',[
   ('Femoral artery','Main arterial supply of the pelvic limb; pulse palpated in the femoral triangle',1),
   ('Femoral triangle','Clinical: palpation site for the femoral pulse',1),
   ('Superficial circumflex iliac artery','Sartorius, tensor fasciae latae, rectus femoris',0),
   ('Lateral circumflex femoral artery','Quadriceps (between rectus femoris + vastus medialis) + more blood to the coxal joint capsule than any other single vessel',1),
   ('Proximal caudal femoral artery','Caudal thigh muscles (mid-thigh)',0),
   ('Saphenous artery','Skin of the medial stifle; continues as cranial + caudal branches to the paw',1),
   ('Cranial branch (saphenous artery)','Medial crus → flexor surface of the tarsus → dorsal common digital arteries',0),
   ('Caudal branch (saphenous artery)','Through the tarsal tunnel → deep branches → plantar surface of the paw (plantar common digital arteries)',0),
   ('Descending genicular artery','Medial surface of the stifle',0),
   ('Middle caudal femoral artery','Semimembranosus + caudal thigh muscles',0),
   ('Distal caudal femoral artery','Large vessel → gastrocnemius + caudal thigh/stifle region',0)]),
  ('🟠 Popliteal + crus',[
   ('Popliteal artery','Continuation of the femoral after the distal caudal femoral → stifle → splits into cranial + caudal tibial',1),
   ('Caudal tibial artery','Tiny branches into the popliteus (rarely found)',0),
   ('Cranial tibial artery','Craniolateral crus muscles → continues as the dorsal pedal artery = MAIN supply to the pes',1)]),
  ('🔵 Veins + nerves',[
   ('Medial saphenous vein','Satellites the saphenous artery; venipuncture site in CATS',1),
   ('Lateral saphenous vein','No satellite artery; cranial branch = most common venipuncture site in DOGS',1),
   ('Saphenous nerve','Sensory (branch of the femoral nerve) to the skin of the medial thigh, stifle, crus + paw',0),
   ('Caudal cutaneous sural nerve','Nerve-biopsy site near the lateral saphenous vein — mixed fibers, partial plantar motor → no obvious deficit',1),
   ('Deep branch (common peroneal nerve)','Runs with the cranial tibial artery under the cranial tibial + long digital extensor muscles',0)])]}
}
def build_rest(): return {}
