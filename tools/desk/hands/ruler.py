#!/usr/bin/env python3
"""
Nutrimatic desk scene - hands/ruler.py
Version 1.0.0

Created: 2026-10-06 - Ruler views for drawing hands: a pose (or any RGBA picture) enlarged with a pixel grid and the
  figure-sprite coordinates written along the edges, every 5th line darker (v1.0.0)

python3 ruler.py WHO POSE OUT.png [x0 y0 x1 y1] [zoom]      (coordinates in figure-sprite pixels; default the hands area)
"""
import os, sys
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))


def ruler(im, x0, y0, zoom=12, out=None):
    """im: RGBA picture whose top-left pixel is sprite (x0, y0); returns the enlarged picture with grid and labels"""
    W, H = im.size; m = 28
    big = im.convert('RGB').resize((W * zoom, H * zoom), Image.NEAREST)
    can = Image.new('RGB', (W * zoom + m, H * zoom + m), (255, 255, 255)); can.paste(big, (m, m)); d = ImageDraw.Draw(can)
    for i in range(W + 1):
        x = m + i * zoom; X = x0 + i
        d.line([(x, m), (x, m + H * zoom)], fill=(90, 90, 90) if X % 5 == 0 else (200, 200, 200), width=1)
        if X % 5 == 0 and i < W: d.text((x + 1, 2), str(X), fill=(0, 0, 0))
    for j in range(H + 1):
        y = m + j * zoom; Y = y0 + j
        d.line([(m, y), (m + W * zoom, y)], fill=(90, 90, 90) if Y % 5 == 0 else (200, 200, 200), width=1)
        if Y % 5 == 0 and j < H: d.text((1, y + 1), str(Y), fill=(0, 0, 0))
    if out: can.save(out)
    return can


def main():
    from hands import core
    who, pose, out = sys.argv[1:4]
    box = tuple(map(int, sys.argv[4:8])) if len(sys.argv) >= 8 else (-20, 30, 100, 100)
    zoom = int(sys.argv[8]) if len(sys.argv) >= 9 else 10
    built = core.build(who, poses=[pose])
    im = core.composite(who, built, pose, box=box)
    ruler(im, box[0], box[1], zoom, out); print(out, im.size)


if __name__ == '__main__': main()
