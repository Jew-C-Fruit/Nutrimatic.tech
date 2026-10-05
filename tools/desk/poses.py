#!/usr/bin/env python3
"""
Nutrimatic desk scene - poses.py
Version 1.10.0

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
Modified: 2026-10-03 - Note 5: a new chin-on-fist picture for Ilinca; her forearm crosses in front of her hair, so in
  boxes round the fist and the crossing all the pose drew except its own hair goes in front (front mode 'nothair', front
  boxes may be several) (v1.4.2)
Modified: 2026-10-03 - Note 6: the neck patch follows the portrait's round neckline (it had squared Cole's T-shirt off); a
  new rest pose for Cole with his hands flat on the desk, apart (v1.4.3)
Modified: 2026-10-03 - Note 7: a hole in Ilinca's top (the cut-out took its grey shadow for the wall) filled; tiny gaps
  enclosed in any pose are filled automatically (pinholes) (v1.4.4)
Modified: 2026-10-03 - Note 8: Ilinca's laptop squared off with an outline all round and her hands at its sides redrawn
  clean; props are lifted from the pose before its head area is cut (the cat showed through a gap at the top of her
  laptop when it was drawn over her) (v1.4.5)
Modified: 2026-10-03 - Note 9: small motion frames for every activity (typing forearms, a hand to the trackpad, thumbs on
  the console, a fidgeting hand, a phone scrolled, a second soldering position); a frame may edit pixels as well as
  shift a box; Cole types from the front with his hands hidden behind the screen; the writing paper and the soldering
  boards edge-on, as the flat front view of the desk needs, and Cole's laptop standing on the desk line; hands under
  the desk ('hide') for both, for when Maker walks by (v1.5.0)
Modified: 2026-10-03 - The soldering boards are props, so they stay on the desk while Cole waves smoke away (v1.5.1)
Modified: 2026-10-04 - Petting at the desk's front edge (note 12): petedge poses, made with Maker pasted where she now
  lies; the 'cat' fix clears her outline in the picture but the hand on her (v1.6.0)
Modified: 2026-10-04 - Typing hides the hands completely (to-do T1): the forearms (Cole) and the sleeves (Ilinca) run in
  behind the laptop's edges; the typing frames move only them (v1.6.1)
Modified: 2026-10-04 - To-do fixes: typing forearms full width again (T13); the DS lid drawn over the thumbs, thumb tips on
  the base, the long right thumb gone (T14); the hand left empty after the handover closes (T17, empty_fix); a frame
  can move only some parts ('move': hands and bottle shaking in front of a still shirt, T19); the hand on Maker in the
  petting pictures redrawn clean, her outline kept clear of the hole filling (T25: it had read as a black hand) (v1.7.0)
Modified: 2026-10-04 - Ilinca's typing: a new picture with a narrower laptop below her hair's ends, her hands hidden behind
  it, a lump of blazer above her shoulder cleared (T24) (v1.7.1)
Modified: 2026-10-04 - One shaker everywhere (T28): the generated bottles in the shake, offer, take and drink poses replaced
  by the shaker that stands on the desk, behind the fingers, tipped for the drink (shaker()) (v1.8.0)
Modified: 2026-10-04 - Cole's notes T29-T46: typing built on the writing arms with one laptop (LID) for both (base poses);
  Ilinca's hands redrawn clean (op 'hand', HANDS) and new take, drink, phone, carry (two mugs) and think pictures; fingers
  keep their outline in front of a prop ('under' ... True); Cole's shoulders take the rest pose's line (SHOULDERS); a
  greeting pose per activity (WAVE_FROM); a new yawn and a facepalm; the DS grip redrawn (DS_HAND); the paper folded in
  three steps and one plane (PLANE); motion frames for thinking and the call; gaps up to 24 px filled, the desk line closing
  them; frames past the sprite's edge leave no doubled outline (v1.9.0)
Modified: 2026-10-05 - Notes T49-T63: Ilinca's phone held in one hand from below (a new picture); her drink's shaker up at
  her lips, tipped without its mark; her yawn's sleeve drawn over her hair (arm_front); her hands-in-lap pose narrows to
  the desk; Cole's resting hands redrawn closed (op 'mitten'); the shake frame moves only hands, forearms and shaker;
  no watch block on his wrist; every frame of a capped pose capped too (think1 had blipped); a bigger plane, the size
  of the folded one; the petting stroke moves the hand on Maker's head (v1.10.0)

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
from PIL import Image
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
# T28 ("the shaker changes shape multiple times"): one shaker in every hand, the one standing on the desk afterwards
# (assets/desk/prop-bottle.png, generated): red flip cap with its spout, white body, a grey shaded side, the nu mark.
SHAKER = ['aaaa.....aaa..', '.abba...acba..', '..abaaaadcba..', '.aaabbbbbdba..', '.abbbbbbbbbea.', 'abccbbbbbbeeea', 'abccbbbbbbeeea',
          'aaaaaaaaaaaaaa', 'affffffffggga.'] + ['.affffffffgga.'] * 6 + ['.afhhhffffgga.', '.afhfhffffgga.', '.afhfhfhffgga.',
          '.afhfhfhffgga.', '.afffhhhffgga.'] + ['.affffffffgga.'] * 7 + ['.affffffffga..', '..affffffgga..', '...aaaaaaaa...']
SHAKER_KEYS = {'cole': dict(a='k', b='r', c='p', d='b', e='R', f='w', g='g', h='k'),
               'ilinca': dict(a='k', b='r', c='r', d='R', e='R', f='W', g='g', h='k')}


def shaker(who, angle=0):
    """the shaker as a pixel map in the figure's own letters; tilted by angle degrees (clockwise) for a drink, by scaling
    up, turning and scaling back down so its pixels stay clean; tilted, without its mark (turned, the five-pixel mark
    broke into black specks: T51)"""
    m = dict(SHAKER_KEYS[who])
    if angle: m['h'] = m['f']
    rows = [''.join(m.get(ch, '.') for ch in r) for r in SHAKER]
    if not angle: return rows
    h, w = len(rows), len(rows[0]); Z = 8
    letters = sorted({ch for r in rows for ch in r if ch != '.'}); code = {ch: i + 1 for i, ch in enumerate(letters)}
    a = np.array([[code.get(ch, 0) for ch in r] for r in rows], np.uint8)
    big = np.kron(a, np.ones((Z, Z), np.uint8))
    im = Image.fromarray(big).rotate(-angle, resample=Image.NEAREST, expand=True)
    b = np.asarray(im); H, W = b.shape[0] // Z, b.shape[1] // Z; out = []
    for y in range(H):
        row = ''
        for x in range(W):
            cell = b[y * Z + Z // 2 - 1:y * Z + Z // 2 + 1, x * Z + Z // 2 - 1:x * Z + Z // 2 + 1].ravel()
            v = int(np.bincount(cell).argmax()); row += '.' if v == 0 else letters[v - 1]
        out.append(row)
    while out and set(out[0]) == {'.'}: out.pop(0)
    while out and set(out[-1]) == {'.'}: out.pop()
    lo = min(len(r) - len(r.lstrip('.')) for r in out); hi = max(len(r.rstrip('.')) for r in out)
    return [r[lo:hi] for r in out]

# T51 (c) ("ilinca drinking from shaker looks broken"; T28 one shaker; "Object scale must be consistent"): her drink is
# drawn by hand, not turned by code (turning the pixels broke the cap, the mark and the outline). SHAKER tipped 45 degrees
# on clean 1:1 steps, its spout at her lips: the same red cap with the flip tab and the spout, the black band, the white
# body with its grey side, the rounded bottom (no mark), 30 px long and 12 wide as upright; her fist round its lower
# end, four fingers across the near side parted by dark-skin lines, the thumb up its side, the wrist and the sleeve
# below. Composite coordinates (her head already 3 rows down); drawn over the body and again in front of her head.
DRINK_HAND = ['....................kk.......',
              '...................krrk......',
              '...................krrk......',
              '..................krrrk......',
              '.................krrrrk......',
              '................krrrrrk......',
              '................krrrrrrk...k.',
              '................kkrrrrrrk.krk',
              '...............kWWkrrrrrrkrrk',
              '..............kWWWWkrrrrrrrRk',
              '.............kWWWWWWkrrrrrRRk',
              '............kWWWWWWWWkrrrRRRk',
              '........kkkkWWWWWWWWWWkrRRRRk',
              '......kksakWWWWWWWWWWWWkRRRk.',
              '.....kssakWWWWWWWWWWWWggkRk..',
              '....kssakWWWWWWWWWWWWgggkk...',
              '...kssakWWWWWWWWWWWWgggk.....',
              '..kssakkkkkkkWWWWWWgggk......',
              '.kssssssssssakWWWWgggk.......',
              'ksssssssssssakWWWgggk........',
              'ksssssdddddddkWWgggk.........',
              'kssssssssssssakgggk..........',
              'kssssssssssssakggk...........',
              'kssssddddddddkggk............',
              'ksssssssssssakgk.............',
              'kssssssssssssak..............',
              'ksssssdddddddk...............',
              'kssssssssssaak...............',
              '.ksssssssaaak................',
              '.kssssssaaaak................',
              '.kssssssaa...................',
              '.kssssssaa...................',
              'kkkkkkkkkk...................',
              'kjjjjjjjjj...................',
              'kjjjjjJJJ....................']

SKIN_COLE = {'#dc7f6d', '#ee947c', '#f6af8d', '#f8cda6', '#f9eee0'}
SKIN_ILINCA = {'#f9e2d2', '#faebe1', '#e1cec4', '#e0b3a2', '#f1a49b', '#d18881', '#b5705f'}
SLEEVE_ILINCA = {'#292423', '#191718'}

# the stand-in cat's greys in the petting pictures
CAT_GREYS = {'#9a9ea2', '#cfd2d4', '#5f6368', '#a19c9c', '#ddd6cf', '#d9a650'}

# colours of the props that can be lifted out of a pose
LAPTOP = {'#cfd2d4', '#9a9ea2', '#5f6368', '#dfe9f5', '#7fb2e0', '#d9d5c8', '#fbfaf5'}
BOARD = {'#d9a650', '#7d6230', '#2f6b3a', '#1f4a28', '#3d5f99', '#5f6368'}   # the soldering boards and the parts on them
PAPER = {'#fbfaf5', '#d9d5c8'}
BOTTLE = {'#fbfaf5', '#d9d5c8', '#cfd2d4', '#e4002b', '#a3001f', '#ff5a72'}
# T29, T45: the laptop both of them type on, the plain back of its screen, the size and shape of the one in Cole's
# generated typing picture (he: "My laptop dims and shape are good"), redrawn square: that picture's lid had a notch
# where his neck cut into it, and a grey speck at a corner. 'k' outline, 'G' the shaded top and left edges, 'g' panel.
LID = ['k' * 48, 'k' + 'G' * 46 + 'k'] + ['kG' + 'g' * 45 + 'k'] * 35 + ['k' * 48]       # square corners: nothing shows through them
# T42 ("Paper airplane: Reads as a paper football. Full paper stays visible against my chest while I'm folding. Resulting
# airplane should look more like a paper airplane"): the plane seen from above at a slant, nose to the right: the near wing
# white, the far wing in shade, the crease between them ('k' outline, 'w' paper, 'g' paper in shade). The scene draws
# the same map in flight (desk-scene.js PLANE).
def _plane_map(L=22, Hh=15):
    """T57 ("needs to be scale consistent when thrown"): the plane as long as the folded one he holds up (about 22 px),
    seen from above at a slant, nose to the right: the near wing a long white triangle above the crease, the far wing in
    shade below it"""
    c = (Hh - 1) / 2.0; rows = [['.'] * L for _ in range(Hh)]
    def inside(x, y):
        f = 1.0 - x / (L - 1.0)                                          # 1 at the tail, 0 at the nose
        if y <= c: return y >= c - f * c                                 # near wing: from the tail's top corner to the nose
        return y <= c + f * (c * 0.75)                                   # far wing, narrower
    m = [[inside(x, y) for x in range(L)] for y in range(Hh)]
    for y in range(Hh):
        for x in range(L):
            if not m[y][x]: continue
            edge = any(not (0 <= x + dx < L and 0 <= y + dy < Hh and m[y + dy][x + dx]) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
            rows[y][x] = 'k' if edge or abs(y - c) < 0.6 else ('w' if y < c else 'g')
    return [''.join(r) for r in rows]


PLANE = [r for r in _plane_map() if set(r) != {'.'}]


def paper_stage(n):
    """the sheet he folds, at his chest (rows from y 56, columns from x 24): 0 its top corners folded in to the middle (a
    house), 1 its sides folded in again (a dart), 2 the plane folded, held nose up, wings spread, the keel below"""
    W, H, cx = 30, 30, 14.5; rows = [['.'] * W for _ in range(H)]
    def inside(x, y):
        if n == 0: return 5 <= y <= 28 and 2 <= x <= 27 and (y >= 17 or abs(x - cx) <= (y - 5) * 1.05)
        if n == 1: return 2 <= y <= 28 and abs(x - cx) <= (y - 2) * 0.48 + 0.6          # wide enough at its foot for his fingers to hold
        return (0 <= y <= 20 and abs(x - cx) <= y * 0.62 + 0.6) or (20 < y <= 27 and abs(x - cx) <= 1.6)   # the wings to his fingers, then the keel
    m = [[inside(x, y) for x in range(W)] for y in range(H)]
    for y in range(H):
        for x in range(W):
            if not m[y][x]: continue
            edge = any(not (0 <= x + dx < W and 0 <= y + dy < H and m[y + dy][x + dx]) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
            fold = (n == 0 and (y == 17 or (abs(x - cx) < 1 and y < 17))) or (n == 1 and abs(x - cx) < 1) or (n == 2 and abs(x - cx) < 1)
            rows[y][x] = 'k' if edge else ('g' if fold else 'w')
    return [''.join(r) for r in rows]


# T46: Cole's left forearm and hand on the console's left end (x 8-33, rows 60-75; the right is its mirror, x 44-69):
# the forearm comes up from the elbow, the side of the hand wraps the end, the index finger lies along the hinge (row 66)
# on the L button, three fingers lie across the underside of the bottom half (rows 68, 70, 72); the thumb is on top,
# behind the lid
DS_HAND = ['tttttttttttttttttt........',
           'ttttttttttttttkkkk........',
           'tttttttttttttksssmk.......',
           'ttttttttttttksssssmk......',
           'tttttttttttksssssssk......',
           'ttttttttttksssssssmkkkkkk.',
           'tttttttttksssssssmmsssssak',
           'ttttttttksssssssmkkkkkkkk.',
           'tttttttksssssssmmsssssak..',
           'ttttttksssssssmmdddddddk..',
           'tttttksssssssmmmssssssak..',
           'ttttksssssssmmmdddddddkttt',
           'tttksssssssmmmmsssssaktttt',
           'ttksssssssmmmaaaaaakkttttt',
           'tkssssssssmmmaakkkkttttttt',
           'kssssssssmmmaakttttttttttt']

# T57 (i: "needs to be scale consistent when thrown"; audit: the throwing hand "a mottled blob ... no readable fingers; the
# plane touches only one fingertip", and the plane's nose ran off the picture's edge, 17 of its 22 px showing): his raised
# forearm and hand drawn by hand from (62, 30), joined to the forearm where it leaves his sleeve: the wrist bends the hand
# upright, the thumb stands in front of the plane's far wing, the index finger is behind the plane's lower edge (that edge
# is the finger's outline), three fingers curl into the palm (finger lines in the darkest skin). The whole PLANE sits at
# THROW_PLANE, the same plane he folded and the one that flies off from here
THROW_HAND = ['...........kk',
              '..........kssk',
              '..........kssdsssk',
              '..........ksssdssk',
              '..........kssssdssk',
              '..........ksssssdsmk',
              '..........kssssssddmk',
              '.........kssssssssssmk',
              '.........kssssssssssmk',
              '........kssssssssdddddk',
              '........ksssssssssssssmk',
              '........ksssssssssssssmk',
              '.......ksssssssssssddddk',
              '......kssssssssssssssmk',
              '.....ksssssssssssssssmk',
              '....kssssssssssssddddk',
              '...ksssssssssssssmmak',
              '..ksssssssssssssmmmak',
              '.ksssssssssssssmmmaak',
              'ksssssssssssssmmmaak',
              'sssssssssssssmmmaak',
              'ssssssssssssmmmaak',
              'sssssssssssmmmaak',
              'ssssssssssmmmaak',
              'sssssssssmmmaak',
              'ssssssssmmmaak',
              'sssssssmmmaak',
              'ssssssmmmaak',
              'sssssmmmaak',
              'mmmmmmmaak',
              'mmmmmmaak',
              'mmmmmaak',
              'mmmmaak',
              'mmmaak',
              'mmaak',
              'maak',
              'aak',
              'ak']
THROW_PLANE = (66, 22)

# T53 (e: "cole's shaker motion still includes parts of the chest and neck, shaker, hands and arms must be isolated"; audit:
# the cap covered the bottom of his collar every other frame): both hands round the shaker drawn by hand, as the DS grip
# (DS_HAND): each thumb up beside the shaker, four fingers across its front (finger lines in the darkest skin, a notch
# between fingertips), the palm running down into the forearm that stays on the desk. The shake moves only these and the
# shaker, two rows DOWN (shake_grip): the shaker's cap is never higher than the row under his collar, and nothing at or
# above his collar is drawn. SHAKE_HAND_L from (18, 59) (his right hand, on the left), SHAKE_HAND_R from (41, 59)
SHAKE_HAND_L = ['............kk',
                '...........kssk',
                '..........ksssk',
                '.........kssssk',
                '........ksssssk',
                '........ksssssskkkkk',
                '.......ksssssssssssmk',
                '.......ksssssssssssmk',
                '......ksssssssdddddk',
                '......kssssssssssssmk',
                '......kssssssssssssmk',
                '.....ksssssssssddddk',
                '....kkssssssssssssmk',
                '...kssssssssssssmmk',
                'kkksssssssssdddk',
                '.sssssssssssssssmk',
                '.ssssssssssmmmmak',
                '.ssssmmmmaaakkkk',
                '.ssssmmaaaaak',
                '.ssssaaaaakk',
                '.ssaaaakkk',
                '.saaaak']
SHAKE_HAND_R = ['......kk',
                '.....kssk',
                '.....kssk',
                '.....ksssk',
                '.....kssssk',
                '.kkkkksssssk',
                'kmssssssssk',
                'kmsssssssssk',
                '.kddddsssssk',
                'kmssssssssssk',
                'kmssssssssssk',
                '.kdddddssssssk',
                '.kmssssssssssskk',
                '..kmmsssssssssssk',
                '...kdddsssssssssskkk',
                '...kmssssssssssssssk',
                '....kammssssssssssss',
                '.....kkaaammssssssss',
                '.......kkaaammssssss',
                '.........kkaaammssss',
                '...........kkaaammss']
# where the forearms (they stay put) meet the hands two rows lower: their top edges and the shaded inner edge carried on
SHAKE_LOW = [('rows', 18, 74, ['kkk', 'sss']), ('rows', 18, 81, ['s']), ('rows', 16, 82, ['sss']), ('rows', 15, 83, ['sssaaaak']),
             ('rows', 13, 84, ['ssaaaak']), ('rows', 60, 74, ['.t', '.k', 's'])]


def shake_grip(dy):
    """T53: the shaker and both hands holding it, dy rows down (0 or 2), as fix ops over the pose with its own hands taken
    out: a frame of the shake moves nothing else"""
    return [('rows', 33, 55 + dy, shaker('cole')), ('rows', 18, 59 + dy, SHAKE_HAND_L), ('rows', 41, 59 + dy, SHAKE_HAND_R)] + (SHAKE_LOW if dy else [])
# T59 (k: "yawning, black artifact appears on cole's hand, ilinca's hair clips thru arm"), rework after the audit: the
# hands at the yawn and Cole's hand on the desk while he thinks, drawn whole (the reduced pictures had drawn them as
# black strokes and clumps, which pixel patches never cleaned). Pixel maps in the figure's letters, '.' keeps a pixel,
# '_' clears it, placed where the scene draws them (paint()).
# Cole's yawn, x from 36, rows 32-53: the back of his hand over his mouth, four fingers toward his right cheek, finger
# lines in dark skin, one black outline against his face, chin and neck, the wrist down into his forearm.
COLE_YAWN_HAND = [
    '....kk_____________________',
    '...ksskk___________________',
    '..kksssskk_________________',
    '.kssddsssskk_______________',
    '.kssssddsssskk_____________',
    'ksddssssddsssskk___________',
    'ksssddssssddssssk__________',
    '.kssssddssssdmsssk_________',
    '.kddssssddssssssssk________',
    '.kssddssssddsssssssk_______',
    '.kmmssddssssdmsssssk_______',
    '..kkmmssddssssssssssk______',
    '....kkmmssddssssssssk______',
    '......kkmmssdmsssssssk_____',
    '........kkmmsssssssssk_____',
    '..........kkmmssssssssk____',
    '............kkamssssssk____',
    '............kamssssssssk___',
    '...........kaasssssssssk___',
    '...........kaasssssssssk___',
    '...........kaassssssssssk__',
    '............kaaasssssssssk_']
COLE_YAWN_PAINT = [('front', 30, 29, ['_' * 31] * 20),               # the picture's hand and chin at his face go
                   ('front', 36, 32, COLE_YAWN_HAND[:17]), ('body', 36, 32, COLE_YAWN_HAND),
                   ('front', 46, 34, ['s']),                         # the corner of the yawning mouth showed above the fingers
                   # under the hand: the picture's own jaw line (below the chin) is neck in shade; the collar meets the wrist
                   ('body', 36, 45, ['...dd', '....dd', '.....d', '......d', '', '........aaa', '.......aaaa', '......aaaaa', '.....kkkkkkk']),
                   ('body', 66, 85, ['d']), ('body', 48, 88, ['k']),  # two brown specks on his other hand
                   ('body', 53, 77, ['..kk..a', '.kkkkka', 'kkkkkka']),   # where the raised forearm meets the desk: one dark fold, no dark-skin crumbs
                   ('body', -2, 79, ['k', 'k', '', '.k'])]           # the end of his other forearm had no outline against the wall
# Cole thinking, x from 20, rows 84-96: his right hand on the desk under the raised elbow, palm down, four fingers curled
# toward the desk's front edge (index and middle longest), the thumb short beside them, the shirt between the hand and
# the elbow (the picture's hand there had broken, claw-like fingers and a loose fingertip)
COLE_THINK_HAND = [
    '.......................s.skku........',
    '........................ssssku.......',
    '.........................ssskuu......',
    '.........................ssskuuuu....',
    'mmmmmmmmmmmmmmmmmmmmmmmmmmmmkkkkkk...',
    '........kkkkssdssdsssdssdsssk______..',
    '........___kssdssdsssdssdmmmk______..',
    '........___kssdssdsssdsskkkk_______..',
    '........____kmmdssdsssdssk________...',
    '........_____kkkmmdsssdmmk_________..',
    '........________kkkmmmkkk___________.',
    '........___________kkk_______________',
    '........_____________________________']
# the drumming frame: his index and middle fingers a row up
COLE_THINK_TAP = [('rows', 43, 92, ['mm']), ('rows', 39, 93, ['mmmkkk_']), ('rows', 39, 94, ['kkk___']), ('rows', 39, 95, ['___'])]
# Ilinca's yawn, x from 10, rows 27-55, where the scene draws it (her head is 3 rows lower than her picture had it): the
# back of her right hand over her mouth, four fingers up toward her nose, the wrist down into the sleeve's cuff, all in
# front of her hair (the wrist had been under it: the hair crossed her arm)
ILINCA_YAWN_HAND = [
    '............kk...............',
    '.........kkksskkk............',
    '........kssdssdssk...........',
    '.......kssdssdsskkk..........',
    '.......kssdssdssdssk.........',
    '.......kssdssdssdssk.........',
    '......kssdssdssdssk..........',
    '......kssdssdssdssk..........',
    '......kssassassassk..........',
    '......kssssssssssak..........',
    '......ksssssssssak...........',
    '.....ksssssssssak............',
    '.....kssssssssak.............',
    '....kssssssssak..............',
    '....ksssssssak...............',
    '...ksssssssak................',
    '...Jkssssssak................',
    '....kssssssak................',
    '....Jksssssak................',
    '...JJksssssak................',
    '...JJJkssssak................',
    '..JJJJkssssak................',
    '..JJJJJksssak................',
    '...JJJJJkssak................',
    '....JJJJkssak................',
    '....JJJJJksak................',
    '.....JJJJksak................',
    '......JJJJkkk................',
    '..........k..................']
# her other hand on the desk (x from 9, rows 79-86): finger gaps as three short diagonals from the fingertips, a flat
# lower edge (two sleeve-dark pixels and a stub hung below it)
ILINCA_YAWN_DESK = ['...d', '.sd...d', 'kd...d...d', 'ksssdsssd' + 's' * 10, 'kssdsssd', 'kadaaad' + 'a' * 12, '.' + 'k' * 18, '......_____']
ILINCA_YAWN_PAINT = ([('front', 10, 25, ['_' * 29] * 22), ('front', 10, 27, ILINCA_YAWN_HAND),
                      ('front_body', 8, 58, ['..j.', '.j.j', 'j..j', 'j..j', '.jj.'])]   # the black ring her hair's outline left in the sleeve
                     + [(l_, 9, 79, ILINCA_YAWN_DESK) for l_ in ('body', 'front_body')]
                     + [('body', 27, 40, ['a', 'a']), ('body', 34, 41, ['.a', 'ss'])])   # her neck where the picture's hand had covered it
# T60 (n, "while petting maker, cole's hands disconnects"; o, the hole beside her): Cole's petting arm, drawn by hand over
# the rest pose (rows from y 57, columns from x -9; '.' keeps the rest pose, '_' clears). The generated picture's hand
# had no wrist or forearm and ran into his shirt, his other forearm ended in a black block, and the shirt stopped short
# of the desk (the picture was made with a stand-in cat bigger than Maker). Now: the rest pose's sleeve, his elbow on the
# desk where the rest pose has it, the forearm rising from it to the wrist, one outline round arm and hand, the hand
# cupped over Maker's head with four fingers (finger lines in dark skin, the tips in shade) resting between her ears, and
# the rest pose's shirt down to the desk under the arm and behind her. His other arm is the rest pose's, resting behind her.
PET_ARM_COLE = [
    '..........................ttttttkkkkkkkkkkkttuuuuuuttttt',
    '.........................ttttttkssssssssssskkkkttttttttttt',
    '........................ttttttksssssssssssssssskkktttttttttt',
    '.......................ttttttksssssssssssssssssssskkkttttttttt',   # row 60
    '......................ttttttksssssssssssssssssssssssskkttttttttt',
    '.....................ttttttkssssssssssssssssssssssssssskktttttttt',
    '....................ttttttkssssssssssssssssssssssdmsssssskktttttt',
    '...................ttttttkssssssssssssssssssssssssdmssssssskktttt',
    '..................ttttttkssssssssssssssssssssssdmssddmssssssskttt',   # row 65
    '.................ttttttkssssssssmsssssssssssssssdmsssdmsssssssktt',
    '................ttttttkssssssssmmmmsssssmmmmmdmssdmsssdmssssssskt',
    '...............ttttttkssssssssmmaaammmmmaaaaasdmssdmsssdmsssssskt',
    '......__kuutttttttttkssssssssmmaaaaaaaaakkkkkasdmssdmsssddmsssakt',
    '....____kutttttttttkssssssssmmaakkkkkkkktttttkssdmssdmssssdmsaktt',   # row 70
    '.._____kuuutttttttkssssssssmmaakuttttttttttttkassdmssdmssssdakttt',
    '..____kkkkkkkktttkssssssssmmaakuttttttttttttttksssdassdasssaktttt',
    '._____ksssssssktkssssssssmmaakutttttttttttttttkassakmsakaaakttttt',
    '.____ksssssssskkssssssssmmaakutttttt......tttttkaakkaaktkkktttttt',
    '_____ksssssssskssssssssmmaakutttttt........tttttkkttkktttttttttt',   # row 75
    '____kasssssssdssssssssmmaakutttttt.........tttttttttttttttttttt',
    '____kassssssdssssssssmmaakutttttt...........tttttttttttttttttt',
    '____kasssssdssssssssmmaakuttttttt............tttttttttttt',
    '___kaasssssssssssssmmaakuttttttttt',
    '___kaassssssssssssmmaakuttttttttttt',   # row 80
    '___kaasssssssssssmmaakuttttttttttttt',
    '___kaassssssssssmmaakutttttttttttttttttt',
    '___kaasssssssssmmaakuttttttttttttttttttt',
    '___kaassssssssmmaakutttttttttttttttttttt',
    '___kmmmmmmmmsmmaakuttttttttttttttttttttt',   # row 85
    '____kaaaaaaaaaaakuttttttttttttttttttttttt',
    '_____kaaaaaaaaakkkkkkkkkkkkkkkkkkkkkkkkkk',
    '______kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk',   # (to x 36: beside Maker's chin the rest pose's shirt edge was closed only by the hole filling)
]

# T60 (her petting frames, the audit after note o): Ilinca's petting arm as drawn by hand where the picture failed: her
# sleeve outlined down its left side and carried down onto Maker's back (clearing the stand-in cat had left the wall
# showing between them, and a ragged cuff); the hand on Maker's back with one outline, its fingertip no longer hanging
# below it, single finger lines in dark skin, no white speck at the cuff. ('.' keeps the picture, '_' clears.)
PET_ARM_ILINCA = [   # rows from y 62, columns from x -11
    'kjjjjjj',
    'kjjjjj',
    'kjjjjj..d',
    'kjjjjjkkdssdsssdsssskk',
    'kjjjjjkkdsssdssdsssdsskkk',
    'kJJJJJJJkkssdsssdsssdsssak',
    'kJJJJJJJJJkssdsssdsssdssaak',
    'kJJJJJJJJJJkssdsssdsssdaaak',
    '............kaadaaadakkkkk',
    '.............kkkkkkkk',
    '..................__',
]
# and her white top carried on down beside Maker's rump to the desk (clearing the stand-in cat had left a column of wall
# showing between them)
TOP_ILINCA = ['WW', '.WW', '..WW', '...WW', '....W', '....WW', '.....WW', '......W', '......WW', '.......W', '.......W',   # rows from y 68, columns from x 16
              '.......gg', '........g', '........g', '........g', '........k']
# and her other hand, resting on the desk: one closed relaxed hand (the generated one had a loose fingertip with a white
# pixel in it and pale specks), the thumb toward her middle, three short finger lines in dark skin
REST_HAND_ILINCA = [   # rows from y 74, columns from x 28
    '...............k',
    '.............kksskk',
    '............kssssssk',
    '.........kkssssssssak',
    '........ksssssssssssak',
    '......kkesssssssssssak',
    '...kkkesssssssssssssak',
    '..keeessssssssssssssakJ',
    '.kesssdsssssssssssssak',
    '.kasssdssssssssssssak',
    '..kaadsssssssssssssak',
    '___kkessssssdsssssak____',
    '____kasssdssdssdssak____',
    '_____kassdssdssdsak_____',
    '______kasdssdssdak______',
    '_______kadaadaaak_______',
    '________kkkkkkkk________',
    '________________________',
    '________________________',
    '________________________',
    '________________________',
]
# T60 (l) ("at rest, cole's hands are badly drawn"; the 'mitten' redraw had left blank stumps with no thumb, a spur and an
# outline break): his left-hand-side resting hand (his right hand) drawn by hand, x 4-29, rows 86-97, seen from the front
# and a little above, loosely closed: the forearm's shaded band runs on into the pinky side (rows 86-90, the heel rounded),
# the back of the hand (rows 86-89) slopes down to the knuckles (row 90 in mid tone), the knuckles lit with dips over the
# finger divisions (row 91), the fingers bending down (row 92), four finger fronts with three divisions in dark skin (rows
# 93-95) ending in rounded tips with a black notch between them, the pinky a row shorter; the thumb on the inner side, lit,
# angled toward the middle, apart from the index finger by a V notch, its tip on the fingertips' row (a row lower read as a
# pointing hook). One black outline wherever it meets the desk or the shirt. Drawn after the softening ('post'), so every
# outline pixel stays as drawn. The other hand is its mirror (REST_MIRROR: x + x' = 72, where the two forearms meet the desk).
REST_HAND = ['aasssssssssssssssss.......',   # 86
             'aaaassssssssssssssss......',   # 87
             'aaaamsssssssssssssssssk...',   # 88
             'aaaamssssssssssssssmkk____',   # 89
             'kkaammmmmmmmmmmmmmmmk_____',   # 90
             '__kammmsssmsssmssdsmk_____',   # 91
             '___kammmmmmmmmmmmdsssk____',   # 92
             '___kmadmmadmmadmadsssmk___',   # 93
             '___kmadmmadmmadmakksssmk__',   # 94
             '____kkkaaakaaakaak_kaaak__',   # 95
             '_______kkk_kkk_kk___kkk___',   # 96
             '__________________________']   # 97
# the fidget frame (rest1): the same hand from the knuckle slope down lifted a pixel (the back of the hand a row shorter),
# the heel still rounded
REST_HAND_LIFT = REST_HAND[:3] + ['aaaa' + REST_HAND[4][4:20] + 'kk____', 'kk' + REST_HAND[5][2:]] + REST_HAND[6:] + ['_' * 26]
REST_MIRROR = 72


def rest_hands():
    """T60 (l): the fix ops that draw both resting hands (REST_HAND and its mirror) over what the picture had there"""
    m, x0, w = REST_MIRROR, 4, len(REST_HAND[0]); xr = m - (x0 + w - 1)
    return [('clear', x0, 89, 34, 99), ('rows', -1, 89, ['kkkkk']), ('rows', x0, 86, REST_HAND),
            ('clear', m - 34, 89, m - x0, 99), ('rows', m - 3, 89, ['kkkkk']), ('rows', xr, 86, [r[::-1] for r in REST_HAND]),
            ('rows', 69, 86, ['aaa']),                                   # the right forearm's shaded band joined to the hand's
            ('rows', 45, 84, ['.....kkkk..', '.....kksss.', '.kkkk......', '.kkk.......'])]   # its top edge outlined against the shirt, as the left's is


# By eye, per pose: the box (base coordinates) whose pixels go over the face, and named points.
MANUAL = {
    'cole': {
        'sip': dict(front=(30, 26, 58, 48), front_mode='armprops'),        # the fingers round the mug and the mug, in front of the chin (not the picture's own face: T44)
        'drink': dict(front=(40, 28, 61, 58), front_mode='limb'),
        # note 9d: the boards lie edge-on on the desk line (they were drawn in perspective over the desk's front); the
        # irons reach down to them
        'solder': dict(fix=[('recolour', 24, 83, 50, 86, {'#d9a650': '#211f1f', '#5f6368': '#211f1f', '#d9d5c8': '#211f1f', '#0f0503': '#211f1f', '#cfd2d4': '#211f1f'}),
                            ('clear', 22, 89, 52, 93),
                            ('under', 25, 85, ['..kk...k....kk.....k..kk.', '.kkkk.kkk..kkkk...kkk.kkkk'.replace('kkkk', 'kiik'), 'k' + 'c' * 24 + 'k', 'k' + 'C' * 24 + 'k', 'k' * 26], SKIN_COLE),
                            ('rows', 37, 83, ['k', '.k', '.k'])],
                       pts={'tip': (38, 86)}, frames={'solder1': ((48, 68, 68, 88), 0, -1)},
                       props={'board': (BOARD, (24, 85, 51, 89))}),                # the board stays on the desk when he waves the smoke away
        'solder2': dict(fix=[('recolour', 28, 81, 48, 86, {'#2f6b3a': '#211f1f', '#1f4a28': '#211f1f', '#3d5f99': '#211f1f', '#090507': '#211f1f', '#d9a650': '#211f1f'}),
                             ('clear', 26, 89, 52, 96),
                             ('under', 29, 85, ['...k..kk....kk...k..', '..kik.kBBk..kiik.kck.', 'k' + 'v' * 18 + 'k', 'k' + 'V' * 18 + 'k', 'k' * 20], SKIN_COLE),
                             ('rows', 37, 84, ['k', 'k'])],
                        pts={'tip': (37, 86)}, props={'board': (BOARD, (28, 85, 49, 89))}),
        # note 4, "supposed to be a nintendo DS" (his reference: the back of a red New 3DS XL): the console redrawn as seen
        # from across the desk, behind his hands: the lid's red back with its two camera lenses, the hinge with its
        # knuckles, the underside of the bottom half with its label
        # T14 ("thumbs should land on lower part of DS. upper joints of thumbs should be hidden behind system"): the lid is
        # drawn over everything, so no thumb climbs it; on the base the hands stay in front and the thumb tips rest there
        'ds': dict(frames={'ds1': {'edits': [('rows', 32, 65, ['.k.', 'sak', '.k.'])]},          # T46: an index finger presses its shoulder button
                           'ds2': {'edits': [('rows', 42, 65, ['.k.', 'kas', '.k.'])]}},
                   fix=[('rows', 26, 55, [
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
            'kkRRkkkkkkkkkkkkkkkkkkRRkk']),
                        ('under', 26, 67, [
            'kRRRRRRRRRRRRRRRRRRRRRRRRk',
            'kRRRRRRRRRwwwwwwRRRRRRRRRk',
            'kRRRRRRRRRRRRRRRRRRRRRRRRk',
            '.kkkkkkkkkkkkkkkkkkkkkkkk.'], {'#f8cda6', '#f6af8d', '#ee947c', '#dc7f6d', '#f9eee0'}),
                        # the right thumb climbed the lid's edge ("much too long"): the hand stops at the base, shirt above it
                        ('rows', 52, 57, ['ttttttt', 'ttttttt', 'ttttttt', 'ttttttt', 'ttttttt', 'kkkkkkt', 'ksssss.']),
                        # T46 ("simplify the hands, make sure just the thumb is going on top of the console. the 3rd-5th
                        # fingers sit underneath, the pointers sit on the L & R, thumbs operate D-pad and buttons"): seen from
                        # across the desk the thumbs are on top, out of sight behind the lid; each index finger lies along the
                        # hinge on its shoulder button; the other three fingers curl under the bottom half, their tips showing
                        ('recolour', 12, 50, 26, 59, {c_: '#211f1f' for c_ in SKIN_COLE}), ('recolour', 52, 50, 66, 59, {c_: '#211f1f' for c_ in SKIN_COLE}),
                        ('rows', 8, 60, DS_HAND), ('rows', 44, 60, [r[::-1][:-4] + '....' for r in DS_HAND])]),   # (his right side ends where his shirt does)
        'think': dict(neck_fill=False, keep_neck=True, front=(30, 32, 58, 50), front_mode='arm',   # the fist under his chin, in front of the jaw
                      paint=[('body', 20, 84, COLE_THINK_HAND), ('front', 54, 46, ['_'])],   # T59 rework: the hand on the desk drawn whole; a shirt pixel outside his forearm's outline
                      frames={'think1': {'edits': COLE_THINK_TAP}}),            # T7: the fingers on the desk drum (two lift a row; a box shift had doubled a finger line)
        'hide': dict(fix=[('clear', -24, 89, 110, 104)]),                # hands in his lap: nothing of them below the desk line (note 9b)
        # note 9a, motion in every activity: frames the scene cycles through (a forearm typing behind the screen, a hand to
        # the trackpad, thumbs on the console, a fidgeting hand)
        # T60 (l) ("at rest, cole's hands are badly drawn"): both hands drawn by hand (REST_HAND), after the softening; the
        # fidget frame lifts the left hand's fingers a pixel (REST_HAND_LIFT; a box shift had stepped the forearm and the hem)
        'rest': dict(post=rest_hands(), frames={'rest1': {'edits': [('clear', 4, 89, 34, 99), ('rows', 4, 86, REST_HAND_LIFT)]}}),
        # petting Maker lying beside him: the picture had a grey cat under his hand; it goes, and the scene lays Maker in
        # its place (RIG below), so the hand lies exactly on her back; the hand moves a little as it strokes
        'petcat': dict(fix=[('erase', 28, 60, 86, 93, CAT_GREYS)], frames={'petcat2': ((46, 56, 80, 82), -2, 0)}),
        # note 12: Maker lies at the desk's front edge now; this picture was made with her pasted there (work folder
        # petedge/), so the hand lands on her back; everything of the stand-in cat but the hand goes
        # T60 (n, o): built on the rest picture (the shoulders, the sleeves, the shirt to the desk, the other arm), the petting
        # arm drawn over it (PET_ARM_COLE); the forearms on the desk go (the right hand would peek out under her belly); the
        # map again after the softening (it had opened the outline between the fingertips); inside the scene's petting box
        # and her footprint only the hand ('maker'). T62: the stroke moves the hand on her head a pixel, the arm stays.
        'petedge': dict(base='rest', fix=[('mitten', 2, 86, 36, 99), ('mitten', 42, 86, 76, 99), ('rows', -9, 57, PET_ARM_COLE),
                                          ('clear', -10, 89, 70, 100), ('late', [('rows', -9, 57, PET_ARM_COLE)]),
                                          ('maker', 31, 66, (31, 66, 56, 104), 78)],
                        frames={'petedge2': {'box': (28, 57, 56, 78), 'dx': 1, 'edits': [('rows', 36, 57, ['u.....t']), ('maker', 31, 66, (31, 66, 57, 104), 78)]}}),   # (the shirt's crease beside the hand stays put)
        'stretch': dict(fix=[('clear', -8, 54, 7, 92), ('clear', 8, 53, 8, 53)]),   # a chair's edge behind him in the generated picture
        # props the scene also draws on their own: the laptop (the cat sits on it), the paper, the bottle being handed over
        # T31 (2026-10-04: "Typing arms still look really weird", "Writing arms are good"): typing is the writing picture
        # with the laptop (LID, T29) standing in front of the hands, so the forearms run in behind it from the elbows as
        # they reach for the paper (the hands stay hidden, T1); the paper and what hung below the desk line go. "arms
        # should move along X, not along y": the frames slide a forearm in toward the keyboard
        'type': dict(base='write',
                     fix=[('clear', -16, 91, 84, 100), ('recolour', 63, 80, 84, 92, {'#fbfaf5': None, '#d9d5c8': None, '#cfd2d4': None}),
                          ('rows', 16, 53, LID),
                          # right of the laptop his left wrist showed a crease and a thumb hanging down: a plain forearm
                          ('rows', 64, 77, ['.mmssssssss', 'msssss', 'm', '', '', '...s', '', '....s', '....m', '....m',
                                            'kkkk', '____', '___', '__'])],
                     props={'laptop': (LAPTOP, (14, 50, 66, 92))},
                     frames={'type1': ((-16, 74, 15, 92), 1, 0), 'type2': ((64, 74, 84, 92), -1, 0), 'typetrack': ((64, 74, 84, 92), -2, 0)}),
        # note 9d: the desk is seen flat from the front, so the paper lies edge-on: a thin white strip on the desk line,
        # not a sheet in perspective hanging over the desk's front (what the paper covered above the desk is his shirt)
        'write': dict(fix=[('recolour', 20, 82, 64, 87, {'#fbfaf5': '#211f1f', '#d9d5c8': '#211f1f'}), ('clear', 14, 91, 72, 98),
                           ('recolour', 14, 88, 72, 90, {'#fbfaf5': None, '#d9d5c8': None, '#cfd2d4': None}),
                           ('under', 22, 88, ['k' + 'w' * 40 + 'k', 'k' + 'g' * 40 + 'k', 'k' * 42], SKIN_COLE)],
                      props={'paper': (PAPER, (10, 80, 90, 100))}, frames={'write1': ((14, 64, 36, 92), 1, 0), 'write2': ((14, 64, 36, 92), 2, -1)}),
        # T28: the one shaker in every hand (the generated bottle goes, the shaker goes behind the fingers)
        'offer': dict(fix=[('recolour', 70, 12, 90, 52, {'#f9eee0': '#fbfaf5'}), ('erase', 70, 12, 90, 52, BOTTLE), ('under', 72, 16, shaker('cole'), SKIN_COLE)],
                      props={'bottle': (BOTTLE, (58, 0, 100, 50))}, empty={'offerEmpty': 'bottle'},
                      # T17: without the bottle the curled hand read as a hole: the fingers close into a fist
                      empty_fix={'offerEmpty': [('rows', 73, 40, ['k...............',
                                                                  'kkkkkkkkkkkkkkk.',
                                                                  'mmsssssssssssmmk',
                                                                  'mssssssssssssmmk',
                                                                  'msssdsssdsssdmmk',
                                                                  'msssdsssdsssdmmk',
                                                                  'massdsssdsssdmk.',
                                                                  'maasdsssdssadk..',
                                                                  'maaadaaadaaak...',
                                                                  'mdddddddddddk...',
                                                                  '...kkkkkkkkk....'])]}),
        # shaking: only the hands, forearms and the bottle move (T19: a box shift took a chunk of his shirt with them)
        # T53 (e): the generated bottle and hands go (shirt where they were); both frames, 'shake' itself too, are drawn as
        # frames, after the cleanup passes (which had turned outlines between thumb and finger to skin), so the two differ
        # only in the hands and the shaker, two rows apart, all below his collar (shake_grip)
        'shake': dict(fix=[('erase', 30, 50, 50, 86, BOTTLE), ('erase', 19, 58, 39, 80, SKIN_COLE), ('erase', 40, 57, 60, 79, SKIN_COLE),
                           ('holes', 19, 55, 60, 86, '#211f1f')],
                      frames={'shake': {'edits': shake_grip(0)}, 'shake2': {'edits': shake_grip(2)}}),
        'highfive': dict(pts={'hand': (67, 24)}),
        # T42: the plane in his hand is the plane that flies (PLANE); T57 (i): the generated hand goes, his hand-drawn forearm and
        # pinching hand (THROW_HAND) take its place, the whole plane in it. 'hand' is where the flying plane's middle starts:
        # exactly where it was held (the scene draws it behind his open hand for its first frames, so the fingers stay in
        # front of its tail; started 17 px on, it lurched off the hand and grazed Ilinca's head on a phone: re-audit)
        'throw': dict(pts={'hand': (THROW_PLANE[0] + len(PLANE[0]) // 2, THROW_PLANE[1] + len(PLANE) // 2)},
                      fix=[('erase', 74, 18, 98, 38, PAPER), ('clear', 64, 20, 95, 67), ('rows', 62, 30, THROW_HAND),
                           ('under', THROW_PLANE[0], THROW_PLANE[1], PLANE, SKIN_COLE, True)]),
        # T42: he folds it in three steps, the paper getting smaller each time (the generated sheet goes)
        'fold': dict(fix=[('erase', 20, 56, 58, 88, PAPER), ('holes', 20, 56, 58, 88, '#211f1f'), ('under', 24, 56, paper_stage(0), SKIN_COLE, True)],
                     # T57 (i, audit: "the plane held at his chest at the end of folding ... about 1.5x bigger" than the thrown one,
                     # "reads as an up-arrow"): the finished plane is PLANE itself, the one he throws, its tail behind his left
                     # fingers and its nose at his right hand (the earlier folding stage stays as it was)
                     frames={'fold3': {'edits': [('erase', 20, 56, 58, 88, PAPER | {'#cfd2d4'}), ('holes', 20, 56, 58, 88, '#211f1f'), ('under', 29, 61, PLANE, SKIN_COLE, True)]}}),
        # T37 ("On late night yawn, I have 3 arms"): a new picture, one hand over his mouth, the other forearm flat on the desk
        'yawn': dict(front=(30, 29, 60, 48), front_mode='arm', keep_neck=True, paint=COLE_YAWN_PAINT),   # T59 rework: the hand at his mouth drawn whole
        # T38 (the spark: "instead of looking frustrated or surprised I do a little dance"): a hand to his head, frustrated
        'facepalm': dict(front=[(34, -8, 64, 21), (54, 21, 68, 42)], front_mode='notface'),   # the hand on his head and the arm beside his face; never the picture's own face or glasses
        # a chair back stood behind the elbow in the generated picture
        'fist': dict(fix=[('clear', 80, 64, 83, 64), ('clear', 73, 65, 83, 65), ('clear', 74, 66, 83, 66), ('clear', 75, 67, 83, 67), ('clear', 76, 68, 83, 69),
                          ('clear', 77, 70, 83, 70), ('clear', 78, 71, 83, 72), ('clear', 79, 73, 83, 73), ('clear', 80, 74, 83, 75), ('clear', 81, 76, 83, 77),
                          ('clear', 82, 78, 83, 79)]),
    },
    'ilinca': {
        'sip': dict(front=(-2, 20, 24, 46), front_mode='notface', front_face=True),
        # T29 (2026-10-04: "Ilinca's hair still appears in front of her laptop. My laptop dims and shape are good, hers
        # aren't"): Cole's laptop (LID), standing on the desk in front of her middle; the scene draws it over her hair.
        # T31: her writing arms behind it, as his; the frames slide a sleeve in toward the keyboard
        'type': dict(base='write',
                     fix=[('clear', -20, 87, 70, 96), ('recolour', 52, 44, 56, 54, {c_: '#191718' for c_ in ('#cfd2d4', '#9a9ea2', '#5f6368')}), ('rows', 4, 49, LID),
                          # left of the laptop her writing hand and its cuff showed: the sleeve runs on in behind it
                          ('rows', 1, 66, ['.jj', 'jjj', '..j']), ('rows', 0, 72, ['jjjj']),
                          ('rows', -5, 73, ['...jjjjjj', '...jjjjjj', '...jjjjjj', '..jjjjjjJ', '.jjjjjjjJ', '.jjjjjjjJ', '.jjjjjjjJ',
                                            'jjjjjjjjJ', 'jjjjjjjjJ', 'kkkkkkkkk', '_________', '_________', '_________', '_________'])],
                     props={'laptop': (LAPTOP, (2, 46, 54, 88))},
                     frames={'type1': ((-14, 64, 3, 88), 1, 0), 'type2': ((52, 64, 66, 88), -1, 0), 'typetrack': ((52, 64, 66, 88), -2, 0)}),
        'wave': dict(frames={'wave2': ((-12, 12, 12, 38), 1, 0)}),          # a casual wave: the hand rocks a pixel
        # her reaching sleeve ended in a spike up into her hair: its top is cut level at the shoulder, under the hair
        'petcat': dict(fix=[('erase', -38, 60, 32, 94, CAT_GREYS), ('clear', 0, 30, 16, 45), ('rows', 4, 46, ['kkkkkk'])], frames={'petcat2': ((-18, 54, 14, 76), 2, 0)}),
        # as Cole's: Maker at the front edge. T60: the stand-in cat cleared once (not again after the hole filling, which
        # would open the sleeve again), the maps drawn and drawn again after the softening, only the hand over Maker
        # ('maker'). The stroke moves the hand a pixel; the sleeve, shoulders and torso stay (the whole arm had moved, and its
        # old outline stayed behind as a loose sliver)
        'petedge': dict(fix=[('cat', -29, 62, SKIN_ILINCA, False), ('rows', -11, 62, PET_ARM_ILINCA), ('rows', 28, 74, REST_HAND_ILINCA), ('rows', 16, 68, TOP_ILINCA),
                             ('late', [('rows', -11, 62, PET_ARM_ILINCA), ('rows', 28, 74, REST_HAND_ILINCA), ('rows', 16, 68, TOP_ILINCA)]),
                             ('maker', -29, 62, (-29, 62, 24, 100), 74)],
                        frames={'petedge2': {'box': (-6, 58, 16, 72), 'dx': 1, 'edits': [('maker', -29, 62, (-29, 52, 24, 100), 74)]}}),
        'stretch': dict(fix=[('clear', 63, 38, 67, 84)]),                # a chair's edge behind her
        'rest': dict(fix=[('recolour', 56, 55, 64, 66, {'#5f6368': '#191718', '#9a9ea2': '#292423'})],   # a grey chair corner by her shoulder
                     frames={'rest1': ((6, 72, 36, 88), 0, -1)}),
        'write': dict(fix=[('clear', -8, 87, 36, 92), ('recolour', -8, 85, 36, 86, {'#fbfaf5': None}),
                           ('under', -4, 85, ['k' + 'W' * 38 + 'k', 'k' * 40], SKIN_ILINCA | SLEEVE_ILINCA)],
                      props={'paper': (PAPER, (-14, 74, 40, 96))}, frames={'write1': ((-6, 60, 16, 90), 1, 0), 'write2': ((-6, 60, 16, 90), 2, -1)}),
        # T40 (2026-10-04, "the elbow she's resting on should be more towards the middle of her body"): a new picture, the
        # forearm upright down the middle of her chest; the fist under her chin goes in front of her jaw
        'think': dict(keep_neck=True, front=[(17, 31, 34, 48)], front_mode='nothair', front_face=True, frames={'think1': ((8, 72, 38, 92), 1, 0)},   # T7: her fingers drum
                      fix=[('holes', 20, 50, 34, 80, '#ddd6cf')]),          # her white top in shadow, which the cut-out may take for the grey wall          # her white top in shadow, which the cut-out had taken for the grey wall
        # her phone and both hands are in front of her hair (they were drawn under it), and the phone is blue again (the
        # reduction had snapped the picture's blue phone to grey)
        # T49 (2026-10-05, "phone should be held from the bottom, one handed"): a new picture, the phone resting in one hand
        'phone': dict(keep_chest=True, front=(4, 44, 50, 80), front_mode='limb',
                      frames={'phone1': ((14, 50, 42, 80), 0, -1)},           # the hand lifts it a little as she scrolls
                      fix=[('recolour', 14, 48, 40, 76, {'#5f6368': '#3d5f99', '#9a9ea2': '#6f93cf'}),
                           ('recolour', 9, 50, 17, 63, {'#f9e2d2': '#191718', '#faebe1': '#191718', '#f1a49b': '#191718', '#e1cec4': '#191718', '#e0b3a2': '#191718'}),   # the picture's wider neckline: her blazer, under her hair
                           ('recolour', 16, 70, 27, 76, {'#f9e2d2': '#fbfaf5', '#faebe1': '#fbfaf5', '#e1cec4': '#ddd6cf'})]),   # her white top under the phone (shrunk to skin colour)
        'carry': dict(keep_chest=True),
        # T51 (c): the generated bottle, hand and raised forearm all go; the hand-drawn shaker in her fist (DRINK_HAND) goes on
        'drink': dict(fix=[('clear', -8, 14, 14, 59), ('erase', 15, 14, 27, 42, BOTTLE),
                           ('recolour', 21, 54, 22, 54, {'#a19c9c': '#0b0503'}), ('recolour', 21, 55, 21, 55, {'#a19c9c': '#fbfaf5'})],   # a grey scrap of the picture at her neckline: outline and top, as in her rest pose
                      stamp=[(-2, 25, DRINK_HAND)]),
        'yawn': dict(front=(12, 24, 36, 42), front_mode='notface', keep_neck=True, front_face=True,
                     arm_front=[(2, 42, 27, 63), (-6, 63, 14, 66)],   # T59: the sleeve of the arm reaching up is in front of her hair
                     # T59 (k), rework: down to the tip of her hair (the boxes had stopped at row 63 and the tip showed in the sleeve)
                     paint=ILINCA_YAWN_PAINT,                              # T59 rework: her hand, wrist and cuff drawn whole, in front of her hair
                     fix=[('recolour', 7, 57, 13, 63, {'#5f4030': '#292423', '#6f4b3a': '#292423', '#9a6f50': '#292423', '#bd8e5d': '#292423', '#d9ae71': '#292423'})]),   # (her own hair peeked through it there)   # T23: only the hand (the 'diff' box left a pale rectangle by her hair)
        # hands and sleeves that are in front of her hair
        'talk': dict(front=(-16, 28, 14, 64), front_mode='limb'),
        'call': dict(keep_chest=True, front=(4, 24, 15, 46), front_mode='notface', front_face=True, frames={'call1': ((0, 68, 27, 82), 1, 0)}),   # T7: her free hand shifts as she talks
        'surprise': dict(keep_chest=True, front=(48, 24, 68, 58), front_mode='limb'),
        # the bottle came out in her skin colours
        'take': dict(fix=[('erase', -12, 12, 4, 50, BOTTLE), ('under', -11, 14, shaker('ilinca'), SKIN_ILINCA, True)]),   # T35: a picture made with this shaker in her hand; her fingers wrap it
        # note 9b: hands in her lap under the desk (when Maker walks by): her rest picture with the forearms and hands
        # taken out and the blazer and top carried straight down to the desk line (the model would not hide her hands)
        'hide': dict(keep_chest=True, fix=[('handsunder', 71, 84, 15, 25, ('#292423', '#191718', '#010100', '#fbfaf5', '#0b0503')),
                                           ('recolour', 56, 55, 66, 70, {'#5f6368': '#191718', '#9a9ea2': '#292423'})]),
    },
}


# T2, T23, T34 (2026-10-04, "Ilinca's hands are still messy. Make her hands a priority."): every hand she shows is redrawn
# clean (fix op 'hand', after the pose's own fixes): boxes in base coordinates, one per hand
HANDS = {
    'cole': {'sip': [(24, 34, 42, 58)], 'mug': [(-6, 70, 32, 90), (44, 72, 80, 94)],          # T44: his coffee hands too, and every hand the audit found clumped
             'surprise': [(-14, 10, 22, 60), (56, 10, 90, 60)], 'yawn': [(-6, 72, 76, 96)], 'talk': [(-10, 50, 84, 96)],   # T57: not 'throw' (its hand is drawn: THROW_HAND)
             'write': [(40, 70, 84, 96)], 'offer': [(64, 12, 96, 56)]},
    'ilinca': {
        'rest': [(5, 71, 41, 91)], 'mug': [(-8, 67, 41, 85)], 'sip': [(-2, 25, 14, 63), (19, 72, 41, 86)], 'write': [(-6, 71, 17, 87), (26, 73, 52, 88)],
        'call': [(2, 69, 25, 80), (5, 25, 16, 47)], 'yawn': [(8, 75, 29, 87)], 'talk': [(-18, 30, 7, 62), (18, 72, 44, 89)],
        'petcat': [(-15, 53, 6, 69), (15, 66, 39, 85)], 'wave': [(-11, 13, 11, 50), (4, 71, 28, 85)],   # (T60: petedge's hands are drawn by hand: PET_ARM_ILINCA, REST_HAND_ILINCA)
        'surprise': [(-9, 10, 13, 49), (49, 10, 65, 49)],
        'take': [(-14, 20, 4, 56), (10, 71, 34, 89)], 'drink': [(12, 76, 36, 88)], 'phone': [(14, 56, 42, 80), (4, 76, 40, 90)],   # T51 (c): drink's shaker hand is drawn (DRINK_HAND), not cleaned
        'carry': [(1, 68, 11, 77), (43, 69, 52, 77)], 'think': [(17, 31, 34, 48), (10, 73, 36, 91)],
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
                 w='#fbfaf5', r='#e4002b', R='#a3001f', g='#cfd2d4', G='#9a9ea2', p='#ff5a72', c='#d9a650', C='#7d6230',
                 v='#2f6b3a', V='#1f4a28', B='#3d5f99', i='#5f6368'),
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


# The scene draws Ilinca's head three rows lower than her portrait has it (desk-scene.js headDy: her neck read too long).
# Her poses are cut against the head where it is drawn, and their front layer is two: what is at her face (front_face
# poses) is drawn with the head, three rows lower, and its copy leaves the body; hands and things in front of her hair
# are drawn with the body (front_body). Drawing them all with the head had doubled her hands three rows apart and left
# gaps where her shoulders meet her hair (to-do T23, T34: "holes in her shoulder", "messy/doubled hands").
HEAD_DY = {'ilinca': 3}
FACE_PT = {'cole': (40, 31), 'ilinca': (27, 26)}                          # a point on each picture's own cheek (front mode 'notface')


def shifted_head(head, hm, jaw, dy):
    """the base head, its mask and its jaw rows moved dy rows down"""
    if not dy: return head, hm, jaw
    h2 = head.copy(); h2.idx[:] = -1; h2.idx[dy:] = head.idx[:-dy]
    m2 = np.zeros_like(hm); m2[dy:] = hm[:-dy]
    return h2, m2, {x: y + dy for x, y in jaw.items()}


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


def pinholes(body, ox, oy, head, front=None, most=24, desk=None):
    """tiny gaps that show the wall from inside the figure (a few pixels, closed in by the body, the head or the front
    layer; left by a moved writing hand or a speck of the cut-out): filled from the nearest body pixel"""
    h, w = body.idx.shape; fig = body.idx >= 0
    hy, hx = np.where(head.idx >= 0); py, px = hy - oy, hx - ox; ok = (py >= 0) & (py < h) & (px >= 0) & (px < w)
    allfig = fig.copy(); allfig[py[ok], px[ok]] = True
    for fr in (front if isinstance(front, list) else [front]):
        if fr is None: continue
        fs, fx, fy = fr; fy_, fx_ = np.where(fs.idx >= 0); py, px = fy_ + fy - oy, fx_ + fx - ox
        ok = (py >= 0) & (py < h) & (px >= 0) & (px < w); allfig[py[ok], px[ok]] = True
    if desk is not None and 0 <= desk + 1 - oy < h: allfig[desk + 1 - oy:, :] = True   # a notch just above the desk is closed by it (T23)
    lab, n = _nd.label(~allfig); border = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]])).tolist())
    holes = np.zeros((h, w), bool)
    for i in range(1, n + 1):
        if i in border: continue
        m = lab == i
        if m.sum() <= most: holes |= m
    if not holes.any(): return body
    out = body.copy(); _, (iy, ix) = _nd.distance_transform_edt(~fig, return_indices=True); out.idx[holes] = out.idx[iy[holes], ix[holes]]
    return out


def fix(spr, ox, oy, edits, pal_key):
    """per-pose pixel fixes in base coordinates: ('rows', x, y, [..]) maps of palette letters ('.' keep, '_' clear),
    ('clear', x0, y0, x1, y1) and ('recolour', x0, y0, x1, y1, {from: to})"""
    s = spr.copy()
    for e in edits:
        if e[0] == 'cat':                                                # Maker's own outline where she was pasted into the picture: all of it goes
            x0, y0, skin = e[1:4]; _cat_clear(s, ox, oy, x0, y0, skin)  # but the hand on her, redrawn clean
            continue
        if e[0] == 'late': continue                                      # T60 (n): applied after the softening and the hole filling (build)
        if e[0] == 'maker':                                              # T60 (n, o): only the hand where the scene draws the pose again over Maker
            who = 'ilinca' if pal_key is KEYS['ilinca'] else 'cole'; _maker_clear(s, ox, oy, who, *e[1:])
            continue
        if e[0] == 'mitten':                                             # a relaxed hand redrawn closed: one outline, even skin, short finger lines
            who = 'ilinca' if pal_key is KEYS['ilinca'] else 'cole'; _mitten(s, ox, oy, e[1:5], who, *(e[5:] or ()))
            continue
        if e[0] == 'hand':                                               # a hand redrawn clean: one outline, finger lines in dark skin
            who = 'ilinca' if pal_key is KEYS['ilinca'] else 'cole'; _clean_hand(s, ox, oy, e[1:5], who, _face_guard(who, s.idx.shape, ox, oy))
            continue
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
        if e[0] == 'handsunder':                                         # hands down in the lap, under the desk: the torso goes straight down to the desk line
            _, top, desk, bx0, bx1, cols = e                             # cols: jacket, jacket shade, outline, blouse, blouse edge
            jacket, shade, line, blouse, bline = (s.color(c_) for c_ in cols)
            row = s.idx[top - oy]; xs = np.where(row >= 0)[0]; left0, right0 = xs.min(), xs.max(); n_ = max(1, desk - top)
            for y in range(top - oy + 1, desk - oy + 1):
                if not (0 <= y < s.h): continue
                k = int(round(6 * (y - (top - oy)) / n_)); left, right = left0 + k, right0 - k   # T61: the arms drop to her lap, closer in (a flat, wide bottom read as forearms left on the desk)
                s.idx[y, :] = -1; s.idx[y, left:right + 1] = jacket; s.idx[y, left] = line; s.idx[y, right] = line
                for x in (left + 9, right - 9): s.idx[y, x] = shade        # where the arms hang beside the body
                s.idx[y, bx0 - ox:bx1 - ox + 1] = blouse; s.idx[y, bx0 - ox - 1] = bline; s.idx[y, bx1 - ox + 1] = bline
            s.idx[desk - oy + 1:, :] = -1
            continue
        if e[0] == 'holes':                                              # empty pixels in a box filled with one colour (a light shirt the cut-out took for wall)
            _, x0, y0, x1, y1, col = e
            sub = s.idx[max(0, y0 - oy):max(0, y1 + 1 - oy), max(0, x0 - ox):max(0, x1 + 1 - ox)]; sub[sub < 0] = s.color(col)
            continue
        if e[0] == 'under':                                              # a pixel map drawn behind whatever is in the keep colours (hands in front of a prop)
            _, x, y, rows, keepc = e[:5]
            keepix = set(i for i, cc in enumerate(s.pal) if cc in keepc)
            held = np.zeros(s.idx.shape, bool)
            if len(e) > 5 and e[5]:                                      # and the outline round them: fingers keep their edge against the prop (T35)
                from scipy import ndimage
                held = PS.dark(s) & ndimage.binary_dilation(np.isin(s.idx, list(keepix)), structure=np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]], bool))
            for r_, row in enumerate(rows):
                for i_, ch in enumerate(row):
                    sx, sy = x + i_ - ox, y + r_ - oy
                    if ch == '.' or not (0 <= sx < s.w and 0 <= sy < s.h) or int(s.idx[sy, sx]) in keepix or held[sy, sx]: continue
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


def paint(ops, body, fr, fb, ox, oy, hdy, key):
    """T59 (k), rework: pixel maps (rows of palette letters, '.' keeps, '_' clears) drawn on a pose's finished layers, in
    the coordinates where the scene draws them: ('body' | 'front_body' | 'front', x, y, rows). The face's front is drawn
    headDy rows lower than the body, so its maps are moved up by that much; a layer the pose lacks is made. Hands at the
    face that the reduced picture drew as clumps are drawn whole this way (the DS grip, the laptop and the plane passed
    with Cole drawn so). Returns (body, front, front_body) as the build keeps them."""
    lay = {'body': (body.copy(), ox, oy), 'front': (fr[0].copy(), fr[1], fr[2]) if fr else None, 'front_body': (fb[0].copy(), fb[1], fb[2]) if fb else None}
    for name, x, y, rows in ops:
        if lay[name] is None: lay[name] = (Sprite(-np.ones(body.idx.shape, np.int16), list(body.pal)), ox, oy)
        s, sx, sy = lay[name]; s.rows(x - sx, y - sy - (hdy if name == 'front' else 0), rows, key)
    f, b = (l_ if l_ is not None and (l_[0].idx >= 0).any() else None for l_ in (lay['front'], lay['front_body']))
    return lay['body'][0], f, b


def _cat_clear(s, ox, oy, x0, y0, skin):
    """inside Maker's footprint (pasted at x0, y0): everything but the hand on her goes; the hand is redrawn clean, its
    finger gaps in the darkest skin and one outline round it (T25: the cat's own darks between the fingers had read as
    a black hand). In place."""
    from scipy import ndimage
    m = _maker_footprint(); box = np.zeros(s.idx.shape, bool)
    ys, xs = np.where(m); yy, xx = ys + y0 - oy, xs + x0 - ox; ok = (yy >= 0) & (yy < s.h) & (xx >= 0) & (xx < s.w); box[yy[ok], xx[ok]] = True
    box = ndimage.binary_dilation(box, structure=np.ones((3, 3), bool))
    sk = np.isin(s.idx, [i for i, c in enumerate(s.pal) if c in skin])
    hand = sk & box
    lab, n = ndimage.label(hand, structure=np.ones((3, 3), bool))       # specks of the cat's own colours that matched skin go
    for i in range(1, n + 1):
        part = lab == i
        if part.sum() < 6 and not (ndimage.binary_dilation(part, structure=np.ones((3, 3), bool)) & sk & ~box).any(): hand &= ~part
    whole = ndimage.binary_closing(hand | (sk & ~box), structure=np.ones((5, 5), bool)) & box
    whole = ndimage.binary_fill_holes(whole | (sk & ~box)) & box         # the hand with the gaps between its fingers
    line = ndimage.binary_dilation(whole, structure=np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]], bool)) & ~whole & box & ~sk
    dark_skin = sorted(skin, key=lambda c: sum(int(c[k:k + 2], 16) for k in (1, 3, 5)))[0]
    darks = [c for i, c in enumerate(s.pal) if PS.dark(Sprite(np.array([[i]], np.int16), s.pal))[0, 0]]
    ink = min(darks, key=lambda c: sum(int(c[k:k + 2], 16) for k in (1, 3, 5)))
    s.idx[box & ~whole & ~line] = -1
    s.idx[box & sk & ~whole] = -1
    s.idx[whole & ~hand] = s.color(dark_skin)
    s.idx[line] = s.color(ink)


def _maker_clear(s, ox, oy, who, x0, y0, box, hand_below):
    """T60 (n, o): while she is petted Maker lies at the desk's front edge in front of the figure, and the scene draws the
    pose, then Maker, then the pose again inside the petting hand's box (desk-scene.js PET_HAND: x0, y0, x1, y1, the ends
    not included) so the hand lies on her. The pose may now be whole behind her (the shirt down to the desk: no wall
    showing beside her), but inside that box and her exact footprint (pasted at x0, y0, as the scene lays her) it keeps
    only the hand: skin above row `hand_below` and the outline touching it; everything else there is hidden by her in the
    first pass and must not be drawn over her in the second. In place."""
    from scipy import ndimage as nd
    m = _maker_footprint(); foot = np.zeros(s.idx.shape, bool)
    ys, xs = np.where(m); yy, xx = ys + y0 - oy, xs + x0 - ox; ok = (yy >= 0) & (yy < s.h) & (xx >= 0) & (xx < s.w); foot[yy[ok], xx[ok]] = True
    inb = np.zeros(s.idx.shape, bool); bx0, by0, bx1, by1 = box
    inb[max(0, by0 - oy):max(0, by1 - oy), max(0, bx0 - ox):max(0, bx1 - ox)] = True
    sk = np.isin(s.idx, [i for i, c in enumerate(s.pal) if c in SOFTEN[who][0][0]]); sk[max(0, hand_below - oy):, :] = False
    ink = np.isin(s.idx, [i for i, c in enumerate(s.pal) if c in LINES[who] | {KEYS[who]['k']}])
    keep = sk | (ink & nd.binary_dilation(sk, structure=np.ones((3, 3), bool)))
    s.idx[inb & foot & ~keep] = -1


def _maker_ops(who, pose):
    """the 'maker' fix ops of a pose, or of the frame of that name (in its edits)"""
    for p, man in MANUAL.get(who, {}).items():
        if p == pose: return [e for e in man.get('fix', []) if e[0] == 'maker']
        spec = man.get('frames', {}).get(pose)
        if isinstance(spec, dict): return [e for e in spec.get('edits', []) if e[0] == 'maker']
    return []


def _face_guard(who, shape, ox, oy):
    """the base head and two pixels round it, in a pose sprite's coordinates: there a black line parts a hand from the
    face and stays black"""
    _, _, hm = layers(CHARACTERS[who]); g = _nd.binary_dilation(hm, structure=np.ones((3, 3), bool), iterations=2)
    out = np.zeros(shape, bool); hy, hx = np.where(g); py, px = hy - oy, hx - ox; ok = (py >= 0) & (py < shape[0]) & (px >= 0) & (px < shape[1])
    out[py[ok], px[ok]] = True
    return out


def _thin(m):
    """Zhang-Suen thinning of a small mask: lines two pixels thick become one"""
    m = m.copy().astype(np.uint8); H, W = m.shape
    def nb(y, x):
        g = lambda yy, xx: m[yy, xx] if 0 <= yy < H and 0 <= xx < W else 0
        return [g(y - 1, x), g(y - 1, x + 1), g(y, x + 1), g(y + 1, x + 1), g(y + 1, x), g(y + 1, x - 1), g(y, x - 1), g(y - 1, x - 1)]
    changed = True
    while changed:
        changed = False
        for step in (0, 1):
            kill = []
            for y, x in zip(*np.nonzero(m)):
                p = nb(y, x); b = sum(p); a = sum(1 for i in range(8) if p[i] == 0 and p[(i + 1) % 8] == 1)
                if not (2 <= b <= 6 and a == 1): continue
                if step == 0 and p[0] * p[2] * p[4] == 0 and p[2] * p[4] * p[6] == 0: kill.append((y, x))
                if step == 1 and p[0] * p[2] * p[6] == 0 and p[0] * p[4] * p[6] == 0: kill.append((y, x))
            for y, x in kill: m[y, x] = 0
            changed |= bool(kill)
    return m.astype(bool)


def _clean_hand(s, ox, oy, box, who, protect=None):
    """a hand redrawn clean inside the box (base coordinates; to-do T2, T23, T34, Ilinca's "messy hands"): the reduced
    picture drew each finger with black outlines that clumped into blobs. Black lines inside the hand (between skin and
    skin, however long) take a dark skin tone, one pixel wide; the outline round it is one black pixel wherever it meets
    the wall, closed where it had gaps, without spurs, notches or a second pixel of thickness; lone specks of another
    skin tone take their neighbours'. `protect`: a mask where black stays black (a hand against the cheek). In place."""
    from scipy import ndimage as nd
    x0, y0, x1, y1 = box; H, W = s.idx.shape
    inb = np.zeros((H, W), bool); inb[max(0, y0 - oy):max(0, y1 + 1 - oy), max(0, x0 - ox):max(0, x1 + 1 - ox)] = True
    skin_cols, tone = SOFTEN[who][0]; ink = KEYS[who]['k']
    ids = lambda cols: [i for i, c in enumerate(s.pal) if c in cols]
    skin = np.isin(s.idx, ids(skin_cols)); line = np.isin(s.idx, ids(LINES[who])); empty = s.idx < 0
    near_wall = nd.binary_dilation(empty, structure=np.ones((3, 3), bool))
    # 1. lines inside the hand: skin within three pixels on both sides along a row, a column or a diagonal, through
    #    line pixels only, and no wall beside them
    def reach(dy, dx, n=3):
        out = np.zeros((H, W), bool); live = line.copy()
        for k in range(1, n + 1):
            sh = lambda a: np.roll(np.roll(a, -dy * k, 0), -dx * k, 1)
            out |= live & sh(skin); live &= sh(line)
        return out
    held = nd.binary_dilation(np.isin(s.idx, ids(PS.PROPS)), structure=np.ones((3, 3), bool))   # the outline of a thing held stays
    inner = line & inb & ~near_wall & ~held & ((reach(-1, 0) & reach(1, 0)) | (reach(0, -1) & reach(0, 1)) | (reach(-1, -1) & reach(1, 1)) | (reach(-1, 1) & reach(1, -1)))
    if protect is not None: inner &= ~protect
    keep = _thin(inner)                                              # one pixel wide; the rest of a thick line is skin
    base_skin = max(ids(skin_cols), key=lambda i: int(((s.idx == i) & inb).sum()))
    s.idx[inner & ~keep] = base_skin; s.idx[keep] = s.color(tone)
    skin = np.isin(s.idx, ids(skin_cols)); line = np.isin(s.idx, ids(LINES[who])); empty = s.idx < 0
    n4 = lambda m: nd.convolve(m.astype(np.uint8), np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]], np.uint8), mode='constant')   # four-neighbours in m
    for _ in range(2):
        hand = skin & inb
        # 2. spurs: a skin pixel sticking out with at most one skin neighbour (the rest wall or outline) becomes outline
        spur = hand & (n4(hand) <= 1) & (n4(empty) >= 1)
        s.idx[spur] = s.color(ink)
        # notches: an outline pixel with skin on three sides becomes skin
        skin = np.isin(s.idx, ids(skin_cols)); line = np.isin(s.idx, ids(LINES[who])); hand = skin & inb
        notch = line & inb & (n4(hand) >= 3) & ~(protect if protect is not None else np.zeros_like(line))
        s.idx[notch] = base_skin
        skin = np.isin(s.idx, ids(skin_cols)); line = np.isin(s.idx, ids(LINES[who])); empty = s.idx < 0; hand = skin & inb
        # 3. the outline closed: wall touching the hand becomes outline
        s.idx[empty & inb & (n4(hand) >= 1)] = s.color(ink)
        line = np.isin(s.idx, ids(LINES[who])); empty = s.idx < 0
        # and one pixel thick: outline not beside the hand (only touching it at a corner, or a second row out), that
        # touches the wall and nothing but the hand's own outline, goes
        other = ~(skin | line | empty)                                 # sleeves, cuffs, props: their outline stays
        extra = line & inb & (n4(hand) == 0) & (n4(empty) >= 1) & ~nd.binary_dilation(other, structure=np.ones((3, 3), bool))
        s.idx[extra] = -1
        line = np.isin(s.idx, ids(LINES[who])); empty = s.idx < 0
        # and no tails: a pixel of outline poking out into the wall, held by one neighbour only
        tail = line & inb & (n4(line | skin | other) <= 1) & (n4(empty) >= 3)
        s.idx[tail] = -1
        skin = np.isin(s.idx, ids(skin_cols)); line = np.isin(s.idx, ids(LINES[who])); empty = s.idx < 0
    # 4. lone specks of another skin tone inside the hand
    hand = skin & inb; toneix = s.color(tone)
    for y, x in zip(*np.nonzero(hand)):
        if s.idx[y, x] == toneix: continue
        nbs = [int(s.idx[y + dy, x + dx]) for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1)) if 0 <= y + dy < H and 0 <= x + dx < W and hand[y + dy, x + dx] and s.idx[y + dy, x + dx] != toneix]
        if len(nbs) >= 3 and s.idx[y, x] not in nbs:
            s.idx[y, x] = max(set(nbs), key=nbs.count)


