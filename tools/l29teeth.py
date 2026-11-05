# L29 tooth types tap-to-reveal (made by Claude). Source: Bethany's photo of L29 slide 6 (Stromberg 2006 brachydont vs hypsodont).
# Card 2: Bethany's photo of the L29 tooth-section figure (slides 8–12).
# Run from repo root: python3 tools/l29teeth.py /path/to/teeth.jpg /path/to/tooth2.jpg
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
texts = [("Brachydont vs hypsodont (slides 6–7)", ["Brachydont = short crown, distinct crown/neck/root, does NOT grow after eruption (dog)",
            "Hypsodont = long crown, continues erupting, occlusal surface wears (horse)"]),
         ("Hard tissues, hardest → softest (slides 8–10)", ["Enamel 96% hydroxyapatite, no collagen, ameloblasts",
            "Dentine 70%, type I collagen, odontoblasts", "Cementum 45%, type I collagen, cementoblasts"])]
T.write('gross-anatomy-l29-teeth.html', '🦷 L29 Tooth Types · Tap to Reveal', 'Your photos from lecture 11/5 (slides 6 + 8–12) · labels pop up in order', [card, card2], texts, back='gross-anatomy-exam4.html')
p = 'gross-anatomy-l29-teeth.html'; s = open(p).read(); open(p, 'w').write(s.replace('← Back to Lecture', '← Back to Exam 4').replace('</body>', SW + '</body>', 1))
print(len(card['labels']), len(card2['labels']), 'labels')
