# L26 Pelvic Limb Vessels & Nerves · "Trace It" deck (made by Claude). Dr. Malreddy's slides (Lecture 26, 10/26/26).
# SLIDES ONLY so far — names are checked against the slide text; the transcript arrives after Monday's lecture.
# Run from repo root: python3 tools/l26trace.py "/path/to/Lecture 26 Pelvic Limb Vessels and Nerves - Tagged.pdf"
# Technique: same as tracer.vector_card (slide text is vector, so label boxes come from pdftotext -bbox in PDF points),
# but each label carries its own erase test (black text, red text, coloured list text) and the crop keeps the left
# labels that sit closer to the purple bar than tracer's 88 pt default. Slide 21 (plexus) is a raster figure: its label
# boxes are pixel boxes on a 220 dpi page render (found with tesseract, then hand-tightened).
# Text after ' — ' in a name is a note: shown in the reveal list, kept off the badge.
import cv2, sys, os, subprocess, numpy as np
sys.path.insert(0, os.path.dirname(__file__)); import tracer as T
pdf = sys.argv[1]; TMP = '/tmp/claude-0/l26'; os.makedirs(TMP, exist_ok=True)
SEP = ' — '
dark = lambda s: s.max(2) < 120
red = lambda s: (s[..., 2] > 150) & (s[..., 1] < 140) & (s[..., 0] < 140)
dark_or_red = lambda s: dark(s) | red(s)
ink = lambda s: s.min(2) < 200            # any coloured text (lymph-node list)

def render(page, dpi):
    out = f'{TMP}/p{page}_{dpi}'
    if not os.path.exists(out + '.png'):
        subprocess.run(['pdftoppm', '-r', str(dpi), '-png', '-f', str(page), '-l', str(page), '-singlefile', pdf, out], check=True)
    return cv2.imread(out + '.png')

def finish(im, ox, oy, S, out, labels, title, hint, auto=True):
    """Crop to content, save, and turn label boxes into % positions."""
    ys, xs = np.where(im.astype(int).sum(2) < 690)
    for nm, bs, *_ in labels:     # erased labels count as content, so the crop never cuts a label off
        for b in bs:
            xs = np.append(xs, [int(b[0] * S - ox), int(b[2] * S - ox)]); ys = np.append(ys, [int(b[1] * S - oy), int(b[3] * S - oy)])
    xs, ys = xs.clip(0, im.shape[1] - 1), ys.clip(0, im.shape[0] - 1)
    cx0, cy0 = (max(0, xs.min() - 24), max(0, ys.min() - 24)) if auto else (0, 0)
    cx1, cy1 = (min(im.shape[1], xs.max() + 24), min(im.shape[0], ys.max() + 24)) if auto else im.shape[1::-1]
    im = im[cy0:cy1, cx0:cx1]; H, W = im.shape[:2]
    cv2.imwrite(f'assets/{out}.jpg', im, [cv2.IMWRITE_JPEG_QUALITY, 88])
    res = []
    for nm, bs, *_ in labels:
        b = T.union(bs)
        b = (b[0] * S - ox - cx0, b[1] * S - oy - cy0, b[2] * S - ox - cx0, b[3] * S - oy - cy0)
        d = dict(n=nm, p=T.pos(b, H, W))
        if SEP in nm: d['s'] = nm.split(SEP)[0]
        res.append(d)
    return dict(title=title, q=hint, img=f'assets/{out}.jpg', labels=res)

def vcard(page, out, labels, title, hint, top=62, left=64, bottom=None, dpi=200):
    """labels: [(name, [boxes in PDF points], test?)] in reveal order."""
    S = dpi / 72; im = render(page, dpi).copy(); pad = 3
    for nm, bs, *t in labels:
        test = t[0] if t else dark
        im = T.erase(im, [((b[0] - pad) * S, (b[1] - pad) * S, (b[2] + pad) * S, (b[3] + pad) * S) for b in bs], test)
    grey = lambda x: (x.max(2) < 225) & (x.min(2) > 100) & ((x.max(2) - x.min(2)) < 25)
    im = T.erase(im, [(90 * S, 0, 640 * S, 61 * S)], grey)                       # grey slide title
    x = im[int(366 * S):, int(600 * S):]; x[x.min(2) < 250] = 255                # K-State footer logo
    y1 = int((bottom or 404) * S)
    body = im[int(top * S):y1, int(left * S):]
    return finish(body, int(left * S), int(top * S), S, out, labels, title, hint)

