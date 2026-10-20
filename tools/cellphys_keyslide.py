# Cell Physiology Exam 3 · LC23 "Important Regulatory Pathways for Metabolism" table — the slide Dr. Basil said
# "know everything on this and you'll be good for Friday." Tap-reveal, one cell per tap. Called by tools/cellphys.py.
import html, re
import deck
from cellphys_pathways import _copyjs
E = html.escape
FN = 'cellphys-keyslide.html'
IMG = 'assets/cellphys_lc23_regtable.jpg'
INS = 'Insulin → protein phosphatases'
GLU = 'Glucagon / epinephrine → protein kinase A'
F26 = 'phosphofructokinase-2 / fructose-2,6-bisphosphatase'
# (process, main enzyme, activated by, regulated by, hormone pathway, why/clue)
ROWS = [
 ('Glycolysis', 'Phosphofructokinase-1', 'Fructose-2,6-bisphosphate — allosteric activation',
  f'{F26} — DEphosphorylation', INS, 'Dephosphorylated bifunctional enzyme = kinase side ON → makes fructose-2,6-bisphosphate → turns phosphofructokinase-1 ON'),
 ('Gluconeogenesis', 'Fructose-1,6-bisphosphatase', 'RELEASE of fructose-2,6-bisphosphate allosteric inhibition',
  f'{F26} — PHOSPHORYLATION', GLU, 'Phosphorylated = phosphatase side ON → fructose-2,6-bisphosphate falls → brake comes off fructose-1,6-bisphosphatase'),
 ('Glycogenesis', 'Glycogen synthase', 'Blank on the slide',
  'Glycogen synthase — DEphosphorylation', INS, 'Storage enzyme → ON when dephosphorylated'),
 ('Glycogenolysis', 'Glycogen phosphorylase', 'Blank on the slide',
  'Glycogen phosphorylase — PHOSPHORYLATION', GLU, 'Use enzyme → ON when phosphorylated'),
 ('Lipogenesis', 'Acetyl-CoA carboxylase', 'Blank on the slide',
  'Acetyl-CoA carboxylase — DEphosphorylation', INS, 'Storage enzyme → ON when dephosphorylated'),
 ('Lipolysis', 'Hormone-sensitive lipase', 'Blank on the slide',
  'Hormone-sensitive lipase — PHOSPHORYLATION', GLU, 'Use enzyme → ON when phosphorylated'),
]

def row_card(p, enz, act, reg, hor, why):
    S = deck.stg('⬇️ Main enzyme?', f'<b>{E(enz)}</b>')
    S += deck.stg('⬇️ Activated by?', E(act))
    S += deck.stg('⬇️ Regulated by?', f'<b>{E(reg)}</b>')
    S += deck.stg('⬇️ Hormone pathway?', f'<b>{E(hor)}</b>')
    S += deck.stg('💡 Why', E(why))
    return (f'<section class="card"><div class="q textq"><div>Process: <b>{E(p)}</b><span class="tagline">LC23 · regulatory table · say all 4 cells out loud, then tap</span></div></div>{S}'
            f'<div class="rev">💗 TAP TO REVEAL</div></section>')

def plain_card(q, tag, items):
    S = ''.join(deck.stg(pr, an) for pr, an in items)
    return (f'<section class="card"><div class="q textq"><div>{q}<span class="tagline">{E(tag)}</span></div></div>{S}'
            f'<div class="rev">💗 TAP TO REVEAL</div></section>')

