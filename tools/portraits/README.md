# Portrait toolkit: GBA-style pixel portraits from your photos

Version 1.0.0 · Created 2026-10-02

Runs on bagel or bigbaby. Open weights only. The model produces the **head and torso**; everything that moves
(eyes, mouth, brows, arms, props) is built afterwards as layers in the same palette, so the result can be animated
in the desk scene. One good base portrait each is the whole ask of this step.

## 1. Hardware and install

- NVIDIA GPU with 10 GB or more for the SDXL route (the good one). 6 GB works with `--sd15`.
- Python 3.10+. From the repo root:

```bash
cd tools/portraits
python -m venv .venv && source .venv/bin/activate
pip install torch --index-url https://download.pytorch.org/whl/cu124    # pick the line for your CUDA from pytorch.org
pip install -r requirements.txt
```

Models download themselves from Hugging Face on first run (about 7 GB for SDXL + the face adapter). Nothing needs an account.

## 2. Models used

| Piece | What | Where it comes from |
| --- | --- | --- |
| Base | Stable Diffusion XL 1.0 | `stabilityai/stable-diffusion-xl-base-1.0` (auto) |
| Pixel art | `pixel-art-xl` LoRA by nerijs: clean 8x pixel art, open weights | `nerijs/pixel-art-xl` (auto) |
| Likeness | IP-Adapter "plus-face" for SDXL: steers the face toward the photo | `h94/IP-Adapter` (auto) |
| Optional style | A GBA Fire Emblem portrait LoRA. Several exist on Civitai (search "Fire Emblem GBA portrait" or "FE8 mug"); download the `.safetensors` by hand (Civitai wants a login) into `loras/` and pass `--style-lora loras/<file>.safetensors` | manual |

The style LoRAs are trained on Nintendo's portraits. Using one to steer a style is the normal thing people do with them;
we are not copying any actual game art onto the site, which is the line I'd keep.

## 3. Generate

Reference photos: a straight-on or slightly turned head-and-shoulders shot, even light, plain background if you have one.
The two in `assets/team/` work; a plainer one of Cole would help.

```bash
python generate.py --photo ../../assets/team/cole-maisonpierre.jpg --prompt-file prompts/cole.txt --out out/cole --n 12 --seed 1
python generate.py --photo ../../assets/team/ilinca-iorga.jpg   --prompt-file prompts/ilinca.txt --out out/ilinca --n 12 --seed 1
```

Each run writes the candidates and a `contact-sheet.png`. Then adjust and run again; the dials that matter:

- `--strength` (default 0.62): lower keeps more of the photo's structure, higher gives the style more freedom. Try 0.5 and 0.72.
- `--face` (default 0.55): how hard the face adapter pulls toward the photo. 0.4 to 0.7. Too high and it drifts back to a photo.
- `--style-lora ... --style-weight 0.7`: once you have a GBA LoRA; drop `--pixel-weight` to 0.6 when both are on.
- `--seed`: a different batch. Twelve candidates a run, a few runs, and pick with the checklist below.

Picking criteria, in order: it looks like the person; the head is a clean three-quarter or front view with the whole
head in frame; flat shading with few colours; hair reads as locks; a plain torso (arms down or out of frame are
fine, I replace them); nothing important hidden behind text or a border.

## 4. Clean up to a true sprite

```bash
python pixelize.py out/cole/cand-007-seed8.png --out cole --head 36 --colors 15 --block 8
```

`--block 8` averages the 8x8 blocks the pixel-art LoRA draws in, so edges stay crisp; `--head 36` sets the head width
in sprite pixels (the scene wants 32 to 40); `--colors 15` keeps the GBA budget (15 plus transparency).
It writes `cole-1x.png` (the sprite) and `cole-8x.png` (to look at). Same for Ilinca.

## 5. Send back

The `*-1x.png` for each of you, plus the full-size candidate you picked (it carries detail the cleanup can consult).
From there I cut the head and torso into layers, draw the eye, mouth and brow frames in the same palette, build the
seated bodies with arms as separate pieces, and put them into the desk scene with the behaviours already written.