def _mitten(s, ox, oy, box, who, fingers=3, band=3, flat_top=False):
    """T60 ("at rest, cole's hands are badly drawn"): the hand in the box (base coordinates) as one closed shape: the gaps
    between dangling fingers closed, dark specks and shirt-dark lines inside it turned to skin, one black outline where
    it meets the wall, and `fingers` short finger lines in the darkest skin rising `band` rows from its lower edge. In place."""
    from scipy import ndimage as nd
    x0, y0, x1, y1 = box; H, W = s.idx.shape
    inb = np.zeros((H, W), bool); inb[max(0, y0 - oy):max(0, y1 + 1 - oy), max(0, x0 - ox):max(0, x1 + 1 - ox)] = True
    skin_cols = SOFTEN[who][0][0]; K = KEYS[who]
    ids = lambda cols: [i for i, c in enumerate(s.pal) if c in cols]
    skin = np.isin(s.idx, ids(skin_cols)) & inb
    whole = nd.binary_fill_holes(nd.binary_closing(skin, structure=np.ones((3, 3), bool), iterations=2) | skin) & inb
    whole = nd.binary_opening(whole, structure=np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]], bool))
    for _ in range(2):                                               # a smooth edge: lone spikes (a dangling fingertip) go
        n4 = nd.convolve(whole.astype(np.uint8), np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]], np.uint8), mode='constant')
        whole &= n4 >= 2
    light = s.color(K['s']); mid = s.color(K['m']); shade = s.color(K['a']); dark = s.color(K['d']); ink = s.color(K['k'])
    ys, xs = np.where(whole)
    if not len(ys): return
    bottom = {}
    for y, x in zip(ys, xs): bottom[x] = max(bottom.get(x, -1), y)
    for y, x in zip(ys, xs):                                         # even skin: light above, a shade along the lower edge
        s.idx[y, x] = shade if y >= bottom[x] - 1 else (mid if y >= bottom[x] - 3 else light)
    ring = nd.binary_dilation(whole, structure=np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]], bool)) & ~whole & inb
    s.idx[ring & (s.idx != s.color(K['t']))] = ink                  # one outline, whatever specks were there (a blue one sat in it)
    lowest = ys.min() + (ys.max() - ys.min()) // 2                   # scraps of dangling fingertips left below the new outline go
    cloth = s.color(K['t'])
    for y in range(max(0, lowest - oy + 0), min(H, y1 + 1 - oy)):
        for x in range(max(0, x0 - ox), min(W, x1 + 1 - ox)):
            if not whole[y, x] and not ring[y, x] and s.idx[y, x] >= 0 and s.idx[y, x] != cloth: s.idx[y, x] = -1
    for _ in range(2):                                               # and no tails: outline held by one pixel only, below the hand
        fig = (s.idx >= 0)
        n4 = nd.convolve(fig.astype(np.uint8), np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]], np.uint8), mode='constant')
        tail = inb & (s.idx == ink) & (n4 <= 1) & (np.arange(H)[:, None] >= lowest - oy)
        s.idx[tail] = -1
    cols = sorted(bottom); lo, hi = cols[0], cols[-1]
    for k in range(1, fingers + 1):                                  # finger lines, evenly across the lower edge
        x = int(round(lo + (hi - lo) * k / (fingers + 1)))
        if x not in bottom: continue
        for dy in range(1, band + 1):
            y = bottom[x] - dy + 1
            if whole[y, x]: s.idx[y, x] = dark


