# L23 Male Reproductive labeling deck (made by Claude): slide figures with every label/number erased,
# numbered pink badges pop the names back up in order. Reuses tracer.write / tracer.pos.
# Run from repo root: python3 tools/l23labels.py /path/to/Lecture_23_Male_Reproductive_-_Tagged.pdf
import cv2, sys, os, subprocess, numpy as np
sys.path.insert(0, os.path.dirname(__file__)); import tracer as T
pdf = sys.argv[1]; TMP = '/tmp/claude-0/l23lab'; os.makedirs(TMP, exist_ok=True)
NOT_YET = ' (slides; lecture finishes today)'

def page_png(n):
    out = f'{TMP}/p{n}'
    if not os.path.exists(out + '.png'):
        subprocess.run(['pdftoppm', '-r', '200', '-png', '-f', str(n), '-l', str(n), '-singlefile', pdf, out], check=True)
    return cv2.imread(out + '.png')

def grain(out, mask, sd=6):
    rng = np.random.default_rng(1); noise = rng.normal(0, sd, out.shape[:2])
    o = out.astype(float); m = (mask > 0) & (out.min(2) < 232); o[m] += noise[m][:, None]  # no speckle on plain white
    return np.clip(o, 0, 255).astype(np.uint8)

def whiten(im, b):  # text on white: turn only the grey/black strokes (plus halo) white, like l18trace
    x0, y0, x1, y1 = map(int, b); sub = im[y0:y1, x0:x1]; c = sub.astype(int)
    m = ((c.max(2) < 175) & ((c.max(2) - c.min(2)) < 45)).astype(np.uint8)
    m = cv2.dilate(m, np.ones((3, 3), np.uint8), iterations=3)
    sub[m > 0] = 255
    c = sub.astype(int); near = cv2.dilate(m, np.ones((3, 3), np.uint8), iterations=4) > 0
    sub[near & (c.min(2) > 160) & ((c.max(2) - c.min(2)) < 40)] = 255

def big_parts(m, min_area):  # drop stipple dots so only real glyph strokes are inpainted
    n, lab, st, _ = cv2.connectedComponentsWithStats(m, 8)
    keep = np.zeros_like(m)
    for i in range(1, n):
        if st[i, cv2.CC_STAT_AREA] >= min_area: keep[lab == i] = 1
    return keep

def inpaint(im, boxes, kind='dark', thr=160, min_area=12, sd=6):
    H, W = im.shape[:2]; mask = np.zeros((H, W), np.uint8)
    g = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY).astype(int); med = cv2.medianBlur(cv2.cvtColor(im, cv2.COLOR_BGR2GRAY), 21).astype(int)
    for b in boxes:
        x0, y0, x1, y1 = map(int, b); sub = im[y0:y1, x0:x1].astype(int)
        if kind == 'dark': m = (sub.max(2) < thr).astype(np.uint8)
        else: m = (np.abs(g[y0:y1, x0:x1] - med[y0:y1, x0:x1]) > thr).astype(np.uint8)  # 'contrast': white or black letters on grey shading
        mask[y0:y1, x0:x1] |= big_parts(m, min_area)
    mask = cv2.dilate(mask, np.ones((3, 3), np.uint8), iterations=3)
    return grain(cv2.inpaint(im, mask * 255, 9, cv2.INPAINT_TELEA), mask, sd)

