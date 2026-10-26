# Cell Physiology · Exam 4 (LC25–LC33): per-lecture terms pages, "know these" table pages, practice quiz decks.
# Data: tools/cellphys_e4/LC##.json (written from the slides; ★ rows get added after each transcript).
# Called by tools/cellphys.py → build_exam4(HUB, V) returns the hub tiles for the Exam 4 index.
# Reuses: terms-page CSS/JS (systems-lp1-functions.html) and the practice-exam CSS/JS (sys_lecture.py), like cellphys.py.
import html, json, os, re, random, glob
E = html.escape
HERE = os.path.dirname(__file__)
FOOT = '🎀 Bethany · K-State CVM Class of 2030 · VAP 805 · 🐾'

def _load():
    out = []
    for p in sorted(glob.glob(os.path.join(HERE, 'cellphys_e4', 'LC*.json')), key=lambda s: int(re.search(r'LC(\d+)', s).group(1))):
        out.append(json.load(open(p)))
    return out

def _terms_assets():
    fun = open('systems-lp1-functions.html').read()
    css = fun[fun.index('<style>') + 7:fun.index('</style>')]
    js = fun[fun.rindex('<script>') + 8:fun.rindex('</script>')]
    css += ('tr.star td{background:#ffe7f2!important}tr.star td:first-child::before{content:"★ ";color:#d94f7f}'
            '.trap{background:#fbe7ef;border:2px solid #d94f7f;border-radius:16px;padding:12px 14px;margin:14px 0}.trap h2{color:#b8336a;margin:0 0 6px;font-size:18px}.trap li{margin:5px 0;font-size:15px}'
            '.flag{background:#fff1e3;border:2px dashed #e07b39;border-radius:16px;padding:12px 14px;margin:16px 0}.flag h2{color:#b35a00;margin:0 0 6px;font-size:18px}.flag li{margin:5px 0;font-size:14.5px}'
            '.legend{font-size:13.5px;color:#8a6b99;margin:6px 2px}.sl{font:12px ui-monospace,Menlo,monospace;color:#8a6f98;margin-left:6px}'
            '.kt{width:100%;border-collapse:collapse;margin:8px 0}.kt th{background:#f3eafb;color:#65328c;text-align:left;padding:7px;border:1px solid #e6d9f0}.kt td{padding:7px;border:1px solid #e6d9f0;vertical-align:top}'
            '.kn{font-size:14px;color:#7a4f96;margin:4px 0 8px}')
    return css, js

def _quiz_assets():
    src = open(os.path.join(HERE, 'sys_lecture.py')).read()
    css = re.search(r"CSS='''(.*?)'''", src, re.S).group(1)
    css += ('.cite{display:block;margin-top:5px;font:12.5px ui-monospace,Menlo,monospace;color:#8a6f98}'
            '#cpy{background:linear-gradient(120deg,#6a3392,#e05fa8);color:#fff}.done-bar{text-align:center;margin:18px 0}')
    js = re.search(r"JS='''(.*?)'''", src, re.S).group(1)
    js += ("function copyMiss(){const t=[...document.querySelectorAll('.q')].filter(q=>q.dataset.miss).map(q=>{const s=q.querySelector('h3').innerText.replace(/^Q\\d+/,'').trim();"
           "const a=q.querySelector('.why').innerText.split('📖')[0].trim();return '❌ '+s+'\\n   '+a}).join('\\n\\n');"
           "const out=t||'No misses yet 🎉';(navigator.clipboard?navigator.clipboard.writeText(out):Promise.reject()).then(()=>alert('Copied '+document.querySelectorAll('.q[data-miss]').length+' misses'),()=>prompt('Copy your misses:',out))}"
           "document.querySelectorAll('.cpy').forEach(b=>b.onclick=copyMiss);")
    return css, js

def _page(title, css, body, js, hub, V):
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{E(title)}</title><style>{css}</style></head><body><div class="wrap"><a class="back" href="{hub}?v={V}">← Back to Cell Physiology</a>'
            f'{body}<div class="foot" style="text-align:center;margin:18px 0">{FOOT}</div></div><script>{js}</script></body></html>')

