#!/usr/bin/env python3
"""
Nutrimatic portrait toolkit - pixelize.py
Version 2.1.0

Created: 2026-10-02 - Turn a picked candidate (or a photo) into a clean 16-colour sprite (v1.0.0)
Modified: 2026-10-02 - Rewritten after the first real run. The generated pictures look like pixel art but are not on a
  grid, and a plain downscale turned eyes, glasses and mouths into blobs or dropped them. Now two layers: fills by
  majority vote, thin strokes found by black-hat and thinned to one pixel. Cut-out by flood fill (no rembg), palette by
  k-means in OKLab. Needs numpy, scipy, pillow (v2.0.0)
Modified: 2026-10-02 - pixelize() can take a ready mask and a fixed grid origin and return the uncropped grid, so a set
  of pose pictures lands on one shared grid (tools/desk/pose_sprites.py) (v2.1.0)

A generated portrait on a flat background -> a true low-resolution sprite. The generated picture looks like pixel art
but is not on a grid, so it is resampled, in two layers that are treated differently:

  fills   the flat colour areas: palette by k-means in OKLab, then a majority vote per sprite pixel
  lines   thin dark strokes (outlines, glasses frames, eyelids, the mouth): found with a morphological black-hat, then
          reduced to their coverage per sprite pixel and thinned to one pixel wide, so they stay connected instead of
          dissolving (what a plain majority vote does) or turning into blobs (what boosting dark colours does)
  lights  thin light details (eye whites, teeth, a necklace) the same way, without thinning

Then: lone pixels removed, a continuous outline around the silhouette, the palette cut to the colours actually used.
Writes <out>-1x.png (the sprite, transparent), <out>-<zoom>x.png (to look at) and <out>.json (palette, grid).
"""
import argparse, json, sys
import numpy as np
from PIL import Image
from scipy import ndimage


# ---------- colour: sRGB <-> OKLab ----------
def srgb_to_oklab(rgb):
    c = np.asarray(rgb, dtype=np.float64) / 255.0
    lin = np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    l = 0.4122214708 * lin[..., 0] + 0.5363325363 * lin[..., 1] + 0.0514459929 * lin[..., 2]
    m = 0.2119034982 * lin[..., 0] + 0.6806995451 * lin[..., 1] + 0.1073969566 * lin[..., 2]
    s = 0.0883024619 * lin[..., 0] + 0.2817188376 * lin[..., 1] + 0.6299787005 * lin[..., 2]
    l, m, s = np.cbrt(l), np.cbrt(m), np.cbrt(s)
    return np.stack([0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s,
                     1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s,
                     0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s], axis=-1)


def oklab_to_srgb(lab):
    L, a, b = lab[..., 0], lab[..., 1], lab[..., 2]
    l = (L + 0.3963377774 * a + 0.2158037573 * b) ** 3
    m = (L - 0.1055613458 * a - 0.0638541728 * b) ** 3
    s = (L - 0.0894841775 * a - 1.2914855480 * b) ** 3
    lin = np.clip(np.stack([4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
                            -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
                            -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s], axis=-1), 0, 1)
    c = np.where(lin <= 0.0031308, lin * 12.92, 1.055 * lin ** (1 / 2.4) - 0.055)
    return np.clip(np.round(c * 255), 0, 255).astype(np.uint8)


# ---------- cut-out ----------
def subject_mask(rgb, tol=40, min_hole=400):
    """True where the figure is. Background = pixels near the border colour that connect to the top, left or right edge,
    plus enclosed patches of exactly that colour (the gap between an arm and the body)."""
    a = rgb.astype(np.int32)
    border = np.concatenate([a[:4].reshape(-1, 3), a[:, :4].reshape(-1, 3), a[:, -4:].reshape(-1, 3)])
    bg = np.median(border, axis=0)
    near = np.abs(a - bg).sum(axis=2) < tol
    lab, n = ndimage.label(near)
    edge = np.unique(np.concatenate([lab[0], lab[:, 0], lab[:, -1]])); edge = edge[edge != 0]
    bgmask = np.isin(lab, edge)
    if n:
        sizes = ndimage.sum(near, lab, index=np.arange(1, n + 1)); dist = ndimage.mean(np.abs(a - bg).sum(axis=2), lab, index=np.arange(1, n + 1))
        for i in range(1, n + 1):
            if i not in edge and sizes[i - 1] >= min_hole and dist[i - 1] < tol * 0.45: bgmask |= (lab == i)
    mask = ndimage.binary_opening(~bgmask, iterations=1)
    lab2, n2 = ndimage.label(mask)
    if n2 > 1: mask = lab2 == (1 + int(np.argmax(ndimage.sum(mask, lab2, index=np.arange(1, n2 + 1)))))
    return mask, bg


