# Build: Veterinary Systems I · Lecture Exam 4 (Renal = syllabus Exam 5, Fri 11/20, 91 pts, Basel)
# One-page tap-to-reveal Terms Review per lecture + the Exam 4 hub + the Systems Lecture hub tile.
# Run from repo root: python3 tools/sys_lec4_terms.py
# Reuses the Exam 3 look: css/js are read straight out of tools/resp_terms.py (not copied).
# Sources: LC52 + LC53+54 slides (Basel) and the Renal 1/2/3 transcripts (10/27, 11/2, 11/3).
import os,re,time,html,ast
E=html.escape; V=str(int(time.time()))
HUB='systems-lecture.html'; E4='systems-lec-exam4.html'; E3='systems-lec-exam3.html'; E2='systems-lec-exam2.html'

# ---- reuse the Exam 3 page styling + tap/hide/show script ----
_src=open('tools/resp_terms.py').read()
_vals={n.targets[0].id:n.value.value for n in ast.parse(_src).body
       if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id in('css','js') and isinstance(n.value,ast.Constant)}
css,js=_vals['css'],_vals['js']

# (slug, title, who, [(term, short answer)])  — '★ ' prefix = Basel emphasized → pink row · (S#) = slide number
SECS=[
('lc52','LC52 · Renal System 1','Basel · body fluid compartments & kidney anatomy · Tue 10/27',[
 ('Total body water','~60% of body weight (S4)'),
 ('Intracellular fluid (ICF)','~2/3 of body water = ~40% of body weight (S4)'),
 ('Extracellular fluid (ECF)','~1/3 of body water = ~20% of body weight · split into intravascular (plasma) + interstitial (tissue) fluid (S4)'),
 ('Hole-in-the-bucket model','Reaches a STEADY STATE, but not homeostasis: more input → more fluid stays in the system (S5)'),
 ('Steady-state model with a sensor','Sensor compares fluid level to a SET POINT → effector opens/closes the "hole" → same fluid level at any input (S6)'),
 ('2 things needed for fluid homeostasis','A way to SENSE fluid level + a way to CHANGE how much fluid is retained (S6)'),
 ('★ Table 12.1 (Basel: "pretty important to memorize")','ECF vs ICF ion concentrations (S7) · rows below'),
 ('★ Sodium (Na⁺)','ECF 145 mM · ICF 10 mM (S7)'),
 ('★ Potassium (K⁺)','ICF 140 mM · ECF 5 mM (S7)'),
 ('★ Chloride (Cl⁻)','ECF 110 mM · ICF 5–15 mM (S7)'),
 ('Bicarbonate (HCO₃⁻)','ECF 25 mM · ICF 12 mM (S7)'),
 ('Calcium (Ca²⁺)','ECF 1–2 mM · ICF free ~10⁻⁴ mM (S7)'),
 ('pH inside vs outside cells','ICF 7.2 · ECF 7.4 (S7)'),
 ('Why the kidney must reabsorb/secrete solutes','Losing plasma fluid alone would dump huge amounts of Na⁺ and Cl⁻ → must match solute output to intake (S7)'),
 ('Osmosis','Water moves from LOW solute (high water) to HIGH solute (low water) across a semipermeable membrane (S9)'),
 ('Osmotic pressure','Force of that water flow · proportional to the NUMBER of particles in solution (S9)'),
 ('Osmolarity','Sum of the molarity of ALL solutes (S9)'),
 ('Semipermeable membrane','Lets water through but not solute (S9)'),
 ('Hypertonic solution → cell?','Cell loses water and SHRINKS (S10)'),
 ('Hypotonic solution → cell?','Cell takes on water, SWELLS, may burst (S10)'),
 ('Aquaporins','Water channel proteins → water crosses membranes much faster · number available decides if/how fast water moves (S10)'),
 ('Add NaCl to the ECF','ECF swells, ICF shrinks, both end at a higher osmolarity (e.g., 280 → 300) (S11)'),
 ('★ Why RAAS raises blood pressure (Basel: memorize every part of RAAS)','Puts salt (Na⁺) into the ECF → water follows into the ECF → ↑ blood volume → ↑ blood pressure'),
 ('Hydrostatic pressure','Mechanical pressure on a fluid · the heart pushes fluid from plasma toward the interstitium (S13)'),
 ('Oncotic pressure','Colloid osmotic pressure from TRAPPED macromolecules (proteins) · holds fluid in the vessel · opposes hydrostatic pressure (S14)'),
 ('Plasma vs interstitium membrane','Capillary wall: small ions/molecules pass freely, proteins do not (S14)'),
 ('Interstitium vs cell membrane','Nearly perfect semipermeable membrane (plasma membrane) (S14)'),
 ('★ Starling equation','Fluid movement = Kf × [(Pc + πi) − (Pi + πc)] · pushing out minus pushing in (S15)'),
 ('Kf','Filtration coefficient = properties of the barrier (S15)'),
 ('Pc · πi · Pi · πc','Capillary hydrostatic · interstitial oncotic · interstitial hydrostatic · capillary oncotic (S15)'),
 ('3 kidney jobs (S17)','Filtration (plasma from blood) · secretion/reabsorption (change filtrate composition) · concentration/dilution (keep or dump water)'),
 ('Nephron','Basic functional unit: filtration, reabsorption, secretion (S18)'),
 ('Nephron segments in order','Glomerulus → proximal convoluted tubule → thin descending loop of Henle → thin ascending → thick ascending → distal convoluted tubule (→ collecting duct*) (S18)'),
 ('Collecting duct','Water maintenance · asterisk: not technically part of the nephron (S18)'),
 ('In the cortex','Glomerulus, proximal + distal convoluted tubules (S20)'),
 ('Loop of Henle path','Cortex → medulla → back to cortex (S20)'),
 ('Collecting duct path','Cortex down through the medulla (S20)'),
 ('Pars convoluta (cortical labyrinth)','Has the GLOMERULI + proximal and distal convoluted tubules (S21)'),
 ('Pars radiata (medullary ray)','Straight parts: loops of Henle + collecting ducts · no glomeruli (S21)'),
 ('Renal lobule','Middle of one medullary ray to the middle of the next (S21)'),
 ('Arcuate vessels','Run along the corticomedullary junction (S19, S28)'),
 ('★ Normal body osmolarity','~280 mOsm (275–295) · Basel rounds to 300 for math (S23)'),
 ('★ Medullary interstitium osmolarity','~300 at the top → up to 1200 mOsm at the apex (~3.6% saline) · pulls water out of filtrate · tunable (S23)'),
 ('Cortical (superficial) nephron','High in cortex · SHORT loop of Henle · barely enters medulla (S24)'),
 ('Juxtamedullary (deep) nephron','Deep in cortex · LONG loop deep into medulla → concentrated urine (S24)'),
 ('Nephron number scales with…','Body size / blood volume (cat ~0.18 M, dog ~0.4 M, human ~1 M per kidney) (S25)'),
 ('Concentrating ability scales with…','% long-looped nephrons + medullary thickness (beaver 0% = dilute · jerboa ~33% = very concentrated) (S26)'),
 ('Freezing point depression','Higher urine osmolarity → lower freezing point (S26)'),
 ('Renal blood flow at rest','~20–25% of cardiac output (S27)'),
 ('★ Renal blood flow pathway','Renal a. → interlobar a. → arcuate a. → interlobular a. → afferent arteriole → glomerulus → efferent arteriole → peritubular capillaries / vasa recta → interlobular v. → arcuate v. → interlobar v. → renal v. (S29)'),
 ('Vasa recta','Straight capillaries off juxtamedullary efferent arterioles that dip deep into the medulla (S30)'),
]),
('lc53','LC53 · Renal System 2','Basel · glomerulus, filtration, flow & autoregulation · Mon 11/2 · LC53+54 S1–17',[
 ('Glomerulus','"Ball of thread" · tuft of capillaries where filtration happens (S7)'),
 ('Bowman\'s (capsular) space','Space the filtrate is pushed into (S6)'),
 ('Bowman\'s (glomerular) capsule','Squamous cells that hold the initial filtrate (S6)'),
 ('Renal corpuscle','Glomerulus + Bowman\'s capsule (S5–6)'),
 ('★ Afferent arteriole','Brings blood INTO the glomerulus (S6)'),
 ('★ Efferent arteriole','Takes blood OUT · a second arteriole (not a vein) → the kidney controls BOTH ends of the capillary bed (S6)'),
 ('Vascular pole','Where the afferent + efferent arterioles enter/leave (S6)'),
 ('Urinary pole','Where Bowman\'s space joins the proximal convoluted tubule · FILTRATE leaves here (S6)'),
 ('Section shows no pole?','Plane-of-section issue · every glomerulus has both poles, usually on opposite sides'),
 ('3 cell types in the glomerulus','Endothelial cells · podocytes (epithelial "foot cells") · mesangial cells (connective tissue support)'),
 ('Fenestrated endothelium','Capillary lining full of holes · first, coarse filter (S8)'),
 ('★ The REAL filter','Fused basement membrane (basal lamina) (S8)'),
 ('Podocytes','Foot processes wrap the capillary · SUPPORT the basement membrane so it can take high pressure (like a mesh behind filter paper) (S8)'),
 ('Filtration slit','Gap between podocyte foot processes where fluid exits (S8, S10)'),
 ('★ Filtration barrier = 3 layers','Fenestrated endothelium → fused basement membrane → podocytes (S8)'),
 ('★ Size (most important factor)','Freely filtered < ~2 nm radius (~15 kDa) · not filtered approaching ~4 nm (~70 kDa) · in between = partial (S10)'),
 ('Charge','Basement membrane is NEGATIVE (glycosaminoglycans, sulfate groups) → positive molecules filter faster, negative slower · matters most near the size cutoff (S10)'),
 ('Shape','Least important · smallest diameter matters; long thin molecules can slip through (S10)'),
 ('★ Rule 1 · small molecules & ions (Basel: "star this 7 times")','FREELY filtered → filtrate concentration = blood concentration EXACTLY (S11)'),
 ('★ Rule 2 · small proteins','e.g., myoglobin (17 kDa, ~2 nm) → PARTIALLY filtered → filtrate concentration < blood, but present (S11)'),
 ('★ Rule 3 · large proteins & cells','e.g., albumin (66.5 kDa, ~3.6 nm), RBCs → NOT filtered → filtrate ≈ 0 (S11)'),
 ('Why albumin isn\'t filtered (just under cutoff)','It is NEGATIVELY charged → repelled by the basement membrane (S11)'),
 ('★ Glomerular filtration equation','GFR = Kf × [(PGC + πBS) − (PBS + πGC)] (S12)'),
 ('PGC (glomerular capillary hydrostatic)','~50 mmHg, and it STAYS ~50 along the whole glomerulus (efferent resistance prevents the usual drop) (S12)'),
 ('πBS (Bowman\'s space oncotic)','~0 mmHg (almost no protein filtered) (S12)'),
 ('PBS (Bowman\'s space hydrostatic)','~10 mmHg · rises with urinary/tubular OBSTRUCTION → filtration stops (S12)'),
 ('πGC (glomerular capillary oncotic)','~25 mmHg in → up to ~40 by the end (protein concentrates as fluid leaves) (S12)'),
 ('★ Ultrafiltration pressure (UFP)','Start: 50 − (10 + 25) = 15 mmHg · end (low flow): 50 − (10 + 40) = 0 (S12)'),
 ('Low flow rate','Blood concentrates fast → oncotic pressure rises fast → UFP hits 0 early · efficient per unit blood, low total (S13)'),
 ('High flow rate','Oncotic pressure rises slowly → UFP stays up across the glomerulus → more filtrate per minute (S13)'),
 ('Which flow does the kidney prefer?','HIGH · it cares about total filtrate per TIME, not per unit of blood'),
 ('★ GFR','Fluid filtered per unit TIME (S14)'),
 ('★ Filtration fraction (FF)','GFR ÷ renal plasma flow = fluid filtered per unit BLOOD (efficiency) (S14)'),
 ('Low flow → ?','Low GFR → bad, fast (S14)'),
 ('Very high flow → ?','Diminishing GFR returns + strain on the barrier + low FF → bad, slowly (S14)'),
 ('Body defends low or high pressure more?','LOW · low = death in hours–days · high = damage over decades'),
 ('Optimal human renal blood flow','~600 mL/min (🔹 mentioned)'),
 ('★ Afferent constriction','↓ glomerular pressure · ↓ renal blood flow · ↓ GFR (S15)'),
 ('★ Afferent dilation','↑ glomerular pressure · ↑ renal blood flow · ↑ GFR (S15)'),
 ('★ Efferent constriction','↑ glomerular pressure · ↓ renal blood flow · ↑ GFR* (S15)'),
 ('★ Efferent dilation','↓ glomerular pressure · ↑ renal blood flow · ↓ GFR (S15)'),
 ('*Severe efferent constriction','Can eventually LOWER GFR: very low blood flow → oncotic pressure climbs fast (S15)'),
 ('Ratio of afferent : efferent tone sets…','Glomerular PRESSURE'),
 ('Total tone (both open or both closed) sets…','FLOW rate (pressure barely changes)'),
 ('★ Autoregulation','AFFERENT arteriole constricts when pressure rises, dilates when it falls → constant renal blood flow + GFR over MAP ~80–170 mmHg (S17)'),
 ('Autoregulation mechanism','Stretch-sensitive ion channels in the vessel wall (myogenic) (S17)'),
 ('Afferent vs efferent autoregulation','Both can, but AFFERENT is much stronger'),
 ('Below the minimum pressure','Afferent can\'t dilate any more → autoregulation fails → GFR drops'),
 ('"I Love Lucy" conveyor belt','Faster tubular flow → less time to pull Na⁺ out → MORE Na⁺ reaches the macula densa'),
]),
('lc54','LC54 · Renal System 3','Basel · TGF, RAAS, ANP, O₂, NSAIDs, GFR markers, disease · Tue 11/3 · LC53+54 S18–40',[
 ('★ Why low Na⁺ at the macula densa = low flow','Slow filtrate spends more time in the thick ascending limb → more Na⁺ pulled out → LOW Na⁺ at the macula densa (S18)'),
 ('Thick ascending limb','Active Na⁺ reabsorption → makes the filtrate HYPOtonic'),
 ('Macula densa','"Dense spot": stacked nuclei in the distal convoluted tubule wall where it passes the vascular pole · senses Na⁺/Cl⁻ (S20–21)'),
 ('Juxtaglomerular apparatus','Macula densa + granular cells (+ afferent arteriole) at the vascular pole (S20–21)'),
 ('Granular (juxtaglomerular) cells','Release RENIN (S21)'),
 ('★ Tubuloglomerular feedback (TGF)','Low macula densa NaCl → prostaglandin E2 → AFFERENT DILATION (immediate) (S18–19)'),
 ('★ 3 layers of GFR defense (in order)','1 Autoregulation → 2 Tubuloglomerular feedback → 3 RAAS'),
 ('★ 2 main triggers of renin release','Prostaglandin signal from the macula densa + SYMPATHETIC input (epinephrine/norepinephrine) (S22)'),
 ('Heart failure link','Sympathetic overactivation → renin → RAAS activation'),
 ('★ RAAS cascade','Renin cleaves angiotensinogen → angiotensin I · ACE (angiotensin-converting enzyme) → angiotensin II (S22–23)'),
 ('★ Angiotensin II on the arterioles','Constricts the EFFERENT arteriole (afferent is not very sensitive) → ↑ glomerular pressure → ↑ GFR (S22)'),
 ('★ RAAS effect on filtration fraction','↑ FF (afferent open + efferent closed → blood slows, more fluid pulled per unit)'),
 ('★ Angiotensin II → aldosterone','Adrenal gland → aldosterone → ENaC (epithelial Na⁺ channel) inserted in the collecting duct → Na⁺ + water retained (S22–23)'),
 ('Where retained Na⁺ + water go','EXTRACELLULAR → ↑ plasma volume → ↑ mean arterial pressure → ↑ glomerular pressure (S23)'),
 ('RAAS defends against…','LOW blood pressure (S23)'),
 ('★ Atrial natriuretic peptide (ANP)','Released by atrial STRETCH (esp. right atrium) from high volume/preload → natriuresis → ↓ Na⁺/water retention (S24–25)'),
 ('ANP vs aldosterone','ANP opposes aldosterone almost exactly (opposite molecular pathways) · defends against HIGH volume/pressure (S25)'),
 ('ANP receptor type','Guanylyl cyclase receptor'),
 ('Peritubular capillaries','After the efferent arteriole · run along the proximal tubule · deep ones = vasa recta'),
 ('★ Renal O₂ use','~80% tied to active Na⁺ transport · highest in PCT + thick ascending limb (Na⁺/K⁺-ATPase) (S26)'),
 ('O₂ consumption ≈','GFR × tubular Na⁺ reabsorption fraction (S26)'),
 ('Medulla O₂ normally','Already near-hypoxic (PCT uses O₂ upstream) (S26)'),
 ('★ Why efferent constriction risks the medulla','↓ renal blood flow (less O₂ delivered) + ↑ FF (more Na⁺ load = more O₂ demand) → medullary hypoxia → acute tubular necrosis (S26)'),
 ('Opening EITHER arteriole → renal perfusion?','INCREASES (total resistance = both arterioles added together)'),
 ('★ NSAIDs and the kidney','Block prostaglandin E2 → afferent can\'t dilate (closes) → ↓ perfusion, ↓ GFR, ↓ medullary O₂ → acute kidney injury / acute tubular necrosis (S27–28)'),
 ('★ NSAID high-risk patients','Hypotensive, hypovolemic, or on an ACE inhibitor / ARB (angiotensin receptor blocker) · dogs more sensitive (S27–28)'),
 ('Clearance','VOLUME of plasma cleared of a substance per TIME (mL/min) (S30)'),
 ('Clearance routes','Liver (bile) · lungs (volatile) · skin (sweat) · KIDNEY = most important'),
 ('★ Clearance formula','Px × Cx = Ux × V̇ → Cx = (Ux × V̇) ÷ Px · P = plasma conc, U = urine conc, V̇ = urine flow (S30)'),
 ('★ When does clearance = GFR?','Substance is (1) FREELY filtered and (2) NOT reabsorbed or secreted (+ constant plasma concentration) (S31)'),
 ('Why research GFR markers are impractical','Need constant blood concentration → IV infusion / overnight stay'),
 ('Normal dog GFR','3.5–4.5 mL/min/kg · below 1.5 = pathological (S31)'),
 ('★ Creatinine source','Spontaneous breakdown of creatine phosphate in skeletal muscle → steady production ∝ muscle mass (S32)'),
 ('★ Creatinine as a GFR marker','~200 Da → freely filtered · only tiny secretion · ↓ GFR → ↑ serum creatinine (S32)'),
 ('Creatinine confounder','Muscle wasting (less production) (S32)'),
 ('★ When does creatinine rise?','Only after ~75% loss of GFR → poor early marker; good for screening/monitoring CKD (S33)'),
 ('★ SDMA (symmetric dimethylarginine)','Amino acid metabolism byproduct · freely filtered · rises at ~25% GFR loss → MORE sensitive (S33)'),
 ('IRIS staging','Chronic kidney disease stages 1–4 by creatinine / SDMA (S33)'),
 ('Cystatin C','~13 kDa cysteine-protease inhibitor made by almost every cell · filtered · reabsorbed AND destroyed in the PCT → never returns to blood → good GFR marker (dogs) (S34)'),
 ('★ BUN (blood urea nitrogen)','Urea is freely filtered but reabsorbed AND secreted · changes with diet, hydration, metabolism → POOR GFR marker (S35)'),
 ('↑ BUN + normal creatinine','Often PRErenal azotemia (S35)'),
 ('Azotemia','↑ BUN and/or creatinine in blood (S37)'),
 ('Glomerular disease','Inflammation or structural damage to the glomerulus (glomerulonephritis, glomerulosclerosis) → impaired filtration (S37)'),
 ('★ 2 hallmarks of glomerular disease','↓ GFR (lower Kf) + PROTEINURIA (leaky barrier) (S37)'),
 ('★ UPC (urine protein:creatinine) cutoff','> 0.5 dogs · > 0.4 cats (5–10 in severe disease) (S37)'),
 ('Other glomerular disease signs','Hematuria · weight/muscle loss (protein loss) · hypertension (RAAS) · edema (low albumin → low oncotic pressure) (S37)'),
 ('Glomerular disease "doom loop"','Kidney thinks flow is low → RAAS → hypertension → more glomerular damage'),
 ('★ Glomerular disease treatment','Treat the cause + LOWER blood pressure · ACE inhibitors (block RAAS) · diuretics less useful (need filtration) (S38)'),
 ('Acute kidney injury (AKI)','SUDDEN, substantial drop in GFR · can recover (S39)'),
 ('Chronic kidney disease (CKD)','> 3 months loss of usable nephrons → ↓ GFR · unlikely to recover (S39)'),
 ('AKI causes','Trauma · ischemia (clot) · infection (leptospirosis, pyelonephritis) · nephrotoxins (ethylene glycol, grapes, NSAID overdose) (S40)'),
 ('CKD causes','Recurrent AKI · diabetes · hypertension · kidney stones · glomerulonephritis · polycystic kidney disease (cats, genetic) · unknown (S40)'),
 ('CKD support (🔹 preview)','Reduce sodium and phosphate load'),
]),
('lc57','LC57 · Renal System 6','Basel · countercurrent multiplication & urea recycling · Fri 11/6 · LC57+58 S4–17',[
 ('★ NKCC (NKCC2) — Basel: "memorize, have it off the top of your head"','Na⁺/K⁺/2Cl⁻ cotransporter in the THICK ascending limb · secondary active NaCl reabsorption (K⁺ leaks back to the lumen) (S5)'),
 ('★ Why the medulla is salty (3 parts)','1 Active NaCl transport in the thick ascending limb (NKCC + Na⁺/K⁺-ATPase) · 2 Different permeabilities of the thin limbs · 3 Countercurrent flow + vasa recta exchange (S5–6)'),
 ('Gradient NKCC alone can make','~200 mOsm across the thick ascending limb wall (S5)'),
 ('Thin descending limb permeability','WATER yes · salt no → water leaves into the salty medulla, filtrate concentrates (S5)'),
 ('Thin ascending limb permeability','Na⁺ yes (passive) · water no (S5, S7)'),
 ('★ Thick ascending limb','Water-IMPERMEABLE + pumps NaCl out → filtrate becomes HYPOtonic ("diluting segment") (S7)'),
 ('Countercurrent multiplication','Opposite-direction flow in the two loop limbs multiplies the small 200 mOsm step into a large top-to-bottom gradient (S5–6)'),
 ('★ What the whole gradient system depends on','NKCC · no active NaCl pumping = no gradient at all'),
 ('Vasa recta','Medullary capillaries running OPPOSITE to the loop · countercurrent EXCHANGE: carry Na⁺ down, water up · preserve the gradient while returning reabsorbed water/solute (S6)'),
 ('Multiplication vs exchange','Multiplication = the LOOP, powered by NKCC, BUILDS the gradient · exchange = the VASA RECTA, passive, PRESERVES it'),
 ('★ How far NaCl mechanisms alone get the medulla','~600 mOsm (half of the ~1200 maximum)'),
 ('★ Where the other ~600 mOsm comes from','UREA (up to half the inner-medulla osmoles) → total ~1200 (S14)'),
 ('Gradient needs constant power','If NKCC or flow slows, the gradient washes out · very hydrated (diuresis) → less salty medulla'),
 ('Flow effect on loop reabsorption','Slower flow = more efficient reabsorption + more hypotonic filtrate · faster = less (S7)'),
 ('Net effect of the loop (S7)','Thin loop = water + Na⁺ reabsorbed together (isotonic) · thick ascending = Na⁺ only → hypotonic filtrate to the distal tubule'),
 ('High vs low GFR at the macula densa','High GFR = fast flow = HIGH Na⁺ at the distal tubule · low GFR = slow flow = LOW Na⁺ (S9)'),
 ('Urea','Nitrogen waste from protein metabolism · freely filtered (S11)'),
 ('Urea along the nephron (S11)','Proximal tubule reabsorbs ~50% · thin loop SECRETES ~60% (more than filtered) · collecting duct reabsorbs ~70% · ~40% excreted'),
 ('BUN and GFR','Urea is filtered but also reabsorbed + secreted; diet and metabolism change it → BUN only roughly tracks GFR (S12)'),
 ('★ Urea transport is always…','PASSIVE · it cannot build a gradient by itself (S13)'),
 ('Urea in the proximal tubule','Follows water reabsorption (S13)'),
 ('Urea transporter, thin descending limb','UT-A2 (S13)'),
 ('★ Urea transporters, inner medullary collecting duct','UT-A1 and UT-A3 · controlled by ADH (vasopressin) (S13)'),
 ('★ Urea recycling','Water leaves the collecting duct → urea concentrates → inner-medullary collecting duct lets urea out into the interstitium → urea enters the thin loop → comes back around → gradient builds (S14)'),
 ('★ High ADH and urea','More UT-A1/A3 → more urea in the medulla → higher osmolarity → more water reabsorbed → ANTIdiuresis (S15–16)'),
 ('★ Low ADH and urea','Fewer UT-A1/A3 → less medullary urea → weaker gradient → less water reabsorbed → diuresis (S15–16)'),
 ('What the kidney actually tunes to set the gradient','UREA (via ADH) · the NaCl part just depends on flow + NKCC'),
 ('Medullary osmolarity rule','Higher medullary osmolarity = more driving pressure to reabsorb water (S16)'),
]),
('lc58','LC58 · Renal System 7','Basel · ADH, diabetes insipidus, volume vs osmolarity, diuretics · Fri 11/6 · LC57+58 S18–41',[
 ('★ Slide 19 — Basel: "know this slide very, very well"','Collecting-duct filtrate is very HYPOtonic (NKCC + NCC) · medulla is very HYPERtonic (countercurrent + urea) · if water has a PATHWAY it moves out · shrink that difference = diuresis (S19, S32)'),
 ('★ Why collecting-duct filtrate is hypotonic','NKCC (thick ascending limb) and NCC (distal convoluted tubule) pull out salt where water cannot follow (S19)'),
 ('★ Why the medulla is hypertonic','Countercurrent multiplication (NaCl) + urea concentration (S19)'),
 ('Filtrate osmolarity along the nephron (S19)','Bowman\'s 300 · proximal tubule 300 · loop tip ~1000 · end of thick ascending ~200 · distal tubule/early collecting duct ~100'),
 ('NCC','Na⁺/Cl⁻ cotransporter in the DISTAL convoluted tubule (S19)'),
 ('Where ADH is made vs released','Made in the HYPOTHALAMUS (magnocellular neurons) · released from the POSTERIOR pituitary (S20)'),
 ('ADH = AVP','Antidiuretic hormone = arginine vasopressin'),
 ('★ Osmoreceptors','Magnocellular neurons with many aquaporins → water moves in/out easily → cell size tracks ECF osmolarity (S20)'),
 ('★ High ECF osmolarity → ADH (steps)','1 Water leaves the neuron · 2 neuron shrinks · 3 stretch-inactivated TRPV1 channels depolarize it · 4 more action potentials · 5 ADH released (S20)'),
 ('★ Main control of ADH release','Systemic OSMOLARITY · high = ↑ ADH · low = ↓ ADH (S20)'),
 ('ADH half-life','~20 minutes'),
 ('★ ADH in the collecting duct','Inserts aquaporins (AQP2) + urea transporters on the LUMINAL side → water reabsorbed + urea recycling ↑ (S22)'),
 ('AVPR2 (V2) vs AVPR1 (V1)','V2 = collecting duct, water retention · V1 = vessels, constriction (S29–30)'),
 ('★ ADH changes what in urine?','WATER excreted, not solute excreted (S23)'),
 ('High ADH → urine?','Small volume, very CONCENTRATED = antidiuresis (S23)'),
 ('Low ADH → urine?','Large volume, very DILUTE = water diuresis (S23)'),
 ('★ Diabetes insipidus (DI)','Loss of ADH signaling · "insipidus" = tasteless · persistent polyuria/polydipsia (PU/PD) (S24)'),
 ('★ DI lab picture','LOW urine specific gravity (near 1.000) · HIGH plasma osmolarity · urine won\'t concentrate with water deprivation (S24)'),
 ('Urine specific gravity (USG)','Density of urine vs water (water = 1.000) · higher = more concentrated · normal roughly 1.030–1.060 (🔹 ranges later)'),
 ('Water deprivation test','Psychogenic overdrinking → USG RISES · true DI → USG stays LOW'),
 ('★ Central DI','Hypothalamus/posterior pituitary fails to make or secrete ADH (S25)'),
 ('★ Nephrogenic DI','Collecting duct fails to RESPOND to ADH (S25)'),
 ('★ Desmopressin response test','Central DI → urine concentrates (USG ↑) · nephrogenic DI → no change (S25)'),
 ('Desmopressin','ADH analog · much longer half-life (about twice-daily dosing) · targets kidney more than blood pressure (S25)'),
 ('Central DI treatment','Desmopressin (replaces missing ADH) (S25)'),
 ('Nephrogenic DI treatment','Harder · thiazide diuretic (mild hypovolemia → less urine) · lots of water · low-sodium/low-protein diet (S25)'),
 ('★ Two reasons to reabsorb water (S26)','Lower OSMOLARITY (water without solute) vs raise VOLUME (water + Na⁺)'),
 ('★ ADH alone regulates…','OSMOLARITY (water without much solute) (S26)'),
 ('★ RAAS / aldosterone regulates…','VOLUME (Na⁺ + water) (S26–29)'),
 ('Aldosterone in the collecting duct','↑ number + open probability of ENaC in principal cells → Na⁺ reabsorbed, K⁺ lost (via ROMK) (S28)'),
 ('★ Angiotensin II and ADH','Angiotensin II also stimulates ADH release → aldosterone (↑ Na⁺) + ADH (↑ water) → ↑ ECF/blood volume (S29)'),
 ('ANP and volume','Inhibits renin/RAAS, aldosterone, AND ADH → less Na⁺ and water retained (S30)'),
 ('★ How diuretics work (general rule)','RAISE filtrate osmolarity (often also lower medullary osmolarity) → less pull on water → more urine (S32)'),
 ('Carbonic anhydrase inhibitors','Acetazolamide · block bicarbonate reabsorption in the proximal tubule → ↑ HCO₃⁻ in filtrate → ↑ osmolarity · rarely used (acid-base effects) (S33–34)'),
 ('★ Loop diuretics','Furosemide · block NKCC in the thick ascending limb → ↑ Na⁺ in the collecting duct AND wash out the medullary gradient ("double whammy") → STRONGEST (S35–36)'),
 ('★ Thiazide diuretics','Block NCC in the distal tubule → ↑ Na⁺ in the collecting duct · medullary gradient mostly intact → WEAKER (S37–38)'),
 ('★ Why loop + thiazide diuretics waste K⁺','NOT a direct effect · more Na⁺ reaches the collecting duct → more Na⁺ through ENaC → more K⁺ secreted through ROMK (S36, S38)'),
 ('ROMK','Renal outer medullary K⁺ channel · K⁺ secretion in the collecting duct (S36)'),
 ('Long-term loop/thiazide patients','Recheck bloodwork for a slowly falling K⁺'),
 ('★ Potassium-sparing diuretics','Amiloride = blocks ENaC directly · spironolactone = blocks the mineralocorticoid (aldosterone) receptor → less ENaC → no K⁺ loss via ROMK (S39–40)'),
 ('★ ENaC rule for K⁺','↑ ENaC activity = K⁺-WASTING · ↓ ENaC activity = K⁺-SPARING (S40)'),
 ('Coming Monday (✖️ not taught yet)','Glucose/osmotic diuresis, alcohol as a diuretic, fluid therapy (S42–48)'),
]),
]
TRAPS={}  # Clean look (Bethany, Nov 3): no traps/flag boxes on pages — traps live in the chat + misses log
SW='<script>if("serviceWorker"in navigator)navigator.serviceWorker.register("sw.js",{updateViaCache:"none"}).then(r=>r.update()).catch(()=>{})</script>'
rows=lambda items:''.join(
  f'<tr class="{"hy" if t.startswith("★") else ""}"><td>{E(t)}</td><td><span class="ans">{E(a)}</span></td></tr>' for t,a in items)
