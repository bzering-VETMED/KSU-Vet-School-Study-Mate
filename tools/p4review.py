"""Practical 4 · 🎯 'Likely on the practical' deck built from the Nov 8 review-session transcript (Lab 29 heads).  Made by Claude.
What the professor walked through + asked out loud = what he tags. Photo = the matching Lab 29 Head slide (Dr. Stueve).
  python3 tools/p4review.py   → gross-anatomy-p4-review.html, linked on the Practical 4 page + Lab 29 hub."""
import sys,os,html,re,time
sys.path.insert(0,'tools')
import p4lab26 as B
E=html.escape; V=str(int(time.time()))
def img(n): 
    f=f'assets/p4_l29s_{n}.jpg'; return f if os.path.exists(f) else None
def C(q,ans,facts=(),slide=None,kind='structure'):
    tag={'structure':'🔎 identify the STRUCTURE','space':'🕳️ identify the SPACE','concept':'🧠 concept','path':'➡️ pathway'}[kind]
    nm=f'<div class="nm">{E(ans)}</div>'
    if slide and img(slide):
        h=B.card(q,f'{tag} · Lab 29 slide #{slide}',img(slide),nm,facts)
    else:
        fx=''.join(f'<div class="fx"><b>{E(k)}</b> {E(v)}</div>' for k,v in facts if v)
        h=(f'<section class="card"><div class="q">{E(q)}<span class="tagline">{E(tag)}</span></div>'
           f'<div class="stg ans"><div class="pr">❓ Say it out loud first</div><div class="an">{nm}{fx}</div></div><div class="rev">💗 TAP TO REVEAL</div></section>')
    return dict(name=ans,terms=[],html=h)
