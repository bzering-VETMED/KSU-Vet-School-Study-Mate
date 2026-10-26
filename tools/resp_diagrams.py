# Build: Exam 3 · 📈 Key diagrams page (8 clean, labeled SVG diagrams; pink = what changed from normal)
# Run from repo root AFTER tools/resp_terms.py (reuses its CSS). Tile added in resp_terms.py.
import re,time,html,math
E=html.escape; V=str(int(time.time()))
E3='systems-lec-exam3.html'; FN='systems-lec3-diagrams.html'
css=re.search(r'<style>(.*?)</style>',open('systems-lec3-pp3-terms.html').read(),re.S).group(1)
css+=('.dg{background:#fff;border:1px solid var(--line);border-left:6px solid var(--g);border-radius:14px;padding:10px 12px;margin:14px 0}'
      '.dg h2{margin:0 0 2px;font-size:19px;color:var(--v)}.dg .src{font-size:13px;color:#6b4c7d;margin:0 0 6px}'
      '.dg svg{width:100%;height:auto;display:block;background:#FFFBFD;border-radius:10px}'
      '.dg ul{margin:6px 0 0;padding-left:20px}.dg li{margin:4px 0;line-height:1.4}'
      '.lg{font-size:13px;margin:4px 0 0}.lg span{display:inline-block;margin-right:10px}'
      '.toc{display:flex;flex-wrap:wrap;gap:6px;margin:12px 0}.toc a{background:#f3eafb;color:#65328c;font-weight:800;text-decoration:none;border-radius:999px;padding:6px 11px;font-size:14px}')
PU='#6A0DAD'; PK='#E0459A'; OR='#E8A317'; GR='#9A86AB'; INK='#330B4D'
FONT='font-family="-apple-system,Segoe UI,Arial,sans-serif"'

def svg(w,h,inner): return f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" {FONT} role="img">{inner}</svg>'
def t(x,y,s,size=12,fill=INK,anchor='start',w='400'): return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="{w}" stroke="#FFFBFD" stroke-width="3" paint-order="stroke">{s}</text>'
def ln(x1,y1,x2,y2,c=INK,sw=1.5,dash=''): return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{sw}"{f" stroke-dasharray=\"{dash}\"" if dash else ""}/>'
def path(pts,c,sw=3,dash=''): return f'<path d="M'+' L'.join(f'{x:.1f},{y:.1f}' for x,y in pts)+f'" fill="none" stroke="{c}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"{f" stroke-dasharray=\"{dash}\"" if dash else ""}/>'
def dot(x,y,c=PU,r=5): return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{c}" stroke="#fff" stroke-width="1.5"/>'
def axes(x0,y0,x1,y1,xl,yl):
    return (ln(x0,y0,x1,y0,INK,1.5)+ln(x0,y0,x0,y1,INK,1.5)+t((x0+x1)/2,y0+30,xl,12,INK,'middle','700')
            +f'<text x="{x0-34}" y="{(y0+y1)/2}" font-size="12" fill="{INK}" font-weight="700" text-anchor="middle" transform="rotate(-90 {x0-34} {(y0+y1)/2})">{yl}</text>')

D=[]  # (id, title, source, svg, [bullets], legend)

# 1 · Oxygen cascade
steps=[('Room air',159),('Trachea',149),('Alveoli',100),('Arterial blood',100),('Venous blood',40),('Mitochondria',3)]
X0,Y0,W,H=50,250,300,210; sx=W/len(steps); sy=lambda v:Y0-v/170*H
g=axes(X0,Y0,X0+W,Y0-H,'','PO₂ (mmHg)')
for v in (0,50,100,150): g+=ln(X0-4,sy(v),X0,sy(v))+t(X0-7,sy(v)+4,str(v),11,INK,'end')
pts=[]
for i,(n,v) in enumerate(steps):
    xa,xb=X0+i*sx,X0+(i+1)*sx; pts+=[(xa,sy(v)),(xb,sy(v))]
    lbl='~1–5' if n=='Mitochondria' else str(v)
    g+=t((xa+xb)/2,sy(v)-7,lbl,13,PU,'middle','800')
    nm=['Mito-','chondria'] if n=='Mitochondria' else n.split()
    g+=f'<text x="{(xa+xb)/2}" y="{Y0+14}" font-size="10.5" fill="{INK}" text-anchor="middle">{nm[0]}</text>'
    if len(nm)>1: g+=f'<text x="{(xa+xb)/2}" y="{Y0+26}" font-size="10.5" fill="{INK}" text-anchor="middle">{nm[1]}</text>'
    if False: g+=f'<text x="{(xa+xb)/2}" y="{Y0+26}" font-size="10.5" fill="{INK}" text-anchor="middle">{n.split()[1]}</text>'
