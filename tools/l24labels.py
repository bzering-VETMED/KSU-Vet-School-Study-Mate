# L24 Female Reproductive labeling deck (made by Claude). Names checked against the lecture transcript (10/21/26).
# Text after ' — ' in a name is a lecture note: shown in the reveal list, kept off the badge on the image.
# Run from repo root: python3 tools/l24labels.py /path/to/Lecture_24_Female_Reproductive_-_Tagged.pdf
# Boxes and badge points are in 200-dpi page pixels. Box modes: 'w' = repaint with the surrounding colour (labels on plain
# background), ('c', dx, dy) = clone nearby texture, 'i' = inpaint + grain (small marks on drawings), 'f' = fill white.
import cv2, sys, os, subprocess, numpy as np
sys.path.insert(0, os.path.dirname(__file__)); import tracer as T
pdf = sys.argv[1]; TMP = '/tmp/claude-0/l24b'; os.makedirs(TMP, exist_ok=True)
SEP = ' — '

def page_png(n):
    out = f'{TMP}/p{n}'
    if not os.path.exists(out + '.png'):
        subprocess.run(['pdftoppm', '-r', '200', '-png', '-f', str(n), '-l', str(n), '-singlefile', pdf, out], check=True)
    return cv2.imread(out + '.png')

def feather(h, w, f):  # alpha 1 inside, ramping to 0 over the outer f pixels
    ay = np.clip(np.minimum(np.arange(h), np.arange(h)[::-1]) / f, 0, 1); ax = np.clip(np.minimum(np.arange(w), np.arange(w)[::-1]) / f, 0, 1)
    return np.minimum(ay[:, None], ax[None, :])[..., None]

def fill(im, b, pad=6):  # label on plain/gradient background: inpaint the box (incl. JPEG halo) from a copy of its
    H, W = im.shape[:2]   # surroundings in which leader lines / dark edges are first lightened, so nothing dark smears in
    x0, y0, x1, y1 = max(0, int(b[0]) - pad), max(0, int(b[1]) - pad), min(W, int(b[2]) + pad), min(H, int(b[3]) + pad)
    r0, s0, r1, s1 = max(0, x0 - 14), max(0, y0 - 14), min(W, x1 + 14), min(H, y1 + 14)
    sub = im[s0:s1, r0:r1].copy(); m = np.zeros(sub.shape[:2], np.uint8); m[y0 - s0:y1 - s0, x0 - r0:x1 - r0] = 255
    dev = (cv2.medianBlur(sub, 21).astype(int) - sub.astype(int)).max(2) > 8  # JPEG specks darker than local background
    dark = cv2.dilate((((sub.min(2) < 200) | dev) & (m == 0)).astype(np.uint8), np.ones((3, 3), np.uint8), iterations=2) > 0
    if dark.any():
        sub = cv2.inpaint(sub, (dark * 255).astype(np.uint8), 5, cv2.INPAINT_TELEA)
    out = cv2.inpaint(sub, m, 9, cv2.INPAINT_TELEA)
    im[y0:y1, x0:x1] = out[y0 - s0:y1 - s0, x0 - r0:x1 - r0]

def clone(im, b, f=5):  # label on textured drawing: copy the same-size patch from (dx, dy) away; feather only outside the box
    x0, y0, x1, y1 = map(int, b[:4]); dx, dy = b[5], b[6]
    x0, y0, x1, y1 = x0 - f, y0 - f, x1 + f, y1 + f
    src = im[y0 + dy:y1 + dy, x0 + dx:x1 + dx].astype(float); dst = im[y0:y1, x0:x1].astype(float)
    a = feather(*dst.shape[:2], f)
    im[y0:y1, x0:x1] = np.clip(a * src + (1 - a) * dst, 0, 255).astype(np.uint8)

def inpaint(im, boxes, grain):  # l23ductus-style: inpaint the whole small box, then re-add grain so no smooth patch shows
    H, W = im.shape[:2]; mask = np.zeros((H, W), np.uint8)
    for b in boxes: mask[int(b[1]):int(b[3]), int(b[0]):int(b[2])] = 255
    out = cv2.inpaint(im, mask, 7, cv2.INPAINT_TELEA)
    if grain:
        rng = np.random.default_rng(1); noise = rng.normal(0, grain, out.shape[:2])
        m = mask > 0; o = out.astype(float); o[m] += noise[m][:, None]; out = np.clip(o, 0, 255).astype(np.uint8)
    return out

