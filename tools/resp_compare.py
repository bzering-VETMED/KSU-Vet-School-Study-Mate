# Build: Exam 3 · ⚖️ Look-alikes (comparison tables) + 🧮 Equation sheet (note-card view + print)
# Run from repo root AFTER tools/resp_terms.py (reuses its CSS). Tiles added in resp_terms.py.
import re,time,html
E=html.escape; V=str(int(time.time()))
E3='systems-lec-exam3.html'
css=re.search(r'<style>(.*?)</style>',open('systems-lec3-pp3-terms.html').read(),re.S).group(1)
css+=('.cmp{background:#fff;border:1px solid var(--line);border-left:6px solid var(--g);border-radius:14px;padding:8px 10px;margin:12px 0;overflow-x:auto}'
      '.cmp.w4 table{font-size:13px}.cmp.w4 td{padding:4px 3px}.cmp.w4 th{font-size:12.5px;padding:4px 3px}.cmp h2{margin:0 0 2px;font-size:18px;color:var(--v)}.cmp .src{font-size:13px;color:#6b4c7d;margin:0 0 6px}'
      '.cmp table td:first-child{width:auto}.cmp th{background:#5C1B96;color:#fff;font-size:14px;padding:6px;text-align:left}.cmp th:first-child{background:#fff}'
      '.cmp .hook{margin:6px 0 0;font-size:14px;background:#FDE3F1;border-radius:8px;padding:5px 8px}.cmp .hook b{color:var(--p)}'
      'body.quiz .c{background:linear-gradient(135deg,#C9B6E4,#F2B6D6)!important;color:transparent;cursor:pointer;border-radius:6px}body.quiz .c.on{background:transparent!important;color:var(--ink)}'
      '.tag{font-size:12px;font-weight:800;border-radius:999px;padding:1px 7px;margin-left:4px;vertical-align:middle}.t1{background:#FDE3F1;color:#B0206F}.t2{background:#EFE0FE;color:#5C1B96}'
      '.eq{background:#fff;border:1px solid var(--line);border-left:6px solid var(--g);border-radius:14px;padding:8px 12px;margin:10px 0;break-inside:avoid}.eq.star{border-left-color:var(--p)}'
      '.eq h3{margin:0;font-size:17px;color:var(--v)}.eq .f{font:700 17px/1.4 "SF Mono",Menlo,Consolas,monospace;color:var(--ink);background:var(--lav);border-radius:8px;padding:5px 8px;margin:5px 0}'
      '.eq .pl{margin:4px 0;font-size:15px}.eq .ex{margin:4px 0;font-size:14.5px;background:#FFF8EC;border-radius:8px;padding:5px 8px}.eq .ex b{color:#B26B00}.eq .src{font-size:12.5px;color:#6b4c7d}'
      'body.card .pl,body.card .ex,body.card .src,body.card .hide-card{display:none}body.card .eq{padding:4px 8px;margin:5px 0}body.card .eq .f{font-size:14px;padding:2px 6px;margin:2px 0}body.card .eq h3{font-size:14px}'
      '@media print{.back,.bar,.hero p,.foot,.hide-card,.key{display:none!important}body{background:#fff}.hero{background:none;color:#000;padding:0}.hero h1{font-size:14px}.eqs{column-count:2;column-gap:10px}.eq{border:1px solid #999;border-left:3px solid #000;margin:3px 0;padding:2px 6px}.eq h3{font-size:11px;color:#000}.eq .f{font-size:11px;background:none;padding:0;margin:0}.eq .pl,.eq .ex,.eq .src{display:none}}')
def page(fn,title,sub,body,js=''):
    open(fn,'w').write(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(title)}</title><style>{css}</style></head><body><div class="wrap"><a class="back" href="{E3}?v={V}">← Back to Exam 3</a><div class="hero"><h1>{E(title)}</h1><p>{sub}</p></div>{body}<div class="foot">🎀 Bethany · K-State CVM Class of 2030 · 🐾</div></div><script>{js}</script></body></html>')
TAG={'⭐':'<span class="tag t1">⭐ emphasized</span>','🔹':'<span class="tag t2">🔹 mentioned</span>'}

