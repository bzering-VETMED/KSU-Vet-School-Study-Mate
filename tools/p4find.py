"""Practical 4 · Lab 28 '📍 Find it' cards for bold terms the lab-guide drawings show but don't label (made by Claude, Nov 7).
Practical format = 'locate these' stations, so the card names the terms and the reveal says where each one is.
Drawings: Lab 28 notes PDF Figs. 5-14/5-15 (cranial cavity) and 5-11 (teeth)."""
import sys,html
sys.path.insert(0,'tools')
import pymupdf as fz
from PIL import Image
import p4lab26 as B
E=html.escape
PDF='/mnt/user-data/attachments/31594bc3-9d6f-5c02-a55e-32953ff4d455/f954b1d8-Lab_28.pdf'
def crop(pg,y0,y1,out,x0=0,x1=1):
    p=fz.open(PDF)[pg-1]; r=p.rect
    pm=p.get_pixmap(dpi=200,clip=fz.Rect(r.width*x0,r.height*y0,r.width*x1,r.height*y1))
    Image.frombytes('RGB',(pm.width,pm.height),pm.samples).save(out,quality=90); return out
def fcard(q,img,rows,terms,src):
    ans=''.join(f'<div class="fx"><b>{E(k)}:</b> {E(v)}</div>' for k,v in rows)
    return dict(name=q,terms=terms,html=B.card('📍 Find + point to: '+q,f'📖 lab guide drawing · {src}',img,ans))
def build():
    d=crop(11,0.06,0.58,'assets/p4find_58.jpg'); e=crop(5,0.36,0.78,'assets/p4find_53.jpg')
    a=crop(16,0.06,0.57,'assets/p4find_514.jpg'); b=crop(16,0.57,0.95,'assets/p4find_515.jpg'); c=crop(13,0.06,0.62,'assets/p4find_511.jpg')
    return [
     fcard('ossicles · inner ear · tympanic part of the temporal bone',d,[
        ('Ossicles','the 3 middle-ear bones: malleus (on the tympanic membrane) → incus (middle) → stapes (footplate in the vestibular window)'),
        ('Inner ear','inside the petrous part of the temporal bone: cochlea (cochlear duct) + vestibule (utricle, saccule) + semicircular canals/ducts'),
        ('Tympanic part (temporal bone)','the part that forms the tympanic bulla + bony external acoustic meatus (the big rounded chamber in this drawing)')],
        ['ossicles','inner ear','tympanic part (temporal bone)'],'Fig. 5-8, middle + inner ear'),
     fcard('skull · cranium · face · nasal aperture · orbital margin · pterygopalatine fossa',e,[
        ('Skull','all the bones of the head (cranium + face), with the mandibles + hyoid'),
        ('Cranium','the braincase: the caudal part enclosing the brain (frontal, parietal, occipital, temporal bones…)'),
        ('Face','the rostral part: nasal cavity, jaws, orbits (incisive, nasal, maxilla, palatine, zygomatic, lacrimal…)'),
        ('Nasal aperture','the rostral opening of the bony nasal cavity, framed by the nasal + incisive bones at the tip of the muzzle'),
        ('Orbital margin','the bony rim around the orbit (frontal, lacrimal, zygomatic bones; open caudally where the orbital ligament spans it)'),
        ('Pterygopalatine fossa','the depression ventral to the orbit, between the maxilla and the pterygoid/palatine region (medial pterygoid muscle arises here)')],
        ['skull','cranium','face','nasal aperture','orbital margin','pterygopalatine fossa'],'Fig. 5-3, skull lateral view'),
     fcard('rostral, middle + caudal cranial fossae · sella turcica',a,[
        ('Rostral cranial fossa','the front of the cranial floor, over the cribriform plate + presphenoid (holds the olfactory bulbs + frontal lobes)'),
        ('Middle cranial fossa','the middle of the floor, at the hypophyseal fossa, optic canal, orbital fissure, round + oval foramina (temporal lobes, pituitary)'),
        ('Caudal cranial fossa','the back of the floor, behind the dorsum sellae and petrosal crest: cerebellar fossa, internal acoustic meatus, jugular foramen, hypoglossal canal'),
        ('Sella turcica','the "Turkish saddle" in the middle fossa = hypophyseal fossa (seat) + dorsum sellae (back); holds the pituitary gland')],
        ['rostral cranial fossa','middle cranial fossa','caudal cranial fossa','sella turcica'],'Fig. 5-14, skull with calvaria removed'),
     fcard('tentorium cerebelli · transverse canal · foramen for the dorsal sagittal sinus',b,[
        ('Tentorium osseum (labeled)','the bony shelf on the inside of the calvaria between cerebrum + cerebellum'),
        ('Tentorium cerebelli','the dura mater fold attached to the tentorium osseum (soft tissue, so not drawn): it separates the cerebrum from the cerebellum'),
        ('Transverse canal (labeled)','runs side to side through the occipital region at the transverse groove, for the transverse sinus'),
        ('Foramen for the dorsal sagittal sinus','small opening in the midline at the top of the occipital bone, just above the transverse canal, where the dorsal sagittal sinus enters it')],
        ['tentorium cerebelli','transverse canals','foramen for the dorsal sagittal sinus'],'Fig. 5-15, sagittal section of skull'),
     fcard('crown, root, neck · tooth surfaces · alveolar border · interalveolar + interradicular septa',c,[
        ('Crown','the enamel-covered part above the gum'),('Root','the part set in the alveolus (socket), covered by cementum'),
        ('Neck of tooth','where crown meets root = the cementoenamel junction, at the gum line'),
        ('Vestibular surface','faces the lips + cheeks (vestibule)'),('Lingual surface','faces the tongue (lower teeth)'),('Palatine surface','faces the hard palate (upper teeth)'),
        ('Contact surfaces','face the neighboring teeth: mesial contact surface = toward the midline/front of the arcade · distal surface = away from it'),
        ('Occlusal or masticating surface','the biting surface that meets the opposite arcade (Fig. B, shearing teeth)'),
        ('Alveolar border','the rim of bone holding the teeth (edge of the maxilla, incisive bone + mandible)'),
        ('Interalveolar septa','bone BETWEEN the sockets of neighboring teeth'),('Interradicular septa','bone BETWEEN the roots of ONE tooth (see the multi-rooted cheek teeth in Fig. A)')],
        ['crown','root','neck of tooth','vestibular surface','palatine surface','contact surfaces','mesial contact surface','distal surface','occlusal or masticating surface','alveolar border','interalveolar septa','interradicular septa'],'Fig. 5-11, teeth')]