MAP_FN = 'cellphys-keymap.html'
MAP_IMG = 'assets/cellphys_lc23_overview.jpg'
# (arrow prompt, what it is, regulating enzyme / key point, hormone or note)
ARROWS = [
 ('Glucose → glycogen', 'Glycogenesis (store glucose)', '★ Glycogen synthase — ON when DEphosphorylated', 'Insulin → protein phosphatases'),
 ('Glycogen → glucose', 'Glycogenolysis (release glucose)', '★ Glycogen phosphorylase — ON when phosphorylated', 'Glucagon / epinephrine → protein kinase A'),
 ('Glucose → pyruvate (with ATP out)', 'Glycolysis — makes ATP', '★ Phosphofructokinase-1 — activated by fructose-2,6-bisphosphate', 'Insulin → protein phosphatases'),
 ('Pyruvate → glucose (with ATP in)', 'Gluconeogenesis — costs ATP', '★ Fructose-1,6-bisphosphatase — on when fructose-2,6-bisphosphate inhibition is released', 'Glucagon / epinephrine → protein kinase A'),
 ('Triglycerides → glycerol + fatty acids', 'Lipolysis (release fat)', '★ Hormone-sensitive lipase — ON when phosphorylated', 'Glucagon / epinephrine → protein kinase A'),
 ('Acetyl-CoA → fatty acids (with ATP in)', 'Lipid synthesis / lipogenesis', '★ Acetyl-CoA carboxylase — ON when DEphosphorylated; makes malonyl-CoA', 'Insulin → protein phosphatases'),
 ('Fatty acids → acetyl-CoA (NADH + FADH₂ out)', 'Beta-oxidation (burn fat in the mitochondria)', 'Fatty acids get in via the carnitine shuttle (LC20)', 'Runs when hormone-sensitive lipase is releasing fatty acids (glucagon / epinephrine)'),
 ('Glycerol ↔ glycolysis / gluconeogenesis', 'Glycerol enters as glycerol-3-phosphate → dihydroxyacetone phosphate', 'IN to gluconeogenesis = glucose from fat\'s backbone · OUT of glycolysis = the backbone for storing triglycerides', 'LC20: glycerol skips the energy-consuming steps'),
 ('Acetyl-CoA → ketone bodies', 'Ketogenesis — in the liver', 'Driven by heavy beta-oxidation (late fasting / starvation, cow ketosis)', 'Liver can\'t use ketones (lacks 3-oxoacid CoA transferase); the brain shifts to them in starvation'),
 ('Acetyl-CoA ↔ acetyl-CoA (TCA side ↔ lipid side)', 'Same molecule, two compartments', 'Acetyl-CoA leaves the mitochondria as citrate (citrate shuttle) for fat synthesis', 'Fat → acetyl-CoA can NOT go back up to pyruvate / glucose'),
 ('Pyruvate → acetyl-CoA → TCA cycle', 'TCA (tricarboxylic acid) cycle oxidizes it', 'Outputs: CO₂ + NADH + FADH₂', '💭 No regulatory enzyme on his chart for this arrow'),
 ('NADH + FADH₂ + O₂ → ETS', 'ETS = electron transport system', 'Outputs: ATP + H₂O (oxygen is the final electron acceptor)', 'This is where most of the ATP comes from'),
 ('Proteins → amino acids', 'Protein breakdown (muscle in fasting/starvation)', 'Insulin builds protein mainly by INHIBITING breakdown', 'Glucagon / cortisol state → more breakdown'),
 ('Amino acids → pyruvate / acetyl-CoA / TCA cycle', 'Carbon skeletons after transamination', 'Glucogenic → pyruvate / TCA intermediates · Ketogenic → acetyl-CoA', 'Glucogenic carbons feed gluconeogenesis'),
 ('Amino acids → NH₄⁺ → urea cycle (ornithine) → urea', 'Nitrogen disposal — liver', 'Urea cycle (carbamoyl phosphate; N-acetylglutamate = activator)', 'Liver shunt / failure → ammonia builds → hepatic encephalopathy'),
 ('Amino acids → proteins (RNA)', 'Translation', 'RNA template → protein', '💭 Mechanism, not a regulated arrow'),
 ('DNA → RNA · DNA → DNA', 'Transcription · Replication', 'LC13 content (not on this exam)', '💭 Context only'),
 ('Glycolysis line → DNA', 'Glucose carbon → nucleotide building blocks', '⚠️ Not named in your slides or today\'s transcript', 'Outside knowledge: pentose phosphate pathway → ribose-5-phosphate. Confirm before using it on a card'),
]