_FOOT = []
def _maker_footprint():
    """where Maker's lying sprite has pixels, facing left (as she lies to be petted): the stand-in cat pasted into the
    front-edge petting pictures (work folder petedge/guides.py) was exactly this"""
    if not _FOOT:
        import maker_build
        loaf = maker_build.sheet(big=True)['loaf']; _FOOT.append((loaf.idx >= 0)[:, ::-1])
    return _FOOT[0]


GREYS = {'#cfd2d4', '#9a9ea2', '#5f6368', '#dfe9f5', '#d9d5c8', '#ddd6cf'}


def despeck(spr, most=3):
    """lone specks of grey (a laptop's, a wall's or a chair's, left by the reduction: to-do T44 "Individual sprite elements
    need to be checked for extraneous elements"): a group of at most `most` grey pixels with no larger grey thing beside
    it takes its neighbours' colour"""
    from scipy import ndimage
    g = np.isin(spr.idx, [i for i, c in enumerate(spr.pal) if c in GREYS]); lab, n = ndimage.label(g, structure=np.ones((3, 3), bool))
    if not n: return spr
    out = spr.copy(); sizes = ndimage.sum(g, lab, index=np.arange(1, n + 1)); H, W = spr.idx.shape
    for i, sz in enumerate(sizes):
        if sz > most: continue
        for y, x in zip(*np.where(lab == i + 1)):
            nb = [int(spr.idx[y + dy, x + dx]) for dy in (-1, 0, 1) for dx in (-1, 0, 1) if (dy or dx) and 0 <= y + dy < H and 0 <= x + dx < W
                  and spr.idx[y + dy, x + dx] >= 0 and not g[y + dy, x + dx]]
            if nb: out.idx[y, x] = max(set(nb), key=nb.count)
    return out


