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
]

def build_lc08exam(HUB, V):
    qs = []
    for i, (stem, opts, ans, why, cite, multi, ctx) in enumerate(Q, 1):
        L = 'abcde'[:len(opts)]
        qs.append({'sec': SEC, 'n': i, 'stem': stem, 'opts': [[l, t] for l, t in zip(L, opts)], 'multi': multi, 'ctx': ctx, 'img': [],
                   'a': {'ans': list(ans), 'why': why, 'cite': cite, 'conf': 'sure', 'scope': 'in'}})
    cs = [card(q) for q in qs]; cs[0] = cs[0].replace('class="card"', 'class="card on"', 1)
    out = deck.page('LC08 practice exam · Acids, bases & ion trapping', f'{len(cs)} Schultz-style questions written from the LC08 slides · read every option · show your math', ''.join(cs), back=HUB)
    out = re.sub(r'← Back to [^<]+', '← Back to Cell Physiology', out, count=1).replace('</style>', XCSS + '</style>', 1).replace('</body>', _copyjs() + '</body>')
    open(FN, 'w').write(out)
    print('lc08 practice', len(cs))
    return f'<a class="tile" href="{FN}?v={V}" style="border:3px solid #d94f7f"><div class="emoji">🧪</div><h2>LC08 practice exam</h2><p>Acids, bases &amp; ion trapping · {len(cs)} Schultz-style questions · calculations + select-all</p></a>'
