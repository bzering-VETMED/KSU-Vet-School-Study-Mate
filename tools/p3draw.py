"""Practical 3 · hand-drawn schematic cards (made by Claude) for bold terms with NO photo anywhere (Labs 17–23).
Numbered pink badges, no names on the picture; tap = answer. Also crops lab-guide figures (bronchial tree Fig 3-13,
autonomous-zone slide). Writes assets/p3draw_*.svg|jpg + tools/p3draw_cards.json, which p3fill.py puts in each
lab's ⭐ "Last gaps filled" page.   python3 tools/p3draw.py <Lab_17.pdf> <Lab_20_and_21_Forelimb_vessels.pdf>"""
import sys,os,json,re,html
sys.path.insert(0,'tools')
from deck import img_card_facts
import pymupdf
from PIL import Image,ImageDraw,ImageFont
L17,FL=sys.argv[1],sys.argv[2]
A,V,N,LY,PER,ORG='#d64545','#3d6fd6','#d9a400','#2f9e6e','#7b42a0','#f6dbe6'
TAG='✏️ schematic drawing by Claude · gap fill (no photo exists)'
def b(x,y,n,lx=None,ly=None):
    s=f'<line x1="{lx}" y1="{ly}" x2="{x}" y2="{y}" stroke="#5d347e" stroke-width="2"/>' if lx is not None else ''
    return s+f'<circle cx="{x}" cy="{y}" r="17" fill="#e05fa8" stroke="#fff" stroke-width="3"/><text x="{x}" y="{y+6}" text-anchor="middle" font-size="17" font-weight="800" fill="#fff" font-family="Arial">{n}</text>'
def t(x,y,s,sz=15,c='#7a6585',a='start'): return f'<text x="{x}" y="{y}" font-size="{sz}" fill="{c}" font-family="Arial" text-anchor="{a}">{html.escape(s)}</text>'
def svg(name,w,h,body):
    open(f'assets/p3draw_{name}.svg','w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}"><rect width="{w}" height="{h}" fill="#fff"/>{body}</svg>')
    return f'assets/p3draw_{name}.svg?v={{V}}'
C={}
def card(lab,covers,q,img,ans,clue,facts=(),tag=TAG):
    C.setdefault(str(lab),[]).append({'covers':[x.lower() for x in covers],'html':img_card_facts(q,img,ans,clue,'',list(facts),tag)})
# ---------- Lab 17 · pleurae (transverse section, dorsal up)
body=(f'<ellipse cx="400" cy="290" rx="370" ry="255" fill="#efe6f5" stroke="#b9a3c9" stroke-width="14"/>'
 f'<circle cx="400" cy="62" r="38" fill="#ddd" stroke="#aaa" stroke-width="3"/><rect x="378" y="520" width="44" height="26" rx="6" fill="#ddd" stroke="#aaa" stroke-width="3"/>'
 f'<rect x="352" y="100" width="96" height="420" fill="#fff4e8"/><ellipse cx="400" cy="420" rx="88" ry="78" fill="#f2b6c4" stroke="#c46a83" stroke-width="3"/>'
 f'<ellipse cx="200" cy="290" rx="168" ry="215" fill="#fff" stroke="{PER}" stroke-width="4"/><ellipse cx="600" cy="290" rx="168" ry="215" fill="#fff" stroke="{PER}" stroke-width="4"/>'
 f'<ellipse cx="205" cy="295" rx="135" ry="180" fill="{ORG}" stroke="#d4537e" stroke-width="4"/><ellipse cx="595" cy="295" rx="135" ry="180" fill="{ORG}" stroke="#d4537e" stroke-width="4"/>'
 +b(60,170,1,44,230)+b(352,215,2,366,250)+b(130,330,3,72,330)+b(230,100,4,205,93)+b(400,330,5)+t(20,580,'Transverse section · dorsal up · purple = parietal · pink = on the lung',15))
card(17,['pleurae'],'Thorax, transverse section. Name 1–5.',svg('pleurae',800,600,body),
 '#1 Costal pleura (parietal) · #2 Mediastinal pleura (parietal) · #3 Pulmonary (visceral) pleura · #4 Pleural cavity · #5 Mediastinum · Pleurae',
 'Pleurae = the two pleural sacs: parietal pleura (costal, diaphragmatic, mediastinal parts) lines the wall; pulmonary (visceral) pleura covers the lung; pleural cavity = the potential space between',
 [('🔁 Pericardial mediastinal pleura','The mediastinal pleura where it covers the pericardium (around #5\'s heart)')])