# ── ⚖️ COMPARISONS: (title, scope, source, [headers], [(row label, cells…)], hook)
C=[
('Emphysema vs fibrosis','⭐','Deck 6 slide 16 · notes 6',['','Emphysema','Fibrosis'],[
 ('What happens','Holes in the elastin/collagen weave (alveolar walls destroyed)','Scar tissue builds up in the lung'),
 ('Compliance','<b>INCREASED</b> (baggy, too stretchy)','<b>DECREASED</b> (stiff)'),
 ('Recoil','Weak','Strong'),
 ('Hard to…','Get air <b>OUT</b> (airways collapse, air trapped)','Get air <b>IN</b>'),
 ('Pattern','Obstructive','Restrictive'),
 ('Pleural pressure','Less negative','More negative'),
 ('Gas exchange','Lost surface AREA (Fick)','Thicker barrier (Fick) → diffusion limitation on exercise'),
 ('Clue','Crackles','Thin animal (huge work of breathing)')],
 '<b>Hook:</b> Emphysema = an Empty, baggy balloon. Fibrosis = Firm.'),
('Obstructive vs restrictive','⭐','Deck 6 slides 36–39 · notes 6',['','Obstructive','Restrictive'],[
 ('Example','Emphysema, airway narrowing','Fibrosis'),
 ('Main problem','Air can\'t get OUT (airways collapse early)','Lung can\'t expand; can\'t pull airways open'),
 ('Residual volume','<b>Big</b> (air trapped)','Small (small lungs)'),
 ('Total lung capacity','Normal to big <i>(outside knowledge)</i>','<b>Small</b>'),
 ('Max expiratory flow','Low (airway collapse)','Low (small volumes, weak traction on airways)')],
 '<b>Trap:</b> both have LOW max flow, for DIFFERENT reasons.'),
('Functional residual capacity vs residual volume vs vital capacity','⭐','Deck 2 slides 9–11 · notes 2 · <b>your miss (Quiz 9 Q10)</b>',['','Functional residual capacity','Residual volume','Vital capacity'],[
 ('Definition','Volume left after a <b>normal, passive</b> exhale','Volume left after a <b>maximal, forced</b> exhale','Most air you can move: max inhale → max exhale'),
 ('Muscles acting?','<b>NONE</b>; lung recoil in = chest wall springs out','Yes (maximal effort)','Yes'),
 ('Spirometer?','No (contains residual volume)','<b>No</b>: can\'t blow it out → nitrogen washout','Yes'),
 ('Formula','Expiratory reserve + residual volume','Never zero','Total lung capacity − residual volume')],
 '<b>Hook:</b> "Functional" = where you Float at rest. "Residual" = the Reserve you can never get out.'),
('Anatomical vs physiological dead space','⭐','Deck 2 slides 16–20 · notes 2 · <b>your miss (Quiz 9 Q9)</b>',['','Anatomical dead space','Physiological dead space'],[
 ('What it is','Conducting airways (nose → terminal bronchioles); no alveoli','Anatomical + alveoli that get air but <b>no blood</b>'),
 ('Example','Long neck / long airways (cows, horses)','Pulmonary thromboembolism: ventilated, NOT perfused'),
 ('How measured','—','<b>Bohr equation</b>: (PaCO₂ − PECO₂) ÷ PaCO₂'),
 ('In disease','Same','<b>Increases</b> (many lung diseases ↑ dead space)')],
 '<b>Hook:</b> blood clot in the lung → "physiological" dead space, because it\'s physiology (blood flow) that failed.'),
('5 causes of hypoxemia','⭐','Deck 5 · notes 5',['','PaCO₂','Fixed by 100% O₂?','Key clue / example'],[
 ('1. Low inspired PO₂','<b>LOW</b> (animal breathes harder)','Yes','Altitude, wrong anesthetic gas'),
 ('2. Hypoventilation','<b>HIGH</b>','Yes','Airway obstruction, muscle weakness, CNS drugs. Normal alveolar–arterial difference'),
 ('3. Diffusion limitation','Usually normal','Yes','Thick barrier; shows on EXERCISE; measure diffusing capacity'),
 ('4. Right-to-left shunt','Usually normal <i>(outside knowledge)</i>','<b>NO</b> (barely)','Patent ductus arteriosus, septal defect, collapsed lung'),
 ('5. Ventilation-perfusion mismatch','Normal (good units clear CO₂)','Yes','Most lung disease; big alveolar–arterial difference')],
 '<b>Trap:</b> 1 vs 2 → look at CO₂. Shunt → the ONE that 100% O₂ won\'t fix.'),
('Alveolar vs extra-alveolar vessels','⭐','Deck 4 slides 9–12 · notes 4',['','Alveolar vessels','Extra-alveolar vessels'],[
 ('What they are','Capillaries in the alveolar walls','Arterioles, venules (outside alveoli)'),
 ('Pressure around them','Alveolar pressure','Lung tissue (pleural-like) pressure'),
 ('High lung volume','<b>Squeezed / stretched</b> → resistance UP','<b>Pulled OPEN</b> (radial traction) → resistance DOWN'),
 ('Low lung volume','Open','<b>Narrow</b> → resistance UP'),
 ('Ventilator warning','Too much positive pressure squeezes them shut','—')],
 '<b>Hook:</b> inflate the lung: the walls squeeze the capillaries inside them, but tug the big vessels outside open.'),
('Bohr EFFECT vs Bohr EQUATION','⭐','Deck 7 slide 18 + notes 7 · deck 2 slides 18–19',['','Bohr EFFECT','Bohr EQUATION'],[
 ('Topic','Hemoglobin / O₂ curve','Dead space'),
 ('Statement','↑ CO₂, ↑ H⁺, ↑ temperature → curve shifts RIGHT → hemoglobin lets go of O₂','Dead-space fraction = (PaCO₂ − PECO₂) ÷ PaCO₂'),
 ('Where it matters','Exercising muscle unloads more O₂','Measuring wasted ventilation (e.g., clot in lung)')],
 '<b>Trap:</b> same name, different lectures. EFFECT = Exercising muscle. EQUATION = Exhaled CO₂.'),
('Haldane vs Bohr effect','🔹','Notes 7 · deck 7',['','Haldane effect','Bohr effect'],[
 ('Which gas changes binding?','<b>CO₂</b> binding changes','<b>O₂</b> binding changes'),
 ('Caused by','Hemoglobin losing O₂','CO₂ / acid / heat'),
 ('Result','Deoxygenated hemoglobin carries MORE CO₂','Hemoglobin releases MORE O₂'),
 ('Where','Tissues (load CO₂) + lungs (dump CO₂ as O₂ binds)','Tissues (unload O₂)')],
 '<b>Hook:</b> Haldane = Hemoglobin Hauls CO₂ when O₂ leaves. Bohr = O₂ leaves when CO₂ arrives. Mirror images.'),
('Roaring vs honking','⭐','Deck 6 slides 12–13, 38 · notes 6',['','Roaring','Honking'],[
 ('Species','Horse','Toy / brachycephalic dogs (Yorkies, Poms, bulldogs, poodles)'),
 ('Lesion','Left laryngeal hemiplegia (paralyzed left larynx)','Tracheal collapse (weak trachea)'),
 ('Location','Larynx: <b>extrathoracic</b>','<b>Intrathoracic</b> trachea'),
 ('When','<b>INSPIRATION</b> (larynx sucked in)','<b>EXPIRATION</b> (chest pressure squeezes trachea)')],
 '<b>Hook:</b> A horse Roars as it bReathes IN. A dog Honks while blowing OUT.'),
('Type I vs Type II pneumocyte vs club cell','⭐','LC38 (Basel) · deck 1 slides 43–44 · <b>your miss (10/18 quiz Q3)</b>',['','Type I pneumocyte','Type II pneumocyte','Club cell'],[
 ('Where','Alveolus','Alveolus','<b>Bronchiole</b>'),
 ('Shape','Thin, squamous','Cuboidal','Non-ciliated (cuboidal epithelium area)'),
 ('Job','Gas-exchange wall (with endothelium)','<b>Surfactant</b>; repairs Type I','Some surfactant; breaks down mucus'),
 ('Progenitor for','—','<b>Alveolar</b> epithelium (makes new Type I)','<b>Bronchiolar</b> epithelium')],
 '<b>Trap:</b> check LOCATION first. Bronchiole → club cell. Alveolus → Type II.'),
('True vs false vocal fold','⭐','LC37 (Basel) · <b>your miss</b>',['','True vocal fold','False vocal fold'],[
 ('Job','Vibrates → vocalization','Modifies airflow; does NOT vibrate'),
 ('Epithelium','<b>Stratified squamous non-keratinized</b>','<b>Respiratory epithelium</b> (pseudostratified ciliated columnar)'),
 ('Why that epithelium','Takes abrasion from vibrating','No vibration → no need for tough lining'),
 ('Tension','Muscle changes tension → changes how air vibrates','Not tensed; just moderates airflow')],
 '<b>Hook:</b> the TRUE fold does the TOUGH work → TOUGH (stratified squamous) lining.'),
('Adventitia vs serosa','⭐','LC37 (Basel) · <b>your miss</b>',['','Tunica adventitia','Tunica serosa'],[
 ('Outer layer is…','Connective tissue that <b>blends</b> into surroundings','Connective tissue <b>bounded by a serosal membrane</b> (flat squamous mesothelium)'),
 ('Where','Organ NOT in a body cavity','Organ inside a body cavity'),
 ('Trachea','<b>Cervical</b> (neck) trachea','<b>Thoracic</b> trachea / lungs (pleura)')],
 '<b>Hook:</b> Neck → adveNtitia. Serosa → in a Space (body cavity).'),
]
body=('<div class="key">⭐ = Poole/Basel emphasized · 🔹 = mentioned · <b style="color:#E0459A">pink box = memory hook or trap</b></div>'
      '<div class="bar"><button id="qz">🙈 Quiz me (hide cells)</button><button id="sh">👀 Show all</button><span class="n" id="n"></span></div>')
