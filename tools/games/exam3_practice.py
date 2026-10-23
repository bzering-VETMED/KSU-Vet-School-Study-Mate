# Blueprint-weighted practice exam for Gross Anatomy Lecture Exam 3 (made by Claude).
# Run from repo root: python3 tools/games/exam3_practice.py  -> gross-anatomy-exam3-practice.html
# Content comes only from tools/terms/*.json (L17, L18, L19, ABD1=L20, ABD2=L21, L22, L23, L24, L25).
# Blueprint: L17=5, L18=7, L19=7, L20=7, L21=7, L22=3, L23=7, L24=7, L25=3 -> 53 questions.
import os, sys, json, time, random
sys.path.insert(0, os.path.dirname(__file__)); import common
V = str(int(time.time()))

LECS = {
 "L17": "L17 Nervous System 1",
 "L18": "L18 Autonomic Nervous System",
 "L19": "L19 Thoracic Limb Vessels and Nerves",
 "L20": "L20 Abdominal Cavity 1",
 "L21": "L21 Abdominal Cavity 2",
 "L22": "L22 Urinary System",
 "L23": "L23 Male Reproductive",
 "L24": "L24 Female Reproductive",
 "L25": "L25 Abdominal Radiology",
}
BLUEPRINT = {"L17": 5, "L18": 7, "L19": 7, "L20": 7, "L21": 7, "L22": 3, "L23": 7, "L24": 7, "L25": 3}

