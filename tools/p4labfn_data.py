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

LABS[27]={'title':'Lab 27 · Pelvic limb nerves','src':'Pre-lab video · Lab 27 notes · Dr. Stueve lab slides','traps':[],'flags':[],
 'secs':[
  ('🟣 Plexus + trunk',[
   ('Lumbosacral plexus','Ventral branches of L3–S2 (L3 + S2 may or may not contribute) → nerves to body wall, pelvic limb, pelvic viscera, perineum',1),
   ('Lumbosacral trunk','L6, L7, S1 (+ part of S2) → cranial gluteal, caudal gluteal + sciatic nerves; a SUBSET of the plexus',1)]),
  ('🔵 Medial thigh',[
   ('Obturator nerve','L4–L6 → through the obturator foramen → adductor muscles (runs with the medial circumflex femoral branches)',1),
   ('Femoral nerve','Emerges from the iliopsoas → iliopsoas + all four heads of the quadriceps; gives off the saphenous nerve',1),
   ('Saphenous nerve','Branch of the femoral nerve; runs with the saphenous artery + medial saphenous vein → sartorius + skin of medial thigh, stifle, leg, paw',0)]),
  ('🟠 Pudendal + perineum',[
   ('Pudendal nerve','Sacral nerves; medial to the superficial gluteal, lateral to coccygeus/levator ani → 3 branches',1),
   ('Caudal rectal nerve','Most dorsal pudendal branch → external anal sphincter',1),
   ('Perineal nerves','Small branches → anus + perineum, continue to scrotum or labium',0),
   ('Dorsal nerve of the penis / clitoris','Most ventral pudendal branch → dorsum of the penis (with the dorsal artery of the penis) / clitoris',0),
   ('Caudal cutaneous femoral nerve','Sacral plexus; runs with the caudal gluteal artery, surfaces near the sacrotuberous ligament → skin of the caudal thigh (easy to cut when skinning)',1)]),
  ('🟢 Gluteal + sciatic',[
   ('Cranial gluteal nerve','Middle gluteal, deep gluteal + tensor fasciae latae (runs with the cranial gluteal artery)',1),
   ('Caudal gluteal nerve','Sole innervation of the superficial gluteal muscle',1),
   ('Sciatic nerve','Muscular branches to the hamstrings (biceps femoris, semitendinosus, semimembranosus) → divides into common fibular + tibial nerves. Avoid with IM injections',1),
   ('Common fibular nerve','Cranial division of the sciatic (L6, L7) → superficial + deep fibular nerves; gives the lateral cutaneous sural nerve',1),
   ('Lateral cutaneous sural nerve','Cutaneous branch of the COMMON FIBULAR nerve → skin of the lateral crus',1),
   ('Tibial nerve','Caudal division of the sciatic; between the 2 heads of the gastrocnemius → caudal crus muscles + plantar paw muscles; splits into medial + lateral plantar nerves',1),
   ('Caudal cutaneous sural nerve','Cutaneous branch of the TIBIAL nerve → skin of the caudal crus',1),
   ('Superficial fibular nerve','Runs with the cranial branch of the lateral saphenous vein → dorsal paw',0),
   ('Deep fibular nerve','Cranial crus muscles; runs with the cranial tibial artery (cut BOTH crural + tarsal extensor retinacula to follow it)',1)]),
  ('🔴 Pes vessels + tarsal tunnel',[
   ('Dorsal pedal artery','Cranial tibial artery simply RENAMED at the tarsus (no branch given off)',1),
   ('Arcuate artery','Small branch of the dorsal pedal → dorsal metatarsal arteries (smaller than the lab-guide figure shows)',0),
   ('Perforating branch','Of dorsal metatarsal artery II, between metatarsals II + III → deep plantar arch = main supply to the digits',1),
   ('Tarsal tunnel','Calcaneal tuber + sustentaculum tali + flexor retinaculum; carries the lateral digital flexor tendon, medial + lateral plantar nerves, caudal branch of the saphenous artery',1)])]}
