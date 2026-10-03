#!/usr/bin/env python3
"""
Nutrimatic desk scene - walk_rig.py
Version 2.0.0

Created: 2026-10-03 - Maker's walk as a rigged cycle (Cole: "Walking cycle needs more stages and should be based on proper
  animal walk cycle animation techniques"; the generated frames moved only one hind leg) (v1.0.0)
Modified: 2026-10-03 - Rewritten from scratch after Cole's verdict on the first rig ("completely wrong"), following
  docs/animal-walk-cycles.md: a cat's lateral-sequence walk in ten frames of 3 px (hind paw, then the fore paw on the
  same side), duty factor 0.7, the hind paw landing in the fore paw's print, every planted paw fixed to the desk, legs
  turning about a hip and a shoulder inside the body, the fore paw flicking back as it lifts and the hock folding in the
  swing, the body sinking a pixel as each fore paw takes her weight and the raised tail following a frame later; drawn
  on her own standing body (the kneading pose), so walking and kneading share one body (v2.0.0)

walk_rig.py - Maker's walk cycle: four legs drawn for each frame on her standing body.

The gait (see docs/animal-walk-cycles.md for where every number comes from):
  - N = 10 frames a cycle, 3 px a frame: a 30 px stride, 0.83 s a cycle at the scene's 12 frames a second
  - lateral sequence: near hind lands in frame 0, near fore in 2, far hind in 5, far fore in 7 (she faces right, so the
    near legs are her right legs); each fore paw lands 0.2 of a cycle after the hind paw on its side
  - each paw is on the desk for 7 frames (duty factor 0.7) and in the air for 3: lift, pass, reach
  - two or three paws are always down; the two-paw moments are both paws of one side (as in cats)
  - a planted paw is one fixed stamp that moves back exactly 3 px a frame, so it stays put on the desk while she moves
  - the hip and the shoulder are 24 px apart, 0.8 of a stride, so each hind paw lands where the fore paw was

  frames(stand, colours) -> N Sprites the size of `stand` (60 x 54), the paws' bottom on its bottom row; bob=False
                            leaves out the body's dip and the tail's follow-through
  contacts(f)            -> {leg: (heel column, on the desk?)} for checking a frame (walk_check.py)
"""
import math
import numpy as np
from spritekit import Sprite

N, SPEED, STANCE = 10, 3, 7                 # frames a cycle, px a frame, frames a paw is down
CONTACT = {'RH': 0, 'RF': 2, 'LH': 5, 'LF': 7}   # frame each paw lands (lateral sequence)
NEAR = {'RH': True, 'RF': True, 'LH': False, 'LF': False}
KIND = {'RH': 'hind', 'LH': 'hind', 'RF': 'fore', 'LF': 'fore'}
HIP, SHOULDER = 15.0, 39.0                  # pivot columns of the hind and fore legs, inside the body
HEEL = {'fore': 45, 'hind': 21}             # heel column of a paw as it lands; 3 px back each frame on the ground
GROUND = 53                                 # the paws' bottom row (the sprite's last row), near and far alike
DOWN = (2, 3, 7, 8)                         # frames her body sinks a pixel: as each fore paw lands and takes her weight
TIP = (10, 12)                              # the raised tail's top (rows above 10, columns left of 12) follows a frame late

# where the stand sprite's legs are cut off: the lowest body row for each column (haunch, belly, chest)
def _bottom(x):
    if x <= 7: return 39
    if x == 8: return 40
    if x in (9, 17): return 41
    if 10 <= x <= 16: return 42
    if x == 18: return 40
    if 19 <= x <= 33: return 39
    if 34 <= x <= 44: return 41
    if x == 45: return 40
    return 39


def body(stand, LINE, SHADE):
    """the stand sprite without its legs: everything below the cut goes, the new bottom edge gets its outline; the line
    inside the chest where the generated near foreleg met the belly is smoothed into the coat (the legs move now)"""
    b = stand.copy(); h, w = b.idx.shape
    for x in range(w):
        b.idx[_bottom(x) + 1:, x] = -1
    for y in range(33, 40):                                                  # the old foreleg's back edge, column 33
        if b.idx[y, 33] >= 0 and b.pal[b.idx[y, 33]] == LINE: b.idx[y, 33] = b.color(SHADE)
    solid = b.idx >= 0
    for y in range(36, h):
        for x in range(w):
            if solid[y, x] and any(not (0 <= yy < h and 0 <= xx < w) or not solid[yy, xx] for yy, xx in ((y + 1, x), (y, x - 1), (y, x + 1))):
                b.idx[y, x] = b.color(LINE)
    return b


