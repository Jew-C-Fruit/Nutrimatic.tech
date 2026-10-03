#!/usr/bin/env python3
"""
Nutrimatic desk scene - docs/make_walk_refs.py
Version 1.0.0

Created: 2026-10-03 - The pictures of animal-walk-cycles.md: Muybridge's cat (plate 716) and tigress (plate 729) cut
  from the National Gallery of Art's open-access (CC0) scans and labelled, the gait diagram of Maker's walk, her frames
  with each leg's key pose named, each leg's ten poses on their own, and a travel strip (v1.0.0)

make_walk_refs.py - rebuild docs/walk-refs/*.png.

  python3 tools/desk/docs/make_walk_refs.py [CACHE_DIR]

The two scans are fetched once from the NGA's IIIF server into CACHE_DIR (default /tmp/walk-refs-cache); only the cut
and labelled sheets go into the repo. Needs pillow, numpy (and, for Maker's sheets, what maker_build.py needs).

Sources (public domain photographs, scans released by the NGA under CC0):
  Eadweard Muybridge, Animal Locomotion (1887), plate 716 "Cat; walking; change to galloping", NGA 2019.150.9
  Eadweard Muybridge, Animal Locomotion (1887), plate 729 "Tigress walking", NGA 2014.79.655
"""
import os, sys, urllib.request
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'walk-refs')
sys.path.insert(0, os.path.join(HERE, '..'))
SCANS = {'716': 'https://api.nga.gov/iiif/ef95af44-7a4f-4d94-8639-fae0c309d3dc/full/full/0/default.jpg',
         '729': 'https://api.nga.gov/iiif/426ac150-b4ec-47ff-921d-bf86b53e4c0a/full/full/0/default.jpg'}
PAPER, INK, MUTED = (250, 249, 246), (20, 20, 20), (95, 94, 90)
NEAR, FAR = (235, 104, 52), (42, 120, 214)          # near legs orange, far legs blue (always with a text tag)


def font(size, bold=False):
    for name in (('DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf'), ('LiberationSans-Bold.ttf' if bold else 'LiberationSans-Regular.ttf')):
        for d in ('/usr/share/fonts/truetype/dejavu', '/usr/share/fonts/truetype/liberation'):
            p = os.path.join(d, name)
            if os.path.exists(p): return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def scan(plate, cache):
    os.makedirs(cache, exist_ok=True); path = os.path.join(cache, 'muybridge-%s.jpg' % plate)
    if not os.path.exists(path):
        req = urllib.request.Request(SCANS[plate], headers={'User-Agent': 'nutrimatic-walk-refs/1.0'})
        open(path, 'wb').write(urllib.request.urlopen(req, timeout=180).read())
    return Image.open(path).convert('RGB')


# ---------- plate 716, first row: a cat walking (frames 1-6) ----------
# Each frame's box in the 4096 px wide scan, and per frame the paws: (leg, x, y in the frame box, on the ground?).
# Legs: the foreleg drawn in front with the stripes is the near one, the dark one behind it the far one (it is hidden
# behind the near one where they cross). Which hind leg is nearer cannot be seen at this size; the labels follow the
# lateral sequence measured in walking cats (a hind paw lands, then the fore paw on the same side).
CAT_FRAMES = [(51, 57, 707, 507), (715, 57, 1375, 507), (1387, 57, 2045, 507), (2057, 57, 2715, 507), (2727, 57, 3387, 507), (3397, 57, 4051, 507)]
CAT_PAWS = [
    [('Hf', 146, 376, True), ('Hn', 278, 381, True), ('Ff', 460, 374, True), ('Fn', 486, 357, False)],
    [('Hf', 148, 375, True), ('Hn', 287, 381, True), ('Ff', 465, 374, True), ('Fn', 536, 365, False)],
    [('Hf', 111, 369, True), ('Hn', 248, 378, True), ('Ff', 418, 373, True), ('Fn', 544, 368, True)],
    [('Hf', 128, 375, True), ('Hn', 255, 383, True), ('Ff', 422, 376, True), ('Fn', 578, 381, True)],
    [('Hf', 153, 366, False), ('Hn', 240, 385, True), ('Ff', 410, 378, True), ('Fn', 572, 383, True)],
    [('Hn', 245, 383, True), ('Ff', 423, 376, True), ('Fn', 567, 382, True)],
]
CAT_NOTES = ['near fore swinging, paw folded back', 'near fore reaching', 'near fore lands: four paws down',
             'far hind on its toes', 'far hind lifts off', 'far hind swings forward (hidden)']
NAMES = {'Hn': 'near hind', 'Fn': 'near fore', 'Hf': 'far hind', 'Ff': 'far fore'}