def card(n, out, crop, labels, title, hint, extra=(), grain=6):
    """labels: [(name, (badge x, y), [boxes])] in reveal order; extra: boxes to erase that are not quizzed.
    Box modes (5th item): default/'w' fill with surrounding colour ('n' = no padding), 'f' white, ('c', dx, dy) clone, 'i' inpaint."""
    im = page_png(n)
    boxes = [b for _, _, bs in labels for b in bs] + list(extra)
    mode = lambda b: b[4] if len(b) > 4 else 'w'
    for b in boxes:
        if mode(b) == 'f': im[int(b[1]):int(b[3]), int(b[0]):int(b[2])] = 255
    for b in boxes:
        if mode(b) == 'w': fill(im, b)
        if mode(b) == 'n': fill(im, b, pad=0)
    for b in boxes:
        if mode(b) == 'c': clone(im, b)
    ib = [b for b in boxes if mode(b) == 'i']
    if ib: im = inpaint(im, ib, grain)
    X0, Y0, X1, Y1 = crop; im = im[Y0:Y1, X0:X1]
    H, W = im.shape[:2]; cv2.imwrite(f'assets/{out}.jpg', im, [cv2.IMWRITE_JPEG_QUALITY, 90])
    def lab(nm, x, y):
        d = dict(n=nm, p=[round((x - X0) / W * 100, 2), round((y - Y0) / H * 100, 2)])
        if SEP in nm: d['s'] = nm.split(SEP)[0]
        return d
    return dict(title=title, q=hint, img=f'assets/{out}.jpg', labels=[lab(nm, x, y) for nm, (x, y), _ in labels])

cards = []
# Slide 4: ovarian bursa schematic (numbers 1 and 2 are named on the slide; 3, 4, 6 have no legend so they are only erased)
cards.append(card(4, 'l24lab_bursa_schematic', (1505, 55, 1995, 1105), [
    ("Ovary", (1848, 855), [(1828, 828, 1868, 884, 'i')]),
    ("Mesovarium — number 1; attaches the ovary to the dorsolateral abdominal wall", (1808, 300), [(1825, 160, 1852, 205), (1851, 552, 1873, 596, 'n')]),
    ("Mesosalpinx — number 2; arises from the lateral side of the mesovarium", (1745, 600), [(1710, 557, 1742, 600)]),
    ("Ovarian bursa (pouch the mesovarium + mesosalpinx form around the ovary)", (1835, 700), []),
], "Ovarian bursa · cross-section", "Ovary in the middle, peritoneal leaves around it. Name the folds and the pouch.",
   extra=[(1505, 55, 1562, 200, 'f'), (1545, 890, 1578, 935), (1560, 945, 1592, 990), (1785, 1028, 1820, 1075), (1512, 1035, 1552, 1085)]))

# Slide 5 figure B (also slides 8, 9): opened ovarian bursa
cards.append(card(5, 'l24lab_bursa_opened', (900, 182, 1612, 1095), [
    ("Ovary", (1335, 522), []),
    ("Opening of ovarian bursa — can be seen in the lab dogs", (1265, 447), [(1316, 184, 1480, 238)]),
    ("Cut edge of bursa", (1390, 397), [(1402, 293, 1512, 352)]),
    ("Mesosalpinx", (1460, 452), []),
    ("Infundibulum with abdominal ostium of uterine tube", (1233, 556), [(903, 598, 1112, 706)]),
    ("Ascending uterine tube", (1155, 404), [(970, 372, 1112, 432)]),
    ("Descending uterine tube", (1365, 637), []),
    ("Tubouterine junction (uterine ostium opens here)", (1278, 654), []),
    ("Uterine horn", (1200, 787), [(942, 753, 1030, 814)]),
    ("Mesometrium", (1384, 824), []),
], "Ovarian bursa · opened (uterine tube course)", "Bursa cut open to show the ovary. Follow the tube from the funnel to the horn.",
   extra=[(898, 1056, 928, 1092),  # clones run in this order so each source patch is already clean
          (1298, 806, 1471, 840, 'c', 0, 42), (1361, 705, 1527, 773, 'c', 0, 75), (1406, 619, 1556, 690, 'c', 0, 70),
          (1441, 554, 1527, 589, 'c', 0, 38), (1450, 470, 1610, 508, 'c', 0, 40)]))

