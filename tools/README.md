# Deck builder tools (made by Claude)
- `deck.py`: page template, staged-reveal cards (`img_card2` = name → O → I → A; `img_card_facts` = name → custom facts; `text_card2` = text Q→A), `write_lab()` = small-block hub + main/extra decks, auto image cache-busting.
- `unlabel.py`: erases slide/PDF text labels by inpainting only the letter strokes (never boxes, never blur over anatomy).
- `oia_thoracic.py`, `oia_pelvic.py`: professor's origin/insertion/action lists.
- `labN.py`: the build script used for each Gross Anatomy Practical 2 lab (reference examples; source image paths point to Claude's sandbox and must be re-created).
