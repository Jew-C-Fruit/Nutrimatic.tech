"""Pixel portraits of Cole and Ilinca, navel up. Shapes are built as masks, shaded by a light from the
upper left into 4 tones per material, outlined, then the features are stamped by hand."""
import math, sys
from PIL import Image

LIGHT = (-0.6, -0.8)

class Canvas:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.px = {}            # (x,y) -> hex colour
    def put(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h and c: self.px[(x, y)] = c
    def get(self, x, y): return self.px.get((x, y))
    def image(self, bg=None):
        im = Image.new("RGBA", (self.w, self.h), (0, 0, 0, 0) if bg is None else bg)
        for (x, y), c in self.px.items(): im.putpixel((x, y), hexrgb(c))
        return im

def hexrgb(h): return (int(h[1:3], 16), int(h[3:5], 16), int(h[5:7], 16), 255)

# ---------------- masks ----------------
def ellipse(cx, cy, rx, ry):
    m = set()
    for y in range(int(cy - ry) - 1, int(cy + ry) + 2):
        for x in range(int(cx - rx) - 1, int(cx + rx) + 2):
            if ((x + 0.5 - cx) / rx) ** 2 + ((y + 0.5 - cy) / ry) ** 2 <= 1.0: m.add((x, y))
    return m
def circle(cx, cy, r): return ellipse(cx, cy, r, r)
def poly(points):
    """scanline fill of a polygon given as float vertices"""
    m = set(); ys = [p[1] for p in points]
    for y in range(int(min(ys)), int(max(ys)) + 2):
        yc = y + 0.5; xs = []
        n = len(points)
        for i in range(n):
            (x1, y1), (x2, y2) = points[i], points[(i + 1) % n]
            if (y1 <= yc < y2) or (y2 <= yc < y1):
                xs.append(x1 + (yc - y1) * (x2 - x1) / (y2 - y1))
        xs.sort()
        for i in range(0, len(xs) - 1, 2):
            for x in range(int(math.floor(xs[i] + 0.5)), int(math.floor(xs[i + 1] + 0.5))): m.add((x, y))
    return m
def rrect(x0, y0, x1, y1, r):
    m = set()
    for y in range(int(y0), int(y1) + 1):
        for x in range(int(x0), int(x1) + 1):
            dx = max(x0 + r - x, 0, x - (x1 - r)); dy = max(y0 + r - y, 0, y - (y1 - r))
            if dx * dx + dy * dy <= r * r + 0.5: m.add((x, y))
    return m
def band(mask, y0, y1): return {p for p in mask if y0 <= p[1] <= y1}
def edge(mask):
    return {(x, y) for (x, y) in mask if any((x + dx, y + dy) not in mask for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))}

# ---------------- shading ----------------
def tone(d, tones):
    """d in [-1,1] facing the light -> colour from [light, base, shade, dark]"""
    if d > 0.5: return tones[0]
    if d > -0.12: return tones[1]
    if d > -0.58: return tones[2]
    return tones[3]
def shade_ellipsoid(cv, mask, cx, cy, rx, ry, tones, bulge=1.0):
    for (x, y) in mask:
        nx, ny = (x + 0.5 - cx) / rx, (y + 0.5 - cy) / ry
        cv.put(x, y, tone((nx * LIGHT[0] + ny * LIGHT[1]) * bulge, tones))
def shade_cylinder(cv, mask, cx, half, tones, tilt=0.0):
    for (x, y) in mask:
        nx = (x + 0.5 - cx) / half
        cv.put(x, y, tone(nx * LIGHT[0] + tilt, tones))
def shade_lumps(cv, mask, lumps, tones):
    """hair as a bunch of spheres: each pixel shaded by the lump it belongs to"""
    for (x, y) in mask:
        best = None
        for (lx, ly, r) in lumps:
            d2 = (x + 0.5 - lx) ** 2 + (y + 0.5 - ly) ** 2
            if d2 <= r * r and (best is None or r < best[2]): best = (lx, ly, r, d2)
        if best is None:
            cv.put(x, y, tones[1]); continue
        lx, ly, r, _ = best
        nx, ny = (x + 0.5 - lx) / r, (y + 0.5 - ly) / r
        cv.put(x, y, tone(nx * LIGHT[0] + ny * LIGHT[1], tones))