g+=path(pts,PU,3)
g+=t(X0+sx+4,sy(149)-24,'− water vapor 47',10.5,PK,'start','700')
g+=t(X0+2*sx+5,sy(128),'− CO₂ mixing, R 0.8',10.5,PK,'start','700')
g+=t(X0+4*sx+5,sy(62),'− tissues use O₂',10.5,PK,'start','700')
D.append(('cascade','1 · The oxygen cascade','Deck 3 slide 4 · deck 5 slide 4 · ⭐ "explain why alveolar PO₂ is lower than atmospheric"',svg(370,290,g),
 ['<b>159 → 149:</b> air is humidified in the airways. Water vapor (47 mmHg) takes up space: (760 − 47) × 0.21 = 149. ⭐ <i>(your miss: this is water vapor, not CO₂)</i>',
  '<b>149 → 100:</b> fresh air mixes with alveolar CO₂, and you take up more O₂ than you give back CO₂ (R = 0.8). Alveolar gas equation: 149 − 40/0.8 ≈ 100.',
  '<b>100 → 100:</b> healthy lung = arterial matches alveolar. A gap here = disease (alveolar–arterial difference).',
  '<b>100 → 40:</b> tissues pull O₂ off. Mitochondria run at only ~1–5 mmHg.'],''))

# 2 · Equilibration time
X0,Y0,W,H=55,240,290,190; sx=lambda s:X0+s/0.75*W; sy=lambda p:Y0-(p-30)/75*H
g=axes(X0,Y0,X0+W,Y0-H,'Time in capillary (s)','PO₂ in red cell (mmHg)')
for s in (0,0.25,0.5,0.75): g+=ln(sx(s),Y0,sx(s),Y0+4)+t(sx(s),Y0+15,str(s),11,INK,'middle')
for p in (40,70,100): g+=ln(X0-4,sy(p),X0,sy(p))+t(X0-7,sy(p)+4,str(p),11,INK,'end')
g+=ln(X0,sy(100),X0+W,sy(100),GR,1,'4 4')+t(X0+W,sy(100)-5,'alveolar PO₂ 100',10.5,GR,'end')
cur=lambda k,top=100: [(sx(s),sy(40+(top-40)*(1-math.exp(-k*s)))) for s in [i/100*0.75 for i in range(101)]]
g+=path(cur(16),PU,3)+path(cur(4.2),PK,3)+path(cur(3,80),PK,3,'7 5')
g+=f'<rect x="{X0}" y="{Y0-H}" width="{sx(0.28)-X0:.1f}" height="{H}" fill="{OR}" opacity=".10"/>'
g+=ln(sx(0.28),Y0,sx(0.28),Y0-H,OR,2.5,'6 4')+t(sx(0.28)+4,Y0-8,'Exercise: only 0.28 s',11,OR,'start','800')
g+=t(sx(0.07),sy(100)-8,'Normal: full by ~0.25 s',11,PU,'start','800')
g+=t(sx(0.55),sy(87),'Thick barrier',11,PK,'middle','800')
g+=t(sx(0.55),sy(64),'Grossly abnormal',11,PK,'middle','800')
g+=dot(sx(0.28),sy(40+60*(1-math.exp(-4.2*0.28))),PK,6)
D.append(('equil','2 · O₂ equilibration time in the capillary','Deck 3 slide 18 · notes 3 · ⭐ thick barrier + exercise',svg(370,280,g),
 ['<b>Normal:</b> red cell reaches alveolar PO₂ by ~0.25 s, with lots of spare time.',
  '<b>Thick barrier</b> (fibrosis, alveolar proteinosis): slower climb, but still gets there at rest.',
  '<b>What changes in exercise:</b> transit time drops to ~0.28 s (orange). The thick-barrier cell gets cut off at the pink dot → <b>hypoxemia only on exercise</b> ("Fluffy won\'t run").',
  '🟠 <b>Source conflict:</b> resting transit time = <b>0.84 s</b> (deck 2 slide 7 / deck 3 slide 22 calculation) vs <b>~0.75 s</b> (notes 3 text + this figure). Know both; show the calculation if asked.'],
 f'<span style="color:{PU}">━ normal</span><span style="color:{PK}">━ thick barrier</span><span style="color:{PK}">┅ grossly abnormal</span><span style="color:{OR}">┆ exercise</span>'))

