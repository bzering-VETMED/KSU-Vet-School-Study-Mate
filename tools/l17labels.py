# Lecture 17 Nervous System 1 · "Label It" deck (made by Claude). Names checked against the 10/05 L17 transcript.
# Run from repo root: python3 tools/l17labels.py /path/to/Lecture_17_Nervous_System_1_-_Tagged.pdf
import sys, os
sys.path.insert(0, os.path.dirname(__file__)); import tracer as T, labelkit as K
pdf = sys.argv[1]; TMP = '/tmp/claude-0/l17lab'
P = lambda n: K.page_png(pdf, n, TMP)
c = lambda b: ((b[0] + b[2]) / 2, (b[1] + b[3]) / 2)
cards = []

# Slide 27: functional types on the cord cross-section ("spend a couple of minutes on this figure ... six to eight points")
im = P(27)
GSA, GVA, GVE, GSE = (1198, 188, 1292, 246), (1130, 573, 1226, 631), (1105, 666, 1199, 724), (1175, 913, 1264, 971)
K.whiten(im, [GSA, GVA, GVE, GSE], K.nonwhite)
K.whiten(im, [(735, 940, 1110, 968)], K.nonwhite)  # copyright line
cards.append(K.card(im, 'l17lab_functional', (300, 180, 1560, 985), [
    ("Dorsal horn (always sensory: afferent endings of general somatic afferent and general visceral afferent)", (905, 470)),
    ("Lateral horn (general visceral efferent: sympathetic; thoracolumbar cord)", (930, 600)),
    ("Ventral horn (general somatic efferent: lower motor neuron cell bodies)", (870, 700)),
    ("Gray matter (central)", (470, 470)),
    ("White matter (peripheral)", (360, 640)),
    ("Dorsal root", (1010, 318)),
    ("Dorsal root ganglion (pseudounipolar sensory cell bodies; there is NO ventral root ganglion)", (1258, 420)),
    ("Ventral root", (960, 868)),
    ("Spinal nerve (mixed)", (1500, 560)),
    ("General somatic afferent (GSA): skin, muscle, joints → dorsal horn", c(GSA)),
    ("General visceral afferent (GVA): organs → dorsal horn", c(GVA)),
    ("General visceral efferent (GVE): lateral horn → smooth muscle, cardiac muscle, glands (2-neuron chain)", c(GVE)),
    ("General somatic efferent (GSE): ventral horn → skeletal muscle (1 neuron all the way)", c(GSE)),
], "Functional types on the cord cross-section ★ 6–8 points",
   "Professor: \"spend a couple of minutes on this figure ... at least six to eight points.\" Name each region, then each colored fiber.", white=True))

# Slide 10: spinal cord cross-section review
im = P(10)
L10 = dict(dh=(328, 300, 586, 362), lh=(278, 623, 544, 684), vh=(303, 928, 577, 990), gm=(1354, 326, 1617, 388), wm=(1429, 802, 1722, 864))
K.whiten(im, list(L10.values()), K.nonwhite)
K.whiten(im, [(984, 590, 1012, 632)], K.nonwhite)  # legend number 2 (in the canal)
# legend numbers 1, 3-6 (not covered in lecture): recolor only the digit strokes with the local cream
K.whiten(im, [(1002, 402, 1030, 446), (1254, 472, 1275, 503), (1230, 594, 1268, 640), (1316, 796, 1344, 834), (1326, 652, 1356, 694)],
         lambda s: s.astype(int).sum(2) < 660, halo=2, color='auto')
cards.append(K.card(im, 'l17lab_cord', (270, 290, 1735, 1015), [
    ("Dorsal horn", c(L10['dh'])), ("Lateral horn (only thoracolumbar; a little in sacral)", c(L10['lh'])),
    ("Ventral horn", c(L10['vh'])), ("Gray matter (center of the cord; brain is the opposite)", c(L10['gm'])),
    ("White matter (periphery of the cord)", c(L10['wm'])),
], "Spinal cord cross-section", "Gray inside or outside in the cord? Name all three horns.", white=True))

