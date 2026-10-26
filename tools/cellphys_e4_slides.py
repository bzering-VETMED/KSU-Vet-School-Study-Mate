# Cell Physiology · Exam 4 · slide-layout tap-to-reveal pages (keep the professor's grid exactly).
# LC28 S7 "Eicosanoid Functions": 3 enzyme headers over 8 tissue panels (2 rows × 4).
# Called by tools/cellphys_exam4.py → build_slide_pages(HUB, V) returns hub tiles.
import html
E = html.escape
FOOT = '🎀 Bethany · K-State CVM Class of 2030 · VAP 805 · 🐾'

# colors match the slide: brown = PTGS1 (COX-1), green = PTGS2 (COX-2), purple = 5-LOX
C = {'1': '#b5651d', '2': '#7cc242', 'L': '#7b2fa8'}
ENZ = {'1': 'PTGS1 (COX-1)', '2': 'PTGS2 (COX-2)', 'L': '5-LOX'}
# (tissue, enzyme key, eicosanoids HTML, effects HTML)
ROW1 = [('Gastric Mucosa', '1', 'PGE<sub>2</sub>, PGI<sub>2</sub>', 'Cyto&shy;protection<br>Anti-apoptotic'),
        ('Joints / Soft Tissue', '2', 'PGE<sub>2</sub>, PGI<sub>2</sub>, PGD<sub>2</sub>, PGF<sub>2α</sub>', 'Inflammation<br>Pain'),
        ('Colon Cancer', '2', 'PGE<sub>2</sub>', 'Cyto&shy;protection<br>Anti-apoptotic'),
        ('Airways', 'L', 'LTB<sub>4</sub>, LTC<sub>4</sub>, LTD<sub>4</sub>, LTE<sub>4</sub>', 'Broncho&shy;constriction<br>Mucus Secretion')]
ROW2 = [('Platelets', '1', 'TxA<sub>2</sub>', 'Platelet Aggregation<br>Vaso&shy;constriction'),
        ('Endothelium', '2', 'PGI<sub>2</sub>', 'Platelet Resting<br>Vaso&shy;dilation'),
        ('Kidney', '2', 'PGE<sub>2</sub>', 'Dilation of<br>Afferent Arteriole'),
        ('Uterus', '2', 'PGF<sub>2α</sub>', 'Luteolysis')]

CSS = '''*{box-sizing:border-box}body{margin:0;background:#fffafd;color:#34213f;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif}
.wrap{max-width:980px;margin:auto;padding:12px 16px 30px}
.back{display:inline-block;margin:0 0 10px;padding:8px 14px;border-radius:999px;background:#f3eafb;color:#65328c;font-weight:800;text-decoration:none}
.hero{padding:16px 18px;border-radius:20px;color:#fff;background:linear-gradient(135deg,#4b1f70,#8d4eb1 55%,#e05fa8)}.hero h1{margin:0;font-size:clamp(21px,3vw,30px)}.hero p{margin:5px 0 0;font-size:14.5px}
.bar{position:sticky;top:0;z-index:5;background:#fffafdf0;padding:8px 0;display:flex;gap:7px;flex-wrap:wrap;align-items:center}
.bar button{border:0;border-radius:999px;padding:9px 13px;font-weight:800;background:#f3eafb;color:#65328c;font-size:14px}.bar button.on{color:#fff;background:linear-gradient(120deg,#6a3392,#e05fa8)}
.n{margin-left:auto;font-weight:800;color:#754397}
.sub{font-size:14px;color:#5a4566;margin:4px 2px 10px}
.scroll{overflow-x:auto;-webkit-overflow-scrolling:touch;padding-bottom:6px}
.g{display:grid;grid-template-columns:repeat(4,minmax(150px,1fr));gap:8px;min-width:640px}
.enz,.tis,.box{background:#fff;border:3px solid var(--c);text-align:center}
.enz{font-weight:900;font-size:20px;padding:8px 4px}.tis{font-weight:800;padding:5px 4px;font-size:15px}
.box{padding:12px 8px;min-height:120px;display:flex;flex-direction:column;justify-content:center;gap:12px;font-size:15.5px;line-height:1.35}
.r{display:block;cursor:pointer;border-radius:10px;padding:4px 6px;transition:.15s}
.r.h{background:linear-gradient(120deg,#e9dcf5,#f8d4e7);color:transparent;user-select:none}.r.h *{visibility:hidden}
.r.h::after{content:"tap";color:#a0729a;font-weight:800;font-size:13px;visibility:visible}
.r.h{position:relative}.r.h::after{position:absolute;inset:0;display:flex;align-items:center;justify-content:center}
.lg{display:flex;gap:12px;flex-wrap:wrap;font-size:13.5px;margin:10px 2px}.lg span{border-left:6px solid var(--c);padding-left:6px}
.trap{background:#fbe7ef;border:2px solid #d94f7f;border-radius:16px;padding:10px 14px;margin:14px 0}.trap h2{color:#b8336a;margin:0 0 6px;font-size:17px}.trap li{margin:5px 0;font-size:14.5px}
.flag{background:#fff1e3;border:2px dashed #e07b39;border-radius:16px;padding:10px 14px;margin:14px 0;font-size:14px}
.foot{text-align:center;margin:18px 0;font-size:14px}
@media(max-width:700px){.wrap{padding:10px 8px 24px}.g{min-width:0;grid-template-columns:repeat(4,minmax(0,1fr));gap:4px}.enz{font-size:13px;padding:6px 2px;border-width:2px}.enz small{display:block;font-size:10.5px}.tis{font-size:11.5px;padding:4px 2px;border-width:2px}.box{font-size:11.5px;padding:6px 3px;min-height:96px;gap:8px;border-width:2px;overflow-wrap:break-word;hyphens:manual}.r{padding:3px 2px}.r.h::after{font-size:11px}}'''

