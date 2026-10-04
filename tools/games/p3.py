"""Practical 3 games (Labs 16-18+). Run from repo root: python3 tools/games/p3.py"""
import json,sys,os,re,time,glob
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from common import *
V=str(int(time.time()))
BACK=f'gross-anatomy-practical3.html?v={V}'
# ---------- simulator blocks: every Practical 3 lab hub ----------
B=[]
for hub in sorted(glob.glob('gross-anatomy-lab*-images.html'),key=lambda f:int(re.search(r'lab(\d+)',f).group(1))):
    n=int(re.search(r'lab(\d+)',hub).group(1))
    if n<16: continue
    h=open(hub).read()
    for f,name in re.findall(r'<a href="(gross-anatomy-lab\d+-(?:main|extra|diag)\d+\.html)[^"]*">([^<]+)<span>',h):
        kind='⭐' if '-main' in f else ('📚' if '-extra' in f else '📖')
        B.append([n,f,f'{kind} {name}'])
sim=open('tools/games/prac.py').read()
body=re.search(r"body='''(.*?)'''",sim,re.S).group(1)
js=re.search(r"js=TABJS\+f'const B=\{json.dumps\(B\)\};'\+r'''(.*?)'''",sim,re.S).group(1)
js=js.replace("'pracMisses'","'pracMisses3'")
# answer extraction for Practical-3 cards (first stage = orient, names in ❓ stages)
js=js.replace("""let a=s.querySelector('.an');if(!im||!a)return;let ai=a.querySelector('img');let name=[...a.childNodes].filter(n=>!(n.nodeName==='IMG')).map(n=>n.textContent).join(' ').trim();let more=[...s.querySelectorAll('.stg')].slice(1).map(g=>'<div><b>'+g.querySelector('.pr').textContent+'</b> '+g.querySelector('.an').textContent+'</div>').join('');""",
"""let G=[...s.querySelectorAll('.stg')];if(!im||!G.length)return;let N=G.filter(g=>g.querySelector('.pr').textContent.includes('❓'));let name=N.length?N.map(g=>{let p=g.querySelector('.pr').textContent.match(/#\\d+/);return (p?p[0]+' ':'')+g.querySelector('.an').textContent.trim()}).join(' · '):(q?q.childNodes[0].textContent.trim():'');let ai=s.querySelector('.stg .an img');let more=G.filter(g=>!N.includes(g)&&!g.querySelector('img')&&!g.querySelector('.pr').textContent.includes('Orient')).map(g=>'<div><b>'+g.querySelector('.pr').textContent+'</b> '+g.querySelector('.an').textContent+'</div>').join('');""")
assert 'let G=' in js
js=TABJS+f'const B={json.dumps(B)};'+js
js=js.replace("if(b[2].startsWith('⭐'))c.classList.add('sel')","if(b[2].startsWith('⭐'))c.classList.add('sel')")
open('gross-anatomy-p3-games-practical.html','w').write(page('⏱️ Practical 3 simulator','Timed stations from your Lab 16+ decks · ⭐ bold blocks preselected',body,js,back=f'gross-anatomy-p3-games.html?v={V}'))
# ---------- order games ----------
SEQ={
'🩸 Arteries':[
 ('Aorta from the heart outward',['Ascending aorta (gives the coronary aa.)','Aortic arch','Brachiocephalic trunk','Left subclavian artery','Descending aorta']),
 ('Branches of the brachiocephalic trunk (dog)',['Left common carotid artery','Right common carotid artery','Right subclavian artery']),
 ('Branches of the subclavian artery',['Vertebral artery','Costocervical trunk','Superficial cervical artery','Internal thoracic artery','→ continues as the axillary artery']),
 ('Internal thoracic artery, down the ventral wall',['Internal thoracic artery','Ventral intercostal + perforating branches','Musculophrenic artery + cranial epigastric artery','Cranial superficial epigastric artery']),
 ('Left coronary artery → its branches',['Left coronary artery (left aortic sinus)','Paraconal interventricular branch + septal branch','Circumflex branch','Subsinuosal interventricular branch']),
 ('Dorsal intercostal arteries: origin by rib',['Intercostals 1–3: costocervical trunk','Intercostals 4–12: descending aorta','Right 5th intercostal → bronchoesophageal artery'])],
'🩵 Veins + lymph':[
 ('Neck veins → heart',['Maxillary v. + linguofacial v.','External jugular vein','+ subclavian v. → brachiocephalic vein','Cranial vena cava','Sinus venarum (right atrium)']),
 ('Lymph back to blood',['Cisterna chyli (abdomen)','Thoracic duct','Left venous angle / left brachiocephalic vein']),
 ('Heart\'s own venous return',['Great cardiac vein (paraconal groove)','Coronary groove','Coronary sinus','Right atrium']),
 ('Dorsal thoracic wall veins',['Dorsal intercostal veins','Right azygos vein','Cranial vena cava'])],
'❤️ Blood through the heart':[
 ('Systemic venous blood → lungs',['Cranial + caudal vena cava','Sinus venarum (intervenous tubercle diverts flow)','Right atrioventricular orifice + right AV valve','Right ventricle','Conus arteriosus','Pulmonary valve (3 semilunar cusps)','Pulmonary trunk']),
 ('Lungs → body',['Pulmonary veins','Left atrium','Left atrioventricular valve','Left ventricle','Aortic valve (3 semilunar cusps)','Ascending aorta']),
 ('Valve anchoring (cusp → wall)',['AV valve cusp','Chordae tendineae','Papillary muscle','Ventricular wall']),
 ('Pericardium + heart wall, outside → in',['Pericardial mediastinal pleura','Fibrous pericardium','Parietal serous pericardium','Pericardial cavity','Visceral serous pericardium (epicardium)','Myocardium','Endocardium'])],
'🫁 Airway + lungs':[
 ('Air down the bronchial tree',['Trachea','Carina (≈ T4–T5)','Principal bronchi','Lobar bronchi','Segmental bronchi']),
 ('Pleura, outside → lung',['Costal pleura (parietal)','Pleural cavity','Pulmonary (visceral) pleura','Lung'])],
'⚡ Autonomic nerves':[
 ('Sympathetic to a thoracic organ',['Preganglionic cell body (thoracolumbar cord)','Ventral root','Spinal nerve','Ramus communicans','Sympathetic trunk ganglion (synapse)','Postganglionic neuron → heart/lungs (cardiac nn.)']),
 ('Sympathetic to the head',['Sympathetic trunk','Cervicothoracic ganglion','Ansa subclavia (loops the subclavian a.)','Middle cervical ganglion','Vagosympathetic trunk','Cranial cervical ganglion → head']),
 ('Sympathetic to the abdomen',['Preganglionic axon passes THROUGH the trunk','Splanchnic nerve','Prevertebral (collateral) ganglion (synapse)','Postganglionic → abdominal viscera']),
 ('Vagus down the thorax',['Vagosympathetic trunk','Vagus nerve','Dorsal + ventral branches (dorsal to heart)','Dorsal + ventral vagal trunks on the esophagus','Esophageal hiatus']),
 ('Left recurrent laryngeal nerve',['Left vagus nerve','Loops caudal to the aortic arch (by the ligamentum arteriosum)','Runs cranially along the trachea','Caudal laryngeal nerve → larynx'])],
}
SORT=[
 ('Left lung or right lung?',['Left lung','Right lung'],[('Cranial lobe: cranial part',0),('Cranial lobe: caudal part',0),('Aortic impression',0),('Middle lobe',1),('Accessory lobe',1),('Cardiac notch',1),('Lobe most prone to torsion',1)]),
 ('Auricular (LEFT) or atrial (RIGHT) surface?',['Auricular (left)','Atrial (right)'],[('Paraconal interventricular groove',0),('Left auricle',0),('Conus arteriosus + pulmonary trunk',0),('Subsinuosal interventricular groove',1),('Coronary sinus opening',1),('Caudal vena cava',1)]),
 ('Sympathetic or parasympathetic?',['Sympathetic','Parasympathetic'],[('Thoracolumbar',0),('Craniosacral',1),('Cervicothoracic ganglion',0),('Vagus nerve',1),('Splanchnic nerves',0),('Ansa subclavia',0),('Recurrent laryngeal nerve',1),('Sympathetic trunk ganglion',0)]),
 ('Ganglion or nucleus?',['Ganglion (outside CNS)','Nucleus (inside CNS)'],[('Cervicothoracic',0),('Cell bodies of CN X in the brainstem',1),('Dorsal root (spinal) ganglion',0),('Preganglionic sympathetic cell bodies in the cord',1),('Middle cervical',0),('Celiac (prevertebral)',0)]),
 ('Afferent or efferent?',['Afferent (sensory, TO CNS)','Efferent (motor, FROM CNS)'],[('Dorsal root',0),('Ventral root',1),('Somatic efferent neuron',1),('Postganglionic sympathetic axon',1),('Baroreceptor fibers in cardiac nn.',0)]),
 ('Branch of the brachiocephalic trunk or the subclavian a.?',['Brachiocephalic trunk','Subclavian a.'],[('Left common carotid a.',0),('Right common carotid a.',0),('Vertebral a.',1),('Costocervical trunk',1),('Superficial cervical a.',1),('Internal thoracic a.',1),('Right subclavian a.',0)]),
]
body2='<div class="tabs">'+''.join(f'<button class="{"on" if i==0 else ""}" data-t="t{i}">{k}</button>' for i,k in enumerate(list(SEQ)+['🗂️ Sort it']))+'</div>'
for i,k in enumerate(SEQ):
    body2+=f'<div id="t{i}" class="panel{" on" if i==0 else ""}"><h2>{k}</h2><p class="hint">Tap in order. Say each one out loud as you tap it.</p><div class="seqs" data-k="{k}"></div></div>'
