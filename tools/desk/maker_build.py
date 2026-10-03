#!/usr/bin/env python3
"""
Nutrimatic desk scene - maker_build.py
Version 1.7.0

Created: 2026-10-02 - Maker the cat: five generated poses on one palette, eyes tidied (v1.0.0)
Modified: 2026-10-02 - A fifth bigger (reduced again from the generated pictures: 62 px long walking, 45 px tall
  sitting, 60 px long lying), five greys instead of three, new poses (sitting side-on looking up, curled up, standing
  to knead) and derived frames: blinks, eyes shut, kneading paws (v1.1.0)
Modified: 2026-10-02 - Every pose sized so her head is the same size; raised tails redrawn longer and ending in a
  point; lying down she lies with a front paw over the desk edge (the scene adds the hanging tail) (v1.2.0)
Modified: 2026-10-03 - Darker coat; a yawn with her head thrown back; tails end like a paintbrush; a second look with big
  stylized eyes (sheet(big=True), exported as makerB) to compare (v1.3.0)
Modified: 2026-10-03 - Round tail tips again, a little longer (pointed was worse); the tail curled along her side when
  lying smoothed away, so the hanging one is her only tail (v1.3.1)
Modified: 2026-10-03 - The big stylized eyes are her look now (the user: "Big eyes are better"); the exporter asks for
  sheet(big=True) (v1.4.0)
Modified: 2026-10-03 - A real walk cycle: four frames from one generated sheet, cut and reduced on one grid (v1.5.0)
Modified: 2026-10-03 - Note 6: the walk is rigged (walk_rig.py): twelve frames, four legs in a cat's lateral-sequence
  walk with planted feet, on a body the model drew over the rig (v1.6.0)
Modified: 2026-10-03 - The walk redone (Cole: the rigged walk was "completely wrong"): walk_rig.py 2.0 draws ten frames
  (walk0..walk9 and their Blink twins) on her standing body, the one she kneads in, after docs/animal-walk-cycles.md;
  the generated walk body (walk_body) is gone (v1.7.0)

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
        'yawn': ('maker-yawn-back-seed9612.png', 'h', 50), 'loaf': ('maker-loaf-seed533.png', 'w', 53), 'sitside': ('maker-sitside-seed9550.png', 'h', 53),
        'curl': ('maker-curl-seed9529.png', 'w', 51), 'stand': ('maker-knead-seed9536.png', 'w', 60)}
# her coat, darker than first drawn (the user: "a bit darker")
LINE, DEEP, SHADE, FILL, LIGHT, HI = '#1f2129', '#3b3f49', '#4d515c', '#696e79', '#7d828d', '#959aa5'
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


# The walk: one generated picture with four frames of a walk cycle side by side (sources/maker-walkcycle-*.png), cut into
# its four cells and reduced at one scale on one grid, so the frames line up and only the legs move.
WALK = ('maker-walkcycle-seed9703.png', 4, 64)      # picture, frames, her length in pixels in the first frame


def walk_frames(cell=10, colors=12):
    """the four cats of the walk-cycle picture, each found on its own (they overlap the quarters of the picture), reduced
    at one scale, and lined up on the tip of the nose and the feet so only the legs and tail move"""
    from scipy import ndimage
    path, n, target = WALK; rgb = np.asarray(Image.open(os.path.join(SRC, path)).convert('RGB'))
    a = rgb.astype(int); bg = np.median(np.concatenate([a[:4].reshape(-1, 3), a[-4:].reshape(-1, 3)]), axis=0)   # all four cats, not just the biggest
    near = np.abs(a - bg).sum(axis=2) < 40; l0, k0 = ndimage.label(near); edge = np.unique(np.concatenate([l0[0], l0[-1], l0[:, 0], l0[:, -1]]))
    mask = ~np.isin(l0, edge[edge != 0]); mask = ndimage.binary_opening(mask, iterations=2)
    # the cats touch each other here and there: cut between them where the fewest of their pixels stand, near each quarter
    cols = mask.sum(axis=0); qw = rgb.shape[1] // n; cuts = [0]
    for q in range(1, n):
        lo, hi = q * qw - qw // 3, q * qw + qw // 3; cuts.append(lo + int(np.argmin(cols[lo:hi])))
    cuts.append(rgb.shape[1]); lab = np.zeros(mask.shape, int)
    for q in range(n):
        part = np.zeros(mask.shape, bool); part[:, cuts[q]:cuts[q + 1]] = mask[:, cuts[q]:cuts[q + 1]]
        l2, k2 = ndimage.label(part)
        if k2: sz = ndimage.sum(part, l2, index=np.arange(1, k2 + 1)); lab[l2 == (int(np.argmax(sz)) + 1)] = q + 1
    keep = list(range(1, n + 1))
    boxes = [ndimage.find_objects((lab == i).astype(int))[0] for i in keep]
    first = boxes[0]; s = target * cell / (first[1].stop - first[1].start)
    frames = []
    for i, (ys, xs) in zip(keep, boxes):
        y0, y1, x0, x1 = max(0, ys.start - 20), min(rgb.shape[0], ys.stop + 20), max(0, xs.start - 20), min(rgb.shape[1], xs.stop + 20)
        crop = rgb[y0:y1, x0:x1].copy(); m = (lab[y0:y1, x0:x1] == i)
        big = np.asarray(Image.fromarray(crop).resize((int(crop.shape[1] * s), int(crop.shape[0] * s)), Image.LANCZOS))
        mb = np.asarray(Image.fromarray(m.astype(np.uint8) * 255).resize((big.shape[1], big.shape[0]), Image.NEAREST)) > 127
        spr, alpha, centers, _ = PX.pixelize(big, cell, colors=colors, line_colors=2, mask=mb)
        frames.append(Sprite(np.where(alpha, spr, -1).astype(np.int16), [rgb2hex(q) for q in PX.oklab_to_srgb(centers)]))
    # line up: the nose (rightmost pixel) on one column, the feet (lowest pixel) on one row
    left = max(f.w - 1 for f in frames); right = 0; up = max(f.h - 1 for f in frames)
    W, H = left + 1 + right, up + 1; out = []
    for f in frames:
        c = -np.ones((H, W), dtype=np.int16); ox, oy = left - (f.w - 1), up - (f.h - 1)
        c[oy:oy + f.h, ox:ox + f.w] = f.idx; out.append(Sprite(c, f.pal))
    m = np.zeros((H, W), bool)
    for o in out: m |= o.idx >= 0
    ys, xs = np.where(m)
    return [Sprite(o.idx[ys.min():ys.max() + 1, xs.min():xs.max() + 1], o.pal) for o in out]


# The walk the scene uses is drawn by walk_rig.py on the 'stand' sprite (see sprites(big=True) and
# docs/animal-walk-cycles.md); walk_frames() above is the first look's four generated frames, kept for sheet(big=False).


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
EYES = {'loaf': [(40, 12, 3, 1)], 'stand': [(52, 16, 3, 1)], 'walk2': [(57, 11, 3, 1)]}

# Tails held up keep their round generated tips, a few pixels longer (the user preferred round to pointed): the round
# end is lifted `add` rows and the tail below it repeated to fill the gap.
# pose: (first row below the round end, columns the tail is in, rows to add)
TAILS = {'stand': (7, 14, 2)}


def elongate(s, cut, xr, add):
    """the round end of a raised tail (rows above `cut`, columns below xr) lifted `add` rows, the tail stretched to meet it"""
    old = s.idx.copy(); s = s.pad(top=add); s.idx[:cut + add, :xr] = -1
    s.idx[:cut, :xr] = old[:cut, :xr]
    for r in range(cut, cut + add): s.idx[r, :xr] = old[cut, :xr]
    return s


def smooth_lines(s, box, passes=2):
    """dark lines inside the body in a box (x0, y0, x1, y1) become the coat around them (a tail curled along her
    side read as a second tail next to the hanging one)"""
    out = s.copy(); dark = [i for i, c in enumerate(s.pal) if c in (LINE, DEEP)]
    for _ in range(passes):
        idx = out.idx.copy(); x0, y0, x1, y1 = box
        for y in range(max(1, y0), min(out.h - 1, y1 + 1)):
            for x in range(max(1, x0), min(out.w - 1, x1 + 1)):
                if idx[y, x] not in dark: continue
                if min(idx[y - 1, x], idx[y + 1, x], idx[y, x - 1], idx[y, x + 1]) < 0: continue          # the outline stays
                nb = [idx[yy, xx] for yy in (y - 1, y, y + 1) for xx in (x - 1, x, x + 1) if (yy, xx) != (y, x) and idx[yy, xx] >= 0 and idx[yy, xx] not in dark]
                if len(nb) >= 3: out.idx[y, x] = max(set(nb), key=nb.count)
    return out


# kneading: the front paw lifted two pixels, near paw then far paw (columns, rows of the leg)
PAWS = {'knead0': (36, 46, 42, 53), 'knead1': (47, 56, 44, 53)}   # (rows counted after the tail's 2 added on top)


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


# Her eyes, redrawn bigger and more stylized (first tried as a second look to compare; the user picked it on 2026-10-03)
# after cute pixel-art animals (CC0 / CC BY sheets on OpenGameArt, see sources/PROVENANCE.md): round, four
# pixels across, a dark lid line on top, a big round pupil with a white catchlight, and closed as a smiling arc.
BIG_FRONT = ['kkkk', 'epwe', 'eppe', '.ee.']
BIG_SIDE = ['kkk', 'epw', 'epp', '.e.']
BIG_SHUT_FRONT = ['....', 'k..k', '.kk.', '....']
BIG_SHUT_SIDE = ['...', 'k.k', '.k.', '...']


def eye_spots(s):
    """where the drawn eyes are: (x0, y0, x1, y1) of each eye, its eye-coloured pixels taken together with the dark
    pixels of the pupil and lid right around them (an eye can be a single yellow pixel in a dark patch)"""
    from scipy import ndimage
    if EYE not in s.pal: return []
    e = s.idx == s.pal.index(EYE); dark = s.idx == s.pal.index(LINE)
    near = ndimage.binary_dilation(e, structure=np.ones((3, 3), bool), iterations=1)
    lab, n = ndimage.label(ndimage.binary_dilation(e, structure=np.ones((3, 3), bool), iterations=2) & (e | dark))
    spots = []
    for i in range(1, n + 1):
        m = (lab == i) & (e | (dark & near)); ys, xs = np.where(m)
        if (m & e).any() and xs.max() - xs.min() <= 5: spots.append((xs.min(), ys.min(), xs.max(), ys.max()))
    return spots


def big_eyes(s, shut=False):
    """the sprite with its eyes redrawn big and round (or shut, as smiling arcs)"""
    out = s.copy(); spots = eye_spots(s); front = len(spots) >= 2
    key = {'k': LINE, 'e': EYE, 'p': LINE, 'w': WHITE}
    for x0, y0, x1, y1 in spots:
        for y in range(y0, y1 + 1):                                         # the old eye and its pupil go back to coat
            for x in range(x0, x1 + 1):
                if s.idx[y, x] >= 0 and s.pal[s.idx[y, x]] in (EYE, LINE): out.put(x, y, FILL)
        pat = (BIG_SHUT_FRONT if shut else BIG_FRONT) if front else (BIG_SHUT_SIDE if shut else BIG_SIDE)
        cx = (x0 + x1 + 1) // 2; ox, oy = cx - len(pat[0]) // 2, y0 - 1
        for r, row in enumerate(pat):
            for c, ch in enumerate(row):
                if ch != '.': out.put(ox + c, oy + r, key[ch])
    return out


def sprites(big=False):
    out = {k: recolour(reduce(*job)) for k, job in JOBS.items() if not k.startswith('walk')}
    for i, fr in enumerate(walk_frames()): out['walk%d' % i] = recolour(fr)
    for k, eyes in EYES.items():
        for e in eyes: eye(out[k], *e)
    for k, (cut, xr, add) in TAILS.items(): out[k] = elongate(out[k], cut, xr, add)
    out['loaf'] = smooth_lines(out['loaf'], (2, 12, 20, 27))           # lying: only the tail the scene hangs over the edge
    for k, box in PAWS.items(): out[k] = lift(out['stand'], *box)
    if big:
        base = dict(out); out = {}
        for k, s in base.items():
            if k.startswith('walk'): continue                            # the walk is rigged below
            out[k] = big_eyes(s) if k != 'yawn' else s
            if k != 'yawn': out[k + 'Blink'] = big_eyes(s, shut=True)
        # the walk: walk_rig draws her four legs for each frame on the standing body (the pose she kneads in), so walking
        # and kneading share one body; the blink frames are the same walk on the standing body with its eyes shut
        import walk_rig
        cols = dict(LINE=LINE, DEEP=DEEP, SHADE=SHADE, FILL=FILL)
        for i, fr in enumerate(walk_rig.frames(out['stand'], cols)): out['walk%d' % i] = fr
        for i, fr in enumerate(walk_rig.frames(out['standBlink'], cols)): out['walk%dBlink' % i] = fr
        return out
    for k in [k for k in out if k not in ('yawn',)]: out[k + 'Blink'] = blink(out[k])
    return out


# rows of each sprite that hang below the surface she lies on: lying at the desk's front edge, a front paw hangs over
GROUND = {'loaf': 6, 'loafBlink': 6}
_cache = {}


def sheet(big=False):
    """the sprites, made once per run (the exporter asks for both looks)"""
    if big not in _cache: _cache[big] = sprites(big)
    return _cache[big]

if __name__ == '__main__':
    sp = sprites(); ims = []
    for k, s in sp.items():
        print(k, s.w, s.h, len(s.pal)); s.view(os.path.join(os.environ.get('MAKER_VIEWS', '/tmp'), 'maker-%s.png' % k), zoom=12); ims.append(s.image())
    z = 5; W = sum(i.width for i in ims) * z + 10 * (len(ims) + 1); H = max(i.height for i in ims) * z + 20
    sheet = Image.new('RGBA', (W, H), (233, 223, 204, 255)); x = 10
    for i in ims: sheet.alpha_composite(i.resize((i.width * z, i.height * z), Image.NEAREST), (x, H - 10 - i.height * z)); x += i.width * z + 10
    sheet.convert('RGB').save(sys.argv[1] if len(sys.argv) > 1 else '/tmp/maker-sheet.png'); print(sheet.size)