def rcard(page, out, labels, title, hint, crop, dpi=220):
    """Raster slide: labels [(name, [pixel boxes on the dpi render])]; crop = (x0, y0, x1, y1) pixels."""
    im = render(page, dpi).copy()
    for _, bs, *_ in labels:      # raster text leaves JPEG ghosts: whiten every unsaturated pixel in the box
        for x0, y0, x1, y1 in bs:
            sub = im[y0:y1, x0:x1]; c = sub.astype(int); sub[(c.max(2) - c.min(2)) < 45] = 255
    c = im.astype(int); im[(c.min(2) > 200) & ((c.max(2) - c.min(2)) < 45)] = 255   # flatten JPEG background noise
    x0, y0, x1, y1 = crop
    return finish(im[y0:y1, x0:x1], x0, y0, 1, out, labels, title, hint, auto=False)

cards = []
# ── Slide 5: aorta → popliteal (the big one)
cards.append(vcard(5, 'l26_arteries_prox', [
    ("Abdominal aorta", [(134, 51, 289, 69)]),
    ("Internal iliac a. (one side)", [(339, 46, 407, 57)]),
    ("Median sacral a.", [(340, 66, 414, 76)]),
    ("Internal iliac a. (other side)", [(340, 86, 408, 97)]),
    ("External iliac a.", [(109, 86, 253, 104)]),
    ("Deep femoral a. — leaves the external iliac BEFORE the vascular lacuna", [(270, 80, 300, 105), (283, 95, 322, 117)]),
    ("Pudendoepigastric trunk — 1st branch of the deep femoral", [(337, 131, 471, 143)]),
    ("Caudal epigastric a. — from the pudendoepigastric trunk", [(307, 163, 342, 175), (307, 176, 370, 188)]),
    ("External pudendal a. — from the pudendoepigastric trunk", [(363, 153, 404, 165), (363, 166, 423, 178)]),
    ("Medial circumflex femoral a. — continuation of the deep femoral", [(331, 104, 484, 116)]),
    ("Obturator branch — of the medial circumflex femoral", [(460, 70, 549, 83)]),
    ("Transverse branch — of the medial circumflex femoral", [(523, 95, 631, 109)]),
    ("Deep branch — of the medial circumflex femoral", [(485, 172, 559, 185)]),
    ("Vascular lacuna — external iliac a. becomes femoral a. here (green circle)", [(130, 105, 215, 117)]),
    ("Femoral a.", [(157, 124, 251, 141)]),
    ("Superficial circumflex iliac a.", [(82, 198, 249, 212)]),
    ("Lateral circumflex femoral a.", [(354, 192, 520, 206)]),
    ("Proximal caudal femoral a.", [(357, 228, 521, 242)]),
    ("Descending genicular a.", [(99, 266, 239, 280)]),
    ("Saphenous a.", [(143, 311, 264, 327)]),
    ("Cranial branch — of the saphenous a.", [(160, 365, 234, 377)]),
    ("Caudal branch — of the saphenous a.", [(237, 386, 311, 398)]),
    ("Middle caudal femoral a.", [(363, 268, 514, 282)]),
    ("Distal caudal femoral a. — last femoral branch", [(381, 327, 527, 341)]),
    ("Popliteal a. — femoral a. renamed after the distal caudal femoral", [(324, 358, 432, 376)]),
], "Slide 5 · Aorta → popliteal artery", "Cranial = left. Start at the aorta and name every vessel down to the popliteal. Purple triangle = femoral triangle.", top=40))