# ---------- palette ----------
def kmeans(points, weights, k, iters=60, seed=0):
    rng = np.random.default_rng(seed)
    centers = [points[np.argmax(weights)]]
    d2 = ((points - centers[0]) ** 2).sum(axis=1)
    for _ in range(1, k):
        p = d2 * weights
        centers.append(points[rng.choice(len(points), p=p / p.sum())]); d2 = np.minimum(d2, ((points - centers[-1]) ** 2).sum(axis=1))
    centers = np.array(centers)
    for _ in range(iters):
        lab = ((points[:, None, :] - centers[None, :, :]) ** 2).sum(axis=2).argmin(axis=1)
        new = np.array([np.average(points[lab == j], axis=0, weights=weights[lab == j]) if (lab == j).any() else centers[j] for j in range(k)])
        if np.allclose(new, centers, atol=1e-5): break
        centers = new
    return centers


def build_palette(rgb, sel, k, seed=0, chroma_gain=4.0):
    """k colours for the pixels in `sel`: clustering runs on the distinct colours with sub-linear weights, so small
    saturated areas (gold, lips, irises) are not swallowed by the large flat ones."""
    px = rgb[sel]
    q = (px >> 3).astype(np.int32); key = (q[:, 0] << 10) | (q[:, 1] << 5) | q[:, 2]
    uniq, inv, counts = np.unique(key, return_inverse=True, return_counts=True)
    sums = np.zeros((len(uniq), 3)); np.add.at(sums, inv, px); lab = srgb_to_oklab(sums / counts[:, None])
    weights = counts ** 0.6 * (1.0 + chroma_gain * np.hypot(lab[:, 1], lab[:, 2]))
    centers = kmeans(lab, weights, k, seed=seed)
    return centers[np.argsort(centers[:, 0])]


def nearest(lab, centers):
    flat = lab.reshape(-1, 3); out = np.empty(len(flat), dtype=np.int16)
    for i in range(0, len(flat), 200000): out[i:i + 200000] = ((flat[i:i + 200000, None, :] - centers[None, :, :]) ** 2).sum(axis=2).argmin(axis=1)
    return out.reshape(lab.shape[:-1])


# ---------- thinning (Zhang-Suen) ----------
def thin(mask):
    m = np.pad(mask.astype(np.uint8), 1)
    while True:
        changed = False
        for step in (0, 1):
            p2, p3, p4, p5, p6, p7, p8, p9 = m[:-2, 1:-1], m[:-2, 2:], m[1:-1, 2:], m[2:, 2:], m[2:, 1:-1], m[2:, :-2], m[1:-1, :-2], m[:-2, :-2]
            nb = [p2, p3, p4, p5, p6, p7, p8, p9]
            b = sum(nb); a = sum(((nb[i] == 0) & (nb[(i + 1) % 8] == 1)).astype(np.uint8) for i in range(8))
            if step == 0: cond = (p2 * p4 * p6 == 0) & (p4 * p6 * p8 == 0)
            else: cond = (p2 * p4 * p8 == 0) & (p2 * p6 * p8 == 0)
            kill = (m[1:-1, 1:-1] == 1) & (b >= 2) & (b <= 6) & (a == 1) & cond
            if kill.any(): m[1:-1, 1:-1][kill] = 0; changed = True
        if not changed: break
    return m[1:-1, 1:-1].astype(bool)


