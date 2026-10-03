#!/usr/bin/env python3
"""
Nutrimatic desk scene - env_build.py
Version 1.0.0

Created: 2026-10-02 - The room, the skyline and the two anglepoise lamps as generated pictures reduced to the scene's
  pixels, written to assets/desk/ (v1.0.0)

The environment was drawn in code until v0.7 and looked low-fi next to the figures, so it is made the same way as they
are now: pictures generated on the GPU machine (FLUX.2 klein 4B, see sources/PROVENANCE.md) and reduced with
tools/portraits/pixelize.py. This writes, into assets/desk/:

  room-wide.png, room-narrow.png    the wall, ceiling, window frame, poster frame, clock, shelves (window glass cut out)
  desk-wide.png, desk-narrow.png    the desk: the rows from the desk line down, drawn in front of the figures
  sky-day.png, sky-night.png        Midtown seen through the window (sky cut out: the scene paints the sky by the hour)
  lamp-red.png, lamp-white.png      the anglepoise lamps: Cole's red one, Ilinca's white one (the same lamp recoloured)
  prop-*.png                        things on the desk: the shaker bottle, a mug, papers, a vase of tulips, a succulent

and prints the numbers the scene needs (where the glass is, where the red aircraft lights are).

  python3 tools/desk/env_build.py            (needs numpy, scipy, pillow)
"""
import json, os, sys
import numpy as np
from PIL import Image
from scipy import ndimage
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..', 'portraits'))
import pixelize as PX
from spritekit import Sprite, hex2rgb, rgb2hex

SRC = os.path.join(HERE, 'sources')
OUT = os.path.join(HERE, '..', '..', 'assets', 'desk')
DESK_Y = 134                                   # the scene's desk line (js/desk-scene.js)
ROOMS = {'wide': ('room-wide-seed9701.png', (256, 12, 356, 108)), 'narrow': ('room-narrow-seed9802.png', (186, 14, 240, 96))}   # picture, box around the window


def reduce_full(path, cell, colors, line_colors=3):
    """a whole picture (no cut-out) on a grid starting at its corner"""
    rgb = np.asarray(Image.open(path).convert('RGB'))
    spr, alpha, centers, _ = PX.pixelize(rgb, cell, colors=colors, mask=np.ones(rgb.shape[:2], bool), origin=(0, 0), crop=False, outline=False, line_colors=line_colors)
    return Sprite(spr.astype(np.int16), [rgb2hex(c) for c in PX.oklab_to_srgb(centers)])


def glass(s, box):
    """the window panes: pale blue pixels inside the window's box, joined to each other"""
    x0, y0, x1, y1 = box; lab = PX.srgb_to_oklab(np.array([hex2rgb(c) for c in s.pal], dtype=np.float64))
    blue = [i for i, (L, a, b) in enumerate(lab) if L > 0.72 and b < -0.025]
    m = np.zeros(s.idx.shape, bool); sub = np.isin(s.idx[y0:y1, x0:x1], blue); m[y0:y1, x0:x1] = sub
    return m


def room(name):
    path, box = ROOMS[name]; s = reduce_full(os.path.join(SRC, path), 4, 28)
    m = glass(s, box); ys, xs = np.where(m)
    back = s.copy(); back.idx[m] = -1; back.idx[DESK_Y:, :] = -1           # the window glass and the desk are not part of the back wall
    front = s.copy(); front.idx[:DESK_Y, :] = -1
    back.save(os.path.join(OUT, 'room-%s.png' % name)); front.save(os.path.join(OUT, 'desk-%s.png' % name))
    return dict(glass=[int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())], colours=len(s.pal))


def sky_mask(rgb, tol):
    a = rgb.astype(int); top = np.median(a[:8].reshape(-1, 3), axis=0)
    near = np.abs(a - top).sum(axis=2) < tol; lab, _ = ndimage.label(near); keep = np.unique(lab[0]); keep = keep[keep != 0]
    return np.isin(lab, keep)


def reduce_sky(path, tol):
    rgb = np.asarray(Image.open(os.path.join(SRC, path)).convert('RGB')); m = ndimage.binary_opening(~sky_mask(rgb, tol), iterations=1)
    spr, alpha, centers, _ = PX.pixelize(rgb, 10, colors=24, mask=m, origin=(0, 0), crop=False, line_colors=2, outline=False)
    return Sprite(np.where(alpha, spr, -1).astype(np.int16), [rgb2hex(c) for c in PX.oklab_to_srgb(centers)])


# The United Nations slab is a plain glass face 35 px wide; 21 columns out of its middle bring the Empire State Building
# and the Chrysler Building close enough to share the window.
UN_CUT = (46, 67)
WARM, WARM2, COOL, CROWN, RED = '#ffd27a', '#f6b85a', '#e6eeff', '#f4f6ff', '#ff3b30'


def lit(s, x, y, col):
    if 0 <= x < s.w and 0 <= y < s.h and s.idx[y, x] >= 0: s.put(x, y, col)


