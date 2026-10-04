# Where the pictures in this folder came from

Version 1.10.0 · Created 2026-10-02 · Modified 2026-10-03 (walk cycle; petting with a cat; audit references; the walk redone; looking down; petting at the desk's edge; portraits kept out of the repo; the ceiling light)

## Credits to show when the scene goes live (not on the page yet, by Cole's choice)

- Skyline after *Midtown Manhattan Skyline 2025 195* by Kidfly182 (CC BY 4.0) and *Midtown Manhattan night pano* by
  palendromist (CC BY 2.0), Wikimedia Commons.
- *Victory Boogie Woogie*, Piet Mondrian (1942-44), after a photograph by Sailko (CC BY 3.0), Wikimedia Commons.
- Everything else was generated with FLUX.2 klein 4B (Apache 2.0) and needs no credit.

Looked at only, nothing copied, for the audit of hands and objects (2026-10-03): *Typing on a laptop* (Simon Hattinga
Verschure, CC0), *Laptop Typing* (Kristin Hardwick, CC0), *Clem Onojeghuo 2016-12-18* (CC0), *Addiction mug*
(simon.wright, CC BY 2.0), a woman drinking from a bottle (pansy Gronski, CC0), *P20231120AS-1277* (The White House,
public domain), *Furiously Factoring* (CarbonNYC, CC BY 2.0), *Writing Drawing* (Green Chameleon, CC0), *8 Śląski
Festiwal Nauki* (Krzysztof Popławski, CC BY-SA 4.0), *Girl with chin resting on hand* (faceseveryday, CC BY 2.0),
*Ajawajaa* (Yusmery94, CC BY-SA 4.0), *A Warm Welcome from Enniburr* (U.S. Army, public domain), *Katze in Kroatien*
(ElisabethRied, CC0), *A Kitten Relaxing While Being Petted* (Xoqoni Said, CC0). Links in the work folder's
`audit/refs/refs.json`.

Looked at only, nothing copied: cute pixel cats on OpenGameArt for the big-eye look (*Cute cat (32x32)* by limafresh,
CC0; *Cats - Pixel Art* by peony, CC BY 4.0; *Pixel art cute cat* by snoopy11).

## The pictures

Everything here was generated on bigbaby (RTX 3090) with **FLUX.2 klein 4B** (Black Forest Labs, Apache 2.0, 4-step
distilled) through ComfyUI, driven by `tools/portraits/generate_comfy.py`. 1024x1280 for the people, 1024x768 for
Maker. The reference photos are private and are not in this repo. Neither are the full-size generated portraits of
Cole and Ilinca (`cole-merged-seed301.png`, `ilinca-confident-seed407.png` and the two looking-down pictures below), by
Cole's call (2026-10-04, "no portraits in repo"): they are kept on bagel in `~/claude/nutrimatic/work/portraits-src/`;
only the reduced sprites made from them (`../sprites/`) are here.

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

## Later poses (2026-10-03)

- `maker-yawn-back-seed9612.png`: Maker yawning with her head thrown back (her photos; the prompt in `run_maker2.sh`
  of the work folder, same style as her other poses).
- The lean-back stretches (`sprites/poses/*/stretch.png`, `stretchback.png`) come from prompts that let the model
  change the head too (`pose-prompts/pose-prefix-*-free.txt`).

- `maker-walkcycle-seed9703.png`: a four-frame walk cycle for Maker in one picture (her photos; prompt in
  `run_walk.sh` of the work folder), cut into frames by `maker_build.walk_frames`.
- The petting poses (`sprites/poses/*/petcat.png`) were generated with a grey cat under the hand; `poses.py` erases
  that cat and the scene puts Maker in its place.
- The front-edge petting poses (`sprites/poses/*/petedge.png`, 2026-10-04, Cole's note 12): FLUX.2 klein 4B on each pose
  stage with Maker's own lying sprite pasted where the scene now lays her (the desk's front edge), asked to rest a hand
  on her back (work folder `petedge/`); `poses.py` clears her outline but the hand, and the scene draws her there.

## The walk (2026-10-03, Cole's notes 6 and 9)

- `walk_rig.py` (2.0) draws the legs of Maker's walk on her own standing body (the `stand` sprite, from
  `maker-knead-seed9536.png`), ten frames a cycle: a cat's lateral-sequence walk, each paw down 70% of the cycle and
  planted while it is, following `docs/animal-walk-cycles.md`. No new generated pictures. The doc's reference pictures
  and their credits are in `docs/walk-refs/` and at the end of the doc: Eadweard Muybridge, *Animal Locomotion* (1887),
  plates 716 and 729, public domain (National Gallery of Art scans, CC0). Looked at, not copied.
- The first rig (1.0, Cole: "completely wrong") and its generated body `maker-walkbody-seed9815.png` are gone.

## Looking down (2026-10-03, Cole's note 10)

- `cole-down-seed5108.png` (kept outside the repo): FLUX.2 klein 4B on Cole's pose stage picture (the base portrait behind the flat blue desk),
  asked to change only his head: bowed toward the desk, his face turned as before, lids lowered, a faint smile.
  `characters.Cole.down_blank` uses its reduction (`sprites/cole-down-1x.png`) for the head's new shape and redraws
  the face in the base face's style.
- `ilinca-down-seed2003.png` (kept outside the repo): Qwen-Image-Edit 2511 (Apache 2.0) on Ilinca's base portrait, asked to have her look down
  at a desk just in front of her, everything else unchanged. Her outline stayed exactly; `characters.Ilinca.down_blank`
  takes its hairline (`sprites/ilinca-down-1x.png`) and moves her features as it did.
- Work folder `lookdown/` (run.sh to run4.sh): the other candidates, the reductions and the comparison sheets.

## The ceiling light (2026-10-04, Cole: "Give us a new ceiling light")

- `ceiling-seed9603.png`: FLUX.2 klein 4B, with `lamp-seed9401.png` (the anglepoise) as the style reference, asked for
  an industrial black dome pendant on a cord (work folder `ceiling/`); `env_build.pendant` reduces it to
  `assets/desk/pendant-on.png` and an unlit `pendant-off.png`.

## The painting where the poster was (2026-10-02)

- `room-wide-noposter-edit-seed9811.png`, `room-narrow-noposter-edit-seed9821.png`: FLUX.2 klein 4B edits of a crop of
  each room around the poster (prompt `env-prompts/unposter.txt`), blended back into the rooms as
  `room-*-noposter.png`, which `env_build.py` reduces.
- *Victory Boogie Woogie* (Piet Mondrian, 1942-44, Kunstmuseum Den Haag), reduced by `env_build.painting` from the
  photograph *Piet mondrian, victory boogie woogie, 1942-44, 01* by Sailko, CC BY 3.0,
  https://commons.wikimedia.org/wiki/File:Piet_mondrian,_victory_boogie_woogie,_1942-44,_01.jpg
  (licence: https://creativecommons.org/licenses/by/3.0/). Mondrian died in 1944; Wikimedia Commons hosts the painting
  as public domain. The photograph is not in this repo.

**Not used, on purpose:** Qwen-Image 2.1, which is also on that machine. Its licence (Qwen Research License) allows
research and evaluation only, so it must not produce artwork for the company's site.
