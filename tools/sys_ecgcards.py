# Build: Systems lecture · ECG flashcards (real Lecture 21–22 slide images + drawn strips + Arrhythmia Cases sheet)
# Run from repo root: python3 tools/sys_ecgcards.py   (needs /tmp/claude-0/ecgimg extracted slide images)
import os, sys, time, html, shutil
sys.path.insert(0, os.path.dirname(__file__))
import deck
from sys_practice_svg import ecg, six_lead, strip, rhythm
import numpy as np, cv2
from PIL import Image
E = html.escape; V = str(int(time.time()))
SRC = '/tmp/claude-0/ecgimg'; A = 'assets'
HUB = 'systems-lec-ecg-cards.html'

def jpg(src, key, w=1200, crop=None, inpaint=None):
    dst = f'{A}/ecg_{key}.jpg'
    im = Image.open(f'{SRC}/{src}').convert('RGB')
    if crop:
        W, H = im.size; im = im.crop(tuple(int(c * (W if i % 2 == 0 else H)) if c <= 1 else int(c) for i, c in enumerate(crop)))
    if inpaint:
        a = np.array(im)[:, :, ::-1].copy(); m = np.zeros(a.shape[:2], np.uint8)
        g = cv2.cvtColor(a, cv2.COLOR_BGR2GRAY)
        for x0, y0, x1, y1 in inpaint:
            sub = (g[y0:y1, x0:x1] < 120).astype(np.uint8) * 255
            m[y0:y1, x0:x1] = sub
        m = cv2.dilate(m, np.ones((3, 3), np.uint8), 2)
        a = cv2.inpaint(a, m, 3, cv2.INPAINT_TELEA); im = Image.fromarray(a[:, :, ::-1])
    if im.width < w: im = im.resize((w, int(im.height * w / im.width)), Image.LANCZOS)
    elif im.width > w: im = im.resize((w, int(im.height * w / im.width)), Image.LANCZOS)
    im.save(dst, quality=85); return dst

def svg(key, markup):
    dst = f'{A}/ecg_{key}.svg'
    s = markup[markup.index('<svg'):markup.index('</svg>') + 6].replace('<svg ', '<svg xmlns="http://www.w3.org/2000/svg" ', 1)
    open(dst, 'w').write(s); return dst

def C(q, img, name, facts, tag='', aimg=None):
    return deck.img_card_facts(q, img, name, '', aimg, facts, tag)

