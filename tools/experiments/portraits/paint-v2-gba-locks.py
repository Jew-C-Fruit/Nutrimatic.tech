"""GBA Fire Emblem style portraits: three-quarter faces turned toward each other, hair built from locks,
flat cel shading in two tones plus a highlight, darkest colour as the outline, light from the window side."""
import math, sys
from PIL import Image

def hexrgb(h): return (int(h[1:3], 16), int(h[3:5], 16), int(h[5:7], 16), 255)

class Canvas:
    def __init__(self, w, h): self.w, self.h, self.px = w, h, {}
    def put(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h and c: self.px[(int(x), int(y))] = c
    def get(self, x, y): return self.px.get((x, y))
    def image(self, bg=None):
        im = Image.new("RGBA", (self.w, self.h), (0, 0, 0, 0) if bg is None else bg)
        for (x, y), c in self.px.items(): im.putpixel((x, y), hexrgb(c))
        return im

# ---------- geometry ----------
def poly(points):
    m = set(); ys = [p[1] for p in points]
    for y in range(int(math.floor(min(ys))), int(math.ceil(max(ys))) + 1):
        yc = y + 0.5; xs = []
        for i in range(len(points)):
            (x1, y1), (x2, y2) = points[i], points[(i + 1) % len(points)]
            if (y1 <= yc < y2) or (y2 <= yc < y1): xs.append(x1 + (yc - y1) * (x2 - x1) / (y2 - y1))
        xs.sort()
        for i in range(0, len(xs) - 1, 2):
            for x in range(int(math.floor(xs[i] + 0.5)), int(math.floor(xs[i + 1] + 0.5))): m.add((x, y))
    return m
def ellipse(cx, cy, rx, ry):
    m = set()
    for y in range(int(cy - ry) - 1, int(cy + ry) + 2):
        for x in range(int(cx - rx) - 1, int(cx + rx) + 2):
            if ((x + 0.5 - cx) / rx) ** 2 + ((y + 0.5 - cy) / ry) ** 2 <= 1: m.add((x, y))
    return m
def curve(pts, n=40):
    """Catmull-Rom through pts -> list of float points (for smooth lock outlines)"""
    out = []
    P = [pts[0]] + list(pts) + [pts[-1]]
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        for k in range(n):
            t = k / n; t2, t3 = t * t, t * t * t
            x = 0.5 * ((2 * p1[0]) + (-p0[0] + p2[0]) * t + (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t2 + (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t3)
            y = 0.5 * ((2 * p1[1]) + (-p0[1] + p2[1]) * t + (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t2 + (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t3)
            out.append((x, y))
    out.append(pts[-1]); return out
def blob(pts): return poly(curve(pts))
def edge(mask): return {(x, y) for (x, y) in mask if any((x + dx, y + dy) not in mask for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))}
def inner(mask, n=1):
    m = set(mask)
    for _ in range(n): m -= edge(m)
    return m
def shift(mask, dx, dy): return {(x + dx, y + dy) for (x, y) in mask}
def stamp(cv, rows, x0, y0, pal):
    for r, row in enumerate(rows):
        for i, k in enumerate(row):
            if k != "." and k in pal: cv.put(x0 + i, y0 + r, pal[k])
def fill(cv, mask, c):
    for (x, y) in mask: cv.put(x, y, c)
def line(cv, x0, y0, x1, y1, c):
    n = max(abs(x1 - x0), abs(y1 - y0), 1)
    for i in range(n + 1): cv.put(round(x0 + (x1 - x0) * i / n), round(y0 + (y1 - y0) * i / n), c)

# ---------- cel shading helpers ----------
def cel(cv, mask, lit, shade, split, dark=None, dark_split=None):
    """split(x,y) -> True where the light reaches"""
    for (x, y) in mask:
        c = lit if split(x, y) else shade
        if dark is not None and dark_split and dark_split(x, y): c = dark
        cv.put(x, y, c)
def lock(cv, pts, pal, light_dir=(1, -1), tip_dark=True):
    """A lock of hair: smooth blob, base fill, highlight band on the lit edge, dark on the shade edge, outlined."""
    m = blob(pts)
    fill(cv, m, pal["h"])
    e = edge(m); e2 = edge(inner(m, 1))
    for (x, y) in e2 | e:
        # which way does this edge pixel face?  compare with the blob interior
        nx = sum(1 for dx in (-1, 1) if (x + dx, y) not in m) * (1 if (x + 1, y) not in m else -1)
        ny = (1 if (x, y + 1) not in m else -1) if ((x, y + 1) not in m or (x, y - 1) not in m) else 0
        d = nx * light_dir[0] + ny * light_dir[1]
        if d > 0.5 and (x, y) in e2: cv.put(x, y, pal["H"])
        elif d < -0.5: cv.put(x, y, pal["d"])
    for (x, y) in e: cv.put(x, y, pal["O"])
    return m

# ---------- palettes (15 colours each, outline darkest) ----------
COLE = dict(O="#0b0806", d="#1a110a", h="#2e1e14", H="#5c4330", H2="#7a5c45",
            K="#6a4230", k="#b87a57", m="#dca07b", s="#f0c7a3", L="#fae3cb",
            tO="#0b0b0d", t="#17171a", tL="#282830", tH="#3a3a42",
            frame="#141414", rim="#5a5a5a", lens="#d6e4f2", iris="#8a5a3a", irisD="#4a2c18", pupil="#1a0e06", lid="#2a1a12", lip="#8a4a40", lipL="#e3a08c")
ILINCA = dict(O="#3a2614", d="#6a4a2c", h="#96703f", H="#c49a62", H2="#e2bd86",
              K="#7a4a36", k="#c4866a", m="#e2ad8f", s="#f5d2b8", L="#fdeadb",
              tO="#0b0b0e", t="#1b1b20", tL="#2c2c33", tH="#3d3d46", top="#f8f7f3", topS="#dedcd6",
              iris="#7a5236", irisD="#3f2715", pupil="#160c05", lid="#2a1a12", lip="#d4707f", lipL="#f2a7b0", blush="#f0b4a6", gold="#e4bb64")

# ================= COLE: three-quarter, turned to the right; big through the shoulders =================
def paint_cole():
    cv = Canvas(72, 100); P = COLE
    # --- body: black tee, near shoulder (left) larger, shade on the left, light from the right
    body = blob([(10, 54), (6, 66), (5, 100), (69, 100), (68, 64), (62, 53), (52, 48), (40, 46), (24, 47)])
    cel(cv, body, P["tL"], P["t"], lambda x, y: x > 30 + (y - 60) * 0.15)
    for (x, y) in body:
        if x > 56 and y < 64: cv.put(x, y, P["tH"])                        # light on the far shoulder
        if x < 14 and y > 60: cv.put(x, y, P["tO"])                        # near arm falls into shadow
    for (x, y) in edge(body): cv.put(x, y, P["tO"])
    for (x, y) in edge(inner(body, 1)):
        if y < 56: cv.put(x, y, P["tH"] if x > 34 else P["t"])
    line(cv, 15, 66, 24, 80, P["tO"]); line(cv, 16, 74, 22, 86, P["tO"]); line(cv, 60, 70, 52, 84, P["t"])   # armpit folds
    # crew neck ribbing
    collar = blob([(26, 48), (33, 45), (44, 44), (52, 47), (47, 52), (36, 54), (27, 52)])
    cel(cv, collar, P["tH"], P["tL"], lambda x, y: x > 36)
    for (x, y) in edge(collar): cv.put(x, y, P["tO"])
    # --- neck
    neck = poly([(28, 38), (46, 38), (46, 51), (28, 51)])
    cel(cv, neck, P["s"], P["m"], lambda x, y: x > 38)
    for (x, y) in neck:
        if y < 46: cv.put(x, y, P["k"] if x < 40 else P["m"])              # under the jaw
    for (x, y) in edge(neck):
        if x <= 28 or x >= 45: cv.put(x, y, P["K"])
    # --- face: egg turned to the right; near cheek fuller, far side tighter, pointed chin
    face = blob([(16, 14), (12, 24), (13, 34), (19, 43), (27, 48), (34, 47), (41, 42), (46, 33), (47, 22), (43, 13), (30, 9)])
    cel(cv, face, P["s"], P["m"], lambda x, y: x > 22 + (y - 20) * 0.25)
    for (x, y) in face:
        if y > 40 and x < 30: cv.put(x, y, P["k"])                         # jaw underside
        if x > 36 and 20 < y < 32: cv.put(x, y, P["L"])                   # light on the far cheekbone
    for (x, y) in edge(face): cv.put(x, y, P["K"])
    # ear on the near side
    ear = blob([(12, 24), (10, 28), (11, 33), (14, 34), (16, 30), (15, 25)])
    cel(cv, ear, P["s"], P["m"], lambda x, y: x > 13); fill(cv, {(12, 29), (12, 30), (13, 31)}, P["k"])
    for (x, y) in edge(ear): cv.put(x, y, P["K"])
    # --- hair: swept locks, brown-black. Back locks first, then the crown, then the bangs.
    H = P
    lock(cv, [(46, 8), (54, 9), (58, 14), (55, 19), (49, 18), (45, 14)], H)                                   # back lock, far side
    lock(cv, [(14, 12), (10, 20), (10, 30), (12, 36), (15, 35), (16, 26), (17, 16)], H)                         # near side down to the sideburn
    lock(cv, [(16, 10), (22, 3), (34, 0), (46, 1), (55, 6), (57, 12), (48, 10), (36, 9), (24, 11), (18, 15)], H)   # crown mass
    lock(cv, [(24, 4), (31, 0), (40, 1), (36, 6), (28, 8)], H)                                                  # tuft on top for volume
    lock(cv, [(40, 2), (49, 3), (55, 8), (52, 11), (46, 9)], H)                                                 # tuft sweeping back
    lock(cv, [(17, 9), (25, 6), (31, 8), (26, 12), (20, 17), (15, 21), (15, 14)], H)                            # bang 1: down-left over the near temple
    lock(cv, [(26, 7), (34, 6), (39, 9), (35, 13), (31, 17), (30, 12)], H)                                      # bang 2: a point at the middle of the forehead
    lock(cv, [(36, 6), (45, 6), (52, 10), (48, 15), (44, 13), (41, 10)], H)                                     # bang 3: sweeps right
    lock(cv, [(46, 7), (54, 8), (58, 12), (55, 15), (50, 13)], H)                                               # bang 4: trails behind the far temple
    lock(cv, [(31, 10), (35, 10), (36, 16), (34, 21), (32, 16)], H)                                             # one strand dips toward the glasses
    for (x0, y0, x1, y1) in ((20, 4, 28, 2), (34, 2, 44, 2), (48, 4, 55, 7), (19, 9, 24, 7), (28, 8, 34, 7), (38, 7, 46, 8)): line(cv, x0, y0, x1, y1, P["H2"])   # sheen along the locks
    # shadow of the bangs on the forehead
    for (x, y) in face:
        if cv.get(x, y) in (P["s"], P["L"]) and (cv.get(x, y - 1) in (P["O"], P["d"], P["h"], P["H"]) or cv.get(x, y - 2) in (P["O"],)): cv.put(x, y, P["m"])
    # --- brows: thick, a little arched, the near one longer
    stamp(cv, ["..bbbbbbb.", "bbbbbbbbb."], 16, 19, {"b": P["d"]}); stamp(cv, [".bbbbbb", "bbbbbb."], 32, 18, {"b": P["d"]})
    # --- eyes: near eye wide, far eye narrower (three-quarter)
    E = {"l": P["lid"], "w": "#faf7f1", "I": P["irisD"], "i": P["iris"], "p": P["pupil"], "c": "#ffffff", "k": P["k"], "m": P["m"]}
    near = [".llllllll..", "lwwIIIIIwl.", "lwIIiiIIwl.", "lwIIipIIwl.", ".lwIIIIwl..", "..kwwwwk...", "...mmmm...."]
    far = [".llllll.", "lwIIIIwl", "lwIiiIIl", "lwIipIIl", ".wIIIIl.", ".kwwwwk.", "..mmmm.."]
    stamp(cv, near, 17, 23, E); stamp(cv, far, 36, 23, E)
    cv.put(21, 24, "#ffffff"); cv.put(22, 24, "#ffffff"); cv.put(22, 25, "#ffffff"); cv.put(39, 24, "#ffffff"); cv.put(40, 24, "#ffffff")
    cv.put(24, 27, P["iris"]); cv.put(41, 27, P["iris"])
    # --- browline glasses: one heavy bar along the brows, thin lower rims, a bridge, the near temple
    for x in range(14, 46): cv.put(x, 22, P["frame"])
    for y in range(23, 30): cv.put(14, y, P["frame"]); cv.put(28, y, P["frame"]); cv.put(33, y, P["frame"]); cv.put(45, y, P["frame"])
    for x in range(15, 28): cv.put(x, 30, P["rim"])
    for x in range(34, 45): cv.put(x, 30, P["rim"])
    for x in range(29, 33): cv.put(x, 24, P["frame"])
    line(cv, 13, 23, 10, 25, P["frame"]); cv.put(46, 24, P["frame"])
    cv.put(16, 23, P["lens"]); cv.put(35, 23, P["lens"])
    # --- nose: bridge shadow toward the far side, tip, one nostril
    line(cv, 33, 26, 36, 33, P["m"]); line(cv, 34, 27, 37, 33, P["k"])
    cv.put(38, 34, P["K"]); cv.put(37, 35, P["k"]); cv.put(36, 35, P["k"]); cv.put(35, 35, P["m"]); cv.put(39, 33, P["L"]); cv.put(39, 32, P["L"])
    cv.put(33, 35, P["m"]); cv.put(32, 34, P["m"])
    # --- mouth: small, easy smile; lower lip catches light
    cv.put(27, 39, P["lip"]); line(cv, 28, 40, 36, 40, P["lip"]); cv.put(37, 39, P["lip"]); cv.put(28, 40, P["K"]); cv.put(36, 40, P["K"])
    for x in range(29, 36): cv.put(x, 41, P["lipL"])
    for x in range(29, 36): cv.put(x, 42, P["m"])
    cv.put(32, 43, P["k"]); cv.put(33, 43, P["k"])                                    # chin shadow
    return cv

# ================= ILINCA: three-quarter, turned to the left; petite =================
def paint_ilinca():
    cv = Canvas(64, 100); P = ILINCA
    X = 64
    # --- hair behind: a long mass with soft movement, over the shoulders, lighter on the window side (right)
    back = blob([(20, 10), (12, 20), (9, 36), (8, 56), (12, 76), (18, 86), (26, 84), (32, 70), (40, 84), (50, 86), (56, 74), (56, 50), (52, 30), (46, 14), (34, 6)])
    cel(cv, back, P["h"], P["d"], lambda x, y: x > 30 + (y - 40) * 0.1)
    for (x, y) in back:
        if x > 44 and y < 60 and (x + y) % 7 < 2: cv.put(x, y, P["H"])
        if y > 72 and x < 20: cv.put(x, y, P["O"] if (x, y) in edge(back) else P["d"])
    for (x, y) in edge(back): cv.put(x, y, P["O"])
    # --- body: narrow sloping shoulders, waist taper; blazer open over a white top
    body = blob([(16, 62), (12, 72), (12, 100), (54, 100), (54, 72), (49, 62), (42, 57), (32, 55), (22, 57)])
    cel(cv, body, P["tL"], P["t"], lambda x, y: x > 36)
    for (x, y) in body:
        if x > 48 and y < 72: cv.put(x, y, P["tH"])
    for (x, y) in edge(body): cv.put(x, y, P["tO"])
    for y in range(57, 100):                                                       # white top in the V, lapels lit on the right
        t = (y - 57) / 30.0; hw = max(0, int(round(7 - 8 * t)))
        if hw > 0:
            for x in range(33 - hw, 33 + hw + 1): cv.put(x, y, P["top"] if x > 31 else P["topS"])
            for x in range(33 - hw - 3, 33 - hw): cv.put(x, y, P["tL"])
            for x in range(33 + hw + 1, 33 + hw + 4): cv.put(x, y, P["tH"])
            cv.put(33 - hw - 4, y, P["tO"]); cv.put(33 + hw + 4, y, P["tO"])
    cv.put(33, 86, "#8a8a92"); cv.put(33, 87, "#5a5a62")
    for i in range(0, 7): cv.put(29 + i // 2, 58 + i, P["gold"]); cv.put(37 - i // 2, 58 + i, P["gold"])
    cv.put(33, 65, P["gold"]); cv.put(33, 66, "#f6d98a")
    # --- neck: slim
    neck = poly([(27, 44), (39, 44), (40, 58), (26, 58)])
    cel(cv, neck, P["s"], P["m"], lambda x, y: x > 33)
    for (x, y) in neck:
        if y < 50: cv.put(x, y, P["k"] if x < 35 else P["m"])
    for (x, y) in edge(neck):
        if x <= 27 or x >= 39: cv.put(x, y, P["K"])
    # --- face: soft egg turned to the left; narrow jaw, small chin; light from the right
    face = blob([(18, 16), (14, 26), (15, 36), (20, 45), (28, 50), (35, 49), (41, 43), (45, 34), (46, 24), (42, 14), (30, 10)])
    cel(cv, face, P["s"], P["m"], lambda x, y: x > 21 + (y - 24) * 0.1)
    for (x, y) in face:
        if x > 38 and 22 < y < 34: cv.put(x, y, P["L"])
        if y > 44 and x < 30: cv.put(x, y, P["k"])
    for (x, y) in edge(face): cv.put(x, y, P["K"])
    # --- front hair: a parting on the right, long locks framing both sides of the face, soft bangs
    lock(cv, [(44, 12), (52, 20), (54, 36), (52, 54), (46, 60), (42, 46), (42, 28)], P)            # right side lock, over the far cheek
    lock(cv, [(18, 14), (10, 24), (8, 40), (10, 58), (16, 66), (20, 52), (20, 34), (22, 22)], P)   # left side lock, in front of the near cheek
    lock(cv, [(20, 8), (30, 4), (44, 6), (52, 12), (46, 18), (34, 14), (24, 18)], P)                 # crown
    lock(cv, [(22, 12), (30, 8), (40, 10), (36, 20), (28, 24), (22, 22)], P)                          # bangs, sweeping left
    lock(cv, [(38, 8), (46, 9), (50, 18), (44, 22), (40, 16)], P)                                     # bangs, right of the parting
    for (x, y) in face:
        if cv.get(x, y) in (P["s"], P["L"]) and cv.get(x, y - 1) in (P["O"], P["d"], P["h"], P["H"]): cv.put(x, y, P["m"])
    for (x, y) in ((28, 6), (30, 5), (31, 5), (32, 6)): cv.put(x, y, P["H2"])                        # sheen on the crown
    line(cv, 13, 30, 12, 50, P["H"]); line(cv, 15, 26, 14, 40, P["H2"]); line(cv, 49, 24, 50, 44, P["H"]); line(cv, 47, 30, 48, 50, P["H2"])   # strands catching light
    lock(cv, [(10, 70), (16, 66), (18, 80), (14, 92), (9, 84)], P); lock(cv, [(48, 70), (54, 66), (56, 80), (52, 92), (47, 84)], P)         # ends falling to points
    # --- brows: thin, arched
    stamp(cv, [".bbbbbb.", "bb....bb"], 17, 23, {"b": P["O"]}); stamp(cv, [".bbbbb", "b....b"], 36, 22, {"b": P["O"]})
    # --- eyes: large, lashes at the outer corners, warm brown iris, two catchlights
    E = {"l": P["lid"], "w": "#faf7f1", "I": P["irisD"], "i": P["iris"], "p": P["pupil"], "k": P["k"], "m": P["m"]}
    near = ["..lllllll..", ".lwIIIIIwl.", "lwIIiiIIIwl", "lwIIipIIIwl", ".lwIIIIIwl.", "..kwwwwwk..", "...mmmmm..."]
    far = [".llllll.", "lwIIIIwl", "lwIiiIIl", "lwIipIIl", ".wIIIIl.", ".kwwwwk.", "..mmmm.."]
    stamp(cv, near, 17, 26, E); stamp(cv, far, 36, 26, E)
    cv.put(21, 27, "#ffffff"); cv.put(22, 27, "#ffffff"); cv.put(22, 28, "#ffffff"); cv.put(40, 27, "#ffffff"); cv.put(41, 27, "#ffffff")
    cv.put(16, 26, P["lid"]); cv.put(15, 27, P["lid"]); cv.put(44, 26, P["lid"]); cv.put(45, 27, P["lid"])
    cv.put(24, 30, P["iris"]); cv.put(42, 30, P["iris"])
    # --- nose: small, turned left
    line(cv, 30, 30, 28, 36, P["m"]); cv.put(26, 37, P["K"]); cv.put(27, 38, P["k"]); cv.put(28, 38, P["m"]); cv.put(25, 36, P["L"]); cv.put(25, 35, P["L"])
    # --- cheeks and lips
    for (x, y) in ((19, 35), (20, 35), (20, 36), (41, 35), (42, 35), (42, 36)): cv.put(x, y, P["blush"])
    cv.put(24, 41, P["lip"]); line(cv, 25, 42, 32, 42, P["lip"]); cv.put(33, 41, P["lip"]); cv.put(25, 42, P["K"]); cv.put(32, 42, P["K"])
    for x in range(26, 32): cv.put(x, 43, P["lipL"])
    cv.put(28, 43, "#fbd0d6"); cv.put(29, 43, "#fbd0d6")
    for x in range(26, 32): cv.put(x, 44, P["m"])
    # --- earring on the near side
    cv.put(47, 40, P["gold"]); cv.put(47, 41, P["gold"]); cv.put(46, 42, P["gold"])
    return cv

def sheet(cvs, scale, gap=20, bg=(236, 232, 224, 255)):
    h = max(c.h for c in cvs); w = sum(c.w for c in cvs) + gap * (len(cvs) + 1)
    im = Image.new("RGBA", (w, h + 8), bg); x = gap
    for c in cvs: im.alpha_composite(c.image(), (x, h - c.h + 4)); x += c.w + gap
    return im.resize((im.width * scale, im.height * scale), Image.NEAREST)

if __name__ == "__main__":
    out = sys.argv[1]
    cole, il = paint_cole(), paint_ilinca()
    cole.image().save(out + "/cole2-1x.png"); il.image().save(out + "/ilinca2-1x.png")
    sheet([cole, il], 4).save(out + "/portraits2-4x.png")
    cole.image((236, 232, 224, 255)).resize((cole.w * 7, cole.h * 7), Image.NEAREST).save(out + "/cole2-7x.png")
    il.image((236, 232, 224, 255)).resize((il.w * 7, il.h * 7), Image.NEAREST).save(out + "/ilinca2-7x.png")
    print("ok")
