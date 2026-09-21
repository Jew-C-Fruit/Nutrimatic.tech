# Building the site inside Squarespace

Version 1.0.0 · Created 2026-09-13

Use this if you want the pages to live in the Squarespace editor instead of hosting the files in this repo (see `../GO-LIVE.md` for why hosting the files and pointing the domain is the recommended route). Written for Squarespace 7.1. Note the plan requirements: JavaScript in Code Blocks needs the Core plan or higher and Code Injection needs Business or higher; the hero snippet below needs neither.

## 1. Site styles

**Design → Site styles**

- **Fonts:** Headings: *Archivo Black* (or *Archivo* at weight 900), uppercase, letter-spacing −0.03em. Body: *Archivo* (or *Inter*), weight 400.
- **Colors:** Black `#111111`, white `#FFFFFF`, red accent `#E4002B`, light grey `#F6F6F4`, line grey `#E3E3E0`.
- **Buttons:** solid black, white text, 6 px radius; hover red. Secondary: outlined black.
- Paste `custom-css.css` into **Design → Custom CSS** for the red kicker bars, the price ladder, and button hover states.

## 2. Assets

Upload these under **Design → Custom CSS → Manage Custom Files** (or via any Link editor → Files). Squarespace gives each a URL like `/s/machine.svg`; use those URLs in the snippets below.

- `../assets/machine.svg` (animated placeholder), `../assets/machine-static.png` (still)
- `../assets/renders/machine-front.jpg` and the `.mp4` once you have them
- `../assets/nu-mark-red.svg` for the logo, `../assets/favicon.svg` (Squarespace wants a PNG/ICO favicon: export the SVG at 512×512)
- `../assets/team/*.jpg` for the About page

Squarespace **does** accept SVG uploads as custom files, but not through the Image Block. If an SVG is rejected, upload it as a custom file and reference its `/s/…` URL from a Code Block, or use the PNG version.

## 3. Pages

| Page | URL slug | Content source |
| --- | --- | --- |
| Home | `/` | `../index.html` |
| About | `/about` | `../how-it-works.html` |
| Contact | `/contact` | `../contact.html` |
| Waitlist | `/waitlist` | `../waitlist.html` |

Copy the text straight out of the HTML files (headings, paragraphs, bullet lists). Build the layouts with Squarespace sections: a two-column hero, a three-column "How it works", two side-by-side "audience" blocks, the four-column price ladder, and a full-width red band with a button.

## 4. Hero animation

Add a **Code Block** in the hero's right column and paste `hero-code-block.html`. It's SVG + CSS only (no JavaScript), so it works on every Squarespace plan. Update the two `/s/…` URLs to match your uploaded files. When the real rendering animation is ready, use the `<video>` variant in the same file.

## 5. Waitlist form

Squarespace's **Form Block** stores submissions for you (Settings → Storage: email, Google Drive, Mailchimp, Zapier). Recommended: **one form per audience**, each with a hidden "role" value, so the home-page buttons can deep-link to the right one and the fields can differ:

**Gym owners / managers** (`/waitlist-gyms`)

| Field | Type | Required |
| --- | --- | --- |
| Name | Name | no |
| Email | Email | yes |
| Gym name | Text | yes |
| Gym location (City, State) | Text | yes |

**Gym members** (`/waitlist-members`)

| Field | Type | Required |
| --- | --- | --- |
| Name | Name | no |
| Email | Email | yes |
| Which gym do you go to? | Text | yes |
| Gym location (City, State) | Text | yes |

**Nutrition brands** (`/waitlist-brands`)

| Field | Type | Required |
| --- | --- | --- |
| Contact name | Name | yes |
| Email | Email | yes |
| Brand website | Website | yes |
| Product to be stocked | Text | yes |
| Target customer | Text area | yes |

Add a short line above each form (the "role copy" from `../waitlist.html`), and a "Post-submit" message: *"You're on the list. We'll be in touch."*

If you'd rather have a single `/waitlist` page, use one Form Block with a **Radio** field "I am a…" (Gym owner / manager, Gym member, Nutrition brand) followed by the union of the fields above, marking only Email as required. Squarespace can't show or hide fields based on the radio choice.

Point the buttons: "I run a gym" → `/waitlist-gyms`, "I go to a gym" → `/waitlist-members`, "Sponsor a slot" → `/waitlist-brands`.

## 6. Contact page

A Form Block with Name, Email, Message, storage to your inbox, plus a text block with the LinkedIn link (linkedin.com/in/maisonpierre) and the three waitlist links. Don't print an email address on the page; it gets scraped.

## 7. Domain

The domain is already at Squarespace, so **Settings → Domains → nutrimatic.tech** just needs to be set as the primary domain for the site. Turn on **SSL: Secure** under Settings → Advanced.
