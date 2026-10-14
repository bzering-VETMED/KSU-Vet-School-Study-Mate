import sys,re,os,time,html
sys.path.insert(0,'/tmp/claude-0/out'); sys.path.insert(0,'/home/claude/ksu-vet-school-study-mate/tools')
from bs4 import BeautifulSoup
from acr import BASE, spell_soup
os.chdir('/home/claude/ksu-vet-school-study-mate')
import deck
E=html.escape; V=str(int(time.time()))
REV=BeautifulSoup(open('/tmp/claude-0/out/VAP807_LectureExam_ReviewSheet_10.14.26.html').read(),'html.parser')
V2=BeautifulSoup(open('/tmp/claude-0/out/VAP807_StrengthenSheet_v2_10.14.26.html').read(),'html.parser')
def txt(el): return re.sub(r'\s+',' ',el.get_text(' ',strip=True))
def inner(el): return ''.join(str(c) for c in el.contents).strip()
# ---------------------------------------------------------- 1) TERM LIST PAGE
FUN=open('systems-lp1-functions.html').read()
CSS=FUN[FUN.index('<style>')+7:FUN.index('</style>')]
JS=FUN[FUN.rindex('<script>')+8:FUN.rindex('</script>')]
def table_items(tbl):
    rows=tbl.find_all('tr'); hdr=[txt(c) for c in rows[0].find_all(['th','td'])]; items=[]
    for r in rows[1:]:
        cells=r.find_all('td')
        if not cells: continue
        lab=txt(cells[0])
        if len(cells)==2: items.append((lab,inner(cells[1])))
        else:
            for h,c in zip(hdr[1:],cells[1:]):
                if txt(c): items.append((f'{lab} · {h}',inner(c)))
    return items
secs=[]
groups={'💓 Abbreviations · cardio & Musch':['LV dP/dt','LVEDP','LVEDV','LAP','a–vO₂','CaO₂','CvO₂','VO₂max','VO₂','PmvO₂','MAP','SVR','PVR','MPP','SBP','DBP','HR','SV','Q','BP','HFrEF','HFpEF','CHF','HF','EF','MI','NYHA','RAAS','ACE','EDRF','EDHF','NOS','NO','cGMP','cAMP','PKA','CCK','NE','ACh','SERCA','SR','TPR'],
        '⚡ Abbreviations · ECG & electrophysiology':['HCN','GIRK','E-C','MEA','SVT','APC','VPC','V-fib','V-tach','A-fib','SA','AV','RV','RA','LV'],
        '🩸 Abbreviations · blood, hemostasis & immune':['RBC','WBC','PMN','IMHA','MCV','MCHC','Hb','Hct','EPO','TPO','SCF','GM-CSF','G-CSF','M-CSF','IL-5','IL-3','vWF','vWD','TXA₂','PGI₂','tPA','PAI-1/2','TFPI','PT','PTT','BMBT','COX-1','ADP','MHC','TCR','BCR','TH','Tc','NK','IgE','IgM','CKD','IBD','SCID','PALS','MALT','IEL','CT','CNS']}
full=dict(BASE); full['APC']='atrial premature contraction (APC) · in immunology: antigen-presenting cell'
for g,keys in groups.items():
    secs.append((g,[(k,re.sub(r'\s*\('+re.escape(k)+r'\)$','',full[k])) for k in keys if k in full]))
for bid,name in [('lc19','🫀 Heart wall & vessels (LC19)'),('lymph','🧬 Lymphatic tissues, nodes, spleen & thymus (LC36–37)')]:
    blk=REV.select_one('#'+bid); spell_soup(blk)
    for i,t in enumerate(blk.find_all('table')):
        secs.append((name if i==0 else name.split(' (')[0]+' (cont.)',table_items(t)))
    if bid=='lymph':
        secs.append(('🧬 Lymph flow & cases',[('Lymph node flow (in order)','Afferent vessels → <b>subcapsular sinus</b> → <b>trabecular sinus</b> → <b>medullary sinus</b> → efferent vessels at the <b>hilus</b>'),
          ('Dog: diarrhea, lymphocytes invading gut epithelium, no infection','<b>Lymphocytic inflammatory bowel disease</b> → corticosteroids (± azathioprine)'),
          ('Schnauzer: large angular epithelial cells in a lymph node','<b>Metastatic squamous cell carcinoma</b>'),('Cat: many mast cells on a spleen aspirate','<b>Mast cell leukemia</b> (splenomegaly)'),
          ('Arabian foal: no immunoglobulin M, tiny thymus, lymphopenia','<b>Severe combined immunodeficiency</b> (DNA-dependent kinase defect, VDJ rearrangement fails)')]))
n=sum(len(i) for _,i in secs); body=[]
for k,(name,items) in enumerate(secs):
    rows=''.join(f'<tr><td>{E(a)}</td><td><span class="ans">{b}</span></td></tr>' for a,b in items)
    body.append(f'<div class="sec{" p" if k%2 else ""}"><h2>{E(name)}</h2><table>{rows}</table></div>')
