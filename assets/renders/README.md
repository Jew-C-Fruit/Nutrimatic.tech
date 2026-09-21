# Renders

Drop the machine renderings here. The site picks them up automatically; nothing else needs editing.

| File | Used where | Notes |
| --- | --- | --- |
| `machine-front.jpg` | Splash page hero (static fallback / video poster) | The "kiosk against the brick wall" render. 1920×1080 or larger, JPEG, under ~400 KB. |
| `machine.mp4` / `machine.webm` | Splash page hero animation | Optional. Set the path in `js/config.js` (`heroVideo`). Muted, looping, no audio track needed. Keep it under ~5 MB. |
| `cartridge-bay.jpg` | About page, "The machine" section | The "door open, four cartridges" render. |

Until `machine-front.jpg` exists, the hero shows the animated SVG placeholder in `../machine.svg`
(with `../machine-static.png` for visitors who prefer reduced motion).