LABS[28]={'title':'Lab 28 · Skull, teeth + hyoid','src':'Pre-lab video · Lab 28 notes','traps':[],'flags':[],
 'secs':[
  ('🦴 Skull regions + bones',[
   ('Cranium','Encloses the brain; its roof = calvaria',1),('Face','Bones around the respiratory + digestive entrances',0),
   ('Temporal bone','3 parts: squamous (forms the zygomatic arch), tympanic (tympanic bulla), petrous (houses the inner ear)',1),
   ('Zygomatic arch','Zygomatic process of the maxilla + zygomatic bone + zygomatic process of the temporal bone; origin of the masseter',1),
   ('Orbital ligament','Completes the incomplete bony orbit in the dog (complete in the cat)',1),
   ('Temporal fossa','Where the temporalis muscle lives',0),('Nasal aperture','Formed by the incisive + nasal bones',0),
   ('Hard palate','Incisive (rostral) + maxilla (middle) + palatine bone (caudal)',1),('Choanae','Caudal openings of the nasal cavity',0)]),
  ('🕳️ Foramina — what goes through',[
   ('Optic canal','Optic nerve; marks the start of the rostral cranial fossa',1),
   ('Orbital fissure','Oculomotor, trochlear, abducent nerves + ophthalmic nerve',1),
   ('Rostral alar foramen → alar canal → caudal alar foramen','Maxillary artery runs through the alar canal',1),
   ('Round foramen','Maxillary nerve from the cranial cavity into the alar canal',1),
   ('Oval foramen','Mandibular nerve (+ middle meningeal artery)',1),
   ('Maxillary foramen → infraorbital canal → infraorbital foramen','Infraorbital artery, vein + nerve',1),
   ('Sphenopalatine foramen','Into the nasal cavity (sphenopalatine vessels, caudal nasal nerve)',0),
   ('Caudal palatine foramen → major palatine foramen','Major palatine vessels + nerve to the hard palate',0),
   ('Hypoglossal canal','Hypoglossal nerve (cranial nerve XII)',1),
   ('Jugular foramen','Cranial nerves IX, X, XI + sigmoid sinus',0),
   ('Internal acoustic meatus','Facial + vestibulocochlear nerves',0),
   ('Canal for the trigeminal nerve','Houses the trigeminal ganglion',0),
   ('Stylomastoid foramen','Facial nerve exits (between the mastoid process + external acoustic meatus)',0),
   ('Mandibular foramen → mandibular canal → mental foramina','Inferior alveolar vessels + nerve → lower lip + chin',1),
   ('Cribriform plate','Holes for olfactory nerves (nasal → cranial cavity)',1),
   ('Foramen magnum','Spinal cord exits',0)]),
  ('🧠 Cranial fossae',[
   ('Rostral cranial fossa','Cribriform plate → optic canal; olfactory bulbs + rostral frontal lobes',1),
   ('Middle cranial fossa','Orbital fissure → dorsum sellae; contains the sella turcica (pituitary)',1),
   ('Sella turcica','Hypophyseal fossa + dorsum sellae; houses the pituitary',1),
   ('Caudal cranial fossa','Dorsum sellae / petrous part → foramen magnum',1),
   ('Tentorium osseum vs tentorium cerebelli','Bony shelf vs dura mater attached to it; separates cerebrum from cerebellum',1)]),
  ('👂 Ear',[
   ('Ossicles','Malleus (on the tympanic membrane) → incus (middle) → stapes (footplate in the vestibular window)',1),
   ('Promontory','Bulge in the tympanic bulla; holds the cochlear window (membrane-closed); vestibular window is dorsal to it',1)]),
  ('🦷 Teeth + mandible',[
   ('Dental formula (each side)','Upper: 3 incisors, 1 canine, 4 premolars, 2 molars · Lower: 3 incisors, 1 canine, 4 premolars, 3 molars',1),
   ('Shearing (carnassial) teeth','Upper 4th premolar (3 roots) + lower 1st molar — cut meat',1),
   ('Cheek teeth','Premolars + molars',0),
   ('Interalveolar vs interradicular septa','Between 2 teeth vs between 2 roots of ONE tooth',1),
   ('Tooth surfaces','Vestibular (outside) · lingual (lower, tongue side) · palatine (upper, inside) · mesial (toward 1st incisor) · distal (away) · occlusal (bite)',1),
   ('Condylar process','Articulates with the mandibular fossa = temporomandibular joint',1),
   ('Coronoid process','Temporalis muscle attachment',0),('Masseteric fossa','Masseter attachment on the ramus',0)])]}
