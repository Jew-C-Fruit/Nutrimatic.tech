#!/usr/bin/env python3
"""
Nutrimatic desk scene - characters.py
Version 1.4.0

Created: 2026-10-02 - Cole and Ilinca as sprites: generated bases finished by hand in the face, cut into layers (v1.0.0)
Modified: 2026-10-02 - Cole's resting mouth is a half smile, not a straight line (v1.0.1)
Modified: 2026-10-02 - More mouths: grin and smirk for both, soft and pursed for Ilinca, so she isn't smiling all the time (v1.1.0)
Modified: 2026-10-03 - Ilinca looking down: the whole iris under the lowered lid, the pupil low, so she reads as looking at
  her work rather than half asleep (v1.2.0)
Modified: 2026-10-03 - Cole's note 10: a looking-down head for each (down_blank, down_layers, down_frames): the head
  tips toward the desk, from a generated picture of each looking down (klein for Cole, Qwen-Image-Edit 2511 for Ilinca,
  on the base grid; sprites/*-down-1x.png, the full-size pictures in sources/), finished here in the base face's own
  style: brows, glasses, lids, nose and mouth lower, more of the crown, the eyes downcast (v1.3.0)
Modified: 2026-10-04 - Note 11 ("eyes look closed on the look down; the current look down is perfect for a nod"): the
  looking-down head's eyes are frames now: 'closed' (the lids as they were, for a nod or a blink) and 'open' (the
  upper lid lowered, the iris low in the eye: looking at the work) (v1.4.0)

characters.py - Cole and Ilinca for the desk scene.

Each figure starts from a generated portrait reduced to a sprite (sprites/*-1x.png: FLUX.2 klein 4B on the photos,
then tools/portraits/pixelize.py; the full-size pictures are in sources/) and is finished here by hand: the face is blanked and redrawn feature by feature so that eyes, brows and
mouth can change, the figure is cut into a torso and a head so the head can nod, and the arms are taken off so the
scene can draw jointed ones. Everything the scene needs comes out of character(name) as plain data.
"""
import sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from spritekit import Sprite, load

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'sprites')


def diff(a, b):
    """pixels of b that differ from a, as [x, y, colour-or-None]"""
    ys, xs = np.where(a.idx != b.idx)
    return [[int(x), int(y), (None if b.idx[y, x] < 0 else b.pal[b.idx[y, x]])] for y, x in zip(ys, xs)]


def outline_cut(s, removed, color):
    """after removing pixels, draw the outline colour on what is now the figure's edge next to the removed area"""
    h, w = s.idx.shape
    for y in range(h):
        for x in range(w):
            if s.idx[y, x] >= 0 and any(0 <= yy < h and 0 <= xx < w and removed[yy, xx] for yy, xx in ((y, x - 1), (y, x + 1), (y - 1, x), (y + 1, x))):
                s.put(x, y, color)


