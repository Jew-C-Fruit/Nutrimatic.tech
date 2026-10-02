# Where the pictures in this folder came from

Version 1.0.0 · Created 2026-10-02

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

Each picture was reduced with `tools/portraits/pixelize.py --cell 12` (people) or to a target size (Maker: 52 px long
walking, 38 px tall sitting, 50 px long lying) to give the sprites in `../sprites/`.

**Not used, on purpose:** Qwen-Image 2.1, which is also on that machine. Its licence (Qwen Research License) allows
research and evaluation only, so it must not produce artwork for the company's site.