RATE = ('Rate + rhythm?', '')
B = {}
# ---------------- Block 1: real slide strips
B['📈 Slide strips 1'] = [
 C('Name the rhythm', jpg('im-020-020.png', 'nsr'), 'Normal sinus rhythm', [('P for every QRS? QRS for every P?', 'Yes and yes'), ('Rhythm rule?', 'R-R varies <10% = rhythmic')], 'LC21–22 slide 20'),
 C('Name the rhythm', jpg('im-020-021.png', 'rsa', inpaint=[(80, 120, 122, 140), (303, 138, 337, 157), (493, 133, 534, 152)]), 'Respiratory sinus arrhythmia',
   [('Cause?', 'Breathing changes vagal tone'), ('Common in?', 'Brachycephalic dogs'), ('Treat?', 'No (normal)')], 'LC21–22 slide 20'),
 C('Rate and rhythm?', jpg('im-014-015.png', 'rate165'), 'Slightly tachycardic (~165), arrhythmic', [('Arrhythmic means?', 'R-R varies >10%'), ('Normal dog rate?', '70–120 (60–180)')], 'LC21–22 slide 14'),
 C('Rate and rhythm?', jpg('im-014-016.png', 'rate144'), 'Slightly tachycardic (~144), rhythmic', [('Recorded at?', 'Lead II (slide: “often” 25 mm/s)'), ('Normal cat rate?', '120–140 (120–220)')], 'LC21–22 slide 14'),
 C('Name the rhythm', jpg('im-021-023.png', 'brady', w=900), 'Sinus bradycardia', [('3 pathologic H’s?', 'Hypothermia, hypothyroidism, hyperkalemia'), ('Drug causes?', 'β-blockers, Ca²⁺ blockers, digoxin, opioids'), ('Treat if unstable?', 'Atropine')], 'LC21–22 slide 21'),
 C('Name the rhythm', jpg('im-022-024.png', 'sss1'), 'Sick sinus syndrome', [('Key feature?', 'Pauses / sinus arrest'), ('Treat if syncope?', 'Pacemaker')], 'LC21–22 slide 22'),
 C('Name the rhythm', jpg('im-022-025.png', 'sss2'), 'Sick sinus syndrome', [('Causes?', 'SA node fibrosis, inherited, idiopathic'), ('May alternate with?', 'Atrial tachyarrhythmias')], 'LC21–22 slide 22'),
 C('Name the rhythm (look at the circles)', jpg('im-023-028.png', 'avb1'), '1st degree AV block', [('Key feature?', 'Long PR, nothing drops'), ('Treat?', 'None')], 'LC21–22 slide 23'),
 C('Name the rhythm', jpg('im-023-026.png', 'mob2'), '2nd degree AV block, Mobitz II', [('Key feature?', 'Same PR, sudden dropped QRS'), ('Treat?', 'Slide 23 (all AV blocks): none if mild · atropine if vagal · pacemaker if symptomatic advanced · ⚠️ Basel was inconsistent out loud about which Mobitz type is worse; use slide 23')], 'LC21–22 slide 23'),
 C('Name the rhythm', jpg('im-023-027.png', 'avb3'), '3rd degree AV block', [('Key feature?', 'P and QRS unrelated, slow escape'), ('Treat?', 'Pacemaker')], 'LC21–22 slide 23'),
 C('Name the rhythm', jpg('im-024-029.png', 'apc'), 'Atrial premature contraction (APC)', [('Key feature?', 'Early P, short T–P, normal QRS'), ('Treat?', 'Often none')], 'LC21–22 slide 24'),
 C('Name the rhythm', jpg('im-025-030.png', 'afib'), 'Atrial fibrillation', [('Key feature?', 'No P waves, irregularly irregular'), ('Treat?', 'Rate control: β-blocker, Ca²⁺ blocker, digoxin')], 'LC21–22 slide 25'),
 C('Name the odd beat', jpg('im-026-031.png', 'vpc1'), 'Ventricular premature contraction (VPC)', [('Key feature?', 'Wide, bizarre, no P, discordant T'), ('Electrolyte causes?', '↓K⁺, ↓Mg²⁺, acidosis')], 'LC21–22 slide 26'),
 C('Name what you see', jpg('im-026-032.png', 'vpc2'), 'VPCs in runs → ventricular tachycardia', [('VPCs can occur as?', 'Singles, couplets, runs')], 'LC21–22 slide 26'),
 C('Name the rhythm', jpg('im-027-033.png', 'vt1', w=900), 'Ventricular tachycardia', [('Unstable treatment?', 'Lidocaine, cardioversion'), ('Sustained means?', '>30 seconds')], 'LC21–22 slide 27'),
]
B['📈 Slide strips 2 + cases'] = [
 C('Name the rhythm', jpg('im-027-034.png', 'vt2'), 'Ventricular tachycardia', [('Rate?', '>100, wide QRS in a row'), ('Long-term option?', 'Antiarrhythmics, implantable defibrillator')], 'LC21–22 slide 27'),
 C('Name the rhythm', jpg('im-028-035.png', 'vf'), 'Ventricular fibrillation', [('Treat?', 'CPR + defibrillation (unsynchronized)'), ('Add-on drugs?', 'Amiodarone, lidocaine'), ('Electrolyte cause?', 'Hyperkalemia')], 'LC21–22 slide 28'),
 C('14-yr Westie, syncope, HR 20–200. Diagnosis?', jpg('im-002-001.png', 'westie'), 'Sick sinus syndrome', [('Treatment?', 'Pacemaker')], 'LC21–22 clinical case'),
 C('What is this, and why?', jpg('im-033-041.png', 'pacer', w=700), 'Pacemaker', [('Used for?', 'Refractory bradyarrhythmias'), ('Examples?', '2°/3° AV block, sick sinus syndrome')], 'LC21–22 slide 33'),
 C('Is the axis normal?', jpg('im-011-014.png', 'sixlead', w=900), 'Normal mean electrical axis', [('Quick check?', 'Lead II upright = normal'), ('Normally negative lead?', 'aVR'), ('Dog normal range?', '0° to +100°')], 'LC21–22 slide 11'),
 C('Fill every box: ion + drug class', jpg('im-031-037.png', 'apboxes', w=1000), 'See the answer slide', [('Phase 0?', 'Na⁺ in · class 1'), ('Phase 2?', 'Ca²⁺ in · class 4'), ('Phase 3?', 'K⁺ out · class 3'), ('Nodal phase 4?', 'HCN · class 0'), ('β-blocker?', 'Class 2 (slows nodal phase 4)')],
   'LC21–22 slide 31', aimg=jpg('hi-31.png', 'apboxes_ans', w=1200)),
]
CASES = [('1 · Apparently healthy dog', 'rsa', 'Sinus arrhythmia', [('P/QRS normal?', 'Yes, every P has a QRS'), ('Treat?', 'No')]),
         ('2 · Doberman with dilated cardiomyopathy', 'afib', 'Atrial fibrillation', [('Treat?', 'Yes: β-blocker (rate control)')]),
         ('3 · Boxer with arrhythmogenic right ventricular cardiomyopathy', 'vtach', 'Ventricular tachycardia', [('Treat?', 'Lidocaine')]),
         ('4 · Dog with an auscultated arrhythmia', 'sss', 'Sick sinus syndrome', [('Treat?', 'Pacemaker')]),
         ('5 · Dog with an auscultated arrhythmia', 'vpc', 'Ventricular premature contractions', [('Treat?', 'Long-term antiarrhythmic therapy')]),
         ('6 · Dog with a bradyarrhythmia', 'avb3', '3rd degree AV block', [('P for every QRS? QRS for every P?', 'Yes · no'), ('Treat?', 'Pacemaker')])]