# ---------- Lab 17 · tracheal trunks (ventral view, dog's right on the LEFT)
body=(f'<rect x="375" y="40" width="50" height="470" rx="20" fill="#e9e2ee" stroke="#a99bb5" stroke-width="3"/>'
 +''.join(f'<line x1="375" y1="{y}" x2="425" y2="{y}" stroke="#c9bdd3" stroke-width="3"/>' for y in range(60,510,26))+
 f'<path d="M330 40 L330 470" stroke="{A}" stroke-width="7" fill="none"/><path d="M470 40 L470 470" stroke="{A}" stroke-width="7" fill="none"/>'
 f'<path d="M250 40 L250 420 L330 470" stroke="{V}" stroke-width="10" fill="none"/><path d="M550 40 L550 420 L470 470" stroke="{V}" stroke-width="10" fill="none"/>'
 f'<path d="M345 50 L345 400 L262 418" stroke="{LY}" stroke-width="5" fill="none" stroke-dasharray="10 6"/><path d="M455 50 L455 380 L540 410" stroke="{LY}" stroke-width="5" fill="none" stroke-dasharray="10 6"/>'
 f'<path d="M620 560 C600 500 580 450 548 416" stroke="{LY}" stroke-width="7" fill="none"/>'
 f'<ellipse cx="345" cy="45" rx="20" ry="14" fill="#9fd9bd" stroke="{LY}" stroke-width="3"/><ellipse cx="455" cy="45" rx="20" ry="14" fill="#9fd9bd" stroke="{LY}" stroke-width="3"/>'
 +b(345,230,1,300,230)+b(455,230,2,500,230)+b(612,520,3)+b(400,300,4)+b(250,200,5)+b(330,120,6,290,120)+b(345,45,7,300,45)
 +t(20,595,"Ventral view · dog's RIGHT is on the LEFT · green = lymph · red = artery · blue = vein",15))
card(17,['right tracheal trunk'],'Neck + thoracic inlet, ventral view. Name 1–7.',svg('trachtrunks',800,610,body),
 '#1 Right tracheal trunk · #2 Left tracheal trunk · #3 Thoracic duct · #4 Trachea · #5 Right external jugular vein · #6 Right common carotid artery · #7 Medial retropharyngeal lymph node',
 'Tracheal trunks drain the medial retropharyngeal lymph nodes, run beside the carotids; right → right external jugular / brachiocephalic vein area; left → thoracic duct (or left external jugular)',
 [('⚠️ Left vs right','The left one joins the THORACIC DUCT; the right one empties straight into a vein')])
# ---------- Lab 17 · bronchial tree (lab guide Fig 3-13): principal / lobar / segmental
d=pymupdf.open(L17); p=d[7]; R=pymupdf.Rect(100,60,500,350); M=pymupdf.Matrix(3,3)
WANT={'RPB':'Right principal bronchus','LPB':'Left principal bronchus','RB1':'Right cranial lobar bronchus','RB2':'Middle lobar bronchus','RB3':'Accessory lobar bronchus','RB4':'Right caudal lobar bronchus','LB1':'Left cranial lobar bronchus','LB2':'Left caudal lobar bronchus','RB4D1':'Segmental bronchus (of the right caudal lobe)','LB1V2':'Segmental bronchus (of the left cranial lobe)'}
pos={}
for w in p.get_text('words'):
    r=pymupdf.Rect(w[:4])
    if r.intersects(R):
        if w[4] in WANT and w[4] not in pos: pos[w[4]]=r
        p.add_redact_annot(r+(-1,-1,1,1),fill=(1,1,1))
p.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE,graphics=pymupdf.PDF_REDACT_LINE_ART_NONE)
q=p.get_pixmap(matrix=M,clip=R); Q=Image.frombytes('RGB',(q.w,q.h),q.samples); dr=ImageDraw.Draw(Q)
F=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',30); order=list(WANT); ans=[]
for i,k in enumerate(order,1):
    r=pos[k]; cx,cy=((r.x0+r.x1)/2-R.x0)*3,((r.y0+r.y1)/2-R.y0)*3
    dr.ellipse([cx-24,cy-24,cx+24,cy+24],fill=(224,95,168),outline='white',width=4); dr.text((cx,cy),str(i),font=F,fill='white',anchor='mm'); ans.append(f'#{i} {WANT[k]}')
Q.save('assets/p3draw_bronchtree.jpg',quality=92)
card(17,['segmental bronchi','lobar bronchi','principal bronchi'],'Bronchial tree, dorsal view (lab guide Fig 3-13). Name 1–10.','assets/p3draw_bronchtree.jpg?v={V}',' · '.join(ans),
 'Trachea → principal bronchus (1 per lung) → lobar bronchus (1 per lobe: right 4, left 2) → segmental bronchi (the small branches inside each lobe)',
 [('🧠 Hook','Right = 4 lobar (cranial, middle, accessory, caudal) · Left = 2 (cranial, caudal)')],'📖 lab guide Fig 3-13 · Lab 17 (labels → badges)')