# =====================================================================================================================
#  COLE  (candidate C9, seed 109)
# =====================================================================================================================
class Cole:
    name = 'cole'
    BASE = 'cole-301-1x.png'        # merged pick: C9's face, C3's hair and body, C1's skin
    K, BR, W, S, SM, SH, SD = '#010101', '#623e32', '#f9eee0', '#f8cda6', '#f6af8d', '#ee947c', '#dc7f6d'
    GOLD, DM, SHIRT, SHIRTD = '#7d6230', '#3d1714', '#211f1f', '#100f13'

    @classmethod
    def blank(c):
        s = load(os.path.join(SRC, c.BASE))
        s.fill(35, 20, 53, 30, c.S); s.fill(34, 31, 50, 39, c.S)             # glasses, eyes and brows; nose and mouth
        s.fill(54, 20, 56, 30, None)
        for y in range(20, 28): s.put(54, y, c.K)                            # right edge of the face
        for y in (28, 29): s.put(53, y, c.K)
        s.put(52, 30, c.K)
        for y in range(31, 36): s.put(51, y, c.K)
        s.put(50, 36, c.K); s.put(50, 37, c.K)
        s.put(53, 30, None); s.put(54, 28, None); s.put(54, 29, None)
        s.put(34, 20, c.SM); s.put(34, 21, c.SM); s.put(34, 22, c.SM)
        # glasses: black top bar and sides, thin gold lower rims
        for x in range(28, 54): s.put(x, 23, c.K)
        for y in range(24, 30): s.put(35, y, c.K); s.put(44, y, c.K)
        for x in range(36, 44): s.put(x, 30, c.GOLD)
        for y in range(24, 29): s.put(47, y, c.K); s.put(53, y, c.K)
        for x in range(48, 53): s.put(x, 29, c.GOLD)
        # nose
        for x, y, col in ((48, 31, c.BR), (48, 32, c.BR), (47, 33, c.BR), (46, 33, c.BR), (45, 33, c.BR), (44, 32, c.SH), (46, 32, c.SM), (47, 32, c.SM)): s.put(x, y, col)
        return s

    @classmethod
    def eyes(c, s, look=0, state='open'):
        if state == 'closed':
            for x in range(37, 43): s.put(x, 26, c.K)
            for x in range(48, 52): s.put(x, 26, c.K)
            return
        top = 25 if state == 'down' else 24                                  # looking down: the lid comes down a row
        for x in range(37, 43): s.put(x, top, c.K)
        for x in range(48, 52): s.put(x, top, c.K)
        for x in range(37, 42): s.put(x, top + 1, c.W)
        for x in range(48, 51): s.put(x, top + 1, c.W)
        px = 39 + look; rx = 49 + (1 if look > 0 else 0) - (1 if look < 0 else 0)
        rows = (top + 1,) if state == 'down' else (top + 1, top + 2)
        if state != 'down':
            for x in (38, 39, 40): s.put(x, top + 2, c.W)
        for y in rows:
            s.put(px, y, c.K); s.put(px + 1, y, c.K); s.put(rx, y, c.K); s.put(rx + 1, y, c.K)

    @classmethod
    def brows(c, s, kind='neutral'):
        def bar(x0, x1, y, slope):
            return [(x, y + int(round(slope * ((x - x0) / max(1, x1 - x0) - 0.5) * 2)) + d) for x in range(x0, x1 + 1) for d in (0, 1)]
        dy = {'neutral': 0, 'up': -2, 'down': 0, 'sad': -1}[kind]; sl = {'neutral': 0, 'up': 0, 'down': 1, 'sad': -1}[kind]
        for x, y in bar(36, 43, 20 + dy, sl) + bar(48, 52, 20 + dy, -sl): s.put(x, y, c.K)

    MX, MY = 38, 35
    MOUTHS = {
        'smile':   [".b........b.", "..bbbbbbbb..", "............", "....hhhh...."],
        'neutral': ["..........b.", "...bbbbbbb..", "............", ".....hhh...."],     # at rest: one corner up, a half smile
        'flat':    ["............", "..bbbbbbbbb.", "............", "............"],
        'frown':   ["............", "...bbbbbbb..", "..b.......b.", "............"],
        'open':    ["............", "...bbbbbbb..", "....wwwww...", "....ddddd...", ".....bbb...."],
        'o':       ["............", ".....bbb....", "....bdddb...", ".....bbb...."],
        'laugh':   [".b.........b", "..bbbbbbbbb.", "..bwwwwwwwb.", "...ddddddd..", "....bbbbb..."],
        'yawn':    ["....bbbbb...", "...bwwwwwb..", "...bdddddb..", "...bdddddb..", "...bdddddb..", "....bbbbb..."],
        'grin':    [".b........b.", "..bwwwwwwb..", "...bhhhhb...", "............"],
        'smirk':   ["..........b.", "...bbbbbbb..", "............", ".....hh....."],
    }

    @classmethod
    def mouth(c, s, kind='smile', at=None):
        mx, my = at or (c.MX, c.MY)
        s.rows(mx, my - (1 if kind == 'yawn' else 0), c.MOUTHS[kind], {'b': c.BR, 'w': c.W, 'h': c.SH, 'd': c.DM})

    @classmethod
    def full(c, look=0, eye='open', brow='neutral', mouth='smile'):
        s = c.blank(); c.eyes(s, look, eye); c.brows(s, brow); c.mouth(s, mouth); return s

    # ---- layers -------------------------------------------------------------------------------------------------
    JAW = [(29, 34), (29, 36), (30, 38), (31, 39), (32, 40), (34, 41), (36, 42), (38, 43), (41, 44), (42, 45), (45, 46), (47, 46)]

    @classmethod
    def head_mask(c, s):
        m = np.zeros(s.idx.shape, dtype=bool); pts = c.JAW
        def jaw_y(x):
            if x < pts[0][0]: return 33
            if x >= pts[-1][0]: return pts[-1][1]
            for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
                if x0 <= x <= x1: return y0 if x1 == x0 else int(round(y0 + (y1 - y0) * (x - x0) / (x1 - x0)))
            return pts[-1][1]
        for x in range(s.w): m[:jaw_y(x) + 1, x] = True
        return m & (s.idx >= 0)

    @classmethod
    def arm_mask(c, s):
        """the generated arms (sleeve and bare arm): removed from the torso, the scene draws jointed ones"""
        m = np.zeros(s.idx.shape, dtype=bool)
        for y in range(50, s.h):
            lx = 14 if y < 74 else 15
            rx = 61 if y < 69 else 60 if y < 77 else 59
            m[y, :lx + 1] = True; m[y, rx:] = True
        return m & (s.idx >= 0)

    joints = dict(shL=(11, 58), shR=(63, 58))
    arm = dict(upper=27, fore=23, rL=7, rR=6, sleeve=0.62, skin=['#f8cda6', '#ee947c', '#dc7f6d'], cloth=['#211f1f', '#100f13'], cuff=None, line='#010101')
    centre = 37          # the column of the sprite that sits on the character's x in the scene
    desk = 88            # the row of the sprite that meets the desk top
    points = dict(mouth=(43, 37), eye=(40, 25), chin=(44, 45), ear=(24, 28))

    # ---- looking down (note 10) ---------------------------------------------------------------------------------
    # The head tipped toward the desk: FLUX.2 klein 4B on the pose stage (seed 5108) gave the head's new shape (more of
    # the hair on top, the forelock lower, the jaw line and chin), reduced on the base grid (sprites/cole-down-1x.png).
    # Its face is redrawn here in the base's style, from x = 24: the brows and the glasses four rows lower, the lenses
    # seen from above (four rows instead of six), a longer nose pointing down, the jaw line in the base's dark brown.
    # The eyes are frames (down_eyes): open and looking down at the work, or closed for a nod. The mouth frames go one
    # column right and four rows down (DMX, DMY).
    DOWN = 'cole-down-1x.png'
    DMX, DMY = 39, 39
    DOWN_KEY = {'k': '#010101', 'K': '#211f1f', 'b': '#100f13', 'B': '#090507', 'z': '#0f0503', 'S': '#ee947c', 'm': '#f8cda6', 'M': '#f6af8d',
                'h': '#dc7f6d', 'H': '#623e32', 'd': '#f9eee0', 'D': '#7d6230', 'g': '#9a9ea2'}
    DOWN_ROWS = {
        24: "mBBmkBbMMMMMkkkkkkkkmmmmkkkkkmmk....",
        25: "mmBBMkkBMMMMkkkkkkkkmmmmkkkkkmmk....",
        26: "mmBBSkkBBMMM" + "m" * 19 + "k....",
        27: "mhhHS" + "k" * 26 + ".....",
        28: "mhhhm" + "kk" + "hhhh" + "k" + "m" * 8 + "k" + "mm" + "k" + "m" * 5 + "k" + "......",
        29: "mmhhm" + "kk" + "hhhh" + "k" + "m" * 8 + "k" + "mm" + "k" + "m" * 5 + "k" + "......",
        30: "BmmHM" + "MMhhhh" + "k" + "m" * 8 + "k" + "mm" + "k" + "m" * 5 + "k" + "......",
        31: "kmmmm" + "MMMMMm" + "k" + "m" * 8 + "k" + "mmm" + "DDDDD" + "k" + "......",
        32: ".kmmm" + "MMMMMmm" + "D" * 8 + "m" * 8 + "k" + ".......",
        33: ".kkkk" + "hMMMMMm" + "m" * 17 + "k" + "......",
        34: "..kkh" + "mMMMMmm" + "m" * 12 + "H" + "mmmm" + "k" + "......",
        35: "..kkh" + "mmMMMmm" + "m" * 12 + "H" + "mmmm" + "k" + "......",
        36: "...kh" + "mmMMMmm" + "m" * 8 + "S" + "m" + "MM" + "H" + "mmm" + "k" + ".......",
        37: "...kh" + "Szz" + "MMmm" + "m" * 9 + "HHH" + "mmmm" + "k" + ".......",
        38: "...kh" + "Smzz" + "Mmm" + "m" * 15 + "k" + "........",
        39: "...kh" + "hhmzz" + "mm" + "m" * 15 + "k" + "........",
        40: "...kh" + "hhhmzz" + "m" + "m" * 15 + "k" + "........",
        41: "....k" + "Mhhhmzz" + "m" * 14 + "k" + ".........",
        42: "...k" + "hMMhhhmzz" + "m" * 13 + "k" + ".........",
        43: "...k" + "MMMMhhhmzz" + "m" * 11 + "k" + "..........",
        44: "...k" + "MMMMmhhhmzz" + "m" * 9 + "k" + "...........",
        45: "..kz" + "MMMMmMhhhhmzz" + "m" * 7 + "k" + "...........",
        46: ".kk" + "MMMMMmMhhhhhmzzz" + "m" * 5 + "k" + "...........",
        47: "kbk" + "MMMMMmmMMhhhhh" + "hzzzz" + "kk" + "B" + "kk" + ".........",
    }
    # per column, the last row of the looking-down head (the jaw line, then the chin)
    DOWN_JAW = [(24, 33), (28, 33), (29, 36), (30, 37), (31, 38), (32, 39), (33, 40), (34, 41), (35, 42), (36, 43), (37, 43), (38, 44), (39, 45),
                (40, 45), (41, 46), (43, 46), (44, 47), (47, 47), (48, 46), (74, 46)]

    @classmethod
    def down_blank(c):
        s = load(os.path.join(SRC, c.DOWN))
        for y, row in c.DOWN_ROWS.items():
            for i, ch in enumerate(row): s.put(24 + i, y, None if ch == '.' else c.DOWN_KEY[ch])
        return s

    @classmethod
    def down_eyes(c, s, state='open'):
        lids = list(range(37, 43)) + list(range(48, 52))                 # inside the near and the far lens
        if state == 'closed':                                            # a nod: the lids down, a fold of skin above them
            for x in lids: s.put(x, 29, c.SH); s.put(x, 30, c.K)
            return
        for x in lids: s.put(x, 29, c.K)                                 # the upper lid lowered over eyes looking down
        for x, col in ((37, c.W), (38, c.W), (39, c.K), (40, c.K), (41, c.W), (48, c.W), (49, c.K), (50, c.K), (51, c.W)): s.put(x, 30, col)
        s.put(39, 31, c.K); s.put(40, 31, c.K)                           # the near iris low in the eye, against the lower lid

    @classmethod
    def down_mask(c, s):
        m = np.zeros(s.idx.shape, dtype=bool); pts = c.DOWN_JAW
        for x in range(s.w):
            y1 = pts[-1][1]
            for (x0, y0), (x1, yy1) in zip(pts, pts[1:]):
                if x0 <= x <= x1: y1 = y0 if x1 == x0 else int(round(y0 + (yy1 - y0) * (x - x0) / (x1 - x0))); break
            if x < pts[0][0]: y1 = pts[0][1]
            m[:y1 + 1, x] = True
        return m & (s.idx >= 0)


