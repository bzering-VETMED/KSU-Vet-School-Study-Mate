# L29 tooth types tap-to-reveal (made by Claude). Source: Bethany's photo of L29 slide 6 (Stromberg 2006 brachydont vs hypsodont).
# Card 2: Bethany's photo of the L29 tooth-section figure (slides 8–12).
# Run from repo root: python3 tools/l29teeth.py /path/to/teeth.jpg /path/to/tooth2.jpg /path/to/L29.pdf
import sys, os; sys.path.insert(0, os.path.dirname(__file__)); import tracer as T
src = sys.argv[1]
SW = '<script>if("serviceWorker"in navigator)navigator.serviceWorker.register("sw.js",{updateViaCache:"none"}).then(r=>r.update()).catch(()=>{})</script>'
whiteout = lambda s: s.min(2) < 250   # plain white background around every label: fill the whole text box (no ghosting)
B = lambda x, y, w, h: (x, y, x + w, y + h)
card = T.raster_card(src, 'l29_teeth', [
    ("Pulp cavity — black: pulp chamber in the crown + root canal in the root", [B(249, 161, 255, 44)]),
    ("Bone", [B(249, 251, 112, 36)]),
    ("Enamel — horizontal lines: hardest tissue, 96% hydroxyapatite, NO collagen, ameloblasts", [B(249, 322, 166, 60)]),
    ("Dentine — swirled: 70% hydroxyapatite, type I collagen, odontoblasts", [B(249, 418, 180, 44)]),
    ("Cementum — fine dots: bone-like, 45% hydroxyapatite, cementoblasts", [B(247, 505, 252, 46)]),
    ("Brachydont — short crown, stops growing after eruption (dog)", [B(105, 1055, 380, 75)]),
    ("Crown", [B(505, 775, 160, 55)]),
    ("Root", [B(505, 920, 120, 55)]),
    ("Hypsodont — long crown that keeps erupting and wears down (horse)", [B(690, 1055, 375, 75)]),
    ("Occlusal surface — contacts the tooth of the opposite jaw", [B(688, 84, 392, 46)]),
    ("~Crown — 'reserve' crown, much of it below the gumline", [B(1130, 484, 184, 46)]),
    ("~Root", [B(1130, 897, 142, 44)]),
    ("", [B(0, 568, 70, 52)]),   # stray "oot" fragment from the cropped slide — erased, not a label
], "L29 slide 6 · Brachydont vs hypsodont", "Name each tissue in the legend by its pattern, then each tooth type and its parts.", scale=1, test=whiteout)
card['labels'] = [dict(l, s=l['n'].split(' — ')[0]) for l in card['labels'] if l['n']]
import cv2; im = cv2.imread(src)          # redo the image: hard white fill beats inpainting on a plain background
for x0, y0, x1, y1 in [B(249,161,255,44),B(249,251,112,36),B(249,322,166,60),B(249,418,180,44),B(247,505,252,46),B(105,1055,380,75),
                       B(505,775,160,55),B(505,920,120,55),B(690,1055,375,75),B(688,84,392,46),B(1128,484,190,46),B(1128,897,146,44),B(0,568,70,52)]:
    im[max(0,y0-3):y1+3, max(0,x0-3):x1+3] = 255
cv2.imwrite('assets/l29_teeth.jpg', im, [cv2.IMWRITE_JPEG_QUALITY, 90])
src2 = sys.argv[2]
L2 = [("Crown — enamel-covered part above the gum", B(957,198,113,40)), ("Neck — at the gingiva, between crown and root", B(958,318,90,38)),
      ("Root — anchored in the dental alveolus", B(958,599,85,38)),
      ("Enamel — covers the crown", B(63,218,132,38)), ("Gingiva — gum; part of the periodontium", B(63,265,132,47)),
      ("Dentin — bulk of the tooth, under enamel and cementum", B(63,346,115,38)),
      ("Pulp cavity — pulp chamber in the crown; nerves, arteries, veins, lymphatics", B(63,413,187,46)),
      ("Root canal — pulp cavity within the root; opens at the apical foramen", B(63,594,184,39)),
      ("Cementum — covers the root; part of the periodontium", B(60,674,192,39)),
      ("Periodontal ligaments — anchor cementum to the alveolar bone", B(63,748,193,90)),
      ("Dental alveolus — bony socket (alveolar bone)", B(61,848,262,39))]
