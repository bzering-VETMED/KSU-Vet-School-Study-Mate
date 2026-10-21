# L21 Abdominal Cavity 2 labeling deck (made by Claude). Names checked against the 10/14 lecture transcript and the slide legends.
# Run from repo root: python3 tools/abd2labels.py /path/to/abd2.pdf /path/to/abd2.pptx   (needs LibreOffice for the line diagrams)
# The red line diagrams (slides 3, 4, 6, 9, 10) are re-rendered from a copy of the pptx with their text deleted, so the bars stay crisp.
# Other figures come from the pptx media at full resolution. Coordinates are in source-image px
# (200-dpi page renders for slides, native px for media). Box modes: 'w' = whiten grey/black text on white,
# 'i' = inpaint dark strokes (+ grain), 'c' = inpaint a round white number disc (photos), 'b' = inpaint the whole box
# (label plate on a coloured drawing), 'f' = fill white.
import cv2, sys, os, re, subprocess, zipfile, numpy as np
sys.path.insert(0, os.path.dirname(__file__)); import tracer as T
pdf, pptx = sys.argv[1:3]
TMP = '/tmp/claude-0/abd2lab'; os.makedirs(TMP, exist_ok=True)
Z = zipfile.ZipFile(pptx)
NOTEXT = (3, 4, 6, 9, 10)

def notext_pdf():
    out = f'{TMP}/abd2_notext.pdf'
    if not os.path.exists(out):
        src = f'{TMP}/abd2_notext.pptx'; zo = zipfile.ZipFile(src, 'w', zipfile.ZIP_DEFLATED)
        for it in Z.infolist():
            d = Z.read(it.filename)
            if re.fullmatch(r'ppt/slides/slide(%s)\.xml' % '|'.join(map(str, NOTEXT)), it.filename):
                d = re.sub(rb'<a:t>[^<]*</a:t>', b'<a:t></a:t>', d)
            zo.writestr(it.filename, d)  # not the shared ZipInfo: writestr would rewrite its offset
        zo.close()
        subprocess.run(['soffice', '--headless', '--convert-to', 'pdf', '--outdir', TMP, src], check=True, capture_output=True)
    return out

def page_png(n):
    src = notext_pdf() if n in NOTEXT else pdf; out = f'{TMP}/p{n}' + ('nt' if n in NOTEXT else '')
    if not os.path.exists(out + '.png'):
        subprocess.run(['pdftoppm', '-r', '200', '-png', '-f', str(n), '-l', str(n), '-singlefile', src, out], check=True)
    return cv2.imread(out + '.png')

def media(name):
    return cv2.imdecode(np.frombuffer(Z.read('ppt/media/' + name), np.uint8), cv2.IMREAD_COLOR)

def gray(s):  # grey/black anti-aliased text on white (low saturation)
    return (s.max(2) < 242) & ((s.max(2) - s.min(2)) < 45)

def disc(sub):  # white number disc + its dark outline/digit, inside the inscribed ellipse
    h, w = sub.shape[:2]; yy, xx = np.ogrid[:h, :w]
    ell = ((xx - w / 2 + .5) / (w / 2)) ** 2 + ((yy - h / 2 + .5) / (h / 2)) ** 2 <= 1
    white = (sub.min(2) > 150) & ((sub.max(2) - sub.min(2)) < 60)
    return ell & (white | (sub.max(2) < 110))

