#!/usr/bin/env python3
"""
Nutrimatic desk scene - pose_sprites.py
Version 1.2.0

Created: 2026-10-02 - Generated pose pictures -> body sprites that fit under the figure's head (v1.0.0)
Modified: 2026-10-02 - front mode 'limb': a hand or sleeve drawn over long hair without the pose's own hair (v1.1.0)
Modified: 2026-10-03 - front mode 'arm' (only skin joined to an arm from below: a fist at the chin); the neck patch no
  longer paints over a limb reaching the chin (v1.2.0)

The arms are not drawn in code. For every pose the model redraws the whole figure from the "stage" picture (the picked
portrait on a larger canvas, sitting behind a flat blue desk at the scene's desk line; see make_stage in this file), so
arms, hands and whatever they hold come out in the figure's own style. This module turns such a picture into what the
scene draws:

  body    everything except the head, on the base sprite's own pixel grid (the paddings of the stage are multiples of
          the cell), snapped to the figure's palette plus a few prop colours
  front   the part of a pose that must cover the face (a mug at the mouth, a hand over a yawn): a box per pose

The head always comes from characters.py, so the face frames keep working in every pose.
"""
import json, os, sys
import numpy as np
from PIL import Image
from scipy import ndimage

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..', 'portraits'))
from spritekit import Sprite, hex2rgb, rgb2hex
import pixelize as PX

CELL, PAD_X, PAD_TOP, DESK_H = 12, 192, 384, 200
DESK = (72, 120, 200)
# colours a pose may use besides the figure's own: what the props are made of
PROPS = ['#e4002b', '#a3001f', '#ff5a72', '#fbfaf5', '#d9d5c8', '#cfd2d4', '#9a9ea2', '#5f6368', '#2f6b3a', '#1f4a28', '#d9a650', '#dfe9f5', '#7fb2e0']


def make_stage(src, grid, desk_row, out):
    """the picture the pose edits start from. grid = the base sprite's json from pixelize (offset, crop)"""
    im = Image.open(src).convert('RGB'); ox, oy = grid['offset']; cy0 = grid['crop'][1]
    desk_y = int((desk_row + cy0) * CELL + (oy - CELL))
    a = np.asarray(im); bg = tuple(int(v) for v in np.median(np.concatenate([a[:6].reshape(-1, 3), a[:, :6].reshape(-1, 3), a[:, -6:].reshape(-1, 3)]), axis=0))
    W, H = im.width + 2 * PAD_X, PAD_TOP + desk_y + DESK_H; W += (-W) % 16; H += (-H) % 16
    canvas = Image.new('RGB', (W, H), bg); canvas.paste(im.crop((0, 0, im.width, desk_y)), (PAD_X, PAD_TOP))
    canvas.paste(Image.new('RGB', (W, H - (PAD_TOP + desk_y)), DESK), (0, PAD_TOP + desk_y)); canvas.save(out)
    return dict(size=[W, H], desk_y=PAD_TOP + desk_y, bg=bg)


