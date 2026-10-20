# Cell Physiology · old exams (Basil metabolism question bank + Schultz signaling exams), tap-to-reveal answers.
# Data: tools/cellphys_oldexams_data.json (questions + answers written from lecture slides/transcripts).
# Called by tools/cellphys.py (build_oldexams). One card per question: stem + options visible, tap → answer, why, source.
import html, json, os, re
import deck
from cellphys_pathways import _copyjs
E = html.escape
HERE = os.path.dirname(__file__)

PAGES = [  # (file, title, section-prefix match list)
 ('cellphys-old-scope.html', '⭐ Exam 3 scope only · all years', None),
 ('cellphys-old-basil-2025.html', 'Basil 2025 · Exams 2 & 3', ['Basil metabolism · 2025']),
 ('cellphys-old-basil-2024.html', 'Basil 2024 · Exam 3', ['Basil metabolism · 2024']),
 ('cellphys-old-basil-2023.html', 'Basil 2023 · Exam 5', ['Basil metabolism · 2023']),
 ('cellphys-old-basil-2022.html', 'Basil 2022 · Exam 2', ['Basil metabolism · 2022']),
 ('cellphys-old-basil-2021.html', 'Basil 2021 · Exams 1 & 3', ['Basil metabolism · 2021']),
 ('cellphys-old-basil-2020.html', 'Basil 2020 · Exams 2 & 3', ['Basil metabolism · 2020']),
 ('cellphys-old-basil-2019.html', 'Basil 2019 & 2018', ['Basil metabolism · 2019', 'Basil metabolism · 2018']),
 ('cellphys-old-schultz-2025.html', 'Schultz 2025 · Exam 3 (signaling)', ['Schultz 2025']),
 ('cellphys-old-schultz-2024.html', 'Schultz 2024 · Exam 4 (signaling)', ['Schultz 2024']),
 ('cellphys-old-schultz-2023.html', 'Schultz 2023 · Exam 3 (neuro + signaling)', ['Schultz 2023']),
]
XCSS = """.q.exq{text-align:left;font-size:clamp(16px,1.9vw,21px);font-weight:750;color:#3b1d66;line-height:1.35}
.exq .ctx{font-size:14px;font-weight:600;color:#5c5068;background:#f4ebfb;border-radius:10px;padding:8px 10px;margin-bottom:8px}
.exq ol{list-style:none;padding:0;margin:10px 0 0}.exq li{font-size:clamp(15px,1.7vw,18px);font-weight:650;color:#2e2438;padding:7px 10px;margin:5px 0;border:1px solid #e3d5f2;border-radius:10px;background:#fff}
.exq li b{color:#d94f7f;margin-right:6px}.exq .meta{display:block;font-size:12px;font-weight:800;color:#8a6aa8;margin-bottom:6px;letter-spacing:.02em}
.exq img{display:block;max-width:100%;max-height:45vh;margin:8px auto;border-radius:10px;border:1px solid #e3d5f2;background:#fff}
.pill{display:inline-block;font-size:11px;font-weight:800;border-radius:999px;padding:2px 8px;margin-left:6px;vertical-align:middle}
.pill.in{background:#e1f5ec;color:#1f7a55}.pill.out{background:#eee;color:#666}.pill.multi{background:#fbe7ef;color:#d94f7f}
.stg .an{font-size:16px;font-weight:650;line-height:1.4}.stg .an b{font-weight:850}
.pill.unsure{background:#fff1e3;color:#b85a1c}.flag{margin-top:6px;font-size:14px;color:#b85a1c}"""

def load():
    return json.load(open(os.path.join(HERE, 'cellphys_oldexams_data.json')))

def card(q):
    opts = ''.join(f'<li><b>{E(l.upper())}.</b>{E(t)}</li>' for l, t in q['opts'])
    imgs = ''.join(f'<img src="assets/cellphys_old_{E(i)}.jpg" loading="lazy" alt="exam figure">' for i in q.get('img', []))
    ctx = f'<div class="ctx">{E(q["ctx"])}</div>' if q.get('ctx') else ''
    a = q.get('a') or {}
    scope = a.get('scope', '')
    pills = (f'<span class="pill {"in" if scope=="in" else "out"}">{"in Exam 3 scope" if scope=="in" else "not on this exam"}</span>' if scope else '') + \
            ('<span class="pill multi">select all</span>' if q.get('multi') else '')
    meta = f'<span class="meta">{E(q["sec"])} · Q{E(str(q["n"]))}{pills}</span>'
    letters = a.get('ans') or []
    if letters:
        txt = {l: t for l, t in q['opts']}
        ans = '<br>'.join(f'<b>{l.upper()}.</b> {E(txt.get(l, ""))}' for l in letters)
    else:
        ans = '<b>Model answer</b>' if not q['opts'] else '<b>No answer recorded</b>'
    conf = a.get('conf', '')
    conf_html = '<span class="pill unsure">double-check</span>' if conf == 'unsure' else ('<span class="pill unsure">likely</span>' if conf == 'likely' else '')
    S = deck.stg('⬇️ Answer?', ans + conf_html, False)
    why = E(a.get('why', ''))
    fl = f'<div class="flag">⚠️ {E(a["flag"])}</div>' if a.get('flag') else ''
    S += deck.stg('💡 Why + source', f'{why}<div class="clue">📖 {E(a.get("cite", ""))}</div>{fl}')
    return (f'<section class="card"><div class="q exq">{meta}{ctx}{E(q["stem"])}{imgs}<ol>{opts}</ol></div>{S}'
            f'<div class="rev">💗 TAP TO REVEAL</div></section>')

def build_oldexams(HUB, V):
    qs = load(); tiles = []; cj = _copyjs()
    for fn, title, pref in PAGES:
        sel = [q for q in qs if (q.get('a') or {}).get('scope') == 'in' and q['sec'].startswith('Basil')] if pref is None \
              else [q for q in qs if any(q['sec'].startswith(p) for p in pref)]
        if not sel: continue
        cs = [card(q) for q in sel]; cs[0] = cs[0].replace('class="card"', 'class="card on"', 1)
        nin = sum(1 for q in sel if (q.get('a') or {}).get('scope') == 'in')
        sub = f'{len(sel)} questions · {nin} in this exam\'s scope · read every option, answer out loud, then tap'
        out = deck.page(title, sub, ''.join(cs), back=HUB)
        out = re.sub(r'← Back to [^<]+', '← Back to Cell Physiology', out, count=1).replace('</style>', XCSS + '</style>', 1).replace('</body>', cj + '</body>')
        open(fn, 'w').write(out)
        emoji = '⭐' if pref is None else ('🧬' if 'Basil' in title else '📡')
        st = ' style="border:3px solid #d94f7f"' if pref is None else ''
        tiles.append(f'<a class="tile" href="{fn}?v={V}"{st}><div class="emoji">{emoji}</div><h2>{E(title)}</h2><p>{len(sel)} questions · {nin} in scope · tap to reveal</p></a>')
    print('oldexams', len(qs), 'questions,', len(tiles), 'pages')
    head = '<div style="grid-column:1/-1;font-weight:900;color:#70428f;margin-top:8px">📝 Old exams · answered from your lectures + transcripts</div>'
    return head + ''.join(tiles)
