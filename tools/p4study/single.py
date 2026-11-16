"""Per-term single-label images for the Bold Term Study Photos (made by Claude, Nov 16)."""
import sys,os,re
sys.path.insert(0,'/home/claude/repo/tools'); sys.path.insert(0,'/home/claude/studysheets')
import pymupdf as fz
from iso import isolate
A='/mnt/user-data/attachments/31594bc3-9d6f-5c02-a55e-32953ff4d455/'
GPDF={'p4g28':(A+'f954b1d8-Lab_28.pdf',28),'p4g28b':(A+'f954b1d8-Lab_28.pdf',29),'p4g29':(A+'288bd0ef-Lab_29.pdf',29),'p4g29x':(A+'288bd0ef-Lab_29.pdf',31),
      'p4g30':(A+'4999cb83-Lab_30.pdf',30),'p4g31':(A+'f22d97f5-Lab_31.pdf',31),'p4g32':(A+'f870d29f-Lab_32.pdf',32)}
OUT='/home/claude/studysheets/single/'; os.makedirs(OUT,exist_ok=True)
_G={}
def guide(img,term):
    m=re.match(r'assets/(p4g\d+[a-z]?)_(\d+)[qa]\.jpg',img)
    if not m or m.group(1) not in GPDF: return None
    pre,k=m.group(1),int(m.group(2)); pdf,lab=GPDF[pre]
    import guidefigs as G, p4guide
    if pdf not in _G: _G[pdf]=G.run(pdf)
    f=_G[pdf][k]; rects=[fz.Rect(l['rect']) for l in f['labels'] if p4guide.term_for(l['text'],lab)==term]
    if not rects: return None
    out=f'{OUT}{pre}_{k}_{re.sub(r"[^a-z0-9]+","_",term)}.png'
    isolate(pdf,f['page']+1,[rects[0]],fz.Rect(f['box']),out,dpi=200); guide.boxes=isolate.boxes
    lab_txt=[l['text'] for l in f['labels'] if p4guide.term_for(l['text'],lab)==term][0]
    return out,f'the only label on the drawing: "{lab_txt}"'
