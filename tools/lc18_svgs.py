# Builds the LC18 pathway-map study page
import html

W, H = 700, 340

def tx(x, y, s, cls="lbl", anchor="start"):
    return f'<text x="{x}" y="{y}" class="{cls}" text-anchor="{anchor}">{html.escape(s)}</text>'

CORD = ('<circle cx="120" cy="125" r="62" class="cord"/>'
        '<path transform="translate(0,8)" class="gm" d="M120,95 C112,80 100,70 96,74 C92,80 104,100 108,112 L100,128 C88,140 86,158 98,160 C110,160 116,140 120,135 C124,140 130,160 142,160 C154,158 152,140 140,128 L132,112 C136,100 148,80 144,74 C140,70 128,80 120,95 Z"/>'
        '<ellipse cx="143" cy="128" rx="6" ry="5" class="lh"/>')
PARTS = {
 "droot": '<path class="nv" d="M128,66 C140,38 185,30 210,48 C228,62 238,98 240,128"/><ellipse cx="188" cy="41" rx="13" ry="8" class="gang-faint"/>',
 "vroot": '<path class="nv" d="M140,184 C170,200 222,170 240,128"/>',
 "sn": '<path class="nv thick" d="M240,128 L330,128"/>',
 "db": '<path class="nv" d="M330,128 L392,70"/>',
 "vb": '<path class="nv" d="M330,128 L405,152 L586,152"/>',
 "wr": '<path class="nv" d="M270,128 L280,216"/>',
 "gr": '<path class="nv" d="M294,216 L304,128"/>',
 "trunk": '<path class="nv thick" d="M287,176 L287,326"/>',
 "cg": '<ellipse cx="287" cy="238" rx="15" ry="22" class="gang"/>',
 "own": '<path class="nv" d="M302,238 C380,238 480,228 586,228"/>',
 "spl": '<path class="nv" d="M287,260 C292,292 360,297 435,296"/>',
 "pv": '<ellipse cx="452" cy="296" rx="17" ry="12" class="gang"/>',
 "pvpost": '<path class="nv" d="M469,296 L586,296"/>',
}
LABELS = {
 "lh": tx(70,234,"lateral horn","lbl","middle") + '<path d="M80,223 L141,135" class="lead"/>',
 "dorsal": tx(18,60,"DORSAL","tiny"),
 "ventral": tx(18,200,"VENTRAL","tiny"),
 "drg": tx(188,22,"dorsal root ganglion","lbl","middle"),
 "vroot": tx(188,216,"ventral root","lbl","middle"),
 "sn": tx(246,118,"spinal nerve"),
 "db": tx(398,66,"dorsal branch"),
 "vb": tx(420,144,"ventral branch"),
 "wr": tx(266,184,"white ramus","lbl","end"),
 "gr": tx(310,184,"gray ramus"),
 "cg": tx(268,240,"chain ganglion","lbl","end") + tx(268,254,"(paravertebral)","sub","end"),
 "trunk": tx(278,320,"sympathetic trunk","lbl","end") + tx(278,333,"runs cranial ↕ caudal","sub","end"),
 "own": tx(440,219,"its own nerve (cardiac nerve)","lbl","middle"),
 "spl": tx(362,284,"splanchnic nerve","lbl","middle"),
 "pv": tx(452,326,"prevertebral ganglion","lbl","middle"),
}
def target(y, line1, line2="", on=True):
    cls = "tgt" if on else "tgt off"
    t = f'<rect x="588" y="{y-18}" width="104" height="36" rx="9" class="{cls}"/>'
    if line2:
        t += tx(640, y-3, line1, "tgtt", "middle") + tx(640, y+11, line2, "tgtt", "middle")
    else:
        t += tx(640, y+4, line1, "tgtt", "middle")
    return t

RED_START = "M143,128 L141,168 L140,184 C170,200 222,170 240,128 L270,128 L280,216"
def syn(x,y): return f'<circle cx="{x}" cy="{y}" r="6.5" class="syn"/>'
def ring(x,y,r=11): return f'<circle cx="{x}" cy="{y}" r="{r}" class="ring"/>'
def start_dot(): return '<circle cx="143" cy="128" r="5" class="pre-fill"/>'

def svg(pid, routes, labels, targets, parts_on, extra=""):
    defs = (f'<defs><marker id="{pid}r" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="pre-fill"/></marker>'
            f'<marker id="{pid}b" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="post-fill"/></marker></defs>')
    base = CORD + "".join(f'<g class="{"on" if k in parts_on else "faint"}">{v}</g>' for k,v in PARTS.items())
    r = ""
    for kind, d in routes:
        m = f'{pid}r' if kind=="pre" else f'{pid}b'
        me = f' marker-end="url(#{m})"' if d.rstrip().endswith(("582,152","582,228","582,296")) else ""
        r += f'<path d="{d}" class="route {kind}"{me}/>'
    lab = "".join(LABELS[k] for k in labels)
    return (f'<div class="figwrap"><svg viewBox="0 0 {W} {H}" role="img" class="map">{defs}{base}{targets}{r}{extra}{start_dot()}{lab}</svg></div>')