R=[
 C('Identify the midline groove of the upper lip / nose.','Philtrum',[('Why it matters:','an incision through it leads straight to the nasal septum')],41),
 C('What is the nasal septum made of — rostrally vs caudally?','Rostrally CARTILAGINOUS (septal cartilage) · caudally BONY',[('Ventral part:','the vomer forms the ventral midline'),('Job:','splits the nasal cavity into right + left halves')],25,'concept'),
 C('Identify the tagged bony scroll (be specific).','Ventral nasal concha',[('Trap:','say "ventral nasal concha", not just "concha"'),('Looks like:','straight shelf rostrally, complex scrolls caudally')],14),
 C('Identify the tagged shelf (smaller, single).','Dorsal nasal concha',[('3 kinds of conchae:','dorsal · ventral · ethmoidal (from the ethmoid bone)')],12),
 C('Identify the SPACE.','Dorsal nasal meatus',[('Between:','nasal bone ↔ dorsal nasal concha')],27,'space'),
 C('Identify the SPACE.','Middle nasal meatus',[('Between:','dorsal nasal concha ↔ ventral nasal concha')],29,'space'),
 C('Identify the SPACE.','Ventral nasal meatus',[('Between:','ventral nasal concha ↔ hard palate'),('Clinical:','aim the nasogastric tube here')],31,'space'),
 C('Identify the SPACE.','Common nasal meatus',[('Between:','nasal septum ↔ the conchae; all 3 meatuses open into it')],33,'space'),
 C('Identify the caudal opening of the nasal cavity.','Choanae',[('Trap:','CHOANAE = opening (where the hard palate ends) · CONCHAE = bony scrolls'),('Marks:','end of the nasal cavity, start of the nasopharynx')],6),
 C('Trace a nasogastric tube from the nostril to the esophagus.','Nostril → ventral nasal meatus → choanae → nasopharynx → intrapharyngeal ostium → esophagus',[],None,'path'),
 C('Identify the SPACE caudal to the choanae.','Nasopharynx',[],175,'space'),
 C('Identify the arch from the soft palate to the pharynx wall.','Palatopharyngeal arch',[('Its opening:','intrapharyngeal ostium (the NG tube + probe pass through it)')],177),
 C('Name the 3 parts of the pharynx + its rostral and caudal borders.','Nasopharynx · oropharynx · laryngopharynx',[('Rostral borders:','choanae (nasopharynx) + palatoglossal arch (oropharynx)'),('Oropharynx ends:','at the tip of the epiglottis'),('Caudal border:','pharyngoesophageal limen')],None,'concept'),
 C('Identify the fold that ends the oral cavity.','Palatoglossal arch (fold)',[('Rostral to it:','oral cavity · caudal to it: oropharynx')],116),
 C('Identify the tagged ridge (end of the laryngopharynx).','Pharyngoesophageal limen',[('Rostral:','laryngopharynx · caudal: esophagus')],183),
 C('Identify the lymphatic structure in the oropharynx wall.','Palatine tonsil',[('Correction he made:','PALATINE tonsil (not pharyngeal); cigar-shaped'),('Covered by:','the semilunar fold')],167),
 C('Identify the fold covering the tonsil.','Semilunar fold',[],169),
 C('Identify the opening in the nasopharynx.','Auditory tube (opening)',[('Connects:','middle ear (tympanic cavity) ↔ NASOPHARYNX'),('Also called:','Eustachian tube — ear "popping"')],179),
 C('Which tongue papillae are purely MECHANICAL (non-gustatory)?','Filiform + conical papillae',[('Gustatory (taste):','fungiform, vallate, foliate'),('Foliate:','poorly developed in the dog')],126,'concept'),
 C('Identify the tagged papillae (scattered dots).','Fungiform papillae',[],129),
 C('Identify the fold under the tongue (tongue-tie).','Lingual frenulum',[('Connects:','ventral tongue ↔ floor of the oral cavity')],135),
 C('Identify the tagged papilla on the floor of the mouth.','Sublingual caruncle',[('Ducts that open here:','mandibular duct + major sublingual duct')],139),
 C('Where does the PAROTID duct open?','On a small papilla in the vestibule dorsal to the upper 4th premolar',[('Compare:','mandibular + sublingual ducts → sublingual caruncle (floor)')],155,'concept'),
 C('Identify the papilla just caudal to the upper incisors.','Incisive papilla',[('Openings here:','incisive ducts (vomeronasal organ connection)'),('Also on the roof:','transverse ridges = rugae (palatine rugae)')],161),
 C('Identify the muscle around the eye / around the mouth.','Orbicularis oculi · orbicularis oris',[('Also seen:','zygomaticus, levator nasolabialis'),('Innervation type:','SPECIAL visceral efferent (branchial arch muscles of facial expression) — facial nerve')],95),
 C('Identify the SPACE between the lips and the teeth.','Labial vestibule (oral vestibule)',[('Between cheek + teeth:','buccal vestibule'),('What separates vestibule from oral cavity proper:','the dental arcades (teeth)')],47,'space'),
 C('Identify the SPACE inside the dental arcades.','Oral cavity proper',[],114,'space'),
 C('Identify the muscle forming the wall of the cheek.','Buccinator muscle',[('Bounds:','the buccal vestibule')],None),
 C('Identify the tagged gland (large, caudal).','Mandibular salivary gland',[('Shares a capsule with:','monostomatic (major) sublingual gland, just rostral to it')],147),
 C('Identify the gland just rostral to the mandibular gland.','Sublingual gland (major / monostomatic)',[('Minor (polystomatic) sublingual:','scattered in the floor of the mouth, short ducts — not visible')],149),
 C('Identify the gland around the base of the ear.','Parotid salivary gland',[('Name:','para = around + oto = ear')],151),
 C('Identify the angle where upper + lower lips meet.','Commissure of the lips (labial commissure)',[],None),
 C('Identify the tagged corner of the eyelids (be specific).','Lateral palpebral commissure (lateral canthus)',[('Other side:','medial palpebral commissure (medial canthus)')],71),
 C('Identify the opening between the eyelids.','Palpebral fissure',[('Leads into:','the conjunctival sac')],67),
 C('Identify the SPACE the probe is in (eye).','Conjunctival sac',[],82,'space'),
 C('Identify the dead end where palpebral + bulbar conjunctiva meet.','Fornix (conjunctival fornix)',[],80,'space'),
 C('Identify the tiny opening at the medial canthus.','Lacrimal punctum (superior or inferior)',[('Say which:','superior lacrimal punctum (upper lid) / inferior lacrimal punctum (lower lid)')],86),
 C('Name the 2 surfaces of the third eyelid + what covers them.','Palpebral surface + bulbar surface',[('Trap:','BOTH are covered by PALPEBRAL conjunctiva')],92,'concept'),
 C('Trace a tear from the gland to the nose.','Lacrimal gland (+ gland of the third eyelid) → conjunctival sac → superior/inferior lacrimal punctum → lacrimal canaliculi → lacrimal sac → nasolacrimal duct → opening in the nasal vestibule',[],173,'path'),
 C('Identify the tagged muscles + the cartilage they attach to.','Rostral + caudal auricular muscles → scutiform cartilage',[('Ear cartilage itself:','auricular cartilage (annular cartilage comes later)')],102),
 C('Identify the muscle filling the temporal fossa.','Temporalis muscle',[],None),
 C('Skull station format — what will he ask?','"Identify the foramen / opening" + "which cranial nerve (NAME + NUMBER) exits the tagged foramen"',[('Optic canal:','optic nerve (II)'),('Orbital fissure:','oculomotor (III), trochlear (IV), ophthalmic (V1), abducent (VI)'),('Round foramen:','maxillary nerve (V2)'),('Oval foramen:','mandibular nerve (V3)'),('Stylomastoid foramen:','facial nerve (VII)'),('Internal acoustic meatus:','facial (VII) + vestibulocochlear (VIII)'),('Jugular foramen:','glossopharyngeal (IX), vagus (X), accessory (XI)'),('Hypoglossal canal:','hypoglossal nerve (XII)'),('Cribriform plate:','olfactory nerve (I)')],None,'concept'),
]
B.write_deck('gross-anatomy-p4-review.html','🎯 Practical 4 · Review-session must-knows',
 'From the Nov 8 review (Lab 29 heads). Station = 4–5 tags → discuss → answer alone. Read the stem: SPACE vs STRUCTURE.',R,'gross-anatomy-practical4.html')
h=open('gross-anatomy-p4-review.html').read().replace('← Back to Lab hub','← Back to Practical 4'); open('gross-anatomy-p4-review.html','w').write(h)
p=open('gross-anatomy-practical4.html').read()
p=re.sub(r'<!--rev-->.*?<!--/rev-->','',p,flags=re.S)
link=f'<!--rev--><a href="gross-anatomy-p4-review.html?v={V}">🎯 Review-session must-knows (likely on the practical)</a><!--/rev-->'
p=p.replace('<a href="gross-anatomy-lab26-images.html',link+'<a href="gross-anatomy-lab26-images.html',1)
open('gross-anatomy-practical4.html','w').write(p)
print(len(R),'cards')
# link from the Lab 29 hub's study-pages row (re-run this script after rebuilding Lab 29 / p4labfn)
h=open('gross-anatomy-lab29-images.html').read()
h=re.sub(r'<a href="gross-anatomy-p4-review\.html[^"]*">.*?</a>','',h)
h=h.replace('</div><!--/fn-->',f'<a href="gross-anatomy-p4-review.html?v={V}">🎯 Review-session must-knows<span>likely on the practical</span></a></div><!--/fn-->',1)
open('gross-anatomy-lab29-images.html','w').write(h)