im2 = cv2.imread(src2); H2, W2 = im2.shape[:2]
for _, (x0, y0, x1, y1) in L2: im2[max(0,y0-3):y1+3, max(0,x0-3):x1+3] = 255
cv2.imwrite('assets/l29_tooth2.jpg', im2, [cv2.IMWRITE_JPEG_QUALITY, 90])
card2 = dict(title="L29 slides 8–12 · Parts of a tooth", q="Name each tissue and region of the brachydont tooth: crown → neck → root, then outside → in.",
             img='assets/l29_tooth2.jpg', labels=[dict(n=n, s=n.split(' — ')[0], p=T.pos(b, H2, W2)) for n, b in L2])

# ── Tooth numbering (slides 30–37 of the L29 deck PDF, argv[3]) ──
import subprocess, numpy as np
pdf = sys.argv[3]; TMP = '/tmp/claude-0/l29num'; os.makedirs(TMP, exist_ok=True)
def page(n, dpi=200):
    out = f'{TMP}/p{n}'
    if not os.path.exists(out + '.png'):
        subprocess.run(['pdftoppm', '-r', str(dpi), '-png', '-f', str(n), '-l', str(n), '-singlefile', pdf, out], check=True)
    return cv2.imread(out + '.png')
def table_card(n, out, crop, rows, title, hint):
    """crop/boxes in PDF points; rows = [(name, [boxes])]. Text on white: hard white fill."""
    S = 200 / 72; im = page(n).copy()
    for _, bs in rows:
        for b in bs: im[int((b[1]-2)*S):int((b[3]+2)*S), int((b[0]-2)*S):int((b[2]+2)*S)] = 255
    x0, y0, x1, y1 = [int(v * S) for v in crop]; im = im[y0:y1, x0:x1]; H, W = im.shape[:2]
    cv2.imwrite(f'assets/{out}.jpg', im, [cv2.IMWRITE_JPEG_QUALITY, 90])
    lab = []
    for nm, bs in rows:
        u = T.union(bs); b = ((u[0]*S-x0), (u[1]*S-y0), (u[2]*S-x0), (u[3]*S-y0))
        lab.append(dict(n=nm, s=nm.split(' — ')[0], p=T.pos(b, H, W)))
    return dict(title=title, q=hint, img=f'assets/{out}.jpg', labels=lab)
def quad_card(n, out, crop, names, title, hint):
    """Red numbers on a photo: find them by color, inpaint, label by quadrant (TL, TR, BL, BR)."""
    S = 200 / 72; im = page(n).copy(); x0, y0, x1, y1 = [int(v * S) for v in crop]; im = im[y0:y1, x0:x1]
    c = im.astype(int); m = ((c[..., 2] > 170) & (c[..., 1] < 90) & (c[..., 0] < 90)).astype(np.uint8) * 255
    m = cv2.dilate(m, np.ones((5, 5), np.uint8), iterations=3)
    k, lab_im, st, cen = cv2.connectedComponentsWithStats(m)
    big = [i for i in range(1, k) if st[i, 4] > 1500]
    im = cv2.inpaint(im, m, 9, cv2.INPAINT_TELEA); H, W = im.shape[:2]
    cv2.imwrite(f'assets/{out}.jpg', im, [cv2.IMWRITE_JPEG_QUALITY, 88])
    # merge components per quadrant
    q = {}
    for i in big:
        cx, cy = cen[i]; key = (cy > H / 2, cx > W / 2); q.setdefault(key, []).append((cx, cy))
    order = [(False, False), (False, True), (True, True), (True, False)]   # TL, TR, BR, BL = clockwise
    lab = []
    for key, nm in zip(order, names):
        pts = q.get(key, [(W * (0.25 + 0.5 * key[1]), H * (0.25 + 0.5 * key[0]))])
        cx = sum(p[0] for p in pts) / len(pts); cy = sum(p[1] for p in pts) / len(pts)
        lab.append(dict(n=nm, s=nm.split(' — ')[0], p=[round(cx / W * 100, 2), round(cy / H * 100, 2)]))
    return dict(title=title, q=hint, img=f'assets/{out}.jpg', labels=lab), len(big)

