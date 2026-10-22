"""Practical 3 · 🩻 Lab 24 radiology (abdomen) · tap-to-reveal FUNCTIONS / concepts page (made by Claude).
Source: Dr. McHaney's radiology lecture TRANSCRIPT (10/22 upload) + the lecture slides already on the radiology hub.
★ pink rows = she stressed it (asked the class, repeated it, gave a mnemonic, or called it important).
Writes gross-anatomy-rad-abd-functions.html, links it from the radiology hub (🧠 section) and the Practical 3 page.
Run from repo root: python3 tools/p3radfn.py"""
import re,time,html
E=html.escape; V=str(int(time.time()))
TITLE='Lab 24 · Radiology abdomen'
SRC='radiology lecture transcript (Dr. McHaney) + slides'
TRAPS=[
 'Abdomen = END OF EXPIRATION · thorax = peak INSPIRATION (opposite!)',
 'Left lateral (left side DOWN) → gas rises into the RIGHT-side pylorus + duodenum · right lateral → gas in the LEFT-side fundus',
 'Barium/fluid does the OPPOSITE of gas (it sinks): right lateral → barium in pylorus/duodenum · left lateral → barium in fundus',
 'VD (on its back): fundus is dorsal → fills with FLUID; body + pylorus fill with GAS · DV = the reverse',
 'Caudoventral liver margin: DOG = LEFT lateral lobe · CAT = RIGHT lateral lobe',
 'Kidney length on the VD: dog 2.5–3.5 × L2 · cat 2–3 × L2 (not L1, not L3)',
 'LEFT kidney is more CAUDAL ("left is left behind") · RIGHT kidney sits in the renal fossa of the caudate lobe of the liver',
 'Serosal detail comes from intra-abdominal FAT, not gas. Fluid/effusion LOWERS detail (border effacement)',
 'Soft tissue and fluid are the SAME opacity',
 'Spleen HEAD is fixed (gastrosplenic ligament); the TAIL is mobile',
]
FLAGS=[
 ('Gallbladder lobes','She left this as a "think about it" question. Standard anatomy: between the quadrate lobe and the right medial lobe (outside her lecture · confirm in lab).'),
 ('Transcript garbles','fungus = fundus · duagnum / philodnum / diognum = duodenum · pyloris = pylorus · calciform / falsiform = falciform fat · cirrhosal / serotal = serosal detail · crossval / crossfal arch = costal arch · caudite lobe of the river = caudate lobe of the liver · sphonic / splintered = splenic · cruise = crura · pyborisum = pylorus'),
]
S=[  # (section, [(prompt, answer, star)])
 ('🌗 Opacities + technique',[
  ('5 opacities, least → most opaque','Gas → fat → soft tissue = fluid → mineral → metal',1),
  ('When do you expose an abdominal film?','End of EXPIRATION (pause, least motion blur) · thorax is the opposite (peak inspiration)',1),
  ('Field boundaries of an abdominal film','Diaphragm → coxofemoral joints · pelvic limbs extended caudally · take a 2nd film if it does not fit',1),
  ('Standard views at K-State','Left lateral + right lateral + ventrodorsal (VD) · minimum = 2 orthogonal views',1),
  ('Why both laterals?','Different structures fill with gas on each side (left lateral → pylorus + duodenum highlighted)',1),
  ('Why orthogonal views?','A 3-D animal is squashed into a 2-D shadow → need 2 views to localize',0)]),
 ('📸 Additional views',[
  ('Compression view','Wooden spoon presses the abdomen → moves bowel off a region → less superimposition (e.g. small kidney, mass)',1),
  ('Pneumogastrogram / pneumocolonogram','Air into the stomach (orogastric tube) or colon (red rubber catheter) → outlines the organ, tells colon from small bowel',0),
  ('Perineal lateral (pelvic limbs pulled forward)','Shows the region of the urethra for urinary stones (femurs + fabellae moved off it)',0),
  ('Horizontal beam','Beam shot ACROSS the animal → detects free gas in the abdomen (surgical emergency) or thorax',1)]),
 ('🧭 Systematic read',[
  ('Her reading order','Extra-abdominal → serosal detail + contour → large parenchymal organs (liver, spleen) → urogenital → GI tract LAST',1),
  ('Why the GI tract last?','Most superimposition/most complex · and if you find the foreign body first you stop looking at everything else',1),
  ('Extra-abdominal structures','Non-abdominal soft tissues (nipples, prepuce, masses), subcutis, pelvic limb + lumbar muscles, skeleton, body wall, diaphragm, THORAX on the edge',0),
  ('Nipples / skin tags / prepuce','Look like masses → confirm on the orthogonal view',0),
  ('Epaxial vs hypaxial on a film','Epaxial = DORSAL to the transverse processes · hypaxial = VENTRAL · they make confusing lines',0),
  ('Why trace the body wall?','Look for herniation/disruption (trauma, bite wounds)',0)]),
 ('🫁 Diaphragm, contour + serosal detail',[
  ('Which side of the diaphragm do you normally see?','Thoracic side only (gas in the lungs); the abdominal side border-effaces with liver/stomach',1),
  ('When do you see the ABDOMINAL side?','Lots of falciform fat (normal variant, cats) OR free peritoneal gas (pathologic unless post-surgery)',1),
  ('Diaphragm parts seen','Cupola (dome) + right and left crura',0),
  ('Abdominal contour','Breed shape: greyhound = tucked up · English bulldog = pendulous · most dogs in between',0),
  ('What gives serosal detail in the abdomen?','Intra-abdominal (visceral) FAT around organ margins',1),
  ('6 causes of poor serosal detail','Emaciation · young age (brown fat = more water) · peritoneal effusion · serosal disease (peritonitis, carcinomatosis) · mass effect / organomegaly (e.g. pregnancy) · big patient / technique (scatter)',1)]),
 ('🫀 Liver + spleen',[
  ('Liver borders','Cranial: diaphragm · caudal: stomach, right kidney, small bowel · lateral: body wall · ventral: falciform fat',0),
  ('Easiest liver margin to see','Caudoventral margin · DOG = left lateral lobe · CAT = right lateral lobe',1),
  ('Gastric axis','Line fundus → pylorus · normal = between perpendicular to the spine and parallel to the ribs',1),
  ('Normal caudal extent of the liver','Within or just past the costal arch · NOT out to the kidney poles (= too big)',0),
  ('Big liver vs small liver on film','Big: margins past the costal arch, rounded/lumpy, axis shifted caudally · small: axis displaced cranially',0),
  ('Spleen head','Left cranial abdomen, FIXED, triangle on VD / small fusiform shape on lateral (often seen in cats)',0),
  ('Spleen tail','Mobile · dog: usually seen ventrally on the lateral · cat: rarely (smaller spleen)',0),
  ('What attaches the spleen to the stomach?','Gastrosplenic ligament (short gastric arteries run in it) · NOT the greater omentum',1)]),
 ('🫘 Urogenital + retroperitoneum',[
  ('Kidney position','Cranial + dorsal, retroperitoneal · LEFT more caudal + more mobile ("left is left behind")',1),
  ('Right kidney hard to see because…','Superimposed liver, bowel, stomach, spleen · it sits in the renal fossa of the caudate lobe',0),
  ('Kidney size (VD)','Dog 2.5–3.5 × length of L2 · cat 2–3 × L2',1),
  ('Retroperitoneal structures you see','Lumbar muscles + kidneys (sometimes aorta/vessels) · NOT ureters, adrenals, lymph nodes unless abnormal',0),
  ('Round dots ventral to the spine','Deep circumflex iliac arteries seen end-on (mistaken for lymph nodes)',0),
  ('Urinary bladder regions','Apex · body · neck/trigone · easier on the LATERAL (spine, pelvis, colon overlap on VD)',0)]),
 ('🍽️ GI tract',[
  ('Stomach shape: dog vs cat','Dog: left → right across the whole abdomen · cat: J-shaped, pylorus on midline',0),
  ('4 regions of the stomach','Cardia · fundus · body · pylorus',1),
  ('Right lateral: where is the gas?','Fundus (left-sided, now up)',1),
  ('Left lateral: where is the gas?','Pylorus + duodenum (right-sided, now up)',1),
  ('Barium on a right lateral','Pools in the pylorus + duodenum (right side, down)',1),
  ('VD: fundus has…','Fluid / barium (fundus is dorsal) · body + pylorus get the gas · DV = reverse',1),
  ('Small intestine on film','Tubular, uniform diameter, gas/fluid/mixed, smooth margins, everywhere · can NOT judge wall thickness',0),
  ('Fat cat quirk','Small bowel clusters on the right side',0),
  ('Cecum: dog vs cat','Dog: C-shaped / corkscrew, mid-abdomen, gas-filled · cat: comma/cone, rarely seen',0),
  ('Colon parts','Ascending, transverse, descending (descending is mobile) → rectum in the pelvic canal',0)]),
 ('👻 Not seen in health',[
  ('Gallbladder','Border-effaces with the liver · seen only if mineralized · ventral right liver',0),
  ('Pancreas','Body at the pyloroduodenal angle · right lobe along the descending duodenum (bigger in dogs) · left lobe along the greater curvature (bigger in cats; seen in obese cats)',0),
  ('Ureters + urethra','Only with contrast or when huge/stones · male urethra: prostatic, membranous (pelvic), penile',0),
  ('Adrenal glands','Right: medial + slightly cranial to the right kidney · left: more cranial to its kidney · enlarged → kidney pushed caudolaterally',0),
  ('Uterus','Dorsal to the bladder, ventral to the colon · seen only when enlarged (gravid from ~25–30 days)',0),
  ('Prostate','Intact males (not neutered, not cats) · < 70% of pelvic-inlet height · fat triangle separates it from the bladder',0),
  ('Medial iliac lymph nodes','Ventral to L6–L7, dorsal to the descending colon → push it ventrally when enlarged',0),
  ('Mesenteric lymph nodes','Central · drain abdominal viscera · push bowel peripherally when enlarged',0)]),
]
t=open('systems-lp1-functions.html').read()
css=t[t.index('<style>')+7:t.index('</style>')]
css+='''tr.star td{background:#FBE7EF!important}tr.star td:first-child{color:#c2185b}tr.star td:first-child:before{content:"★ ";color:#D94F7F}
.trap{background:#FBE7EF;border:2px solid #D94F7F;border-radius:14px;padding:10px 12px;margin:12px 0}.trap h2{margin:0 0 6px;font-size:17px;color:#b0306a}.trap li{margin:4px 0;font-size:14.5px;line-height:1.35}
.flag{background:#FFF1E3;border:2px dashed #E07B39;border-radius:14px;padding:10px 12px;margin:12px 0;font-size:14.5px}.flag b{color:#b85a1c}
.legend{font-size:13px;color:#8a6b99;margin:8px 0}.legend span{background:#FBE7EF;color:#c2185b;font-weight:800;border-radius:6px;padding:1px 6px}
body.staronly tr:not(.star){display:none}'''
js=t[t.index('<script>'):]
js=js.replace("document.getElementById('hide').onclick","document.getElementById('star').onclick=()=>{document.body.classList.toggle('staronly');document.getElementById('star').textContent=document.body.classList.contains('staronly')?'📋 Show all rows':'★ Starred only'};document.getElementById('hide').onclick",1)
rows=sum(len(r) for _,r in S); stars=sum(1 for _,r in S for x in r if x[2])
b=f'<body><div class="wrap"><a class="back" href="gross-anatomy-practical3.html?v={V}">← Back to Practical 3</a> <a class="back" href="gross-anatomy-rad-abd-images.html?v={V}">🩻 Radiology hub</a>'
b+=f'<div class="hero"><h1>🩻 {E(TITLE)} · Functions + concepts</h1><p>Say it, then tap the pink box · {rows} items · ★ {stars} she stressed · {E(SRC)}</p></div>'
b+='<div class="bar"><button id="hide">🙈 Hide all</button><button id="all">👀 Show all</button><button id="star">★ Starred only</button><span class="n" id="n"></span></div>'
b+='<p class="legend"><span>★ pink row</span> = she asked the class, repeated it, or gave a mnemonic. Blueprint: 2 questions, "ID abdominal viscera."</p>'
b+='<div class="trap"><h2>⚠️ Precision traps</h2><ul>'+''.join(f'<li>{E(x)}</li>' for x in TRAPS)+'</ul></div>'
for ft,fx in FLAGS: b+=f'<div class="flag"><b>{E(ft)}</b> · {E(fx)}</div>'
b+='<div class="cols">'
for i,(h,rs) in enumerate(S):
    b+=f'<div class="sec{" p" if i%2 else ""}"><h2>{E(h)}</h2><table>'+''.join(f'<tr class="{"star" if s else ""}"><td>{E(q)}</td><td><span class="ans">{E(a)}</span></td></tr>' for q,a,s in rs)+'</table></div>'
