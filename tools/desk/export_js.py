#!/usr/bin/env python3
"""
Nutrimatic desk scene - export_js.py
Version 1.1.0

Created: 2026-10-02 - Writes js/desk-sprites.js from the sprite sources (v1.0.0)
Modified: 2026-10-02 - Body poses (poses.py); layers run-length encoded, since there are now dozens of them (v1.1.0)

export_js.py - write js/desk-sprites.js for the site from the finished sprites.

The scene (js/desk-scene.js) draws everything on a small canvas, one sprite pixel at a time. This file holds the art as
plain data so the scene needs no image files and no loading step:

  window.NutrimaticDeskArt = { cole: {...}, ilinca: {...}, maker: {...} }

  figure: w, h          size of the full figure
          centre, desk  the column that sits on the character's x, the row that meets the desk top
          pal           colours; every number below is an index into it
          torso, head   layers: {x, y, w, h, d}; d has one character per pixel, row after row: 0-9a-z = palette index, "." = clear;
                        a run of the same character is written once followed by its length in capitals (base 26, A = 0)
          poses         {name: {b: body layer, f: front layer (optional), pts: {name: [x, y]} (optional)}}
          eyes, brows, mouth   frames as flat [x, y, colour, x, y, colour, ...] lists drawn over the head (-1 clears a pixel)
          joints, arm   where the arms attach and how they are drawn
"""
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from characters import CHARACTERS, layers, frames
from spritekit import Sprite, load

CH = '0123456789abcdefghijklmnopqrstuvwxyz'
SITE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')


def rle(s):
    """runs as the character followed by the run length in capital letters (base 26, A = 0); single pixels stay as they are"""
    out, i = [], 0
    while i < len(s):
        j = i
        while j < len(s) and s[j] == s[i]: j += 1
        n = j - i; out.append(s[i])
        if n > 1:
            digits = ''
            while n: digits = chr(65 + n % 26) + digits; n //= 26
            out.append(digits)
        i = j
    return ''.join(out)


def layer(spr, pal, ox=0, oy=0):
    """the sprite's pixels as a layer; (ox, oy) = where the sprite's own top-left sits in the figure's coordinates"""
    ys, xs = np.where(spr.idx >= 0); x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    rows = []
    for y in range(y0, y1 + 1):
        rows.append(''.join('.' if spr.idx[y, x] < 0 else CH[pal.index(spr.pal[spr.idx[y, x]])] for x in range(x0, x1 + 1)))
    return dict(x=int(x0 + ox), y=int(y0 + oy), w=int(x1 - x0 + 1), h=int(y1 - y0 + 1), d=rle(''.join(rows)))


def figure(c):
    torso, head, _ = layers(c); fr = frames(c)
    import poses as POSES
    built = POSES.build(c)
    pal = []
    def add(col):
        if col is not None and col not in pal: pal.append(col)
    for spr in (torso, head):
        for i in spr.used(): add(spr.pal[i])
    for q in built.values():
        for part in (q['body'], q['front']):
            if part is not None:
                for i in part[0].used(): add(part[0].pal[i])
    for group in fr.values():
        for lst in group.values():
            for _, _, col in lst: add(col)
    arm = dict(c.arm)
    for key in ('skin', 'cloth'):
        for col in arm[key]: add(col)
    add(arm['line'])
    if arm.get('cuff'): add(arm['cuff'])
    if len(pal) > len(CH): raise SystemExit('%s: %d colours is more than the format holds' % (c.name, len(pal)))
    ix = pal.index
    out = dict(w=torso.w, h=torso.h, centre=c.centre, desk=c.desk, pal=pal, torso=layer(torso, pal), head=layer(head, pal))
    for g in ('eyes', 'brows', 'mouth'):
        out[g] = {k: [v for x, y, col in lst for v in (x, y, -1 if col is None else ix(col))] for k, lst in fr[g].items()}
    out['poses'] = {}
    for name, q in built.items():
        b, bx, by = q['body']; entry = dict(b=layer(b, pal, bx, by))
        if q['front'] is not None: f, fx, fy = q['front']; entry['f'] = layer(f, pal, fx, fy)
        if q['pts']: entry['pts'] = {k: list(v) for k, v in q['pts'].items()}
        out['poses'][name] = entry
    out['joints'] = {k: list(v) for k, v in c.joints.items()}
    out['points'] = {k: list(v) for k, v in c.points.items()}
    out['arm'] = dict(upper=arm['upper'], fore=arm['fore'], rL=arm['rL'], rR=arm['rR'], sleeve=arm['sleeve'], skin=[ix(x) for x in arm['skin']], cloth=[ix(x) for x in arm['cloth']],
                      cuff=(ix(arm['cuff']) if arm.get('cuff') else -1), line=ix(arm['line']))
    return out


def sheet(path_or_sprites):
    """a set of plain sprites sharing one palette: {name: Sprite} -> {pal, name: layer}"""
    pal = []
    for spr in path_or_sprites.values():
        for i in spr.used():
            if spr.pal[i] not in pal: pal.append(spr.pal[i])
    out = dict(pal=pal)
    for name, spr in path_or_sprites.items():
        L = layer(spr, pal); L['x'] = 0; L['y'] = 0; out[name] = L
    return out


def js(obj, indent=2):
    """JSON, but one line per leaf container so the file stays readable and diffs stay small"""
    return json.dumps(obj, separators=(', ', ': '))


def main():
    art = {name: figure(c) for name, c in CHARACTERS.items()}
    extra = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'extra_sprites.py')
    if os.path.exists(extra):
        import importlib.util
        spec = importlib.util.spec_from_file_location('extra_sprites', extra); mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
        ground = mod.GROUND() if hasattr(mod, 'GROUND') else {}
        for name, sprites in mod.SHEETS().items():
            art[name] = sheet(sprites)
            for k, rows in ground.get(name, {}).items(): art[name][k]['g'] = rows
    lines = ['/*', ' * Nutrimatic Website - desk-sprites.js', ' * Version 1.0.0', ' *',
             ' * Created: 2026-10-02 - The art for the desk scene as data: Cole, Ilinca and Maker the cat (v1.0.0)',
             ' *',
             ' * GENERATED by tools/desk/export_js.py from the sprites in tools/desk/. Do not edit by hand: change the sprite',
             ' * sources and run the exporter again. Format: see the header of that script.',
             ' */', '', 'window.NutrimaticDeskArt = {']
    names = list(art)
    for n in names:
        a = art[n]; lines.append('  %s: {' % n)
        keys = list(a)
        for k in keys:
            v = a[k]
            if isinstance(v, dict) and k in ('eyes', 'brows', 'mouth', 'poses'):
                lines.append('    %s: {' % k)
                sub = list(v)
                for sk in sub: lines.append('      %s: %s%s' % (json.dumps(sk), js(v[sk]), ',' if sk != sub[-1] else ''))
                lines.append('    }%s' % (',' if k != keys[-1] else ''))
            else:
                lines.append('    %s: %s%s' % (k, js(v), ',' if k != keys[-1] else ''))
        lines.append('  }%s' % (',' if n != names[-1] else ''))
    lines.append('};'); lines.append('')
    out = os.path.join(SITE, 'js', 'desk-sprites.js')
    open(out, 'w').write('\n'.join(lines)); print('wrote', os.path.normpath(out), os.path.getsize(out) // 1024, 'KB', {n: len(art[n]['pal']) for n in art})


if __name__ == '__main__': main()