def pg(fn,title,sub,body,back,backlbl):
    open(fn,'w').write(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(title)}</title><style>{css}</style></head><body><div class="wrap"><a class="back" href="{back}?v={V}">← {backlbl}</a><div class="hero"><h1>{E(title)}</h1><p>{sub}</p></div>{body}<div class="foot">🎀 Bethany · K-State CVM Class of 2030 · 🐾</div></div><script>{js}</script>{SW}</body></html>')
BAR='<div class="bar"><script defer src="shuffle.js"></script><button id="hide">🙈 Hide all</button><button id="all">👀 Show all</button><span class="n" id="n"></span></div>'
links=''
for slug,title,who,items in SECS:
    fn=f'systems-lec4-{slug}-terms.html'
    pg(fn,'🫘 '+title,f'{E(who)} · {len(items)} terms · say it, then tap the pink box',BAR+f'<div class="sec"><table>{rows(items)}</table></div>',E4,'Back to Exam 4')
    links+=f'<a class="tile" href="{fn}?v={V}"><div class="emoji">🧠</div><h2>{E(title)}</h2><p>{E(who)} · {len(items)} terms · tap to reveal</p></a>'
total=sum(len(x[3]) for x in SECS)

# ---- 📈 Diagrams: Claude-drawn SVG (no class slide images in this public repo) ----
PK='#E0459A'; PU='#6A0DAD'; INK='#330B4D'; GR='#2E7D5B'
def badge(n,x,y): return (f'<g class="bd" data-k="{n-1}" style="cursor:pointer"><circle cx="{x}" cy="{y}" r="13" fill="{PK}" stroke="#fff" stroke-width="2"/>'
                          f'<text x="{x}" y="{y+5}" font-size="14" font-weight="800" fill="#fff" text-anchor="middle">{n}</text></g>')
