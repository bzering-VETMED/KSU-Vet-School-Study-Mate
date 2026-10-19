# Cell Physiology Exam 3 · tap-to-reveal PATHWAY decks (one arrow per tap).
# Called by tools/cellphys.py (build_pathways). Reuses deck.page + deck.stg and the COPYJS "Copy misses" block.
# Step markers: ★ = must know (slides / professor emphasis) · 💭 = understanding only.
import html, os, re
import deck
E = html.escape
K, U = True, False  # must-know / understanding-only

# (title, cite, start, [(cue, step, must_know)])
P = {
1: ('Glucagon → glucose out of the liver', 'LC18 slides 12–15', 'Low blood sugar (glucagon) or stress/exercise (epinephrine)', [
  ('What is released, and by whom?', 'Pancreas alpha cells release glucagon', K),
  ('Where does glucagon bind?', 'Its G-protein-coupled receptor on the liver cell (sits in the membrane)', U),
  ('What does the receptor switch on?', 'The Gs protein (relay inside the membrane)', K),
  ('What does Gs turn on?', 'Adenylyl cyclase: converts ATP → cyclic AMP', U),
  ('Which second messenger rises?', 'Cyclic AMP ↑ (carries the signal inside the cell)', K),
  ('What does cyclic AMP activate?', 'Protein kinase A (a kinase = ADDS phosphates)', K),
  ('Middle-man kinase?', 'Protein kinase A phosphorylates phosphorylase kinase → ON', U),
  ('Which breakdown enzyme turns ON?', 'Glycogen phosphorylase ON (phosphorylated) · glycogen synthase OFF', K),
  ('What does phosphorylase cut off?', 'One glucose at a time → glucose-1-phosphate', K),
  ('How does it become glucose-6-phosphate?', 'Phosphoglucomutase moves the phosphate (carbon 1 → 6)', U),
  ('What frees the glucose? Where?', 'Glucose-6-phosphatase removes the phosphate → free glucose · LIVER ONLY (muscle lacks it)', K),
  ('How does it leave the liver?', 'Through GLUT2 (glucose transporter 2) → blood sugar ↑', K)]),
2: ('Insulin → glucose stored as glycogen', 'LC18 slides 9–10, 15 · LC16 slide 6', 'High blood sugar', [
  ('What is released, and by whom?', 'Pancreas beta cells release insulin', K),
  ('Where does insulin bind?', 'The insulin receptor on liver, muscle and fat cells', U),
  ('How does glucose get into muscle and fat?', 'GLUT4 (insulin-dependent glucose transporter) moves to the membrane → glucose enters', K),
  ('Which enzyme does insulin turn on?', 'Protein phosphatase 1 → REMOVES phosphates', K),
  ('Breakdown enzyme?', 'Glycogen phosphorylase OFF (dephosphorylated) → breakdown stops', K),
  ('Building enzyme?', 'Glycogen synthase ON (dephosphorylated)', K),
  ('How is glucose activated?', 'Glucose → glucose-6-phosphate → glucose-1-phosphate → UDP-glucose (activated glucose)', U),
  ('What adds it to the chain?', 'Glycogen synthase adds glucose → glycogen stored', K),
  ('What makes the branches?', 'Glycogen branching enzyme adds the branch points', K)]),
3: ('Glucagon → gluconeogenesis switch', 'LC18 slides 25–26', 'Low blood sugar → glucagon (or epinephrine) released', [
  ('Signal inside the liver cell?', 'Gs protein → cyclic AMP ↑ → protein kinase A ON (adds phosphates)', K),
  ('What does protein kinase A phosphorylate?', 'The two-job enzyme: phosphofructokinase-2 / fructose-2,6-bisphosphatase (one enzyme, two halves)', K),
  ('Which half turns off, which turns on?', 'Phosphofructokinase-2 half OFF (stops MAKING the signal) · fructose-2,6-bisphosphatase half ON (DESTROYS the signal)', K),
  ('What happens to the signal?', 'Fructose-2,6-bisphosphate ↓ (the "fed flag" drops)', K),
  ('Effect on glycolysis?', 'Phosphofructokinase-1 loses its activator → glycolysis ↓ (stop burning glucose)', K),
  ('Effect on gluconeogenesis?', 'Fructose-1,6-bisphosphatase loses its inhibitor → gluconeogenesis ↑ (start making glucose)', K),
  ('Result?', 'Liver makes new glucose → blood sugar ↑', K),
  ('Rule + trap?', 'Fructose-2,6-bisphosphate ACTIVATES phosphofructokinase-1 and INHIBITS fructose-1,6-bisphosphatase · phosphofructokinase-1 ≠ phosphofructokinase-2 · bisphosphaTASE = enzyme, bisphosphaTE = signal molecule', K)]),
4: ('Insulin → glycolysis switch', 'LC18 slides 25–26', 'High blood sugar → insulin released', [
  ('Which enzyme does insulin turn on?', 'Protein phosphatase 1 → REMOVES phosphates', K),
  ('What does it dephosphorylate?', 'The two-job enzyme: phosphofructokinase-2 / fructose-2,6-bisphosphatase', K),
  ('Which half turns on?', 'Phosphofructokinase-2 half ON · fructose-2,6-bisphosphatase half OFF', K),
  ('What happens to the signal?', 'Fructose-2,6-bisphosphate ↑ (the "fed flag" goes up)', K),
  ('Effect on glycolysis?', 'Phosphofructokinase-1 activated → glycolysis ↑', K),
  ('Effect on gluconeogenesis?', 'Fructose-1,6-bisphosphatase inhibited → gluconeogenesis ↓', K)]),
5: ('Fat burning (lipolysis → β-oxidation)', 'LC20 slides 7–11', 'Low blood sugar (glucagon) or stress/exercise (epinephrine)', [
  ('Signal inside the cell?', 'Gs protein → cyclic AMP ↑ → protein kinase A ON', K),
  ('Breakdown enzyme?', 'Protein kinase A phosphorylates hormone-sensitive lipase → ON (the main enzyme to know)', K),
  ('Building enzyme?', '…and phosphorylates acetyl-CoA carboxylase → OFF (stop building fat)', K),
  ('What does hormone-sensitive lipase cut?', 'Triglyceride → 3 fatty acids + glycerol (in fat cells)', K),
  ('Where do they go?', 'Fatty acids + glycerol go into the blood', K),
  ('What happens to glycerol?', 'Glycerol → liver → gluconeogenesis (new glucose)', U),
  ('Activated where?', 'In the tissue cell cytosol: fatty acid + coenzyme A → fatty acyl-CoA (costs 2 ATP)', U),
  ('How does it enter the mitochondria?', "Fatty acyl-CoA can't cross → the carnitine shuttle carries it in", K),
  ('What does β-oxidation do?', 'In the mitochondria: chops off 2 carbons per round → acetyl-CoA + FADH₂ + NADH', K),
  ('The 4 steps?', "4 steps per round → 1 FADH₂ + 1 NADH + 1 acetyl-CoA (\"Don't Hurry, Dad's Tired\" = dehydrogenase, hydratase, dehydrogenase, thiolase)", U),
  ('Where do the products go?', 'Acetyl-CoA → TCA cycle · FADH₂ + NADH → electron transport chain → ATP', K)]),
6: ('Fat storage (lipogenesis)', 'LC20 slides 4–6, 11', 'High blood sugar → beta cells release insulin', [
  ('Which enzyme does insulin turn on?', 'Protein phosphatase 2A → REMOVES a phosphate', K),
  ('Building vs breakdown enzyme?', 'Acetyl-CoA carboxylase ON · hormone-sensitive lipase OFF (stop burning fat)', K),
  ('Second ON switch?', 'Citrate (high when fed) binds acetyl-CoA carboxylase → ON (allosteric, no phosphate; feed-forward)', K),
  ("Citrate's other job?", 'Citrate shuttle: acetyl-CoA rides out of the mitochondria inside citrate → cytoplasm (where fat is built)', U),
  ('What does acetyl-CoA carboxylase do?', 'Adds a carbon (CO₂, uses 1 ATP): acetyl-CoA (2C) → malonyl-CoA (3C) = committed + rate-limiting step', K),
  ('What starts the chain?', 'Starter = 1 plain acetyl-CoA (2 carbons)', K),
  ('How does the chain grow?', 'Malonyl-CoA (3C, "the brick") is added → 1 CO₂ leaves → chain +2 carbons (2 → 4 → 6 …)', K),
  ('Which carrier reduces it?', 'NADPH (not NADH) reduces each new 2-carbon unit: oxygen removed → plain CH₂ fat chain', K),
  ('When does it stop? Where?', 'Repeat → stops at palmitate (16 carbons) · liver + adipose', K),
  ('Where does the backbone come from?', 'Dihydroxyacetone phosphate (from glycolysis) → reduced by NADH → glycerol-3-phosphate', K),
  ('How is triglyceride made?', 'Glycerol-3-phosphate + 3 fatty acids (e.g., palmitate, as fatty acyl-CoA) added at positions 1 → 2 → 3 → triglyceride', K),
  ('Stop after 2 fatty acids?', 'Diacylglycerol phosphate → membrane lipids', U),
  ('Where does it go?', 'Adipose: stores the triglyceride · liver: ships it out in VLDL (very low density lipoprotein)', K)]),
7: ('Ketogenesis', 'LC20 slides 13–17 · LC19 slide 12 · LC18 slide 29', 'Fasting / starvation / diabetes → low insulin, high glucagon', [
  ('Fat burning gives?', 'β-oxidation → tons of acetyl-CoA in the liver', K),
  ('What does gluconeogenesis use up?', 'Oxaloacetate (to make glucose)', K),
  ('Why does acetyl-CoA need it?', 'Acetyl-CoA + oxaloacetate → citrate (TCA step 1)', K),
  ('No oxaloacetate →', "Acetyl-CoA can't enter the TCA cycle → piles up", K),
  ('What runs out?', 'Free coenzyme A (acetyl-CoA = acetate stuck to coenzyme A)', K),
  ('The fix?', 'Liver (and kidney) combine extra acetyl-CoAs → ketone bodies → frees coenzyme A', K),
  ('Steps?', '2 acetyl-CoA → acetoacetyl-CoA → HMG-CoA → acetoacetate', U),
  ('The 3 ketone bodies?', 'Acetoacetate · β-hydroxybutyrate (acetoacetate reduced by NADH) · acetone (acetoacetate breaks down spontaneously → CO₂ + acetone)', K),
  ('Who uses ketones?', 'Heart + brain (ketone → acetyl-CoA → TCA cycle → ATP)', K),
  ("Why can't the liver?", 'It lacks 3-oxoacid CoA transferase', K),
  ('Cutoffs?', 'Normal ~0.1 mM → ketosis > 0.5 mM (normal, fasting) → ketoacidosis > 1.5 mM (pathological, pH < 7.35)', K)]),
8: ('Ischemia → reperfusion injury', 'LC17 slides 2, 8–13, 24–26', 'Clot blocks blood flow (cat with hypertrophic cardiomyopathy → saddle thrombus)', [
  ('First consequence?', 'No oxygen → electron transport chain stops', K),
  ('What runs out?', "NADH can't be emptied → NAD⁺ runs out in the mitochondria", K),
  ('Why does step 8 reverse?', 'Step 8 (malate → oxaloacetate) makes NADH and has a big positive ΔG → with NADH piled up it runs BACKWARD', K),
  ('What gets depleted?', 'Oxaloacetate → steps 1–3 stop (no citrate)', K),
  ('Steps 4–5?', 'Run forward → make succinate', K),
  ('Steps 6–8?', 'Run backward (oxaloacetate → malate → fumarate → succinate)', K),
  ('What builds up?', 'Succinate, from BOTH directions', K),
  ('Reperfusion: oxygen returns →', 'Stored succinate rushes through step 6: succinate → fumarate (complex II, succinate dehydrogenase)', K),
  ('What surges?', 'Huge surge of FADH₂ floods the electron transport chain', K),
  ('Result?', 'Electrons leak onto oxygen → superoxide → oxidative damage → cat dies ~12 hours later', K)]),
9: ('Electron transport chain → ATP', 'LC17 slides 19–23', 'NADH and FADH₂ from glycolysis + TCA cycle', [
  ('Where?', "Inner mitochondrial membrane (protons can't leak through it)", K),
  ('NADH enters at?', 'Complex I → pumps protons (H⁺)', K),
  ('Succinate enters at?', "Complex II = succinate dehydrogenase (succinate → fumarate, makes FADH₂) → doesn't pump", K),
  ('Carrier to complex III?', 'Coenzyme Q (from complexes I and II)', K),
  ('Complex III?', 'Pumps protons', K),
  ('Carrier to complex IV?', 'Cytochrome c', K),
  ('Complex IV?', 'Hands electrons to oxygen (final electron acceptor) → water · pumps protons', K),
  ('Where do protons pile up?', 'Intermembrane space → stored energy = proton motive force', K),
  ('How is ATP made?', 'Protons flow back through ATP synthase → TURN its channel → shape change → ADP + phosphate → ATP', K),
  ('Numbers?', '10 H⁺ = 1 turn = 3 ATP → 3.33 H⁺ per ATP (~4 = whole-system cost, slide 23)', K),
  ('Yield?', 'NADH ~10 H⁺ → ~2.5 ATP · FADH₂ ~6 H⁺ (skips complex I) → ~1.5 ATP', K)]),
10: ('Amino acid → urea', 'LC19 slides 7, 13–17', 'An amino acid to break down', [
  ('First step?', 'Transamination: amine moves onto α-ketoglutarate', K),
  ('Products?', 'Glutamate + an α-keto acid (→ glucose or ketones)', K),
  ('Second step?', 'Glutamate is deaminated → NH₄⁺ (ammonium)', K),
  ('Why is NH₄⁺ dangerous?', 'Base (↑pH) · K⁺-sized → K⁺ dysregulation · ↑glutamine', K),
  ('Where is it detoxified?', 'Liver urea cycle', K),
  ('Regulatory enzyme?', 'Carbamoyl phosphate synthetase', K),
  ('Its activator?', 'N-acetylglutamate (made when glutamate is high)', K),
  ('Output?', 'Urea → blood → kidney excretes it', K)]),
11: ('Liver shunt → hepatic encephalopathy', 'LC19 slides 2, 9, 19–22', 'Irish wolfhound with a patent ductus venosus', [
  ('What is bypassed?', 'Portal blood skips the liver (portosystemic shunt)', K),
  ('Which amino acids aren\'t removed?', 'Aromatic amino acids (phenylalanine, tyrosine)', K),
  ('What happens to ammonia?', 'NH₄⁺ isn\'t made into urea → ammonia ↑', K),
  ('Ratio change?', 'BCAA:AAA (branched-chain : aromatic) falls, 3:1 → ~1.5:1', K),
  ('Other lab sign?', 'Serum bile acids ↑', K),
  ('Why brain signs?', 'Neurotransmitter + K⁺ dysregulation → ataxia, seizures', K),
  ('Treatment?', 'High-quality, low-protein diet enriched in branched-chain amino acids', K)]),
12: ('Glucocorticoid receptor', 'LC15 slides 11–12', 'Cortisol enters the cell', [
  ('Where is the receptor at rest?', 'Cytoplasm, bound to heat shock proteins (HSP70/HSP90), inactive', K),
  ('Cortisol binds →', 'Shape (conformational) change', K),
  ('What is released?', 'The heat shock protein complex', K),
  ('Next?', 'Glucocorticoid receptor forms a dimer', K),
  ('Where does it go?', 'Into the nucleus', K),
  ('What does it do?', 'Turns on immunosuppressive gene transcription', K),
  ('Off switch?', 'Ubiquitinated → proteasome degrades it', K)]),
13: ('Low oxygen → lactate', 'LC16 slides 17–25', 'Low oxygen (sprinting muscle, poor blood flow)', [
  ('Why does the electron transport chain stop?', 'Oxygen is the final electron acceptor', K),
  ('What runs out?', "NADH can't be emptied → NAD⁺ runs out", K),
  ('Which glycolysis step stalls?', 'Step 6 (glyceraldehyde-3-phosphate dehydrogenase) needs NAD⁺ → no ATP', K),
  ('The fix?', 'Lactate dehydrogenase: pyruvate + NADH → lactate + NAD⁺ (takes the hydrogen off NADH, puts it on pyruvate)', K),
  ('Result?', 'NAD⁺ regenerated → glycolysis keeps running, but only 2 ATP per glucose', K),
  ('Where does lactate go?', 'Muscle → blood → liver', K),
  ('Cori cycle?', 'Liver: lactate → pyruvate → glucose (gluconeogenesis) → back to muscle', K),
  ('Cori cost?', 'Muscle +2 ATP, liver −6 ATP → NET −4 ATP', K),
  ('Heart?', 'Always has oxygen → takes up lactate → pyruvate → TCA cycle (up to 70% of its energy in intense exercise)', K),
  ('Too much lactate?', 'Metabolic acidosis', K),
  ('Other animals?', 'Yeast → ethanol · rumen bacteria → succinate or propionate (all refill NAD⁺)', U)]),
14: ('Vasopressin (antidiuretic hormone) V1 and V2', 'LC21 "Vasopressin/ADH Signaling"', '↑ Blood osmolality or ↓ blood volume', [
  ('Who senses it?', 'Hypothalamic neurosecretory cells', K),
  ('Where is it released?', 'Posterior pituitary → vasopressin into the blood', K),
  ('V1 receptor location?', 'Vascular smooth muscle', K),
  ('V1 signal?', 'IP3 (inositol trisphosphate) + DAG (diacylglycerol) → contraction → ↑ blood pressure', K),
  ('V2 receptor location?', 'Kidney collecting duct', K),
  ('V2 signal?', '↑ Cyclic AMP → aquaporins inserted → water retained', K)]),
15: ('Histamine → vasodilation', 'LC21 "Paracrine Signaling" · "Histamine & Nitric Oxide"', 'Inflammation releases histamine', [
  ('Which receptor, where?', 'H1 receptor on endothelial cells', K),
  ('What do endothelial cells make?', 'Nitric oxide (NO), a gas', K),
  ('Where does NO go?', 'Diffuses into nearby smooth muscle (paracrine; no surface receptor)', K),
  ('Its target?', 'Guanylyl cyclase (intracellular enzyme)', K),
  ('Second messenger?', 'Cyclic GMP ↑', K),
  ('Result?', 'Smooth muscle relaxes → vasodilation', K)]),
16: ('Bicarbonate buffer', 'LC08 "Example: Bicarbonate/Carbonic Acid"', 'Extra H⁺ added to the blood', [
  ('H⁺ combines with?', 'Bicarbonate (HCO₃⁻) → carbonic acid (H₂CO₃)', K),
  ('Which enzyme?', 'Carbonic anhydrase', K),
  ('Products?', 'Water + CO₂', K),
  ('Body\'s response?', 'Breathe faster → vent CO₂', K),
  ('Effect on the reaction?', 'Pulls it further right → more H⁺ removed', K),
  ('Bicarbonate pKa?', '6.4 (works because it\'s plentiful and adjustable, not because pKa ≈ 7.4)', K)]),
17: ('Ion trapping (aspirin)', 'LC08 "Practice Problem: Ion Trapping"', 'Aspirin = weak acid, pKa 3.5', [
  ('Stomach pH 2 vs pKa?', 'Below pKa → mostly protonated → UNCHARGED', K),
  ('Can it cross membranes?', 'Yes, uncharged (positive logP) → crosses into cells', K),
  ('Extracellular fluid pH 7 vs pKa?', 'Above pKa → mostly ionized (A⁻) → CHARGED', K),
  ('Can it cross back?', 'No → trapped → accumulates in extracellular fluid', K),
  ('Rule?', 'Weak acid ionized ABOVE pKa · weak base ionized BELOW pKa', K),
  ('Ratio (worked out)?', '10^(pH − pKa): stomach ≈ 0.03 · extracellular ≈ 3,160 (calculated, not on slide)', U)]),
}
# Final '🖼️ Show the slide' reveal (reuses the know-this slide assets)
SLIDE = {i: ('assets/cellphys_lc23_regtable.jpg', 'LC23 "Important Regulatory Pathways for Metabolism"') for i in (1, 2, 3, 4, 5, 6)}