# 3 · Compliance curves
X0,Y0,W,H=55,240,290,190; sx=lambda p:X0+(-p)/30*W; sy=lambda v:Y0-v/3*H
g=axes(X0,Y0,X0+W,Y0-H,'Pleural pressure (cm H₂O) — more negative →','Lung volume (L)')
for p in (0,-10,-20,-30): g+=ln(sx(p),Y0,sx(p),Y0+4)+t(sx(p),Y0+15,str(p),11,INK,'middle')
for v in (1,2,3): g+=ln(X0-4,sy(v),X0,sy(v))+t(X0-7,sy(v)+4,str(v),11,INK,'end')
cv=lambda vmax,k:[(sx(-p),sy(vmax*(1-math.exp(-k*p)))) for p in [i*0.3 for i in range(101)]]
g+=path(cv(3.0,0.33),PK,3,'7 5')+path(cv(2.6,0.11),PU,3)+path(cv(1.4,0.06),PK,3)
g+=t(sx(-8),sy(3)-8,'Emphysema · baggy: ↑ compliance',11.5,PK,'start','800')
g+=t(sx(-22),sy(2.05),'Healthy',12,PU,'start','800')
g+=t(sx(-17),sy(0.62),'Fibrosis',12,PK,'start','800')+t(sx(-17),sy(0.45),'stiff: ↓ compliance',10.5,PK)
D.append(('compliance','3 · Compliance curves: healthy vs emphysema vs fibrosis','Deck 6 slide 16 · notes 6 (his hardest lecture)',svg(370,280,g),
 ['<b>Compliance = slope</b> = change in volume ÷ change in pressure. Steeper = stretchier.',
  '<b>Emphysema (steeper):</b> holes in the elastic weave → too stretchy, weak recoil → air won\'t come OUT (obstructive).',
  '<b>Fibrosis (flatter):</b> scar tissue → stiff, strong recoil → air won\'t go IN (restrictive).',
  '<b>Trap:</b> emphysema = INCREASED compliance (sounds "good," isn\'t). Fibrosis = DECREASED compliance.'],
 f'<span style="color:{PU}">━ healthy</span><span style="color:{PK}">┅ emphysema</span><span style="color:{PK}">━ fibrosis</span>'))

# 4 · PVR vs lung volume
X0,Y0,W,H=55,235,290,185; sx=lambda v:X0+(v-50)/160*W; sy=lambda r:Y0-(r-60)/70*H
g=axes(X0,Y0,X0+W,Y0-H,'Lung volume','Pulmonary vascular resistance')
pts=[(sx(v),sy(65+0.0012*(v-105)**2*3.6 if v<105 else 65+0.0016*(v-105)**2*1.85)) for v in range(55,206,3)]
g+=path(pts,PU,3)
for lbl,v in (('RV',58),('FRC',105),('TLC',200)): g+=ln(sx(v),Y0,sx(v),Y0+4)+t(sx(v),Y0+15,lbl,11.5,INK,'middle','800')
g+=dot(sx(105),sy(65),PU,7)+t(sx(105),sy(65)-12,'lowest at FRC',11,PU,'middle','800')
g+=t(sx(60),sy(124),'Low volume:',11,PK,'start','800')+t(sx(60),sy(117),'extra-alveolar',10.5,PK)+t(sx(60),sy(110),'vessels narrow',10.5,PK)
g+=t(sx(205),sy(124),'High volume:',11,PK,'end','800')+t(sx(205),sy(117),'capillaries in alveolar',10.5,PK,'end')+t(sx(205),sy(110),'walls stretched thin',10.5,PK,'end')
D.append(('pvr','4 · Pulmonary vascular resistance vs lung volume (J/U-curve)','Deck 4 slide 12 · Quiz 9 Q20',svg(370,275,g),
 ['<b>Bottom of the curve = FRC</b> (normal resting volume): resistance is lowest.',
  '<b>Low volume (toward RV):</b> the lung isn\'t pulling on the big extra-alveolar vessels (less radial traction) → they narrow → resistance up.',
  '<b>High volume (toward TLC):</b> the capillaries in the alveolar walls get stretched and squeezed → resistance up.',
  '⭐ <b>Why animals don\'t breathe near TLC:</b> stiff lung (more work) + high vascular resistance → strain on the right heart.'],''))