def lift_prop(spr, ox, oy, cols, box):
    """the prop's pixels (its colours inside the box, base coordinates) and the dark outline touching them: (prop Sprite, mask)"""
    from scipy import ndimage
    x0, y0, x1, y1 = box; m = np.zeros(spr.idx.shape, bool)
    m[max(0, y0 - oy):max(0, y1 + 1 - oy), max(0, x0 - ox):max(0, x1 + 1 - ox)] = True
    part = m & np.isin(spr.idx, [i for i, c in enumerate(spr.pal) if c in cols])
    edge = m & ndimage.binary_dilation(part, structure=np.ones((3, 3), bool)) & PS.dark(spr)
    mask = part | edge; out = spr.copy(); out.idx[~mask] = -1
    return out, mask


def moved_parts(spr, ox, oy, box, dx, dy, cols, fill):
    """only what is of the given colours inside the box (base coordinates), with the dark line along it, moves by (dx, dy);
    where it was, the fill colour (what lies behind it) shows: hands and a bottle shaking in front of a still shirt"""
    from scipy import ndimage
    x0, y0, x1, y1 = box; inbox = np.zeros(spr.idx.shape, bool)
    inbox[max(0, y0 - oy):max(0, y1 + 1 - oy), max(0, x0 - ox):max(0, x1 + 1 - ox)] = True
    part = inbox & np.isin(spr.idx, [i for i, c in enumerate(spr.pal) if c in cols])
    m = part | (inbox & ndimage.binary_dilation(part, structure=np.ones((3, 3), bool)) & PS.dark(spr))
    out = spr.copy(); out.idx[m] = out.color(fill)
    ys, xs = np.nonzero(m); ty, tx = ys + dy, xs + dx; ok = (ty >= 0) & (ty < spr.h) & (tx >= 0) & (tx < spr.w)
    out.idx[ty[ok], tx[ok]] = spr.idx[ys[ok], xs[ok]]
    return out


