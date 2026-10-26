# One-page tap-to-reveal TERMS pages (made by Claude). Replaces the lc_cards.py output pages.
# Data: tools/terms/<KEY>.json  {"sections":[{"title","items":[{"q","a","star","why"}]}],"traps":[...]}
# Run from repo root: python3 tools/terms_page.py
import json, os, html as H, time
HERE = os.path.dirname(__file__)
CSS = open(os.path.join(HERE, "review.css")).read() + """
tr.star td{background:#FBE7EF!important}tr.star td:first-child:before{content:"★ ";color:#D94F7F}
.why{display:none;font-size:12px;color:#8a6b99;font-style:italic;margin-top:2px}.ans.on+.why{display:block}
.traps{background:#FBE7EF;border:2px solid #D94F7F;border-radius:14px;padding:8px 12px;margin:0 0 12px}
.traps h2{margin:0 0 4px;font-size:18px;color:#B03A66}.traps ul{margin:4px 0 0;padding-left:20px}.traps li{margin:3px 0}
.miss{border:0;background:none;font-size:15px;cursor:pointer;opacity:.35;padding:0 2px}.miss.on{opacity:1}
td.m{width:28px;text-align:center}.legend{font-size:13px;color:#8a6b99;margin:6px 0 10px}
.bar button.hot{background:linear-gradient(120deg,#7b42a0,#e05fa8);color:#fff}
"""
JS = r"""const A=[...document.querySelectorAll('.ans')],N=document.getElementById('n');
function u(){N.textContent=A.filter(a=>a.classList.contains('on')).length+' / '+A.length}
A.forEach(a=>a.onclick=()=>{a.classList.toggle('on');u()});
document.getElementById('all').onclick=()=>{A.forEach(a=>a.classList.add('on'));u()};
document.getElementById('hide').onclick=()=>{A.forEach(a=>a.classList.remove('on'));u();scrollTo(0,0)};
document.querySelectorAll('.miss').forEach(b=>b.onclick=()=>b.classList.toggle('on'));
document.getElementById('copy').onclick=()=>{const m=[...document.querySelectorAll('.miss.on')].map(b=>{const r=b.closest('tr');return '• '+r.children[0].textContent+' → '+r.querySelector('.ans').textContent});
 const t=m.length?('Misses — '+document.title+'\n'+m.join('\n')):'No misses marked yet (tap ✗ on a row).';
 (navigator.clipboard?navigator.clipboard.writeText(t):Promise.reject()).then(()=>alert('Copied '+m.length+' misses'),()=>prompt('Copy:',t))};
const cols=document.querySelector('.cols'),orig=[...cols.children],R=[...cols.querySelectorAll('tr')],home=R.map(x=>x.parentNode);
const S=document.getElementById('shuf'),T=document.getElementById('topic'),ST=document.getElementById('staronly');
const mix=document.createElement('div');mix.className='sec';mix.innerHTML='<h2>🔀 Mixed</h2><table></table>';
function rebuild(){R.forEach((x,i)=>home[i].appendChild(x))}
S.onclick=()=>{const r=R.slice();for(let i=r.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[r[i],r[j]]=[r[j],r[i]]}
 const t=mix.querySelector('table');r.forEach(x=>t.appendChild(x));cols.replaceChildren(mix);cols.style.columnCount=1;
 A.forEach(a=>a.classList.remove('on'));u();T.hidden=false;S.textContent='🔀 Reshuffle';scrollTo(0,0)};
T.onclick=()=>{cols.replaceChildren(...orig);rebuild();cols.style.columnCount='';T.hidden=true;S.textContent='🔀 Shuffle';A.forEach(a=>a.classList.remove('on'));u();scrollTo(0,0)};
let so=false;ST.onclick=()=>{so=!so;ST.classList.toggle('hot',so);R.forEach(r=>r.style.display=(so&&!r.classList.contains('star'))?'none':'');
 document.querySelectorAll('.cols .sec').forEach(s=>s.style.display=[...s.querySelectorAll('tr')].some(r=>r.style.display!=='none')?'':'none')};
u();"""

