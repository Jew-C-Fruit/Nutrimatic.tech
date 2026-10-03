#!/usr/bin/env python3
"""
Nutrimatic desk scene - poses.py
Version 1.1.1

Created: 2026-10-02 - The figures' body poses, from generated pictures, as layers under the base head; the neck, and
  Ilinca's top, taken from the base so every pose joins the same head; front boxes by eye (v1.0.0)
Modified: 2026-10-02 - Hands and forearms: black lines inside skin (finger gaps, knuckles, creases) become a dark skin
  tone, and stray outline strokes inside the clothes become the cloth's shade, so hands read as hands, not claws;
  per-pose pixel fixes (FIX); fronts for hands over Ilinca's hair; new poses (lift, pet, petfront); props lifted out
  of a pose (laptop, paper, bottle) so the scene can draw them alone, a pose without one (offerEmpty), and
  writing frames made by moving the writing hand (write1, write2) (v1.1.0)
Modified: 2026-10-02 - New talk, pethead (Cole) and type (Ilinca) pictures: the old ones had a third arm or hands
  through each other; the old talk pose's pixel fix went with it (v1.1.1)

Every activity in the scene is drawn with a body pose: the whole torso with arms, hands and whatever they hold, made
by the image model from the figure's own portrait (pose_sprites.py says how) and reduced to a sprite on the base
sprite's grid. The picked sprites are in sprites/poses/<who>/ with index.json (where each sits, which picture it came
from). This module cuts each into what the scene draws:

  body    the pose without its head (the head always comes from characters.py, so the face frames work everywhere)
  front   for poses that cover the face (a mug at the mouth, a hand over a yawn): the pixels inside a box, drawn over the head
  pts     named points in the pose, in base coordinates: "tip" of the soldering iron, the "hand" of a high five

  pick(who, pose, picture)   reduce a generated picture and store it in sprites/poses/<who>/
  build(character)           -> {pose: {"body": (Sprite, x, y), "front": (Sprite, x, y) or None, "pts": {...}}}
"""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from spritekit import Sprite, load
import pose_sprites as PS
from characters import CHARACTERS, layers

POSES = os.path.join(HERE, 'sprites', 'poses')
GRIDS = {'cole': os.path.join(HERE, 'sprites', 'cole-301.json'), 'ilinca': os.path.join(HERE, 'sprites', 'ilinca-407.json')}

# colours of the props that can be lifted out of a pose
LAPTOP = {'#cfd2d4', '#9a9ea2', '#5f6368', '#dfe9f5', '#7fb2e0', '#d9d5c8', '#fbfaf5'}
PAPER = {'#fbfaf5', '#d9d5c8'}
BOTTLE = {'#fbfaf5', '#d9d5c8', '#cfd2d4', '#e4002b', '#a3001f', '#ff5a72'}

# By eye, per pose: the box (base coordinates) whose pixels go over the face, and named points.
MANUAL = {
    'cole': {
        'sip': dict(front=(37, 26, 58, 46), front_mode='props'),
        'drink': dict(front=(40, 28, 61, 58), front_mode='props'),
        'solder': dict(pts={'tip': (35, 82)}),
        'think': dict(neck_fill=False),                                  # the hand at his chin: the gap there is real
        # props the scene also draws on their own: the laptop (the cat sits on it), the paper, the bottle being handed over
        'type': dict(props={'laptop': (LAPTOP, (20, 56, 100, 100))}),
        'write': dict(props={'paper': (PAPER, (10, 80, 90, 100))}, frames={'write1': ((14, 64, 36, 92), 1, 0), 'write2': ((14, 64, 36, 92), 2, -1)}),
        'offer': dict(fix=[('recolour', 74, 19, 87, 49, {'#f9eee0': '#fbfaf5'})], props={'bottle': (BOTTLE, (58, 0, 100, 50))}, empty={'offerEmpty': 'bottle'}),
        'highfive': dict(pts={'hand': (67, 24)}),
        'throw': dict(pts={'hand': (76, 34)}),
        'yawn': dict(front=(30, 31, 52, 47), keep_neck=True),
        # a chair back stood behind the elbow in the generated picture
        'fist': dict(fix=[('clear', 80, 64, 83, 64), ('clear', 73, 65, 83, 65), ('clear', 74, 66, 83, 66), ('clear', 75, 67, 83, 67), ('clear', 76, 68, 83, 69),
                          ('clear', 77, 70, 83, 70), ('clear', 78, 71, 83, 72), ('clear', 79, 73, 83, 73), ('clear', 80, 74, 83, 75), ('clear', 81, 76, 83, 77),
                          ('clear', 82, 78, 83, 79)]),
    },
    'ilinca': {
        'sip': dict(front=(3, 20, 24, 42), front_mode='props'),
        'type': dict(props={'laptop': (LAPTOP, (-30, 50, 40, 96))}),
        'write': dict(props={'paper': (PAPER, (-14, 74, 40, 96))}, frames={'write1': ((-6, 60, 16, 90), 1, 0), 'write2': ((-6, 60, 16, 90), 2, -1)}),
        'think': dict(front=(8, 28, 34, 48), front_mode='diff', keep_neck=True),
        'phone': dict(keep_chest=True),
        'carry': dict(keep_chest=True),
        'drink': dict(front=(-2, 16, 24, 48), front_mode='props'),
        'yawn': dict(front=(12, 24, 36, 42), front_mode='diff', keep_neck=True),
        # hands and sleeves that are in front of her hair
        'talk': dict(front=(-16, 28, 14, 64), front_mode='limb'),
        'call': dict(keep_chest=True, front=(4, 24, 15, 46), front_mode='limb'),
        'surprise': dict(keep_chest=True, front=(48, 24, 68, 58), front_mode='limb'),
        # the bottle came out in her skin colours
        'take': dict(fix=[('recolour', -18, 19, -4, 47, {'#faebe1': '#fbfaf5', '#f9e2d2': '#fbfaf5', '#d18881': '#d9d5c8', '#e1cec4': '#d9d5c8'})],
                     props={'bottle': (BOTTLE, (-20, 8, -3, 48))}),
    },
}