# (lecture, objective, stem, correct, [3 distractors], one-line explanation)
Q = [
 # ---------- L17 Nervous System 1 (5) ----------
 ("L17", "Gray/white matter, central/peripheral terms",
  "A collection of neuron cell bodies inside the central nervous system is a…",
  "Nucleus", ["Ganglion", "Tract", "Nerve"],
  "Nucleus = cell bodies inside; ganglion = cell bodies outside; tract = axons inside; nerve = axons outside."),
 ("L17", "Neuron groups and reflex arc",
  "The patellar reflex arc is formed by which two neurons?",
  "Primary afferent and final efferent", ["Upper motor and lower motor", "Projection neuron and interneuron", "Primary afferent and projection"],
  "Reflex arc = primary afferent + final efferent (lower motor neuron); monosynaptic, spinal cord only."),
 ("L17", "Functional types",
  "Neurons to the muscles of mastication are which functional type?",
  "Special visceral efferent", ["General somatic efferent", "General visceral efferent", "Special somatic afferent"],
  "Special visceral efferent supplies pharyngeal arch skeletal muscle: mastication, facial expression, pharynx, larynx."),
 ("L17", "Functional types",
  "Neurons arising from the lateral horn of the spinal cord are…",
  "General visceral efferent", ["General somatic efferent", "General visceral afferent", "General somatic afferent"],
  "Lateral horn = general visceral efferent (autonomic); ventral horn = general somatic efferent; dorsal horn receives afferents."),
 ("L17", "Spinal cord segments and vertebral levels",
  "The eighth cervical spinal nerve exits cranial to which vertebra?",
  "First thoracic vertebra", ["Seventh cervical vertebra", "Eighth cervical vertebra", "Second thoracic vertebra"],
  "There is no eighth cervical vertebra, so the eighth cervical nerve exits cranial to the first thoracic vertebra."),

 # ---------- L18 Autonomic (7) ----------
 ("L18", "Two-neuron chain",
  "In the autonomic two-neuron chain, the preganglionic neuron is also the…",
  "Presynaptic neuron", ["Postsynaptic neuron", "Lower motor neuron", "Projection neuron"],
  "Preganglionic = presynaptic (neuron 1); postganglionic = postsynaptic (neuron 2)."),
 ("L18", "Compare sympathetic and parasympathetic",
  "Parasympathetic preganglionic neurons originate in the…",
  "Brain stem and sacral cord", ["Thoracic and lumbar cord", "Cervical and thoracic cord", "Brain stem and lumbar cord"],
  "Parasympathetic = craniosacral (cranial nerves III, VII, IX, X and sacral segments); sympathetic = thoracolumbar."),
 ("L18", "Compare sympathetic and parasympathetic",
  "Which sympathetic target receives acetylcholine from neuron 2?",
  "Sweat glands", ["Cardiac muscle", "Skin blood vessels", "Piloerector muscles"],
  "Sympathetic neuron 2 releases norepinephrine, except at sweat glands (cholinergic)."),
 ("L18", "White and gray rami communicantes",
  "The gray ramus communicans carries which axons?",
  "Postganglionic sympathetic", ["Preganglionic sympathetic", "Preganglionic parasympathetic", "Postganglionic parasympathetic"],
  "Gray = postganglionic, unmyelinated, exit ramp; white = preganglionic, myelinated, entrance ramp. Sympathetic only."),
 ("L18", "Trace sympathetic pathways",
  "In the splanchnic nerve pathway, neuron 1 synapses in a…",
  "Prevertebral ganglion", ["Paravertebral ganglion", "Terminal ganglion", "Dorsal root ganglion"],
  "Splanchnic fibers pass through the chain ganglion without synapsing and synapse in a prevertebral ganglion."),
 ("L18", "Trace sympathetic pathways",
  "Lumbar splanchnic nerves synapse in which ganglion?",
  "Caudal mesenteric ganglion", ["Celiacomesenteric ganglion", "Cervicothoracic ganglion", "Cranial cervical ganglion"],
  "Major and minor splanchnic → celiacomesenteric ganglion; lumbar splanchnic → caudal mesenteric ganglion."),
 ("L18", "Trace sympathetic pathways",
  "From the caudal mesenteric ganglion, sympathetic fibers reach the bladder via the…",
  "Hypogastric nerve", ["Pelvic nerve", "Vertebral nerve", "Vagus nerve"],
  "Lumbar splanchnic → caudal mesenteric ganglion → hypogastric nerve (postganglionic sympathetic) → pelvic plexus."),

 # ---------- L19 Thoracic limb vessels and nerves (7) ----------
 ("L19", "Arterial branches and name changes",
  "The brachial artery becomes the median artery after which branch?",
  "Common interosseous artery", ["Cranial circumflex humeral artery", "Collateral ulnar artery", "Deep brachial artery"],
  "Axillary → brachial after cranial circumflex humeral; brachial → median after common interosseous."),
 ("L19", "Superficial veins",
  "The accessory cephalic vein drains which aspect of the limb?",
  "Dorsal and lateral aspect", ["Medial aspect only", "Palmar and medial aspect", "Caudal and palmar aspect"],
  "Cephalic drains the medial aspect; accessory cephalic drains dorsal and lateral, then joins the cephalic."),
 ("L19", "Paw artery naming",
  "The deep arteries on the palmar surface of the paw are the…",
  "Palmar metacarpal arteries", ["Palmar common digital arteries", "Dorsal metacarpal arteries", "Dorsal common digital arteries"],
  "Paw rule: superficial = common digital, deep = metacarpal; prefix dorsal or palmar by surface. Palmar metacarpals run deep to the deep digital flexor tendons."),
 ("L19", "Lymph nodes of the thoracic limb",
  "Which two lymph nodes of the thoracic limb are constant?",
  "Superficial cervical and axillary", ["Axillary and accessory axillary", "Superficial cervical and accessory axillary", "Axillary and medial retropharyngeal"],
  "Superficial cervical and axillary are constant; accessory axillary is inconstant. There is no terminal node for the limb."),
 ("L19", "Brachial plexus segments",
  "The brachial plexus is formed by ventral branches of spinal nerves…",
  "Sixth cervical to second thoracic", ["Fifth cervical to first thoracic", "Sixth cervical to first thoracic", "Seventh cervical to second thoracic"],
  "Brachial plexus = ventral branches of the sixth cervical through second thoracic spinal nerves."),
 ("L19", "Nerves with autonomous zones",
  "Which nerve has a cutaneous branch but no autonomous zone?",
  "Median nerve", ["Ulnar nerve", "Radial nerve", "Axillary nerve"],
  "Autonomous zones: musculocutaneous, axillary, radial, ulnar. The median nerve has none."),
 ("L19", "Loss of function from nerve injury",
  "Injury to which nerve leaves the dog unable to bear weight on the forelimb?",
  "Radial nerve", ["Median nerve", "Musculocutaneous nerve", "Axillary nerve"],
  "Radial nerve injury → loss of elbow, carpal and digit extension; the limb cannot bear weight."),

 # ---------- L20 Abdominal Cavity 1 (7) ----------
 ("L20", "Stomach",
  "A moderately full stomach extends over which vertebrae?",
  "Ninth to twelfth thoracic", ["Ninth thoracic to third lumbar", "Sixth to ninth thoracic", "Twelfth thoracic to third lumbar"],
  "Moderately full: ninth to twelfth thoracic, palpable. Greatly distended: ninth thoracic to third lumbar."),
 ("L20", "Intestinal segments and the root of the mesentery",
  "Which intestinal segment lies cranial to the root of the mesentery?",
  "Transverse colon", ["Terminal ileum", "Caudal duodenal flexure", "Cranial rectum"],
  "Transverse colon is cranial to the root of the mesentery; the caudal duodenal flexure and ileum are caudal."),
 ("L20", "Zones of the anal canal",
  "The zones of the anal canal, cranial to caudal, are…",
  "Columnar, intermediate, cutaneous", ["Cutaneous, intermediate, columnar", "Intermediate, columnar, cutaneous", "Columnar, cutaneous, intermediate"],
  "Columnar zone (anorectal line, anal columns) → intermediate zone (anocutaneous line) → cutaneous zone (anal sacs open)."),
 ("L20", "Flow of ingesta",
  "After the ascending duodenum, ingesta passes next into the…",
  "Duodenojejunal flexure", ["Caudal duodenal flexure", "Right colic flexure", "Cranial duodenal flexure"],
  "Ascending duodenum → duodenojejunal flexure → jejunum → ileum → ascending colon."),
 ("L20", "Abdominal topography",
  "The descending duodenum runs between which quadrants?",
  "Right cranial to right caudal", ["Left caudal to left cranial", "Right caudal to left caudal", "Left cranial to right cranial"],
  "Descending: right cranial → right caudal. Caudal flexure: right caudal → left caudal. Ascending: left caudal → left cranial."),
 ("L20", "Liver lobes, falciform ligament and gallbladder",
  "The gallbladder sits between which two liver lobes?",
  "Right medial and quadrate", ["Left medial and quadrate", "Right medial and right lateral", "Quadrate and caudate"],
  "Gallbladder: right medial + quadrate. Falciform ligament: left medial + quadrate."),
 ("L20", "Spleen location",
  "Where does the spleen lie?",
  "Left of midline, along greater curvature", ["Right of midline, along lesser curvature", "Left of midline, along lesser curvature", "Right of midline, along greater curvature"],
  "Spleen is left of midline, tied to the greater curvature of the stomach by the gastrosplenic ligament."),

 # ---------- L21 Abdominal Cavity 2 (7) ----------
 ("L21", "Unpaired branches of the abdominal aorta",
  "The unpaired branches of the abdominal aorta, cranial to caudal, are…",
  "Celiac, cranial mesenteric, caudal mesenteric", ["Cranial mesenteric, celiac, caudal mesenteric", "Celiac, caudal mesenteric, cranial mesenteric", "Cranial mesenteric, caudal mesenteric, celiac"],
  "Celiac (most cranial) → cranial mesenteric → caudal mesenteric."),
 ("L21", "Venous drainage, left versus right",
  "The left gonadal vein drains into the…",
  "Left renal vein", ["Caudal vena cava directly", "Hepatic portal vein", "Left lumbar vein"],
  "Right gonadal vein → caudal vena cava directly; left gonadal vein → left renal vein → caudal vena cava."),
 ("L21", "Hepatic portal system",
  "Hepatic portal blood and hepatic arterial blood mix in the…",
  "Liver sinusoids", ["Central vein", "Hepatic veins", "Caudal vena cava"],
  "They mix in the sinusoids, then drain sinusoids → central vein → hepatic veins → caudal vena cava."),
 ("L21", "Structures passing through the inguinal canal",
  "Which nerve passes through the inguinal canal?",
  "Genitofemoral nerve", ["Femoral nerve", "Obturator nerve", "Pudendal nerve"],
  "Inguinal canal (slide 40): spermatic cord or vaginal process, external pudendal artery and vein, genitofemoral nerve, efferent lymph duct of the superficial inguinal node, cremaster muscle."),
 ("L21", "Mesentery, omenta and epiploic foramen",
  "The ventral border of the epiploic foramen is the…",
  "Portal vein", ["Caudal vena cava", "Abdominal aorta", "Splenic vein"],
  "Epiploic foramen: dorsal = caudal vena cava; ventral = portal vein; lateral = caudate process of the caudate lobe."),
 ("L21", "Rectus sheath",
  "The most caudal internal lamina of the rectus sheath is formed by…",
  "Transverse fascia only", ["Transversus abdominis only", "Internal abdominal oblique only", "External abdominal oblique only"],
  "Most caudally, all three muscle aponeuroses go external; the internal lamina is transverse fascia only."),
 ("L21", "Inguinal rings and canal",
  "The superficial inguinal ring is a slit in the aponeurosis of the…",
  "External abdominal oblique", ["Internal abdominal oblique", "Transversus abdominis", "Rectus abdominis"],
  "The external abdominal oblique aponeurosis has two insertions; the slit between them is the superficial inguinal ring."),

 # ---------- L22 Urinary (3) ----------
 ("L22", "Kidney location",
  "Compared with the right kidney, the left kidney is…",
  "More caudal and pendulous", ["More cranial and fixed", "More caudal and fixed", "More cranial and pendulous"],
  "'Left behind': left kidney is caudal and pendulous; right is cranial (by half a kidney) and fixed."),
 ("L22", "Pelvis, sinus, hilus, recess, papilla, crest, pyramid",
  "The renal crest is formed by…",
  "Fusion of the renal papillae", ["Diverticula of the renal pelvis", "Dilatation of the proximal ureter", "Indentation of the medial border"],
  "Renal crest = fused papillae. Pelvic recesses = diverticula; renal pelvis = dilated ureter; hilus = indented medial border."),
 ("L22", "Ligaments of the bladder",
  "The round ligament of the bladder is the free edge of the…",
  "Lateral ligament of the bladder", ["Median ligament of the bladder", "Falciform ligament of the liver", "Broad ligament of the uterus"],
  "Round ligament of the bladder = free edge of the lateral ligament, remnant of the umbilical artery."),

 # ---------- L23 Male reproductive, first half (7) ----------
 ("L23", "Penis: erectile tissue and muscles",
  "The bulb of the penis has which erectile tissue and covering muscle?",
  "Corpus spongiosum and bulbospongiosus", ["Corpus cavernosum and ischiocavernosus", "Corpus spongiosum and ischiocavernosus", "Corpus cavernosum and bulbospongiosus"],
  "Name logic: bulb = corpus spongiosum + bulbospongiosus; crus = corpus cavernosum + ischiocavernosus. The urethra always sits in corpus spongiosum."),
 ("L23", "Accessory sex glands",
  "Which surface of the prostate is covered by peritoneum?",
  "Dorsal surface only", ["Ventral surface only", "Both dorsal and ventral", "Neither surface"],
  "Prostate: dorsal surface has peritoneum, ventral is retroperitoneal. Flipped from the kidney (ventral covered, dorsal free)."),
 ("L23", "Cat versus dog",
  "In the cat, the scrotum is located…",
  "Just ventral to the anus", ["Between the thighs", "Ventral to the penis", "Cranial to the prepuce"],
  "Cat scrotum is just ventral to the anus (dorsal to the short, caudally directed penis); dog scrotum is between the thighs."),
 ("L23", "Testis layers and attachments",
  "The proper ligament of the testis attaches the testis to the…",
  "Tail of the epididymis", ["Head of the epididymis", "Parietal vaginal tunic", "Tunica dartos"],
  "Proper ligament: testis ↔ tail of epididymis. Ligament of the tail: tail ↔ vaginal tunic. Scrotal ligament: ↔ tunica dartos."),
 ("L23", "Epididymis and ductus deferens",
  "A testis image shows the ductus deferens but no epididymis. Which view is it?",
  "Medial view", ["Lateral view", "Cranial view", "Caudal view"],
  "Epididymis is dorsolateral (lateral view only); ductus deferens runs along the dorsomedial border."),
 ("L23", "Spermatic cord, anatomical versus clinical",
  "Which two structures are in the clinical but not the anatomical spermatic cord?",
  "Cremaster and parietal vaginal tunic", ["Mesorchium and mesoductus deferens", "Testicular artery and pampiniform plexus", "Cremaster and visceral vaginal tunic"],
  "Clinical (surgical) cord = anatomical seven + cremaster muscle + parietal vaginal tunic."),
 ("L23", "Open versus closed castration",
  "Open castration incises which layer?",
  "Parietal vaginal tunic", ["Visceral vaginal tunic", "Tunica albuginea", "Mesoductus deferens"],
  "Open: parietal vaginal tunic incised, opening the vaginal cavity (continuous with the peritoneal cavity). Closed: nothing opened."),

 # ---------- L24 Female reproductive (7) ----------
 ("L24", "Ovarian ligaments",
  "During a spay, which ligament is broken by strumming?",
  "Suspensory ligament of the ovary", ["Proper ligament of the ovary", "Round ligament of the uterus", "Broad ligament of the uterus"],
  "Suspensory ligament (last two ribs → ovary) is torn by strumming. The proper ligament of the ovary (ovary → horn) is sturdy and gets clamped."),
 ("L24", "Broad ligament and ovarian bursa",
  "The ovarian bursa is formed by the…",
  "Mesovarium and mesosalpinx", ["Mesosalpinx and mesometrium", "Mesovarium and mesometrium", "Mesometrium and uterine velum"],
  "Mesovarium + mesosalpinx enclose the ovary as the ovarian bursa. Mesovarium + mesosalpinx + mesometrium = broad ligament."),
 ("L24", "Uterine tube",
  "Which opening lies within the infundibulum of the uterine tube?",
  "Abdominal ostium", ["Uterine ostium", "Internal uterine orifice", "External uterine orifice"],
  "Abdominal ostium = entrance in the infundibulum; uterine ostium = exit into the horn. Uterine orifices belong to the cervix."),
 ("L24", "Vagina",
  "Transverse folds of the vaginal mucosa allow an increase in…",
  "Length", ["Diameter", "Wall thickness", "Mucus secretion"],
  "Transverse folds → length; longitudinal folds → diameter."),
 ("L24", "Vestibule",
  "Which mucosal feature identifies the vestibule?",
  "No mucosal folds", ["Only longitudinal folds", "Only transverse folds", "Both fold types"],
  "Vagina = longitudinal plus transverse folds; vestibule = smooth, no mucosal folds."),
 ("L24", "Female blood supply",
  "The uterine artery is a branch of the…",
  "Vaginal artery", ["Ovarian artery", "Abdominal aorta", "Caudal mesenteric artery"],
  "Internal pudendal → vaginal artery → uterine artery, which anastomoses with the uterine BRANCH of the ovarian artery."),
 ("L24", "Vestibule and catheterization",
  "In the bitch, the external urethral orifice sits on the…",
  "Urethral tubercle", ["Vaginal fornix", "Fossa clitoridis", "Cervical canal"],
  "External urethral orifice = cranioventral vestibule, on the urethral tubercle. A catheter that hits it: withdraw and direct dorsally."),

 # ---------- L25 Abdominal radiology (3) ----------
 ("L25", "Optional views",
  "A small kidney is hidden by superimposed bowel. Which view helps most?",
  "Compression view", ["Horizontal beam view", "Pneumocolonogram", "Perineal lateral view"],
  "Compression (wooden spoon) reduces superimposition. Horizontal beam = free gas; perineal view = urethral stones; pneumocolonogram = colon versus small intestine."),
 ("L25", "Stomach gas by recumbency",
  "On a right lateral abdominal radiograph, gas collects in the…",
  "Fundus", ["Pylorus", "Duodenum", "Cardia"],
  "Gas rises: right lateral → the left-sided fundus is up. Left lateral → pylorus and duodenum fill with gas."),
 ("L25", "Kidney size",
  "Normal canine kidney length equals how many second lumbar vertebrae?",
  "2.5 to 3.5", ["2 to 3", "1.5 to 2.5", "3.5 to 4.5"],
  "Dog: 2.5–3.5 × the second lumbar vertebra; cat: 2–3 ×. Measured on the ventrodorsal view."),
]