# 5 · Regional V/Q
X0,Y0,W,H=55,235,250,185; sx=lambda r:X0+(r-5)/-4*W  # rib 5 (bottom) → 1 (top)
sy=lambda f:Y0-f/0.16*H
g=axes(X0,Y0,X0+W,Y0-H,'Base  ←  position in lung  →  Apex','Flow (per lung volume)')
bf=[(sx(r),sy(0.15-0.033*(5-r)-0.0035*(5-r)**2*0)) for r in [5-i*0.1 for i in range(41)]]
bf=[(sx(5-i*0.1),sy(max(0.01,0.145-0.033*i*0.1))) for i in range(41)]
ve=[(sx(5-i*0.1),sy(0.095-0.012*i*0.1)) for i in range(41)]
g+=path(bf,PK,3)+path(ve,PU,3)
g+=t(sx(4.85),sy(0.15)-4,'Blood flow',11.5,PK,'start','800')+t(sx(4.85),sy(0.098)-6,'Ventilation',11.5,PU,'start','800')
# V/Q column
g+=t(345,40,'V/Q',12,INK,'middle','800')
for lbl,val,y,c in (('Apex','~3.3',75,PK),('Middle','~1',140,INK),('Base','~0.6',205,PU)):
    g+=t(345,y,lbl,11,INK,'middle','700')+t(345,y+16,val,13,c,'middle','800')
g+=t(345,y+34,'PO₂ apex 132',9.5,PK,'middle','700')+t(345,y+46,'base 89',9.5,PU,'middle','700')
D.append(('vq','5 · Regional ventilation and blood flow (apex vs base)','Deck 4 slides 27–29 · deck 2 slides 22–24 · notes 4',svg(380,275,g),
 ['<b>Both</b> ventilation and blood flow are highest at the <b>BASE</b> (gravity). ⭐ <i>your miss: base gets the most ventilation</i>.',
  '<b>But blood flow falls off faster</b> going up than ventilation does.',
  '<b>So the ratio is HIGHEST at the APEX</b> → more air than blood → higher PO₂ at the apex (132 vs 89). Tuberculosis likes the apex.',
  '<b>Trap:</b> "most ventilation" = base · "highest ratio / highest PO₂" = apex. Don\'t flip them.',
  '<i>Ratio values (~3.3 / ~0.6) are read off the slide graph, not numbers he stressed.</i>'],''))

# 6 · O2 dissociation curve
X0,Y0,W,H=55,240,290,195; sx=lambda p:X0+p/110*W; sy=lambda s:Y0-s/100*H
sat=lambda p,p50=27,n=2.7:100*p**n/(p**n+p50**n)
g=axes(X0,Y0,X0+W,Y0-H,'PO₂ (mmHg)','Hemoglobin saturation (%)')
for p in (0,20,40,60,80,100): g+=ln(sx(p),Y0,sx(p),Y0+4)+t(sx(p),Y0+15,str(p),11,INK,'middle')
for s in (25,50,75,100): g+=ln(X0-4,sy(s),X0,sy(s))+t(X0-7,sy(s)+4,str(s),11,INK,'end')
g+=path([(sx(p),sy(sat(p,20))) for p in range(0,111)],PU,2,'5 4')+path([(sx(p),sy(sat(p,36))) for p in range(0,111)],PK,2,'5 4')
g+=path([(sx(p),sy(sat(p))) for p in range(0,111)],INK,3.2)
g+=ln(X0,sy(50),sx(27),sy(50),GR,1,'3 3')+ln(sx(27),sy(50),sx(27),Y0,GR,1,'3 3')
for n,p,s,c,dx,dy in ((1,100,97,PU,-6,-10),(2,40,75,PU,-14,-6),(3,27,50,INK,-14,-6),(4,88,95,PK,4,18),(5,20,sat(20,36),PK,10,8)):
    g+=dot(sx(p),sy(s),c,6)+t(sx(p)+dx,sy(s)+dy,str(n),13,c,'middle','900')