def jaw_rows(c, s):
    """the last head row in each column near the face, as characters.py cuts it"""
    if isinstance(c.JAW, dict): return dict(c.JAW)
    pts, out = c.JAW, {}
    for x in range(s.w):
        if x < pts[0][0]: y = 33
        elif x >= pts[-1][0]: y = pts[-1][1]
        else:
            for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
                if x0 <= x <= x1: y = y0 if x1 == x0 else int(round(y0 + (y1 - y0) * (x - x0) / (x1 - x0))); break
        out[x] = y
    return {x: y for x, y in out.items() if pts[0][0] - 10 <= x <= pts[-1][0] + 10}


def master_palette(c):
    base = c.blank(); full = c.full()
    return list(dict.fromkeys(list(base.pal) + list(full.pal) + PS.PROPS))


def index(who):
    p = os.path.join(POSES, who, 'index.json')
    return json.load(open(p)) if os.path.exists(p) else {}


def pick(who, pose, picture):
    """reduce one generated pose picture to a sprite on the base grid, aligned to the base head, and store it"""
    c = CHARACTERS[who]; grid = json.load(open(GRIDS[who])); base = c.blank(); _, _, hm = layers(c)
    spr, x0, y0 = PS.to_sprite(picture, grid); spr = PS.snap(spr, master_palette(c))
    dx, dy, score = PS.align(spr, x0, y0, base, hm); x0 -= dx; y0 -= dy
    os.makedirs(os.path.join(POSES, who), exist_ok=True); spr.save(os.path.join(POSES, who, pose + '.png'))
    ix = index(who); ix[pose] = dict(x=x0, y=y0, src=os.path.basename(os.path.dirname(picture)) + '/' + os.path.basename(picture), align=[dx, dy], fit=round(score, 3))
    json.dump(ix, open(os.path.join(POSES, who, 'index.json'), 'w'), indent=1, sort_keys=True)
    return spr, x0, y0


# Selective outlines: inside a figure's skin, a black line between skin and skin is drawn in a dark skin tone instead
# (black stays only on the outer edge of a hand or arm); the same for stray black strokes inside the clothes.
SOFTEN = {
    'cole': [({'#dc7f6d', '#ee947c', '#f6af8d', '#f8cda6', '#f9eee0'}, '#dc7f6d'), ({'#100f13', '#211f1f'}, '#100f13')],
    'ilinca': [({'#f9e2d2', '#faebe1', '#e1cec4', '#e0b3a2', '#f1a49b', '#d18881', '#b5705f'}, '#d18881'), ({'#191718', '#292423'}, '#191718')],
}
LINES = {'cole': {'#010101', '#090507', '#0f0503'}, 'ilinca': {'#010100', '#0b0503', '#0e0c0b'}}
# letters for the pixel maps in FIX edits ('.' leaves a pixel alone, '_' clears it)
KEYS = {
    'cole': dict(k='#010101', b='#623e32', d='#dc7f6d', a='#ee947c', m='#f6af8d', s='#f8cda6', h='#f9eee0', t='#211f1f', u='#100f13',
                 w='#fbfaf5', r='#e4002b', R='#a3001f', g='#cfd2d4', G='#9a9ea2'),
    'ilinca': dict(k='#010100', D='#b5705f', d='#d18881', a='#f1a49b', e='#e0b3a2', x='#e1cec4', s='#f9e2d2', h='#faebe1', j='#292423', J='#191718',
                   w='#fbfbf9', W='#fbfaf5', N='#5f4030', n='#6f4b3a', o='#9a6f50', O='#bd8e5d', y='#d9ae71', r='#e4002b', R='#a3001f', g='#cfd2d4', G='#9a9ea2'),
}


