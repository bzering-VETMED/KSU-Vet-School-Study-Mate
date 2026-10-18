"""Practical 3 · Labs 19–24 hubs from course slides (Title/Note PDFs via p3slides.py, Abdomen.pdf via p3abd.py).
Bold terms only in ⭐ blocks; non-bold slides go to 📚 extra. Run from repo root (needs `ln -s . site`):
  python3 tools/p3labs.py /home/claude/p3b      then: python3 tools/umn.py; python3 tools/p3check.py; python3 tools/p3simplify.py"""
import sys,os,re,json,time,html,shutil
sys.path.insert(0,'tools')
import deck; deck.PRACTICAL=3
from deck import img_card_facts,text_card2,page,write_lab
import bold,p3bold
from PIL import Image
B=sys.argv[1] if len(sys.argv)>1 else '/home/claude/p3b'
V=str(int(time.time())); E=html.escape
for n,l in p3bold.P3BOLD.items(): bold.BOLD[n]=l
AB={'a':'artery','aa':'arteries','v':'vein','vv':'veins','n':'nerve','nn':'nerves','m':'muscle','mm':'muscles','lig':'ligament','gb':'gallbladder','br':'branch'}
def norm(t):
    out=[]
    for w in re.findall(r'[a-z0-9]+',t.lower()):
        w=AB.get(w,w)
        if len(w)>4 and w.endswith('s') and not w.endswith(('ss','us','is')): w=w[:-1]
        if w=='arterie': w='artery'
        if w in('the','of','and','a'): continue
        out.append(w)
    return out
def has(h,n): return bool(n) and any(h[i:i+len(n)]==n for i in range(len(h)-len(n)+1))
GENERIC={('colon',),('omentum',),('kidney',),('pancrea',),('uteru',),('ovary',),('liver',),('duodenum',),('stomach',),('cortex',),('medulla',),('arcuate',),('lumbar','part'),('costal','part'),('sternal','part'),('cardiac','part'),('body','stomach')}
def bold_hit(label,lab):
    L=norm(re.sub(r'\(.*?\)','',label)) or norm(label)
    for t,al,_ in bold.BOLD[lab]:
        for a in [t]+al:
            A=norm(a)
            if not A: continue
            if L==A or (has(L,A) and (len(A)>1 or tuple(A) not in GENERIC or L==A)) or (len(L)>1 and has(A,L)): return t
    return None
FULL=[(r'\ba\.',' artery'),(r'\bGB\b','Gallbladder'),(r'\blig\.','ligament'),(r' Of ',' of '),(r'\s+',' ')]
def full(t):
    for a,b in FULL: t=re.sub(a,b,t)
    return t.strip().replace('branch of superficial radial nerve branch','branch of the superficial radial nerve')
def clean_note(n):
    n=re.split(r'Dissection:',n)[0].strip()
    return n if len(n)<420 else n[:400].rsplit(' ',1)[0]+'…'
os.makedirs('assets',exist_ok=True)
def asset(src,name,maxw=1800):
    im=Image.open(src).convert('RGB')
    if im.width>maxw: im=im.resize((maxw,int(im.height*maxw/im.width)))
    dst=f'assets/{name}.jpg'; im.save(dst,quality=86); return f'{dst}?v={V}'
for f in os.listdir('assets'):
    if re.match(r'p3s_(fl1|fl2|l23a|l23b|l23m|l24|abd)_',f): os.remove('assets/'+f)
SRCTAG={'fl1':'📚 course slides · Lab 19/20 brachial plexus','fl2':'📚 course slides · Lab 19/20 forelimb','l23a':'📚 course slides · Lab 23','l23b':'📚 course slides · Lab 23','l23m':'📚 course slides · Lab 23','l24':'📚 course slides · Lab 24','abd':'📚 course slides · Abdomen'}
LABOF={'fl1':19,'fl2':19,'l23a':23,'l23b':23,'l23m':23,'l24':24}
SKIP={'Lab 20 Brachial Plexus','End of Lab 20','Lab 21','Lab 23','Lab 24 Pelvic viscera'}
cards={n:[] for n in (19,21,22,23,24)}   # (kind,bold_term_or_None,html,region)
terms={n:[] for n in cards}
def region(lab,title,src,pg):
    t=title.lower()
    if lab==19: return 'Veins' if 'vein' in t else 'Arteries' if ('arter' in t or 'arch' in t) else 'Nerves' if 'nerve' in t else 'Skin zones + digital vessels'
    if lab==23: return 'Nerves + ganglia' if re.search(r'nerve|ganglia|ganglion|plexus|trunk',t) and 'phrenicoabdominal' not in t else 'Veins' if 'vein' in t else 'Arteries'
    if lab==24: return 'Arteries' if 'arter' in t or 'lacuna' in t else 'Pelvic diaphragm + pouches' if re.search(r'levator|coccygeus|diaphragm|plexus|pelvic nerve|fossa|pouch',t) else 'Bladder + rectum + anus'
    return 'Slides'