for i, (stem, r, name, f) in enumerate(CASES, 1):
    B['📈 Slide strips 2 + cases'].append(C(f'Arrhythmia Case {stem}. Diagnosis?', svg(f'case{i}', ecg(r, 'C' + str(i))), name, f, 'Arrhythmia Cases sheet (strip redrawn)'))
# ---------------- Block 3: leads & axis
LEADS = [('I', '0°', 'Right fore (−) → left fore (+)'), ('II', '+60°', 'Right fore (−) → left hind (+)'), ('III', '+120°', 'Left fore (−) → left hind (+)'),
         ('aVR', '−150°', 'Right fore (+)'), ('aVL', '−30°', 'Left fore (+)'), ('aVF', '+90°', 'Left hind / foot (+)')]
lead_cards = []
for k, (nm, ang, how) in enumerate(LEADS):
    col, row = k % 3, k // 3
    f = [('Angle?', ang), ('Electrodes?', how)]
    if nm == 'I': f.append(('Electrode colors?', 'White right fore · black left fore · green right hind · red left hind'))
    if nm == 'aVR': f.append(('Normal QRS here?', 'Negative (wave goes away)'))
    lead_cards.append(C('Which lead is this?', jpg('im-009-012.png', f'lead{nm}', w=500, crop=(col * 229, row * 313, col * 229 + 229, row * 313 + 262)), f'Lead {nm}', f, 'LC21–22 slide 9'))
AX = [(60, 'Normal axis', [('Lead II?', 'Upright'), ('Strongest lead?', 'II (axis ≈ +60°)')]),
      (-60, 'Left axis deviation', [('Lead II?', 'Negative → not normal'), ('Lead I?', 'Upright → LEFT')]),
      (170, 'Right axis deviation', [('Lead II?', 'Negative → not normal'), ('Lead I?', 'Negative → RIGHT')]),
      (90, 'Axis ≈ +90° (normal for a dog)', [('Isoelectric lead?', 'I (0°)'), ('So the axis is?', '⟂ to lead I = ±90°; aVF upright → +90°')])]
