#!/usr/bin/env python3
"""
Nutrimatic portrait toolkit - generate.py
Version 1.0.0

Created: 2026-10-02 - Batch-generate GBA-style pixel portraits from a reference photo (v1.0.0)
  - Open weights only: SDXL base + nerijs/pixel-art-xl LoRA (+ any extra style LoRA you download, e.g. a
    GBA Fire Emblem portrait LoRA from Civitai), image-to-image from the photo, IP-Adapter "plus-face" for likeness.
  - Writes N candidates and a contact sheet. Pick the best, then run pixelize.py on the picks.

Usage (SDXL, ~10 GB VRAM):
  python generate.py --photo cole.jpg --prompt-file prompts/cole.txt --out out/cole --n 12 --seed 1
  python generate.py --photo cole.jpg --prompt-file prompts/cole.txt --out out/cole --style-lora ./loras/gba_portrait.safetensors --style-weight 0.7
Smaller GPU (~6 GB): add --sd15  (uses SD 1.5 at 512px; slightly worse but fine for picking a direction)
"""
import argparse, os, sys, math, json, time

def parse():
    ap = argparse.ArgumentParser()
    ap.add_argument("--photo", required=True, help="reference photo (head and shoulders, plain background works best)")
    ap.add_argument("--prompt", default=None); ap.add_argument("--prompt-file", default=None)
    ap.add_argument("--negative", default="photo, photograph, realistic, 3d render, blurry, soft, noisy, gradient, text, watermark, signature, extra fingers, deformed, cropped head")
    ap.add_argument("--out", required=True); ap.add_argument("--n", type=int, default=8); ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--strength", type=float, default=0.62, help="img2img strength: lower keeps more of the photo (0.45-0.75)")
    ap.add_argument("--face", type=float, default=0.55, help="IP-Adapter face scale (0 = off)")
    ap.add_argument("--guidance", type=float, default=6.5); ap.add_argument("--steps", type=int, default=30)
    ap.add_argument("--pixel-weight", type=float, default=0.9, help="pixel-art-xl LoRA weight")
    ap.add_argument("--style-lora", default=None, help="path or HF id of an extra style LoRA (safetensors)")
    ap.add_argument("--style-weight", type=float, default=0.7)
    ap.add_argument("--sd15", action="store_true", help="use Stable Diffusion 1.5 instead of SDXL")
    ap.add_argument("--size", type=int, default=None, help="generation size (default 1024 SDXL / 512 SD1.5)")
    ap.add_argument("--dry-run", action="store_true", help="print the plan, load nothing")
    return ap.parse_args()

def main():
    a = parse()
    prompt = a.prompt or (open(a.prompt_file).read().strip() if a.prompt_file else None)
    if not prompt: sys.exit("give --prompt or --prompt-file")
    size = a.size or (512 if a.sd15 else 1024)
    plan = dict(model="SD 1.5" if a.sd15 else "SDXL base 1.0", size=size, lora="nerijs/pixel-art-xl" if not a.sd15 else "(none bundled for SD1.5: pass --style-lora)",
                style_lora=a.style_lora, strength=a.strength, face=a.face, n=a.n, seed=a.seed, out=a.out, prompt=prompt)
    print(json.dumps(plan, indent=2))
    if a.dry_run: return
    import torch
    from PIL import Image
    from diffusers import StableDiffusionXLImg2ImgPipeline, StableDiffusionImg2ImgPipeline
    device = "cuda" if torch.cuda.is_available() else ("mps" if getattr(torch.backends, "mps", None) and torch.backends.mps.is_available() else "cpu")
    dtype = torch.float16 if device == "cuda" else torch.float32
    photo = Image.open(a.photo).convert("RGB")
    # square crop around the centre, then resize to the working size
    s = min(photo.size); photo = photo.crop(((photo.width - s) // 2, (photo.height - s) // 2, (photo.width + s) // 2, (photo.height + s) // 2)).resize((size, size), Image.LANCZOS)
    if a.sd15:
        pipe = StableDiffusionImg2ImgPipeline.from_pretrained("stable-diffusion-v1-5/stable-diffusion-v1-5", torch_dtype=dtype, safety_checker=None)
        if a.face > 0: pipe.load_ip_adapter("h94/IP-Adapter", subfolder="models", weight_name="ip-adapter-plus-face_sd15.bin")
    else:
        pipe = StableDiffusionXLImg2ImgPipeline.from_pretrained("stabilityai/stable-diffusion-xl-base-1.0", torch_dtype=dtype, variant="fp16" if dtype == torch.float16 else None, use_safetensors=True)
        pipe.load_lora_weights("nerijs/pixel-art-xl", weight_name="pixel-art-xl.safetensors", adapter_name="pixel")
        adapters, weights = ["pixel"], [a.pixel_weight]
        if a.style_lora:
            folder, name = (os.path.dirname(a.style_lora) or ".", os.path.basename(a.style_lora)) if a.style_lora.endswith(".safetensors") else (a.style_lora, None)
            pipe.load_lora_weights(folder, weight_name=name, adapter_name="style"); adapters.append("style"); weights.append(a.style_weight)
        pipe.set_adapters(adapters, adapter_weights=weights)
        if a.face > 0: pipe.load_ip_adapter("h94/IP-Adapter", subfolder="sdxl_models", weight_name="ip-adapter-plus-face_sdxl_vit-h.safetensors", image_encoder_folder="models/image_encoder")
    if a.face > 0: pipe.set_ip_adapter_scale(a.face)
    pipe.to(device)
    if device == "cuda": pipe.enable_vae_slicing()
    os.makedirs(a.out, exist_ok=True); outs = []
    for i in range(a.n):
        seed = a.seed + i; g = torch.Generator(device="cpu").manual_seed(seed)
        kw = dict(prompt=prompt, negative_prompt=a.negative, image=photo, strength=a.strength, guidance_scale=a.guidance, num_inference_steps=a.steps, generator=g)
        if a.face > 0: kw["ip_adapter_image"] = photo
        t0 = time.time(); im = pipe(**kw).images[0]
        p = os.path.join(a.out, "cand-%03d-seed%d.png" % (i, seed)); im.save(p); outs.append(im); print("wrote", p, "%.0fs" % (time.time() - t0))
    # contact sheet
    cols = min(4, len(outs)); rows = math.ceil(len(outs) / cols); th = 256
    sheet = Image.new("RGB", (cols * th, rows * th), (40, 40, 40))
    for i, im in enumerate(outs): sheet.paste(im.resize((th, th), Image.LANCZOS), ((i % cols) * th, (i // cols) * th))
    sheet.save(os.path.join(a.out, "contact-sheet.png")); print("contact sheet:", os.path.join(a.out, "contact-sheet.png"))

if __name__ == "__main__": main()