def lab(x,y,s,c=INK,anc='middle',sz=12,w=700): return f'<text x="{x}" y="{y}" font-size="{sz}" font-weight="{w}" fill="{c}" text-anchor="{anc}" stroke="#FFFBFD" stroke-width="3" paint-order="stroke">{s}</text>'
tube=(f'<path d="M100,62 C130,40 150,70 130,95 C112,118 150,130 150,150 L150,440 C150,500 230,500 230,440 L230,150 C230,110 260,95 300,92 '
      f'C330,90 340,75 360,72 C385,70 400,80 400,100 L400,470" fill="none" stroke="{PU}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round" opacity=".85"/>')
zones=(f'<rect x="0" y="0" width="560" height="160" fill="#FBF6FE"/><rect x="0" y="160" width="560" height="170" fill="#F6E7F4"/><rect x="0" y="330" width="560" height="190" fill="#EFD3EA"/>'
       +lab(8,20,'CORTEX',PU,'start',11)+lab(8,180,'OUTER MEDULLA',PU,'start',11)+lab(8,350,'INNER MEDULLA',PU,'start',11))
glom=f'<circle cx="70" cy="62" r="30" fill="#fff" stroke="{PU}" stroke-width="4"/>'
seg=(lab(70,112,'Glomerulus')+lab(150,82,'Proximal tubule','#330B4D','start',11)+lab(140,300,'Thin desc.','#330B4D','end',11)
     +lab(240,300,'Thick asc.','#330B4D','start',11)+lab(300,126,'Distal tubule','#330B4D','middle',11)+lab(392,250,'Collecting duct','#330B4D','end',11)
     +lab(470,30,'Interstitium',GR,'middle',12))