# ---- checks ----
from collections import Counter
cnt = Counter(q[0] for q in Q)
assert dict(cnt) == BLUEPRINT, cnt
assert len(Q) == 53
for q in Q:
    opts = [q[3]] + q[4]
    assert len(q[4]) == 3 and len(set(opts)) == 4, q[2]

# ---- balanced answer letters (fixed seed so the default order is stable) ----
letters = (list("ABCD") * 14)[:len(Q)]          # A14 B13 C13 D13
random.Random(806).shuffle(letters)
DATA = []
for (lec, obj, stem, ok, bad, why), L in zip(Q, letters):
    pos = "ABCD".index(L)
    opts = bad[:]; opts.insert(pos, ok)
    DATA.append(dict(l=lec, o=obj, q=stem, opts=opts, a=pos, x=why))
DIST = Counter("ABCD"[d["a"]] for d in DATA)

STYLE = '''<style>
.opts{display:grid;grid-template-columns:1fr;gap:8px}.opts .chip{display:flex;gap:10px;align-items:flex-start;font-size:16px}
.opts .chip b{flex:none;width:26px;height:26px;border-radius:50%;background:#f3eafb;color:#65328c;display:flex;align-items:center;justify-content:center;font-size:14px}
.tag{display:inline-block;padding:4px 10px;border-radius:999px;background:#fde7f0;color:#a0175a;font-weight:800;font-size:13px}
.prog{height:8px;border-radius:99px;background:#f3eafb;overflow:hidden;margin:10px 0 2px}.prog i{display:block;height:100%;background:linear-gradient(90deg,#6a3392,#e05fa8);width:0}
.qn{color:#8a6b99;font-weight:800;font-size:13px;margin-left:8px}
table{width:100%;border-collapse:collapse;margin:10px 0;font-size:15px}th{background:#6a3392;color:#fff;text-align:left;padding:8px}td{padding:8px;border-bottom:1px solid var(--line)}tr:nth-child(even) td{background:#fbf6fe}
.big{font-size:30px;font-weight:900;color:var(--grape);margin:4px 0}.missli{margin:6px 0;padding:8px 10px;border-radius:12px;background:#fde7f0;font-size:15px}
#lec{max-width:100%;flex:1 1 220px;min-width:0}
.toast{position:fixed;left:50%;bottom:20px;transform:translateX(-50%);background:#4b1f70;color:#fff;padding:10px 16px;border-radius:999px;font-weight:800;display:none;z-index:9}
@media(max-width:520px){.row .btn{flex:1 1 45%}.score{margin-left:0;width:100%}}
</style>'''

