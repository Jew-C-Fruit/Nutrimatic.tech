import { chromium } from "playwright";
const base = process.env.SITE_BASE || "http://127.0.0.1:8765/";
const browser = await chromium.launch();
const page = await browser.newPage();
const out = [];
async function check(label, path, fills) {
  await page.goto(base + path, { waitUntil: "networkidle" });
  await page.evaluate(() => { window.NUTRIMATIC_CONFIG.formEndpoint = ""; window.NUTRIMATIC_CONFIG.formEndpoints = { contact: "", waitlist: "" }; window.NUTRIMATIC_CONFIG.formAccessKey = ""; window.NUTRIMATIC_CONFIG.contactEmail = ""; window.NUTRIMATIC_CONFIG.sheetEndpoint = ""; });
  const form = page.locator("form").first();
  for (const [name, value] of Object.entries(fills)) await form.locator(`[name="${name}"]`).fill(value);
  await form.locator('button[type="submit"]').click();
  await page.waitForTimeout(400);
  out.push({
    label,
    status: await form.locator(".form__status").textContent(),
    link: await form.locator(".form__status a").getAttribute("href").catch(() => null),
    fieldsHidden: await form.locator(".form__fields").evaluate(el => el.hidden),
    successShown: await form.locator(".form__success").evaluate(el => el.hasAttribute("data-show")),
    url: page.url()
  });
}
await check("waitlist/member", "waitlist.html?type=member", { email: "t@example.com", gym_name: "Test Gym", gym_location: "Denver" });
await check("waitlist/brand", "waitlist.html?type=brand", { name: "Pat", email: "t@example.com", brand_website: "https://example.com", product: "Whey", target_customer: "Lifters" });
await check("contact", "contact.html", { name: "Pat", email: "t@example.com", message: "Hello there" });
console.log(JSON.stringify(out, null, 2));
await browser.close();
