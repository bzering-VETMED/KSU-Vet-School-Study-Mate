# L25 Abdominal Radiographic Anatomy Lab · Practice Questions (made by Claude). Dr. McHaney's lab deck, 34 slides.
# Answer key = Group 29's turned-in worksheet ("Group 29 answer"); "how you know" lines come only from her lecture
# (transcript + Normal Radiographic Anatomy of the Abdomen slides). Where Claude's read of the image disagrees,
# the group answer is kept and a "⚠️ check:" note explains why. Questions 4–5 were not on the group sheet.
# Run from repo root: python3 tools/l25radlab.py /path/to/Lecture_25_Abdominal_Anatomy_Lab_2026.pptx
# Technique: soffice → PDF → pdftoppm keeps the yellow arrows / circles (vector shapes, they ARE the question pointers);
# each question image is the slide cropped below its title. Questions 4–5 use the full-res embedded TIFFs (no pointers).
import os, sys, subprocess, zipfile, io, cv2, numpy as np
from PIL import Image
sys.path.insert(0, os.path.dirname(__file__)); import tracer as T
pptx = os.path.abspath(sys.argv[1]); TMP = '/tmp/claude-0/l25radlab'; os.makedirs(TMP, exist_ok=True)
SEP = ' — '
G = 'Group 29 answer: '
pdf = f'{TMP}/lab.pdf'
if not os.path.exists(pdf):
    subprocess.run(['cp', pptx, f'{TMP}/lab.pptx'], check=True)
    subprocess.run(['soffice', '--headless', '--convert-to', 'pdf', '--outdir', TMP, f'{TMP}/lab.pptx'], check=True, capture_output=True)

def slide(n):
    f = f'{TMP}/s-{n:02d}.png'
    if not os.path.exists(f):
        subprocess.run(['pdftoppm', '-r', '200', '-png', '-singlefile', '-f', str(n), '-l', str(n), pdf, f[:-4]], check=True)
    return cv2.imread(f)

def save(im, out, maxw=1600):
    if im.shape[1] > maxw: im = cv2.resize(im, (maxw, round(im.shape[0] * maxw / im.shape[1])), interpolation=cv2.INTER_AREA)
    cv2.imwrite(f'assets/{out}.jpg', im, [cv2.IMWRITE_JPEG_QUALITY, 86])
    return f'assets/{out}.jpg'

BADGE = {'Medial iliac': 'Medial iliac lymph nodes', 'Left lobe (left': 'Left lobe of the pancreas'}
def lab(name, p):
    d = dict(n=name, p=[round(p[0], 2), round(p[1], 2)])
    if SEP in name: d['s'] = name.split(SEP)[0].replace(G, '')
    for k, v in BADGE.items():
        if name.startswith(G + k): d['s'] = v
    return d

def qcard(n, out, crop, ref, labels, title, q):
    """crop = slide fractions (x0, y0, x1, y1); labels = [(name, (x, y) in a ref-sized slide, ref = (W, H))]."""
    im = slide(n); H, W = im.shape[:2]; x0, y0, x1, y1 = crop
    img = save(im[int(y0 * H):int(y1 * H), int(x0 * W):int(x1 * W)], out)
    pc = lambda x, y: ((x / ref[0] - x0) / (x1 - x0) * 100, (y / ref[1] - y0) / (y1 - y0) * 100)
    return dict(title=title, q=q, img=img, labels=[lab(nm, pc(*xy)) for nm, xy in labels])

S110, S132 = (1467, 825), (1760, 990)   # the two preview sizes the pointer coordinates were read from
z = zipfile.ZipFile(pptx)
def tiff(name):
    return cv2.cvtColor(np.array(Image.open(io.BytesIO(z.read(f'ppt/media/{name}'))).convert('RGB')), cv2.COLOR_RGB2BGR)

