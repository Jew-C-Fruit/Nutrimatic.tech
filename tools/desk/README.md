# Desk scene art

Version 1.1.0 · Created 2026-10-02 · Modified 2026-10-02 (body poses: arms and hands are generated, not drawn)

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
| `characters.py` | the hand finishing of Cole and Ilinca: the face blanked and redrawn feature by feature, the cut into torso and head |
| `poses.py`, `pose_sprites.py`, `sprites/poses/`, `pose-prompts/` | the body poses: every activity's arms, hands and props, generated, reduced and cut to fit under the head |
| `maker_build.py` | Maker's five poses put on one palette, eyes tidied |
| `spritekit.py` | load a sprite, change pixels, and render it large with a ruler so coordinates can be read off |
| `export_js.py`, `extra_sprites.py` | the exporter |

## How a figure is put together

The scene (`js/desk-scene.js`) draws, in this order: the **body pose** for the current activity (torso, arms, hands
and whatever they hold, all one generated picture), the **head** layer (it moves down a pixel or two for a nod), the
face **frames**, and for a few poses a **front** part that covers the face (a mug at the mouth). After the desk is
drawn, the part of the pose below the desk line goes on again, so hands lie over the desk edge.

- **Face frames** are small lists of pixels drawn over a blank face: eyes (`open` or `down`, looking left, centre or
  right, and `closed`), brows (`neutral`, `up`, `down`, `sad`), and eight mouths (`smile`, `neutral`, `flat`, `frown`,
  `open`, `o`, `laugh`, `yawn`). They are defined in `characters.py` (`eyes`, `brows`, `MOUTHS`).
- **Body poses** (`poses.py`, `pose_sprites.py`, `sprites/poses/<who>/`). Arms drawn in code looked dreadful, so
  every activity has a pose made by the image model: the figure's own portrait is put on a larger canvas sitting
  behind a flat blue desk at the scene's desk line (`pose_sprites.make_stage`), and the model is asked to keep
  everything and change only the arms (`pose-prompts/`). The picked picture is reduced on the base sprite's own grid,
  snapped to the figure's palette plus a few prop colours, its head cut away (the neck under the jaw and, for Ilinca,
  her white top are taken from the base so every pose joins the same head), and stored as a sprite. `MANUAL` in
  `poses.py` holds, per pose, the box that goes in front of the face and named points (the soldering iron's tip, the
  high-five hand).
- `centre` is the sprite column that sits on the character's x; `desk` is the sprite row that meets the desk top.

## Making or replacing a pose

1. Stage pictures: `pose_sprites.make_stage(source, grid json, desk row, out)` for each figure (`sources/` and the
   `sprites/*.json` grids).
2. Generate candidates on the GPU machine, for example
   `generate_comfy.py --model klein --photo cole-stage.png --megapixels 0 --size 1408x1760 --prompt "<prefix> <pose> <style>" --n 3`
   with the texts in `pose-prompts/`.
3. Look at them as the scene will show them (reduce, put the base head on, compose; the session that built this used a
   sheet per figure), pick one, and store it with `poses.pick(who, pose, picture)`.
4. If something must cover the face, add its box to `MANUAL`; then `export_js.py`. The scene finds poses by name
   (`POSE_OF` in `desk-scene.js` maps activities to poses).

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