def card(src, out, crop, labels, title, hint, extra=(), thr=130, grain=6, scale=1, post=None, paper=False, wmode=None):
    """labels: [(name, (badge x, y), [boxes])] in reveal order; extra: boxes erased but not quizzed."""
    im = src.copy() if isinstance(src, np.ndarray) else page_png(src) if isinstance(src, int) else media(src)
    boxes = [b for _, _, bs in labels for b in bs] + list(extra)
    if scale != 1:
        im = cv2.resize(im, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
        boxes = [tuple(v * scale for v in b[:4]) + tuple(b[4:]) for b in boxes]
    H, W = im.shape[:2]; wm = wmode or ('p' if paper else 'w'); mode = lambda b: (b[4] if len(b) > 4 else 'w').replace('w', wm)
    clip = lambda b: (max(0, int(b[0])), max(0, int(b[1])), min(W, int(b[2])), min(H, int(b[3])))
    for b in boxes:
        if mode(b) == 'f': x0, y0, x1, y1 = clip(b); im[y0:y1, x0:x1] = 255
    mask = np.zeros((H, W), np.uint8)
    rimband = lambda x0, y0, x1, y1: [mask.__setitem__(sl, 255) for sl in ((slice(max(0, y0 - 3), y0 + 3), slice(x0, x1)),
        (slice(y1 - 3, y1 + 3), slice(x0, x1)), (slice(y0, y1), slice(max(0, x0 - 3), x0 + 3)), (slice(y0, y1), slice(x1 - 3, x1 + 3)))]
    for b in boxes:  # 'p': label on a noisy off-white margin -> fill the whole box with the paper colour around it
        if mode(b) == 'p':
            x0, y0, x1, y1 = clip(b); sub = im[y0:y1, x0:x1]
            rim = np.concatenate([sub[0], sub[-1], sub[:, 0], sub[:, -1]]); rim = rim[rim.min(1) > 200]
            sub[:] = np.median(rim, axis=0) if len(rim) else 255; rimband(x0, y0, x1, y1)
    for b in boxes:
        if mode(b) == 'w':
            x0, y0, x1, y1 = clip(b); sub = im[y0:y1, x0:x1]
            m = cv2.dilate(gray(sub.astype(int)).astype(np.uint8), np.ones((3, 3), np.uint8), iterations=3)
            rim = np.concatenate([sub[0], sub[-1], sub[:, 0], sub[:, -1]]); rim = rim[rim.min(1) > 200]  # paper colour, not pure white
            sub[m > 0] = np.median(rim, axis=0) if len(rim) else 255
    for b in boxes:  # 'b': label plate on a flat-coloured drawing -> fill with the colour just outside it, blend only the rim
        if mode(b) == 'b':
            x0, y0, x1, y1 = clip(b); r = 6
            ring = np.concatenate([im[max(0, y0 - r):y0, x0:x1].reshape(-1, 3), im[y1:y1 + r, x0:x1].reshape(-1, 3),
                                   im[y0:y1, max(0, x0 - r):x0].reshape(-1, 3), im[y0:y1, x1:x1 + r].reshape(-1, 3)])
            im[y0:y1, x0:x1] = np.median(ring, axis=0)
            rimband(x0, y0, x1, y1)
    for b in boxes:
        x0, y0, x1, y1 = clip(b); md = mode(b); sub = im[y0:y1, x0:x1].astype(int)
        if md == 'i': mx = sub.max(2); m = mx < min(thr, np.median(mx) - 30)  # darker than both thr and the local background
        elif md == 'c': m = disc(sub)
        else: continue
        mask[y0:y1, x0:x1] |= (m * 255).astype(np.uint8)
    if mask.any():
        mask = cv2.dilate(mask, np.ones((3, 3), np.uint8), iterations=3)
        im = cv2.inpaint(im, mask, 9, cv2.INPAINT_TELEA)
        if grain:  # re-add grain so no smooth patch shows on textured figures
            rng = np.random.default_rng(1); noise = rng.normal(0, grain, (H, W))
            m = mask > 0; o = im.astype(float); o[m] += noise[m][:, None]; im = np.clip(o, 0, 255).astype(np.uint8)
    if post: post(im, scale)
    X0, Y0, X1, Y1 = (int(v * scale) for v in crop); im = im[Y0:Y1, X0:X1]
    h, w = im.shape[:2]; cv2.imwrite(f'assets/{out}.jpg', im, [cv2.IMWRITE_JPEG_QUALITY, 90])
    return dict(title=title, q=hint, img=f'assets/{out}.jpg',
                labels=[dict(n=nm, p=[round((x * scale - X0) / w * 100, 2), round((y * scale - Y0) / h * 100, 2)]) for nm, (x, y), _ in labels])

def num(cx, cy, r=24, md='c'):  # box around a number (disc) centred at cx, cy
    return (cx - r, cy - r, cx + r, cy + r, md)

def L(name, x0, y0, x1, y1, md='w', pad=5, at='c'):  # a text label, erase box padded; badge where its leader line starts
    x = {'c': (x0 + x1) / 2, 'l': x0 + 16, 'r': x1 - 16}[at]
    return (name, (x, (y0 + y1) / 2), [(x0 - pad, y0 - pad, x1 + pad, y1 + pad, md)])

def E(x0, y0, x1, y1, md='w', pad=5):  # erase-only text label
    return (x0 - pad, y0 - pad, x1 + pad, y1 + pad, md)

cards = []
LOGO = (1680, 1012, 1960, 1092, 'f')

# ---------- LO1 blood supply ----------
# Slide 3: the three unpaired branches of the abdominal aorta
cards.append(card(3, 'abd2lab_unpaired', (500, 185, 1065, 1035), [
    ("Aorta (abdominal)", (998, 611), []),
    ("Celiac artery", (750, 339), []),
    ("Cranial mesenteric artery", (754, 435), []),
    ("Caudal mesenteric artery", (751, 866), []),
], "Unpaired branches of the abdominal aorta (cranial = top)", "Three unpaired branches. Name them cranial to caudal."))

# Slide 4: celiac artery, three branches. The Y is a picture with its words baked in, so the bars are rebuilt from its
# red pixels (closing fills the letter holes), rotated upright as on the slide, and mapped to slide px for the badges.
def clean_y():
    im = media('image2.png'); c = im.astype(int)
    red = ((c[..., 2] > 150) & (c[..., 2] - c[..., 1] > 90)).astype(np.uint8) * 255
    m = cv2.morphologyEx(red, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (41, 41)))
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9)))
    m = cv2.rotate(m, cv2.ROTATE_90_CLOCKWISE); bar = np.median(c[red > 0], axis=0)
    soft = cv2.GaussianBlur(m, (5, 5), 0).astype(float)[..., None] / 255
    out = (255 * (1 - soft) + bar * soft).astype(np.uint8)
    ys, xs = np.where(m > 0); x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    out = cv2.copyMakeBorder(out[y0:y1 + 1, x0:x1 + 1], 40, 40, 40, 40, cv2.BORDER_CONSTANT, value=(255, 255, 255))
    P = (255, 273, 767, 1020)  # the Y's extent on the 200-dpi slide render
    sx, sy = (x1 - x0) / (P[2] - P[0]), (y1 - y0) / (P[3] - P[1])
    return out, lambda x, y: ((x - P[0]) * sx + 40, (y - P[1]) * sy + 40)