# ---------------- the legs ----------------
# A leg is drawn as rows of pixels between a left and a right column ("spans"), the way a pixel artist draws a limb of
# even width, then shaded: outline at both ends, the back edge a step darker, a light edge in front on the upper leg.
# Paws on the ground are stamps (rows of letters, the heel in column 0, the last row on the ground row).
PAW = {('fore', 'flat'): ['KDSSSK.', 'KDSSSSK', '.KKKKKK'],
       ('fore', 'tilt'): ['KDSSSK.', 'KKDSSSK', '...KKKK'],      # last frame down: the heel lifts, the toes stay
       ('hind', 'flat'): ['KDSSK..', 'KDSSSSK', '.KKKKKK'],
       ('hind', 'tilt'): ['KDSSK..', 'KKDSSSK', '...KKKK']}

# Legs in the air: joints (x, row, width) from inside the body down to the wrist or the foot, the paw's rows given as
# spans (row: (left, right)), and the row of the hock where the heel bone sticks out behind. Near legs; far legs are
# the same, darker and behind the body.
SWING = {
    # fore, lift: the paw has just flicked up off the desk and folds back under the bent wrist, 2 px up
    ('fore', 0): dict(joints=[(36.0, 36, 6), (34.5, 47, 6)], paw={48: (31, 36), 49: (30, 35), 50: (29, 34), 51: (30, 33)}),
    # fore, passing: the forearm swings forward under the chest, the paw still hanging from the bent wrist, 3 px up
    ('fore', 1): dict(joints=[(38.5, 36, 6), (41.0, 47, 6)], paw={48: (38, 43), 49: (37, 42), 50: (38, 41)}),
    # fore, reach: the leg straightens forward, the paw opens toward the desk a pixel above it
    ('fore', 2): dict(joints=[(41.5, 36, 6), (46.5, 49, 6)], paw={50: (44, 50), 51: (44, 51), 52: (45, 50)}),
    # hind, lift: the toes have just left the desk behind her; the hock is up, the foot hangs toes down, 2 px up
    ('hind', 0): dict(joints=[(13.5, 36, 9), (11.5, 42, 7), (7.5, 46, 5), (6.0, 49, 5)], paw={50: (4, 8), 51: (5, 7)}, hock=46),
    # hind, passing: knee forward, hock folded, the paw under the hip three pixels up
    ('hind', 1): dict(joints=[(15.0, 36, 9), (15.5, 42, 7), (12.5, 46, 5), (14.0, 48, 5)], paw={49: (12, 17), 50: (13, 16)}, hock=46),
    # hind, reach: the leg swings forward and opens, the paw a pixel above the desk ahead of the hip
    ('hind', 2): dict(joints=[(16.5, 36, 9), (18.5, 42, 7), (18.0, 47, 5), (20.5, 50, 5)], paw={51: (18, 24), 52: (19, 24)}, hock=47),
}
# the hind leg on the desk, frame by frame (k = 0 lands ... 6 heel up): knee and hock centres. Landing, the foot leans
# forward from the hock; upright in the middle; pushing, the shin slants back more than the foot, so the heel always
# points back (the hock bends the other way from the knee)
HIND_KNEE = [19.5, 18.5, 17.5, 16.5, 15.0, 13.5, 12.0]       # row 42
HIND_HOCK = [20.0, 17.8, 15.3, 12.8, 10.5, 8.5, 6.8]         # row 47 (46 in the last frame: the heel lifts)


def _limb(joints):
    """spans of a limb through joints (x centre, row, width): between two joints the front edge and the back edge each
    run as a straight line, so both outlines are clean even stair steps (the limb narrows by its edges converging)"""
    rnd = lambda v: int(math.floor(v + 0.5))
    out = {}
    for (x0, y0, w0), (x1, y1, w1) in zip(joints, joints[1:]):
        f0, f1, b0, b1 = x0 + (w0 - 1) / 2, x1 + (w1 - 1) / 2, x0 - (w0 - 1) / 2, x1 - (w1 - 1) / 2
        for r in range(y0, y1 + 1):
            t = 0 if y1 == y0 else (r - y0) / (y1 - y0)
            a, b = rnd(b0 + (b1 - b0) * t), rnd(f0 + (f1 - f0) * t)
            if r in out: a, b = min(a, out[r][0]), max(b, out[r][1])
            out[r] = (a, b)
    return out


def _paint(spans, G):
    """spans -> {(row, x): letter}: K outline, D back edge, S coat, F light front edge (upper leg only)"""
    px = {}
    for r, (a, b) in spans.items():
        for x in range(a, b + 1):
            if x in (a, b): ch = 'K'
            elif x == a + 1: ch = 'D'
            elif x == b - 1 and r <= G - 6: ch = 'F'
            else: ch = 'S'
            px[(r, x)] = ch
    return px