# ── Slide 6: popliteal → deep plantar arch
cards.append(vcard(6, 'l26_arteries_dist', [
    ("Popliteal a.", [(353, 82, 456, 99)]),
    ("Caudal tibial a. — small branch, goes caudal", [(359, 135, 450, 149)]),
    ("Cranial tibial a. — the popliteal's main continuation", [(95, 208, 262, 227)]),
    ("Dorsal pedal a. — cranial tibial renamed at the tarsus", [(361, 253, 508, 270)]),
    ("Arcuate a. — the dorsal pedal ends as this (lecture)", [(160, 271, 214, 286), (160, 287, 202, 303)]),
    ("Dorsal metatarsal a. II", [(173, 383, 321, 399)]),
    ("Perforating metatarsal a. — from dorsal metatarsal a. II, between MT II and III; perforates dorsal → plantar (lecture)", [(329, 326, 576, 343)]),
    ("Deep plantar arch", [(411, 382, 586, 399)]),
], "Slide 6 · Popliteal → deep plantar arch", "Keep going from the popliteal artery down to the paw."))

# ── Slide 7: the four metatarsal/digital sets
cards.append(vcard(7, 'l26_arteries_paw', [
    ("Dorsal common digital arteries — dorsal, superficial", [(167, 325, 233, 395)]),
    ("Dorsal metatarsal arteries — dorsal, deep", [(260, 325, 343, 378)]),
    ("Plantar metatarsal arteries — plantar, deep", [(386, 325, 468, 379)]),
    ("Plantar common digital arteries — plantar, superficial", [(491, 325, 557, 396)]),
], "Slide 7 · Arteries of the paw", "Dorsal on the left, plantar on the right. Name each set: superficial vs deep."))

# ── Slide 10: deep veins (dorsal recumbency: dog's right on the left)
cards.append(vcard(10, 'l26_veins_deep', [
    ("Femoral v. (right)", [(147, 302, 231, 317)]),
    ("Vascular lacuna (right)", [(144, 256, 194, 270), (144, 271, 182, 284)]),
    ("External iliac v. (right)", [(196, 207, 280, 223), (225, 224, 252, 239)]),
    ("Common iliac v. (right)", [(212, 161, 306, 176), (244, 178, 274, 193)]),
    ("Femoral v. (left)", [(446, 302, 530, 317)]),
    ("Vascular lacuna (left)", [(456, 261, 506, 275), (456, 275, 494, 289)]),
    ("Deep femoral veins", [(304, 292, 382, 306), (328, 306, 358, 320)]),
    ("External iliac v. (left)", [(402, 207, 486, 223), (430, 224, 458, 239)]),
    ("Internal iliac veins", [(308, 241, 380, 255), (329, 256, 359, 270)]),
    ("Common iliac v. (left)", [(378, 161, 473, 176), (411, 177, 440, 193)]),
    ("Caudal vena cava", [(274, 79, 421, 98)]),
], "Slide 10 · Deep venous system", "Dorsal recumbency (R on the left). Drain it: femoral vein up to the caudal vena cava."))

# ── Slide 11: lateral saphenous (dog venipuncture)
cards.append(vcard(11, 'l26_veins_lat', [
    ("Cranial branch — of the lateral saphenous v.", [(413, 284, 530, 303)]),
    ("Caudal branch — of the lateral saphenous v.", [(208, 280, 324, 298)]),
    ("Lateral saphenous v.", [(131, 185, 290, 206), (192, 207, 228, 228)]),
    ("Venipuncture site in the DOG — red arrow", [(372, 231, 576, 250)]),
    ("Popliteal lymph node — green dot", [(180, 115, 257, 130)]),
    ("Distal caudal femoral v. — what the lateral saphenous drains into", [(296, 75, 531, 100)]),
], "Slide 11 · Superficial veins · lateral surface, right pelvic limb", "Lateral view, cranial = right. Name the vein, its branches, what it drains into, and why it matters."))

# ── Slide 13: medial saphenous (cat venipuncture)
cards.append(vcard(13, 'l26_veins_med', [
    ("Cranial branch — of the medial saphenous v.", [(286, 311, 342, 350)]),
    ("Caudal branch — of the medial saphenous v.", [(445, 311, 501, 350)]),
    ("Medial saphenous v.", [(191, 198, 390, 219)]),
    ("Venipuncture site in the CAT — red arrow", [(460, 198, 659, 216)]),
    ("Femoral v. — what the medial saphenous drains into (femoral triangle)", [(391, 59, 500, 78)]),
], "Slide 13 · Superficial veins · medial surface", "Medial view, cranial = left. Name the vein, its branches, what it drains into, and which species it's for.", top=57))