def outline(cv, mask, colour, only=None):
    for p in edge(mask):
        if only is None or only(p): cv.put(p[0], p[1], colour)
def stamp(cv, rows, x0, y0, pal):
    for r, row in enumerate(rows):
        for i, k in enumerate(row):
            if k != "." and k in pal: cv.put(x0 + i, y0 + r, pal[k])
def line(cv, x0, y0, x1, y1, c):
    n = max(abs(x1 - x0), abs(y1 - y0), 1)
    for i in range(n + 1):
        cv.put(round(x0 + (x1 - x0) * i / n), round(y0 + (y1 - y0) * i / n), c)

# ---------------- palettes ----------------
COLE = dict(
    skin=["#f6d6b6", "#e8b58d", "#c98d66", "#9e6646"], skinO="#5c3824",
    hair=["#5a3f2e", "#2e1d13", "#1c110a", "#0d0704"], hairO="#0a0503",
    shirt=["#6d9fd9", "#3f73b0", "#2b5280", "#1b3658"], shirtO="#122540",
    frame="#1a1a1a", rim="#6b6b6b", lens="#dbe8f4", lip="#8a4a40", lipL="#d9977d", mouthD="#4a2420",
    iris="#5a3a24", irisD="#2d1a0c", eyeW="#fbf8f2", lidL="#b07a58"
)
ILINCA = dict(
    skin=["#fbe3cc", "#f1c6a6", "#d9a07e", "#b27858"], skinO="#6a4030",
    hair=["#c9a06e", "#9a7249", "#6e4d30", "#4a3220"], hairO="#2f1f12",
    blazer=["#3c3c44", "#232328", "#161619", "#0d0d10"], blazerO="#07070a",
    top=["#ffffff", "#efeeea", "#d5d3cd", "#b8b5ae"],
    lip="#c8667a", lipL="#ee9fae", lipD="#9e4558", blush="#f0b0a0",
    iris="#6a4630", irisD="#3a2314", eyeW="#fbf8f2", lidL="#c48b6c", lash="#2a1a12", gold="#e2b55a"
)

