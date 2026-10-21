# Shared helpers for the "Label It" decks (made by Claude): l17labels.py, abd1labels.py, l22labels.py.
# Erase tricks come from l18trace.py (whiten text strokes on white) and l23ductus.py (inpaint + grain on textures).
import cv2, os, subprocess, numpy as np

def page_png(pdf, n, tmp, dpi=200):
    os.makedirs(tmp, exist_ok=True); out = f'{tmp}/p{n}_{dpi}'
    if not os.path.exists(out + '.png'):
        subprocess.run(['pdftoppm', '-r', str(dpi), '-png', '-f', str(n), '-l', str(n), '-singlefile', pdf, out], check=True)
    return cv2.imread(out + '.png')

def dark(s, thr=150):  # dark/black/grey text strokes
    return s.max(2) < thr

def red(s):  # red or dark-red text / arrows
    r, g, b = s[..., 2].astype(int), s[..., 1].astype(int), s[..., 0].astype(int)
    return (r > 120) & (g < 110) & (b < 110)

def nonwhite(s, thr=225):
    return s.min(2) < thr

def whiten(im, boxes, test=dark, halo=3, near=True, color=None):
    """Text on a plain background: turn only the strokes (plus halo) white (or color='auto' = box border median)."""
    for b in boxes:
        x0, y0, x1, y1 = map(int, b); sub = im[y0:y1, x0:x1]
        col = 255 if color is None else (np.median(np.concatenate([sub[0], sub[-1], sub[:, 0], sub[:, -1]]), axis=0) if color == 'auto' else color)
        m = cv2.dilate(test(sub.astype(int)).astype(np.uint8), np.ones((3, 3), np.uint8), iterations=halo)
        sub[m > 0] = col
        if color is not None: continue
        if not near: continue
        c = sub.astype(int); nr = cv2.dilate(m, np.ones((3, 3), np.uint8), iterations=4) > 0
        sub[nr & (c.min(2) > 150) & ((c.max(2) - c.min(2)) < 45)] = 255

def clean(im, box, thr=228, sat=30):
    """Snap near-white, unsaturated pixels (JPEG noise, faint label ghosts) to pure white inside box."""
    x0, y0, x1, y1 = map(int, box); sub = im[y0:y1, x0:x1]; c = sub.astype(int)
    sub[(c.min(2) > thr) & ((c.max(2) - c.min(2)) < sat)] = 255

def yellow(s):
    r, g, b = s[..., 2].astype(int), s[..., 1].astype(int), s[..., 0].astype(int)
    return (r > 170) & (g > 170) & (b < 150) & (abs(r - g) < 60)

def keep_only(im, box, keep):
    """Blank a box to white except pixels matching keep() (grown by 2 px to save anti-aliased edges)."""
    x0, y0, x1, y1 = map(int, box); sub = im[y0:y1, x0:x1]
    k = cv2.dilate(keep(sub.astype(int)).astype(np.uint8), np.ones((3, 3), np.uint8), iterations=2) > 0
    sub[~k] = 255

def fill(im, boxes, color=None):
    """Repaint a whole box with its border median (or a given BGR colour)."""
    for b in boxes:
        x0, y0, x1, y1 = map(int, b); sub = im[y0:y1, x0:x1]
        c = color if color is not None else np.median(np.concatenate([sub[0], sub[-1], sub[:, 0], sub[:, -1]]), axis=0)
        im[y0:y1, x0:x1] = c

def inpaint(im, boxes, test=dark, grow=3, radius=9, grain=0, full=False):
    """Text over a drawing/texture: inpaint the strokes (or the full box) and optionally re-add grain."""
    H, W = im.shape[:2]; mask = np.zeros((H, W), np.uint8)
    for b in boxes:
        x0, y0, x1, y1 = map(int, b)
        if full: mask[y0:y1, x0:x1] = 255
        else: mask[y0:y1, x0:x1] |= (test(im[y0:y1, x0:x1].astype(int)) * 255).astype(np.uint8)
    if grow: mask = cv2.dilate(mask, np.ones((3, 3), np.uint8), iterations=grow)
    out = cv2.inpaint(im, mask, radius, cv2.INPAINT_TELEA)
    if grain:
        rng = np.random.default_rng(1); noise = rng.normal(0, grain, out.shape[:2])
        m = mask > 0; o = out.astype(float); o[m] += noise[m][:, None]; out = np.clip(o, 0, 255).astype(np.uint8)
    im[:] = out

def card(im, out, crop, labels, title, hint, q=90, scale=1.0, white=False):
    """labels: [(name, (x, y))] in page pixels; crop=(x0,y0,x1,y1). white=True snaps the near-white background clean."""
    x0, y0, x1, y1 = crop
    if white: clean(im, crop)
    c = im[y0:y1, x0:x1]
    if scale != 1.0: c = cv2.resize(c, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC if scale > 1 else cv2.INTER_AREA)
    H, W = y1 - y0, x1 - x0
    cv2.imwrite(f'assets/{out}.jpg', c, [cv2.IMWRITE_JPEG_QUALITY, q])
    return dict(title=title, q=hint, img=f'assets/{out}.jpg',
                labels=[dict(n=n, p=[round((x - x0) / W * 100, 2), round((y - y0) / H * 100, 2)]) for n, (x, y) in labels])

def preview(cardd, path):
    """Debug: draw the numbered badges onto the output image so placement can be checked by eye."""
    im = cv2.imread(cardd['img']); H, W = im.shape[:2]
    for i, l in enumerate(cardd['labels']):
        x, y = int(l['p'][0] / 100 * W), int(l['p'][1] / 100 * H)
        cv2.circle(im, (x, y), 15, (168, 95, 224), -1)
        cv2.putText(im, str(i + 1), (x - 9 if i < 9 else x - 14, y + 7), 0, 0.6, (255, 255, 255), 2)
    cv2.imwrite(path, im)
