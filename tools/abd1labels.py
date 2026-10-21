# Abdominal Cavity 1 (Diehl, 10/12) · "Label It" deck (made by Claude). Numbers checked against the 10/12 transcript;
# where the transcript and a slide legend disagree, the slide legend wins (see notes in the card names).
# Skips the flow-of-ingesta quadrant slide (31) and the pancreatic duct slide (41): both already in the app.
# Run from repo root: python3 tools/abd1labels.py /path/to/student_copy_2026_diehl_abdominal_cavity_part_1_-_Tagged.pdf
import sys, os
sys.path.insert(0, os.path.dirname(__file__)); import tracer as T, labelkit as K
pdf = sys.argv[1]; TMP = '/tmp/claude-0/abd1lab'
P = lambda n: K.page_png(pdf, n, TMP)
c = lambda b: ((b[0] + b[2]) / 2, (b[1] + b[3]) / 2)
pad = lambda b, p=4: (b[0] - p, b[1] - p, b[2] + p, b[3] + p)
cards = []

# Slide 10: stomach regions, numbers read aloud in lecture ("cardia ... number one; 2 fundus; 3 body; 4 pylorus")
im = P(10)
N = {1: (691, 476, 714, 507), 2: (331, 538, 354, 568), 3: (695, 945, 718, 975), 4: (953, 628, 977, 659)}
K.whiten(im, list(N.values()), K.dark)
cards.append(K.card(im, 'abd1lab_stomach_regions', (312, 256, 1162, 990), [
    ("Cardia (inlet: esophagus enters; cardiac sphincter)", c(N[1])), ("Fundus (site of gas accumulation)", c(N[2])),
    ("Body", c(N[3])), ("Pylorus (outlet: pyloric sphincter → duodenum)", c(N[4])),
], "Stomach regions · dog, opened", "Four regions, inlet to outlet. Name each number.", white=True))

# Slide 11: Figure 7-38 longitudinal section of stomach + proximal duodenum (bottom drawing and caption cropped off)
im = P(11)
L = dict(eso=(1440, 82, 1559, 110), cos=(1399, 132, 1556, 158), fun=(1740, 126, 1806, 198), gf=(1402, 186, 1534, 212),
         pyl=(1197, 117, 1278, 146), pcan=(1253, 156, 1386, 184), pant=(1316, 225, 1465, 254), ai=(1424, 259, 1510, 309),
         cys=(1070, 156, 1187, 184), hep=(1022, 193, 1164, 222), imb=(1010, 275, 1117, 326), mjp=(945, 343, 1106, 396),
         pd=(964, 413, 1076, 464), mnp=(939, 489, 1100, 543), apd=(1085, 575, 1256, 627), pp=(1268, 571, 1387, 600), bod=(1616, 571, 1673, 600))
K.whiten(im, [b for k, b in L.items() if k != 'fun'], lambda s: K.dark(s, 160), halo=2)
K.inpaint(im, [L['fun']], lambda s: K.dark(s, 140), grow=1, radius=4)  # rotated 'Fundus' overlaps the stomach wall
cards.append(K.card(im, 'abd1lab_stomach_section', (900, 70, 1855, 632), [
    ("Esophagus", c(L['eso'])), ("Cardiac ostium (cardia = inlet)", c(L['cos'])), ("Fundus", c(L['fun'])),
    ("Body", c(L['bod'])), ("Gastric folds (rugae)", c(L['gf'])), ("Angular incisure (on the lesser curvature)", c(L['ai'])),
    ("Pyloric part (pyloric portion)", c(L['pp'])), ("Pyloric antrum (expanded part)", c(L['pant'])), ("Pyloric canal (narrowed part)", c(L['pcan'])),
    ("Pylorus (outlet, pyloric sphincter)", c(L['pyl'])),
    ("Cystic duct", c(L['cys'])), ("Hepatic ducts", c(L['hep'])), ("Intramural bile duct", c(L['imb'])),
    ("Major duodenal papilla (bile duct + pancreatic duct open here)", c(L['mjp'])), ("Pancreatic duct", c(L['pd'])),
    ("Minor duodenal papilla (accessory pancreatic duct opens here)", c(L['mnp'])), ("Accessory pancreatic ducts", c(L['apd'])),
], "Stomach & proximal duodenum · longitudinal section", "Figure 7-38. Inlet → outlet, then the ducts that open into the duodenum.", white=True))

