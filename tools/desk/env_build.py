#!/usr/bin/env python3
"""
Nutrimatic desk scene - env_build.py
Version 1.4.0

Created: 2026-10-02 - The room, the skyline and the two anglepoise lamps as generated pictures reduced to the scene's
  pixels, written to assets/desk/ (v1.0.0)
Modified: 2026-10-02 - Victory Boogie Woogie instead of the poster; the rooms with the poster edited out (v1.1.0)
Modified: 2026-10-03 - The Nutrimatic "nu" mark on the shaker bottle prop (v1.2.0)
Modified: 2026-10-03 - The papers prop drawn edge-on, as the flat front view of the desk needs (v1.3.0)
Modified: 2026-10-04 - The desk has a top now (Cole's note 12, "now that the desk is 3d"): nine rows of wood surface
  above the front edge, in the desk's own colours, darker by the wall; the front edge and the drawers move down (v1.4.0)

The environment was drawn in code until v0.7 and looked low-fi next to the figures, so it is made the same way as they
are now: pictures generated on the GPU machine (FLUX.2 klein 4B, see sources/PROVENANCE.md) and reduced with
tools/portraits/pixelize.py. This writes, into assets/desk/:

  room-wide.png, room-narrow.png    the wall, ceiling, window frame, poster frame, clock, shelves (window glass cut out)
  desk-wide.png, desk-narrow.png    the desk: the rows from the desk line down, drawn in front of the figures
  sky-day.png, sky-night.png        Midtown seen through the window (sky cut out: the scene paints the sky by the hour)
  lamp-red.png, lamp-white.png      the anglepoise lamps: Cole's red one, Ilinca's white one (the same lamp recoloured)
  prop-*.png                        things on the desk: the shaker bottle, a mug, papers, a vase of tulips, a succulent
  painting-wide.png, -narrow.png    Mondrian's Victory Boogie Woogie in its diamond white box frame, where the poster was

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
# picture, box around the window. The "-noposter" pictures are the generated rooms with the poster edited out (a crop
# around it given back to the model, see PROVENANCE.md), so the painting can hang there instead.
ROOMS = {'wide': ('room-wide-seed9701-noposter.png', (256, 12, 356, 108)), 'narrow': ('room-narrow-seed9802-noposter.png', (186, 14, 240, 96))}


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
    front = deepen(s.copy(), name); front.idx[:DESK_Y, :] = -1
    back.save(os.path.join(OUT, 'room-%s.png' % name)); front.save(os.path.join(OUT, 'desk-%s.png' % name))
    return dict(glass=[int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())], colours=len(s.pal))


# The generated rooms show the desk exactly at desk height: its front edge (a lit top line, the board's face, a shadow)
# and then the drawers, no top. Seen a little from above it has one: DEEP rows of surface between the wall and the
# front edge, so the figures sit behind it, their forearms and the things on the desk lie on it, and Maker walks on it.
DEEP = 9
# the surface's wood, from the desk's own colours: (the line where it meets the wall, the far rows, the near rows, grain)
TOP = {'wide': ('#955d3c', '#b57a4f', '#d49a67', '#edbf86'), 'narrow': ('#613925', '#975939', '#ad6e46', '#c58454')}


def deepen(s, name):
    """the desk with a top: everything from the desk line down moves DEEP rows lower (the bottom rows drop off the
    picture) and the gap becomes the top's surface, a little darker toward the wall, with long thin grain streaks"""
    h = s.h; out = s.copy()
    lum = lambda i: sum(w * v for w, v in zip((0.2126, 0.7152, 0.0722), hex2rgb(s.pal[i]))) if i >= 0 else 255
    desk = np.array([lum(s.idx[DESK_Y + 2, x]) < 180 for x in range(s.w)])   # the desk's columns (the narrow room has wall past its end)
    out.idx[DESK_Y + DEEP:, desk] = s.idx[DESK_Y:h - DEEP, desk]
    wall, far, near, light = TOP[name]; rng = np.random.RandomState(12)
    for r in range(DEEP):
        y = DESK_Y + r
        base, streak = (wall, wall) if r == 0 else ((far, wall) if r < 3 else (near, far))
        x = 0; row = -np.ones(s.w, dtype=np.int16)
        while x < s.w:                                                   # runs of the base tone broken by streaks of grain
            run = rng.randint(6, 26); row[x:x + run] = out.color(base); x += run
            if r > 0:
                k = rng.randint(3, 12); col = light if (r >= 5 and rng.rand() < 0.18) else streak
                row[x:x + k] = out.color(col); x += k
        out.idx[y, desk] = row[desk]
        ends = [x for x in range(s.w) if desk[x] and ((x + 1 < s.w and not desk[x + 1]) or (x > 0 and not desk[x - 1]))]
        for x in ends: out.idx[y, x] = out.color('#010102')               # the top's side edge where the desk stops
    return out


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


# Victory Boogie Woogie (Piet Mondrian, 1942-44) where the poster was: a diamond in a white box frame, as it hangs in
# the Kunstmuseum Den Haag. The painting's own lines run level, so each sprite pixel is the average of its patch of the
# photograph snapped to Mondrian's colours; the frame and its shadow are plain shapes. PAINTING = the photo (its
# painting's centre and half-diagonal in the photo's pixels); sizes = the frame's half-diagonal per layout.
PAINTING = ('/home/maker/claude/nutrimatic/work/env/mondrian/vbw-source.jpg', (636, 622), 443)
MONDRIAN = ['#f1efe6', '#cfcfc8', '#a7a7a0', '#1d1d1f', '#c9202f', '#1f3e94', '#efc22c']
PAINTING_SIZES = {'wide': 31, 'narrow': 26}


