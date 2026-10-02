#!/usr/bin/env python3
"""
Nutrimatic desk scene - spritekit.py
Version 1.0.0

Created: 2026-10-02 - Indexed sprites: load, edit pixel by pixel, look at the result with a ruler (v1.0.0)

spritekit.py - small helpers for finishing sprites by hand, with a look after every change.

A sprite here is an indexed image: a 2-D array of palette indices (-1 = transparent) plus a list of '#rrggbb' colours.
  load(png)                      -> Sprite (palette taken from the PNG's own colours, dark to light)
  spr.put(x, y, c)               one pixel; c is a palette index, a '#rrggbb' (added to the palette if new) or None/'.' = clear
  spr.rows(x, y, ["..aab", ...], key)   a small pixel map; key maps letters to colours, '.' leaves the pixel alone, '_' clears it
  spr.fill(x0, y0, x1, y1, c)    a filled rectangle (inclusive)
  spr.view(path, zoom, box)      zoomed picture with a ruler, so coordinates can be read off it
  spr.save(png)
"""
import numpy as np
from PIL import Image, ImageDraw

def hex2rgb(h): h = h.lstrip('#'); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
def rgb2hex(c): return '#%02x%02x%02x' % tuple(int(v) for v in c[:3])
def lum(c): r, g, b = hex2rgb(c); return 0.2126 * r + 0.7152 * g + 0.0722 * b

class Sprite:
    def __init__(self, idx, pal): self.idx = idx.astype(np.int16); self.pal = list(pal)
    @property
    def w(self): return self.idx.shape[1]
    @property
    def h(self): return self.idx.shape[0]
    def copy(self): return Sprite(self.idx.copy(), list(self.pal))
    def color(self, c):
        if c is None or c == '.' or c == '_': return -1
        if isinstance(c, (int, np.integer)): return int(c)
        c = c.lower()
        if c not in self.pal: self.pal.append(c)
        return self.pal.index(c)
    def put(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h: self.idx[y, x] = self.color(c)
    def get(self, x, y): i = self.idx[y, x]; return None if i < 0 else self.pal[i]
    def fill(self, x0, y0, x1, y1, c): self.idx[max(0, y0):y1 + 1, max(0, x0):x1 + 1] = self.color(c)
    def rows(self, x, y, rows, key):
        for r, row in enumerate(rows):
            for i, ch in enumerate(row):
                if ch == '.': continue
                self.put(x + i, y + r, None if ch == '_' else key[ch])
    def replace(self, a, b, box=None):
        ia, ib = self.color(a), self.color(b); x0, y0, x1, y1 = box or (0, 0, self.w - 1, self.h - 1)
        sub = self.idx[y0:y1 + 1, x0:x1 + 1]; sub[sub == ia] = ib
    def crop(self, x0, y0, x1, y1): return Sprite(self.idx[y0:y1 + 1, x0:x1 + 1].copy(), list(self.pal))
    def pad(self, left=0, top=0, right=0, bottom=0):
        out = -np.ones((self.h + top + bottom, self.w + left + right), dtype=np.int16); out[top:top + self.h, left:left + self.w] = self.idx; return Sprite(out, list(self.pal))
    def image(self):
        rgba = np.zeros((self.h, self.w, 4), dtype=np.uint8); pal = np.array([hex2rgb(c) for c in self.pal], dtype=np.uint8)
        m = self.idx >= 0; rgba[m, :3] = pal[self.idx[m]]; rgba[m, 3] = 255; return Image.fromarray(rgba, 'RGBA')
    def save(self, path): self.image().save(path)
    def used(self): return sorted(set(self.idx[self.idx >= 0].tolist()))
    def compact(self):
        used = self.used(); m = {o: n for n, o in enumerate(used)}; out = self.idx.copy()
        for o, n in m.items(): out[self.idx == o] = n
        self.idx = out; self.pal = [self.pal[o] for o in used]; return self
    def view(self, path, zoom=12, box=None, bg=(236, 232, 224), grid=True, ruler=True):
        x0, y0, x1, y1 = box or (0, 0, self.w - 1, self.h - 1)
        sub = self.crop(x0, y0, x1, y1).image(); w, h = sub.size; m = 26 if ruler else 0
        canvas = Image.new('RGB', (w * zoom + m, h * zoom + m), (255, 255, 255))
        tile = Image.new('RGBA', (w, h), bg + (255,)); tile.alpha_composite(sub)
        canvas.paste(tile.convert('RGB').resize((w * zoom, h * zoom), Image.NEAREST), (m, m))
        d = ImageDraw.Draw(canvas)
        if grid and zoom >= 8:
            for i in range(w + 1):
                if (x0 + i) % 5 == 0: d.line([(m + i * zoom, m), (m + i * zoom, m + h * zoom)], fill=(120, 170, 255) if (x0 + i) % 10 else (40, 90, 220), width=1)
            for j in range(h + 1):
                if (y0 + j) % 5 == 0: d.line([(m, m + j * zoom), (m + w * zoom, m + j * zoom)], fill=(120, 170, 255) if (y0 + j) % 10 else (40, 90, 220), width=1)
        if ruler:
            for i in range(w):
                if (x0 + i) % 5 == 0: d.text((m + i * zoom + 1, 2), str(x0 + i), fill=(0, 0, 0))
            for j in range(h):
                if (y0 + j) % 5 == 0: d.text((1, m + j * zoom), str(y0 + j), fill=(0, 0, 0))
        canvas.save(path); return path

def load(path):
    im = Image.open(path).convert('RGBA'); a = np.asarray(im)
    cols = sorted({rgb2hex(c) for c in a[a[..., 3] > 0][:, :3].reshape(-1, 3)}, key=lum)
    idx = -np.ones(a.shape[:2], dtype=np.int16)
    for i, c in enumerate(cols): idx[(a[..., 3] > 0) & (a[..., :3] == np.array(hex2rgb(c), dtype=np.uint8)).all(axis=2)] = i
    return Sprite(idx, cols)

def swatches(spr, path, cell=34):
    im = Image.new('RGB', (cell * len(spr.pal), cell + 14), (255, 255, 255)); d = ImageDraw.Draw(im)
    for i, c in enumerate(spr.pal): d.rectangle([i * cell, 0, (i + 1) * cell - 2, cell - 2], fill=hex2rgb(c)); d.text((i * cell + 2, cell), str(i), fill=(0, 0, 0))
    im.save(path); return path
