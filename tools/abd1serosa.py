# Serosa / omental bursa cross-section tracing deck (made by Claude).
# Run from repo root: python3 tools/abd1serosa.py /path/to/IMG_4543.jpeg /path/to/IMG_4544.jpeg
import cv2, sys, os, numpy as np
sys.path.insert(0, os.path.dirname(__file__)); import tracer as T
a_src, b_src = sys.argv[1:3]

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
T.write('gross-anatomy-abd1-serosa.html', 'Serosa & Omental Bursa',
        'Abdominal Cavity 1 · cross-sections with names hidden · tap to reveal dorsal → ventral', cards, [])
print('ok')