def stance_leg(kind, k, G):
    """a leg in its k-th frame on the desk: it turns about its pivot, the paw stamp stays flat (tilted in the last)"""
    heel = HEEL[kind] - SPEED * k; c = heel + 2.5                          # paw centre under the leg
    if kind == 'fore':
        top = SHOULDER + 0.45 * (c - SHOULDER)                              # the leg's top slides under the chest
        spans = _limb([(top, 36, 6), (c, G - 3, 6)])                         # a straight forearm of even width
    else:
        knee, hock = HIND_KNEE[k], HIND_HOCK[k]; hr = G - 6 if k < STANCE - 1 else G - 7
        spans = _limb([(HIP + 0.45 * (knee - HIP), 36, 9), (knee, G - 11, 7), (hock, hr, 5), (heel + 2, G - 3, 5)])
        a, b = spans[hr]; spans[hr] = (a - 1, b)                             # the hock: the heel bone sticks out behind
    px = _paint(spans, G)
    for key in [q for q in px if q[0] >= G - 2]: del px[key]
    for i, row in enumerate(PAW[(kind, 'tilt' if k == STANCE - 1 else 'flat')]):
        for j, ch in enumerate(row):
            if ch != '.': px[(G - 2 + i, heel + j)] = ch
    return px, heel


def swing_leg(kind, s, G):
    q = SWING[(kind, s)]; spans = _limb(q['joints'])
    if 'hock' in q: a, b = spans[q['hock']]; spans[q['hock']] = (a - 1, b)
    spans.update(q['paw'])
    px = _paint(spans, G); last = max(q['paw'])
    for (r, x) in list(px):
        if r >= last - 1 and px[(r, x)] in 'SF': px[(r, x)] = 'D'          # the paw a shade darker, as on the desk
        if r == last: px[(r, x)] = 'K'                                        # and its underside outlined
    return px


def leg_pixels(leg, f):
    k = (f - CONTACT[leg]) % N; G = GROUND
    if k < STANCE: px, heel = stance_leg(KIND[leg], k, G); return px, heel, True
    return swing_leg(KIND[leg], k - STANCE, G), None, False


def contacts(f):
    """{leg: (heel column or None, on the ground)} in frame f"""
    out = {}
    for leg in CONTACT:
        _, heel, down = leg_pixels(leg, f); out[leg] = (heel, down)
    return out


def _sink(b, f):
    """the body a pixel lower in the DOWN frames (the legs then reach a pixel less far: the paws stay on the desk), and the
    top of the raised tail following a frame later: the upright part of the tail stretches or shortens by a row"""
    dy = 1 if f in DOWN else 0; tip = 1 if (f - 1) % N in DOWN else 0; cut, cols = TIP
    out = b.copy(); out.idx[:] = -1
    out.idx[dy:, :] = b.idx[:b.h - dy, :]
    if tip != dy:
        out.idx[:cut + 1, :cols] = -1
        out.idx[tip:cut + tip, :cols] = b.idx[:cut, :cols]                   # the tip where it follows to
        for r in range(cut + tip, cut + dy + 1): out.idx[r, :cols] = b.idx[cut, :cols]   # the upright part, a row longer if needed
    return out


def frames(stand, colours, bob=True):
    """stand: the standing sprite (big eyes, open or shut); colours: dict LINE, DEEP, SHADE, FILL"""
    LINE, DEEP, SHADE, FILL = (colours[k] for k in ('LINE', 'DEEP', 'SHADE', 'FILL'))
    near_c = {'K': LINE, 'D': DEEP, 'S': SHADE, 'F': FILL}
    far_c = {'K': LINE, 'D': DEEP, 'S': DEEP, 'F': DEEP}                    # the far legs all in the deepest coat grey
    base = body(stand, LINE, SHADE)
    out = []
    for f in range(N):
        bd = _sink(base, f) if bob else base.copy()
        B = bd.idx >= 0; h, w = B.shape
        res = bd.copy(); res.idx[:] = -1
        legs = {leg: leg_pixels(leg, f)[0] for leg in CONTACT}
        for leg in ('LH', 'LF'):                                             # far legs, behind the body
            for (y, x), ch in legs[leg].items():
                if 0 <= y < h and 0 <= x < w and not B[y, x]: res.idx[y, x] = res.color(far_c[ch])
        for y, x in zip(*np.where(B)): res.idx[y, x] = bd.idx[y, x]
        for leg in ('RH', 'RF'):                                             # near legs, in front
            for (y, x), ch in legs[leg].items():
                if not (0 <= y < h and 0 <= x < w): continue
                if B[y, x]:
                    # inside the body the leg is the body, except that the body's bottom line opens where the leg leaves it
                    if bd.pal[bd.idx[y, x]] == LINE and y >= 36 and ch != 'K': res.idx[y, x] = res.color(SHADE)
                    continue
                res.idx[y, x] = res.color(near_c[ch])
        out.append(Sprite(res.idx.copy(), list(res.pal)))
    return out
