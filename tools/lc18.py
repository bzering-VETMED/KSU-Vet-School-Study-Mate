# Lecture 18 ANS pathway quiz deck (made by Claude). Run from repo root: python3 tools/lc18.py
import ast, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(__file__))
import deck
E = deck.E
here = os.path.dirname(__file__)
subprocess.run([sys.executable, os.path.join(here, "lc18_svgs.py")], check=True)
S = ast.literal_eval(open(os.path.join(here, "lc18_svgs.out")).read())

STYLE = """<style>
.cord{fill:#fff;stroke:#B9A8D2;stroke-width:2}.gm{fill:#E3D7F2}.lh{fill:#E3D7F2;stroke:#D2384F;stroke-width:1.5}
.nv{fill:none;stroke:#B9A8D2;stroke-width:4;stroke-linecap:round;stroke-linejoin:round}.nv.thick{stroke-width:6}
.faint .nv{stroke:#E6DEF1}.faint .gang,.faint .gang-faint{fill:#E6DEF1;stroke:#E6DEF1}
.gang,.gang-faint{fill:#EDE4F7;stroke:#B9A8D2;stroke-width:2}
.route{fill:none;stroke-width:4.5;stroke-linecap:round;stroke-linejoin:round}.route.pre{stroke:#D2384F}.route.post{stroke:#2F7FD8}
.pre-fill{fill:#D2384F}.post-fill{fill:#2F7FD8}.syn{fill:#2E2438;stroke:#fff;stroke-width:2.5}
.ring{fill:none;stroke:#5C5068;stroke-width:2;stroke-dasharray:4 4}.tgt{fill:#fff;stroke:#7B54B0;stroke-width:2}.tgt.off{stroke:#E6DEF1}
.src{fill:#EDE4F7;stroke:#D2384F;stroke-width:2}text{font-family:-apple-system,"Segoe UI",Arial,sans-serif}
.lbl{font-size:12.5px;fill:#2E2438;font-weight:700}.sub{font-size:11px;fill:#5C5068}.tiny{font-size:10px;fill:#5C5068;letter-spacing:.1em}
.tgtt{font-size:12.5px;fill:#2E2438;font-weight:700}.nos{font-size:10.5px;fill:#5C5068}.lead{stroke:#5C5068;stroke-width:1;stroke-dasharray:3 3;fill:none}
</style>"""
os.makedirs("assets", exist_ok=True)
def save(key, name):
    svg = re.search(r"<svg.*</svg>", S[key], re.S).group(0)
    svg = svg.replace('<svg ', '<svg xmlns="http://www.w3.org/2000/svg" ', 1)
    vb = re.search(r'viewBox="0 0 (\d+) (\d+)"', svg)
    svg = svg.replace('class="map">', f'class="map">{STYLE}<rect width="{vb.group(1)}" height="{vb.group(2)}" fill="#ffffff"/>', 1)
    open(f"assets/{name}.svg", "w").write(svg)
    return f"assets/{name}.svg"

