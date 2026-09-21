# Going live: Squarespace integration and SEO

Version 1.1.3 · Created 2026-09-13 · Modified 2026-09-21 (site in its own public repo; forms point to LinkedIn until an endpoint is set; custom domain is typed into Pages settings, not read from a CNAME file)

## Part 1 — Squarespace

### The short answer

There is **no direct "push this code into Squarespace" integration** for a current Squarespace site:

- **Developer Mode** (Git / SFTP access to a template) only exists on legacy version 7.0 sites. Version 7.1 sites, which is what any new Squarespace site is, do not support template-level code. ([Squarespace Developer Platform FAQ](https://support.squarespace.com/hc/en-us/articles/206545717-Squarespace-Developer-Platform-FAQ), [overview](https://www.sparkplugin.com/blog/squarespace-developer-mode))
- Squarespace's **APIs** cover commerce (products, orders, inventory, transactions, profiles), not pages or form submissions. ([developers.squarespace.com](https://developers.squarespace.com/quick-start/))
- Custom code on 7.1 goes in through **Code Injection** and **Code Blocks**, and JavaScript in either needs a paid tier: Code Injection is Business plan and up, and JavaScript / iframes in Code Blocks are a premium feature of the current Core plan and up. ([Premium features](https://support.squarespace.com/hc/en-us/articles/115015517328-Premium-features), [Using code injection](https://support.squarespace.com/hc/en-us/articles/205815908-Using-code-injection))

The direct integration that **does** exist is at the domain level. Squarespace officially supports pointing a Squarespace-registered domain at a site hosted somewhere else ("[Pointing a Squarespace domain](https://support.squarespace.com/hc/en-us/articles/215744668-Pointing-a-Squarespace-domain)"), and GitHub Pages is a common target ([GitHub community walkthrough](https://github.com/orgs/community/discussions/78573)).

**Recommendation:** host the site from this repo on GitHub Pages and point `nutrimatic.tech` at it. The site ships exactly as built (scroll story, role-switching waitlist, no plan upgrade), deploys on every merge, and costs nothing. Squarespace keeps the domain (and any domain email). About 15 minutes of clicking plus DNS propagation.

The site lives in its own public repo, this one, because GitHub Pages on a free account only serves public repos. The private Nutrimatic repo keeps everything else and just links here.

### Path A: GitHub Pages + Squarespace DNS (recommended)

**GitHub (once)**

1. Repo **Settings → Pages → Build and deployment → Source: GitHub Actions**.
2. Push to `main` (the first push does it), or run **Actions → Deploy website → Run workflow**. The workflow publishes the repo minus docs and tooling. It also tries to switch Pages on by itself; if that step fails, do step 1 and re-run it.
3. Back in **Settings → Pages**, type `nutrimatic.tech` into **Custom domain** and save. This is typed once: with a GitHub Actions deployment GitHub ignores any `CNAME` file in the repo. When the DNS check under that field goes green, tick **Enforce HTTPS**.

**Squarespace (once)**

4. **Domains → nutrimatic.tech → DNS settings**. Delete the default Squarespace records for `@` and `www` (the "Squarespace defaults" section; there's usually a "delete all" for it), then add under **Custom records**:

   | Type | Host | Data |
   | --- | --- | --- |
   | A | @ | `185.199.108.153` |
   | A | @ | `185.199.109.153` |
   | A | @ | `185.199.110.153` |
   | A | @ | `185.199.111.153` |
   | CNAME | www | `jew-c-fruit.github.io` |

   Leave any MX / TXT records for email alone.
5. Wait for the DNS check on the GitHub Pages settings page to go green (minutes to a few hours; Squarespace says up to 48 h).

**Forms (once)**

6. Squarespace won't receive the forms in this path. Either [web3forms.com](https://web3forms.com) (250 submissions a month free: paste its access key into `formAccessKey` and set `formEndpoint` to `https://api.web3forms.com/submit`) or [formspree.io](https://formspree.io) (50 a month free: paste the form endpoint into `formEndpoint`, or one per form into `formEndpoints`). Both email every submission to you and keep 30 days of history; neither exports to a spreadsheet on the free plan. Until an endpoint is set, submitting a form shows a note pointing to the LinkedIn page, so nobody is told their details were sent when they weren't. `contactEmail` in `js/config.js` is deliberately blank: every visitor downloads that file, so an address there could be scraped.

**Everything else is optional:** analytics IDs in `config.js`, the real renders in `assets/renders/`, the frame sequence in `assets/sequence/`.

### Path B: rebuild inside the Squarespace editor

Choose this only if you want to edit pages in Squarespace's editor or use its built-in form storage and email campaigns.

| Piece | How it transfers | Needs |
| --- | --- | --- |
| Copy, layout, images | Rebuilt with Squarespace sections and blocks from the four HTML files | Any plan |
| Brand fonts / colours / buttons | `squarespace/custom-css.css` in Design → Custom CSS | Any plan |
| Hero machine animation | `squarespace/hero-code-block.html` in a Code Block (SVG + CSS, no JS) | Any plan |
| Scroll-driven story | Code Block containing the section markup + `site.js` + `config.js` | Core plan or higher (JS in Code Blocks) |
| Waitlist with role switching | Not reproducible; use three Form Blocks on three pages (field list in `squarespace/README.md`) | Any plan |
| Contact form | Form Block | Any plan |
| Structured data / social meta | Squarespace generates basics; JSON-LD via Code Injection | Business plan or higher |

Full step-by-step in `squarespace/README.md`.

### Hybrid

Both can coexist: apex `nutrimatic.tech` → GitHub Pages (this site), and a subdomain such as `news.nutrimatic.tech` → a Squarespace site for a blog or press page later (Squarespace: Domains → add subdomain; connect it to the Squarespace site). Don't publish the same pages in both places; search engines will treat it as duplicate content.

### Pre-launch checklist

- [ ] `js/config.js`: `formEndpoint` set and tested (submit once from each role; check the sheet)
- [ ] `js/config.js`: `contactEmail` still blank (anything in that file is public)
- [ ] Real render in `assets/renders/machine-front.jpg` (hero) and `cartridge-bay.jpg` (How it works)
- [ ] Copy pass on the claims (45 s, 8 slots, $3–5, "0 repairs", founder bios) — they come from the deck; make sure you're happy publishing them
- [ ] DNS records added, GitHub DNS check green, HTTPS enforced
- [ ] `https://nutrimatic.tech`, `https://www.nutrimatic.tech`, and `http://` all land on the site
- [ ] Share a link in Slack / iMessage / LinkedIn and check the preview card (`assets/og.png`)
- [ ] Search Console set up (Part 2)

## Part 2 — SEO

The site is small, so most SEO work is done at build time and the rest is a launch-day checklist.

### Already in place

| Item | Where |
| --- | --- |
| Unique `<title>` and meta description per page, one `<h1>` per page, logical heading order | each HTML file |
| Canonical URLs on `https://nutrimatic.tech/…` | `<link rel="canonical">` |
| Open Graph + Twitter cards with a 1200×630 preview image | `<meta property="og:…">`, `assets/og.png` |
| Structured data (JSON-LD): `Organization`, `WebSite`, `WebPage` / `AboutPage` / `ContactPage`, founders as `Person` | `<script type="application/ld+json">` in each page |
| `sitemap.xml` and `robots.txt` | site root |
| Custom 404 (noindex) | `404.html` |
| Performance: no third-party requests, self-hosted variable font (35 KB, preloaded), SVG hero, lazy-loaded below-fold images, explicit image dimensions (no layout shift) | `css/site.css`, `index.html` |
| Mobile layout, keyboard-accessible nav and forms, reduced-motion support | `css/site.css`, `js/site.js` |
| Favicon (SVG) + apple-touch-icon + raster logo for search results | `assets/favicon.svg`, `assets/logo-512.png` |

### Launch day

1. **Google Search Console**: add `nutrimatic.tech` as a Domain property. Verify with the DNS TXT record Google gives you (add it under Squarespace → Domains → DNS → Custom records). Submit `https://nutrimatic.tech/sitemap.xml`.
2. **Bing Webmaster Tools**: import from Search Console (one click) so Bing / DuckDuckGo / ChatGPT search index it too.
3. **Analytics**: set `analytics.plausibleDomain` (cookie-free, no banner) or `analytics.ga4Id` in `js/config.js`. Both forms already fire a `Lead` / `generate_lead` event with the role, so you can see waitlist conversions by audience.
4. **Profiles**: when the LinkedIn company page, Instagram, etc. exist, add their URLs to the `sameAs` array in the JSON-LD `Organization` (each page) so Google links them to the brand.
5. **Request indexing** for the four URLs in Search Console after the DNS check is green.

### Keyword map

Search volume for this category is small and specific, which is good: the queries are high-intent and mostly uncontested.

| Page | Primary query | Secondary queries | Title tag |
| --- | --- | --- | --- |
| Home | protein shake vending machine | protein shake machine for gyms, gym protein shake kiosk, automated protein shake dispenser | Nutrimatic — Protein shake vending machine for gyms *(swap in once live; current title is the brand line)* |
| How it works | supplement sampling for gyms | sports nutrition trial channel, gym supplement kiosk, point-of-sale sampling supplement brands | How Nutrimatic works — the protein shake kiosk, step by step |
| Waitlist | protein shake machine for my gym | get a protein shake machine, gym vending partnership, supplement brand sampling program | Join the Nutrimatic waitlist — gyms, members, brands |
| Contact | nutrimatic contact | — | Contact Nutrimatic |

Work the primary phrase into the `<h1>` or first paragraph where it reads naturally (the home lead already says "self-serve kiosk"; "protein shake vending machine" is the phrase people actually type, so say it once on the home page even if you don't love it).

### Content that will earn rankings (post-launch, optional)

Three or four evergreen pages, each answering a query gym owners type into Google. Static HTML in this folder works fine (add them to `sitemap.xml`), or a Squarespace blog on a subdomain (see Hybrid above).

- "How much does a protein shake vending machine make?" (use the deck's per-machine model, ranges only)
- "Protein shake machine vs smoothie bar: cost, staff, margins"
- "How gyms sell supplements without staff"
- "What's in a Nutrimatic cartridge" (brands, servings, tracking)

Later, per-gym landing pages ("Nutrimatic at Ironworks Fitness, Providence") are a cheap, scalable local-SEO play once machines are installed: each one is a page members will search for and gyms will link to.

### Technical guardrails

- Keep the hero render under ~300 KB (JPEG q80 or WebP) and give it `width` / `height` attributes; it will be the Largest Contentful Paint element.
- Keep every page's total transfer under ~1 MB on first load; the frame sequence for the scroll story loads only on the How it works page and only when configured.
- One canonical host: `www` redirects to the apex automatically on GitHub Pages once the CNAME record is in place. Don't publish the site at a second URL.
- Don't add third-party embeds (chat widgets, fonts, tag managers) without a reason; each one costs real Core Web Vitals points.
- Re-run `node tools/render-static-assets.mjs` whenever the wordmark, tagline, or machine SVG changes so the preview image stays current.

### Measuring

Monthly, in Search Console: impressions and clicks for the queries above, plus any new queries appearing under "Performance". In analytics: waitlist `Lead` events by role. That's the whole dashboard until there are machines on the floor.

Sources: [Squarespace Developer Platform FAQ](https://support.squarespace.com/hc/en-us/articles/206545717-Squarespace-Developer-Platform-FAQ) · [Squarespace Developer Mode guide (sparkplugin)](https://www.sparkplugin.com/blog/squarespace-developer-mode) · [Squarespace Developer Platform quick start](https://developers.squarespace.com/quick-start/) · [Squarespace premium features](https://support.squarespace.com/hc/en-us/articles/115015517328-Premium-features) · [Using code injection](https://support.squarespace.com/hc/en-us/articles/205815908-Using-code-injection) · [Pointing a Squarespace domain](https://support.squarespace.com/hc/en-us/articles/215744668-Pointing-a-Squarespace-domain) · [GitHub Pages + Squarespace domain discussion](https://github.com/orgs/community/discussions/78573)
