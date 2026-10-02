#!/usr/bin/env python3
"""
Nutrimatic portrait toolkit - generate_comfy.py
Version 1.0.2

Created: 2026-10-02 - Photo -> portrait candidates through a ComfyUI server (bigbaby), driven from another machine (v1.0.0)
Modified: 2026-10-02 - --style-file: the person and the style are separate prompt files (v1.0.1)
Modified: 2026-10-02 - No machine addresses in the script: the server and the wake script come from the environment (v1.0.2)
  - The route that matches the GPU machine as it is: ComfyUI is already there, so nothing needs a Python environment
    with torch. This script only builds the workflow, uploads the photo, queues it and downloads the results.
  - Models, all Apache 2.0 so the results may be used on the company site:
      klein     FLUX.2 klein 4B, 4-step distilled. Edits with one or more reference images. Seconds per image.
      qwenedit  Qwen-Image-Edit 2511 (20B). Slower, strongest at keeping a person's identity through a style change.
                --lightning 4 or 8 uses the lightx2v step-distilled LoRA; --lightning 0 runs the full 40 steps at CFG 4.
      zimage    Z-Image Turbo, text only: for a style reference image, not for likeness.
    Qwen-Image 2.1 is deliberately not offered: its licence (Qwen Research License) is research and evaluation only.
  - The graphs follow ComfyUI's own templates (image_flux2_klein_image_edit_4b_distilled, image_qwen_image_edit_2511_int8,
    image_z_image_turbo). Model files come from get_ai_models.ps1 -Only klein,qwenedit on bigbaby.
  - Writes cand-NNN-seedS.png, contact-sheet.png and run.json (every setting, for reproducing a pick).

Usage:
  python generate_comfy.py --model klein --photo cole.jpg --prompt-file prompts/cole-edit.txt --style-file prompts/style.txt --size 1024x1280 --out out/cole --n 12 --seed 101
  python generate_comfy.py --model qwenedit --photo photo.jpg --ref style.png --prompt "Redraw the person in image 1 in the style of image 2" --out out/x
  python generate_comfy.py --model zimage --prompt-file prompts/style-ref-zimage.txt --out out/style --n 4
Server: --server, else $COMFYUI_URL, else http://127.0.0.1:8188. If it does not answer and $COMFYUI_WAKE names a script
(Wake-on-LAN for the GPU machine), that is run first.
Needs Pillow for the contact sheet; everything else is the standard library.
"""
import argparse, json, math, os, subprocess, sys, time, urllib.error, urllib.parse, urllib.request, uuid

DEFAULT_SERVER = "http://127.0.0.1:8188"
WAKE_SCRIPT = os.environ.get("COMFYUI_WAKE", "")          # optional: a script that wakes the GPU machine (Wake-on-LAN)
KLEIN = dict(unet="flux-2-klein-4b.safetensors", clip="qwen_3_4b.safetensors", vae="flux2-vae.safetensors")
QWEN_EDIT = dict(unet="qwen_image_edit_2511_int8_convrot.safetensors", clip="qwen_2.5_vl_7b_fp8_scaled.safetensors", vae="qwen_image_vae.safetensors",
                 lightning={4: "Qwen-Image-Edit-2511-Lightning-4steps-V1.0-bf16.safetensors", 8: "Qwen-Image-Edit-2511-Lightning-8steps-V1.0-bf16.safetensors"})
ZIMAGE = dict(unet="z_image_turbo_bf16.safetensors", clip="qwen_3_4b.safetensors", vae="ae.safetensors")


