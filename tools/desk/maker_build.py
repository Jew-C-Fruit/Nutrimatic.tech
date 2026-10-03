#!/usr/bin/env python3
"""
Nutrimatic desk scene - maker_build.py
Version 1.2.0

Created: 2026-10-02 - Maker the cat: five generated poses on one palette, eyes tidied (v1.0.0)
Modified: 2026-10-02 - A fifth bigger (reduced again from the generated pictures: 62 px long walking, 45 px tall
  sitting, 60 px long lying), five greys instead of three, new poses (sitting side-on looking up, curled up, standing
  to knead) and derived frames: blinks, eyes shut, kneading paws (v1.1.0)
Modified: 2026-10-02 - Every pose sized so her head is the same size; raised tails redrawn longer and ending in a
  point; lying down she lies with a front paw over the desk edge (the scene adds the hanging tail) (v1.2.0)

maker_build.py - Maker the cat: generated sprites (FLUX.2 klein 4B on her photos, see sources/PROVENANCE.md), reduced
with tools/portraits/pixelize.py to a set size, recoloured to one shared palette close to her real blue-grey, and
finished by hand in the eyes only."""
import sys, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..', 'portraits'))
from PIL import Image
from spritekit import Sprite, hex2rgb, rgb2hex
import pixelize as PX

SRC = os.path.join(HERE, 'sources')
# sprite name: (generated picture, which side sets the size, its length in pixels)
# The sizes keep her head the same size in every pose (about 20 px from ear tips to chin, as when walking): each
# generated picture drew her at its own scale, and sizing them all by length made her look bigger lying down and
# smaller sitting side-on.
JOBS = {'walk0': ('maker-walk-seed503.png', 'w', 62), 'walk1': ('maker-walk-seed504.png', 'w', 62), 'sit': ('maker-sit-seed511.png', 'h', 50),
        'yawn': ('maker-yawn-seed521.png', 'h', 50), 'loaf': ('maker-loaf-seed533.png', 'w', 53), 'sitside': ('maker-sitside-seed9550.png', 'h', 53),
        'curl': ('maker-curl-seed9529.png', 'w', 51), 'stand': ('maker-knead-seed9536.png', 'w', 60)}
LINE, DEEP, SHADE, FILL, LIGHT, HI = '#262830', '#474b56', '#5b5f6a', '#7b808b', '#8f949f', '#a9aeb8'
EYE, PINK, MOUTH, WHITE = '#c9d84a', '#c48f9b', '#de7186', '#f4f4f0'
COAT = [DEEP, SHADE, FILL, LIGHT, HI]
BANDS = [0.10, 0.32, 0.74, 0.93]          # share of the coat (darkest first) that each grey ends at


def reduce(name, axis, target, cell=10, colors=12):
    """the picture scaled so the cat is `target` sprite pixels long (or tall), then pixelized"""
    rgb = np.asarray(Image.open(os.path.join(SRC, name)).convert('RGB')); mask, _ = PX.subject_mask(rgb)
    ys, xs = np.where(mask); ext = (xs.max() - xs.min()) if axis == 'w' else (ys.max() - ys.min())
    s = target * cell / ext; rgb2 = np.asarray(Image.fromarray(rgb).resize((int(rgb.shape[1] * s), int(rgb.shape[0] * s)), Image.LANCZOS))
    spr, alpha, centers, _ = PX.pixelize(rgb2, cell, colors=colors, line_colors=2)
    return Sprite(np.where(alpha, spr, -1), [rgb2hex(c) for c in PX.oklab_to_srgb(centers)])


