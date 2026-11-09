"""Practical 4 · 📖 lab-guide figures (Notes for Laboratory N PDFs) → numbered diagram cards (made by Claude).
Uses guidefigs.run (finds figures + vector labels) and guidefigs.render (erases ALL label text, keeps drawing +
leader lines, badges ONLY the labels that are your bold terms). One card per figure, all numbers on one tap.
Used to fill bold terms that have no photo yet (Bethany, Nov 4)."""
import sys,re,html
sys.path.insert(0,'tools')
import guidefigs as G, p4lab26 as B
from p4bold import P4BOLD
E=html.escape
SYN={'nasal':'nasal bone','frontal':'frontal bone','parietal':'parietal bone','occipital':'occipital bone','temporal':'temporal bone',
     'incisive':'incisive bone','temporal line':'temporal lines','canine':'canine tooth','incisors':'incisor teeth','condyloid process':'condylar process',
     'superior fourth premolar':'superior shearing tooth','fossa for lacrimal sac':'fossa for the lacrimal sac','alveolar foramina':'alveolar canals',
     'canal for trigeminal nerve':'canal for the trigeminal nerve','petrous part of temporal':'petrous part (temporal bone)',
     'base of stapes in vestibular window':'vestibular window','mandible':'mandibles','zygomatic process of temporal':'zygomatic process (temporal bone)',
     'tympanohyoid cartilage':'tympanohyoid cartilage','dorsal nasal concha':'dorsal nasal concha','ventral nasal concha':'ventral nasal concha',
     'lingual surface of crown':'lingual surface','hard palate':'hard palate','sublingual gland':'sublingual gland','mandibular gland':'mandibular salivary gland',
     'parotid gland':'parotid salivary gland','zygomatic gland':'zygomatic salivary gland','lacrimal gland':'lacrimal gland','frenulum':'lingual frenulum',
     'duct of lateral nasal gland':'lateral nasal gland','deep facial':'deep facial vein','entrance to maxillary recess':'maxillary recess',
     'semicircular canals':'inner ear','cochlear duct':'inner ear'}
DERIVE=[({'malleus','incus','stapes'},'ossicles'),({'tympanic bulla'},'tympanic part (temporal bone)'),({'hypophyseal fossa','dorsum sellae'},'sella turcica')]   # Nov 8
def term_for(label,lab):
    L=B.norm(re.sub(r'\(.*?\)','',label)); L=B.norm(SYN.get(L,L)) if L in SYN else L
    for t,al,_ in P4BOLD[lab]:
        if any(L==B.norm(a) for a in al): return t
    return None
def cards(pdf,lab,prefix):
    out=[]
    for k,f in enumerate(G.run(pdf)):
        if not f['caption']: continue
        nums=[];seen=set()
        for i,l in enumerate(f['labels']):
            t=term_for(l['text'],lab)
            if t and t not in seen: seen.add(t); nums.append((len(nums)+1,i,t))
        if not nums: continue
        names={t for *_,t in nums}; extra=[d for need,d in DERIVE if need&names and d in [x for x,_,_ in P4BOLD[lab]] and d not in names]
        q=f'assets/{prefix}_{k}q.jpg'; a=f'assets/{prefix}_{k}a.jpg'
        G.render(pdf,f,q,a,[(n,i) for n,i,_ in nums],dpi=220)
        fig=re.match(r'(Fig\.\s*[\d-]+[A-Z]?)',f['caption']); fig=fig.group(1) if fig else 'Figure'
        nm=''.join(f'<div class="nm">#{n} · {E(t[0].upper()+t[1:])}</div>' for n,_,t in nums)+''.join(f'<div class="fx"><b>Also shows:</b> {E(d)}</div>' for d in extra)
        out.append(dict(name=fig,terms=[t for *_,t in nums]+extra,html=B.card(f'Name #1–#{len(nums)}' if len(nums)>1 else 'Name #1',
            f'📖 lab guide · {f["caption"][:70]}',q,nm,[],a)))
    return out
def fill(best,diagrams):
    """diagrams go in ⭐ only when they add a bold term no photo shows; the rest → 📚 Extra"""
    have={t for c in best if '📖' not in c['html'][:400] for t in c['terms']}; add=[];rest=[]
    for c in sorted(diagrams,key=lambda c:-len(set(c['terms'])-have)):
        new=set(c['terms'])-have
        (add if new else rest).append(c); have|=new
    return best+add,rest
