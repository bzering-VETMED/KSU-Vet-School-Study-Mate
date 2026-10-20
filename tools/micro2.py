# Build: Veterinary Systems I · Lab Practical 2 (Microanatomy Exam 2: Labs 9, 11, 12, 14 + review 1, 2, 3, 4, 7)
# Run from repo root: python3 tools/micro2.py
import sys,os,time,html,re
sys.path.insert(0,'tools')
from micro2_data import FUNCS2,COMPARE,TRAPS,DISAGREE
from micro1_data import FUNCS as FUNCS1
E=html.escape; V=str(int(time.time()))
PRAC='systems-lab-practical2.html'; FS='systems-lp2-functions.html'

# 🧠 functions sheet: one page, tap an answer to reveal (same look as Practical 1)
def row(t,a,hy):
    return f'<tr{" class=hy" if hy else ""}><td>{"★ " if hy else ""}{E(t)}</td><td><span class="ans">{E(a)}</span></td></tr>'
secs=''; n=0
for i,(sec,src,ok,items) in enumerate(FUNCS2):
    n+=len(items)
    note=f'<div class="src">📄 {E(src)}</div>'
    secs+=f'<div class="sec{" p" if i%2 else ""}"><h2>{E(sec)}</h2>{note}<table>{"".join(row(*it) for it in items)}</table></div>'
cmp=''
for title,items in COMPARE:
    n+=len(items)
    cmp+=f'<h3>{E(title)}</h3><table>{"".join(row(t,a,False) for t,a in items)}</table>'
secs+=f'<div class="sec cmp"><h2>⚖️ Compare</h2>{cmp}</div>'
secs+='<div class="sec dis"><h2>🟠 Sources disagree</h2><ul>'+''.join(f'<li>{E(t)}</li>' for t in DISAGREE)+'</ul></div>'
secs+='<div class="sec trap"><h2>⚠️ Precision traps</h2><ul>'+''.join(f'<li>{E(t)}</li>' for t in TRAPS)+'</ul></div>'
rev=''
for i,(sec,items) in enumerate(FUNCS1):
    n+=len(items)
    rev+=f'<div class="sec{" p" if i%2 else ""}"><h2>🔁 {E(sec)}</h2><table>{"".join(row(t,a,False) for t,a in items)}</table></div>'
