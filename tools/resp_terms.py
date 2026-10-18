# Build: Veterinary Systems I · Lecture Exam 3 (Respiratory) · one-page tap-to-reveal Terms Review
# Run from repo root: python3 tools/resp_terms.py
# Sources: LC37 + LC38 transcripts/slides (Basel), Poole Pulm Phys 1 + 2 notes/slides/transcripts.
# Same look as the Lab Practical 1 Functions Review (tools/micro1.py).
import os,re,time,html
E=html.escape; V=str(int(time.time()))
FS='systems-lec3-terms.html'; HUB='systems-lecture.html'

# (section, [(term, short answer)])  — '★ ' prefix = professor emphasized → pink row
SECS=[
('lc37','LC37 · Respiratory System 1','Basel · upper airways & pleura',[
 ('Upper airways','Nares, nasal cavity, pharynx'),
 ('Lower airways','Larynx → trachea → bronchial tree → alveolar sacs'),
 ('Mammal lung vs bird lung','Mammal = blind-ended, mixes air (alveolar PO₂ ~100 vs air ~150) · Bird = one-way flow through lung via air sacs → more efficient'),
 ('Reptile breathing (3 ways)','Diaphragm (crocodilians) · chest-wall muscles · buccal pumping (small lizards)'),
 ('Amphibian gas exchange','Mostly through thin moist skin; some lungs or gills'),
 ('★ Obligate nasal breather','Horse; epiglottis position. Nares collapse at high flow → more negative pressure → contributes to EIPH (exercise-induced pulmonary hemorrhage)'),
 ('Elephant pleura','No pleural space (connective tissue instead) · helps snorkeling'),
 ('Marine mammal lungs','Collapsible; water pressure on dives raises lung O₂ pressure'),
 ('3 tunics of airway','Tunica mucosa → tunica submucosa → tunica adventitia (or serosa)'),
 ('Tunica mucosa = 3 parts','Epithelium + lamina propria + muscularis mucosa'),
 ('Tunica muscularis in airways?','No (it appears in the gut)'),
 ('Adventitia vs serosa','Adventitia blends into surroundings · serosa is bounded by a serosal membrane (in a body cavity)'),
 ('Respiratory epithelium','Pseudostratified columnar with cilia + goblet cells'),
 ('Nasal conchae','Thin bones, huge surface area → warm, filter, and especially MOISTEN air'),
 ('Olfactory epithelium','Thicker; contains olfactory sensory neurons'),
 ('Olfactory (Bowman\'s) glands','Mucus dissolves odorants, then washes them away'),
 ('Larynx','First portion 100% devoted to the airway'),
 ('False vocal fold','Respiratory epithelium + glands; does not vibrate'),
 ('True vocal fold','Stratified squamous non-keratinized epithelium + muscle (vibrates)'),
 ('Tracheal cartilage','C-shaped rings in the adventitia → prevent collapse during inhalation'),
 ('Trachealis muscle','Closes back of the rings; relaxes so the esophagus can expand when swallowing'),
 ('Diffuse neuroendocrine cells','Release serotonin; dysregulation → asthma (not visible on H&E)'),
 ('Visceral vs parietal pleura','Visceral = on the lung · parietal = on the chest wall'),
 ('Pleural space pressure','Negative → holds lungs open; more negative on inhalation'),
 ('★ Pneumothorax','Air in pleural space → negative pressure lost → lung collapses'),
 ('Spontaneous pneumothorax','Ruptured blebs/bullae on lung surface (case: Siberian husky)'),
]),
('lc38','LC38 · Respiratory System 2','Basel · lower airways & alveoli',[
 ('Conducting airways','Bronchi + bronchioles · thick walls · NO gas exchange = dead space'),
 ('Exchange airways','Start at respiratory bronchioles → alveolar ducts → alveolar sacs'),
 ('Total cross-sectional area going deeper','Increases → resistance drops + air slows'),
 ('Highest resistance','Trachea + early bronchi'),
 ('★ Poiseuille\'s law','Resistance ∝ 1 / radius⁴ (small constriction → huge resistance)'),
 ('2 types of breathing work','Resistive (airway diameter) + elastic (stretching lungs)'),
 ('Bronchus ID','Cartilage PLATES in the adventitia + glands + pseudostratified epithelium'),
 ('Bronchiole ID','NO cartilage · thick smooth muscle · simple cuboidal/columnar epithelium'),
 ('What replaces cartilage in bronchioles?','Smooth muscle (muscularis mucosa)'),
 ('Club cells','Bronchioles · break down mucus, detoxify, start making surfactant'),
 ('Surface tension','Water shrinks its surface (entropy) → pulls lungs closed'),
 ('Surfactant','Surface-acting agent → lowers surface tension → less elastic work'),
 ('Respiratory bronchiole ID','Bronchiole wall with a FEW alveoli opening off the side'),
 ('Alveolar duct ID','Wall is all alveoli · septa end in smooth-muscle KNOBS'),
 ('Alveolar sac ID','Blind end · septa end in sharp POINTS'),
 ('Type I pneumocyte','Squamous · lines alveoli · forms the blood-air barrier'),
 ('Type II pneumocyte','Cuboidal, at corners · secretes surfactant + stem cell for Type I'),
 ('Alveolar macrophage','Phagocytic; keeps alveoli clean (in lumen or wall)'),
 ('★ Blood-air barrier = 3 layers','Type I pneumocyte → fused basement membrane → capillary endothelial cell'),
 ('Not part of the barrier','Type II pneumocytes + macrophages'),
 ('Why pulmonary pressure stays low','Barrier is so thin, high pressure ruptures capillaries (EIPH)'),
 ('Asthma','Overreactive airways → bronchoconstriction + excess mucus → ↑ resistive work'),
 ('Asthma x-ray','Bright branching pattern (bronchial inflammation/fluid)'),
 ('Albuterol','Beta-2 agonist (mimics sympathetic) → bronchodilation; rescue inhaler'),
 ('Long-term asthma treatment','Corticosteroids (reduce inflammation)'),
]),
('pp1','LC39 · Pulmonary Physiology 1','Poole · structure',[
 ('★ What does breathing regulate?','Arterial PCO₂ (~40 mmHg) and pH'),
 ('Oxygen uptake equation','(Inspired ventilation × inspired O₂ fraction) − (expired ventilation × expired O₂ fraction)'),
 ('% of inspired O₂ the lung extracts','~25%, even during exercise (defends alveolar PO₂; horse = exception)'),
 ('Body size vs resting O₂ use per kg','Smaller animal → higher → more risk under anesthesia'),
 ('Hyperventilation effect','↓ CO₂ → ↑ pH → cerebral arterioles constrict → ↓ brain blood flow'),
 ('Lungs vs kidneys for acid–base','Lungs: fast, ~10,000 mmol CO₂/day · kidneys: low capacity, days–weeks'),
 ('★ Fick\'s law','Gas flow = Area / Thickness × Diffusing capacity × (P alveolar − P blood)'),
 ('Gases move down their…','PRESSURE gradient (not concentration)'),
 ('Blood-gas barrier thickness','~0.3 µm (human)'),
 ('Number of alveoli (human)','~300 million'),
 ('Unicameral lung','One big sac (tegu lizard) → tiny surface area, low capacity'),
 ('Bird lung exchange','Unidirectional, cross-current; no mixing → blood PO₂ near atmospheric (bar-headed geese over Everest)'),
 ('Mammal lung = ?','Mixing-pool (uniform pool) exchanger'),
 ('Intrapleural space','~100 µm of fluid; lubricates lung sliding; lungs have no muscles of their own'),
 ('Particle >5 µm','Impacts in large airways'),
 ('Particle 1–5 µm','Sediments in small airways'),
 ('Particle ~0.1 µm','Reaches alveoli by diffusion (e.g., asbestos)'),
 ('Mucociliary escalator','Goblet-cell mucus + cilia move particles toward mouth; only in non-exchange airways'),
 ('Small airway diameter depends on…','Alveolar tethering → varies with lung volume'),
 ('Pores of Kohn','Holes in alveolar walls; Poole: macrophages climb through'),
 ('Type I cell (Poole)','~90% of alveolar surface; metabolically inert'),
 ('Surfactant molecule','Dipalmitoyl phosphatidylcholine (lecithin), from Type II cells'),
 ('Macrophages won\'t eat…','Silica + asbestos'),
 ('Collateral ventilation','Dog/cat = high · horse = intermediate · pig/cattle = none'),
 ('Conducting zone volume (human)','~150 mL vs respiratory zone 2–5 L'),
 ('Greatest total cross-sectional area','Respiratory zone (gas moves mostly by diffusion)'),
 ('★ Obstruction in large airway vs parenchyma','Large airway = noticed early (small total area) · deep lung = silent for long'),
 ('% of airway resistance in large airways','~70%'),
]),
('pp2','LC40 · Pulmonary Physiology 2','Poole · volumes & ventilation',[
 ('3 steps to get O₂ into blood','Ventilation → diffusion → blood flow'),
 ('Tidal volume','Air per breath (~500 mL human; horse ~7.5 L)'),
 ('★ Red blood cell transit time','Pulmonary capillary blood volume ÷ cardiac output (~0.84 s rest → ~0.28 s exercise)'),
 ('Why transit time falls in exercise','Cardiac output ↑ 6–10× but capillary volume only ~2×'),
 ('Exercise-induced hypoxemia','Racehorses, greyhounds, elite humans (red cells move too fast)'),
 ('★ Functional residual capacity','End of normal exhale; NO muscles acting; intrapleural ≈ −5 cm H₂O'),
 ('Total lung capacity','Maximum air after deepest breath in'),
 ('Residual volume','Air left after maximal exhale (never 0)'),
 ('Vital capacity','Total lung capacity − residual volume'),
 ('Can a spirometer measure residual volume?','No → use nitrogen washout, helium dilution, or plethysmography'),
 ('Nitrogen washout','Breathe 100% O₂, collect N₂ → N₂ volume ÷ 0.79 = lung volume'),
 ('Exhalation at rest','Passive'),
 ('Emphysema','Obstructive; airways collapse (crackles); ↑ functional residual capacity + residual volume'),
 ('Ventilation equation','Total ventilation = dead space ventilation + alveolar ventilation'),
 ('★ Deep-slow vs rapid-shallow','Deep, slow = more alveolar ventilation · rapid, shallow wastes air in dead space'),
 ('Panting dog','Shallow breaths for heat loss, NOT hyperventilation'),
 ('Dead space / tidal volume ratio','Human ~0.3 · horse/cattle 0.5–0.75 · falls with exercise'),
 ('★ Bohr equation','Dead space / tidal volume = (PaCO₂ − expired PCO₂) ÷ PaCO₂'),
 ('Cow: PaCO₂ 40, expired PCO₂ 20','Dead space / tidal volume = 0.5'),
 ('Anatomic vs physiologic dead space','Anatomic = conducting zone · physiologic adds ventilation-perfusion mismatch'),
 ('★ Alveolar ventilation equation','Alveolar ventilation = (CO₂ output ÷ PaCO₂) × 863'),
 ('Alveolar ventilation doubles, CO₂ output unchanged','PaCO₂ halves'),
 ('Ventilation-perfusion mismatch','Always bad → hypoxemia; severe → hypercapnia too'),
 ('★ Which region gets most ventilation?','BASE (gravity)'),
 ('Apex alveoli','Stretched, stiff → expand less'),
 ('Base alveoli','Small, compliant → fill easily'),
 ('Compliance','Volume change ÷ pressure change (lung ~10× a balloon)'),
 ('Diseased lungs + exercise','Respiratory muscles steal cardiac output from limbs → exercise intolerance'),
]),
]
TRAPS={
 'lc37':['Adventitia ≠ serosa · trachea switches to serosa once inside the thorax',
         'False vocal fold = respiratory epithelium · TRUE vocal fold = stratified squamous',
         'Trachea = C-shaped RINGS (bronchus = plates)',
         'Basel said bird lung "CO₂ ~150" → he meant O₂'],
 'lc38':['Bronchus = cartilage PLATES · trachea = C-shaped RINGS · bronchiole = NONE',
         'Alveolar duct septa = KNOBS · alveolar sac septa = POINTS',
         'Type II pneumocyte is NOT part of the blood-air barrier',
         'Basel: premature surfactant deficit before ~36 weeks · Poole: ~34 weeks → use Poole for his questions'],
 'pp1':['Total cross-sectional area is SMALLEST in large airways (individual airways are biggest)',
        'Gases follow PRESSURE gradients, not concentration',
        'Lung O₂ extraction stays ~25% in exercise · TISSUE extraction rises to 80–90%',
        'Poole: premature surfactant deficit before ~34 weeks · Basel said ~36 → use Poole'],
 'pp2':['Functional residual capacity (no muscles acting) ≠ residual volume (after max exhale)',
        'Vital capacity = total lung capacity − residual volume',
        'Panting ≠ hyperventilation (shallow breaths, mostly dead space)',
        'Most ventilation goes to the BASE (compliant alveoli), not the apex'],
}

