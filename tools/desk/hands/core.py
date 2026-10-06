#!/usr/bin/env python3
"""
Nutrimatic desk scene - hands/core.py
Version 1.0.0

Created: 2026-10-06 - The hand library's core (to-do round 31, Cole: "a workflow with example hands for every state,
  with a selection process similar to how we did the faces"): build a pose with a candidate hand drawn in, export the
  pose's layers against the figure's exported palette (a patch the live scene takes with D.patchPoses), and quick
  composites as the scene draws a figure (v1.0.0)

A candidate hand is a list of pixel maps on a pose's finished layers, the build's 'paint' ops: (layer, x, y, rows) with
layer 'body' | 'front_body' | 'front', (x, y) in figure-sprite coordinates, rows of letters where '.' keeps a pixel and
'_' clears it. Skin is written in ROLE digits (1 highlight, 2 light, 3 mid, 4 shadow, 5 crease), the same for both
figures; 'k' is the outline; any other letter is the figure's own (poses.KEYS: Cole's shirt 't', Ilinca's blazer 'j',
her white top or cuff 'W', ...). Optional clear boxes ('clear', x0, y0, x1, y1) go first, in the body layer.

Building: only the poses a candidate needs are built (its pose, the pose whose picture it uses, 'rest' for the shoulder
line, and for a greeting 'wave' with the activity), with the candidate's MANUAL entries swapped in for that build only.
"""
import os, sys, json, copy, subprocess
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); DESK = os.path.dirname(HERE); SITE = os.path.dirname(os.path.dirname(DESK))
if DESK not in sys.path: sys.path.insert(0, DESK)
import poses as P                                                       # noqa: E402
from characters import CHARACTERS, layers                               # noqa: E402
import export_js as E                                                   # noqa: E402

# Skin roles -> each figure's own letters (poses.KEYS). Cole: #f9eee0 #f8cda6 #f6af8d #ee947c #dc7f6d; Ilinca: #faebe1
# #f9e2d2 #f1a49b #d18881 #b5705f. Both already in the figures' palettes (Ilinca uses 33 of the format's 36 colours).
ROLES = {'cole': {'1': 'h', '2': 's', '3': 'm', '4': 'a', '5': 'd'}, 'ilinca': {'1': 'h', '2': 's', '3': 'a', '4': 'd', '5': 'D'}}
SKIN_ROLE_HEX = {who: {r: P.KEYS[who][l] for r, l in m.items()} for who, m in ROLES.items()}


def to_keys(who, rows):
    """a map in role digits -> the figure's own letters"""
    m = ROLES[who]
    return [''.join(m.get(ch, ch) for ch in r) for r in rows]


def paint_ops(who, cand):
    """a candidate's maps as the build's 'paint' ops (role digits translated)"""
    return [(lay, x, y, to_keys(who, rows)) for lay, x, y, rows in cand.get('maps', [])]


def needed(who, pose):
    """the poses a build of `pose` needs"""
    ix = P.index(who); man = P.MANUAL.get(who, {}); want = {pose, 'rest'}
    base = man.get(pose, {}).get('base')
    if base: want.add(base)
    for src, frames in ((k, v.get('frames', {})) for k, v in man.items()):
        if pose in frames: want.add(src)
    if pose.endswith('Wave') or pose in ('wave', 'wave2'):
        want.add('wave'); act = pose[:-4] if pose.endswith('Wave') else None
        if act: want.add({'mug': 'mug'}.get(act, act))
    for w in list(want):
        b = man.get(w, {}).get('base')
        if b: want.add(b)
    return {k for k in want if k in ix}


def build(who, overrides=None, poses=None):
    """build the given poses (default: all) with MANUAL entries overridden: overrides = {pose: {key: value}}; a value
    None deletes the key. Returns the build dict (pose -> layers), as poses.build does."""
    c = CHARACTERS[who]; saved_manual = copy.deepcopy(P.MANUAL); saved_index = P.index
    try:
        for pose, ov in (overrides or {}).items():
            entry = dict(P.MANUAL.setdefault(who, {}).get(pose, {}))
            for k, v in ov.items():
                if v is None: entry.pop(k, None)
                else: entry[k] = v
            P.MANUAL[who][pose] = entry
        if poses is not None:
            keep = set()
            for p_ in poses: keep |= needed(who, p_)
            full = saved_index(who)
            P.index = lambda w, _keep=keep, _full=full, _orig=saved_index: ({k: v for k, v in _full.items() if k in _keep} if w == who else _orig(w))
        return P.build(c)
    finally:
        P.MANUAL.clear(); P.MANUAL.update(saved_manual); P.index = saved_index


