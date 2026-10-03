#!/usr/bin/env python3
"""
Nutrimatic desk scene - extra_sprites.py
Version 1.2.0

Created: 2026-10-02 - Sprite sheets besides the two figures (Maker) for the exporter (v1.0.0)
Modified: 2026-10-03 - makerB: Maker with big stylized eyes, a second look to compare (v1.1.0)
Modified: 2026-10-03 - The big eyes won: they are Maker now; the comparison sheet is gone (v1.2.0)

extra_sprites.py - sprite sheets other than the two figures, for export_js.py: SHEETS() -> {name: {sprite name: Sprite}}"""
import maker_build

def SHEETS(): return {'maker': maker_build.sheet(big=True)}       # the big-eyed look, the user's pick
def GROUND(): return {'maker': maker_build.GROUND}
