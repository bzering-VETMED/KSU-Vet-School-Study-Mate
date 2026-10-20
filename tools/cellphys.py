# Build: Cell Physiology (VAP805) · Exam 3 hub + one-page tap-to-reveal terms sheet + 4 practice exams
# Run from repo root: python3 tools/cellphys.py
# Reuses: terms-page CSS/JS from systems-lp1-functions.html (same as sys_lec_terms_cards.py),
#         practice-exam CSS/JS from sys_lecture.py (same as sys_practice.py), hub style from veterinary-systems.html.
import html, json, re, os, sys, time, random
sys.path.insert(0, os.path.dirname(__file__))
from cellphys_data import TERMS, FLAGS
from cellphys_exams import EXAMS
from cellphys_lectures import NEW, NEWFLAGS
TERMS = list(TERMS) + [(nm, it) for _, nm, it in NEW]; FLAGS = list(FLAGS) + NEWFLAGS
LCNUM = [14 + k for k in range(8)] + [lc for lc, _, _ in NEW]
E = html.escape; V = str(int(time.time()))
HUB = 'cell-physiology.html'
FOOT = '🎀 Bethany · K-State CVM Class of 2030 · VAP 805 · 🐾'

# ---------------------------------------------------------- 1) ONE-PAGE TERMS SHEET
FUN = open('systems-lp1-functions.html').read()
TCSS = FUN[FUN.index('<style>') + 7:FUN.index('</style>')]
TJS = FUN[FUN.rindex('<script>') + 8:FUN.rindex('</script>')]
TCSS += '.flag{background:#fff1e3;border:2px dashed #e07b39;border-radius:16px;padding:12px 14px;margin:16px 0}.flag h2{color:#b35a00;margin:0 0 6px}.flag li{margin:5px 0;font-size:14.5px}'
body = []; n = 0
for k, (name, items) in enumerate(TERMS):
    rows = ''.join(f'<tr><td>{E(a)}</td><td><span class="ans">{E(b)}</span></td></tr>' for a, b in items); n += len(items)
    body.append(f'<div class="sec{" p" if k % 2 else ""}"><h2>{E(name)}</h2><table>{rows}</table></div>')
flags = '<div class="flag"><h2>⚠️ Source flags (ask before trusting)</h2><ul>' + ''.join(f'<li><b>{E(a)}:</b> {E(b)}</li>' for a, b in FLAGS) + '</ul></div>'
open('cellphys-terms.html', 'w').write(
    f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>🧠 Cell Phys Terms</title><style>{TCSS}</style></head><body><div class="wrap">'
    f'<a class="back" href="{HUB}?v={V}">← Back to Cell Physiology</a><div class="hero"><h1>🧠 Cell Physiology Exam 3 · Terms</h1><p>Say it, then tap the pink box to check · {n} terms · LC14–LC21, LC23, LC08 · from your slides + transcripts</p></div>'
    f'<div class="bar"><script defer src="shuffle.js"></script><button id="hide">🙈 Hide all</button><button id="all">👀 Show all</button><span class="n" id="n"></span></div><div class="cols">{"".join(body)}</div>{flags}<div class="foot">{FOOT}</div></div><script>{TJS}</script></body></html>')
print('terms', n)

# ---------------------------------------------------------- 1b) ONE TERMS PAGE PER LECTURE (★ emphasized rows + ⚠️ traps)
from cellphys_lectures import EXTRA, STARS, TRAPS
LCSS = TCSS + ('tr.star td{background:#ffe7f2!important}tr.star td:first-child::before{content:"★ ";color:#d94f7f}'
               '.trap{background:#fbe7ef;border:2px solid #d94f7f;border-radius:16px;padding:12px 14px;margin:14px 0}.trap h2{color:#b8336a;margin:0 0 6px;font-size:18px}.trap li{margin:5px 0;font-size:15px}'
               '.legend{font-size:13.5px;color:#8a6b99;margin:6px 2px}')
