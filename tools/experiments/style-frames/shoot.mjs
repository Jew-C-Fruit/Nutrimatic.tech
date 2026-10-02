import { chromium } from "playwright";
const out = (process.env.SHOTS_DIR || "shots") + "/"; import { mkdirSync } from "node:fs"; mkdirSync(out, { recursive: true });
const browser = await chromium.launch(); const page = await browser.newPage({ viewport: { width: 900, height: 500 } });
const errs = []; page.on("pageerror", e => errs.push(String(e)));
const frames = [["A-day-outline", "mode=day&style=outline&scene=work"], ["B-night-outline", "mode=night&style=outline&scene=night"], ["C-dusk-selout", "mode=dusk&style=selout&scene=talk"], ["D-close-crop", "mode=day&style=outline&scene=write&crop=1"]];
for (const [name, qs] of frames) { await page.goto((process.env.FRAMES_URL || "http://127.0.0.1:8765/tools/experiments/style-frames/styleframes.html") + "?" + qs + "&scale=2"); await page.waitForTimeout(200); await page.locator("#c").screenshot({ path: out + name + ".png" }); }
console.log("errors:", errs.length ? errs : "none"); await browser.close();