# ---------- the grid ----------
class Grid:
    def __init__(self, shape, cell, ox, oy):
        h, w = shape; self.cell = cell
        self.tw, self.th = int(np.ceil((w - ox) / cell)), int(np.ceil((h - oy) / cell))
        xs = np.clip(((np.arange(w) - ox) / cell).astype(int), 0, self.tw - 1); ys = np.clip(((np.arange(h) - oy) / cell).astype(int), 0, self.th - 1)
        self.id = (ys[:, None] * self.tw + xs[None, :]).ravel(); self.n = self.th * self.tw

    def share(self, sel):                       # fraction of each cell covered by the boolean image `sel`
        return (np.bincount(self.id, weights=sel.ravel().astype(np.float64), minlength=self.n) / np.bincount(self.id, minlength=self.n)).reshape(self.th, self.tw)

    def votes(self, idx, sel, k):               # per cell, how many selected pixels carry each palette index
        out = np.zeros((self.n, k)); s = sel.ravel()
        np.add.at(out, (self.id[s], idx.ravel()[s]), 1); return out.reshape(self.th, self.tw, k)

    def mean(self, lab, sel):                   # per cell, the mean OKLab colour of the selected pixels (nan where none)
        s = sel.ravel(); cnt = np.bincount(self.id[s], minlength=self.n)
        out = np.stack([np.bincount(self.id[s], weights=lab[..., c].ravel()[s], minlength=self.n) for c in range(3)], axis=1) / np.maximum(cnt, 1)[:, None]
        out[cnt == 0] = np.nan; return out.reshape(self.th, self.tw, 3)


def despeckle(spr, alpha, keep, passes=2):
    h, w = spr.shape
    for _ in range(passes):
        out = spr.copy()
        for y in range(h):
            for x in range(w):
                if not alpha[y, x] or keep[y, x]: continue
                nb = [spr[yy, xx] for yy, xx in ((y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)) if 0 <= yy < h and 0 <= xx < w and alpha[yy, xx]]
                if len(nb) >= 3 and spr[y, x] not in nb:
                    vals, cnt = np.unique(nb, return_counts=True); out[y, x] = vals[cnt.argmax()]
        spr = out
    return spr


def pixelize(rgb, cell, colors=15, line_w=0.95, line_t=0.22, light_t=0.34, cover=0.5, tol=40, seed=0, phases=4, outline=True, line_colors=2, verbose=False,
             mask=None, origin=None, crop=True):
    """mask: a ready cut-out (True = figure) instead of the flood fill. origin: (x, y) of the grid's first cell, both <= 0,
    to put several pictures on one grid instead of fitting each. crop=False returns the whole grid, uncropped."""
    if mask is None: mask, bg = subject_mask(rgb, tol)
    else: bg = np.zeros(3)
    lab = srgb_to_oklab(rgb); L = lab[..., 0]
    # thin dark strokes: darker than their surroundings by a clear margin and narrower than about one sprite pixel
    r = max(1, int(round(cell * line_w / 2)))
    yy, xx = np.ogrid[-r:r + 1, -r:r + 1]; disk = (xx * xx + yy * yy) <= r * r
    Lm = np.where(mask, L, 1.0)                                        # the background counts as light, so the silhouette outline is a stroke too
    blackhat = ndimage.grey_closing(Lm, footprint=disk) - Lm
    lines = mask & (blackhat > 0.16) & (L < 0.52)
    Ld = np.where(mask, L, 0.0)
    whitehat = Ld - ndimage.grey_opening(Ld, footprint=disk)
    lights = mask & (whitehat > 0.14) & (L > 0.72) & ~lines
    fills = mask & ~lines
    # palette: fills get most of the budget, strokes share one or two dark colours
    fill_k = colors - line_colors
    pal_fill = build_palette(rgb, fills, fill_k, seed)
    pal_line = build_palette(rgb, lines, line_colors, seed, chroma_gain=1.0) if lines.sum() > 50 else pal_fill[:line_colors]
    centers = np.concatenate([pal_line, pal_fill]); k = len(centers)
    fill_idx = nearest(lab, pal_fill) + line_colors; line_idx = nearest(lab, pal_line)
    best = None
    starts = [(origin[0] + cell, origin[1] + cell)] if origin is not None else [(ox, oy) for oy in np.linspace(0, cell, phases, endpoint=False) for ox in np.linspace(0, cell, phases, endpoint=False)]
    for ox, oy in starts:
        if True:
            g = Grid(mask.shape, cell, ox - cell, oy - cell)
            v = g.votes(fill_idx, fills, k); tot = v.sum(axis=2)
            score = v.max(axis=2).sum() / max(1, tot.sum())            # how cleanly the fills fall into the cells
            if best is None or score > best[0]: best = (score, g, v, ox, oy)
    score, g, v, ox, oy = best
    alpha = g.share(mask) >= cover
    spr = v.argmax(axis=2)
    empty = v.sum(axis=2) == 0                                          # cells that are all stroke: borrow the stroke colour
    lv = g.votes(line_idx, lines, k); lchoice = lv.argmax(axis=2)
    spr = np.where(empty, lchoice, spr)
    # light details
    lshare = g.share(lights); lightv = g.votes(fill_idx, lights, k)
    add_light = alpha & (lshare >= light_t)
    spr = np.where(add_light, lightv.argmax(axis=2), spr)
    # strokes: coverage -> one pixel wide
    cov = g.share(lines)
    cand = alpha & (cov >= line_t)
    solid = cov >= 0.75                                                 # really dark cells stay whatever thinning says
    skel = thin(cand) | (solid & alpha)
    spr = np.where(skel, lchoice, spr)
    keep = skel | add_light
    spr = despeckle(spr, alpha, keep)
    if outline:
        h, w = spr.shape; dark = int(np.argmin(centers[:, 0])); out = spr.copy()
        for y in range(h):
            for x in range(w):
                if alpha[y, x] and any((not (0 <= xx_ < w and 0 <= yy_)) or (yy_ < h and not alpha[yy_, xx_]) for yy_, xx_ in ((y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1))):
                    out[y, x] = dark
        spr = out
    ys, xs = np.where(alpha)
    if crop: y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    else: y0, y1, x0, x1 = 0, alpha.shape[0], 0, alpha.shape[1]
    info = dict(cell=cell, offset=[float(ox), float(oy)], crop=[int(x0), int(y0), int(x1), int(y1)], fit=round(float(score), 3), bg=[int(v_) for v_ in bg])
    if verbose: print("  lines %.1f%% lights %.1f%% of figure, fit %.3f" % (100 * lines.sum() / mask.sum(), 100 * lights.sum() / mask.sum(), score))
    return spr[y0:y1, x0:x1], alpha[y0:y1, x0:x1], centers, info


