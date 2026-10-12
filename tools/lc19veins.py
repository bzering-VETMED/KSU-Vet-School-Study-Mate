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
html_cards = []
for i, c in enumerate(cards):
    html_cards.append(f'''<section class="card" data-kind="img" data-labels='{html.escape(json.dumps(c["labels"]))}'>
<div class="q">{html.escape(c["title"])}<span class="tagline">{len(c["labels"])} names</span></div><p class="hint">{html.escape(c["q"])}</p>
<div class="pic"><img src="{c["img"]}?v={V}" alt=""><div class="ov"></div></div><ol class="trace"></ol></section>''')
for q, ans in TEXT:
    html_cards.append(f'''<section class="card" data-kind="text" data-labels='{html.escape(json.dumps([{"n":a} for a in ans]))}'>
<div class="q textq">{html.escape(q)}<span class="tagline">{len(ans)} to reveal</span></div><ol class="trace big"></ol></section>''')

CSS = '''*{box-sizing:border-box}body{margin:0;background:#fffafd;color:#34213f;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif;padding-bottom:env(safe-area-inset-bottom,0px)}
.wrap{max-width:900px;margin:auto;padding:14px}.back{display:inline-block;margin:0 0 10px;padding:8px 14px;border-radius:999px;background:#f3eafb;color:#65328c;font-weight:800;text-decoration:none}
.hero{color:#fff;background:linear-gradient(135deg,#5d347e,#8855b8 55%,#df78ad);padding:18px 20px;border-radius:22px}.hero h1{margin:0;font-size:24px}.hero p{margin:6px 0 0;opacity:.95}
.bar{position:sticky;top:env(safe-area-inset-top,0px);z-index:5;display:flex;flex-wrap:wrap;gap:6px;align-items:center;background:#fffafdee;padding:10px 0;backdrop-filter:blur(6px)}
.bar button{border:0;border-radius:999px;padding:10px 13px;font-weight:800;font-size:14px;background:#f3eafb;color:#65328c;cursor:pointer}
.bar button.hot{background:linear-gradient(120deg,#7b42a0,#e05fa8);color:#fff}.bar button:focus-visible{outline:3px solid #e05fa8}
.count{margin-left:auto;font-weight:800;color:#8a6b99}
.card{display:none;background:#fff;border:1px solid #eadff2;border-radius:20px;padding:14px;margin-top:6px;box-shadow:0 5px 16px rgba(91,44,124,.06)}.card.on{display:block}
.q{font-weight:900;font-size:19px;color:#5d347e}.q.textq{font-size:21px}.tagline{display:inline-block;margin-left:8px;font-size:12px;background:#fdeaf4;color:#b0679a;border-radius:999px;padding:3px 9px;vertical-align:middle}
.hint{margin:6px 0 10px;color:#8a6b99;font-size:14px}
.pic{position:relative;border-radius:14px;overflow:hidden;background:#fff}.pic img{display:block;width:100%;height:auto}
.ov{position:absolute;inset:0;pointer-events:none}
.tag{position:absolute;transform:translate(-50%,-50%);white-space:nowrap;font-weight:800;border-radius:999px;font-size:clamp(9px,1.9vw,14px);line-height:1.2;padding:2px 7px;box-shadow:0 2px 6px rgba(60,20,80,.25)}
.tag.num{background:#e05fa8;color:#fff;min-width:1.7em;text-align:center}
.tag.name{background:#fff;color:#5d347e;border:2px solid #7b42a0}.tag.name.new{background:#7b42a0;color:#fff}
ol.trace{margin:12px 0 0;padding-left:26px;font-weight:700;color:#5d347e}ol.trace li{margin:4px 0}ol.trace li::marker{color:#e05fa8}ol.trace.big{font-size:18px}
ol.trace li.hid{color:#cdb8dc;list-style-type:"🔒  "}
.done{margin-top:10px;font-weight:800;color:#2f9e76}
@media(prefers-reduced-motion:no-preference){.tag.name.new{animation:pop .25s ease-out}@keyframes pop{from{transform:translate(-50%,-50%) scale(.6)}to{transform:translate(-50%,-50%) scale(1)}}}'''
JS = r'''const cards=[...document.querySelectorAll('.card')];let p=0;const shown=cards.map(()=>0);
const C=document.getElementById('count');
function render(){cards.forEach((c,i)=>c.classList.toggle('on',i===p));const c=cards[p],L=JSON.parse(c.dataset.labels),k=shown[p];
 const ov=c.querySelector('.ov');if(ov){ov.innerHTML='';L.forEach((l,i)=>{const t=document.createElement('span');t.className='tag '+(i<k?'name'+(i===k-1?' new':''):'num');t.textContent=i<k?l.n:(i+1);t.style.left=l.p[0]+'%';t.style.top=l.p[1]+'%';ov.appendChild(t)});}
 const ol=c.querySelector('.trace');ol.innerHTML='';L.forEach((l,i)=>{const li=document.createElement('li');li.textContent=i<k?l.n:'';if(i>=k)li.className='hid';ol.appendChild(li)});
 C.textContent=(p+1)+' / '+cards.length+' · '+k+'/'+L.length;document.getElementById('reveal').textContent=k<L.length?'Reveal next':'Next card ▶';
 document.getElementById('skipb').hidden=p===0;document.getElementById('skip').hidden=p===cards.length-1;}
function total(){return JSON.parse(cards[p].dataset.labels).length}
function reveal(){if(shown[p]<total()){shown[p]++;render()}else if(p<cards.length-1){p++;render();scrollTo(0,0)}}
function back(){if(shown[p]>0){shown[p]--;render()}else if(p>0){p--;render();scrollTo(0,0)}}
reveal_btn=document.getElementById('reveal');reveal_btn.onclick=reveal;
document.getElementById('prev').onclick=back;document.getElementById('next').onclick=reveal;
document.getElementById('skip').onclick=()=>{if(p<cards.length-1){p++;render();scrollTo(0,0)}};
document.getElementById('skipb').onclick=()=>{if(p>0){p--;render();scrollTo(0,0)}};
document.getElementById('all').onclick=()=>{shown[p]=total();render()};
document.getElementById('hide').onclick=()=>{shown[p]=0;render()};
document.querySelectorAll('.pic').forEach(x=>x.onclick=reveal);
document.addEventListener('keydown',e=>{if(['ArrowRight','Enter',' '].includes(e.key)){e.preventDefault();reveal()}else if(e.key==='ArrowLeft'){e.preventDefault();back()}});
render();'''
page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><title>🩸 Thoracic Limb Veins · Trace It</title><style>{CSS}</style></head><body><div class="wrap">
<a class="back" href="gross-anatomy-lecture.html?v={V}">← Back to Lecture</a>
<div class="hero"><h1>🩸 Thoracic Limb Veins · Trace It</h1><p>Lecture 19 · say each name, then tap. Names pop up one at a time in drainage order.</p></div>
<div class="bar"><button id="skipb">⏮ Prev card</button><button id="prev">◀ Prev</button><button class="hot" id="reveal">Reveal next</button><button id="next">Next ▶</button><button id="skip">⏭ Next card</button><button id="all">👀 Show all</button><button id="hide">🙈 Hide all</button><span class="count" id="count"></span></div>
{"".join(html_cards)}
</div><script>{JS}</script></body></html>'''
open('gross-anatomy-lc19-veins.html','w').write(page)
print('ok', len(cards), 'image cards,', len(TEXT), 'text cards')
