# L30 extrinsic eye muscles tap-to-reveal (made by Claude). Sources: Bethany's photos of L30 slide 41 (cat faces, muscle actions)
# and slide 42 (innervation, LR6 Do4 Rest3). Professor said this WILL be tested (lecture 11/9).
# Run from repo root: python3 tools/l30eyemuscles.py /path/to/cats.jpg /path/to/innerv.jpg
import sys, os, cv2, numpy as np; sys.path.insert(0, os.path.dirname(__file__)); import tracer as T
SW = '<script>if("serviceWorker"in navigator)navigator.serviceWorker.register("sw.js",{updateViaCache:"none"}).then(r=>r.update()).catch(()=>{})</script>'

def hide(src, out, boxes):
    im = cv2.imread(src); H, W = im.shape[:2]; mask = np.zeros((H, W), np.uint8)
    for x0, y0, x1, y1 in boxes:
        r = im[y0:y1, x0:x1].astype(int); m = ((r.min(2) < 120) | ((r.max(2) - r.min(2)) > 90)).astype(np.uint8) * 255
        mask[y0:y1, x0:x1] |= m
    mask = cv2.dilate(mask, np.ones((9, 9), np.uint8))
    im = cv2.inpaint(im, mask, 5, cv2.INPAINT_TELEA)
    cv2.imwrite(f'assets/{out}.jpg', im, [cv2.IMWRITE_JPEG_QUALITY, 90]); return H, W

P = lambda b: (b[0] - 6, b[1] - 6, b[2] + 6, b[3] + 6)
C = [("Lateral rectus — pulls eye LATERALLY · CN VI abducens (red)", (844, 260, 1049, 410)),
     ("Ventral rectus — pulls eye VENTRALLY · CN III oculomotor", (1751, 260, 1970, 401)),
     ("Medial rectus — pulls eye MEDIALLY · CN III oculomotor", (844, 734, 1053, 890)),
     ("Dorsal oblique — rotates top of eye MEDIALLY (intorsion) · CN IV trochlear (blue)", (1751, 734, 1982, 881)),
     ("Dorsal rectus — pulls eye DORSALLY · CN III oculomotor", (844, 1205, 1225, 1282)),
     ("Ventral oblique — rotates top of eye LATERALLY (extorsion) · CN III oculomotor", (1751, 1205, 1982, 1344))]
H, W = hide(sys.argv[1], 'l30_eyecats', [P(b) for _, b in C])
card1 = dict(title="L30 slide 41 · Which muscle moves the eye this way? ★ TESTED",
             q="Look at the cat's LEFT eye (your right) in each face. Name the muscle pulling it there, then its cranial nerve.",
             img='assets/l30_eyecats.jpg', labels=[dict(n=n, s=n.split(' — ')[0], p=T.pos(P(b), H, W)) for n, b in C])
I = [("Lateral rectus — CN VI abducens", (608, 436, 1077, 491)), ("Medial rectus — CN III oculomotor", (608, 538, 1090, 593)),
     ("Dorsal rectus — CN III oculomotor", (605, 640, 1075, 696)), ("Ventral rectus — CN III oculomotor", (604, 742, 1101, 798)),
     ("Dorsal oblique — CN IV trochlear", (605, 1039, 1120, 1107)), ("Ventral oblique — CN III oculomotor", (604, 1141, 1149, 1209)),
     ("Retractor bulbi — CN VI abducens (red on slide)", (497, 1330, 1030, 1385)),
     ("LR6 Do4 Rest3 — Lateral Rectus = 6, Dorsal oblique = 4, the Rest = 3", (1401, 751, 1948, 842))]
im2 = cv2.imread(sys.argv[2]); H2, W2 = im2.shape[:2]   # plain white slide: hard white fill (no ghosting)
for _, (x0, y0, x1, y1) in I: im2[y0 - 8:y1 + 8, x0 - 8:x1 + 8] = 255
cv2.imwrite('assets/l30_eyeinnerv.jpg', im2, [cv2.IMWRITE_JPEG_QUALITY, 90])
card2 = dict(title="L30 slide 42 · Innervation ★ TESTED", q="Name all 7 muscles of the globe in order, each with its cranial nerve. Then the mnemonic.",
             img='assets/l30_eyeinnerv.jpg', labels=[dict(n=n, s=n.split(' — ')[0], p=T.pos(P(b), H2, W2)) for n, b in I])
texts = [("LR6 Do4 Rest3 (slide 42)", ["Lateral rectus + retractor bulbi → CN VI abducens (red)", "Dorsal oblique → CN IV trochlear (blue)",
            "Rest (medial, dorsal, ventral rectus + ventral oblique) → CN III oculomotor"]),
         ("Actions (slide 41)", ["Each rectus pulls the eye toward its own name (lateral → lateral, dorsal → dorsal…)",
            "Dorsal oblique = intorsion (top of eye rolls medially) · ventral oblique = extorsion (top rolls laterally)",
            "Retractor bulbi pulls the globe back into the orbit"])]
T.write('gross-anatomy-l30-eyemuscles.html', '👁️ L30 Eye Muscles · Tap to Reveal', 'Your lecture photos (slides 41–42) · ★ professor said this will be tested', [card1, card2], texts, back='gross-anatomy-exam4.html')
p = 'gross-anatomy-l30-eyemuscles.html'; s = open(p).read(); open(p, 'w').write(s.replace('← Back to Lecture', '← Back to Exam 4').replace('</body>', SW + '</body>', 1))