JS = '''const R=[...document.querySelectorAll('.r')],N=document.getElementById('n');
function upd(){N.textContent=R.filter(r=>!r.classList.contains('h')).length+' / '+R.length+' shown'}
R.forEach(r=>r.onclick=()=>{r.classList.toggle('h');upd()});
const B=[...document.querySelectorAll('.bar button[data-m]')];
function mode(m){B.forEach(b=>b.classList.toggle('on',b.dataset.m===m));R.forEach(r=>{const k=r.dataset.k;
 r.classList.toggle('h', m==='all'?true: m==='ans'?(k==='ei'||k==='fx'): m==='none'?false: m==='ei'?k==='ei': m==='fx'?k==='fx': m==='enz'?(k==='enz'||k==='ei'||k==='fx'): m==='tis'?k==='tis':false)});upd();scrollTo(0,0)}
B.forEach(b=>b.onclick=()=>mode(b.dataset.m));mode('ans');'''

def _panel(row):
    t = ''.join(f'<div class="tis" style="--c:{C[k]}"><span class="r" data-k="tis">{E(n)}</span></div>' for n, k, _, _ in row)
    b = ''.join(f'<div class="box" style="--c:{C[k]}"><span class="r" data-k="ei">{ei}</span><span class="r" data-k="fx">{fx}</span></div>' for _, k, ei, fx in row)
    return t + b