def build_map(HUB, V):
    cs = [plain_card(f'Arrow: <b>{E(a)}</b>', 'say the process + enzyme + hormone, then tap', [
            ('⬇️ What is it?', f'<b>{E(w)}</b>'), ('⬇️ Enzyme / key point?', E(k)), ('⬇️ Hormone / note?', E(h))]) for a, w, k, h in ARROWS]
    cs.insert(0, plain_card('Before you start: draw the map cold', 'blank page, 3 minutes', [
        ('⬇️ The 4 regions?', 'Left: proteins / amino acids / urea cycle · Center: glucose ↔ pyruvate, TCA cycle · Right: triglycerides, fatty acids, beta-oxidation / lipid synthesis · Bottom: ETS'),
        ('⬇️ The 3 "vicious cycles" he named?', 'Glycolysis ↔ gluconeogenesis · glycogenesis ↔ glycogenolysis · lipogenesis ↔ lipolysis'),
        ('⬇️ The hub molecule everything funnels into?', '<b>Acetyl-CoA</b>')]))
    cs.append(plain_card('Final check: the slide itself', 'compare your drawing', [
        ('🖼️ Show the slide', f'<img src="{MAP_IMG}" loading="lazy" style="width:100%;border-radius:12px">')]))
    cs[0] = cs[0].replace('class="card"', 'class="card on"', 1)
    out = deck.page('⭐ Know-this slide · Overview map', 'LC23 · "be able to tell me something about each of these arrows and what enzymes regulate those arrows" · one arrow per card', ''.join(cs), back=HUB)
    out = re.sub(r'← Back to [^<]+', '← Back to Cell Physiology', out, count=1).replace('</body>', _copyjs() + '</body>')
    open(MAP_FN, 'w').write(out)
    print('keymap', len(cs), 'cards')
    return (f'<a class="tile" href="{MAP_FN}?v={V}" style="border:3px solid #d94f7f"><div class="emoji">🗺️</div><h2>Overview map · LC23</h2><p>Every arrow → process + enzyme + hormone · {len(cs)} cards</p></a>')

TAB_FN = 'cellphys-keytable.html'
TCSS = """*{box-sizing:border-box}body{margin:0;background:#fdfbf8;color:#2e2438;font-family:system-ui,-apple-system,'Nunito',sans-serif}
.wrap{max-width:1100px;margin:0 auto;padding:16px}a.back{display:inline-block;background:#ede4f7;color:#512888;font-weight:800;padding:8px 14px;border-radius:999px;text-decoration:none}
.hero{background:linear-gradient(135deg,#3b1d66,#512888,#6b3aa0);color:#fff;border-radius:18px;padding:16px 18px;margin:12px 0;border-bottom:6px solid #d94f7f}
.hero h1{margin:0 0 4px;font-size:1.35rem}.hero p{margin:0;opacity:.9;font-size:.9rem}
.bar{display:flex;flex-wrap:wrap;gap:8px;margin:10px 0}.bar button{border:0;background:#ede4f7;color:#512888;font-weight:800;padding:9px 14px;border-radius:999px;font-size:.9rem}.bar button.hot{background:#d94f7f;color:#fff}
.tw{overflow-x:auto;border-radius:14px;border:1px solid #c9b6e4}table{border-collapse:collapse;width:100%;min-width:760px;background:#fff}
th{background:#512888;color:#fff;text-align:left;padding:10px;font-size:.9rem}td{padding:10px;border-top:1px solid #ede4f7;vertical-align:top;font-size:.92rem}
tr.use td:first-child{border-left:5px solid #d94f7f}tr.store td:first-child{border-left:5px solid #4fbf95}td.p{font-weight:900}
td.c{cursor:pointer}td.c .a{display:none}td.c .h{display:inline-block;background:#fbe7ef;color:#d94f7f;font-weight:800;border-radius:999px;padding:4px 10px;font-size:.8rem}
td.c.on .a{display:inline}td.c.on .h{display:none}td.blank{color:#9a8fa6;font-style:italic}
.key{font-size:.85rem;margin:10px 2px;color:#5c5068}.rule{background:#fbe7ef;border-radius:14px;padding:12px 14px;margin:12px 0;font-weight:700}
img{width:100%;border-radius:14px;margin-top:8px;border:1px solid #c9b6e4}details{margin:14px 0}summary{font-weight:900;color:#512888;cursor:pointer}"""
TJS = """document.querySelectorAll('td.c').forEach(c=>c.onclick=()=>c.classList.toggle('on'));
const all=(on)=>document.querySelectorAll('td.c').forEach(c=>c.classList.toggle('on',on));
document.getElementById('ra').onclick=()=>all(true);document.getElementById('ha').onclick=()=>all(false);
document.querySelectorAll('[data-col]').forEach(b=>b.onclick=()=>document.querySelectorAll('td.c[data-k="'+b.dataset.col+'"]').forEach(c=>c.classList.add('on')));"""

