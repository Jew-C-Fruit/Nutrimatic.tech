/*
 * Nutrimatic Website - Code.gs (Google Apps Script)
 * Version 1.1.0
 *
 * Created: 2026-09-21 - Receives the site's form submissions: one row per submission in a
 *   Google Sheet and a short notification email (v1.0.0)
 * Modified: 2026-09-22 - One tab per waitlist type (Gym owners, Gym members, Nutrition brands)
 *   with columns to match, plus the Contact tab (v1.1.0)
 *
 * Lives inside the Google Sheet it writes to (Extensions -> Apps Script), deployed as a
 * web app. Setup steps: README.md next to this file. The site posts JSON as text/plain.
 */

// Leave empty to email the Google account that deployed the script; or put an address here.
var NOTIFY_TO = "";

// One tab per kind of submission, each with its own columns.
var TABS = { owner: "Gym owners", member: "Gym members", brand: "Nutrition brands", contact: "Contact" };
var COLUMNS = {
  owner: ["Received", "Name", "Email", "Gym", "Location", "Page"],
  member: ["Received", "Name", "Email", "Gym", "Location", "Page"],
  brand: ["Received", "Contact", "Email", "Brand website", "Product", "Target customer", "Page"],
  contact: ["Received", "Name", "Email", "Message", "Page"]
};
var ROLES = { owner: "Gym owner / manager", member: "Gym member", brand: "Nutrition brand" };

function doPost(e) {
  try {
    var d = JSON.parse((e && e.postData && e.postData.contents) || "{}");
    var kind = kindOf(d);
    if (!kind || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(String(d.email || ""))) {
      return reply({ ok: false, message: "rejected" });
    }
    var row = appendRow(kind, d);
    var mailed = notify(kind, d);
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

// "contact", or the waitlist role ("owner" / "member" / "brand"); "" for anything else.
function kindOf(d) {
  if (d.form === "contact") { return "contact"; }
  if (d.form === "waitlist" && COLUMNS.hasOwnProperty(d.role) && d.role !== "contact") { return d.role; }
  return "";
}

function appendRow(kind, d) {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getSheetByName(TABS[kind]) || ss.insertSheet(TABS[kind]);
  if (sheet.getLastRow() === 0) {
    sheet.appendRow(COLUMNS[kind]);
    sheet.setFrozenRows(1);
    sheet.getRange(1, 1, 1, COLUMNS[kind].length).setFontWeight("bold");
  }
  var when = new Date();
  var row;
  if (kind === "contact") { row = [when, s(d.name), s(d.email), s(d.message), s(d.page)]; }
  else if (kind === "brand") { row = [when, s(d.name), s(d.email), s(d.brand_website), s(d.product), s(d.target_customer), s(d.page)]; }
  else { row = [when, s(d.name), s(d.email), s(d.gym_name), s(d.gym_location), s(d.page)]; }
  sheet.appendRow(row);
  return sheet.getLastRow();
}

// Short email: subject says form and role; body is just the answers, one per line.
function notify(kind, d) {
  var to = NOTIFY_TO || Session.getEffectiveUser().getEmail();
  if (!to) { return false; }
  var lines = [];
  if (kind !== "contact") {
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
    subject: s(d._subject) || ("Nutrimatic " + kind),
    body: lines.join("\n"),
    replyTo: s(d.email),
    name: "Nutrimatic website"
  });
  return true;
}

function roleLabel(role) { return ROLES[role] || s(role); }
function s(v) { return v === undefined || v === null ? "" : String(v).slice(0, 5000); }