LEC = []
for k, (name, items) in enumerate(TERMS):
    lc = LCNUM[k]; allit = list(items) + EXTRA.get(lc, []); st = STARS.get(lc, set())
    miss = st - {a for a, _ in allit}
    if miss: print('⚠️ star not found', lc, miss)
    rows = ''.join(f'<tr{" class=star" if a in st else ""}><td>{E(a)}</td><td><span class="ans">{E(b)}</span></td></tr>' for a, b in allit)
    trap = '<div class="trap"><h2>⚠️ Precision traps</h2><ul>' + ''.join(f'<li>{t}</li>' for t in TRAPS.get(lc, [])) + '</ul></div>'
    fn = f'cellphys-lc{lc}-terms.html'; title = name.split(' ', 1)[1]
    open(fn, 'w').write(
        f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>🧠 {E(title)}</title><style>{LCSS}</style></head><body><div class="wrap">'
        f'<a class="back" href="{HUB}?v={V}">← Back to Cell Physiology</a><div class="hero"><h1>{E(name)}</h1><p>Say it, then tap the pink box to check · {len(allit)} terms · {("★ "+str(len(st))+" the professor stressed") if st else "★ rows added after the transcript"}</p></div>'
        f'{trap}<div class="bar"><script defer src="shuffle.js"></script><button id="hide">🙈 Hide all</button><button id="all">👀 Show all</button><span class="n" id="n"></span></div>'
        f'<div class="legend">★ pink rows = emphasized in lecture or on Canvas quizzes</div><div class="cols"><div class="sec"><h2>{E(name)}</h2><table>{rows}</table></div></div>'
        f'<div class="foot">{FOOT}</div></div><script>{TJS}</script></body></html>')
    LEC.append((fn, name, len(allit), len(st)))
print('lecture pages', [(f, c) for f, _, c, _ in LEC])

# ---------------------------------------------------------- 2) PRACTICE EXAMS
src = open(os.path.join(os.path.dirname(__file__), 'sys_lecture.py')).read()
CSS = re.search(r"CSS='''(.*?)'''", src, re.S).group(1)
CSS += ('.sec{margin:22px 0 4px;padding:10px 14px;border-radius:14px;background:linear-gradient(135deg,#5d347e,#8855b8);color:#fff;font-weight:900;font-size:16px}'
        '.cite{display:block;margin-top:5px;font:12.5px ui-monospace,Menlo,monospace;color:#8a6f98}')
JS = re.search(r"JS='''(.*?)'''", src, re.S).group(1)
JS = JS.replace("document.getElementById('shuf').onclick=()=>{const w=document.getElementById('qs');[...w.children].sort(()=>Math.random()-.5).forEach(x=>w.appendChild(x))};",
                "document.getElementById('shuf').onclick=()=>{const w=document.getElementById('qs');w.querySelectorAll('.sec').forEach(s=>s.style.display='none');[...w.querySelectorAll('.q')].sort(()=>Math.random()-.5).forEach(x=>w.appendChild(x))};")
NOTE = ('Written in the style of your VAP805 Canvas quizzes (short stems, clinical cases, "best explains", select-all). '
        'Tap an answer to check it; select-all questions need ✓ Check. Letters are shuffled. Answers come from the LC14–LC21 slides and transcripts '
        '(<b>not an official key</b>); 📖 = slide (S#) or slide title to look up. Each exam has different questions.')
def build(fn, title, items, seed):
    rnd = random.Random(seed); out = []; q = 0; slots = []
    for it in items:
        if it[0] == '§':
            out.append(f'<div class="sec">{E(it[1])}</div>'); continue
        stem, ok, bad, why, cite, sure = it
        oks = ok if isinstance(ok, list) else [ok]
        if len(oks) == 1:  # balanced letters: cycle the correct position through A–D (shuffled blocks)
            if not slots: slots = list(range(len(bad) + 1)); rnd.shuffle(slots)
            opts = list(bad); rnd.shuffle(opts); opts.insert(min(slots.pop(), len(opts)), oks[0])
        else:
            opts = oks + bad; rnd.shuffle(opts)
        ans = sorted(opts.index(o) for o in oks); q += 1
        m = len(oks) > 1 or 'select all' in stem.lower()
        ob = ''.join(f'<button class="opt">{chr(65 + j)}. {E(o)}</button>' for j, o in enumerate(opts))
        fl = '' if sure else '<div class="flag">⚠️ Not 100% sure. Confirm with the instructor.</div>'
        key = ', '.join(chr(65 + a) for a in ans)
        out.append(f'<div class="q" data-a="{json.dumps(ans)}" data-m="{int(m)}"><h3><span>Q{q}</span>{E(stem)}</h3>{ob}'
                   f'{"<button class=chk>Check ✓</button>" if m else ""}<div class="why">✅ <b>{key}</b> · {E(why)}<span class="cite">📖 {E(cite)}</span>{fl}</div></div>')
    open(fn, 'w').write(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(title)}</title><style>{CSS}</style></head><body><div class="wrap">'
                        f'<a class="back" href="{HUB}?v={V}">← Back to Cell Physiology</a><div class="hero"><h1>{E(title)}</h1><p>{q} questions · LC14–LC21 · Exam 3</p></div><div class="note">{NOTE}</div>'
                        f'<div class="bar"><button id="shuf">🎲 Shuffle</button><button id="miss">🔁 Misses only</button><button id="all">↺ Show all</button><span class="score" id="sc"></span></div>'
                        f'<div id="qs">{"".join(out)}</div><div class="note" style="text-align:center">{FOOT}</div></div><script>{JS}</script></body></html>')
    return q
