# ECG strip + action-potential SVG generators for the Systems lecture practice exams.
# All drawings are original (computed waveforms), no copied images.
import math, random

PX_S = 125          # px per second (25 mm/s, 1 large box = 0.2 s = 25 px)
W = 750             # 6 seconds per strip

def _g(t, mu, sd, a):
    return a * math.exp(-((t - mu) ** 2) / (2 * sd * sd))

def _grid(w, h):
    s = [f'<rect x="0" y="0" width="{w}" height="{h}" fill="#fff6f8"/>']
    for x in range(0, w + 1, 5):
        c, sw = ('#f3b6c6', 0.9) if x % 25 == 0 else ('#fbdde5', 0.4)
        s.append(f'<line x1="{x}" y1="0" x2="{x}" y2="{h}" stroke="{c}" stroke-width="{sw}"/>')
    for y in range(0, h + 1, 5):
        c, sw = ('#f3b6c6', 0.9) if y % 25 == 0 else ('#fbdde5', 0.4)
        s.append(f'<line x1="0" y1="{y}" x2="{w}" y2="{y}" stroke="{c}" stroke-width="{sw}"/>')
    return ''.join(s)

# beat components: (kind, time_of_R)
# kinds: 'n' normal (P+QRS+T), 'p' P wave only, 'q' QRS+T with no P (junctional/escape narrow),
#        'v' wide bizarre ventricular complex (discordant T), 'a' premature atrial (abnormal P + normal QRS)

def _signal(t, beats, pr=0.10, base_noise=None, fib=None, vfib=None):
    y = 0.0
    for kind, tr, *opt in beats:
        o = opt[0] if opt else {}
        p_amp = o.get('pamp', 0.2)
        r_amp = o.get('r', 1.0)
        s_amp = o.get('s', -0.22)
        t_amp = o.get('t', 0.28)
        if kind in ('n', 'a'):
            prv = o.get('pr', pr)
            y += _g(t, tr - prv, 0.022, p_amp if kind == 'n' else p_amp * 0.8)
        if kind == 'p':
            y += _g(t, tr, 0.022, p_amp)
            continue
        if kind in ('n', 'a', 'q'):
            y += _g(t, tr - 0.025, 0.008, -0.08)
            y += _g(t, tr, 0.010, r_amp)
            y += _g(t, tr + 0.026, 0.009, s_amp)
            y += _g(t, tr + 0.22, 0.045, t_amp)
        if kind == 'v':
            y += _g(t, tr, 0.035, 1.25 * o.get('dir', 1))
            y += _g(t, tr + 0.07, 0.03, -0.35 * o.get('dir', 1))
            y += _g(t, tr + 0.30, 0.06, -0.55 * o.get('dir', 1))
    if fib:
        y += 0.045 * math.sin(2 * math.pi * 7.3 * t) + 0.035 * math.sin(2 * math.pi * 11.1 * t + 1.3) + 0.025 * math.sin(2 * math.pi * 5.2 * t + 0.4)
    if vfib:
        env = 0.55 + 0.35 * math.sin(2 * math.pi * 0.45 * t)
        y += env * (0.8 * math.sin(2 * math.pi * 4.6 * t + 0.7 * math.sin(2 * math.pi * 0.9 * t)) + 0.3 * math.sin(2 * math.pi * 7.9 * t + 2))
    return y

def strip(beats, label, h=150, mid=None, scale=55, w=W, **kw):
    mid = mid if mid is not None else h * 0.62
    pts = []
    for x in range(0, w + 1, 1):
        t = x / PX_S
        y = mid - scale * _signal(t, beats, **kw)
        pts.append(f'{x},{y:.1f}')
    path = 'M' + ' L'.join(pts)
    return (f'<figure class="ecg"><svg viewBox="0 0 {w} {h}" role="img" aria-label="ECG strip {label}">{_grid(w, h)}'
            f'<path d="{path}" fill="none" stroke="#222" stroke-width="1.4" stroke-linejoin="round"/>'
            f'<rect x="6" y="6" width="34" height="26" rx="5" fill="#fff" stroke="#7b42a0"/><text x="23" y="25" text-anchor="middle" font-size="17" font-weight="800" fill="#5d347e">{label}</text></svg>'
            f'<figcaption>ECG “{label}” · lead II · 25 mm/s · 1 large box = 0.2 s · strip = 6 s · swipe ↔ on phone</figcaption></figure>')

