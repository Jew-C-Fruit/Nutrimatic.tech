#!/usr/bin/env python3
"""
Nutrimatic desk scene - hand_maps.py
Version 1.0.0

Created: 2026-10-28 - Cole's go-live picks from the hand pages put into the poses (r33-live; Cole: "let's focus on getting
  some scenes DONE so we can bring this live"): his thinking TB, her phone P1, his resting pose R2 (with T134, T137, T114),
  his yawn Y1, his handheld D1, his soldering S2, his petting E2 (on his paper) and E3 (the visit); D1's two gaps at the
  desk line closed (FIXES) (v1.0.0)

The hand pages (work/hands/rounds/...) drew each candidate as finished pose layers in the exported format and showed them
in the live scene (D.patchPoses). The picked ones are copied, unchanged, into sprites/picks.json (with the palette each
page was built on; work/r33/live/tools/make_picks.py wrote it). poses.build() calls apply() last, so:
  - the picked layers replace the pose's body / front / body-front layers exactly as Cole saw them: nothing softens,
    fills holes, caps shoulders or draws tools over them (their outline and finish are drawn);
  - a pick may bring the phone layout's own body ('bn': R2's hidden arm runs on to the phone's desk edge, two rows lower
    than the wide room's), its points (S2's iron tip) and props (S2's board); otherwise the pose keeps its own;
  - every pose not picked stays as it was (the coffee frames keep today's resting arm they were drawn on).
Layers made from a picked pose are made again from it (the stroking arm drawn over a kept paper, 'over'); the visit's
laptop graft (petedgeLap: one hand left at the keyboard) was drawn for the old petting pose and goes (see DROP).
"""
import json, os
import numpy as np
from spritekit import Sprite

HERE = os.path.dirname(os.path.abspath(__file__))
PICKS = os.path.join(HERE, 'sprites', 'picks.json')
CH = '0123456789abcdefghijklmnopqrstuvwxyz'
# Poses that are built from an old pose a pick replaced and would no longer match it: not exported. petedgeLap/2 = the old
# petting pose (E0, his right hand across to her) with his left arm at the keyboard (PET_KEYS); E3 strokes her with his
# left hand, so that graft would cut his stroking hand off. The visit does not start while he types (SCENE_ON in the scene).
DROP = {'cole': ['petedgeLap', 'petedgeLap2']}


# Pixels the scene needs that the pages did not show (r33-live checks), per pose: (x, y, colour) in figure coordinates on
# the body layer. D1 (ds, ds1, ds2): where each elbow meets the shirt's bottom edge on the desk line, two and five pixels of
# wall were left (x 10-11 row 87; x 62 row 86, x 62-65 row 87): on a phone those rows are wall above the desk (the wide room
# draws its desk's back edge there, so the page's views did not show them); the shirt's bottom outline runs on to each
# elbow's outline, as it does everywhere else on row 87, and its shade fills row 86.
_D1 = [(10, 87, '#010101'), (11, 87, '#010101'), (62, 86, '#100f13'), (62, 87, '#010101'), (63, 87, '#010101'), (64, 87, '#010101'), (65, 87, '#010101')]
FIXES = {'cole': {'ds': _D1, 'ds1': _D1, 'ds2': _D1}}


def _unrle(d):
    out, i = [], 0
    while i < len(d):
        c = d[i]; i += 1; n, j = 0, i
        while j < len(d) and 'A' <= d[j] <= 'Z': n = n * 26 + ord(d[j]) - 65; j += 1
        out.append(c * (n if j > i else 1)); i = j
    return ''.join(out)


def layer(L, pal):
    """an exported layer (x, y, w, h, d) in the given palette -> (Sprite, x, y) in figure coordinates"""
    s = _unrle(L['d']); assert len(s) == L['w'] * L['h']
    idx = -np.ones((L['h'], L['w']), np.int16); spr = Sprite(idx, [])
    for k, ch in enumerate(s):
        if ch != '.': spr.idx[k // L['w'], k % L['w']] = spr.color(pal[CH.index(ch)])
    return (spr, L['x'], L['y'])


def picks(who=None):
    data = json.load(open(PICKS))['picks']
    return [p for p in data if who is None or p['who'] == who]


def picked(who):
    """{pose: pick code} for the figure"""
    return {n: p['code'] for p in picks(who) for n in p['poses']}


def apply(who, out):
    """out (poses.build's {pose: entry}) with the figure's picks in place"""
    for p in picks(who):
        for name, q in p['poses'].items():
            e = dict(out.get(name, {}))
            for k in ('_tools', 'over', 'body_narrow'): e.pop(k, None)    # (S2 has its tools drawn; 'over' is made again from the pick)
            e['body'] = layer(q['b'], p['pal'])
            for x, y, col in FIXES.get(who, {}).get(name, []):
                b, bx, by = e['body']; assert b.idx[y - by, x - bx] < 0, (name, x, y)   # (only where the page left wall)
                b.put(x - bx, y - by, col)
            e['front'] = layer(q['f'], p['pal']) if 'f' in q else None
            e['front_body'] = layer(q['fb'], p['pal']) if 'fb' in q else None
            if 'bn' in q: e['body_narrow'] = layer(q['bn'], p['pal'])
            if 'pts' in q: e['pts'] = {k: tuple(v) for k, v in q['pts'].items()}
            else: e.setdefault('pts', {})
            if 'p' in q: e['props'] = {k: layer(v, p['pal']) for k, v in q['p'].items()}
            else: e.setdefault('props', {})
            e['pick'] = p['code']
            out[name] = e
    for name in DROP.get(who, []): out.pop(name, None)
    return out
