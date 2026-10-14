# Abdominal Cavity 1 (Diehl) flow-of-ingesta tracing deck (made by Claude). Run from repo root:
# python3 tools/abd1trace.py /path/to/flow_slide.jpg
import cv2, sys, os; sys.path.insert(0, os.path.dirname(__file__)); import tracer as T
src = sys.argv[1]; panc_src = sys.argv[2] if len(sys.argv) > 2 else None; k = 2473/2000; X = 86
im = cv2.imread(src)[:, X:]; tmp = '/tmp/claude-0/abd1_flow_src.jpg'; os.makedirs('/tmp/claude-0', exist_ok=True)
cv2.imwrite(tmp, im, [cv2.IMWRITE_JPEG_QUALITY, 95])
def purple(s):
    r, g, b = s[...,2], s[...,1], s[...,0]
    return (b-g > 45) & (r-g > 15) & (s.sum(2) < 520)
B = lambda x0,y0,x1,y1: (x0*k-X-8, y0*k-8, x1*k-X+8, y1*k+8)
labels = [
 ("Stomach",[B(895,105,1155,180)]),
 ("Cranial duodenal flexure",[B(345,110,825,245)]),
 ("Descending duodenum",[B(290,310,355,865)]),
 ("Caudal duodenal flexure",[B(535,1110,1130,1175)]),
 ("Ascending duodenum",[B(1210,505,1270,1030)]),
 ("Duodenojejunal flexure (DJF)",[B(1050,370,1135,420)]),
 ("Jejunum",[B(760,495,1010,565)]),
 ("Jejunum",[B(760,645,1010,715)]),
 ("Ileum",[B(730,945,925,1020)]),
 ("Cecum (blind sac; opens into the ascending colon)",[B(465,560,510,755)]),
 ("Ascending colon",[B(550,470,595,715)]),
 ("Right colic flexure (RCF)",[B(555,310,650,365)]),
 ("Transverse colon",[B(720,275,1220,340)]),
 ("Left colic flexure (LCF)",[B(1405,325,1500,380)]),
 ("Descending colon",[B(1465,460,1530,970)]),
 ("DC: descending colon, continuing to the midline → rectum",[B(1350,1025,1450,1110)]),
 ("Root of mesentery (RM)",[B(835,575,900,620)]),
]
card = T.raster_card(tmp, 'abd1_flow', labels, "Flow of ingesta: ventral view, 4 quadrants",
                     "Start at the stomach and follow the arrows. Name each part before you tap.", scale=0.7, test=purple)

cards = [card]
if panc_src:  # LO6 pancreas slide (IMG_4542): grey labels on white
    K = 2536/2000; PX, PY = 60, 180
    P = lambda x0,y0,x1,y1: (x0*K-PX*K-6, y0*K-PY*K-6, x1*K-PX*K+6, y1*K-PY*K+6)
    t2 = '/tmp/claude-0/abd1_panc_src.jpg'
    cv2.imwrite(t2, cv2.imread(panc_src)[int(PY*K):, int(PX*K):], [cv2.IMWRITE_JPEG_QUALITY, 95])
    import numpy as np
    none = lambda s: np.zeros(s.shape[:2], bool)
    PL = [
     ("Pyloric part of stomach", [P(876,203,1328,257)]),
     ("Bile duct", [P(460,320,634,367)]),
     ("Intramural bile duct", [P(230,466,609,514)]),
     ("Major duodenal papilla (pancreatic duct + common bile duct open here)", [P(166,551,609,599)]),
     ("Pancreatic duct (line 1)", [P(640,625,700,655)]),
     ("Duodenum", [P(386,721,602,769)]),
     ("Minor duodenal papilla (accessory pancreatic duct opens here)", [P(163,806,607,854)]),
     ("Accessory pancreatic duct (line 2)", [P(880,975,935,1000)]),
     ("Key: 1 = pancreatic duct · 2 = accessory pancreatic duct", [P(80,898,812,1012)]),
    ]
    im2 = cv2.imread(t2)
    for _, bs in PL:  # labels sit on white: repaint each box with its border colour (no smudge)
        for (x0, y0, x1, y1) in bs:
            x0, y0, x1, y1 = max(0,int(x0)), max(0,int(y0)), int(x1), int(y1)
            sub = im2[y0:y1, x0:x1]; border = np.concatenate([sub[0], sub[-1], sub[:,0], sub[:,-1]])
            im2[y0:y1, x0:x1] = np.median(border, axis=0)
    cv2.imwrite(t2, im2, [cv2.IMWRITE_JPEG_QUALITY, 95])
    cards.append(T.raster_card(t2, 'abd1_pancreas', PL, "Pancreatic ducts and duodenal papillae (LO6)", "Name each label, then which duct opens at which papilla.", scale=0.7, test=none))
texts = [
 ("Trace ingesta from the stomach to the descending colon.", ["Stomach","Cranial duodenal flexure","Descending duodenum","Caudal duodenal flexure","Ascending duodenum","Duodenojejunal flexure","Jejunum","Ileum","Ascending colon","Right colic flexure","Transverse colon","Left colic flexure","Descending colon"]),
 ("Following the transverse colon, ingesta enters…", ["Left colic flexure","Then the descending colon"]),
 ("Descending duodenum runs between which quadrants?", ["Right cranial → right caudal","Pancreas (right lobe) sits in its mesoduodenum"]),
 ("Caudal duodenal flexure runs between which quadrants?", ["Right caudal → left caudal","Caudal to the root of the mesentery"]),
 ("Ascending duodenum runs between which quadrants?", ["Left caudal → left cranial","Duodenocolic fold attaches it to the descending colon"]),
 ("Transverse colon lies ___ to the root of the mesentery.", ["Cranial"]),
 ("In the dog, the ileum opens into the…", ["Ascending colon (ileocolic orifice)","NOT the cecum"]),
 ("In the dog, the cecum opens into the…", ["Ascending colon (cecocolic orifice)"]),
 ("Pancreatic duct vs. accessory pancreatic duct: where do they open?", ["Pancreatic duct → major duodenal papilla (with the common bile duct)","Accessory pancreatic duct → minor duodenal papilla"]),
 ("Which pancreatic duct is larger in the dog? In the cat?", ["Dog: accessory pancreatic duct","Cat: pancreatic duct (accessory absent in ~20% of cats)"]),
 ("Common bile duct is formed by…", ["Cystic duct (gallbladder)","Hepatic duct (liver)"]),
 ("Longest and shortest parts of the small intestine?", ["Longest: jejunum","Shortest: ileum"]),
 ("The midline crossing of the quadrant map is at which level?", ["L1–L2"]),
 ("After the descending colon comes the…", ["Rectum","Then the anus"]),
 ("Where is the root of the mesentery, and what runs in it?", ["Center of the quadrant map","Cranial mesenteric artery"]),
]
T.write('gross-anatomy-abd1-trace.html', '🌀 Flow of Ingesta & Pancreas · Trace It', 'Abdominal Cavity 1 · names pop up one at a time.', cards, texts)
print('ok')