def build_slide_pages(HUB, V):
    enz = (f'<div class="enz" style="--c:{C["1"]}"><span class="r" data-k="enz">PTGS1 <small>(COX-1)</small></span></div>'
           f'<div class="enz" style="--c:{C["2"]};grid-column:span 2"><span class="r" data-k="enz">PTGS2 <small>(COX-2)</small></span></div>'
           f'<div class="enz" style="--c:{C["L"]}"><span class="r" data-k="enz">5-LOX</span></div>')
    grid = f'<div class="scroll"><div class="g">{enz}{_panel(ROW1)}{_panel(ROW2)}</div></div>'
    bar = ('<div class="bar"><button data-m="ans">🙈 Answers</button><button data-m="ei">💊 Eicosanoids</button><button data-m="fx">⚡ Functions</button>'
           '<button data-m="enz">🧪 Enzymes + below</button><button data-m="tis">🫀 Tissues</button><button data-m="all">⬛ Everything</button><button data-m="none">👀 Show all</button><span class="n" id="n"></span></div>')
    legend = (f'<div class="lg"><span style="--c:{C["1"]}"><b>Brown</b> = PTGS1 (prostaglandin G/H synthase 1, COX-1)</span>'
              f'<span style="--c:{C["2"]}"><b>Green</b> = PTGS2 (COX-2)</span><span style="--c:{C["L"]}"><b>Purple</b> = 5-LOX (5-lipoxygenase)</span></div>')
    trap = ('<div class="trap"><h2>⚠️ Precision traps</h2><ul>'
            '<li>Box <b>color = enzyme</b>. Only gastric mucosa + platelets are <b>COX-1</b> (brown). Every other green box is COX-2.</li>'
            '<li><b>Platelets TxA<sub>2</sub></b> = aggregation + vasoCONSTRICTION · <b>Endothelium PGI<sub>2</sub></b> = platelet resting + vasoDILATION. Opposites.</li>'
            '<li>Same PGE<sub>2</sub>, different tissue: gastric/colon = <b>cytoprotection</b> · joints = <b>inflammation, pain</b> · kidney = <b>afferent arteriole dilation</b>.</li>'
            '<li><b>Leukotrienes</b> (LTB<sub>4</sub>–LTE<sub>4</sub>) come from <b>5-LOX</b>, not COX. Airways = bronchoconstriction + mucus.</li>'
            '<li>Uterus = <b>PGF<sub>2α</sub></b> → <b>luteolysis</b> (not PGE<sub>2</sub>).</li>'
            '<li>Why it matters (S20–S29): COX-1 block → <b>ulcers</b> · COX-2-selective block → loses endothelial PGI<sub>2</sub> but keeps platelet TxA<sub>2</sub> → <b>cardiovascular events</b> · any NSAID → less kidney PGE<sub>2</sub> → <b>AKI risk</b>.</li></ul></div>')
    flag = ('<div class="flag">⚠️ <b>Kidney enzyme:</b> green (COX-2) on S7, but S28 draws PTGS1/2 in the kidney. Answer "COX-2" if asked from this table; know both make kidney PGE<sub>2</sub>. Confirm with the transcript.</div>')
    body = (f'<a class="back" href="{HUB}?v={V}">← Back to Cell Physiology</a>'
            f'<div class="hero"><h1>🔥 LC28 · Eicosanoid Functions (S7)</h1><p>Slide layout kept · say it, then tap · repeated on S14, S20, S22, S25, S27, S29: the lecture\'s backbone</p></div>'
            f'{bar}<div class="sub">Different eicosanoids have different functions in different tissues. Pick a mode, say each hidden cell out loud, tap to check.</div>'
            f'{grid}{legend}{trap}{flag}<div class="foot">{FOOT}</div>')
    fn = 'cellphys-lc28-functions.html'
    open(fn, 'w').write(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
                        f'<title>🔥 LC28 Eicosanoid Functions</title><style>{CSS}</style></head><body><div class="wrap">{body}</div><script>{JS}</script></body></html>')
    print('slide pages', [fn])
    return (f'<a class="tile" href="{fn}?v={V}"><div class="emoji">🔥</div><h2>LC28 Eicosanoid Functions (S7)</h2>'
            f'<p>Slide grid kept · tap to reveal · hide eicosanoids, functions, enzymes or tissues</p></a>')

# ---- LC28 S13 "Eicosanoids and Inflammation": 8 effects around the center + 4 cardinal signs
INF = [['Neutrophil Recruitment and Activation', 'Hyperalgesia', 'Enhanced Epithelial Barrier Function'],
       ['Eosinophil Recruitment and Activation', None, 'Platelet Aggregation'],
       ['Mast Cell Maturation', 'Vasodilation and Leakage', 'Smooth Muscle Contraction']]
SIGNS = [('Rubor', 'Redness', 'due to vasodilation'), ('Tumor', 'Swelling', 'due to vascular permeability'),
         ('Calor', '↑ Temperature', 'due to activation of leukocytes (cytokines)'), ('Dolor', 'Pain', 'due to increased nociception')]