YIM, YP = clean_y()
cards.append(card(YIM, 'abd2lab_celiac', (0, 0, YIM.shape[1], YIM.shape[0]), [
    ("Aorta", YP(443, 995), []),
    ("Celiac artery", YP(567, 760), []),
    ("Hepatic artery (→ liver)", YP(679, 440), []),
    ("Left gastric artery (→ stomach)", YP(567, 398), []),
    ("Splenic artery (→ spleen)", YP(437, 433), []),
], "Celiac artery · three branches (cranial = top)", "Follow each branch to its organ to name it.", scale=0.6))

# Slide 5: cat dissection, celiac branches (numbers from the slide caption; the transcript reads the same numbers)
cards.append(card('image3.png', 'abd2lab_cat_celiac', (0, 0, 1182, 864), [
    ("Celiac artery", (912, 660), [num(912, 660)]),
    ("Splenic artery", (708, 520), [num(708, 520)]),
    ("Left gastric artery", (933, 487), [num(933, 487)]),
    ("Hepatic artery", (953, 593), [num(953, 593)]),
], "Celiac artery · cat dissection", "Arrows point to the vessels. Follow each one toward its organ.",
   extra=[num(738, 177), num(468, 245), num(990, 380), num(476, 540), num(140, 625), num(178, 430), num(561, 848)], grain=5))

# Slide 6: celiac artery, full branching (inset figure whited out)
cards.append(card(6, 'abd2lab_celiac_branches', (195, 108, 1975, 1125), [
    ("Aorta", (1925, 750), []),
    ("Celiac artery", (1641, 602), []),
    ("Left gastric artery", (1300, 400), []),
    ("Hepatic artery", (1205, 598), []),
    ("Hepatic branches", (1060, 433), []),
    ("Right gastric artery", (780, 500), []),
    ("Gastroduodenal artery", (865, 745), []),
    ("Right gastroepiploic artery", (405, 782), []),
    ("Cranial pancreaticoduodenal artery", (555, 1022), []),
    ("Splenic artery", (1240, 762), []),
    ("Dorsal branch (of the splenic artery)", (1275, 862), []),
    ("Ventral branch (of the splenic artery)", (1088, 990), []),
    ("Short gastric arteries", (1435, 988), []),
    ("Left gastroepiploic artery", (1565, 745), []),
], "Celiac artery · all branches (cranial = left)", "Aorta on the right. Celiac → hepatic, left gastric, splenic, then each branch onward.",
   extra=[(1362, 0, 2000, 352, 'f'), LOGO]))