Q = "Which pathway is this? Say it before you reveal."
cards = [
 deck.img_card_facts(Q, save("P1","lc18_p1"), "Spinal nerve pathway", "Synapse in the chain ganglion, then BACK into the spinal nerve", None,
   [("Where does neuron 1 synapse?","Chain (paravertebral) ganglion"),("How does neuron 2 leave?","Gray ramus → back into the spinal nerve → dorsal or ventral branch"),
    ("Targets?","Blood vessels, sweat glands, arrector pili of the body wall & limbs"),("Dog scenario?","Scenario 1 · body wall & limbs (slide 32)")], "Slide 22"),
 deck.img_card_facts(Q, save("P2","lc18_p2"), "Postganglionic sympathetic nerve pathway", "Synapse in the chain ganglion, then out its OWN nerve", None,
   [("Where does neuron 1 synapse?","Chain (paravertebral) ganglion"),("How does neuron 2 leave?","Its own nerve. NOT the gray ramus, never back into the spinal nerve"),
    ("Classic target?","Heart, through the cardiac plexus"),("Dog · head, neck, thorax (slide 33)?","No chain ganglia in the neck: synapse in the cervicothoracic ganglion (→ vertebral nerve, cardiac nerves), middle cervical ganglion, or cranial cervical ganglion (→ head, via the vagosympathetic trunk)")], "Slide 23"),
 deck.img_card_facts(Q, save("P3","lc18_p3"), "Splanchnic nerve pathway", "Passes THROUGH the chain ganglion, synapses in a PREVERTEBRAL ganglion", None,
   [("Where does neuron 1 synapse?","Prevertebral ganglion (passes through the chain ganglion with no synapse)"),("Pre vs. post length?","LONG pre, SHORT post (the exception)"),
    ("Abdomen in the dog?","Major & minor splanchnic nerves → celiacomesenteric ganglion & plexus; lumbar splanchnic nerves → caudal mesenteric ganglion"),
    ("Pelvis in the dog?","Lumbar splanchnic nerves → caudal mesenteric ganglion → hypogastric nerve → pelvic plexus")], "Slide 24"),
 deck.img_card_facts(Q, save("P4","lc18_p4"), "Adrenal medulla pathway", "No synapse in ANY ganglion", None,
   [("Where does neuron 1 synapse?","Nowhere in a ganglion. It passes through both and ends on the adrenal medulla"),
    ("Is there a neuron 2?","Not a real one. Chromaffin cells are modified postganglionic sympathetic neurons"),
    ("What do chromaffin cells secrete?","Epinephrine and norepinephrine")], "Slide 25"),
 deck.img_card_facts("Which division is this? Name both outflows.", save("PARA","lc18_para"), "Parasympathetic (craniosacral)", "Long pre, short post; terminal ganglia in the organ wall", None,
   [("Which cranial nerves?","III oculomotor · VII facial · IX glossopharyngeal · X vagus"),("Sacral outflow nerve?","Pelvic nerve, from S1–S3"),
    ("Visible in lab?","No. Terminal ganglia sit in the organ wall"),("Which nerve carries ~80% of the outflow?","Vagus nerve (X)")], "Slides 27–30, 37–40"),
 deck.text_card2("Which pathway has NO synapse in any ganglion?","Adrenal medulla pathway","Name it"),
 deck.text_card2("Which TWO pathways synapse in the chain ganglion?","Spinal nerve pathway and postganglionic sympathetic nerve pathway","Name it"),
 deck.text_card2("Which pathway uses the gray ramus to go back into the spinal nerve?","Spinal nerve pathway","Name it"),
 deck.text_card2("Which pathway is the exception with a long preganglionic and short postganglionic neuron?","Splanchnic nerve pathway","Name it"),
 deck.text_card2("How does sympathetic innervation reach the heart?","Postganglionic sympathetic nerve pathway (own nerve → cardiac plexus)","Name it"),
 deck.text_card2("Vertebral nerve: what fiber type?","Postganglionic sympathetic (synapsed in the cervicothoracic ganglion)","Fiber type"),
 deck.text_card2("Major, minor and lumbar splanchnic nerves: what fiber type?","Preganglionic sympathetic","Fiber type"),
 deck.text_card2("Hypogastric nerve: what fiber type?","Postganglionic sympathetic (synapsed in the caudal mesenteric ganglion)","Fiber type"),
 deck.text_card2("Pelvic nerve: what fiber type?","Preganglionic parasympathetic (from S1–S3)","Fiber type"),
 deck.text_card2("Name the 5 named sympathetic ganglia.","Cranial cervical · middle cervical · cervicothoracic · celiacomesenteric · caudal mesenteric","Name them"),
 deck.text_card2("Sympathetic loop around the axillary artery?","Ansa axillaris","Name it"),
 deck.text_card2("Sympathetic supply to the intestine: which pathway?","Splanchnic nerve pathway (synapse in a prevertebral ganglion)","Name it"),
]
html = deck.page("🧠 ANS Pathways · Name It", "Lecture 18 · look at the route, name the pathway, then reveal", "".join(cards), back="gross-anatomy-lecture.html")
html = html.replace("← Back to Practical 2", "← Back to Lecture").replace("← Back to Practical 3", "← Back to Lecture")
open("gross-anatomy-lc18-quiz.html", "w").write(html)
print("ok", len(cards), "cards")
