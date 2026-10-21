# Lecture 22 Urinary System · "Label It" deck (made by Claude). Names checked against the L22 transcript.
# Run from repo root: python3 tools/l22labels.py /path/to/Lecture_22_Urinary_System.pptx   (converted with soffice → PDF)
import sys, os, subprocess, shutil
sys.path.insert(0, os.path.dirname(__file__)); import tracer as T, labelkit as K
src = sys.argv[1]; TMP = '/tmp/claude-0/l22lab'; os.makedirs(TMP, exist_ok=True)
pdf = f'{TMP}/L22.pdf'
if src.endswith('.pdf'): pdf = src
elif not os.path.exists(pdf):
    shutil.copy(src, f'{TMP}/L22.pptx')
    subprocess.run(['soffice', '--headless', '--convert-to', 'pdf', '--outdir', TMP, f'{TMP}/L22.pptx'], check=True, capture_output=True)
P = lambda n: K.page_png(pdf, n, TMP)
c = lambda b: ((b[0] + b[2]) / 2, (b[1] + b[3]) / 2)
sat = lambda s: (s.max(2).astype(int) - s.min(2)) > 60
cards = []

# Slide 3: urinary system overview, sagittal (lecture: "ureters, that's number 2"; "the urethra joins, number 10")
im = P(3)
N3 = {1: (930, 382, 962, 422), 2: (1292, 478, 1324, 517), 3: (1452, 747, 1485, 787), 4: (1260, 503, 1290, 542), 5: (1042, 488, 1074, 527),
      6: (1349, 488, 1381, 527), 7: (1617, 632, 1648, 668), 8: (1697, 587, 1728, 623), 9: (1652, 620, 1683, 657), 10: (1858, 623, 1901, 660),
      11: (1860, 882, 1895, 919), 12: (1941, 750, 1982, 786), 13: (1561, 892, 1603, 930), 14: (1738, 472, 1785, 512)}
inner = [1, 3, 8, 14]  # digits drawn on top of coloured organs
K.inpaint(im, [N3[k] for k in inner], lambda s: K.dark(s, 120), grow=2, radius=5, grain=5)
K.whiten(im, [N3[k] for k in N3 if k not in inner], lambda s: K.dark(s, 140), halo=2)
K.whiten(im, [(860, 520, 1110, 1040), (1110, 575, 1240, 1040), (1250, 1090, 1600, 1110)], lambda s: K.dark(s, 140), halo=2)  # slide text, copyright
K.whiten(im, [(1110, 528, 1180, 575)], lambda s: K.dark(s, 90), halo=1, near=False)  # end of "pelvic" beside the ovarian bursa
cards.append(K.card(im, 'l22lab_overview', (865, 185, 1990, 1060), [
    ("Kidney", c(N3[1])), ("Ureter (enters the dorsal aspect of the bladder)", c(N3[2])), ("Urinary bladder", c(N3[3])),
    ("Urethra", c(N3[9])),
    ("Number 10: the lecture called it the vagina (the urethra joins the female tract here; slide legend not shown, see notes)", c(N3[10])),
], "Urinary system overview · female, sagittal", "Cranial = left. Kidney → ? → ? → ? Name the path urine takes."))

# Slide 6: transverse section through the lumbar region (dorsal = top)
im = P(6)
N6 = {1: (1588, 556, 1614, 592), 2: (1467, 455, 1494, 488), 3: (1722, 510, 1750, 545)}
K.inpaint(im, [N6[1]], lambda s: K.dark(s, 120), grow=2, radius=5)
K.whiten(im, [N6[2], N6[3]], lambda s: K.dark(s, 140), halo=2)
K.whiten(im, [(1192, 195, 1277, 440)], lambda s: K.dark(s, 140), halo=1, near=False)  # ends of slide bullets
cards.append(K.card(im, 'l22lab_transverse', (1192, 195, 1995, 1082), [
    ("Right kidney", c(N6[2])), ("Left kidney", c(N6[3])),
    ("Parietal peritoneum: covers only the VENTRAL surface → kidneys are retroperitoneal", (1920, 770)),
], "Kidneys in a transverse section · lumbar region", "Dorsal = top, R and L are the dog's sides. Pressed against the abdominal roof: which side is which?", white=True))

# Slide 7: dog on its back, roof of the abdomen (cranial = top). Yellow 'left kidney' tag erased.
im = P(7)
K.inpaint(im, [(1922, 520, 1960, 630)], K.yellow, grow=3, radius=7, grain=6)
K.fill(im, [(1440, 70, 1555, 450)], (255, 255, 255))  # slide title + bullet ends
cards.append(K.card(im, 'l22lab_location', (1440, 70, 1990, 1020), [
    ("Right kidney (more cranial by about half a kidney length; T13/L1 to L3)", (1675, 505)),
    ("Left kidney (L2 to L4)", (1870, 540)),
    ("Caudal vena cava (medial border of the kidney faces it and the aorta)", (1755, 640)),
], "Kidney location · dorsal abdominal wall, cadaver", "Cranial = top. Which kidney is more cranial, and by how much?", white=True))

