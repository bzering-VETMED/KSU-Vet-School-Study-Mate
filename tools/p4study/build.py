"""Bethany's personal study sheets: one HTML per lab, every bold term + one app photo + one study sentence. Not part of the app."""
import re,sys,html,base64,io,json,os
sys.path.insert(0,'/home/claude/repo/tools')
import p4lab26 as B
from p4bold import P4BOLD
from PIL import Image
R='/home/claude/repo/'
E=html.escape
def cards(f):
    if not os.path.exists(R+f): return []
    t=open(R+f).read(); out=[]
    for c in re.findall(r'<section class="card".*?</section>',t,re.S):
        imgs=re.findall(r'<img src="([^"?]+)',c)
        ans=re.search(r'<div class="an">(.*)',c,re.S); ans=ans.group(1) if ans else ''
        lines=[html.unescape(re.sub('<[^>]+>','',x)).strip() for x in re.split(r'</div>',ans)]
        tag=re.search(r'class="tagline">(.*?)</span>',c); tag=html.unescape(tag.group(1)) if tag else ''
        q=re.search(r'<div class="q">(.*?)<span',c,re.S); q=html.unescape(re.sub('<[^>]+>','',q.group(1))) if q else ''
        out.append(dict(imgs=imgs,lines=[l for l in lines if l],tag=tag,q=q))
    return out
def find(L,term,cs,override):
    if term in override: return override[term]
    for pass_ in (0,1):
        for c in cs:
            if not c['imgs']: continue
            for ln in (c['lines'][:1] if pass_==0 else c['lines']):
                for part in re.split(r' · (?=#|Right|Top|Bottom)|(?<=\)) · ',ln) if pass_ else [ln]:
                    if term in B.terms_in(part,L):
                        m=re.match(r'(#\d+|Right \d+|Top-left \d+|Bottom-left \d+)',part.strip())
                        if pass_==1 and not m: continue
                        return dict(img=c['imgs'][0],where=(m.group(1) if m else None),q=c['q'],tag=c['tag'],cue=('highlighted on the photo' if 'highlighted' in c['q'] else 'at the arrow / probe' if 'arrow' in c['q'] or 'probe' in c['q'] else 'on the photo'))
    for c in cs:
        if c['imgs'] and any(term in B.terms_in(ln,L) for ln in c['lines']+[c['q']]):
            return dict(img=c['imgs'][-1] if len(c['imgs'])>1 else c['imgs'][0],where=None,q=c['q'],tag=c['tag'],cue='labeled on the photo')
    return None
APP=os.environ.get('APP')=='1'; V=os.environ.get('V','1')
APPDIR='/home/claude/repo/p4-study-photos/'
BACK=f'<a href="index.html?v={V}" style="display:inline-block;margin:0 0 10px;padding:8px 14px;border-radius:999px;background:#f3eafb;color:#65328c;font-weight:800;text-decoration:none">← Bold Term Study Photos</a>'
def imgsrc(p):
    if APP and not p.startswith('/'): return f'../{p}?v={V}'
    if APP and p.startswith('/home/claude/repo/'): return '../'+p[len('/home/claude/repo/'):]+f'?v={V}'
    im=Image.open(p if p.startswith('/') else R+p).convert('RGB'); im.thumbnail((1000,1000) if APP else (800,800))
    bio=io.BytesIO(); im.save(bio,'JPEG',quality=78 if APP else 70); b=bio.getvalue()
    if APP:
        import hashlib; k=hashlib.md5(b).hexdigest()[:12]; os.makedirs(APPDIR+'img',exist_ok=True)
        open(APPDIR+f'img/{k}.jpg','wb').write(b); return f'img/{k}.jpg?v={V}'
    return 'data:image/jpeg;base64,'+base64.b64encode(b).decode()
def b64(p):
    im=Image.open(p if p.startswith('/') else R+p).convert('RGB'); im.thumbnail((800,800))
    bio=io.BytesIO(); im.save(bio,'JPEG',quality=70); return base64.b64encode(bio.getvalue()).decode()
CSS='''body{font-family:Nunito,system-ui,sans-serif;background:#faf7fc;color:#2a1f33;margin:0;padding:16px}
h1{font-family:Fraunces,Georgia,serif;color:#512888;margin:4px 0}.sub{color:#6b5a7a;margin-bottom:16px}
.t{background:#fff;border-radius:14px;box-shadow:0 2px 8px #51288822;margin:0 auto 18px;max-width:760px;padding:14px}
.n{font-weight:800;font-size:1.25em;color:#512888}.n span{color:#D94F7F;margin-right:6px}
.w{display:inline-block;background:#D94F7F;color:#fff;border-radius:999px;padding:2px 10px;font-weight:700;font-size:.85em;margin:6px 0}
.s{font-size:1.05em;line-height:1.45;margin:8px 0 10px}img{width:100%;border-radius:10px}.src{font-size:.75em;color:#8a7a99;margin-top:4px}
.nav{max-width:760px;margin:0 auto 14px;font-size:.85em;line-height:1.9}.nav a{color:#512888;margin-right:8px}
footer{text-align:center;color:#8a7a99;font-size:.8em;margin:20px}'''
import hashlib
def dedupe(doc):
    imgs={}
    def rep(m):
        k=hashlib.md5(m.group(1).encode()).hexdigest()[:10]; imgs[k]=m.group(1); return f'<img loading="lazy" data-k="{k}" alt="">'
    if APP: return doc
    doc=re.sub(r'<img loading="lazy" src="data:image/jpeg;base64,([^"]+)">',rep,doc)
    js='<script>const I='+json.dumps(imgs)+';document.querySelectorAll("img[data-k]").forEach(e=>e.src="data:image/jpeg;base64,"+I[e.dataset.k]);</script>'
    return doc.replace('</body>',js+'</body>')