def save(spr, alpha, centers, out, zoom=8, info=None):
    used = sorted(set(spr[alpha].tolist())); remap = {old: new for new, old in enumerate(used)}
    pal = oklab_to_srgb(centers[used]); idx = np.vectorize(lambda v: remap.get(int(v), 0))(spr)
    img = np.zeros(spr.shape + (4,), dtype=np.uint8); img[..., :3] = pal[idx]; img[..., 3] = np.where(alpha, 255, 0)
    im = Image.fromarray(img, "RGBA"); im.save(out + "-1x.png")
    big = Image.new("RGBA", im.size, (236, 232, 224, 255)); big.alpha_composite(im)
    big.resize((im.width * zoom, im.height * zoom), Image.NEAREST).convert("RGB").save(out + "-%dx.png" % zoom)
    meta = dict(info or {}); meta.update(size=[im.width, im.height], palette=["#%02x%02x%02x" % tuple(int(v) for v in c) for c in pal])
    json.dump(meta, open(out + ".json", "w"), indent=1)
    return im, meta


def main():
    ap = argparse.ArgumentParser(description="A generated portrait on a flat background -> a true low-resolution sprite")
    ap.add_argument("src"); ap.add_argument("--out", required=True)
    ap.add_argument("--cell", type=float, required=True, help="source pixels per sprite pixel (the scene's figures: 12 on a 1024x1280 picture)")
    ap.add_argument("--colors", type=int, default=15); ap.add_argument("--line-colors", type=int, default=2)
    ap.add_argument("--line-w", type=float, default=0.95, help="widest stroke treated as line work, in sprite pixels")
    ap.add_argument("--line-t", type=float, default=0.22, help="share of a sprite pixel a stroke must cover"); ap.add_argument("--light-t", type=float, default=0.34)
    ap.add_argument("--cover", type=float, default=0.5); ap.add_argument("--tol", type=int, default=40); ap.add_argument("--zoom", type=int, default=8)
    ap.add_argument("--no-outline", action="store_true"); ap.add_argument("--seed", type=int, default=0)
    a = ap.parse_args()
    rgb = np.asarray(Image.open(a.src).convert("RGB"))
    spr, alpha, centers, info = pixelize(rgb, a.cell, a.colors, a.line_w, a.line_t, a.light_t, a.cover, a.tol, a.seed, outline=not a.no_outline, line_colors=a.line_colors, verbose=True)
    info["source"] = a.src
    im, meta = save(spr, alpha, centers, a.out, a.zoom, info)
    print("wrote %s-1x.png %dx%d  cell %.2f  colours %d" % (a.out, im.width, im.height, a.cell, len(meta["palette"])))


if __name__ == "__main__": main()
