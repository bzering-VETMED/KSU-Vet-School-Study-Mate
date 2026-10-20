"""Practical 3 · one tap-to-reveal FUNCTIONS page per lab (made by Claude).
★ pink rows = professor emphasis (pre-lab / lecture transcripts) · ⚠️ precision traps box · orange flag boxes.
Data: tools/p3labfn_data.py. Run from repo root: python3 tools/p3labfn.py
Writes gross-anatomy-labN-functions.html, links them from the Practical 3 page and each lab hub."""
import sys,re,time,html
sys.path.insert(0,'tools')
from p3labfn_data import LABS,build_rest
E=html.escape; V=str(int(time.time()))
ALL=dict(LABS); ALL.update(build_rest())
t=open('systems-lp1-functions.html').read()
css=t[t.index('<style>')+7:t.index('</style>')]
css+='''tr.star td{background:#FBE7EF!important}tr.star td:first-child{color:#c2185b}tr.star td:first-child:before{content:"★ ";color:#D94F7F}
.trap{background:#FBE7EF;border:2px solid #D94F7F;border-radius:14px;padding:10px 12px;margin:12px 0}.trap h2{margin:0 0 6px;font-size:17px;color:#b0306a}.trap li{margin:4px 0;font-size:14.5px;line-height:1.35}
.flag{background:#FFF1E3;border:2px dashed #E07B39;border-radius:14px;padding:10px 12px;margin:12px 0;font-size:14.5px}.flag b{color:#b85a1c}
.legend{font-size:13px;color:#8a6b99;margin:8px 0}.legend span{background:#FBE7EF;color:#c2185b;font-weight:800;border-radius:6px;padding:1px 6px}
.only{margin-left:6px}'''
js=t[t.index('<script>'):]
js=js.replace("document.getElementById('hide').onclick","document.getElementById('star').onclick=()=>{document.body.classList.toggle('staronly');document.getElementById('star').textContent=document.body.classList.contains('staronly')?'📋 Show all rows':'★ Starred only'};document.getElementById('hide').onclick",1)
css+='body.staronly tr:not(.star){display:none}'
pages=[]
for n,L in sorted(ALL.items()):
    rows=sum(len(r) for _,r in L['secs']); stars=sum(1 for _,r in L['secs'] for x in r if x[2])
    body=f'<body><div class="wrap"><a class="back" href="gross-anatomy-practical3.html?v={V}">← Back to Practical 3</a> <a class="back" href="gross-anatomy-lab{n}-images.html?v={V}">🖼️ Lab {n} hub</a>'
    body+=f'<div class="hero"><h1>🧠 {E(L["title"])} · Functions</h1><p>Say it, then tap the pink box · {rows} items · ★ {stars} professor-emphasized · {E(L["src"])}</p></div>'
    body+='<div class="bar"><script defer src="shuffle.js"></script><button id="hide">🙈 Hide all</button><button id="all">👀 Show all</button><button id="star">★ Starred only</button><span class="n" id="n"></span></div>'
    body+='<p class="legend"><span>★ pink row</span> = he stressed it in the pre-lab video or lecture.</p>'
    if L['traps']: body+='<div class="trap"><h2>⚠️ Precision traps</h2><ul>'+''.join(f'<li>{E(x)}</li>' for x in L['traps'])+'</ul></div>'
    for ft,fx in L['flags']: body+=f'<div class="flag"><b>{E(ft)}</b> · {E(fx)}</div>'
    body+='<div class="cols">'
    for i,(h,rs) in enumerate(L['secs']):
        body+=f'<div class="sec{" p" if i%2 else ""}"><h2>{E(h)}</h2><table>'+''.join(f'<tr class="{"star" if s else ""}"><td>{E(q)}</td><td><span class="ans">{E(a)}</span></td></tr>' for q,a,s in rs)+'</table></div>'
    body+='</div><div class="foot">🎀 Bethany · K-State CVM Class of 2030 · 🐾</div></div>'
    fn=f'gross-anatomy-lab{n}-functions.html'
    open(fn,'w').write(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Lab {n} Functions</title><style>{css}</style></head>'+body+js)
    pages.append((n,fn,L['title'],rows,stars))
    # hub link (inside the 🧠 terms section)
    hf=f'gross-anatomy-lab{n}-images.html'
    try:
        h=open(hf).read(); h=re.sub(r'<!--fn-->.*?<!--/fn-->','',h,flags=re.S)
        h=h.replace('<div class="sec terms"><h2>🧠 No-image terms</h2>',f'<div class="sec terms"><h2>🧠 No-image terms</h2><!--fn--><a href="{fn}?v={V}">🧠 Functions page · tap to reveal<span>{rows} items · ★{stars}</span></a><!--/fn-->',1)
        open(hf,'w').write(h)
    except FileNotFoundError: pass
p=open('gross-anatomy-practical3.html').read()
p=re.sub(r'<!--labfn-->.*?<!--/labfn-->','',p,flags=re.S)
grid='<!--labfn--><div style="margin:0 0 14px;padding:12px 14px;border-radius:18px;background:#fff;border:1px solid #eadff2"><div style="font-weight:900;color:#70428f;margin-bottom:6px">🧠 Functions by lab · ★ = he stressed it</div><div style="display:flex;flex-wrap:wrap;gap:6px">'+''.join(f'<a href="{fn}?v={V}" style="text-decoration:none;padding:8px 12px;border-radius:999px;background:#FBE7EF;color:#b0306a;font-weight:800;font-size:14px">Lab {"19+20" if n==19 else n} · ★{s}</a>' for n,fn,_,r,s in pages)+'</div></div><!--/labfn-->'
p=p.replace('<div class="grid">',grid+'<div class="grid">',1)
open('gross-anatomy-practical3.html','w').write(p)
for x in pages: print(x)
