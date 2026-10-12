# L19 vein tracing deck (made by Claude). Labels erased by inpainting only the text strokes;
# names pop back up one at a time, in drainage order.
# Run from repo root: python3 tools/lc19veins.py /path/to/Lecture_19.pdf /path/to/slide13_left.jpg /path/to/slide13_right.jpg
import sys, os, subprocess, json, time, html, cv2, numpy as np
pdf, left_src, right_src = sys.argv[1:4]
os.makedirs('assets', exist_ok=True)
V = str(int(time.time()))

def erase(im, boxes, test):
    H, W = im.shape[:2]; mask = np.zeros((H, W), np.uint8)
    for (x0, y0, x1, y1) in boxes:
        x0, y0, x1, y1 = max(0,int(x0)), max(0,int(y0)), min(W,int(x1)), min(H,int(y1))
        sub = im[y0:y1, x0:x1].astype(int)
        mask[y0:y1, x0:x1] |= (test(sub) * 255).astype(np.uint8)
    mask = cv2.dilate(mask, np.ones((3,3), np.uint8), iterations=2)
    return cv2.inpaint(im, mask, 7, cv2.INPAINT_TELEA)

cards = []
# ---- Card 1: slide 12 schematic (vector labels, page rendered at 200 dpi) ----
tmp = '/tmp/claude-0/lc19v_s12'
subprocess.run(['pdftoppm','-r','200','-png','-f','12','-l','12','-singlefile',pdf,tmp], check=True)
im = cv2.imread(tmp + '.png'); S = 200/72
TOP = 62  # crop the slide title
im = im[int(TOP*S):, :]
def pt(x0,y0,x1,y1,pad=3): return ((x0-pad)*S, (y0-TOP-pad)*S, (x1+pad)*S, (y1-TOP+pad)*S)
L12 = [  # name, box in PDF points (rotated labels measured from the render)
 ("Accessory cephalic v.", (415,344,508,384)),
 ("Cephalic v.", (311,384,407,402)),
 ("Cephalic v.", (420,228,516,246)),
 ("Median cubital v.", (318,196,400,228)),
 ("Brachial v.", (228,276,300,292)),
 ("Axillary v.", (218,136,287,152)),
 ("Axillobrachial v.", (300,118,406,156)),
 ("Omobrachial v.", (321,103,409,115)),
 ("Cephalic v.", (450,121,546,139)),
 ("External jugular v.", (410,65,570,83)),
 ("Deep venous system", (129,174,201,235)),
 ("Superficial venous system", (566,183,670,245)),
]
black = lambda s: s.max(2) < 120
im = erase(im, [pt(*b) for _, b in L12], black)
H, W = im.shape[:2]
cv2.imwrite('assets/lc19v_schematic.jpg', im, [cv2.IMWRITE_JPEG_QUALITY, 85])
def pct(box, H, W): x0,y0,x1,y1 = box; return [round((x0+x1)/2/W*100,2), round((y0+y1)/2/H*100,2)]
cards.append(dict(title="Schematic: right limb, lateral view (slide 12)", img="assets/lc19v_schematic.jpg",
  q="Trace the blood from the paw to the external jugular. Name each vein before you tap.",
  labels=[dict(n=n, p=pct(pt(*b,pad=0),H,W)) for n,b in L12]))

# ---- Cards 2 and 3: slide 13 images (raster labels, positions found by OCR) ----
def raster(src, name, labels, scale):
    im = cv2.imread(src); im = cv2.resize(im, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
    sc = lambda b: tuple(v*scale for v in (b[0]-2, b[1]-2, b[2]+2, b[3]+2))
    def dark(s):
        mx, mn = s.max(2), s.min(2)
        return (mx < 150) & ((mx - mn) < 70)
    im = erase(im, [sc(b) for _, b in labels], dark)
    H, W = im.shape[:2]; cv2.imwrite(f'assets/{name}.jpg', im, [cv2.IMWRITE_JPEG_QUALITY, 88])
    return [dict(n=n, p=pct(sc(b),H,W)) for n,b in labels]
LEFT = [  # distal → proximal
 ("Dorsal common digital vein IV", (0,318,93,343)),
 ("Accessory cephalic vein", (18,231,94,256)),
 ("Cephalic vein", (165,222,243,235)),
 ("Cephalic vein", (8,151,87,164)),
 ("Median cubital vein", (176,47,289,57)),
 ("Brachial vein", (176,70,251,80)),
 ("Cephalic vein", (7,16,85,29)),
]
cards.append(dict(title="Drawing: thoracic limb veins (slide 13, left)", img="assets/lc19v_drawing.jpg",
  q="Start at the paw and work up. Name each vein before you tap.",
  labels=raster(left_src, 'lc19v_drawing', LEFT, 3)))
RIGHT = [  # distal → proximal; artery and nerve labels stay visible
 ("Median cubital vein", (385,564,499,576)),
 ("Cephalic vein", (404,476,484,489)),
 ("Cephalic vein", (441,388,521,401)),
 ("Axillobrachial vein", (454,364,560,376)),
 ("Omobrachial vein", (470,338,573,351)),
 ("External jugular vein", (506,315,624,328)),
]
cards.append(dict(title="Dissection: lateral view (slide 13, right)", img="assets/lc19v_dissection.jpg",
  q="Only the main veins are hidden. Arteries and nerves stay labeled as landmarks.",
  labels=raster(right_src, 'lc19v_dissection', RIGHT, 2)))

TEXT = [  # (question, [staged answers]) from the slides + 10/11 recording
 ("Name the 5 superficial veins of the thoracic limb.", ["Cephalic vein","Accessory cephalic vein","Median cubital vein","Axillobrachial vein","Omobrachial vein"]),
 ("What makes up the deep venous system?", ["Tributaries of the axillary vein (e.g., brachial vein)","He said not to worry much: deeper, with many collaterals"]),
 ("The cephalic vein drains which side? The accessory cephalic?", ["Cephalic: medial side","Accessory cephalic: dorsal / lateral side"]),
 ("Where does the cephalic vein empty?", ["External jugular vein"]),
 ("What links the superficial and deep systems at the elbow?", ["Median cubital vein","Cephalic → median cubital → brachial vein"]),
 ("What drains into the axillary vein?", ["Brachial vein","Axillobrachial vein (another superficial–deep link)"]),
 ("The omobrachial vein comes off what, and empties where?", ["Off the axillobrachial vein","Into the external jugular vein"]),
 ("Trace the dorsal paw to the external jugular.", ["Dorsal common digital veins","Accessory cephalic vein","Joins the cephalic vein (from medial)","Cephalic vein","External jugular vein"]),
]
sys.path.insert(0, os.path.dirname(__file__)); import tracer as T
T.write('gross-anatomy-lc19-veins.html', '🩸 Thoracic Limb Veins · Trace It',
        'Lecture 19 · say each name, then tap. Names pop up one at a time in drainage order.', cards, TEXT)
print('ok', len(cards), 'image cards,', len(TEXT), 'text cards')