body2+=f'<div id="t{len(SEQ)}" class="panel"><h2>🗂️ Sort it</h2><p class="hint">Which bin? Wrong taps are saved to the bottom list.</p><div id="sort"></div></div>'
js2=TABJS+f'const SEQ={json.dumps(SEQ)};const SORT={json.dumps(SORT)};'+r'''
tabs();
document.querySelectorAll('.seqs').forEach(box=>{let L=SEQ[box.dataset.k];let i=0;
function run(){let [title,items]=L[i];let nxt=0,err=0;box.innerHTML='';box.appendChild(el('div','q',`${i+1}/${L.length} · ${title}`));let g=el('div','grid');g.style.gridTemplateColumns='1fr';box.appendChild(g);let fb=el('div','fb');box.appendChild(fb);
sh(items.map((t,k)=>[t,k])).forEach(([t,k])=>{let c=el('button','chip',t);c.onclick=()=>{if(c.classList.contains('ok'))return;if(k===nxt){c.classList.add('ok');c.textContent=(nxt+1)+'. '+t;nxt++;if(nxt===items.length){fb.className='fb show';fb.innerHTML=(err?`✅ Done · ${err} wrong tap${err>1?'s':''}`:'🎉 Perfect!')+'<br><b>Order:</b> '+items.join(' → ')+'<div class="row"><button class="btn hot">Next ▶</button><button class="btn">↺ Redo</button></div>';let bs=fb.querySelectorAll('button');bs[0].onclick=()=>{i=(i+1)%L.length;run()};bs[1].onclick=run}}else{err++;c.classList.add('shake','bad');setTimeout(()=>c.classList.remove('shake','bad'),400)}};g.appendChild(c)})}
run()});
(function(){const S=$('#sort');let si=0,miss=[];function run(){let [q,bins,items]=SORT[si];let qs=sh(items),k=0,right=0;S.innerHTML='';S.appendChild(el('div','q',`${si+1}/${SORT.length} · ${q}`));let it=el('div','q');it.style.cssText='background:#f4ebfb;border-radius:14px;padding:14px;text-align:center';S.appendChild(it);let row=el('div','row');bins.forEach((b,bi)=>{let x=el('button','btn',b);x.style.flex='1';x.onclick=()=>{let [t,a]=qs[k];if(bi===a){right++;fb.className='fb show';fb.textContent='✅ '+t+' → '+bins[a]}else{miss.push(t+' → '+bins[a]);fb.className='fb show';fb.textContent='❌ '+t+' → '+bins[a]}k++;show()};row.appendChild(x)});S.appendChild(row);let fb=el('div','fb');S.appendChild(fb);let ml=el('div','fb');S.appendChild(ml);
function show(){if(k>=qs.length){it.textContent=`Done: ${right}/${qs.length}`;row.innerHTML='';let n=el('button','btn hot','Next set ▶');n.onclick=()=>{si=(si+1)%SORT.length;run()};row.appendChild(n)}else it.textContent=qs[k][0];if(miss.length){ml.className='fb show';ml.innerHTML='<b>Review:</b><br>'+miss.map(m=>'• '+m).join('<br>')}}show()}run()})();
'''
open('gross-anatomy-p3-games-order.html','w').write(page('🧩 Order + sort games','Branching order, blood flow, autonomic pathways, left vs right',body2,js2,back=f'gross-anatomy-p3-games.html?v={V}'))
hub=f'''<div class="panel on" style="margin-top:12px"><h2>Which one should I use?</h2><div class="grid" style="grid-template-columns:1fr">
<a class="chip" style="text-decoration:none" href="gross-anatomy-p3-games-practical.html?v={V}">⏱️ <b>Practical simulator + 🔁 Misses mode</b><br><small>Daily. Timed stations from your Lab 16+ decks (course slides, extras, diagrams). Misses come back until you get them twice in a row.</small></a>
<a class="chip" style="text-decoration:none" href="gross-anatomy-p3-games-order.html?v={V}">🧩 <b>Order + sort games</b><br><small>Arterial branching order, veins + lymph, blood through the heart, pericardium layers, bronchial tree, autonomic pathways · 🗂️ left vs right lung, auricular vs atrial surface, sympathetic vs parasympathetic.</small></a>
<a class="chip" style="text-decoration:none" href="gross-anatomy-games-thorax.html?v={V}">🫁 <b>Thorax games</b> (from Exam 2)<br><small>Space vs structure + layer stacker for pleura/mediastinum/pericardium; needle game.</small></a></div></div>'''
open('gross-anatomy-p3-games.html','w').write(page('🎮 Practical 3 games','Gross Anatomy I · Practical 3 · Oct 29',hub,'',back=BACK))
# link from the Practical 3 page
p=open('gross-anatomy-practical3.html').read()
p=re.sub(r'<a href="gross-anatomy-p3-games\.html[^"]*"[^>]*>.*?</a>','',p,flags=re.S)
btn=f'<a href="gross-anatomy-p3-games.html?v={V}" style="display:block;margin:12px 0 0;padding:14px 16px;border-radius:18px;text-decoration:none;font-weight:900;color:#fff;background:linear-gradient(120deg,#6a3392,#e05fa8)">🎮 Study games · simulator, order + sort games</a>'
p=p.replace('</div><div class="grid">',f'</div>{btn}<div class="grid">',1)
open('gross-anatomy-practical3.html','w').write(p)
print(len(B),'sim blocks')
