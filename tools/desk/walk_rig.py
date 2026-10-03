#!/usr/bin/env python3
"""
Nutrimatic desk scene - walk_rig.py
Version 1.0.0

Created: 2026-10-03 - Maker's walk as a rigged cycle (Cole: "Walking cycle needs more stages and should be based on proper
  animal walk cycle animation techniques"; the generated frames moved only one hind leg) (v1.0.0)

The body, head and tail come from a generated walking picture with its legs taken off; the four legs are drawn for each
frame from a walk-cycle rig, the way a quadruped walk is animated:

  - a lateral-sequence walk, as cats walk (Muybridge, Animal Locomotion, plate 716: a cat walking): the feet land
    left hind, left fore, right hind, right fore, each a quarter of a cycle after the last
  - each foot is on the ground for 60% of the cycle (stance) and in the air for 40% (swing), so two or three feet are
    always down
  - a foot on the ground stays planted: it slides back under the body exactly as fast as the cat walks forward
    (3 px a frame, 12 frames a cycle), so nothing skates
  - in the swing the foot lifts on an arc and eases in; the fore leg's wrist folds the paw back as it leaves the ground,
    the hind leg's hock flexes; elbows point back, knees forward, hocks back
  - the body dips a pixel twice a cycle, as each pair of legs passes under it; the raised tail sways a little behind
  - the near legs (her left side, toward us) are drawn over the body in her coat colours; the far legs behind it, darker

  frames(body, colours)   -> 12 Sprites (same size); body = a generated walking picture of her, reduced, legs and all
                             (they are cut here: sources/maker-walkbody-seed9815.png, a frame the model drew over the rig)
"""
import math
import numpy as np
from scipy import ndimage
from spritekit import Sprite

N = 12                    # frames per cycle
SPEED = 3                 # px per frame (the scene moves her 3 px a tick)
DUTY = 0.6                # share of the cycle a foot is on the ground
R = SPEED * DUTY * N / 2  # half the stance stroke, so stance feet stay planted
BELLY = 40                # the body is cut below this row (its generated legs go)
GROUND = 56               # the bottom row of her paws
TAIL = (21, 12)           # the raised tail: rows above, columns left of
# the legs: anchor (x, y) on the body, segment lengths, neutral foot offset from the anchor, lift, phase, near or far
LEGS = [  # far legs first (drawn behind the body), then near
    dict(name='RH', kind='hind', anchor=(20, 33), lens=(10, 10, 7), neutral=0, lift=3, phase=0.5, near=False),
    dict(name='RF', kind='fore', anchor=(46, 33), lens=(8, 12, 4), neutral=1, lift=4, phase=0.75, near=False),
    dict(name='LH', kind='hind', anchor=(17, 34), lens=(10, 10, 7), neutral=0, lift=3, phase=0.0, near=True),
    dict(name='LF', kind='fore', anchor=(50, 34), lens=(8, 12, 4), neutral=1, lift=4, phase=0.25, near=True),
]
# width of the leg (outline included) at hip/shoulder, knee/elbow, hock/wrist, paw: as thick as the generated cat's legs
WIDTH = {'hind': (9.0, 8.0, 6.6, 7.0), 'fore': (8.6, 8.0, 7.0, 7.4)}
HAUNCH = (6.0, 8.2)       # the hind thigh's oval (half width, half height), turned with the thigh
CORNERS = [(10, 18, 19.5, 34.0, 6.5), (40, 50, 40.0, 33.5, 7.5)]   # body corners to round: columns, circle centre, radius


def ease(s): return s * s * (3 - 2 * s)


def foot(leg, phase):
    """foot position relative to the anchor (dx, dy from the ground), and how far into the swing (0 = planted)"""
    p = (phase + leg['phase']) % 1.0
    if p < DUTY:
        s = p / DUTY; return leg['neutral'] + R - 2 * R * s, 0.0, 0.0
    s = (p - DUTY) / (1 - DUTY)
    return leg['neutral'] - R + 2 * R * ease(s), leg['lift'] * math.sin(math.pi * s), s