g+=t(sx(52),sy(18),'← left shift (holds on)',10.5,PU,'start','700')+t(sx(66),sy(9),'right shift (lets go) →',10.5,PK,'start','700')
D.append(('odc','6 · O₂ dissociation curve (label it!)','Deck 7 slides 14, 18, 19, 21 · notes 7 · ⭐ "label the O₂ dissociation curve"',svg(370,280,g),
 ['<b>1 = arterial, rest</b> (~100 mmHg, ~97%) · <b>2 = venous, rest</b> (~40 mmHg, ~75%) · <b>3 = P50</b> (27 mmHg in humans) · <b>4 = arterial, exercise</b> (may fall a bit in greyhounds/Thoroughbreds) · <b>5 = venous, strenuous exercise</b>.',
  '<b>Flat top</b> = safety for loading in the lung. <b>Steep middle</b> = small PO₂ drop unloads lots of O₂ in tissues.',
  '<b>Right shift</b> (pink, higher P50) = ↑ temperature, ↑ H⁺ (↓ pH), ↑ PCO₂ (= <b>Bohr effect</b>), ↑ 2,3-DPG (chronic). Exercising muscle.',
  '<b>Left shift</b> (purple, lower P50) = carbon monoxide, fetal hemoglobin, myoglobin, bar-headed goose.',
  '🟠 <b>Source conflict:</b> lecture said larger animals have higher P50; notes say <b>SMALLER</b> animals are right-shifted (higher P50; rat ~40). <b>Use the notes.</b>',
  '<i>Exercise points 4 and 5 are placed by shape only; he gave no numbers for them.</i>'],
 f'<span style="color:{INK}">━ normal</span><span style="color:{PK}">┅ right shift</span><span style="color:{PU}">┅ left shift</span>'))

# 7 · CO2 vs O2 curves
X0,Y0,W,H=55,240,290,195; sx=lambda p:X0+p/100*W; sy=lambda c:Y0-c/60*H
g=axes(X0,Y0,X0+W,Y0-H,'PO₂ or PCO₂ (mmHg)','Content (mL/100 mL)')
for p in (0,20,40,60,80,100): g+=ln(sx(p),Y0,sx(p),Y0+4)+t(sx(p),Y0+15,str(p),11,INK,'middle')
for c in (10,20,30,40,50,60): g+=ln(X0-4,sy(c),X0,sy(c))+t(X0-7,sy(c)+4,str(c),11,INK,'end')
g+=path([(sx(p),sy(20*sat(p)/100)) for p in range(0,101)],PU,3)
g+=path([(sx(p),sy(15+0.55*p-0.0012*p*p)) for p in range(10,101)],PK,3)
g+=f'<rect x="{sx(40):.1f}" y="{Y0-H}" width="{sx(46)-sx(40):.1f}" height="{H}" fill="{OR}" opacity=".18"/>'
g+=t(sx(43),Y0-H-4,'40–46',10.5,OR,'middle','800')
g+=t(sx(75),sy(57),'CO₂: steep',12,PK,'middle','800')+t(sx(75),sy(24),'O₂: flat on top',12,PU,'middle','800')
D.append(('co2','7 · CO₂ vs O₂ dissociation curves','Deck 7 slide 27 · notes 7',svg(370,280,g),
 ['<b>In the normal range, the CO₂ curve is far steeper than the O₂ curve.</b>',
  '<b>So extra breathing CAN blow off extra CO₂</b> (steep line: lower PCO₂ = much less CO₂ content).',
  '<b>But extra breathing CAN\'T add O₂</b> once hemoglobin is near full (flat top).',
  '<b>Why it matters:</b> in ventilation-perfusion mismatch, good units fix CO₂ but can\'t fix O₂ → low PaO₂ with normal PaCO₂.',
  '<i>Curve shapes match his slide; exact CO₂ content values on this drawing are not exam numbers.</i>'],
 f'<span style="color:{PK}">━ CO₂</span><span style="color:{PU}">━ O₂</span>'))

# 8 · Hypoxemia decision flowchart
def box(x,y,w,h,txt,fill='#fff',stroke=PU,tc=INK,bold=True):
    lines=txt.split('|'); o=f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
    for i,l in enumerate(lines): o+=t(x+w/2,y+h/2+4+(i-(len(lines)-1)/2)*14,l,11.5,tc,'middle','800' if bold else '500')
    return o
