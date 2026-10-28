"""Practical 3 · pictures Bethany asked for by name → always in that lab's ⭐ (made by Claude).
PINS = {lab: [asset file names]}; copies each card (from any deck) into gross-anatomy-lab{n}-pins1.html, tagged 📌,
and links that page in the hub's 📚 Extra (<!--pins-->) so p3one.py can see + pin them. Run before p3one.py.
  python3 tools/p3pins.py"""
import sys,re,glob,os,time
sys.path.insert(0,'tools')
from bs4 import BeautifulSoup
from deck import page
V=str(int(time.time()))
PINS={22:['p3draw_omentum.svg','p3x_l22_94q.jpg'],16:['lab16_draw_disc_q.svg'],17:['p3s_Lab_17_Dee_s12q.jpg'],19:['p3s_fl2_44_0.jpg','p3draw_ulnarbr.svg','p3draw_cutarea.svg'],25:['p3x_l25_71q.jpg','p3x_l25_69q.jpg','p3x_l25_75rima.jpg','p3web_vulva_draw.jpg'],24:['p3s_l24_70_0.jpg','p3draw_pudendal.svg','p3s_l24_72_0.jpg','p3s_l24_35_0.jpg','p3s_l24_49_0.jpg','p3s_l24_67_0.jpg','umn_4626.jpg'],23:['p3s_abd_44q.jpg','p3s_l23b_26_0.jpg','p3s_l23b_28_0.jpg','p3s_l23b_30_0.jpg','p3s_l23m_9_0.jpg','p3s_l23b_24_0.jpg','p3s_l23b_46_0.jpg','p3s_l23b_50_0.jpg','p3s_l23b_56_0.jpg','umn_4555.jpg','p3draw_hepatic.svg','p3s_l23b_54_0.jpg','p3s_l23a_4_0.jpg'],21:['p3s_abd_1q.jpg','umn_4605.jpg','p3s_abd_7q.jpg','p3s_l24_39_0.jpg','p3s_l23b_30_0.jpg']}
pages=[f for f in sorted(glob.glob('gross-anatomy-*.html')) if not re.search(r'star\d|pins\d|mock|games|practical',f)]
css=re.search(r'<style>(.*?)</style>',open('gross-anatomy-lab22-best1.html').read(),re.S).group(1)
for n,want in PINS.items():
    got={}
    for f in pages:
        if len(got)==len(want): break
        h=open(f).read()
        if not any(w in h for w in want): continue
        for c in BeautifulSoup(h,'html.parser').select('section.card'):
            im=c.select_one('.pic img')
            if not im: continue
            k=im['src'].split('?')[0].split('/')[-1]
            if k in want and k not in got:
                tg=c.select_one('.tagline')
                if tg and '📌' not in tg.get_text(): tg.string=tg.get_text()+' · 📌 always in ⭐'
                got[k]=str(c)
    cs=[got[k] for k in want if k in got]
    fn=f'gross-anatomy-lab{n}-pins1.html'; hubf=f'gross-anatomy-lab{n}-images.html'
    pg=page(f'Lab {n} · 📌 Pictures you asked for',f'{len(cs)} cards',''.join(cs).replace('class="card"','class="card on"',1),back=f'{hubf}?v={V}')
    open(fn,'w').write(re.sub(r'<style>.*?</style>',lambda _:f'<style>{css}</style>',pg,count=1,flags=re.S))
    h=open(hubf).read(); h=re.sub(r'<!--pins-->.*?<!--/pins-->','',h,flags=re.S)
    link=f'<!--pins--><a href="{fn}?v={V}">📌 Pictures you asked for<span>{len(cs)} cards</span></a><!--/pins-->'
    m=re.search(r'(<div class="sec more">.*?)(</div>)',h,re.S); h=h[:m.end(1)]+link+h[m.end(1):]; open(hubf,'w').write(h)
    print(n,len(cs),'of',len(want),[k for k in want if k not in got])
