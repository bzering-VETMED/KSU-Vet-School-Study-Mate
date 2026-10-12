# L19 tracing decks for nerves and arteries (made by Claude). Run from repo root:
# python3 tools/lc19trace.py L19.pdf slide21_img slide23_img slide25_img
import sys, os; sys.path.insert(0, os.path.dirname(__file__)); import tracer as T
pdf, r21, r23, r25 = sys.argv[1:5]

# ---------------- NERVES ----------------
N = []
N.append(T.raster_card(r21, 'lc19n_plexus', [
 ("Suprascapular nerve", [(86,380,310,432)]),
 ("Subscapular nerve", [(165,465,360,516)]),
 ("Cranial pectoral nerve", [(288,503,520,552)]),
 ("Musculocutaneous nerve", [(408,512,665,600)]),
 ("Axillary nerve", [(580,604,702,660)]),
 ("Thoracodorsal nerve", [(755,594,955,646)]),
 ("Radial nerve", [(958,658,1172,722)]),
 ("Median nerve", [(1158,538,1300,596)]),
 ("Ulnar nerve", [(1372,522,1510,580)]),
 ("Lateral thoracic nerve", [(1548,486,1765,540)]),
 ("Caudal pectoral nerve", [(1578,338,1805,396)]),
], "Brachial plexus nerves, cranial → caudal (slide 21)",
 "Name each nerve from cranial to caudal. You don't need the cord segments; he said that isn't tested.", scale=1))
N.append(T.raster_card(r25, 'lc19n_muscles', [
 ("Supraspinatus, infraspinatus", [(793,72,940,123)]),
 ("Subscapularis", [(793,203,938,228)]),
 ("Biceps brachii, brachialis, coracobrachialis", [(793,298,962,372)]),
 ("Deltoideus, teres major, teres minor (subscapularis)", [(793,400,952,505)]),
 ("Triceps brachii, extensor carpi radialis, ulnaris lateralis, common and lateral digital extensors", [(793,569,1040,700)]),
 ("Flexor carpi radialis, superficial digital flexor (deep digital flexor)", [(793,774,1026,853)]),
 ("Flexor carpi ulnaris, deep digital flexor", [(793,903,985,955)]),
], "Nerve → muscles it supplies (slide 25)", "The nerve names are showing. Say every muscle each one supplies, then tap."))
N.append(T.raster_card(r25, 'lc19n_nerves', [
 ("Suprascapular nerve", [(464,85,705,111)]),
 ("Subscapular nerve", [(464,203,645,228)]),
 ("Musculocutaneous nerve", [(465,322,745,346)]),
 ("Axillary nerve", [(464,440,655,466)]),
 ("Radial nerve", [(465,622,675,647)]),
 ("Median nerve", [(465,799,660,824)]),
 ("Ulnar nerve", [(465,916,640,942)]),
], "Muscles → which nerve? (slide 25)", "The muscles are showing. Name the nerve that supplies each group."))
N.append(T.raster_card(r23, 'lc19n_zones', [
 ("Axillary nerve", [(733,416,868,440)]),
 ("Musculocutaneous nerve", [(151,610,402,631)]),
 ("Ulnar nerve", [(712,647,827,668)]),
 ("Radial nerve", [(712,744,837,765)]),
 ("Ulnar nerve", [(283,750,398,770)]),
 ("Radial nerve", [(270,806,395,827)]),
], "Autonomous zones (slide 23)", "Which nerve owns each colored skin zone? Remember: the median nerve has no autonomous zone."))
N.append(T.vector_card(pdf, 24, 'lc19n_sites', [
 ("Musculocutaneous nerve", [(88,110,240,124)]),
 ("2 cm distal to the medial epicondyle of the humerus", [(90,358,215,399)]),
 ("Axillary nerve", [(298,176,370,190)]),
 ("2 cm caudal to the humeral (shoulder) joint", [(227,371,340,398)]),
 ("Radial nerve", [(389,135,451,148)]),
 ("Proximal end of metacarpals II and III", [(348,368,504,395)]),
 ("Ulnar nerve", [(564,95,620,108)]),
 ("Caudal cutaneous antebrachial nerve", [(493,203,598,216)]),
 ("4 cm distal to the olecranon", [(519,349,603,376)]),
 ("Palmar branch", [(594,293,686,305)]),
 ("Lateral surface of the fifth digit", [(615,334,711,360)]),
], "Testing sites for cutaneous nerves (slide 24)", "Name the nerve, then where you pinch to test it.", test=T.black_or_blue, top=92))
NT = [
 ("Brachial plexus is formed by…", ["Ventral branches of spinal nerves C6–T2"]),
 ("Which plexus nerves have cutaneous branches?", ["Musculocutaneous","Axillary","Radial","Median","Ulnar"]),
 ("Which of those has NO autonomous zone?", ["Median nerve"]),
 ("Radial nerve: what kind of muscles?", ["Extensors (triceps, carpal and digital extensors)","The weight-bearing nerve"]),
 ("Median nerve: what kind of muscles?", ["Flexors: flexor carpi radialis, superficial digital flexor (deep digital flexor)"]),
 ("Ulnar nerve supplies…", ["Flexor carpi ulnaris","Deep digital flexor"]),
 ("Lateral thoracic nerve supplies…", ["Cutaneous trunci (the cutaneous trunci reflex)"]),
 ("Cranial vs. caudal pectoral nerve?", ["Cranial pectoral → superficial pectorals","Caudal pectoral → deep pectorals"]),
 ("Autonomous zone vs. overlap zone?", ["Autonomous: center, one nerve only (where you test)","Overlap: edge, two or more nerves"]),
 ("Every plexus nerve carries which fiber types?", ["Motor","Sensory","Sympathetic"]),
]
T.write('gross-anatomy-lc19-nerves.html', '⚡ Thoracic Limb Nerves · Trace It',
        'Lecture 19 · say each name, then tap. Names pop up one at a time.', N, NT)