def soften(spr, who, reach_n=2):
    """black line pixels that separate one material from the same material (looking up to reach_n pixels each way along
    a row, a column or a diagonal, through line pixels only) take that material's dark tone"""
    s = spr.copy(); idx = spr.idx; h, w = idx.shape
    line = np.isin(idx, [i for i, c in enumerate(spr.pal) if c in LINES[who]])
    for cols, tone in SOFTEN[who]:
        mat = np.isin(idx, [i for i, c in enumerate(spr.pal) if c in cols])
        def reach(dy, dx):
            out = np.zeros_like(line); live = line.copy()
            for k in range(1, reach_n + 1):
                m = np.zeros_like(mat); l = np.zeros_like(line)
                ys0, ys1, xs0, xs1 = max(0, -dy * k), h - max(0, dy * k), max(0, -dx * k), w - max(0, dx * k)
                m[ys0:ys1, xs0:xs1] = mat[ys0 + dy * k:ys1 + dy * k, xs0 + dx * k:xs1 + dx * k]; l[ys0:ys1, xs0:xs1] = line[ys0 + dy * k:ys1 + dy * k, xs0 + dx * k:xs1 + dx * k]
                out |= live & m; live &= l
            return out
        inner = line & ((reach(-1, 0) & reach(1, 0)) | (reach(0, -1) & reach(0, 1)) | (reach(-1, -1) & reach(1, 1)) | (reach(-1, 1) & reach(1, -1)))
        s.idx[inner] = s.color(tone)
    return s


def fix(spr, ox, oy, edits, pal_key):
    """per-pose pixel fixes in base coordinates: ('rows', x, y, [..]) maps of palette letters ('.' keep, '_' clear),
    ('clear', x0, y0, x1, y1) and ('recolour', x0, y0, x1, y1, {from: to})"""
    s = spr.copy()
    for e in edits:
        if e[0] == 'rows':
            _, x, y, rows = e; s.rows(x - ox, y - oy, rows, pal_key)
        elif e[0] == 'clear':
            _, x0, y0, x1, y1 = e; s.idx[max(0, y0 - oy):max(0, y1 + 1 - oy), max(0, x0 - ox):max(0, x1 + 1 - ox)] = -1
        elif e[0] == 'recolour':
            _, x0, y0, x1, y1, m = e
            for a, b in m.items(): s.replace(a, b, (max(0, x0 - ox), max(0, y0 - oy), min(s.w - 1, x1 - ox), min(s.h - 1, y1 - oy))) if a in s.pal else None
    return s


def lift_prop(spr, ox, oy, cols, box):
    """the prop's pixels (its colours inside the box, base coordinates) and the dark outline touching them: (prop Sprite, mask)"""
    from scipy import ndimage
    x0, y0, x1, y1 = box; m = np.zeros(spr.idx.shape, bool)
    m[max(0, y0 - oy):max(0, y1 + 1 - oy), max(0, x0 - ox):max(0, x1 + 1 - ox)] = True
    part = m & np.isin(spr.idx, [i for i, c in enumerate(spr.pal) if c in cols])
    edge = m & ndimage.binary_dilation(part, structure=np.ones((3, 3), bool)) & PS.dark(spr)
    mask = part | edge; out = spr.copy(); out.idx[~mask] = -1
    return out, mask


def shifted(spr, ox, oy, box, dx, dy):
    """the pose with what is inside the box (base coordinates) moved by (dx, dy): a hand moving along a line"""
    out = spr.copy(); x0, y0, x1, y1 = box[0] - ox, box[1] - oy, box[2] - ox, box[3] - oy
    for y in range(max(0, y0), min(spr.h, y1 + 1)):
        for x in range(max(0, x0), min(spr.w, x1 + 1)):
            sx, sy = x - dx, y - dy
            if x0 <= sx <= x1 and y0 <= sy <= y1 and 0 <= sx < spr.w and 0 <= sy < spr.h: out.idx[y, x] = spr.idx[sy, sx]
    return out


# the neck, between the jaw and the collar, in base coordinates: x range and the collar row
NECK = {'cole': (28, 50, 49), 'ilinca': (23, 37, 49)}