def _bar():
    return ('<div class="bar"><script defer src="shuffle.js"></script><button id="hide">🙈 Hide all</button>'
            '<button id="all">👀 Show all</button><span class="n" id="n"></span></div>')

def _flags(L):
    if not L.get('flags'):
        return ''
    return ('<div class="flag"><h2>⚠️ Source flags (slides only, transcript pending)</h2><ul>' +
            ''.join(f'<li><b>{E(a)}:</b> {E(b)}</li>' for a, b in L['flags']) + '</ul></div>')

def build_terms(L, css, js, hub, V):
    lc = L['lc']; name = f"{L['emoji']} LC{lc} · {L['title']} ({L['date']})"
    rows = ''.join(f'<tr{" class=star" if t[3] else ""}><td>{E(t[0])}<span class="sl">{E(t[2])}</span></td><td><span class="ans">{E(t[1])}</span></td></tr>' for t in L['terms'])
    st = sum(1 for t in L['terms'] if t[3])
    trap = '<div class="trap"><h2>⚠️ Precision traps</h2><ul>' + ''.join(f'<li>{t}</li>' for t in L['traps']) + '</ul></div>'
    body = (f'<div class="hero"><h1>{E(name)}</h1><p>Say it, then tap the pink box · {len(L["terms"])} terms · Dr. {E(L["prof"])} · from the slides (★ transcript emphasis added after lecture)</p></div>'
            f'{trap}{_bar()}<div class="legend">★ pink rows = flagged on the slide itself · S# = slide number</div>'
            f'<div class="cols"><div class="sec"><h2>{E(name)}</h2><table>{rows}</table></div></div>{_flags(L)}')
    fn = f'cellphys-lc{lc}-terms.html'
    open(fn, 'w').write(_page(f'🧠 LC{lc} {L["title"]}', css, body, js, hub, V))
    return fn, len(L['terms']), st

def build_know(L, css, js, hub, V):
    lc = L['lc']; secs = []; n = 0
    for k in L['know']:
        hide = set(k.get('hide', []))
        th = ''.join(f'<th>{E(h)}</th>' for h in k['headers'])
        trs = ''
        for r in k['rows']:
            tds = ''
            for j, c in enumerate(r):
                if j in hide:
                    tds += f'<td><span class="ans">{E(c)}</span></td>'; n += 1
                else:
                    tds += f'<td>{E(c)}</td>'
            trs += f'<tr>{tds}</tr>'
        note = f'<div class="kn">{E(k.get("note", ""))}</div>' if k.get('note') else ''
        secs.append(f'<div class="sec"><h2>{E(k["title"])} <span class="sl">{E(k["slide"])}</span></h2>{note}<table class="kt"><tr>{th}</tr>{trs}</table></div>')
    body = (f'<div class="hero"><h1>{L["emoji"]} LC{lc} · Know these tables</h1><p>Slide layout kept · say each hidden cell, then tap · {n} cells · Dr. {E(L["prof"])}</p></div>'
            f'{_bar()}<div class="cols" style="display:block">{"".join(secs)}</div>')
    fn = f'cellphys-lc{lc}-know.html'
    open(fn, 'w').write(_page(f'📋 LC{lc} know these', css, body, js, hub, V))
    return fn, len(L['know'])

