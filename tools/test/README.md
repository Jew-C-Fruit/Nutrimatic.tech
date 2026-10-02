# Site checks

Version 1.0.0 · Created 2026-10-02 (moved here from the development session's scratch space)

Playwright scripts that load every page in headless Chromium and fail on console errors, broken form routing, a
scroll story that doesn't scrub, or a missing desk scene.

```bash
cd tools/test
npm install && npx playwright install chromium --with-deps     # once; on a Raspberry Pi use the 64-bit OS
npm run serve &                                                 # serves the repo root on :8765
npm test                                                        # "ALL CHECKS PASSED" or a PROBLEMS list
npm run test:forms                                              # the not-connected fallback note on all three forms
npm run shots:desk                                              # screenshots of the desk scene at several hours and scenarios -> shots/
```

`SITE_BASE` overrides the server (`SITE_BASE=https://nutrimatic.tech/ npm test` checks the live site; form submissions
there are intercepted by the test, nothing is sent). `SHOTS_DIR` sets where screenshots go. Six 404s for
`assets/renders/machine-front.jpg` are expected until a real render is dropped in; the test ignores them.