arrow=f'<path d="M408,440 L452,440" stroke="{PK}" stroke-width="4" marker-end="url(#ah)"/>'
defs=f'<defs><marker id="ah" markerWidth="8" markerHeight="8" refX="4" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="{PK}"/></marker></defs>'
B=[(70,62),(168,170),(190,492),(212,170),(320,72),(380,410),(480,90),(480,250),(505,395),(430,470)]
svgd=(f'<svg viewBox="0 0 560 520" xmlns="http://www.w3.org/2000/svg" font-family="-apple-system,Segoe UI,Arial,sans-serif" role="img">{defs}{zones}{tube}{glom}{seg}{arrow}'
      +''.join(badge(i+1,x,y) for i,(x,y) in enumerate(B))+'</svg>')
DG=[
 ('1 · Filtrate in Bowman\'s space','300 mOsm · freely filtered, so it matches plasma (Renal 2, Rule 1)'),
 ('2 · Filtrate leaving the proximal tubule','300 · salt and water leave TOGETHER, so the concentration doesn\'t change'),
 ('3 · Filtrate at the loop tip','~1000–1200 · thin descending limb lets WATER out into the salty medulla (salt stays in)'),
 ('4 · Filtrate at the top of the thick ascending limb','~200 · NKCC pumps salt out and water can\'t follow → hypotonic'),
 ('5 · Filtrate in the distal tubule','~100 · NCC pulls out MORE salt, still no water → very hypotonic'),
 ('6 · Collecting-duct filtrate at the bottom','Low ADH: stays ~100 (dilute urine, diuresis) · high ADH: water leaves until it nears the medulla (~1100–1200, concentrated urine)'),
 ('7 · Cortex interstitium','300 · same as plasma'),
 ('8 · Outer-medulla interstitium','~500–800 · climbing (countercurrent multiplication: NKCC + thin-limb permeability + vasa recta)'),
 ('9 · Inner-medulla tip interstitium','~1100–1200 · about half NaCl (~600) + half UREA (~600, needs ADH)'),
 ('10 · The arrow: what lets water leave the collecting duct?','A PATHWAY: aquaporins (AQP2) inserted by ADH · no pathway = water stays in = diuresis · diuretics shrink the 100-vs-1200 difference = less pull = diuresis'),
]
how=('<div class="sec"><h2>How to read it</h2><ul><li>Purple tube = the nephron; background darkens as the medulla gets saltier.</li>'
     '<li>Badges 1–6 = osmolarity INSIDE the tube (filtrate). Badges 7–9 = OUTSIDE (interstitium).</li>'
     '<li>The exam idea: very dilute filtrate (100) next to a very salty medulla (1200) = a huge pull on water, used only if ADH opens a pathway.</li></ul></div>')
