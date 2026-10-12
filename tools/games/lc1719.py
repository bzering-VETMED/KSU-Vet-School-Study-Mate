# Lecture games for Gross Anatomy L17–19 (made by Claude). Run from repo root: python3 tools/games/lc1719.py
import os, sys, json, time; sys.path.insert(0, os.path.dirname(__file__)); import common
V = str(int(time.time()))
NERVES = ["Suprascapular","Subscapular","Musculocutaneous","Axillary","Thoracodorsal","Radial","Median","Ulnar","Cranial pectoral","Caudal pectoral","Lateral thoracic"]
MUSCLE = [  # (muscle, nerve) from slide 25 + 10/11 recording
 ("Supraspinatus","Suprascapular"),("Infraspinatus","Suprascapular"),("Subscapularis","Subscapular"),
 ("Biceps brachii","Musculocutaneous"),("Brachialis","Musculocutaneous"),("Coracobrachialis","Musculocutaneous"),
 ("Deltoideus","Axillary"),("Teres major","Axillary"),("Teres minor","Axillary"),("Latissimus dorsi","Thoracodorsal"),
 ("Triceps brachii","Radial"),("Extensor carpi radialis","Radial"),("Ulnaris lateralis","Radial"),
 ("Common digital extensor","Radial"),("Lateral digital extensor","Radial"),
 ("Flexor carpi radialis","Median"),("Superficial digital flexor","Median"),("Flexor carpi ulnaris","Ulnar"),
 ("Superficial pectorals","Cranial pectoral"),("Deep pectorals","Caudal pectoral"),("Cutaneous trunci","Lateral thoracic"),
]
DIV = [  # (effect, division) from L18 slide 18–19
 ("Pupil dilation","Sympathetic"),("Pupil constriction","Parasympathetic"),("Increased heart rate","Sympathetic"),
 ("Decreased heart rate","Parasympathetic"),("Decreased intestinal motility","Sympathetic"),("Increased intestinal motility","Parasympathetic"),
 ("Ejaculation","Sympathetic"),("Erection","Parasympathetic"),("Concentrated, viscous saliva","Sympathetic"),
 ("Abundant, watery saliva","Parasympathetic"),("Dilation of bronchioles","Sympathetic"),("Constriction of bronchioles","Parasympathetic"),
 ("Secretion of sweat glands","Sympathetic"),("Renin secretion","Sympathetic"),("Dilation of muscle vessels","Sympathetic"),
 ("Constriction of skin vessels","Sympathetic"),("Contraction of piloerector muscles","Sympathetic"),
 ("Thoracolumbar origin","Sympathetic"),("Craniosacral origin","Parasympathetic"),("Short pre, long post","Sympathetic"),
 ("Long pre, short post","Parasympathetic"),("Terminal ganglia","Parasympathetic"),("Uses rami communicantes","Sympathetic"),
 ("Cranial nerves III, VII, IX, X","Parasympathetic"),("Pelvic nerve","Parasympathetic"),("Hypogastric nerve","Sympathetic"),
 ("Splanchnic nerves","Sympathetic"),("Ganglia visible in lab","Sympathetic"),("Acetylcholine at both synapses","Parasympathetic"),
 ("Norepinephrine at the target","Sympathetic"),
]
TYPES = ["GSA","GSE","GVA","GVE","SSA","SVA","SVE"]
FUNC = [  # (scenario, type) from L17 slides + 10/5 recording
 ("You pinch the skin of the paw","GSA"),("Pain from a hot surface on the foot","GSA"),("Touch on the flank skin","GSA"),
 ("Motor signal to the biceps brachii","GSE"),("Motor signal to the triceps","GSE"),("Contracting the latissimus dorsi","GSE"),
 ("Feeling of a full stomach","GVA"),("Stretch of a distended colon","GVA"),("Sensation from a full bladder","GVA"),
 ("Slowing the heart rate","GVE"),("Contracting bladder smooth muscle","GVE"),("Saliva secretion from a gland","GVE"),("Pupil constriction","GVE"),
 ("Seeing a ball thrown","SSA"),("Hearing the owner's voice","SSA"),
 ("Tasting food","SVA"),("Smelling a treat","SVA"),
 ("Chewing (muscles of mastication)","SVE"),("Facial expression muscles","SVE"),("Pharyngeal muscles for swallowing","SVE"),("Laryngeal muscles","SVE"),
]
EXPLAIN = {"GSA":"General somatic afferent: sensory from the body wall/skin","GSE":"General somatic efferent: motor to skeletal muscle, 1 neuron",
 "GVA":"General visceral afferent: sensory from organs","GVE":"General visceral efferent: smooth, cardiac, glands; 2 neurons (ANS)",
 "SSA":"Special somatic afferent: vision, hearing","SVA":"Special visceral afferent: taste, smell","SVE":"Special visceral efferent: pharyngeal arch muscles"}
