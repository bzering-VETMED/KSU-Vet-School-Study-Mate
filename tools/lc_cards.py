# Quick-recall flashcards for Gross Anatomy lectures 17–19 (made by Claude).
# 10-second answers, full names (Canvas is text-match strict). Run from repo root.
import os, sys, re
sys.path.insert(0, os.path.dirname(__file__)); import deck
L17 = [
("Bundle of axons OUTSIDE the CNS?","Nerve"),("Bundle of axons INSIDE the CNS?","Tract"),
("Cell bodies OUTSIDE the CNS?","Ganglion"),("Cell bodies INSIDE the CNS?","Nucleus"),
("Correct name for the \"basal ganglia\"?","Basal nucleus"),("Vagosympathetic trunk: nerve or tract?","Nerve"),
("Afferent means…","Toward the CNS (sensory)"),("Efferent means…","Away from the CNS (motor)"),
("Spinal cord: where is the gray matter?","Center (white matter outside)"),("Brain: where is the gray matter?","Outside (white matter center)"),
("Dorsal horn function?","Sensory"),("Ventral horn function?","Motor"),("Lateral horn function?","Autonomic"),
("Lateral horn is found in which cord region?","Thoracolumbar"),
("Multipolar neurons are…","Motor neurons and interneurons"),("Bipolar neurons are…","Special senses"),
("Pseudounipolar neurons are…","Sensory"),("Cell body of a primary afferent neuron?","Dorsal root ganglion"),
("Cell body of a lower motor neuron?","Ventral horn"),("Interneurons are located…","Entirely within the CNS"),
("Two types of interneurons?","Excitatory and inhibitory"),("A descending projection neuron is a…","Upper motor neuron"),
("Which controls which?","Upper motor neuron controls lower motor neuron"),("Is there a ventral root ganglion?","No, only the dorsal root ganglion"),
("Three ways to classify a neuron?","Structural, functional, pathway"),
("GSA example?","Pinching the skin"),("GSE target?","Skeletal muscle"),("GVA example?","Stomach fullness"),
("GVE targets?","Smooth muscle, cardiac muscle, glands"),("SSA senses?","Vision and hearing"),("SVA senses?","Taste and smell"),
("SVE targets?","Pharyngeal arch muscles (chewing, facial expression)"),
("Neurons in a GSE chain?","One"),("Neurons in a GVE chain?","Two"),
("Pairs of spinal nerves in the dog?","31"),("Spinal nerves per region?","C8, T13, L7, S3"),("Pairs of cranial nerves?","12"),
("C1 exits through the…","Lateral vertebral foramen"),("C8 exits…","Cranial to T1"),
("Thoracic and lumbar nerves exit…","Caudal to the same-numbered vertebra"),("Sacral nerves exit through the…","Dorsal and ventral sacral foramina"),
("C4 spinal nerve exits between which vertebrae?","C3 and C4 (cervical = cranial)"),("T4 spinal nerve exits between which vertebrae?","T4 and T5 (thoracic = caudal)"),
("Spinal nerve leaves the canal through the…","Intervertebral foramen"),
("Dorsal branch supplies…","Epaxial muscles, dorsal third of the skin"),("Ventral branch supplies…","Hypaxial muscles, limbs, ventral two-thirds of the skin"),
]
L18 = [
("Autonomic nervous system: motor or sensory?","Motor"),("Three autonomic targets?","Smooth muscle, cardiac muscle, glands"),
("Somatic motor neurotransmitter?","Acetylcholine"),("Neuron 1 is also called…","Preganglionic (presynaptic)"),
("Neuron 2 is also called…","Postganglionic (postsynaptic)"),("Sympathetic origin?","Thoracolumbar lateral horn"),
("Parasympathetic origin?","Craniosacral"),("Parasympathetic cranial nerves?","III, VII, IX, X"),
("Sacral parasympathetic nerve?","Pelvic nerve"),("Sacral parasympathetic segments?","S1–S3"),
("Sympathetic neuron lengths?","Short pre, long post"),("Parasympathetic neuron lengths?","Long pre, short post"),
("Sympathetic neurotransmitters?","Acetylcholine, then norepinephrine"),("Parasympathetic neurotransmitters?","Acetylcholine, then acetylcholine"),
("Sympathetic exception that uses acetylcholine?","Sweat glands"),("Chain ganglia are also called…","Paravertebral ganglia"),
("What links the chain ganglia?","Sympathetic trunk"),("Parasympathetic ganglia in organ walls?","Terminal ganglia"),
("Which ganglia are visible in lab?","Sympathetic"),("White ramus carries…","Preganglionic sympathetic axons"),
("Gray ramus carries…","Postganglionic sympathetic axons"),("Why is the white ramus white?","Myelinated"),
("Rami communicantes connect…","Spinal nerve and sympathetic trunk"),("Rami belong to which division?","Sympathetic only"),
("Most common sympathetic pathway?","Spinal nerve pathway"),("Splanchnic pathway synapse site?","Prevertebral ganglion"),
("Pathway with no ganglion synapse?","Adrenal medulla pathway"),("Chromaffin cells are…","Modified postganglionic sympathetic neurons"),
("Chromaffin cells secrete…","Epinephrine and norepinephrine"),("Sympathetic route to the heart?","Postganglionic sympathetic nerve pathway"),
("Vertebral nerve fiber type?","Postganglionic sympathetic"),("Hypogastric nerve fiber type?","Postganglionic sympathetic"),
("Splanchnic nerves fiber type?","Preganglionic sympathetic"),("Pelvic nerve fiber type?","Preganglionic parasympathetic"),
("Sympathetic loop around the axillary artery?","Ansa axillaris"),("Sympathetic synapse for the head?","Cranial cervical ganglion"),
("Vertebral nerve comes from the…","Cervicothoracic ganglion"),("Major and minor splanchnic nerves synapse in the…","Celiacomesenteric ganglion"),
("Lumbar splanchnic nerves synapse in the…","Caudal mesenteric ganglion"),("Name the 5 sympathetic ganglia.","Cranial cervical, middle cervical, cervicothoracic, celiacomesenteric, caudal mesenteric"),
("Pelvic plexus: synapse there?","No (\"truck stop\")"),("Dorsal vagal trunk fibers are…","Preganglionic parasympathetic (no synapse until the target organ)"),("Vagus share of parasympathetic outflow?","About 80%"),
("Cranial nerve III ganglion?","Ciliary ganglion"),("Cranial nerve VII ganglia?","Pterygopalatine and submandibular"),
("Cranial nerve IX ganglion?","Otic ganglion"),("Point and shoot?","Parasympathetic erection, sympathetic ejaculation"),
("Pupil dilation: which division?","Sympathetic"),("Increased intestinal motility: which division?","Parasympathetic"),
("Abundant watery saliva: which division?","Parasympathetic"),("Bronchiole dilation: which division?","Sympathetic"),
("Accepted synonym for ramus communicans?","Communicating branch"),
]
L19 = [
("Brachial plexus is formed by…","Ventral branches of C6–T2"),("Main artery chain of the thoracic limb?","Subclavian → axillary → brachial → median"),
("Left subclavian artery arises from…","Aortic arch"),("Right subclavian artery arises from…","Brachiocephalic trunk"),
("Subclavian becomes axillary at the…","First rib"),("Axillary becomes brachial after the…","Cranial circumflex humeral artery"),
("Brachial becomes median after the…","Common interosseous artery"),("Last two branches of the subclavian?","Internal thoracic, superficial cervical"),
("External thoracic artery supplies…","Superficial pectorals"),("Lateral thoracic artery supplies…","Deep pectorals"),
("Thoracodorsal artery supplies…","Latissimus dorsi"),("Caudal circumflex humeral artery comes off the…","Subscapular artery"),
("Cranial circumflex humeral artery comes off the…","Axillary artery"),("Median artery continues as the…","Superficial palmar arch"),
("Superficial paw arteries?","Common digital arteries"),("Deep paw arteries?","Metacarpal arteries"),
("Cephalic vein drains which side?","Medial"),("Accessory cephalic vein drains which side?","Dorsal and lateral"),
("Cephalic vein empties into the…","External jugular vein"),("Superficial–deep link at the elbow?","Median cubital vein (cephalic ↔ brachial)"),
("Deep veins are tributaries of the…","Axillary vein"),("Terminal lymph node of the thoracic limb?","None"),
("Terminal lymph node of the head?","Medial retropharyngeal lymph node"),("Clinical name for the superficial cervical lymph node?","Prescapular"),
("Is the axillary lymph node always present?","Yes (constant)"),("Accessory axillary lymph node location?","Intercostal spaces 2–3"),
("Mammary glands drained by the axillary lymph node?","1–3"),("Sentinel lymph node?","First node to drain an area"),
("Terminal lymph node?","Node all or most lymph from a region passes through"),("Afferent lymph vessels carry lymph…","Into the node"),
("Suprascapular nerve supplies…","Supraspinatus and infraspinatus"),("Musculocutaneous nerve supplies…","Biceps brachii, brachialis, coracobrachialis"),
("Axillary nerve supplies…","Deltoideus, teres major, teres minor"),("Thoracodorsal nerve supplies…","Latissimus dorsi"),
("Radial nerve supplies…","Triceps and carpal/digital extensors"),("Median nerve supplies…","Flexor carpi radialis, superficial and deep digital flexors"),
("Ulnar nerve supplies…","Flexor carpi ulnaris, deep digital flexor"),("Lateral thoracic nerve supplies…","Cutaneous trunci"),
("Largest brachial plexus nerve?","Radial nerve"),("Nerve with a cutaneous branch but no autonomous zone?","Median nerve"),
("Autonomous zone?","Skin supplied by only one nerve"),("Overlap zone?","Skin supplied by two or more nerves"),
("Musculocutaneous testing site?","2 cm distal to the medial epicondyle"),("Axillary nerve testing site?","2 cm caudal to the shoulder joint"),
("Radial nerve testing site?","Proximal metacarpals II–III, dorsal"),("Caudal cutaneous antebrachial nerve testing site?","4 cm distal to the olecranon"),
("Ulnar palmar branch testing site?","Lateral surface of digit 5"),("Fiber types in every plexus nerve?","Motor, sensory, sympathetic"),
]