class Comfy:
    def __init__(self, server): self.server = server.rstrip("/")

    def request(self, path, data=None, headers=None, timeout=30):
        with urllib.request.urlopen(urllib.request.Request(self.server + path, data=data, headers=headers or {}), timeout=timeout) as r: return r.read()

    def reachable(self):
        try: self.request("/system_stats", timeout=5); return True
        except (urllib.error.URLError, OSError): return False

    def upload(self, path):
        boundary, name = uuid.uuid4().hex, os.path.basename(path)
        body = b"".join([("--%s\r\nContent-Disposition: form-data; name=\"overwrite\"\r\n\r\ntrue\r\n" % boundary).encode(),
                         ("--%s\r\nContent-Disposition: form-data; name=\"image\"; filename=\"%s\"\r\nContent-Type: application/octet-stream\r\n\r\n" % (boundary, name)).encode(),
                         open(path, "rb").read(), ("\r\n--%s--\r\n" % boundary).encode()])
        reply = json.loads(self.request("/upload/image", body, {"Content-Type": "multipart/form-data; boundary=" + boundary}, timeout=120))
        return (reply["subfolder"] + "/" + reply["name"]) if reply.get("subfolder") else reply["name"]

    def run(self, workflow, timeout):
        try: pid = json.loads(self.request("/prompt", json.dumps({"prompt": workflow, "client_id": uuid.uuid4().hex}).encode(), {"Content-Type": "application/json"}))["prompt_id"]
        except urllib.error.HTTPError as e: sys.exit("ComfyUI rejected the workflow: " + e.read().decode(errors="replace")[:3000])
        t0 = time.time()
        while True:
            time.sleep(1.5)
            hist = json.loads(self.request("/history/" + pid)).get(pid); status = (hist or {}).get("status", {})
            if status.get("status_str") == "error":
                errs = [m[1] for m in status.get("messages", []) if m[0] == "execution_error"]
                sys.exit("generation failed: " + ("; ".join("%s: %s" % (e.get("node_type"), e.get("exception_message", "").strip()) for e in errs) or str(status)))
            if hist and status.get("completed"): return hist["outputs"], time.time() - t0
            if time.time() - t0 > timeout: sys.exit("gave up after %d s (prompt %s may still finish in ComfyUI)" % (timeout, pid))

    def download(self, item, dest):
        q = urllib.parse.urlencode({"filename": item["filename"], "subfolder": item.get("subfolder", ""), "type": item.get("type", "output")})
        open(dest, "wb").write(self.request("/view?" + q, timeout=300))


def klein_workflow(prompt, images, seed, steps, cfg, size, megapixels):
    """FLUX.2 klein 4B distilled. Every reference image is VAE-encoded and chained onto both conditionings as a
    ReferenceLatent. The result has the first image's size (scaled to `megapixels`) unless size=(w, h) is given."""
    wf = {"unet": {"class_type": "UNETLoader", "inputs": {"unet_name": KLEIN["unet"], "weight_dtype": "default"}},
          "clip": {"class_type": "CLIPLoader", "inputs": {"clip_name": KLEIN["clip"], "type": "flux2", "device": "default"}},
          "vae": {"class_type": "VAELoader", "inputs": {"vae_name": KLEIN["vae"]}},
          "pos0": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["clip", 0], "text": prompt}},
          "neg0": {"class_type": "ConditioningZeroOut", "inputs": {"conditioning": ["pos0", 0]}}}
    pos, neg = ["pos0", 0], ["neg0", 0]
    for n, name in enumerate(images, 1):
        wf["load%d" % n] = {"class_type": "LoadImage", "inputs": {"image": name}}
        if megapixels > 0: wf["scale%d" % n] = {"class_type": "ImageScaleToTotalPixels", "inputs": {"image": ["load%d" % n, 0], "upscale_method": "lanczos", "megapixels": megapixels, "resolution_steps": 16}}
        else: wf["scale%d" % n] = {"class_type": "ImageScale", "inputs": {"image": ["load%d" % n, 0], "upscale_method": "nearest-exact", "width": 0, "height": 0, "crop": "disabled"}}   # as it is
        wf["enc%d" % n] = {"class_type": "VAEEncode", "inputs": {"pixels": ["scale%d" % n, 0], "vae": ["vae", 0]}}
        wf["pos%d" % n] = {"class_type": "ReferenceLatent", "inputs": {"conditioning": pos, "latent": ["enc%d" % n, 0]}}
        wf["neg%d" % n] = {"class_type": "ReferenceLatent", "inputs": {"conditioning": neg, "latent": ["enc%d" % n, 0]}}
        pos, neg = ["pos%d" % n, 0], ["neg%d" % n, 0]
    if size or not images: w, h = size or (1024, 1024); width, height = w, h
    else:
        wf["size"] = {"class_type": "GetImageSize", "inputs": {"image": ["scale1", 0]}}; width, height = ["size", 0], ["size", 1]
    wf.update({
        "latent": {"class_type": "EmptyFlux2LatentImage", "inputs": {"width": width, "height": height, "batch_size": 1}},
        "sigmas": {"class_type": "Flux2Scheduler", "inputs": {"steps": steps, "width": width, "height": height}},
        "guider": {"class_type": "CFGGuider", "inputs": {"model": ["unet", 0], "positive": pos, "negative": neg, "cfg": cfg}},
        "noise": {"class_type": "RandomNoise", "inputs": {"noise_seed": seed}},
        "sampler": {"class_type": "KSamplerSelect", "inputs": {"sampler_name": "euler"}},
        "sample": {"class_type": "SamplerCustomAdvanced", "inputs": {"noise": ["noise", 0], "guider": ["guider", 0], "sampler": ["sampler", 0], "sigmas": ["sigmas", 0], "latent_image": ["latent", 0]}},
        "decode": {"class_type": "VAEDecode", "inputs": {"samples": ["sample", 0], "vae": ["vae", 0]}},
        "save": {"class_type": "SaveImage", "inputs": {"images": ["decode", 0], "filename_prefix": "nutrimatic_portraits/klein"}}})
    return wf


