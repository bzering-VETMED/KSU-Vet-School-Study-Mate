# Abdominal blood supply tracing deck (made by Claude). Run from repo root: python3 tools/abd2blood.py /path/to/IMG_4538.jpeg
import cv2, sys, os; sys.path.insert(0, os.path.dirname(__file__)); import tracer as T
src = sys.argv[1]; X, Y = 318, 180
os.makedirs('/tmp/claude-0', exist_ok=True); tmp = '/tmp/claude-0/abd2_blood_src.jpg'
cv2.imwrite(tmp, cv2.imread(src)[Y:, X:], [cv2.IMWRITE_JPEG_QUALITY, 95])
B = lambda x0,y0,x1,y1: (x0-X-4, y0-Y-4, x1-X+4, y1-Y+4)
dark = lambda s: s.max(2) < 115
labels = [
 ("Right gastric a.", [B(915,240,966,264)]),
 ("Left gastric a.", [B(1012,233,1154,260)]),
 ("Right gastroepiploic a.", [B(906,284,947,310)]),
 ("Left gastroepiploic a.", [B(998,288,1214,317)]),
 ("Cranial pancreaticoduodenal a.", [B(593,260,838,336)]),
 ("Cranial pancreaticoduodenal a.", [B(518,372,547,622)]),
 ("Caudal pancreaticoduodenal a.", [B(520,662,550,908)]),
 ("Caudal pancreaticoduodenal a.", [B(820,1038,1088,1088)]),
 ("Caudal pancreaticoduodenal a.", [B(1236,662,1264,912)]),
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
texts = [
 ("Arteries of the stomach?", ["Right gastric a.","Left gastric a.","Right gastroepiploic a.","Left gastroepiploic a."]),
 ("Lesser curvature vs. greater curvature arteries?", ["Lesser curvature: right and left gastric aa.","Greater curvature: right and left gastroepiploic aa."]),
 ("Arteries of the duodenum?", ["Cranial pancreaticoduodenal a.","Caudal pancreaticoduodenal a."]),
 ("Arteries of the jejunum and ileum?", ["Jejunal aa.","Ileal aa.","Antimesenteric ileal a. (from the cecal a.)"]),
 ("The cecocolic a. gives off…", ["Cecal a. (→ antimesenteric ileal a.)","Colic a. (ascending colon)"]),
 ("Arteries of the colon, in order?", ["Colic a. (ascending colon)","Right colic a.","Middle colic a. (transverse → descending)","Left colic a. (descending colon)"]),
]
T.write('gross-anatomy-abd2-blood.html', '🩸 Abdominal Blood Supply · Trace It',
        'Abdominal Cavity 2 · names pop up one at a time, following the gut.', [card], texts)
print('ok')