body = STYLE + '''
<div class="panel on" id="setup" style="margin-top:12px"><h2>📝 Practice exam setup</h2>
<p class="hint">53 questions weighted by the blueprint: L17 = 5 · L18 = 7 · L19 = 7 · L20 = 7 · L21 = 7 · L22 = 3 · L23 = 7 · L24 = 7 · L25 = 3. Pick an option → instant feedback.</p>
<div class="row"><select id="lec"><option value="all">All lectures (53)</option></select>
<button class="btn" id="shuf" aria-pressed="false">🔀 Shuffle: off</button>
<button class="btn hot" id="start">Start ▶</button></div></div>
<div class="panel" id="quiz" style="margin-top:12px">
<div class="row" style="margin-top:0"><span class="tag" id="tag"></span><span class="qn" id="qn"></span><span class="score" id="sc"></span></div>
<div class="prog"><i id="bar"></i></div>
<div class="q" id="stem"></div><div class="opts" id="opts"></div><div class="fb" id="fb"></div>
<div class="row"><button class="btn hot" id="next" disabled>Next ▶</button><button class="btn" id="quit">⏹ End now</button></div></div>
<div class="panel" id="done" style="margin-top:12px"><h2>🎀 Results</h2><div class="big" id="final"></div>
<table id="brk"><thead><tr><th>Lecture</th><th>Correct</th><th>%</th></tr></thead><tbody></tbody></table>
<div class="row"><button class="btn hot" id="redo">🔁 Redo misses</button><button class="btn" id="copy">📋 Copy misses</button><button class="btn" id="again">↺ New attempt</button></div>
<div id="misslist"></div></div><div class="toast" id="toast"></div>'''

