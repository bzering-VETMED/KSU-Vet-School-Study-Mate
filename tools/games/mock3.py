"""Practical 3 · MOCK PRACTICALS (made by Claude). Run from repo root: python3 tools/games/mock3.py
Stations follow the Lab Exam 3 blueprint (questions per lab + per topic).
ID stations use the clearest ⭐ "Bold-term labeled photos" (UMN first, then course slides / my photos),
one numbered structure per station. Conceptual stations use the ★ rows (professor emphasis) from the
per-lab Functions data. Lab 24 radiology (2 Qs) + Lab 25 (6 Qs) are left out until those materials exist.
Writes gross-anatomy-p3-mock.html and links it from the Practical 3 page + Practical 3 games page."""
import sys,os,re,glob,json,random,time,html,collections
sys.path.insert(0,'tools'); sys.path.insert(0,'tools/games')
from bs4 import BeautifulSoup,NavigableString
from common import CSS,TABJS
_src=open('tools/p3split.py').read(); exec(_src[:_src.index('for n in map')])   # norm, terms, item_bold, answer_text
from p3labfn_data import LABS as FNL,build_rest
V=str(int(time.time())); E=html.escape
LABS=[16,17,18,19,21,22,23,24]
T={n:terms(n) for n in LABS}
NMOCK=4
# ---------------- blueprint: (lab, kind, count, filter, label) ----------------
BP=[(16,'ID',2,None,'ID'),(16,'C',1,None,'Conceptual'),
    (17,'ID',4,None,'ID'),(17,'C',1,None,'Conceptual'),
    (18,'ID',5,None,'ID'),(18,'C',2,'ans18','Conceptual'),
    (19,'ID',2,'artery','Major arteries'),(19,'ID',1,'vein','Major veins'),(19,'ID',2,'nerve','Brachial plexus nerves'),
    (19,'C',1,'zone','Autonomous zones'),(19,'C',1,'integ','Innervation → muscle function'),
    (21,'ID',1,'wall','Abdominal wall nerves + vessels'),(21,'ID',1,'cord','Spermatic cord'),(21,'ID',1,'testis','Testis'),(21,'ID',1,'inguinal','Inguinal canal + openings'),
    (22,'ID',5,'organ','Abdominal organs'),(22,'ID',3,'mes','Mesenteries + ligaments'),(22,'ID',2,'kidney','Kidney features'),
    (23,'C',2,'ans23','ANS concepts'),(23,'ID',2,'artery','Arterial supply'),(23,'ID',1,'vein','Venous drainage'),
    (24,'ID',1,'pelvart','Arterial supply to pelvic viscera'),(24,'ID',1,'penisart','Arterial supply to the penis'),(24,'ID',2,'pelvisc','Pelvic viscera'),(24,'ID',1,'pouch','Peritoneal pouches')]
F={'artery':r'arter','vein':r'\bvein|\bvena','nerve':r'nerve',
   'wall':r'epigastric|pudendal|circumflex iliac|iliohypogastric|ilioinguinal|genitofemoral|cutaneous femoral|deep femoral|pudendoepigastric',
   'cord':r'ductus deferens|deferent|testicular (artery|vein|vessel)|pampiniform|cremaster|spermatic cord|mesorchium|mesoductus|vaginal tunic',
   'testis':r'epididym|tunica albuginea|\btestis\b|mediastinum testis|ligament of the tail|proper ligament of the testis|scrot',
   'inguinal':r'inguinal ring|inguinal canal|vaginal ring|vaginal process',
   'mes':r'ligament|omentum|meso|fold|bursa',
   'kidney':r'renal (pelvis|crest|cortex|medulla|hilus|sinus|papilla|pyramid|capsule|recess)|cortex|medulla|hilus|hilum|renal impression|fibrous capsule',
   'pelvart':r'(vesical|vaginal|prostatic|uterine|middle rectal|internal pudendal|umbilical|ductus deferens|internal iliac|ventral perineal|caudal rectal|caudal gluteal).*arter|arter.*(vesical|ductus)',
   'penisart':r'(penis|bulb|clitoris).*arter|arter.*(penis|bulb|clitoris)',
   'pouch':r'pouch|pararectal fossa',
   'pelvisc':r'bladder|rectum|anal canal|\banus\b|urethra|prostate|sphincter|trigone|rugae|paranal|coccygeus|levator ani|rectococcygeus|cutaneous zone'}