def marker(d, x, y, leg, down, f):
    col = NEAR if leg.endswith('n') else FAR; r = 9
    if down: d.ellipse([x - r, y - r, x + r, y + r], fill=col, outline=(255, 255, 255), width=2)
    else:
        for a in range(0, 360, 40): d.arc([x - r, y - r, x + r, y + r], a, a + 22, fill=col, width=3)
    d.text((x - 10, y - 30 if leg.startswith('F') else y + 11), leg, fill=col, font=f, stroke_width=2, stroke_fill=(255, 255, 255))


def cat_sheet(cache):
    im = scan('716', cache); sc = 0.56; f, fb, fs = font(15), font(17, True), font(13)
    cells = []
    for i, (box, paws) in enumerate(zip(CAT_FRAMES, CAT_PAWS)):
        fr = im.crop(box).crop((30, 30, 656, 445)); fr = ImageOps.autocontrast(fr.convert('L'), cutoff=0.5).convert('RGB')
        fr = fr.resize((int(fr.width * sc), int(fr.height * sc)), Image.LANCZOS); d = ImageDraw.Draw(fr)
        for leg, x, y, down in paws: marker(d, (x - 30) * sc, (y - 30) * sc, leg, down, fs)
        cells.append((fr, i, paws))
    cw, ch = cells[0][0].size; pad = 18; W = pad + 3 * (cw + pad); H = 64 + 2 * (ch + 74) + 150
    out = Image.new('RGB', (W, H), PAPER); d = ImageDraw.Draw(out)
    d.text((pad, 14), 'A cat walking: Muybridge, Animal Locomotion, plate 716, frames 1-6 (about a third of a stride)', fill=INK, font=fb)
    d.text((pad, 38), 'Filled dot: paw on the ground.  Dashed ring: paw in the air.  Orange: near legs.  Blue: far legs.', fill=MUTED, font=f)
    for fr, i, paws in cells:
        x = pad + (i % 3) * (cw + pad); y = 64 + (i // 3) * (ch + 74)
        out.paste(fr, (x, y))
        down = [NAMES[l] for l, _, _, g in paws if g]
        d.text((x, y + ch + 6), 'frame %d: %d paws down' % (i + 1, len(down)), fill=INK, font=fb)
        d.text((x, y + ch + 28), ', '.join(down), fill=MUTED, font=fs)
        d.text((x, y + ch + 46), CAT_NOTES[i], fill=MUTED, font=fs)
    y = 64 + 2 * (ch + 74) + 6
    for line in ['Support goes 3, 3, 4, 4, 3, 3: the near fore paw lands (frame 3) before the far hind paw leaves (frame 5).',
                 'Each frame is from its own camera in a row along the track, so the cat stays mid-frame: compare poses, not positions.',
                 'Which hind leg is nearer cannot be seen at this size: the hind labels follow the lateral sequence measured',
                 'in walking cats (a hind paw lands, then the fore paw on the same side).',
                 'Photographs: Eadweard Muybridge, 1887, public domain. Scan: National Gallery of Art, Washington (2019.150.9), CC0.']:
        d.text((pad, y), line, fill=MUTED if not line.startswith('Photo') else INK, font=f); y += 24
    out.save(os.path.join(OUT, 'muybridge-716-cat-walk.png'), optimize=True)


# ---------- plate 729: a tigress walking; frames 3-8 show one foreleg's whole swing ----------
TIGER_ROWS, TIGER_COLS = [(38, 626), (688, 1280), (1340, 1880)], [(30, 1030), (1050, 2035), (2040, 3045), (3055, 4060)]
TIGER_NOTES = {3: 'toes still down, heel up', 4: 'the paw peels off', 5: 'wrist bent: paw flicked back and up',
               6: 'forearm swings forward, paw hangs', 7: 'wrist opens, the leg reaches', 8: 'about to land, ahead of the shoulder'}


def tiger_sheet(cache):
    im = scan('729', cache); f, fb = font(15), font(17, True)
    frames = [im.crop((c[0], r[0], c[1], r[1])) for r in TIGER_ROWS for c in TIGER_COLS]
    cells = []
    for n in range(3, 9):
        fr = frames[n - 1]; w, h = fr.size
        c = fr.crop((int(w * 0.40), int(h * 0.42), int(w * 0.97), int(h * 0.99)))
        c = ImageOps.autocontrast(c.convert('L'), cutoff=1).convert('RGB'); c = c.resize((420, int(c.height * 420 / c.width)), Image.LANCZOS)
        cells.append((n, c))
    cw, ch = cells[0][1].size; pad = 18; W = pad + 3 * (cw + pad); H = 64 + 2 * (ch + 40) + 60
    out = Image.new('RGB', (W, H), PAPER); d = ImageDraw.Draw(out)
    d.text((pad, 14), "One foreleg's swing: Muybridge, Animal Locomotion, plate 729 (tigress walking), frames 3-8", fill=INK, font=fb)
    d.text((pad, 38), 'Watch the white, striped leg (her far foreleg). The plain leg in front stays planted throughout.', fill=MUTED, font=f)
    for k, (n, c) in enumerate(cells):
        x = pad + (k % 3) * (cw + pad); y = 64 + (k // 3) * (ch + 40)
        out.paste(c, (x, y)); d.text((x, y + ch + 6), 'frame %d: %s' % (n, TIGER_NOTES[n]), fill=INK, font=f)
    d.text((pad, H - 34), 'Photographs: Eadweard Muybridge, 1887, public domain. Scan: National Gallery of Art, Washington (2014.79.655), CC0.', fill=INK, font=f)
    out.save(os.path.join(OUT, 'muybridge-729-tigress-foreleg.png'), optimize=True)


# ---------- Maker: gait diagram, frames, legs ----------
LEG_ORDER = ['RH', 'RF', 'LH', 'LF']                              # in footfall order
LEG_NAME = {'RH': 'near hind', 'RF': 'near fore', 'LH': 'far hind', 'LF': 'far fore'}
TAG = {'RH': 'Hn', 'RF': 'Fn', 'LH': 'Hf', 'LF': 'Ff'}
PHASE = ['contact', 'down', 'down', 'mid-stance', 'push', 'push', 'heel up', 'lift', 'passing', 'reach']


def gait_sheet():
    import walk_rig as W
    f, fb, fs = font(15), font(17, True), font(13)
    cyc = 2; n = W.N * cyc; cell = 34; left = 150; top = 92; rowh = 40
    top += 22; Wd = max(left + n * cell + 40, 1000); H = top + 4 * rowh + 150
    out = Image.new('RGB', (Wd, H), PAPER); d = ImageDraw.Draw(out)
    d.text((18, 14), "Maker's walk: when each paw is on the desk (two cycles of %d frames)" % W.N, fill=INK, font=fb)
    d.text((18, 38), 'Lateral sequence: near hind, near fore, far hind, far fore (she faces right: the near legs are her right legs).', fill=MUTED, font=f)
    d.text((18, 60), 'Each paw is down %d of %d frames (duty factor %.1f) and in the air %d; %d px a frame, so a stride is %d px.'
           % (W.STANCE, W.N, W.STANCE / W.N, W.N - W.STANCE, W.SPEED, W.SPEED * W.N), fill=MUTED, font=f)
    for i in range(n):
        x = left + i * cell
        d.text((x + cell // 2 - 4 * len(str(i % W.N)), top - 24), str(i % W.N), fill=MUTED, font=fs)
        if i % W.N == 0: d.line([(x, top - 6), (x, top + 4 * rowh + 34)], fill=(160, 158, 150), width=1)
    for r, leg in enumerate(LEG_ORDER):
        y = top + r * rowh; col = (43, 43, 43) if W.NEAR[leg] else (140, 140, 140)
        d.text((18, y + 9), '%s (%s)' % (LEG_NAME[leg], TAG[leg]), fill=INK, font=f)
        for i in range(n):
            k = (i - W.CONTACT[leg]) % W.N; x = left + i * cell
            if k < W.STANCE: d.rectangle([x + 1, y + 6, x + cell - 1, y + rowh - 8], fill=col)
            else: d.rectangle([x + 1, y + 6, x + cell - 1, y + rowh - 8], outline=(200, 198, 190), width=1)
            if k == 0: d.polygon([(x + 4, y + 2), (x + 14, y + 2), (x + 9, y + 9)], fill=NEAR if W.NEAR[leg] else FAR)
    y = top + 4 * rowh + 6
    d.text((18, y + 4), 'paws down', fill=INK, font=f)
    for i in range(n):
        cnt = sum(1 for leg in LEG_ORDER if (i - W.CONTACT[leg]) % W.N < W.STANCE)
        d.text((left + i * cell + cell // 2 - 4, y + 4), str(cnt), fill=INK if cnt == 3 else NEAR, font=fb)
    y += 40
    for line in ['Dark bars: near legs. Grey bars: far legs. Triangle: the frame a paw lands. Two paws are down only in frames 4 and 9,',
                 'and then both on one side, as in walking cats. Each fore paw lands 2 frames (0.2 of a cycle) after the hind paw of its',
                 'side; 8 frames later that hind paw lands in the fore paw\'s print (direct register).']:
        d.text((18, y), line, fill=MUTED, font=f); y += 22
    out.save(os.path.join(OUT, 'maker-walk-gait.png'), optimize=True)


def frames_sheet():
    import walk_rig as W, maker_build as M
    sh = M.sheet(big=True); fr = [sh['walk%d' % i] for i in range(W.N)]
    z = 4; f, fb, fs = font(14), font(16, True), font(12)
    cw, chh = fr[0].w * z, fr[0].h * z; pad = 16; cols = 5
    H = 60 + 2 * (chh + 104); Wd = pad + cols * (cw + pad)
    out = Image.new('RGB', (Wd, H), PAPER); d = ImageDraw.Draw(out)
    d.text((pad, 14), "Maker's ten walk frames (3 px a frame, 12 frames a second), each leg's pose named", fill=INK, font=fb)
    d.text((pad, 36), 'Red tick: a paw on the desk. "down" frames: the body sinks a pixel as a fore paw takes her weight.', fill=MUTED, font=f)
    for i in range(W.N):
        x = pad + (i % cols) * (cw + pad); y = 60 + (i // cols) * (chh + 104)
        a = fr[i].image().resize((cw, chh), Image.NEAREST); bg = Image.new('RGB', (cw, chh), (236, 232, 224)); bg.paste(a, (0, 0), a); out.paste(bg, (x, y))
        for leg in LEG_ORDER:
            heel, down = W.contacts(i)[leg]
            if down: gx = x + (heel + 3) * z; d.line([(gx, y + chh + 1), (gx, y + chh + 7)], fill=(220, 30, 40) if W.NEAR[leg] else (90, 90, 220), width=3)
        d.text((x, y + chh + 10), 'frame %d%s' % (i, '  (body down)' if i in W.DOWN else ''), fill=INK, font=fb)
        for r, leg in enumerate(LEG_ORDER):
            k = (i - W.CONTACT[leg]) % W.N
            d.text((x, y + chh + 32 + r * 17), '%s: %s' % (LEG_NAME[leg], PHASE[k]), fill=INK if W.NEAR[leg] else MUTED, font=fs)
    out.save(os.path.join(OUT, 'maker-walk-frames.png'), optimize=True)


def legs_sheet():
    """each leg kind on its own through its ten poses (near-leg colours), big, with the pose named"""
    import walk_rig as W, maker_build as M
    pal = {'K': M.LINE, 'D': M.DEEP, 'S': M.SHADE, 'F': M.FILL}
    f, fb, fs = font(14), font(16, True), font(12)
    z = 7; x0, x1, y0, y1 = 0, 56, 34, 54
    cw, chh = (x1 - x0) * z, (y1 - y0) * z
    out = Image.new('RGB', (16 + 5 * (cw + 16), 50 + 4 * (chh + 34)), PAPER); d = ImageDraw.Draw(out)
    d.text((16, 14), 'One fore leg and one hind leg through the cycle (k = frames since the paw landed; 0-6 on the desk, 7-9 in the air)', fill=INK, font=fb)
    for j, kind in enumerate(('hind', 'fore')):
        for k in range(W.N):
            if k < W.STANCE: px, heel = W.stance_leg(kind, k, W.GROUND)
            else: px, heel = W.swing_leg(kind, k - W.STANCE, W.GROUND), None
            im = Image.new('RGB', (x1 - x0, y1 - y0), (236, 232, 224))
            for (r, c), ch in px.items():
                if y0 <= r < y1 and x0 <= c < x1:
                    im.putpixel((c - x0, r - y0), tuple(int(pal[ch][i:i + 2], 16) for i in (1, 3, 5)))
            row = j * 2 + k // 5; col = k % 5
            x = 16 + col * (cw + 16); y = 50 + row * (chh + 34)
            out.paste(im.resize((cw, chh), Image.NEAREST), (x, y))
            d.line([(x, y + (W.GROUND - y0 + 1) * z), (x + cw, y + (W.GROUND - y0 + 1) * z)], fill=(196, 160, 112), width=2)
            d.text((x, y + chh + 6), '%s, k=%d: %s' % (kind, k, PHASE[k]), fill=INK, font=f)
    out.save(os.path.join(OUT, 'maker-walk-legs.png'), optimize=True)


def strip_sheet():
    import walk_check as C
    C.strip(C.walk_frames(), os.path.join(OUT, 'maker-walk-strip.png'), z=4, cycles=1)


def main():
    cache = sys.argv[1] if len(sys.argv) > 1 else '/tmp/walk-refs-cache'
    os.makedirs(OUT, exist_ok=True)
    cat_sheet(cache); tiger_sheet(cache); gait_sheet(); frames_sheet(); legs_sheet(); strip_sheet()
    for name in sorted(os.listdir(OUT)): print(name, Image.open(os.path.join(OUT, name)).size, os.path.getsize(os.path.join(OUT, name)) // 1024, 'KB')


if __name__ == '__main__': main()
