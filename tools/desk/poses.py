#!/usr/bin/env python3
"""
Nutrimatic desk scene - poses.py
Version 1.8.0

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
    up, turning and scaling back down so its pixels stay clean"""
    m = SHAKER_KEYS[who]; rows = [''.join(m.get(ch, '.') for ch in r) for r in SHAKER]
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

# By eye, per pose: the box (base coordinates) whose pixels go over the face, and named points.
MANUAL = {
    'cole': {
        'sip': dict(front=(30, 26, 58, 48), front_mode='limb'),            # the fingers round the mug are in front of it, and of the chin
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
        'ds': dict(frames={'ds1': {'edits': [('rows', 29, 67, ['Rkmmk', 'Rkaak'])]},          # a thumb tip pressing a pixel in
                           'ds2': {'edits': [('rows', 44, 67, ['kmmkR', 'kaakR'])]}},
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
                        ('rows', 29, 67, ['kmmk', 'kaak']), ('rows', 45, 67, ['kmmk', 'kaak']),   # the two thumb tips on the base
                        # the right thumb climbed the lid's edge ("much too long"): the hand stops at the base, shirt above it
                        ('rows', 52, 57, ['ttttttt', 'ttttttt', 'ttttttt', 'ttttttt', 'ttttttt', 'kkkkkkt', 'ksssss.'])]),
        'think': dict(neck_fill=False, keep_neck=True, front=(30, 32, 58, 50), front_mode='arm'),   # the fist under his chin, in front of the jaw
        'hide': dict(fix=[('clear', -24, 89, 110, 104)]),                # hands in his lap: nothing of them below the desk line (note 9b)
        # note 9a, motion in every activity: frames the scene cycles through (a forearm typing behind the screen, a hand to
        # the trackpad, thumbs on the console, a fidgeting hand)
        'rest': dict(frames={'rest1': ((4, 84, 30, 99), 0, -1)}),
        # petting Maker lying beside him: the picture had a grey cat under his hand; it goes, and the scene lays Maker in
        # its place (RIG below), so the hand lies exactly on her back; the hand moves a little as it strokes
        'petcat': dict(fix=[('erase', 28, 60, 86, 93, CAT_GREYS)], frames={'petcat2': ((46, 56, 80, 82), -2, 0)}),
        # note 12: Maker lies at the desk's front edge now; this picture was made with her pasted there (work folder
        # petedge/), so the hand lands on her back; everything of the stand-in cat but the hand goes
        'petedge': dict(fix=[('cat', 31, 66, SKIN_COLE)], frames={'petedge2': ((62, 56, 90, 84), -2, 0)}),
        'stretch': dict(fix=[('clear', -8, 54, 7, 92), ('clear', 8, 53, 8, 53)]),   # a chair's edge behind him in the generated picture
        # props the scene also draws on their own: the laptop (the cat sits on it), the paper, the bottle being handed over
        # note T1 (2026-10-04): "when typing, hands should be COMPLETELY hidden behind laptop screen": below the sleeves
        # each forearm runs in behind the screen's edge, the shirt shows under it down to the desk, the fists are gone
        'type': dict(fix=[('clear', 14, 91, 64, 96), ('fill', 15, 90, 61, 90, '#010101', set()),   # the laptop stands on the desk line (note 9d)
                          ('rows', 0, 77, ['kuuuuuuuukkkkkkkk',               # T13: forearms as thick as the fists were
                                           'kmssssssssssssssm',
                                           'kmssssssssssssssm',
                                           'kmsssssssssssssss',
                                           'kmsssssssssssssss',
                                           'kmssssssssssssssm',
                                           'kassssssssssssmmm',
                                           'kaammmmmmmmmmaaaa',
                                           'kdddaaaaaaaaddddd',
                                           'kdddddddddddddddd',
                                           'kkkkkkkkkkkkkkkkk']),
                          ('rows', 65, 74, ['uuutttk______',
                                            'uuutttk______',
                                            'uuuttttk_____',
                                            'uuuuuuuk_____',
                                            'sssssssmk____',
                                            'ssssssssmk___',
                                            'ssssssssmk___',
                                            'sssssssssmk__',
                                            'sssssssssmk__',
                                            'msssssssamk__',
                                            'mmssssssaak__',
                                            'aammmmmaadk__',
                                            'ddaaaaaddk___',
                                            'kkkkkkkkkk___',
                                            '_____________'])],
                     props={'laptop': (LAPTOP, (20, 56, 100, 100))},
                     frames={'type1': ((-2, 72, 17, 90), 0, -1), 'type2': ((63, 70, 82, 90), 0, -1), 'typetrack': ((63, 70, 82, 90), -1, 0)}),
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
        'shake': dict(fix=[('erase', 30, 50, 50, 86, BOTTLE), ('under', 33, 55, shaker('cole'), SKIN_COLE)],
                      frames={'shake2': {'move': ((24, 44, 58, 86), 0, -2, SKIN_COLE | BOTTLE | {'#623e32'}, '#211f1f')}}),
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
        # note 8 (messy hands): the laptop squared off (straight edges, outline all round), and the two hands at its sides
        # redrawn clean: a white cuff, the hand going behind the screen
        # T24 (2026-10-04, "Her laptop is much too wide and interacts badly with her hair"): a new picture made with a
        # narrower laptop pasted into her stage (work folder ilinca-laptop/), its top below her hair's ends, so her hair
        # falls behind it; its top band back to grey; no hands (T1): her sleeves run in behind its edges
        'type': dict(frames={'type1': ((-3, 70, 4, 82), 0, 1), 'type2': ((52, 70, 58, 82), 0, 1), 'typetrack': ((52, 70, 58, 82), -1, 0)},
                     fix=[('recolour', 6, 64, 50, 64, {'#6f4b3a': '#5f6368', '#9a6f50': '#5f6368'}),
                          ('clear', 5, 44, 13, 47), ('rows', 5, 48, ['kkkkk']),     # a dark lump of blazer above her shoulder, by her hair
                          ('rows', -1, 73, ['JJJJJJ', 'JjjjjJ', 'Jjjjjj', 'Jjjjjj', 'Jjjjjj', 'JJJJJJ', 'JJJJJJ', 'kkkkkk', 'JJJJJJ', 'JJJJJJ', 'kkJJJJ', '__kkkk']),
                          ('rows', 52, 73, ['JJJJJJ', 'JjjjjJ', 'jjjjjJ', 'jjjjjJ', 'jjjjjJ', 'JJJJJJ', 'JJJJJJ', 'kkkkkk', 'JJJJJJ', 'JJJJJJ', 'JJJJkk', 'kkkk_k'])],
                     props={'laptop': (LAPTOP, (4, 62, 52, 88))}),
        'wave': dict(frames={'wave2': ((-12, 12, 12, 38), 1, 0)}),          # a casual wave: the hand rocks a pixel
        # her reaching sleeve ended in a spike up into her hair: its top is cut level at the shoulder, under the hair
        'petcat': dict(fix=[('erase', -38, 60, 32, 94, CAT_GREYS), ('clear', 0, 30, 16, 45), ('rows', 4, 46, ['kkkkkk'])], frames={'petcat2': ((-18, 54, 14, 76), 2, 0)}),
        'petedge': dict(fix=[('cat', -29, 62, SKIN_ILINCA)], frames={'petedge2': ((-12, 52, 14, 76), 2, 0)}),   # as Cole's: Maker at the front edge
        'stretch': dict(fix=[('clear', 63, 38, 67, 84)]),                # a chair's edge behind her
        'rest': dict(fix=[('recolour', 56, 55, 64, 66, {'#5f6368': '#191718', '#9a9ea2': '#292423'})],   # a grey chair corner by her shoulder
                     frames={'rest1': ((6, 72, 36, 88), 0, -1)}),
        'write': dict(fix=[('clear', -8, 87, 36, 92), ('recolour', -8, 85, 36, 86, {'#fbfaf5': None}),
                           ('under', -4, 85, ['k' + 'W' * 38 + 'k', 'k' * 40], SKIN_ILINCA | SLEEVE_ILINCA)],
                      props={'paper': (PAPER, (-14, 74, 40, 96))}, frames={'write1': ((-6, 60, 16, 90), 1, 0), 'write2': ((-6, 60, 16, 90), 2, -1)}),
        # note 5 (suit breaking, doubled hands, clipping hair): chin on her fist, the forearm crossing in front of her left
        # hair strand: in a box round the fist and the crossing, all the pose drew except its own hair goes in front
        'think': dict(keep_neck=True, front=[(14, 31, 25, 47), (8, 48, 25, 62)], front_mode='nothair',
                      fix=[('holes', 17, 63, 27, 75, '#ddd6cf')]),          # her white top in shadow, which the cut-out had taken for the grey wall
        # her phone and both hands are in front of her hair (they were drawn under it), and the phone is blue again (the
        # reduction had snapped the picture's blue phone to grey)
        'phone': dict(keep_chest=True, front=(4, 44, 44, 72), front_mode='limb', base_box=(12, 68, 34, 86),
                      frames={'phone1': ((10, 44, 40, 68), 0, -1)},
                      fix=[('recolour', 12, 44, 36, 70, {'#5f6368': '#3d5f99', '#9a9ea2': '#6f93cf'})]),
        'carry': dict(keep_chest=True),
        'drink': dict(front=(-6, 16, 18, 56), front_mode='limb',                  # T28: the same shaker, tipped to her lips
                      fix=[('erase', -6, 16, 24, 52, BOTTLE), ('under', 1, 27, shaker('ilinca', 38), SKIN_ILINCA)]),   # its spout at her mouth's corner
        'yawn': dict(front=(12, 24, 36, 42), front_mode='diff', keep_neck=True),
        # hands and sleeves that are in front of her hair
        'talk': dict(front=(-16, 28, 14, 64), front_mode='limb'),
        'call': dict(keep_chest=True, front=(4, 24, 15, 46), front_mode='limb'),
        'surprise': dict(keep_chest=True, front=(48, 24, 68, 58), front_mode='limb'),
        # the bottle came out in her skin colours
        'take': dict(fix=[('clear', -30, 78, 13, 84), ('erase', -12, 12, 4, 50, BOTTLE), ('under', -11, 14, shaker('ilinca'), SKIN_ILINCA)]),   # her fingers wrap the shaker; a stray grey bar cleared
        # note 9b: hands in her lap under the desk (when Maker walks by): her rest picture with the forearms and hands
        # taken out and the blazer and top carried straight down to the desk line (the model would not hide her hands)
        'hide': dict(keep_chest=True, fix=[('handsunder', 71, 84, 15, 25, ('#292423', '#191718', '#010100', '#fbfaf5', '#0b0503')),
                                           ('recolour', 56, 55, 66, 70, {'#5f6368': '#191718', '#9a9ea2': '#292423'})]),
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


def pinholes(body, ox, oy, head, front=None, most=8):
    """tiny gaps that show the wall from inside the figure (a few pixels, closed in by the body, the head or the front
    layer; left by a moved writing hand or a speck of the cut-out): filled from the nearest body pixel"""
    h, w = body.idx.shape; fig = body.idx >= 0
    hy, hx = np.where(head.idx >= 0); py, px = hy - oy, hx - ox; ok = (py >= 0) & (py < h) & (px >= 0) & (px < w)
    allfig = fig.copy(); allfig[py[ok], px[ok]] = True
    if front is not None:
        fs, fx, fy = front; fy_, fx_ = np.where(fs.idx >= 0); py, px = fy_ + fy - oy, fx_ + fx - ox
        ok = (py >= 0) & (py < h) & (px >= 0) & (px < w); allfig[py[ok], px[ok]] = True
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
            _, x0, y0, skin = e; _cat_clear(s, ox, oy, x0, y0, skin)    # but the hand on her, redrawn clean
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
            row = s.idx[top - oy]; xs = np.where(row >= 0)[0]; left, right = xs.min(), xs.max()
            for y in range(top - oy + 1, desk - oy + 1):
                if not (0 <= y < s.h): continue
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


_FOOT = []
def _maker_footprint():
    """where Maker's lying sprite has pixels, facing left (as she lies to be petted): the stand-in cat pasted into the
    front-edge petting pictures (work folder petedge/guides.py) was exactly this"""
    if not _FOOT:
        import maker_build
        loaf = maker_build.sheet(big=True)['loaf']; _FOOT.append((loaf.idx >= 0)[:, ::-1])
    return _FOOT[0]


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
            if x0 <= sx <= x1 and y0 <= sy <= y1 and 0 <= sx < spr.w and 0 <= sy < spr.h: out.idx[y, x] = spr.idx[sy, sx]
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
        fr_ = (front, meta['x'], meta['y']) if front is not None and (front.idx >= 0).any() else None
        body = pinholes(body, meta['x'], meta['y'], head, fr_)
        for e in man.get('fix', []):                                     # the hole filling took Maker's outline for a hole: clear it again
            if e[0] == 'cat': body = body.copy(); _cat_clear(body, meta['x'], meta['y'], e[1], e[2], e[3])
        entry = dict(body=(body, meta['x'], meta['y']), front=fr_, pts=man.get('pts', {}), props={})
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
            if who in HAIR_FRONT_ROW: vf = hair_front(moved, meta['x'], meta['y'], HAIR_FRONT_ROW[who], who, vf)
            vfront = (vf, meta['x'], meta['y']) if vf is not None and (vf.idx >= 0).any() else None
            moved = pinholes(moved, meta['x'], meta['y'], head, vfront)
            out[variant] = dict(body=(moved, meta['x'], meta['y']), front=vfront, pts=entry['pts'], props=entry['props'])
    return out
