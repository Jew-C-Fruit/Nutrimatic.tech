# Nutrimatic website

Static marketing site for **nutrimatic.tech**: splash page with the machine animation, How it works, Contact, and a three-way waitlist (gym owners / managers, gym members, nutrition brands).

Version 1.2.3 · Created 2026-09-13 · Modified 2026-09-21 (the site is its own public repo; forms point to LinkedIn until an endpoint is set; per-form endpoints; no CNAME file, the domain is set in Pages settings)

No build step. This repo *is* the site: every file in it is served as-is, apart from the docs and tooling noted below. It is public because GitHub Pages on a free account only serves public repos. Everything else about Nutrimatic (firmware, master controller) stays in the private Nutrimatic repo.

```
nutrimatic.tech/   (repo root)
├── index.html            Splash: the machine animation, one line, calls to action
├── how-it-works.html     Everything else: cutaway process story, feature tiles, pricing, founders
├── contact.html          Contact form + LinkedIn
├── waitlist.html         Waitlist form (owner / member / brand), pre-selectable via ?type=
├── css/site.css          Styles (Archivo, black / white / red from the 2026 deck)
├── js/config.js          ← the only file you need to edit to go live (forms, renders, analytics)
├── js/site.js            Nav, hero media swap, role switch, form submission
├── assets/
│   ├── machine.svg       Animated kiosk placeholder (CSS animation inside the SVG)
│   ├── machine-static.png  Same, still frame, for reduced-motion visitors and as a poster
│   ├── process.svg       Cutaway "how a drink is made" animation (follows the master controller's real dispense sequence)
│   ├── process-static.png  Still frame of the cutaway
│   ├── og.png            Link preview image
│   ├── logo-512.png      Raster logo (structured data, apple-touch-icon)
│   ├── nu-mark*.svg      "nu" monogram (black / red / white), extracted from the deck PDF
│   ├── wordmark.svg      NUTRIMATIC wordmark, extracted from the deck PDF
│   ├── favicon.svg
│   ├── fonts/            Archivo variable font (self-hosted, OFL)
│   ├── renders/          ← drop the real machine renders here (see renders/README.md)
│   ├── sequence/         ← numbered frames for the scroll story (see sequence/README.md)
│   └── team/             Co-founder photos (from the deck)
├── squarespace/          Snippets + instructions if you build the pages inside Squarespace
├── tools/render-static-assets.mjs   Regenerates machine-static.png and og.png
├── 404.html              Not-found page (GitHub Pages serves it automatically)
├── GO-LIVE.md            Squarespace integration + SEO spec
├── .github/workflows/deploy-website.yml   Publishes to GitHub Pages on every push to main
├── robots.txt · sitemap.xml
```

## Preview locally

```bash
python3 -m http.server 8080      # from the repo root; or: npx serve .
# open http://localhost:8080
```

## Before going live: `js/config.js`

