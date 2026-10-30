# Build: Exam 3 · Poole's END-OF-NOTES questions with answers (all 10 notes lectures), tap-to-reveal + 🔀 shuffle
# Source: classmate's answered set (structure + acid-base typed = key; rest handwritten), each answer checked vs lectures.
# Run from repo root AFTER tools/resp_terms.py (reuses its CSS/JS).
import re,time,html
E=html.escape; V=str(int(time.time()))
src=open('systems-lec3-pp3-terms.html').read()
css=re.search(r'<style>(.*?)</style>',src,re.S).group(1)
js=re.findall(r'<script>(.*?)</script>',src,re.S)[-1]
S=[ # (section, [(question, answer)])  ★ = repeats on old exams
('LC39 · Structure',[
 ('Why can the avian lung "arterialize" blood better than the mammalian lung?','Unidirectional flow: fresh air isn\'t mixed with low-O₂/high-CO₂ alveolar gas (mammal = "mixing pool") → alveolar PO₂ closer to inspired'),
 ('How does Fick\'s law explain lung structure?','Gas flow = Area/Thickness × D × (P alveolar − P blood) → huge surface area + thin barrier · O₂ (low solubility) needs ~60 mmHg gradient · CO₂ (high D) only ~6'),
 ('How are inhaled particles 1–5 µm cleared?','Sedimentation onto the walls of SMALL airways'),
 ('Key difference: conducting zone (dead space) vs respiratory zone?','Respiratory zone exchanges O₂/CO₂; dead space doesn\'t'),
 ('Species most affected by partial bronchiolar obstruction? Why?','PIGS and CATTLE: lobules not interconnected (no collateral ventilation) · dogs/cats have collateral airways'),
 ('Where is the greatest TOTAL airway cross-sectional area?','Respiratory zone'),
 ('3 primary alveolar cell types + function?','Type I: >90% of wall, thin barrier · Type II: surfactant (↓ surface tension, stiffness) · Alveolar macrophages: engulf tiny particles + bacteria'),
]),
('LC40 · Ventilation',[
 ('What determines red cell transit time? Change with exercise?','Pulmonary capillary blood volume ÷ cardiac output · rest ~0.75 s → exercise ~0.3 s or less'),
 ('Define functional residual capacity and residual volume','FRC = volume after a QUIET exhale (no muscle force) · RV = volume after a FORCEFUL exhale'),
 ('To raise alveolar ventilation, more efficient to ↑ tidal volume or frequency?','↑ TIDAL VOLUME (minimizes dead-space ventilation)'),
 ('★ Cow: expired PCO₂ 20, arterial PCO₂ 40. Dead space ÷ tidal volume?','Bohr: (40 − 20) ÷ 40 = 0.5 (50%)'),
 ('Sheep doubles alveolar ventilation, CO₂ production unchanged. Arterial PCO₂?','Halves → ~20 mmHg'),
 ('Which lung region gets the most ventilation?','Base in upright species (human, ape) · VENTRAL region in quadrupeds'),
]),
('LC41 · Diffusion',[
 ('★ Why is tracheal PO₂ < atmospheric, and alveolar < tracheal?','Trachea: water vapor added → (Pb − 47) × 0.2093 = 149 · alveoli: gas exchange + mixing with CO₂ → 149 − PaCO₂/R ≈ 99–100'),
 ('Solubilities of O₂ vs CO₂? Effect on diffusion?','O₂ 0.003 · CO₂ ~0.067 mL/100 mL/mmHg (~20× more) → CO₂ needs a much SMALLER pressure gradient'),
 ('Closed chamber, constant temperature, volume doubled. Pressure?','Boyle: P₁V₁ = P₂V₂ → pressure HALVES'),
 ('Healthy lung: time for capillary blood to equilibrate with alveolar gas?','~0.25 s (of ~0.75 s transit)'),
 ('Why severe hypoxemia in exercise in a dog with reduced diffusing capacity?','Thick/damaged barrier slows equilibration + exercise shortens transit time → not enough time to equilibrate'),
 ('Normal O₂ and CO₂ pressures: arterial, alveolar, venous?','Arterial & alveolar: PO₂ ~100, PCO₂ ~40 · venous (rest): PO₂ ~40, PCO₂ ~46 · venous (exercise): PO₂ <20, PCO₂ >60'),
]),
('LC42 · Pulmonary blood flow',[
 ('Structural evidence pulmonary pressures are lower than systemic?','Thinner-walled vessels, more elastic, less smooth muscle'),
 ('★ Principal mechanism of pulmonary capillary rupture in the exercising horse?','HIGH capillary pressure from very high cardiac output (LC50 adds: + very NEGATIVE alveolar pressure; they add across the barrier)'),
 ('How do you calculate pulmonary vascular resistance?','(Mean pulmonary artery pressure − left atrial pressure) ÷ cardiac output'),
 ('2 mechanisms by which pulmonary vascular resistance falls in exercise?','RECRUITMENT + DISTENSION'),
 ('★ Why is pulmonary vascular resistance lowest at moderate lung volumes?','Low volume: extra-alveolar vessels narrow (less radial traction) · high volume: alveolar capillaries stretched/squeezed → middle is lowest'),
 ('Fick: horse cardiac output 250 L/min, arterial O₂ 25, venous 4 mL/100 mL. VO₂?','250 × (25 − 4)/100 = 52.5 L/min'),
 ('How does gravity affect regional blood flow?','Hydrostatic forces send more flow to the BASE (ventral in quadrupeds) · not the only factor'),
]),
('LC43 · Causes of hypoxemia',[
 ('★ 5 causes of hypoxemia?','Low inspired O₂ · hypoventilation · diffusion limitation · shunt · ventilation/perfusion mismatch'),
 ('★ Tell hypoventilation from low inspired O₂?','PaCO₂: HIGH in hypoventilation · LOW with low inspired O₂ (carotid bodies → hyperventilation)'),
 ('★ Dog: barbiturate overdose halves alveolar ventilation, PaCO₂ was 40, R 0.8. New PaCO₂ and PaO₂?','PaCO₂ → 80 · PaO₂ ≈ 149 − 80/0.8 = 49 mmHg'),
 ('When a unit\'s ventilation/perfusion ratio increases, does alveolar PO₂ rise and PCO₂ fall?','YES'),
 ('Apex (dorsal, quadruped) vs base (ventral): ventilation/perfusion, PO₂, PCO₂, pH?','Apex/dorsal: HIGHER ratio, HIGHER PO₂, LOWER PCO₂, HIGHER pH'),
 ('Cat with marked mismatch, NO shunt, given 100% O₂. PaO₂ rises to?','ABOVE 500 mmHg (100% O₂ fixes mismatch; only shunt resists)'),
 ('★ Dog on air: PaO₂ 49, PaCO₂ 48, R 0.8. Alveolar–arterial difference?','Alveolar = 149 − 48/0.8 = 89 → 89 − 49 = 40 mmHg'),
]),
('LC44 · Mechanics',[
 ('Which DECREASES compliance: age, saline inflation, fibrosis?','FIBROSIS'),
 ('Two bubbles, same surface tension; A has twice B\'s diameter. Pressures?','Laplace: pressure in B (smaller) is TWICE that in A'),
 ('Surfactant is made by?','Type II alveolar cells'),
 ('Pneumothorax: lung? chest wall?','Lung RECOILS to a smaller volume · chest wall EXPANDS'),
 ('Healthy animal: most airway resistance is in?','LARGE airways (small total cross-sectional area)'),
 ('Why is expiratory flow so high at high lung volumes?','Flow = alveolar pressure ÷ resistance · high elastic recoil (driving pressure) + airways held open (low resistance)'),
 ('Why is much of the expiratory flow–volume loop "effort independent"?','Dynamic airway compression: flow set by recoil ÷ resistance, not muscle effort'),
 ('Breathing strategy with ↑ compliance + airway obstruction (emphysema)?','SLOW exhalation, ↑ mouth pressure to hold airways open ("pursed lips")'),
 ('★ Exercise: what causes "roaring" in horses? "Honking" in some dogs?','Roaring: laryngeal hemiplegia (INSPIRATION) · honking: tracheal collapse/compression (EXPIRATION)'),
]),
('LC45 · Blood gas transport',[
 ('Healthy dog on 100% O₂, PaO₂ 600. Dissolved O₂?','600 × 0.003 = 1.8 mL/100 mL'),
 ('Which shift the curve RIGHT: ↓ temperature, ↑ pH, ↑ PCO₂, ↑ 2,3-DPG?','↑ PCO₂ and ↑ 2,3-DPG'),
 ('How does P50 change across species?','SMALLER species = more right-shifted (higher P50) → offload O₂ for high metabolic rate (hamster an exception)'),
 ('★ O₂ content: (a) Hb 10, PaO₂ 100, 97% · (b) Hb 18, PaO₂ 80, 93%. When healthy?','(a) 13.0 + 0.3 = 13.3 · (b) 22.4 + 0.24 = 22.6 mL/100 mL · horse at REST (a) vs EXERCISE (b, spleen)'),
 ('Dog exposed to car exhaust (carbon monoxide). Arterial gases?','PO₂ NORMAL, PCO₂ normal, O₂ CONTENT ↓'),
 ('Most CO₂ in arterial and venous blood is carried as?','BICARBONATE'),
 ('Carbonic anhydrase blocked, carbamino share unchanged. Venous PCO₂ needed for venous–arterial CO₂ difference of 4 mL/100 mL?','70% (2.8 mL) must be dissolved: 2.8 ÷ 0.067 ≈ 42 mmHg above arterial → ~82 mmHg'),
 ('★ St. Bernard: cardiac output 4 → 2 L/min, same VO₂, P50 32. Extraction, venous PO₂, saturation?','Arteriovenous difference DOUBLES (5 → 10) · venous 10 of 20 = 50% saturated → PO₂ = P50 = 32 mmHg'),
]),
('LC46 · Acid–base (typed key)',[
 ('★ Everest summit: PCO₂ 7 mmHg. pH with NO bicarbonate dumping? With bicarbonate 14?','24 ÷ (0.03 × 7 = 0.21) = 114 → log 2.06 → 8.16 · 14 ÷ 0.21 = 66.6 → log 1.82 → 7.92'),
 ('Small dog: PO₂ 60, PCO₂ 110, pH 7.2. Deduction (think inspired gas)?','On room air alveolar PO₂ = 149 − 110/0.8 = 11.5 → measured 60 is impossible → dog must be on SUPPLEMENTAL O₂'),
 ('★ Pony: lactate ↑ 15 mM. pH if PCO₂ (a) stays 40 (b) falls to 20?','(a) 9 ÷ 1.2 = 7.5 → 6.98 · (b) 9 ÷ 0.6 = 15 → 7.28 (key writes "Log[7.5]" for b: typo, answer 7.28 is right)'),
 ('★ pH >7.4, bicarbonate 40, PCO₂ 50?','Metabolic alkalemia · respiratory compensation · can\'t tell acute vs chronic'),
 ('★ pH <7.4, bicarbonate 36, PCO₂ 80?','Respiratory acidemia · metabolic compensation · CHRONIC'),
 ('★ pH <7.4, bicarbonate 10, PCO₂ 30?','Metabolic acidemia · respiratory compensation · can\'t tell acute vs chronic'),
 ('★ pH >7.4, bicarbonate 24, PCO₂ 15?','Respiratory alkalemia · ACUTE (bicarbonate still normal = kidneys haven\'t compensated yet)'),
]),
('LC48 · Control of breathing',[
 ('Where is the rhythmicity center?','MEDULLA'),
 ('Breathing pattern after midpontine section?','Deep inspiratory gasping (slower, deeper breaths)'),
 ('Hering–Breuer reflex inhibits?','INSPIRATION'),
 ('★ Most important arterial control of breathing normally: PO₂, PCO₂, pH?','PCO₂'),
 ('★ Principal O₂ sensor? Pressure or content?','Peripheral chemoreceptors (carotid + aortic bodies) · PO₂ (pressure), not content'),
 ('★ Dog with chronic CO₂ retention given 100% O₂: why very high PaCO₂?','High O₂ silences carotid/aortic bodies (its hypoxic drive) → ↓ ventilation · (+ Haldane: more O₂ → hemoglobin holds less CO₂)'),
 ('High-CO₂ gas breathed: which receptors trigger the INITIAL increase?','PERIPHERAL (only seconds downstream of the lung) · central give most of the sustained response'),
 ('★ PO₂ where peripheral chemoreceptors take powerful control? Why?','~60 mmHg · above that, O₂ CONTENT barely falls (flat top of the curve)'),
]),
('LC49 · Exercise',[
 ('★ Phases I–III of ventilation at exercise onset?','I: ↑ cardiac output/pulmonary blood flow · II: venous blood (↓ O₂, ↑ CO₂) arrives + cardiac output keeps rising · III: steady state'),
 ('★ Why can\'t the horse make a respiratory compensation at max exercise (numbers)?','Alveolar ventilation = (CO₂ output ÷ PaCO₂) × 863 → lowering PaCO₂ to 30 needs ~2,300–2,600 L/min → too high'),
 ('Can VO₂ and lactate stabilize in the SEVERE domain?','NO'),
 ('Muscle venous O₂ vs mixed venous in heavy exercise?','Much LOWER: muscle extracts a higher % of arterial O₂'),
 ('Splenic red cell dumping: effect on O₂ transport and VO₂max?','↑ arterial O₂ content → ↑ VO₂max'),
 ('Why doesn\'t exercising muscle extract ALL O₂?','Diffusing capacity is not infinite (needs a PO₂ gradient)'),
 ('Resting VO₂ vs body size? Highest resting metabolic rate?','Smaller = higher VO₂/kg (more surface area/mass → heat loss) · Etruscan shrew (~2 g)'),
]),
]
rows=lambda it:''.join(f'<tr class="{"hy" if q.startswith("★") else ""}"><td>{E(q)}</td><td><span class="ans">{E(a)}</span></td></tr>' for q,a in it)
secs=''.join(f'<div class="sec{" p" if i%2 else ""}"><h2>{E(s)}</h2><table>{rows(it)}</table></div>' for i,(s,it) in enumerate(S))
n=sum(len(i) for _,i in S)
trap='<div class="sec trap"><h2>⚠️ Notes on the answers</h2><ul><li>Structure + acid–base answers are TYPED (Poole\'s key) · the rest are a classmate\'s handwriting, checked against the lectures</li><li>Blood flow Q2: the full EIPH answer also needs very NEGATIVE alveolar pressure (LC50)</li><li>Acid–base Q3b: key shows "Log[7.5]" but the math is 9 ÷ 0.6 = 15 → pH 7.28</li><li>Acid–base Q4d: "acute" because bicarbonate is still 24 (no renal compensation yet)</li></ul></div>'
bar='<div class="bar"><script defer src="shuffle.js"></script><button id="hide">🙈 Hide all</button><button id="all">👀 Show all</button><span class="n" id="n"></span></div>'
open('systems-lec3-notesqs.html','w').write(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>❓ Poole End-of-Notes Questions</title><style>{css}</style></head><body><div class="wrap"><a class="back" href="systems-lec-exam3.html?v={V}">← Back to Exam 3</a><div class="hero"><h1>❓ Poole\'s End-of-Notes Questions</h1><p>All 10 notes lectures · {n} questions with answers · his quizzes and exams reuse these</p></div><div class="key">★ pink = also on the 2023/2024 old exams</div>{bar}{secs}{trap}<div class="foot">🎀 Bethany · K-State CVM Class of 2030 · 🐾</div></div><script>{js}</script></body></html>')
print(n)
