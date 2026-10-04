// Screenshots of the desk scene (v8): times of day, activities, every scenario, Maker's visits, the handover, writing frames,
// a close-up, the phone layout. -> SHOTS_DIR (default shots/)
import { chromium } from "playwright";
const out = (process.env.SHOTS_DIR || "shots") + "/"; import { mkdirSync } from "node:fs"; mkdirSync(out, { recursive: true });
const browser = await chromium.launch();
const errors = [];
async function open(width, dpr) {
  const page = await browser.newPage({ viewport: { width, height: 900 }, deviceScaleFactor: dpr || 1 });
  page.on("pageerror", e => errors.push(String(e))); page.on("console", m => { if (m.type() === "error" && !/404/.test(m.text())) errors.push(m.text()); });
  await page.goto((process.env.SITE_BASE || "http://127.0.0.1:8765/") + "how-it-works.html", { waitUntil: "networkidle" });
  await page.locator("[data-desk-scene]").scrollIntoViewIfNeeded(); await page.waitForTimeout(600);
  return page;
}
const page = await open(1200, 2);
console.log("state:", JSON.stringify(await page.evaluate(() => window.NutrimaticDesk.state())));
const cv = page.locator("[data-desk-scene] canvas");
const REST = "D.activity('cole','rest',60); D.activity('ilinca','rest',60); D.step(3);";
async function shot(name, code) { await page.evaluate(new Function("const D = window.NutrimaticDesk; " + code)); await page.waitForTimeout(150); await cv.screenshot({ path: out + name + ".png" }); }
await shot("v6-day", "D.setHour(10.5); " + REST);
await shot("v6-work", "D.activity('cole','solder',60); D.activity('ilinca','write',60); D.step(24);");
await shot("v6-type", "D.setHour(15); D.activity('cole','type',60); D.activity('ilinca','type',60); D.step(8);");
await shot("v6-think", "D.activity('cole','think',60); D.activity('ilinca','phone',60); D.step(8);");
await shot("v6-coffee", "D.activity('cole','coffee',60); D.activity('ilinca','coffee',60); D.step(16);");
await shot("v6-sunset", "D.setHour(18.9); " + REST);
await shot("v6-night", "D.setHour(23.2); D.activity('cole','think',60); D.activity('ilinca','type',60); D.step(16);");
await shot("v8-night-work", "D.setHour(22.5); D.activity('cole','solder',60); D.activity('ilinca','write',60); D.step(16);");
for (let i = 0; i < 4; i++) await shot("v8-write-" + i, (i ? "D.step(4);" : "D.setHour(11); D.activity('cole','write',60); D.activity('ilinca','write',60); D.step(1);"));
await shot("v6-ds", "D.setHour(11); " + REST + " D.scenario('ds'); D.step(60);");
await shot("v6-ds-caught", "D.step(42);");
await shot("v6-highfive", "D.step(120); " + REST + " D.scenario('highfive'); D.step(18);");
await shot("v8-maker-hands", "D.step(60); D.activity('cole','type',60); D.activity('ilinca','type',60); D.step(3); D.scenario('visit'); D.step(44);");
await shot("v8-maker-knead", "D.step(26);");
await shot("v8-maker-pet", "D.step(110);");
await shot("v8-maker-look", "D.step(90);");
await shot("v8-maker-laptop", "D.step(200); D.activity('cole','type',60); D.activity('ilinca','rest',60); D.step(3); D.scenario('laptop'); D.step(46);");
await shot("v8-maker-laptop-pet", "D.step(44);");
await shot("v8-maker-paper", "D.step(300); D.activity('cole','rest',60); D.activity('ilinca','write',60); D.step(3); D.scenario('laptop'); D.step(96);");
await shot("v6-pigeon", "D.step(140); " + REST + " D.scenario('pigeon'); D.step(48);");
await shot("v6-plane", "D.step(140); " + REST + " D.scenario('airplane'); D.step(35);");
await shot("v6-coffee-run", "D.step(120); " + REST + " D.scenario('coffee'); D.step(112);");
await shot("v8-handover-offer", "D.step(320); " + REST + " D.scenario('shake'); D.step(36);");
await shot("v8-handover-take", "D.step(13);");
await shot("v8-handover-drink", "D.step(20);");
await shot("v6-call", "D.step(140); " + REST + " D.scenario('call'); D.step(110);");
await shot("v6-spark", "D.step(60); D.activity('cole','solder',30); D.step(10); D.scenario('spark'); D.step(8);");
await shot("v6-yawn", "D.step(100); D.setHour(23.5); " + REST + " D.scenario('latenight'); D.step(10);");
console.log("state after:", JSON.stringify(await page.evaluate(() => window.NutrimaticDesk.state())));
// close-up of the two of them at 4x
const z = await open(1200, 2);
await z.evaluate(() => { const D = window.NutrimaticDesk; D.setHour(11); D.activity("cole", "rest", 30); D.activity("ilinca", "rest", 30); D.step(3); });
const box = await z.locator("[data-desk-scene] canvas").boundingBox(); const sc = box.width / 360;
await z.screenshot({ path: out + "v6-zoom.png", clip: { x: box.x + 84 * sc, y: box.y + 40 * sc, width: 180 * sc, height: 100 * sc } });
// phone
const m = await open(390, 3);
await m.evaluate(() => { const D = window.NutrimaticDesk; D.setHour(19.5); D.activity("cole", "solder", 30); D.activity("ilinca", "write", 30); D.step(24); });
console.log("mobile:", JSON.stringify(await m.evaluate(() => window.NutrimaticDesk.state())), await m.$eval("[data-desk-scene] canvas", c => c.style.width));
await m.locator("[data-desk-scene] canvas").screenshot({ path: out + "v6-mobile.png" });
console.log("errors:", errors.length ? errors : "none");
await browser.close();