open('systems-lec-terms.html','w').write(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>🧠 Terms Review</title><style>{CSS}</style></head><body><div class="wrap"><a class="back" href="systems-lecture.html?v={V}">← Back to Lecture</a><div class="hero"><h1>🧠 Terms Review: abbreviations, heart &amp; vessels, lymphatics</h1><p>Say the answer, then tap the pink box to check · {n} items · spelled out</p></div><div class="bar"><button id="hide">🙈 Hide all</button><button id="all">👀 Show all</button><span class="n" id="n"></span></div><div class="cols">{"".join(body)}</div><div class="foot">🎀 Bethany · K-State CVM Class of 2030 · VAP 807 · 🐾</div></div><script>{JS}</script></body></html>')
print('terms',n)
# ---------------------------------------------------------- 2) FLIP FLASHCARDS from Strengthen v2
def card(q,stages):
    S=''.join(deck.stg(E(p),a,big=(len(stages)==1)) for p,a in stages)
    return f'<section class="card"><div class="q textq">{E(q)}</div>{S}<div class="rev">💗 TAP TO REVEAL</div></section>'
decks=[]
for blk in V2.select('div.block'):
    h2=blk.find('h2'); 
    if not h2: continue
    title=txt(h2); tag=txt(blk.select_one('.tag')) if blk.select_one('.tag') else ''
    cards=[]; ctx=title
    for el in blk.find_all(['h3','table','div']):
        if el.name=='h3': ctx=txt(el); continue
        if el.name=='div' and 'tells' in (el.get('class') or []):
            b=el.find('b'); q=txt(b).rstrip(':') if b else ctx
            ans=inner(el)
            if b: ans=ans.replace(str(b),'',1)
            cards.append(card(f'Say it: {q}',[('❓ Your answer?',ans)])); continue
        if el.name=='div' and 'aa' in (el.get('class') or []):
            parts=' · '.join(txt(d) for d in el.find_all('div',recursive=False))
            cards.append(card(f'{ctx}: list them all',[('❓ Your answer?',E(parts))])); continue
        if el.name!='table': continue
        rows=el.find_all('tr'); hdr=[txt(c) for c in rows[0].find_all(['th','td'])]
        for r in rows[1:]:
            cells=r.find_all('td')
            if len(cells)<2: continue
            lab=txt(cells[0]).replace('⭐','').strip()
            if len(cells)==2: st=[('❓ '+(hdr[1] if len(hdr)>1 and hdr[1] else 'Answer')+'?',inner(cells[1]))]
            else: st=[(f'{h}?',inner(c)) for h,c in zip(hdr[1:],cells[1:]) if txt(c) and h!='🪝']
            if st: cards.append(card(f'{ctx} · {lab}',st))
    if cards: decks.append((title,tag,cards))
links_lec=[];links_mus=[];cnt=0
HUB='systems-lec-strength-cards.html'
for i,(title,tag,cards) in enumerate(decks,1):
    chunks=[cards[j:j+15] for j in range(0,len(cards),15)]
    for k,cs in enumerate(chunks,1):
        fn=f'systems-lec-sc{i}-{k}.html'; cs=list(cs); cs[0]=cs[0].replace('class="card"','class="card on"',1)
        nm=title+(f' · {k}' if len(chunks)>1 else '')
        out=deck.page(f'💪 {nm}',f'{len(cs)} cards · from your Strengthen Sheet · {tag}',''.join(cs),back=HUB).replace('← Back to Practical 2','← Back to Strengthen cards').replace('← Back to Practical 3','← Back to Strengthen cards')
        open(fn,'w').write(out); cnt+=len(cs)
        (links_mus if ('Part' in tag or 'Musch' in tag) else links_lec).append(f'<a href="{fn}?v={V}">{E(nm)}<span>{len(cs)} cards</span></a>')
hub=(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><title>Strengthen flashcards</title><style>{deck.HUBCSS}</style></head><body><div class="wrap">'
     f'<a class="back" href="systems-lecture.html?v={V}">← Back to Lecture</a><div class="hero"><h1>💪 Strengthen flashcards</h1><p>Every row of your Strengthen Sheet as a flip card · {cnt} cards · say it, then tap through · ✅/❌ to track misses 🐾</p></div>'
     f'<div class="sec main"><h2>⚡ Lectures 20–35</h2><p>Electrophysiology, ECG, smears, marrow, hemostasis, defensive cells.</p>{"".join(links_lec)}</div>'
     f'<div class="sec extra"><h2>🏃 Dr. Musch</h2><p>Parts 1–6.</p>{"".join(links_mus)}</div></div></body></html>')
open(HUB,'w').write(hub)
print('cards',cnt,len(links_lec),len(links_mus))
