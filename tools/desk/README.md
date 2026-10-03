# Desk scene art

Version 1.5.0 · Created 2026-10-02 · Modified 2026-10-03 (motion frames for every activity, hands under the desk for Maker, everything on the desk edge-on, a looking-down head)

Everything the co-founders' scene draws that is not simple geometry lives here as sprites, and reaches the site as
data in `js/desk-sprites.js`. That file is **generated**: change the sources here and run the exporter.

```bash
python3 tools/desk/export_js.py        # writes js/desk-sprites.js: the figures, their poses, Maker (needs numpy, scipy, pillow)
python3 tools/desk/env_build.py        # writes assets/desk/*.png: the room, the desk, the skyline, the lamps, the props
```

## What is here

| File | What |
| --- | --- |
| `sprites/cole-301-1x.png`, `sprites/ilinca-407-1x.png` | the figures as they came out of `tools/portraits/pixelize.py` |
| `sprites/maker/*.png` | Maker as first reduced (v1.0; `maker_build.py` now reduces her again from `sources/` at a fifth bigger) |
| `sources/` | the full-size generated pictures those came from, and `PROVENANCE.md` (model, prompts, seeds) |
| `characters.py` | the hand finishing of Cole and Ilinca: the face blanked and redrawn feature by feature, the cut into torso and head |
| `poses.py`, `pose_sprites.py`, `sprites/poses/`, `pose-prompts/` | the body poses: every activity's arms, hands and props, generated, reduced and cut to fit under the head |
| `maker_build.py` | Maker: her generated pictures reduced to size (her head the same size in every pose), five greys with light on her back, big stylized eyes, blink and kneading frames |
| `env_build.py`, `env_guides.py`, `env-prompts/` | the room, the desk, the Midtown skyline (day and night), the anglepoise lamps and the desk props, written as PNGs to `assets/desk/` |
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

- **Hands** (`poses.soften`): inside skin, a black line between skin and skin (finger gaps, knuckles, forearm creases)
  becomes the darkest skin tone, and black stays only on a hand's outside edge; the same for stray black strokes inside
  the clothes. That is what makes the hands read as hands at this size. What is still wrong in one pose is fixed pixel
  by pixel in `MANUAL[who][pose]['fix']`, after looking at the hand zoomed next to its generated picture.
- **Props and frames** (`MANUAL`): `props` lifts a prop out of a pose so the scene can draw it alone (the laptop or
  the paper stays on the desk while the hands are under it for the cat; the soldering board while Cole waves smoke
  away; the shaker bottle), `empty` makes the pose without it (`offerEmpty`), and `frames` makes extra frames by moving
  a box and/or editing pixels (the writing hand: `write1`, `write2`).
- **Motion** (Cole's note 9: something always moves): every activity has small motion frames that the scene steps
  through (`MOTION` in `js/desk-scene.js`): typing forearms `type1`/`type2` and a hand to the trackpad `typetrack`,
  thumbs on the console `ds1`/`ds2`, a fidgeting hand `rest1`, a scrolled phone `phone1`, `solder1`, and a second way
  of holding the iron (`solder2`, its own picture). A frame moves a pixel or two, never more.
- **Hands under the desk** (`hide`): when Maker walks past, hands go down out of her way instead of up in the air.
- **Looking down** (`characters.py`: `down_blank`, `down_layers`, `down_frames`): a second head for each, tipped toward
  the desk, from a generated picture of them looking down, finished in the base face's style. The scene draws it
  whenever they look down at something (the work, the cat, a pointer over the desk) and for a nod; only the mouth
  changes on it.
- **Flat desk**: the desk is seen straight from the front, so anything lying on it is drawn edge-on (the paper, the
  soldering boards, the papers by the plant), never from above.
- **Fronts**: `front_mode='limb'` draws a hand or sleeve, not the pose's own hair, over Ilinca's long hair.

## The room (env_build.py)

Generated like the figures (FLUX.2 klein 4B on bigbaby, `env-prompts/`), from flat layout guides (`env_guides.py`) so
the window, poster, clock and shelves land where the scene needs them, then reduced at cell 4 to 360x160 (240x160 for
the phone). The window glass is cut out: the scene paints the sky by the hour behind it, then the skyline picture (day,
and the night one faded in at dusk). The poster's mark and the clock's hands are drawn by the scene on the generated
board and face. The lamps are one generated lamp, recoloured white for Ilinca and mirrored. Mondrian's Victory Boogie Woogie hangs where
the poster was (the poster edited out of the generated rooms; the painting reduced from a photograph, its colours
favoured over the white so its small squares survive). `sources/PROVENANCE.md`
lists every picture, prompt and seed, and the photographs the skyline follows (CC BY, credited there).

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