def ik(a, t, la, lb, bend):
    """2-bone IK: the joint between a and t, with the bend toward +x (bend = 1) or -x (bend = -1)"""
    ax, ay = a; tx, ty = t; dx, dy = tx - ax, ty - ay; d = max(abs(la - lb) + 0.01, min(la + lb - 0.01, math.hypot(dx, dy)))
    base = math.atan2(dy, dx); off = math.acos(max(-1, min(1, (la * la + d * d - lb * lb) / (2 * la * d))))
    best = None
    for sgn in (1, -1):
        th = base + sgn * off; j = (ax + la * math.cos(th), ay + la * math.sin(th))
        side = (tx - ax) * (j[1] - ay) - (ty - ay) * (j[0] - ax)          # which side of a->t the joint is on
        score = (j[0] - (ax + tx) / 2) * bend
        if best is None or score > best[0]: best = (score, j)
    return best[1]


def leg_points(leg, phase, bob):
    ax, ay = leg['anchor']; ay -= bob
    fx, lift, swing = foot(leg, phase); px_, py_ = ax + fx, GROUND - 1 - lift
    l1, l2, l3 = leg['lens']
    if leg['kind'] == 'hind':
        ang = math.radians(68 - 30 * math.sin(math.pi * swing))          # the metatarsus: steep when planted, flexes back in the swing
        hock = (px_ - l3 * math.cos(ang), py_ - l3 * math.sin(ang))
        knee = ik((ax, ay), hock, l1, l2, +1)                            # knee forward
        return [(ax, ay), knee, hock, (px_, py_)]
    fold = math.sin(math.pi * min(1, swing * 1.6)) if swing > 0 else 0.0  # the wrist folds early in the swing
    wrist = (px_ + 0.6 + 2.2 * fold, py_ - l3 + 1.0 * fold)
    elbow = ik((ax, ay), wrist, l1, l2, -1)                              # elbow back
    return [(ax, ay), elbow, wrist, (px_ - 1.2 * fold, py_)]


def stamp(mask, pts, widths, h, w):
    yy, xx = np.mgrid[0:h, 0:w]
    for (x0, y0), (x1, y1), r0, r1 in zip(pts, pts[1:], widths, widths[1:]):
        L = max(1.0, math.hypot(x1 - x0, y1 - y0))
        for k in range(int(L * 3) + 1):
            t = k / max(1, int(L * 3)); cx, cy = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t; r = (r0 + (r1 - r0) * t) / 2
            mask |= (xx + 0.5 - cx) ** 2 + (yy + 0.5 - cy) ** 2 <= r * r
    return mask


def paw(mask, x, y, h, w, flat=True):
    yy, xx = np.mgrid[0:h, 0:w]
    rx, ry = (3.7, 2.1) if flat else (3.0, 2.3)
    mask |= ((xx + 0.5 - x) / rx) ** 2 + ((yy + 0.5 - (y - 0.8)) / ry) ** 2 <= 1.0
    return mask


def haunch(mask, hip, knee, h, w, scale=1.0):
    """the hind thigh: an oval from the hip toward the knee"""
    yy, xx = np.mgrid[0:h, 0:w]; (hx, hy), (kx, ky) = hip, knee
    cx, cy = hx + (kx - hx) * 0.45, hy + (ky - hy) * 0.45; ang = math.atan2(ky - hy, kx - hx)
    a, b = HAUNCH[1] * scale, HAUNCH[0] * scale; c, s = math.cos(ang), math.sin(ang)
    u = (xx + 0.5 - cx) * c + (yy + 0.5 - cy) * s; v = -(xx + 0.5 - cx) * s + (yy + 0.5 - cy) * c
    mask |= (u / a) ** 2 + (v / b) ** 2 <= 1.0
    return mask


