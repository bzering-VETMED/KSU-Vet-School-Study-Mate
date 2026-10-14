# Build: Systems lecture PRACTICE exams (3 unique exams with drawn ECG strips + action potentials)
# Run from repo root: python3 tools/sys_practice.py   (then python3 tools/sys_lecture.py to refresh the hub)
import html, json, re, sys, time, os
sys.path.insert(0, os.path.dirname(__file__))
from sys_practice_data import EXAMS
E = html.escape; V = str(int(time.time()))
src = open(os.path.join(os.path.dirname(__file__), 'sys_lecture.py')).read()
CSS = re.search(r"CSS='''(.*?)'''", src, re.S).group(1)
CSS += ('.sec{margin:22px 0 4px;padding:10px 14px;border-radius:14px;background:linear-gradient(135deg,#5d347e,#8855b8);color:#fff;font-weight:900;font-size:16px}'
        '.fig{margin:8px 0 10px}.fig figure{margin:0}.fig svg{width:100%;height:auto;border-radius:10px;border:1px solid #eadff2;display:block}'
        '.fig{overflow-x:auto;-webkit-overflow-scrolling:touch}.fig svg[aria-label^="ECG strip"]{min-width:720px}.fig svg[aria-label^="six-lead"]{min-width:460px}.fig figcaption{font-size:12.5px;color:#8a6f98;margin-top:4px}.tf .opt{display:inline-block;width:auto;min-width:110px;margin-right:8px}'
        '.legend{font-size:14px}.legend b{color:#5d347e}')
JS = re.search(r"JS='''(.*?)'''", src, re.S).group(1)
JS = JS.replace("document.getElementById('shuf').onclick=()=>{const w=document.getElementById('qs');[...w.children].sort(()=>Math.random()-.5).forEach(x=>w.appendChild(x))};",
                "document.getElementById('shuf').onclick=()=>{const w=document.getElementById('qs');w.querySelectorAll('.sec').forEach(s=>s.style.display='none');[...w.querySelectorAll('.q')].sort(()=>Math.random()-.5).forEach(x=>w.appendChild(x))};")
JS = ("document.querySelectorAll('.fig[data-fig]').forEach(d=>{const t=document.getElementById('fig-'+d.dataset.fig);if(t)d.appendChild(t.content.cloneNode(true))});" + JS)

NOTE = ('Practice exam written in the style of the 2024/2025 exams and Dr. Musch’s exam setup '
        '(HR 7 · SV 6 · SVR 4 · a-vO2 2 · microcirculation 3 · exercise 6 · heart failure 6 · CV facts 5). '
        'Tap an answer to check it. Select-all questions need ✓ Check. ECG strips and action potentials are drawn for practice '
        '(not the real exam images). Answers come from the lecture slides and transcripts, <b>not an official key</b>. '
        'Each practice exam has different questions.')

def build(fn, title, items, figs):
    out = []; n = 0
    for it in items:
        if it[0] == '§':
            out.append(f'<div class="sec">{E(it[1])}</div>'); continue
        stem, opts, ans, why, sure, fig = it
        n += 1
        m = len(ans) > 1 or 'select all' in stem.lower()
        tf = opts == ['True', 'False']
        ob = ''.join(f'<button class="opt">{"" if tf else chr(65 + j) + ". "}{E(o)}</button>' for j, o in enumerate(opts))
        fl = '' if sure else '<div class="flag">⚠️ Not 100% sure. Confirm with the instructor.</div>'
        fg = f'<div class="fig" data-fig="{fig}"></div>' if fig else ''
        key = ', '.join((opts[a] if tf else chr(65 + a)) for a in ans)
        out.append(f'<div class="q{" tf" if tf else ""}" data-a="{json.dumps(ans)}" data-m="{int(m)}"><h3><span>Q{n}</span>{E(stem)}</h3>{fg}{ob}'
                   f'{"<button class=chk>Check ✓</button>" if m else ""}<div class="why">✅ <b>{E(key)}</b>{" · " + E(why) if why else ""}{fl}</div></div>')
    tpl = ''.join(f'<template id="fig-{k}">{v}</template>' for k, v in figs.items())
    sub = f'{n} questions · ECG & electrophysiology · blood, marrow & hemostasis · defensive cells & lymphatics · Musch cardiovascular physiology'
    open(fn, 'w').write(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
                        f'<title>{E(title)}</title><style>{CSS}</style></head><body><div class="wrap"><a class="back" href="systems-lecture.html?v={V}">← Back to Lecture</a>'
                        f'<div class="hero"><h1>{E(title)}</h1><p>{E(sub)}</p></div><div class="note">{NOTE}</div>'
                        f'<div class="bar"><button id="shuf">🎲 Shuffle</button><button id="miss">🔁 Misses only</button><button id="all">↺ Show all</button><span class="score" id="sc"></span></div>'
                        f'<div id="qs">{"".join(out)}</div>{tpl}</div><script>{JS}</script></body></html>')
    return n

if __name__ == '__main__':
    for fn, title, items, figs in EXAMS:
        print(fn, build(fn, title, items, figs))
