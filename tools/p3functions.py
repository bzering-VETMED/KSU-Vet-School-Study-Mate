"""Practical 3 one-page Functions review (tap-to-reveal), same look as systems-lp1-functions.html.
python3 tools/p3functions.py  → gross-anatomy-p3-functions.html"""
import sys,re,time,html
sys.path.insert(0,'tools'); from p3functions_data import S
E=html.escape; V=str(int(time.time()))
t=open('systems-lp1-functions.html').read()
head=t[:t.index('<body>')].replace('<title>🧠 Functions Review</title>','<title>Practical 3 Functions</title>')
js=t[t.index('<script>'):]
n=sum(len(r) for _,_,r in S)
body=f'<body><div class="wrap"><a class="back" href="gross-anatomy-practical3.html?v={V}">← Back to Practical 3</a><div class="hero"><h1>🧠 Practical 3 · Functions</h1><p>Say the answer, then tap the pink box to check · {n} items · Labs 16–24 · from your slides + lab guide, plus standard anatomy</p></div><div class="bar"><button id="hide">🙈 Hide all</button><button id="all">👀 Show all</button><span class="n" id="n"></span></div><div class="cols">'
for title,pink,rows in S:
    body+=f'<div class="sec{" p" if pink else ""}"><h2>{E(title)}</h2><table>'+''.join(f'<tr><td>{E(q)}</td><td><span class="ans">{E(a)}</span></td></tr>' for q,a in rows)+'</table></div>'
body+='</div><div class="foot">🎀 Bethany · K-State CVM Class of 2030 · 🐾</div></div>'
open('gross-anatomy-p3-functions.html','w').write(head+body+js)
p=open('gross-anatomy-practical3.html').read()
link=f'<a href="gross-anatomy-p3-functions.html?v={V}">🧠 Functions · one page · tap to reveal<span>{n} items</span></a>'
if 'p3-functions' in p: p=re.sub(r'(<a [^>]*href=")gross-anatomy-p3-functions\.html\?v=\d+',r'\1gross-anatomy-p3-functions.html?v='+V,p)
else: p=p.replace('<div class="grid">','<a style="display:block;margin:0 0 14px;padding:14px 16px;border-radius:18px;text-decoration:none;font-weight:900;color:#fff;background:linear-gradient(120deg,#6a3392,#e05fa8)" href="gross-anatomy-p3-functions.html?v='+V+'">🧠 Functions · one page · tap to reveal · '+str(n)+' items</a><div class="grid">',1)
open('gross-anatomy-practical3.html','w').write(p)
print(n,'items')
