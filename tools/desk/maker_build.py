#!/usr/bin/env python3
"""
Nutrimatic desk scene - maker_build.py
Version 1.0.0

Created: 2026-10-02 - Maker the cat: five generated poses on one palette, eyes tidied (v1.0.0)

maker_build.py - Maker the cat: generated sprites (FLUX.2 klein 4B on her photos, then pixelize), recoloured to
one shared palette closer to her real grey, with the eyes tidied by hand."""
import sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from spritekit import Sprite, load, hex2rgb
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'portraits'))
from pixelize import srgb_to_oklab

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sprites', 'maker')
LINE, DARK, MID, LIGHT, EYE, PINK, MOUTH, WHITE = '#262830', '#575b66', '#747985', '#8f949f', '#c9d84a', '#c48f9b', '#de7186', '#f4f4f0'

def recolour(s):
    out = s.copy(); pal = []
    for col in s.pal:
        L, a, b = srgb_to_oklab(np.array([hex2rgb(col)], dtype=np.float64))[0]; chroma = float(np.hypot(a, b)); hue = float(np.degrees(np.arctan2(b, a)))
        if chroma > 0.08 and 80 < hue < 140: new = EYE                    # yellow-green
        elif chroma > 0.05 and (hue < 40 and hue > -40): new = MOUTH if L < 0.72 and chroma > 0.11 else PINK
        elif L < 0.30: new = LINE
        elif L < 0.50: new = DARK
        elif L < 0.60: new = MID
        elif L < 0.88: new = LIGHT
        else: new = WHITE
        pal.append(new)
    out.pal = pal; return dedupe(out)

def dedupe(s):
    pal = []; idx = s.idx.copy()
    for i, col in enumerate(s.pal):
        if col not in pal: pal.append(col)
        idx[s.idx == i] = pal.index(col)
    return Sprite(idx, pal)

def get(name): return recolour(load(os.path.join(SRC, name + '-1x.png')))

FILL, SHADE, HI = '#7b808b', '#5b5f6a', '#989da8'

def unify(s):
    """the same three greys on every pose: the commonest grey becomes the coat, darker ones the shade, lighter ones the sheen"""
    greys = [c for c in (DARK, MID, LIGHT) if c in s.pal]
    counts = {c: int((s.idx == s.pal.index(c)).sum()) for c in greys}; main = max(counts, key=counts.get); order = [DARK, MID, LIGHT]
    pal = []
    for c in s.pal:
        if c not in greys: pal.append(c)
        elif c == main: pal.append(FILL)
        else: pal.append(SHADE if order.index(c) < order.index(main) else HI)
    out = s.copy(); out.pal = pal; return dedupe(out)

def eye(s, x, y, w=2, pupil=0):
    """a w x 2 yellow-green eye with a one-pixel-wide slit pupil in column `pupil`"""
    for dx in range(w):
        for dy in (0, 1): s.put(x + dx, y + dy, LINE if dx == pupil else EYE)

def sprites():
    out = {}
    for key, name in (('walk0', 'walk-002'), ('walk1', 'walk-003'), ('sit', 'sit-000'), ('yawn', 'yawn-000'), ('loaf', 'loaf-002')): out[key] = unify(get(name))
    s = out['walk0']; eye(s, 46, 14, 2, 1)
    s = out['walk1']; s.put(47, 13, FILL); s.put(47, 14, FILL); eye(s, 46, 13, 2, 1)
    s = out['sit']
    for x in range(3, 13): s.put(x, 8, FILL); s.put(x, 9, FILL)
    s.put(4, 9, FILL); s.put(5, 9, FILL); eye(s, 3, 8, 3, 1); eye(s, 9, 8, 3, 1)
    s.put(7, 11, PINK)
    s = out['loaf']
    for x in range(36, 41): s.put(x, 11, FILL); s.put(x, 12, FILL)
    eye(s, 37, 11, 3, 1); s.put(45, 10, FILL); s.put(46, 10, FILL); eye(s, 44, 11, 3, 1)
    s = out['yawn']; s.put(21, 13, WHITE); s.put(22, 16, MOUTH); s.put(21, 16, MOUTH)
    return out

# rows of each sprite that hang below the surface she stands on (the loaf's paw goes over the desk edge)
GROUND = {'walk0': 0, 'walk1': 0, 'sit': 0, 'yawn': 0, 'loaf': 4}

if __name__ == '__main__':
    from PIL import Image
    sp = sprites(); ims = []
    for k, s in sp.items():
        print(k, s.w, s.h, s.pal); s.view(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'maker-%s.png' % k), zoom=12); ims.append(s.image())
    z = 6; W = sum(i.width for i in ims) * z + 10 * (len(ims) + 1); H = max(i.height for i in ims) * z + 20
    sheet = Image.new('RGBA', (W, H), (233, 223, 204, 255)); x = 10
    for i in ims: sheet.alpha_composite(i.resize((i.width * z, i.height * z), Image.NEAREST), (x, H - 10 - i.height * z)); x += i.width * z + 10
    sheet.convert('RGB').save(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'maker-sheet.png')); print(sheet.size)