# ================= COLE: a largish man, navel up, 64 x 90 =================
def paint_cole():
    cv = Canvas(64, 90); P = COLE
    cx = 32
    # torso + arms (drawn first, the head goes over the neck)
    torso = poly([(23, 42), (41, 42), (54, 47), (58, 55), (58, 90), (6, 90), (6, 55), (10, 47)])
    left_arm = rrect(4, 50, 15, 90, 5); right_arm = rrect(49, 50, 60, 90, 5)
    body = torso | left_arm | right_arm
    shade_cylinder(cv, torso, cx, 26, P["shirt"])
    shade_cylinder(cv, left_arm, 9.5, 6, P["shirt"]); shade_cylinder(cv, right_arm, 54.5, 6, P["shirt"], tilt=-0.35)
    # shoulder tops catch the light, armpit seams, chest folds
    for (x, y) in torso:
        if y < 46 and x < 40: cv.put(x, y, P["shirt"][0] if y < 44 else P["shirt"][1])
        if y < 46 and x >= 44: cv.put(x, y, P["shirt"][2])
    for y in range(52, 90): cv.put(15, y, P["shirt"][2]); cv.put(49, y, P["shirt"][3])
    line(cv, 16, 56, 26, 66, P["shirt"][2]); line(cv, 17, 62, 25, 70, P["shirt"][2]); line(cv, 48, 58, 40, 68, P["shirt"][3]); line(cv, 47, 66, 41, 74, P["shirt"][3])
    # henley: round neckline, placket, buttons
    neckline = ellipse(cx, 44, 9, 4)
    for (x, y) in neckline:
        if (x, y) in torso: cv.put(x, y, P["skin"][2] if y > 42 else P["skin"][1])
    for p in edge(neckline):
        if p in torso and p[1] >= 43: cv.put(p[0], p[1], P["shirt"][3])
    for y in range(46, 66):
        for x in range(29, 36): cv.put(x, y, P["shirt"][0] if x in (30, 31) else P["shirt"][1])
        cv.put(29, y, P["shirt"][3]); cv.put(35, y, P["shirt"][3])
    for by in (49, 55, 61):
        cv.put(32, by, "#f4f1ea"); cv.put(33, by, "#f4f1ea"); cv.put(32, by + 1, "#d8d4ca"); cv.put(33, by + 1, "#d8d4ca"); cv.put(33, by + 1, "#9a968e")
    outline(cv, body, P["shirtO"])
    # neck
    neck = rrect(26, 34, 38, 44, 2)
    shade_cylinder(cv, neck, cx, 6, P["skin"])
    for (x, y) in neck:
        if y < 39: cv.put(x, y, P["skin"][3] if x > 29 else P["skin"][2])   # shadow under the jaw
    # head: a long oval with a square-ish jaw
    head = ellipse(cx, 22, 11.5, 13.5) | poly([(22, 24), (42, 24), (42, 32), (38, 37), (26, 37), (22, 32)])
    shade_ellipsoid(cv, head, cx - 1, 22, 11.5, 14, P["skin"], bulge=0.9)
    for (x, y) in head:                                                     # jaw and temple shadows
        if y >= 30 and x > 36: cv.put(x, y, P["skin"][2] if y < 35 else P["skin"][3])
        if y >= 35 and 27 <= x <= 36: cv.put(x, y, P["skin"][2])
    ears = circle(20.5, 25, 2.6) | circle(43.5, 25, 2.6)
    for (x, y) in ears:
        if (x, y) not in head: cv.put(x, y, P["skin"][1] if x < 32 else P["skin"][2])
    cv.put(20, 25, P["skin"][2]); cv.put(44, 25, P["skin"][3]); cv.put(44, 26, P["skin"][3])
    outline(cv, head | ears, P["skinO"], only=lambda p: p[1] > 12)
    # hair: short curls as lumps over the crown, trimmed sides, a curl on the forehead
    lumps = [(23, 12, 5), (28, 9, 5.5), (34, 8, 5.5), (40, 10, 5), (44, 15, 4.5), (20, 16, 4), (31, 13, 7), (37, 13, 6), (25, 15, 5), (41, 17, 4), (18, 20, 3), (46, 20, 3)]
    hair = set()
    for l in lumps: hair |= circle(*l)
    hairline = {(x, y) for x in range(14, 50) for y in range(0, 30) if y < 15 + 0.028 * (x - 33) ** 2}
    hair = (hair & hairline) | {(x, y) for (x, y) in hair if (x < 22 or x > 42) and y < 24}
    hair |= circle(36, 16, 1.8)                                              # the forehead curl
    hair -= {(x, y) for (x, y) in hair if y >= 26}
    shade_lumps(cv, hair, lumps, P["hair"])
    for (x, y) in hair:                                                     # hair shadow where it meets the forehead
        if (x, y + 1) in head and (x, y + 1) not in hair: cv.put(x, y + 1, P["skin"][2])
    outline(cv, hair, P["hairO"], only=lambda p: True)
    for (x, y) in hair:
        if (x, y + 1) not in hair and (x, y + 1) in head: cv.put(x, y, P["hair"][2])
    # brows (thick, straight, a touch of arch), then browline glasses over them
    stamp(cv, ["bbbbbb.", ".bbbbbb"], 23, 17, {"b": P["hair"][2]}); stamp(cv, [".bbbbbb", "bbbbbb."], 35, 17, {"b": P["hair"][2]})
    # eyes
    eye = ["LLLLLL..", "wIiiwL..", "wiPiwl..", ".llll..."]
    pal = {"L": "#3a2416", "w": P["eyeW"], "I": P["irisD"], "i": P["iris"], "P": "#120a05", "l": P["lidL"]}
    stamp(cv, eye, 23, 20, pal); stamp(cv, eye, 34, 20, pal)
    cv.put(25, 21, "#ffffff"); cv.put(36, 21, "#ffffff")
    # glasses: heavy top bar, thin rims, bridge, temples, a glint
    for x in range(21, 44): cv.put(x, 19, P["frame"]); cv.put(x, 18, P["frame"] if x not in (31, 32, 33) else cv.get(x, 18))
    for y in range(20, 25): cv.put(21, y, P["frame"]); cv.put(30, y, P["frame"]); cv.put(34, y, P["frame"]); cv.put(43, y, P["frame"])
    for x in range(22, 30): cv.put(x, 25, P["rim"])
    for x in range(35, 43): cv.put(x, 25, P["rim"])
    cv.put(31, 20, P["frame"]); cv.put(32, 20, P["frame"]); cv.put(33, 20, P["frame"])
    cv.put(20, 20, P["frame"]); cv.put(19, 21, P["frame"]); cv.put(44, 20, P["frame"]); cv.put(45, 21, P["frame"])
    cv.put(22, 20, P["lens"]); cv.put(23, 20, P["lens"]); cv.put(22, 21, P["lens"]); cv.put(35, 20, P["lens"]); cv.put(36, 20, P["lens"])
    # nose: bridge shadow on the right, tip, nostrils
    for y in range(24, 29): cv.put(34, y, P["skin"][2])                     # the bridge's shadow side
    cv.put(32, 28, P["skin"][0])                                            # tip
    cv.put(30, 30, P["skin"][3]); cv.put(34, 30, P["skin"][3]); cv.put(31, 30, P["skin"][2]); cv.put(33, 30, P["skin"][2]); cv.put(32, 30, P["skin"][2])
    # mouth: a clean line with the corners lifted, a shaded lower lip
    cv.put(27, 33, P["mouthD"]); cv.put(37, 33, P["mouthD"])
    for x in range(28, 37): cv.put(x, 34, P["mouthD"])
    for x in range(29, 36): cv.put(x, 35, P["lip"])
    cv.put(31, 35, P["lipL"]); cv.put(32, 35, P["lipL"])
    for x in range(30, 35): cv.put(x, 36, P["skin"][2])
    return cv

