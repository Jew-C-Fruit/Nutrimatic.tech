# Hands in the desk scene: rules, style cards, sources

Version 1.0.0 · Created 2026-10-06 (to-do round 31; Cole: "a workflow with example hands for every state, with a
selection process similar to how we did the faces" and "hands can read as hands without showing all 5 fingers. There
are methods for simplifying them while still having them read right.")

The scene shows the figures on a 360x160 canvas at 2x on a desktop (3x on wide screens) and about 1.46x on a phone. A
hand is 14-22 sprite pixels wide. At that size a hand reads from its **silhouette** and a few **tone clusters**, never
from counting fingers. This note is the brief for every hand drawn for the scene; the style round decides which card
below becomes the house style.

## Why the earlier hands failed (2026-10-06 review)

- "Fin": four fingers pressed into one flat paddle of skin, black separation only at the very tips, tips in one even
  arc, finger lines in a low-contrast skin tone that vanish at 2x and at night (the old WAVE_HAND, PET_ARM_COLE).
- "Paw": four equal rounded tips in a row, no thumb (the old ILINCA_YAWN_HAND).
- "Toes": finger columns hanging below the knuckles of a resting hand (the old REST_HAND).
- "Mush": hands reduced from whole-body generated pictures, already broken in the picture.
- "Backward": the palm and thumb shown where the angle shows the back of the hand (the old PHONE_GRIP).
What passed: Ilinca's clasped resting hands, her wave, the DS grip (drawn from Cole's photo), the shaker grips (fingers
as bars across a rigid object).

## Simplification methods (research)