b+='</div><div class="foot">🎀 Bethany · K-State CVM Class of 2030 · 🐾</div></div>'
FN='gross-anatomy-rad-abd-functions.html'
open(FN,'w').write(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Radiology Functions</title><style>{css}</style></head>'+b+js)
# links
h=open('gross-anatomy-rad-abd-images.html').read(); h=re.sub(r'<!--fn-->.*?<!--/fn-->','',h,flags=re.S)
m=re.search(r'(<div class="sec terms"[^>]*><h2>[^<]*</h2>)',h)
link=f'<!--fn--><a href="{FN}?v={V}">🧠 Functions + concepts · tap to reveal<span>{rows} items · ★{stars}</span></a><!--/fn-->'
h=h.replace(m.group(1),m.group(1)+link,1) if m else h.replace('</body>',link+'</body>',1)
open('gross-anatomy-rad-abd-images.html','w').write(h)
p=open('gross-anatomy-practical3.html').read(); p=re.sub(r'<!--radfn-->.*?<!--/radfn-->','',p,flags=re.S)
pill=f'<!--radfn--><a href="{FN}?v={V}" style="display:inline-block;text-decoration:none;margin:-6px 0 14px;padding:8px 12px;border-radius:999px;background:#FBE7EF;color:#b0306a;font-weight:800;font-size:14px">🩻 Lab 24 radiology · Functions · ★{stars}</a><!--/radfn-->'
p=p.replace('<!--/labfn-->','<!--/labfn-->'+pill,1) if '<!--/labfn-->' in p else p.replace('<div class="grid">',pill+'<div class="grid">',1)
open('gross-anatomy-practical3.html','w').write(p)
print(FN,rows,'items ★',stars,'· hub link',bool(m))
