# L29 tooth types tap-to-reveal (made by Claude). Source: Bethany's photo of L29 slide 6 (Stromberg 2006 brachydont vs hypsodont).
# Run from repo root: python3 tools/l29teeth.py /path/to/teeth.jpg
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
texts = [("Brachydont vs hypsodont (slides 6–7)", ["Brachydont = short crown, distinct crown/neck/root, does NOT grow after eruption (dog)",
            "Hypsodont = long crown, continues erupting, occlusal surface wears (horse)"]),
         ("Hard tissues, hardest → softest (slides 8–10)", ["Enamel 96% hydroxyapatite, no collagen, ameloblasts",
            "Dentine 70%, type I collagen, odontoblasts", "Cementum 45%, type I collagen, cementoblasts"])]
T.write('gross-anatomy-l29-teeth.html', '🦷 L29 Tooth Types · Tap to Reveal', 'Slide 6 (your photo from lecture 11/5) · labels pop up in order', [card], texts, back='gross-anatomy-exam4.html')
p = 'gross-anatomy-l29-teeth.html'; s = open(p).read(); open(p, 'w').write(s.replace('← Back to Lecture', '← Back to Exam 4').replace('</body>', SW + '</body>', 1))
print(len(card['labels']), 'labels')
