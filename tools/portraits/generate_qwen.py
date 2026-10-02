#!/usr/bin/env python3
"""
Nutrimatic portrait toolkit - generate_qwen.py
Version 1.0.0

Created: 2026-10-02 - Photo -> GBA-style pixel portrait with Qwen-Image-Edit (v1.0.0)
  - An instruction-following edit model: give it the photo and tell it what to draw. Identity holds far better
    than SDXL image-to-image, with no face adapter. Optional second reference image for the style (the 2509 /
    "plus" models take several inputs): e.g. a GBA-style portrait made with Z-Image Turbo from text.
  - Writes N candidates and a contact sheet, like generate.py. Then run pixelize.py on the picks.

Usage:
  python generate_qwen.py --photo cole.jpg --prompt-file prompts/cole-edit.txt --out out/cole-qwen --n 8
  python generate_qwen.py --photo cole.jpg --style-ref refs/gba-style.png --prompt-file prompts/cole-edit.txt --out out/cole-qwen --model Qwen/Qwen-Image-Edit-2509
VRAM: the model is ~20B parameters. bf16 needs ~40 GB; with --offload it runs on a 24 GB card (slowly).
      ComfyUI's FP8 build of the same weights fits 24 GB comfortably if you'd rather use that.
"""
import argparse, os, sys, math, json, time

def parse():
    ap = argparse.ArgumentParser()
    ap.add_argument("--photo", required=True); ap.add_argument("--style-ref", default=None, help="second reference image for the style (multi-image edit models)")
    ap.add_argument("--prompt", default=None); ap.add_argument("--prompt-file", default=None)
    ap.add_argument("--negative", default="photo, photographic, realistic skin, blurry, soft gradients, text, watermark")
    ap.add_argument("--model", default="Qwen/Qwen-Image-Edit", help="Qwen/Qwen-Image-Edit, Qwen/Qwen-Image-Edit-2509, or a newer edit checkpoint you have locally")
    ap.add_argument("--out", required=True); ap.add_argument("--n", type=int, default=6); ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--steps", type=int, default=40); ap.add_argument("--cfg", type=float, default=4.0, help="true_cfg_scale")
    ap.add_argument("--size", type=int, default=1024); ap.add_argument("--offload", action="store_true", help="CPU offload for 24 GB cards")
    ap.add_argument("--dry-run", action="store_true")
    return ap.parse_args()

def main():
    a = parse()
    prompt = a.prompt or (open(a.prompt_file).read().strip() if a.prompt_file else None)
    if not prompt: sys.exit("give --prompt or --prompt-file")
    print(json.dumps(dict(model=a.model, size=a.size, steps=a.steps, cfg=a.cfg, n=a.n, seed=a.seed, style_ref=a.style_ref, out=a.out, prompt=prompt), indent=2))
    if a.dry_run: return
    import torch, diffusers
    from PIL import Image
    Pipe = None
    for name in ("QwenImageEditPlusPipeline", "QwenImageEditPipeline"):      # multi-image class first if this diffusers has it
        if hasattr(diffusers, name) and (a.style_ref or name == "QwenImageEditPipeline" or "2509" in a.model or "2.1" in a.model): Pipe = getattr(diffusers, name); break
    if Pipe is None: sys.exit("this diffusers has no Qwen-Image-Edit pipeline; pip install -U diffusers")
    dtype = torch.bfloat16 if torch.cuda.is_available() else torch.float32
    pipe = Pipe.from_pretrained(a.model, torch_dtype=dtype)
    if a.offload: pipe.enable_model_cpu_offload()
    else: pipe.to("cuda" if torch.cuda.is_available() else "cpu")
    photo = Image.open(a.photo).convert("RGB")
    s = min(photo.size); photo = photo.crop(((photo.width - s) // 2, (photo.height - s) // 2, (photo.width + s) // 2, (photo.height + s) // 2)).resize((a.size, a.size), Image.LANCZOS)
    images = [photo] + ([Image.open(a.style_ref).convert("RGB").resize((a.size, a.size), Image.LANCZOS)] if a.style_ref else [])
    os.makedirs(a.out, exist_ok=True); outs = []
    for i in range(a.n):
        seed = a.seed + i; g = torch.Generator(device="cpu").manual_seed(seed); t0 = time.time()
        kw = dict(prompt=prompt, negative_prompt=a.negative, num_inference_steps=a.steps, true_cfg_scale=a.cfg, generator=g)
        kw["image"] = images if len(images) > 1 else images[0]
        im = pipe(**kw).images[0]
        p = os.path.join(a.out, "cand-%03d-seed%d.png" % (i, seed)); im.save(p); outs.append(im); print("wrote", p, "%.0fs" % (time.time() - t0))
    cols = min(4, len(outs)); rows = math.ceil(len(outs) / cols); th = 256
    sheet = Image.new("RGB", (cols * th, rows * th), (40, 40, 40))
    for i, im in enumerate(outs): sheet.paste(im.resize((th, th), Image.LANCZOS), ((i % cols) * th, (i // cols) * th))
    sheet.save(os.path.join(a.out, "contact-sheet.png")); print("contact sheet:", os.path.join(a.out, "contact-sheet.png"))

if __name__ == "__main__": main()
