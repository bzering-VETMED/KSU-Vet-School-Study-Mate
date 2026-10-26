# Exam 4 lecture hub (made by Claude): gross-anatomy-exam4.html, linked from the course hub (gross-anatomy.html).
# Add a tile to TILES as each lecture's pages are built. Run from repo root: python3 tools/exam4hub.py
import time, re, html as H
V = str(int(time.time()))
TILES = [  # (emoji, href, title, blurb)
    ("⚡", "gross-anatomy-lc26-cards.html", "L26 Terms", "Pelvic Limb Vessels & Nerves · 105 terms · ★ 48 · slides + lecture 10/26 · exam signals, scope, traps"),
    ("🧭", "gross-anatomy-l26-trace.html", "L26 Trace It", "Arteries aorta → paw, deep + superficial veins, lymph nodes, lumbosacral plexus, testing sites · names pop up in order"),
]
LECTURES = [  # from the Canvas lecture schedule
    ("Mon 10/26", "L26", "Pelvic limb vessels & nerves", "Dr. Malreddy", "built (slides + transcript)"),
    ("Mon 11/2", "L28", "Digestive components of head 1", "Dr. Diehl", ""),
    ("Wed 11/4", "L30", "Eye", "Dr. Malreddy", ""),
    ("Thu 11/5", "L29", "Digestive components of head 2", "Dr. Diehl", ""),
    ("Mon 11/9", "L31", "Ear", "Dr. Malreddy", ""),
    ("Wed 11/11", "L32", "Head vessels · Quiz 8", "Dr. Klimek", ""),
    ("Thu 11/12", "L33", "Respiratory components of head", "Dr. Malreddy", ""),
    ("Mon 11/16", "L34", "Meninges & brain · Quiz 9", "Dr. Klimek", ""),
    ("Wed 11/18", "L35", "Cranial nerves", "Dr. Klimek", ""),
    ("Thu 11/19", "L36", "Spinal cord & ligaments", "Dr. Klimek", ""),
    ("Mon 11/30", "L37", "Radiology: head", "Dr. Cassel", ""),
    ("Wed 12/2", "L38", "Game-based learning 4 · Quiz 10", "Dr. Malreddy", "review"),
]
CSS = open('gross-anatomy-lecture.html').read().split('<style>')[1].split('</style>')[0] + '''
table{width:100%;border-collapse:collapse;background:#fff;border-radius:15px;overflow:hidden;font-size:14px}th{background:#70428f;color:#fff;text-align:left;padding:7px 9px}
td{padding:6px 9px;border-top:1px solid var(--line)}tr:nth-child(even) td{background:#fbf6ff}tr.done td{background:#ffe7f2}.note b{color:#70428f}.note ul{margin:6px 0 0;padding-left:20px}'''
tiles = ''.join(f'<a class="tile" href="{h}?v={V}"><div class="emoji">{e}</div><h2>{H.escape(t)}</h2><p>{H.escape(b)}</p></a>' for e, h, t, b in TILES)
rows = ''.join(f'<tr class="{"done" if s.startswith("built") else ""}"><td>{d}</td><td><b>{n}</b></td><td>{H.escape(t)}</td><td>{p}</td><td>{s}</td></tr>' for d, n, t, p, s in LECTURES)
page = f'''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#8855b8"><title>📖 Gross Anatomy I · Exam 4</title><style>{CSS}</style></head><body><div class="wrap">
<section class="hero"><h1>📖 Gross Anatomy I · Exam 4</h1><p>Lectures 26–37 · Labs 26–36 · practical Thu 12/3, 8:00 AM · lecture exam Fri 12/4</p></section>
<div class="nav"><a href="gross-anatomy-lecture.html?v={V}">← Back to Lecture</a></div>
<div class="note"><b>📣 Scope notes (Canvas + syllabus)</b><ul>
<li><b>L26 pelvic limb vessels & nerves is NOT on Exam 3</b>, not on Wednesday's Quiz 7, and excluded from Lab Exam 3 → it starts Exam 4.</li>
<li>Exam 4 = 100 pt written + 100 pt practical; up to <b>20% review</b> of earlier material.</li>
<li><b>Lab Exam 4 is a group exam</b> (format explained after Exam 3). Dissection Checkoff 4 + review = Wed 12/2.</li>
<li>Lecture Exam 4 time not posted yet (Exam 3 was 8:00 AM). Blueprint comes ~1 week before.</li></ul></div>
<div class="grid">{tiles}</div>
<h2 style="color:#70428f;margin:22px 0 8px">🗓️ Lecture tracker</h2>
<table><tr><th>Date</th><th>#</th><th>Topic</th><th>Instructor</th><th>Pages</th></tr>{rows}</table>
<div class="footer">🎀 Bethany · K-State CVM Class of 2030 · 🐾</div></div></body></html>'''
open('gross-anatomy-exam4.html', 'w').write(page); print('exam4 hub:', len(TILES), 'tiles')
