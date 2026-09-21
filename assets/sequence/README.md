# Frame sequence for the scroll story

The About page's scroll-driven section (the apple.com-style walkthrough) scrubs a numbered image
sequence with the scroll position. Until the frames exist it scrubs the animated SVG placeholder.

## Exporting frames

1. Render the machine animation as still frames: about **5–8 seconds at 24 fps = 120–192 frames**
   is plenty. Fewer frames = a choppier scrub, more frames = more to download.
2. JPEG, quality ~80, **1600×900** (16:9) or the aspect you want full-bleed. Keep each frame under ~120 KB.
3. Name them `frame-0001.jpg`, `frame-0002.jpg`, … (four-digit, starting at 1) and put them in this folder.
4. In `js/config.js` set `scrollSequence.count` to the number of frames. Done.

Storyboard the sequence to match the four captions in `how-it-works.html` (they fade at these scroll fractions):

| Scroll | Caption | What the frames should show |
| --- | --- | --- |
| 0.00–0.08 | Drop a bottle in the port. | Bottle placed at the port |
| 0.08–0.19 | A splash of water first. | Carriage to the mixer, mixer dips, priming water |
| 0.19–0.52 | Your blend, one cartridge at a time. | Carriage stops under three cartridges; each pours a different colour |
| 0.52–0.73 | Water and whisk, bottom to rim. | Back to the mixer, water while the whisk rises, layers blend |
| 0.73–0.82 | Yours, in about 45 seconds. | Carriage to the port, port lights |
| 0.82–1.00 | Then it cleans itself. | Mixer into the wash tank, rinse, drain, spin dry |

Change the caption text or the `data-start` / `data-end` fractions in `how-it-works.html` to match your edit.

Frames in this folder are served as-is, so don't commit anything you don't want public.