cards = []
NOT = 'Not on group sheet · Claude\'s read'
# ---- Questions 4 and 5: Husky case (slides 3–6), no pointers on the slide
Q45 = 'Question 4 and 5 — slide has no other text. Worksheet 4 = your systematic approach; 5 = find items a–q (see the worksheet cards).'
for out, media, ref, title, labels in [
    ('l25radlab_q45_rlat', 'image1.tiff', (1600, 1191), 'Questions 4 and 5 · Husky · view 1', [
        (f"Right lateral — RIGHT marker, right side down. {NOT}", (1000, 1015)),
        (f"Liver — cranioventral soft tissue against the diaphragm; ventral border outlined by falciform fat. {NOT}", (190, 650)),
        (f"Descending colon — mottled fecal material, dorsal caudal abdomen. {NOT}", (1180, 510)),
        (f"Small intestine — tubular, gas and fluid, spread through the mid abdomen. {NOT}", (560, 610))]),
    ('l25radlab_q45_llat', 'image2.tiff', (1600, 968), 'Questions 4 and 5 · Husky · view 2', [
        (f"Left lateral — LEFT marker, left side down. {NOT}", (920, 935)),
        (f"Pylorus — likely: gas in the ventral cranial stomach; left lateral puts the right-sided pylorus up, so it fills with gas — confirm in lab. {NOT}", (330, 640)),
        (f"Descending colon — fecal material ventral to the caudal lumbar spine. {NOT}", (1110, 380))]),
    ('l25radlab_q45_vd', 'image3.tiff', (1195, 1600), 'Questions 4 and 5 · Husky · view 3', [
        (f"Ventrodorsal — LEFT marker sits on the viewer's right. {NOT}", (1020, 1210)),
        (f"Body of the stomach — likely: gas on the patient's left; ventrodorsal sends gas to the body and pylorus — confirm in lab. {NOT}", (720, 420)),
        (f"Pylorus — likely: rounded structure on the patient's right cranial abdomen — confirm in lab. {NOT}", (430, 310)),
        (f"Rectum — feces in the pelvic canal (continuation of the colon). {NOT}", (540, 1500))]),
]:
    im = tiff(media); img = save(im, out)
    cards.append(dict(title=title, q=Q45, img=img,
                      labels=[lab(nm, (x / ref[0] * 100, y / ref[1] * 100)) for nm, (x, y) in labels]))

