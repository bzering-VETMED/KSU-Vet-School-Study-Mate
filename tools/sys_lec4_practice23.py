# Build: Exam 4 (renal, Basel) · Practice Exams 2 + 3 (new Basel-hard Qs, one page each, tap-to-check)
# Run from repo root BEFORE tools/sys_lec4_terms.py (which adds hub tiles + cache-busts)
import html,time,re,json,random
from collections import Counter
E=html.escape; V=str(int(time.time()))
_py=open('tools/sys_lecture.py').read()
CSS=re.search(r"^CSS='''(.*?)'''",_py,re.S|re.M).group(1)
JS=re.search(r"^JS='''(.*?)'''",_py,re.S|re.M).group(1)
SW='<script>if("serviceWorker"in navigator)navigator.serviceWorker.register("sw.js",{updateViaCache:"none"}).then(r=>r.update()).catch(()=>{})</script>'
SA=' (select ALL that apply)'

P2=[
# Renal 1
("Renal 1","A 30 kg dog. About how much PLASMA volume does it have?",["1.5 L","4.5 L","6 L","12 L"],[0],"Water 60% = 18 L · extracellular ⅓ = 6 L · plasma ≈ ¼ of extracellular = 1.5 L"),
("Renal 1","Which pairing of normal concentrations (mM) is correct?",["Na⁺ 145 outside · K⁺ 140 inside","Na⁺ 140 inside · K⁺ 145 outside","Na⁺ 145 outside · K⁺ 5 inside","Na⁺ 10 outside · K⁺ 140 inside"],[0],"Table 12.1: Na⁺ 145 outside / 10 inside · K⁺ 5 outside / 140 inside"),
("Renal 1","A cow receives hypertonic saline. Once water finishes moving, which is NOT true?",["Extracellular osmolarity rises","Intracellular volume falls","Intracellular osmolarity rises","Intracellular volume rises"],[3],"Salt stays outside → water leaves cells → cells shrink, and both compartments end at a higher osmolarity"),
("Renal 1","Inflammation lets protein leak into a tissue's interstitial fluid. What happens at that capillary?",["Interstitial oncotic pressure rises, so fluid moves out","Capillary oncotic pressure rises, so fluid moves in","Capillary hydrostatic pressure falls, so fluid moves in","Interstitial hydrostatic pressure falls, so fluid moves in"],[0],"Protein in the tissue pulls water toward the tissue → edema"),
# Renal 2
("Renal 2","Which is NOT part of the glomerular filtration barrier?",["Fenestrated endothelium","Fused basement membrane","Podocyte foot processes","Intraglomerular mesangial cells"],[3],"Mesangial cells are support only"),
("Renal 2","Two drugs are both 30 kDa. One is positively charged, the other negatively charged. Which statement is correct?",["The positive drug is filtered more","The negative drug is filtered more","Both are filtered equally","Neither is filtered at 30 kDa"],[0],"The basement membrane is negative → repels anions, lets cations through more easily (size > charge > shape)"),
("Renal 2","Which change would most DECREASE GFR?",["Constricting the efferent arteriole","Dilating the efferent arteriole","Dilating the afferent arteriole","Lowering plasma albumin"],[1],"Efferent dilation drops glomerular pressure · the other three raise GFR"),
("Renal 2","GFR is 100 mL/min and renal plasma flow is 500 mL/min. What is the filtration fraction?",["5%","20%","50%","500%"],[1],"Filtration fraction = GFR ÷ renal plasma flow = 100/500 = 20%"),
("Renal 2","Basel says the kidney prefers HIGH renal plasma flow. Why?",["High flow raises the filtration fraction","More total filtrate is made per minute","High flow lowers glomerular pressure","Albumin is filtered more at high flow"],[1],"Filtration fraction falls, but far more plasma passes per minute → more total filtrate"),
# Renal 3
("Renal 3","LOW NaCl at the macula densa causes which?"+SA,["Renin release","Prostaglandin E2 release","Afferent arteriole dilation","Efferent arteriole dilation","ANP release"],[0,1,2],"Low NaCl = GFR too low → open the entrance + start RAAS (angiotensin II then constricts the efferent)"),
("Renal 3","Which is NOT a trigger for renin release?",["Low NaCl at the macula densa","Sympathetic nerve activity","Prostaglandin E2","Stretch of the right atrium"],[3],"Atrial stretch triggers ANP, which suppresses renin"),
("Renal 3","A dog with heart failure has high renin. What is the main reason?",["Atrial stretch releases ANP","The weak heart activates sympathetic tone","Hypertension stretches the afferent","High GFR delivers more NaCl"],[1],"Basel: a failing heart puts the body in fight-or-flight → sympathetic nerves → renin"),
("Renal 3","About 80% of the kidney's oxygen consumption is used for:",["Glomerular filtration","Sodium reabsorption by Na⁺/K⁺ pumps","Producing renin and erythropoietin","Organic anion secretion"],[1],"Mostly in the proximal tubule and thick ascending limb"),
("Renal 3","An emaciated 15-year-old cat needs screening for early CKD. Which marker is most useful?",["BUN","Creatinine","Urine glucose","SDMA"],[3],"SDMA rises after ~25% loss and isn't affected by muscle mass"),
("Renal 3","Which are hallmarks of glomerular disease?"+SA,["Proteinuria","Decreased GFR","Hypoalbuminemia","Glucosuria with normal blood glucose","Hypertension"],[0,1,2,4],"Glucosuria with normal blood glucose = proximal tubule (Fanconi)"),
# Renal 4
("Renal 4","How does glucose leave the proximal tubule cell to reach the blood?",["SGLT on the basolateral side","GLUT on the basolateral side","GLUT on the apical side","Na⁺/K⁺ pump on the basolateral side"],[1],"SGLT brings it in (apical) · GLUT lets it out (basolateral, passive)"),
("Renal 4","Which proximal tubule transporters are SECONDARY active?"+SA,["SGLT","NaPi-IIa","Na⁺/H⁺ exchanger","Na⁺/K⁺ pump","Na⁺-amino acid cotransporters"],[0,1,2,4],"The Na⁺/K⁺ pump is PRIMARY active (uses ATP directly)"),
("Renal 4","Why does the proximal tubule filtrate stay at ~300 even though so much is reabsorbed?",["Water follows solute through leaky tight junctions","The proximal tubule is impermeable to water","ADH adds aquaporins to the proximal tubule","Urea is secreted to replace lost solute"],[0],"Isosmotic reabsorption: solute out, water follows → smaller volume, same concentration"),
("Renal 4","A dog drank antifreeze. Which ethylene glycol metabolite is secreted into the tubule and forms crystals?",["Oxalate","Lactate","Glutamine","Urea"],[0],"Ethylene glycol → oxalate → secreted (OAT pathway) → crystals + tubule damage"),
("Renal 4","Which statement about megalin/cubam is INCORRECT?",["It sits on the apical side of the proximal tubule","It swallows small filtered proteins","It concentrates gentamicin in the cell","It pulls tetracycline in from the blood"],[3],"Tetracycline enters through OAT from the BLOOD side"),
# Renal 5
("Renal 5","The thin descending limb is permeable to ___ but not ___.",["Sodium; water","Water; sodium","Potassium; sodium","Urea; water"],[1],"Water out only → filtrate concentrates as it dives"),
("Renal 5","Which pairing is correct for THIAZIDES?",["Potassium-sparing; calcium-wasting","Potassium-wasting; calcium-sparing","Potassium-sparing; calcium-sparing","Potassium-wasting; calcium-wasting"],[1],"Loop = wastes both · thiazide = wastes K⁺, spares Ca²⁺"),
("Renal 5","Aldosterone acts on principal cells. What happens to potassium?",["It is reabsorbed through ENaC","It is secreted through ROMK","It is reabsorbed through the H⁺/K⁺ pump","It is secreted through NKCC"],[1],"ENaC brings Na⁺ in → lumen negative → K⁺ out through ROMK"),
("Renal 5","Why are the thick ascending limb and distal tubule waterproof?",["So they can make a dilute filtrate","So urea can be recycled there","So ADH can act on them directly","So the filtrate stays isosmotic"],[0],"Basel: 'if water can move, it will' → block water, make the filtrate hypotonic, then let ADH decide"),
("Renal 5","Which statement about NKCC is INCORRECT?",["It moves Na⁺, K⁺ and 2 Cl⁻ together","It is electroneutral","It sits in the thick ascending limb","It is blocked by thiazides"],[3],"Thiazides block NCC · loop diuretics block NKCC"),
# Renal 6
("Renal 6","Which segment SECRETES urea back into the filtrate?",["Proximal tubule","Thin loop of Henle","Thick ascending limb","Distal tubule"],[1],"Thin loop secretes ~60% of the filtered load (recycling), via UT-A2"),
("Renal 6","Which best describes the vasa recta?",["It actively pumps salt into the medulla","It is a passive countercurrent exchanger","It builds the gradient with NKCC","It reabsorbs urea through UT-A1"],[1],"Exchange = keeps the gradient; multiplication (loop + NKCC) builds it"),
("Renal 6","During antidiuresis, about how much of the ~1200 mOsm medulla is UREA?",["~100 mOsm","~300 mOsm","~600 mOsm","~1200 mOsm"],[2],"~600 NaCl + ~600 urea"),
("Renal 6","If NKCC is completely blocked, what happens to the medullary gradient?",["It increases because urea rises","It stays the same because of the vasa recta","It washes out","It reverses direction"],[2],"Everything depends on NKCC"),
# Renal 7
("Renal 7","Filtrate entering the collecting duct is ~100 mOsm. With NO ADH, the final urine is about:",["100 mOsm","300 mOsm","600 mOsm","1200 mOsm"],[0],"No apical aquaporins → water stays in → dilute urine"),
("Renal 7","Where is ADH made, and where is it released?",["Made in the posterior pituitary; released from the hypothalamus","Made in the hypothalamus; released from the posterior pituitary","Made in the adrenal cortex; released from the kidney","Made in the anterior pituitary; released from the hypothalamus"],[1],""),
("Renal 7","ADH acts on which receptor in the collecting duct?",["V1","V2","Mineralocorticoid receptor","AT1"],[1],"V1 = blood vessels (constriction) · V2 = kidney (water)"),
("Renal 7","A dog's dilute urine concentrates after desmopressin but not after water deprivation. Where is the problem?",["Collecting duct","Hypothalamus/posterior pituitary","Thick ascending limb","Adrenal gland"],[1],"Central DI: the kidney responds, the brain doesn't make ADH"),
("Renal 7","Why is furosemide called a 'double whammy' diuretic?",["It blocks both NKCC and NCC","It wastes both potassium and calcium","It raises filtrate salt AND washes out the medulla","It blocks both ADH and aldosterone"],[2],"Narrows the filtrate–medulla difference from both sides"),
("Renal 7","Which is a downside of giving large volumes of 0.9% NaCl?",["Hyperkalemia","Hyperchloremic metabolic acidosis","Water moving into cells","Hypercalcemia"],[1],"Extra Cl⁻ displaces bicarbonate"),
("Renal 7","Which is NOT one of Basel's goals of fluid therapy?",["Restore circulating volume","Maintain renal oxygenation","Correct electrolyte and acid–base problems","Concentrate the urine to save water"],[3],"The 4th goal is to flush and dilute toxins"),
# Renal 8
("Renal 8","Which are PTH effects in the kidney?"+SA,["↑ ECaC and calbindin in the distal tubule","↑ CYP27B1 in the proximal tubule","Blocks claudin-14 in the thick ascending limb","Removes NaPi-IIa in the proximal tubule","Blocks claudin-16 in the thick ascending limb"],[0,1,2,3],"Blocking claudin-16 is CALCITONIN"),
("Renal 8","What happens if claudin-14 activity INCREASES in the thick ascending limb?",["More calcium is reabsorbed","Less calcium is reabsorbed","More sodium is reabsorbed","Less potassium is secreted"],[1],"Claudin-14 blocks claudin-16 (the calcium door)"),
("Renal 8","A dog is HYPERcalcemic and hypertensive. Which diuretic should you AVOID?",["Furosemide","Hydrochlorothiazide","Amiloride","Spironolactone"],[1],"Thiazides spare calcium (more negative distal cell pulls Ca²⁺ in)"),
("Renal 8","Why can too LITTLE phosphate excretion cause acidosis?",["Phosphate blocks the Na⁺/H⁺ exchanger","Less phosphate is left to buffer secreted H⁺","Phosphate raises FGF23, which retains acid","Phosphate binds bicarbonate in the blood"],[1],"Phosphate is the main titratable buffer in urine"),
# Renal 9
("Renal 9","Which is the FASTEST way the body handles a sudden potassium load?",["Aldosterone adds ROMK","High flow opens BK","Insulin moves K⁺ into muscle","Alpha cells secrete K⁺"],[2],"Insulin works in minutes · the kidney takes hours"),
("Renal 9","Which statement about BK channels is INCORRECT?",["They are opened by tubular flow","Flow bends the primary cilium","TRPV4 opening helps activate them","Aldosterone is their main regulator"],[3],"Aldosterone mainly regulates ROMK · BK = flow-activated safety valve"),
("Renal 9","Which acidosis has a NORMAL anion gap?",["Ethylene glycol toxicity","Diabetic ketoacidosis","Severe diarrhea","Late-stage kidney failure"],[2],"Diarrhea loses bicarbonate · nothing new is added"),
("Renal 9","Why can't the kidney excrete a day's acid as free H⁺?",["Free H⁺ is reabsorbed by NKCC","Urine pH can't go below ~4.5","H⁺ is too large to filter","Free H⁺ blocks aquaporins"],[1],"Buffers (phosphate, ammonia) must grab the H⁺"),
("Renal 9","Which are features of TYPE 2 (proximal) renal tubular acidosis?"+SA,["Normal anion gap","Glucosuria with normal blood glucose","Bicarbonate in the urine","Seen with Fanconi syndrome","High blood potassium"],[0,1,2,3],"High K⁺ = type 4"),
# Renal 10
("Renal 10","Phenylpropanolamine treats urinary incontinence by:",["Blocking M3 on the detrusor","Stimulating α₁ on the internal sphincter","Stimulating M3 on the detrusor","Blocking β₃ on the detrusor"],[1],"Tightens the internal sphincter"),
("Renal 10","A dog with a lumbosacral fracture has a large, flaccid bladder that overflows. Best drug?",["Oxybutynin","Phenylpropanolamine","Bethanechol","Desmopressin"],[2],"Lower motor neuron = Limp → stimulate M3 (Bethanechol Bears down)"),
("Renal 10","During storage, why does the detrusor relax?",["Parasympathetic M3 activation","Sympathetic β₃ activation","Sympathetic α₁ activation","Somatic pudendal activation"],[1],"β = Balloon relaxes · α₁ = sphincter shut"),
# Cases
("Cases","Why does the gentamicin-treated Lab become hyperkalemic?"+SA,["Acidosis shifts K⁺ out of cells","Low tubular flow limits K⁺ secretion","High aldosterone retains K⁺","Gentamicin blocks the Na⁺/K⁺ pump directly"],[0,1],"Basel: acidosis + low flow"),
("Cases","A Boston terrier was sick, improved, then got sick again a day later, with a high anion gap and azotemia. Why the second illness?",["The kidney damage appears a day after the toxin","The dog drank more antifreeze","Ethanol treatment caused vomiting","The liver failed on day 2"],[0],"Day 1 = toxin + acidosis · day 2 = kidney damage shows up"),
("Cases","An acidotic Arabian horse has K⁺ at the bottom of normal and urine pH 8. What explains the potassium?",["Alpha cells can't run the H⁺/K⁺ pump, so K⁺ isn't kept","Aldosterone is low, so ROMK is reduced","Insulin is high, pushing K⁺ into muscle","Acidosis always lowers blood potassium"],[0],"Type 1 RTA is the exception: acidosis with LOW K⁺"),
("Cases","A dog on tetracycline has glucose, amino acids, phosphate and bicarbonate in its urine, normal GFR, and granular casts. Most likely?",["Diabetes mellitus","Glomerular disease","Acquired Fanconi syndrome","Chronic kidney disease"],[2],"Proximal tubule death → everything leaks"),
("Cases","A blocked cat has bilateral pyelectasis on ultrasound. What causes it?",["Back pressure from the urethra up through the ureters","Polycystic kidney disease","Glomerular inflammation","Ethylene glycol crystals"],[0],"Postrenal obstruction · the same back pressure raises Bowman's space pressure and drops GFR"),
("Cases","A dog has BUN 58, creatinine 1.3, USG 1.050 after 3 days of not drinking. Best interpretation?",["Chronic kidney disease","Acute tubular necrosis","Prerenal azotemia","Diabetes insipidus"],[2],"Concentrated urine = the kidney works; BUN rises with dehydration"),
]

