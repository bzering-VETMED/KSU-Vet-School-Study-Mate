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
("Basel's upper airways are the:",["Nares, nasal cavity, and pharynx","Larynx, trachea, and bronchial tree","Nares, larynx, and trachea","Pharynx, larynx, and bronchi"],"Lower = larynx, trachea, bronchial tree, lungs"),
("The loose connective tissue of the mucosa is the:",["Lamina propria","Submucosa","Adventitia","Muscularis mucosa"],""),
("In the nasal cavity, the submucosa often contains:",["Submucosal (mucus) glands","Olfactory sensory neurons","Cartilage rings","Smooth muscle knobs"],""),
("The cilia and goblet cells of respiratory epithelium work together to:",["Move mucus up the airways to clear debris","Dissolve odors and refresh the olfactory system","Secrete surfactant to lower surface tension","Detoxify inhaled substances with CYP450"],""),
("The larynx is best described as:",["A cartilage-walled structure housing the vocal folds","A muscular tube closed by the trachealis","A bony chamber lined by olfactory epithelium","A thin-walled duct with smooth muscle knobs"],""),
("Club cells act as stem cells in the:",["Bronchioles","Trachea","Nasal cavity","Alveolar sacs"],""),
("Type I pneumocytes are:",["Squamous cells lining alveoli that form the barrier","Cuboidal cells that secrete pulmonary surfactant","Phagocytic cells that keep alveoli free of debris","Non-ciliated cells that break down mucus"],""),
("Alveoli are best described as:",["Blind ends where gas exchange occurs by diffusion","Conducting tubes lined by respiratory epithelium","Transition zones with continuous smooth muscle","Spaces between visceral and parietal pleura"],""),
("A dog has dusky mucous membranes, orthopneic posture, and air outside the lungs on x-ray with no trauma. Diagnosis?",["Spontaneous pneumothorax","Allergic airway inflammation (asthma)","Collapse of the tracheal cartilage rings","Excess pleural fluid from lymphatics"],"Husky case (LC38)"),
("Which reptiles use a diaphragm similar to mammals?",["Crocodilians","Snakes","Lizards that buccal pump","Lizards using chest wall muscles"],""),
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
("Epithelium plus lamina propria (plus muscularis mucosa) make up the:",["Mucosa","Submucosa","Adventitia","Serosa"],""),
("Basel's slide describes the outer layer of the trachea as:",["Adventitia that blends into surrounding tissue","Serosa bounded by a serous membrane","Submucosa with seromucous glands","Muscularis mucosa with the trachealis"],""),
("Which feature is found in bronchi but NOT bronchioles?",["Submucosal (bronchial) glands","Smooth muscle","Ciliated epithelial cells","Lamina propria"],""),
("Club (Clara) cells are:",["Non-ciliated cells of the bronchiolar epithelium","Ciliated cells of the bronchial epithelium","Squamous cells of the alveolar wall","Mucus-secreting cells of the trachea"],""),
("Respiratory bronchioles are the transition between:",["Conducting and gas-exchange airways","Upper and lower airways","Visceral and parietal pleura","The trachea and the bronchi"],""),
("As alveoli crowd the alveolar duct wall, its epithelium:",["Persists only in small cuboidal patches","Becomes taller pseudostratified epithelium","Changes to stratified squamous epithelium","Gains more goblet cells and glands"],""),
("Endothelial cells of the alveolar septum are:",["Squamous cells lining the capillaries","Cuboidal cells that secrete surfactant","Phagocytic cells that remove debris","Columnar cells with motile cilia"],""),
("The pleural cavity wraps around each lung like:",["A double-walled balloon","A C-shaped cartilage ring","A spiral of smooth muscle","A blind-ended alveolar sac"],""),
("Pleural fluid mainly functions to:",["Minimize friction as the lungs move","Exchange gas with pleural capillaries","Secrete surfactant onto the lung surface","Hold the airway cartilage rings open"],""),
("Bronchi have which cartilage arrangement?",["Plates, not complete rings","C-shaped rings closed by muscle","Complete circular rings","No cartilage at all"],""),
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
("Which is NOT true of the trachealis muscle?",["It secretes seromucous fluid","It closes the C-shaped rings","It accommodates the esophagus","It helps prevent collapse on inhalation"],""),
("Which is NOT a cell of the alveoli/alveolar septum?",["Club cell","Type I pneumocyte","Type II pneumocyte","Endothelial cell"],""),
("Compared with bronchial epithelium, bronchiolar epithelium is:",["Simple columnar/cuboidal with club cells","Pseudostratified with goblet cells","Stratified squamous non-keratinized","Olfactory with sensory neurons"],""),
("Which airway has a continuous muscularis mucosa AND openings to alveoli?",["Respiratory bronchiole","Alveolar sac","Bronchus","Alveolar duct"],""),
("Which pair is correctly matched?",["Vestibular fold — respiratory epithelium","True vocal fold — respiratory epithelium","Olfactory region — stratified squamous","Bronchiole — pseudostratified with glands"],""),
("Inflammation in feline asthma leads to all of these EXCEPT:",["Air entering the pleural cavity","Recruitment of more immune cells","Increased mucus secretion","Increased airway muscle contraction"],""),
("A connective tissue layer that blends into surrounding organs is called:",["Adventitia","Serosa","Submucosa","Lamina propria"],""),
("On Basel's upper airway slide, the hard and soft palates separate the nasal cavity from the:",["Oral cavity","Larynx","Trachea","Pleural cavity"],""),
("Alveolar macrophages:",["Phagocytose debris to keep alveoli clear","Secrete surfactant to lower surface tension","Form the blood–air barrier with endothelium","Act as stem cells for bronchioles"],""),
("Which change does NOT occur moving from bronchi to bronchioles?",["Glands increase","Cartilage disappears","Epithelium gets shorter","Club cells increase"],""),
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
        out.append(f'<div class="q" data-a="{json.dumps(ans)}" data-m="0"><h3><span>Q{i}</span>{E(stem)}</h3>{ob}<div class="ans">✅ <b>{chr(65+ans[0])}. {E(opts[ans[0]])}</b>{" · "+E(why) if why else ""}</div></div>')
    open(fn,'w').write(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(title)}</title><style>{CSS}.ans{{display:none;margin-top:8px;padding:10px 12px;border-radius:12px;background:#fdf2f9;font-size:15px}}.q.done .ans{{display:block}}</style></head><body><div class="wrap"><a class="back" href="systems-lec-exam3.html?v={V}">← Back to Exam 4 hub</a><div class="hero"><h1>{E(title)}</h1><p>{E(sub)}</p></div><div class="bar"><button id="shuf">🎲 Shuffle</button><button id="miss">🔁 Misses only</button><button id="all">↺ Show all</button><span class="score" id="sc"></span></div><div id="qs">{"".join(out)}</div></div><script>{JS}</script></body></html>')
import collections
for k,(X,seed) in enumerate(((X1,11),(X2,22),(X3,33)),1):
    q=arrange(X,seed)
    page(f'systems-lec3-basel{k}.html',f'🔬 Basel Practice Exam {k}','25 Q · LC38–39 pulmonary microanatomy · from Basel\'s slides only',q)
    print(k,len(q),''.join(chr(65+a[2][0]) for a in q),collections.Counter(chr(65+a[2][0]) for a in q))