rows=lambda items:''.join(
  f'<tr class="{"hy" if t.startswith("★") else ""}"><td>{E(t)}</td><td><span class="ans">{E(a)}</span></td></tr>' for t,a in items)
css=""":root{--ink:#330B4D;--v:#6A0DAD;--g:#7B2FBE;--p:#E0459A;--line:#E3D0F2;--lav:#F5ECFD}*{box-sizing:border-box}body{margin:0;color:var(--ink);font:16px/1.4 -apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif;background:radial-gradient(circle at 0 0,#FBE4F4 0,transparent 30%),radial-gradient(circle at 100% 0,#EFE0FE 0,transparent 32%),#FFFBFD}.wrap{max-width:900px;margin:auto;padding:14px 12px 50px}.back{display:inline-block;margin:0 0 10px;padding:8px 14px;border-radius:999px;background:#f3eafb;color:#65328c;font-weight:800;text-decoration:none}.hero{color:#fff;border-radius:20px;padding:16px 18px;background:linear-gradient(135deg,#5C1B96,#A22FB5 55%,#E0459A)}.hero h1{margin:0;font-size:24px}.hero p{margin:4px 0 0;font-size:14px}.bar{position:sticky;top:0;z-index:5;display:flex;gap:8px;flex-wrap:wrap;padding:10px 0;background:#FFFBFD}.bar button{border:0;border-radius:999px;padding:9px 14px;background:#f3eafb;color:#65328c;font-weight:800;font-size:15px}.bar .n{margin-left:auto;align-self:center;font-weight:800;color:var(--g)}.cols{column-count:2;column-gap:12px}@media(max-width:700px){.cols{column-count:1}}.sec{break-inside:avoid;background:#fff;border:1px solid var(--line);border-left:6px solid var(--g);border-radius:14px;padding:8px 10px;margin:0 0 12px}.sec.p{border-left-color:var(--p)}.sec.trap{border-left-color:#E8A317;background:#FFF8EC}.sec.trap ul{margin:4px 0;padding-left:20px;font-size:15px}.sec.trap li{margin:3px 0}.sec h2{margin:0 0 4px;font-size:18px;color:var(--v)}table{width:100%;border-collapse:collapse;font-size:15px}td{padding:6px;border-bottom:1px solid #F0E4F7;vertical-align:top}tr:nth-child(even) td{background:var(--lav)}tr.hy td{background:#FDE3F1}td:first-child{font-weight:700;color:var(--v);width:47%}.ans{display:inline-block;min-width:90%;border-radius:8px;padding:2px 6px;cursor:pointer;background:linear-gradient(135deg,#C9B6E4,#F2B6D6);color:transparent;user-select:none;transition:background .15s}.ans.on{background:transparent;color:var(--ink);padding:2px 0}.ans:not(.on):after{content:"tap";color:#fff;font-size:12px;font-weight:800}.ans:not(.on){font-size:0;min-height:22px}.key{font-size:13px;margin:8px 0 0;color:#6b4c7d}.foot{text-align:center;font-size:12px;color:#8a6b99;margin-top:20px}"""
js="""const A=[...document.querySelectorAll('.ans')],N=document.getElementById('n');function u(){N.textContent=A.filter(a=>a.classList.contains('on')).length+' / '+A.length}A.forEach(a=>a.onclick=()=>{a.classList.toggle('on');u()});document.getElementById('all').onclick=()=>{A.forEach(a=>a.classList.add('on'));u()};document.getElementById('hide').onclick=()=>{A.forEach(a=>a.classList.remove('on'));u();scrollTo(0,0)};u();"""
def pg(fn,title,sub,body,back,backlbl):
    open(fn,'w').write(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(title)}</title><style>{css}</style></head><body><div class="wrap"><a class="back" href="{back}?v={V}">← {backlbl}</a><div class="hero"><h1>{E(title)}</h1><p>{sub}</p></div>{body}<div class="foot">🎀 Bethany · K-State CVM Class of 2030 · 🐾</div></div><script>{js}</script></body></html>')