def clone(im, boxes, pad=3, ring=7):
    """Clone-stamp each box from the best-matching nearby patch (matched on a ring around the box), then swap the
    patch's low frequencies for an inpainted fill so brightness matches; feathered edges. Keeps the engraving texture."""
    H, W = im.shape[:2]; src = im.copy(); bad = np.zeros((H, W), np.uint8)
    for b in boxes: bad[max(0, b[1]-pad):b[3]+pad, max(0, b[0]-pad):b[2]+pad] = 1
    smooth = cv2.inpaint(src, bad * 255, 9, cv2.INPAINT_TELEA).astype(float)
    for b in boxes:
        x0, y0, x1, y1 = b[0]-pad, b[1]-pad, b[2]+pad, b[3]+pad; w, h = x1-x0, y1-y0
        X0, Y0, X1, Y1 = x0-ring, y0-ring, x1+ring, y1+ring; hh, ww = Y1-Y0, X1-X0
        rm = np.ones((hh, ww), bool); rm[ring:-ring, ring:-ring] = False
        tgt = src[Y0:Y1, X0:X1].astype(float); best = None
        for dy in range(-3*h, 3*h+1, 2):
            for dx in range(-3*w, 3*w+1, 2):
                if abs(dx) < w + 2 and abs(dy) < h + 2: continue
                sx0, sy0 = X0+dx, Y0+dy
                if sx0 < 0 or sy0 < 0 or sx0+ww > W or sy0+hh > H: continue
                if bad[sy0:sy0+hh, sx0:sx0+ww].any(): continue
                cand = src[sy0:sy0+hh, sx0:sx0+ww].astype(float)
                d = ((cand - tgt)[rm] ** 2).mean() + 0.02 * (dx*dx + dy*dy)
                if best is None or d < best[0]: best = (d, dx, dy)
        _, dx, dy = best
        patch = src[Y0+dy:Y1+dy, X0+dx:X1+dx].astype(float)
        patch = patch - cv2.GaussianBlur(patch, (0, 0), 4) + cv2.GaussianBlur(smooth[Y0:Y1, X0:X1], (0, 0), 4)
        a = np.zeros((hh, ww), np.float32); a[ring-2:hh-ring+2, ring-2:ww-ring+2] = 1
        a = cv2.GaussianBlur(a, (0, 0), 2.5); a[ring:-ring, ring:-ring] = 1; a = a[..., None]
        im[Y0:Y1, X0:X1] = np.clip(patch * a + im[Y0:Y1, X0:X1].astype(float) * (1 - a), 0, 255).astype(np.uint8)
    return im

def card(n, out, crop, labels, title, hint, extra=(), white=(), mode='w', thr=160, kind='dark', anchor='auto'):
    """labels: [(name, box, mode-or-None)] page px at 200 dpi, badge sits where the label was.
    extra: boxes to erase with no card label. white: rects to blank fully (slide text overlapping the crop)."""
    im = page_png(n)
    for w in white: im[w[1]:w[3], w[0]:w[2]] = 255
    jobs = [(lab[1], (lab[2] or mode)) for lab in labels] + [(b[0], b[1]) if len(b) == 2 else (b, mode) for b in extra]
    for b, m in jobs:
        if m == 'w': whiten(im, b)
    ib = [b for b, m in jobs if m == 'i']
    if ib: im = clone(im, ib) if kind == 'clone' else inpaint(im, ib, kind, thr)
    X0, Y0, X1, Y1 = crop; im = im[Y0:Y1, X0:X1].copy()
    c = im.astype(int); im[(c.min(2) > 222) & ((c.max(2) - c.min(2)) < 14)] = 255  # flatten JPEG haze so erased boxes don't show edges
    H, W = im.shape[:2]; cv2.imwrite(f'assets/{out}.jpg', im, [cv2.IMWRITE_JPEG_QUALITY, 90])
    sh = lambda b: (b[0] - X0, b[1] - Y0, b[2] - X0, b[3] - Y0)
    ov = {lab[1]: lab[3] for lab in labels if len(lab) > 3 and lab[3]}
    def spot(b):  # badge sits at the end of the label that touches its leader line, not mid-word
        a = ov.get(b, anchor)
        if a == 'C' or b[2] - b[0] < 60: return b
        a = a if a != 'auto' else ('L' if (b[0] + b[2]) / 2 > (X0 + X1) / 2 else 'R')
        return (b[0], b[1], b[0] + 36, b[3]) if a == 'L' else (b[2] - 36, b[1], b[2], b[3])
    return dict(title=title, q=hint, img=f'assets/{out}.jpg', labels=[dict(n=lab[0], p=T.pos(sh(spot(lab[1])), H, W)) for lab in labels])

L = lambda name, box, mode=None, anchor=None: (name, box, mode, anchor)
cards = []

