# Build: Veterinary Systems I · Lab Practical 1 (Microanatomy Exam 1: Labs 1,2,3,4,7)
# Run from repo root: python3 tools/micro1.py  (source crops in SRC; copies to assets/mic1_*.jpg)
import sys,os,time,html,re
sys.path.insert(0,'tools'); import deck
from micro1_data import DECKS,TERMS,OBJ,ATTACH,EXTRA,EXAM25,LAYERS,EXAM2B
SRC=os.environ.get('MIC1_SRC','/home/claude/w')
E=html.escape; V=str(int(time.time()))
TITLES={'lab1':'Lab 1 · Microscopy & Cytology','lab2':'Lab 2 · Connective Tissue, Epithelium & Skin','lab3':'Lab 3 · Nerve, Cartilage & Bone','lab4':'Lab 4 · Muscle, Heart & Circulation','lab7':'Lab 7 · Lymphatic Tissues & Organs'}
PRAC='systems-lab-practical1.html'
def card(img,q,a,tell,fn,ver,extra=()):
    facts=[]
    if tell: facts.append(('🔎 How do you know?',tell))
    if fn: facts.append(('💡 Function / remember',fn))
    for eq,ea in extra: facts.append(('🧩 '+eq,ea))
    clue='⚠️ verify in lab' if ver else ''
    if img:
        dst=f'assets/mic1_{img.replace("/","_")}.jpg'
        if not os.path.exists(dst): deck.save_img(f'{SRC}/c_{img}.jpg',dst,1000)
        return deck.img_card_facts(q,dst,a,clue,None,facts)
    ans=E(a)+''.join(f'<div class="clue">{E(p)}: {E(t)}</div>' for p,t in facts)
    return f'<section class="card"><div class="q textq">{E(q)}</div>{deck.stg("❓ Your answer?",ans,True)}<div class="rev">💗 TAP TO REVEAL</div></section>'
