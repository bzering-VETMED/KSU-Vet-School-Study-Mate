# Cell Physiology Exam 3 · "Name the key enzymes" decks, one card per pathway (one enzyme per tap).
# Called by tools/cellphys.py (build_enzymes). Same machinery as cellphys_pathways.py (deck.page + deck.stg + COPYJS).
# ★ = must know · 💭 = understanding only.
import html, re
import deck
from cellphys_pathways import _copyjs
E = html.escape
K, U = True, False

# (pathway title, cite, [(must_know, enzyme full name, what it does ≤10 words)])
Z = {
1: ('Glucagon → glucose out of the liver', 'LC18 slides 11–15', [
  (K, 'Protein kinase A', 'activated by cyclic AMP; adds phosphates'),
  (U, 'Adenylyl cyclase', 'converts ATP into cyclic AMP'),
  (U, 'Phosphorylase kinase', 'middle-man; phosphorylates glycogen phosphorylase'),
  (K, 'Glycogen phosphorylase', 'snips glucose-1-phosphate off glycogen; ON when phosphorylated'),
  (K, 'Glycogen debranching enzyme', 'clears branch points so phosphorylase keeps cutting'),
  (U, 'Phosphoglucomutase', 'moves the phosphate from carbon 1 to carbon 6'),
  (K, 'Glucose-6-phosphatase', 'liver only; frees glucose so it can leave')]),
2: ('Insulin → glucose stored as glycogen', 'LC18 slides 5, 9–10, 15', [
  (K, 'Protein phosphatase 1', 'turned on by insulin; removes phosphates'),
  (K, 'Hexokinase / glucokinase', 'traps glucose as glucose-6-phosphate; glucokinase in liver'),
  (U, 'Phosphoglucomutase', 'moves phosphate carbon 6 → 1 (glucose-1-phosphate)'),
  (U, 'UDP-glucose pyrophosphorylase', 'makes UDP-glucose (activated glucose)'),
  (K, 'Glycogen synthase', 'adds glucose to the chain; regulatory step; ON dephosphorylated'),
  (K, 'Glycogen branching enzyme', 'adds the alpha-1,6 branch points')]),
3: ('Glucagon → gluconeogenesis switch', 'LC18 slides 21–26', [
  (K, 'Protein kinase A', 'phosphorylates the two-job enzyme'),
  (K, 'Phosphofructokinase-2 / fructose-2,6-bisphosphatase', 'one enzyme, two halves; phosphorylated → bisphosphatase half on'),
  (K, 'Phosphofructokinase-1', 'glycolysis control step; loses its activator → slows'),
  (K, 'Fructose-1,6-bisphosphatase', 'gluconeogenesis control step; loses its inhibitor → speeds up'),
  (K, 'Pyruvate carboxylase', 'bypass: pyruvate → oxaloacetate'),
  (K, 'Phosphoenolpyruvate carboxykinase', 'bypass: oxaloacetate → phosphoenolpyruvate'),
  (K, 'Glucose-6-phosphatase', 'last bypass; liver only; releases free glucose')]),
4: ('Insulin → glycolysis switch', 'LC18 slides 25–26 · LC16', [
  (K, 'Protein phosphatase 1', 'turned on by insulin; dephosphorylates the two-job enzyme'),
  (K, 'Phosphofructokinase-2 (kinase half)', 'ON → makes fructose-2,6-bisphosphate'),
  (K, 'Phosphofructokinase-1', 'activated by fructose-2,6-bisphosphate → glycolysis on'),
  (K, 'Fructose-1,6-bisphosphatase', 'inhibited by fructose-2,6-bisphosphate → gluconeogenesis off'),
  (K, 'Pyruvate kinase', 'last glycolysis step; feed-forward activated by fructose-1,6-bisphosphate')]),
5: ('Fat burning (lipolysis → beta-oxidation)', 'LC20 slides 7–11', [
  (K, 'Protein kinase A', 'turned on by epinephrine or glucagon; phosphorylates'),
  (K, 'Hormone-sensitive lipase', 'cuts fatty acids off glycerol; ON when phosphorylated'),
  (U, 'Fatty acyl-CoA synthetase', 'activates fatty acid in cytosol; costs 2 ATP'),
  (K, 'Carnitine shuttle', 'carries fatty acyl-CoA into the mitochondria'),
  (U, 'Acyl-CoA dehydrogenase', 'beta-oxidation step 1; makes FADH₂'),
  (U, 'Enoyl-CoA hydratase', 'beta-oxidation step 2; adds water'),
  (U, '3-hydroxyacyl-CoA dehydrogenase', 'beta-oxidation step 3; makes NADH'),
  (U, 'Thiolase', 'beta-oxidation step 4; cuts off acetyl-CoA')]),
6: ('Fat storage (lipogenesis)', 'LC20 slides 5–6, 11', [
  (K, 'Protein phosphatase (2A on slide 11)', 'turned on by insulin; dephosphorylates'),
  (K, 'Acetyl-CoA carboxylase', 'acetyl-CoA → malonyl-CoA; committed, rate-limiting; citrate activates'),
  (U, 'Glycerol-3-phosphate dehydrogenase', 'dihydroxyacetone phosphate → glycerol-3-phosphate (triglyceride backbone)')]),
7: ('Ketogenesis', 'LC20 slides 15–16', [
  (U, 'Thiolase', 'joins 2 acetyl-CoA → acetoacetyl-CoA'),
  (U, 'HMG-CoA synthase', 'adds a third acetyl-CoA → HMG-CoA'),
  (U, 'HMG-CoA lyase', 'splits HMG-CoA → acetoacetate (+ acetyl-CoA)'),
  (U, 'Beta-hydroxybutyrate dehydrogenase', 'acetoacetate ⇄ beta-hydroxybutyrate'),
  (K, '3-oxoacid CoA transferase', 'missing in liver → liver can\'t use ketones')]),
8: ('Low oxygen → lactate', 'LC16 slides 17–21', [
  (K, 'Glyceraldehyde-3-phosphate dehydrogenase', 'glycolysis step 6; needs NAD⁺ to run'),
  (K, 'Lactate dehydrogenase', 'pyruvate → lactate; regenerates NAD⁺'),
  (U, 'Liver gluconeogenesis enzymes', 'Cori cycle turns lactate back into glucose')]),
9: ('Electron transport → ATP', 'LC17 slides 19–23', [
  (K, 'Complex I', 'NADH entry point; pumps protons'),
  (K, 'Complex II (succinate dehydrogenase)', 'succinate/FADH₂ entry; does NOT pump protons'),
  (K, 'Complex III', 'from coenzyme Q to cytochrome c; pumps protons'),
  (K, 'Complex IV', 'hands electrons to oxygen → water; pumps protons'),
  (K, 'ATP synthase', 'protons turn the channel; 10 protons = 3 ATP')]),
10: ('Ischemia → reperfusion', 'LC17 slides 10–13, 26', [
  (K, 'Malate dehydrogenase', 'TCA step 8; runs backward without oxygen'),
  (K, 'Succinate dehydrogenase (complex II)', 'reperfusion surge of succinate → FADH₂ flood')]),
11: ('Amino acid → urea', 'LC19 slides 7, 13–17', [
  (K, 'Transaminases', 'move amine onto alpha-ketoglutarate → glutamate'),
  (U, 'Glutamate deamination', 'releases ammonium (NH₄⁺), regenerates alpha-ketoglutarate'),
  (K, 'Carbamoyl phosphate synthetase', 'urea cycle regulatory step'),
  (K, 'N-acetylglutamate synthetase', 'makes the activator N-acetylglutamate when glutamate is high')]),
12: ('Glucose trapping → glycolysis', 'LC16 slides 8–14', [
  (K, 'Hexokinase', 'low Km; most tissues; inhibited by glucose-6-phosphate'),
  (K, 'Glucokinase', 'high Km (~15 mM); liver + beta cells; not inhibited'),
  (K, 'Phosphofructokinase-1', 'main regulatory, rate-limiting glycolysis step'),
  (K, 'Pyruvate kinase', 'last step; makes ATP; feed-forward activated')]),
13: ('Bicarbonate buffer', 'LC08', [
  (K, 'Carbonic anhydrase', 'carbonic acid ⇄ water + carbon dioxide')]),
14: ('Histamine → vasodilation', 'LC21 "Paracrine Signaling"', [
  (K, 'Guanylyl cyclase', 'target of nitric oxide; makes cyclic GMP → relaxation')]),
}
DECKS = [('cellphys-enz1.html', '🧪 Enzymes · carbs & fats', 'Glycogen · switches · glycolysis start · fat', [1, 2, 3, 4, 12, 5, 6]),
         ('cellphys-enz2.html', '🧪 Enzymes · energy, nitrogen, signaling', 'Ketones · lactate · electron transport · urea · buffers', [7, 8, 9, 10, 11, 13, 14])]

