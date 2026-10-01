/*
 * Nutrimatic Website - desk-scene.js
 * Version 0.3.0
 *
 * Created: 2026-10-01 - Living pixel-art scene of the co-founders at their desk (v0.1.0)
 * Modified: 2026-10-01 - Likeness pass from the video and photos: dark frames, black tee, curls; shoulder-length dark hair, dotted top (v0.2.0)
 * Modified: 2026-10-01 - Browline glasses, desk lamp, Ilinca in a blazer over a white top (v0.3.0)
 *   - 208 x 117 logical pixels drawn on an offscreen canvas, shown at an integer scale
 *   - Window shows the visitor's time of day (sun / moon / stars, lamp comes on at night), wall clock too
 *   - Desk props rotate every couple of minutes; the two figures cycle through activities
 *     (typing, soldering, coffee, phone, thinking, stretching) and talk in speech bubbles
 *   - They watch the pointer when it moves nearby and react to clicks / taps
 *   - Reduced motion: one still frame. Off-screen or hidden tab: paused.
 *
 * Markup: <div data-desk-scene><canvas></canvas> ...fallback... </div>
 * Test hooks: window.NutrimaticDesk.setHour(h), .say(who, text), .react(who)
 */

(function () {
  "use strict";

  var W = 208, H = 117, FPS = 12;
  var DESK_Y = 84;                       // top edge of the desk surface
  var reduceMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  var host = document.querySelector("[data-desk-scene]");
  var canvas = host && host.querySelector("canvas");
  if (!host || !canvas || !canvas.getContext) { return; }
  var ctx = canvas.getContext("2d");
  var off = document.createElement("canvas"); off.width = W; off.height = H;
  var g = off.getContext("2d");

  /* ---------- palette ---------- */
  var C = {
    wall: "#e9e9e5", wallDark: "#d9d9d4", floorLine: "#cfcfca",
    ink: "#111111", ink2: "#2a2a2c", ink3: "#3d3d40", grey: "#8d8d90", greyLight: "#c4c4c0", white: "#ffffff",
    red: "#e4002b", redDeep: "#b80022",
    deskTop: "#3a3a3d", deskFront: "#1f1f21", deskEdge: "#515154",
    frame: "#111111",
    gold: "#c9a36a",
    // Cole
    cSkin: "#e6b792", cSkinS: "#c9936e", cHair: "#22160f", cHairH: "#3d2a20", cShirt: "#161616", cShirtS: "#2c2c2c", frames: "#2b2b2b",
    // Ilinca
    iSkin: "#f0cdb0", iSkinS: "#d6ad8e", iHair: "#45301f", iHairH: "#6a4a34", iTop: "#1b1b1d", iTopS: "#3a3a3e", blouse: "#f4f4f1", dots: "#d9d9d5",
    lips: "#c4727b", mouth: "#6e3b36", teeth: "#ffffff",
    green: "#2f7d4f", greenL: "#58a56f", leaf: "#3f8f55", stem: "#4b7a3a",
    petal: "#e4002b", petal2: "#ffffff", petalY: "#f2c744",
    pot: "#9a5a3c", potS: "#7a4530",
    board: "#2f6b3a", boardS: "#214d2a", copper: "#d19a4a",
    iron: "#9a9a9e", ironHot: "#ff6a3d", smoke: "#b9b9b6", smoke2: "#d6d6d2",
    phone: "#111111", phoneScreen: "#dfe9f5",
    paper: "#f7f7f3", paperLine: "#c9c9c4",
    mug: "#e4002b", mugS: "#b80022",
    lampBody: "#111111", lampShade: "#f4f4f0", lampShadeOn: "#ffe9a8", lampGlow: "rgba(255, 224, 150, 0.28)",
    skyNight: "#0d1030", skyNight2: "#1a1f4a", star: "#ffffff", moon: "#f3f1d8",
    skyDawn1: "#f0a66a", skyDawn2: "#86a2d6", skyDay1: "#8dc5f0", skyDay2: "#cfe8fb", skyDusk1: "#f29a5c", skyDusk2: "#5d4e8c",
    sun: "#ffd84a", cloud: "#ffffff", cloudS: "#e8f1f8",
    bubble: "#ffffff", bubbleLine: "#111111", text: "#111111",
    nightTint: "rgba(14, 16, 48, 0.28)"
  };

  /* ---------- tiny drawing helpers (everything is whole pixels) ---------- */
  function px(x, y, c) { g.fillStyle = c; g.fillRect(x | 0, y | 0, 1, 1); }
  function rect(x, y, w, h, c) { g.fillStyle = c; g.fillRect(x | 0, y | 0, w | 0, h | 0); }
  function hline(x, y, w, c) { rect(x, y, w, 1, c); }
  function vline(x, y, h, c) { rect(x, y, 1, h, c); }
  function outline(x, y, w, h, c) { hline(x, y, w, c); hline(x, y + h - 1, w, c); vline(x, y, h, c); vline(x + w - 1, y, h, c); }
  // Draw a string sprite: each char is a key into pal; '.' is transparent.
  function sprite(rows, x, y, pal) {
    for (var r = 0; r < rows.length; r++) {
      var row = rows[r];
      for (var cI = 0; cI < row.length; cI++) {
        var k = row[cI];
        if (k !== "." && pal[k]) { px(x + cI, y + r, pal[k]); }
      }
    }
  }

  /* ---------- 3x5 pixel font ---------- */
  var FONT = {
    A: "010101111101101", B: "110101110101110", C: "011100100100011", D: "110101101101110", E: "111100110100111",
    F: "111100110100100", G: "011100101101011", H: "101101111101101", I: "111010010010111", J: "001001001101010",
    K: "101101110101101", L: "100100100100111", M: "101111111101101", N: "110101101101101", O: "010101101101010",
    P: "110101110100100", Q: "010101101110011", R: "110101110101101", S: "011100010001110", T: "111010010010010",
    U: "101101101101111", V: "101101101101010", W: "101101111111101", X: "101101010101101", Y: "101101010010010",
    Z: "111001010100111", "0": "010101101101010", "1": "010110010010111", "2": "110001010100111", "3": "110001010001110",
    "4": "101101111001001", "5": "111100110001110", "6": "011100110101010", "7": "111001010010010", "8": "010101010101010",
    "9": "010101011001110", ".": "000000000000010", ",": "000000000010100", "!": "010010010000010", "?": "110001010000010",
    "'": "010010000000000", "-": "000000111000000", ":": "000010000010000", " ": "000000000000000"
  };
  function textWidth(s) { return s.length * 4 - 1; }
  function drawText(s, x, y, c) {
    s = String(s).toUpperCase();
    for (var i = 0; i < s.length; i++) {
      var bits = FONT[s[i]] || FONT["?"];
      for (var j = 0; j < 15; j++) { if (bits[j] === "1") { px(x + i * 4 + (j % 3), y + ((j / 3) | 0), c); } }
    }
  }

  /* ---------- time of day ---------- */
  var hourOverride = null;
  function hourNow() {
    if (hourOverride !== null) { return hourOverride; }
    var d = new Date(); return d.getHours() + d.getMinutes() / 60;
  }
  function lerp(a, b, t) { return a + (b - a) * t; }
  function hexToRgb(h) { return [parseInt(h.slice(1, 3), 16), parseInt(h.slice(3, 5), 16), parseInt(h.slice(5, 7), 16)]; }
  function mix(h1, h2, t) {
    var a = hexToRgb(h1), b = hexToRgb(h2);
    return "rgb(" + Math.round(lerp(a[0], b[0], t)) + "," + Math.round(lerp(a[1], b[1], t)) + "," + Math.round(lerp(a[2], b[2], t)) + ")";
  }
  // Sky top/bottom colours for an hour (0-24), blended across dawn and dusk.
  function skyFor(h) {
    function pick(h) {
      if (h < 5 || h >= 21) { return [C.skyNight, C.skyNight2]; }
      if (h < 7) { return [C.skyDawn1, C.skyDawn2]; }
      if (h < 17.5) { return [C.skyDay1, C.skyDay2]; }
      if (h < 20) { return [C.skyDusk1, C.skyDusk2]; }
      return [C.skyNight, C.skyNight2];
    }
    // blend over the half hour on either side of a boundary
    var bounds = [5, 7, 17.5, 20, 21];
    for (var i = 0; i < bounds.length; i++) {
      var b = bounds[i];
      if (Math.abs(h - b) < 0.5) {
        var t = (h - (b - 0.5)); var a = pick(b - 0.6), z = pick(b + 0.6);
        return [mix(a[0], z[0], t), mix(a[1], z[1], t)];
      }
    }
    return pick(h);
  }
  function isDark(h) { return h < 6.5 || h >= 18.5; }

  /* ---------- static background layers ---------- */
  var WIN = { x: 80, y: 10, w: 48, h: 44 };
  var stars = [];
  (function () { var seed = 7; function rnd() { seed = (seed * 9301 + 49297) % 233280; return seed / 233280; }
    for (var i = 0; i < 18; i++) { stars.push({ x: WIN.x + 2 + ((rnd() * (WIN.w - 4)) | 0), y: WIN.y + 2 + ((rnd() * (WIN.h - 14)) | 0), p: (rnd() * 20) | 0 }); } })();
  var clouds = [{ x: 0, y: 18, w: 11 }, { x: 24, y: 28, w: 8 }];

  function drawWall(h) {
    rect(0, 0, W, DESK_Y, C.wall);
    hline(0, DESK_Y - 1, W, C.wallDark);
    // skirting / shadow line under the window area for depth
    rect(0, DESK_Y - 6, W, 5, C.wallDark);
    // poster: the nu mark
    rect(12, 8, 20, 20, C.red);
    sprite([
      "wwwww.ww.ww",
      "ww.ww.ww.ww",
      "ww.ww.ww.ww",
      "ww.ww.ww.ww",
      "ww.ww.wwwww"
    ], 16, 15, { w: C.white });
    // wall clock on the visitor's time
    drawClock(185, 14, h);
  }

  function drawClock(cx, cy, h) {
    rect(cx - 6, cy - 6, 13, 13, C.white); outline(cx - 6, cy - 6, 13, 13, C.ink);
    px(cx, cy - 5, C.ink); px(cx, cy + 5, C.ink); px(cx - 5, cy, C.ink); px(cx + 5, cy, C.ink);
    var hr = (h % 12) / 12 * Math.PI * 2, mn = (h % 1) * Math.PI * 2;
    for (var i = 1; i <= 3; i++) { px(cx + Math.round(Math.sin(hr) * i), cy - Math.round(Math.cos(hr) * i), C.ink); }
    for (var j = 1; j <= 4; j++) { px(cx + Math.round(Math.sin(mn) * j), cy - Math.round(Math.cos(mn) * j), C.red); }
    px(cx, cy, C.ink);
  }

  function drawWindow(h, f) {
    var sky = skyFor(h);
    // sky gradient in bands
    var bands = 6;
    for (var i = 0; i < bands; i++) {
      var t = i / (bands - 1);
      rect(WIN.x, WIN.y + Math.round(i * WIN.h / bands), WIN.w, Math.ceil(WIN.h / bands) + 1, mix(hexOf(sky[0]), hexOf(sky[1]), t));
    }
    var dark = isDark(h);
    if (dark) {
      // stars twinkle slowly; moon
      for (var s = 0; s < stars.length; s++) { var st = stars[s]; if (((f >> 3) + st.p) % 7 !== 0) { px(st.x, st.y, C.star); } }
      var mx = WIN.x + 8 + Math.round(((h + 3) % 24) / 24 * 28), my = WIN.y + 8;
      rect(mx, my, 4, 4, C.moon); px(mx, my, sky[0]); px(mx + 3, my + 3, sky[0]); px(mx + 3, my, sky[0]); px(mx, my + 3, sky[0]);
    } else {
      // sun travels left to right between 6 and 19
      var sx = WIN.x + 3 + Math.round(Math.min(1, Math.max(0, (h - 6) / 13)) * (WIN.w - 10));
      var sy = WIN.y + 4 + Math.round(Math.abs((h - 12.5) / 6.5) * 14);
      rect(sx, sy, 4, 4, C.sun); px(sx, sy, hexOf(sky[0])); px(sx + 3, sy, hexOf(sky[0])); px(sx, sy + 3, hexOf(sky[0])); px(sx + 3, sy + 3, hexOf(sky[0]));
      // clouds drift
      for (var c = 0; c < clouds.length; c++) {
        var cl = clouds[c]; var cxp = WIN.x + ((cl.x + (f / 18)) % (WIN.w + cl.w)) - cl.w;
        drawCloud(cxp, WIN.y + cl.y, cl.w);
      }
    }
    // distant skyline at the bottom of the window
    var sil = dark ? "#0a0c22" : mix(hexOf(sky[1]), "#4b5566", 0.55);
    rect(WIN.x, WIN.y + WIN.h - 9, WIN.w, 9, sil);
    rect(WIN.x + 4, WIN.y + WIN.h - 14, 6, 5, sil); rect(WIN.x + 14, WIN.y + WIN.h - 18, 5, 9, sil); rect(WIN.x + 26, WIN.y + WIN.h - 12, 9, 3, sil); rect(WIN.x + 39, WIN.y + WIN.h - 16, 4, 7, sil);
    if (dark) { px(WIN.x + 16, WIN.y + WIN.h - 15, C.sun); px(WIN.x + 6, WIN.y + WIN.h - 12, C.sun); px(WIN.x + 40, WIN.y + WIN.h - 13, C.sun); }
    // frame and cross bars
    outline(WIN.x - 2, WIN.y - 2, WIN.w + 4, WIN.h + 4, C.frame); outline(WIN.x - 1, WIN.y - 1, WIN.w + 2, WIN.h + 2, C.frame);
    vline(WIN.x + WIN.w / 2 - 1, WIN.y, WIN.h, C.frame); vline(WIN.x + WIN.w / 2, WIN.y, WIN.h, C.frame);
    hline(WIN.x, WIN.y + 20, WIN.w, C.frame);
    // sill
    rect(WIN.x - 4, WIN.y + WIN.h + 2, WIN.w + 8, 2, C.ink2);
  }
  function hexOf(c) { // mix() needs hex; rgb() strings from an earlier blend are converted back
    if (c[0] === "#") { return c; }
    var m = /rgb\((\d+),(\d+),(\d+)\)/.exec(c); if (!m) { return "#000000"; }
    return "#" + [m[1], m[2], m[3]].map(function (n) { return ("0" + (+n).toString(16)).slice(-2); }).join("");
  }
  function drawCloud(x, y, w) {
    hline(x + 1, y, w - 2, C.cloud); hline(x, y + 1, w, C.cloud); hline(x, y + 2, w, C.cloudS); px(x + 2, y - 1, C.cloud); px(x + 3, y - 1, C.cloud);
  }

  function drawDesk() {
    rect(0, DESK_Y, W, 4, C.deskTop); hline(0, DESK_Y, W, C.deskEdge);
    rect(0, DESK_Y + 4, W, H - DESK_Y - 4, C.deskFront);
    hline(0, DESK_Y + 4, W, C.ink);
    // a drawer line and the red nu on the desk front
    hline(0, DESK_Y + 5, W, C.ink3);
  }

  /* ---------- props ---------- */
  function propLamp(x, on) { // base at (x, DESK_Y)
    rect(x - 5, DESK_Y - 2, 11, 2, C.lampBody); hline(x - 4, DESK_Y - 3, 9, C.lampBody);
    rect(x - 1, DESK_Y - 16, 2, 13, C.lampBody);                       // lower arm
    for (var i = 0; i < 8; i++) { px(x + i, DESK_Y - 17 - i, C.lampBody); px(x + i + 1, DESK_Y - 17 - i, C.lampBody); }   // upper arm, angled
    rect(x + 7, DESK_Y - 26, 3, 3, C.lampBody);                        // joint
    // shade: a trapezoid opening downward
    hline(x + 6, DESK_Y - 25, 7, on ? C.lampShadeOn : C.lampShade); hline(x + 5, DESK_Y - 24, 9, on ? C.lampShadeOn : C.lampShade);
    hline(x + 4, DESK_Y - 23, 11, on ? C.lampShadeOn : C.lampShade); hline(x + 3, DESK_Y - 22, 13, on ? C.lampShadeOn : C.lampShade);
    hline(x + 6, DESK_Y - 26, 7, C.lampBody); px(x + 5, DESK_Y - 25, C.lampBody); px(x + 13, DESK_Y - 25, C.lampBody); px(x + 4, DESK_Y - 24, C.lampBody); px(x + 14, DESK_Y - 24, C.lampBody);
    px(x + 3, DESK_Y - 23, C.lampBody); px(x + 15, DESK_Y - 23, C.lampBody); hline(x + 2, DESK_Y - 22, 1, C.lampBody); px(x + 16, DESK_Y - 22, C.lampBody);
    hline(x + 3, DESK_Y - 21, 13, C.lampBody);
    if (on) { hline(x + 6, DESK_Y - 20, 7, C.sun); }
  }
  function propVase(x, kind) {
    rect(x - 2, DESK_Y - 8, 5, 8, C.white); outline(x - 2, DESK_Y - 8, 5, 8, C.ink); hline(x - 3, DESK_Y - 9, 7, C.ink);
    vline(x, DESK_Y - 16, 7, C.stem); vline(x - 2, DESK_Y - 14, 5, C.stem); vline(x + 2, DESK_Y - 15, 6, C.stem);
    var p = kind === 0 ? C.petal : kind === 1 ? C.petal2 : C.petalY;
    rect(x - 1, DESK_Y - 19, 3, 3, p); rect(x - 3, DESK_Y - 16, 2, 2, p); rect(x + 2, DESK_Y - 17, 2, 2, p);
    if (kind === 1) { px(x, DESK_Y - 18, C.petalY); }
  }
  function propPlant(x) {
    rect(x - 3, DESK_Y - 6, 7, 6, C.pot); hline(x - 4, DESK_Y - 7, 9, C.potS);
    rect(x - 4, DESK_Y - 12, 3, 4, C.leaf); rect(x + 2, DESK_Y - 13, 3, 5, C.greenL); rect(x - 1, DESK_Y - 15, 3, 8, C.green); px(x, DESK_Y - 16, C.greenL);
  }
  function propPapers(x) {
    rect(x - 8, DESK_Y - 3, 16, 3, C.paper); outline(x - 8, DESK_Y - 3, 16, 3, C.paperLine); rect(x - 7, DESK_Y - 5, 15, 2, C.paper); hline(x - 7, DESK_Y - 5, 15, C.paperLine);
    hline(x - 5, DESK_Y - 4, 8, C.paperLine);
  }
  function propBottle(x) { // the Nutrimatic shaker
    rect(x - 3, DESK_Y - 16, 7, 16, C.white); outline(x - 3, DESK_Y - 16, 7, 16, C.ink);
    rect(x - 2, DESK_Y - 19, 5, 3, C.red); hline(x - 1, DESK_Y - 20, 3, C.redDeep);
    rect(x - 1, DESK_Y - 10, 3, 6, C.greyLight); px(x, DESK_Y - 7, C.red);
  }
  function propCartridge(x) {
    rect(x - 4, DESK_Y - 9, 9, 9, C.white); outline(x - 4, DESK_Y - 9, 9, 9, C.ink); rect(x - 1, DESK_Y - 6, 3, 3, C.gold); hline(x - 4, DESK_Y - 11, 9, C.ink); rect(x - 3, DESK_Y - 10, 7, 1, C.greyLight);
  }
  function propMug(x, steam, f) {
    rect(x - 3, DESK_Y - 7, 6, 7, C.mug); vline(x + 3, DESK_Y - 6, 4, C.mug); px(x + 4, DESK_Y - 6, C.mug); px(x + 4, DESK_Y - 3, C.mug); hline(x - 3, DESK_Y - 7, 6, C.mugS);
    if (steam) { var k = (f >> 2) % 3; px(x - 1 + k, DESK_Y - 10, C.smoke2); px(x + 1 - k, DESK_Y - 12, C.smoke2); }
  }
  function propLaptop(x) { // lid back facing the viewer, in front of a figure centred at x
    rect(x - 9, DESK_Y - 12, 18, 12, C.ink2); outline(x - 9, DESK_Y - 12, 18, 12, C.ink); px(x, DESK_Y - 6, C.red);
    hline(x - 10, DESK_Y - 1, 20, C.ink);
  }
  function propSolderStation(x) {
    rect(x - 6, DESK_Y - 4, 12, 4, C.ink3); outline(x - 6, DESK_Y - 4, 12, 4, C.ink); px(x - 4, DESK_Y - 3, C.red); px(x - 2, DESK_Y - 3, C.greenL);
    vline(x + 4, DESK_Y - 10, 6, C.grey); // iron stand
  }
  function propPhoneOnDesk(x) { rect(x - 2, DESK_Y - 1, 5, 1, C.phone); rect(x - 2, DESK_Y - 2, 5, 1, C.ink3); }

  /* ---------- characters ---------- */
  // Head sprites are 12 wide. Face rows 3..12; eyes at rows 6-7; mouth row 10.
  var HEAD_COLE = [
    "..hh.hhh.hh.",
    ".hhhhhhhhhh.",
    "hhhHhhhhhHhh",
    "hhhhssssshhh",
    "hhsssssssshh",
    "hssssssssssh",
    "ssssssssssss",
    "ssssssssssss",
    ".ssssssssss.",
    ".ssssssssss.",
    ".ssssssssss.",
    "..SssssssS..",
    "...ssssss...",
    "....ssss...."
  ];
  var HEAD_ILINCA = [
    "....hhHh....",
    "..hhhhhhhh..",
    ".hhhhhhhhhh.",
    "hhhssssssshh",
    "hhssssssssHh",
    "hhsssssssshh",
    "hhsssssssshh",
    "hhsssssssshh",
    "hhsssssssshh",
    "h.ssssssss.h",
    "h.ssssssss.h",
    "h..SssssS..h",
    "h...ssss...h",
    "h...ssss...h"
  ];
  // Shoulder-length hair behind the head (drawn before the body); 16 wide.
  var HAIR_BACK_ILINCA = [
    "....hhhhhhhh....",
    "..hhhhhhhhhhhh..",
    ".hhhhhhhhhhhhhh.",
    "hhhhhhhhhhhhhhhh",
    "hhhhhhhhhhhhhhhh",
    "hhhhhhhhhhhhhhhh",
    "hhhhhhhhhhhhhhhh",
    "hhhhhhhhhhhhhhhh",
    "hHhhhhhhhhhhhhHh",
    "hhhhhhhhhhhhhhhh",
    "hhhhhhhhhhhhhhhh",
    "hhhhhhhhhhhhhhhh",
    "hhhhhhhhhhhhhhhh",
    "hhhhhhhhhhhhhhhh",
    "hhhhhhhhhhhhhhhh",
    "hhhhhhhhhhhhhhhh",
    "hhhhhhhhhhhhhhhh",
    "hhhhhhhhhhhhhhhh",
    "hhhhhhhhhhhhhhhh",
    ".hhhhhhhhhhhhhh.",
    ".hhhhhhhhhhhhhh.",
    "..hhhhhhhhhhhh.."
  ];

  function makeCharacter(opts) {
    return {
      name: opts.name, x: opts.x, headY: 40, pal: opts.pal, head: opts.head, hairBack: opts.hairBack, glasses: !!opts.glasses, pattern: !!opts.pattern,
      shirt: opts.shirt, shirtS: opts.shirtS, collar: opts.collar,
      activities: opts.activities, activity: "rest", actUntil: 0, actFrame: 0,
      look: { x: 0, y: 0 }, lookTarget: { x: 0, y: 0 },
      mouth: "neutral", brows: null, blink: 0, nextBlink: 20 + Math.random() * 40,
      say: null, sayUntil: 0, react: null, reactUntil: 0, bob: 0, phoneOnDesk: false
    };
  }

  var cole = makeCharacter({
    name: "cole", x: 62, head: HEAD_COLE, glasses: true, pattern: false,
    pal: { h: C.cHair, H: C.cHairH, s: C.cSkin, S: C.cSkinS }, shirt: C.cShirt, shirtS: C.cShirtS, collar: "vee",
    activities: ["type", "solder", "solder", "think", "coffee", "stretch", "rest"]
  });
  var ilinca = makeCharacter({
    name: "ilinca", x: 146, head: HEAD_ILINCA, hairBack: HAIR_BACK_ILINCA,
    pal: { h: C.iHair, H: C.iHairH, s: C.iSkin, S: C.iSkinS }, shirt: C.iTop, shirtS: C.iTopS, collar: "blazer", pattern: false,
    activities: ["type", "type", "phone", "coffee", "think", "write", "stretch", "rest"]
  });
  var people = [cole, ilinca];

  // Body: shoulders and torso from the neck down to the desk. x = centre.
  function drawBody(p, y) {
    var x = p.x;
    rect(x - 2, y, 4, 2, p.pal.S);                       // neck
    rect(x - 10, y + 2, 20, DESK_Y - (y + 2), p.shirt);   // torso
    px(x - 10, y + 2, C.wall); px(x + 9, y + 2, C.wall);  // rounded shoulders
    if (p.collar === "vee") { hline(x - 2, y + 2, 4, p.pal.s); hline(x - 1, y + 3, 2, p.pal.s); hline(x - 3, y + 2, 1, p.shirtS); px(x + 2, y + 2, p.shirtS); }
    else if (p.collar === "blazer") {
      // white top showing in the V, lapels as a lighter edge, one button at the waist
      var half = [3, 3, 2, 2, 1, 1];
      for (var r = 0; r < half.length; r++) { rect(x - half[r], y + 2 + r, half[r] * 2, 1, C.blouse); px(x - half[r] - 1, y + 2 + r, p.shirtS); px(x + half[r], y + 2 + r, p.shirtS); }
      px(x, y + 8, p.shirtS); px(x, y + 9, p.shirtS); hline(x - 1, y + 12, 1, C.greyLight);
      px(x, y + 4, C.gold);
      hline(x - 9, y + 2, 2, p.shirtS); hline(x + 7, y + 2, 2, p.shirtS);   // shoulder line of the jacket
    }
    else { hline(x - 4, y + 2, 8, p.shirtS); px(x, y + 5, C.gold); }
    if (p.pattern) {
      for (var yy = y + 6; yy < DESK_Y - 1; yy += 3) { for (var xx = x - 8 + (((yy / 3) | 0) % 2) * 2; xx < x + 9; xx += 4) { px(xx, yy, C.dots); } }
    }
  }

  // Arms for each pose; drawn after the body so they overlap it. Returns nothing.
  function drawArms(p, y, f) {
    var x = p.x, skin = p.pal.s, sh = p.shirt, a = p.activity, k = p.actFrame;
    var sleeveY = y + 4;
    function upperArm(side) { rect(x + (side < 0 ? -13 : 10), sleeveY, 3, 10, sh); }
    function forearmOnDesk(side, dy) { rect(x + (side < 0 ? -14 : 6), DESK_Y - 4 + (dy || 0), 9, 3, sh); rect(x + (side < 0 ? -6 : 3), DESK_Y - 4 + (dy || 0), 3, 3, skin); }
    if (a === "type" || a === "write") {
      upperArm(-1); upperArm(1);
      if (a === "write") {
        forearmOnDesk(-1, 0); rect(x + 6, DESK_Y - 4, 7, 3, sh); rect(x + 10 + (k % 4 < 2 ? 0 : 1), DESK_Y - 5, 3, 3, skin); px(x + 12 + (k % 4 < 2 ? 0 : 1), DESK_Y - 6, C.ink);
      } else {
        // laptop lid hides the hands; elbows move a little
        var t = (k % 2) ? 1 : 0; rect(x - 13, sleeveY + 8 + t, 4, 2, sh); rect(x + 9, sleeveY + 8 + (1 - t), 4, 2, sh);
      }
    } else if (a === "solder") {
      upperArm(-1); upperArm(1);
      rect(x - 14, DESK_Y - 5, 8, 3, sh); rect(x - 8, DESK_Y - 7, 3, 3, skin);           // left hand steadies the board
      rect(x + 8, DESK_Y - 9, 5, 3, sh); rect(x + 8, DESK_Y - 13, 3, 3, skin);            // right hand holds the iron
    } else if (a === "coffee") {
      upperArm(-1); forearmOnDesk(-1, 0);
      var phase = k % 36; var up = phase >= 10 && phase < 22;
      if (up) { rect(x + 10, sleeveY, 3, 6, sh); rect(x + 7, sleeveY + 2, 4, 3, sh); rect(x + 5, y + 7, 3, 3, skin); }
      else { upperArm(1); forearmOnDesk(1, 0); }
    } else if (a === "think") {
      upperArm(1); forearmOnDesk(1, 0);
      rect(x - 13, sleeveY, 3, 6, sh); rect(x - 12, sleeveY + 6, 3, 3, sh); rect(x - 8, y + 8, 3, 3, skin);  // hand under chin
    } else if (a === "phone") {
      rect(x - 12, sleeveY + 2, 4, 6, sh); rect(x + 8, sleeveY + 2, 4, 6, sh);
      rect(x - 9, sleeveY + 7, 4, 3, skin); rect(x + 5, sleeveY + 7, 4, 3, skin);
    } else if (a === "stretch") {
      var s = Math.min(k, 6);
      rect(x - 14, y - s + 2, 3, 8, sh); rect(x + 11, y - s + 2, 3, 8, sh); rect(x - 14, y - s - 1, 3, 3, skin); rect(x + 11, y - s - 1, 3, 3, skin);
    } else if (a === "wave") {
      upperArm(-1); forearmOnDesk(-1, 0);
      var w = (k % 4) < 2 ? 0 : 2;
      rect(x + 10, y - 2, 3, 12, sh); rect(x + 9 + w, y - 5, 3, 3, skin);
    } else { // rest, talk, surprise...
      upperArm(-1); upperArm(1); forearmOnDesk(-1, 0); forearmOnDesk(1, 0);
    }
  }

  function drawFace(p, y, f) {
    var x = p.x - 6, pal = p.pal;
    sprite(p.head, x, y, pal);
    // eyes (rows 6-7), pupils follow look
    var ey = y + 6, lx = Math.round(p.look.x), ly = Math.round(p.look.y);
    var eyes = [[x + 2, ey], [x + 7, ey]];
    var closed = p.blink > 0 || p.mouth === "laugh";
    for (var i = 0; i < 2; i++) {
      var ex = eyes[i][0];
      if (closed) { hline(ex, ey + 1, 3, C.ink); continue; }
      rect(ex, ey, 3, 2, C.white);
      var pxl = ex + 1 + lx, pyl = ly > 0 ? ey + 1 : ey, ph = ly === 0 ? 2 : 1;
      rect(pxl, pyl, 1, ph, C.ink);
    }
    // brows
    if (p.brows === "up") { hline(x + 2, y + 4, 3, pal.h); hline(x + 7, y + 4, 3, pal.h); }
    else if (p.brows === "down") { hline(x + 3, y + 5, 2, pal.h); hline(x + 7, y + 5, 2, pal.h); px(x + 4, y + 4, pal.h); px(x + 7, y + 4, pal.h); }
    // glasses
    if (p.glasses) {
      hline(x + 1, y + 5, 10, C.frames);                                   // browline bar
      px(x + 1, y + 6, C.frames); px(x + 1, y + 7, C.frames); px(x + 5, y + 7, C.frames); px(x + 6, y + 7, C.frames); px(x + 10, y + 6, C.frames); px(x + 10, y + 7, C.frames);
      px(x, y + 6, C.frames); px(x + 11, y + 6, C.frames);                  // temples
      // re-draw the eye pixels the frame covered inside the lenses
      if (!closed) { for (var j = 0; j < 2; j++) { var ex2 = eyes[j][0]; rect(ex2, ey, 3, 2, C.white); var pxl2 = ex2 + 1 + lx, pyl2 = ly > 0 ? ey + 1 : ey; rect(pxl2, pyl2, 1, ly === 0 ? 2 : 1, C.ink); } }
    }
    // mouth (row 10)
    var my = y + 10, mc = p.name === "ilinca" ? C.lips : C.mouth;
    var m = p.mouth;
    if (m === "talk") { m = (f % 4 < 2) ? "open" : "neutral"; }
    if (m === "smile") { px(x + 4, my - 1, mc); hline(x + 5, my, 2, mc); px(x + 7, my - 1, mc); }
    else if (m === "laugh") { px(x + 3, my - 1, mc); hline(x + 4, my, 4, mc); hline(x + 4, my + 1, 4, C.teeth); px(x + 8, my - 1, mc); }
    else if (m === "open" || m === "o") { rect(x + 5, my, 2, 2, C.mouth); }
    else { hline(x + 5, my, 2, mc); }
  }

  function drawCharacter(p, f) {
    var y = p.headY + p.bob;
    var a = p.activity;
    if (a === "phone" || a === "type" || a === "write" || a === "solder") { y += 1; }      // head dips toward the work
    if (p.hairBack) { sprite(p.hairBack, p.x - 7, y - 1, p.pal); }
    drawBody(p, y + 14);
    if (p.hairBack) { // hair in front of the shoulders
      rect(p.x - 8, y + 13, 3, 9, p.pal.h); rect(p.x + 5, y + 13, 3, 9, p.pal.h); px(p.x - 7, y + 17, p.pal.H); px(p.x + 6, y + 16, p.pal.H);
    }
    drawArms(p, y + 14, f);
    drawFace(p, y, f);
    // props held
    if (a === "solder") {
      rect(p.x - 8, DESK_Y - 8, 10, 5, C.board); outline(p.x - 8, DESK_Y - 8, 10, 5, C.boardS); px(p.x - 6, DESK_Y - 6, C.copper); px(p.x - 3, DESK_Y - 6, C.copper); px(p.x, DESK_Y - 6, C.copper);
      rect(p.x + 6, DESK_Y - 12, 3, 2, C.red);                                            // handle, in the hand
      px(p.x + 5, DESK_Y - 10, C.iron); px(p.x + 4, DESK_Y - 9, C.iron); px(p.x + 3, DESK_Y - 8, C.iron);
      px(p.x + 2, DESK_Y - 7, (f % 6 < 3) ? C.ironHot : C.iron);                          // tip on the board
      var sm = (f >> 1) % 8; px(p.x + 2 + (sm % 2), DESK_Y - 9 - sm, sm < 4 ? C.smoke : C.smoke2);
      if (f % 23 === 0) { px(p.x + 1, DESK_Y - 8, C.sun); }
    } else if (a === "coffee") {
      var phase = p.actFrame % 36, up = phase >= 10 && phase < 22;
      if (up) { rect(p.x + 3, y + 8, 5, 5, C.mug); px(p.x + 8, y + 9, C.mug); px(p.x + 8, y + 11, C.mug); }
      else { propMug(p.x + 10, true, f); }
    } else if (a === "phone") {
      rect(p.x - 3, y + 21, 6, 8, C.phone); rect(p.x - 2, y + 22, 4, 6, (f % 24 < 20) ? C.phoneScreen : C.white);
    } else if (a === "write") {
      rect(p.x - 2, DESK_Y - 3, 14, 3, C.paper); hline(p.x - 2, DESK_Y - 3, 14, C.paperLine);
    } else if (a === "type") {
      propLaptop(p.x);
    }
  }

  /* ---------- speech bubbles ---------- */
  function drawBubble(p, text) {
    var w = textWidth(text) + 6, h = 9;
    var bx = Math.round(p.x - w / 2), by = p.headY - 14;
    if (bx < 2) { bx = 2; } if (bx + w > W - 2) { bx = W - 2 - w; }
    rect(bx, by, w, h, C.bubble); outline(bx, by, w, h, C.bubbleLine);
    // tail
    var tx = Math.min(Math.max(p.x, bx + 3), bx + w - 4);
    hline(tx - 1, by + h, 3, C.bubbleLine); px(tx, by + h + 1, C.bubbleLine); hline(tx - 1, by + h - 1, 3, C.bubble); px(tx, by + h, C.bubble);
    drawText(text, bx + 3, by + 2, C.text);
  }

  /* ---------- the desk population ---------- */
  var SETS = [
    ["vase0", "plant", "papers"], ["bottle", "vase1", "cartridge"], ["plant", "bottle", "papers"],
    ["vase2", "cartridge", "plant"], ["papers", "vase0", "bottle"], ["cartridge", "plant", "vase1"]
  ];
  var setIndex = 0, setChangeAt = 0;
  var SLOTS = [104, 24, 190];   // between the two, far left (beside the lamp), far right
  function drawProps(h, f) {
    propLamp(10, isDark(h));
    var set = SETS[setIndex];
    for (var i = 0; i < set.length; i++) {
      var k = set[i], x = SLOTS[i];
      if (k === "plant") { propPlant(x); }
      else if (k === "papers") { propPapers(x); }
      else if (k === "bottle") { propBottle(x); }
      else if (k === "cartridge") { propCartridge(x); }
      else if (k.indexOf("vase") === 0) { propVase(x, +k[4]); }
    }
    if (cole.activity === "solder") { propSolderStation(cole.x + 20); }
    if (ilinca.activity !== "coffee" && ilinca.phoneOnDesk) { propPhoneOnDesk(ilinca.x + 16); }
  }

  /* ---------- conversation ---------- */
  var LINES = [
    [["cole", "FIRMWARE'S FLASHED."], ["ilinca", "DID IT DISPENSE?"], ["cole", "45 SECONDS."]],
    [["ilinca", "GYM CALLED BACK."], ["cole", "AND?"], ["ilinca", "THEY WANT TWO."]],
    [["cole", "OUT OF CREATINE."], ["ilinca", "SWAP THE CARTRIDGE."]],
    [["ilinca", "COFFEE?"], ["cole", "ALWAYS."]],
    [["ilinca", "DEMO DAY FRIDAY."], ["cole", "IT'LL BE READY."], ["ilinca", "IT'D BETTER."]],
    [["cole", "SMELLS LIKE SOLDER."], ["ilinca", "OPEN THE WINDOW."]],
    [["ilinca", "PROTEIN'S TRENDING."], ["cole", "WE KNOW."]],
    [["cole", "WHAT'S 39 TIMES 1433?"], ["ilinca", "55887."], ["cole", "SHOW-OFF."]],
    [["ilinca", "ONE MORE CALL."], ["cole", "ONE MORE BOARD."]]
  ];
  var LINES_NIGHT = [[["ilinca", "GO HOME, COLE."], ["cole", "ONE MORE BOARD."]], [["cole", "STILL HERE?"], ["ilinca", "SPREADSHEETS."]]];
  var LINES_MORNING = [[["cole", "MORNING."], ["ilinca", "MORNING."], ["cole", "COFFEE'S ON."]]];
  var VISITOR = [["cole", "WHO'S THAT?"], ["ilinca", "A VISITOR. WAVE."]];
  var convo = null, convoAt = 0, nextConvoAt = 6 * FPS, saidHello = false;

  function startConvo(lines) { convo = { lines: lines, i: 0, until: 0 }; }
  function who(n) { return n === "cole" ? cole : ilinca; }
  function stepConvo(f) {
    if (!convo) {
      if (f >= nextConvoAt) {
        var h = hourNow(), pool = LINES;
        if (isDark(h) && Math.random() < 0.5) { pool = LINES_NIGHT; }
        else if (h >= 6 && h < 10 && Math.random() < 0.5) { pool = LINES_MORNING; }
        startConvo(pool[(Math.random() * pool.length) | 0]);
        nextConvoAt = f + (30 + Math.random() * 30) * FPS;
      }
      return;
    }
    if (f >= convo.until) {
      if (convo.i >= convo.lines.length) {
        convo = null; cole.say = ilinca.say = null; cole.mouth = ilinca.mouth = "neutral";
        return;
      }
      var line = convo.lines[convo.i]; var sp = who(line[0]), other = sp === cole ? ilinca : cole;
      cole.say = ilinca.say = null; cole.mouth = ilinca.mouth = "neutral";
      sp.say = line[1]; sp.mouth = "talk"; other.mouth = (convo.i === convo.lines.length - 1 && Math.random() < 0.5) ? "smile" : "neutral";
      // look at each other
      sp.lookTarget = { x: other.x < sp.x ? -1 : 1, y: 0 }; other.lookTarget = { x: sp.x < other.x ? -1 : 1, y: 0 };
      convo.until = f + Math.round((1.2 + line[1].length * 0.09) * FPS);
      convo.i++;
      if (line[1] === "A VISITOR. WAVE.") { setTimeout(function () { setActivity(cole, "wave", 3); setActivity(ilinca, "wave", 3); }, 900); }
    }
  }

  /* ---------- activities ---------- */
  function setActivity(p, a, seconds) {
    p.activity = a; p.actFrame = 0; p.actUntil = frame + Math.round(seconds * FPS);
    p.brows = a === "think" ? "down" : null;
    if (p === ilinca) { p.phoneOnDesk = a !== "phone" && a !== "wave"; }
  }
  function nextActivity(p) {
    var a = p.activities[(Math.random() * p.activities.length) | 0];
    if (a === p.activity) { a = p.activities[(Math.random() * p.activities.length) | 0]; }
    var secs = a === "stretch" ? 2.5 : a === "coffee" ? 9 : a === "rest" ? 4 : 10 + Math.random() * 12;
    setActivity(p, a, secs);
  }

  /* ---------- pointer ---------- */
  var pointer = { x: 0, y: 0, at: -1e9, inside: false };
  var scale = 1, cssW = W, cssH = H;
  function toScene(clientX, clientY) {
    var r = canvas.getBoundingClientRect();
    return { x: (clientX - r.left) / r.width * W, y: (clientY - r.top) / r.height * H, near: clientX > r.left - r.width * 0.6 && clientX < r.right + r.width * 0.6 && clientY > r.top - r.height && clientY < r.bottom + r.height };
  }
  window.addEventListener("pointermove", function (e) {
    var s = toScene(e.clientX, e.clientY);
    if (!s.near) { return; }
    pointer.x = s.x; pointer.y = s.y; pointer.at = Date.now(); pointer.inside = s.x >= 0 && s.x <= W && s.y >= 0 && s.y <= H;
  }, { passive: true });
  canvas.addEventListener("pointerdown", function (e) {
    var s = toScene(e.clientX, e.clientY);
    pointer.x = s.x; pointer.y = s.y; pointer.at = Date.now() + 1500; pointer.inside = true;
    var target = null;
    for (var i = 0; i < people.length; i++) { if (Math.abs(s.x - people[i].x) < 16 && s.y > people[i].headY - 16 && s.y < DESK_Y + 6) { target = people[i]; } }
    if (target) { react(target); }
    else { cole.lookTarget = aimAt(cole, s.x, s.y); ilinca.lookTarget = aimAt(ilinca, s.x, s.y); }
  });
  function aimAt(p, x, y) {
    var dx = x - p.x, dy = y - (p.headY + 7);
    return { x: Math.abs(dx) < 6 ? 0 : (dx < 0 ? -1 : 1), y: dy < -10 ? -1 : (dy > 12 ? 1 : 0) };
  }

  var REACTIONS = ["wave", "surprise", "laugh", "wave"];
  function react(p) {
    var now = frame;
    p.reactCount = (p.reactUntil > now - FPS * 4) ? (p.reactCount || 0) + 1 : 1;
    var kind = REACTIONS[(Math.random() * REACTIONS.length) | 0];
    if (p.reactCount >= 4) { kind = "enough"; }
    p.react = kind; p.reactUntil = now + Math.round((kind === "enough" ? 2.2 : 1.8) * FPS);
    p.say = kind === "wave" ? "HI!" : kind === "surprise" ? "!" : kind === "laugh" ? "HA!" : "OK, OK.";
    p.mouth = kind === "laugh" ? "laugh" : kind === "surprise" ? "o" : "smile";
    p.brows = kind === "surprise" ? "up" : null;
    if (kind === "wave") { setActivity(p, "wave", 1.8); }
    if (kind === "surprise") { p.bob = -1; }
    var other = p === cole ? ilinca : cole; other.lookTarget = { x: p.x < other.x ? -1 : 1, y: 0 };
  }

  /* ---------- the frame ---------- */
  var frame = 0, running = false, visible = true, lastTick = 0;
  function tick(now) {
    if (!running) { return; }
    requestAnimationFrame(tick);
    if (now - lastTick < 1000 / FPS) { return; }
    lastTick = now; frame++;
    update(frame);
    render(frame);
  }

  function update(f) {
    var h = hourNow();
    // desk population
    if (f >= setChangeAt) { setIndex = (setIndex + 1 + ((Math.random() * (SETS.length - 1)) | 0)) % SETS.length; setChangeAt = f + (90 + Math.random() * 60) * FPS; }
    // pointer attention
    var pointerActive = (Date.now() - pointer.at) < 2500;
    for (var i = 0; i < people.length; i++) {
      var p = people[i];
      // reactions wear off
      if (p.react && f >= p.reactUntil) { p.react = null; p.say = null; p.mouth = "neutral"; p.brows = p.activity === "think" ? "down" : null; p.bob = 0; }
      // activities
      p.actFrame++;
      if (f >= p.actUntil && !p.react) { nextActivity(p); }
      // where to look
      if (pointerActive) { p.lookTarget = aimAt(p, pointer.x, pointer.y); }
      else if (!convo && !p.react) {
        var a = p.activity;
        if (a === "type" || a === "write" || a === "solder" || a === "phone") { p.lookTarget = { x: 0, y: 1 }; }
        else if (a === "think") { p.lookTarget = { x: (f >> 5) % 2 ? -1 : 1, y: -1 }; }
        else if (a === "coffee") { p.lookTarget = { x: 0, y: 0 }; }
        else { p.lookTarget = { x: ((f >> 4) + i) % 3 - 1, y: 0 }; }
      }
      p.look.x += (p.lookTarget.x - p.look.x) * 0.6; p.look.y += (p.lookTarget.y - p.look.y) * 0.6;
      // blinking
      if (p.blink > 0) { p.blink--; }
      else if (--p.nextBlink <= 0) { p.blink = 2; p.nextBlink = 24 + Math.random() * 48; }
      // breathing
      if (!p.react) { p.bob = ((f + i * 7) % 48) < 24 ? 0 : 1; }
      // laugh when the other one laughs
      var other = people[1 - i];
      if (other.react === "laugh" && !p.react && f % 5 === 0) { p.mouth = "smile"; }
    }
    // the visitor exchange, once, when the pointer lingers over the scene
    if (pointer.inside && pointerActive && !saidHello && !convo && f > 4 * FPS) { saidHello = true; startConvo(VISITOR); }
    if (!(pointerActive && pointer.inside) && saidHello && convo && convo.lines === VISITOR) { /* keep going */ }
    stepConvo(f);
  }

  function render(f) {
    var h = hourNow();
    drawWall(h);
    drawWindow(h, f);
    drawDesk();
    // characters, far one first so bubbles layer sensibly
    for (var i = 0; i < people.length; i++) { drawCharacter(people[i], f); }
    drawProps(h, f);
    if (isDark(h)) {
      // dim the room except the window, then the lamp's pool of light
      g.fillStyle = C.nightTint; g.fillRect(0, 0, W, WIN.y - 2); g.fillRect(0, WIN.y - 2, WIN.x - 2, WIN.h + 4); g.fillRect(WIN.x + WIN.w + 2, WIN.y - 2, W - WIN.x - WIN.w - 2, WIN.h + 4); g.fillRect(0, WIN.y + WIN.h + 2, W, H - WIN.y - WIN.h - 2);
      g.fillStyle = C.lampGlow; g.fillRect(8, DESK_Y - 20, 30, 20); g.fillRect(2, DESK_Y - 14, 44, 14); g.fillRect(0, DESK_Y - 8, 56, 8);
    }
    for (var j = 0; j < people.length; j++) { if (people[j].say) { drawBubble(people[j], people[j].say); } }
    blit();
  }

  function blit() {
    ctx.imageSmoothingEnabled = false;
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.drawImage(off, 0, 0, canvas.width, canvas.height);
  }

  /* ---------- sizing ---------- */
  function resize() {
    var cw = host.clientWidth || W;
    scale = cw >= 2 * W ? Math.floor(cw / W) : cw / W;
    cssW = Math.round(W * scale); cssH = Math.round(H * scale);
    var dpr = Math.min(window.devicePixelRatio || 1, 3);
    canvas.style.width = cssW + "px"; canvas.style.height = cssH + "px";
    canvas.width = Math.round(cssW * dpr); canvas.height = Math.round(cssH * dpr);
    render(frame);
  }
  if (window.ResizeObserver) { new ResizeObserver(resize).observe(host); } else { window.addEventListener("resize", resize); }

  /* ---------- start / stop ---------- */
  function start() { if (running || reduceMotion) { return; } running = true; lastTick = 0; requestAnimationFrame(tick); }
  function stop() { running = false; }
  if ("IntersectionObserver" in window) {
    new IntersectionObserver(function (entries) { visible = entries[0].isIntersecting; if (visible && !document.hidden) { start(); } else { stop(); } }, { threshold: 0.05 }).observe(host);
  } else { start(); }
  document.addEventListener("visibilitychange", function () { if (document.hidden) { stop(); } else if (visible) { start(); } });

  // initial state
  setActivity(cole, "solder", 12); setActivity(ilinca, "type", 14); setChangeAt = (100 + Math.random() * 60) * FPS;
  host.setAttribute("data-live", reduceMotion ? "still" : "on");
  resize();
  if (reduceMotion) { hourOverride = null; update(0); render(0); }

  // test / preview hooks
  window.NutrimaticDesk = {
    setHour: function (h) { hourOverride = (h === null || h === undefined) ? null : +h; render(frame); },
    say: function (n, text) { who(n).say = text; who(n).mouth = "talk"; render(frame); },
    react: function (n) { react(who(n)); render(frame); },
    activity: function (n, a, secs) { setActivity(who(n), a, secs || 10); render(frame); },
    state: function () { return { cole: cole.activity, ilinca: ilinca.activity, set: setIndex, hour: hourNow(), running: running }; }
  };
})();
