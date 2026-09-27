import sys; sys.path.insert(0,'.')
from deck import *; from oia_pelvic import OIA
L12=["Quadriceps femoris","Iliopsoas","Cranial tibial","Long digital extensor","Fibularis longus","Gastrocnemius","Superficial digital flexor","Deep digital flexor","Popliteus"]
O={k:OIA[k] for k in L12}
D='/home/claude/l12/'; Sg='📚 course slide · Lab 12 Distal Pelvic Limb'
def mk(pn,qq,name,m,clue=''):
    save_img(D+f's{pn}q.jpg',f'site/assets/lab12_s{pn}q.jpg',1600); save_img(D+f's{pn}a.jpg',f'site/assets/lab12_s{pn}a.jpg',1600)
    return img_card2(qq,f'assets/lab12_s{pn}q.jpg',name,clue,f'assets/lab12_s{pn}a.jpg',m,O,Sg)
H='Identify the highlighted structure.'
c={3:mk(3,H,'Rectus femoris (quadriceps femoris)',['Quadriceps femoris'],'Only quad head that crosses the hip → also flexes the coxal joint'),
4:mk(4,H,'Vastus medialis (quadriceps femoris)',['Quadriceps femoris']),
5:mk(5,H,'Vastus lateralis (quadriceps femoris)',['Quadriceps femoris']),
6:mk(6,H,'Vastus intermedius (quadriceps femoris)',['Quadriceps femoris'],'Deep, on the cranial femur; seen after reflecting rectus femoris'),
8:mk(8,H,'Patella',[],'Sesamoid bone in the quadriceps insertion'),
10:mk(10,H,'Patellar ligament',[],'Patella → tibial tuberosity'),
12:mk(12,H,'Iliopsoas',['Iliopsoas'],'= psoas major + iliacus'),
14:mk(14,H,'Iliacus (part of iliopsoas)',['Iliopsoas']),
16:mk(16,H,'Psoas major (part of iliopsoas)',['Iliopsoas']),
19:mk(19,H,'Crural extensor retinaculum',[],'Oblique band, distal fibula → tibia; holds cranial tibial + long digital extensor tendons'),
21:mk(21,H,'Tarsal extensor retinaculum',[],'In the deep crural fascia at the tarsus; holds the long digital extensor tendon'),
23:mk(23,H,'Cranial tibial',['Cranial tibial']),
25:mk(25,H,'Long digital extensor',['Long digital extensor'],'4 tendons to digits II–V'),
27:mk(27,H,'Fibularis longus',['Fibularis longus'],'Lies caudal to the long digital extensor'),
29:mk(29,H,'Gastrocnemius, lateral head',['Gastrocnemius']),
30:mk(30,H,'Gastrocnemius, medial head',['Gastrocnemius']),
32:mk(32,H,'Common calcanean tendon',[],'Gastrocnemius + SDF (+ biceps femoris, semitendinosus, gracilis via fascia)'),
34:mk(34,H,'Superficial digital flexor',['Superficial digital flexor'],'Its tendon caps the tuber calcanei'),
35:mk(35,H,'Calcaneal bursa',[],'Over the tuber calcanei, under the SDF tendon'),
38:mk(38,H,'Deep digital flexor',['Deep digital flexor']),
40:mk(40,H,'Lateral digital flexor (head of the deep digital flexor)',['Deep digital flexor']),
42:mk(42,H,'Medial digital flexor (head of the deep digital flexor)',['Deep digital flexor']),
44:mk(44,H,'Popliteus',['Popliteus'],'Popliteal sesamoid lies in its tendon; tendon passes deep to the lateral collateral ligament')}
main=[('Quadriceps + patella',[c[k] for k in [3,4,5,6,8,10]]),('Iliopsoas + craniolateral crus',[c[k] for k in [12,14,16,19,21,23,25,27]]),('Caudal crus',[c[k] for k in [29,30,32,34,35,38,40,42,44]])]
T=[("Quadriceps femoris: 4 heads?","Rectus femoris · vastus lateralis · vastus intermedius · vastus medialis"),("Which quad head also flexes the hip, and why?","Rectus femoris: the only head that originates on the ilium (crosses the hip)"),("What attaches the patella to the tibia?","Patellar ligament (to the tibial tuberosity)"),("Iliopsoas = which 2 muscles? Insertion + action?","Psoas major + iliacus · lesser trochanter · flex the coxal joint"),("Name the 4 superficial fasciae of the distal pelvic limb (bold).","Superficial crural · superficial tarsal · superficial metatarsal · superficial digital fascia"),("Deep crural fascia = continuation of what?","The medial + lateral femoral fasciae; covers the leg muscles"),("Crural vs tarsal extensor retinaculum: which tendons?","Crural: cranial tibial + long digital extensor · Tarsal: long digital extensor only"),("Craniolateral crus group action (pelvic limb)?","FLEX the tarsus, EXTEND the digits (opposite pattern from the forelimb!)"),("Caudal crus group action?","EXTEND the tarsus, FLEX the digits"),("Common calcanean tendon contributors?","Gastrocnemius + SDF (main) · biceps femoris, semitendinosus, gracilis (via fascia)"),("Where is the calcaneal bursa?","Over the tuber calcanei, under the SDF tendon cap"),("DDF (pelvic): which named parts are bold?","Lateral digital flexor + medial digital flexor"),("Flexor retinaculum (pelvic limb): what does it hold?","The deep digital flexor tendon on the medial tarsus"),("Popliteal sesamoid: where, and what's unique about the popliteus tendon?","In the popliteus tendon, near the caudal lateral tibial condyle; tendon passes DEEP to the lateral collateral lig"),("Which muscle rotates the paw medially? Laterally?","Medially: fibularis longus · Laterally: cranial tibial"),("Long digital extensor origin (trap)?","Extensor fossa of the FEMUR, so it also extends the stifle"),("SDF (pelvic) inserts where?","Tuber calcanei + bases of the middle phalanges"),("Fibularis brevis: 'brevis' means?","Short")]
TT=[text_card2(q,a,'🧠 Concept / integration') for q,a in T]; TT[0]=TT[0].replace('class="card"','class="card on"',1)
open('site/gross-anatomy-lab12-terms.html','w').write(page('Lab 12 · No-Image Terms',f'{len(TT)} cards · fascia + concepts',''.join(TT)))
write_lab(12,'Lab 12 · Distal Pelvic Limb',main,[],len(TT))
print(sum(len(g) for _,g in main),len(TT))
