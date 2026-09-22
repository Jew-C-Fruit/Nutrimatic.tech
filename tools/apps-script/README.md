# Waitlist and contact submissions into a Google Sheet

Version 1.2.0 · Created 2026-09-21 · Modified 2026-09-22 (one tab per waitlist type; manifest with pinned permissions)

`Code.gs` is a Google Apps Script that lives inside a Google Sheet. Deployed as a web app, it takes each submission from the site, appends a row on the tab for that kind of submission (**Gym owners**, **Gym members**, **Nutrition brands** or **Contact**; each tab and its header row are created on first use) and emails you a short notification: subject line, then one line per answer, nothing else. Free, runs in your own Google account, no third party. About five minutes to set up.

## Setup

1. Create a Google Sheet (any name, e.g. *Nutrimatic sign-ups*).
2. **Extensions → Apps Script.** Delete the sample code, paste in the whole of `Code.gs`, and save (the disk icon or Ctrl/Cmd-S).
3. Optional: at the top of the file, put an address in `NOTIFY_TO` if the emails should go somewhere other than the Google account you're using.
3b. Optional but recommended: pin the permissions. Project Settings (gear icon) → tick **Show "appsscript.json" manifest file in editor** → open `appsscript.json` and replace it with the one next to this README (keep your own `timeZone` if it differs). The script then asks for exactly three things: edit *this* spreadsheet only, send email as you (send only, no reading), and see your email address. Without it Google may ask for access to all your spreadsheets.
4. **Deploy → New deployment.** Click the gear next to "Select type" and choose **Web app**. Set:
   - Description: anything
   - Execute as: **Me**
   - Who has access: **Anyone** (this is what lets the site post to it without a Google sign-in; the `Anyone with Google account` option won't work)
5. **Deploy.** Google asks you to authorise the script for your sheet and your email: Authorize access → pick your account → if it says "Google hasn't verified this app", click Advanced → Go to … (unsafe) → Allow. It's your own script in your own account; the warning is standard for unpublished scripts.
6. Copy the **Web app URL** (it ends in `/exec`). Paste it into `sheetEndpoint` in `js/config.js` and push.
7. Test from the site. The row appears in the sheet within a second or two and the email a moment later.

Paste the `/exec` URL into a browser tab and you should see `{"ok":true,"message":"Nutrimatic form receiver is up"}`; that confirms the deployment before touching the site.

## Changing the script later

Edits don't go live by themselves. After saving a change: **Deploy → Manage deployments → pencil icon → Version: New version → Deploy.** The URL stays the same.

## What lands where

| Tab | Columns |
| --- | --- |
| Gym owners | Received, Name, Email, Gym, Location, Page |
| Gym members | Received, Name, Email, Gym, Location, Page |
| Nutrition brands | Received, Contact, Email, Brand website, Product, Target customer, Page |
| Contact | Received, Name, Email, Message, Page |

Each waitlist type has its own tab because they don't share fields. *Received* is a real date-time cell, so the sheet sorts and filters by it. *Page* is the URL the form was submitted from, useful if you ever share links like `waitlist.html?type=owner` in different places.

## Notes

- The web app URL is public by design, like the Web3Forms key. The script rejects anything that isn't a waitlist or contact submission with an email address, and the site's honeypot stops most bots before they post. If junk rows ever appear, delete them; nothing else is exposed.
- Gmail's own limit for scripts is 100 emails a day per account, far above what a waitlist produces. Rows have no such limit.
- With both `sheetEndpoint` and `formEndpoint` set, each submission goes to both, and the visitor sees "sent" if either one lands. Once the sheet is working, set `formEndpoint` to `""` to stop the Web3Forms duplicate, or keep both as a belt-and-braces copy.