DFN='systems-lec4-diagrams.html'
dbody=(BAR+f'<div class="sec"><h2>⭐ Nephron osmolarity map (Basel: "know this slide very, very well") · LC57+58 S19 / S32</h2>'
       f'<div style="background:#FFFBFD;border-radius:12px;padding:6px">{svgd}</div><p style="font-size:14px;margin:6px 0 0">Tap a pink number (or its row) to reveal.</p></div>'
       f'<div class="sec"><table>{rows(DG)}</table></div>{how}'
       '<script>document.querySelectorAll(".bd").forEach(g=>g.addEventListener("click",()=>{const n=(+g.dataset.k+1)+" ·";const tr=[...document.querySelectorAll("table tr")].find(r=>r.cells[0].textContent.trim().startsWith(n));if(tr)tr.querySelector(".ans").click()}))</script>')
pg(DFN,'📈 Renal diagrams','Exam 4 · Renal · tap-to-reveal · redrawn by Claude from Basel\'s slides',dbody,E4,'Back to Exam 4')
links+=f'<a class="tile" href="{DFN}?v={V}"><div class="emoji">📈</div><h2>Diagrams</h2><p>⭐ Nephron osmolarity map (S19) · tap the numbers</p></a>'

HCSS=re.search(r'<style>.*?</style>',open(E2).read(),re.S).group(0)
def hub(fn,title,h1,sub,back,backlbl,tiles):
    open(fn,'w').write(f'<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#8855b8"><title>{title}</title>{HCSS}</head><body><div class="wrap"><section class="hero"><h1>{h1}</h1><p>{sub}</p></section><div class="nav"><a href="{back}?v={V}">← {backlbl}</a></div><div class="grid">{tiles}</div><div class="footer">KSU Vet School Study Mate · Fall 2026</div></div>{SW}</body></html>')