def build_quiz(L, css, js, hub, V):
    lc = L['lc']; rnd = random.Random(1000 + lc); out = []; q = 0; slots = []
    for it in L['quiz']:
        ok = it['ok']; oks = ok if isinstance(ok, list) else [ok]; bad = list(it['bad'])
        if len(oks) == 1:  # balanced letters: cycle the correct position through all slots
            if not slots:
                slots = list(range(len(bad) + 1)); rnd.shuffle(slots)
            opts = list(bad); rnd.shuffle(opts); opts.insert(min(slots.pop(), len(opts)), oks[0])
        else:
            opts = oks + bad; rnd.shuffle(opts)
        ans = sorted(opts.index(o) for o in oks); q += 1
        m = len(oks) > 1 or 'select all' in it['stem'].lower()
        ob = ''.join(f'<button class="opt">{chr(65 + j)}. {E(o)}</button>' for j, o in enumerate(opts))
        fl = '' if it.get('sure', True) else '<div class="flag">⚠️ Not 100% sure from the slides. Confirm with the transcript.</div>'
        key = ', '.join(chr(65 + a) for a in ans)
        out.append(f'<div class="q" data-a="{json.dumps(ans)}" data-m="{int(m)}"><h3><span>Q{q}</span>{E(it["stem"])}</h3>{ob}'
                   f'{"<button class=chk>Check ✓</button>" if m else ""}<div class="why">✅ <b>{key}</b> · {E(it["why"])}<span class="cite">📖 {E(it["cite"])}</span>{fl}</div></div>')
    note = (f'Exam-style questions on LC{lc} only, written from the slides (<b>not an official key</b>). Tap an answer to check it; select-all needs ✓ Check. '
            f'Keep your FIRST answer unless you can name the fact that proves it wrong. 📖 = slide number.')
    body = (f'<div class="hero"><h1>{L["emoji"]} LC{lc} · {E(L["title"])} quiz</h1><p>{q} questions · Dr. {E(L["prof"])} style · Exam 4</p></div><div class="note">{note}</div>'
            f'<div class="bar"><button id="shuf">🎲 Shuffle</button><button id="miss">🔁 Misses only</button><button id="all">↺ Show all</button><button class="cpy" id="cpy">📋 Copy misses</button><span class="score" id="sc"></span></div>'
            f'<div id="qs">{"".join(out)}</div><div class="done-bar"><button class="cpy opt" style="width:auto;display:inline-block">📋 Copy misses</button></div>')
    fn = f'cellphys-lc{lc}-quiz.html'
    open(fn, 'w').write(_page(f'🧪 LC{lc} quiz', css, body, js, hub, V))
    return fn, q

def build_exam4(HUB, V):
    lecs = _load()
    tcss, tjs = _terms_assets(); qcss, qjs = _quiz_assets()
    head = lambda t: f'<div style="grid-column:1/-1;font-weight:900;color:#70428f;margin-top:8px">{t}</div>'
    have = {L['lc'] for L in lecs}
    pend = [f'LC{n}' for n in range(25, 34) if n not in have]
    tiles = head('📅 Exam 4 · Fri 11/13 · 8:00 AM · 61.5 pts · LC25–LC33' + (f' · coming: {", ".join(pend)}' if pend else ''))
    from cellphys_pathways import build_pathways_e4
    tiles += build_pathways_e4(HUB, V)
    from cellphys_e4_slides import build_slide_pages
    tiles += build_slide_pages(HUB, V)
    rep = []
    for L in lecs:
        tf, tn, st = build_terms(L, tcss, tjs, HUB, V)
        kf, kn = build_know(L, tcss, tjs, HUB, V)
        qf, qn = build_quiz(L, qcss, qjs, HUB, V)
        rep.append((L['lc'], tn, kn, qn))
        tiles += (f'<a class="tile" href="{tf}?v={V}"><div class="emoji">{L["emoji"]}</div><h2>LC{L["lc"]} {E(L["title"])} terms</h2><p>{E(L["date"])} · Dr. {E(L["prof"])} · {tn} terms · ⚠️ traps</p></a>'
                  f'<a class="tile" href="{kf}?v={V}"><div class="emoji">📋</div><h2>LC{L["lc"]} know these</h2><p>{kn} slide tables · tap to reveal</p></a>'
                  f'<a class="tile" href="{qf}?v={V}"><div class="emoji">🧪</div><h2>LC{L["lc"]} quiz</h2><p>{qn} exam-style questions · 📋 copy misses</p></a>')
    print('exam4', rep)
    return tiles
