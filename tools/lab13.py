import sys; sys.path.insert(0,'.')
from deck import *
D='/home/claude/l13/'; Sg='📚 course slide · Lab 13 Hindlimb Joints'
def mk(pn,name,facts,clue=''):
    save_img(D+f's{pn}q.jpg',f'site/assets/lab13_s{pn}q.jpg',1600); save_img(D+f's{pn}a.jpg',f'site/assets/lab13_s{pn}a.jpg',1600)
    return img_card_facts('Identify the highlighted structure.',f'assets/lab13_s{pn}q.jpg',name,clue,f'assets/lab13_s{pn}a.jpg',facts,Sg)
c={4:mk(4,'Ligament of the femoral head',[("📍 Attachments?","Fovea capitis of the femoral head → acetabular fossa")]),
6:mk(6,'Transverse acetabular ligament',[("📍 Where?","Spans the acetabular notch on the ventrocaudal acetabulum"),("⭐ Continues as…","The acetabular lip; deepens the acetabulum")]),
8:mk(8,'Acetabular lip',[("⚙️ Function?","Fibrocartilage rim that deepens the acetabulum; continuous with the transverse acetabular lig")]),
10:mk(10,'Medial femoropatellar ligament',[("📍 Attachments?","Patella ↔ medial gastrocnemial sesamoid (fabella); thin fascial band")]),
12:mk(12,'Lateral femoropatellar ligament',[("📍 Attachments?","Patella ↔ lateral gastrocnemial sesamoid (fabella)")]),
14:mk(14,'Medial meniscus',[("⭐ Why does it move less than the lateral?","Attached to the medial collateral ligament along its margin")],'Semilunar fibrocartilage'),
15:mk(15,'Lateral meniscus',[("⭐ Unique attachment?","Its caudal part attaches to the femur by the meniscofemoral ligament")]),
17:mk(17,'Cranial meniscotibial ligament (of the medial meniscus)',[("📍 Attachments?","Each meniscus → cranial + caudal intercondylar areas of the tibia (cranial + caudal meniscotibial ligs)")]),
19:mk(19,'Transverse ligament',[("📍 What does it connect?","The two menisci, across their cranial surface")]),
21:mk(21,'Meniscofemoral ligament',[("📍 Attachments?","Caudal part of the LATERAL meniscus → intercondylar fossa of the femur")]),
23:mk(23,'Medial collateral ligament (stifle)',[("📍 Attachments?","Medial epicondyle of femur → medial condyle of tibia"),("⭐ Key fact?","Fuses with the medial meniscus")]),
25:mk(25,'Lateral collateral ligament (stifle)',[("📍 Attachments?","Lateral epicondyle of femur → fibular head (runs over the popliteus tendon)")]),
27:mk(27,'Cranial cruciate ligament',[("📍 Tibial attachment?","Cranial intercondylar area of the tibia (named for the TIBIAL attachment)"),("⚙️ Function?","Prevents cranial drawer (tibia sliding cranially on the femur)")]),
28:mk(28,'Caudal cruciate ligament',[("📍 Tibial attachment?","Caudal intercondylar area (popliteal notch) of the tibia"),("⚙️ Function?","Prevents excessive caudal movement of the tibia on the femur")])}
main=[('Hip + patella',[c[k] for k in [4,6,8,10,12]]),('Menisci + their ligaments',[c[k] for k in [14,15,17,19,21]]),('Collaterals + cruciates',[c[k] for k in [23,25,27,28]])]
T=[("Symphysis pelvis: what is it?","Midventral union of the 2 hip bones (not dissected, but fair game)"),("Sacroiliac joint + its ligaments?","Ilium ↔ sacrum; supported by dorsal + ventral sacroiliac ligaments"),("Sacrotuberous ligament?","Sacrum → lateral angle of the ischiatic tuberosity"),("Coxal (hip) joint type?","Ball-and-socket: femoral head in the acetabulum"),("Cruciates are named for which bone's attachment?","The TIBIA"),("Cranial drawer sign means which ligament is torn?","Cranial cruciate ligament"),("Excessive caudal movement of the tibia (femur held still): inspect which ligament?","Caudal cruciate; cranial cruciate attaches at the cranial intercondylar area"),("Which meniscus moves LESS during flexion, and why?","Medial; attached to the medial collateral ligament"),("What connects the two menisci cranially?","Transverse ligament"),("What anchors the lateral meniscus to the femur?","Meniscofemoral ligament"),("Femoropatellar ligaments connect what?","Patella ↔ gastrocnemial sesamoids (fabellae)"),("Genual joint = ?","The stifle: femorotibial + femoropatellar (+ proximal tibiofibular)"),("Infrapatellar fat pad: why care?","Don't mistake it for joint effusion on stifle radiographs"),("Two tibiofibular joints?","Proximal: fibular head ↔ lateral tibial condyle · Distal: lateral malleolus ↔ distal tibia"),("Interosseous membrane (pelvic)?","Sheet between tibia + fibula across the interosseous space"),("Greatest movement of the tarsus?","Tarsocrural joint (tibial cochlea ↔ trochlea of the talus)"),("Long digital extensor originates where?","Extensor fossa of the femur")]
TT=[text_card2(q,a,'🧠 Concept') for q,a in T]; TT[0]=TT[0].replace('class="card"','class="card on"',1)
open('site/gross-anatomy-lab13-terms.html','w').write(page('Lab 13 · No-Image Terms',f'{len(TT)} cards · joints not dissected + concepts',''.join(TT)))
write_lab(13,'Lab 13 · Hindlimb Joints',main,[],len(TT))
print(sum(len(g) for _,g in main),len(TT))