# =====================================================================================================================
#  ILINCA  (candidate I4, seed 204)
# =====================================================================================================================
class Ilinca:
    name = 'ilinca'
    BASE = 'ilinca-407-1x.png'      # I4 with a more confident bearing
    K, DB, HB, W = '#0b0503', '#5f4030', '#6f4b3a', '#fbfbf9'
    S, SA, SKIN_SRC = '#f9e2d2', '#f1a49b', '#faebe1'
    ROSE, NOSE, DM, BLAZER, TOPSH = '#b5705f', '#e0b3a2', '#4a1f20', '#292423', '#ddd6cf'

    @classmethod
    def blank(c):
        s = load(os.path.join(SRC, c.BASE))
        # the generator gave skin and the white top one colour: split them (top from row 55 down), warm the skin a little
        src = s.color(c.SKIN_SRC); top = s.color(c.W); skin = s.color(c.S)
        region = np.zeros(s.idx.shape, dtype=bool); region[55:, :] = True
        s.idx[(s.idx == src) & region] = top; s.idx[(s.idx == src) & ~region] = skin
        cream = s.color('#e1cec4'); s.idx[(s.idx == cream) & region] = s.color(c.TOPSH)
        spans = {15: (18, 29), 16: (18, 30), 17: (18, 30), 18: (18, 30), 19: (19, 31), 20: (19, 30), 21: (19, 32), 22: (19, 32), 23: (19, 33), 24: (19, 34), 25: (19, 34), 26: (19, 34),
                 29: (20, 35), 30: (20, 35), 31: (21, 33)}
        for y, (x0, x1) in spans.items(): s.fill(x0, y, x1, y, c.S)
        for y in (16, 17, 18): s.put(17, y, c.K)                             # far cheek edge where the brow and lashes had merged into it
        s.put(16, 16, c.HB); s.put(16, 17, c.HB); s.put(16, 18, c.HB); s.put(17, 19, c.HB); s.put(18, 19, c.K)
        s.put(31, 18, c.K); s.put(32, 19, c.K)
        for y in (22, 23, 24, 25): s.put(22, y, c.NOSE)                      # nose: a soft line, darker at the tip
        s.put(22, 26, c.ROSE); s.put(23, 27, c.ROSE); s.put(24, 27, c.ROSE)
        return s

    @classmethod
    def eyes(c, s, look=0, state='open'):
        if state == 'closed':
            for x in range(27, 33): s.put(x, 19, c.K)
            for x in range(18, 23): s.put(x, 19, c.K)
            return
        top = 19 if state == 'down' else 18
        for x in range(27, 33): s.put(x, top, c.K)
        for x in range(18, 23): s.put(x, top, c.K)
        for x in range(27, 32): s.put(x, top + 1, c.W)
        for x in range(19, 23): s.put(x, top + 1, c.W)
        ix = 29 + look; fx = 20 + look
        rows = (top + 1, top + 2)                                          # looking down: the lid lower, the iris whole below it
        for y in rows: s.put(ix, y, c.DB); s.put(ix + 1, y, c.DB); s.put(fx, y, c.DB); s.put(fx + 1, y, c.DB)
        py = top + 2 if state == 'down' else top + 1                       # the pupil sits low when she looks down at her work
        s.put(ix if look <= 0 else ix + 1, py, c.K); s.put(fx if look <= 0 else fx + 1, py, c.K)

    @classmethod
    def brows(c, s, kind='neutral'):
        near = {'neutral': [(26, 15), (27, 15), (28, 15), (29, 15), (30, 16)], 'up': [(26, 14), (27, 13), (28, 13), (29, 13), (30, 14)],
                'down': [(26, 16), (27, 16), (28, 15), (29, 15), (30, 15)], 'sad': [(26, 14), (27, 15), (28, 15), (29, 16), (30, 16)]}[kind]
        far = {'neutral': [(18, 16), (19, 15), (20, 15), (21, 15)], 'up': [(18, 14), (19, 13), (20, 13), (21, 13)],
               'down': [(18, 15), (19, 15), (20, 16), (21, 16)], 'sad': [(18, 16), (19, 16), (20, 15), (21, 14)]}[kind]
        for x, y in near + far: s.put(x, y, c.DB)

    MX, MY = 20, 28
    MOUTHS = {
        'smile':   [".r......r.", "..rrrrrr..", "...llll..."],
        'neutral': ["..........", "..rrrrrr..", "...llll..."],
        'flat':    ["..........", ".rrrrrrrr.", ".........."],
        'frown':   ["..........", "..rrrrrr..", ".r......r."],
        'open':    ["..........", "..rrrrrr..", "...dddd...", "...llll..."],
        'o':       ["..........", "...rrr....", "..rdddr...", "...lll...."],
        'laugh':   [".r......r.", "..rrrrrr..", "..wwwwww..", "...dddd...", "...llll..."],
        'yawn':    ["...rrrr...", "..rwwwwr..", "..rddddr..", "..rddddr..", "...llll..."],
        'grin':    [".r......r.", "..rwwwwr..", "...llll..."],
        'smirk':   ["........r.", "..rrrrrr..", "....ll...."],
        'soft':    ["..........", "...rrrr...", "...llll..."],
        'purse':   ["..........", "....rr....", "...rllr...", "....ll...."],
    }

    @classmethod
    def mouth(c, s, kind='smile', at=None):
        mx, my = at or (c.MX, c.MY)
        s.rows(mx, my - (1 if kind == 'yawn' else 0), c.MOUTHS[kind], {'r': c.ROSE, 'w': c.W, 'l': c.SA, 'd': c.DM})

    @classmethod
    def full(c, look=0, eye='open', brow='neutral', mouth='smile'):
        s = c.blank(); c.eyes(s, look, eye); c.brows(s, brow); c.mouth(s, mouth); return s

    HAIR = ('#5f4030', '#6f4b3a', '#9a6f50', '#bd8e5d', '#d9ae71')
    JAW = {18: 30, 19: 31, 20: 33, 21: 34, 22: 35, 23: 36, 24: 36, 25: 36, 26: 36, 27: 36, 28: 36, 29: 35, 30: 35, 31: 34, 32: 34, 33: 33, 34: 32, 35: 31,
           36: 30, 37: 30, 38: 30, 39: 30, 40: 30, 41: 29}

    @classmethod
    def head_mask(c, s):
        """hair anywhere (with its outline), plus the face down to the jaw"""
        from scipy import ndimage
        hair = np.isin(s.idx, [s.pal.index(h) for h in c.HAIR if h in s.pal])
        hair[49:58, 20:33] = False                                           # the necklace and the top's neckline are brown too
        dark = np.isin(s.idx, [i for i, col in enumerate(s.pal) if col in ('#010100', '#0b0503', '#0e0c0b')])
        m = hair | (ndimage.binary_dilation(hair, structure=np.ones((3, 3), bool)) & dark)
        for x, y1 in c.JAW.items(): m[8:y1 + 1, x] |= s.idx[8:y1 + 1, x] >= 0
        return m & (s.idx >= 0)

    @classmethod
    def arm_mask(c, s):
        m = np.zeros(s.idx.shape, dtype=bool)
        for y in range(46, s.h):
            m[y, 47:] = True                                                 # the near arm and shoulder cap
            if y >= 57: m[y, :9] = True                                      # the far arm
        return m & (s.idx >= 0)

    joints = dict(shL=(10, 62), shR=(51, 56))
    arm = dict(upper=25, fore=21, rL=5, rR=6, sleeve=1.0, skin=['#f9e2d2', '#f1a49b', '#e0b3a2'], cloth=['#292423', '#0e0c0b'], cuff='#3d3837', line='#010100')
    centre = 28
    desk = 84
    points = dict(mouth=(25, 30), eye=(29, 19), chin=(26, 36), ear=(38, 27))

    # ---- looking down (note 10) ---------------------------------------------------------------------------------
    # Qwen-Image-Edit 2511 tipped her head toward the desk (seed 2003) and kept her outline exactly; what it changed is
    # done here on her finished face: the hairline two rows lower (its pixels from the generated picture, reduced on the
    # base grid: sprites/ilinca-down-1x.png), brows three rows lower, the eyes downcast (the lash lines only), nose and
    # mouth two rows lower over the same chin. The eyes are frames (down_eyes): open looking down, or closed for a nod.
    DOWN = 'ilinca-down-1x.png'
    DMX, DMY = 20, 30
    FIXCOL = {'#d9a650': '#d9ae71', '#b5705f': '#bd8e5d'}         # the reduction read hair lights as prop gold, hair shade as her lip rose

    @classmethod
    def down_blank(c):
        s = c.blank(); g = load(os.path.join(SRC, c.DOWN))
        for y in (7, 8, 9):                                          # the hairline, two rows lower
            for x in range(16, 30):
                if g.idx[y, x] >= 0: col = g.pal[g.idx[y, x]]; s.put(x, y, c.FIXCOL.get(col, col))
        s.put(31, 18, c.S); s.put(32, 19, c.S)                       # the open eye's outer corner is not there when she looks down
        for x, y in [(26, 18), (27, 18), (28, 18), (29, 18), (30, 19), (18, 19), (19, 18), (20, 18), (21, 18)]: s.put(x, y, c.DB)
        for x, y in [(22, 22), (22, 23), (22, 26), (23, 27), (24, 27)]: s.put(x, y, c.S)
        for y in (24, 25, 26, 27): s.put(22, y, c.NOSE)
        s.put(22, 28, c.ROSE); s.put(23, 29, c.ROSE); s.put(24, 29, c.ROSE)
        return s

    @classmethod
    def down_eyes(c, s, state='open'):
        if state == 'closed':                                            # a nod: the lash lines only
            for x, y in [(27, 22), (28, 22), (29, 22), (30, 22), (31, 22), (32, 21), (18, 22), (19, 22), (20, 22), (21, 22), (17, 21)]: s.put(x, y, c.K)
            return
        top = 21                                                         # her open 'down' eyes, three rows lower: the lid low,
        for x in range(27, 33): s.put(x, top, c.K)                       # the iris whole under it, the pupil at its bottom
        for x in range(18, 23): s.put(x, top, c.K)
        for x in range(27, 32): s.put(x, top + 1, c.W)
        for x in range(19, 23): s.put(x, top + 1, c.W)
        for y in (top + 1, top + 2):
            for x in (29, 30, 20, 21): s.put(x, y, c.DB)
        s.put(29, top + 2, c.K); s.put(20, top + 2, c.K)

    @classmethod
    def down_mask(c, s): return c.head_mask(s)