def shifted(spr, ox, oy, box, dx, dy):
    """the pose with what is inside the box (base coordinates) moved by (dx, dy): a hand moving along a line"""
    out = spr.copy(); x0, y0, x1, y1 = box[0] - ox, box[1] - oy, box[2] - ox, box[3] - oy
    for y in range(max(0, y0), min(spr.h, y1 + 1)):
        for x in range(max(0, x0), min(spr.w, x1 + 1)):
            sx, sy = x - dx, y - dy
            if not (x0 <= sx <= x1 and y0 <= sy <= y1): continue
            out.idx[y, x] = spr.idx[sy, sx] if (0 <= sx < spr.w and 0 <= sy < spr.h) else -1   # past the sprite's edge is empty (it left a doubled outline)
    return out


# the neck, between the jaw and the collar, in base coordinates: x range and the collar row
NECK = {'cole': (28, 50, 49), 'ilinca': (23, 37, 49)}


# beside the neck, where a pose's shoulder stops short of the head and the wall showed through under the jaw (the face
# "lost its clean outline"): columns, last row
NECK_FILL = {'cole': (44, 60, 47)}
CLOTH_EDGE = {'cole': ('#010101', '#211f1f')}


def neck_patch(c, torso, jaw):
    """pixels of the base torso just under the jaw: (torso sprite, mask). Per column it reaches down only as far as the
    base portrait's neck skin goes, plus the collar's outline under it, so the patch has the portrait's round neckline;
    a patch cut off at one row made the T-shirt's neckline square (Cole's note 6)"""
    x0, x1, collar = NECK[c.name]; m = np.zeros(torso.idx.shape, dtype=bool)
    skin = [i for i, col in enumerate(torso.pal) if col in SOFTEN[c.name][0][0]]
    for x in range(x0, x1 + 1):
        top = jaw.get(x, 0) + 1
        col = torso.idx[top:collar + 9, x]; rows = np.where(np.isin(col, skin))[0]
        if not len(rows): continue                                   # no neck in this column of the portrait: the pose's own shirt stays
        bottom = top + int(rows.max()) + 1                           # the last neck pixel, and the collar line under it
        m[top:bottom + 1, x] = True
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