def nkey(n): return ' '.join(w for w in norm(re.sub(r'\(.*?\)','',n)) if w not in ('liver','lung','heart'))
def passes(lab,flt,name):
    l=re.sub(r'\(.*?\)','',name.lower())
    if flt is None: return True
    if flt=='organ': return not re.search(F['mes']+'|'+F['kidney']+r'|arter|vein|vessel|nerve|crus|diaphragm|kidney|adrenal|ureter',l)
    return bool(re.search(F[flt],l))
# ---------------- photo pool from the ⭐ best pages ----------------
LAB=re.compile(r'^(\d+[a-z]?|[A-Z]|#\d+|(?:double |long |short |white |unnumbered )?arrows?(?:head)?|asterisks?)$',re.I)
def clean(n):
    n=re.sub(r'^#?\d+\s+','',re.sub(r'\s*\((both|left|right|cut|reflected)\)','',n)).strip(' .;')
    return n[0].upper()+n[1:] if n else n
items=[]; seen=set()
for n in LABS:
    for f in sorted(glob.glob(f'gross-anatomy-lab{n}-best*.html'),key=lambda x:int(re.search(r'best(\d+)',x).group(1))):
        s=BeautifulSoup(open(f).read(),'html.parser')
        for c in s.select('section.card'):
            im=c.select_one('.pic img')
            if not im: continue
            q=c.select_one('.q'); tag=q.select_one('.tagline'); tg=tag.get_text() if tag else ''
            if tag: tag.extract()
            qt=q.get_text(' ',strip=True)
            find=bool(re.search(r'find|no labels|point to',qt,re.I))
            src=im['src'].split('?')[0]
            if not os.path.exists(src): continue
            kind='umn' if ('UMN' in tg or '🌐' in tg) else ('mine' if '📷' in tg else 'slide')
            imgs=[x['src'].split('?')[0] for x in c.select('.an img')]
            aimg=next((x for x in imgs if x!=src and os.path.exists(x)),'')
            facts=[x.get_text(' ',strip=True) for x in c.select('.fx')]+[x.get_text(' ',strip=True) for x in c.select('.clue')]
            big=c.select_one('.an.big')
            if big:
                bt=''.join(t for t in big.contents if isinstance(t,NavigableString)).strip()
                mm=re.findall(r'#(\d+)\s*([^#·]+)',bt)
                pairs=[(a,b.strip(' ·')) for a,b in mm] if len(mm)>1 else [(None,bt)]
            else:
                parts=[p.strip(' ·') for p in re.split(r'\s·\s',re.sub(r'#(\d+)\s',r'\1 · ',answer_text(c))) if p.strip(' ·')]
                pairs=[];i=0
                while i<len(parts):
                    if LAB.match(parts[i]) and i+1<len(parts): pairs.append((parts[i],parts[i+1])); i+=2
                    else: pairs.append((None,parts[i])); i+=1
            orient=re.split(r'\s*(Name|Identify)\b',qt)[0].strip(' .:')
            for lab_,name in pairs:
                if not name or len(name)>120: continue
                if find and not re.search(r'pouch|fossa',name,re.I): continue
                if lab_ is None and len(pairs)>1: continue          # unnumbered item on a multi-item photo → can't point to it
                key=(src,lab_,name.lower())
                if key in seen: continue
                seen.add(key)
                labs=[L for L in LABS if item_bold(name,T[L])]
                if not labs: continue
                if find: prompt='Name the peritoneal space the string is in.'
                elif lab_ is None: prompt='Identify the highlighted structure.'
                elif lab_.lower().startswith(('arrow','double','long','short','white','unnumbered')): prompt='Name the structure at the arrows.'
                elif lab_.lower().startswith('asterisk'): prompt='Name the structure marked with the asterisk.'
                else: prompt=f'Name structure {lab_.lstrip("#")}.'
                o=orient
                if lab_ is None or any(len(w)>4 and w in norm(o) for w in norm(re.sub(r'\(.*?\)','',name))): o=''
                w={'umn':3.0,'slide':2.0,'mine':2.5}[kind]*(0.02 if re.search(r'\bcats?\b',qt,re.I) else 1)
                items.append(dict(src=src,aimg=aimg,orient=o,prompt=prompt,ans=clean(name),facts=facts[:2],kind=kind,labs=labs,w=w))
