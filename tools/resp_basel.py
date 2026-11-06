# Build: Exam 4 · three Basel practice exams (LC38–39 pulmonary microanatomy), tap-to-check
# Source: Basel's LC38 + LC39 slides only. Correct answer listed FIRST in each item; letters are
# then spread evenly with no repeat letter twice in a row.
import html,time,re,json,random
E=html.escape; V=str(int(time.time()))
_py=open('tools/sys_lecture.py').read()
CSS=re.search(r"^CSS='''(.*?)'''",_py,re.S|re.M).group(1)
JS=re.search(r"^JS='''(.*?)'''",_py,re.S|re.M).group(1)
X1=[
("Which epithelium lines most of the airways until they enter the lungs?",["Pseudostratified columnar with cilia and goblet cells","Simple columnar/cuboidal with cilia and club cells","Stratified squamous non-keratinized epithelium","Simple squamous epithelium of type I pneumocytes"],"Respiratory epithelium (LC38)"),
("Glands beneath the olfactory epithelium that make mucus to dissolve odors and clear old ones are:",["Olfactory (Bowman's) glands","Submucosal seromucous glands","Bronchial glands of the submucosa","Goblet cells of the epithelium"],"LC38 olfactory slide"),
("The vestibular (false) vocal fold is covered by:",["Respiratory epithelium with mixed glands","Stratified squamous non-keratinized epithelium","Simple cuboidal epithelium with club cells","Olfactory epithelium with sensory neurons"],"True fold = stratified squamous non-keratinized"),
("Tracheal cartilage rings mainly prevent airway collapse during:",["Inhalation, when airway pressure is negative","Exhalation, when airway pressure is positive","Swallowing, when the esophagus expands","Coughing, when the trachealis contracts"],"LC38: rigidity at negative pressures (inhalation)"),
("Scattered tracheal cells, not identifiable on H&E, that secrete serotonin and contribute to asthma when misregulated are:",["Diffuse neuroendocrine cells","Club (Clara) cells","Basal cells","Goblet cells"],"DNES"),
("The outermost connective tissue layer of a respiratory organ is called serosa when it:",["Is bounded by a serous membrane","Blends into connective tissue of other organs","Contains submucosal glands and cartilage","Lies directly beneath the epithelium"],"Blends in = adventitia"),
("In spontaneous pneumothorax, the most common cause of air entering the pleural cavity is:",["Rupture of blebs/bullae on the lung surface","Penetrating trauma through the chest wall","Over-drainage of pleural fluid by lymphatics","Collapse of the trachea during inhalation"],"Failure of the visceral pleura (husky case)"),
("The pleural cavity is held at a slightly negative pressure by:",["Specialized lymphatic drainage","Contraction of the trachealis muscle","Surfactant from type II pneumocytes","Elastic fibers in the visceral pleura"],"LC38 pleural membrane slide"),
("Which species has no pleural space (filled with connective tissue), which may let it snorkel?",["Elephant","Dolphin","Horse","Crocodile"],"Dolphin = collapsible lungs · horse = obligate nasal breather"),
("Which combination identifies a bronchus?",["Pseudostratified epithelium, glands, cartilage plates","Simple cuboidal epithelium, club cells, no cartilage","Smooth muscle knobs with patchy cuboidal epithelium","C-shaped cartilage rings closed by trachealis muscle"],"C-rings + trachealis = trachea"),
("Which is NOT a function of club (Clara) cells?",["Secreting serotonin as neuroendocrine signals","Producing surfactant","Breaking down mucus","Detoxifying substances (CYP450)"],"Club cells also act as stem cells · serotonin = DNES"),
("What distinguishes an alveolar sac from an alveolar duct?",["No smooth muscle knobs and no cuboidal epithelium","Club cells and continuous smooth muscle present","Cartilage plates and submucosal glands present","Pseudostratified epithelium with goblet cells"],"LC39 alveolar sacs slide"),
("The blood–air barrier is formed mainly by:",["Type I pneumocytes and endothelial cells","Type II pneumocytes and endothelial cells","Type I pneumocytes and alveolar macrophages","Club cells and type II pneumocytes"],"Both squamous cells"),
("In feline asthma, the bright branching pattern along the airways on x-ray reflects:",["Inflammation around bronchi and bronchioles","Air pockets in the pleural cavity","Ruptured blebs on the lung surface","Collapse of tracheal cartilage rings"],"Himalayan cat case (LC39)"),
("Birds achieve unidirectional airflow through their lungs using:",["Anterior and posterior air sacs","Buccal pumping with throat muscles","A diaphragm like crocodilians","Gas exchange across the skin"],"Buccal pumping = some lizards · skin = amphibians"),
]
X2=[
("Which three cell types make up the olfactory epithelium?",["Sustentacular, basal, olfactory sensory neurons","Ciliated, goblet, and basal cells","Type I, type II, and macrophages","Ciliated, club, and neuroendocrine cells"],"Bowman's glands sit BELOW it"),
("A muscular fold covered by stratified squamous non-keratinized epithelium is the:",["True vocal fold","Vestibular fold","Soft palate","Nasal concha"],"False (vestibular) fold = respiratory epithelium + mixed glands"),
("In the nasal cavity, the adventitia often contains:",["Bone (nasal conchae, skull)","Cartilage plates","Smooth muscle knobs","Olfactory sensory neurons"],"LC38 upper airway microanatomy"),
("The thin layer of muscle that defines the end of the mucosa is the:",["Muscularis mucosa","Trachealis muscle","Submucosa","Lamina propria"],"Mucosa = epithelium + lamina propria + muscularis mucosa"),
("Moving down the respiratory tree, which DECREASES?",["Relative number of goblet cells","Relative number of club cells","Relative amount of smooth muscle","Number of alveoli opening off the wall"],"Cartilage, glands, epithelial height, goblet cells all decrease"),
("Cuboidal epithelium, continuous smooth muscle, club cells, and scattered alveolar openings identify a:",["Respiratory bronchiole","Alveolar duct","Bronchiole","Alveolar sac"],"Duct = mostly alveoli + knobs"),
("Besides closing the C-shaped rings, the trachealis muscle:",["Accommodates the esophagus during swallowing","Secretes seromucous fluid into the lumen","Pulls the vocal folds together for sound","Keeps air out of the pleural cavity"],"Still rigid enough to prevent collapse on inhalation"),
("Cuboidal alveolar cells that secrete surfactant to reduce surface tension are:",["Type II pneumocytes","Type I pneumocytes","Endothelial cells","Alveolar macrophages"],""),
("Horses are obligate nasal breathers because of:",["The position of the epiglottis","The absence of a pleural space","Collapsible lungs with air sacs","Chest wall muscles that ventilate"],"LC38 species differences"),
("Collapsible lungs in dolphins help them:",["Extract O₂ efficiently and avoid the bends","Snorkel using a connective tissue pleura","Keep air flowing one way through air sacs","Breathe through the skin as adults"],"Elephant = snorkel · birds = air sacs · amphibians = skin"),
("Air entering the pleural cavity collapses the lung because it:",["Removes the negative pleural pressure","Increases friction between the pleurae","Blocks lymphatic drainage of the alveoli","Stops surfactant secretion by type II cells"],"Pneumothorax"),
("Compared with tracheal respiratory epithelium, bronchial epithelium is:",["Shorter, with fewer goblet cells","Taller, with more goblet cells","Simple cuboidal with many club cells","Stratified squamous non-keratinized"],"Still pseudostratified columnar with cilia"),
("Which structure is ABSENT from bronchioles?",["Cartilage","Smooth muscle","Ciliated cells","Club cells"],"Also no glands"),
("The 'smooth muscle knobs' of alveolar ducts are really:",["A spiral of smooth muscle seen in cross-section","Remnants of the bronchial cartilage plates","Clusters of type II pneumocytes","Bundles of collagen and elastin"],"Covered by a few cuboidal cells"),
("The serous membrane that covers the surface of the lung is the:",["Visceral pleura","Parietal pleura","Pleural cavity","Adventitia"],"Parietal = on the thoracic wall"),
]
X3=[
("Which statement about respiratory epithelium is INCORRECT?",["It is simple cuboidal with many club cells","Its cilia move mucus up the airways","Its goblet cells produce mucus","It covers most airways until the lungs"],"That's bronchiolar epithelium"),
("Snakes and many lizards ventilate their lungs mainly with:",["Muscles of the chest wall","A diaphragm like mammals","Buccal pumping of the throat","Gas exchange across the skin"],"Crocodilians = diaphragm · some lizards = buccal pumping"),
("Adult amphibians depend significantly on which for gas exchange?",["Skin, along with simple lungs","Anterior and posterior air sacs","A muscular diaphragm","Collapsible lungs"],"Larvae = gills and/or skin"),
("The glands in the tracheal submucosa are:",["Seromucous glands","Olfactory (Bowman's) glands","Goblet cells","Absent, as in bronchioles"],""),
("The relative number of club cells is highest in the:",["Respiratory bronchioles","Trachea","Bronchi","Nasal cavity"],"Club cells increase down the tree"),
("Simple columnar/cuboidal ciliated epithelium with club cells, a muscularis mucosa, no glands, and no cartilage is a:",["Bronchiole","Bronchus","Alveolar duct","Trachea"],""),
("In alveolar ducts, the epithelium is:",["Simple cuboidal, only in small patches","Pseudostratified with goblet cells","Continuous simple cuboidal with club cells","Completely absent, as in sacs"],"Sacs = no cuboidal left"),
("The stroma of the alveolar septum is made mostly of:",["Collagen and elastin","Hyaline cartilage plates","Smooth muscle knobs","Seromucous glands"],"LC39 blood–air barrier slide"),
("Diffusion across the blood–air barrier is limited mainly by its:",["Area and thickness","Cilia and goblet cell number","Cartilage and smooth muscle","Pleural fluid volume"],"Big area + thin barrier = efficient exchange"),
("The cause of feline asthma is:",["Over-reactive immune cells: more mucus and muscle contraction","Ruptured blebs that let air into the pleural cavity","Parasitic infection of the bronchioles","Loss of type II pneumocytes and surfactant"],"Parasites and pneumonia were ruled out in the case"),
("Which is NOT a role of the pleural membrane and cavity?",["Exchanging O₂ with the pulmonary capillaries","Lubricating the lungs to reduce friction","Keeping a slightly negative pressure","Supporting lung movement and inflation"],""),
("Submucosal glands of the airways are found in the:",["Submucosa","Lamina propria","Adventitia","Muscularis mucosa"],""),
("Which is the correct airflow order?",["Nares → nasal cavity → pharynx → larynx → trachea","Nares → pharynx → nasal cavity → larynx → trachea","Nares → nasal cavity → larynx → pharynx → trachea","Nasal cavity → nares → pharynx → trachea → larynx"],""),
("Which structure does Basel classify as part of the LOWER airways?",["Larynx","Pharynx","Nasal cavity","Nares"],"Upper = nares, nasal cavity, pharynx"),
("Which feature is continuous in respiratory bronchioles but breaks into knobs in alveolar ducts?",["Smooth muscle (muscularis mucosa)","Hyaline cartilage plates","Goblet cells","Submucosal glands"],""),
]
def letters(n,seed):
    r=random.Random(seed)
    while True:
        s=([0,1,2,3]*((n+3)//4))[:n]; r.shuffle(s)
        if all(s[i]!=s[i+1] for i in range(n-1)): return s
def arrange(qs,seed):
    out=[];L=letters(len(qs),seed)
    for (stem,opts,why),t in zip(qs,L):
        rest=opts[1:]; random.Random(seed+len(stem)).shuffle(rest)
        o=rest[:]; o.insert(t,opts[0]); out.append((stem,o,[t],why))
    return out
def page(fn,title,sub,qs):
    out=[]
    for i,(stem,opts,ans,why) in enumerate(qs,1):
        ob=''.join(f'<button class="opt">{chr(65+j)}. {E(o)}</button>' for j,o in enumerate(opts))
        out.append(f'<div class="q" data-a="{json.dumps(ans)}" data-m="0"><h3><span>Q{i}</span>{E(stem)}</h3>{ob}<div class="why">✅ <b>{chr(65+ans[0])}</b>{" · "+E(why) if why else ""}</div></div>')
    open(fn,'w').write(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(title)}</title><style>{CSS}</style></head><body><div class="wrap"><a class="back" href="systems-lec-exam3.html?v={V}">← Back to Exam 4 hub</a><div class="hero"><h1>{E(title)}</h1><p>{E(sub)}</p></div><div class="bar"><button id="shuf">🎲 Shuffle</button><button id="miss">🔁 Misses only</button><button id="all">↺ Show all</button><span class="score" id="sc"></span></div><div id="qs">{"".join(out)}</div></div><script>{JS}</script></body></html>')
import collections
for k,(X,seed) in enumerate(((X1,11),(X2,22),(X3,33)),1):
    q=arrange(X,seed)
    page(f'systems-lec3-basel{k}.html',f'🔬 Basel Practice Exam {k}','15 Q · LC38–39 pulmonary microanatomy · from Basel\'s slides only',q)
    print(k,len(q),''.join(chr(65+a[2][0]) for a in q),collections.Counter(chr(65+a[2][0]) for a in q))
