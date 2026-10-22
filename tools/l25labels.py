# L25 Normal Radiographic Anatomy of the Abdomen · "Read the Radiograph" deck (made by Claude). Dr. McHaney's slides.
# Names checked against the slide text and the lecture transcript (10/22/26).
# Run from repo root: python3 tools/l25labels.py /path/to/Normal_Radiographic_Anatomy_of_the_Abdomen_Student_2026_-_Tagged.pdf
# Technique: the slide arrows, dashed lines, coloured outlines and C/F/B/P/D letters are vector overlays, so each card is
# built from the clean embedded radiograph (pdfimages) stretched to its on-slide box; label points come from where the
# slide's overlays sat (converted to % of that box). Letters burned into the image itself (slide 69, slide 3 viewer text)
# are inpainted with grain. Text after ' — ' in a name is a lecture note: shown in the reveal list, kept off the badge.
import cv2, sys, os, glob, subprocess, numpy as np
sys.path.insert(0, os.path.dirname(__file__)); import tracer as T
pdf = sys.argv[1]; TMP = '/tmp/claude-0/l25lab'; os.makedirs(TMP, exist_ok=True)
SEP = ' — '

def raw(n, size):
    """Embedded image of slide n with pixel size (w, h)."""
    if not glob.glob(f'{TMP}/r-{n:03d}-*'):
        subprocess.run(['pdfimages', '-j', '-p', '-f', str(n), '-l', str(n), pdf, f'{TMP}/r'], check=True)
    for f in sorted(glob.glob(f'{TMP}/r-{n:03d}-*')):
        im = cv2.imread(f)
        if im is not None and (im.shape[1], im.shape[0]) == size: return im
    raise SystemExit(f'slide {n}: no image {size}')

def erase(im, boxes, grain=5):
    """Inpaint whole boxes given in % of the image (burned-in letters / viewer text), then re-add film grain."""
    H, W = im.shape[:2]; m = np.zeros((H, W), np.uint8)
    for x0, y0, x1, y1 in boxes: m[int(y0 * H / 100):int(y1 * H / 100), int(x0 * W / 100):int(x1 * W / 100)] = 255
    out = cv2.inpaint(im, m, 7, cv2.INPAINT_TELEA)
    if grain:
        noise = np.random.default_rng(1).normal(0, grain, (H, W)); k = m > 0
        o = out.astype(float); o[k] += noise[k][:, None]; out = np.clip(o, 0, 255).astype(np.uint8)
    return out

def panel(n, size, bbox, erase_boxes=()):
    """Raw image, cleaned, with its on-slide aspect (PowerPoint sometimes stretches) — bbox in PDF points."""
    im = raw(n, size)
    if erase_boxes: im = erase(im, erase_boxes)
    return im, (bbox[2] - bbox[0]) / (bbox[3] - bbox[1])

def pt(bbox, x, y):  # a point in PDF points -> % of that image's box
    return [(x - bbox[0]) / (bbox[2] - bbox[0]) * 100, (y - bbox[1]) / (bbox[3] - bbox[1]) * 100]

def card(out, panels, labels, title, hint, height=900, maxw=1500, gap=14):
    """panels: [panel(...)] laid side by side at one height; labels: [(name, panel index, [x%, y%]), ...] in reveal order."""
    ws = [round(height * a) for _, a in panels]
    if sum(ws) + gap * (len(ws) - 1) > maxw:
        height = int(height * (maxw - gap * (len(ws) - 1)) / sum(ws)); ws = [round(height * a) for _, a in panels]
    W = sum(ws) + gap * (len(ws) - 1); canvas = np.zeros((height, W, 3), np.uint8); xs = []; x = 0
    for (im, _), w in zip(panels, ws):
        interp = cv2.INTER_CUBIC if w > im.shape[1] else cv2.INTER_AREA
        canvas[:, x:x + w] = cv2.resize(im, (w, height), interpolation=interp); xs.append(x); x += w + gap
    cv2.imwrite(f'assets/{out}.jpg', canvas, [cv2.IMWRITE_JPEG_QUALITY, 88])
    def lab(nm, i, p):
        d = dict(n=nm, p=[round((xs[i] + p[0] / 100 * ws[i]) / W * 100, 2), round(p[1], 2)])
        if SEP in nm: d['s'] = nm.split(SEP)[0]
        return d
    return dict(title=title, q=hint, img=f'assets/{out}.jpg', labels=[lab(*l) for l in labels])

