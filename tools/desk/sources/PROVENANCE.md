# Where the pictures in this folder came from

Version 1.1.0 · Created 2026-10-02 · Modified 2026-10-02 (the room, the skyline, the lamps, props, Maker's new poses)

Everything here was generated on bigbaby (RTX 3090) with **FLUX.2 klein 4B** (Black Forest Labs, Apache 2.0, 4-step
distilled) through ComfyUI, driven by `tools/portraits/generate_comfy.py`. 1024x1280 for the people, 1024x768 for
Maker. The reference photos are private and are not in this repo.

| File | Prompt | References (image 1, 2, 3) | Seed |
| --- | --- | --- | --- |
| `cole-merged-seed301.png` | `cole-merge.txt` + `style.txt` | three earlier candidates: C9 (face), C3 (hair and body), C1 (skin) | 301 |
| `ilinca-confident-seed407.png` | `ilinca-confident.txt` + `style.txt` | candidate I4, the studio photo | 407 |
| `maker-walk-seed503.png`, `-seed504.png` | `maker-poses.txt` walk + `maker-style.txt` | three photos of her | 503, 504 |
| `maker-sit-seed511.png` | sit | same | 511 |
| `maker-yawn-seed521.png` | yawn | same | 521 |
| `maker-loaf-seed533.png` | loaf | same | 533 |

The candidates C1 to C12 and I1 to I12 were made with `cole-edit.txt` / `ilinca-edit.txt` + `style.txt`, seeds 101 to 112
(Cole: a three-quarter photo, a front photo and the deck headshot) and 201 to 212 (Ilinca: the studio photo).

Each picture was reduced with `tools/portraits/pixelize.py --cell 12` (people) or to a target size (Maker, since v1.1 of
`maker_build.py`: 62 px long walking, 45 px tall sitting, 60 px long lying) to give the sprites in `../sprites/` and
`assets/desk/`.

## Maker's later poses (2026-10-02)

Same model, photos and style (`maker-style.txt`); prompts in `../env-prompts/maker.json`, 1024x768.

| File | Pose | Seed |
| --- | --- | --- |
| `maker-sitside-seed9550.png` | sitting side-on, looking up at someone | 9550 |
| `maker-curl-seed9529.png` | lying down (the scene shuts her eyes when she is petted) | 9529 |
| `maker-knead-seed9536.png` | standing; the kneading frames lift one front paw, then the other | 9536 |

## The room, the skyline, the lamps and the props (2026-10-02)

All FLUX.2 klein 4B (Apache 2.0) on bigbaby through ComfyUI; prompts in `../env-prompts/`; reduced by
`../env_build.py` into `assets/desk/`.

| File | What | Picture given to the model | Prompt | Seed |
| --- | --- | --- | --- | --- |
| `room-wide-seed9701.png` | the room, 1440x640 (reduced at cell 4 to 360x160) | `guide-wide.png`, a flat layout drawn by `work/env/guides.py` | `room2.txt` + `style-bg.txt` | 9701 |
| `room-narrow-seed9802.png` | the phone layout's room, 960x640 | `guide-narrow.png` | same | 9802 |
| `sky-day-seed9101.png` | Midtown by day, 1536x864 (cell 10) | a crop of the photo *Midtown Manhattan Skyline 2025 195* (below) | `sky-day.txt` | 9101 |
| `sky-night-seed9603.png` | the same at night | the day picture above, and a crop of *Midtown Manhattan night pano* (below) | `sky-night.txt` | 9603 |
| `lamp-seed9401.png` | the anglepoise lamp, 1024x1024; the white one is the red one recoloured | a blank grey canvas | `lamp.txt` + `style-sprite.txt` | 9401 |
| `prop-*.png` | shaker bottle, mug, papers, vase of tulips, succulent, 768x768 | a blank grey canvas | `props.json` + `style-sprite.txt` | in the names |

The night lights were then finished in code after the real skyline at night (`env_build.skyline`): more windows lit,
the Empire State Building's floodlit top and mast, the Chrysler Building's crown chevrons; the scene blinks the red
aircraft lights. 21 columns were taken out of the middle of the UN Secretariat's plain glass face so the Empire State
and Chrysler buildings share the window.

### Photographs used as references for the skyline (adapted: redrawn as pixel art, cropped, recoloured)

- *Midtown Manhattan Skyline 2025 195* by Kidfly182, CC BY 4.0, https://commons.wikimedia.org/wiki/File:Midtown_Manhattan_Skyline_2025_195.jpg
  (licence: https://creativecommons.org/licenses/by/4.0/). Building shapes and positions.
- *Midtown Manhattan night pano* by palendromist (https://www.flickr.com/photos/cygbin/), CC BY 2.0,
  https://commons.wikimedia.org/wiki/File:Midtown_Manhattan_night_pano.jpg (licence: https://creativecommons.org/licenses/by/2.0/). Night lighting.
- Looked at, not given to the model: *NewYork-Skyline-night-May-2007* by Acediscovery (CC BY 4.0) and other Wikimedia
  Commons photos of Midtown, for how the Empire State and Chrysler tops are lit.

The photographs themselves are not in this repo.

**Not used, on purpose:** Qwen-Image 2.1, which is also on that machine. Its licence (Qwen Research License) allows
research and evaluation only, so it must not produce artwork for the company's site.