def arr(x1,y1,x2,y2,lbl='',c=INK):
    o=f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="1.8" marker-end="url(#ah)"/>'
    if lbl: o+=t((x1+x2)/2+(6 if x1==x2 else 0),(y1+y2)/2-3,lbl,10.5,c,'start' if x1==x2 else 'middle','800')
    return o
g=f'<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{INK}"/></marker></defs>'
g+=box(110,8,150,34,'Low PaO₂ (hypoxemia)','#F5ECFD')
g+=arr(185,42,185,62)+box(105,62,160,34,'PaCO₂ HIGH?')
g+=arr(265,79,300,79)+t(282,73,'yes',10.5,PK,'middle','800')+box(300,58,74,44,'2. Hypo-|ventilation','#FDE3F1',PK)
g+=arr(185,96,185,118,'no (low / normal)')+box(95,118,180,34,'Low inspired O₂? (altitude,|wrong gas)')
g+=arr(275,135,300,135)+t(287,129,'yes',10.5,PK,'middle','800')+box(300,114,74,44,'1. Low|inspired PO₂','#FDE3F1',PK)
g+=arr(185,152,185,174,'no')+box(105,174,160,34,'Give 100% O₂: PaO₂|rises a lot?')
g+=arr(175,208,90,232)+t(115,226,'no',10.5,PK,'middle','800')+box(8,232,150,40,'4. Right-to-left SHUNT','#FDE3F1',PK)
g+=arr(195,208,280,232)+t(255,226,'yes',10.5,PU,'middle','800')+box(205,232,165,40,'5. V/Q mismatch|or 3. diffusion limitation','#F5ECFD',PU)
g+=box(205,284,165,40,'Diffusion: worse on exercise|→ measure diffusing capacity','#FFF8EC',OR,INK,False)
g+=ln(287,272,287,284,OR,1.5)
D.append(('hypox','8 · The 5 causes of hypoxemia: decision flowchart','Deck 5 slides 3–23 · notes 5 · ⭐ inspired hypoxia vs hypoventilation; ⭐ shunt diagnosis with 100% O₂',svg(380,330,g),
 ['<b>Step 1, PaCO₂:</b> HIGH = hypoventilation (not breathing enough). LOW = low inspired O₂ (the low O₂ makes the animal breathe harder). ⭐',
  '<b>Step 2, 100% O₂:</b> shunt barely improves (shunted blood never sees the O₂). PaO₂ >500 on 100% O₂ ≈ small shunt; ~250 ≈ big shunt.',
  '<b>Mismatch vs diffusion:</b> mismatch is the most common (most lung disease). Diffusion limitation usually shows only during exercise.',
  '<b>Severity of mismatch:</b> alveolar–arterial difference (see 🧮 equations). Big gap = bad mismatch.',
  '<i>The order of steps is a study aid built from his 5 causes and diagnostic clues; he did not draw this flowchart.</i>'],''))

SHORT=['1 O₂ cascade','2 Equilibration','3 Compliance','4 PVR J-curve','5 Apex vs base','6 O₂ curve','7 CO₂ vs O₂','8 Hypoxemia flow']
toc='<div class="toc">'+''.join(f'<a href="#{d[0]}">{E(n)}</a>' for d,n in zip(D,SHORT))+'</div>'
body='<div class="key">Purple = normal · <b style="color:#E0459A">pink = what changed from normal</b> · orange = exercise / source conflict · ⭐ = Poole said exam</div>'+toc
for i,tt,src,s,bl,lg in D:
    body+=f'<div class="dg" id="{i}"><h2>{tt}</h2><p class="src">{src}</p>{s}'+(f'<p class="lg">{lg}</p>' if lg else '')+'<ul>'+''.join(f'<li>{b}</li>' for b in bl)+'</ul></div>'
open(FN,'w').write(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>📈 Exam 3 Key Diagrams</title><style>{css}</style></head><body><div class="wrap"><a class="back" href="{E3}?v={V}">← Back to Exam 3</a><div class="hero"><h1>📈 Key Diagrams</h1><p>8 must-know Poole pictures · draw each one from memory, then check</p></div>{body}<div class="foot">🎀 Bethany · K-State CVM Class of 2030 · 🐾</div></div></body></html>')
print(FN,len(D))
