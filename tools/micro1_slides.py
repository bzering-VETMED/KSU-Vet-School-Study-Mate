# Slides Dr. Basel pulled up in lab (from lab transcripts) + where to find missing objective images
import sys,time,html,re
sys.path.insert(0,'tools'); import deck
E=html.escape; V=str(int(time.time()))
LABS=[
("🔬 Lab 1 · Microscopy & Cytology","No lab transcript (Lab 1 was 8/25–8/27). Slides below are from the Lab 1 objectives sheet.",
 [("Glass 59","Liver: nucleus, cytoplasm, first slide"),("Glass 4 / 7","Skin: planes of section"),("Glass 97","Mitosis"),("MH 126b","Liver: nucleus, cytoplasm, lipid/glycogen vacuoles"),("MH 031","Kupffer cells: phagocytosis"),("MH 024–026","Mesentery: macrophages"),("MH 211","Pancreas: secretory vesicles, RER basophilia"),("MH 112 / MHS 251","Fundic stomach: chief vs parietal cells"),("MH 219","Jejunum: secretory vesicles in gland cells"),("MH 091","Thick skin: lipid in fat cells"),("MH 015","Stages of mitosis")],
 [("Anaphase + telophase","MH 015 · Glass 97"),("Cross, oblique, tangential sections","Glass 4/7 skin · MH 219 jejunum"),("Glycogen inclusion","MH 126b liver"),("Macrophage with ingested material","MH 031 Kupffer cells · MH 024–026")]),
("🧫 Lab 2 · CT, Epithelium & Skin","Transcript 9/1–9/2: he spent 30–40 min on Glass slide 4 and covered most objectives on it.",
 [("Glass 4 ⭐","Thick skin (palmar / footpad): epidermis layers, dermis, sweat glands + ducts, epithelia. His favorite slide."),("Glass 7","Skin: more examples")],
 [("Transitional epithelium","MH 214 · Glass 66 bladder"),("Dense regular elastic CT","Glass 123 nuchal ligament"),("Hair follicle + hair bulb","MH 086c / 087b scalp · MH 090 thin skin"),("Arrector pili","MH 087b scalp · MH 090 thin skin"),("Apocrine sweat gland","MH 090 thin skin · MHS 258 recto-anal junction"),("Myoepithelial cells","Glass 4 · MH 091 thick skin")]),
("🦴 Lab 3 · Nerve, Cartilage & Bone","Transcript 9/8 (#15) + start of 9/15 (#16): mostly virtual slides.",
 [("MH 024","Mesentery: nerve vs vessel, perineurium"),("MH 091 / Glass 4","Thick skin: find nerves next to vessels"),("MH 059","Sympathetic ganglion: neuron cell bodies, satellite cells"),("MH 095","Submandibular gland: nerve/ganglion inside an organ"),("MH 046 ⭐","Articular cartilage → also used for the endochondral growth plate"),("VH 040","Ear: elastic cartilage (“look at the ear slide”)"),("MH 040","Intervertebral disc: fibrocartilage"),("MH 043","Cancellous vs compact bone"),("MHS 202","Ground bone: osteons, lacunae, canaliculi"),("MHS 242","Fetal (primate) face: intramembranous; osteoblasts, osteocytes, osteoclasts"),("MHS 287","Early bone development: bone collar, primary center")],
 [("Node of Ranvier","MH 052 peripheral nerve (longitudinal part) · Glass 138"),("Epineurium","MH 052 · Glass 104"),("Isogenous groups","MH 136 trachea · MH 038 epiglottis"),("Articular cartilage surface","MH 046 (the slide he used)"),("Perforating canal","MHS 202 · MH 044 ground bone")]),
("🫀 Lab 4 · Muscle, Heart & Circulation","Transcript 9/15 (#16): got through muscle + heart. Vessels weren’t reached in the recording, so those are from the objectives sheet.",
 [("MH 262","Skeletal muscle, cross section"),("MH 055","Skeletal muscle, longitudinal"),("MH 054","Cardiac muscle"),("MH 109","Esophagus: smooth vs skeletal muscle"),("MH 070 ⭐","Heart ventricles: epicardium, myocardium, endocardium"),("MHS 245","Purkinje fibers (epicardium torn off)"),("MH 071","Right atrium + ventricle, valve")],
 [("Epicardium + myocardium","MH 070 (not 245; epicardium is torn off there)"),("Capillary","MH 024–026 mesentery"),("Vein","MH 061–062 popliteal · MH 063 brachiocephalic · VH 062 vein valve"),("Internal + external elastic lamina","MH 061–062 popliteal artery · Glass 104"),("Endomysium / perimysium / epimysium","MH 262 · MHS 030"),("Elastic artery (extra practice)","MHS 244 · MH 063 carotid")]),
("🛡️ Lab 7 · Lymphatic","Lab is Tue 10/6, so there’s no transcript yet. Slides are from the Lab 7 objectives sheet. Send the transcript after lab and this updates.",
 [("Glass 35","Palatine tonsil"),("Glass 38","Spleen"),("Glass 121","Rectum (MALT)"),("MH 081a","Palatine tonsil"),("MH 076–077–078","Lymph node"),("MH 024–026","Mesentery: small lymph nodes"),("MH 084 / MHS 212 / MHS 293 · MH 085","Spleen"),("MH 079 · MHS 210","Thymus"),("MH 120 · MH 118","Ileum / small intestine: Peyer’s patches"),("MH 122 · MHS 221","Appendix"),("MH 123 · MHS 258","Colon / recto-anal junction: diffuse + nodular MALT")],
 [("Cortex, paracortex, medulla + medullary sinus","MH 076–077–078"),("Marginal zone; splenic cords vs sinuses","MH 084 / MHS 212 / MHS 293 · MH 085"),("Peyer’s patch","MH 120 ileum · MH 118")]),
]
def tbl(rows,h1,h2): return f'<div class="tw"><table><tr><td>{h1}</td><td><b>{h2}</b></td></tr>'+''.join(f'<tr><td>{E(a)}</td><td>{E(b)}</td></tr>' for a,b in rows)+'</table></div>'
body=''
for t,note,used,gaps in LABS:
    body+=f'<div class="sec main chk"><h2>{E(t)}</h2><p>{E(note)}</p><h3>🎙️ Slides he pulled up</h3>{tbl(used,"Slide","What he showed")}<h3>📷 Screenshot these (missing objective images → ⭐ main blocks)</h3>{tbl(gaps,"Need","Where to find it")}</div>'
css=deck.HUBCSS+'.sec h3{margin:12px 0 4px;color:#b0679a;font-size:16px}'
page=f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><title>Slides Dr. Basel used</title><style>{css}</style></head><body><div class="wrap"><a class="back" href="systems-lab-practical1.html?v={V}">← Back to Lab Practical 1</a><div class="hero"><h1>🎙️ Slides Dr. Basel used</h1><p>MH/MHS/VH = Histology Guide · Glass = your slide box · ⭐ = he spent the most time here</p></div>{body}</div></body></html>'
open('systems-lp1-slides.html','w').write(page)
p=open('systems-lab-practical1.html').read()
link=f'<a href="systems-lp1-slides.html?v={V}" style="display:block;margin:12px 0;padding:14px 16px;border-radius:18px;text-decoration:none;font-weight:900;color:#fff;background:linear-gradient(120deg,#6a3392,#e05fa8)">🎙️ Slides Dr. Basel used + where to screenshot</a>'
p=re.sub(r'<a href="systems-lp1-slides\.html[^>]*>.*?</a>','',p)
p=p.replace('<div class="grid">',link+'<div class="grid">',1)
open('systems-lab-practical1.html','w').write(p)