# T33 (2026-10-04, "When cole greets the user, he should raise his hand in a casual wave. The hand doesn't have to
# actually wave once raised, The other arm shouldn't move."): for each activity he can be greeting from, a pose whose left
# part (left of a seam, per row) is the wave picture's raised arm and shirt and whose right part is the activity's own,
# so the other arm stays exactly where it was. Things lying on the desk (laptop, paper, board, mug) stay too.
# A seam is a column, or ('arm', [(row from, row to, column), ...], column): in those rows the left edge of the first skin
# right of that column (the chin-on-fist arm and its elbow: the shirt left of it is the wave picture's, with no shade
# boundary down his chest), elsewhere the column
WAVE_FROM = {'cole': {'rest': 36, 'type': 30, 'write': 49, 'solder': 40, 'mug': 40, 'think': ('arm', [(44, 76, 38), (76, 100, 55)], 36)}}


def wave_from(c, act, wave, seam):
    """the activity pose `act` (a built entry) with its left part replaced by the wave pose's raised arm (see WAVE_FROM)"""
    from scipy import ndimage
    who = c.name; K = KEYS[who]; (ab, ax, ay), (wb, wx, wy) = act['body'], wave['body']
    x0, y0 = min(ax, wx), min(ay, wy); x1, y1 = max(ax + ab.w, wx + wb.w), max(ay + ab.h, wy + wb.h)
    out = Sprite(-np.ones((y1 - y0, x1 - x0), np.int16), list(ab.pal))
    def place(s, sx, sy):
        a = -np.ones(out.idx.shape, np.int16); src = np.array([out.color(col) for col in s.pal] + [-1], np.int16)
        a[sy - y0:sy - y0 + s.h, sx - x0:sx - x0 + s.w] = src[s.idx]; return a
    A, Wv = place(ab, ax, ay), place(wb, wx, wy)
    H, Wd = out.idx.shape; X = np.arange(Wd)[None, :] + x0; Y = np.arange(H)[:, None] + y0
    skin = set(SOFTEN[who][0][0]); askin = np.isin(A, [i for i, col in enumerate(out.pal) if col in skin])
    if isinstance(seam, tuple):                                      # along the arm's left edge (its outline stays the activity's)
        _, spans, col0 = seam; sx = np.full(Y.shape, col0)
        for ya, yb, xm in spans:
            for yy in range(ya, yb):
                r = yy - y0
                if not (0 <= r < H): continue
                xs = np.where(askin[r] & (np.arange(Wd) + x0 >= xm))[0]
                sx[r, 0] = (xs.min() + x0 - 1) if len(xs) else xm
    else: sx = np.full(Y.shape, seam)
    sx = np.broadcast_to(sx, (H, 1)) if sx.shape[1] == 1 else sx
    left = X < sx
    props = np.isin(A, [i for i, col in enumerate(out.pal) if col in PS.PROPS]) & (A >= 0)
    lab, n = ndimage.label(props, structure=np.ones((3, 3), bool))   # only whole things (a laptop, paper, board, mug), not specks of a pen or an iron
    if n:                                                             # or anything lying on the desk (an iron stand), however small
        low = ndimage.maximum(np.broadcast_to(Y, props.shape), lab, index=np.arange(1, n + 1))
        props &= np.isin(lab, [i + 1 for i, s_ in enumerate(ndimage.sum(props, lab, index=np.arange(1, n + 1))) if s_ >= 20 or low[i] >= c.desk - 3])
    dark = np.isin(A, [i for i, col in enumerate(out.pal) if PS.dark(Sprite(np.array([[i]], np.int16), out.pal))[0, 0]]) & (A >= 0)
    keep_a = props | (dark & ndimage.binary_dilation(props, structure=np.ones((3, 3), bool)))   # a laptop, paper, board or mug with its outline
    wskin = np.isin(Wv, [i for i, col in enumerate(out.pal) if col in skin])
    other = wskin & (Y >= 66) & (X >= 20)                           # the wave picture's other hand, on the desk: not wanted
    other = ndimage.binary_dilation(other, structure=np.ones((3, 3), bool)) & (Y >= 64) & (X >= 18) & (Wv >= 0) & ~np.isin(Wv, [out.color(K['t']), out.color(K['u'])])
    res = A.copy()
    res[left & ~keep_a] = -1
    take = left & (Wv >= 0) & ~other & ~keep_a & (Y <= c.desk - 1 + 0 * Y)
    res[take] = Wv[take]
    # the shirt goes on down to the desk where the wave picture's other arm was: between its side and the seam
    shirt = out.color(K['t'])
    for yy in range(max(46, y0), min(c.desk, y1)):
        r = yy - y0; xs = np.where((res[r] >= 0) & left[r])[0]
        if not len(xs): continue
        for xx in range(xs.min(), int(sx[r, 0]) - x0):
            if res[r, xx] < 0: res[r, xx] = shirt
    lab, n = ndimage.label(res >= 0, structure=np.ones((3, 3), bool))   # crumbs the cut left behind
    if n > 1:
        sizes = ndimage.sum(res >= 0, lab, index=np.arange(1, n + 1)); res[np.isin(lab, [i + 1 for i, s_ in enumerate(sizes) if s_ < 12])] = -1
    out.idx = res
    fr = None
    if act['front']:
        f, fx, fy = act['front']; fa = place(f, fx, fy); fa[left] = -1
        if (fa >= 0).any(): fr = (Sprite(fa, out.pal), x0, y0)
    return dict(body=(out, x0, y0), front=fr, pts={}, props=act['props'])