CHARACTERS = {'cole': Cole, 'ilinca': Ilinca}


def layers(c):
    """(torso, head) sprites on the full-size canvas. The head is the blank face; features come as pixel lists."""
    from scipy import ndimage
    s = c.blank(); hm = c.head_mask(s); am = c.arm_mask(s) & ~hm
    rest = (s.idx >= 0) & ~hm & ~am
    lab, n = ndimage.label(rest, structure=np.ones((3, 3), int))
    if n > 1:                                                                # stray specks (outline fragments) belong to the head
        keep = 1 + int(np.argmax(ndimage.sum(rest, lab, index=np.arange(1, n + 1))))
        hm |= rest & (lab != keep)
    head = s.copy(); head.idx[~hm] = -1
    torso = s.copy(); torso.idx[hm | am] = -1
    outline_cut(torso, am, c.K)
    if hasattr(c, 'BLAZER'):                                                 # long hair lies on the torso: give the torso cloth underneath it
        cloth = torso.color(c.BLAZER)
        for x in range(torso.w):
            ys = np.where(torso.idx[46:, x] >= 0)[0]
            if len(ys):
                top = 46 + ys[0]
                for y in range(max(46, top - 16), top):
                    if hm[y, x] and torso.idx[y, x] < 0: torso.idx[y, x] = cloth
    return torso, head, hm