cards = []

# Slides 3-4: the cat that ate a sewing needle (slide 3 arrow = needle, slide 4 arrow = falciform fat); one label per opacity
B3 = (168, 199, 724, 528)
cards.append(card('l25lab_opacities', [panel(4, (969, 573), B3, [(0, 0, 9, 3.5), (56, 1, 64, 5)])], [
    ("Gas in the lung — gas: least opaque, black", 0, [4, 32]),
    ("Falciform fat — fat: darker grey (slide 4 arrow)", 0, pt(B3, 314.6, 471.6)),
    ("Liver — soft tissue: medium grey (soft tissue and fluid are the same opacity)", 0, [14, 62]),
    ("Lumbar vertebra — mineral (bone): white", 0, [55, 17]),
    ("Sewing needle — metal: most opaque, very white (slide 3 arrow)", 0, pt(B3, 389, 368)),
], "Radiographic opacities · cat, lateral", "Cranial = left. Point at one example of each opacity, least opaque to most opaque."))

# Slide 7 (= slide 8): the three standard views of the same cat; slide captions erased by using the raw images
B7 = [(2, 199, 311, 449), (309, 205, 641, 449), (642, 53, 928, 528)]
cards.append(card('l25lab_views', [panel(7, (857, 696), B7[0]), panel(7, (921, 680), B7[1]), panel(7, (893, 1475), B7[2])], [
    ("Left lateral — left side down", 0, [72, 90]),
    ("Gas in the pylorus and duodenum — right-sided structures are up on the left lateral", 0, [24, 56]),
    ("Right lateral — right side down; the pylorus and duodenum are not gas-highlighted", 1, [76, 86]),
    ("Ventrodorsal — on its back, beam enters ventrally", 2, [50, 4]),
], "Standard views · cat", "Three views of the same cat a minute or two apart. Name each view, then the gas-filled structures."))

# Slide 20: lumbar musculature lines (yellow dashed overlays on the slide)
B20 = [(284, 270, 618, 534), (641, 67, 900, 534)]
cards.append(card('l25lab_lumbar', [panel(20, (927, 734), B20[0]), panel(20, (459, 829), B20[1])], [
    ("Epaxial muscles — dorsal to the transverse processes", 0, [62, 7]),
    ("Hypaxial muscles — ventral to the transverse processes", 0, [62, 27]),
    ("Lumbar muscle line — may create confusing lines", 1, [28, 52]),
    ("Lumbar muscle line (other side)", 1, [69, 62]),
], "Lumbar musculature · lateral + ventrodorsal", "Lateral on the left (cranial = left), ventrodorsal on the right. Name the muscle groups and the lines they make."))

# Slide 25: diaphragm (yellow dashed = cupola + crura on the ventrodorsal, thoracic surface on the lateral)
B25 = [(164, 291, 666, 534), (696, 8, 904, 534)]
cards.append(card('l25lab_diaphragm', [panel(25, (1369, 661), B25[0]), panel(25, (557, 1408), B25[1])], [
    ("Cupola — the dome in the middle", 0, pt(B25[0], 396, 389)),
    ("Right crus", 0, pt(B25[0], 295, 443)),
    ("Left crus", 0, pt(B25[0], 525, 428)),
    ("Diaphragm, thoracic surface — seen because gas in the lung outlines it", 1, pt(B25[1], 785, 237)),
    ("Liver — border-effaces with the abdominal side of the diaphragm", 1, [72, 62]),
], "Diaphragm · ventrodorsal + lateral", "Ventrodorsal on the left (patient's right = viewer's left), lateral on the right. Name the three parts, then why only one surface shows."))