# Slide 9 · testis layers (Dyce numbered figure; legend on the slide is cropped out)
cards.append(card(9, 'l23lab_layers', (1285, 105, 1985, 1092), [
    L("Scrotal skin and tunica dartos", (1946, 282, 1976, 326), 'w'),
    L("Scrotal septum", (1694, 729, 1727, 772)),
    L("External spermatic fascia", (1794, 612, 1826, 656)),
    L("Cremaster muscle", (1659, 119, 1689, 163), 'w'),
    L("Parietal layer of the vaginal tunic", (1819, 549, 1851, 592)),
    L("Visceral layer of the vaginal tunic (dissected off the surface of the testis)", (1814, 471, 1846, 514)),
    L("Visceral layer of the vaginal tunic covering the structures in the spermatic cord", (1586, 126, 1616, 167), 'w'),
    L("Visceral layer of the vaginal tunic on the testis", (1288, 808, 1332, 862), 'w'),
    L("Ductus deferens (deferent duct)", (1517, 542, 1549, 586)),
    L("Tail of the epididymis", (1511, 1051, 1543, 1096), 'w'),
], "Testis layers · numbered figure", "Scrotum opened from the front: left compartment shows the epididymis side, right compartment has the tunics cut and folded back. Outer → inner.",
   extra=[((1528, 108, 1562, 152), 'w'), ((1713, 98, 1747, 141), 'w'), ((1366, 188, 1397, 227), 'w'), ((1383, 220, 1412, 262), 'w'), ((1323, 254, 1357, 297), 'w')],
   white=[(1285, 100, 1432, 188), (1400, 1088, 1800, 1100)], mode='i', thr=150))

# Slide 10 · testis attachments (lecture: this is the MEDIAL view, ductus deferens side)
cards.append(card(10, 'l23lab_attach', (1125, 300, 1990, 885), [
    L("Ductus deferens", (1457, 318, 1662, 350), None, 'R'),
    L("Cremaster muscle", (1379, 376, 1516, 406), None, 'R'),
    L("Parietal vaginal tunic", (1748, 359, 1906, 422)),
    L("Ligament of the tail of the epididymis", (1144, 615, 1343, 681)),
    L("Proper ligament of the testis", (1132, 741, 1339, 800)),
], "Testis attachments", "Medial view of the testis (the side you see the ductus deferens on). Two ligaments = remnants of the gubernaculum.",
   extra=[(1128, 845, 1163, 885)], white=[(1120, 560, 1192, 619), (1120, 800, 1192, 885)]))

# Slide 12 · spermatic cord / mesorchium cross-section
cards.append(card(12, 'l23lab_cord', (1200, 495, 1985, 1000), [
    L("Spermatic fascia", (1705, 590, 1985, 634)),
    L("Cremaster muscle", (1348, 947, 1531, 985)),
    L("Parietal vaginal tunic", (1713, 668, 1935, 706)),
    L("Vaginal canal", (1440, 512, 1668, 557), None, 'C'),
    L("Visceral vaginal tunic", (1711, 735, 1940, 772)),
    L("Mesorchium", (1212, 740, 1422, 776)),
    L("Testicular artery and vein", (1185, 589, 1451, 676)),
    L("Mesoductus (mesoductus deferens)", (1216, 841, 1424, 878)),
    L("Deferent duct (ductus deferens)", (1718, 821, 1948, 858)),
    L("Deferent artery (artery of the ductus deferens)", (1703, 897, 1985, 942)),
], "Spermatic cord · cross-section", "Cross-section through the cord inside the vaginal tunic. Outer wrappings first, then the folds and what they carry.",
   white=[(1195, 540, 1242, 606), (1950, 912, 1985, 945)]))