def down_layers(c):
    """the looking-down head as a layer on the full-size canvas (it is drawn instead of the head), down to its own jaw and
    never short of the base head's (the torso has nothing where the base head was)"""
    s = c.down_blank(); _, _, hm = layers(c); m = c.down_mask(s)
    base_rows = np.array([max([y for y in range(hm.shape[0]) if hm[y, x]], default=-1) for x in range(hm.shape[1])])
    for x in range(s.w):
        if base_rows[x] >= 0: m[:base_rows[x] + 1, x] |= s.idx[:base_rows[x] + 1, x] >= 0
    head = s.copy(); head.idx[~m] = -1
    return head


def down_frames(c):
    b = c.down_blank(); out = {'eyes': {}, 'mouth': {}}
    for state in ('open', 'closed'):
        s = b.copy(); c.down_eyes(s, state); out['eyes'][state] = diff(b, s)
    for k in c.MOUTHS:
        s = b.copy(); c.mouth(s, k, at=(c.DMX, c.DMY)); out['mouth'][k] = diff(b, s)
    return out


def frames(c):
    b = c.blank(); out = {'eyes': {}, 'brows': {}, 'mouth': {}}
    for state in ('open', 'down'):
        for look in (-1, 0, 1):
            s = b.copy(); c.eyes(s, look, state); out['eyes']['%s%d' % (state, look)] = diff(b, s)
    s = b.copy(); c.eyes(s, 0, 'closed'); out['eyes']['closed'] = diff(b, s)
    for k in ('neutral', 'up', 'down', 'sad'):
        s = b.copy(); c.brows(s, k); out['brows'][k] = diff(b, s)
    for k in c.MOUTHS:
        s = b.copy(); c.mouth(s, k); out['mouth'][k] = diff(b, s)
    return out


if __name__ == '__main__':
    from PIL import Image
    for name, c in CHARACTERS.items():
        torso, head, hm = layers(c)
        torso.view(os.path.join(HERE, '%s-torso.png' % name), zoom=7); head.view(os.path.join(HERE, '%s-head.png' % name), zoom=7)
        fr = frames(c); print(name, {k: {kk: len(vv) for kk, vv in v.items()} for k, v in fr.items()})
        # a sheet of mouths
        ims = []
        for k in c.MOUTHS:
            s = c.full(mouth=k); x0 = 14 if name == 'cole' else 0
            ims.append(s.crop(x0, 0, x0 + 50, 52).image())
        z = 6; Wd = sum(i.width for i in ims) * z + 10 * (len(ims) + 1); H = ims[0].height * z + 20
        sheet = Image.new('RGBA', (Wd, H), (246, 246, 244, 255)); x = 10
        for i in ims: sheet.alpha_composite(i.resize((i.width * z, i.height * z), Image.NEAREST), (x, 10)); x += i.width * z + 10
        sheet.convert('RGB').save(os.path.join(HERE, '%s-mouths.png' % name)); print(name, 'mouths', list(c.MOUTHS), sheet.size)