for ti,sc,src,hd,rows,hook in C:
    body+=(f'<div class="cmp{" w4" if len(hd)>3 else ""}"><h2>{E(ti)}{TAG[sc]}</h2><p class="src">{src}</p><table><tr>'+''.join(f'<th>{h}</th>' for h in hd)+'</tr>'
           +''.join('<tr><td>'+r[0]+'</td>'+''.join(f'<td class="c">{c}</td>' for c in r[1:])+'</tr>' for r in rows)+f'</table><p class="hook">{hook}</p></div>')
js=("const B=document.body,C=[...document.querySelectorAll('.c')],N=document.getElementById('n');function u(){N.textContent=B.classList.contains('quiz')?C.filter(c=>c.classList.contains('on')).length+' / '+C.length:''}"
    "C.forEach(c=>c.onclick=()=>{if(B.classList.contains('quiz')){c.classList.toggle('on');u()}});"
    "document.getElementById('qz').onclick=()=>{B.classList.add('quiz');C.forEach(c=>c.classList.remove('on'));u()};document.getElementById('sh').onclick=()=>{B.classList.remove('quiz');u()};")
page('systems-lec3-compare.html','⚖️ Look-alikes','12 comparison tables · read, then hit 🙈 Quiz me and say each cell out loud',body,js)