def recolour(s):
    """eyes, pink and the mouth by hue; the darkest colours are the outline; the coat's colours to five greys by lightness"""
    lab = PX.srgb_to_oklab(np.array([hex2rgb(c) for c in s.pal], dtype=np.float64)); out = []
    for L, a, b in lab:
        chroma, hue = float(np.hypot(a, b)), float(np.degrees(np.arctan2(b, a)))
        if chroma > 0.08 and 80 < hue < 140: out.append(EYE)
        elif chroma > 0.05 and -40 < hue < 40: out.append(MOUTH if L < 0.72 and chroma > 0.11 else PINK)
        elif L < 0.30: out.append(LINE)
        elif L > 0.9: out.append(WHITE)
        else: out.append(DEEP if L < 0.40 else SHADE if L < 0.53 else FILL if L < 0.64 else LIGHT if L < 0.72 else HI)
    pal, idx = [], s.idx.copy()
    for i, c in enumerate(out):
        if c not in pal: pal.append(c)
        idx[s.idx == i] = pal.index(c)
    return shade_form(Sprite(idx, pal))


def shade_form(s):
    """the generated coat is nearly one flat grey: light from above, so in every column the back catches the light
    and the belly and the underside fall into shade (only plain coat pixels change; marks, eyes and outline stay)"""
    out = s.copy(); solid = s.idx >= 0; fill = s.idx == (s.pal.index(FILL) if FILL in s.pal else -9)
    h, w = s.idx.shape
    for x in range(w):
        ys = np.where(solid[:, x])[0]
        if len(ys) < 4: continue
        top, bot = ys.min(), ys.max()
        for y in range(top, bot + 1):
            if not fill[y, x]: continue
            t, n = (y - top) / max(1, bot - top), bot - top
            if y - top == 1 and n >= 10: out.put(x, y, HI)
            elif t < 0.22 and n >= 6: out.put(x, y, LIGHT)
            elif t > 0.9 and n >= 12: out.put(x, y, DEEP)
            elif t > 0.68 and n >= 8: out.put(x, y, SHADE)
    return out


def eye(s, x, y, w=2, pupil=0):
    """a w x 2 yellow-green eye with a one-pixel-wide slit pupil in column `pupil`"""
    for dx in range(w):
        for dy in (0, 1): s.put(x + dx, y + dy, LINE if dx == pupil else EYE)


def shut(s, x, y, w=2, below=FILL):
    """a closed eye: a dark lid line where the eye was, the coat under it"""
    for dx in range(w): s.put(x + dx, y, below); s.put(x + dx, y + 1, LINE)


# eyes the reduction lost (x, y, width, pupil column), found by looking at the zoomed sprites
EYES = {'walk1': [(54, 15, 3, 1)], 'loaf': [(40, 12, 3, 1)]}

# Tails held up end in a point now, a few pixels longer than the generated ones' round ends: the round end is cleared
# above a row and the tail is drawn on from there, narrowing to a point along a short curve.
# pose: (row to cut at, x where the tail is at that row, its width there, the curve on from it, rows to add on top)
TAILS = {'walk0': (8, 4.5, 6, [(4.8, 4), (5.8, 0), (7.5, -3), (9, -4.5)], 5),
         'walk1': (9, 3.5, 5, [(3.8, 5), (4.8, 1), (6.5, -2), (8, -3.5)], 4),
         'stand': (8, 4.0, 5, [(4.3, 4), (5.5, 0.5), (7.5, -2), (9.5, -3.5)], 4)}


def taper(s, cut, x0, w0, pts, add):
    """the tail above row `cut` redrawn as a tapering stroke from (x0, cut) through pts to a point"""
    s = s.pad(top=add); cut += add; pts = [(x, y + add) for x, y in pts]
    tail = np.zeros(s.idx.shape, bool); tail[:cut, :max(1, int(x0 + w0 + 3))] = True
    s.idx[tail & (s.idx >= 0)] = -1                                        # the old round end goes
    path = [(x0, cut + 0.5)] + pts; samples = []
    seg = [np.hypot(bx - ax, by - ay) for (ax, ay), (bx, by) in zip(path, path[1:])]; total = sum(seg)
    for (ax, ay), (bx, by), L in zip(path, path[1:], seg):
        for k in range(int(L * 4) + 1):
            t = k / max(1, int(L * 4)); samples.append((ax + (bx - ax) * t, ay + (by - ay) * t))
    h, w = s.idx.shape; yy, xx = np.mgrid[0:h, 0:w]; outline = np.zeros((h, w), bool); fill = np.zeros((h, w), bool); light = np.zeros((h, w), bool)
    for i, (cx, cy) in enumerate(samples):
        t = i / max(1, len(samples) - 1); r = (w0 / 2 - 0.5) * (1 - t) ** 1.3 + 0.2
        d = np.hypot(xx + 0.5 - cx, yy + 0.5 - cy)
        outline |= d <= r + 0.85; fill |= d <= r; light |= np.hypot(xx + 0.5 - (cx + 0.9), yy + 0.5 - cy) <= r - 0.8
    region = outline & ~(s.idx >= 0) | (outline & (yy < cut))
    s.idx[region & ~fill] = s.color(LINE); s.idx[region & fill] = s.color(FILL); s.idx[region & fill & light] = s.color(LIGHT)
    return s
