"""Practical 4 · hub for a lab whose photo decks haven't arrived yet (made by Claude).
Checklist (every bold term, list order, ❗ = no photo yet) + ⚡ definitions page (Canvas bold-term definitions → name it).
Replace with a full p4labN.py build when the lab-slide PDF/.pptx arrives.   python3 tools/p4stub.py 28 'Lab 28 · Skull, teeth + hyoid'"""
import sys,time
sys.path.insert(0,'tools')
import p4lab26 as B, terms_page as TP
from p4bold import P4BOLD
lab=int(sys.argv[1]); title=sys.argv[2]; V=str(int(time.time()))
tf=f'gross-anatomy-lab{lab}-terms.html'
pg,n,s=TP.build(f'LAB{lab}',tf,f'Lab {lab} Bold Terms · definition → name it',V,f'gross-anatomy-lab{lab}-images.html')
open(tf,'w').write(pg.replace('← Back to Exam 4','← Back to Lab hub'))
B.two_area_hub(lab,title,'Two decks once photos arrive. Definitions page below. 🐾',[],[])
print(lab,n,'terms')
h=open(f'gross-anatomy-lab{lab}-images.html').read()
h=h.replace('</div></body></html>',f'<!--fn--><div class="sec terms" style="padding:8px 14px"><p style="margin:4px 0 0">📄 Study pages (no photos)</p><a href="{tf}?v={V}">⚡ Bold-term definitions page<span>{n} terms</span></a></div><!--/fn--></div></body></html>',1)
open(f'gross-anatomy-lab{lab}-images.html','w').write(h)