P3=[
# Renal 1
("Renal 1","A 450 kg horse. About how much INTRACELLULAR fluid does it have?",["45 L","90 L","180 L","270 L"],[2],"Water 60% = 270 L · intracellular ⅔ = 180 L"),
("Renal 1","A dog is given hypotonic fluid. Once water finishes moving, which is true?",["Only plasma volume rises","Cells swell slightly and both compartments dilute","Cells shrink as water leaves them","Extracellular osmolarity rises"],[1],"Extra free water spreads into cells too"),
("Renal 1","Which does a system need for true HOMEOSTASIS?"+SA,["A sensor","A set point","An adjustable output","Constant input","A fixed leak"],[0,1,2],"The hole-in-the-bucket has a fixed leak → steady state only"),
("Renal 1","Osmotic pressure of a solution depends mainly on:",["The number of dissolved particles","The size of dissolved particles","The protein content","The charge of the particles"],[0],"NaCl counts double (Na⁺ + Cl⁻)"),
# Renal 2
("Renal 2","A urethral stone blocks urine flow. Which Starling force changes first at the glomerulus?",["Capillary hydrostatic pressure falls","Bowman's space hydrostatic pressure rises","Capillary oncotic pressure falls","Bowman's space oncotic pressure rises"],[1],"Urine backs up into the cup → pushes back → GFR falls"),
("Renal 2","Which would essentially NOT be filtered?",["Myoglobin (17 kDa)","Lysozyme (14 kDa)","Albumin (66.5 kDa)","β2-microglobulin (12 kDa)"],[2],"Just under 70 kDa but negative → repelled"),
("Renal 2","Where does the myogenic response of autoregulation mainly occur?",["Efferent arteriole","Afferent arteriole","Peritubular capillaries","Vasa recta"],[1],"Stretch → constriction of the entrance"),
("Renal 2","A dog's blood pressure rises from 110 to 150 mmHg. What happens to GFR?",["It rises sharply","It falls sharply","It stays about the same","It stops completely"],[2],"Within 80–170 → autoregulation holds it steady"),
("Renal 2","Normally, about what fraction of renal plasma is filtered?",["~5%","~20%","~65%","~99%"],[1],"Filtration fraction ≈ 20%"),
# Renal 3
("Renal 3","Which is the correct order of RAAS?",["Renin → angiotensin II → angiotensin I → aldosterone","Angiotensinogen → renin → ACE → aldosterone","Renin cuts angiotensinogen → angiotensin I → ACE → angiotensin II","ACE → renin → angiotensin I → angiotensin II"],[2],"Angiotensin II then constricts the efferent and releases aldosterone (and ADH)"),
("Renal 3","Angiotensin II mainly constricts which vessel, and what happens to filtration fraction?",["Afferent; filtration fraction falls","Efferent; filtration fraction rises","Afferent; filtration fraction rises","Efferent; filtration fraction falls"],[1],"Pressure ↑ (GFR ↑), flow ↓ → filtration fraction ↑"),
("Renal 3","Renal clearance is best defined as:",["The amount of a substance filtered per minute","The volume of plasma fully cleared of a substance per minute","The concentration of a substance in urine","The fraction of plasma that is filtered"],[1],"mL/min · = GFR only if freely filtered, not reabsorbed, not secreted"),
("Renal 3","Which is NOT a typical cause of CHRONIC kidney disease?",["Repeated acute kidney injury","Polycystic kidney disease","Grape ingestion","Glomerulonephritis"],[2],"Grapes cause ACUTE kidney injury"),
("Renal 3","In glomerular disease, why does the 'doom loop' develop?",["Leaky glomeruli activate RAAS, and hypertension damages more glomeruli","Proteinuria raises GFR, which damages tubules","Low albumin blocks ADH, causing dehydration","Glucosuria causes osmotic diuresis and dehydration"],[0],"Break it with an ACE inhibitor"),
# Renal 4
("Renal 4","On which side of the proximal tubule cell is the Na⁺/K⁺ pump?",["Apical (lumen) side","Basolateral (blood) side","Both sides equally","Only in the tight junctions"],[1],"Keeps Na⁺ low inside so it flows in from the lumen"),
("Renal 4","Which ions are reabsorbed passively in the proximal tubule by lumen-positive charge?"+SA,["Calcium","Potassium","Sodium","Glucose","Bicarbonate"],[0,1,2],"Glucose and bicarbonate are sodium-coupled (secondary active)"),
("Renal 4","Where is carbonic anhydrase found in the proximal tubule?",["Only inside the cell","Only on the lumen side","On the lumen side AND inside the cell","Only on the basolateral side"],[2],"External converts bicarbonate → CO₂ · internal rebuilds it"),
("Renal 4","Besides gentamicin, which antibiotic is concentrated in proximal cells by megalin?",["Penicillin","Tetracycline","Colistin","Amoxicillin"],[2],"Megalin/cubam: aminoglycosides + colistin"),
("Renal 4","On a slide, a tubule has tall, very pink cells with a fuzzy lumen. Why are the cells so pink?",["Packed with mitochondria","Packed with aquaporins","Packed with glycogen","Packed with mucus"],[0],"Proximal tubule = huge energy use (Na⁺/K⁺ pumps)"),
# Renal 5
("Renal 5","About what share of filtered sodium does the distal tubule reabsorb?",["~65%","~25%","~5%","~0%"],[2],"65 → 90 → 95 → 98–100%"),
("Renal 5","Which cell makes NEW bicarbonate for the blood?",["Principal cell","Alpha-intercalated cell","Beta-intercalated cell","Proximal tubule cell"],[1],"Proximal tubule only RECLAIMS filtered bicarbonate"),
("Renal 5","A healthy horse's urine is expected to be:",["Acidic, from many alpha cells","Alkaline, from many beta cells","Acidic, from many beta cells","Alkaline, from many alpha cells"],[1],"Herbivores eat less acid"),
("Renal 5","Which filtrate is the most DILUTE in a dog with no ADH?",["End of the proximal tubule","Tip of the loop","End of the thick ascending limb","End of the distal tubule"],[3],"~100 mOsm"),
("Renal 5","ANP acts on the collecting duct to:",["Insert aquaporin-2","Block ENaC","Add urea transporters","Stimulate ROMK"],[1],"Opposite of aldosterone"),
# Renal 6
("Renal 6","NKCC by itself can create about what difference across the thick ascending limb wall?",["~20 mOsm","~200 mOsm","~600 mOsm","~1200 mOsm"],[1],"Countercurrent flow multiplies it"),
("Renal 6","Filtrate flows SLOWLY through the loop. Which is true?",["Less NaCl reaches the macula densa","More NaCl reaches the macula densa","The filtrate leaves less dilute","GFR rises from feedback"],[0],"More time for NKCC → less Na⁺ left → reads as 'GFR too low'"),
("Renal 6","Where is UT-A2 found?",["Inner medullary collecting duct","Thin descending limb","Proximal tubule","Distal tubule"],[1],"UT-A1/A3 = inner medullary collecting duct (ADH)"),
("Renal 6","What does the kidney actually adjust to change the strength of the medullary gradient?",["The number of vasa recta","Urea, through ADH","NaCl, through aldosterone","Glucose, through insulin"],[1],"The NaCl part depends on flow and NKCC"),
# Renal 7
("Renal 7","ADH release is mainly controlled by:",["Blood volume","Plasma osmolarity","Plasma potassium","Plasma calcium"],[1],"Volume → RAAS/aldosterone"),
("Renal 7","Why does a thiazide REDUCE urine output in nephrogenic DI?",["It restores the response to ADH","Mild volume loss lowers GFR, so less fluid reaches the collecting duct","It blocks ENaC, trapping water","It increases urea transporters"],[1],"The thiazide paradox"),
("Renal 7","Mannitol causes diuresis because it:",["Blocks NKCC","Is filtered but never reabsorbed","Blocks ADH release","Inhibits carbonic anhydrase"],[1],"An osmolyte left in the filtrate holds water in"),
("Renal 7","Above about what blood glucose do SGLTs become saturated (Basel)?",["~100 mg/dL","~200 mg/dL","~350 mg/dL","~800 mg/dL"],[2],"Transport maximum → glucosuria → osmotic diuresis"),
("Renal 7","Which hormones does angiotensin II stimulate?"+SA,["Aldosterone","ADH","Renin","ANP","Calcitonin"],[0,1],"Salt + water → volume ↑"),
("Renal 7","Which statement about desmopressin is INCORRECT?",["It is a lab-made ADH","It lasts longer than natural ADH","It treats central diabetes insipidus","It treats nephrogenic diabetes insipidus"],[3],"Nephrogenic DI ignores ADH"),
# Renal 8
("Renal 8","About how much filtered calcium is reabsorbed PASSIVELY, no matter what?",["~8%","~25%","~65%","~90%"],[3],"65% proximal + 25% thick ascending · the distal 8% decides the rest"),
("Renal 8","Which odd effect does calcitonin have?",["It blocks claudin-14","It slightly increases CYP27B1","It adds ECaC","It adds NaPi-IIa"],[1],"Otherwise it mostly opposes PTH"),
("Renal 8","High blood phosphate triggers which response?",["Osteocytes release FGF23 → NaPi-IIa removed","Parathyroid releases calcitonin → NaPi-IIa added","Kidney releases renin → phosphate excreted","Liver releases FGF23 → NaPi-IIa added"],[0],"Phosphate dumped"),
("Renal 8","In which segment is calcium reabsorption ACTIVE?",["Proximal tubule","Thin descending limb","Thick ascending limb","Distal convoluted tubule"],[3],"ECaC + calbindin + NCX/PMCA"),
# Renal 9
("Renal 9","Which explain why ACIDOSIS raises blood potassium?"+SA,["H⁺/K⁺ pump brings K⁺ back as H⁺ is secreted","H⁺ blocks the Na⁺/K⁺ pump in muscle","H⁺ blocks ROMK","H⁺ increases BK activity","H⁺ increases insulin release"],[0,1,2],""),
("Renal 9","Where is ammonia made, and what helps it reach the collecting duct lumen?",["Collecting duct; ROMK","Proximal tubule; RhCG","Thick ascending limb; ENaC","Distal tubule; NCC"],[1],"From glutamine · RhCG is increased by aldosterone"),
("Renal 9","Na⁺ 140, Cl⁻ 115, HCO₃⁻ 15. Anion gap and meaning?",["10; normal gap, bicarbonate lost","10; high gap, acid added","30; high gap, acid added","30; normal gap, bicarbonate lost"],[0],"140 − 130 = 10 → RTA, diarrhea, saline"),
("Renal 9","An acidotic dog has a normal anion gap. Which pairing points to TYPE 1 rather than type 4 RTA?",["High K⁺; urine pH 5.0","Low K⁺; urine pH 7.5","High K⁺; urine pH 7.5","Low K⁺; urine pH 5.0"],[1],"Type 1 can't acidify + low K⁺"),
("Renal 9","Why does LATE chronic kidney disease cause a HIGH anion gap?",["Bicarbonate is lost in the urine","Phosphate, sulfate and organic acids build up","Chloride is retained by the kidney","Ketones are produced by the kidney"],[1],"The R in GOLD MARK"),
# Renal 10
("Renal 10","On a cystometrogram, what happens in phase 3?",["Pressure barely changes as volume rises","Pressure rises sharply and the urge to void begins","The external sphincter contracts","Bladder volume falls to zero"],[1],"The detrusor can't relax any more"),
("Renal 10","Which center switches the bladder from storage to voiding?",["Hypothalamic osmoreceptors","Pontine micturition center","Posterior pituitary","Spinal pudendal nucleus"],[1],"Barrington's nucleus"),
("Renal 10","A dog with a cervical spinal lesion has reflexive, uncontrolled voiding. Best drug?",["Bethanechol","Oxybutynin","Phenylpropanolamine","Furosemide"],[1],"Upper motor neuron → calm the detrusor"),
# Cases
("Cases","Which belong in Basel's CKD treatment plan?"+SA,["ACE inhibitor or ARB","Low-phosphate diet","Low-sodium diet","High-quality protein","Potassium supplement"],[0,1,2,3],"K⁺ already trends high in CKD"),
("Cases","In CKD, high phosphate leads to bone wasting. What is the first step?",["Phosphate binds ionized calcium","Phosphate raises calcitonin","Phosphate blocks vitamin D receptors","Phosphate increases FGF23 to toxic levels"],[0],"Low ionized Ca²⁺ → PTH ↑ → bone"),
("Cases","A dog's urine fails to concentrate with water deprivation but rises to 1.022 after desmopressin. Best treatment?",["Thiazide and free water","Desmopressin","Water restriction","ACE inhibitor"],[1],"Central DI"),
("Cases","A blocked cat has K⁺ 7.5. Which is the FIRST priority?",["Pass a urinary catheter","Give glucose with insulin and bicarbonate","Start an ACE inhibitor","Give potassium-sparing fluids"],[1],"Stabilize K⁺ before unblocking"),
("Cases","A dog has azotemia, USG 1.009 on three samples, high phosphate, and 6 months of PU/PD. Most likely?",["Prerenal azotemia","Acute kidney injury","Chronic kidney disease","Diabetes insipidus"],[2],"Slow + isosthenuric + high phosphate"),
("Cases","A seizing dog with water intoxication needs treatment. Why NOT rely on diuretics?",["They worsen hyponatremia","They act too slowly","They raise blood pressure","They cause hyperkalemia"],[1],"Hypertonic saline works now"),
]