# Slide 22: Figure 14-18, canine duodenum, cecum, colon in situ (ventral view); legend cropped off
im = P(22)
F = {1: (1686, 163, 1701, 184), 2: (1674, 280, 1690, 304), 3: (1820, 450, 1837, 473), 5: (1503, 450, 1521, 471), 6: (1669, 476, 1686, 500),
     7: (1584, 601, 1601, 624), 8: (1585, 483, 1601, 505), 9: (1575, 406, 1592, 427), 10: (1615, 359, 1644, 379), 11: (1707, 650, 1732, 673),
     14: (1657, 788, 1684, 811)}
OUT = {4: (1401, 432, 1422, 455), 12: (1858, 519, 1905, 547), 13: (1858, 594, 1910, 622)}
K.inpaint(im, [pad(b, 2) for b in F.values()], full=True, grow=1, radius=5, grain=7)
K.whiten(im, list(OUT.values()), lambda s: K.dark(s, 170), halo=2)
K.fill(im, [(1395, 930, 1525, 1110)], (255, 255, 255))  # end of the figure caption
cards.append(K.card(im, 'abd1lab_insitu', (1395, 0, 1932, 1022), [
    ("Liver", c(F[1])), ("Stomach", c(F[2])), ("Spleen", c(F[3])), ("Pancreas (in the mesoduodenum)", c(OUT[4])),
    ("Descending duodenum (right side, cranial → caudal)", c(F[5])), ("Ascending duodenum (left side)", c(F[6])),
    ("Ileum (jejunum cut away in this image)", c(F[7])), ("Cecum (does NOT communicate with the ileum in the dog)", c(F[8])),
    ("Ascending colon (short, right side)", c(F[9])), ("Transverse colon (cranial to the root of the mesentery)", c(F[10])),
    ("Descending colon", c(F[11])), ("Vessels in the root of the mesentery (cranial mesenteric artery)", c(OUT[12])),
    ("Duodenocolic fold (ascending duodenum ↔ descending colon)", c(OUT[13])), ("Urinary bladder", c(F[14])),
], "Duodenum, cecum & colon in situ · ventral view", "Figure 14-18. R and L are the dog's sides. Name all 14 in order."))

# Slide 23: line diagram of the large intestine + unpaired arteries
im = P(23)
D = {7: (931, 326, 960, 367), 8: (1498, 286, 1532, 325), 4: (1598, 400, 1632, 439), 9: (1281, 453, 1312, 494), 5: (948, 536, 980, 577),
     "9'": (474, 610, 522, 652), 3: (1418, 676, 1450, 717), 2: (1066, 731, 1099, 772), 6: (383, 731, 415, 772), 1: (1219, 870, 1245, 910)}
K.whiten(im, list(D.values()), lambda s: K.dark(s, 120), halo=2)
cards.append(K.card(im, 'abd1lab_linediagram', (340, 190, 1700, 930), [
    ("Ileum", c(D[1])), ("Cecum", c(D[2])), ("Ascending colon", c(D[3])), ("Transverse colon", c(D[4])),
    ("Descending colon", c(D[5])), ("Rectum and anus", c(D[6])), ("Abdominal aorta", c(D[7])), ("Celiac artery", c(D[8])),
    ("Cranial mesenteric artery (root of the mesentery; transverse colon passes cranial to it)", c(D[9])),
    ("Caudal mesenteric artery", c(D["9'"])),
], "Large intestine line diagram + unpaired arteries", "Ascend, cross, descend. Then name the 3 unpaired branches of the aorta.", white=True))

# Slide 21: cecum, internal view ("number 1 is the ileum, 2 is the cecum, 3 is the ascending colon")
im = P(21)
C3 = {1: (1710, 396, 1735, 428), 3: (1311, 606, 1339, 638), 2: (1661, 621, 1692, 654)}
K.inpaint(im, [pad(b, 1) for b in C3.values()], lambda s: K.dark(s, 110), grow=2, radius=5, grain=6)
cards.append(K.card(im, 'abd1lab_cecum', (1025, 40, 1930, 765), [
    ("Ileum", c(C3[1])), ("Cecum (blind sac; removed in a typhlectomy)", c(C3[2])), ("Ascending colon (opened)", c(C3[3])),
    ("Ileocolic orifice (ileum → ascending colon)", (1430, 625)),
    ("Cecocolic orifice (cecum → ascending colon; ileum and cecum do not communicate)", (1492, 712)),
], "Cecum & the two orifices", "Which openings lead into the ascending colon? Which two segments never connect in the dog?"))