| Setting | What it does |
| --- | --- |
| `formEndpoint` | Where the waitlist and contact forms POST (JSON). Empty = submitting shows a note pointing to the LinkedIn page (or, if `contactEmail` is set, opens the visitor's email app with everything pre-filled). See **Forms** below. |
| `formEndpoints` | Optional per-form overrides, `contact` and `waitlist`, for two separate inboxes. Either one left empty falls back to `formEndpoint`. |
| `formAccessKey` | Web3Forms only: the access key for your inbox (a string, or `{ contact, waitlist }` for two inboxes), with `formEndpoint` set to `https://api.web3forms.com/submit`. |
| `contactEmail` | Optional "to" address for the email-app fallback when `formEndpoint` is empty. Blank on purpose: every visitor downloads this file, so anything here can be scraped. Public contact is the LinkedIn link in the footers. |
| `heroImage` | Path to the still render. Defaults to `assets/renders/machine-front.jpg`; the page uses it as soon as the file exists. |
| `heroVideo` | Optional `mp4` / `webm` paths for the rendering animation. Plays muted and looping, with `heroImage` as the poster. |
| `scrollSequence` | Frame sequence for the scroll-driven story: `path` pattern, `count`, `pad`, `fit`. With `count: 0` the section scrubs the SVG placeholder. See `assets/sequence/README.md`. |
| `analytics` | `plausibleDomain` or `ga4Id`. Off until set. Forms fire a lead event with the role. |

### Hero fallback chain

1. `heroVideo` if set and the browser can play it (skipped when the visitor prefers reduced motion)
2. `heroImage` still render, if the file exists
3. `assets/machine.svg`, the animated placeholder
4. `assets/machine-static.png` for visitors with reduced-motion enabled

### Scroll-driven story

The section at the top of the How it works page pins to the viewport for about four screens of scrolling. Scroll position drives two things: which of the six captions is visible, and the frame of the visual. With a frame sequence configured it draws the matching frame on a canvas (the apple.com technique). Without one it pauses the cutaway SVG's CSS animations (`assets/process.svg`) and sets their current time from the scroll position, so the real sequence plays under your thumb: place, prime, dose, mix, deliver, wash. The section reads its SVG, scrub length and still from `data-scrolly-src`, `data-scrolly-ms` and `data-scrolly-still` on the section element.

## Forms

Both forms post JSON to `formEndpoint` with an `Accept: application/json` header, which is what Formspree, Web3Forms, Basin, Getform and most form back-ends expect. For a Web3Forms endpoint the payload also carries `access_key` and `from_name`, and the subject line is sent as `subject` instead of `_subject`. Field names:

| Form | Fields |
| --- | --- |
| Waitlist, owner / member | `role` (`owner` or `member`), `name` (optional), `email`, `gym_name`, `gym_location` |
| Waitlist, brand | `role` (`brand`), `name` (contact), `email`, `brand_website`, `product`, `target_customer` |
| Contact | `name`, `email`, `message` |
| All | `_subject` (a readable subject line), `form`, `page`, `submitted_at`; `_gotcha` is a honeypot and is dropped |

Two ready-made options, both free and both keep your address off the site:

- **Web3Forms** (250 submissions a month free): sign up at web3forms.com with the inbox you want, paste the access key it gives you into `formAccessKey`, set `formEndpoint` to `https://api.web3forms.com/submit`. Submissions arrive as email; the dashboard keeps 30 days of history. Honeypot plus a server-side check are on by default; hCaptcha is a free option, domain restriction is paid.
- **Formspree** (50 submissions a month free): create a form at formspree.io, paste its endpoint (`https://formspree.io/f/xxxxxxxx`) into `formEndpoint` (or two forms into `formEndpoints`). Emailed to you and kept in the Formspree inbox for 30 days; the Google Sheets export is on the paid plans. Any endpoint that accepts JSON works; a Google Apps Script web app writing to a Sheet is a free alternative.

Links like `waitlist.html?type=owner`, `?type=member` and `?type=brand` pre-select the role.

## Going live

Read **`GO-LIVE.md`** first: it explains the one direct Squarespace integration that exists (pointing the domain), the exact DNS records, what the Squarespace-editor route would cost you, and the SEO launch checklist. The short version follows.

## Hosting with the domain at Squarespace

The domain **nutrimatic.tech** is registered at Squarespace. Two ways to put this site behind it:

### Option A: host the files on GitHub Pages, keep the domain at Squarespace (recommended)

The site stays exactly as built here, deploys from this repo, and costs nothing.

1. GitHub → repo **Settings → Pages → Build and deployment → Source: GitHub Actions**.
2. Push to `main` (or run the **Deploy website** workflow manually under **Actions**). The workflow in `.github/workflows/deploy-website.yml` publishes the repo minus docs and tooling.
3. Still under **Settings → Pages**, type `nutrimatic.tech` into **Custom domain** and save (once; a `CNAME` file is ignored for GitHub Actions deployments). Once the DNS check goes green, tick **Enforce HTTPS**.
4. Squarespace → **Domains → nutrimatic.tech → DNS settings**. Remove Squarespace's default A / CNAME records for `@` and `www`, then add:

   | Type | Host | Value |
   | --- | --- | --- |
   | A | @ | `185.199.108.153` |
   | A | @ | `185.199.109.153` |
   | A | @ | `185.199.110.153` |
   | A | @ | `185.199.111.153` |
   | CNAME | www | `jew-c-fruit.github.io` |

   DNS takes minutes to a few hours. GitHub's "DNS check" on the Pages settings page turns green when it's ready.

### Option B: rebuild the pages inside the Squarespace editor

If you'd rather edit copy in Squarespace and use its built-in form storage, follow `squarespace/README.md`. It has the hero animation as a paste-in Code Block, custom CSS for the brand, and the exact waitlist field list.

## Regenerating the static images

`assets/machine-static.png` and `assets/og.png` are rendered from the SVGs with headless Chromium:

```bash
npm i -D playwright && npx playwright install chromium   # once
node tools/render-static-assets.mjs
```

Run it again if you change `machine.svg`, the wordmark, or the tagline in the script.

## Editing notes

- Headers, footers and `<head>` blocks are repeated in each HTML file (no templating). Change all four when you change one.
- Every file carries a version / date header per the repo's file modification protocol. Bump it when you edit.
- The Archivo font is self-hosted in `assets/fonts/` (SIL Open Font License, `OFL.txt` alongside it), so the site makes no third-party requests at all.