- **Mitten first, then fingers.** Treat the four fingers as one shape and the thumb as its own; add divisions only where
  they carry the gesture (Preston Blair, *Cartoon Animation*: "conceive the hand as a mitten first"; Richard Williams,
  *The Animator's Survival Kit*; Leriisa, "Simplifying the Hand", Clip Studio Tips).
- **Bundling.** Middle and ring finger as one unit, so the hand reads as three fingers + thumb (David Rickert,
  "3 finger bundling"); the four-finger cartoon convention works because the eye completes the hand.
- **Hide fingers behind fingers** by the angle of view (Rickert).
- **Separate only the finger that matters**: the index for a pen, a pinch or a point; a pinky out for grace; group the
  rest (Clip Studio, Konart; Prokopenko).
- **Imply, don't draw**: one notch cut into the silhouette, a knuckle ridge, or a value change says "fingers"; an
  outline per finger at this size makes a paddle with stripes.
- **Uneven tips**: stagger the fingertips (the middle highest, the pinky clearly lower and splayed) so the mass never
  reads as a paddle or "a bunch of bananas" (Disney).
- **Pixel practice**: silhouette first; as few clusters as possible and no one-pixel clusters (Saint11); darker
  colours, not black, inside a shape and selective outline where a shape meets a lighter one (Derek Yu; skeddles,
  Lospec "Pixel Art Outlines"); keep hands simple and finish them last, copy reference closely (2D Will Never Die);
  the sleeve or cuff edge marks where the hand starts (Slynyrd).

At this size: **open hands** = three units + thumb (or a mitten with one deep notch and an unmistakable thumb);
**resting hands** = the back of the hand as one plane, the knuckle ridge, one band for the finger fronts with at most two
divisions, a separate thumb wedge, a flat contact with the desk, never separate tips; **grips** = 2-px bars across the
object, the thumb on the other side; **pinch** = thumb + index, the rest one mass; **at the face or on Maker** = the back
of the hand, the thumb, one or two tip notches. **The thumb is never optional.**

## Rules (each checked by tools/desk/hands/lint.py)

| # | Rule |
| --- | --- |
| R1 | Silhouette first: filled in one colour, at 1x and 2x, on the wall and on the shirt, the hand says what it does. Open hands: at least (units - 1) notches 2 px deep and a thumb V 2 px deep. |
| R2 | No fin, paw or toes: never four equal parallel fingers, never three or more equal tips in an even arc, never tips hanging below a resting hand's knuckles. Stagger tips (middle highest; index and ring 1 row lower; pinky 2-3 rows lower, splayed 1 px). |
| R3 | The thumb is its own shape: a background V when open, an outline where it crosses the palm or an object; 2-3 px wide, widening into the heel of the hand. |
| R4 | Fingers 2 px wide (3 px only on a palm 15 px or wider); nothing under 2 px; a bundle is two fingers with one short line at its tip. |
| R5 | Where fingers are apart the gap is background or black from the tip for at least half the finger; where they touch, a crease-tone line no longer than 3 px. |
| R6 | Three skin tones plus a crease tone (roles 2 light, 3 mid, 4 shadow, 5 crease; 1 highlight in clusters of 2+); light from the upper left like the face and forearms; the forearm's shadow band carries on into the hand. |
| R7 | Black outline wherever skin meets something that is not skin (wall, desk, shirt, blazer, hair, face, object), except the soft card's lit edges; never black inside the hand (a black pixel with skin on three sides), never a 2x2 black block. |
| R8 | Size from the forearm: palm width = forearm width at the wrist + 1-3 px; wrist to middle fingertip 1.7-2.0 x the forearm width; the card's exaggeration applies to the hand only. Ilinca's hands 1 px narrower and 2 px shorter than Cole's in the same state. |
| R9 | Hands on the desk, seen from the front just above the desk top: the back of the hand a lit plane 3-5 rows deep, the knuckle ridge as a light/mid boundary, the finger fronts a 2-3 row band with at most 2 divisions, the bottom edge on the desk-top row, the thumb a lit wedge on the inner side. |
| R10 | Objects are the canonical sprites at their size: the mug (tools/desk/hands/slots.py MUG, 14x12; to-do T47), the shaker, the plane, the laptop; fingers in front of an object keep their outline. |
| R11 | Joins: the hand starts on the forearm's own outline columns; the shade band continues within 1 px; Ilinca's white cuff row stays between sleeve and hand. |
| R12 | Motion frames move whole clusters 1-2 px; silhouette overlap between frames at least 85%; no single-pixel flicker. |
| R13 | Night: separations must still read under the night overlay; a crease-tone line alone is not a separation. |

## Palette roles

Maps are written with ROLE digits for skin (1 highlight, 2 light, 3 mid, 4 shadow, 5 crease), `k` for the outline, `.`
to keep a pixel, `_` to clear one, and the figure's own letters for anything else (tools/desk/poses.py KEYS: Cole's
shirt `t`/`u`; Ilinca's blazer `j`/`J`, white top or cuff `W`; reds `r`/`R`, grey `g`). No new colours: Ilinca's
palette holds 33 of the format's 36.

| Role | Cole | Ilinca |
| --- | --- | --- |
| 1 highlight | #f9eee0 | #faebe1 |
| 2 light | #f8cda6 | #f9e2d2 |
| 3 mid | #f6af8d | #f1a49b |
| 4 shadow | #ee947c | #d18881 |
| 5 crease | #dc7f6d | #b5705f |
| k outline | #010101 | #010100 |

## The five style cards (the style round)

Each candidate in the style round is labelled with its attribute codes, so Cole can combine attributes as he did with the
faces (for example "F2 fingers with V4 shading and O1 outline").

| Attribute | H1 Mitten | H2 Bundled three | H3 Full four | H4 Soft clusters | H5 Bold planes |
| --- | --- | --- | --- | --- | --- |
| F fingers | F1: one mass; an open hand gets exactly one black notch (index from the rest), 2 px deep | F2: index 2 px, middle+ring bundle 4 px with a 2-3 px crease line from its tip, pinky 2 px set 2-3 rows lower | F3: four fingers 2 px each | F4: three or four implied by tone | F5: three square-ended blocks (index, middle+ring, pinky) |
| S separation | S1: silhouette only | S2: black for half the finger length, then crease tone | S3: shared black separators half way, then crease tone | S4: 1-px tip notches and fingers alternating light/mid, no lines | S5: black notches 3 px deep and hard plane changes |
| V shading | V1: light + shadow band only | V2: light, mid, shadow; highlight at most 2 px | V3: light, mid, shadow, crease; highlight clusters of 2+ | V4: highlight, light, mid, shadow in soft clusters of 3+ | V5: three hard planes: top light, front mid, shadow |
| O outline | O1: black all round | O2: black outside, crease tone inside | O2 | O4: selective: black on shadow sides and at the desk, crease tone on lit edges against the wall, none against black cloth | O5: black, 2 px where the hand sits on the desk |
| Z size | x1.10 | x1.05 | x1.00 | x1.00 | x1.15-1.20 |
| shape | round | round | round | soft | angular |

Shared micro-pattern for separated fingers (H2, H3): a black separator with staggered tips, the fix for the fin.

```
....kk.    the higher fingertip, corners cut
.kkk22k    the lower fingertip's cap meets the black separator
k22k22k    black separator for half the finger length
k22k22k
k22522k    then crease tone where the fingers touch
```

Fingers shown per hand type:

| Hand type | H1 | H2 | H3 | H4 | H5 |
| --- | --- | --- | --- | --- | --- |
| Open (wave, talk, surprise, highfive) | mitten + 1 notch + thumb | 3 units + thumb | 4 + thumb | 3-4 implied + thumb | 3 blocks + thumb |
| Resting on the desk | one band, thumb bump | knuckle ridge with 2 dips (3 fronts) | 3 divisions, band 2 rows max | 1-2 bottom notches over value planes | 2 planes, 1 notch |
| Grip (mug, shaker, phone, pen, iron) | one band | 3 bars | 4 bars (as the DS grip) | alternating value bars | 2-3 square-ended bars |
| Pinch (plane, paper) | thumb + index, rest one mass | rest as a bundle | rest 3 curled | value mass | bundle block |
| Fist (chin, fist pump, thumbs-up) | loaf + thumb across | ridge with 2 dips | ridge with 3 dips | values | plane + 1 notch |
| At the face (yawn, facepalm, ear) | mitten + thumb | index + bundle | 4 if room | values | blocks |
| On Maker (petting) | plane + thumb | ridge + 2 tip notches | 3 tip notches | values + 1-2 notches | planes + 1 notch |

## Workflow (tools/desk/hands)

1. References: photoreal close-ups made with klein 4B (work/hands/refgen), checked for anatomy; the founders' own photos
   where those don't convince (private, work/refs-user/hands, never published).
2. A trace kit per reference (reduce.py): the hand at the slot's size, the scene's angle.
3. Candidates drawn over the trace, in a card (or the chosen style), as JSON candidate files; view.py shows each in the
   live scene; lint.py and a blind legibility test gate them.
4. Cole picks on a selection page (per state; attributes combinable); picks become constants in tools/desk/hand_maps.py.

## Sources

- Preston Blair, *Cartoon Animation* (hands as mittens), via Gurney Journey: http://gurneyjourney.blogspot.com/2012/03/drawing-cartoon-hands.html
- Richard Williams, *The Animator's Survival Kit* (Faber, 2001), hands chapter
- David Rickert, "Drawing hands: 3 finger bundling": https://davidrickert.substack.com/p/drawing-hands-3-finger-bundling
- Leriisa, "Hand Gestures and Simplifying the Hand", Clip Studio Tips: https://tips.clip-studio.com/en-us/articles/3251
- Konart, "Draw Better Hands", Clip Studio Tips: https://tips.clip-studio.com/en-us/articles/3319
- Stan Prokopenko, Proko, "How to Draw Hands": https://www.proko.com/course-lesson/how-to-draw-expressive-hands
- Derek Yu, "Pixel Art Tutorial: Basics": http://derekyu.com/makegames/pixelart.html
- skeddles, "Pixel Art Outlines Part 2: Using Color", Lospec: https://lospec.com/articles/pixel-art-outlines-part-2-using-color/
- Pedro Medeiros (Saint11), "Cluster Sketching and Painting": https://saint11.art/pixel_art_articles/article2/
- 2D Will Never Die, "A Basic Sprite Tutorial" and "Fix My Sprite!": https://2dwillneverdie.com/tutorial/a-basic-sprite-tutorial/
- Slynyrd, Pixelblog catalogue: https://www.slynyrd.com/pixelblog-catalogue
- Screen Rant, why cartoon characters have four fingers: https://screenrant.com/cartoon-characters-four-fingers-hands-animation-reason/