# Slide 10: Budras sagittal section (lecture: "that's number 5" = ureter; 3 = renal artery + renal vein)
im = P(10)
N10 = {18: (1806, 202, 1860, 248), 16: (1866, 290, 1922, 334), 19: (1836, 408, 1888, 456), 14: (1622, 482, 1678, 532),
       11: (1692, 587, 1742, 637), 5: (1472, 702, 1507, 748)}
K.inpaint(im, list(N10.values()), lambda s: K.dark(s, 120), grow=2, radius=6, grain=5)
K.fill(im, [(1360, 1010, 1440, 1045)], (255, 255, 255))  # "Budras"
cards.append(K.card(im, 'l22lab_sagittal', (1412, 185, 1998, 1060), [
    ("Renal artery (enters at the hilus)", (1470, 585)), ("Renal vein (leaves at the hilus)", (1468, 655)),
    ("Ureter (number 5 in lecture)", c(N10[5])),
    ("Renal hilus (indented medial border = the garage door)", (1575, 600)),
    ("Renal sinus (the space/garage; filled with fat)", c(N10[14])),
    ("Renal pelvis (funnel-shaped dilation of the ureter)", c(N10[11])),
    ("Pelvic recess (diverticulum of the pelvis between pyramids)", (1780, 432)),
], "Kidney · sagittal section (Budras)", "Medial border = left. What goes through the hilus, and what sits in the sinus?", white=True))

# Slide 11: corrosion cast of the renal pelvis
im = P(11)
K.whiten(im, [(1345, 55, 1520, 150)], lambda s: ((s.max(2).astype(int) - s.min(2)) < 40) & (s.min(2) < 235), halo=2)  # end of the slide title
cards.append(K.card(im, 'l22lab_cast', (1345, 75, 1990, 1000), [
    ("Renal pelvis (yellow cast)", (1690, 610)), ("Pelvic recesses (5–6 from each border; the 'rivers' feeding the pelvis)", (1580, 450)),
    ("Ureter", (1915, 850)), ("Renal vessels (red cast) at the hilus", (1940, 578)),
], "Renal pelvis cast", "Yellow = the urine-collecting system. Name the main chamber, its branches, and the tube leaving it.", white=True))

# Slide 13/14: median section photo
im = P(13)
K.whiten(im, [(1455, 135, 1560, 165), (1455, 395, 1478, 470), (1455, 560, 1478, 620)], lambda s: K.dark(s, 80), halo=2, near=False)
cards.append(K.card(im, 'l22lab_median', (1455, 135, 1992, 1072), [
    ("Fibrous capsule (covers the whole kidney; peels off easily if healthy)", (1972, 560)),
    ("Renal cortex (outer, granular: renal corpuscles)", (1905, 640)),
    ("Renal medulla (inner, darker, striated: medullary rays)", (1745, 640)),
    ("Renal crest (thickened free edge of the medulla facing the pelvis; fused papillae)", (1668, 520)),
    ("Renal pelvis", (1638, 600)),
    ("Renal sinus (fat)", (1590, 500)),
    ("Renal hilus (medial border)", (1478, 560)),
], "Kidney · median section", "Medial = left. Outside → in: name each layer, then what faces the pelvis.", white=True))

# Slide 15: paramedian section photo
im = P(15)
K.whiten(im, [(1412, 135, 1500, 170)], lambda s: ((s.max(2).astype(int) - s.min(2)) < 40) & (s.min(2) < 235), halo=2)
cards.append(K.card(im, 'l22lab_paramedian', (1412, 140, 1992, 1072), [
    ("Renal cortex", (1955, 600)),
    ("Renal pyramid (pyramid-shaped medulla = one lobe; paramedian sections only)", (1800, 575)),
    ("Renal papilla (apex of the pyramid)", (1758, 580)),
    ("Pelvic recess (between the pyramids)", (1748, 495)),
    ("Renal pelvis", (1640, 600)),
    ("Ureter", (1450, 572)),
], "Kidney · paramedian section", "Off the midline you see what the median section hides. Name the pyramid parts.", white=True))

# Slide 17: blood supply chain. Reveal ONLY the five the professor tests; the rest are greyed ("this is all systems, we will not worry about those")
im = P(17)
HIDE = dict(ao=(395, 330, 748, 378), ra=(482, 416, 652, 465), arc=(452, 602, 668, 658), rv=(1386, 488, 1552, 535), cvc=(1283, 378, 1645, 428))
GREY = [(464, 513, 726, 562), (436, 688, 736, 738), (430, 772, 798, 825), (428, 858, 788, 908), (904, 598, 1120, 650),
        (796, 672, 1350, 722), (906, 748, 1118, 800), (830, 858, 1333, 908), (1374, 858, 1670, 908), (1368, 740, 1580, 790), (1368, 608, 1625, 660)]
K.whiten(im, list(HIDE.values()), sat, halo=2, near=False)
for b in GREY:
    x0, y0, x1, y1 = b; sub = im[y0:y1, x0:x1]; sub[sat(sub)] = (205, 205, 205)
