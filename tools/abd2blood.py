# Abdominal blood supply tracing deck (made by Claude). Run from repo root: python3 tools/abd2blood.py /path/to/IMG_4538.jpeg
import cv2, sys, os; sys.path.insert(0, os.path.dirname(__file__)); import tracer as T
src, cvc_src, portal_src = sys.argv[1:4]; X, Y = 318, 180
os.makedirs('/tmp/claude-0', exist_ok=True); tmp = '/tmp/claude-0/abd2_blood_src.jpg'
cv2.imwrite(tmp, cv2.imread(src)[Y:, X:], [cv2.IMWRITE_JPEG_QUALITY, 95])
B = lambda x0,y0,x1,y1: (x0-X-4, y0-Y-4, x1-X+4, y1-Y+4)
dark = lambda s: s.max(2) < 115
labels = [
 ("Right gastric a.", [B(915,240,966,264)]),
 ("Left gastric a.", [B(1012,233,1154,260)]),
 ("Right gastroepiploic a.", [B(906,284,947,310)]),
 ("Left gastroepiploic a.", [B(998,288,1214,317)]),
 ("Cranial pancreatoduodenal a.", [B(593,260,838,336)]),
 ("Cranial pancreatoduodenal a.", [B(518,372,547,622)]),
 ("Caudal pancreatoduodenal a.", [B(520,662,550,908)]),
 ("Caudal pancreatoduodenal a.", [B(820,1038,1088,1088)]),
 ("Caudal pancreatoduodenal a.", [B(1236,662,1264,912)]),
 ("Jejunal aa.", [B(1090,456,1160,485)]),
 ("Jejunal aa.", [B(922,676,992,703)]),
 ("Jejunal → ileal aa.", [B(873,886,1010,916)]),
 ("Cecocolic → cecal → antimesenteric ileal a.", [B(686,848,1032,962)]),
 ("Cecocolic → cecal a.", [B(634,596,664,758)]),
 ("Cecocolic → colic a.", [B(706,543,738,702)]),
 ("Right colic a.", [B(710,383,802,457)]),
 ("Right colic a. / middle colic a.", [B(903,380,1118,406)]),
 ("Middle colic a.", [B(1360,400,1460,480)]),
 ("Middle colic a.", [B(1433,548,1464,664)]),
 ("Left colic a.", [B(1433,706,1464,794)]),
 ("Left colic a.", [B(1326,963,1407,1024)]),
]
card = T.raster_card(tmp, 'abd2_blood', labels, "Blood supply on the flow-of-ingesta map",
                     "Each label sits on the gut segment it supplies. Follow the gut from the stomach and name each artery before you tap.", scale=0.8, test=dark)

# ---- Venous drainage slides (blue/magenta text) ----
def colored(s):
    r, g, b = s[...,2], s[...,1], s[...,0]
    r, g, b = r.astype(int), g.astype(int), b.astype(int)
    return (r + g + b) < 740  # labels sit on white; any non-white pixel in the box is text
import numpy as np
def crop(path, out, y0):
    t = f'/tmp/claude-0/{out}_src.jpg'; cv2.imwrite(t, cv2.imread(path)[y0:, 14:], [cv2.IMWRITE_JPEG_QUALITY, 95]); return t
def blank(path, labels):
    # labels sit on plain white: repaint each box with its own border colour (invisible, no smudge)
    im = cv2.imread(path)
    for _, bs in labels:
        for (x0, y0, x1, y1) in bs:
            x0, y0, x1, y1 = max(0,int(x0)), max(0,int(y0)), int(x1), int(y1)
            sub = im[y0:y1, x0:x1]
            border = np.concatenate([sub[0], sub[-1], sub[:,0], sub[:,-1]])
            im[y0:y1, x0:x1] = np.median(border, axis=0)
    cv2.imwrite(path, im, [cv2.IMWRITE_JPEG_QUALITY, 95]); return path
