# Cell Physiology · LC08 Acids, Bases & Ion Trapping (Dr. Schultz) — practice exam written from the LC08 slides.
# Schultz style: select-all, unit traps, calculations. Reuses the old-exam card renderer. Called by tools/cellphys.py.
import re
import deck
from cellphys_pathways import _copyjs
from cellphys_oldexams import card, XCSS

FN = 'cellphys-lc08-practice.html'
SEC = 'LC08 practice (written from slides)'
ASP = 'Aspirin is a weak acid, pKa ≈ 3.5. Stomach lumen pH ≈ 2; extracellular fluid pH ≈ 7. Octanol:water ≈ 17 for the protonated form, ≈ 0 for the deprotonated form.'
# (stem, [options], [correct letters], why, cite, multi, ctx)
Q = [
 ('What is the pH of a 1 mM solution of HCl, a monoprotic strong acid? (select one)', ['1', '2', '3', '7', '11'], 'c',
  'Strong acid dissociates fully: [H⁺] = 10⁻³ M, so pH = −log(10⁻³) = 3.', 'LC08 slide "pH"', False, ''),
 ('According to the Brönsted-Lowry definition, an acid is any molecular species that: (select one)', ['Accepts a proton (H⁺)', 'Donates a proton (H⁺)', 'Accepts an electron pair', 'Raises the pH of water', 'Carries a net negative charge'], 'b',
  'Acid = proton donor; base = proton acceptor. The acid form is always the protonated form.', 'LC08 slide "Acids and Bases: Brönsted-Lowry"', False, ''),
 ('Which statements about conjugate acid/base pairs are correct? (select ALL that are correct)', ['The acid form is always the protonated form', 'Either the acid form or the base form carries a net charge', 'Both forms of a pair are always uncharged', 'NH₄⁺ is the acid form of the ammonia pair', 'Acetate (CH₃COO⁻) is the acid form of the acetic acid pair'], 'abd',
  'Protons carry + charge, so one member of each pair is charged. NH₄⁺ (protonated) is the acid; acetate is the conjugate BASE.', 'LC08 slide "Acids and Bases: Brönsted-Lowry"', True, ''),
 ('When the pH of a solution equals the pKa of a weak acid dissolved in it: (select one)', ['[HA] >> [A⁻]', '[HA] = [A⁻]', '[HA] << [A⁻]', 'The acid is fully dissociated', 'The solution is at pH 7'], 'b',
  'pH = pKa → half protonated, half deprotonated. This is also the inflection point of the titration curve (best buffering).', 'LC08 slides "Weak Acid Dissociation Constant" and "Buffering"', False, ''),
 ('A weak acid with pKa 5.0 is placed in a solution at pH 3.0. What is the ratio [A⁻]/[HA]? (select one)', ['100', '2', '1', '0.01', '0.001'], 'd',
  '10^(pH − pKa) = 10^(3 − 5) = 10⁻² = 0.01. Two pH units below pKa → 99% protonated.', 'LC08 slide "pKa & pH: Henderson-Hasselbalch"', False, ''),
 ('For a WEAK BASE drug, which form predominates when the pH is well below its pKa? (select one)', ['Deprotonated, uncharged, more lipid soluble', 'Protonated, charged, less lipid soluble', 'Protonated, uncharged, more lipid soluble', 'Deprotonated, charged, less lipid soluble', 'Equal amounts of both forms'], 'b',
  'Low pH = lots of H⁺ → protonated. For a base, the protonated form (e.g., NH₄⁺) is the charged one → poor membrane crossing. Weak bases are "ionized at pH lower than pKa."', 'LC08 slide "Body Compartments & Drugs"', False, ''),
 ('Which form of a drug crosses a lipid bilayer most readily? (select one)', ['The charged form, because it is attracted to membrane phospholipids', 'The uncharged form, because it has a measurable positive logP', 'The charged form, because it has a negative logP', 'Both forms cross equally; only size matters', 'Whichever form is protonated, regardless of charge'], 'b',
  'Small uncharged solutes with positive logP cross; charged solutes (negative logP) don\'t. Trap E: protonated is uncharged only for ACIDS.', 'LC08 slide "pH & Permeability"', False, ''),
 ('In the aspirin practice problem, what is the ratio of base/acid ([A⁻]/[HA]) in the stomach lumen at equilibrium? (select one)', ['≈ 0.0003', '≈ 0.03', '≈ 1', '≈ 32', '≈ 3,160'], 'b',
  '10^(2 − 3.5) = 10^−1.5 ≈ 0.0316. Mostly protonated (uncharged) in the stomach → it can cross into cells.', 'LC08 practice problem "Ion Trapping"', False, ASP),
 ('In the same problem, what is the ratio of base/acid ([A⁻]/[HA]) in the extracellular fluid? (select one)', ['≈ 0.03', '≈ 3.5', '≈ 32', '≈ 316', '≈ 3,160'], 'e',
  '10^(7 − 3.5) = 10^3.5 ≈ 3,162. Almost all deprotonated (charged) → it can\'t cross back → trapped.', 'LC08 practice problem "Ion Trapping"', False, ASP),
 ('Bonus: if the protonated form equilibrates at 1 µM on both sides of the stomach lining, what is the TOTAL aspirin concentration in the extracellular fluid? (select one)', ['≈ 1 µM', '≈ 1.03 µM', '≈ 31.6 µM', '≈ 3.16 mM', '≈ 3.16 M'], 'd',
  'Total = HA + A⁻ = 1 µM + 3,162 µM ≈ 3,163 µM ≈ 3.16 mM. Watch the µM → mM step (÷1,000). Stomach total ≈ 1.03 µM.', 'LC08 practice problem "Ion Trapping" (bonus)', False, ASP),
 ('Based on the aspirin problem, which statements are correct? (select ALL that are correct)', ['A significant amount of aspirin is absorbed across the stomach lining', 'Aspirin accumulates on the more alkaline side of the membrane', 'Aspirin accumulates in the stomach lumen because it is protonated there', 'The deprotonated form diffuses freely back into the stomach', 'Ion trapping makes total concentration differ across a membrane even when the uncharged form is equal on both sides'], 'abe',
  'Weak acids get trapped on the alkaline side (charged there). The charged form can\'t diffuse back. Uncharged form equal on both sides, totals very different.', 'LC08 slides "Ion Trapping" and practice problem', True, ASP),
 ('Which of the following are listed as physiological buffers? (select ALL that are correct)', ['Bicarbonate / carbonic acid', 'Phosphate (HPO₄²⁻ / H₂PO₄⁻)', 'Deoxyhemoglobin (histidines)', 'Sodium chloride', 'Proteins, peptides and amino acids'], 'abce',
  'NaCl is a salt of a strong acid and strong base — no buffering. Hemoglobin buffers through its histidines.', 'LC08 slide "Physiological Buffers"', True, ''),
 ('What is the pKa of the bicarbonate / carbonic acid buffer system? (select one)', ['6.4', '7.2', '7.4', '7.7', '8.4'], 'a',
  'Bicarbonate 6.4; phosphate 7.2 (trap); deoxyhemoglobin 7–7.7; plasma pH 7.4 (trap).', 'LC08 slide "Physiological Buffers"', False, ''),
 ('Bicarbonate is an effective physiological buffer even though its pKa is not close to 7.4. Why? (select two correct responses)', ['It is plentiful', 'Its components can be manipulated physiologically (CO₂ vented by the lungs)', 'It has a very wide buffering plateau', 'Its pKa is close to the pH of plasma', 'It has multiple H⁺ binding sites per molecule'], 'ab',
  'Physiological buffers succeed because they are plentiful and their acid/base components can be adjusted (lungs blow off CO₂, kidneys handle HCO₃⁻).', 'LC08 slide "Ideal & Physiological Buffers"', True, ''),
 ('H⁺ is added to blood: H⁺ + HCO₃⁻ ⇌ H₂CO₃ ⇌ H₂O + CO₂. Which statements are correct? (select ALL that are correct)', ['The reaction shifts to the right', 'Carbonic anhydrase catalyzes H₂CO₃ ⇌ H₂O + CO₂', 'Increased respiratory rate vents CO₂ and pulls the reaction further right', 'Bicarbonate concentration rises', 'The body responds by decreasing respiratory rate'], 'abc',
  'Added H⁺ is consumed by HCO₃⁻ (so bicarbonate FALLS), making carbonic acid → water + CO₂. Breathing faster removes CO₂ (mass action).', 'LC08 slide "Example: Bicarbonate/Carbonic Acid"', True, ''),
 ('Which properties describe an IDEAL buffer? (select two correct responses)', ['pKa close to the target pH', 'High buffer capacity', 'pKa at least 2 units from the target pH', 'Low concentration so it does not alter osmolality', 'A single H⁺ donor/acceptor site per molecule'], 'ab',
  'Ideal: pKa near target pH + high capacity (e.g., multiple H⁺ sites per molecule). Real physiological buffers fall short and rely on abundance + manipulation.', 'LC08 slide "Ideal & Physiological Buffers"', True, ''),
 ('What is the typical pH of plasma and of cytosol? (select one)', ['Plasma 7.2; cytosol 7.4', 'Plasma 7.4; cytosol 7.2', 'Plasma 7.4; cytosol 7.4', 'Plasma 7.0; cytosol 6.4', 'Plasma 6.4; cytosol 7.2'], 'b',
  'Plasma/ECF ≈ 7.4, cytosol ≈ 7.2. Trap A flips them. (The compartment table lists intracellular fluid as 6.8 — the slide text says 7.2.)', 'LC08 slide "Physiology & pH"', False, ''),
 ('For water, Kw = [H₃O⁺][OH⁻] equals: (select one)', ['10⁻⁷', '10⁻⁷ M²', '10⁻¹⁴', '10⁻¹⁴ M', '14'], 'c',
  '10⁻⁷ M × 10⁻⁷ M = 10⁻¹⁴ (as written on the slide). Trap: 10⁻⁷ is [H⁺] in pure water, not Kw.', 'LC08 slide "Water as Weak Acid or Weak Base"', False, ''),
 ('H₂SO₄ is a strong acid that yields H⁺ and HSO₄⁻. Which statement about HSO₄⁻ is correct? (select one)', ['It is also a strong acid', 'It is a weak acid with pKa ≈ 1.9', 'It is a weak base with pKa ≈ 12.6', 'It cannot donate a proton', 'It is fully protonated at pH 7'], 'b',
  'Slide: HSO₄⁻ is a weak acid, Ka = 12.6 mM, pKa = 1.9. Trap C reuses the 12.6 number.', 'LC08 slide "pH" (note)', False, ''),
 ('A weak base drug (pKa 9.8) is in a patient whose urine is acidified (pH ≈ 5.8). What happens to the drug in the urine? (select ALL that are correct)', ['It is mostly protonated', 'It is mostly charged', 'It is trapped in the urine, increasing excretion', 'It is reabsorbed more readily across the tubule', 'It is mostly uncharged because the urine is acidic'], 'abc',
  'pH << pKa → protonated; for a base, protonated = charged → can\'t cross back → trapped and excreted. Outside the slides: this is why urine pH is manipulated in some toxicities.', 'LC08 slides "Ion Trapping" + "Body Compartments & Drugs"', True, ''),
 ('What is the pH of a 10 nM solution of HCl (a strong acid) in pure water? (select one)', ['8.0', '7.0 exactly', 'Slightly below 7', '10.0', '6.0'], 'c',
  'Spoken trap: 10 nM = 10⁻⁸ M, but water already has 10⁻⁷ M H⁺, so the added acid barely lowers it — just under 7. "Don\'t be misled by very low concentrations."', 'LC08 lecture 10/21 (spoken)', False, ''),
 ('Which statements about protonation and charge are correct? (select ALL that are correct)', ['A protonated weak acid is neutral', 'A protonated weak base is charged', 'The acid form of a pair is always the protonated form', 'The protonated form always crosses membranes', 'A deprotonated weak base is neutral'], 'abce',
  '"The acid form is always protonated, but that doesn\'t mean it\'s always charged." Weak acid: HA neutral. Weak base: BH⁺ charged, B neutral. Only the UNCHARGED form crosses.', 'LC08 lecture 10/21 + slide "Acids and Bases"', True, ''),
 ('A weak acid drug is placed on both sides of a lipid membrane, and both sides are at the same pH. At equilibrium: (select one)', ['The drug accumulates on the side with more water', 'Total drug concentration is equal on both sides', 'All of the drug becomes uncharged', 'The drug is trapped on the side it was added to', 'Only the charged form is equal on both sides'], 'b',
  'Same pH → same charged:uncharged split on both sides → equal totals. Trapping needs a pH DIFFERENCE.', 'LC08 slide "pH & Permeability" + lecture', False, ''),
 ('Acetazolamide blocks carbonic anhydrase. What happens to urine pH? (select one)', ['Decreases', 'Increases', 'No change', 'Falls to the pKa of bicarbonate', 'Becomes equal to plasma pH'], 'b',
  'Spoken: blocking carbonic anhydrase raises urine pH — and urine pH can be manipulated to trap a drug in the urine.', 'LC08 lecture 10/21 (spoken)', False, ''),
 ('Why is histidine a particularly good physiological buffer residue? (select one)', ['It is the most abundant amino acid in plasma', 'Its side-chain pKa (~6–6.5) is close to physiological pH', 'It is always positively charged', 'It is a strong base', 'It binds bicarbonate directly'], 'b',
  'Good buffers have a pKa near the target pH. Deoxyhemoglobin has ~38 exposed histidines → big buffering capacity.', 'LC08 lecture 10/21 + slide "Physiological Buffers"', False, ''),
]

