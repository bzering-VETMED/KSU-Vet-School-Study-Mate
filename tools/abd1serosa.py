# Serosa / omental bursa cross-section tracing deck (made by Claude).
# Run from repo root: python3 tools/abd1serosa.py /path/to/IMG_4543.jpeg /path/to/IMG_4544.jpeg
import cv2, sys, os, numpy as np
sys.path.insert(0, os.path.dirname(__file__)); import tracer as T
a_src, b_src, rs_src = sys.argv[1:4]

def text(s):  # grey/black print on white
    return (s.max(2) < 170) & ((s.max(2) - s.min(2)) < 40)

def card(src, out, labels, title, hint, crop_w):
    im = cv2.imread(src)[:, :crop_w]
    for _, bs in labels:
        for (x0, y0, x1, y1) in bs:
            sub = im[y0:y1, x0:x1]  # labels sit on plain paper: repaint with the paper colour around the box
            im[y0:y1, x0:x1] = np.median(np.concatenate([sub[0], sub[-1], sub[:, 0], sub[:, -1]]), axis=0)
    im = cv2.resize(im, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)
    H, W = im.shape[:2]; cv2.imwrite(f'assets/{out}.jpg', im, [cv2.IMWRITE_JPEG_QUALITY, 90])
    sc = lambda b: tuple(v * 1.5 for v in b)
    return dict(title=title, q=hint, img=f'assets/{out}.jpg',
                labels=[dict(n=n, p=T.pos(sc(T.union(bs)), H, W)) for n, bs in labels])

A = [
    ("Internal fascia of the trunk", [(845, 150, 1125, 232)]),
    ("Stomach", [(893, 315, 1040, 362)]),
    ("Omental bursa (heading for the next 3)", [(62, 326, 216, 406)]),
    ("Visceral serosa", [(0, 402, 214, 446)]),
    ("Caudal omental recess", [(0, 482, 216, 574)]),
    ("Parietal serosa", [(0, 600, 214, 645)]),
    ("Gastrosplenic ligament", [(892, 552, 1112, 660)]),
    ("Liver", [(133, 682, 216, 722)]),
    ("Falciform ligament", [(893, 703, 1050, 797)]),
]
B = [
    ("Internal fascia of the trunk", [(860, 160, 1146, 246)]),
    ("Intermediate serosa", [(0, 242, 210, 326)]),
    ("Spleen", [(933, 310, 1054, 366)]),
    ("Visceral serosa (on the stomach)", [(68, 476, 208, 562)]),
    ("Stomach", [(933, 474, 1084, 519)]),
    ("Parietal serosa", [(76, 595, 208, 680)]),
    ("Visceral serosa (on the liver)", [(68, 712, 208, 797)]),
    ("Liver", [(124, 804, 210, 845)]),
    ("Falciform ligament", [(933, 786, 1095, 880)]),
]
cards = [
    card(b_src, 'abd1_serosa_before', B, "Before rotation · serosa layers",
         "Cross-section, dorsal at top. The arrows show the stomach about to rotate. Name each layer dorsal → ventral.", 1150),
    card(a_src, 'abd1_serosa_after', A, "After rotation · omental bursa forms",
         "Same section after the stomach rotates. Where is the omental bursa, and what ligament ties stomach to spleen?", 1135),
]

# Rectus sheath slide (IMG_4545): hide the layer lists, keep "External/Internal lamina" as the prompts
k = 2306 / 2000
RS = [(n, [tuple(int(v * k) for v in b)]) for n, b in [
    ("Cranial · external lamina: external abdominal oblique + superficial leaf of internal abdominal oblique", (1498, 345, 1915, 400)),
    ("Cranial · internal lamina: deep leaf of internal abdominal oblique + transversus abdominis + transversalis fascia", (1498, 465, 1865, 520)),
    ("Middle · external lamina: external abdominal oblique + internal abdominal oblique", (1498, 625, 1665, 680)),
    ("Middle · internal lamina: transversus abdominis + transversalis fascia", (1498, 750, 1615, 800)),
    ("Caudal · external lamina: external abdominal oblique + internal abdominal oblique + transversus abdominis", (1498, 830, 1730, 880)),
    ("Caudal · internal lamina: transversalis fascia only", (1498, 950, 1560, 1000)),
]]
def rs_card():
    im = cv2.imread(rs_src)
    for _, bs in RS:
        for (x0, y0, x1, y1) in bs:
            sub = im[y0:y1, x0:x1]
            im[y0:y1, x0:x1] = np.median(np.concatenate([sub[0], sub[-1], sub[:, 0], sub[:, -1]]), axis=0)
    X0, Y0 = int(165 * k), int(170 * k); im = im[Y0:int(1140 * k), X0:int(1960 * k)]
    H, W = im.shape[:2]; cv2.imwrite('assets/abd1_rectus_sheath.jpg', im, [cv2.IMWRITE_JPEG_QUALITY, 88])
    sh = lambda b: (b[0] - X0, b[1] - Y0, b[2] - X0, b[3] - Y0)
    return dict(title="Rectus sheath · what forms each lamina?",
                q="Ventral view, cranial at top. For each level, name every layer in the external and internal lamina — spelled out.",
                img='assets/abd1_rectus_sheath.jpg', labels=[dict(n=n, s=f'{i + 1} ✓', p=T.pos(sh(T.union(bs)), H, W)) for i, (n, bs) in enumerate(RS)])
cards.append(rs_card())
T.write('gross-anatomy-abd1-serosa.html', 'Serosa, Omental Bursa & Rectus Sheath',
        'Abdominal Cavity 1 · names hidden · tap to reveal one at a time', cards, [])
print('ok')