ABD1 = [
("Alimentary tract runs from… to…","Mouth to anus"),("Gastrointestinal tract runs from… to…","Stomach to anus"),
("Largest body cavity?","Abdominal cavity"),("Serous lining of the abdomen?","Peritoneum (parietal and visceral)"),
("Four regions of the stomach?","Cardia, fundus, body, pylorus"),("Stomach inlet?","Cardia"),("Stomach outlet?","Pylorus"),
("Cardiac sphincter in the dog: strong or weak?","Weak (dogs vomit)"),("Pyloric sphincter regulates…","Outflow into the duodenum"),
("Site of gas accumulation in the stomach?","Fundus"),("Lesser curvature attaches the…","Lesser omentum"),
("Greater curvature attaches the…","Greater omentum"),("Pylorus: wide part, then narrow part?","Pyloric antrum, then pyloric canal"),
("Gastric folds that aid peristalsis?","Rugae"),("Stomach lies on which side?","Left, caudal to the liver"),
("Empty stomach: palpable?","No (under the costal arch)"),("Moderately full stomach extends…","T9–T12"),
("Greatly distended stomach extends…","T9–L3"),("GDV usually twists which direction?","Clockwise"),
("GDV compresses which vessels?","Caudal vena cava and portal vein"),("Three parts of the small intestine?","Duodenum, jejunum, ileum"),
("Longest part of the small intestine?","Jejunum"),("Shortest part of the small intestine?","Ileum"),
("Ileum vs. ilium spelling?","Ileum with an E (intestine); ilium is the bone"),
("Descending duodenum runs…","Right cranial → right caudal quadrant"),("Caudal duodenal flexure runs…","Right caudal → left caudal, caudal to the root of the mesentery"),
("Ascending duodenum runs…","Left caudal → left cranial quadrant"),("Fold between ascending duodenum and descending colon?","Duodenocolic fold"),
("Turn from duodenum into jejunum?","Duodenojejunal flexure"),("Jejunum is suspended by the…","Mesojejunum"),
("Jejunum is covered by the…","Greater omentum"),("First thing you see when you open the abdomen?","Greater omentum"),
("Fold that marks the length of the ileum?","Ileocecal fold"),("Ileum opens into the…","Ascending colon (ileocolic orifice)"),
("Cecum opens into the…","Ascending colon (cecocolic orifice)"),("Do the ileum and cecum communicate in the dog?","No"),
("Cecum lies on which side?","Right of midline"),("Removing the cecum is called…","Typhlectomy"),
("Order of the colon?","Ascending → right colic flexure → transverse → left colic flexure → descending"),
("Following the transverse colon, ingesta enters…","Left colic flexure → descending colon"),
("Transverse colon relative to the root of the mesentery?","Cranial (in every species)"),
("Artery in the root of the mesentery?","Cranial mesenteric artery"),
("Structures cranial to the root of the mesentery in large animals?","Not palpable per rectum"),
("Cranial rectum: peritoneal or retroperitoneal?","Covered by peritoneum (pararectal fossae)"),
("Caudal rectum: peritoneal or retroperitoneal?","Retroperitoneal"),("Other retroperitoneal organ he named?","Kidneys"),
("Internal anal sphincter muscle type?","Smooth muscle (involuntary)"),("External anal sphincter muscle type?","Skeletal muscle (voluntary)"),
("Three zones of the anal canal?","Columnar, intermediate, cutaneous"),("Line between rectum and anal canal?","Anorectal line"),
("Line between anal canal and skin?","Anocutaneous line"),("Anal sacs open in which zone?","Cutaneous zone"),
("Liver produces… stored in…","Bile, stored in the gallbladder"),("Largest organ in the body?","Liver"),
("Six liver lobes?","Left lateral, left medial, quadrate, right medial, right lateral, caudate"),
("Two processes of the caudate lobe?","Caudate process and papillary process"),
("Gallbladder sits between which lobes?","Right medial and quadrate"),("Falciform ligament sits between which lobes?","Left medial and quadrate"),
("Falciform ligament attaches the liver to…","The ventral body wall"),("Triangular ligaments attach the liver to…","The diaphragm"),
("Coronary ligament surrounds the…","Caudal vena cava (\"crown\")"),("Hepatorenal ligament connects…","Caudate process of the liver ↔ right kidney"),
("Hepatogastric and hepatoduodenal ligaments connect…","Liver ↔ stomach; liver ↔ duodenum"),
("Common bile duct is formed by…","Cystic duct + hepatic duct"),("Spleen lies on which side?","Left of midline"),
("Spleen attaches to the stomach by the…","Gastrosplenic ligament (greater curvature)"),
("Splenic tumor he named?","Hemangiosarcoma"),("Pancreas lies in the…","Mesoduodenum"),
("Pancreas parts?","Head (right lobe), body, tail (left lobe, near the spleen)"),
("Pancreatic duct opens at the…","Major duodenal papilla (with the common bile duct)"),
("Accessory pancreatic duct opens at the…","Minor duodenal papilla"),
("Larger pancreatic duct in the dog?","Accessory pancreatic duct (cats: the pancreatic duct)"),
("Most common pancreas biopsy site?","Left lobe (tail)"),
("Dog vs. horse vs. ruminant fermentation?","Dog: limited · horse: hindgut (cecum, colon) · ruminant: foregut (rumen)"),
]
# One-page tap-to-reveal review (same layout as the systems lab "Functions Review" page).
SECTIONS = {
 17: [("🧠 Nerve vs. tract · gray matter · horns", range(0, 14)), ("🔌 Neuron types", range(14, 25)),
      ("🏷️ Functional types", range(25, 34)), ("🦴 Spinal nerves", range(34, 46))],
 18: [("⚙️ Autonomic basics", range(0, 15)), ("🔗 Ganglia & rami", range(15, 24)),
      ("🛣️ Sympathetic pathways & nerves", range(24, 41)), ("🌿 Parasympathetic", range(41, 46)),
      ("⚖️ Which division?", range(46, 52))],
 19: [("❤️ Arteries", range(1, 16)), ("🩸 Veins", range(16, 21)), ("🫧 Lymph nodes", range(21, 30)),
      ("⚡ Nerves", [0] + list(range(30, 40)) + [47]), ("📍 Zones & testing sites", range(40, 47))],
 "abd1": [("🗺️ Overview", [0, 1, 2, 3, 73]), ("🍽️ Stomach", range(4, 20)), ("🌀 Small intestine & cecum", range(20, 38)),
          ("💩 Colon, rectum & anal canal", range(38, 52)), ("🟤 Liver & bile", range(52, 64)),
          ("🫘 Spleen & pancreas", range(64, 73))],
}
import html as H
CSS = open(os.path.join(os.path.dirname(__file__), "review.css")).read()
JS = """const A=[...document.querySelectorAll('.ans')],N=document.getElementById('n');function u(){N.textContent=A.filter(a=>a.classList.contains('on')).length+' / '+A.length}A.forEach(a=>a.onclick=()=>{a.classList.toggle('on');u()});document.getElementById('all').onclick=()=>{A.forEach(a=>a.classList.add('on'));u()};document.getElementById('hide').onclick=()=>{A.forEach(a=>a.classList.remove('on'));u();scrollTo(0,0)};u();
const cols=document.querySelector('.cols'),orig=[...cols.children],R=[...document.querySelectorAll('tr')],S=document.getElementById('shuf'),T=document.getElementById('topic');
const mix=document.createElement('div');mix.className='sec';mix.innerHTML='<h2>🔀 Mixed</h2><table></table>';
S.onclick=()=>{const r=R.slice();for(let i=r.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[r[i],r[j]]=[r[j],r[i]]}
 const t=mix.querySelector('table');r.forEach(x=>t.appendChild(x));cols.replaceChildren(mix);cols.style.columnCount=1;
 A.forEach(a=>a.classList.remove('on'));u();T.hidden=false;S.textContent='🔀 Reshuffle';scrollTo(0,0)};
T.onclick=()=>{orig.forEach(sec=>cols.appendChild(sec));mix.remove();rebuild();cols.style.columnCount='';T.hidden=true;S.textContent='🔀 Shuffle';A.forEach(a=>a.classList.remove('on'));u();scrollTo(0,0)};
const home=R.map(x=>x.parentNode);function rebuild(){R.forEach((x,i)=>home[i].appendChild(x))}"""
V = str(int(__import__("time").time()))
def review(title, sub, cards, secs):
    used = sorted(i for _, r in secs for i in r); assert used == list(range(len(cards))), (title, set(range(len(cards))) - set(used))
    body = ""
    for k, (h, r) in enumerate(secs):
        rows = "".join(f'<tr><td>{H.escape(cards[i][0])}</td><td><span class="ans">{H.escape(cards[i][1])}</span></td></tr>' for i in r)
        body += f'<div class="sec{" p" if k % 2 else ""}"><h2>{H.escape(h)}</h2><table>{rows}</table></div>'
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{H.escape(title)}</title><style>{CSS}</style></head><body><div class="wrap">'
            f'<a class="back" href="gross-anatomy-lecture.html?v={V}">← Back to Lecture</a>'
            f'<div class="hero"><h1>{H.escape(title)}</h1><p>{H.escape(sub)}</p></div>'
            f'<div class="bar"><button id="hide">🙈 Hide all</button><button id="all">👀 Show all</button><button id="shuf">🔀 Shuffle</button><button id="topic" hidden>📚 By topic</button><span class="n" id="n"></span></div>'
            f'<div class="cols">{body}</div><div class="foot">🎀 Bethany · K-State CVM Class of 2030 · 🐾</div></div><script>{JS}</script></body></html>')
for n, title, cards in [(17,"Nervous System 1",L17),(18,"Autonomic Nervous System",L18),(19,"Thoracic Limb",L19),("abd1","Abdominal Cavity 1",ABD1)]:
    lab = (f"L{n}" if isinstance(n,int) else "Abdominal Cavity 1")
    html = review(f"⚡ {lab} Quick Review", f"{title} · say the answer, then tap the pink box to check · {len(cards)} items", cards, SECTIONS[n])
    open(f"gross-anatomy-lc{n}-cards.html", "w").write(html)
    print(n, len(cards))