counts = [build(fn, t, it, i) for i, (fn, t, it) in enumerate(EXAMS, 1)]
print('exams', counts)

# ---------------------------------------------------------- 3) COURSE HUB + HOME TILE + SW
VS = open('veterinary-systems.html').read()
style = VS[VS.index('<style>'):VS.index('</style>') + 8]
from cellphys_pathways import build_pathways
from cellphys_enzymes import build_enzymes
from cellphys_keyslide import build_keyslide
tiles = build_keyslide(HUB, V) + build_pathways(HUB, V) + build_enzymes(HUB, V) + '<div style="grid-column:1/-1;font-weight:900;color:#70428f;margin-top:8px">🧠 Terms by lecture · tap to reveal</div>' + ''.join(f'<a class="tile" href="{fn}?v={V}"><div class="emoji">{E(nm.split(" ")[0])}</div><h2>{E(nm.split(" · ")[0].split(" ", 1)[1])} terms</h2><p>{E(nm.split(" · ", 1)[1])} · {c} terms · {("★ "+str(s)) if s else "★ after transcript"} · ⚠️ traps</p></a>' for fn, nm, c, s in LEC)
tiles += '<div style="grid-column:1/-1;font-weight:900;color:#70428f;margin-top:8px">🧪 Combined sheet + practice exams</div>'
tiles += f'<a class="tile" href="cellphys-terms.html?v={V}"><div class="emoji">🧠</div><h2>All terms, one page</h2><p>{n} tap-to-reveal terms · all exam lectures + source flags</p></a>'
for (fn, t, it), c in zip(EXAMS, counts):
    tiles += f'<a class="tile" href="{fn}?v={V}"><div class="emoji">🧪</div><h2>{E(t[2:])}</h2><p>{c} questions · quiz style · all lectures</p></a>'
open(HUB, 'w').write(f'<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#8855b8"><title>🧫 Cell Physiology</title>{style}</head><body><div class="wrap">'
    f'<section class="hero"><h1>🧫 Cell Physiology · Exam 3</h1><p>Fri 10/23 · LC14–LC21 + LC23 (Mon 10/19) + LC08 pH (Wed 10/21)</p></section>'
    f'<div class="nav"><a href="fall2026.html?v={V}">← Back</a></div><div class="grid">{tiles}</div><div class="footer">KSU Vet School Study Mate · Fall 2026</div></div></body></html>')
home = open('fall2026.html').read()
if HUB not in home:
    home = home.replace('</div><div class="footer">', f'<a class="tile" href="{HUB}?v={V}"><div class="emoji">🧫</div><h2>Cell Physiology</h2><p>Exam 3 · terms + practice exams</p></a>\n</div><div class="footer">', 1)
home = re.sub(r'cell-physiology\.html\?v=\d+', f'{HUB}?v={V}', home)
open('fall2026.html', 'w').write(home)
sw = open('sw.js').read(); open('sw.js', 'w').write(re.sub(r"ksu-study-mate-v(\d+)-\d+", lambda m: f"ksu-study-mate-v{int(m.group(1)) + 1}-{V}", sw))
print('hub ok')
