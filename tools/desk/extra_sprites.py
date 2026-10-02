#!/usr/bin/env python3
"""
Nutrimatic desk scene - extra_sprites.py
Version 1.0.0

Created: 2026-10-02 - Sprite sheets besides the two figures (Maker) for the exporter (v1.0.0)

extra_sprites.py - sprite sheets other than the two figures, for export_js.py: SHEETS() -> {name: {sprite name: Sprite}}"""
import maker_build

def SHEETS(): return {'maker': maker_build.sprites()}
def GROUND(): return {'maker': maker_build.GROUND}