# Slide 6 (= slide 7): broad ligament parts and ovarian ligaments
cards.append(card(6, 'l24lab_broad_ligament', (1200, 182, 1990, 1108), [
    ("Ovary", (1570, 500), [(1313, 473, 1429, 532)]),
    ("Suspensory ligament of the ovary — broken by strumming during an ovariohysterectomy", (1540, 287), [(1618, 188, 1937, 287)]),
    ("Proper ligament of the ovary — ovary to uterine horn; sturdy, the one you clamp", (1530, 607), [(1248, 543, 1408, 692)]),
    ("Mesovarium", (1688, 507), [(1743, 493, 1967, 542)]),
    ("Mesosalpinx", (1625, 462), [(1743, 383, 1972, 442)]),
    ("Descending uterine tube", (1595, 432), [(1208, 353, 1429, 442)]),
    ("Left uterine horn", (1520, 730), [(1661, 703, 1962, 752)]),
    ("Mesometrium", (1595, 820), [(1660, 798, 1912, 847)]),
    ("Round ligament of the uterus — gubernaculum remnant; runs into the inguinal canal", (1382, 893), [(1368, 973, 1537, 1107)]),
], "Broad ligament · left side", "Ventral view of the left ovary and horn. Name each fold and each ligament.",
   extra=[(1208, 1058, 1252, 1102)]))

# Slide 13: sagittal section through the cervix (slide text left of the drawing is cropped/whited out)
cards.append(card(13, 'l24lab_cervix', (1165, 285, 1995, 880), [
    ("Body of the uterus", (1465, 345), [(1622, 264, 1997, 328)]),
    ("Internal uterine orifice — opens toward the uterine body", (1520, 495), [(1622, 371, 1984, 498)]),
    ("Cervical canal", (1485, 525), [(1622, 551, 1996, 605)]),
    ("Cervix — most caudal part of the uterus; lies obliquely", (1500, 580), [(1622, 651, 1808, 705)]),
    ("External uterine orifice — opens toward the vagina", (1435, 565), []),
    ("Vaginal fornix — in the vaginal lumen, not part of the cervix; misleads a catheter", (1410, 455), []),
    ("Vagina — longitudinal and transverse folds", (1455, 720), []),
], "Cervix · sagittal section (cranial = top)", "Uterus on top, vagina below. Start in the uterine body and work caudally.",
   extra=[(1165, 285, 1327, 880, 'f')]))

# Slide 14: whole tract, dorsal view opened (sagittal-section inset whited out)
cards.append(card(14, 'l24lab_tract', (1068, 185, 1715, 1105), [
    ("Suspensory ligament of the ovary", (1186, 201), [(1226, 183, 1532, 214)]),
    ("Uterine tube", (1228, 237), [(1238, 220, 1370, 247)]),
    ("Mesosalpinx", (1233, 273), [(1248, 256, 1385, 287)]),
    ("Proper ligament of the ovary", (1218, 310), [(1086, 262, 1182, 347)]),
    ("Left uterine horn", (1248, 380), [(1288, 367, 1462, 395)]),
    ("Body of the uterus", (1383, 610), [(1110, 598, 1264, 629)]),
    ("Cervical canal", (1378, 652), [(1130, 644, 1280, 675)]),
    ("Cervix", (1363, 673), [(1218, 688, 1292, 718)]),
    ("Vagina — longitudinal and transverse folds", (1373, 822), [(1228, 806, 1307, 839)]),
    ("Vestibule — no mucosal folds", (1418, 960), [(1513, 918, 1615, 952)]),
    ("Urethral tubercle — ridge; the external urethral orifice is ventral to it", (1362, 942), [(1068, 944, 1238, 974)]),
    ("External urethral orifice", (1398, 905), [(1463, 870, 1704, 900)]),
    ("Vestibular bulb", (1326, 922), [(1110, 898, 1268, 929)]),
    ("Constrictor vestibuli — not identified in lab", (1308, 1005), [(1128, 988, 1248, 1044)]),
    ("Clitoris", (1402, 1033), [(1444, 1031, 1522, 1062)]),
    ("Fossa clitoridis — holds the glans of the clitoris", (1398, 1068), [(1442, 1065, 1602, 1096)]),
    ("Labium (lip of the vulva)", (1336, 1068), [(1234, 1066, 1318, 1096)]),
    ("Ureter", (1290, 455), [(1310, 438, 1382, 468)]),
    ("Urinary bladder", (1298, 570), [(1166, 553, 1252, 584)]),
], "Female tract · dorsal view, opened (cranial = top)", "Ovary down to the vulva. Name every label in order, then the two urinary landmarks.",
   extra=[(1585, 530, 1715, 800, 'f'), (1068, 185, 1180, 196, 'f'), (1494, 972, 1522, 1018, 'i')]))