# T30 (2026-10-04, "My shoulders change shape and size frequently"): ten of his poses share the rest pose's shoulders;
# the others had higher, wider ones. Those take the rest pose's shoulder line: from his collar down, left of his neck (L)
# and right of it (R), the outline is the rest pose's, then over BLEND rows it eases out to the pose's own (its arms
# may be further out) by `end`; his own arm, hand and anything held stay in front. Sides with a raised arm keep theirs.
# T59 (k), rework: 'arm' boxes where a raised wrist beside his neck is his own arm, and 'fix' (fix ops after the cap): the
# yawn's forearm keeps its own outline where the rest pose's shoulder had shown a dark sliver beyond it
YAWN_FOREARM_EDGE = [('rows', 61, 54 + i, [r]) for i, r in enumerate(['.k_', '..k_', '...k_', '...k__', '...k___', '....k__', '.....k__', '......k__', '.......kk_'])]
# and in both, the capped left shoulder line closed where it stepped two pixels (a shirt pixel touched the wall)
SHOULDER_STEP = [('rows', 7, 56, ['k'])]
SHOULDERS = {'cole': {'think': {'L': 66, 'R': 64, 'arm': [(46, 44, 53, 53)], 'fix': SHOULDER_STEP}, 'yawn': {'L': 66, 'R': 62, 'arm': [(46, 36, 53, 53)], 'fix': YAWN_FOREARM_EDGE + SHOULDER_STEP}, 'facepalm': {'L': 66}, 'sip': {'R': 56},
                      'solder': {'L': 66, 'R': 66}, 'solder1': {'L': 66, 'R': 66}, 'petedge': {'L': 70, 'R': 66}, 'petedge2': {'L': 70, 'R': 66},
                      'petcat': {'L': 70}, 'petcat2': {'L': 70}, 'offer': {'L': 66}, 'offerEmpty': {'L': 66},
                      'surprise': {'L': 58}, 'talk': {'L': 70, 'R': 70}}}   # T58 (j): talking arms in a conversation took narrower, lower shoulders
BLEND = 10


def shoulder_cap(c, entry, rest, ends):
    """the pose `entry` with the rest pose's shoulder line (see SHOULDERS)"""
    from scipy import ndimage
    who = c.name; K = KEYS[who]; (pb, px_, py_), (rb, rx, ry) = entry['body'], rest['body']
    x0, y0 = min(px_, rx), min(py_, ry); x1, y1 = max(px_ + pb.w, rx + rb.w), max(py_ + pb.h, ry + rb.h)
    out = Sprite(-np.ones((y1 - y0, x1 - x0), np.int16), list(pb.pal))
    def place(s, sx, sy):
        a = -np.ones(out.idx.shape, np.int16); src = np.array([out.color(col) for col in s.pal] + [-1], np.int16)
        a[sy - y0:sy - y0 + s.h, sx - x0:sx - x0 + s.w] = src[s.idx]; return a
    A, R = place(pb, px_, py_), place(rb, rx, ry)
    own = np.isin(A, [i for i, col in enumerate(out.pal) if col in set(SOFTEN[who][0][0]) | set(PS.PROPS)]) & (A >= 0)
    Yg = np.arange(A.shape[0])[:, None] + y0; Xg = np.arange(A.shape[1])[None, :] + x0
    neckzone = (Yg < 54) & (Xg >= NECK[who][0] - 2) & (Xg <= NECK[who][1] + 2)
    for ax0, ay0, ax1, ay1 in ends.get('arm', ()):                        # T59 (k): a raised wrist beside the neck is an arm (the rest pose's
        neckzone &= ~((Xg >= ax0) & (Xg <= ax1) & (Yg >= ay0) & (Yg <= ay1))   # shirt had been pasted into it: the black block on his wrist)
    own &= ~neckzone                                                     # the neck is not an arm: the shoulder beside it is the rest pose's
    lab, n = ndimage.label(own, structure=np.ones((3, 3), bool))           # and skin that does not reach down to an arm is a scrap of the picture's own neck
    if n: own &= np.isin(lab, [i for i in range(1, n + 1) if (Yg[:, 0][np.where(lab == i)[0]] >= 52).any()])
    cloth = np.isin(A, [out.color(K['t']), out.color(K['u'])])
    own |= ndimage.binary_dilation(own, structure=np.ones((3, 3), bool)) & (A >= 0) & ~cloth & PS.dark(Sprite(np.where(A >= 0, A, 0).astype(np.int16), out.pal))
    res = A.copy(); ink = out.color(K['k']); collar = 30; x_l, x_r = NECK[who][0] + 2, NECK[who][1] - 2
    for side, end in ((k_, v_) for k_, v_ in ends.items() if k_ in ('L', 'R')):
        for yy in range(collar, end + 1):
            r = yy - y0
            if not (0 <= r < A.shape[0]): continue
            cols = np.arange(0, x_l - x0) if side == 'L' else np.arange(x_r - x0 + 1, A.shape[1])
            pa = np.where(A[r, cols] >= 0)[0]; ra = np.where(R[r, cols] >= 0)[0]
            if not len(pa): continue
            if not len(ra):                                               # the rest pose has no shoulder this high: nothing but his own arm stays
                for cx in cols:
                    if not own[r, cx]: res[r, cx] = -1
                continue
            e_p, e_r = (pa.min(), ra.min()) if side == 'L' else (pa.max(), ra.max())
            s = min(1.0, max(0.0, (yy - (end - BLEND)) / BLEND)); e_d = int(round(e_r + (e_p - e_r) * s))
            for k, cx in enumerate(cols):
                if own[r, cx]: continue                                   # his own arm or hand, in front
                outside = k < e_d if side == 'L' else k > e_d
                if outside: res[r, cx] = -1
                elif k == e_d: res[r, cx] = ink
                else: res[r, cx] = R[r, cx] if (s == 0 or A[r, cx] < 0) and R[r, cx] >= 0 else A[r, cx]
    out.idx = res
    return dict(entry, body=(out, x0, y0))