TEETH = ['I1', 'I2', 'I3', 'C', 'P1', 'P2', 'P3', 'P4', 'M1', 'M2', 'M3']
QN = {1: 'right upper', 2: 'left upper', 3: 'left lower', 4: 'right lower', 5: 'right upper', 6: 'left upper', 7: 'left lower', 8: 'right lower'}
def cells(q, y0, y1, xs, w, teeth, missing=None):
    """One label per cell: badge = the number, list text says which tooth."""
    out = []
    for x, t in zip(xs, teeth):
        if t == missing: out.append((f"MISSING — {QN[q]} {t} (no deciduous P1)", [(x, y0, x + w, y1)])); continue
        num = q * 100 + TEETH.index(t) + 1
        out.append((f"{num} — {QN[q]} {t}", [(x, y0, x + w, y1)]))
    return out
num_cards = []
c, nb = quad_card(30, 'l29_triadan_quads', (125, 100, 606, 400), [
    "100 — patient's RIGHT upper (on YOUR left)", "200 — LEFT upper", "300 — LEFT lower", "400 — RIGHT lower"],
    "Slide 30 · Triadan quadrants (permanent)", "Facing the patient: R is on your left. Name each quadrant number, going clockwise from the patient's right upper.")
num_cards.append(c)
X32 = [219, 262, 306, 350, 394, 438, 482, 526, 569, 613, 657]
rows32 = []
for q, (y0, y1) in zip([1, 2, 3, 4], [(156, 176), (207, 227), (257, 277), (308, 328)]):
    rows32 += cells(q, y0, y1, X32[:10] if q < 3 else X32, 28, TEETH[:10] if q < 3 else TEETH)
    if q < 3: rows32.append((f"– — no upper M3 ({QN[q]})", [(668, y0, 674, y1)]))
num_cards.append(table_card(32, 'l29_triadan_perm', (82, 112, 705, 357), rows32,
    "Slide 32 · Triadan numbers, adult dog", "Fill the table cell by cell: quadrant digit + tooth position (I1 = 01 … C = 04 … P4 = 08, M1 = 09). Tap Show all to check a whole row."))
c, nb2 = quad_card(34, 'l29_triadan_dquads', (125, 100, 606, 400), [
    "500 — deciduous RIGHT upper", "600 — deciduous LEFT upper", "700 — deciduous LEFT lower", "800 — deciduous RIGHT lower"],
    "Slide 34 · Triadan quadrants (deciduous)", "Same layout as 100–400. What are the deciduous quadrant numbers?")
num_cards.append(c)
X35 = [257, 312, 368, 424, 473, 547, 604, 658]
rows35 = []
for q, (y0, y1) in zip([5, 6, 7, 8], [(149, 169), (200, 220), (251, 271), (302, 322)]):
    xs = X35[:4] + [473] + X35[5:]
    for x, t in zip(xs, TEETH[:8]):
        if t == 'P1': rows35.append((f"Missing — {QN[q]} P1 (dog has no deciduous P1)", [(473, y0, 525, y1 - 3)]))
        else: rows35.append((f"{q * 100 + TEETH.index(t) + 1} — deciduous {QN[q]} {t}", [(x, y0, x + 28, y1)]))
num_cards.append(table_card(35, 'l29_triadan_decid', (88, 105, 700, 340), rows35,
    "Slide 35 · Triadan numbers, deciduous dog", "Fill the table. Which position is missing in every quadrant, and why does it stop at 08?"))