PAGES = [("L17", "gross-anatomy-lc17-cards.html", "L17 Terms · Nervous System 1"),
         ("L18", "gross-anatomy-lc18-cards.html", "L18 Terms · Autonomic Nervous System"),
         ("L19", "gross-anatomy-lc19-cards.html", "L19 Terms · Thoracic Limb Vessels & Nerves"),
         ("ABD1", "gross-anatomy-lcabd1-cards.html", "Abdominal Cavity 1 Terms"),
         ("ABD2", "gross-anatomy-lcabd2-cards.html", "Abdominal Cavity 2 Terms"),
         ("L22", "gross-anatomy-lc22-cards.html", "L22 Terms · Urinary System"),
         ("L23", "gross-anatomy-lc23-cards.html", "L23 Terms · Male Reproductive"),
         ("L24", "gross-anatomy-lc24-cards.html", "L24 Terms · Female Reproductive"),
         ("L25", "gross-anatomy-lc25-cards.html", "L25 Terms · Abdominal Radiology"),
         ("PATTERNS", "gross-anatomy-patterns.html", "Memory Patterns · Exam 3"),
         ("L26", "gross-anatomy-lc26-cards.html", "L26 Terms · Pelvic Limb Vessels & Nerves (slides · lecture Monday)", "gross-anatomy-exam4.html")]

def build(key, out, title, V, back="gross-anatomy-exam3.html"):
    d = json.load(open(os.path.join(HERE, "terms", key + ".json")))
    n = sum(len(s["items"]) for s in d["sections"]); ns = sum(1 for s in d["sections"] for i in s["items"] if i.get("star"))
    body = ""
    for k, s in enumerate(d["sections"]):
        rows = ""
        for it in s["items"]:
            why = f'<div class="why">★ {H.escape(it["why"])}</div>' if it.get("star") and it.get("why") else ""
            rows += (f'<tr class="{"star" if it.get("star") else ""}"><td>{H.escape(it["q"])}</td>'
                     f'<td><span class="ans">{H.escape(it["a"])}</span>{why}</td><td class="m"><button class="miss" title="Mark as missed">✗</button></td></tr>')
        body += f'<div class="sec{" p" if k % 2 else ""}"><h2>{H.escape(s["title"])}</h2><table>{rows}</table></div>'
    traps = "".join(f"<li>{H.escape(t)}</li>" for t in d.get("traps", []))
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{H.escape(title)}</title><style>{CSS}</style></head><body><div class="wrap">'
            f'<a class="back" href="{back}?v={V}">← Back to {"Exam 3" if back == "gross-anatomy-exam3.html" else "Exam 4"}</a>'
            f'<div class="hero"><h1>⚡ {H.escape(title)}</h1><p>Say it, then tap the pink box · {n} terms · ★ {ns} emphasized by the professor</p></div>'
            f'<div class="bar"><button id="hide">🙈 Hide all</button><button id="all">👀 Show all</button><button id="shuf">🔀 Shuffle</button>'
            f'<button id="topic" hidden>📚 By topic</button><button id="staronly">★ Only</button><button id="copy">📋 Copy misses</button><span class="n" id="n"></span></div>'
            f'<p class="legend">★ pink rows = professor emphasized · tap ✗ to mark a miss, then 📋 Copy misses</p>'
            f'<div class="traps"><h2>⚠️ Precision traps</h2><ul>{traps}</ul></div>'
            f'<div class="cols">{body}</div><div class="foot">🎀 Bethany · K-State CVM Class of 2030 · 🐾</div></div><script>{JS}</script></body></html>'), n, ns

if __name__ == "__main__":
    V = str(int(time.time()))
    for key, out, title, *back in PAGES:
        if not os.path.exists(os.path.join(HERE, "terms", key + ".json")):
            print("skip", key); continue
        page, n, ns = build(key, out, title, V, *back)
        open(out, "w").write(page); print(key, n, "terms", ns, "stars")