# ---------- Lab 18 · spinal cord / neuron schematic
body=(f'<circle cx="250" cy="250" r="120" fill="#f4eef8" stroke="#a48bb8" stroke-width="4"/>'
 f'<path d="M190 175 L230 230 L210 330 M310 175 L270 230 L290 330 M230 250 L270 250" stroke="#b07fbf" stroke-width="26" fill="none" stroke-linecap="round"/>'
 f'<path d="M300 185 C380 150 430 150 470 200" stroke="{N}" stroke-width="8" fill="none"/><ellipse cx="420" cy="165" rx="30" ry="20" fill="#f7dd84" stroke="{N}" stroke-width="3"/>'
 f'<path d="M300 315 C380 350 430 340 470 290" stroke="{N}" stroke-width="8" fill="none"/>'
 f'<path d="M470 200 L470 290" stroke="{N}" stroke-width="12"/><path d="M470 245 L760 245" stroke="{N}" stroke-width="10"/>'
 f'<rect x="720" y="210" width="60" height="70" rx="10" fill="#f3b2a6" stroke="#c46a5a" stroke-width="3"/>'
 f'<circle cx="300" cy="300" r="9" fill="#5d347e"/><path d="M300 300 C360 380 430 420 520 430" stroke="#5d347e" stroke-width="4" fill="none"/>'
 f'<ellipse cx="540" cy="430" rx="26" ry="18" fill="#d8c3ec" stroke="#5d347e" stroke-width="3"/><circle cx="540" cy="430" r="7" fill="#e05fa8"/>'
 f'<path d="M560 432 C620 440 660 470 700 480" stroke="#e05fa8" stroke-width="4" fill="none" stroke-dasharray="9 5"/><ellipse cx="740" cy="490" rx="42" ry="26" fill="#f7cfa0" stroke="#c48a4a" stroke-width="3"/>'
 +b(360,140,1,370,165)+b(420,120,2,420,145)+b(360,368,3,370,335)+b(600,190,4,560,245)+b(750,180,5)+b(250,400,6,300,360)+b(540,380,7,540,412)+b(660,500,8,650,465)+b(210,215,9)+b(120,110,10,165,165)+b(620,300,11,560,245)
 +t(20,585,'Transverse spinal cord · yellow = spinal nerve parts · purple/pink = autonomic 2-neuron chain',15))
card(18,['ganglion','=ganglion','nucleus','=nucleus','ventral root','dorsal root','sensory (afferent) axons','motor (efferent) axons','somatic efferent neurons','visceral efferent neurons','preganglionic neuron','postganglionic neuron','prevertebral (collateral) ganglia','central nervous system','peripheral nervous system'],
 'Spinal cord + nerve schematic. Name 1–11.',svg('spinal',800,600,body),
 '#1 Dorsal root (sensory / afferent axons) · #2 Ganglion (dorsal root ganglion = cell bodies OUTSIDE the CNS) · #3 Ventral root (motor / efferent axons) · #4 Spinal nerve → peripheral nervous system · #5 Skeletal muscle ← somatic efferent neuron · #6 Preganglionic neuron (cell body in the CNS) · Visceral efferent neurons = #6 + #8 · #7 Prevertebral (collateral) ganglia · #8 Postganglionic neuron → smooth muscle / gland (gut) · #9 Nucleus (cell bodies INSIDE the CNS = gray matter) · #10 Central nervous system (spinal cord) · #11 Motor (efferent) axons in the spinal nerve',
 'Neuron = cell body + axon. Nucleus = cluster of cell bodies inside the CNS; ganglion = cluster outside it. Afferent = toward the CNS (sensory, dorsal root); efferent = away (motor, ventral root)',
 [('⚠️ Somatic vs visceral efferent','Somatic = 1 neuron to skeletal muscle · visceral (autonomic) = 2 neurons: preganglionic → ganglion → postganglionic')])
# ---------- Lab 18 · ANS divisions
body=(f'<ellipse cx="120" cy="170" rx="85" ry="65" fill="#e9dcf3" stroke="{PER}" stroke-width="4"/>'
 f'<path d="M200 185 L760 185" stroke="#b9a3c9" stroke-width="30" stroke-linecap="round"/>'
 f'<rect x="300" y="168" width="290" height="34" fill="#f5b3cc"/><rect x="640" y="168" width="110" height="34" fill="#a8d7c0"/>'
 +''.join(f'<path d="M{x} 145 L{x} 60" stroke="#2f9e6e" stroke-width="4"/>' for x in (95,120,145,170))+
 ''.join(f'<path d="M{x} 205 L{x} 300" stroke="#d4537e" stroke-width="4"/>' for x in range(320,590,40))+
 ''.join(f'<path d="M{x} 205 L{x} 300" stroke="#2f9e6e" stroke-width="4"/>' for x in (665,705,735))+
 t(445,380,'C8/T1 … L4',14,'#7a6585','middle')+t(700,380,'S1–S3',14,'#7a6585','middle')+t(220,145,'cervical cord',13)
 +b(120,170,1)+b(60,60,2,95,90)+b(445,130,3,445,168)+b(700,130,4,700,168)+b(445,330,5,445,300)+b(700,330,6,700,300)+b(230,330,7)
 +t(20,410,'Lateral schematic · cranial left · pink = one division · green = the other',15)+t(20,440,'#7 = the whole autonomic system',14))
card(18,['brain','cranial nerves','sympathetic division','parasympathetic division','thoracolumbar','craniosacral','autonomic nervous system'],
 'Autonomic nervous system map. Name 1–7.',svg('ans',800,460,body),
 '#1 Brain · #2 Cranial nerves (III, VII, IX, X carry parasympathetic) · #3 Thoracolumbar outflow · #4 Sacral outflow · #5 Sympathetic division (thoracolumbar) · #6 Parasympathetic division · Craniosacral = cranial nerves + sacral · #7 Autonomic nervous system',
 'CNS = brain + spinal cord; PNS = cranial + spinal nerves and ganglia. Sympathetic = thoracolumbar; parasympathetic = craniosacral',
 [('⚠️ Flip trap','THORACOlumbar = SYMPATHETIC · CRANIOsacral = PARASYMPATHETIC'),('🔁 Prevertebral ganglia','Sympathetic ganglia on the aorta (celiac, cranial + caudal mesenteric)')])