def card(i):
    title, cite, enz = Z[i]
    S = ''.join(deck.stg(f'⬇️ Enzyme {n}?', ('★ ' if mk else '💭 ') + f'<b>{E(nm)}</b> — {E(what)}') for n, (mk, nm, what) in enumerate(enz, 1))
    S += deck.stg('📖 Source', E(cite))
    return (f'<section class="card"><div class="q textq"><div>Name the key enzymes: {E(title)}<span class="tagline">{len(enz)} enzymes · ★ must know · 💭 understanding only</span></div></div>{S}'
            f'<div class="rev">💗 TAP TO REVEAL</div></section>')

def build_enzymes(HUB, V):
    cj = _copyjs(); tiles = []
    for fn, name, sub, ids in DECKS:
        cs = [card(i) for i in ids]; cs[0] = cs[0].replace('class="card"', 'class="card on"', 1)
        out = deck.page(name, f'{len(cs)} pathways · one enzyme per tap · ★ must know · 💭 understanding only', ''.join(cs), back=HUB)
        out = re.sub(r'← Back to [^<]+', '← Back to Cell Physiology', out, count=1).replace('</body>', cj + '</body>')
        open(fn, 'w').write(out)
        tiles.append(f'<a class="tile" href="{fn}?v={V}"><div class="emoji">🧪</div><h2>{E(name.split(" · ", 1)[1].capitalize())} enzymes</h2><p>{E(sub)} · {len(cs)} pathways</p></a>')
    head = '<div style="grid-column:1/-1;font-weight:900;color:#70428f;margin-top:8px">🧪 Enzymes per pathway · tap one enzyme at a time</div>'
    print('enzymes', [(f, len(i)) for f, _, _, i in DECKS])
    return head + ''.join(tiles)