def qwen_edit_workflow(prompt, negative, images, seed, steps, cfg, lightning, size):
    """Qwen-Image-Edit 2511: the text encoder sees the pictures (up to three); the first one is also the start latent,
    so the result keeps its size unless size=(w, h) is given."""
    wf = {"unet": {"class_type": "UNETLoader", "inputs": {"unet_name": QWEN_EDIT["unet"], "weight_dtype": "default"}},
          "shift": {"class_type": "ModelSamplingAuraFlow", "inputs": {"model": ["unet", 0], "shift": 3.1}},
          "norm": {"class_type": "CFGNorm", "inputs": {"model": ["shift", 0], "strength": 1.0}},
          "clip": {"class_type": "CLIPLoader", "inputs": {"clip_name": QWEN_EDIT["clip"], "type": "qwen_image", "device": "default"}},
          "vae": {"class_type": "VAELoader", "inputs": {"vae_name": QWEN_EDIT["vae"]}}}
    model = ["norm", 0]
    if lightning:
        wf["lora"] = {"class_type": "LoraLoaderModelOnly", "inputs": {"model": model, "lora_name": QWEN_EDIT["lightning"][lightning], "strength_model": 1.0}}; model = ["lora", 0]
    enc_p = {"clip": ["clip", 0], "vae": ["vae", 0], "prompt": prompt}; enc_n = {"clip": ["clip", 0], "vae": ["vae", 0], "prompt": negative}
    for n, name in enumerate(images[:3], 1):
        wf["load%d" % n] = {"class_type": "LoadImage", "inputs": {"image": name}}
        wf["scale%d" % n] = {"class_type": "FluxKontextImageScale", "inputs": {"image": ["load%d" % n, 0]}}
        enc_p["image%d" % n] = ["scale%d" % n, 0]; enc_n["image%d" % n] = ["scale%d" % n, 0]
    if size: wf["latent"] = {"class_type": "EmptySD3LatentImage", "inputs": {"width": size[0], "height": size[1], "batch_size": 1}}
    else: wf["latent"] = {"class_type": "VAEEncode", "inputs": {"pixels": ["scale1", 0], "vae": ["vae", 0]}}
    wf.update({
        "pos": {"class_type": "TextEncodeQwenImageEditPlus", "inputs": enc_p}, "neg": {"class_type": "TextEncodeQwenImageEditPlus", "inputs": enc_n},
        "posm": {"class_type": "FluxKontextMultiReferenceLatentMethod", "inputs": {"conditioning": ["pos", 0], "reference_latents_method": "index_timestep_zero"}},
        "negm": {"class_type": "FluxKontextMultiReferenceLatentMethod", "inputs": {"conditioning": ["neg", 0], "reference_latents_method": "index_timestep_zero"}},
        "sample": {"class_type": "KSampler", "inputs": {"model": model, "seed": seed, "steps": steps, "cfg": cfg, "sampler_name": "euler", "scheduler": "simple",
                                                        "positive": ["posm", 0], "negative": ["negm", 0], "latent_image": ["latent", 0], "denoise": 1.0}},
        "decode": {"class_type": "VAEDecode", "inputs": {"samples": ["sample", 0], "vae": ["vae", 0]}},
        "save": {"class_type": "SaveImage", "inputs": {"images": ["decode", 0], "filename_prefix": "nutrimatic_portraits/qwenedit"}}})
    return wf


