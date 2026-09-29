import sys,re; sys.path.insert(0,'.')
from deck import *
D='/home/claude/l14p/'; Y='📷 your photo'
def my(k,name,facts,clue='',q='Identify every highlighted structure.'):
    save_img(D+f'{k}q.jpg',f'site/assets/lab14_m{k}q.jpg',1600); save_img(D+f'{k}a.jpg',f'site/assets/lab14_m{k}a.jpg',2000)
    return img_card_facts(q,f'assets/lab14_m{k}q.jpg',name,clue,f'assets/lab14_m{k}a.jpg',facts,Y)
S1='Identify the highlighted structure.'
c={
'long':my('long','Longus capitis · longus colli',[("📍 Longus capitis?","Transverse processes of cervical vertebrae → muscular tubercle of the occipital bone (lateral to longus colli)"),("📍 Longus colli?","Ventral surfaces of the first 6 thoracic + cervical vertebrae → cervical vertebrae + atlas"),("💪 Action?","Flex the head and neck")],'Hypaxial neck flexors, ventral to the vertebrae'),
'scal':my('scal','Scalenus · serratus ventralis',[("📍 Scalenus?","C4–7 transverse processes → 1st rib, ribs 2–4 + 8–9 · inspiration"),("📍 Serratus ventralis?","Cervical transverse processes + ribs → serrated face of scapula · supports the trunk (the sling)")]),
'sdcr':my('sdcr','Serratus dorsalis cranialis',[("📍 Attachments?","Thoracolumbar fascia + median raphe → ribs 2–10"),("💪 Action?","Inspiration (pulls ribs craniolaterally)")],'',S1),
'sdca':my('sdca','Serratus dorsalis caudalis',[("📍 Attachments?","Thoracolumbar fascia → last ribs (12–13)"),("💪 Action?","Expiration (pulls ribs caudomedially)")],'Small; often damaged in dissection',S1),
'eic':my('eic','External intercostal mm.',[("↘️ Fiber direction?","CAUDOVENTRAL (hands in front pockets)"),("💪 Action?","Respiration (in + out)")],'',S1),
'iic':my('iic','Internal intercostal mm.',[("↙️ Fiber direction?","CRANIOVENTRAL (opposite of external)"),("💪 Action?","Respiration (in + out)")],'',S1),
'eao':my('eao','External abdominal oblique',[("↘️ Fiber direction?","CAUDOVENTRAL (same as external intercostals)"),("📍 Attachments?","Ribs + thoracolumbar fascia → linea alba + prepubic tendon, via an aponeurosis"),("⭐ Key fact?","Its aponeurosis forms the superficial inguinal ring + inguinal ligament; expiration")],'Most superficial abdominal muscle',S1),
'iao':my('iao','Internal abdominal oblique',[("↙️ Fiber direction?","CRANIOVENTRAL (same as internal intercostals)"),("📍 Attachments?","Thoracolumbar fascia + tuber coxae + inguinal ligament → last rib + linea alba (aponeurosis)")],'Deep to the external oblique',S1),
'ra':my('ra','Rectus abdominis',[("📍 Attachments?","Pubic (prepubic) tendon → sternum + first costal cartilages"),("⭐ Form?","Wide muscle with TENDINOUS INTERSECTIONS; fibers run parallel to midline (rectus)")],'',S1),
'ta':my('ta','Transversus abdominis · linea alba',[("↔️ Transversus fiber direction?","TRANSVERSE (perpendicular to the midline); deepest abdominal muscle"),("📍 Linea alba?","Midline fibrous raphe where the abdominal aponeuroses meet (xiphoid → pubis)")]),
'sir':my('sir','Superficial inguinal ring',[("📍 What is it?","A slit in the aponeurosis of the EXTERNAL abdominal oblique")],'',S1),
'il':my('il','Inguinal ligament',[("📍 What is it?","Caudal border of the external abdominal oblique aponeurosis")],'',S1),
'vl':my('vl','Vascular lacuna',[("📍 What passes?","Femoral vessels, between the inguinal ligament and the pelvis")],'',S1),
'dir':my('dir','Deep inguinal ring',[("📍 What bounds it?","Internal abdominal oblique, rectus abdominis, and inguinal ligament; not a distinct structure")],'',S1),
'spl':my('spl','Splenius',[("📍 Attachments?","Thoracolumbar fascia + spines of the first thoracic vertebrae → nuchal crest + mastoid part of temporal bone"),("💪 Action?","Extend/raise the head and neck")],'Large, flat, dorsal neck',S1),
'epax':my('epax','Epaxial systems: iliocostalis · longissimus · transversospinalis',[("🌿 Order lateral → medial?","I Love Tacos: Iliocostalis · Longissimus · Transversospinalis"),("💪 Action?","Both sides: extend the vertebral column · one side: bend laterally")],'Dorsal to the transverse processes; dorsal branches of spinal nn.'),
'semi':my('semi','Semispinalis capitis: a = biventer cervicis · b = complexus',[("⭐ Which is dorsal?","Biventer cervicis = dorsal (has tendinous intersections) · complexus = ventral"),("📍 Insertion?","Occipital bone")],'Part of the transversospinalis system'),
'semia':my('semia','Biventer cervicis (semispinalis capitis, dorsal part)',[],'Tendinous intersections cross it',S1),
'semib':my('semib','Complexus (semispinalis capitis, ventral part)',[],'',S1),
'nuch':my('nuch','Nuchal ligament · supraspinous ligament',[("📍 Nuchal ligament?","Spine of the axis → first thoracic spines; paired, yellow ELASTIC band; supports the head"),("📍 Supraspinous ligament?","Continues caudally along the tips of the thoracic + lumbar spines")])}
old=[]
for f in sorted(__import__('glob').glob('/home/claude/repo/gross-anatomy-lab14-main*.html'))+sorted(__import__('glob').glob('/home/claude/repo/gross-anatomy-lab14-extra*.html')):
    t=open(f).read(); t=re.sub(r'\?v=\d+','',t)
    name=re.search(r'<h1>Lab 14 · ([^<]+)</h1>',t).group(1)
    cs=[x.replace('class="card on"','class="card"') for x in re.findall(r'<section class="card[^"]*">.*?</section>',t,re.S)]
    old.append((name,cs,'main' in f))
main=[('Neck + thorax',[c[k] for k in ['long','scal','sdcr','sdca','eic','iic']]),('Abdominal wall',[c[k] for k in ['eao','iao','ra','ta']]),('Inguinal region',[c[k] for k in ['sir','il','vl','dir']]),('Epaxial + dorsal neck',[c[k] for k in ['epax','spl','semi','semia','semib','nuch']])]
extra=[('Course · '+n,cs) for n,cs,m in old if m]+[(n,cs) for n,cs,m in old if not m]
write_lab(14,'Lab 14 · Trunk + Neck',main,extra,len(re.findall('<section',open('site/gross-anatomy-lab14-terms.html').read())))
print(sum(len(g) for _,g in main),[ (n,len(g)) for n,g in extra])
