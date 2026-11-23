"""'🔧 To fix' list for each Bold Term Study Photos page: terms sharing one photo (+ stand-in photos). Made by Claude, Nov 18."""
import re,html,collections
SAME={frozenset(x) for x in [('Dura mater','Pachymeninges'),('Middle vascular coat','Uvea'),('Zonule','Zonular fibers')]}
STANDIN_OLD={'Lumbosacral plexus':'whole-region UMN photo, no single label','Obliquus muscles':'whole-region photo, no single label','Dilator pupillae':'lecture slide still shows #1 and #2',
 'Crown':'teeth cartoon still shows other numbers','Root':'teeth cartoon still shows other numbers','Neck of tooth':'teeth cartoon still shows other numbers',
 'Vestibular surface':'color-coded teeth slide (all colors show)','Mesial contact surface':'color-coded teeth slide (all colors show)','Distal surface':'color-coded teeth slide (all colors show)'}
CSS='.fix{max-width:760px;margin:0 auto 18px;background:#fff;border:2px dashed #512888;border-radius:14px;padding:14px}.fix h2{font-family:Fraunces,Georgia,serif;color:#512888;margin:0 0 4px}.fix li{margin:6px 0}.fix .ok{color:#3a7d44}.fix .h{color:#4a3d57;font-size:.95em}'
def section(doc):
    g=collections.OrderedDict(); num={}
    for m in re.finditer(r'<div class="t" id="t(\d+)".*?<img loading="lazy" (?:src|data-k)="([^"?]+)[^"]*".*?<div class="n">(.*?)</div>',doc,re.S):
        n=html.unescape(m.group(3)); num[n]=m.group(1); g.setdefault(m.group(2),[]).append(n)
    rows=[]
    for v in g.values():
        if len(v)<2: continue
        tag=' <span class="ok">✓ same structure, fine</span>' if frozenset(v) in SAME else ''
        rows.append('<li>'+' · '.join(f'<a href="#t{num[x]}">#{num[x]} {html.escape(x)}</a>' for x in v)+f' share one photo{tag}</li>')
    grouped={x for v in g.values() if len(v)>1 for x in v}
    STANDIN={k:v for k,v in STANDIN_OLD.items() if 'Gross Anatomy notes' not in doc.split(f'<div class="n">{k}</div>')[0].rsplit('<div class="t"',1)[-1]}
    for n,why in STANDIN.items():
        if n in num and n not in grouped: rows.append(f'<li><a href="#t{num[n]}">#{num[n]} {html.escape(n)}</a>: {why}</li>')
    if not rows: return ''
    return (f'<div class="fix" id="fix"><h2>🔧 To fix</h2><div class="h">Swap in a better photo (from the pre-lab video or your own) so each term gets its own picture. Tap a term to jump to it.</div><ul>{"".join(rows)}</ul></div>')
def inject(doc):
    doc=re.sub(r'<div class="fix" id="fix">.*?</ul></div>','',doc,flags=re.S)
    s=section(doc)
    if not s: return doc
    if '.fix{' not in doc: doc=doc.replace('</style>',CSS+'</style>',1)
    anchor='<div class="todo" id="todo">' if '<div class="todo" id="todo">' in doc else '<footer>'
    doc=doc.replace(anchor,s+anchor,1)
    if '#fix"' not in doc.split('<div class="t"')[0]:
        doc=doc.replace('</details>',' <a href="#fix">🔧 To fix</a></details>',1)
    return doc
if __name__=='__main__':
    import sys,glob
    for f in sys.argv[1:]:
        d=open(f).read(); n=inject(d); open(f,'w').write(n); print(f.split('/')[-1],n.count('<li>')-d.count('<li>'),'fix rows')