# beside the neck, where a pose's shoulder stops short of the head and the wall showed through under the jaw (the face
# "lost its clean outline"): columns, last row
NECK_FILL = {'cole': (44, 60, 47)}
CLOTH_EDGE = {'cole': ('#010101', '#211f1f')}


def neck_patch(c, torso, jaw):
    """pixels of the base torso just under the jaw: (torso sprite, mask)"""
    x0, x1, collar = NECK[c.name]; m = np.zeros(torso.idx.shape, dtype=bool)
    for x in range(x0, x1 + 1):
        top = jaw.get(x, 0) + 1
        m[top:collar + 1, x] = True
    return torso, m & (torso.idx >= 0)


def neck_fill(c, torso, head, body, ox, oy):
    """a gap of a few pixels in a row between the head's right edge and the pose's shoulder: the shoulder carries on to
    the head (its cloth colour, with the outline against the head), so the jaw keeps a clean edge"""
    if c.name not in NECK_FILL: return body
    x0, x1, collar = NECK_FILL[c.name]; out = body.copy(); line, cloth = CLOTH_EDGE[c.name]
    for y in range(30, collar + 1):
        hx = [x for x in range(x0, x1 + 1) if x < head.w and head.idx[y, x] >= 0]
        if not hx: continue
        right = max(hx); xb = None
        for x in range(right + 1, x1 + 1):
            sx, sy = x - ox, y - oy
            if 0 <= sx < out.w and 0 <= sy < out.h and out.idx[sy, sx] >= 0: xb = x; break
        if xb is None or xb - right > 5: continue
        for x in range(right + 1, xb):
            out.put(x - ox, y - oy, line if x == right + 1 else cloth)
    return out


def chest_patch(c, torso):
    """Ilinca: where her base top is white, a pose that drew bare skin there gets the top back"""
    if c.name != 'ilinca': return None
    whites = [i for i, col in enumerate(torso.pal) if col in (c.W, c.TOPSH)]
    m = np.zeros(torso.idx.shape, dtype=bool); m[49:76, 14:36] = True
    return torso, m & np.isin(torso.idx, whites), {c.S, c.SA, '#e1cec4', '#faebe1'}


def build(c):
    who = c.name; ix = index(who); base = c.blank(); torso, head, hm = layers(c); jaw = jaw_rows(c, base)
    hair = set(c.HAIR) if hasattr(c, 'HAIR') else None; out = {}; neck = neck_patch(c, torso, jaw); chest = chest_patch(c, torso)
    for pose, meta in sorted(ix.items()):
        spr = load(os.path.join(POSES, who, pose + '.png')); man = MANUAL.get(who, {}).get(pose, {})
        if man.get('fix'): spr = fix(spr, meta['x'], meta['y'], man['fix'], KEYS[who])     # before softening: a recoloured prop is not skin any more
        spr = soften(spr, who)
        body, front = PS.split(spr, meta['x'], meta['y'], hm, jaw, man.get('front'), hair, None if man.get('keep_neck') else neck, man.get('front_mode', 'all'),
                               base_head=head, chest=None if man.get('keep_chest') else chest,
                               limb=set().union(*[cols for cols, _ in SOFTEN[who]]) | set(PS.PROPS))
        if not man.get('keep_neck') and man.get('neck_fill', True): body = neck_fill(c, torso, head, body, meta['x'], meta['y'])
        entry = dict(body=(body, meta['x'], meta['y']), front=(front, meta['x'], meta['y']) if front is not None and (front.idx >= 0).any() else None, pts=man.get('pts', {}), props={})
        masks = {}
        for name, (cols, box) in man.get('props', {}).items():
            prop, mask = lift_prop(body, meta['x'], meta['y'], cols, box); entry['props'][name] = (prop, meta['x'], meta['y']); masks[name] = mask
        out[pose] = entry
        for variant, name in man.get('empty', {}).items():
            from scipy import ndimage
            b2 = body.copy(); b2.idx[masks[name]] = -1
            lab, n = ndimage.label(b2.idx >= 0, structure=np.ones((3, 3), bool))           # crumbs of the prop's outline go too
            if n > 1:
                sizes = ndimage.sum(b2.idx >= 0, lab, index=np.arange(1, n + 1))
                b2.idx[np.isin(lab, [i + 1 for i, s in enumerate(sizes) if s < 12])] = -1
            out[variant] = dict(body=(b2, meta['x'], meta['y']), front=None, pts=entry['pts'], props={})
        for variant, (box, dx, dy) in man.get('frames', {}).items():
            out[variant] = dict(body=(shifted(body, meta['x'], meta['y'], box, dx, dy), meta['x'], meta['y']), front=entry['front'], pts=entry['pts'], props=entry['props'])
    return out