# Slide 26: the two exceptions (blue arrows on the slide)
B26 = [(315, 312, 500, 540), (536, 27, 878, 426)]
cards.append(card('l25lab_exceptions', [panel(26, (142, 168), B26[0]), panel(26, (941, 1267), B26[1])], [
    ("Abdominal surface of the diaphragm — seen because of excessive falciform fat (a variant of normal)", 0, pt(B26[0], 358, 414)),
    ("Falciform fat", 0, [36, 62]),
    ("Diaphragm, both surfaces outlined — thoracic side by lung gas, abdominal side by free gas", 1, pt(B26[1], 620, 188.6)),
    ("Free peritoneal gas (ruptured bowel) — pathologic unless introduced, e.g. after surgery", 1, [27.5, 47]),
], "Diaphragm exceptions · lateral views", "Zoomed cat on the left, dog on the right (cranial = left). Why can you see the abdominal side of the diaphragm in each?"))

# Slide 44: liver outline (blue fill) and gastric axis (blue line), left dog only
B44 = (321, 109, 639, 431)
cards.append(card('l25lab_liver', [panel(44, (1186, 1206), B44)], [
    ("Liver", 0, pt(B44, 388.8, 324)),
    ("Diaphragm — cranial border of the liver", 0, [12, 50]),
    ("Caudoventral margin of the liver — easiest to see; dogs: left lateral lobe (cats: right lateral lobe)", 0, [40, 77]),
    ("Gastric axis — fundus to pylorus; normal = between perpendicular to the spine and parallel to the ribs", 0, pt(B44, 421, 233)),
    ("Falciform fat — ventral border of the liver", 0, [27, 89]),
], "Liver & gastric axis · dog, lateral", "Cranial = left. Outline the liver, name its borders, then draw the line used to judge liver size.", height=1000))

# Slide 46: splenic head in a cat (blue boxes on the slide)
B46 = [(331, 0, 617, 369), (593, 65, 960, 259)]
cards.append(card('l25lab_spleen', [panel(46, (793, 1026), B46[0]), panel(46, (752, 398), B46[1])], [
    ("Head of the spleen — immobile, left cranial abdomen (attached to the stomach by the gastrosplenic ligament)", 0, pt(B46[0], 547.5, 116.5)),
    ("Head of the spleen — fusiform soft tissue on the lateral; cats show it because they put fat there", 1, pt(B46[1], 735, 139)),
], "Spleen · cat, ventrodorsal + lateral", "Ventrodorsal on the left (patient's left = viewer's right), lateral on the right. Find the immobile part of the spleen in both."))

# Slide 53: kidneys on the ventrodorsal (blue fills + double arrow on the slide)
B53 = (467, 3, 917, 540)
cards.append(card('l25lab_kidneys', [panel(53, (1278, 1525), B53)], [
    ("Right kidney — cranial; sits in the renal fossa of the caudate lobe of the liver", 0, pt(B53, 617.8, 270)),
    ("Left kidney — more caudal (\"left is left behind\")", 0, pt(B53, 777.6, 313.2)),
    ("Second lumbar vertebra — kidney length: dogs 2.5 to 3.5 times its length, cats 2 to 3 times", 0, pt(B53, 681.8, 266.4)),
], "Kidneys · ventrodorsal", "Cranial = top, patient's right = viewer's left. Name each kidney and the ruler used to size them.", height=1000))

# Slides 56 + 57: retroperitoneal vessels (yellow arrows on the slides)
B56, B57 = (248, 17, 809, 529), (226, 116, 734, 540)
cards.append(card('l25lab_retro', [panel(56, (1108, 1010), B56), panel(57, (1114, 930), B57)], [
    ("Aorta — in the retroperitoneal space", 0, pt(B56, 637.2, 217.4)),
    ("Deep circumflex iliac arteries — seen end-on as round dots; sometimes mistaken for lymph nodes", 1, pt(B57, 573.8, 277.2)),
], "Retroperitoneal space · lateral views", "Two dogs, cranial = left. Name the vessel running under the spine, then the round dots near the end of it."))