X36 = [390, 423, 452, 477, 501, 531, 560, 587, 619, 652, 684]
U = ['1', '1', '1', '1', '1', '2', '2', '3', '3', '3', '–']; L = ['1', '1', '1', '1', '1', '2', '2', '2', '2', '2', '1']
rows36 = [(f"{u} — upper {t}" + (" (three-rooted)" if u == '3' else "") if u != '–' else "– — no upper M3", [(x, 50, x + 7, 63)]) for x, t, u in zip(X36, TEETH, U)]
rows36 += [(f"{l} — lower {t}", [(x, 74, x + 7, 88)]) for x, t, l in zip(X36, TEETH, L)]
num_cards.append(table_card(36, 'l29_roots', (288, 20, 702, 93), rows36,
    "Slide 36 · Roots of teeth (dog)", "Root count per tooth, upper row then lower. Which three teeth have three roots?"))
print('quad red components:', nb, nb2)

texts = [("Brachydont vs hypsodont (slides 6–7)", ["Brachydont = short crown, distinct crown/neck/root, does NOT grow after eruption (dog)",
            "Hypsodont = long crown, continues erupting, occlusal surface wears (horse)"]),
         ("Hard tissues, hardest → softest (slides 8–10)", ["Enamel 96% hydroxyapatite, no collagen, ameloblasts",
            "Dentine 70%, type I collagen, odontoblasts", "Cementum 45%, type I collagen, cementoblasts"]),
         ("Dental formulae, DOG (slides 26, 28)", ["Deciduous: 2 × (Di3 Dc1 Dp3 / Di3 Dc1 Dp3) = 28 — Dp1 missing, no molars",
            "Adult: 2 × (i3 c1 p4 m2 / i3 c1 p4 m3) = 42 — upper M3 missing",
            "Carnassials: deciduous Dp3/ + Dp/4 · adult p4/ (upper P4) + m/1 (lower M1)"]),
         ("Dental formulae, CAT (slide 29)", ["Deciduous: 2 × (Di3 Dc1 Dp3 / Di3 Dc1 Dp2) = 26 — Dp1/ and Dp/1, Dp/2 missing, no molars",
            "Adult: 2 × (i3 c1 p3 m1 / i3 c1 p2 m1) = 30 — p1/ and p/1, p/2 missing",
            "Carnassials: deciduous Dp3/ + Dp/4 · adult p3/ + m/1"]),
         ("Notation (slides 26–29)", ["Slash AFTER the number = UPPER (p4/) · slash BEFORE = LOWER (m/1)",
            "Capital D = deciduous (Di, Dc, Dp) · lowercase = permanent (i, c, p, m)",
            "Diphyodont = two sets: deciduous complete by 20 days after birth, permanent by 6 months (slide 26)"]),
         ("Triadan rules (slides 30–35)", ["1st digit = quadrant: 1 right upper → 2 left upper → 3 left lower → 4 right lower (clockwise); 5–8 = deciduous",
            "Last 2 digits = position from midline: I1 01, I2 02, I3 03, C 04, P1 05 … P4 08, M1 09, M2 10, M3 11",
            "Canines always end in 04 (Hal's fractured lower right canine = 404); dog carnassials = 108/208 (upper P4) + 309/409 (lower M1)"]),
         ("Eruption times (slide 37) — NOT tested except adult canines by 5–6 months", ["DOG deciduous: incisors 3–4 wk, canines 3–4 wk, premolars 3–5 wk",
            "DOG permanent: incisors 4 mo, canines 5–6 mo, premolars 5–7 mo, molars 5–7 mo",
            "CAT deciduous: incisors 2–3 wk, canines 3–4 wk, premolars 3–6 wk",
            "CAT permanent: incisors 3.5 mo, canines 4–5 mo, premolars 4–6 mo, molars 4–6 mo"])]
T.write('gross-anatomy-l29-teeth.html', '🦷 L29 Teeth · Tap to Reveal', 'Your lecture photos (slides 6, 8–12) + tooth numbering (slides 30–37) · labels pop up in order', [card, card2] + num_cards, texts, back='gross-anatomy-exam4.html')
p = 'gross-anatomy-l29-teeth.html'; s = open(p).read(); open(p, 'w').write(s.replace('← Back to Lecture', '← Back to Exam 4').replace('</body>', SW + '</body>', 1))
print(len(card['labels']), len(card2['labels']), 'labels')