# Slide 7: neuron shapes
im = P(7)
L7 = dict(m=(1166, 463, 1356, 517), ml=(1450, 458, 1790, 563), b=(1166, 691, 1298, 745), bl=(1450, 687, 1804, 791),
          p=(1151, 900, 1427, 954), pl=(1450, 900, 1798, 1004))
K.whiten(im, list(L7.values()), K.nonwhite)
K.fill(im, [(1675, 1012, 1965, 1095)], (255, 255, 255))  # university logo
cards.append(K.card(im, 'l17lab_neurons', (300, 255, 1820, 1080), [
    ("Multipolar", c(L7['m'])), ("Where: motor neurons and interneurons", c(L7['ml'])),
    ("Bipolar", c(L7['b'])), ("Where: auditory, visual, and vestibular neurons", c(L7['bl'])),
    ("Pseudounipolar", c(L7['p'])), ("Where: muscle spindles, cutaneous afferents (cell body in a sensory ganglion)", c(L7['pl'])),
], "Neuron types by shape", "Name the shape, then where you find it.", white=True))

# Slide 14: monosynaptic patellar reflex arc
im = P(14)
L14 = dict(pa=(508, 533, 1092, 601), fe=(511, 708, 1171, 776), ex=(276, 886, 1163, 954))
K.whiten(im, list(L14.values()) + [(228, 190, 1240, 432), (200, 1066, 1160, 1110), (1490, 1092, 1780, 1115)], K.nonwhite)
K.fill(im, [(228, 150, 1276, 196)], (255, 255, 255))  # bottom of the slide title
n2, n3, n4, n1 = (1402, 195, 1430, 227), (1652, 461, 1681, 494), (1383, 543, 1412, 574), (1390, 786, 1418, 817)
K.whiten(im, [n2, n4], K.dark)
K.inpaint(im, [n3, n1], K.dark, grow=2, radius=5)
cards.append(K.card(im, 'l17lab_patellar', (260, 170, 1990, 1115), [
    ("Tap on the patellar ligament → stretches the muscle → picked up by the muscle spindle", c(n1)),
    ("Primary afferent neuron (number 2 in lecture)", c(L14['pa'])),
    ("Cell body of the primary afferent neuron: in the dorsal root ganglion (pseudounipolar)", c(n2)),
    ("Cell body of the lower motor neuron: in the ventral horn", c(n3)),
    ("Final efferent neuron = lower motor neuron (back to the quadriceps, extrafusal fibers)", c(L14['fe'])),
    ("Monosynaptic patellar reflex (1 synapse: primary afferent + final efferent = reflex arc)", c(L14['ex'])),
], "Reflex arc · patellar reflex", "Follow the stretch from the tendon into the cord and back out to the muscle.", white=True))

# Slide 16: withdrawal reflex with interneurons (photos cropped off)
im = P(16)
L16 = dict(pns=(560, 316, 895, 350), cns=(1085, 316, 1385, 350), skin=(398, 480, 458, 512), rec=(513, 518, 662, 550),
           pa=(493, 478, 815, 510), ex=(700, 430, 1000, 464), inh=(1262, 670, 1522, 702), ee=(1090, 713, 1395, 747),
           fe=(988, 758, 1292, 792), em=(748, 773, 954, 807), fm=(302, 833, 509, 897))
K.whiten(im, list(L16.values()), K.dark, halo=2)
cards.append(K.card(im, 'l17lab_withdrawal', (225, 312, 1530, 1060), [
    ("Skin", c(L16['skin'])), ("Receptor", c(L16['rec'])), ("Primary afferent neuron (cell body in the dorsal root ganglion)", c(L16['pa'])),
    ("Excitatory interneuron", c(L16['ex'])), ("Inhibitory interneuron", c(L16['inh'])),
    ("Flexor efferent neuron (lower motor neuron, stimulated)", c(L16['fe'])), ("Flexor muscle = effector (agonist, contracts: limb withdraws)", c(L16['fm'])),
    ("Extensor efferent neuron (silenced by the inhibitory interneuron)", c(L16['ee'])), ("Extensor muscle (relaxes; e.g., triceps)", c(L16['em'])),
    ("Peripheral nervous system", c(L16['pns'])), ("Central nervous system (interneurons live entirely here)", c(L16['cns'])),
], "Withdrawal reflex · interneurons", "Pinch → withdraw. Which neuron excites, which inhibits, and which muscle relaxes? (Local: no brain needed.)", white=True))