def candidate_overrides(who, pose, cand):
    """MANUAL overrides that put a candidate into its pose: its clear boxes join the pose's fix list, its maps join the
    pose's paint list (after the pose's own), its frame edits replace the named frames' edits"""
    man = P.MANUAL.get(who, {}).get(pose, {}); ov = {}
    clears = [tuple(b) for b in cand.get('clear', [])]
    drop = set(cand.get('drop_hands', []))                              # HANDS boxes to skip (their clean pass would redo the map)
    if clears: ov['fix'] = list(man.get('fix', [])) + [('clear',) + tuple(b) for b in clears]
    ov['paint'] = list(man.get('paint', [])) + paint_ops(who, cand)
    if cand.get('frames'):
        frames = copy.deepcopy(man.get('frames', {}))
        for name, spec in cand['frames'].items():
            cur = frames.get(name, {}); cur = dict(cur) if isinstance(cur, dict) else {'box': cur[0], 'dx': cur[1], 'dy': cur[2]}
            if spec.get('box') is None: cur.pop('box', None)
            cur['edits'] = [(e[0],) + tuple(e[1:3]) + (to_keys(who, e[3]),) if e[0] == 'rows' else tuple(e) for e in spec.get('edits', [])]
            frames[name] = cur
        ov['frames'] = frames
    if drop: ov['_drop_hands'] = drop
    return ov


def build_candidate(who, pose, cand):
    """the pose (and the poses built from it) with the candidate drawn in"""
    ov = candidate_overrides(who, pose, cand); drop = ov.pop('_drop_hands', set())
    saved = copy.deepcopy(P.HANDS)
    try:
        if drop: P.HANDS.setdefault(who, {})[pose] = [b for b in P.HANDS.get(who, {}).get(pose, []) if tuple(b) not in drop] or None
        if P.HANDS.get(who, {}).get(pose) is None: P.HANDS.get(who, {}).pop(pose, None)
        return build(who, {pose: ov}, poses=[pose] + list(cand.get('also', [])))
    finally:
        P.HANDS.clear(); P.HANDS.update(saved)


_PAL = {}
def exported_palette(who):
    """the palette the scene uses (js/desk-sprites.js), so a patch's indices are valid"""
    if who not in _PAL:
        js = os.path.join(SITE, 'js', 'desk-sprites.js')
        out = subprocess.check_output(['node', '-e', "global.window={}; eval(require('fs').readFileSync(process.argv[1],'utf8')); "
                                       "console.log(JSON.stringify({c: window.NutrimaticDeskArt.cole.pal, i: window.NutrimaticDeskArt.ilinca.pal}))", js])
        d = json.loads(out); _PAL['cole'], _PAL['ilinca'] = d['c'], d['i']
    return _PAL[who]


class NewColour(Exception): pass


def patch(who, built, names):
    """pose entries for D.patchPoses: the layers of `names` in the exported palette (NewColour if a pixel uses a
    colour the figure's palette does not have)"""
    pal = exported_palette(who); out = {}
    def lay(spr, ox, oy):
        missing = {spr.pal[i] for i in spr.used()} - set(pal)
        if missing: raise NewColour('%s: colours not in the palette: %s' % (who, sorted(missing)))
        return E.layer(spr, pal, ox, oy)
    for name in names:
        q = built[name]; b, bx, by = q['body']; entry = dict(b=lay(b, bx, by))
        if q['front'] is not None: f, fx, fy = q['front']; entry['f'] = lay(f, fx, fy)
        if q.get('front_body') is not None: f, fx, fy = q['front_body']; entry['fb'] = lay(f, fx, fy)
        if q['pts']: entry['pts'] = {k: list(v) for k, v in q['pts'].items()}
        if q.get('props'): entry['p'] = {k: lay(s, sx, sy) for k, (s, sx, sy) in q['props'].items()}
        if q.get('own_head'): entry['oh'] = 1
        out[name] = entry
    return out


def composite(who, built, name, box=(-40, -10, 110, 100), face='smile', bg=(233, 223, 204)):
    """an RGBA picture of a pose as the scene draws a figure (body, head with face at headDy, body-front layer,
    face-front layer at headDy, a typing pose's laptop); box in sprite coordinates"""
    from PIL import Image
    c = CHARACTERS[who]; torso, head, hm = layers(c); hdy = P.HEAD_DY.get(who, 0)
    full = c.full(mouth=face if who == 'cole' else ('soft' if face == 'smile' else face)); hd = full.copy(); hd.idx[~hm] = -1
    X0, Y0, X1, Y1 = box; im = Image.new('RGBA', (X1 - X0, Y1 - Y0), bg + (255,))
    q = built[name]; b, bx, by = q['body']
    im.alpha_composite(b.image(), (bx - X0, by - Y0))
    if not q.get('own_head'): im.alpha_composite(hd.image(), (-X0, -Y0 + hdy))
    if q.get('front_body'): f, fx, fy = q['front_body']; im.alpha_composite(f.image(), (fx - X0, fy - Y0))
    if q['front']: f, fx, fy = q['front']; im.alpha_composite(f.image(), (fx - X0, fy - Y0 + hdy))
    if name.startswith('type') and q.get('props', {}).get('laptop'): s, sx, sy = q['props']['laptop']; im.alpha_composite(s.image(), (sx - X0, sy - Y0))
    return im


def load_candidate(path):
    """a candidate file: JSON {who, pose, maps: [[layer, x, y, [rows]]], clear: [[x0,y0,x1,y1]], frames: {...},
    also: [poses], drop_hands: [[box]], meta: {...}}"""
    d = json.load(open(path))
    d['maps'] = [tuple(m) for m in d.get('maps', [])]
    return d
