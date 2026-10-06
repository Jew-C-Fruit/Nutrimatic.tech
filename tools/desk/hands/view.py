#!/usr/bin/env python3
"""
Nutrimatic desk scene - hands/view.py
Version 1.0.0

Created: 2026-10-06 - A candidate hand in the live scene (the hand library, to-do round 31): builds the pose with the
  candidate drawn in, patches it into the scene (D.patchPoses), captures exact frames in the wide and phone layouts by
  day and at night, and writes the views a drawer, an auditor and Cole look at (v1.0.0)

python3 view.py CANDIDATE.json OUTDIR [--slot NAME] [--no-night] [--frames N --step S]
python3 view.py --current SLOT OUTDIR            (the hand as it is now, for comparison)

Writes into OUTDIR:
  scene-wide.png / scene-phone.png      the whole canvas, exact pixels (360x160 / 240x160), day
  ctx-2x.png                            the figure's area at 2x (desktop size), day and night side by side
  ctx-phone.png                         the same in the phone layout at 1.5x (about what a phone shows)
  hand-8x.png                           the slot's view box at 8x with a ruler (sprite coordinates)
  frames-2x.png                         every captured frame at 2x (motion), when frames > 1
  patch.json                            the pose layers sent to the scene
Needs the site served at http://127.0.0.1:8765/ (python3 -m http.server 8765 in the repo root).
"""
import os, sys, json, subprocess, argparse
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
from hands import core, slots as SL            # noqa: E402
from hands.ruler import ruler                  # noqa: E402

FIG_X = {'wide': {'cole': 124, 'ilinca': 226}, 'narrow': {'cole': 60, 'ilinca': 150}}
ART = {'cole': (37, 88), 'ilinca': (28, 84)}   # centre column, desk row
DESK_Y = 134


def origin(who, layout):
    cx, desk = ART[who]; return FIG_X[layout][who] - cx, DESK_Y - desk


def capture(shots, out, base='http://127.0.0.1:8765/how-it-works.html'):
    job = os.path.join(out, 'job.json'); json.dump({'base': base, 'out': out, 'shots': shots}, open(job, 'w'))
    subprocess.check_call(['node', os.path.join(HERE, 'capture.mjs'), job])


def crop_figure(im, who, layout, box):
    """the slot's view box (sprite coordinates) cut from a capture"""
    ox, oy = origin(who, layout); x0, y0, x1, y1 = box
    return im.crop((max(0, x0 + ox), max(0, y0 + oy), min(im.width, x1 + ox), min(im.height, y1 + oy)))


def label(im, text):
    can = Image.new('RGB', (im.width, im.height + 14), 'white'); can.paste(im.convert('RGB'), (0, 14))
    ImageDraw.Draw(can).text((2, 1), text, fill=(0, 0, 0)); return can


def row(images, gap=8):
    W = sum(i.width for i in images) + gap * (len(images) - 1); H = max(i.height for i in images)
    can = Image.new('RGB', (W, H), 'white'); x = 0
    for i in images: can.paste(i, (x, 0)); x += i.width + gap
    return can


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('candidate'); ap.add_argument('out'); ap.add_argument('--slot'); ap.add_argument('--current', action='store_true')
    ap.add_argument('--no-night', action='store_true'); ap.add_argument('--frames', type=int, default=1); ap.add_argument('--step', type=int, default=1)
    a = ap.parse_args(); os.makedirs(a.out, exist_ok=True)
    if a.current:
        slot_name = a.candidate; slot = SL.SLOTS[slot_name]; cand = None
    else:
        cand = core.load_candidate(a.candidate); slot_name = a.slot or cand.get('slot'); slot = SL.SLOTS[slot_name]
    who, pose = slot['who'], slot['pose']
    names = sorted(core.needed(who, pose) | set(slot.get('dependents', [])) | set(slot.get('frames', {})))
    if cand is None: built = core.build(who, poses=[pose] + slot.get('dependents', []))
    else: built = core.build_candidate(who, pose, dict(cand, also=slot.get('dependents', [])))
    names = [n for n in names if n in built]
    patch = {} if cand is None else {who: core.patch(who, built, names)}
    json.dump(patch, open(os.path.join(a.out, 'patch.json'), 'w'))
    shots = [dict(name='day', patch=patch, widths=[1200, 390], hour=13, code=slot['code'], frames=a.frames, step=a.step)]
    if not a.no_night: shots.append(dict(name='night', patch=patch, widths=[1200, 390], hour=23, code=slot['code'], frames=1))
    capture(shots, a.out)
    day_w = Image.open(os.path.join(a.out, 'day-w1200-00.png')); day_n = Image.open(os.path.join(a.out, 'day-w390-00.png'))
    day_w.save(os.path.join(a.out, 'scene-wide.png')); day_n.save(os.path.join(a.out, 'scene-phone.png'))
    big = (slot['view'][0] - 14, slot['view'][1] - 14, slot['view'][2] + 14, slot['view'][3] + 6)
    ctx = [label(crop_figure(day_w, who, 'wide', big).resize(((big[2] - big[0]) * 2, (big[3] - big[1]) * 2), Image.NEAREST), 'day, 2x')]
    if not a.no_night:
        night_w = Image.open(os.path.join(a.out, 'night-w1200-00.png'))
        ctx.append(label(crop_figure(night_w, who, 'wide', big).resize(((big[2] - big[0]) * 2, (big[3] - big[1]) * 2), Image.NEAREST), 'night, 2x'))
    row(ctx).save(os.path.join(a.out, 'ctx-2x.png'))
    ph = crop_figure(day_n, who, 'narrow', big); ph.resize((int(ph.width * 1.5), int(ph.height * 1.5)), Image.NEAREST).save(os.path.join(a.out, 'ctx-phone.png'))
    ruler(crop_figure(day_w, who, 'wide', slot['view']), slot['view'][0], slot['view'][1], 8, os.path.join(a.out, 'hand-8x.png'))
    if a.frames > 1:
        fr = [label(crop_figure(Image.open(os.path.join(a.out, 'day-w1200-%02d.png' % i)), who, 'wide', big).resize(((big[2] - big[0]) * 2, (big[3] - big[1]) * 2), Image.NEAREST), str(i)) for i in range(a.frames)]
        row(fr).save(os.path.join(a.out, 'frames-2x.png'))
    print(a.out, 'poses', names)


if __name__ == '__main__': main()
