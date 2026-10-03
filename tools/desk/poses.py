#!/usr/bin/env python3
"""
Nutrimatic desk scene - poses.py
Version 1.4.1

Created: 2026-10-02 - The figures' body poses, from generated pictures, as layers under the base head; the neck, and
  Ilinca's top, taken from the base so every pose joins the same head; front boxes by eye (v1.0.0)
Modified: 2026-10-02 - Hands and forearms: black lines inside skin (finger gaps, knuckles, creases) become a dark skin
  tone, and stray outline strokes inside the clothes become the cloth's shade, so hands read as hands, not claws;
  per-pose pixel fixes (FIX); fronts for hands over Ilinca's hair; new poses (lift, pet, petfront); props lifted out
  of a pose (laptop, paper, bottle) so the scene can draw them alone, a pose without one (offerEmpty), and
  writing frames made by moving the writing hand (write1, write2) (v1.1.0)
Modified: 2026-10-02 - New talk, pethead (Cole) and type (Ilinca) pictures: the old ones had a third arm or hands
  through each other; the old talk pose's pixel fix went with it (v1.1.1)
Modified: 2026-10-03 - Poses may keep their own head (a stretch frame tried it; dropped: Cole's face shape drifted);
  the "nu" mark on the shaker bottles; Ilinca's wave, surprise, think and yawn redone with cleaner hands; her wave rocks
  a pixel (v1.2.0)
Modified: 2026-10-03 - Audit fixes: Ilinca's hands and held things in front of her hair in every pose; outlines kept
  where a hand meets the face (the sip); hands in front of mugs and bottles; petting pictures with the stand-in cat
  erased (the scene puts Maker there); a new typing pose for Cole and take pose for Ilinca; shake2; stray chairs and
  specks cleared (v1.3.0)
Modified: 2026-10-03 - Cole's note 1 ("major hand and arm distortion", chin on hand): the cleanup softens only short line
  runs (finger gaps), so crossed limbs keep their outline; a new chin-on-hand picture for Cole whose fist goes in front of
  the jaw (front mode 'arm'); stray dashes cleared from Ilinca's (v1.3.1)
Modified: 2026-10-03 - Notes 2 and 3: gaps and one-pixel cracks inside a figure are closed (close_holes); objects in
  front of Ilinca's hair are taken from the uncut pose (a laptop reaching into her hair was cut where it lies); her
  phone pose with a blue phone and hands over her hair; a larger laptop for her, its panel made whole (v1.4.0)
Modified: 2026-10-03 - Note 4: Cole's console redrawn after his reference (the back of a red New 3DS XL), behind his
  hands (fix op 'under') (v1.4.1)

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
from scipy import ndimage as _nd
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from spritekit import Sprite, load
import pose_sprites as PS
from characters import CHARACTERS, layers

POSES = os.path.join(HERE, 'sprites', 'poses')
GRIDS = {'cole': os.path.join(HERE, 'sprites', 'cole-301.json'), 'ilinca': os.path.join(HERE, 'sprites', 'ilinca-407.json')}

# the Nutrimatic "nu" monogram (assets/nu-mark.svg reduced to five pixels) for the shaker bottles; '.' keeps a pixel
NU_MARK = ['kkk..', 'k.k..', 'k.k.k', 'k.k.k', '..kkk']

# the stand-in cat's greys in the petting pictures
CAT_GREYS = {'#9a9ea2', '#cfd2d4', '#5f6368', '#a19c9c', '#ddd6cf', '#d9a650'}

# colours of the props that can be lifted out of a pose
LAPTOP = {'#cfd2d4', '#9a9ea2', '#5f6368', '#dfe9f5', '#7fb2e0', '#d9d5c8', '#fbfaf5'}
PAPER = {'#fbfaf5', '#d9d5c8'}
BOTTLE = {'#fbfaf5', '#d9d5c8', '#cfd2d4', '#e4002b', '#a3001f', '#ff5a72'}

# By eye, per pose: the box (base coordinates) whose pixels go over the face, and named points.
MANUAL = {
    'cole': {
        'sip': dict(front=(30, 26, 58, 48), front_mode='limb'),            # the fingers round the mug are in front of it, and of the chin
        'drink': dict(front=(40, 28, 61, 58), front_mode='limb'),
        'solder': dict(pts={'tip': (35, 82)}),
        # note 4, "supposed to be a nintendo DS" (his reference: the back of a red New 3DS XL): the console redrawn as seen
        # from across the desk, behind his hands: the lid's red back with its two camera lenses, the hinge with its
        # knuckles, the underside of the bottom half with its label
        'ds': dict(fix=[('under', 26, 55, [
            '.kkkkkkkkkkkkkkkkkkkkkkkk.',
            'kpppprrrrrrrrrrrrrrrrrrrrk',
            'kprrrrrrrrrkrrkrrrrrrrrrRk',
            'kprrrrrrrrrrrrrrrrrrrrrrRk',
            'krrrrrrrrrrrrrrrrrrrrrrrRk',
            'krrrrrrrrrrrrrrrrrrrrrrrRk',
            'krrrrrrrrrrrrrrrrrrrrrrrRk',
            'krrrrrrrrrrrrrrrrrrrrrrrRk',
            'krrrrrrrrrrrrrrrrrrrrrrRRk',
            'kRRrrrrrrrrrrrrrrrrrrrRRRk',
            'kRRRRRRRRRRRRRRRRRRRRRRRRk',
            'kkRRkkkkkkkkkkkkkkkkkkRRkk',
            'kRRRRRRRRRRRRRRRRRRRRRRRRk',
            'kRRRRRRRRRwwwwwwRRRRRRRRRk',
            'kRRRRRRRRRRRRRRRRRRRRRRRRk',
            '.kkkkkkkkkkkkkkkkkkkkkkkk.'], {'#f8cda6', '#f6af8d', '#ee947c', '#dc7f6d', '#f9eee0'})]),
        'think': dict(neck_fill=False, keep_neck=True, front=(30, 32, 58, 50), front_mode='arm'),   # the fist under his chin, in front of the jaw
        # petting Maker lying beside him: the picture had a grey cat under his hand; it goes, and the scene lays Maker in
        # its place (RIG below), so the hand lies exactly on her back; the hand moves a little as it strokes
        'petcat': dict(fix=[('erase', 28, 60, 86, 93, CAT_GREYS)], frames={'petcat2': ((46, 56, 80, 82), -2, 0)}),
        'stretch': dict(fix=[('clear', -8, 54, 7, 92), ('clear', 8, 53, 8, 53)]),   # a chair's edge behind him in the generated picture
        # props the scene also draws on their own: the laptop (the cat sits on it), the paper, the bottle being handed over
        'type': dict(props={'laptop': (LAPTOP, (20, 56, 100, 100))}),
        'write': dict(props={'paper': (PAPER, (10, 80, 90, 100))}, frames={'write1': ((14, 64, 36, 92), 1, 0), 'write2': ((14, 64, 36, 92), 2, -1)}),
        'offer': dict(fix=[('recolour', 74, 19, 87, 49, {'#f9eee0': '#fbfaf5'}), ('rows', 78, 28, NU_MARK)], props={'bottle': (BOTTLE, (58, 0, 100, 50))}, empty={'offerEmpty': 'bottle'}),
        'shake': dict(fix=[('rows', 38, 78, NU_MARK)], frames={'shake2': ((24, 44, 58, 86), 0, -2)}),   # shaking: only the arms and the bottle move
        'highfive': dict(pts={'hand': (67, 24)}),
        'throw': dict(pts={'hand': (76, 34)}),
        'yawn': dict(front=(30, 31, 52, 47), keep_neck=True),
        # a chair back stood behind the elbow in the generated picture
        'fist': dict(fix=[('clear', 80, 64, 83, 64), ('clear', 73, 65, 83, 65), ('clear', 74, 66, 83, 66), ('clear', 75, 67, 83, 67), ('clear', 76, 68, 83, 69),
                          ('clear', 77, 70, 83, 70), ('clear', 78, 71, 83, 72), ('clear', 79, 73, 83, 73), ('clear', 80, 74, 83, 75), ('clear', 81, 76, 83, 77),
                          ('clear', 82, 78, 83, 79)]),
    },
    'ilinca': {
        'sip': dict(front=(-2, 20, 24, 46), front_mode='limb'),
        # a big laptop (note 3: hers was too small); the picture hung her hair over its top edge, so its silver panel is
        # filled solid and the whole laptop goes in front of her hair
        'type': dict(fix=[('fill', 0, 57, 58, 84, '#cfd2d4', {'#cfd2d4', '#9a9ea2', '#5f6368'}), ('fill', -1, 56, 59, 56, '#5f6368', set())],
                     props={'laptop': (LAPTOP, (-14, 50, 66, 96))}),
        'wave': dict(frames={'wave2': ((-12, 12, 12, 38), 1, 0)}),          # a casual wave: the hand rocks a pixel
        # her reaching sleeve ended in a spike up into her hair: its top is cut level at the shoulder, under the hair
        'petcat': dict(fix=[('erase', -38, 60, 32, 94, CAT_GREYS), ('clear', 0, 30, 16, 45), ('rows', 4, 46, ['kkkkkk'])], frames={'petcat2': ((-18, 54, 14, 76), 2, 0)}),
        'stretch': dict(fix=[('clear', 63, 38, 67, 84)]),                # a chair's edge behind her
        'rest': dict(fix=[('recolour', 56, 55, 64, 66, {'#5f6368': '#191718', '#9a9ea2': '#292423'})]),   # a grey chair corner by her shoulder
        'write': dict(props={'paper': (PAPER, (-14, 74, 40, 96))}, frames={'write1': ((-6, 60, 16, 90), 1, 0), 'write2': ((-6, 60, 16, 90), 2, -1)}),
        'think': dict(front=(8, 28, 34, 48), front_mode='diff', keep_neck=True, fix=[('clear', 3, 41, 16, 58)]),   # dashes of a lost shoulder outline cleared
        # her phone and both hands are in front of her hair (they were drawn under it), and the phone is blue again (the
        # reduction had snapped the picture's blue phone to grey)
        'phone': dict(keep_chest=True, front=(4, 44, 44, 72), front_mode='limb', base_box=(12, 68, 34, 86),
                      fix=[('recolour', 12, 44, 36, 70, {'#5f6368': '#3d5f99', '#9a9ea2': '#6f93cf'})]),
        'carry': dict(keep_chest=True),
        'drink': dict(front=(-6, 16, 24, 50), front_mode='limb'),
        'yawn': dict(front=(12, 24, 36, 42), front_mode='diff', keep_neck=True),
        # hands and sleeves that are in front of her hair
        'talk': dict(front=(-16, 28, 14, 64), front_mode='limb'),
        'call': dict(keep_chest=True, front=(4, 24, 15, 46), front_mode='limb'),
        'surprise': dict(keep_chest=True, front=(48, 24, 68, 58), front_mode='limb'),
        # the bottle came out in her skin colours
        'take': dict(fix=[('clear', -30, 78, 13, 84), ('rows', -6, 30, NU_MARK)]),   # her fingers wrap the bottle; a stray grey bar cleared
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


def pick(who, pose, picture, align=True):
    """reduce one generated pose picture to a sprite on the base grid, aligned to the base head (unless the pose keeps
    its own head), and store it"""
    c = CHARACTERS[who]; grid = json.load(open(GRIDS[who])); base = c.blank(); _, _, hm = layers(c)
    spr, x0, y0 = PS.to_sprite(picture, grid); spr = PS.snap(spr, master_palette(c))
    dx, dy, score = PS.align(spr, x0, y0, base, hm) if align else (0, 0, 0.0); x0 -= dx; y0 -= dy
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
SOFT_MAX = 6                                                         # the longest line run that counts as a finger gap
# letters for the pixel maps in FIX edits ('.' leaves a pixel alone, '_' clears it)
KEYS = {
    'cole': dict(k='#010101', b='#623e32', d='#dc7f6d', a='#ee947c', m='#f6af8d', s='#f8cda6', h='#f9eee0', t='#211f1f', u='#100f13',
                 w='#fbfaf5', r='#e4002b', R='#a3001f', g='#cfd2d4', G='#9a9ea2', p='#ff5a72'),
    'ilinca': dict(k='#010100', D='#b5705f', d='#d18881', a='#f1a49b', e='#e0b3a2', x='#e1cec4', s='#f9e2d2', h='#faebe1', j='#292423', J='#191718',
                   w='#fbfbf9', W='#fbfaf5', N='#5f4030', n='#6f4b3a', o='#9a6f50', O='#bd8e5d', y='#d9ae71', r='#e4002b', R='#a3001f', g='#cfd2d4', G='#9a9ea2'),
}


def soften(spr, who, reach_n=2, keep=None):
    """black line pixels that separate one material from the same material (looking up to reach_n pixels each way along
    a row, a column or a diagonal, through line pixels only) take that material's dark tone; where `keep` is set (around
    the face) lines stay black: there they part a hand from a cheek, not one finger from the next"""
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
        if keep is not None: inner &= ~keep
        # only short runs: a gap between two fingers or a crease is a few pixels; a long line between skin and skin is
        # where two separate limbs meet (crossed forearms, a fist against an arm) and keeps its outline
        lab, n = _nd.label(inner, structure=np.ones((3, 3), bool))
        if n:
            sizes = _nd.sum(inner, lab, index=np.arange(1, n + 1)); inner &= np.isin(lab, [i + 1 for i, sz in enumerate(sizes) if sz <= SOFT_MAX])
        s.idx[inner] = s.color(tone)
    return s


# Ilinca's hair hangs down over her chest; her hands, and what they hold, are in front of it whenever they are below her
# collar (her top starts at row 55, so skin below that is hands): those pixels go on the front layer of every pose.
HAIR_FRONT_ROW = {'ilinca': 56}


def hair_front(body, ox, oy, row, who, front, raw=None):
    """the skin and props of a pose below `row` (base coordinates), with the outline touching them, added to its front.
    Props come from the raw pose (`raw`, before the head's area was cut away: a laptop reaching up into the long hair
    was cut where the hair lies), skin from the body"""
    from scipy import ndimage
    skin = set(SOFTEN[who][0][0]); props = set(PS.PROPS); src = raw if raw is not None and raw.idx.shape == body.idx.shape else body
    part_s = np.isin(body.idx, [i for i, c in enumerate(body.pal) if c in skin | (props if src is body else set())])
    part_p = np.isin(src.idx, [i for i, c in enumerate(src.pal) if c in props]) if src is not body else np.zeros_like(part_s)
    part = part_s | part_p; part[:max(0, row - oy), :] = False
    edge_s = ndimage.binary_dilation(part, structure=np.ones((3, 3), bool))
    m_s = part_s | (edge_s & PS.dark(body)); m_p = part_p | (edge_s & PS.dark(src) & ~PS.dark(body) & (body.idx < 0))
    m_s[:max(0, row - oy), :] = False; m_p[:max(0, row - oy), :] = False
    out = front.copy() if front is not None else body.copy()
    if front is None: out.idx[:] = -1
    for y, x in zip(*np.where(m_s)): out.idx[y, x] = out.color(body.pal[body.idx[y, x]]) if body.idx[y, x] >= 0 else out.idx[y, x]
    for y, x in zip(*np.where(m_p)): out.idx[y, x] = out.color(src.pal[src.idx[y, x]])
    return out


def close_holes(body, ox, oy, head, desk, hair=None):
    """gaps that open inside a figure (where the picture's hair or a limb was wider than what replaces it): empty pixels
    of the torso, below the chin, with the figure (body or base head) on both sides and below, take the nearest body
    pixel; the wall stays wall outside the figure"""
    out = body.copy(); h, w = out.idx.shape
    solid = out.idx >= 0
    hd = np.zeros((h, w), bool); hy, hx = np.where(head.idx >= 0); py, px = hy - oy, hx - ox
    ok = (py >= 0) & (py < h) & (px >= 0) & (px < w); hd[py[ok], px[ok]] = True
    fig = solid | hd
    left = np.maximum.accumulate(fig, axis=1); right = np.maximum.accumulate(fig[:, ::-1], axis=1)[:, ::-1]
    below = np.maximum.accumulate(fig[::-1], axis=0)[::-1]
    holes = ~fig & left & right & below
    top = max(0, 40 - oy); bottom = max(0, desk + 1 - oy); holes[:top, :] = False; holes[bottom:, :] = False
    if hair is not None:                                             # long hair: the gaps open beside it, where the picture's hair was wider
        hm = np.zeros((h, w), bool); hy, hx = np.where(np.isin(head.idx, [i for i, c in enumerate(head.pal) if c in hair]))
        py, px = hy - oy, hx - ox; ok = (py >= 0) & (py < h) & (px >= 0) & (px < w); hm[py[ok], px[ok]] = True
        holes &= _nd.binary_dilation(hm, structure=np.ones((3, 3), bool), iterations=4)
        limit = 120
    else: limit = 40
    lab, n = _nd.label(holes)
    if n:                                                            # only small, enclosed gaps (not the space between an arm and the body)
        sizes = _nd.sum(holes, lab, index=np.arange(1, n + 1)); holes = np.isin(lab, [i + 1 for i, sz in enumerate(sizes) if sz <= limit])
    # and cracks: one-pixel splits with the figure on both sides (above and below, or left and right), even where they run
    # out to the figure's edge, such as a slit across a shoulder where the hair above and the arm below don't meet
    up = np.zeros_like(fig); up[1:] = fig[:-1]; dn = np.zeros_like(fig); dn[:-1] = fig[1:]
    lf = np.zeros_like(fig); lf[:, 1:] = fig[:, :-1]; rt = np.zeros_like(fig); rt[:, :-1] = fig[:, 1:]
    crack = ~fig & ((up & dn) | (lf & rt)); crack[:top, :] = False; crack[bottom:, :] = False
    holes |= crack
    if holes.any():
        _, (iy, ix) = _nd.distance_transform_edt(~solid, return_indices=True)
        out.idx[holes] = out.idx[iy[holes], ix[holes]]
    return out


def fix(spr, ox, oy, edits, pal_key):
    """per-pose pixel fixes in base coordinates: ('rows', x, y, [..]) maps of palette letters ('.' keep, '_' clear),
    ('clear', x0, y0, x1, y1) and ('recolour', x0, y0, x1, y1, {from: to})"""
    s = spr.copy()
    for e in edits:
        if e[0] == 'erase':                                              # a generated object to take out (the stand-in cat under a petting hand)
            from scipy import ndimage
            _, x0, y0, x1, y1, cols = e; box = np.zeros(s.idx.shape, bool); box[max(0, y0 - oy):max(0, y1 + 1 - oy), max(0, x0 - ox):max(0, x1 + 1 - ox)] = True
            obj = box & np.isin(s.idx, [i for i, c in enumerate(s.pal) if c in cols])
            keep = np.isin(s.idx, [i for i, c in enumerate(s.pal) if c not in cols]) & ~PS.dark(s)
            rim = box & PS.dark(s) & ndimage.binary_dilation(obj, structure=np.ones((3, 3), bool)) & ~ndimage.binary_dilation(keep, structure=np.ones((3, 3), bool))
            s.idx[obj | rim] = -1
            lab, n = ndimage.label(s.idx >= 0, structure=np.ones((3, 3), bool))           # crumbs left in the box go too
            if n > 1:
                sizes = ndimage.sum(s.idx >= 0, lab, index=np.arange(1, n + 1))
                small = np.isin(lab, [i + 1 for i, sz in enumerate(sizes) if sz < 20]) & box; s.idx[small] = -1
            continue
        if e[0] == 'fill':                                               # a plain panel made whole: everything in the box not in its own colours
            _, x0, y0, x1, y1, col, own = e
            sub = s.idx[max(0, y0 - oy):max(0, y1 + 1 - oy), max(0, x0 - ox):max(0, x1 + 1 - ox)]
            ownix = [i for i, cc in enumerate(s.pal) if cc in own]; ci = s.color(col)
            sub[~np.isin(sub, ownix)] = ci
            continue
        if e[0] == 'under':                                              # a pixel map drawn behind whatever is in the keep colours (hands in front of a prop)
            _, x, y, rows, keepc = e
            keepix = set(i for i, cc in enumerate(s.pal) if cc in keepc)
            for r_, row in enumerate(rows):
                for i_, ch in enumerate(row):
                    sx, sy = x + i_ - ox, y + r_ - oy
                    if ch == '.' or not (0 <= sx < s.w and 0 <= sy < s.h) or int(s.idx[sy, sx]) in keepix: continue
                    s.idx[sy, sx] = -1 if ch == '_' else s.color(pal_key[ch])
            continue
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
        if man.get('own_head'):                                          # the whole picture, head and all (a stretch leaning back)
            if man.get('fix'): spr = fix(spr, meta['x'], meta['y'], man['fix'], KEYS[who])
            out[pose] = dict(body=(soften(spr, who), meta['x'], meta['y']), front=None, pts=man.get('pts', {}), props={}, own_head=True)
            continue
        if man.get('fix'): spr = fix(spr, meta['x'], meta['y'], man['fix'], KEYS[who])     # before softening: a recoloured prop is not skin any more
        face = np.zeros(spr.idx.shape, bool); hy, hx = np.where(_nd.binary_dilation(hm, structure=np.ones((3, 3), bool), iterations=2))
        py, px = hy - meta['y'], hx - meta['x']; ok = (py >= 0) & (py < spr.h) & (px >= 0) & (px < spr.w); face[py[ok], px[ok]] = True
        spr = soften(spr, who, keep=face)
        body, front = PS.split(spr, meta['x'], meta['y'], hm, jaw, man.get('front'), hair, None if man.get('keep_neck') else neck, man.get('front_mode', 'all'),
                               base_head=head, chest=None if man.get('keep_chest') else chest,
                               limb=set().union(*[cols for cols, _ in SOFTEN[who]]) | set(PS.PROPS))
        if not man.get('keep_neck') and man.get('neck_fill', True): body = neck_fill(c, torso, head, body, meta['x'], meta['y'])
        if man.get('base_box'):                                          # clothes from the base portrait in a box (a white top that read as a cup)
            bx0, by0, bx1, by1 = man['base_box']; skin = set(SOFTEN[who][0][0])
            for y in range(by0, by1 + 1):
                for x in range(bx0, bx1 + 1):
                    sx, sy = x - meta['x'], y - meta['y']
                    if not (0 <= sx < body.w and 0 <= sy < body.h and 0 <= y < torso.h and 0 <= x < torso.w): continue
                    if torso.idx[y, x] < 0 or (body.idx[sy, sx] >= 0 and body.pal[body.idx[sy, sx]] in skin): continue
                    body.idx[sy, sx] = body.color(torso.pal[torso.idx[y, x]])
        if who in HAIR_FRONT_ROW:                                        # long hair: hands and things held below the collar go in front of it
            front = hair_front(body, meta['x'], meta['y'], HAIR_FRONT_ROW[who], who, front, raw=spr)
        if man.get('fill_holes', True):                                  # repeated: a slit wider than a pixel closes from both sides in turn
            for _ in range(4):
                closed = close_holes(body, meta['x'], meta['y'], head, c.desk, hair)
                if np.array_equal(closed.idx, body.idx): break
                body = closed
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
            moved = shifted(body, meta['x'], meta['y'], box, dx, dy)
            vfront = (hair_front(moved, meta['x'], meta['y'], HAIR_FRONT_ROW[who], who, None), meta['x'], meta['y']) if who in HAIR_FRONT_ROW else entry['front']   # the front moves with the hand
            out[variant] = dict(body=(moved, meta['x'], meta['y']), front=vfront, pts=entry['pts'], props=entry['props'])
    return out