# Slide 25: rectum & anal canal (text labels on the right of the drawing)
im = P(25)
R = dict(rec=(1292, 113, 1401, 143), amp=(1700, 303, 1908, 340), ext=(1700, 494, 1980, 531), int=(1700, 550, 1982, 586),
         par=(1700, 605, 1890, 636), ac=(1697, 660, 1854, 691), col=(1715, 715, 1929, 746), inter=(1716, 770, 1966, 801), cut=(1714, 825, 1943, 857))
K.whiten(im, [R[k] for k in R if k != 'rec'], lambda s: K.dark(s, 170), halo=2)
K.inpaint(im, [R['rec']], lambda s: K.dark(s, 170), grow=2, radius=5)
cards.append(K.card(im, 'abd1lab_rectum', (1050, 50, 1995, 935), [
    ("Rectum", c(R['rec'])), ("Rectal ampulla (ampulla recti)", c(R['amp'])),
    ("External anal sphincter muscle (skeletal: voluntary)", c(R['ext'])), ("Internal anal sphincter muscle (smooth: involuntary)", c(R['int'])),
    ("Paranal sinus (anal sac)", c(R['par'])), ("Anal canal: 3 zones ↓", c(R['ac'])),
    ("Columnar zone (cranial part: anorectal line, anal columns, anal sinuses)", c(R['col'])),
    ("Intermediate zone (middle part: anocutaneous line)", c(R['inter'])), ("Cutaneous zone (caudal part: anal sacs open here)", c(R['cut'])),
], "Rectum & anal canal", "Cranial → caudal. Which sphincter can the dog control?", white=True))

# Slide 26: anal canal zones (labels were already blank on the student copy; names from the 10/12 lecture)
im = P(26)
cards.append(K.card(im, 'abd1lab_analcanal', (1030, 205, 1895, 890), [
    ("Anal columns (longitudinal folds; columnar zone)", (1460, 430)), ("Anal sinuses (grooves between the columns)", (1530, 640)),
    ("Anocutaneous line (intermediate zone; anus ↔ skin)", (1500, 702)), ("Cutaneous zone", (1500, 800)),
    ("Opening of the anal sac (cranial cutaneous zone)", (1312, 690)), ("Anal sac (paranal sinus)", (1236, 455)),
], "Anal canal zones", "Slide labels are blank on the student copy. Columnar → intermediate → cutaneous.", white=True))

# Slide 34: liver lobes, diaphragmatic + visceral surfaces (legend 1-13 cropped off; the legend wins over the transcript)
im = P(34)
LV = {'1a': (378, 422, 407, 462), '2a': (468, 637, 499, 677), '3a': (666, 653, 699, 693), '4a': (856, 677, 887, 717), '6a': (985, 462, 1018, 502),
      '3b': (1466, 234, 1497, 271), '6b': (1238, 359, 1268, 395), '4b': (1403, 372, 1434, 410), '10': (1301, 512, 1349, 548), '7': (1216, 537, 1242, 575),
      '11': (1555, 522, 1598, 558), '1b': (1693, 512, 1722, 548), '12': (1478, 634, 1525, 670), '8': (1281, 672, 1309, 710),
      '13': (1610, 687, 1662, 725), '9': (1253, 832, 1282, 871)}