# Slide 7: stomach blood supply quadrants (raw drawing from the pptx; the slide's quadrant lines redrawn)
S7 = lambda x, y: ((x - 428.6) / 1.624, (y - 202.5) / 1.624)  # slide px -> media px
def quad(im, s):
    c, t = (70, 70, 190), max(3, int(3 * s))
    cv2.line(im, (int(423 * s), int(62 * s)), (int(423 * s), int(512 * s)), c, t, cv2.LINE_AA)
    cv2.line(im, (int(186 * s), int(317 * s)), (int(694 * s), int(317 * s)), c, t, cv2.LINE_AA)
cards.append(card('image5.jpeg', 'abd2lab_stomach_quadrants', (60, 40, 740, 520), [
    ("Left gastric artery (left lesser curvature)", S7(1258, 532), []),
    ("Right gastric artery (right lesser curvature)", S7(957, 613), []),
    ("Right gastroepiploic artery (right greater curvature)", S7(957, 803), []),
    ("Left gastroepiploic artery (left greater curvature)", S7(1272, 797), []),
], "Stomach blood supply · four quadrants", "Patient's left and right. Which artery supplies each quarter?",
   scale=1.5, post=quad))

# Slide 9: cranial mesenteric artery (Miller's figure on the left and the inset on the right whited out)
cards.append(card(9, 'abd2lab_cranial_mesenteric', (625, 330, 1790, 1125), [
    ("Aorta", (1731, 560), []),
    ("Cranial mesenteric artery", (1560, 785), []),
    ("Common trunk", (1490, 757), []),
    ("Middle colic artery", (1362, 580), []),
    ("Right colic artery", (1235, 690), []),
    ("Ileocolic artery", (1165, 892), []),
    ("Colic branch (of the ileocolic artery)", (862, 845), []),
    ("Mesenteric ileal branch", (748, 926), []),
    ("Cecal branch", (900, 1005), []),
    ("Antimesenteric ileal artery", (745, 1040), []),
    ("Caudal pancreaticoduodenal artery", (1240, 945), []),
    ("Jejunal arteries", (1525, 985), []),
    ("Ileal arteries", (1168, 1098), []),
], "Cranial mesenteric artery · branches (cranial = top)", "Aorta top right. Common trunk first, then the ileocolic's three branches, then the rest.",
   extra=[(1415, 0, 2000, 388, 'f'), (600, 150, 912, 775, 'f'), LOGO]))

# Slide 10: caudal mesenteric artery
cards.append(card(10, 'abd2lab_caudal_mesenteric', (1240, 392, 1830, 1092), [
    ("Aorta", (1287, 575), []),
    ("Caudal mesenteric artery", (1500, 800), []),
    ("Left colic artery (→ descending colon)", (1772, 790), []),
    ("Cranial rectal artery (→ rectum)", (1572, 1030), []),
], "Caudal mesenteric artery · two branches", "The last unpaired branch. Name both branches.",
   extra=[(1684, 1018, 1960, 1092, 'f')]))

# ---------- LO3 peritoneum ----------
# Slide 16 left: female sagittal (Fig 9-34); all labels erased, peritoneum-related ones quizzed
F_OTHER = [E(1777, 278, 2010, 329), E(1784, 353, 1896, 393), E(253, 375, 644, 415), E(1167, 407, 1286, 438), E(1786, 426, 2013, 457),
           E(1640, 498, 1892, 543), E(129, 546, 644, 577), E(1543, 571, 1771, 602), E(159, 633, 643, 664), E(1496, 644, 1967, 684),
           E(514, 718, 642, 749), E(473, 840, 796, 880), E(1785, 940, 1840, 975)]