# ── Slide 16: lymph nodes
cards.append(vcard(16, 'l26_lymph', [
    ("Popliteal lymph node — constant, palpable", [(242, 286, 301, 299)]),
    ("Superficial inguinal lymph node — constant, palpable", [(72, 184, 184, 197)]),
    ("Femoral lymph node — inconstant (open circle)", [(171, 204, 228, 216)]),
    ("Iliofemoral (deep inguinal) lymph node — inconstant (open circle)", [(234, 117, 304, 130)]),
    ("Medial iliac lymph node — constant; the single terminal node", [(99, 118, 171, 130)]),
    ("Cisterna chyli (CH) — medial iliac drains here", [(105, 87, 119, 98)]),
    ("Deep circumflex iliac a. (D.C.I. a.) — landmark", [(119, 109, 154, 120)], red),
    ("Abdominal aorta", [(109, 71, 193, 84)], red),
    ("External iliac a.", [(200, 72, 214, 87), (207, 81, 222, 96), (215, 90, 230, 105), (222, 99, 242, 120)], red),
    ("CONSTANT: popliteal (palpable), superficial inguinal (palpable), medial iliac", [(380, 82, 682, 197)], ink),
    ("INCONSTANT: iliofemoral (deep inguinal), femoral", [(380, 216, 671, 299)], ink),
    ("SINGLE TERMINAL NODE: medial iliac", [(380, 319, 655, 371)], ink),
], "Slide 16 · Lymphatics of the pelvic limb", "Filled dot = constant node, open circle = inconstant. Name each node, then say the three lists on the right."))

# ── Slide 21: lumbosacral plexus (raster figure)
cards.append(rcard(21, 'l26_plexus', [
    ("Ilioinguinal n. (L3)", [(1595, 440, 1775, 535)]),
    ("Lateral cutaneous femoral n. (L3–L4)", [(1450, 535, 1805, 625)]),
    ("Genitofemoral n. (L3–L4)", [(1305, 655, 1540, 745)]),
    ("Femoral n. (L4–L6)", [(1160, 730, 1300, 855)]),
    ("Obturator n. (L4–L6)", [(970, 483, 1195, 570)]),
    ("Sciatic n. (L6–L7–S1)", [(1010, 585, 1190, 712)]),
    ("Proximal caudal cutaneous sural n. (L6–L7–S1)", [(460, 655, 740, 785)]),
    ("Lateral cutaneous sural n. (L6–L7)", [(345, 925, 660, 1010)]),
    ("Distal caudal cutaneous sural n. (L7–S1)", [(415, 1040, 810, 1125)]),
    ("Tibial n. (L6–L7–S1)", [(865, 1108, 1060, 1195)]),
    ("Superficial fibular n. (L6–L7)", [(1075, 908, 1365, 1000)]),
    ("Deep fibular n. (L6–L7)", [(1075, 1015, 1300, 1100)]),
    ("Caudal cutaneous femoral n. (S1–S2)", [(380, 540, 745, 625)]),
    ("Dorsal n. of the penis (S1–S2)", [(425, 430, 715, 515)]),
    ("Pudendal n. (S1–S3) — ✅ corrected in lecture 10/26: slide 21 mislabels it 'superficial fibular'", [(430, 325, 715, 410)]),
], "Slide 21 · Lumbosacral plexus", "Segments L3 (right) to S3 (left) along the top. Name each nerve, cranial to caudal. Dr. Malreddy: memorize this figure; segments are NOT tested.",
    crop=(300, 214, 1830, 1210)))

# ── Slide 24: testing sites for cutaneous nerves
cards.append(vcard(24, 'l26_testing', [
    ("Lateral cutaneous femoral n.", [(81, 132, 209, 148), (81, 149, 154, 165)]),
    ("4 cm cranial to the greater trochanter", [(91, 357, 201, 371), (91, 372, 197, 386)], ink),
    ("Genitofemoral n.", [(220, 157, 340, 172)]),
    ("Femoral triangle", [(223, 353, 318, 367)], ink),
    ("Saphenous n.", [(368, 158, 464, 174)]),
    ("4 cm distal to the medial epicondyle of the femur", [(350, 345, 431, 359), (350, 359, 456, 373), (350, 374, 423, 388)], ink),
    ("Sciatic n.", [(489, 146, 552, 162)]),
    ("Midlateral leg at the level of the tibial tuberosity", [(480, 354, 579, 368), (480, 368, 581, 382), (480, 383, 587, 397)], ink),
    ("Caudal cutaneous femoral n.", [(637, 36, 687, 51), (637, 52, 711, 68), (637, 70, 710, 85)]),
    ("4 cm distal to the ischiatic tuberosity", [(600, 327, 680, 340), (600, 341, 710, 355)], ink),
], "Slide 24 · Testing sites for cutaneous nerves", "Blue dot = testing site. Name the nerve, then say where you test it.", top=30, bottom=402))

