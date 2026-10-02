"""Photo -> pixel portrait: cut out the person, downscale to sprite size, boost contrast, quantise to a small palette,
clean stray pixels, add an outline. A test of likeness, not of style."""
import sys
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
from rembg import remove, new_session

def pixelate(src, out, head_px=40, colors=14):
    im = Image.open(src).convert("RGBA")
    cut = remove(im, session=SESSION)                                    # alpha matte
    bbox = cut.getbbox(); cut = cut.crop(bbox)
    # scale so the figure width maps to roughly head_px * 1.7 (bust)
    target_w = int(head_px * 1.75); scale = target_w / cut.width
    small = cut.resize((target_w, max(1, int(cut.height * scale))), Image.LANCZOS)
    alpha = small.getchannel("A").point(lambda a: 255 if a > 120 else 0)
    rgb = small.convert("RGB")
    rgb = ImageEnhance.Contrast(rgb).enhance(1.25); rgb = ImageEnhance.Color(rgb).enhance(1.15)
    q = rgb.quantize(colors=colors, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    q = q.filter(ImageFilter.ModeFilter(3))                              # knock out lone pixels
    rgbq = q.convert("RGB")
    # outline: darkest palette colour around the matte
    pal = q.getpalette()[:colors * 3]; darkest = min(range(colors), key=lambda i: sum(pal[i * 3:i * 3 + 3]))
    dark = tuple(pal[darkest * 3:darkest * 3 + 3])
    outl = Image.new("RGBA", small.size, (0, 0, 0, 0)); px = outl.load(); a = alpha.load(); w, h = small.size
    for y in range(h):
        for x in range(w):
            if a[x, y] and any(0 <= x + dx < w and 0 <= y + dy < h and not a[x + dx, y + dy] for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))): px[x, y] = dark + (255,)
    res = Image.new("RGBA", small.size, (0, 0, 0, 0)); res.paste(rgbq, (0, 0), alpha); res.alpha_composite(outl)
    res.save(out + "-1x.png")
    bg = Image.new("RGBA", res.size, (236, 232, 224, 255)); bg.alpha_composite(res)
    bg.resize((res.width * 6, res.height * 6), Image.NEAREST).save(out + "-6x.png")
    return res

SESSION = new_session("u2net_human_seg")
for name in ("cole-maisonpierre", "ilinca-iorga"):
    r = pixelate("/home/user/nutrimatic.tech/assets/team/%s.jpg" % name, "/tmp/claude-0/-home-user-Nutrimatic/3b0d6bb5-0976-50b9-895d-87e17656c294/scratchpad/photo2px/" + name.split("-")[0])
    print(name, r.size)