css=""":root{--ink:#330B4D;--v:#6A0DAD;--g:#7B2FBE;--p:#E0459A;--line:#E3D0F2;--lav:#F5ECFD}*{box-sizing:border-box}body{margin:0;color:var(--ink);font:16px/1.4 -apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif;background:radial-gradient(circle at 0 0,#FBE4F4 0,transparent 30%),radial-gradient(circle at 100% 0,#EFE0FE 0,transparent 32%),#FFFBFD}.wrap{max-width:900px;margin:auto;padding:14px 12px 50px}.back{display:inline-block;margin:0 0 10px;padding:8px 14px;border-radius:999px;background:#f3eafb;color:#65328c;font-weight:800;text-decoration:none}.hero{color:#fff;border-radius:20px;padding:16px 18px;background:linear-gradient(135deg,#5C1B96,#A22FB5 55%,#E0459A)}.hero h1{margin:0;font-size:24px}.hero p{margin:4px 0 0;font-size:14px}.key{margin:10px 0 0;background:#fff;border:1px dashed var(--line);border-radius:12px;padding:8px 10px;font-size:14px}.bar{position:sticky;top:0;z-index:5;display:flex;gap:8px;flex-wrap:wrap;padding:10px 0;background:#FFFBFD}.bar button{border:0;border-radius:999px;padding:9px 14px;background:#f3eafb;color:#65328c;font-weight:800;font-size:15px}.bar .n{margin-left:auto;align-self:center;font-weight:800;color:var(--g)}.cols{column-count:2;column-gap:12px}@media(max-width:700px){.cols{column-count:1}}.sec{break-inside:avoid;background:#fff;border:1px solid var(--line);border-left:6px solid var(--g);border-radius:14px;padding:8px 10px;margin:0 0 12px}.sec.p{border-left-color:var(--p)}.sec h2{margin:0 0 4px;font-size:18px;color:var(--v)}.sec h3{margin:8px 0 2px;font-size:15px;color:var(--p)}.src{font-size:12px;color:#8a6b99;margin:0 0 4px}.sec.trap{border-left-color:#E8A317;background:#FFF8EC}.sec.trap ul{margin:0;padding-left:18px;font-size:15px}.sec.trap li{margin:3px 0}.sec.dis{border-left-color:#F07F1A;background:#FFF1E4}.sec.dis ul{margin:0;padding-left:18px;font-size:15px}.sec.dis li{margin:3px 0}.sec.cmp{border-left-color:var(--p)}table{width:100%;border-collapse:collapse;font-size:15px}td{padding:6px;border-bottom:1px solid #F0E4F7;vertical-align:top}tr:nth-child(even) td{background:var(--lav)}tr.hy td{background:#FDE3F1}td:first-child{font-weight:700;color:var(--v);width:47%}.ans{display:inline-block;min-width:90%;border-radius:8px;padding:2px 6px;cursor:pointer;background:linear-gradient(135deg,#C9B6E4,#F2B6D6);color:transparent;user-select:none;transition:background .15s}.ans.on{background:transparent;color:var(--ink);padding:2px 0}.ans:not(.on):after{content:"tap";color:#fff;font-size:12px;font-weight:800}.ans:not(.on){font-size:0;min-height:22px}.div{margin:18px 0 10px;padding:10px 14px;border-radius:14px;background:#f3eafb;color:#65328c;font-weight:800}.foot{text-align:center;font-size:12px;color:#8a6b99;margin-top:20px}"""
js="""const A=[...document.querySelectorAll('.ans')],N=document.getElementById('n');function u(){N.textContent=A.filter(a=>a.classList.contains('on')).length+' / '+A.length}A.forEach(a=>a.onclick=()=>{a.classList.toggle('on');u()});document.getElementById('all').onclick=()=>{A.forEach(a=>a.classList.add('on'));u()};document.getElementById('hide').onclick=()=>{A.forEach(a=>a.classList.remove('on'));u();scrollTo(0,0)};u();"""
key='<div class="key">★ pink row = high yield · 📘 = standard histology, not stated in your uploaded slides (no CNS, renal or endocrine microanatomy lecture yet) · 🟠 = sources disagree (see box) · 🔁 = review labs 1, 2, 3, 4 & 7</div>'
open(FS,'w').write(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>🧠 Functions Review · Practical 2</title><style>{css}</style></head><body><div class="wrap"><a class="back" href="{PRAC}?v={V}">← Back to Lab Practical 2</a><div class="hero"><h1>🧠 Functions Review · Practical 2</h1><p>Say the answer, then tap the pink box · {n} items · Labs 9, 11, 12, 14 + review</p></div>{key}<div class="bar"><script defer src="shuffle.js"></script><button id="hide">🙈 Hide all</button><button id="all">👀 Show all</button><span class="n" id="n"></span></div><div class="cols">{secs}</div><div class="div">🔁 Review labs 1, 2, 3, 4 & 7 (also on this exam)</div><div class="cols">{rev}</div><div class="foot">🎀 Bethany · K-State CVM Class of 2030 · 🐾</div></div><script>{js}</script></body></html>')

# exam hub
tiles=[f'<div class="tile"><h2>🧠 Functions review</h2><a href="{FS}?v={V}">One page · tap to reveal · {n} items</a></div>',
'<div class="tile"><h2>🔁 Review labs 1, 2, 3, 4 & 7</h2><a href="systems-lab-practical1.html?v='+V+'">Practical 1 image cards + layers</a></div>',
'<div class="tile"><h2>🖼️ Lab image cards</h2><p class="soon">Lab 9 Respiratory · Lab 11 Central nervous system · Lab 12 Urinary · Lab 14 Endocrine · coming next</p></div>']
prac=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>🔬 Systems I · Lab Practical 2</title><style>body{{margin:0;background:#fff9fd;color:#493451;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif}}.wrap{{max-width:1000px;margin:auto;padding:18px}}.hero{{color:#fff;background:linear-gradient(135deg,#5d347e,#8855b8 55%,#df78ad);padding:24px;border-radius:24px}}.hero h1{{margin:0}}.grid{{display:grid;grid-template-columns:repeat(2,1fr);gap:14px;margin-top:16px}}.tile{{background:#fff;border:1px solid #eadff2;border-radius:18px;padding:18px}}.tile h2{{color:#70428f;margin:0 0 10px;font-size:20px}}.tile a{{display:block;text-decoration:none;margin:7px 0;padding:10px;border-radius:12px;background:#f7eefb;color:#70428f;font-weight:800}}.soon{{margin:0;color:#786c7c;font-size:15px}}.note{{margin-top:14px;background:#fff;border:1px dashed #eadff2;border-radius:16px;padding:12px 14px;font-size:15px}}@media(max-width:700px){{.grid{{grid-template-columns:1fr}}}}</style></head><body><div class="wrap"><a href="systems-lab.html?v={V}" style="display:inline-block;margin:0 0 10px;padding:8px 14px;border-radius:999px;background:#f3eafb;color:#65328c;font-weight:800;text-decoration:none">← Back to Systems Lab</a><div class="hero"><h1>🔬 Veterinary Systems I · Lab Practical 2</h1><p>Microanatomy Exam 2 · Labs 9, 11, 12 & 14 + review of 1, 2, 3, 4 & 7 · 50 images, fill-in-the-blank</p></div><div class="note">Spell it exactly; there's no word bank. Lab 13 (Urinalysis) is NOT on this exam.</div><div class="grid">{"".join(tiles)}</div></div></body></html>'''
open(PRAC,'w').write(prac)

s=open('systems-lab.html').read()
s=s.replace('<div class="tile"><h2>Lab Practical 2</h2><p>Ready for study materials</p></div>',f'<a class="tile" href="{PRAC}?v={V}"><div class="emoji">🔬</div><h2>Lab Practical 2</h2><p>Microanatomy · Labs 9, 11, 12 & 14 + review</p></a>')
s=re.sub(r'href="(systems-lab-practical[12]\.html|veterinary-systems\.html)\?v=\d+"',lambda m:f'href="{m.group(1)}?v={V}"',s)
open('systems-lab.html','w').write(s)
for f in ['index.html','fall2026.html','veterinary-systems.html']:
    t=open(f).read(); open(f,'w').write(re.sub(r'href="([a-z0-9\-]+\.html)\?v=\d+"',lambda m:f'href="{m.group(1)}?v={V}"',t))
sw=open('sw.js').read(); open('sw.js','w').write(re.sub(r"ksu-study-mate-v(\d+)-\d+",lambda m:f"ksu-study-mate-v{int(m.group(1))+1}-{V}",sw))
print('items',n)