ALL_T = target(152,"Body wall","& limbs") + target(228,"Heart") + target(296,"Gut / organ")

KEY = svg("k", [], list(LABELS.keys()), ALL_T, set(PARTS.keys()))

P1 = svg("p1",
  [("pre", RED_START+" L285,232"), ("post","M290,232 L294,216 L304,128 L330,128 L405,152 L582,152")],
  ["lh","vroot","sn","wr","cg","gr","vb","trunk","dorsal","ventral"],
  target(152,"Vessels, glands,","hair muscles")+target(228,"Heart",on=False)+target(296,"Gut / organ",on=False),
  {"droot","vroot","sn","db","vb","wr","gr","trunk","cg"},
  syn(287,236))
P2 = svg("p2",
  [("pre", RED_START+" L285,232"), ("post","M292,238 L302,238 C380,238 480,228 582,228")],
  ["lh","sn","wr","cg","own","trunk"],
  target(152,"Body wall","& limbs",on=False)+target(228,"Heart")+target(296,"Gut / organ",on=False),
  {"droot","vroot","sn","wr","trunk","cg","own"},
  syn(287,236))
P3 = svg("p3",
  [("pre", RED_START+" L287,260 C292,292 360,297 436,296"), ("post","M458,296 L582,296")],
  ["lh","sn","wr","cg","spl","pv","trunk"],
  target(152,"Body wall","& limbs",on=False)+target(228,"Heart",on=False)+target(296,"Intestine"),
  {"droot","vroot","sn","wr","trunk","cg","spl","pv","pvpost"},
  ring(287,238,26)+syn(452,296)+tx(320,212,"no synapse","nos"))
P4 = svg("p4",
  [("pre", RED_START+" L287,260 C292,292 360,297 435,296 L582,296")],
  ["lh","sn","wr","cg","spl","pv","trunk"],
  target(152,"Body wall","& limbs",on=False)+target(228,"Heart",on=False)+target(296,"Adrenal","medulla"),
  {"droot","vroot","sn","wr","trunk","cg","spl","pv","pvpost"},
  ring(287,238,26)+ring(452,296,20)+tx(320,212,"no synapse","nos")+tx(470,272,"no synapse","nos")
  + tx(640,332,"epinephrine → blood","nos","middle"))

# parasympathetic diagram
PARA = f'''<div class="figwrap"><svg viewBox="0 0 700 250" role="img" class="map">
<defs><marker id="par" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" class="pre-fill"/></marker>
<marker id="pab" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" class="post-fill"/></marker></defs>
<rect x="16" y="44" width="150" height="56" rx="10" class="src"/>{tx(91,68,"Brainstem nuclei","tgtt","middle")}{tx(91,84,"cranial outflow","sub","middle")}
<rect x="470" y="30" width="214" height="84" rx="12" class="tgt"/>{tx(577,50,"Target organ","tgtt","middle")}{tx(577,100,"heart · lungs · gut","sub","middle")}
<path d="M166,72 L496,72" class="route pre" marker-end="url(#par)"/>
<ellipse cx="510" cy="72" rx="13" ry="10" class="gang"/>{syn(510,72)}
<path d="M523,72 L584,72" class="route post" marker-end="url(#pab)"/>
{tx(320,62,"LONG preganglionic · CN III, VII, IX, X","lbl","middle")}
{tx(577,132,"terminal ganglion sits in the organ wall","lbl","middle")}{tx(553,65,"short","sub","middle")}
<rect x="16" y="164" width="150" height="56" rx="10" class="src"/>{tx(91,188,"Sacral cord S1–S3","tgtt","middle")}{tx(91,204,"lateral horn","sub","middle")}
<rect x="470" y="150" width="214" height="84" rx="12" class="tgt"/>{tx(577,170,"Pelvic organs","tgtt","middle")}{tx(577,220,"colon · bladder · repro","sub","middle")}
<path d="M166,192 L496,192" class="route pre" marker-end="url(#par)"/>
<ellipse cx="510" cy="192" rx="13" ry="10" class="gang"/>{syn(510,192)}
<path d="M523,192 L584,192" class="route post" marker-end="url(#pab)"/>
{tx(320,182,"LONG preganglionic · pelvic nerve","lbl","middle")}
{tx(320,212,"(joins the pelvic plexus)","sub","middle")}
</svg></div>'''

open(__import__("os").path.join(__import__("os").path.dirname(__file__),"lc18_svgs.out"),"w").write(repr({"KEY":KEY,"P1":P1,"P2":P2,"P3":P3,"P4":P4,"PARA":PARA}))
