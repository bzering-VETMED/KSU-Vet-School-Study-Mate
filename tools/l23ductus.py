# L23 ductus deferens path deck (made by Claude). Names come from the 10/19 L23 transcript; prostate from the L23 slides.
# Run from repo root: python3 tools/l23ductus.py /path/to/IMG_4707.jpeg /path/to/IMG_4708.jpeg
import cv2, sys, os, numpy as np
sys.path.insert(0, os.path.dirname(__file__)); import tracer as T
a_src, b_src = sys.argv[1:3]
def wipe(im, boxes, thr=185):  # inpaint number strokes incl. their grey anti-aliasing, then re-add stipple grain so no smooth patch shows
    H, W = im.shape[:2]; mask = np.zeros((H, W), np.uint8)
    for (x0, y0, x1, y1) in boxes:
        sub = im[y0:y1, x0:x1].astype(int); mask[y0:y1, x0:x1] |= ((sub.max(2) < thr) * 255).astype(np.uint8)
    mask = cv2.dilate(mask, np.ones((3, 3), np.uint8), iterations=3)
    out = cv2.inpaint(im, mask, 9, cv2.INPAINT_TELEA)
    rng = np.random.default_rng(1); noise = rng.normal(0, 9, out.shape[:2])
    m = mask > 0; out = out.astype(float); out[m] += noise[m][:, None]
    return np.clip(out, 0, 255).astype(np.uint8)

def card(src, out, erase, crop, labels, title, hint, thr=185):
    im = wipe(cv2.imread(src), erase, thr)
    x0, y0, x1, y1 = crop; im = im[y0:y1, x0:x1]
    H, W = im.shape[:2]; cv2.imwrite(f'assets/{out}.jpg', im, [cv2.IMWRITE_JPEG_QUALITY, 90])
    return dict(title=title, q=hint, img=f'assets/{out}.jpg',
                labels=[dict(n=n, p=[round((x - x0) / W * 100, 2), round((y - y0) / H * 100, 2)]) for n, (x, y) in labels])

A = card(a_src, 'l23_ductus_lateral',
         [(335, 55, 398, 128), (452, 472, 508, 543), (562, 532, 632, 608), (968, 448, 1068, 522), (682, 798, 742, 872), (866, 878, 934, 952)],
         (82, 30, 1356, 1180),
         [("Testis", (900, 985)),
          ("Epididymis (head → body → tail; the tail continues as the ductus deferens)", (1010, 812)),
          ("Ductus deferens (starts coiled, then straightens; runs in the spermatic cord through the inguinal canal)", (472, 640)),
          ("Ductus deferens enters the abdomen at the vaginal ring, then loops OVER the ureter to the dorsal bladder", (430, 205)),
          ("Ureter (enters the dorsal aspect of the bladder)", (150, 115)),
          ("Urinary bladder", (190, 560)),
          ("Prostate (slides; lecture continues Wednesday)", (745, 205))],
         "Ductus deferens · lateral view (cranial = left)",
         "Start at the testis and follow the sperm out to the bladder. Name each structure before you tap.")
B = card(b_src, 'l23_ductus_dorsal',
         [(488, 178, 528, 222), (252, 278, 293, 328), (705, 308, 762, 352), (678, 383, 714, 427), (387, 423, 443, 472), (422, 672, 468, 722),
          (492, 962, 538, 1008), (412, 1268, 453, 1322), (327, 1188, 383, 1258), (557, 1238, 608, 1298), (337, 1018, 408, 1068),
          (182, 548, 228, 602), (167, 1113, 218, 1168), (772, 722, 813, 772), (822, 1048, 868, 1098), (327, 638, 378, 692),
          (832, 1148, 875, 1203), (687, 748, 738, 803), (637, 623, 685, 672)],
         (78, 100, 985, 1396),
         [("Urinary bladder", (500, 240)),
          ("Ureter (grey tube, enters the dorsal bladder)", (255, 380)),
          ("Ductus deferens (pink; crosses over the ureter)", (358, 470)),
          ("Genital fold (yellow; serous fold the 2 ductus deferens enter)", (505, 405)),
          ("Prostate (slides; lecture continues Wednesday)", (455, 712)),
          ("Urethra: the ductus deferens join it", (515, 900)),
          ("Ischiatic tuberosity (caudal landmark of the pelvis)", (195, 1170))],
         "Ductus deferens · dorsal view of the bladder (cranial = top)",
         "Both ductus deferens come up to the dorsal bladder. Where do they enter, and what do they join?", thr=256)
TEXT = [
    ("Trace a sperm cell from where it is made to the ductus deferens.",
     ["Seminiferous tubules", "Straight tubules", "Rete testis", "Efferent ductules", "Head of the epididymis",
      "Body of the epididymis", "Tail of the epididymis", "Ductus deferens"]),
    ("Trace the ductus deferens from the tail of the epididymis to the urethra.",
     ["Tail of the epididymis", "Ductus deferens runs cranially along the dorsomedial border of the testis",
      "Through the inguinal canal (superficial → deep inguinal ring) in the spermatic cord",
      "Enters the abdominal cavity at the vaginal ring", "Crosses over the ureter",
      "Enters the genital fold (female equivalent: mesometrium)", "Dorsal aspect of the bladder", "Joins the urethra"]),
    ("Trace testicular descent.",
     ["Testes start intra-abdominal, caudal to the kidneys", "Gubernaculum (its bulb shrinks) pulls the testis",
      "Deep inguinal ring", "Inguinal canal", "Superficial inguinal ring", "Scrotum",
      "Normal by ~6 weeks; cryptorchid if not down by 7 months (abdominal or inguinal; unilateral or bilateral)"]),
]
T.write('gross-anatomy-l23-ductus.html', 'Trace the Ductus Deferens',
        'Lecture 23 · names from the 10/19 lecture · tap to reveal along the path', [A, B], TEXT)
print('ok')
