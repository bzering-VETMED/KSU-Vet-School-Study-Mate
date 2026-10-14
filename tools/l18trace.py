# Lecture 18 dog-route nerve tracing deck (made by Claude).
# Run from repo root: python3 tools/l18trace.py /path/to/Lecture_18_Nervous_System_2_-_Tagged.pdf
import cv2, sys, os, subprocess, numpy as np
sys.path.insert(0, os.path.dirname(__file__)); import tracer as T
pdf = sys.argv[1]; TMP = '/tmp/claude-0/l18t'; os.makedirs(TMP, exist_ok=True)

def page_png(n):
    out = f'{TMP}/p{n}'
    subprocess.run(['pdftoppm', '-r', '200', '-png', '-f', str(n), '-l', str(n), '-singlefile', pdf, out], check=True)
    return cv2.imread(out + '.png')

def ink(s):  # black/dark text + dark-red text; leaves grey nerves and green lines alone
    r, g, b = s[..., 2].astype(int), s[..., 1].astype(int), s[..., 0].astype(int)
    return (s.max(2) < 95) | ((r > 110) & (g < 100) & (b < 100))

def gray(s):  # grey or black text on white
    return (s.max(2) < 215) & ((s.max(2) - s.min(2)) < 30)

def blank(im, b):  # label on plain white: repaint with border median
    x0, y0, x1, y1 = map(int, b); sub = im[y0:y1, x0:x1]
    im[y0:y1, x0:x1] = np.median(np.concatenate([sub[0], sub[-1], sub[:, 0], sub[:, -1]]), axis=0)

def raster(n, out, labels, title, hint, crop, mode='blank', white=()):
    """labels: [(name, [boxes in 200-dpi page px])]; crop=(x0,y0,x1,y1)."""
    im = page_png(n)
    for w in white: im[w[1]:w[3], w[0]:w[2]] = 255
    boxes = [b for _, bs in labels for b in bs]
    test = gray if mode == 'gray' else ink
    for b in boxes:  # turn only the text strokes (plus a 3-px halo) white: no smudges, lines elsewhere untouched
        x0, y0, x1, y1 = map(int, b); sub = im[y0:y1, x0:x1]
        m = cv2.dilate(test(sub.astype(int)).astype(np.uint8), np.ones((3, 3), np.uint8), iterations=3)
        sub[m > 0] = 255
        c = sub.astype(int); greenish = c[..., 1] > c[..., 2] + 25
        near = cv2.dilate(m, np.ones((3, 3), np.uint8), iterations=4) > 0
        sub[near & (c.min(2) > 165) & ((c.max(2) - c.min(2)) < 40) & ~greenish] = 255  # wipe the faint anti-aliased halo too
    X0, Y0, X1, Y1 = crop; im = im[Y0:Y1, X0:X1]
    H, W = im.shape[:2]; cv2.imwrite(f'assets/{out}.jpg', im, [cv2.IMWRITE_JPEG_QUALITY, 88])
    sh = lambda b: (b[0] - X0, b[1] - Y0, b[2] - X0, b[3] - Y0)
    return dict(title=title, q=hint, img=f'assets/{out}.jpg',
                labels=[dict(n=nm, p=T.pos(sh(T.union(bs)), H, W)) for nm, bs in labels])

cards = []
# Slide 32: body wall / limb route
cards.append(raster(32, 'l18_route_bodywall', [
    ("Ventral root (preganglionic fiber leaves the cord)", [(1075, 718, 1215, 795)]),
    ("Spinal nerve", [(848, 528, 960, 608)]),
    ("Ramus communicans (white → into the trunk)", [(950, 975, 1190, 1042)]),
    ("Sympathetic trunk (synapse in a trunk ganglion)", [(700, 945, 866, 1008)]),
    ("Dorsal branch of another spinal nerve", [(636, 452, 782, 556)]),
    ("Ventral branch of another spinal nerve", [(468, 582, 632, 658)]),
], "Sympathetic route 1 · body wall & limbs",
   "Start at the lateral horn star. Name each stop out to the skin (sweat glands, arrector pili, vessels).",
   crop=(440, 400, 1900, 1100), mode='gray'))

# Slides 33-35: vector labels (PDF points)
cards.append(T.vector_card(pdf, 33, 'l18_route_head', [
    ("Rami communicantes", [(472, 159, 592, 171)]),
    ("Cervicothoracic ganglion", [(313, 154, 405, 181)]),
    ("Vertebral nerve", [(182, 229, 246, 241)]),
    ("Middle cervical ganglion", [(240, 351, 330, 377)]),
    ("Vagosympathetic trunk", [(119, 327, 220, 354)]),
    ("Cranial cervical ganglion (synapse → head)", [(128, 157, 173, 198)]),
    ("Vagus nerve", [(487, 364, 536, 376)]),
], "Sympathetic route 2 · head & neck",
   "Thoracic cord → up the trunk to the head. Name each ganglion in order.", top=116))
