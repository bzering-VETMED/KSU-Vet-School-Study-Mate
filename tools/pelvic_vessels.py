# Renal, pelvic & reproductive vessel tracing deck (made by Claude). Text cards only.
# Sources: tools/terms/L22.json, L23.json, L24.json, ABD2.json + Lab 24 notes. Run from repo root.
import sys, os
sys.path.insert(0, os.path.dirname(__file__)); import tracer as T
TEXT = [
 ("Kidney: arteries, aorta → glomerulus (L22)",
  ["Abdominal aorta", "Renal artery (enters at the hilus)", "Interlobar arteries", "Arcuate arteries (arc at the corticomedullary junction)",
   "Interlobular arteries", "Afferent arteriole", "Glomerulus", "Efferent arteriole"]),
 ("Kidney: veins, cortex → heart (L22)",
  ["Interlobular veins", "Arcuate veins", "Interlobar veins", "Renal vein (leaves at the hilus)", "Caudal vena cava"]),
 ("Medulla blood supply (L22)", ["Straight arteries supply the medullary capillary plexus", "Straight veins drain it"]),
 ("Testis: blood supply (L23)",
  ["Testicular artery: direct branch of the abdominal aorta (left and right)", "Artery of the ductus deferens (internal iliac level)",
   "Testicular VEIN forms the pampiniform plexus around the artery (cools arterial blood)"]),
 ("Gonadal veins: left vs. right (L23, L24, Abdominal Cavity 2)",
  ["LEFT testicular/ovarian vein → left renal vein → caudal vena cava", "RIGHT testicular/ovarian vein → caudal vena cava directly",
   "Why: the left kidney is more caudal ('left is left behind')"]),
 ("Penis: trace the artery (L23)",
  ["Internal iliac artery", "Internal pudendal artery", "Ventral perineal artery (its last branch)", "→ becomes the artery of the penis",
   "Dorsal artery of the penis: dorsal surface", "Deep artery of the penis: corpus cavernosum", "Artery of the bulb of the penis: corpus spongiosum"]),
 ("Ovary & uterus: arteries (L24)",
  ["Ovarian artery: direct branch of the abdominal aorta", "Uterine branch (to the cranial uterine horn)", "Tubal branch (to the uterine tube)",
   "Internal pudendal artery → vaginal artery", "Vaginal artery → uterine artery", "Uterine artery anastomoses with the uterine branch of the ovarian artery",
   "Internal pudendal also gives: artery of the clitoris + artery of the vestibular bulb"]),
 ("Internal iliac artery: branches (Lab 24 guide)",
  ["Umbilical artery (rudimentary; remnant = round ligament of the bladder, in the lateral ligament)",
   "Terminates cranial to the sacroiliac joint as:", "Caudal gluteal artery (muscles outside the pelvis, caudal thigh)",
   "Internal pudendal artery (pelvic viscera + external genitalia)"]),
 ("Prostatic vs. vaginal artery (Lab 24 notes: homologous)",
  ["Male = prostatic artery; female = vaginal artery (old unisex name: urogenital artery)",
   "Both supply: ureter, urinary bladder (caudal vesical artery), urethra, rectum",
   "Female extra: uterine artery · Male equivalent: artery of the ductus deferens"]),
 ("Lymph drainage, male & female (L23, L24)",
  ["INTERNAL (testis, epididymis, prostate · ovary, uterus) → medial iliac lymph nodes",
   "Vagina & vestibule → hypogastric (+ lateral sacral) lymph nodes",
   "EXTERNAL (scrotum, prepuce, penis · vulva, clitoris) → superficial inguinal lymph nodes",
   "In lab: identify medial iliac + superficial inguinal only"]),
 ("Umbilical remnants (L22, L23)",
  ["Umbilical ARTERIES → round ligament of the bladder (in the LATERAL ligament)", "Umbilical VEIN → round ligament of the liver (falciform ligament)",
   "Round ligament of the UTERUS → gubernaculum remnant (different!)"]),
]
T.write('gross-anatomy-pelvic-vessels.html', 'Trace the Renal, Pelvic & Repro Vessels',
        'Lectures 22–24 · say each step, then tap to reveal in order', [], TEXT, back='gross-anatomy-lecture.html')
print('ok', len(TEXT))