TODO_CSS='.todo{max-width:760px;margin:0 auto 18px;background:#fff;border:2px dashed #D94F7F;border-radius:14px;padding:14px}.todo h2{font-family:Fraunces,Georgia,serif;color:#512888;margin:0 0 4px}.todo label{display:flex;gap:10px;align-items:flex-start;padding:10px 0;border-top:1px solid #eee}.todo input{width:22px;height:22px;accent-color:#D94F7F;flex:none;margin-top:2px}.todo .h{color:#4a3d57;font-size:.95em;margin-top:3px}.todo b.tm{color:#512888}'
def todo_html(L,todo):
    if not todo: return ''
    rows=''.join(f'<label><input type="checkbox" data-k="L{L}-{i}"><div><b class="tm">{E(t)}</b><div class="h">{h}</div></div></label>' for i,(t,h) in enumerate(todo))
    js='<script>document.querySelectorAll(".todo input").forEach(c=>{try{c.checked=localStorage.getItem(c.dataset.k)==="1"}catch(e){};c.onchange=()=>{try{localStorage.setItem(c.dataset.k,c.checked?"1":"0")}catch(e){}}})</script>'
    return f'<div class="todo" id="todo"><h2>📷 Photograph at lab</h2><div class="h">These terms have only a drawing or slide stand-in above. Find them, snap a photo, tick them off.</div>{rows}</div>{js}'
def build(L,title,sent,override={},todo=None):
    cs=cards(f'gross-anatomy-lab{L}-bold.html')+cards(f'gross-anatomy-lab{L}-extra.html')
    items=[];miss=[]
    for i,(t,_,_) in enumerate(P4BOLD[L]):
        h=find(L,t,cs,override)
        if not h: miss.append(t)
        items.append((i+1,t,h))
    body=''.join(
        f'<div class="t" id="t{i}"><div class="n"><span>{i}.</span>{E(t[0].upper()+t[1:])}</div>'
        +(f'<div class="w">👉 {E(h["where"])} on the photo</div>' if h and h.get('where') else f'<div class="w">👉 {E(h.get("cue","highlighted / at the arrow"))}</div>' if h else '')
        +f'<div class="s">{sent.get(t,"✏️ (study sentence coming)")}</div>'
        +(f'<img loading="lazy" src="{imgsrc(h["img"])}"><div class="src">{E(h["tag"])}</div>' if h else '<div class="src">No photo in the app yet.</div>')
        +'</div>' for i,t,h in items)
    nav='<div class="nav">'+' '.join(f'<a href="#t{i}">{E(t)}</a>' for i,t,_ in items)+(' <a href="#todo">📷 Photograph at lab</a>' if todo else '')+'</div>'
    out=(APPDIR+f'lab{L}.html') if APP else f'/home/claude/studysheets/VAP806_Lab{L}_BoldTerms.html'
    open(out,'w').write(dedupe(f'<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Lab {L} Bold Terms</title><style>{CSS}{TODO_CSS}</style></head><body>{BACK if APP else ""}<h1>Lab {L}: {E(title)}</h1><div class="sub">{len(items)} bold terms · one photo + one study sentence each · VAP806 Practical 4</div>{nav}{body}{todo_html(L,todo)}<footer>🎀 Bethany · K-State CVM Class of 2030</footer></body></html>'))
    print(out,os.path.getsize(out)//1024,'KB · no photo:',miss,'· no sentence:',[t for _,t,_ in items if t not in sent])

def build_items(L,title,items,todo=None):
    """items: list of (term, img_path or None, cue, source, sentence)"""
    body=''.join(
        f'<div class="t" id="t{i}"><div class="n"><span>{i}.</span>{E(t[0].upper()+t[1:])}</div>'
        +(f'<div class="w">👉 {E(cue)}</div>' if cue else '')
        +f'<div class="s">{s}</div>'
        +(f'<img loading="lazy" src="{imgsrc(img)}"><div class="src">{E(src)}</div>' if img else '<div class="src">No photo yet.</div>')
        +'</div>' for i,(t,img,cue,src,s) in enumerate(items,1))
    nav='<div class="nav">'+' '.join(f'<a href="#t{i}">{E(t)}</a>' for i,(t,*_) in enumerate(items,1))+(' <a href="#todo">📷 Photograph at lab</a>' if todo else '')+'</div>'
    out=(APPDIR+f'lab{L}.html') if APP else f'/home/claude/studysheets/VAP806_Lab{L}_BoldTerms.html'
    open(out,'w').write(dedupe(f'<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Lab {L} Bold Terms</title><style>{CSS}{TODO_CSS}</style></head><body>{BACK if APP else ""}<h1>Lab {L}: {E(title)}</h1><div class="sub">{len(items)} bold terms · one photo + one study sentence each · VAP806 Practical 4</div>{nav}{body}{todo_html(L,todo)}<footer>🎀 Bethany · K-State CVM Class of 2030</footer></body></html>'))
    print(out,os.path.getsize(out)//1024,'KB')