FL23 = 'Body fluids and pH: Plasma 7.4 · Bile 6.5 · Pancreatic secretions 7.8 · Milk 6.6 · Stomach 1.5 · Cytosolic fluid 7.2 · Urine 4.5 · Semen 7.9 · Small intestine 7.0'
FL24 = 'Body fluids and pH: Plasma 7.4 · Bile 6.5 · Pancreatic secretions 7.8 · Milk 6.8 · Stomach 1.5 · Cytosolic fluid 7.2 · Urine 4.5 · Semen 7.9 · Small intestine 7.0'
HEM = 'g-Coniceine is one of the primary toxic alkaloids in poisonous hemlock. Assume its pKa is 9.4 and that the PROTONATED form is uncharged (neutral). Serum concentration in a rabbit: 24 nM. Serum pH = 7.4; urine pH = 12.4.'
# (sec, n, stem, opts, ans, why, multi, ctx, img)
REAL = [
 ('Schultz 2023 Exam 2', 3, 'In the carbonic acid reaction: H⁺ + HCO₃⁻ ⇌ H₂CO₃ ⇌ H₂O + CO₂, which component is an acid? (select one correct response)', ['H⁺', 'HCO₃⁻', 'H₂CO₃', 'H₂O', 'CO₂'], 'c',
  'An acid DONATES a proton. Carbonic acid (H₂CO₃) gives up H⁺ to become bicarbonate. H⁺ is the proton itself; bicarbonate is the conjugate base.', False, '', []),
 ('Schultz 2023 Exam 2', 5, 'You administer a drug that is a weak acid with a pKa of 6.5. The drug distributes to fluids throughout the body and reaches equilibrium distribution. Select two fluids (or body compartments) from the list that would have the highest concentrations of this drug. (select two correct responses)', ['Pancreatic secretions', 'Semen', 'Small intestine', 'Stomach', 'Urine'], 'ab',
  'Weak acids are trapped (ionized) on the ALKALINE side. The two most alkaline fluids are semen (7.9) and pancreatic secretions (7.8). Stomach and urine are the trap: that is where weak BASES collect.', True, FL23, []),
 ('Schultz 2023 Exam 2', 6, 'In which fluid or body compartment would there be equal concentrations of the charged and uncharged (ionized and neutral) forms of the drug? (select one correct response)', ['Bile', 'Cytosolic fluid', 'Plasma', 'Small intestine', 'Stomach'], 'a',
  'Charged = uncharged when pH = pKa. pKa 6.5 → bile (pH 6.5).', False, FL23, []),
 ('Schultz 2023 Exam 2', 52, 'Calculate the pH of a solution containing the equivalent of 0.2 millimoles per liter of H₂SO₄. Assume complete dissociation: H₂SO₄ + 2 H₂O ⇒ SO₄²⁻ + 2 H₃O⁺', [], '',
  'Each H₂SO₄ gives TWO H⁺ → [H⁺] = 0.4 mM = 4 × 10⁻⁴ M. pH = −log(4 × 10⁻⁴) ≈ 3.4. Trap: forgetting the ×2 gives 3.7.', False, '', []),
 ('Schultz 2023 Exam 2', 55, 'In the extracellular fluid of the body (e.g., serum), is a greater proportion of the g-coniceine in the uncharged acid form or in the ionized base form?', ['Acid', 'Base'], 'a',
  'Serum pH 7.4 is BELOW pKa 9.4 → mostly protonated = the uncharged acid form.', False, HEM, []),
 ('Schultz 2023 Exam 2', 56, 'What is the ratio of base to acid in the serum?', [], '',
  '10^(pH − pKa) = 10^(7.4 − 9.4) = 10⁻² = 0.01 (1 base : 100 acid).', False, HEM, []),
 ('Schultz 2023 Exam 2', 57, 'In the rabbit\'s urine, is a greater proportion of the g-coniceine in the uncharged acid form or in the ionized base form?', ['Acid', 'Base'], 'b',
  'Urine pH 12.4 is ABOVE pKa 9.4 → mostly deprotonated = the ionized base form (trapped in urine).', False, HEM, []),
 ('Schultz 2023 Exam 2', 58, 'What is the ratio of base to acid in urine?', [], '',
  '10^(12.4 − 9.4) = 10³ = 1,000 (1,000 base : 1 acid).', False, HEM, []),
 ('Schultz 2024 Exam 2', 9, 'What is the pH of a 1 mM (10⁻³ M) solution of HBr, a strong acid? (select one correct response)', ['1.0', '2.0', '3.0', '4.0', '5.0'], 'c',
  'Strong acid fully dissociates → [H⁺] = 10⁻³ M → pH 3.', False, '', []),
 ('Schultz 2024 Exam 2', 12, 'Aspirin (3.5) and phenytoin (8.4) are weak acids with pKa\'s of 3.5 and 8.4, respectively. Lignocaine (7.9) and methyldopa (10.6) are weak bases with pKa\'s of 7.9 and 10.6, respectively. Which response correctly indicates the compounds that will be more than 50% ionized in typical plasma? (select one correct response)', ['Aspirin, lignocaine and methyldopa, but not phenytoin', 'Aspirin and phenytoin, but not lignocaine or methyldopa', 'Aspirin, but not phenytoin, lignocaine or methyldopa', 'Lignocaine and methyldopa, but not aspirin or phenytoin', 'Phenytoin, lignocaine and methyldopa, but not aspirin'], 'a',
  'Plasma pH 7.4. Weak ACID ionized when pH > pKa → aspirin yes, phenytoin no. Weak BASE ionized when pH < pKa → lignocaine (7.9) yes, methyldopa (10.6) yes.', False, '', []),
 ('Schultz 2024 Exam 2', 13, 'You administer a drug orally that is a weak base with a pKa of 6.8. The base form of the drug has a logP of 2.5 (P = 300). The drug distributes to fluids throughout the body and reaches equilibrium distribution. Which fluids from the list would have the highest concentrations of this drug at equilibrium? (select one correct response)', ['Milk', 'Plasma', 'Semen and pancreatic secretions', 'Small intestine', 'Stomach and urine'], 'e',
  'Weak BASES are trapped (protonated = charged) on the ACIDIC side → stomach (1.5) and urine (4.5). Semen/pancreatic is the weak-acid answer.', False, FL24, []),
 ('Schultz 2024 Exam 2', 14, 'In which body compartment would there be equal concentrations of the charged and uncharged (ionized and neutral) forms of the drug? (select one correct response)', ['Cytosolic fluid', 'Milk', 'Plasma', 'Small intestine', 'Stomach'], 'b',
  'pH = pKa (6.8) → milk (6.8 on this year\'s list). Note milk was 6.6 on the 2023 list — read the table each time.', False, FL24, []),
 ('Schultz 2025 Exam 2', 4, 'A system shown in class has two aqueous volumes separated by a thin organic layer. A weak acid, WA (pKa = 5.3), is added to the upper chamber and the protonated form has a logP = 1.2. What pH of the upper chamber will maximize the rate at which WA appears in the lower chamber? (select one correct response)', ['10^(1.2)', '3.0', '5.3', '7.4', '9.0'], 'b',
  'Only the uncharged form crosses. For a weak ACID, that is the protonated form, maximized at LOW pH (below pKa) → 3.0. 5.3 gives only 50% uncharged.', False, '', ['e2_25_image1']),
 ('Schultz 2025 Exam 2', 5, 'Same system. A weak base, WB (pKa = 8.3), is added to the upper chamber and the neutral (deprotonated) form has a logP = 0.6. What pH of the upper chamber will maximize the rate at which WB appears in the lower chamber (first answer), and to what pH should the upper chamber be adjusted to end (at equilibrium) with the same concentration of WB in both aqueous compartments (second answer)? (select one correct response)', ['10^(0.6) · 8.3', '6.0 · 7.2', '6.0 · 8.3', '9.0 · 7.2', '9.0 · 8.3'], 'd',
  'Rate: a weak BASE is uncharged when deprotonated → HIGH pH (9.0). Equal totals at equilibrium: no ion trapping only when BOTH chambers have the SAME pH — not pH = pKa (that trap only makes charged = uncharged within one chamber). 7.2 assumes the lower chamber is at 7.2.', False, '', ['e2_25_image1']),
 ('Schultz 2025 Exam 2', 15, 'Aspirin (3.5) and pentobarbital (8.1) are weak acids with pKa\'s of 3.5 and 8.1, respectively. Amiodarone (6.6) and atropine (9.7) are weak bases with pKa\'s of 6.6 and 9.7, respectively. Which response correctly indicates the compounds that will be more than 50% ionized in typical plasma? (select one correct response)', ['Amiodarone and aspirin, but not atropine or pentobarbital', 'Amiodarone and atropine, but not aspirin or pentobarbital', 'Amiodarone, atropine and pentobarbital, but not aspirin', 'Aspirin and atropine, but not amiodarone or pentobarbital', 'Aspirin, but not amiodarone, atropine or pentobarbital'], 'd',
  'Plasma 7.4. Acids ionized if pKa < 7.4 → aspirin yes, pentobarbital (8.1) no. Bases ionized if pKa > 7.4 → atropine (9.7) yes, amiodarone (6.6) no.', False, '', []),
]
FLAGS = {('Schultz 2025 Exam 2', 5): 'Lecture 10/21 confirms the logic: same pH on both sides → same concentration at equilibrium. The stem still never states the lower chamber pH (7.2 assumed).'}

