// Nutrimatic desk scene - hands/capture.mjs
// Version 1.0.0
// Created: 2026-10-06 - Exact frames of the live scene with candidate poses patched in (the hand library, to-do round 31) (v1.0.0)
//
// node capture.mjs JOB.json
// JOB = { "base": "http://127.0.0.1:8765/how-it-works.html", "out": "/abs/dir", "shots": [
//   { "name": "cand-a", "patch": {"cole": {pose: layers}}, "widths": [1200, 390], "hour": 13,
//     "code": "D.review({cole:'rest', ilinca:'rest'})", "frames": 1, "step": 1, "warm": 2 } ] }
// For each shot and width: <out>/<name>-w<width>-<NN>.png, the scene's own pixels (360x160 wide, 240x160 phone), and
// <name>-w<width>.json with the pose drawn in each frame. The scene is held still (reduced motion; only D.step advances).
import { chromium } from "../../test/node_modules/playwright/index.mjs";
import { readFileSync, writeFileSync, mkdirSync } from "node:fs";

const job = JSON.parse(readFileSync(process.argv[2], "utf8"));
mkdirSync(job.out, { recursive: true });
const browser = await chromium.launch();
const errors = [];
for (const width of [...new Set(job.shots.flatMap(s => s.widths || [1200, 390]))]) {
  const page = await browser.newPage({ viewport: { width, height: 900 }, deviceScaleFactor: 1, reducedMotion: "reduce" });
  page.on("pageerror", e => errors.push(String(e)));
  await page.goto(job.base || "http://127.0.0.1:8765/how-it-works.html", { waitUntil: "networkidle" });
  await page.addStyleTag({ content: `[data-desk-scene]{width:${width < 480 ? 240 : 720}px !important;max-width:none !important;flex:none !important}` });
  await page.locator("[data-desk-scene]").scrollIntoViewIfNeeded(); await page.waitForTimeout(400);
  for (const s of job.shots.filter(s => (s.widths || [1200, 390]).includes(width))) {
    const log = await page.evaluate(async (s) => {
      const D = window.NutrimaticDesk; D.unpatchPoses("cole"); D.unpatchPoses("ilinca");
      for (const who of Object.keys(s.patch || {})) { D.patchPoses(who, s.patch[who]); }
      D.setHour(s.hour === undefined ? 13 : s.hour); D.still(s.still !== false);
      D.review({ cole: "rest", ilinca: "rest" });
      (new Function("D", s.code || ""))(D);
      D.step(s.warm === undefined ? 3 : s.warm);                       // the faces settle (looks ease toward their targets)
      return true;
    }, s);
    const poses = [];
    for (let i = 0; i < (s.frames || 1); i++) {
      if (i > 0) { await page.evaluate(n => window.NutrimaticDesk.step(n), s.step || 1); }
      const url = await page.evaluate(() => {
        const c = document.querySelector("[data-desk-scene] canvas"), half = c.width > 400, W = half ? c.width / 2 : c.width, H = half ? c.height / 2 : c.height;
        const o = document.createElement("canvas"); o.width = W; o.height = H; const x = o.getContext("2d"); x.imageSmoothingEnabled = false; x.drawImage(c, 0, 0, W, H); return o.toDataURL("image/png");
      });
      writeFileSync(`${job.out}/${s.name}-w${width}-${String(i).padStart(2, "0")}.png`, Buffer.from(url.split(",")[1], "base64"));
      poses.push(await page.evaluate(() => window.NutrimaticDesk.state().poses));
    }
    writeFileSync(`${job.out}/${s.name}-w${width}.json`, JSON.stringify({ poses, layout: width < 480 ? "narrow" : "wide" }));
  }
  await page.close();
}
await browser.close();
if (errors.length) { console.error("page errors:", errors); process.exit(1); }
console.log("captured", job.shots.length, "shots into", job.out);
