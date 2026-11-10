# Cell Physiology · Exam 4 · Dr. Schultz old exams (2023 Ex3, 2024 Ex4, 2025 Ex3, 2025 Ex4), answered from LC25–LC27 (2026 numbering).
# Data: tools/cellphys_e4_oldexams.json. One page per exam (tap-to-reveal deck, same look as the Exam 3 old-exam pages) + a repeats page.
# Called by cellphys_exam4.build_exam4 → returns hub tiles.
import html, json, os, re
import deck
from cellphys_pathways import _copyjs
from cellphys_oldexams import XCSS
E = html.escape
HERE = os.path.dirname(__file__)
PAGES = [('cellphys-e4old-2025.html', 'Schultz 2025 · Exam 4', '2025 Exam 4'),
         ('cellphys-e4old-2024.html', 'Schultz 2024 · Exam 4', '2024 Exam 4'),
         ('cellphys-e4old-2025e3.html', 'Schultz 2025 · Exam 3', '2025 Exam 3'),
         ('cellphys-e4old-2023.html', 'Schultz 2023 · Exam 3', '2023 Exam 3')]
REP = 'cellphys-e4old-repeats.html'
PILL = {'in': ('in', 'Exam 4 lecture'), 'rep': ('multi', 'asked EVERY year'), 'e3': ('out', 'Exam 3 topic · review'), 'out': ('out', 'not on Exam 4 (neuro)')}

def card(q):
    opts = ''.join(f'<li><b>{E(l.upper())}.</b>{E(t)}</li>' for l, t in q['opts'])
    imgs = ''.join(f'<img src="assets/cellphys_old_{E(i)}.jpg" loading="lazy" alt="exam figure">' for i in q.get('img', []))
    ctx = f'<div class="ctx">{E(q["ctx"])}</div>' if q.get('ctx') else ''
    a = q['a']; c, lab = PILL[a.get('scope', 'out')]
    pills = f'<span class="pill {c}">{lab}</span>' + ('<span class="pill multi">select all</span>' if q.get('multi') else '')
    if q.get('rep'):
        pills += f'<span class="pill multi">🔁 also {E(", ".join(y for y in q["rep"] if y != q["year"]))}</span>'
    meta = f'<span class="meta">Schultz {E(q["year"])} · Q{E(str(q["n"]))}{pills}</span>'
    txt = {l: t for l, t in q['opts']}
    ans = '<br>'.join(f'<b>{l.upper()}.</b> {E(txt.get(l, ""))}' for l in a.get('ans', [])) or '<b>Model answer</b>'
    conf = a.get('conf', '')
    ans += '<span class="pill unsure">double-check</span>' if conf == 'unsure' else ('<span class="pill unsure">likely</span>' if conf == 'likely' else '')
    S = deck.stg('⬇️ Answer?', ans, False)
    fl = f'<div class="flag">⚠️ {E(a["flag"])}</div>' if a.get('flag') else ''
    S += deck.stg('💡 Why + source', f'{E(a.get("why", ""))}<div class="clue">📖 {E(a.get("cite", ""))}</div>{fl}')
    return (f'<section class="card"><div class="q exq">{meta}{ctx}{E(q["stem"])}{imgs}<ol>{opts}</ol></div>{S}'
            f'<div class="rev">💗 TAP TO REVEAL</div></section>')

def _write(fn, title, sub, sel, HUB, cj):
    cs = [card(q) for q in sel]; cs[0] = cs[0].replace('class="card"', 'class="card on"', 1)
    out = deck.page(title, sub, ''.join(cs), back=HUB)
    out = re.sub(r'← Back to [^<]+', '← Back to Cell Physiology', out, count=1).replace('</style>', XCSS + '</style>', 1).replace('</body>', cj + '</body>')
    open(fn, 'w').write(out)

def build_e4_oldexams(HUB, V):
    qs = json.load(open(os.path.join(HERE, 'cellphys_e4_oldexams.json'))); cj = _copyjs()
    tiles = '<div style="grid-column:1/-1;font-weight:900;color:#70428f;margin-top:8px">📝 Dr. Schultz old exams · answered from LC25–LC27 · tap to reveal</div>'
    # repeats first: one card per repeated stem (newest year wins)
    seen = set(); rep = []
    for q in qs:
        if q['rep'] and q['a']['scope'] != 'out':
            k = re.sub(r'[^a-z]', '', q['stem'].lower())[:60]
            if k in seen: continue
            seen.add(k); rep.append(q)
    _write(REP, '🔁 Schultz repeated questions', f'{len(rep)} stems asked on 2+ exams · highest-yield · answer out loud, then tap', rep, HUB, cj)
    tiles += f'<a class="tile" href="{REP}?v={V}" style="border:3px solid #d94f7f"><div class="emoji">🔁</div><h2>Schultz repeated questions</h2><p>{len(rep)} stems asked on 2+ exams · start here</p></a>'
    for fn, title, yr in PAGES:
        sel = [q for q in qs if q['year'] == yr]
        nin = sum(1 for q in sel if q['a']['scope'] in ('in', 'rep'))
        _write(fn, '📡 ' + title, f'Whole exam · {len(sel)} questions · {nin} on Exam 4 lectures · read every option, answer out loud, then tap', sel, HUB, cj)
        tiles += f'<a class="tile" href="{fn}?v={V}"><div class="emoji">📡</div><h2>{E(title)}</h2><p>{len(sel)} questions · {nin} on Exam 4 · tap to reveal</p></a>'
    print('e4 oldexams', len(qs), 'questions,', len(rep), 'repeats')
    return tiles