texts = [
    ("Main arterial chain, aorta to paw (slide 4; lecture adds arcuate → dorsal metatarsal II before the perforating)", ["Abdominal aorta", "External iliac a.", "Femoral a.", "Popliteal a.", "Cranial tibial a.",
        "Dorsal pedal a.", "Perforating metatarsal a.", "Deep plantar arch", "Plantar metatarsal arteries"]),
    ("Deep femoral artery: its two branches and their branches (slide 5)", ["Pudendoepigastric trunk → caudal epigastric a. + external pudendal a.",
        "Medial circumflex femoral a. → obturator, transverse and deep branches"]),
    ("Femoral artery branches, proximal → distal (slide 5 drawing)", ["Superficial circumflex iliac a.", "Lateral circumflex femoral a.",
        "Proximal caudal femoral a.", "Descending genicular a.", "Saphenous a. (cranial + caudal branches)", "Middle caudal femoral a.",
        "Distal caudal femoral a. → then it's the popliteal a."]),
    ("Superficial vs deep venous system (slide 9)", ["Superficial: lateral saphenous v. + medial saphenous v.", "Deep: deep femoral v. + femoral v."]),
    ("Deep venous drainage, femoral v. → heart (slide 10)", ["Femoral v.", "through the vascular lacuna", "External iliac v.",
        "Common iliac v. (internal iliac v. joins)", "Caudal vena cava"]),
    ("Venipuncture: dog vs cat (slides 11, 13)", ["DOG: cranial branch of the lateral saphenous v. (lateral surface)", "CAT: medial saphenous v. (medial surface)"]),
    ("Lymph nodes of the pelvic limb (slide 16)", ["Constant: popliteal (palpable), superficial inguinal (palpable), medial iliac",
        "Inconstant: iliofemoral (deep inguinal), femoral", "Single terminal node: medial iliac", "Slide 17 lymphangiogram: popliteal → medial iliac → cisterna chyli → thoracic duct"]),
    ("Lumbosacral plexus: what makes it? (slide 20)", ["Ventral branches of spinal nerves L3–S3 (dog)", "Supplies the nerves to the pelvic limb muscles"]),
    ("Nerve → muscles (slide 22)", ["Femoral (L4–6): iliopsoas, quadriceps, sartorius", "Obturator ((L4), 5, 6): external obturator, pectineus, gracilis, adductor",
        "Cranial gluteal (L6, 7, S1): middle gluteal, deep gluteal, tensor fasciae latae", "Caudal gluteal (L7, (S1, 2)): superficial gluteal (middle gluteal)",
        "Sciatic (L6, 7, S1, (2)): biceps femoris, semimembranosus, semitendinosus",
        "Common peroneal = common fibular: peroneus (fibularis) longus, lateral digital extensor, long digital extensor, cranial tibial",
        "Tibial: gastrocnemius, popliteus, superficial digital flexor, deep digital flexor", "Pudendal (S1, 2, 3) → caudal rectal n.: external anal sphincter"]),
]

T.write('gross-anatomy-l26-trace.html', '🧭 L26 Trace It · Pelvic Limb Vessels & Nerves',
        'Slides + lecture 10/26 · names pop up in order · then the chain lists', cards, texts, back='gross-anatomy-exam4.html')
print(len(cards), 'image cards,', sum(len(c['labels']) for c in cards), 'labels;', len(texts), 'chain cards')
p = 'gross-anatomy-l26-trace.html'; txt = open(p).read(); open(p, 'w').write(txt.replace('← Back to Lecture', '← Back to Exam 4'))