print('photo items',len(items),collections.Counter(i['kind'] for i in items))
# ---------------- concept pool (★ rows) ----------------
A=dict(FNL); A.update(build_rest())
def star_rows(n,sec_rx=None):
    out=[]
    for h,rows in A[n]['secs']:
        if sec_rx and not re.search(sec_rx,h,re.I): continue
        out+= [(h,q,a) for q,a,s in rows if s]
    return out
def cprompt(h,q):
    return f'🧠 {q}: function / key concept?'
CPOOL={(16,None):[(cprompt(h,q),x) for h,q,x in star_rows(16,r'joint|thoracic wall')],
       (17,None):[(cprompt(h,q),x) for h,q,x in star_rows(17)],
       (18,'ans18'):[(cprompt(h,q),x) for h,q,x in star_rows(18,r'ANS|autonomic|pericard|heart')],
       (23,'ans23'):[(cprompt(h,q),x) for h,q,x in star_rows(23,r'ANS')],
       # Lab 19/20 integration + zones: written from the Lab 19/20 Functions rows (pre-lab transcript)
       (19,'zone'):[('🧭 Which thoracic limb nerves have autonomous zones, and which major nerve does NOT?','Musculocutaneous, axillary, radial, ulnar · NOT the median'),
                    ('🧭 Autonomous zone vs cutaneous area: what is the difference?','Cutaneous area = ALL skin a nerve supplies · autonomous zone = skin supplied ONLY by that nerve (no overlap) → the testing site'),
                    ('🧭 Where do you test the autonomous zone of the radial nerve?','Dorsal (cranial) surface over the proximal metacarpals 2–3 (superficial branch of the radial nerve)'),
                    ('🧭 Where do you test the autonomous zone of the musculocutaneous nerve?','Medial forearm, ~2 cm distal to the medial epicondyle (medial cutaneous antebrachial nerve)'),
                    ('🧭 Where do you test the autonomous zone of the axillary nerve?','Lateral arm, ~2 cm caudal to the shoulder (cranial lateral cutaneous brachial nerve)'),
                    ('🧭 Where do you test the autonomous zone of the ulnar nerve?','Caudal forearm ~4 cm distal to the olecranon (caudal cutaneous antebrachial nerve) · palmar branch = lateral 5th digit')],
       (19,'integ'):[('💪 A dog cannot bear weight on the thoracic limb (cannot extend the elbow, carpus, or digits). Which nerve is damaged?','Radial nerve (triceps + ALL the extensors)'),
                    ('💪 Musculocutaneous nerve damage weakens which action, through which muscles?','Elbow flexion · biceps brachii + brachialis'),
                    ('💪 Axillary nerve damage weakens which action, through which muscles?','Shoulder flexion · deltoideus, teres major, teres minor'),
                    ('💪 Suprascapular nerve damage affects which muscles?','Supraspinatus + infraspinatus'),
                    ('💪 The flexor carpi radialis and the superficial + deep digital flexors are innervated mainly by which nerve?','Median nerve (with the ulnar nerve for the caudolateral flexors)'),
                    ('💪 Which nerve supplies the latissimus dorsi? Which supplies the cutaneous trunci?','Thoracodorsal nerve · lateral thoracic nerve (panniculus reflex)'),
                    ('💪 Superficial pectorals vs deep pectoral: which nerves?','Cranial pectoral nerves → superficial pectorals · caudal pectoral nerves → deep pectoral')]}