# ── 🧮 EQUATIONS: (name, scope, formula, plain English, worked example, source)
Q=[
('Fick\'s law of diffusion','⭐','V̇gas = A/T × D × (P₁ − P₂)   ·   D ∝ solubility ÷ √molecular weight','More gas crosses with a BIG area, THIN wall, and BIG pressure difference. Every lung disease breaks one of these.','CO₂: D ∝ 0.067/√44 ≈ 0.010 · O₂: D ∝ 0.003/√32 ≈ 0.0005 → CO₂ diffuses ~20× more easily, but its push is only 46 − 40 = <b>6</b> vs O₂ 100 − 40 = <b>60</b>.','Deck 3 slides 14–15 · deck 1 slide 22'),
('Dalton\'s law','🔹','Pgas = P_barometric × fraction of gas','Each gas\'s pressure = total pressure × its share. At altitude the 21% stays the same; the total drops.','Sea level: 760 × 0.21 = <b>159 mmHg</b>. Altitude (P_B 240): 240 × 0.21 ≈ <b>50 mmHg</b>.','Deck 3 slides 7–8'),
('Inspired PO₂ (in the trachea)','⭐','PIO₂ = (P_B − 47) × FIO₂','Air gets humidified; water vapor (47 mmHg) takes its share first. This is your 159 → 149 step.','(760 − 47) × 0.21 = <b>149 mmHg</b>.','Deck 3 slide 8 · your Quiz 9 Q11 miss'),
('Alveolar gas equation','⭐','PAO₂ = PIO₂ − (PACO₂ ÷ R)','Alveolar O₂ = what you breathe in, minus what CO₂ displaces. R = 0.8 at rest (more O₂ in than CO₂ out).','149 − (40 ÷ 0.8) = 149 − 50 = <b>~99–100 mmHg</b>. Hypoventilation (PaCO₂ 80): 149 − 100 = <b>49</b>.','Deck 3 slide 9 · deck 5 slide 10'),
('Respiratory exchange ratio','🔹','R = V̇CO₂ ÷ V̇O₂','CO₂ out ÷ O₂ in. ~0.8 at rest on a mixed diet → less CO₂ leaves than O₂ enters.','250 mL/min O₂ in, 200 mL/min CO₂ out → R = <b>0.8</b>.','Deck 3 slide 10'),
('Alveolar–arterial difference','⭐','A–a difference = PAO₂ (calculated) − PaO₂ (measured)','How much worse the blood is than the alveolar air. Big gap = ventilation-perfusion mismatch (or shunt/diffusion). Pure hypoventilation = normal gap.','Dog on room air: PaO₂ 49, PaCO₂ 48, R 0.8 → PAO₂ = 149 − 48/0.8 = 89 → 89 − 49 = <b>40 mmHg = severe mismatch</b>.','Deck 5 slide 23'),
('Bohr equation (dead space)','⭐','V_D ÷ V_T = (PaCO₂ − PECO₂) ÷ PaCO₂','How much of each breath is wasted. Dead-space air has no CO₂, so it dilutes exhaled CO₂.','(40 − 20) ÷ 40 = <b>0.5</b> → half of each breath is dead space.','Deck 2 slides 18–20 · your Quiz 9 Q9 miss'),
('Ventilation equations','🔹','V̇E = V_T × f   ·   V_T = V_D + V_A   ·   V̇E = (V_D × f) + (V_A × f)','Total breathing = breath size × rate. Every breath pays the dead-space "tax" first.','V̇E 8 L/min, V_D 0.15 L: slow (f 16, V_T 0.5) → V̇A = 16 × 0.35 = <b>5.6</b>. Fast (f 32, V_T 0.25) → 32 × 0.10 = <b>3.2</b>. Fast shallow wastes air.','Deck 2 slides 16–17'),
('Alveolar ventilation equation','⭐','V̇A = (V̇CO₂ × 0.863) ÷ PaCO₂','PaCO₂ is set by breathing vs CO₂ production. Breathe more → CO₂ down. Make more CO₂ → CO₂ up.','Same V̇CO₂, <b>double</b> V̇A → PaCO₂ 40 → <b>20</b>. Halve V̇A → <b>80</b>.','Deck 2 slide 21 · Quiz 9'),
('Red blood cell transit time','⭐','Transit time = pulmonary capillary blood volume ÷ cardiac output','How long a red cell stays in the lung capillary to load O₂.','Rest: 70 mL ÷ 83 mL/s = <b>0.84 s</b>. Exercise: 140 mL ÷ 500 mL/s = <b>0.28 s</b>. 🟠 Notes 3 rounds rest to ~0.75 s.','Deck 2 slide 7 · deck 3 slide 22'),
('Fick principle','🔹','V̇O₂ = Q̇ × (CaO₂ − CvO₂)','O₂ used = blood flow × how much O₂ each bit of blood drops off.','Rest: 5,000 mL/min × (20 − 15)/100 = <b>250 mL/min</b>. Exercise: 24,000 × (20 − 4)/100 = <b>3,840 mL/min</b>.','Deck 4 slides 21–22 · deck 7 slide 32'),
('Pulmonary vascular resistance','⭐','PVR = (mean pulmonary artery P − left atrial P) ÷ cardiac output','Pressure drop across the lung ÷ flow. The lung moves the SAME flow with ~1/10 the pressure drop → very low resistance.','Lung: (15 − 5) ÷ 5 L/min = <b>2</b>. Body: (100 − 2) ÷ 5 = <b>~20</b> → lung ≈ 1/10.','Deck 4 slides 3–4'),
('Henry\'s law','⭐','Dissolved gas = partial pressure × solubility  (O₂ 0.003 · CO₂ 0.067 mL/100 mL/mmHg)','Gas dissolves in proportion to its pressure. O₂ barely dissolves → we need hemoglobin.','O₂ at 100 mmHg: 100 × 0.003 = <b>0.3 mL/100 mL</b>. CO₂ at 46: 46 × 0.067 ≈ <b>3.1</b> (~20× more soluble).','Deck 3 slide 11 · your Quiz 9 Q13 miss'),
('Boyle\'s law','🔹','P₁V₁ = P₂V₂  (constant temperature)','Make the space bigger → pressure drops. That\'s how inspiration pulls air in.','2 L at 760 mmHg squeezed to 1 L → <b>1,520 mmHg</b> (halve volume = double pressure).','Deck 3 slides 12–13'),
('Law of Laplace','⭐','Alveolus: P = 2T ÷ r   (soap bubble with 2 surfaces: 4T ÷ r)','Small bubbles have higher collapsing pressure, so they empty into big ones. Surfactant lowers T to stop this.','Halve the radius → pressure <b>doubles</b> → small alveolus would collapse into a big one without surfactant.','Notes 6 · deck 6 slide 22'),
('Poiseuille\'s law (bonus)','🔹','R = 8ηl ÷ πr⁴   ·   V̇ = (P_atm − P_alv) ÷ R','Resistance depends on radius to the 4th power. Narrow a tube a little → resistance goes up a LOT.','Halve the radius → resistance × 2⁴ = <b>16×</b>.','Deck 6 slides 30–31'),
('Blood O₂ content','⭐','CaO₂ = (Hb × 1.34 × SaO₂) + (PO₂ × 0.003)','O₂ on hemoglobin + the tiny dissolved bit. He likes to give a NEW hemoglobin value.','Hb 15, 97%, PO₂ 100: 19.5 + 0.3 = <b>19.8 mL/100 mL</b>. Hb 10: 10 × 1.34 × 0.97 = 13.0 + 0.3 = <b>13.3</b>.','Deck 7 slide 15 · notes 7'),
('Nitrogen washout (FRC)','🔹','FRC = volume of N₂ exhaled ÷ 0.79','Breathe 100% O₂ until all N₂ (79% of lung air) is washed out; collect it.','5% × 40 L = 2 L N₂ → 2 ÷ 0.79 = <b>~2.5 L</b>.','Deck 2 slide 11'),
]
body=('<div class="key hide-card">⭐ = he stressed or quizzed it · 🔹 = mentioned · <b style="color:#B26B00">orange = worked example</b> · your note card is allowed</div>'
      '<div class="bar"><button id="cd">🗂️ Note-card view</button><button id="fl">📖 Full view</button><button onclick="print()">🖨️ Print</button></div><div class="eqs">')
for nm,sc,f,pl,ex,src in Q:
    body+=f'<div class="eq{" star" if sc=="⭐" else ""}"><h3>{E(nm)}{TAG[sc]}</h3><div class="f">{f}</div><p class="pl">💬 {pl}</p><p class="ex"><b>Example:</b> {ex}</p><div class="src">{src}</div></div>'
body+='</div>'
js="document.getElementById('cd').onclick=()=>document.body.classList.add('card');document.getElementById('fl').onclick=()=>document.body.classList.remove('card');"
page('systems-lec3-equations.html','🧮 Equation Sheet',f'{len(Q)} Poole equations · plain English + 1 worked example each · 🗂️ note-card view / 🖨️ print for your card',body,js)
print('compare',len(C),'equations',len(Q))