def build(c):
    who = c.name; ix = index(who); base = c.blank(); torso, head0, hm0 = layers(c); jaw0 = jaw_rows(c, base)
    hdy = HEAD_DY.get(who, 0); head, hm, jaw = shifted_head(head0, hm0, jaw0, hdy)   # the head where the scene draws it
    hair = set(c.HAIR) if hasattr(c, 'HAIR') else None; out = {}; neck = neck_patch(c, torso, jaw); chest = chest_patch(c, torso)
    for pose, meta in sorted(ix.items()):
        man = dict(MANUAL.get(who, {}).get(pose, {}))
        if HANDS.get(who, {}).get(pose): man['fix'] = list(man.get('fix', [])) + [('hand',) + b for b in HANDS[who][pose]]
        if man.get('base'): meta = ix[man['base']]                      # a pose built on another pose's picture (typing on the writing arms)
        spr = load(os.path.join(POSES, who, man.get('base', pose) + '.png'))
        if man.get('own_head'):                                          # the whole picture, head and all (a stretch leaning back)
            if man.get('fix'): spr = fix(spr, meta['x'], meta['y'], man['fix'], KEYS[who])
            out[pose] = dict(body=(soften(spr, who), meta['x'], meta['y']), front=None, pts=man.get('pts', {}), props={}, own_head=True)
            continue
        if man.get('fix'): spr = fix(spr, meta['x'], meta['y'], man['fix'], KEYS[who])     # before softening: a recoloured prop is not skin any more
        face = np.zeros(spr.idx.shape, bool); hy, hx = np.where(_nd.binary_dilation(hm0, structure=np.ones((3, 3), bool), iterations=2))   # the picture's own face
        py, px = hy - meta['y'], hx - meta['x']; ok = (py >= 0) & (py < spr.h) & (px >= 0) & (px < spr.w); face[py[ok], px[ok]] = True
        spr = soften(spr, who, keep=face)
        body, front = PS.split(spr, meta['x'], meta['y'], hm | hm0, jaw, man.get('front'), hair, None if man.get('keep_neck') else neck, man.get('front_mode', 'all'),   # the picture's own head goes too
                               base_head=head, chest=None if man.get('keep_chest') else chest,
                               limb=set().union(*[cols for cols, _ in SOFTEN[who]]) | set(PS.PROPS), face_pt=FACE_PT.get(who), own_head=hm0,
                               hands_touch={c_ for c_ in SOFTEN[who][1][0]} | {'#e4002b', '#a3001f', '#ff5a72'})
        if not man.get('keep_neck') and man.get('neck_fill', True): body = neck_fill(c, torso, head, body, meta['x'], meta['y'])
        if man.get('base_box'):                                          # clothes from the base portrait in a box (a white top that read as a cup)
            bx0, by0, bx1, by1 = man['base_box']; skin = set(SOFTEN[who][0][0])
            for y in range(by0, by1 + 1):
                for x in range(bx0, bx1 + 1):
                    sx, sy = x - meta['x'], y - meta['y']
                    if not (0 <= sx < body.w and 0 <= sy < body.h and 0 <= y < torso.h and 0 <= x < torso.w): continue
                    if torso.idx[y, x] < 0 or (body.idx[sy, sx] >= 0 and body.pal[body.idx[sy, sx]] in skin): continue
                    body.idx[sy, sx] = body.color(torso.pal[torso.idx[y, x]])
        for sx_, sy_, rows_ in man.get('stamp', []):                     # T51 (c): a hand-authored limb and what it holds, drawn whole over the cut pose
            body.rows(sx_ - meta['x'], sy_ - meta['y'], rows_, KEYS[who])
        front_body = None
        if hdy:                                                          # her face's front goes with the head; the rest is the body's
            if not man.get('front_face'): front_body, front = front, None
        if who in HAIR_FRONT_ROW:                                        # long hair: hands and things held below the collar go in front of it
            if hdy: front_body = hair_front(body, meta['x'], meta['y'], HAIR_FRONT_ROW[who], who, front_body, raw=spr)
            else: front = hair_front(body, meta['x'], meta['y'], HAIR_FRONT_ROW[who], who, front, raw=spr)
        if hdy and man.get('arm_front'):                                 # an arm crossing in front of her hair: its sleeve drawn with the body, over the hair
            fbm = front_body.copy() if front_body is not None else Sprite(-np.ones(spr.idx.shape, np.int16), list(spr.pal))
            cloth = np.isin(spr.idx, [i for i, c_ in enumerate(spr.pal) if c_ in SOFTEN[who][1][0]])
            for x0b, y0b, x1b, y1b in man['arm_front']:
                bx_ = np.zeros(spr.idx.shape, bool); bx_[max(0, y0b - meta['y']):max(0, y1b + 1 - meta['y']), max(0, x0b - meta['x']):max(0, x1b + 1 - meta['x'])] = True
                arm = cloth & bx_; arm |= _nd.binary_dilation(arm, structure=np.ones((3, 3), bool)) & bx_ & PS.dark(spr)
                for y_, x_ in zip(*np.where(arm)): fbm.idx[y_, x_] = fbm.color(spr.pal[spr.idx[y_, x_]])
                gaps = _nd.binary_fill_holes(arm) & ~arm                 # her own hair peeking through the sleeve: sleeve there too
                for y_, x_ in zip(*np.where(gaps)): fbm.idx[y_, x_] = fbm.color(SOFTEN[who][1][0] and '#292423')
            front_body = fbm
        if hdy and man.get('stamp'):                                     # T51 (c): and the same map in front of her head and hair, unshifted
            fbm = front_body.copy() if front_body is not None else Sprite(-np.ones(spr.idx.shape, np.int16), list(spr.pal))
            for sx_, sy_, rows_ in man['stamp']: fbm.rows(sx_ - meta['x'], sy_ - meta['y'], rows_, KEYS[who])
            front_body = fbm
        if man.get('fill_holes', True):                                  # repeated: a slit wider than a pixel closes from both sides in turn
            for _ in range(4):
                closed = close_holes(body, meta['x'], meta['y'], head, c.desk, hair)
                if np.array_equal(closed.idx, body.idx): break
                body = closed
        fr_ = (front, meta['x'], meta['y']) if front is not None and (front.idx >= 0).any() else None
        fb_ = (front_body, meta['x'], meta['y']) if front_body is not None and (front_body.idx >= 0).any() else None
        body = pinholes(body, meta['x'], meta['y'], head, [(fr_[0], fr_[1], fr_[2] + hdy) if fr_ else None, fb_], desk=c.desk)
        if hdy and fr_:                                                   # the face's front is drawn three rows lower: its copy in the body goes
            body = body.copy(); body.idx[fr_[0].idx >= 0] = -1
            body = pinholes(body, meta['x'], meta['y'], head, [(fr_[0], fr_[1], fr_[2] + hdy), fb_], desk=c.desk)
        for e in man.get('fix', []):                                     # the hole filling took Maker's outline for a hole: clear it again
            if e[0] == 'cat' and (len(e) < 5 or e[4]): body = body.copy(); _cat_clear(body, meta['x'], meta['y'], e[1], e[2], e[3])   # (T60: not again where a map closes the arm against her: 'maker' instead)
            if e[0] == 'late':                                           # T60 (n): an authored map exactly as drawn (the softening had opened its outline)
                body = fix(body, meta['x'], meta['y'], e[1], KEYS[who])
                if fb_:                                                  # and in her layer in front of the hair, where it has pixels
                    fbn = fix(fb_[0], meta['x'], meta['y'], e[1], KEYS[who]); fbn.idx[fb_[0].idx < 0] = -1; fb_ = (fbn, fb_[1], fb_[2])
            if e[0] == 'maker': body = body.copy(); _maker_clear(body, meta['x'], meta['y'], who, *e[1:])   # T60 (n, o): and here
        body = despeck(body)
        if man.get('paint'):                                             # T59 (k): hand-drawn maps on the finished layers, where they are drawn
            body, fr_, fb_ = paint(man['paint'], body, fr_, fb_, meta['x'], meta['y'], hdy, KEYS[who])
        # T60 (l): pixel maps drawn last, after the softening and the hole filling, so a hand-authored hand keeps every
        # outline pixel as drawn (softening had turned outline beside a fingertip into skin)
        if man.get('post'): body = fix(body, meta['x'], meta['y'], man['post'], KEYS[who])
        entry = dict(body=(body, meta['x'], meta['y']), front=fr_, front_body=fb_, pts=man.get('pts', {}), props={})
        masks = {}
        for name, (cols, box) in man.get('props', {}).items():
            # the prop comes from the pose before its head area was cut away (a laptop reaching up into the hair was cut
            # there, and the cat showed through that gap when the laptop was drawn over her alone)
            prop, mask = lift_prop(spr if spr.idx.shape == body.idx.shape else body, meta['x'], meta['y'], cols, box)
            entry['props'][name] = (prop, meta['x'], meta['y']); masks[name] = mask & (body.idx >= 0)
        out[pose] = entry
        for variant, name in man.get('empty', {}).items():
            from scipy import ndimage
            b2 = body.copy(); b2.idx[masks[name]] = -1
            lab, n = ndimage.label(b2.idx >= 0, structure=np.ones((3, 3), bool))           # crumbs of the prop's outline go too
            if n > 1:
                sizes = ndimage.sum(b2.idx >= 0, lab, index=np.arange(1, n + 1))
                b2.idx[np.isin(lab, [i + 1 for i, s in enumerate(sizes) if s < 12])] = -1
            if man.get('empty_fix', {}).get(variant): b2 = fix(b2, meta['x'], meta['y'], man['empty_fix'][variant], KEYS[who])   # e.g. close the hand
            out[variant] = dict(body=(b2, meta['x'], meta['y']), front=None, pts=entry['pts'], props={})
        for variant, spec in man.get('frames', {}).items():
            # a frame of motion: a box of the pose moved (dx, dy), only some parts moved ('move': box, dx, dy, colours, what
            # shows where they were), and/or pixel edits ('edits': fix ops); the front layer moves
            # with the body, so a hand that is in front of the hair or the face stays in front
            if isinstance(spec, dict): box, dx, dy, edits = spec.get('box'), spec.get('dx', 0), spec.get('dy', 0), spec.get('edits', [])
            else: (box, dx, dy), edits = spec, []
            moved = shifted(body, meta['x'], meta['y'], box, dx, dy) if box else body.copy()
            vf = shifted(entry['front'][0], meta['x'], meta['y'], box, dx, dy) if (box and entry['front']) else (entry['front'][0].copy() if entry['front'] else None)
            if isinstance(spec, dict) and spec.get('move'): moved = moved_parts(moved, meta['x'], meta['y'], *spec['move'])   # only some parts move
            if edits: moved = fix(moved, meta['x'], meta['y'], edits, KEYS[who])
            vfb = None
            if who in HAIR_FRONT_ROW:
                if hdy:                                                  # her body-front layer moves with the box too (phone1 had lost her hands)
                    fb0 = entry['front_body'][0] if entry.get('front_body') else None
                    vfb = (shifted(fb0, meta['x'], meta['y'], box, dx, dy) if box else fb0.copy()) if fb0 is not None else None
                    vfb = hair_front(moved, meta['x'], meta['y'], HAIR_FRONT_ROW[who], who, vfb)
                else: vf = hair_front(moved, meta['x'], meta['y'], HAIR_FRONT_ROW[who], who, vf)
            vfront = (vf, meta['x'], meta['y']) if vf is not None and (vf.idx >= 0).any() else None
            vfbody = (vfb, meta['x'], meta['y']) if vfb is not None and (vfb.idx >= 0).any() else None
            moved = pinholes(moved, meta['x'], meta['y'], head, [(vfront[0], vfront[1], vfront[2] + hdy) if vfront else None, vfbody], desk=c.desk)
            for e in _maker_ops(who, variant): moved = moved.copy(); _maker_clear(moved, meta['x'], meta['y'], who, *e[1:])   # T60 (n, o)
            out[variant] = dict(body=(moved, meta['x'], meta['y']), front=vfront, front_body=vfbody, pts=entry['pts'], props=entry['props'])
    if 'rest' in out:
        capped = dict(SHOULDERS.get(who, {}))
        for pose, ends in list(capped.items()):                          # T58: and every frame made from a capped pose (think1 had kept the old shoulders: a blip)
            m_ = MANUAL.get(who, {}).get(pose, {})
            for v in list(m_.get('frames', {})) + list(m_.get('empty', {})): capped.setdefault(v, ends)
        for pose, ends in capped.items():
            if pose in out:
                out[pose] = shoulder_cap(c, out[pose], out['rest'], ends); bb, bx, by = out[pose]['body']
                if ends.get('fix'): bb = fix(bb, bx, by, ends['fix'], KEYS[who])   # T59 (k): fixes where the capped line meets his own arm
                out[pose]['body'] = (pinholes(bb, bx, by, head, out[pose]['front'], desk=c.desk), bx, by)   # no gap where the line eased out
                for e in _maker_ops(who, pose): bb, bx, by = out[pose]['body']; bb = bb.copy(); _maker_clear(bb, bx, by, who, *e[1:]); out[pose]['body'] = (bb, bx, by)   # T60 (n, o)
    if 'wave' in out:
        for act, seam in WAVE_FROM.get(who, {}).items():
            if act in out:
                e = wave_from(c, out[act], out['wave'], seam); bb, bx, by = e['body']
                e['body'] = (pinholes(bb, bx, by, head, e['front'], desk=c.desk), bx, by); out[act + 'Wave'] = e
    return out
