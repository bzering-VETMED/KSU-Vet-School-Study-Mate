"""Practical 3 · 🧵 Trace It: drawn branching maps that GROW one branch per tap (made by Claude).
Data: tools/p3trace_data.py. Run from repo root: python3 tools/p3trace.py
Writes gross-anatomy-p3-trace.html (hub) + gross-anatomy-p3-trace-labN.html, links the hub from Practical 3."""
import sys,re,json,time,html
sys.path.insert(0,'tools'); from p3trace_data import LABS
E=html.escape; V=str(int(time.time()))
def js_tree(n): return {'n':n[0],'k':n[1],'t':n[2],'c':[js_tree(c) for c in n[3]]}
CSS='''*{box-sizing:border-box}:root{--bg:#fffafd;--ink:#34213f;--soft:#8a6b99;--pill:#f3eafb;--pillt:#65328c;--card:#fff;--line:#eadff2}
body{margin:0;background:var(--bg);color:var(--ink);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif;padding-bottom:env(safe-area-inset-bottom,0px)}
.wrap{max-width:900px;margin:auto;padding:14px max(14px,env(safe-area-inset-left,0px))}
.back{display:inline-block;margin:0 0 10px;padding:8px 14px;border-radius:999px;background:var(--pill);color:var(--pillt);font-weight:800;text-decoration:none}
.hero{color:#fff;background:linear-gradient(135deg,#5d347e,#8855b8 55%,#df78ad);padding:18px 20px;border-radius:22px}.hero h1{margin:0;font-size:24px}.hero p{margin:6px 0 0;opacity:.95;font-size:14px}
.bar{position:sticky;top:env(safe-area-inset-top,0px);z-index:5;display:flex;flex-wrap:wrap;gap:6px;align-items:center;background:#fffafdee;padding:10px 0;backdrop-filter:blur(6px)}
.bar button{border:0;border-radius:999px;padding:10px 13px;font-weight:800;font-size:14px;background:var(--pill);color:var(--pillt);cursor:pointer}
.bar button.hot{background:linear-gradient(120deg,#7b42a0,#e05fa8);color:#fff}.bar button[hidden]{display:none}
.count{margin-left:auto;font-weight:800;color:var(--soft);font-size:14px}
.map{background:var(--card);border:1px solid var(--line);border-radius:20px;padding:14px;box-shadow:0 5px 16px rgba(91,44,124,.06)}
.map h2{margin:0;color:#5d347e;font-size:20px}.map .sub{margin:4px 0 8px;color:var(--soft);font-size:14px}
.key{display:flex;flex-wrap:wrap;gap:10px;font-size:12px;font-weight:700;color:var(--soft);margin-bottom:6px}.key i{display:inline-block;width:18px;height:4px;border-radius:2px;vertical-align:middle;margin-right:4px}
.tree{position:relative;overflow-x:auto;-webkit-overflow-scrolling:touch;cursor:pointer}
.tree svg{position:absolute;left:0;top:0;overflow:visible}
.node{position:absolute;display:flex;flex-direction:column;gap:1px;max-width:min(340px,calc(100vw - 80px))}
.lab{display:inline-block;align-self:flex-start;font-weight:800;font-size:15px;line-height:1.2;padding:4px 10px;border-radius:12px;background:#fff;border:2px solid;white-space:normal}
.lab.q{background:linear-gradient(135deg,#C9B6E4,#F2B6D6);border-color:transparent;color:#fff;min-width:64px;text-align:center}
.lab.new{box-shadow:0 0 0 4px rgba(224,95,168,.25)}
.note{font-size:12.5px;color:var(--soft);font-weight:600;padding-left:4px;line-height:1.25}
.node.hid{display:none}
.done{margin-top:10px;font-weight:800;color:#2f9e76;text-align:center}
.mode{font-size:13px;color:var(--soft);margin:6px 0 0}
@media(prefers-reduced-motion:no-preference){.grow{animation:dash .45s ease-out forwards}@keyframes dash{to{stroke-dashoffset:0}}.node.in{animation:fade .3s ease-out}@keyframes fade{from{opacity:0;transform:translateX(-6px)}to{opacity:1}}}
.list a{display:flex;justify-content:space-between;align-items:center;text-decoration:none;margin:7px 0;padding:12px 14px;border-radius:14px;background:#f7eefb;color:#70428f;font-weight:800}.list a span{font-size:13px;background:#fff;border-radius:999px;padding:3px 10px;color:#b0679a}
.sec{margin-top:16px;background:#fff;border:1px solid var(--line);border-radius:18px;padding:14px}.sec h2{margin:0 0 4px;color:#70428f;font-size:19px}.sec p{margin:0 0 8px;color:var(--soft);font-size:14px}
.foot{text-align:center;font-size:12px;color:var(--soft);margin-top:20px}'''
JS=r'''
const COL={a:'#d6455d',v:'#3f6fd8',n:'#c99700',l:'#2f9e76',s:'#7b42a0',d:'#1f9aa8',f:'#e05fa8'};
const NAME={a:'artery',v:'vein (arrow = flow)',n:'nerve',l:'lymph',s:'structure',d:'duct',f:'route step'};
const ROW=60,IND=30,X0=14,Y0=22;
let mi=0,mode='grow';const S=MAPS.map(()=>({k:0,named:new Set([0])}));
function flat(t){const out=[];(function walk(n,d,p){const i=out.length;out.push({n:n.n,k:n.k,t:n.t,d,p});n.c.forEach(c=>walk(c,d+1,i))})(t,0,-1);return out}
const F=MAPS.map(m=>flat(m.tree));
function steps(i){return (F[i].length-1)*2}       // each branch: appear (?) then name
function stateOf(i,j){const s=S[i];if(j===0)return 'named';if(mode==='quiz')return s.named.has(j)?'named':'q';
  const k=s.k,a=(j-1)*2+1;if(k<a)return 'hid';if(k===a)return 'q';return 'named'}
function render(){
  const m=MAPS[mi],f=F[mi],box=document.getElementById('tree'),svg=document.getElementById('svg');
  document.getElementById('title').textContent=m.title;document.getElementById('sub').textContent=m.sub||'';
  const kinds=[...new Set(f.map(x=>x.k))];document.getElementById('key').innerHTML=kinds.map(k=>`<span><i style="background:${COL[k]}"></i>${NAME[k]}</span>`).join('');
  box.querySelectorAll('.node').forEach(e=>e.remove());svg.innerHTML='<defs>'+Object.entries(COL).map(([k,c])=>`<marker id="ar${k}" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="${c}"/></marker>`).join('')+'</defs>';
  let maxX=0,shown=0,last=-1;
  f.forEach((x,j)=>{const st=stateOf(mi,j);const y=Y0+j*ROW,xx=X0+x.d*IND;
    if(st==='hid')return; shown++;
    if(x.p>=0){const p=f[x.p],px=X0+p.d*IND,py=Y0+x.p*ROW;const c=COL[x.k];
      const d=`M${px} ${py+8} V${y-12} Q${px} ${y} ${px+12} ${y} H${xx-6}`;
      const path=document.createElementNS('http://www.w3.org/2000/svg','path');path.setAttribute('d',d);path.setAttribute('fill','none');path.setAttribute('stroke',c);path.setAttribute('stroke-width','3.5');path.setAttribute('stroke-linecap','round');
      if(x.k==='v')path.setAttribute('marker-start',`url(#ar${x.k})`);else path.setAttribute('marker-end',`url(#ar${x.k})`);
      const isNew=mode==='grow'&&S[mi].k===(j-1)*2+1;
      if(isNew){path.setAttribute('class','grow');svg.appendChild(path);const L=path.getTotalLength();path.style.strokeDasharray=L;path.style.strokeDashoffset=L}else svg.appendChild(path)}
    const dot=document.createElementNS('http://www.w3.org/2000/svg','circle');dot.setAttribute('cx',xx);dot.setAttribute('cy',y);dot.setAttribute('r',x.p<0?7:5.5);dot.setAttribute('fill',COL[x.k]);svg.appendChild(dot);
    const el=document.createElement('div');el.className='node';el.style.left=(xx+12)+'px';el.style.top=(y-14)+'px';
    const lab=document.createElement('span');lab.className='lab'+(st==='q'?' q':'');lab.style.borderColor=COL[x.k];lab.style.color=st==='q'?'#fff':COL[x.k];
    lab.textContent=st==='q'?'?':x.n;if(mode==='grow'&&S[mi].k===(j-1)*2+2)lab.classList.add('new');
    if(mode==='quiz'&&j>0)lab.onclick=e=>{e.stopPropagation();S[mi].named.has(j)?S[mi].named.delete(j):S[mi].named.add(j);render()};
    el.appendChild(lab);if(st==='named'&&x.t){const nt=document.createElement('span');nt.className='note';nt.textContent=x.t;el.appendChild(nt)}
    if(mode==='grow'&&S[mi].k===(j-1)*2+1)el.classList.add('in');
    box.appendChild(el);maxX=Math.max(maxX,xx);last=j});
  const H=Y0+(mode==='grow'?Math.max(last,0):f.length-1)*ROW+46;box.style.height=H+'px';svg.setAttribute('width',maxX+40);svg.setAttribute('height',H);
  const tot=steps(mi),k=S[mi].k,nn=mode==='quiz'?S[mi].named.size-1:Math.floor(k/2);
  document.getElementById('count').textContent=`Map ${mi+1}/${MAPS.length} · ${nn}/${f.length-1} named`;
  document.getElementById('next').textContent=mode==='quiz'?'Next map ▶':(k<tot?(k%2===0?'Grow next branch 🌱':'Name it ✨'):(mi<MAPS.length-1?'Next map ▶':'🎉 Done'));
  document.getElementById('done').hidden=!(mode==='grow'&&k>=tot);
  document.getElementById('pm').hidden=mi===0;document.getElementById('nm').hidden=mi===MAPS.length-1;
  document.getElementById('back').hidden=mode==='quiz'||k===0;
  if(mode==='grow'&&last>0){const el=box.querySelectorAll('.node');const lastEl=el[el.length-1];const r=lastEl.getBoundingClientRect();if(r.bottom>innerHeight-20)scrollBy({top:r.bottom-innerHeight+80,behavior:'smooth'})}}
function next(){if(mode==='quiz'){if(mi<MAPS.length-1){mi++;render();scrollTo(0,0)}return}
  if(S[mi].k<steps(mi)){S[mi].k++;render()}else if(mi<MAPS.length-1){mi++;render();scrollTo(0,0)}}
function back(){if(S[mi].k>0){S[mi].k--;render()}}
document.getElementById('next').onclick=next;document.getElementById('back').onclick=back;
document.getElementById('tree').onclick=()=>{if(mode==='grow')next()};
document.getElementById('all').onclick=()=>{S[mi].k=steps(mi);F[mi].forEach((_,j)=>S[mi].named.add(j));render()};
document.getElementById('reset').onclick=()=>{S[mi].k=0;S[mi].named=new Set([0]);render();scrollTo(0,0)};
document.getElementById('pm').onclick=()=>{if(mi>0){mi--;render();scrollTo(0,0)}};
document.getElementById('nm').onclick=()=>{if(mi<MAPS.length-1){mi++;render();scrollTo(0,0)}};
const MB=document.getElementById('mode');MB.onclick=()=>{mode=mode==='grow'?'quiz':'grow';MB.textContent=mode==='grow'?'❓ Quiz mode':'🌱 Grow mode';
  document.getElementById('modetxt').textContent=mode==='grow'?'🌱 Grow: tap anywhere on the map. A branch appears as “?” → say it → tap to name it.':'❓ Quiz: whole tree drawn, names hidden. Tap any pink box to check it.';render()};
document.addEventListener('keydown',e=>{if(['ArrowRight','Enter',' ','PageDown'].includes(e.key)){e.preventDefault();next()}else if(['ArrowLeft','PageUp'].includes(e.key)){e.preventDefault();back()}});
render();'''
def page(n,title,maps):
    data=[{'title':t,'sub':s,'tree':js_tree(tr)} for t,s,tr in maps]
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><title>{E(title)} · Trace It</title><style>{CSS}</style></head><body><div class="wrap">
<a class="back" href="gross-anatomy-p3-trace.html?v={V}">← Back to Trace It</a>
<div class="hero"><h1>🧵 {E(title)}</h1><p>{len(maps)} branching maps · say each branch before you tap</p></div>
<div class="bar"><button id="pm">⏮ Prev map</button><button id="back">◀ Back</button><button class="hot" id="next">Grow next branch 🌱</button><button id="nm">⏭ Next map</button><button id="all">👀 Show all</button><button id="reset">↺ Reset</button><button id="mode">❓ Quiz mode</button><span class="count" id="count"></span></div>
<div class="map"><h2 id="title"></h2><p class="sub" id="sub"></p><div class="key" id="key"></div><div class="tree" id="tree"><svg id="svg"></svg></div><div class="done" id="done" hidden>🎉 Map complete · ⏭ Next map, or ❓ Quiz mode to test it cold</div><p class="mode" id="modetxt">🌱 Grow: tap anywhere on the map. A branch appears as “?” → say it → tap to name it.</p></div>
<div class="foot">🎀 Bethany · K-State CVM Class of 2030 · 🐾 · from your bold lists + slide notes; “(not bold)” = connector only</div>
</div><script>const MAPS={json.dumps(data,ensure_ascii=False)};{JS}</script></body></html>'''
links=[]
for n,(title,maps) in LABS.items():
    fn=f'gross-anatomy-p3-trace-lab{n}.html'; open(fn,'w').write(page(n,title,maps))
    links.append(f'<a href="{fn}?v={V}">{E(title)}<span>{len(maps)} maps</span></a>')
IMG=[('gross-anatomy-lc19-arteries.html','❤️ Thoracic limb arteries (Labs 19–20)'),('gross-anatomy-lc19-veins.html','🩸 Thoracic limb veins (Labs 19–20)'),('gross-anatomy-lc19-nerves.html','⚡ Thoracic limb nerves (Labs 19–20)'),('gross-anatomy-l18-routes.html','⚡ ANS routes (Labs 18 + 23)'),('gross-anatomy-abd2-blood.html','🩸 Abdominal blood supply + drainage (Lab 23)'),('gross-anatomy-abd1-trace.html','🌀 Flow of ingesta + pancreas (Lab 22)')]
IMG=[x for x in IMG if __import__('os').path.exists(x[0])]+[('gross-anatomy-p3-trace-img.html','📚 Abdomen slides: nerves + arteries (Labs 22–23)')] if __import__('os').path.exists('gross-anatomy-p3-trace-img.html') else [x for x in IMG if __import__('os').path.exists(x[0])]
hub=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><title>Practical 3 Trace It</title><style>{CSS}</style></head><body><div class="wrap">
<a class="back" href="gross-anatomy-practical3.html?v={V}">← Back to Practical 3</a>
<div class="hero"><h1>🧵 Practical 3 · Trace It</h1><p>Watch the branches grow. Say each name before you tap.</p></div>
<div class="sec"><h2>🌳 Branching maps (every lab)</h2><p>Arteries red · veins blue (arrows = flow) · nerves gold · lymph green. 🌱 Grow mode adds one branch per tap; ❓ Quiz mode hides every name.</p><div class="list">{"".join(links)}</div></div>
<div class="sec"><h2>🖼️ Trace on real images</h2><p>Course slides with names erased; names pop back up in order along the route.</p><div class="list">{"".join(f'<a href="{f}?v={V}">{E(t)}<span>slides</span></a>' for f,t in IMG)}</div></div>
<div class="foot">🎀 Bethany · K-State CVM Class of 2030 · 🐾</div></div></body></html>'''
open('gross-anatomy-p3-trace.html','w').write(hub)
p=open('gross-anatomy-practical3.html').read()
btn=f'<a style="display:block;margin:0 0 14px;padding:14px 16px;border-radius:18px;text-decoration:none;font-weight:900;color:#fff;background:linear-gradient(120deg,#3f6fd8,#d6455d)" href="gross-anatomy-p3-trace.html?v={V}">🧵 Trace It · branching maps for vessels + nerves</a>'
if 'p3-trace.html' in p: p=re.sub(r'<a [^>]*href="gross-anatomy-p3-trace\.html[^"]*">[^<]*</a>',btn,p,count=1)
else: p=p.replace('<div class="grid">',btn+'<div class="grid">',1)
open('gross-anatomy-practical3.html','w').write(p)
print('maps:',sum(len(m) for _,m in LABS.values()),'image decks:',len(IMG))