# ---------- rhythm builders (return beats list + kwargs) ----------
def regular(rate, start=0.25, end=6.0, kind='n', **o):
    rr = 60.0 / rate; b = []; t = start
    while t < end:
        b.append((kind, t, o)); t += rr
    return b

def rhythm(name, seed=1):
    random.seed(seed)
    if name == 'nsr':        return regular(110), {}
    if name == 'brady':      return regular(42, start=0.5), {}
    if name == 'tachy':      return regular(210, start=0.2), {}
    if name == 'rsa':
        b = []; t = 0.3
        for rr in [0.55, 0.5, 0.48, 0.55, 0.75, 0.9, 0.95, 0.8, 0.6, 0.52, 0.5, 0.6]:
            if t > 5.9: break
            b.append(('n', t)); t += rr
        return b, {}
    if name == 'sss':
        ts = [0.3, 0.85, 1.4, 4.1, 4.65, 5.2, 5.75]
        return [('n', t) for t in ts], {}
    if name == 'avb1':       return [(k, t, {'pr': 0.30}) for k, t, *_ in regular(60, start=0.75)], {}
    if name == 'mobitz1':
        b = []; t = 0.35
        prs = [0.12, 0.21, 0.30, None]
        i = 0
        while t < 5.9:
            pr = prs[i % 4]
            if pr is None: b.append(('p', t - 0.12))
            else: b.append(('n', t + pr - 0.12, {'pr': pr}))
            t += 0.75; i += 1
        return b, {}
    if name == 'mobitz2':
        b = []; t = 0.35; i = 0
        while t < 5.9:
            if i % 3 == 2: b.append(('p', t - 0.12))
            else: b.append(('n', t, {'pr': 0.12}))
            t += 0.6; i += 1
        return b, {}
    if name == 'avb3':
        b = [('p', t) for t in [x * 0.48 + 0.2 for x in range(13)] if t < 5.95]
        b += [('v', t, {'dir': 1}) for t in [0.78, 2.5, 4.2]]
        return b, {}
    if name == 'apc':
        ts = [0.3, 0.95, 1.6, 2.02, 3.0, 3.65, 4.3, 4.95, 5.6]
        b = [('n', t) for t in ts]
        b[3] = ('a', 2.02, {'pamp': 0.1, 'pr': 0.1})
        return b, {}
    if name == 'afib':
        ts = [0.3, 0.62, 1.1, 1.33, 1.85, 2.1, 2.62, 3.05, 3.3, 3.85, 4.2, 4.5, 5.05, 5.32, 5.8]
        return [('q', t) for t in ts], {'fib': True}
    if name == 'vpc':
        ts = [0.3, 0.95, 1.6, 3.0, 3.65, 4.3, 5.7]
        b = [('n', t) for t in ts] + [('v', 2.05, {'dir': 1}), ('v', 4.75, {'dir': 1})]
        return b, {}
    if name == 'vtach':
        b = [('n', 0.3)] + [('v', t, {'dir': 1}) for t in [0.85 + i * 0.3 for i in range(17)] if t < 5.95]
        return b, {}
    if name == 'vfib':       return [], {'vfib': True}
    raise ValueError(name)

def ecg(name, label, seed=1):
    beats, kw = rhythm(name, seed)
    return strip(beats, label, **kw)

# ---------- six-lead panel for mean electrical axis ----------
LEADS = [('I', 0), ('II', 60), ('III', 120), ('aVR', -150), ('aVL', -30), ('aVF', 90)]