def build_lc08exam(HUB, V):
    qs = []
    for sec, n, stem, opts, ans, why, multi, ctx, img in REAL:
        a = {'ans': list(ans), 'why': why, 'cite': 'LC08 slides "Ion Trapping", "pH & Permeability", "Body Compartments & Drugs"', 'conf': 'sure', 'scope': 'in'}
        if (sec, n) in FLAGS: a['flag'] = FLAGS[(sec, n)]
        qs.append({'sec': sec + ' (real exam)', 'n': n, 'stem': stem, 'opts': [[l, t] for l, t in zip('abcde', opts)], 'multi': multi, 'ctx': ctx, 'img': img, 'a': a})
    for i, (stem, opts, ans, why, cite, multi, ctx) in enumerate(Q, 1):
        L = 'abcde'[:len(opts)]
        qs.append({'sec': SEC, 'n': i, 'stem': stem, 'opts': [[l, t] for l, t in zip(L, opts)], 'multi': multi, 'ctx': ctx, 'img': [],
                   'a': {'ans': list(ans), 'why': why, 'cite': cite, 'conf': 'sure', 'scope': 'in'}})
    cs = [card(q) for q in qs]; cs[0] = cs[0].replace('class="card"', 'class="card on"', 1)
    out = deck.page('LC08 practice exam · Acids, bases & ion trapping', f'{len(REAL)} real questions from Schultz\'s 2023–2025 Exam 2s first, then {len(Q)} written from the LC08 slides · show your math', ''.join(cs), back=HUB)
    out = re.sub(r'← Back to [^<]+', '← Back to Cell Physiology', out, count=1).replace('</style>', XCSS + '</style>', 1).replace('</body>', _copyjs() + '</body>')
    open(FN, 'w').write(out)
    print('lc08 practice', len(cs))
    return f'<a class="tile" href="{FN}?v={V}" style="border:3px solid #d94f7f"><div class="emoji">🧪</div><h2>LC08 practice exam</h2><p>Acids, bases &amp; ion trapping · {len(REAL)} real old-exam Qs + {len(Q)} practice · calculations + select-all</p></a>'
