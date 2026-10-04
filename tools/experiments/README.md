# Experiments (pinned, not in use)

Version 1.1.0 · Created 2026-10-02 · Modified 2026-10-04 (the portrait results taken out of the repo)

Things tried for the co-founders' figures and set aside. Kept so nobody repeats them; see the handover for the verdicts.

- `style-frames/`: a standalone room renderer (ceiling, pendant light, warm walls, day / dusk / night lighting, New York
  skyline) with four candidate stills. **The room direction was liked; the figures in it were not.** Run with a local
  server: `node shoot.mjs` after `npm install playwright` in `tools/test`.
- `portraits/`: two attempts at navel-up portraits painted procedurally in Python (PIL). v1 shaded realistic forms
  ("I look like an ape, she looks like a fish"); v2 followed the GBA mug method with lock-built hair and cel shading,
  closer but still rejected. Their renders are no longer in the repo (Cole, 2026-10-04: no portraits in the repo).
- `photo2px/`: the headshots cut out and reduced to a 16-colour sprite automatically. Keeps the likeness, loses the
  art: it reads as a smeared photo. Useful only as a likeness check. Its result is no longer in the repo either.

The live plan replaces all of this: portraits generated on a GPU machine from the photos with `tools/portraits/`, then
cut into animatable layers.