K.inpaint(im, list(LV.values()), lambda s: (s.max(2) < 75) | (s.min(2) > 225), grow=3, radius=7, grain=7)
cards.append(K.card(im, 'abd1lab_liver_lobes', (215, 170, 1890, 955), [
    ("Left lateral lobe", c(LV['1a'])), ("Left medial lobe", c(LV['2a'])), ("Quadrate lobe", c(LV['3a'])), ("Gallbladder (between quadrate and right medial)", c(LV['4a'])),
    ("Right medial lobe", c(LV['6a'])),
    ("Quadrate lobe", c(LV['3b'])), ("Right medial lobe", c(LV['6b'])), ("Gallbladder", c(LV['4b'])), ("Right lateral lobe", c(LV['7'])),
    ("Caudate process of the caudate lobe", c(LV['8'])), ("Renal impression at the caudate process (right kidney)", c(LV['9'])),
    ("Bile duct", c(LV['10'])), ("Papillary process of the caudate lobe (not a separate lobe)", c(LV['11'])),
    ("Left lateral lobe", c(LV['1b'])), ("Portal vein (fixed specimen)", c(LV['12'])), ("Esophageal impression", c(LV['13'])),
], "Liver lobes · diaphragmatic (left) & visceral (right)", "Six lobes + two caudate processes. Left lateral, left medial, quadrate, right medial, right lateral, caudate."))

# Slide 35: liver schematic (lobe names were already blank on the student copy)
im = P(35)
S5 = dict(oes=(432, 243, 762, 285), cvc=(1588, 316, 1832, 350), por=(1588, 538, 1836, 648), fal=(460, 874, 776, 946), gb=(1422, 914, 1594, 948))
K.whiten(im, list(S5.values()), lambda s: K.dark(s, 170), halo=2)
K.fill(im, [(255, 1060, 790, 1095)], (255, 255, 255))
cards.append(K.card(im, 'abd1lab_liver_schema', (245, 225, 1860, 985), [
    ("Esophageal impression", c(S5['oes'])), ("Caudal vena cava", c(S5['cvc'])),
    ("Hepatic porta (portal vein and hepatic artery enter)", c(S5['por'])),
    ("Falciform ligament with the round ligament (between left medial and quadrate; to the ventral body wall)", c(S5['fal'])),
    ("Gallbladder", c(S5['gb'])),
], "Liver schematic · landmarks", "Anatomy of the Domestic Animals Fig 7-96.", white=True))

# Slide 37: Miller's Fig 26-18A, diaphragmatic aspect: triangular + coronary ligaments ("left triangular ligament is at 15 and the right ... at 10; coronary ... at 7")
im = P(37)
G = {1: (1268, 310, 1288, 330), 2: (1571, 43, 1588, 62), 3: (1641, 43, 1656, 62), 4: (1695, 43, 1710, 64), 5: (1828, 150, 1845, 170),
     6: (1868, 203, 1885, 224), 7: (1893, 248, 1910, 269), '8a': (1908, 285, 1924, 305), 9: (1933, 400, 1950, 420), 14: (1521, 486, 1545, 508),
     '8b': (1553, 486, 1569, 508), 13: (1568, 500, 1594, 522), 15: (1431, 520, 1458, 542), 12: (1586, 522, 1612, 543), 11: (1618, 573, 1642, 594), 10: (1633, 598, 1659, 619)}
K.inpaint(im, list(G.values()), lambda s: K.dark(s, 150), grow=2, radius=5, grain=5)
cards.append(K.card(im, 'abd1lab_liver_ligaments', (1268, 30, 1955, 628), [
    ("Left lateral lobe", (1300, 320)), ("Left medial lobe", c(G[2])), ("Quadrate lobe", c(G[3])), ("Gallbladder", c(G[4])), ("Right medial lobe", c(G[5])),
    ("Falciform ligament", c(G[6])), ("Coronary ligament (crown around the caudal vena cava; joins triangular ligaments to the falciform)", c(G[7])),
    ("Hepatic veins", c(G['8a'])), ("Right lateral lobe", c(G[9])),
    ("Right triangular ligament (right lateral lobe → right crus of the diaphragm)", c(G[10])), ("Area nuda (bare area)", c(G[11])),
    ("Caudal vena cava", c(G[12])), ("Caudate lobe", c(G[13])), ("Lesser omentum", c(G[14])),
    ("Left triangular ligament (left lateral lobe → left crus of the diaphragm)", c(G[15])),
], "Liver ligaments · diaphragmatic aspect", "Miller's Fig 26-18A. Find the 2 triangular ligaments and the coronary ligament first (the lecture called them out by number)."))