cards.append(card('image13.png', 'abd2lab_peritoneum_female', (300, 20, 2060, 1085), [
    L("Pararectal fossa", 437, 229, 741, 260, at='r'),
    L("Rectogenital pouch (rectum ↔ vagina)", 281, 460, 639, 500, at='r'),
    L("Vesicogenital pouch (bladder ↔ vagina)", 475, 156, 852, 196, at='r'),
    L("Pubovesical pouch (pubis ↔ bladder)", 568, 915, 919, 955, at='r'),
    L("Parietal peritoneum", 1170, 957, 1534, 997),
    L("Visceral peritoneum", 1460, 717, 1832, 757, at='l'),
    L("Vaginal process", 894, 1025, 1194, 1065),
    L("Rectum", 494, 296, 635, 327, at='r'),
    L("Bladder", 1445, 789, 1590, 820, at='l'),
], "Peritoneum · female, sagittal (cranial = right)", "Peritoneum caps off as pouches before the caudal pelvis. Name the pouches dorsal to ventral, then the layers.",
   extra=F_OTHER))

# Slide 16 right: male sagittal (Fig 9-16)
M_OTHER = [E(1028, 306, 1120, 333), E(134, 382, 535, 416), E(293, 437, 568, 464), E(1175, 462, 1273, 489), E(271, 502, 546, 536),
           E(1241, 543, 1665, 577), E(159, 580, 523, 614), E(130, 622, 526, 656), E(404, 658, 521, 685), E(129, 715, 544, 749),
           E(147, 784, 564, 818), E(325, 880, 495, 914), E(1675, 933, 1718, 963), E(231, 940, 496, 1014), E(858, 1021, 1089, 1055),
           E(1452, 1043, 1592, 1077), E(873, 1108, 1078, 1142), E(1386, 1098, 1679, 1132), E(1042, 1158, 1275, 1233), E(1317, 1146, 1742, 1180)]
cards.append(card('image14.png', 'abd2lab_peritoneum_male', (380, 100, 1808, 1250), [
    L("Pararectal fossa", 469, 149, 726, 176, at='r'),
    L("Parietal peritoneum", 1452, 806, 1760, 840),
    L("Visceral peritoneum", 1236, 649, 1552, 683, at='l'),
    L("Vaginal ring (parietal peritoneum dips into the inguinal canal)", 1242, 762, 1430, 796, at='l'),
    L("Testicular artery, vein and nerves (spermatic cord)", 1236, 708, 1768, 742, at='l'),
    L("Parietal vaginal tunic", 221, 1057, 550, 1091, at='r'),
    L("Visceral vaginal tunic", 472, 1115, 810, 1149),
    L("Bladder", 1238, 595, 1360, 622, at='l'),
    L("Prostate", 1066, 364, 1196, 391, at='l'),
    L("Ductus deferens", 1106, 409, 1364, 436, at='l'),
], "Peritoneum · male, sagittal (cranial = right)", "Follow the parietal peritoneum from the abdominal wall down through the vaginal ring to the testis.",
   extra=M_OTHER))

# Slide 18: intraperitoneal vs retroperitoneal (label plates on the drawing are repainted)
cards.append(card('image17.jpeg', 'abd2lab_retroperitoneal', (0, 0, 1800, 1300), [
    L("Parietal peritoneum", 1535, 311, 1773, 415, at='l'),
    L("Visceral peritoneum", 981, 370, 1221, 476, 'b', 14),
    L("Mesentery", 976, 578, 1199, 621, 'b', 14),
    L("Intraperitoneal organ (fully wrapped)", 592, 73, 1033, 115),
    L("Retroperitoneal organ (kidney: covered on one side only)", 276, 600, 601, 706, 'b', 14),
], "Peritoneum · transverse section", "Which organ is behind the peritoneum? Name the layers and the fold.", grain=0))

# Slide 21: lecture cartoon, transverse section (no labels on the slide; names from the lecture)
cards.append(card(21, 'abd2lab_transverse_cartoon', (560, 200, 1440, 1090), [
    ("Kidney (retroperitoneal)", (912, 330), []),
    ("Kidney (retroperitoneal)", (1085, 327), []),
    ("Caudal vena cava (blue)", (1024, 397), []),
    ("Aorta (red)", (966, 397), []),
    ("Peritoneal sac (= peritoneal cavity)", (800, 800), []),
    ("Organ (viscus) pushed into the sac", (982, 698), []),
    ("Visceral peritoneum (on the organ)", (1038, 692), []),
    ("Parietal peritoneum (on the wall)", (1367, 640), []),
], "Peritoneum · lecture cartoon, transverse section", "Hand-in-a-balloon: the organ pushes into the sac. Name each part.",
   extra=[(540, 380, 600, 452, 'f')]))