for tag in ('fl1','fl2','l23a','l23m','l23b','l24'):
    for it in json.load(open(f'{B}/{tag}.json')):
        T=full(it['title']); lab=LABOF[tag]
        if T in SKIP: continue
        note=clean_note(it['note']); bt=bold_hit(T,lab); rg=region(lab,T,tag,it['page'])
        if not it['hl']:
            terms[lab].append(text_card2(f'Define / locate: {T}',note or T,SRCTAG[tag])); continue
        for k,h in enumerate(it['hl']):
            q=asset(h,f'p3s_{tag}_{it["page"]}_{k}')
            if it['clean']:
                c=img_card_facts('Identify the highlighted structure.',q,T,note,asset(it['clean'],f'p3s_{tag}_{it["page"]}c'),[],SRCTAG[tag])
            else:
                c=img_card_facts(f'📍 Find + point to: {T}',q,T,note,'',[],SRCTAG[tag])
            cards[lab].append(('main' if bt else 'extra',bt,c,rg))
# Abdomen.pdf: numbered labels
import importlib.util
spec=importlib.util.spec_from_file_location('p3abd','tools/p3abd.py'); A=importlib.util.module_from_spec(spec); spec.loader.exec_module(A)
def abdlab(pg): return 21 if pg<=3 else 22 if pg<=36 else 23
items=A.run('/home/claude/drv/Abdomen.pdf.pdf',B,lambda pg,t:bool(bold_hit(full(t),abdlab(pg))))
ABDREG=[(11,'Wall, peritoneum + diaphragm'),(17,'Liver + stomach'),(27,'Intestines'),(36,'Pancreas, kidneys + ligaments'),(47,'Abdomen slides')]
for it in items:
    pg=it['page']; lab=abdlab(pg)
    if not it['tags']: continue
    rg='Abdomen slides' if lab!=22 else next(n for hi,n in ABDREG if pg<=hi)
    nums=[n for n,_ in it['tags']]
    q=f'Name #{nums[0]}' if len(nums)==1 else f'Name #1–#{nums[-1]}'
    ans=' · '.join(f'#{n} {full(t)}' for n,t in it['tags'])
    note=' '.join(it['notes'])
    c=img_card_facts(q,asset(f'{B}/abd_{pg}q.jpg',f'p3s_abd_{pg}q'),ans,note,asset(f'{B}/abd_{pg}a.jpg',f'p3s_abd_{pg}a'),[],SRCTAG['abd'])
    cards[lab].append(('main',bold_hit(full(it['tags'][0][1]),lab),c,rg))
D=lambda q,a:text_card2(q,a,'🧠 concept · standard anatomy')
TERMCARDS={22:[D('Abdominal cavity vs peritoneal cavity?','Abdominal cavity = the whole space bounded by the diaphragm, abdominal walls and pelvic inlet (holds organs + peritoneum). Peritoneal cavity = only the potential space BETWEEN parietal and visceral peritoneum (a film of fluid; no organs inside).'),
 D('Parietal vs visceral vs connecting peritoneum?','Parietal peritoneum = lines the abdominal walls · visceral peritoneum = covers the organs · connecting peritoneum = double folds joining them (mesenteries, omenta, ligaments, folds).'),
 D('Empty vs full stomach: where does it sit?','Empty stomach: entirely within the intrathoracic part of the abdomen, under the ribs; not palpable. Full stomach: expands caudoventrally past the costal arch, can reach the umbilicus and contact the ventral abdominal wall.')],
 21:[D('Cutaneous nerves of the flank/inguinal skin (cranial → caudal)?','Cranial iliohypogastric nerve (L1) · caudal iliohypogastric nerve (L2) · ilioinguinal nerve (L3) · lateral cutaneous femoral nerve (L4) · genitofemoral nerve (L3–L4, through the inguinal canal).')]}
TITLE={19:'Labs 19 + 20 · Thoracic limb vessels + nerves',21:'Lab 21 · Abdominal wall + inguinal region',22:'Lab 22 · Abdominal viscera',23:'Lab 23 · Abdominal viscera vessels + nerves',24:'Lab 24 · Pelvic viscera'}
def chunk(lst,kind):
    out=[]; regs=[]
    for k,b,c,r in lst:
        if k!=kind: continue
        if r not in regs: regs.append(r)
    ORD=['Wall, peritoneum + diaphragm','Liver + stomach','Intestines','Pancreas, kidneys + ligaments','Arteries','Nerves','Veins','Nerves + ganglia','Pelvic diaphragm + pouches','Bladder + rectum + anus','Abdomen slides','Skin zones + digital vessels','Slides']
    regs.sort(key=lambda r:ORD.index(r) if r in ORD else 99)
    for r in regs:
        cs=[c for k,b,c,rr in lst if k==kind and rr==r]; n=(len(cs)+14)//15
        for i in range(n):
            part=cs[i*len(cs)//n:(i+1)*len(cs)//n]
            out.append((r+(f' {i+1}' if n>1 else ''),part))
    return out
for lab in cards:
    tc=terms[lab]+TERMCARDS.get(lab,[]) if 'TERMCARDS' in globals() else terms[lab]
    if tc:
        tc[0]=tc[0].replace('class="card"','class="card on"',1)
        open(f'gross-anatomy-lab{lab}-terms.html','w').write(page(f'Lab {lab} · 🧠 No-image terms',f'{len(tc)} cards',''.join(tc),back=f'gross-anatomy-lab{lab}-images.html'))
    write_lab(lab,TITLE[lab],chunk(cards[lab],'main'),chunk(cards[lab],'extra'),len(tc))
    print(lab,{k:sum(1 for x in cards[lab] if x[0]==k) for k in('main','extra')},'terms',len(tc),[ (n,len(c)) for n,c in chunk(cards[lab],'main')])
