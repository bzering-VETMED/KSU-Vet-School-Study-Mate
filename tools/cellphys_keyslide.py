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

def build_keyslide(HUB, V):
    cs = [plain_card('The big rule for the whole table', 'say it before you tap', [
            ('⬇️ Insulin turns on…?', '<b>Protein phosphatases</b> → DEphosphorylation → <b>storage</b> pathways ON'),
            ('⬇️ Glucagon / epinephrine turn on…?', '<b>Protein kinase A</b> → PHOSPHORYLATION → <b>use / release</b> pathways ON'),
            ('⬇️ Which column is filled only for the 2 glucose rows?', '<b>Activated by</b> — fructose-2,6-bisphosphate (the 4 glycogen + fat rows are blank)')])]
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
    return ('<div style="grid-column:1/-1;font-weight:900;color:#d94f7f;margin-top:8px">⭐ The slide he said to know for Friday</div>'
            f'<a class="tile" href="{FN}?v={V}" style="border:3px solid #d94f7f"><div class="emoji">⭐</div><h2>Regulatory table · LC23</h2><p>6 processes × enzyme / activator / regulation / hormone · group drills · traps · {len(cs)} cards</p></a>')