DECKS = [('cellphys-path1.html', '🔀 Hormone switches', 'Glucagon vs insulin · glycogen · PFK-2 · fat · ketones', [1, 2, 3, 4, 5, 6, 7]),
         ('cellphys-path2.html', '⚡ Energy & oxygen', 'Lactate · ischemia/reperfusion · electron transport', [13, 8, 9]),
         ('cellphys-path3.html', '🧬 Nitrogen, signaling & pH', 'Urea · liver shunt · receptors · buffers · ion trapping', [10, 11, 12, 14, 15, 16, 17])]

def _copyjs():
    src = open(os.path.join(os.path.dirname(__file__), 'sys_lec_terms_cards.py')).read()
    return re.search(r'COPYJS=r"""(.*?)"""', src, re.S).group(1)

def card(i):
    title, cite, start, steps = P[i]
    S = ''.join(deck.stg('⬇️ ' + E(cue), ('★ ' if mk else '💭 ') + E(step)) for cue, step, mk in steps)
    S += deck.stg('📖 Source', E(cite))
    if i in SLIDE:
        src, lab = SLIDE[i]
        S += deck.stg('🖼️ Show the slide', f'<div class="clue">{E(lab)}</div><img src="{src}" loading="lazy" style="width:100%;border-radius:12px">')
    return (f'<section class="card"><div class="q textq">{E(title)}<span class="tagline">Start: {E(start)}</span></div>{S}'
            f'<div class="rev">💗 TAP TO REVEAL</div></section>')

def build_pathways(HUB, V):
    cj = _copyjs(); tiles = []
    for fn, name, sub, ids in DECKS:
        cs = [card(i) for i in ids]; cs[0] = cs[0].replace('class="card"', 'class="card on"', 1)
        out = deck.page(f'🧭 {name}', f'{len(cs)} pathways · tap one arrow at a time · ★ must know · 💭 understanding only', ''.join(cs), back=HUB)
        out = re.sub(r'← Back to [^<]+', '← Back to Cell Physiology', out, count=1).replace('</body>', cj + '</body>')
        open(fn, 'w').write(out)
        tiles.append(f'<a class="tile" href="{fn}?v={V}"><div class="emoji">{name.split(" ")[0]}</div><h2>{E(name.split(" ", 1)[1])}</h2><p>{E(sub)} · {len(cs)} pathways</p></a>')
    head = '<div style="grid-column:1/-1;font-weight:900;color:#70428f;margin-top:4px">🧭 Pathways · tap arrow by arrow</div>'
    print('pathways', [(f, len(i)) for f, _, _, i in DECKS])
    return head + ''.join(tiles)