# Slide 29: basic make-up of all spinal nerves (inset + Miller's Fig 17-1)
im = P(29)
for b in [(400, 300, 1094, 604), (1155, 300, 1300, 525), (1300, 300, 1925, 668)]: K.keep_only(im, b, K.yellow)  # top summary text
L29 = dict(drl=(208, 680, 268, 718), vrl=(476, 903, 534, 937), drg=(403, 926, 468, 982), mt=(228, 940, 304, 978),
           dr=(762, 765, 952, 808), vr=(767, 900, 962, 943), db=(1505, 755, 1735, 798), vb=(1508, 818, 1750, 862),
           ivf=(1497, 962, 1875, 1008), cb=(1458, 1022, 1828, 1065))
K.whiten(im, [L29[k] for k in ('drl', 'vrl', 'drg', 'mt')], lambda s: K.dark(s, 170), halo=1)
K.whiten(im, [(762, 765, 880, 808), (767, 900, 935, 943)], lambda s: K.dark(s, 170))  # left (white) part of the root labels
K.whiten(im, [(880, 765, 952, 808), (935, 900, 962, 943)], lambda s: K.dark(s, 140), halo=2, near=False)  # part touching the vertebra outline
K.whiten(im, [L29[k] for k in ('db', 'vb', 'ivf', 'cb')], lambda s: K.dark(s, 170))
cards.append(K.card(im, 'l17lab_spinalnerve', (190, 440, 1920, 1066), [
    ("Dorsal rootlets", c(L29['drl'])), ("Ventral rootlets", c(L29['vrl'])), ("Dorsal root ganglion (sensory)", c(L29['drg'])),
    ("Spinal nerves (main trunks)", c(L29['mt'])),
    ("Dorsal root (sensory, afferent)", c(L29['dr'])), ("Ventral root (motor, efferent)", c(L29['vr'])),
    ("Dorsal branch (motor and sensory)", c(L29['db'])), ("Ventral branch (motor and sensory)", c(L29['vb'])),
    ("Intervertebral foramen (spinal nerve exits here; C1 is the exception)", c(L29['ivf'])),
    ("Communicating branch (thoracolumbar only)", c(L29['cb'])),
], "Basic make-up of ALL spinal nerves", "Rootlets → roots → spinal nerve → branches. Name each piece.", white=True))

# Slide 30: dorsal root ganglion + branches with afferent/efferent fibers
im = P(30)
L30 = dict(drg=(1352, 126, 1772, 228), db=(772, 220, 1082, 372), vb=(222, 735, 542, 888), aff=(492, 930, 800, 976), eff=(492, 980, 800, 1026))
K.fill(im, [(205, 40, 1165, 152), (1680, 1015, 1965, 1100)], (255, 255, 255))  # slide title, logo
K.whiten(im, list(L30.values()), lambda s: K.dark(s, 170))
cards.append(K.card(im, 'l17lab_drg', (195, 115, 1790, 1062), [
    ("Dorsal root ganglion (sensory / afferent ganglion)", c(L30['drg'])),
    ("Dorsal branch of the spinal nerve (mixed nerve)", c(L30['db'])),
    ("Ventral branch of the spinal nerve (mixed nerve)", c(L30['vb'])),
    ("Red = afferents (somatic): cell body in the dorsal root ganglion → dorsal horn", c(L30['aff'])),
    ("Blue = efferents (somatic): ventral horn → out the ventral root", c(L30['eff'])),
], "Dorsal root ganglion & the two branches", "Where is the sensory cell body? Which color is afferent?", white=True))