# ---------- Lab 18 · heart wall layers
cx,cy=400,330
rings=[(300,'#efe2f6','#b9a3c9'),(280,'#fff','#7b42a0'),(240,'#f6c6d3','#d4537e'),(175,'#fff','#e05fa8'),(165,'#ffe9ee','#e05fa8')]
body=''.join(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{f}" stroke="{s}" stroke-width="5"/>' for r,f,s in rings)
import math
def pr(r,deg): return cx+r*math.cos(math.radians(deg)),cy-r*math.sin(math.radians(deg))
for n,(r,dg) in enumerate([(292,90),(280,55),(260,25),(240,-5),(208,-35),(175,-70),(0,0)],1):
    x,y=pr(r,dg); body+=b(round(x),round(y),n)
body+=t(20,680,'Wedge of heart wall, outside → in (not to scale) · #3 = the space between the two serous layers',15)
card(18,['endocardium'],'Heart wall + pericardium, outside → in. Name 1–7.',svg('heartlayers',800,700,body),
 '#1 Fibrous pericardium · #2 Parietal layer of serous pericardium · #3 Pericardial cavity · #4 Visceral layer of serous pericardium = epicardium · #5 Myocardium · #6 Endocardium · #7 Chamber (blood)',
 'Pericardium = fibrous + serous (parietal + visceral). Visceral serous pericardium IS the epicardium. Heart wall = epicardium → myocardium → endocardium',
 [('🔴 You said re-study this','Say it out loud: fibrous → parietal serous → cavity → visceral serous/epicardium → myocardium → endocardium')])
# ---------- Lab 18 · caudal laryngeal
body=(f'<path d="M110 60 L170 60 L180 140 L100 140 Z" fill="#e9e2ee" stroke="#a99bb5" stroke-width="3"/><rect x="118" y="140" width="44" height="420" rx="14" fill="#e9e2ee" stroke="#a99bb5" stroke-width="3"/>'
 f'<path d="M260 40 L260 520" stroke="{N}" stroke-width="8"/><path d="M200 470 C320 470 420 460 520 520" stroke="{A}" stroke-width="20" fill="none"/>'
 f'<path d="M330 420 L400 470" stroke="#999" stroke-width="10"/><path d="M260 430 C290 520 360 520 340 450 C330 380 190 330 175 140" stroke="{N}" stroke-width="5" fill="none"/>'
 f'<path d="M175 140 L160 105" stroke="{N}" stroke-width="5" stroke-dasharray="8 5"/>'
 +b(300,90,1,262,90)+b(230,300,2,205,300)+b(215,100,3,170,118)+b(140,90,4)+b(440,425,5,372,445)+b(470,560,6,470,505)+t(20,610,'Left side, schematic · cranial up',15))
card(18,['caudal laryngeal nerve'],'Left vagus + recurrent nerve, schematic. Name 1–6.',svg('caudlaryng',800,630,body),
 '#1 Left vagus nerve · #2 Left recurrent laryngeal nerve · #3 Caudal laryngeal nerve · #4 Larynx · #5 Ligamentum arteriosum · #6 Aortic arch',
 'The recurrent laryngeal nerve hooks around the ligamentum arteriosum (left) / subclavian (right), runs cranially beside the trachea, and ends at the larynx as the caudal laryngeal nerve','',)
# ---------- Lab 19 · forepaw metacarpal vs common digital
def paw(ox,dorsal):
    s=''
    for i,x in enumerate((60,110,160,210)): s+=f'<rect x="{ox+x}" y="90" width="34" height="230" rx="16" fill="#f1ece4" stroke="#bfb3a3" stroke-width="3"/><ellipse cx="{ox+x+17}" cy="365" rx="22" ry="30" fill="#f1ece4" stroke="#bfb3a3" stroke-width="3"/>'
    for x in (102,152,202):
        s+=f'<path d="M{ox+x} 110 L{ox+x} 300" stroke="{A}" stroke-width="4" stroke-dasharray="8 5"/>'
        s+=f'<path d="M{ox+x-8} 40 L{ox+x-8} 330 M{ox+x+8} 40 L{ox+x+8} 330" stroke="{A if dorsal else V}" stroke-width="6"/><path d="M{ox+x+16} 40 L{ox+x+16} 330" stroke="{N}" stroke-width="5"/>' if False else ''
        s+=f'<path d="M{ox+x} 30 L{ox+x} 70 M{ox+x} 330 L{ox+x} 345" stroke="{A}" stroke-width="7"/><path d="M{ox+x+7} 30 L{ox+x+7} 345" stroke="{N}" stroke-width="4"/>'
    return s
body=paw(0,True)+paw(400,False)+t(140,440,'DORSAL view',16,'#5d347e','middle')+t(540,440,'PALMAR view',16,'#5d347e','middle')
body+=b(152,22,1,152,40)+b(102,205,2,85,205)+b(552,22,3,552,40)+b(502,205,4,485,205)+t(20,480,'Solid = superficial, between the digits · dashed = deep, in the grooves between metacarpal bones',14)
card(19,['dorsal metacarpal vessels/nerves','palmar metacarpal vessels/nerves','dorsal common digital vessels/nerves','palmar common digital vessels/nerves'],
 'Forepaw, dorsal (left) + palmar (right). Name 1–4.',svg('paw',800,500,body),
 '#1 Dorsal common digital vessels/nerves · #2 Dorsal metacarpal vessels/nerves · #3 Palmar common digital vessels/nerves · #4 Palmar metacarpal vessels/nerves',
 'Common digital = superficial, run toward the spaces between the digits. Metacarpal = deep, lie in the grooves between the metacarpal bones. Dorsal common digital come from the cranial superficial antebrachial artery + superficial radial nerve; palmar from the superficial palmar arch + median/ulnar nerves','',)
# ---------- Lab 19 · cranial vs caudal pectoral nerves
body=(''.join(f'<path d="M80 {y} L330 {y+40}" stroke="{N}" stroke-width="8"/>'+t(30,y+6,l,15) for y,l in ((80,'C6'),(140,'C7'),(200,'C8'),(260,'T1')))+
 f'<ellipse cx="340" cy="210" rx="40" ry="110" fill="#f7dd84" opacity=".55"/>'
 f'<path d="M360 140 C450 110 520 100 600 110" stroke="{N}" stroke-width="5" fill="none"/><path d="M360 280 C450 320 520 360 600 380" stroke="{N}" stroke-width="5" fill="none"/>'
 f'<rect x="600" y="70" width="170" height="80" rx="16" fill="#f3b2a6" stroke="#c46a5a" stroke-width="3"/><rect x="600" y="330" width="170" height="110" rx="16" fill="#e98f84" stroke="#b7564b" stroke-width="3"/>'
 +b(480,90,1,480,112)+b(480,370,2,480,338)+b(685,110,3)+b(685,385,4)+b(340,210,5)+t(20,490,'Brachial plexus schematic (right side) · roots left → muscles right',15))
card(19,['caudal pectoral nerves','cranial pectoral nerves'],'Brachial plexus → pectoral muscles. Name 1–5.',svg('pectoral',800,510,body),
 '#1 Cranial pectoral nerves · #2 Caudal pectoral nerves · #3 Superficial pectoral muscle · #4 Deep pectoral muscle · #5 Brachial plexus',
 'Cranial pectoral nerves (C6–C8) → superficial pectoral muscles · caudal pectoral nerves (C8, T1) → deep pectoral muscle','',
 )
# ---------- Lab 19 · cutaneous area vs autonomous zone (course slide)
d2=pymupdf.open(FL); pg=d2[113]; pm=pg.get_pixmap(matrix=pymupdf.Matrix(2,2),clip=pymupdf.Rect(312,134,960,458)); pm.save('assets/p3draw_autozone.jpg')
card(19,['cutaneous area','autonomous zone'],'Course slide: what does the shaded skin area show, and for which nerve?','assets/p3draw_autozone.jpg?v={V}',
 'Autonomous zone of the axillary nerve',
 'Cutaneous area = ALL the skin a nerve supplies (overlaps neighbors). Autonomous zone = the part supplied ONLY by that nerve, so testing it checks that one nerve',
 [('⚠️ Pair','cutaneous area (big, overlapping) vs autonomous zone (small, exclusive)')],'📚 course slide · Lab 20/21 forelimb slides #114')
# ---------- Lab 21 · abdominal wall nerves (Fig 4-3 schematic), lateral view, cranial LEFT
body=(f'<rect x="60" y="70" width="680" height="420" rx="30" fill="#f6eadf" stroke="#d8c0aa" stroke-width="3"/>'
 f'<path d="M70 60 C140 120 170 260 150 470" stroke="#bfb3a3" stroke-width="22" fill="none" stroke-linecap="round"/>'
 +''.join(f'<path d="M{x} 70 L{x+120} 480" stroke="{N}" stroke-width="7"/>' for x in (190,300,410,520))+
 f'<path d="M640 70 L700 300" stroke="{N}" stroke-width="7"/><path d="M700 300 L740 480" stroke="{N}" stroke-width="7" stroke-dasharray="10 6"/>'
 f'<path d="M318 70 L438 480" stroke="{A}" stroke-width="5"/><path d="M660 70 L720 300" stroke="{A}" stroke-width="5"/><circle cx="700" cy="300" r="14" fill="#fff" stroke="#999" stroke-width="4"/>'
 f'<path d="M560 520 L590 600" stroke="{N}" stroke-width="6"/><path d="M574 520 L604 600" stroke="{V}" stroke-width="7"/><ellipse cx="590" cy="525" rx="40" ry="14" fill="none" stroke="#999" stroke-width="3" stroke-dasharray="6 4"/>'
 +b(205,140,1,232,160)+b(330,140,2,340,160)+b(440,140,3,452,160)+b(550,140,4,562,160)+b(690,140,5,664,160)+b(540,600,6,578,585)+b(385,330,7,388,300)+b(770,250,8,690,220)+b(100,330,9,145,330)+b(720,330,10)
 +t(20,640,'Lateral abdominal wall on the transversus abdominis · cranial LEFT · yellow = nerves · red = arteries',14)+t(20,662,'Dashed ellipse = superficial inguinal ring · grey circle = tuber coxae',14))
card(21,['cranial iliohypogastric nerve','caudal iliohypogastric nerve','ilioinguinal nerve','genitofemoral nerve','lateral cutaneous femoral nerve','cutaneous nerves'],
 'Abdominal wall nerves (after lab guide Fig 4-3). Name 1–10.',svg('abdnerves',800,680,body),
 '#1 Costoabdominal nerve (T13) · #2 Cranial iliohypogastric nerve (L1) · #3 Caudal iliohypogastric nerve (L2) · #4 Ilioinguinal nerve (L3) · #5 Lateral cutaneous femoral nerve (L4) · #6 Genitofemoral nerve (with the external pudendal vein) · #7 Cranial abdominal artery (largest branch runs with L1) · #8 Deep circumflex iliac artery (runs with L4) · #9 13th rib · #10 Tuber coxae',
 'They run parallel and caudoventrally on the transversus abdominis, deep to the internal abdominal oblique. TA review: "T13, L1, L2, L3, L4 … make sure you know the names"',
 [('🧠 Hook','Cranial, Caudal, Ilio, Lateral = L1 → L4 (T13 = costoabdominal, behind the 13th rib)'),('⚠️ Genitofemoral','NOT on the transversus: runs through the inguinal canal stuck to the external pudendal vein')])
# ---------- Lab 22 · peritoneum
body=(f'<ellipse cx="400" cy="300" rx="350" ry="250" fill="#efe6f5" stroke="#b9a3c9" stroke-width="16"/><ellipse cx="400" cy="300" rx="330" ry="230" fill="#fff" stroke="{PER}" stroke-width="5"/>'
 f'<circle cx="400" cy="85" r="34" fill="#ddd" stroke="#aaa" stroke-width="3"/><ellipse cx="250" cy="120" rx="50" ry="30" fill="#d9a0a0" stroke="#b06a6a" stroke-width="3"/><path d="M200 140 C230 150 270 150 300 140" stroke="{PER}" stroke-width="5" fill="none"/>'
 f'<path d="M390 118 L385 300 M410 118 L415 300" stroke="#d4537e" stroke-width="4"/><circle cx="400" cy="350" r="62" fill="{ORG}" stroke="#d4537e" stroke-width="5"/>'
 +b(600,420,1,560,430)+b(560,200,2)+b(720,300,3,728,300)+b(470,390,4,452,375)+b(450,220,5,412,220)+b(250,120,6)+t(20,580,'Transverse section of the abdomen · dorsal up · purple = lining the wall · pink = on the organ',15))
card(22,['peritoneal cavity','connecting peritoneum','parietal peritoneum','visceral peritoneum','abdominal cavity'],'Abdomen, transverse section. Name 1–6.',svg('peritoneum',800,600,body),
 '#1 Abdominal cavity (everything inside the wall) · #2 Peritoneal cavity (space between peritoneal layers) · #3 Parietal peritoneum · #4 Visceral peritoneum · #5 Connecting peritoneum (mesentery: double fold) · #6 Kidney = retroperitoneal',
 'Parietal lines the wall, visceral covers organs, connecting peritoneum (mesenteries, omenta, ligaments) joins them. Peritoneal cavity = potential space inside the peritoneum; abdominal cavity = the whole space inside the wall',
 [('⚠️ Pair','abdominal cavity (big) ≠ peritoneal cavity (inside the peritoneal sac only)')])
# ---------- Lab 22 · empty vs full stomach
def sil(ox,full):
    s=f'<path d="M{ox+20} 120 C{ox+80} 60 {ox+300} 50 {ox+360} 110 L{ox+360} 330 C{ox+300} 380 {ox+80} 380 {ox+20} 330 Z" fill="#f6eadf" stroke="#d8c0aa" stroke-width="3"/>'
    s+=f'<path d="M{ox+90} 70 C{ox+150} 160 {ox+190} 260 {ox+170} 370" stroke="#bfb3a3" stroke-width="12" fill="none"/>'
    s+=(f'<path d="M{ox+60} 140 C{ox+120} 110 {ox+150} 150 {ox+140} 210 C{ox+120} 260 {ox+70} 250 {ox+55} 200 Z" fill="#f2b6c4" stroke="#c46a83" stroke-width="3"/>' if not full else
        f'<path d="M{ox+55} 130 C{ox+160} 90 {ox+290} 150 {ox+290} 260 C{ox+280} 350 {ox+120} 365 {ox+60} 300 Z" fill="#f2b6c4" stroke="#c46a83" stroke-width="3"/>')
    return s
body=sil(20,False)+sil(420,True)+t(200,420,'A',20,'#5d347e','middle')+t(600,420,'B',20,'#5d347e','middle')
body+=b(100,190,1)+b(640,250,2)+b(196,330,3,186,330)+t(20,460,'Left lateral view · cranial LEFT · grey arc = costal arch',15)
card(22,['empty stomach','full stomach'],'Left lateral view: stomach A vs B. Name 1–3.',svg('stomach',800,480,body),
 '#1 Empty stomach (A) · #2 Full stomach (B) · #3 Costal arch',
 'Empty stomach sits cranial to / within the costal arch, against the liver. Full stomach pushes caudally past the costal arch and contacts the ventral abdominal wall','',)
# ---------- Lab 22 · pancreatic ducts
body=(f'<path d="M300 40 C300 200 300 380 330 520" stroke="#e7b9a0" stroke-width="80" fill="none" stroke-linecap="round"/>'
 f'<path d="M420 120 C520 200 560 330 520 460 L460 480 C480 360 450 250 390 180 Z" fill="#f7d9a8" stroke="#c9a46a" stroke-width="3"/>'
 f'<path d="M120 60 C200 120 260 160 330 175" stroke="#3a9b5c" stroke-width="7" fill="none"/><path d="M440 200 C400 190 360 185 335 180" stroke="#c48a2a" stroke-width="6" fill="none"/>'
 f'<path d="M470 330 C420 320 380 315 345 318" stroke="#c48a2a" stroke-width="6" fill="none"/><circle cx="330" cy="178" r="10" fill="#5d347e"/><circle cx="342" cy="318" r="9" fill="#5d347e"/>'
 +b(170,70,1,190,105)+b(420,150,2,400,190)+b(240,200,3,320,180)+b(460,280,4,420,322)+b(240,340,5,332,320)+b(520,410,6)+b(300,470,7)+t(20,580,'Ventral view of the descending duodenum (cranial up) · green = bile · orange = pancreatic',15))
card(22,['accessory pancreatic duct','pancreatic duct','major duodenal papilla','minor duodenal papilla'],'Duodenum + pancreatic ducts (after lab guide Fig 4-13). Name 1–7.',svg('pancducts',800,600,body),
 '#1 Bile duct · #2 Pancreatic duct · #3 Major duodenal papilla · #4 Accessory pancreatic duct · #5 Minor duodenal papilla · #6 Right lobe of the pancreas · #7 Descending duodenum',
 'Pancreatic duct opens WITH the bile duct on the major duodenal papilla; the accessory pancreatic duct opens a little more caudally on the minor duodenal papilla',
 [('🧠 Hook','Major = bile + pancreatic (2 ducts) · minor = accessory (1 duct)')])
# ---------- Lab 22 · umbilical vein (fetal)
body=(f'<path d="M80 130 C200 60 600 60 720 130 L720 300 C600 360 200 360 80 300 Z" fill="#f6eadf" stroke="#d8c0aa" stroke-width="3"/>'
 f'<path d="M120 150 C170 110 260 120 300 180 C300 250 220 290 140 280 Z" fill="#c98a7a" stroke="#9c5e50" stroke-width="3"/>'
 f'<path d="M260 230 C380 300 470 330 560 335" stroke="{V}" stroke-width="8" fill="none"/><path d="M230 200 C360 290 480 330 560 340 L560 350 C460 345 330 320 240 260 Z" fill="#d8c3ec" opacity=".7"/>'
 f'<circle cx="565" cy="345" r="16" fill="#fff" stroke="#999" stroke-width="4"/><path d="M565 360 L585 440" stroke="#bbb" stroke-width="14"/>'
 +b(420,270,1,420,305)+b(330,330,2,340,300)+b(200,130,3)+b(610,345,4,582,345)+t(20,400,'FETUS · left lateral view · cranial LEFT · lavender = falciform ligament',15))
card(22,['umbilical vein','falciform ligament','round ligament of the liver'],'Fetus, left lateral. Name 1–4.',svg('umbvein',800,420,body),
 '#1 Umbilical vein · #2 Falciform ligament · #3 Liver · #4 Umbilicus',
 'The umbilical vein runs from the umbilicus to the liver in the free border of the falciform ligament. After birth it becomes the round ligament of the liver',
 [('🔁 Fetal remnants','Umbilical vein → round ligament of the liver · ductus arteriosus → ligamentum arteriosum · foramen ovale → fossa ovalis')])
# ---------- Lab 23 · short gastric arteries
body=(f'<path d="M120 200 C120 80 330 60 420 120 C520 190 560 330 470 400 C380 460 220 430 180 360 C150 300 260 260 250 210 Z" fill="#f2b6c4" stroke="#c46a83" stroke-width="3"/>'
 f'<path d="M560 110 C640 160 680 300 650 470 C640 500 610 500 610 470 C630 320 600 200 540 140 Z" fill="#b25b7a" stroke="#86405a" stroke-width="3"/>'
 f'<path d="M760 280 L640 290" stroke="{A}" stroke-width="9"/><path d="M640 290 C620 250 600 200 575 160 M640 290 C630 340 630 400 625 450" stroke="{A}" stroke-width="6" fill="none"/>'
 +''.join(f'<path d="M{575+i*6} {160+i*18} C540 {150+i*20} 500 {140+i*24} 470 {150+i*26}" stroke="{A}" stroke-width="4" fill="none"/>' for i in range(3))+
 f'<path d="M625 450 C560 450 520 420 480 400 C420 430 300 445 220 400" stroke="{A}" stroke-width="5" fill="none"/>'
 +b(730,250,1,720,282)+b(500,95,2,505,160)+b(400,470,3,400,432)+b(630,330,4)+b(260,170,5)+t(20,560,'Ventral view of stomach + spleen · cranial up · dog\'s left on the RIGHT',15))
card(23,['short gastric arteries'],'Stomach + spleen, ventral view. Name 1–5.',svg('shortgastric',800,580,body),
 '#1 Splenic artery · #2 Short gastric arteries · #3 Left gastroepiploic artery · #4 Spleen · #5 Stomach (fundus/body)',
 'Short gastric arteries leave the splenic branches at the cranial (dorsal) end of the spleen and run in the gastrosplenic ligament to the fundus / greater curvature. The splenic artery continues as the left gastroepiploic along the greater curvature',
 [('🔁 Celiac','Celiac → hepatic, left gastric, splenic (→ short gastrics + left gastroepiploic)')])

# ---------- Lab 16 · ligaments of vertebral column (lab guide Fig 2-85/2-86) + dorsal atlantoaxial ligament schematic
L16=sys.argv[3] if len(sys.argv)>3 else None
if L16:
    doc=pymupdf.open(L16); p=doc[3]; R=pymupdf.Rect(55,395,580,600); lines=[]
    for bl in p.get_text('dict')['blocks']:
        for l in bl.get('lines',[]):
            tx=' '.join(s_['text'] for s_ in l['spans']).strip(); r=pymupdf.Rect(l['bbox'])
            if tx and r.intersects(R): lines.append([r,re.sub(r'\s+',' ',tx)])
    lines.sort(key=lambda x:(x[0].y0,x[0].x0)); blocks=[]
    for r,tx in lines:
        pr=next((b_ for b_ in reversed(blocks) if 0<=r.y0-b_[0].y1<4 and abs(r.x0-b_[0].x0)<40),None)
        if pr and (tx[:1].islower() or re.search(r'\b(of|the)$',pr[1])): pr[0]|=r; pr[1]+=' '+tx
        else: blocks.append([r,tx])
    for w in p.get_text('words'):
        if pymupdf.Rect(w[:4]).intersects(R): p.add_redact_annot(pymupdf.Rect(w[:4])+(-1,-1,1,1),fill=False)
    p.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE,graphics=pymupdf.PDF_REDACT_LINE_ART_NONE,text=pymupdf.PDF_REDACT_TEXT_REMOVE)
    q=p.get_pixmap(matrix=pymupdf.Matrix(3,3),clip=R); Q=Image.frombytes('RGB',(q.w,q.h),q.samples); dr=ImageDraw.Draw(Q); ans=[]
    W16={'yellow':'Yellow ligament','intercapital':'Intercapital ligament','nucleus':'Nucleus pulposus','intervertebral':'Intervertebral disc','ventral longitudinal':'Ventral longitudinal ligament','dorsal longitudinal':'Dorsal longitudinal ligament'}
    for r,tx in blocks:
        for part in re.split(r'(?<=disc) (?=Intercapital)',tx):
            k=next((v for k2,v in W16.items() if k2 in part.lower()),None)
            if not k: continue
            cx,cy=((r.x0+r.x1)/2-R.x0)*3,((r.y0+r.y1)/2-R.y0)*3
            if part!=tx: cy+= -14 if 'disc' in part.lower() else 14
            ans.append(f'#{len(ans)+1} {k}'); dr.ellipse([cx-24,cy-24,cx+24,cy+24],fill=(224,95,168),outline='white',width=4); dr.text((cx,cy),str(len(ans)),font=F,fill='white',anchor='mm')
    Q.save('assets/p3draw_l16ligs.jpg',quality=92)
    card(16,['yellow ligament','intercapital ligament','nucleus pulposus','intervertebral disc','ventral longitudinal ligament','dorsal longitudinal ligament'],'Ligaments of the vertebral column + ribs: ventral view (left), dorsal view with arches removed (right). Name each number.','assets/p3draw_l16ligs.jpg?v={V}',' · '.join(ans),
     'Intercapital ligament: joins the two rib heads across the floor of the vertebral canal (T2–T10), dorsal to the disc. Yellow ligament: between the arches of neighboring vertebrae. Nucleus pulposus = soft center of the disc, annulus fibrosus = outer ring',[],'📖 lab guide Fig 2-85 + 2-86 · Lab 16 (labels → badges)')
    body=(f'<path d="M80 250 C80 180 160 150 230 160 L300 175 L300 330 L230 340 C160 350 80 320 80 250 Z" fill="#f1ece4" stroke="#bfb3a3" stroke-width="4"/>'
     f'<path d="M300 200 L420 190 L430 300 L300 310 Z" fill="#f1ece4" stroke="#bfb3a3" stroke-width="4"/><path d="M430 210 L650 200 C690 200 700 230 690 260 L680 320 L430 330 Z" fill="#f1ece4" stroke="#bfb3a3" stroke-width="4"/>'
     f'<path d="M470 205 C520 120 640 90 700 110 C690 160 650 190 600 205 Z" fill="#f1ece4" stroke="#bfb3a3" stroke-width="4"/>'
     f'<path d="M330 195 C380 150 450 140 500 165" stroke="#e05fa8" stroke-width="10" fill="none"/><path d="M300 330 L430 330" stroke="#7b42a0" stroke-width="8"/>'
     +b(400,120,1,405,165)+b(150,250,2)+b(365,255,3)+b(560,265,4)+b(640,140,5)+t(20,420,'Atlas + axis, left lateral schematic · cranial LEFT · skull not shown',15))
    card(16,['dorsal atlantoaxial ligament'],'Atlas + axis, lateral schematic. Name 1–5.',svg('atlantoaxial',800,440,body),
     '#1 Dorsal atlantoaxial ligament · #2 Atlas (C1) · #3 Atlantoaxial joint · #4 Axis (C2) · #5 Spinous process of the axis',
     'Dorsal atlantoaxial ligament: dorsal arch of the atlas → cranial end of the spinous process of the axis (dorsal to the atlantoaxial joint)',[('🔁 Others here','Transverse ligament of the atlas holds the dens to the atlas floor; apical + alar ligaments join the dens to the skull')])
json.dump(C,open('tools/p3draw_cards.json','w'))
print({k:len(v) for k,v in C.items()})
