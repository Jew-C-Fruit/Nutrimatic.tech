#!/usr/bin/env python3
"""
Nutrimatic desk scene - hands/slots.py
Version 1.0.0

Created: 2026-10-06 - Where each hand state goes (the hand library, to-do round 31): for every state its pose, the
  box the old hand is cleared from, where the drawn hand joins the forearm, the layer it is painted on, the object it
  holds, how the scene shows it, and the poses built from it. First the five anchors of the style round (v1.0.0)

Coordinates are figure-sprite pixels (Cole 75x97, desk row 88; Ilinca 63x94, desk row 84, her head drawn 3 rows lower).
VL / VR = the hand on the viewer's left / right (VL is the figure's own right hand).

A slot:
  who, pose          the pose the hand is drawn into (frames and poses built from it follow: see `dependents`)
  hands              which hands the candidate draws: 'VL', 'VR' or both
  clear              boxes (x0, y0, x1, y1) cleared in the picture before the split (the old hand and object go)
  joins              per hand: the forearm's cut, as the rows/columns where the drawn hand must meet the arm left in
                     place: {'VL': {'edge': 'top'|'bottom'|'left'|'right', 'at': n, 'span': (a, b)}}
  layer              'body' (behind her hair and the face) or 'front_body' (Ilinca's hands in front of her hair)
  view               the box (sprite coordinates) the 8x views show
  object             the canonical object drawn with the hand (None, 'mug', ...)
  code               how the scene holds the state for a capture (JS with D = window.NutrimaticDesk)
  frames             motion frames the candidate must also give (name -> what moves)
  base_shape         A resting, B flat palm, C open raised, D fist, E cylinder grip, F pinch, G at the face, H stroking
  size               target hand box (w, h) at style size x1.0, from the figure's forearm width (R8)
"""

# The one mug (to-do T47: one mug size everywhere): the desk mug's shape, 14 x 12, in colours both figures' palettes
# already have (the desk prop's own reds are not in them, and Ilinca uses 33 of the format's 36 colours). Handle on the
# right; mirror the rows for a handle on the left. k outline, r red, R shade, p light (Cole: #ff5a72; for Ilinca the
# same letter maps to her red, see MUG_KEYS), g the handle's inner grey.
MUG = ['kkkkkkkkkk....',
       'krrrrrrrrrkkk.',
       'kprrrrrrrRkggk',
       'kprrrrrrrRk.gk',
       'kprrrrrrrRk..k',
       'kprrrrrrrRk..k',
       'kprrrrrrrRk.gk',
       'kprrrrrrrRkggk',
       'krrrrrrrrRkkk.',
       'kRrrrrrrrRk...',
       'kRRrrrrrRRk...',
       '.kkkkkkkkk....']
MUG_KEYS = {'cole': {'p': 'p'}, 'ilinca': {'p': 'r'}}       # Ilinca's palette has no light red: her mug's light side is red


def mug(who, flip=False):
    rows = [''.join(MUG_KEYS[who].get(ch, ch) for ch in r) for r in MUG]
    return [r[::-1] for r in rows] if flip else rows


SLOTS = {
    # Cole waving: the raised open hand (VL); every greeting (restWave, typeWave, ...) takes it through wave_from
    'cole.wave': dict(who='cole', pose='wave', hands=['VL'], clear=[(-8, -2, 17, 31)],
                      joins={'VL': dict(edge='bottom', at=32, span=(-3, 12))}, layer='body', view=(-14, -6, 30, 50),
                      object=None, base_shape='C', size=(16, 22),
                      code="D.review({cole:'rest', ilinca:'rest', greet:'wave', relay:false}); D.step(4); D.react('cole'); D.step(10)",
                      dependents=['restWave', 'typeWave', 'writeWave', 'solderWave', 'mugWave', 'thinkWave'], frames={}),
    # Cole resting: both hands at the inner ends of the forearms on the desk top (and rest1, the fidget)
    'cole.rest': dict(who='cole', pose='rest', hands=['VL', 'VR'], clear=[(2, 85, 70, 99)],
                      joins={'VL': dict(edge='left', at=8, span=(84, 90)), 'VR': dict(edge='right', at=64, span=(84, 90))},
                      layer='body', view=(-14, 66, 86, 100), object=None, base_shape='A', size=(20, 10),
                      code="D.review({cole:'rest', ilinca:'rest'})", dependents=['rest1', 'restWave'],
                      frames={'rest1': 'one hand shifts or lifts its fingers a pixel (the fidget)'}),
    # Cole with his coffee on the desk: VL holds the mug by its handle, VR rests beside it or steadies it
    'cole.mug': dict(who='cole', pose='mug', hands=['VL', 'VR'], clear=[(20, 70, 68, 95)],
                     joins={'VL': dict(edge='left', at=21, span=(73, 89)), 'VR': dict(edge='right', at=66, span=(76, 91))},
                     layer='body', view=(-12, 60, 84, 100), object='mug', base_shape='E', size=(15, 12),
                     code="D.review({cole:'coffee', ilinca:'rest'})", dependents=['mugWave'], frames={}),   # (coffee shows mug, then sip after 12 ticks)
    # Ilinca with her coffee on the desk: VL holds the mug, VR is her desk hand (unchanged in the style round)
    'ilinca.mug': dict(who='ilinca', pose='mug', hands=['VL'], clear=[(-10, 60, 17, 87)],
                       joins={'VL': dict(edge='left', at=-8, span=(66, 82))}, layer='front_body', view=(-12, 56, 50, 92),
                       object='mug', base_shape='E', size=(14, 11),
                       code="D.review({cole:'rest', ilinca:'coffee'})", dependents=[], frames={}),
    # Ilinca talking with her hand up (VL raised beside her hair, open, gesturing); VR stays on the desk
    'ilinca.talk': dict(who='ilinca', pose='talk', hands=['VL'], clear=[(-20, 28, 3, 49)],
                        joins={'VL': dict(edge='bottom', at=50, span=(-6, 3))}, layer='front_body', view=(-22, 24, 14, 66),
                        object=None, base_shape='C', size=(15, 18),
                        code="D.review({cole:'rest', ilinca:'talk'})", dependents=[], frames={}),
}

ANCHORS = ['cole.wave', 'cole.rest', 'cole.mug', 'ilinca.mug', 'ilinca.talk']

# Fixed points shown beside the style candidates (they passed Cole's review, or rest on a real reference): not redrawn.
REFERENCE_POINTS = {'ilinca.rest': 'her clasped hands (go live)', 'ilinca.wave': 'her wave (go live)',
                    'cole.ds': 'the DS grip (go live; drawn from his photo)', 'ilinca.drink': 'the tilted shaker in her fist'}
