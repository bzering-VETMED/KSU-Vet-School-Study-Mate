# Cell Physiology · Exam 4 · Dr. Basel old exams (2018–2023), answered from LC28–LC33 (2026 numbering), graphs included.
# Data: tools/cellphys_e4_baselold.json (built from Bethany's "Cell Signaling Questions" doc). One page per exam + a repeats page.
import html, json, os, re
import deck
from cellphys_pathways import _copyjs
from cellphys_oldexams import XCSS
E = html.escape
HERE = os.path.dirname(__file__)
YEARS = ['2023', '2022', '2021', '2020', '2019', '2018']
LABEL = {'2022': '2022 Exam 2'}
REP = 'cellphys-basel-repeats.html'
GCSS = '.exq img{max-width:100%;border:1px solid #e6d9f0;border-radius:10px;margin:6px 0;background:#fff}.parts{margin:6px 0 0 18px;padding:0}.parts li{margin:3px 0}'

def card(q):
    ctx = f'<div class="ctx">{E(q["ctx"])}</div>' if q.get('ctx') else ''
    imgs = ''.join(f'<img src="{E(i)}" loading="lazy" alt="exam graph">' for i in q['img'])
    opts = ''.join(f'<li><b>{E(l.upper())}.</b>{E(t)}</li>' for l, t in q['opts'])
    parts = ('<ul class="parts">' + ''.join(f'<li>{E(p)}</li>' for p in q['parts']) + '</ul>') if q['parts'] else ''
    pills = '<span class="pill in">Exam 4 lecture</span>' if q['scope'] == 'in' else '<span class="pill out">not tested in 2026</span>'
    if q['multi']: pills += '<span class="pill multi">select all</span>'
    if q['free']: pills += '<span class="pill multi">short answer</span>'
    if q['rep']: pills += f'<span class="pill multi">🔁 also {E(", ".join(y for y in q["rep"] if y != q["year"]))}</span>'
    meta = f'<span class="meta">Basel {E(LABEL.get(q["year"], q["year"] + " Exam 4"))} · Q{q["n"]}{pills}</span>'
    if q['free']:
        ans = E(q['ans'].replace('MODEL ANSWER: ', ''))
    else:
        txt = {l: t for l, t in q['opts']}
        ans = '<br>'.join(f'<b>{l.upper()}.</b> {E(txt.get(l, ""))}' for l in q['ans'])
    ans += {'unsure': '<span class="pill unsure">double-check</span>', 'likely': '<span class="pill unsure">likely</span>'}.get(q['conf'], '')
    fl = f'<div class="flag">⚠️ {E(q["flag"])}</div>' if q.get('flag') else ''
    S = deck.stg('⬇️ Answer?', ans, False)
    S += deck.stg('💡 Why + source', f'{E(q["why"])}<div class="clue">📖 {E(q["cite"])}</div>{fl}')
    return (f'<section class="card"><div class="q exq">{meta}{ctx}{E(q["stem"])}{imgs}'
            f'{"<ol>" + opts + "</ol>" if opts else ""}{parts}</div>{S}<div class="rev">💗 TAP TO REVEAL</div></section>')

def _write(fn, title, sub, sel, HUB, cj):
    cs = [card(q) for q in sel]; cs[0] = cs[0].replace('class="card"', 'class="card on"', 1)
    out = deck.page(title, sub, ''.join(cs), back=HUB)
    out = re.sub(r'← Back to [^<]+', '← Back to Cell Physiology', out, count=1).replace('</style>', XCSS + GCSS + '</style>', 1).replace('</body>', cj + '</body>')
    open(fn, 'w').write(out)

def build_e4_baselold(HUB, V):
    qs = json.load(open(os.path.join(HERE, 'cellphys_e4_baselold.json'))); cj = _copyjs()
    tiles = '<div style="grid-column:1/-1;font-weight:900;color:#70428f;margin-top:8px">📝 Dr. Basel old exams (2018–2023) · graphs included · tap to reveal</div>'
    seen = set(); rep = []
    for q in qs:
        if q['rep'] and q['scope'] == 'in' and q['grp'] not in seen:
            seen.add(q['grp']); rep.append(q)
    _write(REP, '🔁 Basel repeated questions', f'{len(rep)} stems asked on 2+ exams · answer out loud, then tap', rep, HUB, cj)
    tiles += f'<a class="tile" href="{REP}?v={V}" style="border:3px solid #d94f7f"><div class="emoji">🔁</div><h2>Basel repeated questions</h2><p>{len(rep)} stems asked on 2+ exams · start here</p></a>'
    for y in YEARS:
        sel = [q for q in qs if q['year'] == y]
        fn = f'cellphys-basel-{y}.html'; lab = LABEL.get(y, y + ' Exam 4')
        ng = sum(1 for q in sel if q['img'])
        _write(fn, f'🧪 Basel {lab}', f'Whole exam · {len(sel)} questions' + (f' · {ng} with graphs' if ng else '') + ' · answer out loud, then tap', sel, HUB, cj)
        tiles += f'<a class="tile" href="{fn}?v={V}"><div class="emoji">🧪</div><h2>Basel {E(lab)}</h2><p>{len(sel)} questions{" · 📈 graphs" if ng else ""} · tap to reveal</p></a>'
    print('basel oldexams', len(qs), 'questions,', len(rep), 'repeats')
    return tiles