# Slide 23: Fig 03-32, schematic transverse section of the dog (legend cropped; numbers erased)
cards.append(card(23, 'abd2lab_transverse', (640, 225, 1615, 1085), [
    ("Visceral peritoneum (continuous line)", (852, 808), [(838, 790, 866, 826, 'w')]),
    ("Parietal peritoneum (broken line)", (1035, 990), [(1020, 972, 1050, 1008, 'w')]),
    ("Root of the mesentery", (1157, 587), [(1143, 569, 1171, 605, 'i')]),
    ("Right kidney (retroperitoneal)", (1412, 403), [(1398, 385, 1426, 421, 'w')]),
    ("Left kidney (retroperitoneal)", (1077, 513), [(1055, 493, 1102, 533, 'w')]),
    ("Spleen", (825, 618), [(811, 600, 839, 636, 'w')]),
    ("Jejunum", (1335, 882), [(1321, 864, 1349, 900, 'w')]),
    ("Descending duodenum", (1467, 500), [(1453, 482, 1481, 518, 'i')]),
], "Peritoneum · transverse section of the dog (L = left, R = right)", "Solid vs broken line first. Which organs are retroperitoneal?", thr=120, grain=0))

# Slide 25: peritoneal pouches (Fig 03-33 detail; the slide's answer boxes and legend are cropped off)
cards.append(card('image25.png', 'abd2lab_pouches', (1080, 120, 1540, 520), [
    ("Pararectal fossa (either side of the mesorectum)", (1145, 240), [(1127, 227, 1163, 254, 'w')]),
    ("Rectogenital pouch (rectum ↔ vagina / genital fold)", (1152, 305), [(1134, 292, 1171, 318, 'w')]),
    ("Vesicogenital pouch (bladder ↔ vagina / genital fold)", (1126, 353), [(1108, 340, 1144, 366, 'w')]),
    ("Pubovesical pouch (pubis ↔ bladder)", (1222, 442), [(1204, 429, 1241, 455, 'w')]),
    ("Bladder", (1175, 471), [(1157, 458, 1193, 485, 'w')]),
    ("Prostate", (1266, 412), [(1248, 399, 1284, 426, 'w')]),
    ("Rectum", (1312, 275), [(1291, 259, 1332, 292, 'b')]),
    ("Ischium", (1395, 412), [(1377, 399, 1414, 426, 'w')]),
    ("Anus", (1505, 287), [(1487, 274, 1524, 301, 'w')]),
], "Peritoneal pouches · paramedian section (cranial = left)", "Four pouches, dorsal to ventral. Say what each one sits between.",
   extra=[(1000, 285, 1022, 316, 'w')], scale=2, grain=0))

# ---------- LO4 mesentery / omenta ----------
# Slide 28: Fig 03-33 paramedian section (numbers 16-24 erased too; pouches have their own card)
P28 = {1: (351, 175), 2: (269, 243), 3: (214, 373), 4: (171, 532), 5: (168, 610), 6: (181, 448), 7: (493, 340), 8: (592, 203),
       9: (568, 360), 10: (520, 515), 11: (598, 577), 12: (776, 467), 13: (922, 463), 14: (982, 442), 15: (1002, 300)}