def six_lead(axis, label):
    cells = []
    cw, ch = 240, 110
    for k, (nm, ang) in enumerate(LEADS):
        c = math.cos(math.radians(axis - ang))
        pc = math.cos(math.radians(55 - ang))
        r = 0.18 + max(c, 0) * 1.0
        s = -(0.18 + max(-c, 0) * 1.0)
        o = {'r': r, 's': s, 't': 0.28 * c, 'pamp': 0.13 * pc}
        beats = [('n', 0.42, o), ('n', 1.30, o)]
        col, row = k // 3, k % 3
        x0, y0 = col * (cw + 10), row * (ch + 8)
        pts = []
        for x in range(0, cw + 1):
            t = x / PX_S
            y = y0 + ch * 0.55 - 40 * _signal(t, beats)
            pts.append(f'{x0 + x},{y:.1f}')
        cells.append(f'<g><rect x="{x0}" y="{y0}" width="{cw}" height="{ch}" fill="#fff6f8" stroke="#f3b6c6"/>'
                     f'<path d="M{" L".join(pts)}" fill="none" stroke="#222" stroke-width="1.4"/>'
                     f'<text x="{x0 + 8}" y="{y0 + 20}" font-size="15" font-weight="800" fill="#5d347e">{nm}</text></g>')
    W2, H2 = 2 * cw + 10, 3 * (ch + 8)
    return (f'<figure class="ecg"><svg viewBox="0 0 {W2} {H2}" role="img" aria-label="six-lead ECG {label}">{"".join(cells)}</svg>'
            f'<figcaption>ECG “{label}” · six limb leads (one beat pattern shown per lead)</figcaption></figure>')

# ---------- action potentials with lettered sections ----------
def ap_vent(letters):
    """letters: dict phase->letter for phases 0..4 (ventricular cardiomyocyte)."""
    # piecewise curve
    path = ('M20 210 L120 210 '            # phase 4
            'L132 40 '                      # phase 0
            'Q140 32 152 62 '               # phase 1
            'C200 70 280 72 330 86 '        # phase 2 plateau
            'C365 100 385 200 410 208 '     # phase 3
            'L560 210')                     # phase 4
    pos = {4: (70, 232), 0: (112, 110), 1: (160, 38), 2: (250, 58), 3: (402, 150)}
    lab = ''.join(f'<circle cx="{x}" cy="{y-5}" r="13" fill="#fff" stroke="#7b42a0" stroke-width="1.5"/><text x="{x}" y="{y}" text-anchor="middle" font-size="15" font-weight="800" fill="#5d347e">{letters[p]}</text>' for p, (x, y) in pos.items())
    return (f'<figure class="ecg"><svg viewBox="0 0 580 250" role="img" aria-label="ventricular action potential with lettered sections">'
            f'<rect width="580" height="250" fill="#fbf6fe"/><line x1="20" y1="60" x2="560" y2="60" stroke="#ddd" stroke-dasharray="4 4"/>'
            f'<text x="565" y="64" font-size="11" fill="#999" text-anchor="end">0 mV</text>'
            f'<path d="{path}" fill="none" stroke="#3b1d66" stroke-width="3"/>{lab}</svg>'
            f'<figcaption>Depolarization profile of a regular (ventricular) cardiomyocyte</figcaption></figure>')

def ap_node(letters):
    """letters: dict for 'slow' (phase 4), 'up' (phase 0), 'down' (phase 3)."""
    path = ('M20 170 Q90 160 140 130 '      # phase 4 ramp
            'Q160 60 185 50 '               # phase 0
            'Q215 55 250 170 '              # phase 3
            'Q320 160 370 130 Q390 60 415 50 Q445 55 480 170 L560 165')
    pos = {'slow': (80, 140), 'up': (148, 80), 'down': (238, 105)}
    lab = ''.join(f'<circle cx="{x}" cy="{y-5}" r="13" fill="#fff" stroke="#7b42a0" stroke-width="1.5"/><text x="{x}" y="{y}" text-anchor="middle" font-size="15" font-weight="800" fill="#5d347e">{letters[p]}</text>' for p, (x, y) in pos.items())
    return (f'<figure class="ecg"><svg viewBox="0 0 580 210" role="img" aria-label="sinoatrial node action potential with lettered sections">'
            f'<rect width="580" height="210" fill="#fbf6fe"/><line x1="20" y1="130" x2="560" y2="130" stroke="#e0459a" stroke-dasharray="5 4"/>'
            f'<text x="565" y="124" font-size="11" fill="#e0459a" text-anchor="end">threshold</text>'
            f'<path d="{path}" fill="none" stroke="#3b1d66" stroke-width="3"/>{lab}</svg>'
            f'<figcaption>Depolarization profile of a nodal (pacemaker) cardiomyocyte</figcaption></figure>')
