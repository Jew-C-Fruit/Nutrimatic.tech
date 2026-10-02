# nutrimatic.tech — notes for Claude Code sessions

Version 1.0.0 · Created 2026-10-02

This repo **is** the public website. Every push to `main` deploys to https://nutrimatic.tech within a minute via
`.github/workflows/deploy-website.yml` (GitHub Pages). `README.md`, `GO-LIVE.md`, `CLAUDE.md`, `squarespace/` and
`tools/` are left out of the deploy; everything else is served as-is. There is no build step.

The full project handover (history, decisions, feedback, open items) lives in the **private** Nutrimatic repo at
`website-handover/HANDOVER.md`. Read it first when picking this work up.

## Branches

- `main`: live. Only push what's ready to be seen.
- `desk-scene`: work in progress on the co-founders' pixel-art desk scene (How it works page) and the portrait toolkit.
  Not merged; preview it locally. See the handover for its status.

## Conventions (keep these)

- **Headers**: every edited file carries a `Version X.Y.Z` and a `Modified: YYYY-MM-DD - what changed (vX.Y.Z)` line in its
  header comment; bump PATCH for fixes, MINOR for features. Same rule as the private repo's protocol.
- **No email address anywhere in the tree**, including config and history. Public contact is the LinkedIn URL,
  written out. `contactEmail` in `js/config.js` stays blank.
- **Language**: never "fresh" (it's protein powder); brands "advertise with us", never "sponsor a slot"; the page is
  "How it works", not "About"; headline is "Custom nutrition in 45 seconds." The site speaks plainly and short.
- **Design**: hard edges everywhere (`--radius: 0`, no rounded corners in CSS or in the SVG animations; the bottle
  may stay curvy); black / white / red `#e4002b`; Archivo, self-hosted. Image- and animation-forward pages, Apple-style.
- **Commits**: descriptive subject, body says why; author is `Cole Maisonpierre <67285155+Jew-C-Fruit@users.noreply.github.com>`
  (no real email in public history); end with the Claude attribution footer the private repo's protocol uses.

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