B28 = lambda k, md='w', r=(13, 16): (P28[k][0] - r[0] - (6 if k >= 10 else 0), P28[k][1] - r[1], P28[k][0] + r[0] + (6 if k >= 10 else 0), P28[k][1] + r[1], md)
cards.append(card('image25.png', 'abd2lab_paramedian', (20, 30, 1535, 820), [
    ("Aorta", P28[1], [B28(1)]),
    ("Esophagus", P28[2], [B28(2)]),
    ("Caudal vena cava", P28[3], [B28(3)]),
    ("Diaphragm", P28[4], [B28(4)]),
    ("Liver", P28[5], [B28(5)]),
    ("Lesser omentum", P28[6], [B28(6)]),
    ("Pancreas", P28[7], [B28(7, 'i')]),
    ("Root of the mesentery", P28[8], [B28(8, 'i')]),
    ("Transverse colon", P28[9], [(556, 343, 577, 370, 'w')]),
    ("Stomach", P28[10], [B28(10, 'i')]),
    ("Omental bursa (between the walls of the greater omentum)", P28[11], [B28(11, 'i')]),
    ("Small intestine", P28[12], [(752, 452, 800, 484, 'w')]),
    ("Deep wall of the greater omentum", P28[13], [B28(13)]),
    ("Superficial wall of the greater omentum", P28[14], [B28(14)]),
    ("Parietal peritoneum", P28[15], [B28(15)]),
], "Mesentery & omenta · paramedian section (cranial = left)", "Greater omentum loops off the greater curvature; lesser omentum runs stomach → liver.",
   extra=[(1127, 227, 1163, 254), (1134, 292, 1171, 318), (1108, 340, 1144, 366), (1204, 429, 1241, 455), (1157, 458, 1193, 485),
          (1248, 399, 1284, 426), (1291, 259, 1332, 292, 'b'), (1377, 399, 1414, 426), (1487, 274, 1524, 301)], thr=120, grain=0))

# Slide 33: lesser omentum on the visceral surface of the liver (epiploic foramen borders live here too)
LV_OTHER = [E(647, 46, 808, 64), E(484, 82, 634, 100), E(972, 106, 1084, 156), E(126, 199, 309, 222), E(126, 297, 246, 315),
            E(54, 394, 230, 417), E(56, 489, 169, 540), E(42, 732, 168, 783), E(746, 762, 987, 785), E(64, 832, 186, 850), E(275, 936, 452, 960)]
cards.append(card('image30.png', 'abd2lab_lesser_omentum', (0, 0, 1168, 1012), [
    L("Lesser omentum", 781, 720, 955, 738, at='l'),
    L("Papillary process of the caudate lobe (lesser omentum lies over it)", 858, 20, 1042, 67, at='l'),
    L("Caudate process of the caudate lobe (lateral border of the epiploic foramen)", 0, 612, 170, 660, at='r'),
    L("Caudal vena cava (dorsal border of the epiploic foramen)", 320, 980, 508, 999, at='r'),
    L("Portal vein (ventral border of the epiploic foramen)", 630, 893, 740, 912, at='l'),
    L("Hepatic artery", 658, 850, 805, 873, at='l'),
    L("Hepatic branches", 696, 806, 882, 828, at='l'),
    L("Bile duct", 602, 936, 692, 955, at='l'),
    L("Gastroduodenal artery", 160, 892, 396, 916, at='r'),
    L("Right gastric artery", 536, 980, 735, 1002, at='l'),
], "Lesser omentum · visceral surface of the liver", "Find the lesser omentum, then the three borders of the epiploic foramen.",
   extra=LV_OTHER + [(750, 985, 1168, 1012, 'f')], paper=True, grain=0))

# Slide 34: figure on the epiploic foramen slide (hepatic portal flow vs a shunt)
cards.append(card('image31.png', 'abd2lab_portal_shunt', (0, 0, 968, 708), [
    L("Caudal vena cava (leading to the heart)", 216, 41, 734, 62),
    ("Liver", (330, 262), []),
    L("Gastrointestinal tract", 666, 394, 907, 445),
    L("Normal blood flow through the hepatic portal vein", 68, 534, 358, 618),
    L("Abnormal blood flow bypassing the liver (portosystemic shunt)", 526, 493, 760, 681),
], "Hepatic portal flow (epiploic foramen slide)", "Gut blood should reach the liver first. Name the normal route and the bypass.", paper=True, grain=0))

# ---------- LO6 inguinal rings / canal ----------
# Slide 38 left (also slide 37): female, superficial inguinal ring (caption cropped)
cards.append(card('image36.png', 'abd2lab_inguinal_female', (27, 25, 1160, 938), [
    ("Vaginal process (emerging from the ring)", (743, 490), [num(743, 490)]),
    ("External pudendal vessels", (832, 735), [num(832, 735)]),
    ("Superficial inguinal ring", (897, 648), [num(897, 648)]),
    ("Superficial inguinal lymph node", (682, 768), [num(682, 768)]),
    ("External abdominal oblique muscle", (342, 338), [num(342, 338)]),
    ("Aponeurosis of the external abdominal oblique", (660, 490), [num(660, 490)]),
    ("Internal abdominal oblique muscle", (643, 328), [num(643, 328)]),
], "Superficial inguinal ring · female", "Name what comes out of the ring first, then the muscles that make it.",
   extra=[num(928, 244), num(136, 801), num(522, 786)], grain=5))