# Slide 19 · penis divisions (lateral view, cranial = left)
cards.append(card(19, 'l23lab_penis', (905, 175, 1995, 1000), [
    L("Ureters", (1052, 336, 1150, 366)),
    L("Bladder", (1039, 511, 1141, 544), 'i'),
    L("Ductus deferens", (911, 647, 1115, 678)),
    L("Prostate", (1358, 259, 1466, 290), None, 'C'),
    L("Pelvic urethra", (1478, 302, 1650, 333), None, 'C'),
    L("Ischiocavernosus muscle", (1694, 314, 1910, 375)),
    L("Retractor penis muscle", (1751, 392, 1942, 454)),
    L("Bulbospongiosus muscle", (1745, 472, 1959, 534)),
    L("Bulb of the penis", (1726, 551, 1890, 587)),
    L("Corpus cavernosum", (1338, 565, 1495, 627), 'i'),
    L("Corpus spongiosum", (1650, 636, 1897, 673)),
    L("Urethra", (1579, 712, 1677, 743)),
    L("Os penis", (1325, 653, 1441, 690), 'i'),
    L("Bulbus glandis", (1466, 839, 1650, 876)),
    L("Pars longa glandis", (936, 855, 1168, 892)),
], "Penis · root, body, glans" + NOT_YET, "Lateral view, cranial = left, penis curves cranially under the pelvis. Bladder → root → body → glans."))

# Slide 21 · perineal muscles (A superficial caudal view, B deeper, pelvis cut)
cards.append(card(21, 'l23lab_perineum', (650, 445, 1985, 1090), [
    L("Rectococcygeus", (981, 495, 1187, 532)),
    L("Coccygeus", (1111, 582, 1255, 619)),
    L("Levator ani", (1111, 635, 1255, 666)),
    L("External anal sphincter", (1003, 704, 1289, 740)),
    L("Internal obturator", (1125, 759, 1341, 791)),
    L("Ischiourethralis", (1143, 847, 1334, 879)),
    L("Ischiocavernosus", (1130, 900, 1348, 931)),
    L("Bulbospongiosus", (1129, 948, 1344, 985)),
    L("Retractor penis", (1143, 992, 1335, 1028)),
    L("Urethra (pelvic, B)", (1493, 632, 1591, 663)),
    L("Prostate", (1627, 649, 1737, 681)),
    L("Ischiatic tuber", (1797, 948, 1974, 980)),
    L("Urethra (in the bulb, B)", (1742, 991, 1842, 1022)),
    L("Bulb of the penis", (1710, 1038, 1876, 1074)),
], "Perineum · root of the penis" + NOT_YET, "Caudal views. A = superficial (tail up, anus hooked); B = deeper, with the root cut across. Leader lines from the middle labels hit both A and B.",
   white=[(650, 440, 848, 462)], anchor='L'))

# Slide 24 · longitudinal section
cards.append(card(24, 'l23lab_longsec', (860, 0, 1995, 490), [
    L("Bulbospongiosus", (1075, 5, 1289, 42)),
    L("Bulb of the penis", (1103, 45, 1268, 81)),
    L("Urethra", (1121, 83, 1219, 114)),
    L("Retractor penis", (1152, 117, 1343, 153)),
    L("Corpus spongiosum penis", (1177, 154, 1498, 192)),
    L("Corpus cavernosum penis", (1254, 193, 1578, 229)),
    L("Bulbus glandis", (1337, 231, 1521, 268)),
    L("Prepuce", (1481, 270, 1590, 307)),
    L("Pars longa glandis", (1596, 325, 1827, 362)),
    L("Os penis", (1661, 364, 1776, 401)),
    L("Fibrocartilaginous end of the os penis", (1687, 408, 1910, 475)),
], "Penis · longitudinal section" + NOT_YET, "Bulb (top left) to tip (right). Letters A–E mark where the cross-sections on the next cards are cut.",
   white=[(855, 66, 896, 160)], anchor='L'))

# Slide 24 · cross-sections A + B (root)
cards.append(card(24, 'l23lab_xsecAB', (760, 500, 1380, 1126), [
    L("Urethra", (1036, 540, 1135, 571)),
    L("Corpus spongiosum", (1068, 593, 1317, 630)),
    L("Bulb of the penis", (1068, 641, 1233, 677)),
    L("Bulbospongiosus", (1064, 694, 1280, 731)),
    L("Retractor penis", (1033, 741, 1225, 778)),
    L("Crus of the corpus cavernosum", (1034, 856, 1374, 892)),
    L("Ischiocavernosus", (1098, 899, 1317, 930)),
    L("Urethra", (1114, 940, 1213, 971)),
    L("Corpus spongiosum", (1115, 987, 1364, 1024)),
    L("Bulbospongiosus", (1092, 1031, 1307, 1068)),
    L("Retractor penis", (1067, 1077, 1259, 1113)),
], "Penis cross-sections A & B · root" + NOT_YET, "A = through the bulb; B = a bit further, where the crura appear. Dorsal = top.",
   white=[(755, 845, 802, 902)]))

