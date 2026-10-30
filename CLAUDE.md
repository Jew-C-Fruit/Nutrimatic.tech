# nutrimatic.tech — notes for Claude Code sessions

Version 1.4.0 · Created 2026-10-02 · Modified 2026-10-30 (the desk scene goes live on the new About us page; https redirect)

This repo **is** the public website. Every push to `main` deploys to https://nutrimatic.tech within a minute via
`.github/workflows/deploy-website.yml` (GitHub Pages). `README.md`, `GO-LIVE.md`, `CLAUDE.md`, `squarespace/` and
`tools/` are left out of the deploy; everything else is served as-is. There is no build step.

The full project handover (history, decisions, feedback, open items) lives in the **private** Nutrimatic repo at
`website-handover/HANDOVER.md`. Read it first when picking this work up.

## Branches

- `main`: live. Only push what's ready to be seen.
- `desk-scene` and the `r3x-*` round branches: work on the co-founders' pixel-art desk scene and the portrait toolkit.
  The scene went live on 2026-10-30 on the About us page (`about.html`) with only the finished scenes switched on
  (`SCENE_ON` in `js/desk-scene.js`); the rest stay off until Cole OKs them.

## The desk scene (About us page)

- `js/desk-scene.js` is the scene: light, behaviour, scenarios. `js/desk-sprites.js` is the figures' and Maker's art
  and `assets/desk/*.png` the room's (wall, desk, skyline, lamps, props); both are **generated**: edit the sources in
  `tools/desk/` and run `python3 tools/desk/export_js.py` / `python3 tools/desk/env_build.py`. Never edit them by hand.
  If the room pictures do not load, the scene falls back to the room drawn in code.
- The figures come from portraits generated on the GPU machine and reduced to sprites (`tools/portraits/`), then finished
  by hand in the face only (`tools/desk/characters.py`). Every activity's arms and hands are generated poses as well
  (`tools/desk/poses.py`). Drawing figures or arms in code was tried and rejected each time; don't go back to it.
- **Model licences**: only models whose licence allows commercial use may make art for the site. FLUX.2 klein 4B and
  Qwen-Image-Edit 2511 are Apache 2.0. Qwen-Image 2.1 is research-only: not for site art.
- Reference photos of the founders and the cat are private. They are not in this repo and must not be added.
- The skyline follows two CC BY photographs and the Mondrian a CC BY photograph (`tools/desk/sources/PROVENANCE.md`);
  the credits at the bottom of `about.html` (footer) carry them. Keep them whenever the scene is shown.
- Look before you ship: `npm run shots:desk` in `tools/test` writes screenshots of every activity and scenario.

## Conventions (keep these)

- **Headers**: every edited file carries a `Version X.Y.Z` and a `Modified: YYYY-MM-DD - what changed (vX.Y.Z)` line in its
  header comment; bump PATCH for fixes, MINOR for features. Same rule as the private repo's protocol.
- **No email address anywhere in the tree**, including config and history. Public contact is the LinkedIn URL,
  written out. `contactEmail` in `js/config.js` stays blank.
- **Language**: never "fresh" (it's protein powder); brands "advertise with us", never "sponsor a slot"; the page is
  "How it works" (the product); the co-founders have their own "About us" page (Cole, 2026-10-30); headline is "Custom nutrition in 45 seconds." The site speaks plainly and short.
- **Design**: hard edges everywhere (`--radius: 0`, no rounded corners in CSS or in the SVG animations; the bottle
  may stay curvy); black / white / red `#e4002b`; Archivo, self-hosted. Image- and animation-forward pages, Apple-style.
- **Commits**: descriptive subject, body says why; author is `Cole Maisonpierre <67285155+Jew-C-Fruit@users.noreply.github.com>`
  (no real email in public history); end with the Claude attribution footer the private repo's protocol uses.

## HTTPS

Every page's head redirects plain http to https before anything loads (an inline script that leaves localhost alone).
The proper server-side redirect is GitHub's Settings -> Pages -> "Enforce HTTPS"; keep it ticked.

## Checks before pushing to main

```bash
cd tools/test && npm install && npx playwright install chromium --with-deps   # once
npm run serve &  &&  npm test
```

Also re-run `node tools/render-static-assets.mjs` if `assets/machine.svg`, the wordmark or the tagline changed.

## Forms (live)

Submissions go to Web3Forms (key in `js/config.js`, public by design) and to the Google Apps Script in
`tools/apps-script/` (URL in `js/config.js`), which fills the Google Sheet and sends a short email. Both are on.
Test from the live site shows up as rows in the sheet: delete them afterwards.
