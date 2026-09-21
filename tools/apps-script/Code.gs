/*
 * Nutrimatic Website - Code.gs (Google Apps Script)
 * Version 1.0.0
 *
 * Created: 2026-09-21 - Receives the site's form submissions: one row per submission in a
 *   Google Sheet (tabs "Waitlist" and "Contact") and a short notification email (v1.0.0)
 *
 * Lives inside the Google Sheet it writes to (Extensions -> Apps Script), deployed as a
 * web app. Setup steps: README.md next to this file. The site posts JSON as text/plain.
 */

// Leave empty to email the Google account that deployed the script; or put an address here.
var NOTIFY_TO = "";

var TABS = { waitlist: "Waitlist", contact: "Contact" };
var COLUMNS = {
  waitlist: ["Received", "Role", "Name", "Email", "Gym", "Location", "Brand website", "Product", "Target customer", "Page"],
  contact: ["Received", "Name", "Email", "Message", "Page"]
};
var ROLES = { owner: "Gym owner / manager", member: "Gym member", brand: "Nutrition brand" };

function doPost(e) {
  try {
    var d = JSON.parse((e && e.postData && e.postData.contents) || "{}");
    var form = d.form === "contact" ? "contact" : (d.form === "waitlist" ? "waitlist" : "");
    if (!form || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(String(d.email || ""))) {
      return reply({ ok: false, message: "rejected" });
    }
    var row = appendRow(form, d);
    var mailed = notify(form, d);
    return reply({ ok: true, row: row, mailed: mailed });
  } catch (err) {
    return reply({ ok: false, message: String(err) });
  }
}

// Opening the /exec URL in a browser shows this, which is a handy "is it deployed" check.
function doGet() {
  return reply({ ok: true, message: "Nutrimatic form receiver is up" });
}

function reply(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}

function appendRow(form, d) {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getSheetByName(TABS[form]) || ss.insertSheet(TABS[form]);
  if (sheet.getLastRow() === 0) {
    sheet.appendRow(COLUMNS[form]);
    sheet.setFrozenRows(1);
    sheet.getRange(1, 1, 1, COLUMNS[form].length).setFontWeight("bold");
  }
  var when = new Date();
  var row = form === "waitlist"
    ? [when, roleLabel(d.role), s(d.name), s(d.email), s(d.gym_name), s(d.gym_location), s(d.brand_website), s(d.product), s(d.target_customer), s(d.page)]
    : [when, s(d.name), s(d.email), s(d.message), s(d.page)];
  sheet.appendRow(row);
  return sheet.getLastRow();
}

// Short email: subject says form and role; body is just the answers, one per line.
function notify(form, d) {
  var to = NOTIFY_TO || Session.getEffectiveUser().getEmail();
  if (!to) { return false; }
  var lines = [];
  if (form === "waitlist") {
    lines.push(roleLabel(d.role));
    if (d.name) { lines.push(s(d.name)); }
    lines.push(s(d.email));
    if (d.gym_name) { lines.push(s(d.gym_name) + (d.gym_location ? " — " + s(d.gym_location) : "")); }
    if (d.brand_website) { lines.push(s(d.brand_website)); }
    if (d.product) { lines.push("Product: " + s(d.product)); }
    if (d.target_customer) { lines.push("Target customer: " + s(d.target_customer)); }
  } else {
    lines.push(s(d.name) + " <" + s(d.email) + ">");
    lines.push("");
    lines.push(s(d.message));
  }
  MailApp.sendEmail({
    to: to,
    subject: s(d._subject) || ("Nutrimatic " + form),
    body: lines.join("\n"),
    replyTo: s(d.email),
    name: "Nutrimatic website"
  });
  return true;
}

function roleLabel(role) { return ROLES[role] || s(role); }
function s(v) { return v === undefined || v === null ? "" : String(v).slice(0, 5000); }