# ================= ILINCA: petite, navel up, 56 x 90 (she stands shorter in the frame) =================
def paint_ilinca():
    cv = Canvas(56, 90); P = ILINCA
    cx = 28
    top0 = 14                                                              # her hair starts lower: smaller overall height
    # hair behind everything: crown + two falling masses with wavy outer edges, ending in soft curls
    def hair_mask():
        m = circle(cx, top0 + 12, 12.5) | ellipse(cx, top0 + 15, 13.5, 11)
        for y in range(top0 + 8, 76):
            t = (y - top0 - 8) / 60.0
            spread = 12 + 8 * min(t, 0.7) / 0.7 + (0 if t < 0.85 else -14 * (t - 0.85) / 0.15)
            wl = 1.0 * math.sin(y / 5.0)
            wr = 1.0 * math.sin(y / 4.6 + 1.2)
            xl, xr = cx - spread + wl, cx + spread + wr
            inner_l, inner_r = (cx - 6 - 0.15 * (y - 40), cx + 6 + 0.15 * (y - 40)) if y > 44 else (cx - 20, cx + 20)
            for x in range(int(xl), int(xr) + 1):
                if y <= 44 or x <= inner_l or x >= inner_r: m.add((x, y))
        return {p for p in m if p[1] >= top0}
    hair_back = hair_mask()
    # face: an oval with a soft pointed chin
    face = ellipse(cx, top0 + 20, 9.5, 12) | poly([(19, top0 + 24), (37, top0 + 24), (33, top0 + 33), (28, top0 + 35), (23, top0 + 33)])
    # body: slim neck, narrow sloping shoulders, waist taper
    neck = rrect(24, top0 + 32, 32, top0 + 42, 2)
    torso = poly([(23, top0 + 41), (33, top0 + 41), (40, top0 + 44), (44, top0 + 52), (43, 90), (13, 90), (12, top0 + 52), (16, top0 + 44)])
    larm = rrect(8, top0 + 48, 15, 90, 3); rarm = rrect(41, top0 + 48, 48, 90, 3)
    body = torso | larm | rarm
    # paint order: back hair, body, neck, face, front hair
    for (x, y) in hair_back:
        t = (y - top0) / 62.0
        strand = (x + 1.2 * math.sin(y / 6.0) + (y // 9)) % 6
        base = P["hair"][1]
        if x < cx - 4 and strand < 1.6: base = P["hair"][0]
        elif x > cx + 4 and strand < 1.2: base = P["hair"][0]
        if (x > cx + 10 and strand > 4.4) or (t > 0.8): base = P["hair"][2]
        if abs(x - cx) < 10 and y > top0 + 34: base = P["hair"][2]           # under the face it's in shadow
        cv.put(x, y, base)
    for (x, y) in hair_back:                                                # crown highlight and the parting
        if y < top0 + 9 and x < cx + 4 and (x + y) % 5 in (0, 1): cv.put(x, y, P["hair"][0])
        if y < top0 + 11 and x in (cx, cx - 1) and y > top0 + 1: cv.put(x, y, P["hair"][3])
    outline(cv, hair_back, P["hairO"])
    shade_cylinder(cv, torso, cx, 15, P["blazer"])
    shade_cylinder(cv, larm, 11.5, 4, P["blazer"]); shade_cylinder(cv, rarm, 44.5, 4, P["blazer"], tilt=-0.3)
    for (x, y) in torso:
        if y < top0 + 47 and x < cx: cv.put(x, y, P["blazer"][0])
    for y in range(top0 + 50, 90): cv.put(15, y, P["blazer"][2]); cv.put(41, y, P["blazer"][3])
    # lapels: a V of lighter blazer with white top inside, a single button, a thin chain
    for y in range(top0 + 41, top0 + 66):
        t = (y - top0 - 41) / 25.0
        hw = int(round(6 - 6 * t)); lw = 3
        for x in range(cx - hw, cx + hw + 1): cv.put(x, y, P["top"][0] if x < cx else P["top"][1])
        for x in range(cx - hw - lw, cx - hw): cv.put(x, y, P["blazer"][0])
        for x in range(cx + hw + 1, cx + hw + lw + 1): cv.put(x, y, P["blazer"][1])
        cv.put(cx - hw - lw - 1, y, P["blazer"][3]); cv.put(cx + hw + lw + 1, y, P["blazer"][3])
    cv.put(cx, top0 + 68, "#8a8a90"); cv.put(cx, top0 + 69, "#5a5a60")
    for i in range(0, 8): cv.put(cx - 5 + i // 2, top0 + 43 + i, P["gold"]); cv.put(cx + 5 - i // 2, top0 + 43 + i, P["gold"])
    cv.put(cx, top0 + 51, P["gold"]); cv.put(cx, top0 + 52, "#f4d58a")
    outline(cv, body, P["blazerO"])
    shade_cylinder(cv, neck, cx, 4, P["skin"])
    for (x, y) in neck:
        if y < top0 + 37: cv.put(x, y, P["skin"][3] if x > 27 else P["skin"][2])
    shade_ellipsoid(cv, face, cx - 1, top0 + 20, 9.5, 12.5, P["skin"], bulge=0.85)
    for (x, y) in face:
        if y > top0 + 27 and x > 32: cv.put(x, y, P["skin"][2])
    outline(cv, face, P["skinO"], only=lambda p: p[1] > top0 + 12)
    # front hair: frames the face, over the shoulders, soft ends; lighter strands on the left
    front = set()
    for y in range(top0 + 6, top0 + 58):
        for side in (-1, 1):
            w = 4 + (2 if y > top0 + 30 else 0)
            wob = 0.7 * math.sin(y / 5.5 + (0 if side < 0 else 1.5))
            edge_x = cx + side * (10.5 + 0.08 * (y - top0 - 6)) + wob
            for k in range(w):
                x = int(round(edge_x + side * k))
                front.add((x, y))
    front = {p for p in front if p[1] >= top0 + 6 and not (p in face and p[1] > top0 + 12 and abs(p[0] - cx) < 9)}
    for (x, y) in front:
        strand = (x + 1.0 * math.sin(y / 6.0)) % 5
        c = P["hair"][1]
        if x < cx and strand < 1.4: c = P["hair"][0]
        if x > cx and strand > 3.8: c = P["hair"][2]
        if y > top0 + 50: c = P["hair"][2]
        cv.put(x, y, c)
    for (x, y) in front:                                                     # fringe shadow on the forehead
        if (x, y + 1) in face and (x, y + 1) not in front: cv.put(x, y + 1, P["skin"][2])
    outline(cv, front, P["hairO"], only=lambda p: (p[0] - cx) * (1 if p[0] > cx else -1) > 9 or p[1] > top0 + 44)
    # brows: thin, arched
    stamp(cv, [".bbbb.", "b....b"], 18, top0 + 14, {"b": P["hair"][3]}); stamp(cv, [".bbbb.", "b....b"], 32, top0 + 14, {"b": P["hair"][3]})
    # eyes with lashes, a catchlight
    eye = ["LLLLLL", "wIiiwL", "wiPiwl", ".llll."]
    pal = {"L": P["lash"], "w": P["eyeW"], "I": P["irisD"], "i": P["iris"], "P": "#120a05", "l": P["lidL"]}
    stamp(cv, eye, 19, top0 + 17, pal); stamp(cv, eye, 31, top0 + 17, pal)
    cv.put(18, top0 + 17, P["lash"]); cv.put(17, top0 + 18, P["lash"]); cv.put(37, top0 + 17, P["lash"]); cv.put(38, top0 + 18, P["lash"])
    cv.put(21, top0 + 18, "#ffffff"); cv.put(33, top0 + 18, "#ffffff")
    # nose and cheeks
    cv.put(29, top0 + 22, P["skin"][2]); cv.put(29, top0 + 23, P["skin"][2]); cv.put(28, top0 + 24, P["skin"][0])
    cv.put(27, top0 + 25, P["skin"][3]); cv.put(29, top0 + 25, P["skin"][3]); cv.put(28, top0 + 25, P["skin"][2])
    for (x, y) in ((20, top0 + 24), (21, top0 + 24), (20, top0 + 25), (35, top0 + 24), (36, top0 + 24), (36, top0 + 25)): cv.put(x, y, P["blush"])
    # lips: soft smile
    for x in range(25, 32): cv.put(x, top0 + 28, P["lipD"])
    cv.put(24, top0 + 27, P["lipD"]); cv.put(32, top0 + 27, P["lipD"])
    for x in range(26, 31): cv.put(x, top0 + 29, P["lip"])
    cv.put(27, top0 + 29, P["lipL"]); cv.put(28, top0 + 29, P["lipL"])
    for x in range(26, 31): cv.put(x, top0 + 30, P["skin"][2])
    # earrings peeking through the hair
    cv.put(16, top0 + 29, P["gold"]); cv.put(16, top0 + 30, P["gold"]); cv.put(40, top0 + 29, P["gold"]); cv.put(40, top0 + 30, P["gold"])
    return cv

def sheet(cvs, scale, gap=24, bg=(236, 232, 224, 255)):
    h = max(c.h for c in cvs); w = sum(c.w for c in cvs) + gap * (len(cvs) + 1)
    im = Image.new("RGBA", (w, h + 8), bg); x = gap
    for c in cvs:
        im.alpha_composite(c.image(), (x, h - c.h + 4)); x += c.w + gap
    return im.resize((im.width * scale, im.height * scale), Image.NEAREST)

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "."
    cole, il = paint_cole(), paint_ilinca()
    cole.image().save(out + "/cole-1x.png"); il.image().save(out + "/ilinca-1x.png")
    sheet([cole, il], 5).save(out + "/portraits-5x.png")
    cole.image((236, 232, 224, 255)).resize((cole.w * 8, cole.h * 8), Image.NEAREST).save(out + "/cole-8x.png")
    il.image((236, 232, 224, 255)).resize((il.w * 8, il.h * 8), Image.NEAREST).save(out + "/ilinca-8x.png")
    print("ok")