def build_table(HUB, V):
    cols = [('enz','Main enzyme'),('act','Activated by'),('reg','Regulated by'),('hor','Hormone pathway')]
    rows = ''
    for p, enz, act, reg, hor, why in ROWS:
        cls = 'store' if hor == INS else 'use'
        cells = ''
        for k, val in zip([c for c,_ in cols], [enz, act, reg, hor]):
            if val == 'Blank on the slide':
                cells += '<td class="blank">— blank on slide</td>'
            else:
                cells += f'<td class="c" data-k="{k}"><span class="h">tap</span><span class="a">{E(val)}</span></td>'
        rows += f'<tr class="{cls}"><td class="p">{E(p)}</td>{cells}</tr>'
    head = '<tr><th>Process</th>' + ''.join(f'<th>{E(n)}</th>' for _, n in cols) + '</tr>'
    colbtn = ''.join(f'<button data-col="{k}">Show {E(n)}</button>' for k, n in cols)
    out = (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
           f'<title>Regulatory table · LC23</title><style>{TCSS}</style></head><body><div class="wrap">'
           f'<a class="back" href="{HUB}?v={V}">← Back to Cell Physiology</a>'
           '<div class="hero"><h1>⭐ Regulatory table · table view</h1><p>LC23 · Dr. Basil\'s slide, same layout · say each cell out loud, then tap it</p></div>'
           '<div class="bar"><button class="hot" id="ra">Reveal all</button><button id="ha">Hide all</button>' + colbtn + '</div>'
           f'<div class="tw"><table>{head}{rows}</table></div>'
           '<div class="key">🟢 green edge = insulin → protein phosphatases (store) · 🩷 pink edge = glucagon / epinephrine → protein kinase A (release)</div>'
           '<div class="rule">Insulin stores (dephosphorylate). Glucagon releases (phosphorylate). Only glycolysis + gluconeogenesis have the "Activated by" middle step (fructose-2,6-bisphosphate).</div>'
           f'<details><summary>🖼️ The original slide</summary><img src="{IMG}" alt="LC23 regulatory table slide"></details>'
           f'<details><summary>🗺️ The overview map slide</summary><img src="{MAP_IMG}" alt="LC23 overview of metabolism slide"></details>'
           f'</div><script>{TJS}</script></body></html>')
    open(TAB_FN, 'w').write(out)
    print('keytable ok')
    return f'<a class="tile" href="{TAB_FN}?v={V}" style="border:3px solid #d94f7f"><div class="emoji">📋</div><h2>Regulatory table · table view</h2><p>The slide as a table · tap any cell · reveal by column · original slides included</p></a>'