def umn(i,captop=None):
    import p4umn; return p4umn.crop(i,p4umn.CAP[i] if hasattr(p4umn,'CAP') else dict((x[0],x[2]) for x in p4umn.SPEC)[i])
def build29():
    import p4umn; cap=dict((x[0],x[2]) for x in p4umn.SPEC); U=lambda i:p4umn.crop(i,cap[i])
    def uc(q,i,rows,terms): 
        c=fcard(q,U(i),rows,terms,''); c['html']=c['html'].replace('📖 lab guide drawing · ',f'🌐 UMN #{i} · '); return c
    return [
     uc('nose · philtrum · superior + inferior lips · cheek','5440',[('Nose','the rostral tip of the muzzle (nasal plane)'),('Philtrum','the median groove of the upper lip/nasal plane'),
        ('Superior + inferior lips','upper + lower lips (#6 orbicularis oris lies in them)'),('Cheek','the side wall of the mouth, caudal to the lips (#1 platysma runs over it)')],
        ['nose','philtrum','superior lips','inferior lips','cheek']),
     uc('oral cavity proper · body of tongue · sublingual fold','5445',[('Oral cavity proper','the space INSIDE the dental arches (the vestibule is outside the teeth)'),
        ('Body of tongue','the middle part between the apex (rostral) and the root (caudal, at #5 vallate papillae)'),
        ('Sublingual fold','the mucosal fold on the floor of the mouth beside the tongue where the ducts (#3) run to the sublingual caruncle (#4)')],
        ['oral cavity proper','body of tongue','sublingual fold']),
     uc('conjunctival sac · conjunctival fornix · lacrimal canaliculus · lacrimal sac','5443',[('Conjunctival sac','the space between the eyelids and the eyeball'),
        ('Conjunctival fornix','the deepest fold where palpebral conjunctiva turns onto the eyeball as bulbar conjunctiva'),
        ('Lacrimal canaliculus','the tiny canal leading from each lacrimal punctum (#12, #13) at the medial commissure'),
        ('Lacrimal sac','where the two canaliculi meet, in the fossa for the lacrimal sac → continues as the nasolacrimal duct')],
        ['conjunctival sac','conjunctival fornix','lacrimal canaliculus','lacrimal sac']),
     uc('ethmoid bone · ectoturbinates · endoturbinates · nasal aperture','5452',[('Ethmoid bone','the bone forming the ethmoidal labyrinth (#8) + cribriform plate at the back of the nasal cavity'),
        ('Endoturbinates','the large scrolls of the ethmoidal labyrinth that reach the nasal septum (#8 area)'),('Ectoturbinates','the smaller scrolls lying lateral to/between the endoturbinates (hidden here)'),
        ('Nasal aperture','the rostral bony opening of the nasal cavity, at the nose end (right side of the photo)')],
        ['ethmoid bone','ectoturbinates','endoturbinates','nasal aperture'])]