ICSS = ('.ig{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin:8px 0}.ic{border:2px solid #c9b3dc;border-radius:12px;background:#fff;padding:10px 6px;text-align:center;min-height:74px;display:flex;align-items:center;justify-content:center;font-size:15px}'
        '.ic.mid{border:3px solid #6a3392;flex-direction:column;font-size:13px}.ic.mid b{font-size:19px;color:#4b1f70}.ic.mid i{display:block;line-height:1.35}'
        '.cs{display:grid;grid-template-columns:110px 1fr;gap:6px 10px;align-items:center;margin:8px 0}.cs .lat{font-weight:900;font-size:18px;color:#4b1f70}.cs .r{text-align:left;background:#fff;border:2px solid #c9b3dc}'
        'h2.s{font-size:18px;color:#65328c;margin:16px 0 4px}@media(max-width:700px){.ic{font-size:12.5px;min-height:64px;padding:6px 3px}.ic.mid b{font-size:15px}.ic.mid{font-size:11px}}')
IJS = JS.replace("m==='ei'?k==='ei': m==='fx'?k==='fx': m==='enz'?(k==='enz'||k==='ei'||k==='fx'): m==='tis'?k==='tis':false", "m==='ei'?k==='ei': m==='fx'?k==='fx': m==='tis'?k==='tis':false")

def build_inflam(HUB, V):
    cells = ''
    for row in INF:
        for c in row:
            cells += ('<div class="ic mid"><b>Eicosanoids</b><i>Prostaglandins<br>Prostacyclins<br>Thromboxanes<br>Leukotrienes</i></div>' if c is None
                      else f'<div class="ic"><span class="r" data-k="ei">{E(c)}</span></div>')
    signs = ''.join(f'<div class="lat"><span class="r" data-k="tis">{a}</span></div><div><span class="r" data-k="fx"><b>{E(b)}</b> {E(c)}</span></div>' for a, b, c in SIGNS)
    bar = ('<div class="bar"><button data-m="ans">🙈 Answers</button><button data-m="ei">🕸️ 8 effects</button><button data-m="fx">🔥 Sign meanings</button>'
           '<button data-m="tis">🔁 Latin names</button><button data-m="none">👀 Show all</button><span class="n" id="n"></span></div>')
    trap = ('<div class="trap"><h2>⚠️ Precision traps</h2><ul>'
            '<li><b>Rubor</b> = redness (vasoDILATION) · <b>Tumor</b> = swelling (vascular PERMEABILITY), not a cancer here.</li>'
            '<li><b>Calor</b> = heat from leukocyte activation (<b>cytokines</b>) · <b>Dolor</b> = pain from ↑ <b>nociception</b> (hyperalgesia).</li>'
            '<li>Slide says <b>FOUR</b> cardinal signs (textbooks add a 5th, loss of function, outside).</li>'
            '<li>Not every arrow is "bad": eicosanoids also <b>enhance epithelial barrier function</b>.</li></ul></div>')
    body = (f'<a class="back" href="{HUB}?v={V}">← Back to Cell Physiology</a>'
            '<div class="hero"><h1>🔥 LC28 · Eicosanoids and Inflammation (S13)</h1><p>Slide layout kept · say it, then tap</p></div>'
            f'{bar}<h2 class="s">8 things eicosanoids do</h2><div class="ig">{cells}</div>'
            f'<h2 class="s">Eicosanoids mediate all four cardinal signs of inflammation</h2><div class="cs">{signs}</div>{trap}<div class="foot">{FOOT}</div>')
    fn = 'cellphys-lc28-inflammation.html'
    open(fn, 'w').write(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
                        f'<title>🔥 LC28 Inflammation</title><style>{CSS}{ICSS}</style></head><body><div class="wrap">{body}</div><script>{IJS}</script></body></html>')
    print('slide pages', [fn])
    return (f'<a class="tile" href="{fn}?v={V}"><div class="emoji">🌡️</div><h2>LC28 Eicosanoids and Inflammation (S13)</h2>'
            f'<p>8 effects + rubor, tumor, calor, dolor · tap to reveal</p></a>')
