#!/usr/bin/env python3
"""
Nutrimatic desk scene - env_guides.py
Version 1.0.0

Created: 2026-10-02 - The flat layout pictures the room was generated from (v1.0.0)

The room pictures (sources/room-*.png) were made by the image model from these guides: flat blocks at four times the
scene's size where the window, the poster, the clock, the shelf and the desk go, so the generated room puts them where
the scene needs them (the people are drawn over it; the window glass is cut out for the skyline).
"""
import os
SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sources')
from PIL import Image, ImageDraw
S = 4
WALL, CEIL, CEIL_D, FRAME, GLASS, SILL, POSTER, PFRAME, CLOCK, SHELF, BOOKS, DESK, DESK_T, DESK_D, PLANT, POT = (
    (226, 216, 196), (196, 186, 168), (150, 142, 128), (40, 40, 46), (170, 205, 235), (210, 204, 192), (246, 244, 238), (24, 24, 26),
    (244, 242, 236), (120, 78, 48), (60, 90, 140), (112, 74, 46), (150, 104, 66), (78, 50, 32), (70, 130, 70), (170, 96, 60))
def room(W, win, poster, clock, shelf, plants, out):
    im = Image.new('RGB', (W * S, 160 * S), WALL); d = ImageDraw.Draw(im); r = lambda x0, y0, x1, y1, c: d.rectangle([x0 * S, y0 * S, x1 * S - 1, y1 * S - 1], fill=c)
    r(0, 0, W, 9, CEIL); r(0, 9, W, 10, CEIL_D)
    x0, y0, x1, y1 = win; r(x0 - 3, y0 - 3, x1 + 3, y1 + 3, FRAME); r(x0, y0, x1, y1, GLASS); mx = (x0 + x1) // 2; r(mx - 1, y0, mx + 1, y1, FRAME); ty = y0 + (y1 - y0) // 3; r(x0, ty - 1, x1, ty + 1, FRAME); r(x0 - 6, y1 + 3, x1 + 6, y1 + 7, SILL)
    px0, py0, px1, py1 = poster; r(px0 - 2, py0 - 2, px1 + 2, py1 + 2, PFRAME); r(px0, py0, px1, py1, POSTER)
    cx, cy, cr = clock; d.ellipse([(cx - cr - 1) * S, (cy - cr - 1) * S, (cx + cr + 1) * S, (cy + cr + 1) * S], fill=FRAME); d.ellipse([(cx - cr) * S, (cy - cr) * S, (cx + cr) * S, (cy + cr) * S], fill=CLOCK)
    if shelf:
        sx0, sy, sx1 = shelf; r(sx0, sy, sx1, sy + 2, SHELF)
        for i, bx in enumerate(range(sx0 + 3, sx0 + 15, 3)): r(bx, sy - 9 + (i % 2), bx + 2, sy, [BOOKS, (150, 50, 50), (60, 120, 90), (200, 170, 90)][i % 4])
        r(sx1 - 10, sy - 5, sx1 - 4, sy, POT); r(sx1 - 12, sy - 11, sx1 - 2, sy - 5, PLANT)
    r(0, 134, W, 160, DESK); r(0, 134, W, 137, DESK_T); r(0, 137, W, 138, DESK_D)
    for px in plants: r(px - 5, 124, px + 5, 134, POT); r(px - 8, 110, px + 8, 124, PLANT)
    im.save(out)
room(360, (262, 18, 350, 102), (14, 20, 72, 82), (88, 34, 7), (152, 30, 204), [12], os.path.join(SRC, 'guide-wide.png'))
room(240, (192, 20, 236, 90), (4, 20, 52, 70), (98, 30, 6), None, [], os.path.join(SRC, 'guide-narrow.png'))
print('wrote the guides into', SRC)
