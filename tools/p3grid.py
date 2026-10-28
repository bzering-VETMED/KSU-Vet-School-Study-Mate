"""Practical 3 · "▦ All cards" overview grid on deck pages (made by Claude, Bethany Oct 27).
Opening a deck shows every card as a small numbered thumbnail; tap one to start there and go in order.
"▦ All cards" in the toolbar reopens the grid. Idempotent (<!--grid--> marker).
  python3 tools/p3grid.py <deck.html> …     (p3one.py calls it for the ⭐ decks)"""
import sys,re
CSS='''<style id="gridcss">#gridov{position:fixed;inset:0;z-index:50;background:#fff9fd;overflow:auto;padding:max(12px,env(safe-area-inset-top)) max(12px,env(safe-area-inset-right)) 24px max(12px,env(safe-area-inset-left))}#gridov[hidden]{display:none}#gridov h2{margin:4px 0 10px;color:#70428f;font-size:20px}#gridov .gtop{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin-bottom:10px}#gridov .gtop button{border:0;border-radius:999px;padding:9px 14px;background:#7b42a0;color:#fff;font-weight:800;font-size:15px}#gridov .gtop a{color:#70428f;font-weight:800;text-decoration:none;background:#f3eafb;border-radius:999px;padding:9px 14px}#gridov .gg{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:10px}#gridov .gi{position:relative;border:2px solid #eadff2;border-radius:14px;background:#fff;padding:0;overflow:hidden;cursor:pointer;text-align:left}#gridov .gi img{width:100%;height:120px;object-fit:cover;display:block;background:#f3eafb}#gridov .gi span{position:absolute;top:6px;left:6px;background:#e05fa8;color:#fff;font-weight:900;border-radius:999px;min-width:26px;height:26px;display:flex;align-items:center;justify-content:center;font-size:14px;padding:0 6px}#gridov .gi small{display:block;padding:6px 8px;font-size:12px;color:#5d347e;line-height:1.25;max-height:3.8em;overflow:hidden}#gridov .gi.got{border-color:#4fbf95}#gridov .gi.miss{border-color:#e05f5f}</style>'''
JS='''<script id="gridjs">(function(){const cs=[...document.querySelectorAll('section.card')];if(!cs.length)return;
const ov=document.createElement('div');ov.id='gridov';const back=document.querySelector('a.back');
ov.innerHTML='<div class="gtop"><h2 style="flex:1 1 100%">▦ All cards · '+cs.length+' · tap one to start there</h2><button id="gstart">▶ Start at card 1</button>'+(back?'<a href="'+back.getAttribute('href')+'">← Back</a>':'')+'</div><div class="gg"></div>';
const gg=ov.querySelector('.gg');
cs.forEach((c,i)=>{const im=c.querySelector('.pic img');const q=(c.querySelector('.q')?.childNodes[0]?.textContent||'').trim();const b=document.createElement('button');b.className='gi';
b.innerHTML=(im?'<img loading="lazy" src="'+im.getAttribute('src')+'">':'<img alt="">')+'<span>'+(i+1)+'</span><small></small>';b.querySelector('small').textContent=q;
b.onclick=()=>{try{ord=cs.map((_,k)=>k);p=i;show()}catch(e){}ov.hidden=true;scrollTo(0,0)};gg.appendChild(b)});
document.body.appendChild(ov);
ov.querySelector('#gstart').onclick=()=>{try{ord=cs.map((_,k)=>k);p=0;show()}catch(e){}ov.hidden=true};
const bar=document.querySelector('.bar');if(bar){const gb=document.createElement('button');gb.textContent='▦ All cards';gb.onclick=()=>{cs.forEach((c,i)=>{const t=gg.children[i];t.classList.toggle('got',c.classList.contains('got'));t.classList.toggle('miss',c.classList.contains('miss'))});ov.hidden=false;ov.scrollTop=0};bar.insertBefore(gb,bar.firstChild)}
})();</script>'''
for f in sys.argv[1:]:
    h=open(f).read()
    h=re.sub(r'<!--grid-->.*?<!--/grid-->','',h,flags=re.S)
    if 'section class="card' not in h: continue
    h=h.replace('</body>','<!--grid-->'+CSS+JS+'<!--/grid--></body>',1)
    open(f,'w').write(h)
