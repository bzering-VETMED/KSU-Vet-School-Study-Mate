# Tap-to-reveal tracing decks (made by Claude): slide images with labels erased by inpainting
# only the text strokes; names pop back up one at a time, in order. Used by lc19trace.py.
import os, subprocess, json, time, html, cv2, numpy as np
V = str(int(time.time()))
def erase(im, boxes, test):
    H, W = im.shape[:2]; mask = np.zeros((H, W), np.uint8)
    for (x0, y0, x1, y1) in boxes:
        x0, y0, x1, y1 = max(0,int(x0)), max(0,int(y0)), min(W,int(x1)), min(H,int(y1))
        if x1 <= x0 or y1 <= y0: continue
        mask[y0:y1, x0:x1] |= (test(im[y0:y1, x0:x1].astype(int)) * 255).astype(np.uint8)
    mask = cv2.dilate(mask, np.ones((3,3), np.uint8), iterations=2)
    return cv2.inpaint(im, mask, 7, cv2.INPAINT_TELEA)
black = lambda s: s.max(2) < 120
def black_or_blue(s):
    r, g, b = s[...,2], s[...,1], s[...,0]
    return (s.max(2) < 120) | ((b > 140) & (r < 130) & (g < 130))
def union(bs): return (min(b[0] for b in bs), min(b[1] for b in bs), max(b[2] for b in bs), max(b[3] for b in bs))
def vector_card(pdf, page, out, labels, title, hint, test=black, top=62, tmpdir='/tmp/claude-0'):
    """labels: [(name, [boxes in PDF points])] in reveal order."""
    os.makedirs(tmpdir, exist_ok=True); tmp = f'{tmpdir}/trace_p{page}'
    subprocess.run(['pdftoppm','-r','200','-png','-f',str(page),'-l',str(page),'-singlefile',pdf,tmp], check=True)
    S = 200/72; im = cv2.imread(tmp+'.png')[int(top*S):, :]
    px = lambda b, pad=3: ((b[0]-pad)*S, (b[1]-top-pad)*S, (b[2]+pad)*S, (b[3]-top+pad)*S)
    im = erase(im, [px(b) for _, bs in labels for b in bs], test)
    x0 = int(88*S); body = im[:, x0:]
    ys, xs = np.where(body.astype(int).sum(2) < 690)
    cx0, cy0 = max(0, xs.min()-24), max(0, ys.min()-24)
    cx1, cy1 = min(body.shape[1], xs.max()+24), min(body.shape[0], ys.max()+24)
    im = body[cy0:cy1, cx0:cx1]; ox, oy = x0+cx0, cy0
    H, W = im.shape[:2]; cv2.imwrite(f'assets/{out}.jpg', im, [cv2.IMWRITE_JPEG_QUALITY, 85])
    sh = lambda b: (b[0]-ox, b[1]-oy, b[2]-ox, b[3]-oy)
    return dict(title=title, q=hint, img=f'assets/{out}.jpg', labels=[dict(n=n, p=pos(sh(px(union(bs),0)),H,W)) for n, bs in labels])
def raster_card(src, out, labels, title, hint, scale=2, test=None):
    im = cv2.imread(src); im = cv2.resize(im, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
    sc = lambda b: tuple(v*scale for v in (b[0]-2, b[1]-2, b[2]+2, b[3]+2))
    test = test or (lambda s: s.max(2) < 120)
    im = erase(im, [sc(b) for _, bs in labels for b in bs], test)
    H, W = im.shape[:2]; cv2.imwrite(f'assets/{out}.jpg', im, [cv2.IMWRITE_JPEG_QUALITY, 88])
    return dict(title=title, q=hint, img=f'assets/{out}.jpg', labels=[dict(n=n, p=pos(sc(union(bs)),H,W)) for n, bs in labels])
def pos(b, H, W): return [round((b[0]+b[2])/2/W*100,2), round((b[1]+b[3])/2/H*100,2)]
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
.ov{position:absolute;inset:0;pointer-events:none}.inner{position:relative}body.zoomed .pic{overflow:auto}body.zoomed .inner{width:200%}body.zoomed .tag{font-size:clamp(11px,2.6vw,16px)}
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
 const ov=c.querySelector('.ov');if(ov){ov.innerHTML='';L.forEach((l,i)=>{const t=document.createElement('span');t.className='tag '+(i<k?'name'+(i===k-1?' new':''):'num');t.textContent=i<k?(l.s||l.n):(i+1);t.style.left=l.p[0]+'%';t.style.top=l.p[1]+'%';ov.appendChild(t)});}
 const ol=c.querySelector('.trace');ol.innerHTML='';L.forEach((l,i)=>{const li=document.createElement('li');li.textContent=i<k?l.n:'';if(i>=k)li.className='hid';ol.appendChild(li)});
 C.textContent=(p+1)+' / '+cards.length+' · '+k+'/'+L.length;document.getElementById('reveal').textContent=k<L.length?'Reveal next':'Next card ▶';
 document.getElementById('skipb').hidden=p===0;document.getElementById('skip').hidden=p===cards.length-1;}
function total(){return JSON.parse(cards[p].dataset.labels).length}
function reveal(){if(shown[p]<total()){shown[p]++;render()}else if(p<cards.length-1){p++;document.getElementById('zoom').onclick=e=>{document.body.classList.toggle('zoomed');e.target.classList.toggle('hot')};render();scrollTo(0,0)}}
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

def write(path, title, sub, cards, texts, back='gross-anatomy-exam3.html'):
    hc = []
    for c in cards:
        hc.append(f'''<section class="card" data-kind="img" data-labels='{html.escape(json.dumps(c["labels"]))}'>
<div class="q">{html.escape(c["title"])}<span class="tagline">{len(c["labels"])} names</span></div><p class="hint">{html.escape(c["q"])}</p>
<div class="pic"><div class="inner"><img src="{c["img"]}?v={V}" alt=""><div class="ov"></div></div></div><ol class="trace"></ol></section>''')
    for q, ans in texts:
        hc.append(f'''<section class="card" data-kind="text" data-labels='{html.escape(json.dumps([{"n":a} for a in ans]))}'>
<div class="q textq">{html.escape(q)}<span class="tagline">{len(ans)} to reveal</span></div><ol class="trace big"></ol></section>''')
    page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><title>{html.escape(title)}</title><style>{CSS}</style></head><body><div class="wrap">
<a class="back" href="{back}?v={V}">← Back to {"Exam 3" if back == "gross-anatomy-exam3.html" else "Lecture"}</a>
<div class="hero"><h1>{html.escape(title)}</h1><p>{html.escape(sub)}</p></div>
<div class="bar"><button id="skipb">⏮ Prev card</button><button id="prev">◀ Prev</button><button class="hot" id="reveal">Reveal next</button><button id="next">Next ▶</button><button id="skip">⏭ Next card</button><button id="all">👀 Show all</button><button id="hide">🙈 Hide all</button><button id="zoom">🔍 Zoom</button><span class="count" id="count"></span></div>
{"".join(hc)}
</div><script>{JS}</script></body></html>'''
    open(path, 'w').write(page)