cards.append(T.vector_card(pdf, 34, 'l18_route_abd', [
    ("Rami communicantes", [(129, 131, 250, 144)]),
    ("Major & minor splanchnic nerves", [(138, 271, 250, 298)]),
    ("Diaphragm", [(245, 376, 307, 389)]),
    ("Celiacomesenteric ganglion & plexus", [(297, 307, 404, 334)]),
    ("Lumbar splanchnic nerves", [(455, 119, 582, 131)]),
    ("Caudal mesenteric ganglion", [(506, 298, 614, 324)]),
], "Sympathetic route 3 · abdominal viscera",
   "Preganglionic fibers pass THROUGH the trunk. Where do they synapse?", top=107))
cards.append(T.vector_card(pdf, 35, 'l18_route_pelvis', [
    ("Lumbar splanchnic nerves", [(269, 131, 397, 144)]),
    ("Caudal mesenteric ganglion", [(305, 311, 414, 338)]),
    ("Hypogastric nerve", [(448, 158, 519, 184)]),
    ("Pelvic plexus", [(512, 216, 587, 228)]),
], "Sympathetic route 4 · pelvic viscera",
   "Lumbar cord → caudal mesenteric ganglion → pelvis.", top=107))

# Slides 38-39: vagus (parasympathetic, cranial)
cards.append(raster(38, 'l18_route_vagus_left', [
    ("Left vagosympathetic nerve trunk", [(312, 616, 556, 717)]),
    ("Left vagus nerve", [(545, 692, 724, 764)]),
    ("Cardiac nerves", [(662, 770, 826, 802)]),
    ("Recurrent laryngeal nerve", [(728, 804, 898, 876)]),
    ("Esophagus", [(1066, 556, 1236, 596)]),
    ("Ventral vagal nerve trunk → liver & stomach", [(1084, 650, 1290, 797)]),
    ("Dorsal vagal nerve trunk", [(1134, 354, 1476, 392)]),
    ("Dorsal vagal nerve trunk → celiacomesenteric nerve plexus", [(1458, 432, 1742, 579)]),
    ("Celiac plexus → stomach, spleen, liver, gallbladder, pancreas", [(1380, 627, 1726, 742)]),
    ("Cranial mesenteric plexus → small intestine, cecum, ascending & transverse colon", [(1344, 742, 1752, 920)]),
], "Parasympathetic · vagus, LEFT side",
   "Brainstem → neck → thorax → abdomen. Name each branch and where it ends.",
   crop=(290, 300, 1790, 930), white=[(0, 778, 600, 1126)]))
cards.append(raster(39, 'l18_route_vagus_right', [
    ("Right vagosympathetic nerve trunk", [(1408, 702, 1742, 826)]),
    ("Right vagus nerve", [(1194, 762, 1442, 852)]),
    ("Recurrent laryngeal nerve", [(1400, 544, 1556, 607)]),
    ("Heart & lungs (cardiac/pulmonary branches)", [(1090, 550, 1242, 636)]),
    ("Esophagus", [(738, 582, 932, 632)]),
    ("Dorsal vagal nerve trunk", [(518, 404, 900, 444)]),
    ("Ventral vagal nerve trunk → liver & stomach", [(740, 694, 986, 800)]),
    ("Dorsal vagal nerve trunk → celiacomesenteric nerve plexus", [(260, 468, 536, 609)]),
    ("Celiac plexus → stomach, spleen, liver, gallbladder, pancreas", [(296, 655, 652, 770)]),
    ("Cranial mesenteric plexus → small intestine, cecum, ascending & transverse colon", [(256, 770, 712, 908)]),
], "Parasympathetic · vagus, RIGHT side",
   "Same trip, right side. Which nerve hooks around the subclavian artery here?",
   crop=(240, 330, 1760, 920)))

# Slide 40: pelvic (sacral parasympathetic)
cards.append(raster(40, 'l18_route_pelvic', [
    ("Ventral root", [(868, 736, 982, 802)]),
    ("Spinal nerve", [(1050, 600, 1146, 656)]),
    ("Lumbosacral plexus", [(1205, 672, 1384, 733)]),
    ("Pelvic nerve (preganglionic parasympathetic)", [(1266, 834, 1356, 890)]),
    ("Pelvic plexus (synapse near/in the organ)", [(1250, 922, 1354, 978)]),
    ("Hypogastric nerve (sympathetic, joins the pelvic plexus)", [(814, 950, 970, 1004)]),
], "Parasympathetic · pelvic (S1–S3)",
   "Sacral cord → pelvic organs. Which nerve is parasympathetic and which is sympathetic?",
   crop=(560, 360, 1520, 1090), mode='gray'))

T.write('gross-anatomy-l18-routes.html', 'Trace the ANS Routes',
        'Lecture 18 · dog slides with names hidden · tap to pop them up in order along the route', cards, [])
print('ok', len(cards), sum(len(c['labels']) for c in cards))
