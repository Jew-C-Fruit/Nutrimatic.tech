#!/usr/bin/env python3
"""
Nutrimatic desk scene - walk_check.py
Version 1.0.0

Created: 2026-10-03 - Pictures for checking Maker's walk before exporting: a contact sheet, a travel strip, an onion skin
  and a 12 fps GIF (docs/animal-walk-cycles.md, "How to check a walk") (v1.0.0)

walk_check.py - render the walk the way the scene plays it, so a sliding paw or a jumping body shows.

  python3 tools/desk/walk_check.py OUTDIR

writes, into OUTDIR:
  walk-contact.png  every frame large, numbered, the paws on the desk named and ticked under it (red near, blue far)
  walk-strip.png    two cycles, one frame per row, each row moved on by the 3 px she travels a frame: a planted paw
                    must stay in the same column from row to row (red ticks mark the paws on the desk)
  walk-onion.png    one cycle drawn over itself at the travel offsets, faintly: planted paws pile up into one sharp paw
  walk.gif          walking across a desk-coloured strip at 12 frames a second (the scene's speed), 4x
  walk-inplace.gif  the cycle on the spot at 12 frames a second, 6x
"""
import os, sys
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import walk_rig as W

BG, DESK, INK, RED = (236, 232, 224), (196, 160, 112), (40, 40, 40), (220, 30, 40)
LABEL = {'RH': 'near hind', 'RF': 'near fore', 'LH': 'far hind', 'LF': 'far fore'}


def walk_frames(blink=False):
    import maker_build as M
    sh = M.sheet(big=True)
    return [sh['walk%d%s' % (i, 'Blink' if blink else '')] for i in range(W.N)]


def contact_sheet(frames, path, z=6, cols=5):
    fw, fh = frames[0].w * z, frames[0].h * z; rows = (len(frames) + cols - 1) // cols
    im = Image.new('RGB', ((fw + 16) * cols + 16, (fh + 48) * rows + 16), BG); d = ImageDraw.Draw(im)
    for i, fr in enumerate(frames):
        x, y = 16 + (i % cols) * (fw + 16), 16 + (i // cols) * (fh + 48)
        a = fr.image().resize((fw, fh), Image.NEAREST); im.paste(a, (x, y + 14), a)
        d.text((x, y), 'frame %d' % i, fill=INK)
        down = [LABEL[leg] for leg in ('RH', 'RF', 'LH', 'LF') if W.contacts(i)[leg][1]]
        d.text((x, y + fh + 18), '%d down: ' % len(down) + ', '.join(down), fill=INK)
        for leg, (heel, on) in W.contacts(i).items():
            if on:
                gx = x + (heel + 3) * z; d.line([(gx, y + 14 + fh + 2), (gx, y + 14 + fh + 10)], fill=RED if W.NEAR[leg] else (120, 120, 200), width=2)
    im.save(path)


def strip(frames, path, z=4, cycles=2):
    n = len(frames) * cycles; fw, fh = frames[0].w, frames[0].h; travel = W.SPEED
    width = (fw + travel * n + 4) * z; rowh = (fh + 4) * z // 2 + 8
    im = Image.new('RGB', (width + 60, rowh * n + 20), BG); d = ImageDraw.Draw(im)
    for i in range(n):
        f = i % len(frames); fr = frames[f]; ox = 50 + (2 + travel * i) * z; oy = 10 + i * rowh
        a = fr.image().resize((fw * z, fh * z), Image.NEAREST).crop((0, fh * z // 2, fw * z, fh * z))
        im.paste(a, (ox, oy), a)
        d.text((4, oy + rowh // 2 - 6), 'f%d' % f, fill=INK)
        for leg, (heel, on) in W.contacts(f).items():
            if on:
                gx = ox + (heel + 3) * z + z // 2; d.line([(gx, oy + rowh - 10), (gx, oy + rowh - 3)], fill=RED if W.NEAR[leg] else (90, 90, 220), width=2)
    im.save(path)


def onion(frames, path, z=6):
    fw, fh = frames[0].w, frames[0].h; travel = W.SPEED; n = len(frames)
    acc = np.zeros(((fh + 4) * z, (fw + travel * n + 4) * z, 3)); cnt = 0
    base = Image.new('RGB', (acc.shape[1], acc.shape[0]), BG)
    for i, fr in enumerate(frames):
        layer = base.copy(); a = fr.image().resize((fw * z, fh * z), Image.NEAREST); layer.paste(a, ((2 + travel * i) * z, 2 * z), a)
        acc += np.asarray(layer, dtype=np.float64); cnt += 1
    Image.fromarray((acc / cnt).astype(np.uint8)).save(path)


def gif(frames, path, z=4, cycles=3, inplace=False):
    fw, fh = frames[0].w, frames[0].h; travel = 0 if inplace else W.SPEED; n = len(frames) * cycles
    width = fw + travel * n + 8; height = fh + 8; out = []
    for i in range(n):
        im = Image.new('RGB', (width, height), BG); d = ImageDraw.Draw(im)
        d.rectangle([0, height - 4, width, height], fill=DESK)
        fr = frames[i % len(frames)].image(); im.paste(fr, (4 + travel * i, height - 4 - fh), fr)
        out.append(im.resize((width * z, height * z), Image.NEAREST))
    # GIF delays are in hundredths of a second: 80, 80, 90 ms averages the scene's 12 frames a second
    out[0].save(path, save_all=True, append_images=out[1:], duration=[(90 if i % 3 == 2 else 80) for i in range(len(out))], loop=0, disposal=1)


def main(outdir):
    os.makedirs(outdir, exist_ok=True)
    fr = walk_frames()
    contact_sheet(fr, os.path.join(outdir, 'walk-contact.png'))
    strip(fr, os.path.join(outdir, 'walk-strip.png'))
    onion(fr, os.path.join(outdir, 'walk-onion.png'))
    gif(fr, os.path.join(outdir, 'walk.gif'))
    gif(fr, os.path.join(outdir, 'walk-inplace.gif'), z=6, cycles=2, inplace=True)
    sizes = {(f.w, f.h) for f in fr}
    print('frames', len(fr), 'sizes', sizes, '->', outdir)


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else '/tmp/maker-walk')
