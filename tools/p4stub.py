"""Practical 4 · hub for a lab whose photo decks haven't arrived yet (made by Claude).
Checklist (every bold term, list order, ❗ = no photo yet) + ⚡ definitions page (Canvas bold-term definitions → name it).
Replace with a full p4labN.py build when the lab-slide PDF/.pptx arrives.   python3 tools/p4stub.py 28 'Lab 28 · Skull, teeth + hyoid'"""
import sys,time,os
sys.path.insert(0,'tools')
import p4lab26 as B, terms_page as TP
from p4bold import P4BOLD
lab=int(sys.argv[1]); title=sys.argv[2]; V=str(int(time.time()))
tf=f'gross-anatomy-lab{lab}-terms.html'
pg,n,s=TP.build(f'LAB{lab}',tf,f'Lab {lab} Bold Terms · definition → name it',V,f'gross-anatomy-lab{lab}-images.html')
open(tf,'w').write(pg.replace('← Back to Exam 4','← Back to Lab hub'))
best=[];extra=[]
if lab==28:                                        # Nov 8: Dr. Sparks skull-quiz photos (real skulls, yellow highlight) + Dr. Diehl teeth slides FIRST
    import p4skull,p4find,p4lec
    lec=p4lec.skull_quiz()+p4lec.al_quiz()+p4lec.teeth(); have28=set()
    for c in lec:
        new=set(c['terms'])-have28
        (best if new else extra).append(c); have28|=new
    for c in sorted(p4skull.build(),key=lambda c:-len(set(c['terms'])-have28)):
        new=set(c['terms'])-have28; (best if new else extra).append(c); have28|=new
    for c in p4find.build():
        if set(c['terms'])-have28: best.append(c); have28|=set(c['terms'])
import p4guide
GPDF={28:'/mnt/user-data/attachments/31594bc3-9d6f-5c02-a55e-32953ff4d455/f954b1d8-Lab_28.pdf',29:'/mnt/user-data/attachments/31594bc3-9d6f-5c02-a55e-32953ff4d455/288bd0ef-Lab_29.pdf'}
if lab in GPDF and os.path.exists(GPDF[lab]): best,gx=p4guide.fill(best,p4guide.cards(GPDF[lab],lab,f'p4g{lab}')); extra+=gx
if lab==29:                                        # Nov 8: Bethany's Lab 29 Head slides FIRST, then UMN, then the rest only for gaps
    import p4find,p4pptlab,p4umn,p4wil
    guide=best; best,extra,concept=p4pptlab.build(29,'/home/claude/p4w/l29.pdf')
    have={t for c in best for t in c['terms']}
    def add(cs,keep_dupes=True):
        global have
        for c in sorted(cs,key=lambda c:-len(set(c['terms'])-have)):
            new=set(c['terms'])-have
            if new: best.append(c); have|=new
            elif keep_dupes: extra.append(c)
    add(p4umn.cards_for(29))
    add(p4wil.cards(29)[0])
    l31=[]
    if os.path.exists('/home/claude/p4w/l31.pdf'):
        for c in p4pptlab.build(31,'/home/claude/p4w/l31.pdf')[0]:
            ts=B.terms_in(c['name'],29)
            if ts: c=dict(c); c['terms']=ts; l31.append(c)
    add(l31,False); add(guide,False); add(p4find.build29()+p4find.build29b(),False)
    best+=[c for c in concept if set(c['terms'])-have]
    for src,wd,tag,pre in (('/home/claude/new/eye.pptx','/home/claude/p4eye','Dr. Malreddy eye lecture','p4eye'),('/home/claude/new/diehl1.pptx','/home/claude/p4dh1','Dr. Diehl Digestive Head 1','p4dh1')):
        if os.path.exists(src): extra+=p4wil.deck(src,wd,tag,pre).get(lab,[])          # Nov 8: lecture slides → 📚 Extra
    nu=0
elif lab==28:                                      # UMN only fills what the course photos don't show
    import p4umn; have28={x for c in best if '🧠' not in c['html'][:300] for x in c['terms']}
    for c in sorted(p4umn.cards_for(28),key=lambda c:-len(set(c['terms'])-have28)):
        new=set(c['terms'])-have28; (best if new else extra).append(c); have28|=new
    nu=0
else:
    import p4umn; best,extra,nu=p4umn.merge(lab,best,extra)
note='your Lab 29 Head slides first, UMN photos fill the gaps' if lab==29 else 'course skull-quiz photos + teeth lecture first, then your photos, UMN + drawings fill the gaps' if lab==28 else ((f'{nu} UMN cadaver photos first, then ' if nu else '')+'your photos + lab-guide drawings fill the gaps' if best else '')
B.two_area_hub(lab,title,'Two decks. One tap = full answer. 🐾',best,extra,note)
print(lab,n,'terms')
h=open(f'gross-anatomy-lab{lab}-images.html').read()
h=h.replace('</div></body></html>',f'<!--fn--><div class="sec terms" style="padding:8px 14px"><p style="margin:4px 0 0">📄 Study pages (no photos)</p><a href="{tf}?v={V}">⚡ Bold-term definitions page<span>{n} terms</span></a></div><!--/fn--></div></body></html>',1)
open(f'gross-anatomy-lab{lab}-images.html','w').write(h)