links=''
for slug,title,who,items in SECS:
    fn=f'systems-lec3-{slug}-terms.html'
    traps='<div class="sec trap"><h2>⚠️ Precision traps</h2><ul>'+''.join(f'<li>{E(t)}</li>' for t in TRAPS[slug])+'</ul></div>'
    body=(f'<div class="key">★ pink row = professor emphasized</div><div class="bar"><button id="hide">🙈 Hide all</button><button id="all">👀 Show all</button><span class="n" id="n"></span></div>'
          f'<div class="sec"><table>{rows(items)}</table></div>{traps}')
    pg(fn,'🫁 '+title,f'{E(who)} · {len(items)} terms · say it, then tap the pink box',body,FS,'Back to Exam 3 Terms')
    links+=f'<a class="lt" href="{fn}?v={V}"><b>{E(title)}</b><span>{E(who)} · {len(items)} terms</span></a>'
total=sum(len(x[3]) for x in SECS)
idx_css='.lt{display:block;text-decoration:none;background:#fff;border:1px solid var(--line);border-left:6px solid var(--p);border-radius:14px;padding:12px 14px;margin:12px 0;color:var(--v)}.lt b{display:block;font-size:18px}.lt span{font-size:14px;color:#6b4c7d}'
open(FS,'w').write(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>🫁 Exam 3 Terms Review</title><style>{css}{idx_css}</style></head><body><div class="wrap"><a class="back" href="{HUB}?v={V}">← Back to Systems Lecture</a><div class="hero"><h1>🫁 Exam 3 · Terms Review</h1><p>One page per lecture · tap to reveal · {total} terms so far</p></div>{links}<div class="foot">🎀 Bethany · K-State CVM Class of 2030 · 🐾</div></div></body></html>')

# Lecture hub: add an Exam 3 (Respiratory) tile at the top (idempotent), keep all old tiles
s=open(HUB).read()
tile=f'<a class="tile" href="{FS}?v={V}"><div class="emoji">🫁</div><h2>Exam 3 · Terms Review</h2><p>One page per lecture · {total} tap-to-reveal terms · LC37–40 so far · Fri 11/6</p></a>'
if FS in s: s=re.sub(r'<a class="tile" href="'+re.escape(FS)+r'\?v=\d+">.*?</a>',tile,s,flags=re.S)
else: s=s.replace('<div class="grid">','<div class="grid">'+tile,1)
s=re.sub(r'(<section class="hero"><h1>[^<]*</h1><p>)[^<]*(</p>)',r'\1Next up: Exam 3 · Respiratory · Fri 11/6, 8 AM · LC37–50 (🫁 tiles) · other tiles = previous exam (10/16)\2',s)
s=re.sub(r'(href="[^"?]+\.html)\?v=\d+"',lambda m:f'{m.group(1)}?v={V}"',s)
open(HUB,'w').write(s)
# cache-bust links into the hub + service worker
for f in ['veterinary-systems.html','fall2026.html','index.html']:
    if os.path.exists(f):
        t=open(f).read(); open(f,'w').write(re.sub(r'(href="(?:veterinary-systems|systems-lecture|fall2026)\.html)\?v=\d+"',lambda m:f'{m.group(1)}?v={V}"',t))
sw=open('sw.js').read(); open('sw.js','w').write(re.sub(r"ksu-study-mate-v(\d+)-\d+",lambda m:f"ksu-study-mate-v{int(m.group(1))+1}-{V}",sw))
print(FS,total,'terms',[len(x[3]) for x in SECS])