def pick_colour(counts):
    """a patch's colour: one of the red, blue or yellow if it covers a good part of it (they are what the painting is
    about, and a plain majority loses most of its small squares to the white and greys), else black, else the
    commonest of the white and greys"""
    total = max(1, counts.sum()); hues = {4: counts[4], 5: counts[5], 6: counts[6]}; best = max(hues, key=hues.get)
    if hues[best] / total >= 0.28: return best
    if counts[3] / total >= 0.35: return 3
    return int(np.argmax(counts[:3]))


def painting(name):
    path, (scx, scy), sr = PAINTING; R = PAINTING_SIZES[name]; ri = R - 4
    src = np.asarray(Image.open(path).convert('RGB')).astype(np.float64); n = 2 * R + 3
    area = src[int(scy - sr * 0.5):int(scy + sr * 0.5), int(scx - sr * 0.5):int(scx + sr * 0.5)].reshape(-1, 3)
    src = np.clip(src * (241.0 / np.percentile(area.mean(axis=1), 90)), 0, 255)     # the gallery light to paper white
    pal = np.array([hex2rgb(c) for c in MONDRIAN], dtype=np.float64); lab_pal = PX.srgb_to_oklab(pal)
    out = Sprite(-np.ones((n, n), dtype=np.int16), [])
    c = R; k = sr / (ri + 0.5)
    for y in range(n):
        for x in range(n):
            dx, dy = x - c, y - c
            if abs(dx) + abs(dy) <= ri:                                     # the painting
                x0, y0 = scx + (dx - 0.5) * k, scy + (dy - 0.5) * k
                patch = src[int(max(0, y0)):int(y0 + k), int(max(0, x0)):int(x0 + k)].reshape(-1, 3)
                lab = PX.srgb_to_oklab(patch); counts = np.bincount(((lab[:, None, :] - lab_pal[None]) ** 2).sum(axis=2).argmin(axis=1), minlength=len(MONDRIAN))
                out.put(x, y, MONDRIAN[pick_colour(counts)])
            elif abs(dx) + abs(dy) == ri + 1: out.put(x, y, '#d8d6cf')     # the painting's edge in the mat
            elif abs(dx) + abs(dy) < R: out.put(x, y, '#f6f5f0')            # the white mat
            elif abs(dx) + abs(dy) == R: out.put(x, y, '#b9b8b2' if dy >= 0 else '#e6e5df')   # the frame's edge, darker below
    for y in range(n):                                                       # its shadow on the wall, down and right
        for x in range(n):
            dx, dy = x - c - 1, y - c - 2
            if out.idx[y, x] < 0 and abs(dx) + abs(dy) <= R: out.put(x, y, '#9a9a96')
    out.save(os.path.join(OUT, 'painting-%s.png' % name)); return [out.w, out.h]


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
        if name == 'bottle':                                                    # the "nu" monogram on its white body
            whites = [i for i, c in enumerate(sp.pal) if sum(hex2rgb(c)) > 690]; ys, xs = np.where(np.isin(sp.idx, whites))
            mx, my = int(np.median(xs)) - 2, int(ys.min() + (ys.max() - ys.min()) * 0.45) - 2; ink = sp.color('#111111')
            for r, row in enumerate(['kkk..', 'k.k..', 'k.k.k', 'k.k.k', '..kkk']):
                for c, ch in enumerate(row):
                    if ch == 'k': sp.idx[my + r, mx + c] = ink
        if name == 'papers':                                                    # the desk is seen flat from the front: papers lie edge-on
            sp = edge_on_papers()
        sp.save(os.path.join(OUT, 'prop-%s.png' % name)); out[name] = [sp.w, sp.h]
    return out


def edge_on_papers():
    """a short stack of paper with a red notebook on it, seen exactly from the front at desk height (note 9d: the
    generated stack was drawn from above, in perspective, against the flat desk)"""
    rows = ['..kkkkkkkkkkkkk.......',
            '..krrrrrrrrrrrrk......',
            '..kRRRRRRRRRRRRk......',
            'kkkkkkkkkkkkkkkkkkkkk.',
            'kwwwwwwwwwwwwwwwwwwwk.',
            'kgggggggggggggggggggk.',
            'kwwwwwwwwwwwwwwwwwwwk.',
            'kkkkkkkkkkkkkkkkkkkkkk']
    key = {'k': '#1d1d1f', 'w': '#fbfaf5', 'g': '#d9d5c8', 'r': '#e4002b', 'R': '#a3001f'}
    s = Sprite(-np.ones((len(rows), len(rows[0])), dtype=np.int16), [])
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch != '.': s.put(x, y, key[ch])
    return s


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    info = {'wide': room('wide'), 'narrow': room('narrow'), 'sky': skyline(), 'lamp': lamps(), 'props': props(), 'painting': [painting('wide'), painting('narrow')]}
    print(json.dumps(info, indent=1))