def frames(body, colours, extra_top=3):
    """body: a Sprite of her walking (its legs are cut away here); colours: dict LINE, DEEP, SHADE, FILL, LIGHT"""
    LINE, DEEP, SHADE, FILL, LIGHT = (colours[k] for k in ('LINE', 'DEEP', 'SHADE', 'FILL', 'LIGHT'))
    base = body.pad(top=extra_top); off = extra_top
    for leg in LEGS: leg['_a'] = (leg['anchor'][0], leg['anchor'][1] + off)
    cut = base.copy(); cut.idx[BELLY + off + 1:, :] = -1                 # the generated legs go
    for (x0, x1, cx, cy, r) in CORNERS:                                  # round the cut body's lower corners (rump, chest)
        for y in range(BELLY - 6 + off, BELLY + off + 1):
            for x in range(x0, x1 + 1):
                if (x + 0.5 - cx) ** 2 + (y + 0.5 - (cy + off)) ** 2 > r * r: cut.idx[y, x] = -1
    solid = cut.idx >= 0; below_empty = np.zeros_like(solid); below_empty[:-1] = ~solid[1:]
    edge = solid & below_empty; edge[:BELLY + off - 2, :] = False
    cut.idx[edge] = cut.color(LINE)                                      # the belly gets its outline back
    tail = np.zeros_like(solid); tail[:TAIL[0] + off, :TAIL[1]] = True; tail &= solid
    h, w = cut.idx.shape; out = []
    for i in range(N):
        ph = i / N; bob = 1 if math.cos(4 * math.pi * ph) > 0.35 else 0
        fr = cut.copy(); fr.idx[:] = -1
        # body (with the tail swaying a pixel or two behind the step) moved up by the bob
        sway = 1.6 * math.sin(2 * math.pi * ph - 0.9)
        src = cut.idx.copy()
        for y in range(h):
            for x in range(w):
                v = src[y, x]
                if v < 0: continue
                dx = int(round(sway * (1 - (y - off) / float(TAIL[0])))) if tail[y, x] else 0
                ny, nx = y - bob, x + dx
                if 0 <= ny < h and 0 <= nx < w: fr.idx[ny, nx] = v
        body_mask = fr.idx >= 0
        layers = []
        for leg in LEGS:
            a = leg['_a']; L = dict(leg); L['anchor'] = a
            pts = leg_points(L, ph, bob)
            pts = [(x, y + 0) for x, y in pts]; pts[-1] = (pts[-1][0], pts[-1][1] + off)
            m = np.zeros((h, w), bool); m = stamp(m, pts, WIDTH[leg['kind']], h, w)
            if leg['kind'] == 'hind': m = haunch(m, pts[0], pts[1], h, w, 1.0 if leg['near'] else 0.85)
            fx, fy = pts[-1]; m = paw(m, fx, fy + 0.5, h, w, flat=(foot(leg, ph)[2] == 0))
            layers.append((leg, m, pts))
        def paint(target, leg, m, pts, behind):
            inner = ndimage.binary_erosion(m, structure=np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]], bool))
            rim = m & ~inner
            # rear side of the leg: left of its centreline (she faces right) is shaded
            cx = np.full(h, np.nan)
            for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
                for k in range(40):
                    t = k / 39; y = int(round(y0 + (y1 - y0) * t)); x = x0 + (x1 - x0) * t
                    if 0 <= y < h: cx[y] = x
            near_col, rear_col = (SHADE, DEEP) if leg['near'] else (SHADE, DEEP)  # legs are in the shade under her, as in the generated cat
            for y, x in zip(*np.where(m)):
                if behind and body_mask[y, x]: continue                   # far legs: the body hides their tops
                if leg['near'] and body_mask[y, x] and y < BELLY + off - bob:   # near legs merge into the body above the belly
                    if rim[y, x] and not np.isnan(cx[y]) and x < cx[y]: target.idx[y, x] = target.color(SHADE)
                    continue
                if rim[y, x]: target.idx[y, x] = target.color(LINE); continue
                rear = (not np.isnan(cx[y])) and x + 0.5 < cx[y] - 1.4
                front = (not np.isnan(cx[y])) and x + 0.5 > cx[y] + 1.6
                col = rear_col if rear else near_col
                if front and leg['near'] and y < GROUND + off - 3: col = FILL      # light on the front of the near legs
                if not leg['near'] and not front: col = DEEP                       # the far legs a step darker
                target.idx[y, x] = target.color(col)
        res = fr.copy(); res.idx[:] = -1
        for leg, m, pts in layers:                                       # far legs, behind the body
            if not leg['near']: paint(res, leg, m, pts, behind=True)
        for y, x in zip(*np.where(body_mask)): res.idx[y, x] = res.color(fr.pal[fr.idx[y, x]])
        for leg, m, pts in layers:                                       # near legs
            if leg['near']: paint(res, leg, m, pts, behind=False)
        out.append(Sprite(res.idx[:GROUND + off + 1].copy(), list(res.pal)))   # the paws' bottom is the sprite's bottom row
    return out