for k,v in CPOOL.items(): print('concept',k,len(v))
# ---------------- build mocks ----------------
used=collections.Counter(); cused=collections.Counter(); MOCKS=[]
for m in range(NMOCK):
    rnd=random.Random(1000+m); st=[]; imgs=set(); names=set()
    for lab,kind,cnt,flt,label in BP:
        for _ in range(cnt):
            if kind=='C':
                pool=CPOOL.get((lab,flt)) or CPOOL.get((lab,None)) or []
                cand=[r for r in pool if r[0] not in names]
                if not cand: continue
                mn=min(cused[r[0]] for r in cand); cand=[r for r in cand if cused[r[0]]==mn]
                q,a=rnd.choice(cand); cused[q]+=1; names.add(q)
                st.append(dict(lab=lab,topic=label,type='C',prompt=q,ans=a,facts=[],src='',aimg='',orient=''))
            else:
                cand=[i for i in items if lab in i['labs'] and passes(lab,flt,i['ans']) and i['src'] not in imgs and nkey(i['ans']) not in names]
                if not cand: cand=[i for i in items if lab in i['labs'] and passes(lab,flt,i['ans']) and nkey(i['ans']) not in names]
                if not cand: print('  ⚠️ no photo for',lab,label); continue
                mn=min(used[(i['src'],i['prompt'])] for i in cand); cand=[i for i in cand if used[(i['src'],i['prompt'])]==mn]
                it=rnd.choices(cand,weights=[i['w'] for i in cand])[0]
                used[(it['src'],it['prompt'])]+=1; imgs.add(it['src']); names.add(nkey(it['ans']))
                st.append(dict(lab=lab,topic=label,type='ID',prompt=it['prompt'],ans=it['ans'],facts=it['facts'],src=it['src']+f'?v={V}',aimg=(it['aimg']+f'?v={V}') if it['aimg'] else '',orient=it['orient'],kind=it['kind']))
    for i,s in enumerate(st): s['id']=f'M{m+1}-{i+1}'
    MOCKS.append(st); print(f'Mock {m+1}: {len(st)} stations',collections.Counter(s['lab'] for s in st))
