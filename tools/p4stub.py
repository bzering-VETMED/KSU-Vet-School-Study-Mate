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
cards=[dict(name=t,terms=[t]) for t,_,_ in P4BOLD[lab]]
B.write_hub(lab,title,'Photo decks come when the lab slides arrive. Start with the definitions page. 🐾',[
  ('terms','⚡ Bold-term definitions · start here','Your Canvas definitions → say the term out loud, then tap. ❗ No photo decks yet — send the Lab slide PDF/.pptx.',[(tf,'⚡ Definitions page · tap to reveal',cards)],'⚡')])
print(lab,n,'terms')
