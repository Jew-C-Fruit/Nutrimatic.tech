import { chromium } from "playwright";
const base = process.env.SITE_BASE || "http://127.0.0.1:8765/";
const out = (process.env.SHOTS_DIR || "shots") + "/"; import { mkdirSync } from "node:fs"; mkdirSync(out, { recursive: true });
const browser = await chromium.launch();
const problems = [];
const expected404 = (m) => /assets\/renders\//.test(m) || /404 \(File not found\)/.test(m);
async function visit(name, url, vp, opts = {}) {
  const ctx = await browser.newContext({ viewport: vp, deviceScaleFactor: 1, ...opts });
  const page = await ctx.newPage();
  const errs = [];
  page.on("console", m => { if (m.type() === "error") errs.push("console: " + m.text()); });
  page.on("pageerror", e => errs.push("pageerror: " + e.message));
  page.on("requestfailed", r => errs.push("reqfailed: " + r.url() + " " + (r.failure() || {}).errorText));
  page.on("response", r => { if (r.status() >= 400 && r.url().startsWith(base)) errs.push("http " + r.status() + " " + r.url()); });
  await page.goto(base + url, { waitUntil: "networkidle" });
  await page.waitForTimeout(400);
  await page.screenshot({ path: out + name + ".png", fullPage: true });
  errs.forEach(e => problems.push(name + " | " + e));
  return { page, ctx };
}
const desk = { width: 1366, height: 900 }, mob = { width: 390, height: 844 };
{ const nf = await visit("404-desk", "404.html", desk); await nf.ctx.close(); }
for (const [n, u] of [["index","index.html"],["about","how-it-works.html"],["contact","contact.html"],["waitlist","waitlist.html"]]) {
  const d = await visit(n + "-desk", u, desk); await d.ctx.close();
  const m = await visit(n + "-mob", u, mob); 
  // mobile nav toggle
  await m.page.click(".nav__toggle"); await m.page.waitForTimeout(200);
  const open = await m.page.$eval(".nav", n => n.classList.contains("is-open"));
  if (!open) problems.push(n + "-mob | nav toggle did not open");
  if (n === "index") await m.page.screenshot({ path: out + "index-mob-nav.png" });
  await m.ctx.close();
}
// waitlist role behaviour
{
  const { page, ctx } = await visit("waitlist-brand", "waitlist.html?type=brand", desk);
  const checked = await page.$eval('input[name="role"]:checked', e => e.value);
  if (checked !== "brand") problems.push("waitlist | ?type=brand not preselected (" + checked + ")");
  const gymHidden = await page.$eval('#wl-gym', e => e.closest('[data-role-only]').hidden && e.disabled);
  const siteVisible = await page.$eval('#wl-website', e => !e.closest('[data-role-only]').hidden && !e.disabled);
  const nameReq = await page.$eval('#wl-name', e => e.required);
  const label = await page.$eval('label[for="wl-name"] [data-role-text]', e => e.textContent);
  if (!gymHidden || !siteVisible || !nameReq || label !== "Contact name") problems.push(`waitlist brand | gymHidden=${gymHidden} siteVisible=${siteVisible} nameReq=${nameReq} label=${label}`);
  // validation: submit empty
  await page.click('button[type="submit"]');
  const errCount = await page.$$eval('.field.has-error', els => els.length);
  if (errCount < 4) problems.push("waitlist brand | expected >=4 validation errors, got " + errCount);
  // switch to member
  await page.click('label[for="role-member"]');
  const memberLabel = await page.$eval('label[for="wl-gym"] [data-role-text]', e => e.textContent);
  const gymShown = await page.$eval('#wl-gym', e => !e.closest('[data-role-only]').hidden && !e.disabled);
  const nameReq2 = await page.$eval('#wl-name', e => e.required);
  const url = page.url();
  if (memberLabel !== "Which gym do you go to?" || !gymShown || nameReq2 || !url.includes("type=member")) problems.push(`waitlist member | label=${memberLabel} gymShown=${gymShown} nameReq=${nameReq2} url=${url}`);
  await page.screenshot({ path: out + "waitlist-member-errors.png", fullPage: true });
  // mocked endpoint submission
  await page.evaluate(() => { window.NUTRIMATIC_CONFIG.formEndpoint = "https://example.test/submit"; window.NUTRIMATIC_CONFIG.sheetEndpoint = ""; });
  let posted = null;
  await page.route("https://example.test/submit", async route => { posted = JSON.parse(route.request().postData()); await route.fulfill({ status: 200, contentType: "application/json", body: "{\"ok\":true}" }); });
  await page.fill('#wl-email', 'test@example.com'); await page.fill('#wl-gym', 'Ironworks'); await page.fill('#wl-location', 'Providence, RI');
  await page.click('button[type="submit"]'); await page.waitForTimeout(500);
  const success = await page.$eval('.form__success', e => e.hasAttribute('data-show'));
  if (!success || !posted || posted.role !== "member" || posted.gym_name !== "Ironworks" || posted.brand_website !== undefined || !posted._subject.includes("Gym member")) problems.push("waitlist submit | success=" + success + " posted=" + JSON.stringify(posted));
  await page.screenshot({ path: out + "waitlist-success.png", fullPage: true });
  await ctx.close();
}
// contact mailto fallback (no endpoint): success panel shows mailto note, navigation to mailto attempted
{
  const { page, ctx } = await visit("contact-fallback", "contact.html", desk);
  let mailto = null;
  await page.route("**/*", route => { const u = route.request().url(); if (u.startsWith("mailto:")) { mailto = u; return route.abort(); } return route.continue(); });
  await page.evaluate(() => { window.NUTRIMATIC_CONFIG.formEndpoint = ""; window.NUTRIMATIC_CONFIG.formEndpoints = { contact: "", waitlist: "" }; window.NUTRIMATIC_CONFIG.formAccessKey = ""; window.NUTRIMATIC_CONFIG.contactEmail = ""; window.NUTRIMATIC_CONFIG.sheetEndpoint = ""; });
  await page.fill('#ct-name', 'Test'); await page.fill('#ct-email', 'test@example.com'); await page.fill('#ct-message', 'Hello there');
  await page.click('button[type="submit"]'); await page.waitForTimeout(500);
  // no endpoint and no contactEmail: a status note with the LinkedIn link, fields stay visible, no fake success
  const note = await page.$eval('.form__status', e => e.textContent);
  const noteLink = await page.$eval('.form__status a', e => e.getAttribute('href')).catch(() => null);
  const fieldsHidden = await page.$eval('.form__fields', e => e.hidden);
  const successShown = await page.$eval('.form__success', e => e.hasAttribute('data-show'));
  if (!/isn.t connected yet/.test(note) || noteLink !== 'https://www.linkedin.com/in/maisonpierre' || fieldsHidden || successShown)
    problems.push(`contact fallback | note=${JSON.stringify(note)} link=${noteLink} fieldsHidden=${fieldsHidden} success=${successShown}`);
  await ctx.close();
}
// reduced motion: picture swaps to static png
{
  const { page, ctx } = await visit("index-reduced", "index.html", desk, { reducedMotion: "reduce" });
  const src = await page.$eval('[data-hero-media] img', e => e.currentSrc);
  if (!src.includes("machine-static.png")) problems.push("reduced motion | hero currentSrc=" + src);
  await ctx.close();
}
// scroll story on the About page
{
  const { page, ctx } = await visit("about-scrolly", "how-it-works.html", desk);
  await page.waitForFunction(() => { const s = document.querySelector(".scrolly__svg"); return s && s.getBoundingClientRect().height > 100; }, null, { timeout: 5000 }).catch(() => problems.push("scrolly | SVG not injected or zero-size"));
  const paused = await page.$eval(".scrolly__svg", s => s.getAnimations({ subtree: true }).filter(a => a.effect.getTiming().duration >= 1000).every(a => a.playState === "paused"));
  if (!paused) problems.push("scrolly | animations not paused");
  const top = await page.$eval("[data-scrolly]", s => s.offsetTop);
  const h = await page.$eval("[data-scrolly]", s => s.offsetHeight);
  const vh = 900;
  const seen = [];
  for (const f of [0, 0.13, 0.3, 0.62, 0.77, 0.9, 1]) {
    await page.evaluate(y => { document.documentElement.style.scrollBehavior = "auto"; window.scrollTo(0, y); }, top + f * (h - vh));
    await page.waitForTimeout(150);
    const state = await page.$$eval("[data-chapter]", els => els.map(e => e.classList.contains("is-active") ? 1 : 0).join(""));
    const time = await page.$eval(".scrolly__svg", s => Math.round(s.getAnimations({ subtree: true })[0].currentTime));
    const bar = await page.$eval("[data-scrolly-bar]", b => b.style.transform);
    seen.push(f + ":" + state + "@" + time + "ms " + bar);
    if (f === 0.3) await page.screenshot({ path: out + "about-scrolly-dose.png" }); if (f === 0.62) await page.screenshot({ path: out + "about-scrolly-mix.png" }); if (f === 0.9) await page.screenshot({ path: out + "about-scrolly-wash.png" });
    if (f === 1) await page.screenshot({ path: out + "about-scrolly-end.png" });
  }
  console.log("scrolly states:", seen.join(" | "));
  const order = seen.map(x => x.split(":")[1].split("@")[0]);
  const idx = order.map(o => o.indexOf("1"));
  const monotonic = idx.every((v, i) => i === 0 || v >= idx[i - 1]);
  if (idx[0] !== 0 || idx[idx.length - 1] !== order[0].length - 1 || !monotonic || order.some(o => (o.match(/1/g) || []).length !== 1)) problems.push("scrolly | chapter order wrong: " + order.join(","));
  await ctx.close();
  // mobile scrolly screenshot
  const m = await visit("about-scrolly-mob", "how-it-works.html", mob);
  await m.page.waitForSelector(".scrolly__svg", { timeout: 5000 }).catch(() => {});
  const mtop = await m.page.$eval("[data-scrolly]", s => s.offsetTop), mh = await m.page.$eval("[data-scrolly]", s => s.offsetHeight);
  await m.page.evaluate(y => { document.documentElement.style.scrollBehavior = "auto"; window.scrollTo(0, y); }, mtop + 0.65 * (mh - 844)); await m.page.waitForTimeout(150);
  await m.page.screenshot({ path: out + "about-scrolly-mob-mid.png" });
  await m.ctx.close();
}
// per-form endpoints: waitlist (brand) and contact each hit their own endpoint
{
  const { page, ctx } = await visit("endpoints-brand", "waitlist.html?type=brand", desk);
  await page.evaluate(() => { window.NUTRIMATIC_CONFIG.formEndpoint = "https://example.test/global"; window.NUTRIMATIC_CONFIG.formEndpoints = { contact: "https://example.test/contact", waitlist: "https://example.test/waitlist" }; window.NUTRIMATIC_CONFIG.sheetEndpoint = ""; });
  const hits = [];
  await page.route("https://example.test/**", async route => { hits.push({ url: route.request().url(), body: JSON.parse(route.request().postData()) }); await route.fulfill({ status: 200, contentType: "application/json", body: "{\"ok\":true}" }); });
  const f = page.locator("form").first();
  for (const [n, v] of Object.entries({ name: "Pat", email: "pat@example.com", brand_website: "https://brand.example", product: "Whey isolate", target_customer: "Lifters" })) await f.locator(`[name="${n}"]`).fill(v);
  await f.locator('button[type="submit"]').click(); await page.waitForTimeout(500);
  const ok = hits.length === 1 && hits[0].url === "https://example.test/waitlist" && hits[0].body.role === "brand" && hits[0].body._subject === "Nutrimatic waitlist: Nutrition brand — Pat";
  if (!ok) problems.push("endpoints brand | " + JSON.stringify(hits));
  await ctx.close();
}
{
  const { page, ctx } = await visit("endpoints-contact", "contact.html", desk);
  await page.evaluate(() => { window.NUTRIMATIC_CONFIG.formEndpoint = "https://example.test/global"; window.NUTRIMATIC_CONFIG.formEndpoints = { contact: "https://example.test/contact", waitlist: "" }; window.NUTRIMATIC_CONFIG.sheetEndpoint = ""; });
  const hits = [];
  await page.route("https://example.test/**", async route => { hits.push({ url: route.request().url(), body: JSON.parse(route.request().postData()) }); await route.fulfill({ status: 200, contentType: "application/json", body: "{\"ok\":true}" }); });
  await page.fill('#ct-name', 'Pat'); await page.fill('#ct-email', 'pat@example.com'); await page.fill('#ct-message', 'Hello there');
  await page.click('button[type="submit"]'); await page.waitForTimeout(500);
  const success = await page.$eval('.form__success', e => e.hasAttribute('data-show'));
  const ok = success && hits.length === 1 && hits[0].url === "https://example.test/contact" && hits[0].body.form === "contact" && hits[0].body._subject === "Nutrimatic contact: Pat";
  if (!ok) problems.push("endpoints contact | success=" + success + " " + JSON.stringify(hits));
  await ctx.close();
}
// empty per-form entry falls back to the global endpoint
{
  const { page, ctx } = await visit("endpoints-fallback", "waitlist.html?type=member", desk);
  await page.evaluate(() => { window.NUTRIMATIC_CONFIG.formEndpoint = "https://example.test/global"; window.NUTRIMATIC_CONFIG.formEndpoints = { contact: "", waitlist: "" }; window.NUTRIMATIC_CONFIG.sheetEndpoint = ""; });
  const hits = [];
  await page.route("https://example.test/**", async route => { hits.push(route.request().url()); await route.fulfill({ status: 200, contentType: "application/json", body: "{\"ok\":true}" }); });
  await page.fill('#wl-email', 'test@example.com'); await page.fill('#wl-gym', 'Ironworks'); await page.fill('#wl-location', 'Providence, RI');
  await page.click('button[type="submit"]'); await page.waitForTimeout(500);
  if (hits.length !== 1 || hits[0] !== "https://example.test/global") problems.push("endpoints fallback | " + JSON.stringify(hits));
  await ctx.close();
}
// Web3Forms: access key + renamed subject; a {success:false} reply is a failure; no key = not connected
{
  const { page, ctx } = await visit("web3forms", "contact.html", desk);
  await page.evaluate(() => { window.NUTRIMATIC_CONFIG.formEndpoint = "https://api.web3forms.com/submit"; window.NUTRIMATIC_CONFIG.formEndpoints = { contact: "", waitlist: "" }; window.NUTRIMATIC_CONFIG.formAccessKey = "key-123"; window.NUTRIMATIC_CONFIG.sheetEndpoint = ""; });
  let body = null, reply = { status: 200, body: "{\"success\":true,\"message\":\"ok\"}" };
  await page.route("https://api.web3forms.com/submit", async route => { body = JSON.parse(route.request().postData()); await route.fulfill({ status: reply.status, contentType: "application/json", body: reply.body }); });
  await page.fill('#ct-name', 'Pat'); await page.fill('#ct-email', 'pat@example.com'); await page.fill('#ct-message', 'Hello there');
  await page.click('button[type="submit"]'); await page.waitForTimeout(500);
  const success = await page.$eval('.form__success', e => e.hasAttribute('data-show'));
  const keys = body ? Object.keys(body).join(",") : "";
  const ok = success && body && body.access_key === "key-123" && body.subject === "Nutrimatic contact: Pat" && body.from_name === "Nutrimatic website" && body.email === "pat@example.com" && body.Name === "Pat" && body.Message === "Hello there" && keys === "access_key,subject,from_name,Name,email,Message";
  if (!ok) problems.push("web3forms payload | success=" + success + " " + JSON.stringify(body));
  await ctx.close();
}
{
  const { page, ctx } = await visit("web3forms-fail", "contact.html", desk);
  await page.evaluate(() => { window.NUTRIMATIC_CONFIG.formEndpoint = "https://api.web3forms.com/submit"; window.NUTRIMATIC_CONFIG.formEndpoints = { contact: "", waitlist: "" }; window.NUTRIMATIC_CONFIG.formAccessKey = "key-123"; window.NUTRIMATIC_CONFIG.sheetEndpoint = ""; });
  await page.route("https://api.web3forms.com/submit", async route => { await route.fulfill({ status: 200, contentType: "application/json", body: "{\"success\":false,\"message\":\"Invalid access key\"}" }); });
  await page.fill('#ct-name', 'Pat'); await page.fill('#ct-email', 'pat@example.com'); await page.fill('#ct-message', 'Hello there');
  await page.click('button[type="submit"]'); await page.waitForTimeout(500);
  const success = await page.$eval('.form__success', e => e.hasAttribute('data-show'));
  const status = await page.$eval('.form__status', e => e.textContent);
  const busy = await page.$eval('button[type="submit"]', e => e.disabled);
  if (success || !/didn.t send/.test(status) || busy) problems.push(`web3forms fail | success=${success} status=${JSON.stringify(status)} busy=${busy}`);
  await ctx.close();
}
{
  const { page, ctx } = await visit("web3forms-nokey", "contact.html", desk);
  await page.evaluate(() => { window.NUTRIMATIC_CONFIG.formEndpoint = "https://api.web3forms.com/submit"; window.NUTRIMATIC_CONFIG.formEndpoints = { contact: "", waitlist: "" }; window.NUTRIMATIC_CONFIG.formAccessKey = ""; window.NUTRIMATIC_CONFIG.sheetEndpoint = ""; });
  let hit = false; await page.route("https://api.web3forms.com/submit", async route => { hit = true; await route.fulfill({ status: 200, body: "{}" }); });
  await page.fill('#ct-name', 'Pat'); await page.fill('#ct-email', 'pat@example.com'); await page.fill('#ct-message', 'Hello there');
  await page.click('button[type="submit"]'); await page.waitForTimeout(400);
  const status = await page.$eval('.form__status', e => e.textContent);
  if (hit || !/isn.t connected yet/.test(status)) problems.push(`web3forms nokey | hit=${hit} status=${JSON.stringify(status)}`);
  await ctx.close();
}
// sheet endpoint (Apps Script): text/plain JSON with the full record; success if either delivery lands
async function sheetCase(label, path, fills, cfgPatch, replies) {
  const { page, ctx } = await visit(label, path, desk);
  await page.evaluate((patch) => { Object.assign(window.NUTRIMATIC_CONFIG, { sheetEndpoint: "" }, patch); }, cfgPatch);
  const hits = [];
  await page.route(/example\.test|api\.web3forms\.com|script\.google\.com/, async route => {
    const url = route.request().url(); const ct = route.request().headers()["content-type"] || "";
    hits.push({ url, ct, body: JSON.parse(route.request().postData()) });
    const r = replies[Object.keys(replies).find(k => url.includes(k))] || { status: 200, body: "{\"ok\":true}" };
    await route.fulfill({ status: r.status, contentType: "application/json", body: r.body });
  });
  const f = page.locator("form").first();
  for (const [n, v] of Object.entries(fills)) await f.locator(`[name="${n}"]`).fill(v);
  await f.locator('button[type="submit"]').click(); await page.waitForTimeout(600);
  const success = await page.$eval('.form__success', e => e.hasAttribute('data-show'));
  const status = await page.$eval('.form__status', e => e.textContent);
  await ctx.close();
  return { hits, success, status };
}
const SHEET = "https://script.google.com/macros/s/TESTID/exec";
const memberFill = { email: "t@example.com", gym_name: "Ironworks", gym_location: "Providence, RI" };
{ // both configured, both land
  const r = await sheetCase("sheet-both", "waitlist.html?type=member", memberFill,
    { formEndpoint: "https://api.web3forms.com/submit", formEndpoints: { contact: "", waitlist: "" }, formAccessKey: "key-123", sheetEndpoint: SHEET }, {});
  const sheetHit = r.hits.find(h => h.url === SHEET), mailHit = r.hits.find(h => h.url.includes("web3forms"));
  const ok = r.success && r.hits.length === 2 && sheetHit && sheetHit.ct.startsWith("text/plain") && sheetHit.body.form === "waitlist" && sheetHit.body.role === "member" && sheetHit.body.gym_name === "Ironworks" && sheetHit.body.page && sheetHit.body.submitted_at && sheetHit.body._subject.includes("Gym member") && mailHit && mailHit.body.Gym === "Ironworks" && mailHit.body.Location === "Providence, RI" && mailHit.body.form === undefined;
  if (!ok) problems.push("sheet both | " + JSON.stringify(r));
}
{ // sheet only
  const r = await sheetCase("sheet-only", "contact.html", { name: "Pat", email: "pat@example.com", message: "Hi" },
    { formEndpoint: "", formEndpoints: { contact: "", waitlist: "" }, formAccessKey: "", sheetEndpoint: SHEET }, {});
  if (!(r.success && r.hits.length === 1 && r.hits[0].url === SHEET && r.hits[0].body.form === "contact" && r.hits[0].body.message === "Hi")) problems.push("sheet only | " + JSON.stringify(r));
}
{ // sheet fails, email lands -> still a success
  const r = await sheetCase("sheet-fail-mail-ok", "waitlist.html?type=member", memberFill,
    { formEndpoint: "https://api.web3forms.com/submit", formEndpoints: { contact: "", waitlist: "" }, formAccessKey: "key-123", sheetEndpoint: SHEET },
    { "script.google.com": { status: 500, body: "{\"ok\":false,\"message\":\"boom\"}" } });
  if (!(r.success && r.hits.length === 2)) problems.push("sheet fail / mail ok | " + JSON.stringify(r));
}
{ // both fail -> error, no success
  const r = await sheetCase("sheet-both-fail", "waitlist.html?type=member", memberFill,
    { formEndpoint: "https://api.web3forms.com/submit", formEndpoints: { contact: "", waitlist: "" }, formAccessKey: "key-123", sheetEndpoint: SHEET },
    { "script.google.com": { status: 200, body: "{\"ok\":false}" }, "web3forms": { status: 200, body: "{\"success\":false,\"message\":\"bad key\"}" } });
  if (r.success || !/didn.t send/.test(r.status) || r.hits.length !== 2) problems.push("sheet both fail | " + JSON.stringify(r));
}
await browser.close();
const real = problems.filter(m => !expected404(m));
console.log(real.length ? "PROBLEMS:\n" + real.join("\n") : "ALL CHECKS PASSED" + (problems.length ? ` (${problems.length} expected render-probe 404s ignored)` : ""));