def _pdf(path,pg,y0,y1,out):
    p=fz.open(path)[pg-1]; r=p.rect; pm=p.get_pixmap(dpi=200,clip=fz.Rect(0,r.height*y0,r.width,r.height*y1))
    Image.frombytes('RGB',(pm.width,pm.height),pm.samples).save(out,quality=90); return out
A='/mnt/user-data/attachments/31594bc3-9d6f-5c02-a55e-32953ff4d455/'
def build29b():
    import p4umn; cap=dict((x[0],x[2]) for x in p4umn.SPEC); U=lambda i:p4umn.crop(i,cap[i])
    def uc(q,i,rows,terms):
        c=fcard(q,U(i),rows,terms,''); c['html']=c['html'].replace('📖 lab guide drawing · ',f'🌐 UMN #{i} · '); return c
    m=_pdf(PDF,16,0.57,0.95,'assets/p4find_515b.jpg')
    return [
     fcard('maxillary recess · lateral nasal gland',m,[('Maxillary recess','the lateral pocket of the nasal cavity inside the maxilla; its entrance is labeled ("Entrance to maxillary recess")'),
        ('Lateral nasal gland','the gland lying in the wall of the maxillary recess; its duct opens near the nostril and moistens the nose')],['maxillary recess','lateral nasal gland'],'Lab 28 Fig. 5-15'),
     uc('articular disc','5459',[('Articular disc','the fibrocartilage disc INSIDE the temporomandibular joint (#3), between the condylar process and the mandibular fossa')],['articular disc']),
     uc('septal cartilage','5449',[('Septal cartilage','the cartilaginous rostral part of the nasal septum (#9); the caudal part is bone')],['septal cartilage']),
     uc('lateral palpebral ligament','5443',[('Lateral palpebral ligament','the band anchoring the lateral commissure (#5) of the eyelids to the orbital rim')],['lateral palpebral ligament']),
     uc('ducts of the zygomatic gland · incisive duct','5445',[('Ducts of the zygomatic gland','open into the vestibule beside the LAST upper molar (one major + several minor ducts)'),
        ('Incisive duct','opens beside the incisive papilla just caudal to the upper incisors, rostral end of the hard palate (#7)')],['ducts of the zygomatic gland','incisive duct']),
     uc('parotid lymph node','5448',[('Parotid lymph node','small node at the ROSTRAL border of the parotid salivary gland (#1), under the gland edge near the masseter')],['parotid lymph node'])]
def build31():
    P31=A+'f22d97f5-Lab_31.pdf'
    e=_pdf(P31,7,0.04,0.6,'assets/p4find_538.jpg'); v=_pdf(P31,11,0.06,0.5,'assets/p4find_542.jpg')
    return [
     fcard('fundus · aqueous humor · dilator pupillae',e,[('Fundus','the posterior interior of the eyeball seen with an ophthalmoscope: optic disk + tapetum lucidum + nontapetal nigrum'),
        ('Aqueous humor','the watery fluid filling the anterior chamber (#6) + posterior chamber (#5), in front of the lens'),
        ('Dilator pupillae','the RADIAL smooth muscle of the iris (#7); dilates the pupil (the sphincter pupillae is circular)')],['fundus','aqueous humor','dilator pupillae'],'Lab 31 Fig. 5-38'),
     fcard('deep facial vein',v,[('Deep facial vein','labeled "Deep facial": runs from the facial vein deep under the orbit to the ophthalmic plexus / pterygoid plexus')],['deep facial vein'],'Lab 31 Fig. 5-42')]