# Slide 15: sagittal section of the vestibule and vulva
cards.append(card(15, 'l24lab_vestibule_sagittal', (1315, 62, 1830, 740), [
    ("Vagina", (1545, 377), [(1653, 333, 1737, 367)]),
    ("Urethral tubercle", (1525, 414), [(1658, 386, 1757, 447)]),
    ("Urethra", (1493, 410), [(1348, 476, 1437, 507)]),
    ("Vestibule", (1635, 577), [(1710, 476, 1820, 507)]),
    ("Vulva", (1735, 647), [(1750, 633, 1822, 667)]),
    ("Clitoris", (1550, 640), [(1383, 616, 1470, 647)]),
    ("Fossa clitoridis (labeled 'fossa for clitoris')", (1610, 652), [(1318, 698, 1508, 730)]),
    ("Rectum", (1465, 157), [(1503, 62, 1602, 97)]),
    ("Anal canal", (1570, 237), [(1613, 143, 1742, 177)]),
], "Vestibule & vulva · sagittal section (cranial = left)", "Vagina runs down to the vulva. Name the tract parts first, then the gut landmarks."))

# Slide 16 (= slides 15 bottom, 17): vestibule opened, dorsal view
cards.append(card(16, 'l24lab_vestibule_opened', (1170, 180, 1945, 650), [
    ("Vagina", (1570, 240), [(1348, 223, 1464, 264)]),
    ("Vestibule", (1630, 430), [(1768, 362, 1900, 396)]),
    ("External urethral orifice (labeled 'urethral opening')", (1590, 370), [(1700, 293, 1932, 330)]),
    ("Vestibular bulb", (1500, 390), [(1178, 360, 1408, 410)]),
    ("Constrictor vestibuli", (1470, 500), [(1208, 498, 1378, 577)]),
    ("Clitoris", (1595, 535), [(1673, 527, 1772, 563)]),
    ("Fossa clitoridis", (1600, 565), [(1672, 568, 1878, 608)]),
    ("Labium (lip of the vulva)", (1540, 575), [(1370, 600, 1481, 642)]),
], "Vestibule · opened, dorsal view (cranial = top)", "Vagina at the top, vulva at the bottom. What sits on the floor and the walls?",
   extra=[(1746, 451, 1772, 497, 'i')]))

# Slide 19: ventral urogenital view, split into two cards on the same image
L19 = {  # every label box on the figure
    'radr': (743, 258, 907, 284), 'ladr': (1023, 230, 1177, 255), 'crus': (1098, 263, 1289, 290),
    'phren': (1273, 298, 1447, 344), 'rkid': (630, 400, 744, 426), 'renal': (1278, 436, 1457, 462),
    'susp': (495, 456, 744, 482), 'tube': (636, 510, 744, 537), 'curet': (1268, 531, 1452, 558),
    'bursa': (531, 566, 744, 592), 'ova': (1261, 603, 1458, 629), 'prop': (536, 621, 744, 648),
    'utbr': (1255, 653, 1444, 700), 'horn': (636, 678, 744, 704), 'aorta': (1246, 726, 1297, 752),
    'broad': (495, 731, 752, 759), 'cvc': (1234, 778, 1385, 804), 'ureter': (698, 788, 757, 814),
    'dci': (1233, 828, 1398, 878), 'colon': (731, 893, 785, 920), 'uta': (1238, 902, 1430, 928),
    'round': (1238, 940, 1452, 967), 'ext': (1153, 980, 1317, 1007), 'body': (713, 1001, 840, 1029),
    'blad': (1076, 1020, 1148, 1045)}
TIP19 = {'radr': (953, 276), 'ladr': (1052, 338), 'crus': (1068, 405), 'phren': (1092, 383), 'rkid': (861, 421), 'renal': (1075, 471), 'susp': (814, 489), 'tube': (803, 550), 'curet': (1104, 496), 'bursa': (829, 590), 'ova': (1125, 596), 'prop': (825, 614), 'utbr': (1143, 675), 'horn': (836, 696), 'aorta': (1007, 682), 'broad': (871, 718), 'cvc': (986, 721), 'ureter': (979, 732), 'dci': (1064, 796), 'colon': (982, 843), 'uta': (1108, 850), 'round': (1140, 903), 'ext': (1082, 942), 'body': (971, 911), 'blad': (1029, 982)}  # leader-line ends on the structures
def c19(names, out, title, hint):
    used = {k for _, k in names}
    return card(19, out, (490, 225, 1465, 1050),
                [(nm, TIP19[k], [L19[k]]) for nm, k in names],
                title, hint, extra=[b for k, b in L19.items() if k not in used] + [(1138, 910, 1170, 952, 'i')])