# Slide 38: visceral surface, Miller's (all text labels hidden; inset cropped)
im = P(38)
V = dict(pap=(1742, 75, 1882, 115), llat=(1585, 93, 1712, 113), quad=(1465, 120, 1583, 140), gas=(1825, 137, 1917, 181), rmed=(1200, 206, 1343, 228),
         gb=(1199, 279, 1296, 300), rlat=(1147, 350, 1285, 371), duo=(1148, 420, 1240, 465), cp=(1108, 512, 1240, 551), lo=(1684, 590, 1821, 611),
         hr=(1138, 600, 1240, 645), ltri=(1658, 622, 1844, 646), hb=(1621, 654, 1766, 675), rf=(1154, 673, 1252, 695), ha=(1593, 687, 1710, 711),
         pv=(1572, 718, 1662, 740), gda=(1225, 718, 1407, 742), rlat2=(1310, 750, 1448, 772), bd=(1551, 750, 1627, 772), cvc=(1343, 782, 1490, 805),
         rga=(1503, 782, 1658, 806))
K.whiten(im, list(V.values()), lambda s: K.dark(s, 160), halo=2)
K.fill(im, [(1560, 796, 1965, 815)], (255, 255, 255))  # top of the small inset
cards.append(K.card(im, 'abd1lab_liver_visceral', (1100, 62, 1960, 812), [
    ("Left lateral lobe", c(V['llat'])), ("Quadrate lobe", c(V['quad'])), ("Right medial lobe", c(V['rmed'])), ("Gallbladder", c(V['gb'])),
    ("Right lateral lobe", c(V['rlat'])), ("Right lateral lobe", c(V['rlat2'])), ("Papillary process of the caudate lobe", c(V['pap'])),
    ("Caudate process of the caudate lobe", c(V['cp'])), ("Hepatorenal ligament (caudate process → cranial pole of the right kidney)", c(V['hr'])),
    ("Renal fossa", c(V['rf'])), ("Duodenal impression", c(V['duo'])), ("Gastric impression", c(V['gas'])),
    ("Lesser omentum", c(V['lo'])), ("Left triangular ligament", c(V['ltri'])),
    ("Caudal vena cava", c(V['cvc'])), ("Portal vein", c(V['pv'])), ("Hepatic artery", c(V['ha'])), ("Hepatic branches", c(V['hb'])),
    ("Bile duct", c(V['bd'])), ("Gastroduodenal artery", c(V['gda'])), ("Right gastric artery", c(V['rga'])),
], "Liver · visceral surface", "Lobes first, then the caudate processes and the hepatorenal ligament, then the vessels at the porta."))

# Slide 40: pancreas with its neighbours (lobes: right lobe = head, along the duodenum; left lobe = tail, along the stomach)
im = P(40)
PN = dict(eso=(1510, 133, 1583, 154), sto=(1806, 428, 1868, 447), duo=(1216, 629, 1296, 648), tc=(1750, 679, 1862, 698),
          dc=(1766, 820, 1887, 842), cec=(1258, 786, 1311, 806), ile=(1354, 873, 1399, 893), jej=(1617, 922, 1676, 943))
K.whiten(im, list(PN.values()), lambda s: K.dark(s, 190), halo=2)
cards.append(K.card(im, 'abd1lab_pancreas', (1200, 120, 1900, 955), [
    ("Right lobe of the pancreas (head): in the descending mesoduodenum", (1418, 440)),
    ("Left lobe of the pancreas (tail): deep leaf of the greater omentum; most common biopsy site", (1545, 525)),
    ("Esophagus", c(PN['eso'])), ("Stomach", c(PN['sto'])), ("Duodenum", c(PN['duo'])), ("Transverse colon", c(PN['tc'])),
    ("Descending colon", c(PN['dc'])), ("Cecum", c(PN['cec'])), ("Ileum", c(PN['ile'])), ("Jejunum", c(PN['jej'])),
], "Pancreas & neighbours", "Which lobe follows the duodenum, and which follows the stomach?", white=True))

T.write('gross-anatomy-abd1-labels.html', 'Label It · Abdominal Cavity 1',
        'Lecture 20 (Dr. Diehl, 10/12) · slide figures with labels hidden · numbered badges · tap to reveal in order', cards, [])
if '--preview' in sys.argv:
    for cd in cards: K.preview(cd, f"{TMP}/prev_{os.path.basename(cd['img'])}")
print('ok', len(cards), sum(len(cd['labels']) for cd in cards))
