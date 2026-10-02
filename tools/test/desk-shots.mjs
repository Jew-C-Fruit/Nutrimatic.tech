import { chromium } from "playwright";
const out = (process.env.SHOTS_DIR || "shots") + "/"; import { mkdirSync } from "node:fs"; mkdirSync(out, { recursive: true });
const browser = await chromium.launch();
const errors = [];
async function open(width, dpr) {
  const page = await browser.newPage({ viewport: { width, height: 900 }, deviceScaleFactor: dpr || 1 });
  page.on("pageerror", e => errors.push(String(e))); page.on("console", m => { if (m.type() === "error") errors.push(m.text()); });
  await page.goto((process.env.SITE_BASE || "http://127.0.0.1:8765/") + "how-it-works.html", { waitUntil: "networkidle" });
  await page.locator("[data-desk-scene]").scrollIntoViewIfNeeded(); await page.waitForTimeout(600);
  return page;
}
const page = await open(1200);
console.log("state:", JSON.stringify(await page.evaluate(() => window.NutrimaticDesk.state())));
const cv = page.locator("[data-desk-scene] canvas");
async function shot(name, setup) { await page.evaluate(setup); await page.waitForTimeout(250); await cv.screenshot({ path: out + name + ".png" }); }
await shot("v5-day", () => { const D = window.NutrimaticDesk; D.setHour(10.5); D.activity("cole", "solder", 30); D.activity("ilinca", "type", 30); D.step(14); });
await shot("v5-write", () => { const D = window.NutrimaticDesk; D.setHour(15); D.activity("cole", "type", 30); D.activity("ilinca", "write", 30); D.step(14); });
await shot("v5-night", () => { const D = window.NutrimaticDesk; D.setHour(23.2); D.activity("cole", "think", 30); D.activity("ilinca", "coffee", 30); D.step(14); });
await shot("v5-ds", () => { const D = window.NutrimaticDesk; D.setHour(11); D.scenario("ds"); D.step(Math.round(8.3 * 12)); });
await shot("v5-ds-guilty", () => { const D = window.NutrimaticDesk; D.step(Math.round(1.2 * 12)); });
await shot("v5-highfive", () => { const D = window.NutrimaticDesk; D.step(60); D.scenario("highfive"); D.step(Math.round(1.5 * 12)); });
await shot("v5-cat", () => { const D = window.NutrimaticDesk; D.step(60); D.scenario("cat"); D.step(Math.round(10 * 12)); });
await shot("v5-pigeon", () => { const D = window.NutrimaticDesk; D.step(120); D.scenario("pigeon"); D.step(Math.round(4 * 12)); });
await shot("v5-plane", () => { const D = window.NutrimaticDesk; D.step(120); D.scenario("airplane"); D.step(Math.round(2.9 * 12)); });
await shot("v5-coffee", () => { const D = window.NutrimaticDesk; D.step(120); D.scenario("coffee"); D.step(Math.round(10 * 12)); });
await shot("v5-spark", () => { const D = window.NutrimaticDesk; D.step(120); D.activity("cole", "solder", 30); D.scenario("spark"); D.step(Math.round(0.9 * 12)); });
console.log("state after:", JSON.stringify(await page.evaluate(() => window.NutrimaticDesk.state())));
// zoom on the heads at 3x
const z = await open(1200, 3);
await z.evaluate(() => { const D = window.NutrimaticDesk; D.setHour(11); D.activity("cole", "rest", 30); D.activity("ilinca", "rest", 30); D.step(3); });
const box = await z.locator("[data-desk-scene] canvas").boundingBox(); const sc = box.width / 360;
await z.screenshot({ path: out + "v5-zoom.png", clip: { x: box.x + 100 * sc, y: box.y + 48 * sc, width: 150 * sc, height: 92 * sc } });
// phone
const m = await open(390, 2);
await m.evaluate(() => { const D = window.NutrimaticDesk; D.setHour(19.5); D.activity("cole", "solder", 30); D.activity("ilinca", "write", 30); D.step(14); });
console.log("mobile:", JSON.stringify(await m.evaluate(() => window.NutrimaticDesk.state())), await m.$eval("[data-desk-scene] canvas", c => c.style.width));
await m.locator("[data-desk-scene] canvas").screenshot({ path: out + "v5-mobile.png" });
console.log("errors:", errors.length ? errors : "none");
await browser.close();