Q = [
    (7, 'q06', (0.218, 0.288, 0.781, 1), S110, [
        (G + "Right lateral — group's reason: the diaphragmatic crura are parallel (outside knowledge, NOT in her lecture; her rule: gas in the fundus = right lateral, gas in the pylorus and duodenum = left lateral). "
         "⚠️ check: the only big gas pocket is the rounded VENTRAL cranial stomach (pylorus region) and the dorsal fundus looks soft tissue, which by her rule reads LEFT lateral — confirm in lab.", (555, 650))],
     '6. Is this a right lateral or left lateral radiograph? How do you know?'),
    (8, 'q07', (0.03, 0.25, 0.89, 0.985), S110, [
        (G + "Cecum — C-shaped, compartmentalized, gas-filled corkscrew in the right mid abdomen (dog). High confidence.", (420, 482)),
        ("Same structure on the ventrodorsal — Cecum, patient's right mid abdomen.", (1015, 477))],
     '7. Identify the indicated structure.'),
    (9, 'q08', (0.198, 0.27, 0.758, 0.98), S110, [
        (G + "Medial iliac (iliosacral / sublumbar) lymph nodes — circle sits ventral to the sixth and seventh lumbar vertebrae, dorsal to the descending colon. High confidence.", (950, 460))],
     '8. Which lymph nodes, not normally seen on radiographs, are present within the region indicated by the circle?'),
    (10, 'q09', (0.17, 0.285, 0.86, 1), S110, [
        (G + "Deep circumflex iliac arteries — seen end-on as round soft tissue dots ventral to the caudal lumbar spine; mistaken for lymph nodes or stones. High confidence.", (910, 480))],
     '9. Identify the indicated vascular structure, which may be misidentified as a ureteral stone or enlarged lymph node.'),
    (11, 'q10', (0.06, 0.24, 0.88, 1), S110, [
        (G + "Colon — large-diameter segment with mixed fecal / gas content running toward the pelvic canal; the descending colon is mobile and can sit left or right. Medium-high confidence.", (565, 512)),
        ("Same sock on the ventrodorsal — Colon.", (925, 477))],
     '10. This patient ate a sock, which is currently visible within the intestinal tract and indicated by an arrow. In which segment of the GI tract is the sock located?'),
    (12, 'q11', (0.26, 0.2, 0.64, 1), S110, [
        (G + "Duodenum — right cranial abdomen just caudal to the costal arch (R marker = patient's right); the duodenum is a right-sided structure. Medium confidence.", (522, 360))],
     '11. Identify the indicated structure.'),
    (13, 'q12', (0.18, 0.23, 0.79, 1), S110, [
        (G + "Left lateral — the pylorus has gas in it: left side down puts the right-sided pylorus and duodenum up, so they fill with gas. High confidence.", (735, 560))],
     '12. Is this a right lateral or left lateral radiograph? How to you know?'),
    (14, 'q13', (0.05, 0.30, 1, 1), S110, [
        (G + "Pancreas and liver — ⚠️ check: the circle is far cranial (inside the costal arch, ventral on the lateral, patient's right on the ventrodorsal) with mineral — her lecture puts the gallbladder on the ventral and right aspect of the liver (between the right medial and quadrate lobes); the pancreas sits more caudal, at the pyloroduodenal angle. Claude's read: liver and gallbladder — confirm in lab.", (208, 597)),
        ("Same lesion on the ventrodorsal.", (957, 328))],
     '13. This dog is extremely sick and has increased liver enzymes. The abnormality on the abdominal radiographs is circled. Based on the anatomic location, there are two possible organs which may be abnormal. What are those two organs?'),
    (15, 'q14', (0.05, 0.27, 0.95, 1), S132, [
        (G + "Fundus — dorsal stomach just caudal to the diaphragm; left-sided, so it fills with gas on the right lateral. High confidence.", (310, 592)),
        ("Same region on the left lateral — Fundus (now down, holding fluid / food).", (1085, 628))],
     '14. Identify the specific region of the stomach indicated.'),
    (16, 'q15', (0.198, 0.27, 0.758, 0.98), S132, [
        (G + "Mesenteric lymph nodes — circle is in the CENTRAL mid abdomen (not under L6–L7); mesenteric nodes are central and push bowel peripherally. High confidence.", (905, 680))],
     '15. Which lymph nodes, not normally seen on radiographs, are present within the region indicated by the circle?'),
    (17, 'q16', (0.59, 0, 0.895, 1), S132, [
        (G + "Left lobe (left limb) of the pancreas — seen in obese cats because fat surrounds it; runs along the greater curvature of the stomach, larger in cats. High confidence.", (1485, 418))],
     '16. Identify the indicated structure, seen sometimes, especially in obese cats.'),
    (18, 'q17', (0.255, 0.2, 0.745, 1), S132, [
        (G + "Prostate — round soft tissue at the pelvic inlet caudal to the bladder in an intact male; the triangle of fat separates it from the bladder. Medium-high confidence.", (1170, 630))],
     '17. Identify the indicated structure.'),
    (19, 'q18', (0.2, 0.285, 0.745, 1), S132, [
        (G + "Mineral opacity: kidney stones (nephroliths) — white foci in the dorsal retroperitoneal kidney. Medium-high confidence (a few small darker dots in the circle are not explained by the lecture; ask).", (800, 475))],
     '18. This cat has a profoundly abnormal urinary tract. Identify the abnormal opacities present within the indicated kidney.'),
    (20, 'q19', (0.46, 0, 0.98, 1), S132, [
        (G + "Right kidney — on the viewer's left of a ventrodorsal = patient's right. Medium confidence (no side marker visible on the crop; trust but verify).", (1100, 555))],
     '19. This is the same cat as the previous question. Which kidney is indicated?'),
    (21, 'q20', (0.24, 0.18, 0.725, 1), S132, [
        (G + "Spleen — ⚠️ check: the question says 'be specific' — ventral mid abdomen on a dog lateral = the TAIL of the spleen (mobile; the head is fixed in the left cranial abdomen). Write 'tail of the spleen' — confirm in lab.", (1035, 800))],
     '20. Identify the indicated structure. Be specific.'),
    (22, 'q21', (0.105, 0.21, 0.895, 0.95), S132, [
        (G + "Right lateral (liver lobe) — full answer: right lateral liver lobe. In cats the easiest-seen caudoventral liver margin is the right lateral lobe (dogs: left lateral lobe). High confidence.", (620, 705))],
     '21. Which liver lobe is indicated in this cat?'),
    (23, 'q22', (0.05, 0.27, 0.95, 1), S132, [
        (G + "Body of the stomach — ventral, between the fundus and the pylorus. Medium confidence: on the left lateral the gas-filled ventral segment could also be read as the pylorus (left lateral = gas in pylorus) — confirm in lab.", (315, 855)),
        ("Same region on the left lateral — Body (gas-filled).", (1088, 805))],
     '22. Identify the specific region of the stomach indicated.'),
]
for n, out, crop, ref, labels, q in Q:
    cards.append(qcard(n, f'l25radlab_{out}', crop, ref, labels, f"Question {q.split('.')[0]}", q))