LABS[29]={'title':'Lab 29 · Nose, face, eye, mouth + pharynx','src':'Pre-lab video · Lab 29 notes','traps':[],'flags':[],
 'secs':[
  ('👃 Nasal cavity',[
   ('Nasal septum','Separates left + right nasal cavities; cartilaginous rostrally, bony caudally',0),
   ('Conchae','Scrolls (turbinates): dorsal, ventral (more extensive), ethmoidal',0),
   ('Dorsal / middle / ventral nasal meatus','Nasal bone↔dorsal concha · dorsal↔ventral concha · ventral concha↔hard palate',1),
   ('Common nasal meatus','Vertical space beside the septum joining all meatuses',1),
   ('Paranasal sinuses (dog)','ONLY 2: frontal sinus + maxillary recess',1),
   ('Lateral nasal gland','Occupies the maxillary recess',0),
   ('Vomeronasal organ','Pheromone chemosensation; dorsal to the hard palate; drains via the incisive duct at the incisive papilla',0)]),
  ('😶 Face muscles (facial nerve)',[
   ('Platysma','Cutaneous muscle of head + neck',0),('Orbicularis oris','Closes the lips (round muscle around the mouth)',0),
   ('Buccinator','Returns food from the vestibule to the occlusal surfaces',1),
   ('Levator nasolabialis','Raises the upper lip + dilates the nostril',0),
   ('Orbicularis oculi','Closes the eyelids',1),
   ('Retractor anguli oculi lateralis','At the lateral commissure (near the angularis oculi vein)',0),
   ('Levator palpebrae superioris','Raises the upper lid — OCULOMOTOR nerve (not facial)',1),
   ('Scutiform cartilage','Boot-shaped; rostral + caudal auricular muscles attach',0)]),
  ('👁️ Eye + tears',[
   ('Palpebral fissure','Opening between the eyelids',0),
   ('Medial palpebral ligament','Better developed than the lateral',1),
   ('Conjunctival fornix','Where palpebral meets bulbar conjunctiva (full 360°)',1),
   ('Lacrimal caruncle','Medial triangular thickening; pools tears',0),
   ('Tear drainage','Lacrimal punctum → lacrimal canaliculus → lacrimal sac → nasolacrimal duct → opening at the ventral alar fold (rostral ventral nasal meatus)',1),
   ('Clinical: fluorescein','Exits at the nostril via the nasolacrimal duct opening',1),
   ('Third eyelid','Superficial gland of the third eyelid contributes tears',0)]),
  ('👅 Mouth + salivary',[
   ('Parotid duct','Opens at the papilla by the upper 4th premolar',1),
   ('Zygomatic ducts','Open by the last upper molar',1),
   ('Mandibular + major sublingual ducts','Run in the sublingual fold → open at the sublingual caruncle',1),
   ('Parotid lymph node','Rostral to the parotid salivary gland',0),
   ('Papillae','Filiform (body + apex) · conical (root) · fungiform (spots) · vallate (root, circular) · foliate (lateral root)',1),
   ('Lyssa','Fibrous rod on the ventral midline of the tongue apex; drinking/lapping',0)]),
  ('🔁 Pharynx',[
   ('Oropharynx','Palatoglossal arch → palatopharyngeal arch',1),
   ('Nasopharynx','Choanae → palatopharyngeal arch; auditory tube opens here',1),
   ('Laryngopharynx','Dorsal to the larynx → pharyngoesophageal limen (start of the esophagus)',1),
   ('Palatine tonsil','Under the semilunar fold in the oropharynx',0),
   ('Pharyngeal constrictors (rostral → caudal)','Hyopharyngeus → thyropharyngeus → cricopharyngeus (HTC); cricopharyngeus continues into the esophagus',1),
   ('Cranial laryngeal nerve','Passes between the hyopharyngeus (cranial) + thyropharyngeus (caudal)',1)])]}

def build_rest(): return {}