ax_cards = [C('Normal axis, left deviation, or right deviation?', svg(f'axis{i}', six_lead(a, 'E' + str(i))), n, f, 'Drawn six-lead') for i, (a, n, f) in enumerate(AX, 1)]
B['🧭 Leads & axis'] = lead_cards + ax_cards
# ---------------- Block 4: action potentials, waves, extra drawn strips
B['⚡ Action potentials, waves & extra strips'] = [
 C('Which cell? What moves at each phase?', jpg('im-005-005.png', 'apnode', w=700, crop=(0, 0, 1, 0.59)), 'Pacemaker (SA node) cell', [('Phase 4?', 'HCN funny current (Na⁺ in)'), ('Phase 0?', 'Ca²⁺ in (T-type, Cav3.1) · ⚠️ Dr. Musch says L-type'), ('Phase 3?', 'K⁺ out'), ('Missing phases?', 'No phase 1 or 2 · Basel: “directly from phase zero to phase 3” · ⚠️ this textbook picture labels a “2” anyway')], 'LC20'),
 C('Which cell? What moves at each phase?', jpg('im-005-007.png', 'apvent', w=700, crop=(0, 0, 1, 0.74)), 'Working (ventricular) cardiomyocyte', [('Phase 0?', 'Na⁺ in (Nav1.5)'), ('Phase 1?', 'Brief K⁺ out (slide 25: K⁺/Cl⁻ out) · ⚠️ Basel said out loud: Na⁺ channels closing'), ('Phase 2?', 'Ca²⁺ in (L-type) = K⁺ out'), ('Phase 3?', 'K⁺ out'), ('Why plateau?', 'Full contraction before relaxing (“we don’t want to twitch”)')], 'LC20'),
 C('Name each wave and its event', jpg('im-032-039.png', 'pqrst', w=800), 'P · QRS · T', [('P?', 'Atrial depolarization'), ('QRS?', 'Ventricular depolarization'), ('T?', 'Ventricular repolarization'), ('Atrial repolarization?', 'Not visible · happens during the QRS (slide 8: 3a with 3b)'), ('PQ segment?', 'Atrial plateau (slide 8)')], 'LC21–22', aimg=jpg('im-008-011.png', 'pqrst_ans', w=900)),
 C('Name the rhythm', svg('mob1', ecg('mobitz1', 'M1')), '2nd degree AV block, Mobitz I (Wenckebach)', [('Key feature?', 'PR longer, longer, then drop'), ('Treat?', 'Slide 23 (all AV blocks): none if mild · atropine if vagal · pacemaker if symptomatic advanced · ⚠️ Basel was inconsistent out loud about which Mobitz type is worse; use slide 23')], 'Drawn strip'),
 C('Rate? (count beats × 10)', svg('brady', ecg('brady', 'BR')), '~40/min · bradycardic', [('Normal dog?', '70–120')], 'Drawn strip'),
 C('Complexes look normal, but no pulse or Doppler. Diagnosis?', svg('pea', ecg('nsr', 'PEA')), 'Pulseless electrical activity', [('Why?', 'E-C coupling failed'), ('Treat?', 'Not on the slide (slide 17 = definition only) · CPR'), ('Interpretation step?', '#6: pulse/Doppler every beat')], 'Drawn strip'),
 C('Name the rhythm', svg('vf2', ecg('vfib', 'VF')), 'Ventricular fibrillation', [('Shock type?', 'Defibrillation, unsynchronized'), ('Cardioversion is?', 'Synchronized to R, for organized rhythms')], 'Drawn strip'),
 C('Name the early beat', svg('apc2', ecg('apc', 'APC')), 'Atrial premature contraction', [('QRS?', 'Normal, narrow'), ('vs VPC?', 'VPC = wide, no P')], 'Drawn strip'),
]
# ---------------- pages
links = []
for i, (name, cards) in enumerate(B.items(), 1):
    fn = f'systems-lec-ecg{i}.html'
    cs = list(cards); cs[0] = cs[0].replace('class="card"', 'class="card on"', 1)
    out = deck.page(f'ECG · {name}', f'{len(cs)} cards · name it, then tap through each question', ''.join(cs), back=HUB)
    out = out.replace('← Back to Practical 2', '← Back to ECG cards').replace('← Back to Practical 3', '← Back to ECG cards')
    out = out.replace('.svg"', f'.svg?v={V}"')
    open(fn, 'w').write(out)
    links.append(f'<a href="{fn}?v={V}">{E(name)}<span>{len(cs)} cards</span></a>')
hub = (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><title>ECG flashcards</title><style>{deck.HUBCSS}</style></head><body><div class="wrap">'
       f'<a class="back" href="systems-lecture.html?v={V}">← Back to Lecture</a><div class="hero"><h1>🫀 ECG flashcards</h1><p>Real strips from Lecture 21–22 slides + the Arrhythmia Cases sheet (redrawn) + extra drawn strips. Small decks. Name it before you tap. 🐾</p></div>'
       f'<div class="sec main"><h2>⭐ Decks</h2><p>Each card: name the rhythm, then tap through the short follow-ups. ✅/❌ to track misses.</p>{"".join(links)}</div></div></body></html>')
open(HUB, 'w').write(hub)
print({k: len(v) for k, v in B.items()})