# ---------------- page ----------------
BPROWS=''.join(f'<tr><td>Lab {"19 + 20" if l==19 else l}</td><td>{E(lb)}</td><td>{c}</td></tr>' for l,k,c,f,lb in BP)
body=f'''<div class="tabs"><button class="on" data-t="p1">⏱️ Take a mock</button><button data-t="p2">🔁 Misses</button><button data-t="p3">📋 Blueprint</button></div>
<div id="p1" class="panel on">
 <div id="setup"><h2>Pick a mock practical</h2><p class="hint">Each mock follows the blueprint: <b>46 stations</b>, stations in lab order like the real thing. Write your answer <b>complete and specific</b> (full names, left/right), then grade yourself at the end.</p>
 <div class="grid" id="mpick"></div>
 <div class="row"><label><b>Seconds per station:</b> <select id="secs"><option>45</option><option selected>60</option><option>90</option><option value="0">Untimed</option></select></label>
 <label><b>Order:</b> <select id="ord"><option value="lab" selected>Lab order (like the exam)</option><option value="mix">Shuffled</option></select></label></div>
 <p class="hint" style="margin-top:10px">⚠️ Not included yet: <b>Lab 24 radiology</b> (2 Qs) + <b>Lab 25 repro</b> (6 Qs). They get added when those materials are posted.</p></div>
 <div id="stage" style="display:none">
  <div class="row" style="margin-top:0"><b id="snum"></b><span id="stopic" style="color:#8a6b99;font-weight:700"></span><span class="score" id="timer" style="font-size:26px"></span></div>
  <div id="sorient" class="hint" style="margin:6px 0 0"></div>
  <div class="q" id="sq"></div>
  <div id="sbox" style="background:#f7f0fb;border-radius:14px"><img id="simg" style="display:block;max-width:100%;max-height:62vh;margin:auto;border-radius:14px;cursor:zoom-in"></div>
  <div class="row"><input id="sin" autocomplete="off" autocapitalize="off" placeholder="Your answer (full name)" style="flex:1;min-width:200px;font-size:17px;padding:12px;border-radius:12px;border:2px solid var(--line)"><button class="btn hot" id="snext">Next ▶</button></div>
  <div class="row"><button class="btn" id="sback">◀ Back</button><button class="btn" id="squit">🏁 End + grade now</button></div>
 </div>
 <div id="review" style="display:none"></div>
</div>
<div id="p2" class="panel"><h2>🔁 Misses</h2><p class="hint">Every station you mark ❌ is saved on this device. Get it right <b>twice in a row</b> to clear it.</p>
 <div class="row" style="margin-top:0"><b id="mcount"></b><button class="btn hot" id="mgo">▶ Drill my misses</button><button class="btn" id="mclear">🗑️ Clear all</button></div>
 <div id="mstage" style="display:none"><div id="morient" class="hint"></div><div class="q" id="mq"></div><div style="background:#f7f0fb;border-radius:14px"><img id="mimg" style="display:block;max-width:100%;max-height:60vh;margin:auto;border-radius:14px"></div><div class="fb" id="mans"></div>
 <div class="row"><button class="btn hot" id="mrev">💗 Reveal</button><button class="btn" id="mgot" style="display:none">✅ Got it</button><button class="btn" id="mmiss" style="display:none">❌ Missed</button></div></div><div class="fb" id="mend"></div></div>
<div id="p3" class="panel"><h2>📋 What each mock samples</h2><p class="hint">From the Lab Exam 3 blueprint (54 Qs, 2 pts each). ID = photo station · Conceptual = function / concept question from his ★ emphasis.</p>
 <table style="width:100%;border-collapse:collapse;font-size:15px"><tr style="background:#f3eafb"><th align="left">Lab</th><th align="left">Topic</th><th>Qs</th></tr>{BPROWS}<tr><td>Lab 24</td><td>Radiology abdomen <i>(not yet)</i></td><td>2</td></tr><tr><td>Lab 25</td><td>Male + female repro <i>(not yet)</i></td><td>6</td></tr></table></div>
<div id="zoom" style="display:none;position:fixed;inset:0;background:#000d;z-index:9;padding:env(safe-area-inset-top,0px) 0 0;overflow:auto" onclick="this.style.display='none'"><img id="zimg" style="width:100%;height:auto;display:block"></div>'''
EXTRA_CSS='''.rv{border:1px solid var(--line);border-radius:16px;padding:10px;margin:10px 0;background:#fff}.rv img{max-width:100%;max-height:260px;border-radius:12px;display:block;margin:6px 0}
.rv .you{font-weight:800}.rv .key{background:#f4ebfb;border-radius:10px;padding:8px;margin-top:6px;font-weight:800;color:#4b1f70}.rv .fx{font-size:14px;color:#6b5579;margin-top:4px}
.rv.ok{border-left:8px solid var(--ok)}.rv.bad{border-left:8px solid var(--bad)}.gb{border:0;border-radius:12px;padding:9px 13px;font-weight:800;font-size:15px;margin-right:6px;background:#f3eafb;color:#65328c}.gb.on.y{background:#1d8a4b;color:#fff}.gb.on.n{background:#c2185b;color:#fff}
table td,table th{padding:6px;border-bottom:1px solid var(--line)}'''
js=TABJS+'const M='+json.dumps(MOCKS,ensure_ascii=False)+';'+r'''
tabs();
const LS={get(){try{return JSON.parse(localStorage.getItem('p3mockMisses')||'[]')}catch(e){return[]}},set(v){try{localStorage.setItem('p3mockMisses',JSON.stringify(v))}catch(e){}}};
const BEST={get(){try{return JSON.parse(localStorage.getItem('p3mockBest')||'{}')}catch(e){return{}}},set(v){try{localStorage.setItem('p3mockBest',JSON.stringify(v))}catch(e){}}};
function esc(s){return (s||'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]))}
function pick(){let P=$('#mpick');P.innerHTML='';let b=BEST.get();M.forEach((m,i)=>{let c=el('button','chip',`📝 <b>Mock ${i+1}</b><br><small>${m.length} stations${b[i]!=null?' · best '+b[i]+'%':''}</small>`);c.onclick=()=>start(i);P.appendChild(c)})}
pick();
let S=[],K=0,ANS=[],TM=null,LEFT=0,MI=0;
function start(i){MI=i;S=M[i].slice();if($('#ord').value==='mix')S=sh(S);ANS=S.map(()=>'');K=0;$('#setup').style.display='none';$('#review').style.display='none';$('#stage').style.display='';show()}
function show(){let s=S[K];$('#snum').textContent=`Station ${K+1} / ${S.length}`;$('#stopic').textContent=` · Lab ${s.lab===19?'19/20':s.lab} · ${s.topic}`;$('#sorient').textContent=s.orient?('🧭 '+s.orient):'';$('#sq').textContent=s.prompt;
 if(s.src){$('#sbox').style.display='';$('#simg').src=s.src}else $('#sbox').style.display='none';
 $('#sin').value=ANS[K]||'';$('#sback').style.display=K?'':'none';$('#snext').textContent=K===S.length-1?'Finish 🏁':'Next ▶';
 clearInterval(TM);LEFT=+$('#secs').value;if(LEFT){$('#timer').textContent='⏱ '+LEFT;TM=setInterval(()=>{LEFT--;$('#timer').textContent='⏱ '+LEFT;if(LEFT<=0){clearInterval(TM);go(1)}},1000)}else $('#timer').textContent='';
 setTimeout(()=>{try{$('#sin').focus({preventScroll:true})}catch(e){}},50)}
function go(d){ANS[K]=$('#sin').value.trim();K+=d;if(K>=S.length){finish();return}if(K<0)K=0;show()}
$('#snext').onclick=()=>go(1);$('#sback').onclick=()=>go(-1);$('#squit').onclick=()=>{ANS[K]=$('#sin').value.trim();finish()};
$('#sin').addEventListener('keydown',e=>{if(e.key==='Enter'){e.preventDefault();go(1)}});
$('#simg').onclick=()=>{$('#zimg').src=$('#simg').src;$('#zoom').style.display='block'};
const STOP=new Set(['the','of','and','a','an','to','its','with','or','in','on','for','artery','vein','nerve','muscle','ligament']);
function toks(t){return (t||'').toLowerCase().replace(/\(.*?\)/g,' ').match(/[a-z0-9]+/g)||[]}
function guess(you,key){let y=new Set(toks(you).map(w=>w.replace(/s$/,'')));let k=toks(key).filter(w=>!STOP.has(w)).map(w=>w.replace(/s$/,''));if(!y.size||!k.length)return false;let hit=k.filter(w=>y.has(w)).length;
 let side=['left','right','cranial','caudal','dorsal','ventral','medial','lateral','superficial','deep','major','minor'].filter(w=>k.includes(w));if(side.some(w=>!y.has(w)))return false;
 let typ=['artery','vein','nerve','muscle','ligament'].filter(w=>toks(key).includes(w));if(typ.length&&!typ.some(w=>toks(you).map(x=>x.replace(/s$/,'')).includes(w)))return false;return hit>=Math.ceil(k.length*0.75)}
function finish(){clearInterval(TM);$('#stage').style.display='none';let R=$('#review');R.style.display='';
 let G=S.map((s,i)=>s.type==='ID'?guess(ANS[i],s.ans):null);
 R.innerHTML='<h2>🏁 Grade yourself</h2><p class="hint">Auto-check guessed ✅/❌ for photo stations: fix any it got wrong (be strict: "complete and specific"). Conceptual 🧠 stations: grade them yourself.</p><div id="sumbox" class="fb show"></div>'+
 S.map((s,i)=>`<div class="rv" id="rv${i}"><div><b>${i+1}. Lab ${s.lab===19?'19/20':s.lab} · ${esc(s.topic)}</b></div>${s.orient?'<div class="fx">🧭 '+esc(s.orient)+'</div>':''}<div>${esc(s.prompt)}</div>${s.src?'<img loading="lazy" src="'+s.src+'">':''}<div class="you">✍️ You: ${ANS[i]?esc(ANS[i]):'<i>(blank)</i>'}</div><div class="key">🔑 ${esc(s.ans)}</div>${(s.facts||[]).map(f=>'<div class="fx">'+esc(f)+'</div>').join('')}${s.aimg?'<details><summary class="fx">Show labeled version</summary><img loading="lazy" src="'+s.aimg+'"></details>':''}<div class="row"><button class="gb y" data-i="${i}" data-v="1">✅ Right</button><button class="gb n" data-i="${i}" data-v="0">❌ Wrong</button></div></div>`).join('')+
 '<div class="row"><button class="btn hot" id="save">💾 Save score + misses</button><button class="btn" id="again">↺ Pick another mock</button></div>';
 S.forEach((s,i)=>{if(G[i]!==null)mark(i,G[i]?1:0)});
 R.querySelectorAll('.gb').forEach(b=>b.onclick=()=>mark(+b.dataset.i,+b.dataset.v));
 $('#save').onclick=save;$('#again').onclick=()=>{R.style.display='none';$('#setup').style.display='';pick()};summ();window.scrollTo(0,0)}
let MARK={};function mark(i,v){MARK[i]=v;let r=document.getElementById('rv'+i);r.classList.toggle('ok',v===1);r.classList.toggle('bad',v===0);r.querySelectorAll('.gb').forEach(b=>b.classList.toggle('on',+b.dataset.v===v));summ()}
function summ(){let by={},ok=0,done=0;S.forEach((s,i)=>{let k='Lab '+(s.lab===19?'19/20':s.lab);by[k]=by[k]||[0,0];by[k][1]++;if(MARK[i]===1){by[k][0]++;ok++}if(MARK[i]!=null)done++});
 $('#sumbox').innerHTML=`<div style="font-size:22px">Score: ${ok}/${S.length} · ${Math.round(100*ok/S.length)}% · ${ok*2}/${S.length*2} pts</div><div class="fx">${done}/${S.length} graded</div><div class="row">`+Object.entries(by).map(([k,v])=>`<span style="padding:6px 10px;border-radius:999px;background:${v[0]===v[1]?'#e7f6ec':'#fde7f0'};font-weight:800">${k}: ${v[0]}/${v[1]}</span>`).join('')+'</div>'}
function save(){let m=LS.get();S.forEach((s,i)=>{if(MARK[i]===0&&!m.find(x=>x.id===s.id))m.push({...s,streak:0,you:ANS[i]})});LS.set(m);let ok=S.filter((s,i)=>MARK[i]===1).length;let b=BEST.get();b[MI]=Math.max(b[MI]||0,Math.round(100*ok/S.length));BEST.set(b);updM();$('#save').textContent='✅ Saved · misses in the 🔁 tab'}
// misses drill
let mq=[],mk=0;function updM(){$('#mcount').textContent=`${LS.get().length} saved misses`}updM();
function mShow(){if(mk>=mq.length){$('#mstage').style.display='none';$('#mend').className='fb show';$('#mend').innerHTML=`Round done. ${LS.get().length} misses left.`;updM();return}let c=mq[mk];$('#morient').textContent=(c.orient?'🧭 '+c.orient+' · ':'')+`Lab ${c.lab===19?'19/20':c.lab} · streak ${c.streak||0}/2`;$('#mq').textContent=c.prompt;if(c.src){$('#mimg').style.display='';$('#mimg').src=c.src}else $('#mimg').style.display='none';$('#mans').className='fb';$('#mrev').style.display='';$('#mgot').style.display=$('#mmiss').style.display='none'}
$('#mgo').onclick=()=>{mq=sh(LS.get());mk=0;$('#mend').className='fb';if(!mq.length){$('#mend').className='fb show';$('#mend').textContent='No misses saved yet. Take a mock and save your grade first!';return}$('#mstage').style.display='';mShow()};
$('#mrev').onclick=()=>{let c=mq[mk];$('#mans').className='fb show';$('#mans').innerHTML='<div style="font-size:20px">🔑 '+esc(c.ans)+'</div>'+(c.facts||[]).map(f=>'<div style="font-size:14px;font-weight:600">'+esc(f)+'</div>').join('')+(c.aimg?'<img src="'+c.aimg+'" style="max-width:100%;border-radius:12px;margin-top:8px">':'');$('#mrev').style.display='none';$('#mgot').style.display=$('#mmiss').style.display=''};
function mRes(ok){let m=LS.get(),c=mq[mk],x=m.find(y=>y.id===c.id);if(x){x.streak=ok?(x.streak||0)+1:0;if(x.streak>=2)m=m.filter(y=>y!==x)}LS.set(m);mk++;updM();mShow()}
$('#mgot').onclick=()=>mRes(true);$('#mmiss').onclick=()=>mRes(false);
let clr=0;$('#mclear').onclick=()=>{if(!clr){clr=1;$('#mclear').textContent='Tap again to clear';setTimeout(()=>{clr=0;$('#mclear').textContent='🗑️ Clear all'},3000);return}LS.set([]);updM();$('#mclear').textContent='🗑️ Clear all';clr=0};
document.addEventListener('keydown',e=>{if($('#stage').style.display!=='none'&&e.key==='ArrowLeft'&&document.activeElement!==$('#sin'))go(-1)});'''
pg=(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><title>Practical 3 mock exams</title><style>{CSS}{EXTRA_CSS}</style></head>'
    f'<body><div class="wrap"><a class="back" href="gross-anatomy-practical3.html?v={V}">← Back to Practical 3</a><div class="hero"><h1>📝 Practical 3 · Mock exams</h1><p>{NMOCK} full mocks · blueprint-weighted · your clearest bold-term photos + his ★ function questions</p></div>{body}'
    f'<div style="text-align:center;color:#8a6b99;margin:18px 0">🎀 Bethany · K-State CVM Class of 2030 · 🐾</div></div><script>{js}</script></body></html>')