def zimage_workflow(prompt, seed, steps, size):
    w, h = size or (1024, 1024)
    return {"unet": {"class_type": "UNETLoader", "inputs": {"unet_name": ZIMAGE["unet"], "weight_dtype": "default"}},
            "clip": {"class_type": "CLIPLoader", "inputs": {"clip_name": ZIMAGE["clip"], "type": "lumina2", "device": "default"}},
            "vae": {"class_type": "VAELoader", "inputs": {"vae_name": ZIMAGE["vae"]}},
            "shift": {"class_type": "ModelSamplingAuraFlow", "inputs": {"model": ["unet", 0], "shift": 3}},
            "pos": {"class_type": "CLIPTextEncode", "inputs": {"text": prompt, "clip": ["clip", 0]}},
            "neg": {"class_type": "ConditioningZeroOut", "inputs": {"conditioning": ["pos", 0]}},
            "latent": {"class_type": "EmptySD3LatentImage", "inputs": {"width": w, "height": h, "batch_size": 1}},
            "sample": {"class_type": "KSampler", "inputs": {"model": ["shift", 0], "seed": seed, "steps": steps, "cfg": 1.0, "sampler_name": "res_multistep", "scheduler": "simple",
                                                            "positive": ["pos", 0], "negative": ["neg", 0], "latent_image": ["latent", 0], "denoise": 1.0}},
            "decode": {"class_type": "VAEDecode", "inputs": {"samples": ["sample", 0], "vae": ["vae", 0]}},
            "save": {"class_type": "SaveImage", "inputs": {"images": ["decode", 0], "filename_prefix": "nutrimatic_portraits/zimage"}}}


def parse():
    ap = argparse.ArgumentParser(description="Portrait candidates through ComfyUI (FLUX.2 klein 4B, Qwen-Image-Edit 2511, Z-Image Turbo)")
    ap.add_argument("--model", choices=["klein", "qwenedit", "zimage"], default="klein")
    ap.add_argument("--photo", help="the person (image 1)"); ap.add_argument("--ref", action="append", default=[], help="further reference images (image 2, 3): a style reference, a second photo")
    ap.add_argument("--prompt"); ap.add_argument("--prompt-file"); ap.add_argument("--style-file", help="text appended to the prompt (prompts/style.txt)")
    ap.add_argument("--negative", default="", help="qwenedit at CFG > 1 only")
    ap.add_argument("--out", required=True); ap.add_argument("--n", type=int, default=6); ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--steps", type=int); ap.add_argument("--cfg", type=float)
    ap.add_argument("--lightning", type=int, choices=[0, 4, 8], default=4, help="qwenedit: 4- or 8-step LoRA, or 0 for the full model (40 steps, CFG 4)")
    ap.add_argument("--size", help="WxH of the result (multiples of 16); default: the photo's shape at --megapixels")
    ap.add_argument("--megapixels", type=float, default=1.0, help="klein: size the reference images are scaled to; 0 = use them as they are (sides must be multiples of 16)")
    ap.add_argument("--server", default=os.environ.get("COMFYUI_URL", DEFAULT_SERVER)); ap.add_argument("--timeout", type=int, default=1800)
    ap.add_argument("--free", action="store_true", help="unload the models from the GPU afterwards"); ap.add_argument("--dry-run", action="store_true", help="print the first workflow and stop")
    return ap.parse_args()