# Slide 31: epaxial vs hypaxial territory
im = P(31)
L31 = dict(db=(598, 362, 812, 474), vb=(214, 718, 444, 830), ep=(1216, 540, 1518, 602), hy=(1216, 668, 1542, 730))
PINK = (194, 178, 226)
def text31(s):  # anything that is not white, not the pink muscle, and not a saturated red/blue fiber arrow
    d = abs(s - PINK).sum(2); return (s.min(2) < 235) & (d > 30) & ((s.max(2) - s.min(2)) < 90)
K.inpaint(im, [L31['db'], L31['vb']], text31, grow=2, radius=5)
K.fill(im, [(1195, 330, 1990, 534), (1205, 735, 1990, 1000), (720, 955, 1190, 985)], (255, 255, 255))
K.whiten(im, [L31['ep'], L31['hy']], K.nonwhite)
cards.append(K.card(im, 'l17lab_epaxial', (195, 205, 1560, 995), [
    ("Dorsal branch of the spinal nerve", (722, 505)),
    ("Ventral branch of the spinal nerve", c(L31['vb'])),
    ("Epaxial muscles", (1010, 420)),
    ("Epaxial region (above the transverse processes): epaxial muscles + dorsal 1/3 of the skin ← dorsal branches", c(L31['ep'])),
    ("Hypaxial region (below the transverse processes): hypaxial muscles, limbs + ventral 2/3 of the skin ← ventral branches", c(L31['hy'])),
], "Epaxial vs hypaxial territory", "The dashed line = level of the transverse processes. Which branch serves each side?", white=True))

# Slide 32: where each spinal nerve exits relative to its vertebra
im = P(32)
L32 = dict(C1=(478, 336, 522, 390), C2=(551, 336, 596, 390), C7=(980, 336, 1025, 390), C8=(1056, 336, 1101, 390),
           T1=(534, 546, 580, 596), T2=(618, 546, 664, 596), T13=(1531, 546, 1590, 600),
           L1=(534, 742, 576, 790), L7=(1046, 742, 1090, 790), S1=(508, 922, 552, 970), S2=(554, 922, 600, 970), S3=(616, 922, 660, 970))
K.whiten(im, list(L32.values()), K.dark)
cards.append(K.card(im, 'l17lab_exits', (190, 215, 1585, 990), [
    ("C1: exits the lateral vertebral foramen of the atlas (not an intervertebral foramen)", c(L32['C1'])),
    ("C2: cranial to its vertebra", c(L32['C2'])),
    ("C7: cranial to its vertebra", c(L32['C7'])),
    ("C8: no 8th cervical vertebra, exits cranial to T1", c(L32['C8'])),
    ("T1: caudal to its vertebra (all thoracic and lumbar)", c(L32['T1'])),
    ("T2", c(L32['T2'])), ("T13 (13 thoracic pairs)", c(L32['T13'])),
    ("L1: caudal to its vertebra", c(L32['L1'])), ("L7 (7 lumbar pairs)", c(L32['L7'])),
    ("S1: out the dorsal & ventral sacral foramina (past exam question)", c(L32['S1'])), ("S2", c(L32['S2'])), ("S3 (8 + 13 + 7 + 3 = 31 pairs)", c(L32['S3'])),
], "Spinal nerve exits vs vertebrae", "Cervical nerves exit cranial to their vertebra; thoracic and lumbar exit caudal. Name each hidden nerve.", white=True))

T.write('gross-anatomy-l17-labels.html', 'Label It · Nervous System 1',
        'Lecture 17 · slide figures with labels hidden · numbered badges · tap to reveal in order', cards, [])
if '--preview' in sys.argv:
    for cd in cards: K.preview(cd, f"{TMP}/prev_{os.path.basename(cd['img'])}")
print('ok', len(cards), sum(len(cd['labels']) for cd in cards))
