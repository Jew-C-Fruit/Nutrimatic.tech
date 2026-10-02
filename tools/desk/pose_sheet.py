#!/usr/bin/env python3
"""
Nutrimatic desk scene - pose_sheet.py
Version 1.0.0

Created: 2026-10-02 - A picking sheet for generated poses, each shown as the scene will draw it (v1.0.0)

pose_sheet.py who [pose ...] - run in the folder that holds the generated candidates (out/<who>-<pose>/cand-*.png) and
the stage's json (<who>-stage.json, with "desk_y"). Every candidate is reduced, put under the base head and composed
over a desk, in one sheet per figure (rows = poses, columns = candidates). The label gives the head alignment and how
far the model moved the desk line (source pixels; near 0 is what you want).
"""
import sys, os, glob, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from PIL import Image, ImageDraw
import pose_sprites as PS, poses as P
from characters import CHARACTERS, layers

def desk_line(path, stage_desk_y):
    a = np.asarray(Image.open(path).convert('RGB')).astype(int)
    blue = ((a[..., 2] - a[..., 0]) > 45) & ((a[..., 2] - a[..., 1]) > 22) & (a[..., 2] > 100)
    rows = np.where(blue.mean(axis=1) > 0.5)[0]
    return int(rows[0] - stage_desk_y) if len(rows) else None

def main(who, only):
    c = CHARACTERS[who]; grid = json.load(open(P.GRIDS[who])); base = c.blank(); _, _, hm = layers(c); jaw = P.jaw_rows(c, base)
    full = c.full(); head = full.copy(); head.idx[~hm] = -1; master = P.master_palette(c); hair = set(c.HAIR) if hasattr(c, 'HAIR') else None
    stage = json.load(open('%s-stage.json' % who)); rows = []
    for d in sorted(glob.glob('out/%s-*/' % who)):
        pose = d.rstrip('/').split('-', 1)[1]
        if only and pose not in only: continue
        cells = []
        for f in sorted(glob.glob(d + 'cand-*.png')):
            spr, x0, y0 = PS.to_sprite(f, grid); spr = PS.snap(spr, master); dx, dy, sc = PS.align(spr, x0, y0, base, hm); x0 -= dx; y0 -= dy
            body, front = PS.split(spr, x0, y0, hm, jaw, None, hair)
            im = PS.compose(body, front, x0, y0, head, base.idx.shape, desk_row=c.desk, zoom=3)
            cells.append((im, '%s %s  al %d,%d  desk %s' % (pose, os.path.basename(f)[5:-4], dx, dy, desk_line(f, stage['desk_y']))))
        if cells: rows.append(cells)
    if not rows: print('nothing'); return
    cw = max(im.width for r in rows for im, _ in r); ch = max(im.height for r in rows for im, _ in r) + 16; cols = max(len(r) for r in rows)
    sheet = Image.new('RGB', (cols * (cw + 6), len(rows) * (ch + 6)), (255, 255, 255)); d = ImageDraw.Draw(sheet)
    for j, r in enumerate(rows):
        for i, (im, label) in enumerate(r):
            x, y = i * (cw + 6), j * (ch + 6); sheet.paste(im.convert('RGB'), (x, y + 16 + (ch - 16 - im.height))); d.text((x + 2, y + 2), label, fill=(0, 0, 0))
    name = 'out/sheet-%s%s.png' % (who, ('-' + '-'.join(only)) if only else ''); sheet.save(name); print(name, sheet.size)

if __name__ == '__main__': main(sys.argv[1], sys.argv[2:])