def build_keyslide(HUB, V):
    cs = [plain_card('The big rule for the whole table', 'say it before you tap', [
            ('⬇️ Insulin turns on…?', '<b>Protein phosphatases</b> → DEphosphorylation → <b>storage</b> pathways ON'),
            ('⬇️ Glucagon / epinephrine turn on…?', '<b>Protein kinase A</b> → PHOSPHORYLATION → <b>use / release</b> pathways ON'),
            ('⬇️ On the slide, the "Activated by" column is blank for 4 rows. Which 2 rows have it filled in, and with what?', '<b>Glycolysis + gluconeogenesis</b> — fructose-2,6-bisphosphate (the "weird middle step"). The 4 glycogen + fat enzymes are switched directly by phosphorylation, so their cells are blank.')])]
    cs += [row_card(*r) for r in ROWS]
    cs += [plain_card('Group drill: name ALL members at once', 'name the whole group, then tap', [
            ('⬇️ The 3 insulin → protein phosphatase processes + enzymes?', '<b>Glycolysis</b> (phosphofructokinase-1) · <b>Glycogenesis</b> (glycogen synthase) · <b>Lipogenesis</b> (acetyl-CoA carboxylase)'),
            ('⬇️ The 3 glucagon / epinephrine → protein kinase A processes + enzymes?', '<b>Gluconeogenesis</b> (fructose-1,6-bisphosphatase) · <b>Glycogenolysis</b> (glycogen phosphorylase) · <b>Lipolysis</b> (hormone-sensitive lipase)'),
            ('⬇️ The 3 enzymes turned ON by PHOSPHORYLATION?', 'Glycogen phosphorylase · hormone-sensitive lipase · (the phosphatase side of) phosphofructokinase-2 / fructose-2,6-bisphosphatase'),
            ('⬇️ The 3 enzymes turned ON by DEphosphorylation?', 'Glycogen synthase · acetyl-CoA carboxylase · (the kinase side of) phosphofructokinase-2 / fructose-2,6-bisphosphatase')]),
           plain_card('Reverse: enzyme → process', 'name the process + hormone', [
            ('⬇️ Hormone-sensitive lipase?', 'Lipolysis · glucagon / epinephrine → protein kinase A'),
            ('⬇️ Acetyl-CoA carboxylase?', 'Lipogenesis · insulin → protein phosphatases'),
            ('⬇️ Fructose-1,6-bisphosphatase?', 'Gluconeogenesis · glucagon / epinephrine → protein kinase A'),
            ('⬇️ Glycogen synthase?', 'Glycogenesis · insulin → protein phosphatases'),
            ('⬇️ Phosphofructokinase-1?', 'Glycolysis · insulin → protein phosphatases'),
            ('⬇️ Glycogen phosphorylase?', 'Glycogenolysis · glucagon / epinephrine → protein kinase A')]),
           plain_card('⚠️ Precision traps', 'say the right half of each pair', [
            ('⬇️ Phosphofructokinase-1 vs phosphofructokinase-2?', '<b>-1</b> = the glycolysis enzyme on the table · <b>-2</b> = the regulator that makes fructose-2,6-bisphosphate'),
            ('⬇️ Fructose-1,6-bisphosphatase vs fructose-2,6-bisphosphatase?', '<b>1,6</b> = gluconeogenesis enzyme · <b>2,6</b> = phosphatase half of the bifunctional regulator'),
            ('⬇️ Gluconeogenesis "activated by"?', 'RELEASE of fructose-2,6-bisphosphate <b>inhibition</b> — not activation by it'),
            ('⬇️ Low fructose-2,6-bisphosphate means…?', '<b>Gluconeogenesis</b> ON, glycolysis OFF (your repeat flip)'),
            ('⬇️ Phosphorylated phosphofructokinase-2 / fructose-2,6-bisphosphatase?', 'Glucagon state → phosphatase side ON → fructose-2,6-bisphosphate DOWN'),
            ('⬇️ Off the slide (earlier lectures, 💭)', 'Allosteric: glucose-6-phosphate → glycogen synthase · citrate → acetyl-CoA carboxylase')]),
           plain_card('Final check: the slide itself', 'rebuild the whole table on paper first', [
            ('🖼️ Show the slide', f'<img src="{IMG}" loading="lazy" style="width:100%;border-radius:12px">')])]
    cs[0] = cs[0].replace('class="card"', 'class="card on"', 1)
    out = deck.page('⭐ Know-this slide · Regulatory table', 'LC23 · Dr. Basil: "know everything on this slide and you\'ll be good Friday" · one cell per tap', ''.join(cs), back=HUB)
    out = re.sub(r'← Back to [^<]+', '← Back to Cell Physiology', out, count=1).replace('</body>', _copyjs() + '</body>')
    open(FN, 'w').write(out)
    print('keyslide', len(cs), 'cards')
    return ('<div style="grid-column:1/-1;font-weight:900;color:#d94f7f;margin-top:8px">⭐ The 2 slides he said to know for Friday</div>' + build_table(HUB, V) + build_map(HUB, V) +
            f'<a class="tile" href="{FN}?v={V}" style="border:3px solid #d94f7f"><div class="emoji">⭐</div><h2>Regulatory table · LC23</h2><p>6 processes × enzyme / activator / regulation / hormone · group drills · traps · {len(cs)} cards</p></a>')
