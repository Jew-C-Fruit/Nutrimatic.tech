# Desk scene art

Version 1.0.0 · Created 2026-10-02

Everything the co-founders' scene draws that is not simple geometry lives here as sprites, and reaches the site as
data in `js/desk-sprites.js`. That file is **generated**: change the sources here and run the exporter.

```bash
python3 tools/desk/export_js.py        # writes js/desk-sprites.js (needs numpy, scipy, pillow)
```

## What is here

| File | What |
| --- | --- |
| `sprites/cole-301-1x.png`, `sprites/ilinca-407-1x.png` | the figures as they came out of `tools/portraits/pixelize.py` |
| `sprites/maker/*.png` | Maker the cat: two walking frames, sitting, yawning, lying with a paw out |
| `sources/` | the full-size generated pictures those came from, and `PROVENANCE.md` (model, prompts, seeds) |
| `characters.py` | the hand finishing of Cole and Ilinca: the face blanked and redrawn feature by feature, the cut into torso and head, the arms taken off, the joints |
| `maker_build.py` | Maker's five poses put on one palette, eyes tidied |
| `spritekit.py` | load a sprite, change pixels, and render it large with a ruler so coordinates can be read off |
| `export_js.py`, `extra_sprites.py` | the exporter |

## How a figure is put together

The scene (`js/desk-scene.js`) draws, in this order: the **torso** layer, the two **upper arms**, the **head** layer
(it moves down a pixel or two for a nod), the face **frames**, then the **forearms and hands** and whatever is held.

- **Face frames** are small lists of pixels drawn over a blank face: eyes (`open` or `down`, looking left, centre or
  right, and `closed`), brows (`neutral`, `up`, `down`, `sad`), and eight mouths (`smile`, `neutral`, `flat`, `frown`,
  `open`, `o`, `laugh`, `yawn`). They are defined in `characters.py` (`eyes`, `brows`, `MOUTHS`).
- **Arms** are not sprites. The scene draws each as two capsules and a hand from the shoulder joints given here
  (`joints`, `arm`), posed by a small inverse-kinematics routine, so any activity can put a hand anywhere.
- `centre` is the sprite column that sits on the character's x; `desk` is the sprite row that meets the desk top.

## Changing something

- **A face detail**: edit the coordinates in `characters.py`, then look before exporting:

  ```python
  from characters import Cole
  Cole.full(look=1, brow='up', mouth='laugh').view('look.png', zoom=22, box=(18, 10, 57, 48))
  ```

- **A new mouth**: add a pattern to `MOUTHS` (letters are colours, `.` leaves the pixel alone), export, and use its
  name as `p.mouth` in the scene.
- **A new portrait**: generate and pixelize (see `tools/portraits/README.md`), put the `-1x.png` in `sprites/`, point
  `BASE` at it, and move the coordinates. Dumping the sprite as a character grid (see the loop at the bottom of
  `characters.py` for the view calls) is the quickest way to find them.
- **A new pose for Maker**: add the sprite to `maker_build.sprites()`; the scene finds it by name (`drawMaker`).