# kneading: the front paw lifted two pixels, near paw then far paw (columns, rows of the leg)
PAWS = {'knead0': (36, 46, 44, 55), 'knead1': (47, 56, 46, 55)}   # (rows counted after the tail's 4 added on top)


def blink(s):
    """the same sprite with the eyes shut: each eye's top row becomes coat, its bottom row the dark lid line"""
    from scipy import ndimage
    out = s.copy(); e = s.idx == (s.pal.index(EYE) if EYE in s.pal else -9)
    lab, n = ndimage.label(ndimage.binary_dilation(e, structure=np.ones((3, 3), bool)) & (e | (s.idx == s.pal.index(LINE))))
    for i in range(1, n + 1):
        ys, xs = np.where((lab == i) & e)
        if not len(ys): continue
        y0, y1, x0, x1 = ys.min(), ys.max(), xs.min(), xs.max()
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                if s.idx[y, x] >= 0 and s.pal[s.idx[y, x]] in (EYE, LINE): out.put(x, y, LINE if y == y1 else FILL)
    return out


def lift(s, x0, x1, y0, y1, dy=2):
    """a paw lifted: the leg's pixels in the box moved up dy rows, the rows left under it cleared"""
    out = s.copy(); block = s.idx[y0:y1 + 1, x0:x1 + 1].copy()
    out.idx[y1 - dy + 1:y1 + 1, x0:x1 + 1] = -1
    m = block >= 0; tgt = out.idx[y0 - dy:y1 + 1 - dy, x0:x1 + 1]; tgt[m] = block[m]
    return out


def sprites():
    out = {k: recolour(reduce(*job)) for k, job in JOBS.items()}
    for k, eyes in EYES.items():
        for e in eyes: eye(out[k], *e)
    for k, (cut, x0, w0, pts, add) in TAILS.items(): out[k] = taper(out[k], cut, x0, w0, pts, add)
    for k, box in PAWS.items(): out[k] = lift(out['stand'], *box)
    for k in [k for k in out if k not in ('yawn',)]: out[k + 'Blink'] = blink(out[k])
    return out


# rows of each sprite that hang below the surface she lies on: lying at the desk's front edge, a front paw hangs over
GROUND = {'loaf': 6, 'loafBlink': 6}

if __name__ == '__main__':
    sp = sprites(); ims = []
    for k, s in sp.items():
        print(k, s.w, s.h, len(s.pal)); s.view(os.path.join(os.environ.get('MAKER_VIEWS', '/tmp'), 'maker-%s.png' % k), zoom=12); ims.append(s.image())
    z = 5; W = sum(i.width for i in ims) * z + 10 * (len(ims) + 1); H = max(i.height for i in ims) * z + 20
    sheet = Image.new('RGBA', (W, H), (233, 223, 204, 255)); x = 10
    for i in ims: sheet.alpha_composite(i.resize((i.width * z, i.height * z), Image.NEAREST), (x, H - 10 - i.height * z)); x += i.width * z + 10
    sheet.convert('RGB').save(sys.argv[1] if len(sys.argv) > 1 else '/tmp/maker-sheet.png'); print(sheet.size)