# Slide 38 right: male, fresh tissue
cards.append(card('image36.png', 'abd2lab_inguinal_male', (1190, 22, 2402, 1040), [
    ("Spermatic cord", (1778, 352), [num(1778, 352)]),
    ("External pudendal vessels", (1611, 630), [num(1611, 630)]),
    ("Superficial inguinal ring", (1465, 211), [num(1465, 211)]),
    ("Testis (in the scrotum)", (2125, 683), [num(2125, 683)]),
    ("Superficial inguinal lymph node", (1461, 648), [num(1461, 648)]),
], "Superficial inguinal ring · male (fresh tissue)", "Cord and vessels both leave the ring. Where does each go?",
   extra=[(1322, 432, 1362, 472, 'i')], grain=5))

# Slide 39: deep inguinal ring with the external abdominal oblique aponeurosis reflected
cards.append(card('image37.png', 'abd2lab_deep_ring', (825, 22, 2365, 962), [
    ("Deep inguinal ring", (1777, 243), [num(1777, 243, 34)]),
    ("Internal abdominal oblique muscle (cranial border)", (1398, 446), [num(1398, 446, 34)]),
    ("Rectus abdominis muscle (medial border)", (1234, 690), [num(1234, 690, 34)]),
    ("Inguinal ligament (caudal border: caudal edge of the external abdominal oblique aponeurosis)", (1386, 176), [num(1386, 176, 34)]),
    ("External abdominal oblique muscle (reflected)", (1051, 260), [num(1051, 260, 34)]),
    ("Aponeurosis of the external abdominal oblique (reflected)", (1610, 278), [(1590, 258, 1630, 298, 'i')]),
    ("Aponeurosis of the external abdominal oblique (reflected)", (1720, 657), [(1694, 618, 1746, 680, 'i')]),
    ("Cremaster muscle (on the spermatic cord)", (2078, 404), [num(2078, 404, 34)]),
    ("External pudendal vessels", (1876, 637), [num(1876, 637, 34)]),
    ("Superficial inguinal lymph node", (2019, 762), [num(2019, 762, 34)]),
], "Deep inguinal ring · aponeurosis reflected", "Find the ring, then name its cranial, medial and caudal borders.", grain=5))

# Slide 40: Fig 4-6, male genitalia ventral view (caption cropped)
G_OTHER = [E(1115, 79, 1276, 120), E(1214, 383, 1325, 479), E(144, 487, 601, 528), E(407, 664, 597, 697), E(415, 754, 598, 787),
           E(1188, 892, 1386, 1031), E(498, 931, 643, 965), E(1009, 1213, 1221, 1255)]
cards.append(card('image40.png', 'abd2lab_spermatic_cord', (100, 0, 1560, 1280), [
    L("External abdominal oblique", 235, 271, 597, 365, at='r'),
    L("Superficial inguinal ring", 148, 397, 601, 439, at='r'),
    L("Spermatic cord", 319, 841, 617, 883, at='r'),
    L("Cremaster (from the internal abdominal oblique)", 396, 576, 600, 610, at='r'),
    L("External pudendal artery and vein", 1173, 539, 1461, 686, at='l'),
    L("Right testis", 538, 1208, 755, 1249, at='r'),
], "Spermatic cord leaving the superficial ring · ventral view", "Name the ring and what passes out of it. Which two named structures do NOT go through the vaginal ring?",
   extra=G_OTHER, wmode='i', thr=215, grain=0))

T.write('gross-anatomy-abd2-labels.html', 'Label It · Abdominal Cavity 2',
        'L21 · Dr. Diehl · dog slides with labels hidden · tap to reveal names in order', cards, texts=[])
import json; json.dump(cards, open(f'{TMP}/cards.json', 'w'))
print('ok', len(cards), sum(len(c['labels']) for c in cards))