cards.append(K.card(im, 'l22lab_blood', (380, 300, 1700, 930), [
    ("Abdominal aorta", c(HIDE['ao'])), ("Renal artery", c(HIDE['ra'])),
    ("Arcuate artery (arcs at the corticomedullary junction)", c(HIDE['arc'])),
    ("Renal vein", c(HIDE['rv'])), ("Caudal vena cava", c(HIDE['cvc'])),
], "Renal blood supply · the 5 you need", "Grey boxes = systems content (\"we will not worry about those\"). Name the 5 hidden vessels.", white=True))

# Slide 20: oblique entry of the ureter (legend not on the slide; number 4 erased and skipped)
im = P(20)
N20 = {'1a': (1302, 62, 1328, 98), '3a': (1564, 152, 1593, 188), '4a': (1767, 177, 1796, 213), '2a': (1376, 309, 1404, 345),
       '1b': (1255, 585, 1281, 618), '3b': (1547, 687, 1575, 721), '4b': (1807, 702, 1835, 738), '2b': (1349, 939, 1375, 975)}
K.whiten(im, [N20[k] for k in ('1a', '3a', '4a', '1b', '3b', '4b')], lambda s: K.dark(s, 140), halo=2)
K.inpaint(im, [N20['2a'], N20['2b']], lambda s: K.dark(s, 140), grow=2, radius=5, grain=5)
K.fill(im, [(1400, 1085, 1730, 1112)], (255, 255, 255))
cards.append(K.card(im, 'l22lab_ureter_entry', (1190, 50, 1965, 1080), [
    ("Ureter", c(N20['1a'])), ("Ureter tunnels OBLIQUELY through the bladder wall", c(N20['3a'])), ("Lumen of the bladder", c(N20['2a'])),
    ("Full bladder: intravesical pressure squeezes the oblique segment shut → no reflux (peristalsis still pushes urine in)", (1500, 820)),
], "Ureter entering the bladder", "Why does the oblique entry matter when the bladder is full?", white=True))

# Slide 22: bladder opened ventrally (slide legend 1-6 cropped off; apex/body/neck from slide 21 + lecture)
im = P(22)
N22 = {1: (1628, 60, 1654, 90), 3: (1930, 178, 1957, 208), "3'": (1888, 552, 1928, 588)}
W22 = {2: (1686, 324, 1714, 362), 4: (1703, 613, 1729, 650), 5: (1681, 738, 1707, 772), 6: (1679, 968, 1707, 1002)}
K.whiten(im, list(N22.values()), lambda s: K.dark(s, 140), halo=2)
K.inpaint(im, list(W22.values()), full=True, grow=0, radius=6, grain=5)
cards.append(K.card(im, 'l22lab_bladder', (1420, 50, 1990, 1095), [
    ("Apex (cranial blind end; scar = urachus remnant)", c(N22[1])), ("Body of the bladder", (1478, 430)), ("Neck of the bladder (narrow caudal part)", (1612, 745)),
    ("Lumen of the bladder", c(W22[2])), ("Ureter (enters dorsally, obliquely)", c(N22[3])), ("Ureteric orifice", c(N22["3'"])),
    ("Trigone of the bladder (2 ureteric orifices + urethral crest)", c(W22[4])), ("Urethral crest", c(W22[5])), ("Urethra", c(W22[6])),
], "Urinary bladder · opened, ventral view", "Cranial = top. Ventral wall cut open, looking at the dorsal wall. Ureteric (not uterine!) orifice.", white=True))

# Slide 24: ligaments of the bladder (lecture: "Number 6 is your lateral ligament ... the median ligament is 6 double prime")
im = P(24)
N24 = {'5': (1455, 576, 1480, 608), '6': (1530, 514, 1554, 545), "6'": (1508, 548, 1540, 580), "6''": (1434, 642, 1468, 676),
       '14': (1464, 534, 1498, 565), '4': (1583, 498, 1607, 530), "11'''": (1543, 488, 1590, 517), 'Y': (1496, 626, 1522, 657)}
K.inpaint(im, list(N24.values()), lambda s: K.dark(s, 90), grow=1, radius=4, grain=14)
cards.append(K.card(im, 'l22lab_ligaments', (1310, 165, 2000, 1110), [
    ("Urinary bladder", c(N24['5'])),
    ("Lateral ligament of the bladder (number 6: bladder → lateral pelvic wall)", c(N24['6'])),
    ("Round ligament of the bladder (thickened free edge of the lateral ligament; umbilical artery remnant)", c(N24["6'"])),
    ("Median ligament of the bladder (6 double prime: ventral bladder → pelvic symphysis & linea alba)", c(N24["6''"])),
], "Ligaments of the bladder · left lateral view", "3 ligaments suspend the bladder. Find the bladder first, then each ligament.", white=True))

T.write('gross-anatomy-l22-labels.html', 'Label It · Urinary',
        'Lecture 22 · slide figures with labels hidden · numbered badges · tap to reveal in order', cards, [])
if '--preview' in sys.argv:
    for cd in cards: K.preview(cd, f"{TMP}/prev_{os.path.basename(cd['img'])}")
print('ok', len(cards), sum(len(cd['labels']) for cd in cards))