def chunk(xs,n=15):
    k=max(1,-(-len(xs)//n)); s=-(-len(xs)//k); return [xs[i:i+s] for i in range(0,len(xs),s)]
tiles=[]
for slug,title,fav,cards in DECKS:
    T=TITLES[slug]; hubfn=f'systems-lp1-{slug}-images.html'; termfn=f'systems-lp1-{slug}-terms.html'
    img=[c for c in cards if c[0]]; txt=[c for c in cards if not c[0]]
    pool=[(c[1],c[2]+(' ('+c[3]+')' if c[3] else '')) for c in txt]+list(TERMS[slug]); used=set(); EX={}
    for key,pre in ATTACH[slug]:
        hit=[(q,a) for q,a in pool if q.startswith(pre)]
        assert hit,(slug,pre)
        EX.setdefault(key,[]).append(hit[0]); used.add(hit[0][0])
    left=[q for q,a in pool if q not in used]; assert not left,(slug,left)
    seen=set()
    links=[]; alltext=[]
    for i,blk in enumerate(chunk(img),1):
        fn=f'systems-lp1-{slug}-main{i}.html'; cs=[]
        for c in blk:
            ex=(EX.get(c[0],[])+EXTRA.get(c[0],[])) if c[0] not in seen else []; seen.add(c[0]); cs.append(card(*c,extra=ex))
        alltext+=cs
        cs[0]=cs[0].replace('class="card"','class="card on"',1)
        open(fn,'w').write(deck.page(f'{T.split(" · ")[0]} · Block {i}',f'⭐ Objective images · {len(cs)} cards',''.join(cs),back=hubfn))
        links.append(f'<a href="{fn}?v={V}">Block {i}<span>{len(cs)} cards</span></a>')
    # objective checklist
    blob=html.unescape(re.sub(r'<[^>]+>',' ',' '.join(alltext))).lower()
    rows=[];got=0
    for t in OBJ[slug]:
        ok=t in blob; got+=ok
        rows.append(f'<tr><td>{E(t)}</td><td>{"✅" if ok else "❗ add from screenshots"}</td></tr>')
    chk=f'<details class="sec chk"><summary>✅ Objective-term checklist · {got}/{len(OBJ[slug])} covered</summary><p>Terms from the Microanatomy Exam 1 objectives list.</p><div class="tw"><table>{"".join(rows)}</table></div></details>'
    hub=f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><title>{E(T)}</title><style>{deck.HUBCSS}</style></head><body><div class="wrap"><a class="back" href="{PRAC}?v={V}">← Back to Lab Practical 1</a><div class="hero"><h1>{fav} {E(T)}</h1><p>Small decks. Do one, take a breath, do the next. 🐾</p></div>{chk}<div class="sec main"><h2>⭐ Objective images (start here)</h2><p>Every question for each image is on that card (🧩 = extra objective question). Say it before you tap.</p>{"".join(links)}</div><div class="sec extra"><h2>📚 Extra images</h2><p>📷 Your lecture screenshots land here next.</p></div></div></body></html>'
    open(hubfn,'w').write(hub)
    tiles.append(f'<div class="tile"><h2>{fav} {E(T)}</h2><a href="{hubfn}?v={V}">🖼️ Image decks · small blocks ⭐📚</a></div>')
    print(slug,len(img),'img',sum(len(v) for v in EX.values()),'folded',f'{got}/{len(OBJ[slug])}')
# 📝 2025 practice exam
ecards=[]
for i,(a,tell,fn) in enumerate(EXAM25,1):
    key=f'exam25/q{i:02d}'; dst=f'assets/mic1_exam25_q{i:02d}.jpg'
    if not os.path.exists(dst): deck.save_img(f'{SRC}/c_{key}.jpg',dst,1400)
    f=[]
    if tell: f.append(('🔎 How do you know?',tell))
    if fn: f.append(('💡 Remember',fn))
    ecards.append(deck.img_card_facts(f'Q{i} · Answer the question in the image',dst,a,'',None,f))
ecards[0]=ecards[0].replace('class="card"','class="card on"',1)
EXF='systems-lp1-exam2025.html'
open(EXF,'w').write(deck.page('📝 2025 Lab Practical (last year)','51 questions · ✅ answers checked against the teacher-confirmed key',''.join(ecards),back=PRAC).replace('← Back to Practical 2','← Back to Lab Practical 1'))
bc=[]
for q,(a,tell,fn) in sorted(EXAM2B.items()):
    key=f'exam2b/q{q:02d}'; dst=f'assets/mic1_exam2b_q{q:02d}.jpg'
    if not os.path.exists(dst): deck.save_img(f'{SRC}/c_{key}.jpg',dst,1320)
    f=[]
    if tell: f.append(('🔎 How do you know?',tell))
    if fn: f.append(('💡 Remember',fn))
    bc.append(deck.img_card_facts(f'Q{q} · Answer the question in the image',dst,a,'',None,f))
bc[0]=bc[0].replace('class="card"','class="card on"',1)
EX2='systems-lp1-exam2b.html'
open(EX2,'w').write(deck.page('📝 Practice Lab Exam 2','✅ answers confirmed with Dr. Klimek · Q46 missing from the screenshots',''.join(bc),back=PRAC).replace('← Back to Practical 2','← Back to Lab Practical 1'))
tiles.append(f'<div class="tile"><h2>📝 Practice exams</h2><a href="{EXF}?v={V}">Practice Exam 1 (2025) · 51 Q ✅</a><a href="{EX2}?v={V}">Practice Exam 2 · 50 Q ✅</a></div>')
# 🧅 layers drill (2 blocks)
lnk=[]
for i,(lo,hi,sub) in enumerate([(0,16,'Nerve · skeletal muscle · heart · vessels'),(16,len(LAYERS),'Skin · cartilage & bone · lymph node & thymus')],1):
    LYF=f'systems-lp1-layers{i}.html'
    lc=[card(*c) for c in LAYERS[lo:hi]]; lc[0]=lc[0].replace('class="card"','class="card on"',1)
    open(LYF,'w').write(deck.page(f'🧅 All the Layers · Block {i}',sub+' · say ALL layers before you tap',''.join(lc),back=PRAC).replace('← Back to Practical 2','← Back to Lab Practical 1'))
    lnk.append(f'<a href="{LYF}?v={V}">Block {i} · {sub} · {len(lc)}</a>')
tiles.insert(0,f'<div class="tile"><h2>🧅 All the Layers</h2>{"".join(lnk)}</div>')
prac=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>🔬 Systems I · Lab Practical 1</title><style>body{{margin:0;background:#fff9fd;color:#493451;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif}}.wrap{{max-width:1000px;margin:auto;padding:18px}}.hero{{color:#fff;background:linear-gradient(135deg,#5d347e,#8855b8 55%,#df78ad);padding:24px;border-radius:24px}}.hero h1{{margin:0}}.grid{{display:grid;grid-template-columns:repeat(2,1fr);gap:14px;margin-top:16px}}.tile{{background:#fff;border:1px solid #eadff2;border-radius:18px;padding:18px}}.tile h2{{color:#70428f;margin:0 0 10px;font-size:20px}}.tile a{{display:block;text-decoration:none;margin:7px 0;padding:10px;border-radius:12px;background:#f7eefb;color:#70428f;font-weight:800}}.note{{margin-top:14px;background:#fff;border:1px dashed #eadff2;border-radius:16px;padding:12px 14px;font-size:15px}}@media(max-width:700px){{.grid{{grid-template-columns:1fr}}}}</style></head><body><div class="wrap"><a href="systems-lab.html?v={V}" style="display:inline-block;margin:0 0 10px;padding:8px 14px;border-radius:999px;background:#f3eafb;color:#65328c;font-weight:800;text-decoration:none">← Back</a><div class="hero"><h1>🔬 Veterinary Systems I · Lab Practical 1</h1><p>Microanatomy Exam 1 · Tue 10/13 · Labs 1, 2, 3, 4 & 7 · 50 images, fill-in-the-blank</p></div><div class="note">Spell it exactly; there's no word bank. ⚠️ = slide key was ambiguous, confirm in lab. Labs 5–6 (ECG) are NOT on this practical.</div><div class="grid">{"".join(tiles)}</div></div></body></html>'''
open(PRAC,'w').write(prac)
s=open('systems-lab.html').read()
s=s.replace('<div class="tile"><h2>Lab Practical 1</h2><p>Ready for study materials</p></div>',f'<a class="tile" href="{PRAC}?v={V}"><div class="emoji">🔬</div><h2>Lab Practical 1</h2><p>Microanatomy · Labs 1, 2, 3, 4 & 7 · 10/13</p></a>')
s=re.sub(r'href="systems-lab-practical1\.html\?v=\d+"',f'href="{PRAC}?v={V}"',s)
open('systems-lab.html','w').write(s)
sw=open('sw.js').read(); open('sw.js','w').write(re.sub(r"ksu-study-mate-v(\d+)-\d+",lambda m:f"ksu-study-mate-v{int(m.group(1))+1}-{V}",sw))