# ---- Free practice: slides 25–34 (6 cases, 10 slides). Labels only where certain (view from the marker, one gas pattern).
ORIENT = 'Orient: view, cranial side, then name every structure you can.'
P = [(25, 1, [("Right lateral — R marker", (144, 196)), ("Ventrodorsal — L marker on the viewer's right", (1345, 216))]),
     (26, 1, [("Left lateral — L marker", (826, 766))]),
     (27, 2, [("Right lateral — R marker", (432, 782)), ("Ventrodorsal — two exposures, cranial and caudal", (1250, 278))]),
     (28, 2, [("Left lateral — L marker", (996, 766)),
              ("Pylorus — gas-filled: left lateral puts the right-sided pylorus up", (790, 526))]),
     (29, 3, [("Right lateral — R marker", (480, 762)), ("Ventrodorsal — L marker", (1396, 350))]),
     (30, 3, [("Left lateral — L marker", (904, 756))]),
     (31, 4, [("Right lateral — R marker", (216, 794)), ("Ventrodorsal — L marker", (1350, 52))]),
     (32, 4, [("Left lateral — L marker", (342, 782))]),
     (33, 5, [("Right lateral — R marker", (522, 30))]),
     (34, 6, [("Left lateral — L marker", (896, 760))])]
for n, case, labels in P:
    cards.append(qcard(n, f'l25radlab_p{n}', (0, 0, 1, 1), S110, labels, f'Free practice · case {case} · slide {n}', ORIENT))