hub(E4,'🫘 Systems I · Lecture Exam 4','🫘 Lecture Exam 4 · Renal','Syllabus Exam 5 · Fri 11/20 · LC52–63 · Basel 91 pts',HUB,'Back to Lecture',links)

# Systems Lecture hub: keep every older exam tile, add/refresh the Exam 4 tile on top
TILE4=f'<a class="tile" href="{E4}?v={V}"><div class="emoji">🫘</div><h2>Exam 4 · Renal</h2><p>Fri 11/20 · LC52–63 · {total} terms so far · ⭐ current</p></a>'
h=open(HUB).read()
h=re.sub(r'<a class="tile" href="systems-lec-exam4\.html[^"]*">.*?</a>','',h,flags=re.S)
h=h.replace('<div class="grid">','<div class="grid">'+TILE4,1)
h=re.sub(r'(href="systems-lec-exam\d\.html)\?v=\d+"',lambda m:f'{m.group(1)}?v={V}"',h)
open(HUB,'w').write(h)
# cache-bust links into the hub + service worker
for f in ['veterinary-systems.html','fall2026.html','index.html']:
    if os.path.exists(f):
        t=open(f).read(); open(f,'w').write(re.sub(r'(href="(?:veterinary-systems|systems-lecture|fall2026)\.html)\?v=\d+"',lambda m:f'{m.group(1)}?v={V}"',t))
sw=open('sw.js').read(); open('sw.js','w').write(re.sub(r"ksu-study-mate-v(\d+)-\d+",lambda m:f"ksu-study-mate-v{int(m.group(1))+1}-{V}",sw))
print(E4,total,'terms',[len(x[3]) for x in SECS])