# Slide 24 · cross-sections C–E (body → glans)
cards.append(card(24, 'l23lab_xsecCE', (1405, 500, 2000, 1126), [
    L("Corpus cavernosum", (1631, 516, 1882, 553)),
    L("Tunica albuginea", (1631, 554, 1846, 603)),
    L("Urethra", (1631, 593, 1730, 624)),
    L("Corpus spongiosum", (1631, 631, 1880, 668)),
    L("Retractor penis", (1631, 670, 1823, 705)),
    L("Bulbus glandis", (1632, 765, 1817, 802)),
    L("Os penis", (1631, 808, 1747, 844)),
    L("Anastomosis of the bulbus glandis and corpus spongiosum", (1631, 849, 2000, 916)),
    L("Skin", (1631, 976, 1692, 1007)),
    L("Pars longa glandis", (1632, 1016, 1862, 1053)),
    L("Os penis", (1631, 1055, 1747, 1092)),
    L("Corpus spongiosum", (1631, 1096, 1880, 1126)),
], "Penis cross-sections C–E · body → glans" + NOT_YET, "C = body; D = bulbus glandis; E = pars longa glandis. Dorsal = top."))

# Slide 26 · os penis
cards.append(card(26, 'l23lab_ospenis', (240, 280, 1990, 1090), [
    L("Base", (1837, 283, 1977, 337)),
    L("Body", (743, 841, 881, 906)),
    L("Apex", (385, 851, 523, 915)),
    L("Fibrocartilage (fibrocartilaginous tip)", (244, 595, 598, 662)),
    L("Urethral groove", (1376, 929, 1587, 1061)),
], "Os penis" + NOT_YET, "Lateral view, tip (distal) = left. Two cross-sections on the right show which surface the groove is on.",
   white=[(240, 280, 1012, 500)], anchor='C'))

# Slide 28 · penis muscles a–d (legend a–d on slide; every other letter/number erased)
cards.append(card(28, 'l23lab_muscles', (1290, 70, 1995, 955), [
    L("Bulbospongiosus", (1543, 523, 1566, 547)),
    L("Ischiocavernosus", (1658, 536, 1683, 563)),
    L("Retractor penis", (1576, 562, 1601, 589)),
    L("Ischiourethralis", (1659, 489, 1686, 515)),
], "Penis muscles (a–d)" + NOT_YET, "Caudal view of the perineum, tail up, anus in the middle. Only the 4 penis muscles get badges.",
   extra=[(1506, 490, 1533, 516), (1609, 525, 1633, 551), (1493, 536, 1519, 563), (1500, 677, 1530, 702), (1530, 683, 1566, 702),
          (1500, 752, 1527, 775), (1527, 757, 1566, 772), (1476, 717, 1501, 748), (1543, 724, 1562, 748),
          (1588, 268, 1612, 298), (1518, 312, 1544, 340), (1529, 340, 1554, 365), (1559, 364, 1588, 386), (1472, 338, 1497, 366),
          (1575, 421, 1602, 450), (1403, 384, 1430, 412), (1771, 394, 1797, 422), (1440, 440, 1467, 469), (1385, 463, 1411, 491),
          (1771, 469, 1798, 497), (1208, 630, 1238, 662), (1427, 588, 1456, 617), (1340, 709, 1371, 741), (1549, 798, 1583, 828),
          (1510, 854, 1543, 885), (1606, 856, 1639, 887), (1310, 912, 1343, 945), (1940, 878, 1985, 925)],
   white=[(1290, 60, 1427, 142)], mode='i', kind='clone'))

