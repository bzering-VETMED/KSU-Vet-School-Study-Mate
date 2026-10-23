# Build: Exam 3 · Poole calculation practice (tap-to-reveal worked answers + 🔀 shuffle)
# Run from repo root AFTER tools/resp_terms.py (reuses that page's CSS/JS). Linked from systems-lec-exam3.html.
import re,time,html
E=html.escape; V=str(int(time.time()))
FN='systems-lec3-calcs.html'; E3='systems-lec-exam3.html'
src=open('systems-lec3-pp3-terms.html').read()
css=re.search(r'<style>(.*?)</style>',src,re.S).group(1)
js=re.findall(r'<script>(.*?)</script>',src,re.S)[-1]

EQ=[ # (name, equation, lecture)
 ('Dalton\'s law','Gas pressure = barometric pressure × fraction of gas','LC41'),
 ('Inspired (tracheal) PO₂','(Barometric pressure − 47) × 0.21','LC41'),
 ('Alveolar gas equation','Alveolar PO₂ = inspired PO₂ − (PaCO₂ ÷ R)','LC41/43'),
 ('Alveolar–arterial PO₂ difference','"Ideal" alveolar PO₂ (from equation above) − measured PaO₂','LC43'),
 ('Bohr equation','Dead space ÷ tidal volume = (PaCO₂ − expired PCO₂) ÷ PaCO₂','LC40'),
 ('Ventilation','Total = dead space ventilation + alveolar ventilation · each = volume × breathing frequency','LC40'),
 ('Alveolar ventilation equation','Alveolar ventilation = (CO₂ output ÷ PaCO₂) × 863 → PaCO₂ ∝ CO₂ output ÷ alveolar ventilation','LC40'),
 ('Red blood cell transit time','Pulmonary capillary blood volume ÷ cardiac output (in mL/s)','LC40/41'),
 ('Fick principle','O₂ uptake = cardiac output × (arterial O₂ content − venous O₂ content)','LC42'),
 ('Pulmonary vascular resistance','(Mean pulmonary artery pressure − left atrial pressure) ÷ cardiac output','LC42'),
 ('Arterial O₂ content','(Hemoglobin × 1.34 × saturation) + (PO₂ × 0.003)','LC45'),
 ('Henry\'s law','Dissolved O₂ = PO₂ × 0.003 mL/100 mL/mmHg','LC41'),
 ('Boyle\'s law','P₁V₁ = P₂V₂','LC41'),
 ('Nitrogen washout','Lung volume = exhaled N₂ volume ÷ 0.79','LC40'),
]
PROBS=[ # (section, [(question, worked answer)])
('Dalton · inspired · alveolar gas (LC41)',[
 ('Dry-air PO₂ at sea level (barometric pressure 760)?','760 × 0.21 ≈ 160 mmHg (Poole: 159 using 20.93%)'),
 ('Dry-air PO₂ at 10,000 ft (barometric pressure 523)?','523 × 0.21 ≈ 110 mmHg'),
 ('Inspired (tracheal) PO₂ at sea level?','(760 − 47) × 0.21 ≈ 149–150 mmHg'),
 ('Inspired PO₂ at 10,000 ft (barometric pressure 523)?','(523 − 47) × 0.21 = 476 × 0.21 ≈ 100 mmHg'),
 ('★ Alveolar PO₂ at sea level: PaCO₂ 40, R 0.8?','149 − (40 ÷ 0.8) = 149 − 50 ≈ 100 mmHg'),
 ('Alveolar PO₂ at 10,000 ft: inspired 100, PaCO₂ 32 (hyperventilating), R 0.8?','100 − (32 ÷ 0.8) = 100 − 40 = 60 mmHg'),
 ('★ Explain why alveolar PO₂ (~100) < dry air (~159)','Warming + moistening (water vapor 47 mmHg) → 149 · then diluted by alveolar CO₂ · and R < 1 (more O₂ removed than CO₂ added)'),
]),
('Hypoventilation · alveolar–arterial difference (LC43)',[
 ('★ Barbiturate overdose halves alveolar ventilation, CO₂ output unchanged. PaCO₂ was 40. New PaCO₂?','PaCO₂ ∝ 1 ÷ alveolar ventilation → doubles → 80 mmHg'),
 ('Same dog, R 0.8: new alveolar PO₂?','149 − (80 ÷ 0.8) = 149 − 100 = 49 mmHg'),
 ('Sheep: PaCO₂ 60, R 0.8. Alveolar PO₂?','149 − (60 ÷ 0.8) = 149 − 75 = 74 mmHg'),
 ('★ Dog on room air: PaO₂ 49, PaCO₂ 48, R 0.8. Alveolar–arterial difference?','Ideal alveolar = 149 − 48/0.8 = 149 − 60 = 89 → 89 − 49 = 40 mmHg (big → mismatch)'),
 ('Dog: PaO₂ 70, PaCO₂ 40, R 0.8. Alveolar–arterial difference?','Ideal alveolar = 149 − 50 = 99 → 99 − 70 ≈ 29 mmHg'),
 ('Alveolar ventilation doubles, CO₂ output unchanged. PaCO₂ from 40 →?','Halves → 20 mmHg (hyperventilation)'),
 ('CO₂ output doubles (exercise) and alveolar ventilation doubles. PaCO₂?','Stays 40 mmHg (that\'s the goal of breathing)'),
]),
('Bohr · breathing pattern · nitrogen washout (LC40)',[
 ('★ Cow: PaCO₂ 40, expired PCO₂ 20. Dead space ÷ tidal volume?','(40 − 20) ÷ 40 = 0.5'),
 ('Horse: PaCO₂ 40, expired PCO₂ 24. Dead space ÷ tidal volume?','(40 − 24) ÷ 40 = 0.4'),
 ('Dog: PaCO₂ 40, expired PCO₂ 28. Dead space ÷ tidal volume?','(40 − 28) ÷ 40 = 0.3'),
 ('Total ventilation 8 L/min, dead space 0.15 L, 16 breaths × 0.5 L. Alveolar ventilation?','Dead space: 16 × 0.15 = 2.4 · alveolar: 8 − 2.4 = 5.6 L/min'),
 ('Same 8 L/min but 40 breaths × 0.2 L. Alveolar ventilation?','Dead space: 40 × 0.15 = 6.0 · alveolar: 8 − 6 = 2.0 L/min → rapid shallow wastes air'),
 ('Nitrogen washout: 40 L exhaled at 6% N₂. Starting lung volume?','40 × 0.06 = 2.4 L N₂ → 2.4 ÷ 0.79 ≈ 3.0 L'),
]),
('Transit time · Henry · Boyle (LC40–41)',[
 ('Capillary volume 70 mL, cardiac output 6,000 mL/min. Transit time?','6,000 ÷ 60 = 100 mL/s → 70 ÷ 100 = 0.7 s'),
 ('Exercise: capillary volume 150 mL, cardiac output 30,000 mL/min. Transit time?','30,000 ÷ 60 = 500 mL/s → 150 ÷ 500 = 0.3 s'),
 ('Dissolved O₂ at PaO₂ 100?','100 × 0.003 = 0.3 mL/100 mL'),
 ('Dissolved O₂ at PaO₂ 600 (breathing 100% O₂)?','600 × 0.003 = 1.8 mL/100 mL'),
 ('Closed chamber, constant temperature: volume doubles. Pressure?','Halves (P₁V₁ = P₂V₂)'),
 ('O₂ vs CO₂ pressure gradient across the barrier?','O₂: 100 − 40 = 60 mmHg · CO₂: 46 − 40 = 6 mmHg'),
]),
('Fick principle · pulmonary vascular resistance (LC42)',[
 ('Rest: cardiac output 5,000 mL/min, arterial 20, venous 15 mL/100 mL. O₂ uptake?','5,000 × (20 − 15)/100 = 250 mL/min'),
 ('Dog: cardiac output 3 L/min, arterial 20, venous 15 mL/100 mL. O₂ uptake?','3,000 × 5/100 = 150 mL/min'),
 ('★ Horse: cardiac output 250 L/min, arterial 25, venous 4 mL/100 mL. O₂ uptake?','250,000 × 21/100 = 52,500 mL/min ≈ 52.5 L/min'),
 ('Rest: mean pulmonary artery 15, left atrial 5, cardiac output 5 L/min. Resistance?','(15 − 5) ÷ 5 = 2 mmHg·min/L'),
 ('Exercise: mean pulmonary artery 25, left atrial 8, cardiac output 25 L/min. Resistance?','(25 − 8) ÷ 25 ≈ 0.7 → resistance FALLS (recruitment + distension)'),
]),
('O₂ content · extraction (LC45)',[
 ('★ Hemoglobin 15 g/100 mL, 97% saturated, PaO₂ 100. Arterial O₂ content?','15 × 1.34 × 0.97 = 19.5 + 0.3 = 19.8 ≈ 20 mL/100 mL'),
 ('★ Hemoglobin 10, PaO₂ 100, 97% saturated?','10 × 1.34 × 0.97 = 13.0 + 0.3 ≈ 13.3 mL/100 mL (anemia)'),
 ('★ Hemoglobin 18, PaO₂ 80, 93% saturated?','18 × 1.34 × 0.93 = 22.4 + 0.24 ≈ 22.7 mL/100 mL (horse in exercise: spleen ↑ hemoglobin, mild hypoxemia)'),
 ('No hemoglobin: O₂ uptake 250 mL/min, dissolved O₂ 0.3 mL/100 mL all extracted. Cardiac output needed?','250 ÷ (0.3 × 10 per L) = 250 ÷ 3 ≈ 83 L/min'),
 ('★ St. Bernard in heart failure: cardiac output 4 → 2 L/min, same O₂ uptake. Extraction?','Arteriovenous O₂ difference DOUBLES (e.g., 5 → 10 mL/100 mL)'),
 ('Same dog: arterial 20 → venous 10 mL/100 mL, P50 32. Venous PO₂ and saturation?','10/20 = 50% saturated → PO₂ = P50 = 32 mmHg'),
]),
]
eq='<div class="sec trap"><h2>📇 Equations for your note card</h2><table>'+''.join(f'<tr><td>{E(n)}</td><td>{E(e)} <span style="color:#8a6b99;font-size:13px">({l})</span></td></tr>' for n,e,l in EQ)+'</table></div>'
rows=lambda it:''.join(f'<tr class="{"hy" if q.startswith("★") else ""}"><td>{E(q)}</td><td><span class="ans">{E(a)}</span></td></tr>' for q,a in it)
secs=''.join(f'<div class="sec{" p" if i%2 else ""}"><h2>{E(s)}</h2><table>{rows(it)}</table></div>' for i,(s,it) in enumerate(PROBS))
total=sum(len(i) for _,i in PROBS)
bar='<div class="bar"><script defer src="shuffle.js"></script><button id="hide">🙈 Hide all</button><button id="all">👀 Show all</button><span class="n" id="n"></span></div>'
open(FN,'w').write(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>🧮 Exam 3 Calculation Practice</title><style>{css}</style></head><body><div class="wrap"><a class="back" href="{E3}?v={V}">← Back to Exam 3</a><div class="hero"><h1>🧮 Calculation Practice</h1><p>Poole lets you bring a note card with equations · work it on paper, then tap to check · {total} problems</p></div><div class="key">★ pink = from Poole\'s own notes/questions · numbers rounded like he does · not tested: memorizing values</div>{eq}{bar}{secs}<div class="foot">🎀 Bethany · K-State CVM Class of 2030 · 🐾</div></div><script>{js}</script></body></html>')
print(FN,total)