# Slide 58: urinary bladder regions (blue / yellow / red fills on the slide)
B58 = (427, 270, 810, 525)
cards.append(card('l25lab_bladder', [panel(58, (344, 229), B58)], [
    ("Apex (blue on the slide)", 0, [48.4, 52.3]),
    ("Body (yellow)", 0, [59.2, 50.1]),
    ("Neck / trigone (red)", 0, [71.4, 43.1]),
], "Urinary bladder · lateral", "Cranial = left. The bladder extends cranially from the pelvic canal. Name its three regions.", height=800))

# Slide 65: stomach regions (C / F / B / P letters are slide text)
B65 = [(235, 171, 670, 497), (646, 71, 960, 523)]
cards.append(card('l25lab_stomach', [panel(65, (1344, 1010), B65[0]), panel(65, (871, 1254), B65[1])], [
    ("Cardia", 0, pt(B65[0], 560.5, 269.5)), ("Fundus", 0, pt(B65[0], 568.5, 337.5)),
    ("Body", 0, pt(B65[0], 500.5, 371)), ("Pylorus", 0, pt(B65[0], 420.5, 371)),
    ("Cardia", 1, pt(B65[1], 840, 164)), ("Fundus", 1, pt(B65[1], 841.5, 212)),
    ("Body", 1, pt(B65[1], 777.5, 197)), ("Pylorus", 1, pt(B65[1], 724.5, 164)),
], "Stomach regions · dog, ventrodorsal", "Barium study on the left, plain film on the right; patient's left = viewer's right. Name the four regions on each."))

# Slide 67: right vs left lateral, gas only (F / D / P letters are slide text; captions under the images)
B67 = [(427, 121, 690, 486), (700, 111, 945, 507)]
cards.append(card('l25lab_rl_lateral', [panel(67, (730, 1014), B67[0]), panel(67, (679, 1100), B67[1])], [
    ("Fundus — gas-filled", 0, pt(B67[0], 570, 231)),
    ("Duodenum — gas-filled", 1, pt(B67[1], 857, 241.5)),
    ("Pylorus — gas-filled", 1, pt(B67[1], 850.5, 319)),
    ("Right lateral — fundus is a left-sided structure, so it is up and fills with gas", 0, [50, 95]),
    ("Left lateral — pylorus and duodenum are right-sided, so they are up and fill with gas", 1, [50, 95]),
], "Fundus vs pylorus · two laterals", "Same dog twice, cranial = left. Name each gas-filled region, then name which lateral each image is."))

# Slide 69: dorsoventral vs ventrodorsal barium study (letters burned into the images, inpainted here)
B69 = [(66, 173, 503, 528), (550, 42, 922, 540)]
cards.append(card('l25lab_vd_dv', [
    panel(69, (606, 493), B69[0], [(15.5, 36.5, 21.5, 46.5), (43, 38.5, 49, 47.5), (59, 38.5, 65, 47.5), (91, 47.5, 96, 56.5)]),
    panel(69, (517, 692), B69[1], [(7, 20.5, 14, 29.5), (32, 26.5, 39, 35.5), (45, 23.5, 52, 32.5), (71.5, 27.5, 77.5, 36.5)])], [
    ("Duodenum", 0, [18.3, 41.5]), ("Pylorus — ventral: holds barium on the dorsoventral", 0, [45.8, 43]),
    ("Body — ventral: holds barium on the dorsoventral", 0, [62, 43]), ("Fundus — dorsal: holds gas on the dorsoventral", 0, [93.3, 52]),
    ("Duodenum", 1, [10.5, 25]), ("Pylorus — ventral: holds gas on the ventrodorsal", 1, [35.5, 31]),
    ("Body — ventral: holds gas on the ventrodorsal", 1, [48.5, 28]), ("Fundus — dorsal: fills with barium on the ventrodorsal", 1, [74.5, 32]),
    ("Dorsoventral (left image) — on its sternum", 0, [50, 5]), ("Ventrodorsal (right image) — on its back", 1, [50, 4]),
], "Fundus vs pylorus · dorsoventral vs ventrodorsal", "Barium study, cranial = top. Name each region on both, then decide which image is which view."))