# Slide 31 · prostate, dorsal view
cards.append(card(31, 'l23lab_prost_dorsal', (1185, 150, 1985, 1100), [
    L("Ureter", (1806, 207, 1921, 248)),
    L("Ductus deferens", (1801, 315, 1956, 402)),
    L("Bladder", (1750, 468, 1893, 507)),
    L("Genital fold", (1683, 577, 1885, 617)),
    L("Prostate", (1597, 839, 1749, 878)),
    L("Urethral muscle", (1518, 961, 1793, 1003)),
    L("Urethra", (1516, 1048, 1652, 1088)),
], "Prostate · dorsal view" + NOT_YET, "Dorsal view, cranial = top. Follow the two ductus deferens down to the prostate.", mode='i', thr=150,
   white=[(1185, 140, 1335, 172)], anchor='L'))

# Slide 32 · prostate opened, ventral view
cards.append(card(32, 'l23lab_prost_ventral', (1150, 195, 1990, 1100), [
    L("Ureteral orifice", (1558, 637, 1806, 675)),
    L("Orifices of the deferent ducts", (1555, 717, 1801, 799)),
    L("Trigone", (1846, 701, 1979, 745)),
    L("Colliculus seminalis", (1552, 837, 1722, 919)),
    L("Urethral muscle", (1492, 961, 1758, 1001)),
    L("Urethra", (1474, 1045, 1603, 1084)),
], "Prostate · opened, ventral view" + NOT_YET, "Bladder and urethra slit open from the ventral side, cranial = top. What sits on the hillock?", mode='i', thr=150,
   white=[(1148, 680, 1188, 752)], anchor='L'))

# Slide 34 · blood supply of the penis
cards.append(card(34, 'l23lab_penis_vessels', (325, 190, 1680, 1100), [
    L("Internal pudendal artery and vein", (659, 209, 945, 293)),
    L("Ventral perineal artery and vein", (480, 341, 742, 427)),
    L("Artery of the penis", (1260, 300, 1503, 344)),
    L("Artery and vein of the bulbus penis", (1265, 435, 1518, 520)),
    L("Deep artery and vein of the penis", (408, 521, 676, 607)),
    L("Dorsal artery and vein of the penis", (1225, 618, 1508, 703)),
    L("Anastomosis of the deep artery of the penis and the artery of the bulb", (330, 862, 780, 948)),
    L("Artery of the bulb", (1390, 1034, 1613, 1076)),
    L("Deep artery of the penis", (1390, 872, 1589, 958)),
    L("Urethra", (1256, 372, 1386, 410)),
    L("Urethra", (1390, 975, 1520, 1013)),
    L("Bulbus penis", (481, 751, 697, 796)),
    L("Corpus cavernosum penis", (1248, 742, 1678, 787)),
    L("Corpus spongiosum penis", (434, 989, 862, 1035)),
], "Blood supply · penis" + NOT_YET, "Root of the penis from the side, cut across at the bottom right. Internal pudendal → artery of the penis → its 3 branches."))

# Slide 35 · testicular veins (kidneys & adrenals, ventral view)
cards.append(card(35, 'l23lab_testic_veins', (405, 250, 1660, 990), [
    L("Aorta", (1176, 372, 1252, 402)),
    L("Caudal vena cava", (536, 257, 765, 288)),
    L("Renal artery", (1403, 675, 1559, 710)),
    L("Renal vein", (409, 700, 546, 731)),
    L("Left kidney", (1403, 764, 1548, 799)),
    L("Ureter", (613, 792, 699, 822)),
    L("Adrenal gland (right)", (516, 304, 697, 340)),
    L("Adrenal gland (left)", (1176, 423, 1355, 459)),
    L("Common trunk: caudal phrenic artery, cranial abdominal artery", (1350, 471, 1641, 571)),
    L("1st lumbar transverse process", (1179, 274, 1420, 341)),
    L("4th lumbar vertebra", (540, 857, 793, 887)),
    L("Right testicular vein → caudal vena cava", (626, 921, 810, 952)),
    L("Left testicular vein → left renal vein", (1049, 941, 1232, 971)),
], "Blood supply · testicular veins" + NOT_YET, "Ventral view: the dog's right is on YOUR left. Where does each testicular vein drain?"))

T.write('gross-anatomy-l23-labels.html', 'Label It · Male Reproductive',
        'Lecture 23 · slide figures with every label hidden · tap to reveal in order', cards, [])
print('ok', len(cards), sum(len(c['labels']) for c in cards))
