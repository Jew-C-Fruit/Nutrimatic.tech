/*
 * Nutrimatic Website - render-static-assets.mjs
 * Version 1.2.1
 *
 * Created: 2026-09-13 - Renders the static fallbacks with headless Chromium (v1.0.0)
 * Modified: 2026-09-15 - Also renders process-static.png for the About page cutaway (v1.1.0)
 *   - assets/machine-static.png : the machine SVG with animation off (reduced-motion state), 2x
 *   - assets/og.png             : 1200x630 link-preview image
 *   - assets/logo-512.png       : square raster logo for structured data / apple-touch-icon
 * Modified: 2026-09-21 - Run from the repo root of the site's own repo (v1.2.1)
 *
 * Usage (from the repo root, Playwright installed globally or in node_modules):
 *   node tools/render-static-assets.mjs
 */

import { chromium } from "playwright";
import { fileURLToPath, pathToFileURL } from "node:url";
import path from "node:path";
import fs from "node:fs";
import os from "node:os";

const here = path.dirname(fileURLToPath(import.meta.url));
const site = path.resolve(here, "..");
const assets = path.join(site, "assets");

const proxy = process.env.HTTPS_PROXY || process.env.https_proxy;
const browser = await chromium.launch(proxy ? { proxy: { server: proxy } } : {});

// 1) Static machine fallback: same SVG, animations disabled via prefers-reduced-motion.
{
  const ctx = await browser.newContext({ viewport: { width: 960, height: 900 }, deviceScaleFactor: 2, reducedMotion: "reduce" });
  const page = await ctx.newPage();
  const svg = fs.readFileSync(path.join(assets, "machine.svg"), "utf8");
  const fontUrl = pathToFileURL(path.join(assets, "fonts", "archivo-latin-var.woff2")).href;
  const tmp = path.join(os.tmpdir(), "nutrimatic-machine.html");
  fs.writeFileSync(tmp, `<!doctype html><html><head><style>@font-face{font-family:Archivo;src:url("${fontUrl}") format("woff2");font-weight:100 900}body{margin:0;background:transparent}svg{display:block;width:960px;height:900px}</style></head><body>${svg}</body></html>`);
  await page.goto(pathToFileURL(tmp).href, { waitUntil: "load" });
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(200);
  await page.screenshot({ path: path.join(assets, "machine-static.png"), omitBackground: true });
  await ctx.close();
  console.log("wrote assets/machine-static.png");
}

// 1b) Static cutaway for the About page scroll story.
{
  const ctx = await browser.newContext({ viewport: { width: 940, height: 520 }, deviceScaleFactor: 2, reducedMotion: "reduce" });
  const page = await ctx.newPage();
  const svg = fs.readFileSync(path.join(assets, "process.svg"), "utf8");
  await page.setContent(`<!doctype html><html><body style="margin:0;background:transparent">${svg}</body></html>`);
  await page.waitForTimeout(200);
  await page.screenshot({ path: path.join(assets, "process-static.png"), omitBackground: true });
  await ctx.close();
  console.log("wrote assets/process-static.png");
}

// 2) Open Graph image.
{
  const ctx = await browser.newContext({ viewport: { width: 1200, height: 630 }, deviceScaleFactor: 1, reducedMotion: "reduce", ignoreHTTPSErrors: !!proxy });
  const page = await ctx.newPage();
  const wordmark = fs.readFileSync(path.join(assets, "wordmark.svg"), "utf8");
  const mark = fs.readFileSync(path.join(assets, "nu-mark-red.svg"), "utf8");
  const machine = fs.readFileSync(path.join(assets, "machine.svg"), "utf8");
  const fontUrl = pathToFileURL(path.join(assets, "fonts", "archivo-latin-var.woff2")).href;
  const html = `<!doctype html><html><head>
    <style>
      @font-face{font-family:Archivo;src:url("${fontUrl}") format("woff2");font-weight:100 900}
      body{margin:0;width:1200px;height:630px;background:#fff;font-family:Archivo,"Helvetica Neue",Helvetica,Arial,sans-serif;color:#111;overflow:hidden}
      .wrap{position:relative;width:1200px;height:630px}
      .left{position:absolute;left:80px;top:78px;width:660px}
      .mark{width:84px;height:84px}
      .word{width:520px;margin-top:38px;color:#111}
      .rule{width:96px;height:8px;background:#e4002b;margin:34px 0 30px}
      .tag{font-size:34px;line-height:1.25;font-weight:500;color:#333336;max-width:600px}
      .url{position:absolute;left:80px;bottom:60px;font-size:20px;font-weight:900;letter-spacing:.18em;text-transform:uppercase}
      .machine{position:absolute;right:0;top:75px;width:512px;height:480px}
      .machine svg{width:100%;height:100%}
      .bg{position:absolute;right:0;top:0;width:520px;height:630px;background:radial-gradient(120% 90% at 55% 45%,#fff 0%,#f6f6f4 55%,#ebebe8 100%)}
    </style></head><body><div class="wrap">
      <div class="bg"></div>
      <div class="left">
        <div class="mark">${mark}</div>
        <div class="word">${wordmark}</div>
        <div class="rule"></div>
        <div class="tag">Custom nutrition in 45 seconds. Built into the gym floor.</div>
      </div>
      <div class="url">nutrimatic.tech</div>
      <div class="machine">${machine}</div>
    </div></body></html>`;
  const tmp = path.join(os.tmpdir(), "nutrimatic-og.html");
  fs.writeFileSync(tmp, html);
  await page.goto(pathToFileURL(tmp).href, { waitUntil: "load" });
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(300);
  await page.screenshot({ path: path.join(assets, "og.png") });
  await ctx.close();
  console.log("wrote assets/og.png");
}

// 3) Square raster logo (structured data wants a raster, and iOS wants a touch icon).
{
  const ctx = await browser.newContext({ viewport: { width: 512, height: 512 }, deviceScaleFactor: 1 });
  const page = await ctx.newPage();
  const mark = fs.readFileSync(path.join(assets, "nu-mark-white.svg"), "utf8");
  await page.setContent(`<!doctype html><html><body style="margin:0;width:512px;height:512px;background:#111111;display:grid;place-items:center"><div style="width:360px;height:360px">${mark}</div></body></html>`);
  await page.screenshot({ path: path.join(assets, "logo-512.png") });
  await ctx.close();
  console.log("wrote assets/logo-512.png");
}

await browser.close();