# Slide 76: dog cecum (blue ellipses on the slide)
B76 = [(209, 254, 616, 540), (625, 75, 943, 540)]
cards.append(card('l25lab_cecum', [panel(76, (1129, 794), B76[0]), panel(76, (997, 1460), B76[1])], [
    ("Cecum — C-shaped, compartmentalized, usually gas-filled; sometimes confused for abnormal small intestine", 0, pt(B76[0], 456.5, 347)),
    ("Cecum — right mid abdomen", 1, pt(B76[1], 710.6, 313.2)),
], "Large intestine · dog cecum", "Lateral on the left (cranial = left), ventrodorsal on the right (patient's right = viewer's left). Find the corkscrew gas structure."))

# Slides 91 + 92: prostate and medial iliac lymph nodes (lines / yellow triangle / dashed outline on the slides)
B91, B92 = (439, 217, 780, 530), (144, 277, 469, 530)
cards.append(card('l25lab_caudal', [panel(91, (1502, 1376), B91), panel(92, (902, 702), B92, [(91, 3, 99, 9)])], [
    ("Triangle of fat — separates the prostate from the bladder and ventral body wall; important landmark", 0, pt(B91, 651.6, 381.6)),
    ("Prostate — intact male; should be under 70% of the height of the pelvic inlet", 0, pt(B91, 662, 323)),
    ("Urinary bladder", 0, [48, 58]),
    ("Medial iliac lymph nodes (enlarged here) — ventral to the sixth and seventh lumbar vertebrae, dorsal to the descending colon; not seen in health", 1, pt(B92, 389, 380)),
], "Caudal abdomen · prostate & medial iliac lymph nodes", "Two male dogs, lateral, cranial = left. Name the landmark fat, the gland it outlines, then the abnormal mass under the spine."))

TEXTS = [
    ("Opacities: least → most opaque", ["Gas (black)", "Fat (darker grey)", "Soft tissue and fluid (same medium grey)", "Mineral (white)", "Metal (very white)"]),
    ("Dr. McHaney's systematic order for an abdomen", [
        "Extra-abdominal structures: non-abdominal soft tissues, body wall, diaphragm, skeleton, thorax",
        "Serosal detail and abdominal contour", "Large parenchymal organs: liver and spleen",
        "Urogenital: kidneys, urinary bladder, reproductive tract", "Gastrointestinal tract LAST: stomach, small intestine, colon"]),
    ("Standard views, then optional views + why", [
        "Standard: left lateral, right lateral, ventrodorsal (two orthogonal views minimum)",
        "Compression view: reduces superimposition over an area of interest",
        "Pneumogastrogram / pneumocolonogram: air outlines the stomach or colon",
        "Lateral with pelvic limbs pulled forward (perineal view): region of the urethra, urinary stones",
        "Horizontal beam: highlights free gas"]),
    ("Where gas goes on each view (barium does the opposite)", [
        "Right lateral: gas in the fundus · barium in the pylorus and duodenum",
        "Left lateral: gas in the pylorus and duodenum · barium in the fundus",
        "Ventrodorsal: gas in the body and pylorus · barium in the fundus",
        "Dorsoventral: gas in the fundus · barium in the body and pylorus"]),
]

T.write('gross-anatomy-l25-labels.html', 'Read the Radiograph · Abdomen',
        'Lecture 25 · Dr. McHaney · normal radiographic anatomy · tap to reveal in order', cards, texts=TEXTS)
print('ok', len(cards), sum(len(c['labels']) for c in cards), len(TEXTS), sum(len(a) for _, a in TEXTS))
