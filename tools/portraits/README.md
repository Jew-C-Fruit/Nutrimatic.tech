# Portrait toolkit: pixel portraits from photos

Version 1.2.0 · Created 2026-10-02 · Modified 2026-10-02 (first real run: the ComfyUI route is the one in use; pixelize v2)

This is how the figures in the desk scene were made: a generative model redraws each person from photos as a
pixel-art portrait, and `pixelize.py` reduces the pick to a true sprite at the scene's resolution. The hand finishing
(faces, layers, arms) and the export to the site happen in `tools/desk/`.

## 1. What was used

| Step | Tool | Notes |
| --- | --- | --- |
| Generate | `generate_comfy.py --model klein` | FLUX.2 klein 4B through ComfyUI on bigbaby (RTX 3090), driven from the Pi. About 8 s per picture. |
| Reduce | `pixelize.py --cell 12` | 1024x1280 picture to a figure about 75x97 px with a 36 px head |
| Finish | `tools/desk/` | face frames, torso and head layers, arms off; then `export_js.py` writes `js/desk-sprites.js` |

Nothing needs a GPU or torch on the machine that runs these scripts. `generate_comfy.py` only talks to the ComfyUI
server; `pixelize.py` needs numpy, scipy and pillow.

## 2. Models and licences

The site is commercial, so the model's licence has to allow that.

| Model | Licence | Use |
| --- | --- | --- |
| **FLUX.2 klein 4B** (Black Forest Labs), 4-step distilled | Apache 2.0 | **Used.** Edits from one to three reference images; best likeness and the most flattering of what was tried. |
| **Qwen-Image-Edit 2511** (Alibaba), with the lightx2v Lightning LoRAs | Apache 2.0 | Installed and wired up (`--model qwenedit`). More regular pixels, weaker likeness on these photos. |
| **Z-Image Turbo** | Apache 2.0 | `--model zimage`, text only. Not needed in the end. |
| Qwen-Image 2.1 | Qwen Research License: research and evaluation only | **Do not use for site art.** It is on the same machine, which is why this note exists. |

The model files come from `get_ai_models.ps1 -Only klein,qwenedit` on bigbaby (about 37 GB, hashes checked).

## 3. Generate

The prompt is in two files: the person (`prompts/cole-edit.txt`, `prompts/ilinca-edit.txt`) and the style
(`prompts/style.txt`). Reference photos are private and stay out of this repo.

```bash
cd tools/portraits
export COMFYUI_URL=http://<gpu machine>:8188        # and optionally COMFYUI_WAKE=<a Wake-on-LAN script>
python3 generate_comfy.py --model klein --photo three-quarter.png --ref front.png --ref headshot.jpg \
  --prompt-file prompts/cole-edit.txt --style-file prompts/style.txt --size 1024x1280 --out out/cole --n 12 --seed 101
python3 generate_comfy.py --model klein --photo studio.jpg \
  --prompt-file prompts/ilinca-edit.txt --style-file prompts/style.txt --size 1024x1280 --out out/ilinca --n 12 --seed 201
```

Each run writes the candidates, a `contact-sheet.png` and `run.json` (every setting, for reproducing a pick).

What mattered in practice:

- **Give it a photo in the pose you want.** A three-quarter photo as image 1 gave three-quarter portraits; a frontal
  headshot alone drifted.
- **Several references help the likeness**: klein takes up to three; put the pose first.
- **Say what to keep**, feature by feature (hair, brows, glasses, build, clothes), then the style. "Half-body from the
  hips up" gives enough torso for a figure seated behind a desk.
- **A flat light grey background** makes the cut-out trivial (yellow for the grey cat).
- **To combine candidates**, pass them as the references and say which part comes from which
  (`prompts/cole-merge.txt`: face from one, hair and body from another, skin from a third).
- **To change bearing or expression**, edit the pick itself (`prompts/ilinca-confident.txt`). The same works for
  expression studies; no second person's photos are needed.

Picking: it looks like the person; a three-quarter view with the whole head in frame; clear shapes; a plain torso
(the arms are replaced later).

## 4. Reduce to a sprite

```bash
python3 pixelize.py out/cole/cand-008-seed109.png --out cole --cell 12
```

`--cell` is source pixels per sprite pixel. The generated pictures look like pixel art but are not on a grid, so this
is a real resampling, in two layers: the flat areas by majority vote per sprite pixel, and the thin dark strokes
(outlines, glasses frames, eyelids, mouth) found separately and thinned to one pixel so they neither vanish nor turn
into blobs. It writes `cole-1x.png` (the sprite), `cole-8x.png` (to look at) and `cole.json` (palette and grid).

Faces still need finishing by hand at this size: an eye is three pixels. That is `tools/desk/characters.py`.

## 5. Other routes, kept but not run on real hardware

- `generate_qwen.py`: Qwen-Image-Edit through diffusers, for a machine without ComfyUI. Needs about 58 GB of weights.
- `generate.py`: SDXL + pixel-art-xl LoRA + IP-Adapter plus-face. The fallback from the first plan.