def balance(Q):
    t=0
    for k,(s,stem,opts,ans,why) in enumerate(Q):
        if len(ans)==1 and len(opts)==4:
            tgt=[1,2,3,0][t%4]; t+=1
            c=ans[0]; opts=opts[:]; opts[c],opts[tgt]=opts[tgt],opts[c]
            Q[k]=(s,stem,opts,[tgt],why)
        elif len(ans)>1:
            idx=list(range(len(opts))); random.Random(k*11+5).shuffle(idx)
            Q[k]=(s,stem,[opts[j] for j in idx],sorted(idx.index(a) for a in ans),why)
    return Q

def build(Q,fn,title):
    Q=balance(list(Q)); rows=[];sec=None
    for i,(s,stem,opts,ans,why) in enumerate(Q,1):
        if s!=sec: rows.append(f'<div class="note" style="margin-top:14px"><b>{E(s)}</b></div>');sec=s
        m=len(ans)>1
        ob=''.join(f'<button class="opt">{chr(65+j)}. {E(o)}</button>' for j,o in enumerate(opts))
        rows.append(f'<div class="q" data-a="{json.dumps(ans)}" data-m="{int(m)}"><h3><span>Q{i}</span>{E(stem)}</h3>{ob}{"<button class=chk>Check ✓</button>" if m else ""}<div class="why">✅ <b>{", ".join(chr(65+a) for a in ans)}</b>{" · "+E(why) if why else ""}</div></div>')
    NOTE='New questions in Basel\'s style (not from his old exams or Practice Exam 1). Tap an answer to check it; select-all questions need ✓ Check. Covers every renal lecture + the cases.'
    open(fn,'w').write(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(title)}</title><style>{CSS}</style></head><body><div class="wrap"><a class="back" href="systems-lec-exam4.html?v={V}">← Back to Exam 4</a><div class="hero"><h1>🎯 {E(title)}</h1><p>Basel-style · {len(Q)} Q · all renal lectures + cases</p></div><div class="note">{NOTE}</div><div class="bar"><button id="shuf">🎲 Shuffle</button><button id="miss">🔁 Misses only</button><button id="all">↺ Show all</button><span class="score" id="sc"></span></div><div id="qs">{"".join(rows)}</div></div><script>{JS}</script>{SW}</body></html>')
    print(fn,len(Q),Counter(chr(65+q[3][0]) for q in Q if len(q[3])==1),Counter(q[0] for q in Q))

build(P2,'systems-lec4-practice2.html','Renal Practice Exam 2')
build(P3,'systems-lec4-practice3.html','Renal Practice Exam 3')