TEXTS = [
    ('Worksheet 1. Radiographic opacities, least → most opaque', ['Gas (black)', 'Fat (darker grey)', 'Soft tissue and fluid (same medium grey)', 'Mineral (white)', 'Metal (very white)']),
    ('Worksheet 2. Roentgen signs', ['Deferred to next year — not covered in this lecture']),
    ('Worksheet 3. Two non-standard views + the indication for each', [
        'Compression view — reduces superimposition over an area of interest',
        'Horizontal beam — highlights free gas (peritoneal free gas = possible surgical emergency)',
        'Lateral with the pelvic limbs pulled forward (perineal view) — region of the urethra, urinary stones',
        'Pneumogastrogram / pneumocolonogram — air outlines the stomach or colon (foreign material, mass, colon vs small intestine)',
        "⚠️ Group 29 wrote 'compression: evaluate urinary stones' — wrong per lecture; urinary stones go with the perineal view"]),
    ('Worksheet 4. Systematic approach, in order', [
        'Extra-abdominal structures: non-abdominal soft tissues, body wall, diaphragm, skeleton, thorax',
        'Serosal detail and abdominal contour', 'Large parenchymal organs: liver and spleen',
        'Urogenital: kidneys, urinary bladder, reproductive tract', 'Gastrointestinal tract LAST: stomach, small intestine, colon']),
    ('Worksheet 5. Find it, a–q — where each one lives', [
        'a. Lateral epaxial margins on the ventrodorsal — lumbar muscle lines running alongside the spine',
        'b. Abdominal contour — shape of the abdomen: tucked up, pendulous, or in between',
        "c. Right crus — dorsal part of the diaphragm on the patient's right (ventrodorsal)",
        'd. Falciform fat — fat opacity ventral to the liver',
        'e. Caudoventral liver margin — dogs: left lateral lobe; cats: right lateral lobe',
        'f. Gastric axis — fundus to pylorus; normal = between perpendicular to the spine and parallel to the ribs',
        'g. Splenic head — left cranial abdomen; triangle on the ventrodorsal, fusiform on the lateral',
        'h. Fundus — dorsal, left; gas on the right lateral and dorsoventral',
        'i. Pylorus — right, ventral; gas on the left lateral and ventrodorsal',
        'j. Duodenum — right side; gas on the left lateral',
        'k. Small bowel — tubular, uniform diameter, throughout the abdomen',
        'l. Cecum — C-shaped, compartmentalized, gas-filled, right mid abdomen (dog)',
        'm. Sublumbar (medial iliac) lymph nodes — ventral to the sixth and seventh lumbar vertebrae, dorsal to the descending colon; not seen in health',
        'n. Right kidney size versus the second lumbar vertebra — dogs 2.5 to 3.5 times, cats 2 to 3 times (ventrodorsal)',
        'o. Trigone — neck of the urinary bladder, toward the pelvic canal',
        'p. Deep circumflex iliac artery — round dots ventral to the caudal lumbar spine',
        'q. Uterus — dorsal to the bladder, ventral to the colon; not seen in health']),
]

OUT = 'gross-anatomy-l25-radlab.html'
T.write(OUT, 'Radiology Lab · Practice Questions',
        "Lecture 25 lab · Dr. McHaney · answer key = Group 29's worksheet + lecture reasoning · tap Reveal", cards, texts=TEXTS)
# Move the worksheet text cards ahead of Free practice, and add Shuffle (reorders cards when the URL hash is #shuffle).
h = open(OUT).read()
head, rest = h.split('<section class="card"', 1); rest = '<section class="card"' + rest
body, tail = rest.rsplit('</section>', 1); body += '</section>'
secs = ['<section class="card"' + s for s in body.split('<section class="card"')[1:]]
img = [s for s in secs if 'data-kind="img"' in s]; txt = [s for s in secs if 'data-kind="text"' in s]
k = next(i for i, s in enumerate(img) if 'Free practice' in s)
secs = img[:k] + txt + img[k:]
h = head + '\n'.join(s.rstrip() for s in secs) + tail
h = h.replace('<button id="zoom">', '<button id="shuf">🔀 Shuffle</button><button id="zoom">', 1)
SHUF = ('<script>(function(){const b=document.getElementById("shuf");if(location.hash==="#shuffle"){b.classList.add("hot");'
        'const s=[...document.querySelectorAll("section.card")],par=s[0].parentNode,end=s[s.length-1].nextSibling;'
        'for(let i=s.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[s[i],s[j]]=[s[j],s[i]]}s.forEach(x=>par.insertBefore(x,end))}'
        'b.onclick=()=>{location.hash=location.hash==="#shuffle"?"":"shuffle";location.reload()}})()</script>')
h = h.replace('</div><script>', '</div>' + SHUF + '<script>', 1)
open(OUT, 'w').write(h)
print('ok', len(cards), sum(len(c['labels']) for c in cards), len(TEXTS))
