"""Practical 4 bold-term lists, SAME order as Bethany's Canvas bold-term lists (Lab 26: Canvas "LAB 26: BOLD TERMS" page — its cranial/caudal branches belong to the SAPHENOUS artery).
Format matches tools/bold.py: (term, [lowercase search aliases], note).  Made by Claude."""
from bold import T
import p3bold
P4BOLD={
25: p3bold.P3BOLD[25],   # Lab 25 = male + female reproductive (same list as built for Practical 3)
26:[T('caudal gluteal artery'),T('cranial gluteal artery'),T('cranial gluteal nerve'),T('iliolumbar artery'),
    T('external iliac artery','external iliac arteries','ext. iliac'),T('vascular lacuna'),T('deep femoral artery'),
    T('caudal epigastric artery'),T('femoral triangle'),T('medial circumflex femoral artery'),
    T('deep branch (medial circumflex femoral artery)','deep branch of medial circumflex femoral','deep branch of the medial circumflex femoral'),
    T('transverse branch (medial circumflex femoral artery)','transverse branch of medial circumflex femoral','transverse branch of the medial circumflex femoral'),
    T('femoral artery'),T('superficial circumflex iliac artery'),T('lateral circumflex femoral artery'),
    T('proximal caudal femoral artery'),T('saphenous artery'),T('saphenous nerve'),
    T('medial saphenous vein'),
    T('cranial branch (saphenous artery)','cranial branch of the saphenous artery','cranial branch of saphenous artery'),
    T('caudal branch (saphenous artery)','caudal branch of the saphenous artery','caudal branch of saphenous artery'),
    T('lateral saphenous vein'),
    T('cranial branch (lateral saphenous vein)','cranial branch of the lateral saphenous vein','lateral saphenous vein cranial branch','cranial branch of lateral saphenous vein'),
    T('caudal branch (lateral saphenous vein)','caudal branch of the lateral saphenous vein','lateral saphenous vein caudal branch','caudal branch of lateral saphenous vein'),
    T('descending genicular artery'),T('middle caudal femoral artery'),T('distal caudal femoral artery'),
    T('popliteal artery'),T('cranial tibial artery')],
}
