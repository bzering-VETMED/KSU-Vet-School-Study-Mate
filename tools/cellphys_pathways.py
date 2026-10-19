# Cell Physiology Exam 3 · tap-to-reveal PATHWAY decks (one arrow per tap).
# Called by tools/cellphys.py (build_pathways). Reuses deck.page + deck.stg and the COPYJS "Copy misses" block.
# Step markers: ★ = must know (slides / professor emphasis) · 💭 = understanding only.
import html, os, re
import deck
E = html.escape
K, U = True, False  # must-know / understanding-only

# (title, cite, start, [(cue, step, must_know)])
P = {
1: ('Glucagon → glucose out of the liver', 'LC18 slides 12–15', 'Low blood sugar', [
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
3: ('Glucagon → gluconeogenesis switch', 'LC18 slides 25–26', 'Low blood sugar → glucagon', [
  ('Signal inside the liver cell?', 'Gs protein → cyclic AMP ↑ → protein kinase A (PKA) ON', K),
  ('What does PKA phosphorylate?', 'The two-job enzyme phosphofructokinase-2 / fructose bisphosphatase-2 (PFK-2/FBPase-2)', K),
  ('Which half turns on?', 'Kinase half OFF · phosphatase half ON', K),
  ('What happens to the signal molecule?', 'Fructose-2,6-bisphosphate (F2,6BP) ↓', K),
  ('Effect on glycolysis?', 'Phosphofructokinase-1 (PFK-1) loses its activator → glycolysis ↓', K),
  ('Effect on gluconeogenesis?', 'Fructose bisphosphatase-1 (FBPase-1) loses its inhibitor → gluconeogenesis ↑', K),
  ('Result?', 'Liver makes new glucose', K),
  ('Trap?', 'F2,6BP ACTIVATES PFK-1 and INHIBITS FBPase-1 · PFK-1 ≠ PFK-2', K)]),
4: ('Insulin → glycolysis switch', 'LC18 slides 25–26', 'High blood sugar → insulin', [
  ('Which enzyme does insulin turn on?', 'Protein phosphatase 1 (PP1) → removes phosphates', K),
  ('What does it dephosphorylate?', 'Phosphofructokinase-2 / fructose bisphosphatase-2 (PFK-2/FBPase-2)', K),
  ('Which half turns on?', 'Kinase half ON · phosphatase half OFF', K),
  ('What happens to the signal molecule?', 'Fructose-2,6-bisphosphate (F2,6BP) ↑ (the "fed flag")', K),
  ('Effect on glycolysis?', 'Activates phosphofructokinase-1 (PFK-1) → glycolysis ON', K),
  ('Effect on gluconeogenesis?', 'Inhibits fructose bisphosphatase-1 (FBPase-1) → gluconeogenesis OFF', K)]),
5: ('Fat burning (lipolysis → β-oxidation)', 'LC20 slides 7–11', 'Epinephrine or glucagon (stress / fasting)', [
  ('Signal inside the fat cell?', 'Protein kinase A (PKA) → phosphorylates', K),
  ('Breakdown enzyme?', 'Hormone-sensitive lipase (HSL) ON', K),
  ('Building enzyme?', 'Acetyl-CoA carboxylase (ACC) OFF', K),
  ('What does HSL cut?', 'Triglyceride → fatty acids + glycerol', K),
  ('Activated where?', 'Fatty acids → fatty acyl-CoA in the cytosol (costs ATP)', U),
  ('How does it enter the mitochondria?', 'Carnitine shuttle (fatty acyl-CoA can\'t cross alone)', K),
  ('β-oxidation steps?', 'Acyl-CoA dehydrogenase (FADH₂) → enoyl-CoA hydratase → 3-hydroxyacyl-CoA dehydrogenase (NADH) → thiolase', K),
  ('Product of each round?', 'Acetyl-CoA (chain shorter by 2 carbons) → TCA cycle', K)]),
6: ('Fat storage (lipogenesis)', 'LC20 slides 4–6, 11', 'Fed state → insulin', [
  ('Which enzyme does insulin turn on?', 'Protein phosphatase (2A on the slide) → dephosphorylates', K),
  ('Building enzyme?', 'Acetyl-CoA carboxylase (ACC) ON (+ high citrate feed-forward)', K),
  ('Breakdown enzyme?', 'Hormone-sensitive lipase (HSL) OFF', K),
  ('Committed, rate-limiting step?', 'ACC: acetyl-CoA → malonyl-CoA', K),
  ('Which electron carrier builds the chain?', 'NADPH (not NADH), 2 carbons at a time · liver + adipose', K),
  ('Where does the backbone come from?', 'Glycerol-3-phosphate (from DHAP, dihydroxyacetone phosphate) + 3 fatty acids → triglyceride', K),
  ('Where does it go?', 'Adipose: stored · liver: shipped out as VLDL (very low density lipoprotein)', K)]),
7: ('Ketogenesis', 'LC20 slides 13–17 · LC19 slide 12', 'Fasting or diabetes (low glucose inside cells)', [
  ('What does gluconeogenesis use up?', 'Oxaloacetate', K),
  ('Consequence for acetyl-CoA?', 'Can\'t combine with oxaloacetate to make citrate → can\'t enter the TCA cycle', K),
  ('What piles up?', 'Acetyl-CoA (from fat and ketogenic amino acids)', K),
  ('What runs out?', 'Free coenzyme A (CoA)', K),
  ('Fix?', 'Liver (and kidney) make ketone bodies: acetoacetate, β-hydroxybutyrate, acetone → frees CoA', K),
  ('Who uses ketones?', 'Heart and brain · liver CAN\'T (lacks 3-oxoacid CoA transferase)', K),
  ('Cutoffs?', 'Normal ~0.1 mM · ketosis > 0.5 mM · ketoacidosis > 1.5 mM (pH < 7.35)', K)]),
8: ('Ischemia → reperfusion injury', 'LC17 slides 9–13, 26', 'Blood flow stops (e.g., cat saddle thrombus)', [
  ('First consequence?', 'No oxygen → NADH can\'t be oxidized → NAD⁺ runs out', K),
  ('Which TCA step reverses?', 'Step 8 (malate → oxaloacetate) runs backward to refill NAD⁺', K),
  ('What gets depleted?', 'Oxaloacetate → steps 1–3 stop', K),
  ('Direction of the other steps?', 'Steps 4–5 forward + steps 6–8 backward', K),
  ('What builds up?', 'Succinate (from both directions)', K),
  ('Reperfusion: oxygen returns →', 'Succinate → fumarate runs very fast (complex II)', K),
  ('What surges?', 'FADH₂ surge floods the electron transport system', K),
  ('Result?', 'Superoxide → oxidative damage (cat dies hours after the clot buster)', K)]),
9: ('Electron transport → ATP', 'LC17 slides 19–23', 'NADH and FADH₂ from glycolysis + TCA cycle', [
  ('Where?', 'Inner mitochondrial membrane (impervious to H⁺)', K),
  ('NADH enters at?', 'Complex I → pumps protons', K),
  ('Succinate / FADH₂ enters at?', 'Complex II (succinate dehydrogenase) → NO pump', K),
  ('Carrier to complex III?', 'Coenzyme Q', K),
  ('Carrier to complex IV?', 'Cytochrome c (complex III pumps protons)', K),
  ('Final electron acceptor?', 'Complex IV → O₂ → water (pumps protons)', K),
  ('Where do protons pile up?', 'Intermembrane space → proton motive force', K),
  ('How is ATP made?', 'Protons flow through ATP synthase → channel TURNS → shape change → ADP + phosphate → ATP', K),
  ('Numbers?', '10 H⁺ per turn = 3 ATP (3.33 H⁺/ATP) · NADH ≈ 2.5 ATP · FADH₂ ≈ 1.5 ATP', K)]),
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
13: ('Low oxygen → lactate', 'LC16 slides 18–21', 'Muscle working faster than oxygen delivery', [
  ('What can\'t be oxidized?', 'NADH → NAD⁺ runs out', K),
  ('Which glycolysis step stalls?', 'Step 6 (glyceraldehyde-3-phosphate dehydrogenase) needs NAD⁺', K),
  ('Fix?', 'Lactate dehydrogenase: pyruvate → lactate, regenerating NAD⁺', K),
  ('Energy yield?', 'Glycolysis keeps going, but only 2 ATP per glucose', K),
  ('Where does lactate go?', 'Blood → liver (or heart burns it)', K),
  ('Liver recycling?', 'Cori cycle: lactate → glucose → back to muscle', K),
  ('Cost?', 'Net −4 ATP (+2 muscle, −6 liver)', K)]),
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