DATA = dict(muscle=dict(items=MUSCLE, opts=NERVES, q="Which nerve supplies…", sfx=" nerve"),
            div=dict(items=DIV, opts=["Sympathetic","Parasympathetic"], q="Sympathetic or parasympathetic?", sfx=""),
            func=dict(items=FUNC, opts=TYPES, q="Which functional type?", sfx="", explain=EXPLAIN))
body = '''<div class="tabs"><button class="on" data-t="muscle">💪 Nerve → muscle</button><button data-t="div">⚖️ Sympathetic or para?</button><button data-t="func">🧬 Functional type</button></div>''' + "".join(f'''
<div class="panel{' on' if k=='muscle' else ''}" id="{k}"><h2>{t}</h2><p class="hint">{h}</p>
<div class="q" id="{k}-q"></div><div class="grid" id="{k}-o"></div><div class="fb" id="{k}-fb"></div>
<div class="row"><button class="btn hot" id="{k}-next">Next ▶</button><button class="btn" id="{k}-miss">🔁 Misses only</button><button class="btn" id="{k}-clear">🧹 Clear</button><span class="score" id="{k}-s"></span></div></div>''' for k,t,h in [
 ("muscle","💪 Which nerve supplies it?","Lecture 19 · he said nerve functions are tested. Radial = extensors, median = flexors."),
 ("div","⚖️ Sympathetic or parasympathetic?","Lecture 18 · the effects table he expects you to know, plus anatomy features."),
 ("func","🧬 Which functional type?","Lecture 17 · the 7-type figure is worth 6–8 exam points.")])
js = common.TABJS + "const D=" + json.dumps(DATA) + r''';
function store(k){try{return JSON.parse(localStorage.getItem('lc1719-'+k)||'{}')}catch(e){return {}}}
function save(k,v){try{localStorage.setItem('lc1719-'+k,JSON.stringify(v))}catch(e){}}
function game(k){const g=D[k];let miss=store(k),only=false,deck=[],cur=null,ok=0,n=0,done=false;
 function build(){deck=sh(g.items.filter(it=>!only||miss[it[0]]));if(!deck.length){$('#'+k+'-q').textContent='No misses left. 🎉';$('#'+k+'-o').innerHTML='';return false}return true}
 function next(){if(!deck.length&&!build())return;cur=deck.pop();done=false;$('#'+k+'-q').textContent=(g.q.endsWith('…')?g.q.slice(0,-1)+' ':'')+cur[0]+(g.q.endsWith('…')?'?':'');
  const o=$('#'+k+'-o');o.innerHTML='';const fb=$('#'+k+'-fb');fb.classList.remove('show');
  g.opts.forEach(x=>{const b=el('button','chip',x+(g.sfx||''));b.onclick=()=>pick(b,x);o.appendChild(b)});score()}
 function pick(b,x){if(done)return;done=true;n++;const right=x===cur[1];if(right){ok++;b.classList.add('ok');if(miss[cur[0]]){miss[cur[0]]--;if(miss[cur[0]]<=0)delete miss[cur[0]]}}
  else{b.classList.add('bad','shake');miss[cur[0]]=2;[...$('#'+k+'-o').children].forEach(c=>{if(c.textContent===cur[1]+(g.sfx||''))c.classList.add('ok')})}
  save(k,miss);const fb=$('#'+k+'-fb');fb.innerHTML=(right?'✅ ':'❌ ')+'<b>'+cur[1]+(g.sfx||'')+'</b>'+(g.explain?' · '+g.explain[cur[1]]:'');fb.classList.add('show');score()}
 function score(){$('#'+k+'-s').textContent=ok+'/'+n+' · misses: '+Object.keys(miss).length}
 $('#'+k+'-next').onclick=next;$('#'+k+'-miss').onclick=e=>{only=!only;e.target.classList.toggle('hot',only);deck=[];next()};
 $('#'+k+'-clear').onclick=()=>{miss={};save(k,miss);deck=[];next()};build();next()}
tabs();['muscle','div','func'].forEach(game);document.addEventListener('keydown',e=>{if(e.key==='Enter'){const p=document.querySelector('.panel.on');if(p)p.querySelector('.btn.hot').click()}});'''
open('gross-anatomy-lc17-19-games.html','w').write(common.page('🎮 L17–19 Games','Lecture games · nerve functions, sympathetic vs. parasympathetic, functional types · 🔁 misses come back until you get them right twice',body,js,back=f'gross-anatomy-lecture.html?v={V}'))
print('ok', len(MUSCLE), len(DIV), len(FUNC))