def pose_mask(rgb, tol=42):
    """True where the figure and what it holds are: not the wall (flood from the top and sides), not the desk (blue, flood from the bottom)"""
    a = rgb.astype(np.int32); h, w, _ = a.shape
    border = np.concatenate([a[:4].reshape(-1, 3), a[:h // 2, :4].reshape(-1, 3), a[:h // 2, -4:].reshape(-1, 3)])
    bg = np.median(border, axis=0)
    near = np.abs(a - bg).sum(axis=2) < tol
    lab, _ = ndimage.label(near); edge = np.unique(np.concatenate([lab[0], lab[:, 0], lab[:, -1]])); wall = np.isin(lab, edge[edge != 0])
    blue = ((a[..., 2] - a[..., 0]) > 45) & ((a[..., 2] - a[..., 1]) > 22) & (a[..., 2] > 100)
    lab2, _ = ndimage.label(blue); e2 = np.unique(lab2[-1]); desk = np.isin(lab2, e2[e2 != 0])
    # holes of wall colour enclosed by an arm (the gap between a raised arm and the head) are wall too
    lab3, n3 = ndimage.label(near & ~wall)
    if n3:
        sizes = ndimage.sum(near, lab3, index=np.arange(1, n3 + 1)); dist = ndimage.mean(np.abs(a - bg).sum(axis=2), lab3, index=np.arange(1, n3 + 1))
        for i in range(1, n3 + 1):
            if sizes[i - 1] >= 500 and dist[i - 1] < tol * 0.5: wall |= lab3 == i
    m = ~(wall | desk); m = ndimage.binary_opening(m, iterations=1)
    lab4, n4 = ndimage.label(m)
    if n4 > 1:
        sizes = ndimage.sum(m, lab4, index=np.arange(1, n4 + 1)); keep = [i + 1 for i, sz in enumerate(sizes) if sz >= max(900, 0.02 * sizes.max())]
        m = np.isin(lab4, keep)
    return m


def to_sprite(path, grid, colors=22):
    """a pose picture -> Sprite in the base sprite's coordinates: (sprite, x0, y0), the sprite's top-left in base coordinates"""
    rgb = np.asarray(Image.open(path).convert('RGB')); mask = pose_mask(rgb)
    ox, oy = grid['offset']; cx0, cy0 = grid['crop'][:2]
    spr, alpha, centers, _ = PX.pixelize(rgb, CELL, colors=colors, mask=mask, origin=(ox - CELL, oy - CELL), crop=False, line_colors=2)
    pal = [rgb2hex(c) for c in PX.oklab_to_srgb(centers)]; idx = np.where(alpha, spr, -1).astype(np.int16)
    ys, xs = np.where(alpha); y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    # stage cell (gx, gy) = base cell + (PAD_X, PAD_TOP) / CELL; base sprite pixel = base cell - crop
    return Sprite(idx[y0:y1, x0:x1], pal), int(x0 - PAD_X // CELL - cx0), int(y0 - PAD_TOP // CELL - cy0)


def snap(spr, master):
    """every colour to the nearest one of the figure's palette or the prop colours"""
    lab_m = PX.srgb_to_oklab(np.array([hex2rgb(c) for c in master], dtype=np.float64))
    lab_s = PX.srgb_to_oklab(np.array([hex2rgb(c) for c in spr.pal], dtype=np.float64))
    near = ((lab_s[:, None, :] - lab_m[None, :, :]) ** 2).sum(axis=2).argmin(axis=1)
    out = -np.ones_like(spr.idx); pal = []
    for i in range(len(spr.pal)):
        col = master[near[i]]
        if col not in pal: pal.append(col)
        out[spr.idx == i] = pal.index(col)
    return Sprite(out, pal)


def place(spr, x0, y0, shape):
    """the sprite on a canvas big enough for it and for the base (shape = base h, w): returns canvas Sprite and its (ox, oy) in base coordinates"""
    bh, bw = shape; ax0, ay0 = min(0, x0), min(0, y0); ax1, ay1 = max(bw, x0 + spr.w), max(bh, y0 + spr.h)
    canvas = -np.ones((ay1 - ay0, ax1 - ax0), dtype=np.int16); canvas[y0 - ay0:y0 - ay0 + spr.h, x0 - ax0:x0 - ax0 + spr.w] = spr.idx
    return Sprite(canvas, list(spr.pal)), ax0, ay0


def dark(spr):
    lum = np.array([0.2126 * r + 0.7152 * g + 0.0722 * b for r, g, b in (hex2rgb(c) for c in spr.pal)] + [255.0])
    return (lum[spr.idx] < 70) & (spr.idx >= 0)


def align(pose, ox, oy, base, head_mask, reach=5):
    """how far the pose's head sits from the base's: the (dx, dy) that makes dark-on-dark and light-on-light agree best over the head"""
    bd = dark(base); ys, xs = np.where(head_mask); best = (-1, 0, 0); pd = dark(pose); pa = pose.idx >= 0
    for dy in range(-reach, reach + 1):
        for dx in range(-reach, reach + 1):
            py, px = ys - oy + dy, xs - ox + dx
            ok = (py >= 0) & (py < pose.h) & (px >= 0) & (px < pose.w)
            score = int((pa[py[ok], px[ok]] & (pd[py[ok], px[ok]] == bd[ys[ok], xs[ok]])).sum())
            if score > best[0]: best = (score, dx, dy)
    return best[1], best[2], best[0] / max(1, len(ys))


def split(pose, ox, oy, head_mask, jaw_rows, front_box=None, hair=None, neck=None, front_mode='all', base_head=None, chest=None, limb=None):
    """body = the pose without its head; front = what must be drawn over the base head (inside front_box, base coordinates).
    The head is removed with a little margin above and beside it (the redrawn hair is never exactly the base's), but not
    below the jaw, where the neck has to meet the base head."""
    H = np.zeros(pose.idx.shape, dtype=bool); hy, hx = np.where(head_mask)
    py, px = hy - oy, hx - ox; ok = (py >= 0) & (py < pose.h) & (px >= 0) & (px < pose.w); H[py[ok], px[ok]] = True
    grown = ndimage.binary_dilation(H, structure=np.ones((3, 3), bool), iterations=2)
    below = np.zeros_like(H)
    for x, jy in jaw_rows.items():
        cx = x - ox
        if 0 <= cx < pose.w: below[max(0, jy + 1 - oy):, cx] = True
    remove = H | (grown & ~below)
    if hair is not None:                                             # long hair: its colours go wherever they are (the base head brings its own)
        hair_px = np.isin(pose.idx, [i for i, c in enumerate(pose.pal) if c in hair])
        hair_px[max(0, 46 - oy):, max(0, 19 - ox):max(0, 34 - ox)] = False          # not the necklace
        ring = ndimage.binary_dilation(hair_px, structure=np.ones((3, 3), bool)) & dark(pose) & ~ndimage.binary_erosion(dark(pose), structure=np.ones((3, 3), bool), iterations=1)
        remove |= hair_px | (ring & grown)
    front = None
    if front_box:
        x0, y0, x1, y1 = front_box; fm = np.zeros_like(H); fm[max(0, y0 - oy):max(0, y1 + 1 - oy), max(0, x0 - ox):max(0, x1 + 1 - ox)] = True
        if front_mode == 'props':                                    # only what is made of prop colours (a mug, a bottle) and its outline
            prop = np.isin(pose.idx, [i for i, c in enumerate(pose.pal) if c in PROPS])
            fm &= prop | (ndimage.binary_dilation(prop, structure=np.ones((3, 3), bool)) & dark(pose))
        elif front_mode == 'arm':                                      # a hand at the face: only the skin joined to an arm coming up from below the box
            skin = np.zeros(pose.idx.shape, bool)
            lab_p = PX.srgb_to_oklab(np.array([hex2rgb(c) for c in pose.pal], dtype=np.float64))
            for i, (L, a_, b_) in enumerate(lab_p):
                if L > 0.55 and a_ > 0.02 and b_ > 0.02: skin |= pose.idx == i
            lab, n = ndimage.label(skin); bottom = max(0, y1 + 1 - oy); arm = np.zeros_like(H)
            for i in range(1, n + 1):
                comp = lab == i
                if (comp & fm).any() and comp[bottom:, :].sum() >= 6: arm |= comp
            fm &= arm | (ndimage.binary_dilation(arm, structure=np.ones((3, 3), bool)) & dark(pose))
        elif front_mode == 'limb' and limb is not None:                # a hand or sleeve over long hair: skin, cloth and props, with their outline
            part = np.isin(pose.idx, [i for i, c in enumerate(pose.pal) if c in limb])
            fm &= part | (ndimage.binary_dilation(part, structure=np.ones((3, 3), bool)) & dark(pose))
        elif front_mode == 'diff' and base_head is not None:         # what the pose draws differently from the base head there (a hand over hair)
            lab_p = PX.srgb_to_oklab(np.array([hex2rgb(c) for c in pose.pal], dtype=np.float64)); lab_b = PX.srgb_to_oklab(np.array([hex2rgb(c) for c in base_head.pal], dtype=np.float64))
            differ = np.zeros_like(H)
            ys, xs = np.where(fm & (pose.idx >= 0))
            for y, x in zip(ys, xs):
                by, bx = y + oy, x + ox
                if not (0 <= by < base_head.h and 0 <= bx < base_head.w) or base_head.idx[by, bx] < 0: differ[y, x] = True; continue
                if ((lab_p[pose.idx[y, x]] - lab_b[base_head.idx[by, bx]]) ** 2).sum() > 0.08 ** 2: differ[y, x] = True
            lab_d, n_d = ndimage.label(differ)
            if n_d:
                sizes = ndimage.sum(differ, lab_d, index=np.arange(1, n_d + 1)); differ = np.isin(lab_d, [i + 1 for i, sz in enumerate(sizes) if sz >= 4])
            fm &= differ
        f = pose.copy(); f.idx[~(fm & (pose.idx >= 0))] = -1; front = f
    body = pose.copy(); body.idx[remove] = -1
    if hair is not None:
        # where the redrawn hair lay on the clothes, the base hair does not always cover: fill those holes from the
        # nearest clothes, but only inside the figure (holes with figure pixels left, right and below)
        holes = remove & ~H & (pose.idx >= 0)
        solid = body.idx >= 0
        left = np.maximum.accumulate(solid, axis=1); right = np.maximum.accumulate(solid[:, ::-1], axis=1)[:, ::-1]; below = np.maximum.accumulate(solid[::-1], axis=0)[::-1]
        holes &= left & right & below
        if holes.any():
            _, (iy, ix) = ndimage.distance_transform_edt(~solid, return_indices=True)
            body.idx[holes] = body.idx[iy[holes], ix[holes]]
    if chest is not None:                                            # where the pose drew skin and the base wears its top, the top comes back
        cspr, cmask, skin = chest
        ys, xs = np.where(cmask); py, px = ys - oy, xs - ox; ok = (py >= 0) & (py < body.h) & (px >= 0) & (px < body.w)
        for y, x, by, bx in zip(py[ok], px[ok], ys[ok], xs[ok]):
            if body.idx[y, x] >= 0 and body.pal[body.idx[y, x]] in skin: body.idx[y, x] = body.color(cspr.pal[cspr.idx[by, bx]])
    if neck is not None:                                             # the neck under the jaw comes from the base torso, so the head joins without a seam
        nspr, nmask = neck
        ys, xs = np.where(nmask); py, px = ys - oy, xs - ox; ok = (py >= 0) & (py < body.h) & (px >= 0) & (px < body.w)
        hand = limb_in_neck(pose, ox, oy, nmask) if limb is not None else np.zeros(pose.idx.shape, bool)
        for y, x, by, bx in zip(py[ok], px[ok], ys[ok], xs[ok]):
            if hand[y, x]: continue                                  # a hand or forearm reaching the chin stays as drawn
            body.idx[y, x] = body.color(nspr.pal[nspr.idx[by, bx]])
    return body, front


def limb_in_neck(pose, ox, oy, nmask):
    """pixels of the neck area that belong to a limb coming into it from below or the side: skin connected (through skin
    and its outline) to skin well outside the neck area, below the collar"""
    skin = np.zeros(pose.idx.shape, bool)
    lab_p = PX.srgb_to_oklab(np.array([hex2rgb(c) for c in pose.pal], dtype=np.float64))
    for i, (L, a, b) in enumerate(lab_p):
        if L > 0.6 and a > 0.02 and b > 0.02: skin |= pose.idx == i      # warm light colours: skin
    area = np.zeros(pose.idx.shape, bool); ys, xs = np.where(nmask); py, px = ys - oy, xs - ox
    ok = (py >= 0) & (py < pose.h) & (px >= 0) & (px < pose.w); area[py[ok], px[ok]] = True
    grown = ndimage.binary_dilation(area, structure=np.ones((3, 3), bool), iterations=3)
    lab, n = ndimage.label(skin, structure=np.ones((3, 3), bool)); out = np.zeros(pose.idx.shape, bool)
    bottom = int(py[ok].max()) + 1 if ok.any() else pose.h
    for i in range(1, n + 1):
        comp = lab == i
        if not (comp & area).any(): continue
        outside = comp & ~grown
        if outside[bottom:, :].sum() >= 12: out |= comp & area             # it reaches down past the collar: an arm, not a neck
    return out


def compose(body, front, ox, oy, head, base_shape, wall=(233, 223, 204), desk_row=None, zoom=5):
    """a look at the pose as the scene will draw it: body, the base head over it, the front part over that"""
    bh, bw = base_shape; x0, y0 = min(0, ox), min(0, oy); x1, y1 = max(bw, ox + body.w), max(bh, oy + body.h)
    im = Image.new('RGBA', (x1 - x0, y1 - y0), wall + (255,))
    im.alpha_composite(body.image(), (ox - x0, oy - y0))
    if desk_row is not None:
        d = Image.new('RGBA', (x1 - x0, max(1, y1 - y0 - (desk_row - y0))), (107, 74, 48, 255)); im.alpha_composite(d, (0, desk_row - y0))
        cut = body.copy(); cut.idx[:max(0, desk_row - oy), :] = -1; im.alpha_composite(cut.image(), (ox - x0, oy - y0))      # hands lie on the desk
    im.alpha_composite(head.image(), (-x0, -y0))
    if front is not None: im.alpha_composite(front.image(), (ox - x0, oy - y0))
    return im.resize((im.width * zoom, im.height * zoom), Image.NEAREST)