cards.append(c19([
    ("Suspensory ligament of the ovary", 'susp'), ("Uterine tube", 'tube'), ("Opening of the ovarian bursa", 'bursa'),
    ("Proper ligament of the ovary", 'prop'), ("Uterine horn", 'horn'), ("Broad ligament (mesometrium)", 'broad'),
    ("Round ligament of the uterus", 'round'), ("Body of the uterus", 'body'), ("Right kidney", 'rkid'),
    ("Right adrenal gland", 'radr'), ("Left adrenal gland", 'ladr'), ("Left crus of the diaphragm", 'crus'),
    ("Ureter", 'ureter'), ("Colon", 'colon'), ("Urinary bladder", 'blad'),
], 'l24lab_ventral', "Urogenital system · ventral view: tract & ligaments", "Dog on its back, cranial = top. Tract and ligaments first, then landmarks."))
cards.append(c19([
    ("Aorta", 'aorta'), ("Caudal vena cava", 'cvc'), ("Phrenicoabdominal artery and vein", 'phren'),
    ("Renal artery and vein", 'renal'), ("Cranial ureteral artery", 'curet'), ("Ovarian artery and vein — artery is a direct branch of the aorta; left vein drains to the left renal vein, right to the caudal vena cava", 'ova'),
    ("Uterine branch of the ovarian artery and vein", 'utbr'), ("Deep circumflex iliac artery and vein", 'dci'),
    ("External iliac artery", 'ext'), ("Uterine artery and vein — artery comes off the vaginal artery and anastomoses with the uterine branch of the ovarian artery", 'uta'),
], 'l24lab_ventral', "Urogenital system · ventral view: vessels", "Same view. Aorta and caudal vena cava first, then cranial to caudal."))

# Slide 20: lymphatics (numbers from the slide legend; letters have no legend, so they are only erased)
LETTERS = [(1005, 368, 1042, 400), (1196, 305, 1222, 336), (1143, 375, 1170, 406), (1300, 358, 1332, 396), (1381, 324, 1410, 352),
           (1376, 540, 1406, 569), (1500, 487, 1546, 513), (1505, 520, 1533, 551), (1591, 533, 1616, 563), (1677, 479, 1710, 506),
           (1724, 510, 1753, 536), (1827, 485, 1864, 513), (1894, 483, 1922, 516), (1963, 489, 1997, 523), (1417, 600, 1447, 633),
           (1539, 651, 1567, 679), (1555, 620, 1585, 652)]
cards.append(card(20, 'l24lab_lymph', (965, 265, 2000, 840), [
    ("Lumbar aortic lymph node (2) — ovary and uterus; not identified in lab", (1190, 470), []),
    ("Lumbar aortic lymph node (3) — not identified in lab", (1084, 479), [(1058, 483, 1084, 508, 'i'), (1168, 441, 1185, 462, 'i')]),
    ("Medial iliac lymph node — internal structures; identified in lab", (1295, 447), [(1254, 408, 1280, 442, 'i')]),
    ("Hypogastric lymph node — vagina and vestibule", (1515, 470), [(1497, 436, 1527, 471, 'i')]),
    ("Lateral sacral lymph node", (1648, 420), [(1617, 421, 1646, 453, 'i')]),
    ("Superficial inguinal lymph nodes — vulva and clitoris; identified in lab", (1700, 578), [(1657, 552, 1684, 585, 'i')]),
    ("Lymph vessel bending over to the other surface of the uterine horn", (1436, 528), [(1395, 511, 1421, 539, 'i')]),
], "Lymphatics · lateral view (cranial = left)", "Blue = lymph vessels and nodes. Name each node, then say what drains to it.",
   extra=[b + ('i',) for b in LETTERS] + [(940, 560, 1092, 840, 'f')], grain=10))

T.write('gross-anatomy-l24-labels.html', 'Label It · Female Reproductive',
        'Lecture 24 · dog slides with labels hidden · tap to reveal in order', cards, texts=[])
print('ok', len(cards), sum(len(c['labels']) for c in cards))