none = lambda s: np.zeros(s.shape[:2], bool)
Yc = 170; C = lambda x0,y0,x1,y1: (x0-18, y0-Yc-6, x1-10, y1-Yc+6)
CVC = [
 ("Caudal vena cava", [C(756,205,1250,255)]),
 ("Hepatic veins", [C(649,351,878,391)]),
 ("Phrenicoabdominal vein", [C(470,563,882,595)]),
 ("Phrenicoabdominal vein", [C(1203,563,1616,595)]),
 ("Renal vein", [C(712,663,894,696)]),
 ("Renal vein", [C(1196,661,1378,693)]),
 ("Right ovarian/testicular vein (→ caudal vena cava)", [C(401,779,905,820)]),
 ("Left ovarian/testicular vein (→ left renal vein)", [C(1125,776,1604,808)]),
 ("Deep circumflex iliac vein", [C(492,911,893,947)]),
 ("Deep circumflex iliac vein", [C(1192,916,1594,952)]),
 ("Common iliac vein", [C(604,1071,941,1102)]),
 ("Common iliac vein", [C(1124,1071,1461,1102)]),
]
cvc = T.raster_card(blank(crop(cvc_src, 'abd2_cvc', Yc), CVC), 'abd2_cvc', CVC, "Caudal vena cava and its tributaries", "Cranial → caudal. Note which gonadal vein drains where (R vs L).", scale=0.8, test=none)
Yp = 155; P = lambda x0,y0,x1,y1: (x0-18, y0-Yp-6, x1-10, y1-Yp+6)
PORTAL = [
 ("Jejunal branches", [P(728,1185,964,1218)]),
 ("Caudal pancreaticoduodenal V.", [P(240,1054,723,1090)]),
 ("Cranial mesenteric V.", [P(892,1033,1298,1066)]),
 ("Caudal mesenteric V.", [P(1025,938,1424,970)]),
 ("Portal V. (begins here)", [P(640,733,773,759)]),
 ("Splenic V.", [P(929,698,1112,739)]),
 ("Gastroduodenal V.", [P(353,568,692,599)]),
 ("Portal vein → liver", [P(703,174,963,213)]),
 ("Liver sinusoids", [P(735,323,959,350)]),
 ("Liver sinusoids", [P(1328,238,1532,266)]),
 ("Central V.", [P(1356,317,1494,346)]),
 ("Hepatic V.", [P(1358,403,1493,433)]),
 ("Caudal vena cava", [P(1276,486,1554,512)]),
]
portal = T.raster_card(blank(crop(portal_src, 'abd2_portal', Yp), PORTAL), 'abd2_portal', PORTAL, "Portal vein: what drains into it, then through the liver", "Bottom → top, then the liver path on the right.", scale=0.8, test=none)
texts = [
 ("Arteries of the stomach?", ["Right gastric a.","Left gastric a.","Right gastroepiploic a.","Left gastroepiploic a."]),
 ("Lesser curvature vs. greater curvature arteries?", ["Lesser curvature: right and left gastric aa.","Greater curvature: right and left gastroepiploic aa."]),
 ("Arteries of the duodenum?", ["Cranial pancreatoduodenal a.","Caudal pancreatoduodenal a."]),
 ("Arteries of the jejunum and ileum?", ["Jejunal aa.","Ileal aa.","Antimesenteric ileal a. (from the cecal a.)"]),
 ("The cecocolic a. gives off…", ["Cecal a. (→ antimesenteric ileal a.)","Colic a. (ascending colon)"]),
 ("Tributaries of the caudal vena cava, cranial → caudal?", ["Hepatic veins","Phrenicoabdominal veins","Renal veins","Right ovarian/testicular vein","Deep circumflex iliac veins","Common iliac veins (formed at the caudal end)"]),
 ("Right vs. left ovarian/testicular vein drain into…", ["Right: caudal vena cava","Left: left renal vein"]),
 ("Veins draining into the portal vein?", ["Gastroduodenal V.","Splenic V.","Caudal mesenteric V.","Cranial mesenteric V. (with jejunal branches and caudal pancreaticoduodenal V.)"]),
 ("Blood path through the liver?", ["Portal vein","Liver sinusoids","Central V.","Hepatic V.","Caudal vena cava"]),
 ("Arteries of the colon, in order?", ["Colic a. (ascending colon)","Right colic a.","Middle colic a. (transverse → descending)","Left colic a. (descending colon)"]),
]
T.write('gross-anatomy-abd2-blood.html', '🩸 Abdominal Blood Supply & Drainage · Trace It',
        'Abdominal Cavity 2 · names pop up one at a time, following the gut.', [card, cvc, portal], texts)
print('ok')