def main():
    a = parse()
    prompt = a.prompt or (open(a.prompt_file).read().strip() if a.prompt_file else None)
    if not prompt: sys.exit("give --prompt or --prompt-file")
    if a.style_file: prompt += " " + open(a.style_file).read().strip()
    if a.model != "zimage" and not a.photo: sys.exit("--model %s edits a picture: give --photo" % a.model)
    size = tuple(int(v) for v in a.size.lower().split("x")) if a.size else None
    if a.model == "klein": steps, cfg = a.steps or 4, a.cfg or 1.0
    elif a.model == "qwenedit": steps, cfg = a.steps or (a.lightning or 40), a.cfg or (1.0 if a.lightning else 4.0)
    else: steps, cfg = a.steps or 8, 1.0
    comfy = Comfy(a.server)
    if a.dry_run: names = [os.path.basename(p) for p in ([a.photo] if a.photo else []) + a.ref]
    else:
        if not comfy.reachable() and WAKE_SCRIPT and os.path.exists(os.path.expanduser(WAKE_SCRIPT)):
            print("ComfyUI not answering; running the wake script", flush=True); subprocess.run([sys.executable, os.path.expanduser(WAKE_SCRIPT)], check=False)
            for _ in range(45):
                if comfy.reachable(): break
                time.sleep(2)
        if not comfy.reachable(): sys.exit("ComfyUI at %s is not answering" % a.server)
        names = [comfy.upload(p) for p in ([a.photo] if a.photo else []) + a.ref]

    def build(seed):
        if a.model == "klein": return klein_workflow(prompt, names, seed, steps, cfg, size, a.megapixels)
        if a.model == "qwenedit": return qwen_edit_workflow(prompt, a.negative, names, seed, steps, cfg, a.lightning, size)
        return zimage_workflow(prompt, seed, steps, size)

    if a.dry_run: print(json.dumps(build(a.seed), indent=1)); return
    os.makedirs(a.out, exist_ok=True); outs = []
    settings = dict(model=a.model, files=dict(klein=KLEIN, qwenedit=QWEN_EDIT, zimage=ZIMAGE)[a.model], photo=a.photo, refs=a.ref, prompt=prompt, negative=a.negative,
                    steps=steps, cfg=cfg, lightning=a.lightning if a.model == "qwenedit" else None, size=size, megapixels=a.megapixels, seeds=[], server=a.server)
    for i in range(a.n):
        seed = a.seed + i
        outputs, secs = comfy.run(build(seed), a.timeout)
        files = [it for node in outputs.values() for items in node.values() if isinstance(items, list) for it in items if isinstance(it, dict) and "filename" in it]
        if not files: sys.exit("finished but produced no file: " + json.dumps(outputs)[:500])
        dest = os.path.join(a.out, "cand-%03d-seed%d.png" % (i, seed)); comfy.download(files[0], dest); outs.append(dest); settings["seeds"].append(seed)
        print("wrote %s  %.0f s" % (dest, secs), flush=True)
    json.dump(settings, open(os.path.join(a.out, "run.json"), "w"), indent=1)
    if a.free: comfy.request("/free", json.dumps({"unload_models": True, "free_memory": True}).encode(), {"Content-Type": "application/json"})
    try: from PIL import Image
    except ImportError: print("no Pillow: skipping the contact sheet"); return
    ims = [Image.open(p).convert("RGB") for p in outs]; th = 384; cols = min(4, len(ims)); rows = math.ceil(len(ims) / cols)
    cell_h = max(round(th * im.height / im.width) for im in ims); sheet = Image.new("RGB", (cols * th, rows * cell_h), (40, 40, 40))
    for i, im in enumerate(ims): sheet.paste(im.resize((th, round(th * im.height / im.width)), Image.LANCZOS), ((i % cols) * th, (i // cols) * cell_h))
    sheet.save(os.path.join(a.out, "contact-sheet.png")); print("contact sheet:", os.path.join(a.out, "contact-sheet.png"))


if __name__ == "__main__": main()
