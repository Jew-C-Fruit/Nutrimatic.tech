#!/usr/bin/env python3
"""
Nutrimatic portrait toolkit - pixelize.py
Version 1.0.0

Created: 2026-10-02 - Turn a picked candidate (or a photo) into a clean 16-colour sprite (v1.0.0)
  - Cuts the figure out (rembg), downsamples to the sprite size, boosts contrast, quantises to a small palette
    without dithering, removes lone pixels, draws the outline in the darkest colour, saves 1x and a zoomed preview.
  - Generated pixel art is usually drawn at 8x: use --block 8 to average each 8x8 block first (keeps edges crisp).

Usage:
  python pixelize.py cand-003-seed4.png --out cole --head 36 --colors 15 --block 8
  python pixelize.py photo.jpg --out cole --head 36 --colors 15          # from a photo: likeness test only
"""
import argparse, sys
from PIL import Image, ImageEnhance, ImageFilter

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("src"); ap.add_argument("--out", required=True)
    ap.add_argument("--head", type=int, default=36, help="target head width in sprite pixels (whole bust is about 1.8x that)")
    ap.add_argument("--colors", type=int, default=15); ap.add_argument("--block", type=int, default=1, help="average NxN blocks first (8 for pixel-art-xl output)")
    ap.add_argument("--no-cut", action="store_true", help="skip background removal (already transparent)")
    ap.add_argument("--contrast", type=float, default=1.2); ap.add_argument("--zoom", type=int, default=8)
    a = ap.parse_args()
    im = Image.open(a.src).convert("RGBA")
    if a.block > 1: im = im.resize((im.width // a.block, im.height // a.block), Image.BOX)
    if not a.no_cut:
        from rembg import remove, new_session
        im = remove(im, session=new_session("u2net_human_seg"))
    bbox = im.getbbox() or (0, 0, im.width, im.height); im = im.crop(bbox)
    target_w = int(a.head * 1.8); scale = target_w / im.width
    small = im.resize((target_w, max(1, int(im.height * scale))), Image.LANCZOS) if abs(scale - 1) > 0.02 else im
    alpha = small.getchannel("A").point(lambda v: 255 if v > 120 else 0)
    rgb = ImageEnhance.Contrast(small.convert("RGB")).enhance(a.contrast)
    q = rgb.quantize(colors=a.colors, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).filter(ImageFilter.ModeFilter(3))
    pal = q.getpalette()[:a.colors * 3]; darkest = min(range(a.colors), key=lambda i: sum(pal[i * 3:i * 3 + 3])); dark = tuple(pal[darkest * 3:darkest * 3 + 3]) + (255,)
    res = Image.new("RGBA", small.size, (0, 0, 0, 0)); res.paste(q.convert("RGB"), (0, 0), alpha)
    px, al, w, h = res.load(), alpha.load(), small.width, small.height
    for y in range(h):
        for x in range(w):
            if al[x, y] and any(0 <= x + dx < w and 0 <= y + dy < h and not al[x + dx, y + dy] for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))): px[x, y] = dark
    res.save(a.out + "-1x.png")
    bg = Image.new("RGBA", res.size, (236, 232, 224, 255)); bg.alpha_composite(res); bg.resize((res.width * a.zoom, res.height * a.zoom), Image.NEAREST).save(a.out + "-%dx.png" % a.zoom)
    print("wrote", a.out + "-1x.png", "and", a.out + "-%dx.png" % a.zoom, "size", res.size, "colours", a.colors)

if __name__ == "__main__": main()