# ---------------- ARTERIES ----------------
A = []
A.append(T.vector_card(pdf, 5, 'lc19a_proximal', [
 ("Right subclavian a.", [(323,76,439,88)]),
 ("Superficial cervical a.", [(211,104,324,115)]),
 ("Internal thoracic a.", [(359,109,459,120)]),
 ("Axillary a.", [(341,141,402,154)]),
 ("External thoracic a.", [(202,134,290,143)]),
 ("Lateral thoracic a.", [(209,167,291,177)]),
 ("Subscapular a.", [(453,140,542,153)]),
 ("Thoracodorsal a.", [(467,165,557,176)]),
 ("Caudal circumflex humeral a.", [(386,186,542,197)]),
 ("Cranial circumflex humeral a.", [(140,190,298,201)]),
 ("Brachial a.", [(269,227,332,239)]),
 ("Deep brachial a.", [(408,235,494,246)]),
 ("Bicipital a.", [(245,290,300,300)]),
 ("Collateral ulnar a.", [(406,308,502,319)]),
 ("Transverse cubital a.", [(193,316,306,327)]),
 ("Superficial brachial a.", [(169,337,285,348)]),
 ("Cranial superficial antebrachial a. (medial and lateral branches)", [(148,367,302,377),(156,384,287,393)]),
], "Shoulder and arm, right medial view (slide 5)", "Start at the subclavian and work down. Name each artery before you tap."))
A.append(T.vector_card(pdf, 6, 'lc19a_forearm', [
 ("Brachial a.", [(337,117,399,129)]),
 ("Common interosseous a.", [(212,175,348,186)]),
 ("Ulnar a.", [(396,186,436,197)]),
 ("Median a.", [(377,215,436,227)]),
 ("Cranial interosseous a.", [(167,218,287,228)]),
 ("Caudal interosseous a.", [(215,235,325,246)]),
 ("Deep antebrachial a.", [(374,288,484,299)]),
 ("Radial a.", [(311,302,356,312)]),
], "Forearm, right medial view (slide 6)", "The brachial becomes the median once the common interosseous comes off."))
A.append(T.vector_card(pdf, 7, 'lc19a_paw', [
 ("Brachial a.", [(337,59,399,72)]),
 ("Common interosseous a.", [(212,118,348,129)]),
 ("Ulnar a.", [(396,128,436,139)]),
 ("Median a.", [(377,157,436,170)]),
 ("Cranial interosseous a.", [(167,160,287,171)]),
 ("Caudal interosseous a.", [(198,184,307,194)]),
 ("Deep antebrachial a.", [(392,201,502,212)]),
 ("Radial a.", [(387,229,432,240)]),
 ("Deep palmar arch", [(190,262,272,272)]),
 ("Superficial palmar arch", [(448,261,555,270)]),
 ("Palmar metacarpal arteries (deep: deep to the deep digital flexor tendons, in the interosseous muscles)", [(103,278,291,328)]),
 ("Palmar common digital arteries (superficial: between the superficial and deep digital flexor tendons)", [(434,282,604,333)]),
], "Forearm to paw, palmar view (slide 7)", "Trace down to the two palmar arches and what each one gives off.", top=60))
A.append(T.vector_card(pdf, 10, 'lc19a_grid', [
 ("Dorsal common digital arteries", [(167,327,238,395)]),
 ("Dorsal metacarpal arteries", [(260,327,351,378)]),
 ("Palmar metacarpal arteries", [(386,327,476,379)]),
 ("Palmar common digital arteries", [(491,327,562,396)]),
], "⭐ \"All I want you to care about\" (slide 10)", "Superficial = common digital. Deep = metacarpal. Add the surface name."))
AT = [
 ("Main artery chain of the thoracic limb?", ["Subclavian a.","Axillary a.","Brachial a.","Median a.","Superficial palmar arch","Palmar common digital arteries"]),
 ("Where does each name change happen?", ["Subclavian → axillary: at the first rib","Axillary → brachial: after the cranial circumflex humeral","Brachial → median: after the common interosseous"]),
 ("Left vs. right subclavian origin?", ["Left: aortic arch","Right: brachiocephalic trunk"]),
 ("Branches of the subscapular a.?", ["Thoracodorsal a. (→ latissimus dorsi)","Caudal circumflex humeral a."]),
 ("External vs. lateral thoracic a.?", ["External thoracic → superficial pectorals","Lateral thoracic → deep pectorals"]),
 ("Branches of the common interosseous a.?", ["Ulnar a.","Cranial interosseous a.","Caudal interosseous a."]),
 ("Superficial palmar arch is formed by…", ["Median a.","Superficial branch of the caudal interosseous a."]),
 ("Deep palmar arch is formed by…", ["Radial a.","Caudal interosseous a."]),
 ("Why does a sideways cephalic stick hurt?", ["You hit a branch of the radial nerve","(Superficial antebrachial arteries also run beside the vein)"]),
]
T.write('gross-anatomy-lc19-arteries.html', '❤️ Thoracic Limb Arteries · Trace It',
        'Lecture 19 · proximal → distal. Names pop up one at a time.', A, AT)
print('ok', len(N), 'nerve cards,', len(A), 'artery cards')