def skyline():
    day, night = reduce_sky('sky-day-seed9101.png', 26), reduce_sky('sky-night-seed9603.png', 18)
    cut = lambda s: Sprite(np.concatenate([s.idx[:, :UN_CUT[0]], s.idx[:, UN_CUT[1]:]], axis=1), s.pal)
    day, night = cut(day), cut(night); dx = UN_CUT[1] - UN_CUT[0]
    # Lights after the real skyline at night (the night photos in PROVENANCE.md): many office windows lit warm, some
    # cool white; the Empire State Building's top floodlit white with its mast; the Chrysler Building's crown lit in
    # white chevrons; red aircraft lights on the tallest tops (these blink, so the scene draws them).
    dlab = PX.srgb_to_oklab(np.array([hex2rgb(c) for c in day.pal], dtype=np.float64)); rng = np.random.RandomState(7)
    for y in range(night.h):
        for x in range(night.w):
            if night.idx[y, x] < 0 or day.idx[y, x] < 0 or y < 30: continue
            L = dlab[day.idx[y, x]][0]; r = rng.rand()
            if L > 0.62 and r < 0.26: lit(night, x, y, WARM if r < 0.17 else COOL if r < 0.22 else WARM2)
    esb = (16, 36)                                                       # mast top; the stepped crown below it
    for y in range(44, 57):
        for x in range(12, 21):
            if night.idx[y, x] >= 0 and day.idx[y, x] >= 0 and dlab[day.idx[y, x]][0] > 0.5 and (x + y) % 2 == 0: lit(night, x, y, CROWN)
    for y in range(37, 44): lit(night, 16, y, '#cfd8ff')
    chrysler = (101 - dx, 33)
    for y in range(34, 47):
        w = (y - 33) // 3
        for x in (chrysler[0] - w, chrysler[0] + w): lit(night, x, y, CROWN)
    tops = [esb, chrysler, (115 - dx, 24), (144 - dx, 38), (131 - dx, 47)]
    day.save(os.path.join(OUT, 'sky-day.png')); night.save(os.path.join(OUT, 'sky-night.png'))
    return dict(size=[day.w, day.h], aircraft=[list(t) for t in tops], un_cut=list(UN_CUT))


def lamps():
    """the red lamp from its picture; the white one is the same lamp with the red ramp swapped for a white-and-grey one"""
    rgb = np.asarray(Image.open(os.path.join(SRC, 'lamp-seed9401.png')).convert('RGB')); mask, _ = PX.subject_mask(rgb)
    ys, xs = np.where(mask); s = 46 * 10 / (ys.max() - ys.min())              # 46 px tall
    rgb2 = np.asarray(Image.fromarray(rgb).resize((int(rgb.shape[1] * s), int(rgb.shape[0] * s)), Image.LANCZOS))
    spr, alpha, centers, _ = PX.pixelize(rgb2, 10, colors=12, line_colors=2)
    red = Sprite(np.where(alpha, spr, -1).astype(np.int16), [rgb2hex(c) for c in PX.oklab_to_srgb(centers)])
    lab = PX.srgb_to_oklab(np.array([hex2rgb(c) for c in red.pal], dtype=np.float64)); white = red.copy(); pal = []
    for (L, a, b), c in zip(lab, red.pal):
        chroma, hue = float(np.hypot(a, b)), float(np.degrees(np.arctan2(b, a)))
        if chroma > 0.08 and -30 < hue < 60:                                    # the red paint -> white enamel, shaded in cool greys
            v = min(255, int(120 + 150 * L)); pal.append(rgb2hex((v - 6, v - 3, v)) if L < 0.7 else rgb2hex((v, v, min(255, v + 4))))
        else: pal.append(c)
    white.pal = pal
    red.save(os.path.join(OUT, 'lamp-red.png')); white.save(os.path.join(OUT, 'lamp-white.png'))
    return dict(size=[red.w, red.h])


PROPS = {'bottle': ('prop-bottle-seed9967.png', 30), 'mug': ('prop-mug-seed9933.png', 12), 'papers': ('prop-papers-seed9966.png', 10),
         'vase': ('prop-vase-seed9944.png', 30), 'plant': ('prop-plant-seed9956.png', 18)}


def props():
    """small things on the desk, each reduced to a set height; a grey drop shadow or steam in the picture is left out"""
    out = {}
    for name, (path, tall) in PROPS.items():
        rgb = np.asarray(Image.open(os.path.join(SRC, path)).convert('RGB')); mask, bg = PX.subject_mask(rgb)
        lab = PX.srgb_to_oklab(rgb); chroma = np.hypot(lab[..., 1], lab[..., 2])
        greyish = (chroma < 0.03) & (lab[..., 0] > 0.45) & (lab[..., 0] < 0.80)            # shadow on the grey ground
        if name in ('bottle', 'mug'): mask &= ~greyish
        if name == 'mug': mask &= ~((chroma < 0.03) & (lab[..., 0] > 0.80))                # the steam (the scene draws its own)
        lab_m, n = ndimage.label(mask); sizes = ndimage.sum(mask, lab_m, index=np.arange(1, n + 1)); mask = lab_m == (int(np.argmax(sizes)) + 1)
        mask = ndimage.binary_fill_holes(mask)
        ys, xs = np.where(mask); s = tall * 10 / (ys.max() - ys.min())
        rgb2 = np.asarray(Image.fromarray(rgb).resize((int(rgb.shape[1] * s), int(rgb.shape[0] * s)), Image.LANCZOS))
        m2 = np.asarray(Image.fromarray(mask.astype(np.uint8) * 255).resize((rgb2.shape[1], rgb2.shape[0]), Image.NEAREST)) > 127
        spr, alpha, centers, _ = PX.pixelize(rgb2, 10, colors=10, line_colors=2, mask=m2)
        sp = Sprite(np.where(alpha, spr, -1).astype(np.int16), [rgb2hex(c) for c in PX.oklab_to_srgb(centers)])
        sp.save(os.path.join(OUT, 'prop-%s.png' % name)); out[name] = [sp.w, sp.h]
    return out


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    info = {'wide': room('wide'), 'narrow': room('narrow'), 'sky': skyline(), 'lamp': lamps(), 'props': props()}
    print(json.dumps(info, indent=1))
