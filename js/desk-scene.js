/*
 * Nutrimatic Website - desk-scene.js
 * Version 0.5.1
 *
 * Created: 2026-10-01 - Living pixel-art scene of the co-founders at their desk (v0.1.0)
 * Modified: 2026-10-01 - Likeness pass (v0.2.0); browline glasses, desk lamp, blazer (v0.3.0); redraw at a larger scale (v0.4.0)
 * Modified: 2026-10-01 - Seated proportions with jointed arms; two layouts (wide desk on desktop, closer on phones);
 *   blue henley, neater hair with a forehead curl, lighter hair for Ilinca; name plates; articulated lamp that swings
 *   over whoever is soldering or writing and casts a cone of light; New York skyline that lights up at night;
 *   scripted scenarios (Nintendo DS, high five, paper airplane, pigeon, cat, coffee run, shake break, late night,
 *   solder spark); desk set per visit; no frame, no speech bubbles (v0.5.0)
 *
 * Markup: <div data-desk-scene><canvas></canvas> ...fallback... </div>
 * Test hooks: window.NutrimaticDesk.setHour(h), .activity(who, name, secs), .react(who), .scenario(name), .converse(), .state()
 */

(function () {
  "use strict";

  var FPS = 12, HEAD_Y = 56, DESK_Y = 118;
  var reduceMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  var host = document.querySelector("[data-desk-scene]");
  var canvas = host && host.querySelector("canvas");
  if (!host || !canvas || !canvas.getContext) { return; }
  var ctx = canvas.getContext("2d");
  var off = document.createElement("canvas");
  var g = off.getContext("2d");

  /* ---------- layouts: a wide desk on desktop, the two of them closer on phones ---------- */
  var LAYOUTS = {
    wide:   { W: 360, H: 144, cole: 136, ilinca: 212, poster: { x: 20, y: 12, w: 58, h: 60 }, clock: { x: 174, y: 22 }, win: { x: 272, y: 14, w: 66, h: 74 }, lamp: 174, slots: [58, 250, 318, 22] },
    narrow: { W: 240, H: 144, cole: 70, ilinca: 142, poster: { x: 4, y: 10, w: 50, h: 50 }, clock: { x: 106, y: 20 }, win: { x: 178, y: 14, w: 54, h: 70 }, lamp: 106, slots: [168, 212, 16] }
  };
  var L = LAYOUTS.wide, W = L.W, H = L.H, WIN = L.win, layoutName = "";

  /* ---------- palette ---------- */
  var C = {
    wall: "#f6f6f4", wallShade: "#e4e4e0",
    ink: "#111111", ink2: "#2a2a2c", ink3: "#3d3d40", grey: "#8d8d90", greyLight: "#c4c4c0", white: "#ffffff", red: "#e4002b", redDeep: "#b80022",
    deskTop: "#3a3a3d", deskFront: "#1f1f21", deskEdge: "#56565a", plate: "#f4f4f1", plateS: "#b9b9b5",
    cSkin: "#e6b792", cSkinS: "#c48e68", cHair: "#22160f", cHairH: "#43302a", henley: "#3b6ea9", henleyS: "#2b5486", henleyL: "#5b8fcb", frames: "#262626", rim: "#a9a9a6",
    iSkin: "#f0cdb0", iSkinS: "#d1a585", iHair: "#6f4f35", iHairH: "#a07b57", blazer: "#232326", blazerS: "#4a4a50", blouse: "#f4f4f1", blush: "#e9b4a2",
    lips: "#c4727b", lipsL: "#dc9a9f", mouth: "#6e3b36", teeth: "#ffffff", brow: "#2a1b12", browI: "#4a3220",
    green: "#2f7d4f", greenL: "#58a56f", leaf: "#3f8f55", stem: "#4b7a3a", petalR: "#e4002b", petalW: "#ffffff", petalY: "#f2c744",
    pot: "#9a5a3c", potS: "#7a4530", board: "#2f6b3a", boardS: "#214d2a", copper: "#d19a4a",
    iron: "#9a9a9e", ironHot: "#ff6a3d", smoke: "#b9b9b6", smoke2: "#d6d6d2", phone: "#111111", phoneScreen: "#dfe9f5",
    paper: "#ffffff", paperLine: "#c9c9c4", mug: "#e4002b", mugS: "#b80022",
    laptop: "#cfcfcb", laptopS: "#9a9a97", laptopD: "#7c7c79", ds: "#d6162f", dsS: "#9d0f22", dsScreen: "#cfe3d4",
    lampBody: "#111111", lampShade: "#f4f4f0", lampShadeOn: "#ffe9a8", cone: "rgba(255, 214, 120, 0.20)", cone2: "rgba(255, 224, 150, 0.16)",
    skyNight: "#0d1030", skyNight2: "#1a1f4a", star: "#ffffff", moon: "#f3f1d8", skyDawn1: "#f0a66a", skyDawn2: "#86a2d6",
    skyDay1: "#8dc5f0", skyDay2: "#cfe8fb", skyDusk1: "#f29a5c", skyDusk2: "#5d4e8c", sun: "#ffd84a", cloud: "#ffffff", cloudS: "#e8f1f8",
    bldg: "#6e7a8c", bldgFar: "#8f9bab", bldgNight: "#0b0d20", bldgNightFar: "#141735", winLit: "#ffd97a", winLit2: "#ffe9b0", beacon: "#ff3b3b",
    cat: "#141414", catEye: "#7fd07f", pigeon: "#8a8f99", pigeonL: "#b4b8c0", pigeonD: "#5c6070", plane: "#ffffff", planeS: "#b9b9b5"
  };

  /* ---------- helpers: whole pixels only ---------- */
  function px(x, y, c) { g.fillStyle = c; g.fillRect(x | 0, y | 0, 1, 1); }
  function rect(x, y, w, h, c) { g.fillStyle = c; g.fillRect(x | 0, y | 0, w | 0, h | 0); }
  function hline(x, y, w, c) { rect(x, y, w, 1, c); }
  function vline(x, y, h, c) { rect(x, y, 1, h, c); }
  function outline(x, y, w, h, c) { hline(x, y, w, c); hline(x, y + h - 1, w, c); vline(x, y, h, c); vline(x + w - 1, y, h, c); }
  function sprite(rows, x, y, pal) {
    for (var r = 0; r < rows.length; r++) { var row = rows[r]; for (var i = 0; i < row.length; i++) { var k = row[i]; if (k !== "." && pal[k]) { px(x + i, y + r, pal[k]); } } }
  }
  function limb(x1, y1, x2, y2, w, c) {
    var dx = Math.abs(x2 - x1), dy = Math.abs(y2 - y1), sx = x1 < x2 ? 1 : -1, sy = y1 < y2 ? 1 : -1, err = dx - dy, x = x1, y = y1, o = (w / 2) | 0;
    g.fillStyle = c;
    for (var guard = 0; guard < 500; guard++) {
      g.fillRect(x - o, y - o, w, w);
      if (x === x2 && y === y2) { break; }
      var e2 = 2 * err; if (e2 > -dy) { err -= dy; x += sx; } if (e2 < dx) { err += dx; y += sy; }
    }
  }
  function lerp(a, b, t) { return a + (b - a) * t; }
  function hexToRgb(h) { return [parseInt(h.slice(1, 3), 16), parseInt(h.slice(3, 5), 16), parseInt(h.slice(5, 7), 16)]; }
  function mix(h1, h2, t) {
    var a = hexToRgb(h1), b = hexToRgb(h2);
    return "#" + [0, 1, 2].map(function (i) { return ("0" + Math.round(a[i] + (b[i] - a[i]) * t).toString(16)).slice(-2); }).join("");
  }
  function hash(a, b, c) { var n = (a * 73856093) ^ (b * 19349663) ^ (c * 83492791); n = (n ^ (n >>> 13)) * 1274126177; return ((n ^ (n >>> 16)) >>> 0) % 1000; }

  /* ---------- 3x5 pixel font ---------- */
  var FONT = {
    A: "010101111101101", B: "110101110101110", C: "011100100100011", D: "110101101101110", E: "111100110100111", F: "111100110100100",
    G: "011100101101011", H: "101101111101101", I: "111010010010111", J: "001001001101010", K: "101101110101101", L: "100100100100111",
    M: "101111111101101", N: "110101101101101", O: "010101101101010", P: "110101110100100", Q: "010101101110011", R: "110101110101101",
    S: "011100010001110", T: "111010010010010", U: "101101101101111", V: "101101101101010", W: "101101111111101", X: "101101010101101",
    Y: "101101010010010", Z: "111001010100111", " ": "000000000000000"
  };
  function textWidth(s) { return s.length * 4 - 1; }
  function drawText(s, x, y, c) {
    s = String(s).toUpperCase();
    for (var i = 0; i < s.length; i++) { var bits = FONT[s[i]] || FONT[" "]; for (var j = 0; j < 15; j++) { if (bits[j] === "1") { px(x + i * 4 + (j % 3), y + ((j / 3) | 0), c); } } }
  }

  /* ---------- time of day ---------- */
  var hourOverride = null;
  function hourNow() { if (hourOverride !== null) { return hourOverride; } var d = new Date(); return d.getHours() + d.getMinutes() / 60; }
  function skyFor(h) {
    function pick(h) {
      if (h < 5 || h >= 21) { return [C.skyNight, C.skyNight2]; } if (h < 7) { return [C.skyDawn1, C.skyDawn2]; }
      if (h < 17.5) { return [C.skyDay1, C.skyDay2]; } if (h < 20) { return [C.skyDusk1, C.skyDusk2]; } return [C.skyNight, C.skyNight2];
    }
    var bounds = [5, 7, 17.5, 20, 21];
    for (var i = 0; i < bounds.length; i++) { var b = bounds[i]; if (Math.abs(h - b) < 0.5) { var t = h - (b - 0.5), a = pick(b - 0.6), z = pick(b + 0.6); return [mix(a[0], z[0], t), mix(a[1], z[1], t)]; } }
    return pick(h);
  }
  function isDark(h) { return h < 6.5 || h >= 18.5; }

  /* ---------- wall: poster, clock ---------- */
  var NU = ["wwwww.ww.ww", "ww.ww.ww.ww", "ww.ww.ww.ww", "ww.ww.ww.ww", "ww.ww.wwwww"];
  function drawPoster(P) {
    rect(P.x, P.y, P.w, P.h, C.ink); rect(P.x + 3, P.y + 3, P.w - 6, P.h - 6, C.white);
    var mx = P.x + ((P.w - 22) / 2 | 0), my = P.y + (P.h > 55 ? 12 : 9);
    for (var r = 0; r < NU.length; r++) { for (var i = 0; i < NU[r].length; i++) { if (NU[r][i] === "w") { rect(mx + i * 2, my + r * 2, 2, 2, C.ink); } } }
    hline(P.x + 10, my + 16, P.w - 20, C.ink);
    drawText("NUTRIMATIC", P.x + ((P.w - 39) / 2 | 0), my + 22, C.ink);
    hline(P.x + ((P.w - 18) / 2 | 0), my + 31, 18, C.greyLight);
  }
  function drawClock(cx, cy, h) {
    rect(cx - 7, cy - 7, 15, 15, C.white); outline(cx - 7, cy - 7, 15, 15, C.ink);
    px(cx, cy - 6, C.ink); px(cx, cy + 6, C.ink); px(cx - 6, cy, C.ink); px(cx + 6, cy, C.ink);
    var hr = (h % 12) / 12 * Math.PI * 2, mn = (h % 1) * Math.PI * 2;
    for (var i = 1; i <= 3; i++) { px(cx + Math.round(Math.sin(hr) * i), cy - Math.round(Math.cos(hr) * i), C.ink); }
    for (var j = 1; j <= 5; j++) { px(cx + Math.round(Math.sin(mn) * j), cy - Math.round(Math.cos(mn) * j), C.red); }
    px(cx, cy, C.ink);
  }
  function drawWall(h) { rect(0, 0, W, DESK_Y, C.wall); rect(0, DESK_Y - 5, W, 5, C.wallShade); drawPoster(L.poster); drawClock(L.clock.x, L.clock.y, h); }

  /* ---------- window with a New York skyline ---------- */
  var stars = [], clouds = [{ x: 0, y: 14, w: 14 }, { x: 30, y: 26, w: 9 }, { x: 52, y: 8, w: 11 }];
  function makeStars() {
    stars = []; var seed = 11; function rnd() { seed = (seed * 9301 + 49297) % 233280; return seed / 233280; }
    for (var i = 0; i < 26; i++) { stars.push({ x: 2 + ((rnd() * (WIN.w - 4)) | 0), y: 2 + ((rnd() * (WIN.h - 40)) | 0), p: (rnd() * 20) | 0 }); }
  }
  // Buildings in a 66-wide strip, left to right: x, width, height, kind. Heights from the window bottom.
  var FAR = [[2, 10, 22], [26, 9, 20], [44, 12, 24], [58, 8, 18]];
  var NEAR = [
    [0, 6, 12, "block"], [7, 10, 18, "empire"], [18, 4, 36, "slender"], [23, 8, 14, "block"], [31, 7, 24, "chrysler"],
    [39, 6, 10, "block"], [46, 8, 30, "wtc"], [55, 6, 16, "block"], [62, 5, 9, "block"]
  ];
  function drawBuilding(b, bx, by, dark, f, far) {
    var x = bx + b[0], w = b[1], h = b[2], kind = b[3] || "block", col = far ? (dark ? C.bldgNightFar : C.bldgFar) : (dark ? C.bldgNight : C.bldg);
    var top = by - h;
    if (x + w > bx + WIN.w) { w = bx + WIN.w - x; if (w <= 0) { return; } }
    rect(x, top, w, h, col);
    if (kind === "empire") {        // stepped setbacks and a spire
      rect(x + 1, top - 6, w - 2, 6, col); rect(x + 2, top - 11, w - 4, 5, col); rect(x + 3, top - 16, w - 6, 5, col); vline(x + (w / 2 | 0), top - 22, 6, col);
      if (dark) { rect(x + 3, top - 16, w - 6, 3, C.winLit2); px(x + (w / 2 | 0), top - 22, (f % 12 < 6) ? C.beacon : C.winLit2); }
    } else if (kind === "chrysler") { // the crown: narrowing tiers, lit arches at night
      rect(x + 1, top - 3, w - 2, 3, col); rect(x + 2, top - 6, w - 4, 3, col); vline(x + (w / 2 | 0), top - 11, 5, col);
      if (dark) { px(x + 1, top - 2, C.winLit2); px(x + w - 2, top - 2, C.winLit2); px(x + 2, top - 5, C.winLit2); px(x + w - 3, top - 5, C.winLit2); px(x + (w / 2 | 0), top - 7, C.winLit2); }
    } else if (kind === "wtc") {      // tapering tower, antenna with a beacon
      rect(x + 1, top - 4, w - 2, 4, col); rect(x + 2, top - 8, w - 4, 4, col); vline(x + (w / 2 | 0), top - 16, 8, col);
      if (dark) { px(x + (w / 2 | 0), top - 16, (f % 10 < 5) ? C.beacon : C.winLit2); rect(x + 2, top - 8, w - 4, 1, C.winLit2); }
    } else if (kind === "slender") {  // 432 Park: a thin grid
      if (dark) { for (var yy = top + 2; yy < by - 1; yy += 3) { if (hash(x, yy, f >> 6) % 3) { px(x + 1, yy, C.winLit); } if (hash(x + 2, yy, f >> 6) % 3) { px(x + 2, yy, C.winLit); } } }
      else { for (var y2 = top + 2; y2 < by - 1; y2 += 3) { hline(x, y2, w, mix(col, C.white, 0.18)); } }
      return;
    }
    if (!far) {
      if (dark) { for (var wy = top + 2; wy < by - 1; wy += 2) { for (var wx = x + 1; wx < x + w - 1; wx += 2) { if (hash(wx, wy, f >> 5) % 5 < 2) { px(wx, wy, (hash(wx, wy, 3) % 2) ? C.winLit : C.winLit2); } } } }
      else { for (var dy = top + 2; dy < by - 1; dy += 3) { for (var dx = x + 1; dx < x + w - 1; dx += 3) { px(dx, dy, mix(col, C.white, 0.22)); } } }
    }
  }
  function drawWindow(h, f) {
    var sky = skyFor(h), bands = 8, dark = isDark(h);
    for (var i = 0; i < bands; i++) { rect(WIN.x, WIN.y + Math.round(i * WIN.h / bands), WIN.w, Math.ceil(WIN.h / bands) + 1, mix(sky[0], sky[1], i / (bands - 1))); }
    if (dark) {
      for (var s = 0; s < stars.length; s++) { var st = stars[s]; if (((f >> 3) + st.p) % 7 !== 0) { px(WIN.x + st.x, WIN.y + st.y, C.star); } }
      var mx = WIN.x + 8 + Math.round(((h + 3) % 24) / 24 * (WIN.w - 22)), my = WIN.y + 8;
      rect(mx, my, 6, 6, C.moon); px(mx, my, sky[0]); px(mx + 5, my, sky[0]); px(mx, my + 5, sky[0]); px(mx + 5, my + 5, sky[0]); rect(mx + 3, my + 1, 3, 3, mix(C.moon, sky[0], 0.35));
    } else {
      var sx = WIN.x + 4 + Math.round(Math.min(1, Math.max(0, (h - 6) / 13)) * (WIN.w - 14)), sy = WIN.y + 5 + Math.round(Math.abs((h - 12.5) / 6.5) * 20);
      rect(sx, sy, 6, 6, C.sun); px(sx, sy, sky[0]); px(sx + 5, sy, sky[0]); px(sx, sy + 5, sky[0]); px(sx + 5, sy + 5, sky[0]);
      for (var c = 0; c < clouds.length; c++) { var cl = clouds[c]; var cx = WIN.x + ((cl.x + f / 20) % (WIN.w + cl.w)) - cl.w; hline(cx + 1, WIN.y + cl.y, cl.w - 2, C.cloud); hline(cx, WIN.y + cl.y + 1, cl.w, C.cloud); hline(cx, WIN.y + cl.y + 2, cl.w, C.cloudS); hline(cx + 3, WIN.y + cl.y - 1, 3, C.cloud); }
    }
    // the skyline: far row, then the landmarks
    var by = WIN.y + WIN.h - 4;
    for (var a = 0; a < FAR.length; a++) { drawBuilding(FAR[a], WIN.x, by - 2, dark, f, true); }
    for (var b = 0; b < NEAR.length; b++) { drawBuilding(NEAR[b], WIN.x, by, dark, f, false); }
    rect(WIN.x, by, WIN.w, 4, dark ? "#06071a" : mix(sky[1], "#3a4252", 0.7));                 // the river line
    if (dark) { for (var r = 0; r < WIN.w; r += 4) { if (hash(r, 1, f >> 4) % 3 === 0) { px(WIN.x + r + 1, by + 1, mix(C.winLit, "#06071a", 0.5)); } } }
    // frame, bars, sill
    rect(WIN.x - 3, WIN.y - 3, WIN.w + 6, 3, C.ink); rect(WIN.x - 3, WIN.y + WIN.h, WIN.w + 6, 3, C.ink); rect(WIN.x - 3, WIN.y, 3, WIN.h, C.ink); rect(WIN.x + WIN.w, WIN.y, 3, WIN.h, C.ink);
    rect(WIN.x + (WIN.w / 2 | 0) - 1, WIN.y, 2, WIN.h, C.ink); rect(WIN.x, WIN.y + (WIN.h * 0.42 | 0), WIN.w, 2, C.ink);
    rect(WIN.x - 6, WIN.y + WIN.h + 3, WIN.w + 12, 3, C.ink2);
  }
  function sillY() { return WIN.y + WIN.h + 3; }

  function drawDesk() {
    rect(0, DESK_Y, W, 5, C.deskTop); hline(0, DESK_Y, W, C.deskEdge);
    rect(0, DESK_Y + 5, W, H - DESK_Y - 5, C.deskFront); hline(0, DESK_Y + 5, W, C.ink); hline(0, DESK_Y + 6, W, C.ink3);
  }
  function drawNamePlate(p) {
    var name = p.name === "cole" ? "COLE" : "ILINCA", w = textWidth(name) + 8, x = p.x - (w / 2 | 0), y = DESK_Y + 10;
    rect(x, y, w, 9, C.plate); hline(x, y + 9, w, C.plateS); vline(x + w, y + 1, 9, C.plateS);
    drawText(name, x + 4, y + 2, C.ink);
  }

  /* ---------- the lamp: articulated, swings over whoever is working ---------- */
  var lamp = { base: 174, hx: 180, hy: 46, tx: 180, ty: 46, on: false, target: null };
  function lampIdle() { return { x: lamp.base + 8, y: 46 }; }
  function updateLamp(h) {
    var work = null;
    if (cole.activity === "solder") { work = { x: cole.x - 9, y: DESK_Y - 30 }; }
    else if (ilinca.activity === "write") { work = { x: ilinca.x + 7, y: DESK_Y - 30 }; }
    else if (cole.activity === "write") { work = { x: cole.x + 7, y: DESK_Y - 30 }; }
    var t = work || lampIdle();
    lamp.tx = t.x; lamp.ty = t.y; lamp.on = isDark(h) || !!work;
    lamp.hx += (lamp.tx - lamp.hx) * 0.18; lamp.hy += (lamp.ty - lamp.hy) * 0.18;
  }
  function drawLampCone() {
    if (!lamp.on) { return; }
    var hx = Math.round(lamp.hx), hy = Math.round(lamp.hy), top = hy + 7, bottom = DESK_Y + 5;
    for (var y = top; y < bottom; y++) { var t = (y - top) / (bottom - top), half = Math.round(lerp(7, 20, t)); rect(hx - half, y, half * 2, 1, C.cone); }
    rect(hx - 24, DESK_Y, 48, 5, C.cone2);
  }
  // Base and arm sit behind the figures (drawn before them); the head hangs in front (drawn after the props).
  function drawLampArm() {
    var bx = lamp.base, hx = Math.round(lamp.hx), hy = Math.round(lamp.hy), jy = 40;
    rect(bx - 6, DESK_Y - 4, 13, 3, C.lampBody); hline(bx - 5, DESK_Y - 5, 11, C.lampBody);
    limb(bx, DESK_Y - 5, bx, jy, 3, C.lampBody);
    limb(bx, jy, hx, hy, 3, C.lampBody);
    rect(bx - 2, jy - 2, 4, 4, C.lampBody);
  }
  function drawLamp() {
    var hx = Math.round(lamp.hx), hy = Math.round(lamp.hy);
    rect(hx - 2, hy - 2, 4, 4, C.lampBody);
    var sh = lamp.on ? C.lampShadeOn : C.lampShade;
    for (var r = 0; r < 7; r++) { hline(hx - 4 - r, hy + r, 8 + r * 2, sh); px(hx - 5 - r, hy + r, C.lampBody); px(hx + 4 + r, hy + r, C.lampBody); }
    hline(hx - 4, hy - 1, 8, C.lampBody); hline(hx - 11, hy + 7, 22, C.lampBody);
    if (lamp.on) { hline(hx - 8, hy + 8, 16, C.sun); }
  }

  /* ---------- props ---------- */
  function propVase(x, kind) {
    rect(x - 3, DESK_Y - 11, 7, 11, C.white); outline(x - 3, DESK_Y - 11, 7, 11, C.ink); hline(x - 4, DESK_Y - 12, 9, C.ink); hline(x - 2, DESK_Y - 7, 5, C.greyLight);
    vline(x, DESK_Y - 22, 10, C.stem); vline(x - 3, DESK_Y - 19, 7, C.stem); vline(x + 3, DESK_Y - 20, 8, C.stem);
    var p = kind === 0 ? C.petalR : kind === 1 ? C.petalW : C.petalY, ctr = kind === 1 ? C.petalY : C.ink;
    rect(x - 2, DESK_Y - 26, 5, 4, p); rect(x - 5, DESK_Y - 22, 4, 3, p); rect(x + 2, DESK_Y - 23, 4, 3, p); px(x, DESK_Y - 25, ctr); px(x - 3, DESK_Y - 21, ctr); px(x + 3, DESK_Y - 22, ctr);
  }
  function propPlant(x) {
    rect(x - 5, DESK_Y - 8, 11, 8, C.pot); hline(x - 6, DESK_Y - 9, 13, C.potS); vline(x - 4, DESK_Y - 7, 6, C.potS);
    rect(x - 6, DESK_Y - 16, 4, 6, C.leaf); rect(x + 3, DESK_Y - 18, 4, 8, C.greenL); rect(x - 2, DESK_Y - 22, 4, 12, C.green); rect(x - 1, DESK_Y - 24, 2, 2, C.greenL); px(x - 5, DESK_Y - 17, C.greenL);
  }
  function propPapers(x) {
    rect(x - 11, DESK_Y - 4, 22, 4, C.paper); outline(x - 11, DESK_Y - 4, 22, 4, C.paperLine); rect(x - 10, DESK_Y - 7, 21, 3, C.paper); outline(x - 10, DESK_Y - 7, 21, 3, C.paperLine); hline(x - 7, DESK_Y - 6, 12, C.greyLight);
  }
  function propBottle(x, y) {   // the Nutrimatic shaker; bottom at y
    rect(x - 4, y - 22, 9, 22, C.white); outline(x - 4, y - 22, 9, 22, C.ink); rect(x - 3, y - 26, 7, 4, C.red); hline(x - 2, y - 27, 5, C.redDeep);
    rect(x - 2, y - 14, 5, 8, C.greyLight); px(x, y - 10, C.red); px(x - 1, y - 11, C.red); px(x + 1, y - 11, C.red);
  }
  function propCartridge(x) {
    rect(x - 6, DESK_Y - 12, 13, 12, C.white); outline(x - 6, DESK_Y - 12, 13, 12, C.ink); rect(x - 5, DESK_Y - 15, 11, 3, C.greyLight); outline(x - 5, DESK_Y - 15, 11, 3, C.ink);
    rect(x - 2, DESK_Y - 8, 5, 4, "#c9a36a"); px(x - 1, DESK_Y - 7, C.ink); px(x + 1, DESK_Y - 7, C.ink);
  }
  function propMug(x, y, steam, f) {   // bottom at y
    rect(x - 4, y - 9, 8, 9, C.mug); hline(x - 4, y - 9, 8, C.mugS); vline(x + 5, y - 7, 5, C.mug); px(x + 4, y - 7, C.mug); px(x + 4, y - 3, C.mug);
    if (steam) { var k = (f >> 2) % 3; px(x - 1 + k, y - 12, C.smoke2); px(x + 1 - k, y - 15, C.smoke2); }
  }
  function propLaptop(x) {
    rect(x - 14, DESK_Y - 20, 28, 20, C.laptop); outline(x - 14, DESK_Y - 20, 28, 20, C.laptopS);
    rect(x - 2, DESK_Y - 12, 4, 4, C.laptopD); px(x - 1, DESK_Y - 11, C.laptop); px(x, DESK_Y - 11, C.laptop);
    hline(x - 16, DESK_Y - 1, 32, C.laptopD); hline(x - 15, DESK_Y - 2, 30, C.laptopS);
  }
  function propSolderStation(x) {
    rect(x - 8, DESK_Y - 6, 16, 6, C.ink3); outline(x - 8, DESK_Y - 6, 16, 6, C.ink); px(x - 5, DESK_Y - 4, C.red); px(x - 2, DESK_Y - 4, C.greenL); rect(x + 1, DESK_Y - 4, 4, 2, C.greyLight);
    rect(x + 5, DESK_Y - 16, 2, 10, C.grey); hline(x + 3, DESK_Y - 16, 6, C.grey);
  }
  function propPhoneOnDesk(x) { rect(x - 3, DESK_Y - 2, 7, 2, C.phone); hline(x - 2, DESK_Y - 2, 5, C.ink3); }
  function propPlane(x, y, dir) {   // a paper airplane pointing in dir (1 = right)
    var d = dir || 1;
    hline(x - 3 * d, y, 7, C.plane); hline(x - 2 * d, y - 1, 4, C.plane); px(x + 3 * d, y, C.planeS); px(x - 3 * d, y + 1, C.planeS); px(x - 2 * d, y + 1, C.planeS);
  }
  function propDS(x, y, open, f) {   // red Nintendo DS; (x, y) = centre of the hinge
    if (open) {
      rect(x - 6, y - 7, 12, 6, C.ds); outline(x - 6, y - 7, 12, 6, C.dsS); rect(x - 4, y - 6, 8, 4, C.dsScreen); if ((f >> 1) % 3 === 0) { px(x - 2 + (f % 4), y - 5, C.greenL); }
      rect(x - 6, y, 12, 4, C.ds); outline(x - 6, y, 12, 4, C.dsS); rect(x - 3, y + 1, 6, 2, C.dsScreen); px(x - 5, y + 2, C.ink); px(x + 4, y + 2, C.ink); hline(x - 6, y - 1, 12, C.dsS);
    } else { rect(x - 6, y - 2, 12, 4, C.ds); outline(x - 6, y - 2, 12, 4, C.dsS); }
  }

  /* ---------- the characters ---------- */
  // Heads: 18 wide x 22 tall. Face columns 2..15, eyes rows 11-12, nose 13-14, mouth row 17, neck rows 20-21.
  var HEAD_COLE = [
    ".....hhhhhhhh.....",
    "...hhhhhhhhhhhh...",
    "..hhhhhhhhhhhhhh..",
    ".hhhhhHhhhhhhhhhh.",
    ".hhhhhhhhhhhhhhhh.",
    "hhhhhhhhhhhhhhhhhh",
    "hhhhhssshhssshhhhh",
    "hhssssssshHssssshh",
    "hhsssssssssssssshh",
    "h.ssssssssssssss.h",
    "hsssssssssssssssSh",
    ".sssssssssssssssS.",
    ".sssssssssssssssS.",
    "..ssssssssssssss..",
    "..ssssssssssssss..",
    "..ssssssssssssss..",
    "..ssssssssssssss..",
    "...ssssssssssss...",
    "...SssssssssssS...",
    "....ssssssssss....",
    ".....SssssssS.....",
    ".......ssss......."
  ];
  var HEAD_ILINCA = [
    "......hhHhhh......",
    "....hhhhhhhhhh....",
    "...hhhhhhhhhhhh...",
    "..hhhhhhhhhhhhhh..",
    ".hhhhhhhhhhhhhhhh.",
    "hhhhhhhhhhhhhhhhhh",
    "hhhhsssssssssshhhh",
    "hhhsssssssssssshhh",
    "hhsssssssssssssshh",
    "hhsssssssssssssshh",
    "hhsssssssssssssshh",
    "hhsssssssssssssshh",
    "hhsssssssssssssshh",
    "hhsssssssssssssshh",
    "hhsssssssssssssshh",
    "hh.ssssssssssss.hh",
    "hh.ssssssssssss.hh",
    "hh..ssssssssss..hh",
    "hh..SssssssssS..hh",
    "hh...ssssssss...hh",
    "hh....SssssS....hh",
    "hh.....ssss.....hh"
  ];

  function makeCharacter(o) {
    return {
      name: o.name, x: 0, head: o.head, pal: o.pal, longHair: !!o.longHair, glasses: !!o.glasses, outfit: o.outfit, activities: o.activities,
      activity: "rest", actUntil: 0, actFrame: 0, look: { x: 0, y: 0 }, lookTarget: { x: 0, y: 0 }, turn: 0, nod: 0, bob: 0, slide: 0, hidden: false,
      mouth: "neutral", brows: null, blink: 0, nextBlink: 20 + Math.random() * 40, talking: false, gesture: false, react: null, reactUntil: 0,
      phoneOnDesk: false, hold: null
    };
  }
  var cole = makeCharacter({ name: "cole", head: HEAD_COLE, glasses: true, outfit: "henley", pal: { h: C.cHair, H: C.cHairH, s: C.cSkin, S: C.cSkinS },
    activities: ["type", "solder", "solder", "think", "coffee", "stretch", "rest", "type", "write"] });
  var ilinca = makeCharacter({ name: "ilinca", head: HEAD_ILINCA, longHair: true, outfit: "blazer", pal: { h: C.iHair, H: C.iHairH, s: C.iSkin, S: C.iSkinS },
    activities: ["type", "type", "phone", "coffee", "think", "write", "write", "stretch", "rest"] });
  var people = [cole, ilinca];
  function other(p) { return p === cole ? ilinca : cole; }
  function who(n) { return n === "cole" ? cole : ilinca; }
  function midX() { return (cole.x + ilinca.x) / 2 | 0; }

  // Arm poses: [elbowDx, elbowDy, handDx, handDy] from (x, shoulder line). A hand on the desk is at dy 36.
  function armPose(p, f) {
    var k = p.actFrame, a = p.activity, R = [20, 15, 10, 36], Lp = [-20, 15, -10, 36], t = (k >> 2) % 2, dir = other(p).x > p.x ? 1 : -1;
    if (a === "type") { Lp = [-21, 16, -13, 30 + t]; R = [21, 16, 13, 31 - t]; }
    else if (a === "write") { R = [20, 14, 6 + ((k >> 2) % 3), 35]; }
    else if (a === "solder") { Lp = [-21, 15, -11, 34]; R = [21, 12, 9, 24]; }
    else if (a === "coffee") { var up = (k % 40) >= 12 && (k % 40) < 26; R = up ? [19, 6, 5, -1] : [20, 14, 13, 34]; }
    else if (a === "think") { Lp = [-19, 10, -4, 1]; }
    else if (a === "phone") { Lp = [-18, 14, -5, 12]; R = [18, 14, 5, 12]; }
    else if (a === "ds") { Lp = [-18, 13, -7, 14 + (t ? 0 : 1)]; R = [18, 13, 7, 14 + t]; }
    else if (a === "dsAway") { Lp = [-20, 22, -10, 44]; R = [20, 22, 10, 44]; }
    else if (a === "stretch") { var s = Math.min(k, 6); Lp = [-21, 2 - s, -18, -14 - s]; R = [21, 2 - s, 18, -14 - s]; }
    else if (a === "wave") { var w = ((k >> 1) % 2) ? 3 : -2; R = [21, 4, 18 + w, -10]; }
    else if (a === "highfive") { var reach = Math.min(k * 2, 10); if (dir > 0) { R = [21, 6, 14 + reach, 4 - reach]; } else { Lp = [-21, 6, -14 - reach, 4 - reach]; } }
    else if (a === "fold") { Lp = [-18, 14, -6, 12 + t]; R = [18, 14, 6, 12 + (1 - t)]; }
    else if (a === "throw") { R = [21, 8, 24, 2]; }
    else if (a === "shake") { var sh = (k % 2) ? 2 : -1; Lp = [-16, 12, -4, 8 + sh]; R = [16, 12, 4, 8 + sh]; }
    else if (a === "drink") { R = [18, 6, 4, -2]; }
    else if (a === "offer") { if (dir > 0) { R = [21, 8, 22, 10]; } else { Lp = [-21, 8, -22, 10]; } }
    else if (a === "take") { if (dir > 0) { R = [21, 8, 22, 10]; } else { Lp = [-21, 8, -22, 10]; } }
    else if (a === "rubEye") { R = [18, 4, 4, -11]; }
    else if (a === "yawn") { R = [18, 6, 4, -3]; }
    else if (a === "pet") { if (dir > 0) { R = [21, 12, 22, 34]; } else { Lp = [-21, 12, -22, 34]; } }
    else if (a === "fan") { var fw = ((k >> 1) % 2) ? 2 : -2; R = [20, 6, 12 + fw, -4]; }
    else if (a === "fistpump") { R = [21, 2, 16, -18 + ((k >> 1) % 2) * 2]; }
    if (p.gesture) { var gg = ((f >> 2) % 2) ? 1 : -1; if (dir > 0) { R = [19, 10, 13 + gg, 6]; } else { Lp = [-19, 10, -13 - gg, 6]; } }
    if (p.react === "surprise") { Lp = [-19, 8, -14, 2]; R = [19, 8, 14, 2]; }
    if (p.react === "laugh") { Lp = [-19, 12, -8, 10]; }
    return { L: Lp, R: R };
  }

  function drawArm(p, x, sy, side, pose) {
    var skin = p.pal.s, shx = x + (side < 0 ? -15 : 15), shy = sy + 3;
    var ex = x + pose[0], ey = sy + pose[1], hx = x + pose[2], hy = sy + pose[3];
    var sleeve = p.outfit === "henley" ? C.henley : C.blazer, sleeveS = p.outfit === "henley" ? C.henleyS : C.blazerS;
    limb(shx, shy, ex, ey, 9, sleeveS); limb(ex, ey, hx, hy, 8, sleeveS);
    limb(shx, shy, ex, ey, 7, sleeve); limb(ex, ey, hx, hy, 6, sleeve);
    // cuff and hand
    var cx = Math.round(ex + (hx - ex) * 0.82), cy = Math.round(ey + (hy - ey) * 0.82);
    limb(cx, cy, hx, hy, 6, p.outfit === "henley" ? C.henleyL : C.blazerS);
    rect(hx - 3, hy - 3, 7, 7, p.pal.S); rect(hx - 2, hy - 2, 5, 5, skin); px(hx + 2, hy - 1, p.pal.S);
  }

  function drawTorso(p, x, sy) {
    if (p.outfit === "henley") {
      rect(x - 17, sy + 2, 34, DESK_Y - sy - 2, C.henley); hline(x - 15, sy, 30, C.henley); hline(x - 16, sy + 1, 32, C.henley);
      vline(x - 17, sy + 2, DESK_Y - sy - 2, C.henleyS); vline(x + 16, sy + 2, DESK_Y - sy - 2, C.henleyS);
      rect(x - 4, sy, 8, 2, p.pal.s); hline(x - 5, sy + 2, 10, C.henleyS);                     // round neck
      rect(x - 2, sy + 3, 4, 13, C.henleyL); vline(x - 2, sy + 3, 13, C.henleyS); vline(x + 1, sy + 3, 13, C.henleyS);   // placket
      px(x, sy + 6, C.white); px(x, sy + 10, C.white); px(x, sy + 14, C.white);                  // buttons
    } else {
      rect(x - 17, sy + 2, 34, DESK_Y - sy - 2, C.blazer); hline(x - 15, sy, 30, C.blazer); hline(x - 16, sy + 1, 32, C.blazer);
      var half = [6, 6, 5, 5, 4, 4, 3, 3, 2, 2, 1, 1];
      for (var i = 0; i < half.length; i++) { rect(x - half[i], sy + i, half[i] * 2, 1, C.blouse); rect(x - half[i] - 2, sy + i, 2, 1, C.blazerS); rect(x + half[i], sy + i, 2, 1, C.blazerS); }
      vline(x, sy + 10, 5, C.blazerS); px(x, sy + 17, C.greyLight); px(x, sy + 5, "#c9a36a");
      hline(x - 17, sy + 2, 4, C.blazerS); hline(x + 13, sy + 2, 4, C.blazerS);
    }
  }
  function drawLongHairBack(p, x, y) {
    var hb = p.pal.h; rect(x - 12, y + 3, 24, 31, hb); rect(x - 11, y + 1, 22, 2, hb); rect(x - 9, y, 18, 1, hb);
    hline(x - 11, y + 34, 22, hb); hline(x - 10, y + 35, 20, hb); hline(x - 8, y + 36, 16, hb);
    vline(x - 10, y + 6, 24, p.pal.H); vline(x + 9, y + 8, 22, p.pal.H); vline(x - 4, y + 2, 4, p.pal.H);
  }
  function drawLongHairFront(p, x, y) {
    var hb = p.pal.h; rect(x - 12, y + 20, 4, 14, hb); rect(x + 8, y + 20, 4, 14, hb); hline(x - 11, y + 34, 2, hb); hline(x + 9, y + 34, 2, hb);
    px(x - 10, y + 24, p.pal.H); px(x + 9, y + 23, p.pal.H); px(x - 10, y + 25, p.pal.H);
  }

  function drawFace(p, x0, y, f) {
    var x = x0 - 9 + p.turn, pal = p.pal, ink = C.ink;
    var ey = y + 11, lx = Math.round(p.look.x), ly = Math.round(p.look.y), eyes = [x + 3, x + 11], closed = p.blink > 0 || p.mouth === "laugh" || p.mouth === "yawn";
    for (var i = 0; i < 2; i++) {
      var ex = eyes[i];
      if (closed) { hline(ex, ey + 1, 4, pal.S); hline(ex + 1, ey + 1, 2, ink); continue; }
      rect(ex, ey, 4, 2, C.white);
      var pxl = Math.max(ex, Math.min(ex + 2, ex + 1 + lx)), pyl = ly > 0 ? ey + 1 : ey, ph = ly === 0 ? 2 : 1;
      rect(pxl, pyl, 2, ph, ink); px(pxl, pyl, "#3a3a3a");
      if (p.name === "ilinca") { px(i === 0 ? ex - 1 : ex + 4, ey, C.browI); }                   // a lash at the outer corner
    }
    var bc = p.name === "cole" ? C.brow : C.browI;
    if (p.brows === "up") { hline(x + 3, y + 8, 4, bc); hline(x + 11, y + 8, 4, bc); }
    else if (p.brows === "down") { hline(x + 3, y + 9, 3, bc); px(x + 6, y + 10, bc); hline(x + 12, y + 9, 3, bc); px(x + 11, y + 10, bc); }
    else if (p.brows === "sad") { px(x + 3, y + 10, bc); hline(x + 4, y + 9, 3, bc); hline(x + 11, y + 9, 3, bc); px(x + 14, y + 10, bc); }
    else if (!p.glasses) { hline(x + 3, y + 9, 4, bc); hline(x + 11, y + 9, 4, bc); }
    px(x + 8, y + 14, pal.S); px(x + 9, y + 14, pal.S); px(x + 9, y + 13, pal.S);                  // nose
    if (p.name === "ilinca") { px(x + 3, y + 14, C.blush); px(x + 14, y + 14, C.blush); }
    if (p.glasses) {
      hline(x + 2, y + 9, 14, C.frames); px(x + 1, y + 9, C.frames); px(x + 16, y + 9, C.frames);
      vline(x + 2, y + 10, 4, C.frames); vline(x + 7, y + 10, 4, C.frames); vline(x + 10, y + 10, 4, C.frames); vline(x + 15, y + 10, 4, C.frames);
      hline(x + 8, y + 10, 2, C.frames); hline(x + 3, y + 13, 4, C.rim); hline(x + 11, y + 13, 4, C.rim);
      if (p.brows === "up") { hline(x + 3, y + 7, 4, bc); hline(x + 11, y + 7, 4, bc); }
    }
    var my = y + 17, m = p.mouth, lipc = p.name === "ilinca" ? C.lips : C.mouth;
    if (m === "talk") { m = (f % 4 < 2) ? "open" : "neutral"; }
    if (m === "smile") { px(x + 5, my - 1, lipc); hline(x + 6, my, 6, lipc); px(x + 12, my - 1, lipc); if (p.name === "ilinca") { hline(x + 7, my - 1, 4, C.lipsL); } }
    else if (m === "laugh") { px(x + 4, my - 1, lipc); hline(x + 5, my, 8, lipc); hline(x + 5, my + 1, 8, C.teeth); hline(x + 6, my + 2, 6, C.mouth); px(x + 13, my - 1, lipc); }
    else if (m === "open") { rect(x + 7, my, 4, 3, C.mouth); hline(x + 7, my, 4, C.teeth); }
    else if (m === "o") { rect(x + 7, my, 3, 3, C.mouth); }
    else if (m === "yawn") { rect(x + 6, my - 1, 6, 5, C.mouth); hline(x + 7, my - 1, 4, C.teeth); }
    else if (m === "frown") { px(x + 5, my + 1, lipc); hline(x + 6, my, 6, lipc); px(x + 12, my + 1, lipc); }
    else if (m === "flat") { hline(x + 5, my, 8, lipc); }
    else if (p.name === "ilinca") { hline(x + 7, my, 4, lipc); px(x + 6, my - 1, lipc); px(x + 11, my - 1, lipc); hline(x + 8, my - 1, 2, C.lipsL); }   // a soft resting smile
    else { hline(x + 6, my, 6, lipc); }
  }

  function drawCharacter(p, f) {
    if (p.hidden) { return; }
    var x = p.x + Math.round(p.slide), y = HEAD_Y + p.bob + p.nod, a = p.activity;
    if (a === "type" || a === "write" || a === "solder" || a === "phone" || a === "ds") { y += 1; }
    var sy = y + 22, pose = armPose(p, f);
    if (p.longHair) { drawLongHairBack(p, x, y - 1); }
    drawTorso(p, x, sy);
    drawArm(p, x, sy, -1, pose.L); drawArm(p, x, sy, 1, pose.R);
    sprite(p.head, x - 9, y, p.pal);
    if (p.longHair) { drawLongHairFront(p, x, y); }
    if (p.longHair) { vline(x, y, 4, mix(p.pal.h, C.ink, 0.35)); }   // the parting
    drawFace(p, x, y, f);
    // things in hand
    var hx = x + pose.R[2], hy = sy + pose.R[3], lhx = x + pose.L[2], lhy = sy + pose.L[3];
    if (a === "solder") {
      rect(x - 16, DESK_Y - 9, 14, 6, C.board); outline(x - 16, DESK_Y - 9, 14, 6, C.boardS); px(x - 13, DESK_Y - 7, C.copper); px(x - 9, DESK_Y - 7, C.copper); px(x - 5, DESK_Y - 7, C.copper); hline(x - 12, DESK_Y - 5, 6, C.copper);
      rect(hx - 4, hy - 1, 6, 3, C.red); var tipX = x - 6, tipY = DESK_Y - 8; limb(hx - 5, hy + 1, tipX, tipY, 1, C.iron);
      px(tipX, tipY, (f % 6 < 3) ? C.ironHot : C.iron); var sm = (f >> 1) % 10; px(tipX + (sm % 2), tipY - 2 - sm, sm < 5 ? C.smoke : C.smoke2);
      if (f % 23 === 0) { px(tipX - 1, tipY - 1, C.sun); px(tipX + 1, tipY - 2, C.sun); }
    } else if (a === "coffee") {
      var up = (p.actFrame % 40) >= 12 && (p.actFrame % 40) < 26;
      if (up) { rect(hx - 3, hy - 7, 7, 7, C.mug); hline(hx - 3, hy - 7, 7, C.mugS); vline(hx + 4, hy - 6, 4, C.mug); px(hx + 5, hy - 6, C.mug); px(hx + 5, hy - 3, C.mug); }
      else { propMug(x + 14, DESK_Y, true, f); }
    } else if (a === "phone") {
      rect(x - 4, sy + 8, 8, 12, C.phone); rect(x - 3, sy + 9, 6, 10, (f % 24 < 20) ? C.phoneScreen : C.white); px(x, sy + 18, C.ink3);
    } else if (a === "ds") { propDS(x, sy + 11, true, f); }
    else if (a === "write") {
      rect(x - 2, DESK_Y - 4, 18, 4, C.paper); outline(x - 2, DESK_Y - 4, 18, 4, C.paperLine); hline(x, DESK_Y - 3, 8, C.greyLight); px(hx + 2, hy - 4, C.ink); px(hx + 2, hy - 5, C.ink); px(hx + 3, hy - 6, C.ink);
    } else if (a === "type") { propLaptop(x); }
    else if (a === "fold") { rect(x - 5, sy + 9, 10, 4, C.paper); outline(x - 5, sy + 9, 10, 4, C.paperS || C.paperLine); }
    else if (a === "shake" || a === "drink" || a === "offer") { var bx = a === "shake" ? x : hx, by = a === "shake" ? sy + 14 : hy + 4; propBottle(bx, by); }
    else if (a === "take" && p.hold === "bottle") { propBottle(other(p).x > p.x ? hx : lhx, (other(p).x > p.x ? hy : lhy) + 4); }
    else if (a === "rubEye") { /* hand already at the eye */ }
    if (p.name === "cole" && a === "coffee" && !up) { /* mug drawn */ }
  }

  /* ---------- desk set per visit ---------- */
  var SETS = [
    ["vase0", "plant", "papers", "mug"], ["plant", "bottle", "vase1", "cartridge"], ["bottle", "vase2", "plant", "mug"],
    ["vase1", "papers", "bottle", "cartridge"], ["papers", "plant", "vase0", "bottle"], ["plant", "cartridge", "papers", "mug"], ["vase2", "papers", "plant", "bottle"]
  ];
  var setIndex = (function () {
    try { var n = parseInt(localStorage.getItem("nutrimatic-desk-visit") || "-1", 10); n = isNaN(n) ? Math.floor(Math.random() * SETS.length) : n + 1; localStorage.setItem("nutrimatic-desk-visit", String(n)); return n % SETS.length; }
    catch (e) { return Math.floor(Math.random() * SETS.length); }
  })();
  var extras = [];   // things left on the desk by scenarios: {kind, x}
  function drawProps(f) {
    var set = SETS[setIndex];
    for (var i = 0; i < L.slots.length && i < set.length; i++) {
      var k = set[i], x = L.slots[i];
      if (k === "plant") { propPlant(x); } else if (k === "papers") { propPapers(x); } else if (k === "bottle") { propBottle(x, DESK_Y); }
      else if (k === "cartridge") { propCartridge(x); } else if (k === "mug") { propMug(x, DESK_Y, false, f); } else if (k.indexOf("vase") === 0) { propVase(x, +k[4]); }
    }
    if (cole.activity === "solder") { propSolderStation(cole.x - 34); }
    if (ilinca.phoneOnDesk && !ilinca.hidden) { propPhoneOnDesk(ilinca.x - 22); }
    for (var e = 0; e < extras.length; e++) { var ex = extras[e]; if (ex.kind === "plane") { propPlane(ex.x, DESK_Y - 2, ex.dir); } else if (ex.kind === "bottle") { propBottle(ex.x, DESK_Y); } else if (ex.kind === "mug") { propMug(ex.x, DESK_Y, ex.steam, f); } }
  }

  /* ---------- conversation without bubbles: turn, talk, gesture, nod ---------- */
  var EXCHANGES = [
    [["cole", 2.2], ["ilinca", 1.6], ["cole", 1.2]], [["ilinca", 1.8], ["cole", 0.9], ["ilinca", 1.6]], [["cole", 1.9], ["ilinca", 2.0]],
    [["ilinca", 1.0], ["cole", 0.9]], [["ilinca", 2.0], ["cole", 1.7], ["ilinca", 1.3]], [["cole", 2.3], ["ilinca", 1.5]]
  ];
  var convo = null, nextConvoAt = 9 * FPS, saidHello = false;
  function startConvo(lines) { convo = { lines: lines, i: 0, until: 0 }; }
  function stepConvo(f) {
    if (!convo) {
      if (f >= nextConvoAt && !scenario) { startConvo(EXCHANGES[(Math.random() * EXCHANGES.length) | 0]); nextConvoAt = f + (26 + Math.random() * 30) * FPS; }
      return;
    }
    if (f >= convo.until) {
      people.forEach(function (p) { p.talking = false; p.gesture = false; if (p.mouth === "talk") { p.mouth = "neutral"; } });
      if (convo.i >= convo.lines.length) { convo = null; people.forEach(function (p) { p.turn = 0; p.mouth = Math.random() < 0.6 ? "smile" : "neutral"; p.smileUntil = f + 3 * FPS; }); return; }
      var line = convo.lines[convo.i], sp = who(line[0]), ls = other(sp);
      sp.talking = true; sp.mouth = "talk"; sp.gesture = Math.random() < 0.7;
      sp.turn = ls.x < sp.x ? -1 : 1; ls.turn = sp.x < ls.x ? -1 : 1;
      sp.lookTarget = { x: sp.turn, y: 0 }; ls.lookTarget = { x: ls.turn, y: 0 };
      ls.nodAt = f + Math.round(line[1] * FPS * 0.6);
      convo.until = f + Math.round(line[1] * FPS); convo.i++;
    }
  }

  /* ---------- activities ---------- */
  var frame = 0;
  function setActivity(p, a, seconds) {
    p.activity = a; p.actFrame = 0; p.actUntil = frame + Math.round(seconds * FPS);
    p.brows = a === "think" ? "down" : (p.brows === "down" ? null : p.brows);
    if (p === ilinca) { p.phoneOnDesk = a !== "phone"; }
  }
  function nextActivity(p) {
    var a = p.activities[(Math.random() * p.activities.length) | 0];
    if (a === p.activity) { a = p.activities[(Math.random() * p.activities.length) | 0]; }
    var secs = a === "stretch" ? 2.5 : a === "coffee" ? 10 : a === "rest" ? 4 : 12 + Math.random() * 14;
    setActivity(p, a, secs);
  }
  function faceOf(p, o) { if (o.mouth !== undefined) { p.mouth = o.mouth; } if (o.brows !== undefined) { p.brows = o.brows; } if (o.look) { p.lookTarget = o.look; } if (o.turn !== undefined) { p.turn = o.turn; } }
  function lookAtEachOther() { cole.turn = ilinca.x > cole.x ? 1 : -1; ilinca.turn = -cole.turn; cole.lookTarget = { x: cole.turn, y: 0 }; ilinca.lookTarget = { x: ilinca.turn, y: 0 }; }
  function lookAt(p, x, y) { p.lookTarget = aimAt(p, x, y); p.turn = p.lookTarget.x; }

  /* ---------- scenarios: little scripted scenes ---------- */
  var scenario = null, nextScenarioAt = 22 * FPS, actors = {};
  function startScenario(name) {
    var sc = SCENARIOS[name]; if (!sc || (sc.when && !sc.when())) { return false; }
    scenario = { name: name, t0: frame, steps: sc.steps.map(function (s) { return { at: s[0], fn: s[1], done: false }; }), dur: sc.dur, update: sc.update, drawBack: sc.drawBack, drawFront: sc.drawFront, end: sc.end };
    actors = {}; if (sc.setup) { sc.setup(); }
    people.forEach(function (p) { p.actUntil = frame + 1e6; p.gesture = false; }); convo = null;
    return true;
  }
  function stepScenario(f) {
    if (!scenario) { return; }
    var t = (f - scenario.t0) / FPS;
    scenario.steps.forEach(function (s) { if (!s.done && t >= s.at) { s.done = true; s.fn(t); } });
    if (scenario.update) { scenario.update(t, f); }
    if (t >= scenario.dur) { if (scenario.end) { scenario.end(); } scenario = null; people.forEach(function (p) { p.turn = 0; p.brows = p.activity === "think" ? "down" : null; p.mouth = "neutral"; p.hold = null; nextActivity(p); }); nextScenarioAt = f + (45 + Math.random() * 35) * FPS; }
  }
  function neutral(p) { p.mouth = "neutral"; p.brows = null; p.turn = 0; p.lookTarget = { x: 0, y: 1 }; }

  var SCENARIOS = {
    // Cole sneaks a game on a red DS; Ilinca notices; he puts it away.
    ds: {
      dur: 13,
      steps: [
        [0, function () { setActivity(cole, "ds", 99); faceOf(cole, { mouth: "smile", look: { x: 0, y: 1 }, turn: 0 }); }],
        [6.5, function () { faceOf(ilinca, { brows: "down", mouth: "flat" }); lookAt(ilinca, cole.x, HEAD_Y + 12); }],
        [8.0, function () { faceOf(cole, { brows: "up", mouth: "o" }); lookAt(cole, ilinca.x, HEAD_Y + 12); }],
        [9.0, function () { faceOf(cole, { brows: "sad", mouth: "frown", look: { x: 0, y: 1 }, turn: 0 }); setActivity(cole, "dsAway", 99); }],
        [10.6, function () { setActivity(cole, "type", 99); faceOf(cole, { brows: null, mouth: "neutral" }); faceOf(ilinca, { brows: null, mouth: "smile" }); ilinca.turn = 0; ilinca.lookTarget = { x: 0, y: 1 }; }]
      ]
    },
    // Something worked: a high five across the gap.
    highfive: {
      dur: 4.2,
      steps: [
        [0, function () { lookAtEachOther(); cole.mouth = "smile"; ilinca.mouth = "smile"; }],
        [0.5, function () { setActivity(cole, "highfive", 99); setActivity(ilinca, "highfive", 99); }],
        [1.4, function () { cole.mouth = "laugh"; ilinca.mouth = "laugh"; actors.clap = frame; }],
        [2.6, function () { setActivity(cole, "rest", 99); setActivity(ilinca, "rest", 99); cole.mouth = "smile"; ilinca.mouth = "smile"; }]
      ],
      drawFront: function (t, f) { if (actors.clap && f - actors.clap < 6) { var mx = midX(), my = HEAD_Y + 18; px(mx, my - 3, C.sun); px(mx - 3, my, C.sun); px(mx + 3, my, C.sun); px(mx, my + 3, C.sun); px(mx - 2, my - 2, C.white); px(mx + 2, my + 2, C.white); } }
    },
    // Cole folds a paper airplane and throws it; it lands in Ilinca's space and stays on the desk.
    airplane: {
      dur: 7.5,
      steps: [
        [0, function () { setActivity(cole, "fold", 99); faceOf(cole, { look: { x: 0, y: 1 }, turn: 0, mouth: "smile" }); }],
        [2.4, function () { setActivity(cole, "throw", 99); lookAt(cole, ilinca.x, HEAD_Y + 8); actors.plane = { t0: frame, x: cole.x + 24, y: HEAD_Y + 30 }; }],
        [3.4, function () { faceOf(ilinca, { brows: "down", mouth: "flat" }); lookAt(ilinca, cole.x, HEAD_Y + 12); setActivity(ilinca, "rest", 99); }],
        [3.6, function () { faceOf(cole, { brows: "up", mouth: "smile" }); setActivity(cole, "rest", 99); }],
        [5.5, function () { faceOf(ilinca, { brows: null, mouth: "smile" }); }]
      ],
      update: function (t, f) {
        var pl = actors.plane; if (!pl || pl.landed) { return; }
        var k = (f - pl.t0) / 10, dir = ilinca.x > cole.x ? 1 : -1;
        pl.x = cole.x + 24 * dir + (ilinca.x - cole.x - 20 * dir) * Math.min(1, k); pl.y = HEAD_Y + 30 - Math.sin(Math.min(1, k) * Math.PI) * 22 + Math.min(1, k) * 26;
        if (k >= 1) { pl.landed = true; extras.push({ kind: "plane", x: ilinca.x - 24 * dir, dir: dir }); }
      },
      drawFront: function (t, f) { var pl = actors.plane; if (pl && !pl.landed) { propPlane(Math.round(pl.x), Math.round(pl.y), ilinca.x > cole.x ? 1 : -1); } }
    },
    // A pigeon lands on the sill, pecks about, and leaves. Both watch it.
    pigeon: {
      dur: 11,
      setup: function () { actors.bird = { x: WIN.x + WIN.w - 8, y: WIN.y + 16, state: "land" }; },
      steps: [
        [1.2, function () { people.forEach(function (p) { lookAt(p, WIN.x + WIN.w / 2, sillY()); }); }],
        [8.4, function () { actors.bird.state = "fly"; }],
        [9.6, function () { people.forEach(function (p) { neutral(p); }); }]
      ],
      update: function (t, f) {
        var b = actors.bird, target = sillY() - 6;
        if (b.state === "land") { if (b.y < target) { b.y += 2; b.x -= 1; } else { b.y = target; b.state = "walk"; b.t0 = f; } }
        else if (b.state === "walk") { var k = f - b.t0; if (k % 24 < 12) { b.x += (k % 2) ? -1 : 0; } b.peck = (k % 30) >= 22; }
        else if (b.state === "fly") { b.y -= 3; b.x += 2; }
      },
      drawFront: function (t, f) {
        var b = actors.bird, x = Math.round(b.x), y = Math.round(b.y), flap = b.state !== "walk" && (f % 4 < 2);
        rect(x - 3, y, 7, 4, C.pigeon); rect(x - 4, y + 1, 2, 2, C.pigeonD); px(x + 4, y - 1 + (b.peck ? 2 : 0), C.pigeonL); rect(x + 3, y - 2 + (b.peck ? 2 : 0), 3, 3, C.pigeonL); px(x + 6, y - 1 + (b.peck ? 2 : 0), C.sun);
        if (flap) { hline(x - 2, y - 2, 5, C.pigeonL); } else { hline(x - 2, y + 1, 4, C.pigeonL); }
        if (b.state === "walk") { px(x - 1, y + 4, C.sun); px(x + 1, y + 4, C.sun); }
      }
    },
    // A cat walks the length of the desk, sits for a scratch from Ilinca, moves on.
    cat: {
      dur: 18,
      setup: function () { actors.cat = { x: -16, state: "walk", dir: 1 }; },
      steps: [
        [2.0, function () { people.forEach(function (p) { lookAt(p, actors.cat.x, DESK_Y - 4); p.mouth = "smile"; }); }],
        [9.0, function () { setActivity(ilinca, "pet", 99); }],
        [12.5, function () { setActivity(ilinca, "rest", 99); actors.cat.state = "walk"; }],
        [15.5, function () { people.forEach(function (p) { neutral(p); }); }]
      ],
      update: function (t, f) {
        var c = actors.cat, sitX = ilinca.x - 30;
        if (c.state === "walk") { c.x += 3; if (c.x >= sitX && t < 9) { c.state = "sit"; c.x = sitX; } }
        if (t >= 2 && t < 15) { people.forEach(function (p) { p.lookTarget = aimAt(p, c.x, DESK_Y - 4); }); }
      },
      drawFront: function (t, f) {
        var c = actors.cat, x = Math.round(c.x), y = DESK_Y - 1;
        if (c.state === "sit") {
          rect(x - 3, y - 8, 7, 8, C.cat); rect(x - 2, y - 11, 6, 4, C.cat); px(x - 2, y - 12, C.cat); px(x + 3, y - 12, C.cat);
          px(x - 1, y - 10, (f % 40 < 36) ? C.catEye : C.cat); px(x + 2, y - 10, (f % 40 < 36) ? C.catEye : C.cat); limb(x + 4, y - 2, x + 7 + ((f >> 3) % 2), y - 6, 1, C.cat);
        } else {
          var s = (f >> 1) % 2;
          rect(x - 6, y - 6, 12, 4, C.cat); rect(x + 5, y - 8, 5, 4, C.cat); px(x + 6, y - 9, C.cat); px(x + 9, y - 9, C.cat); px(x + 7, y - 7, C.catEye);
          px(x - 5, y - 2, C.cat); px(x - 2 + s, y - 2, C.cat); px(x + 2 - s, y - 2, C.cat); px(x + 5, y - 2, C.cat); limb(x - 6, y - 5, x - 9, y - 10 + s, 1, C.cat);
        }
      }
    },
    // Ilinca rolls off for coffee and comes back with two mugs.
    coffee: {
      dur: 15,
      when: function () { return ilinca.activity !== "coffee" && cole.activity !== "coffee"; },
      steps: [
        [0, function () { setActivity(ilinca, "rest", 99); lookAt(ilinca, cole.x, HEAD_Y + 12); ilinca.mouth = "smile"; }],
        [0.8, function () { lookAt(cole, ilinca.x, HEAD_Y + 12); cole.nodAt = frame + 2; cole.mouth = "smile"; }],
        [1.6, function () { actors.away = { dir: ilinca.x > cole.x ? 1 : -1, phase: "out" }; }],
        [8.5, function () { actors.away.phase = "in"; ilinca.hold = "mugs"; }],
        [11.5, function () { extras.push({ kind: "mug", x: cole.x + 14, steam: true }); ilinca.hold = null; setActivity(cole, "coffee", 99); setActivity(ilinca, "coffee", 99); cole.mouth = "smile"; neutral(cole); cole.mouth = "smile"; }]
      ],
      update: function (t, f) {
        var a = actors.away; if (!a) { return; }
        if (a.phase === "out") { if (Math.abs(ilinca.slide) < 90) { ilinca.slide += 6 * a.dir; } if (Math.abs(ilinca.slide) >= 84) { ilinca.hidden = true; } }
        else if (a.phase === "in") { ilinca.hidden = false; ilinca.slide -= 6 * a.dir; if (a.dir * ilinca.slide <= 0) { ilinca.slide = 0; a.phase = "home"; } }
      },
      drawFront: function (t, f) { if (ilinca.hold === "mugs" && !ilinca.hidden) { var x = ilinca.x + Math.round(ilinca.slide), sy = HEAD_Y + 22; propMug(x - 8, sy + 30, true, f); propMug(x + 10, sy + 30, true, f); } },
      end: function () { ilinca.slide = 0; ilinca.hidden = false; ilinca.hold = null; extras = extras.filter(function (e) { return e.kind !== "mug"; }); }
    },
    // Shake break: Cole mixes a bottle, drinks, passes it over.
    shake: {
      dur: 12,
      steps: [
        [0, function () { setActivity(cole, "shake", 99); faceOf(cole, { mouth: "smile", look: { x: 0, y: 0 }, turn: 0 }); }],
        [2.6, function () { setActivity(cole, "drink", 99); cole.mouth = "o"; cole.lookTarget = { x: 0, y: -1 }; }],
        [4.6, function () { lookAt(ilinca, cole.x, HEAD_Y + 12); ilinca.mouth = "smile"; setActivity(ilinca, "take", 99); }],
        [5.2, function () { setActivity(cole, "offer", 99); lookAt(cole, ilinca.x, HEAD_Y + 12); cole.mouth = "smile"; }],
        [6.6, function () { ilinca.hold = "bottle"; setActivity(cole, "rest", 99); }],
        [7.4, function () { setActivity(ilinca, "drink", 99); ilinca.mouth = "o"; ilinca.turn = 0; ilinca.lookTarget = { x: 0, y: -1 }; }],
        [9.6, function () { setActivity(ilinca, "rest", 99); ilinca.mouth = "smile"; ilinca.nodAt = frame + 1; ilinca.hold = null; extras.push({ kind: "bottle", x: midX() }); }]
      ],
      end: function () { extras = extras.filter(function (e) { return e.kind !== "bottle"; }); }
    },
    // Late: a yawn passes between them.
    latenight: {
      dur: 7, when: function () { return isDark(hourNow()); },
      steps: [
        [0, function () { setActivity(cole, "yawn", 99); cole.mouth = "yawn"; cole.lookTarget = { x: 0, y: -1 }; }],
        [1.8, function () { setActivity(cole, "rubEye", 99); cole.mouth = "neutral"; }],
        [2.4, function () { lookAt(ilinca, cole.x, HEAD_Y + 12); }],
        [3.2, function () { setActivity(ilinca, "yawn", 99); ilinca.mouth = "yawn"; ilinca.turn = 0; ilinca.lookTarget = { x: 0, y: -1 }; }],
        [5.0, function () { setActivity(ilinca, "stretch", 99); ilinca.mouth = "neutral"; setActivity(cole, "rest", 99); lookAt(cole, ilinca.x, HEAD_Y + 12); cole.mouth = "smile"; }]
      ]
    },
    // A bigger spark while soldering: a puff of smoke, a startle, a hand fanning the air, then a laugh.
    spark: {
      dur: 6.5, when: function () { return cole.activity === "solder"; },
      steps: [
        [0, function () { actors.puff = { t0: frame }; }],
        [0.25, function () { faceOf(cole, { brows: "up", mouth: "o" }); cole.bob = -2; setActivity(cole, "fan", 99); }],
        [0.8, function () { lookAt(ilinca, cole.x, HEAD_Y + 12); faceOf(ilinca, { brows: "down", mouth: "flat" }); }],
        [2.6, function () { lookAt(cole, ilinca.x, HEAD_Y + 12); faceOf(cole, { brows: "up", mouth: "smile" }); cole.bob = 0; }],
        [3.6, function () { faceOf(ilinca, { brows: null, mouth: "laugh" }); faceOf(cole, { brows: null, mouth: "laugh" }); }],
        [5.2, function () { setActivity(cole, "solder", 99); cole.mouth = "neutral"; ilinca.mouth = "smile"; ilinca.turn = 0; ilinca.lookTarget = { x: 0, y: 1 }; }]
      ],
      drawFront: function (t, f) {
        var pf = actors.puff; if (!pf) { return; }
        var k = f - pf.t0, cx = cole.x - 6, cy = DESK_Y - 10;
        if (k < 3) { px(cx, cy - 2, C.sun); px(cx - 2, cy, C.sun); px(cx + 2, cy - 1, C.sun); px(cx + 1, cy - 4, C.white); }
        if (k < 30) { var col = k < 14 ? C.smoke : C.smoke2, r = 2 + (k >> 2); for (var i = 0; i < 4; i++) { var ox = [-3, 2, -1, 4][i] * (1 + k / 12), oy = -k * 1.2 - [0, 3, 6, 2][i]; rect(cx + Math.round(ox) - r / 2, cy + Math.round(oy) - r / 2, r, r, col); } }
      }
    },
    // The phone buzzes; good news; a fist pump.
    call: {
      dur: 11,
      when: function () { return ilinca.activity !== "phone"; },
      steps: [
        [0, function () { actors.buzz = { t0: frame }; }],
        [1.4, function () { setActivity(ilinca, "phone", 99); actors.buzz = null; ilinca.phoneOnDesk = false; faceOf(ilinca, { mouth: "talk", look: { x: 0, y: 0 }, turn: 0 }); }],
        [5.6, function () { ilinca.mouth = "smile"; ilinca.nodAt = frame + 1; }],
        [7.0, function () { setActivity(ilinca, "rest", 99); lookAt(ilinca, cole.x, HEAD_Y + 12); ilinca.gesture = true; ilinca.mouth = "talk"; lookAt(cole, ilinca.x, HEAD_Y + 12); }],
        [8.6, function () { ilinca.gesture = false; ilinca.mouth = "laugh"; setActivity(cole, "fistpump", 99); cole.mouth = "laugh"; }],
        [10.2, function () { setActivity(cole, "rest", 99); cole.mouth = "smile"; ilinca.mouth = "smile"; }]
      ],
      drawFront: function (t, f) { var b = actors.buzz; if (b && ilinca.phoneOnDesk) { var x = ilinca.x - 22 + ((f % 2) ? 1 : -1); rect(x - 3, DESK_Y - 3, 7, 2, C.phone); px(x - 5, DESK_Y - 5, C.greyLight); px(x + 5, DESK_Y - 5, C.greyLight); px(x - 6, DESK_Y - 8, C.greyLight); px(x + 6, DESK_Y - 8, C.greyLight); } }
    }
  };
  var SCENARIO_NAMES = Object.keys(SCENARIOS);
  function pickScenario() {
    var order = SCENARIO_NAMES.slice().sort(function () { return Math.random() - 0.5; });
    for (var i = 0; i < order.length; i++) { if (startScenario(order[i])) { return order[i]; } }
    return null;
  }

  /* ---------- pointer ---------- */
  var pointer = { x: 0, y: 0, at: -1e9, inside: false };
  function toScene(cx, cy) {
    var r = canvas.getBoundingClientRect();
    return { x: (cx - r.left) / r.width * W, y: (cy - r.top) / r.height * H, near: cx > r.left - r.width * 0.5 && cx < r.right + r.width * 0.5 && cy > r.top - r.height && cy < r.bottom + r.height };
  }
  window.addEventListener("pointermove", function (e) {
    var s = toScene(e.clientX, e.clientY); if (!s.near) { return; }
    pointer.x = s.x; pointer.y = s.y; pointer.at = Date.now(); pointer.inside = s.x >= 0 && s.x <= W && s.y >= 0 && s.y <= H;
  }, { passive: true });
  canvas.addEventListener("pointerdown", function (e) {
    var s = toScene(e.clientX, e.clientY);
    pointer.x = s.x; pointer.y = s.y; pointer.at = Date.now() + 1500; pointer.inside = true;
    var target = null;
    for (var i = 0; i < people.length; i++) { if (!people[i].hidden && Math.abs(s.x - people[i].x) < 24 && s.y > HEAD_Y - 8 && s.y < DESK_Y + 8) { target = people[i]; } }
    if (target) { react(target); } else { people.forEach(function (p) { p.lookTarget = aimAt(p, s.x, s.y); }); }
  });
  function aimAt(p, x, y) { var dx = x - p.x, dy = y - (HEAD_Y + 12); return { x: Math.abs(dx) < 10 ? 0 : (dx < 0 ? -1 : 1), y: dy < -16 ? -1 : (dy > 20 ? 1 : 0) }; }

  var REACTIONS = ["wave", "surprise", "laugh", "wave"];
  function react(p) {
    if (scenario) { return; }
    var now = frame;
    p.reactCount = (p.reactUntil > now - FPS * 4) ? (p.reactCount || 0) + 1 : 1;
    var kind = REACTIONS[(Math.random() * REACTIONS.length) | 0];
    if (p.reactCount >= 4) { kind = "enough"; }
    p.react = kind; p.reactUntil = now + Math.round((kind === "enough" ? 2.2 : 1.9) * FPS);
    p.mouth = kind === "laugh" ? "laugh" : kind === "surprise" ? "o" : kind === "enough" ? "flat" : "smile";
    p.brows = kind === "surprise" ? "up" : kind === "enough" ? "down" : null;
    p.turn = 0; p.lookTarget = { x: 0, y: 0 };
    if (kind === "wave") { setActivity(p, "wave", 1.9); }
    if (kind === "surprise") { p.bob = -2; }
    var o = other(p); o.lookTarget = { x: p.x < o.x ? -1 : 1, y: 0 }; o.turn = p.x < o.x ? -1 : 1; o.turnUntil = now + 2 * FPS;
  }

  /* ---------- the frame loop ---------- */
  var running = false, visible = true, lastTick = 0;
  function tick(now) {
    if (!running) { return; }
    requestAnimationFrame(tick);
    if (now - lastTick < 1000 / FPS) { return; }
    lastTick = now; frame++; update(frame); render(frame);
  }
  function update(f) {
    var h = hourNow(), pointerActive = (Date.now() - pointer.at) < 2500;
    for (var i = 0; i < people.length; i++) {
      var p = people[i];
      if (p.react && f >= p.reactUntil) { p.react = null; p.mouth = "neutral"; p.brows = p.activity === "think" ? "down" : null; p.bob = 0; }
      if (p.turnUntil && f >= p.turnUntil && !convo && !scenario) { p.turn = 0; p.turnUntil = 0; }
      if (p.smileUntil && f >= p.smileUntil) { if (p.mouth === "smile") { p.mouth = "neutral"; } p.smileUntil = 0; }
      p.actFrame++;
      if (f >= p.actUntil && !p.react && !scenario) { nextActivity(p); }
      if (p.nodAt && f >= p.nodAt) { var k = f - p.nodAt; p.nod = (k < 10) ? [0, 1, 2, 2, 1, 0, 1, 2, 2, 1][k] : 0; if (k >= 10) { p.nodAt = 0; p.nod = 0; } }
      if (pointerActive && !scenario) { p.lookTarget = aimAt(p, pointer.x, pointer.y); if (!convo && !p.react) { p.turn = p.lookTarget.x; } }
      else if (!convo && !p.react && !scenario) {
        var a = p.activity; p.turn = 0;
        if (a === "type" || a === "write" || a === "solder" || a === "phone") { p.lookTarget = { x: 0, y: 1 }; }
        else if (a === "think") { p.lookTarget = { x: (f >> 5) % 2 ? -1 : 1, y: -1 }; }
        else if (a === "coffee") { p.lookTarget = { x: 0, y: 0 }; }
        else { p.lookTarget = { x: ((f >> 4) + i) % 3 - 1, y: 0 }; }
      }
      p.look.x += (p.lookTarget.x - p.look.x) * 0.6; p.look.y += (p.lookTarget.y - p.look.y) * 0.6;
      if (p.blink > 0) { p.blink--; } else if (--p.nextBlink <= 0) { p.blink = 2; p.nextBlink = 24 + Math.random() * 48; }
      if (!p.react && !(scenario && scenario.name === "spark")) { p.bob = ((f + i * 7) % 48) < 24 ? 0 : 1; }
      var o = people[1 - i];
      if (o.react === "laugh" && !p.react && f % 5 === 0) { p.mouth = "smile"; p.smileUntil = f + 2 * FPS; }
    }
    if (pointer.inside && pointerActive && !saidHello && !convo && !scenario && f > 4 * FPS) {
      saidHello = true; startConvo([["cole", 1.2], ["ilinca", 1.4]]);
      setTimeout(function () { if (!scenario) { setActivity(cole, "wave", 2.4); setActivity(ilinca, "wave", 2.4); } }, 2600);
    }
    if (!scenario && !convo && f >= nextScenarioAt && !pointerActive) { if (!pickScenario()) { nextScenarioAt = f + 15 * FPS; } }
    stepScenario(f);
    stepConvo(f);
    updateLamp(h);
  }

  function render(f) {
    var h = hourNow(), t = scenario ? (f - scenario.t0) / FPS : 0;
    drawWall(h); drawWindow(h, f);
    drawLampArm();
    if (scenario && scenario.drawBack) { scenario.drawBack(t, f); }
    for (var i = 0; i < people.length; i++) { drawCharacter(people[i], f); }
    drawDesk();
    drawProps(f);
    drawLampCone(); drawLamp();
    people.forEach(drawNamePlate);
    if (scenario && scenario.drawFront) { scenario.drawFront(t, f); }
    blit();
  }
  function blit() { ctx.imageSmoothingEnabled = false; ctx.clearRect(0, 0, canvas.width, canvas.height); ctx.drawImage(off, 0, 0, canvas.width, canvas.height); }

  /* ---------- layout + sizing ---------- */
  function applyLayout(name) {
    if (name === layoutName) { return; }
    layoutName = name; L = LAYOUTS[name]; W = L.W; H = L.H; WIN = L.win; off.width = W; off.height = H;
    cole.x = L.cole; ilinca.x = L.ilinca; lamp.base = L.lamp; var idle = lampIdle(); lamp.hx = lamp.tx = idle.x; lamp.hy = lamp.ty = idle.y;
    makeStars(); extras = [];
    canvas.setAttribute("width", W); canvas.setAttribute("height", H);
  }
  function resize() {
    var cw = host.clientWidth || 360;
    applyLayout(cw < 480 ? "narrow" : "wide");
    var scale = cw >= 2 * W ? Math.floor(cw / W) : cw / W;
    var cssW = Math.round(W * scale), cssH = Math.round(H * scale), dpr = Math.min(window.devicePixelRatio || 1, 3);
    canvas.style.width = cssW + "px"; canvas.style.height = cssH + "px";
    canvas.width = Math.round(cssW * dpr); canvas.height = Math.round(cssH * dpr);
    render(frame);
  }
  if (window.ResizeObserver) { new ResizeObserver(resize).observe(host); } else { window.addEventListener("resize", resize); }

  function start() { if (running || reduceMotion) { return; } running = true; lastTick = 0; requestAnimationFrame(tick); }
  function stop() { running = false; }
  if ("IntersectionObserver" in window) {
    new IntersectionObserver(function (entries) { visible = entries[0].isIntersecting; if (visible && !document.hidden) { start(); } else { stop(); } }, { threshold: 0.05 }).observe(host);
  } else { start(); }
  document.addEventListener("visibilitychange", function () { if (document.hidden) { stop(); } else if (visible) { start(); } });

  setActivity(cole, Math.random() < 0.6 ? "solder" : "type", 14); setActivity(ilinca, Math.random() < 0.5 ? "type" : "write", 16);
  host.setAttribute("data-live", reduceMotion ? "still" : "on");
  resize();
  if (reduceMotion) { update(0); render(0); }

  window.NutrimaticDesk = {
    setHour: function (h) { hourOverride = (h === null || h === undefined) ? null : +h; updateLamp(hourNow()); render(frame); },
    activity: function (n, a, secs) { setActivity(who(n), a, secs || 10); updateLamp(hourNow()); render(frame); },
    react: function (n) { react(who(n)); render(frame); },
    scenario: function (name) { var ok = startScenario(name); render(frame); return ok; },
    converse: function () { startConvo(EXCHANGES[0]); stepConvo(frame); render(frame); },
    step: function (n) { for (var i = 0; i < (n || 1); i++) { frame++; update(frame); } render(frame); },
    state: function () { return { layout: layoutName, cole: cole.activity, ilinca: ilinca.activity, set: setIndex, hour: hourNow(), running: running, convo: !!convo, scenario: scenario ? scenario.name : null, lamp: { on: lamp.on, x: Math.round(lamp.hx) } }; }
  };
})();
