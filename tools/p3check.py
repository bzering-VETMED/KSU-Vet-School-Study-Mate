"""Re-count each Practical 3 hub's bold-term checklist over EVERY deck the hub links (slides, UMN, my photos, terms).
Run LAST (after umn.py, p3simplify.py, p3split.py):  python3 tools/p3check.py 16 17 18 19 21 22 23 24"""
import sys,re,html,os
sys.path.insert(0,'tools'); import bold,p3bold
from deck import E
for n,l in p3bold.P3BOLD.items(): bold.BOLD[n]=l
import p3shots as SH
for n,S in ((16,SH.S16),(17,SH.S17),(18,SH.S18)):
    bold.BOLD[n]=[(t,[x.lower().lstrip('=') for x in [t]+al],'') for t,al in S]
_s=open('tools/p3split.py').read(); exec(_s[_s.index('AB={'):_s.index('def terms')])   # norm, has
def _norm_hit(als,t,tn):
    return any(a in t for a in als) or any(has(tn,norm(re.sub(r'\(.*?\)','',a))) for a in als if len(norm(a))>=2)
def txt(f):
    try: return html.unescape(re.sub(r'<[^>]+>',' ',open(f).read())).lower()
    except: return ''
for n in map(int,sys.argv[1:]):
    hub=f'gross-anatomy-lab{n}-images.html'; h=open(hub).read()
    links=[]
    for sec in re.findall(r'<div class="sec (main|more|extra|terms|diag)"[^>]*>(.*?)</div>',h,re.S):
        for href,name in re.findall(r'<a href="([^"?]+)[^"]*">([^<]*)<',sec[1]):
            icon={'main':'⭐','more':'🔁','extra':'📚','terms':'🧠','diag':'📖'}[sec[0]]
            tt=txt(href); links.append((icon,name.strip(),tt,norm(tt)))
    links.sort(key=lambda x:'⭐🔁📖📚🧠'.index(x[0]))
    rows=[];got=0
    for term,al,note in bold.BOLD[n]:
        w=next(((i,nm) for i,nm,t,tn in links if _norm_hit(al,t,tn)),None)
        if w: got+=1
        cell=f'{w[0]} {E(w[1])}' if w else '❗ no photo yet'
        if note: cell+=f' · {E(note)}'
        rows.append(f'<tr><td>{E(term)}</td><td>{cell}</td></tr>')
    blk=f'<details class="sec chk"><summary>✅ Bold-term checklist · {got}/{len(bold.BOLD[n])} covered</summary><p>Same order as your bold-term list. ⭐ = best pictures · 🔁 = more practice · 📖 = lab-guide diagram · 📚 = extra block · 🧠 = no-image terms deck. ❗ = waiting on a photo.</p><div class="tw"><table>{"".join(rows)}</table></div></details>'
    h=re.sub(r'<details class="sec chk">.*?</details>',blk,h,flags=re.S)
    open(hub,'w').write(h)
    print(n,f'{got}/{len(bold.BOLD[n])}','MISSING:',html.unescape('; '.join(t for t,a,_ in bold.BOLD[n] if not any(_norm_hit(a,tt,tn) for i,nm,tt,tn in links))))