js = common.TABJS + "const D=" + json.dumps(DATA) + ";const LECS=" + json.dumps(LECS) + r''';
let shuf=false,deck=[],i=0,ans=[],picked=false;
const sel=$('#lec');Object.keys(LECS).forEach(k=>{const n=D.filter(d=>d.l===k).length;sel.appendChild(el('option',null,LECS[k]+' ('+n+')')).value=k});
try{const s=localStorage.getItem('exam3p-shuf');if(s==='1')shuf=true}catch(e){}
function shufBtn(){$('#shuf').textContent='🔀 Shuffle: '+(shuf?'on':'off');$('#shuf').classList.toggle('hot',shuf);$('#shuf').setAttribute('aria-pressed',shuf)}
$('#shuf').onclick=()=>{shuf=!shuf;shufBtn();try{localStorage.setItem('exam3p-shuf',shuf?'1':'0')}catch(e){}};shufBtn();
function show(id){['setup','quiz','done'].forEach(x=>$('#'+x).classList.toggle('on',x===id));window.scrollTo(0,0)}
function makeDeck(src){return(shuf?sh(src):src.slice()).map(d=>{let idx=[0,1,2,3];if(shuf)idx=sh(idx);return{d,opts:idx.map(k=>d.opts[k]),a:idx.indexOf(d.a)}})}
function begin(src){if(!src.length)return;deck=makeDeck(src);i=0;ans=[];show('quiz');render()}
function render(){const c=deck[i];picked=false;$('#tag').textContent=LECS[c.d.l];$('#qn').textContent='Question '+(i+1)+' of '+deck.length;
 $('#stem').textContent=c.d.q;const o=$('#opts');o.innerHTML='';
 c.opts.forEach((t,k)=>{const b=el('button','chip');b.appendChild(el('b',null,'ABCD'[k]));b.appendChild(document.createTextNode(t));b.dataset.k=k;b.onclick=()=>pick(k);o.appendChild(b)});
 $('#fb').classList.remove('show');$('#next').disabled=true;$('#next').textContent=i===deck.length-1?'See results ▶':'Next ▶';score()}
function pick(k){if(picked)return;picked=true;const c=deck[i],ok=k===c.a;ans.push({c,ok,k});
 [...$('#opts').children].forEach((b,j)=>{if(j===c.a)b.classList.add('ok');else if(j===k)b.classList.add('bad','shake');else b.classList.add('dim')});
 $('#fb').innerHTML=(ok?'✅ Correct. ':'❌ Answer: <b>'+'ABCD'[c.a]+'. '+c.opts[c.a]+'</b>. ')+c.d.x;$('#fb').classList.add('show');$('#next').disabled=false;score()}
function score(){const r=ans.filter(a=>a.ok).length;$('#sc').textContent=r+'/'+ans.length+' correct';$('#bar').style.width=(100*(i+(picked?1:0))/deck.length)+'%'}
$('#next').onclick=()=>{if(!picked)return;if(i<deck.length-1){i++;render()}else finish()};
$('#quit').onclick=()=>{if(ans.length)finish();else show('setup')};
function misses(){return ans.filter(a=>!a.ok)}
function finish(){const r=ans.filter(a=>a.ok).length,n=ans.length;$('#final').textContent=r+' / '+n+' · '+(n?Math.round(100*r/n):0)+'%';
 const tb=$('#brk tbody');tb.innerHTML='';Object.keys(LECS).forEach(k=>{const a=ans.filter(x=>x.c.d.l===k);if(!a.length)return;const g=a.filter(x=>x.ok).length;
  const tr=el('tr');tr.innerHTML='<td>'+LECS[k]+'</td><td>'+g+' / '+a.length+'</td><td>'+Math.round(100*g/a.length)+'%</td>';tb.appendChild(tr)});
 const m=misses(),ml=$('#misslist');ml.innerHTML=m.length?'<h2 style="margin-top:12px">❌ Misses ('+m.length+')</h2>':'<p class="hint" style="margin-top:12px">No misses. 🎉</p>';
 m.forEach(a=>{const d=el('div','missli');d.innerHTML='<b>'+a.c.d.l+'</b> · '+a.c.d.q+'<br>✅ '+a.c.opts[a.c.a];ml.appendChild(d)});
 $('#redo').disabled=!m.length;$('#copy').disabled=!m.length;
 try{localStorage.setItem('exam3p-last',JSON.stringify(m.map(a=>a.c.d.q)))}catch(e){}
 show('done')}
$('#redo').onclick=()=>begin(misses().map(a=>a.c.d));
$('#again').onclick=()=>show('setup');
$('#start').onclick=()=>{const v=sel.value;begin(D.filter(d=>v==='all'||d.l===v))};
function toast(t){const e=$('#toast');e.textContent=t;e.style.display='block';setTimeout(()=>e.style.display='none',1800)}
$('#copy').onclick=()=>{const txt=misses().map((a,n)=>(n+1)+'. ['+LECS[a.c.d.l]+'] '+a.c.d.q+'\n   Answer: '+a.c.opts[a.c.a]).join('\n');
 const fallback=()=>{const t=el('textarea');t.value=txt;t.style.position='fixed';t.style.opacity='0';document.body.appendChild(t);t.select();let ok=false;try{ok=document.execCommand('copy')}catch(e){}t.remove();toast(ok?'📋 Misses copied':'Copy failed')};
 if(navigator.clipboard&&window.isSecureContext)navigator.clipboard.writeText(txt).then(()=>toast('📋 Misses copied'),fallback);else fallback();window.__lastCopy=txt};
document.addEventListener('keydown',e=>{if(!$('#quiz').classList.contains('on'))return;if(/^[1-4a-dA-D]$/.test(e.key)){const k=/\d/.test(e.key)?+e.key-1:'abcd'.indexOf(e.key.toLowerCase());pick(k)}else if(e.key==='Enter')$('#next').click()});'''

out = common.page('📝 Exam 3 Practice Exam', 'Gross Anatomy Lecture Exam 3 · 53 blueprint-weighted multiple-choice questions · tap an option for instant feedback',
                  body, js, back=f'gross-anatomy-lecture.html?v={V}')
open('gross-anatomy-exam3-practice.html', 'w').write(out)
print('ok', len(DATA), dict(cnt), 'letters', dict(sorted(DIST.items())))
