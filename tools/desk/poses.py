#!/usr/bin/env python3
"""
Nutrimatic desk scene - poses.py
Version 1.0.0

Created: 2026-10-02 - The figures' body poses, from generated pictures, as layers under the base head; the neck, and
  Ilinca's top, taken from the base so every pose joins the same head; front boxes by eye (v1.0.0)

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

# By eye, per pose: the box (base coordinates) whose pixels go over the face, and named points.
MANUAL = {
    'cole': {
        'sip': dict(front=(37, 26, 58, 46), front_mode='props'),
        'drink': dict(front=(40, 28, 61, 58), front_mode='props'),
        'solder': dict(pts={'tip': (35, 82)}),
        'highfive': dict(pts={'hand': (67, 24)}),
        'throw': dict(pts={'hand': (76, 34)}),
        'yawn': dict(front=(30, 31, 52, 47), keep_neck=True),
    },
    'ilinca': {
        'sip': dict(front=(3, 20, 24, 42), front_mode='props'),
        'think': dict(front=(8, 28, 34, 48), front_mode='diff', keep_neck=True),
        'phone': dict(keep_chest=True),
        'carry': dict(keep_chest=True),
        'surprise': dict(keep_chest=True),
        'drink': dict(front=(-2, 16, 24, 48), front_mode='props'),
        'yawn': dict(front=(12, 24, 36, 42), front_mode='diff', keep_neck=True),
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


# the neck, between the jaw and the collar, in base coordinates: x range and the collar row
NECK = {'cole': (28, 50, 49), 'ilinca': (23, 37, 49)}


def neck_patch(c, torso, jaw):
    """pixels of the base torso just under the jaw: (torso sprite, mask)"""
    x0, x1, collar = NECK[c.name]; m = np.zeros(torso.idx.shape, dtype=bool)
    for x in range(x0, x1 + 1):
        top = jaw.get(x, 0) + 1
        m[top:collar + 1, x] = True
    return torso, m & (torso.idx >= 0)


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
        body, front = PS.split(spr, meta['x'], meta['y'], hm, jaw, man.get('front'), hair, None if man.get('keep_neck') else neck, man.get('front_mode', 'all'),
                               base_head=head, chest=None if man.get('keep_chest') else chest)
        out[pose] = dict(body=(body, meta['x'], meta['y']), front=(front, meta['x'], meta['y']) if front is not None and (front.idx >= 0).any() else None, pts=man.get('pts', {}))
    return out