open('gross-anatomy-p3-mock.html','w').write(pg)
# ---------------- links ----------------
LINK=f'<!--mock--><a href="gross-anatomy-p3-mock.html?v={V}" style="display:block;text-decoration:none;margin:0 0 14px;padding:14px 16px;border-radius:18px;color:#fff;font-weight:900;font-size:18px;background:linear-gradient(120deg,#6a3392,#e05fa8)">📝 Mock practicals · 4 full timed exams<span style="display:block;font-size:14px;font-weight:700;opacity:.9">Blueprint-weighted · clearest bold-term photos · function Qs · self-grade + misses</span></a><!--/mock-->'
p=open('gross-anatomy-practical3.html').read(); p=re.sub(r'<!--mock-->.*?<!--/mock-->','',p,flags=re.S)
anchor='<!--labfn-->' if '<!--labfn-->' in p else '<div class="grid">'
p=p.replace(anchor,LINK+anchor,1); open('gross-anatomy-practical3.html','w').write(p)
g='gross-anatomy-p3-games.html'
if os.path.exists(g):
    h=open(g).read(); h=re.sub(r'<!--mock-->.*?<!--/mock-->','',h,flags=re.S)
    m=re.search(r'<div class="hero">.*?</div>',h,re.S)
    if m: h=h.replace(m.group(0),m.group(0)+'<div style="margin-top:12px">'+LINK+'</div>',1); open(g,'w').write(h)
print('wrote gross-anatomy-p3-mock.html')
