/*
 * Nutrimatic Website - desk-scene.js
 * Version 0.8.0
 *
 * Created: 2026-10-01 - Living pixel-art scene of the co-founders at their desk (v0.1.0)
 * Modified: 2026-10-01 - Likeness pass (v0.2.0); browline glasses, desk lamp, blazer (v0.3.0); redraw at a larger scale (v0.4.0)
 * Modified: 2026-10-01 - Seated proportions with jointed arms; two layouts (wide desk on desktop, closer on phones);
 *   name plates; articulated lamp that swings over whoever is soldering or writing and casts a cone of light; New York
 *   skyline that lights up at night; scripted scenarios (Nintendo DS, high five, paper airplane, pigeon, cat, coffee run,
 *   shake break, late night, solder spark); desk set per visit; no frame, no speech bubbles (v0.5.0)
 * Modified: 2026-10-02 - The figures are no longer drawn in code: they come from portraits generated from photos and
 *   finished as sprites (js/desk-sprites.js). A figure is a torso and a head (the head nods), a face built from blink /
 *   look / brow / mouth frames, and jointed arms drawn as capsules and posed by two-bone IK, so every behaviour and
 *   scenario from v0.5 still plays. Stage 160 pixels high (the phone layout is 240x160, a Game Boy Advance screen).
 *   The room: ceiling, pendant light, warm walls, a sun patch by day, blue dark with warm pools at night. The cat is
 *   Maker (v0.6.0)
 *
 * Modified: 2026-10-02 - No arm is drawn in code any more ("arms and hands look dreadful"). Every activity has a body pose
 *   generated as one picture (torso, arms, hands and what they hold) and drawn under the same head; the hands' part of a
 *   pose lies over the desk; a few poses have a front part over the face (v0.7.0)
 *
 * Modified: 2026-10-02 - Bodies no longer bob (a laptop moved with the breath); a nod is a forward tilt (the face
 *   shortens a pixel) rather than the head moving down; both tilt toward their work and look at it; Ilinca's head
 *   sits lower (her neck read too long); small expression changes for both, Ilinca at rest no longer smiling. The room
 *   is generated art now, like the figures (assets/desk/*.png): painted brick, a steel factory window onto Midtown
 *   (Empire State, Chrysler, One Vanderbilt; lit at night after the real skyline), shelves, a walnut desk, and an
 *   anglepoise lamp each, Cole's red and Ilinca's white. Writing moves the hand; the bottle is handed across with
 *   both arms out. Maker is a fifth bigger and shaded; she kneads her spot, lies on the desk for a while, gets
 *   petted, blinks, looks at them, sits on a laptop or the paper (and is petted anyway), keeps clear of the
 *   soldering, and they lift their hands when she walks past (v0.8.0)
 *
 * Markup: <div data-desk-scene><canvas></canvas> ...fallback... </div>, with js/desk-sprites.js loaded first.
 * Test hooks: window.NutrimaticDesk.setHour(h), .activity(who, name, secs), .react(who), .scenario(name), .converse(),
 *   .face(who, {mouth, brows, look}), .poses(who), .step(n), .state()
 */

(function () {
  "use strict";

  var FPS = 12, DESK_Y = 134, CEIL = 8;
  var reduceMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  var ART = window.NutrimaticDeskArt;
  var host = document.querySelector("[data-desk-scene]");
  var canvas = host && host.querySelector("canvas");
  if (!host || !canvas || !canvas.getContext || !ART || !ART.cole || !ART.ilinca) { return; }   // the photos stay as the fallback
  var ctx = canvas.getContext("2d");
  var off = document.createElement("canvas");
  var g = off.getContext("2d");

  /* ---------- layouts: a wide desk on desktop, the two of them closer on phones (240x160) ---------- */
  // With the generated room (assets/desk) the poster, clock and window are where that picture has them; `art` holds
  // those places, `win` etc. are the drawn room's (the fallback when the pictures do not load).
  var LAYOUTS = {
    wide:   { W: 360, H: 160, cole: 124, ilinca: 226, poster: { x: 14, y: 20, w: 58, h: 62 }, clock: { x: 88, y: 34 }, win: { x: 280, y: 22, w: 66, h: 74 }, lamp: 177, pendant: 177, slots: [36, 272, 338, 12, 306],
              art: { poster: { x: 13, y: 20, w: 51, h: 62 }, clock: { x: 88, y: 34, r: 7 }, win: { x: 262, y: 18, w: 88, h: 84 }, sky: { x: 254, y: 15 }, lamps: [67, 290], slots: [34, 318, 344] } },
    narrow: { W: 240, H: 160, cole: 60, ilinca: 162, poster: { x: 1, y: 20, w: 51, h: 50 }, clock: { x: 98, y: 30 }, win: { x: 190, y: 22, w: 46, h: 66 }, lamp: 112, pendant: 126, slots: [226, 10],
              art: { poster: { x: 4, y: 20, w: 38, h: 50, mark: true }, clock: { x: 99, y: 31, r: 7 }, win: { x: 192, y: 20, w: 44, h: 70 }, sky: { x: 130, y: 3 }, lamps: [0, 226], slots: [] } }
  };
  // The environment pictures. Until they have loaded (or if they never do) the room is drawn in code as before.
  var ENV = { ready: false, img: {} };
  (function () {
    var base = "assets/desk/", names = ["room-wide", "desk-wide", "room-narrow", "desk-narrow", "sky-day", "sky-night", "lamp-red", "lamp-white", "prop-bottle", "prop-mug", "prop-papers", "prop-vase", "prop-plant"], left = names.length;
    var inline = window.NutrimaticDeskAssets || {};                      // a self-contained preview hands the pictures over as data
    try { if (document.currentScript && document.currentScript.src) { base = new URL("../assets/desk/", document.currentScript.src).href; } } catch (e) { /* relative path */ }
    names.forEach(function (n) {
      var im = new Image();
      im.onload = function () { if (--left === 0) { ENV.ready = true; applyArt(); if (typeof render === "function") { render(frame); } } };
      im.onerror = function () { left = -1; };
      im.src = inline[n] || (base + n + ".png"); ENV.img[n] = im;
    });
  })();
  var L = LAYOUTS.wide, W = L.W, H = L.H, WIN = L.win, layoutName = "";

  /* ---------- palette (room and props; the figures carry their own) ---------- */
  var C = {
    wall: "#e9dfcc", wallD: "#d9ccb4", wallNight: "#1a1f3a", wallDusk: "#c47a4a", ceil: "#2d2a29", ceilL: "#4a4542", rail: "#b9a888",
    ink: "#111111", ink2: "#2a2a2c", ink3: "#3d3d40", grey: "#8d8d90", greyLight: "#c4c4c0", white: "#ffffff", red: "#e4002b", redDeep: "#a3001f", redLight: "#ff4d6a",
    deskTop: "#6b4a30", deskTopL: "#8a6442", deskTopD: "#4e3522", deskFront: "#3b2817", deskFrontD: "#2a1b0f", plate: "#efe9dc", plateS: "#b7ad99",
    green: "#2d6a3c", greenL: "#6fb57f", leaf: "#3f8f55", stem: "#4b7a3a", petalR: "#e4002b", petalW: "#ffffff", petalY: "#f2c744",
    pot: "#a3603c", potS: "#7c4428", board: "#2f6b3a", boardS: "#1f4a28", copper: "#d9a650",
    iron: "#9a9a9e", ironHot: "#ff6a3d", smoke: "#c9c6bf", smoke2: "#dedbd4", phone: "#111111", phoneScreen: "#dfe9f5",
    paper: "#fbfaf5", paperLine: "#d9d5c8", mug: "#e4002b", mugS: "#a3001f", mugL: "#ff4d6a",
    laptop: "#cfd2d4", laptopS: "#9a9ea2", laptopL: "#eaeced", ds: "#d6162f", dsS: "#9d0f22", dsScreen: "#cfe3d4",
    lampBody: "#1b1b1b", lampShade: "#f2efe6", lampShadeOn: "#ffe9a8", bulb: "#fff1b8", pendant: "#1f1f22", pendantIn: "#ffe6a0", pendantOff: "#6d6d70", cord: "#2a2a2c",
    skyNight: "#0d1030", skyNight2: "#1a1f4a", star: "#ffffff", moon: "#f3f1d8", skyDawn1: "#f0a66a", skyDawn2: "#86a2d6",
    skyDay1: "#8dc5f0", skyDay2: "#cfe8fb", skyDusk1: "#f29a5c", skyDusk2: "#5d4e8c", sun: "#ffd84a", cloud: "#ffffff", cloudS: "#e8f1f8",
    bldg: "#6e7a8c", bldgFar: "#8f9bab", bldgNight: "#0b0d20", bldgNightFar: "#141735", winLit: "#ffd97a", winLit2: "#ffe9b0", beacon: "#ff3b3b",
    cat: "#7c8088", catD: "#5a5e66", catL: "#9ba0a8", catEye: "#c8d84a", catNose: "#4a4d54", catMouth: "#d98a92",
    pigeon: "#8a8f99", pigeonL: "#b4b8c0", pigeonD: "#5c6070", plane: "#ffffff", planeS: "#b9b9b5"
  };

  /* ---------- helpers: whole pixels only ---------- */
  function px(x, y, c) { g.fillStyle = c; g.fillRect(x | 0, y | 0, 1, 1); }
  function rect(x, y, w, h, c) { g.fillStyle = c; g.fillRect(x | 0, y | 0, w | 0, h | 0); }
  function hline(x, y, w, c) { rect(x, y, w, 1, c); }
  function vline(x, y, h, c) { rect(x, y, 1, h, c); }
  function outline(x, y, w, h, c) { hline(x, y, w, c); hline(x, y + h - 1, w, c); vline(x, y, h, c); vline(x + w - 1, y, h, c); }
  function limb(x1, y1, x2, y2, w, c) {
    var dx = Math.abs(x2 - x1), dy = Math.abs(y2 - y1), sx = x1 < x2 ? 1 : -1, sy = y1 < y2 ? 1 : -1, err = dx - dy, x = x1, y = y1, o = (w / 2) | 0;
    g.fillStyle = c;
    for (var guard = 0; guard < 600; guard++) {
      g.fillRect(x - o, y - o, w, w);
      if (x === x2 && y === y2) { break; }
      var e2 = 2 * err; if (e2 > -dy) { err -= dy; x += sx; } if (e2 < dx) { err += dx; y += sy; }
    }
  }
  function lerp(a, b, t) { return a + (b - a) * t; }
  function clamp(v, a, b) { return v < a ? a : v > b ? b : v; }
  function hexToRgb(h) { return [parseInt(h.slice(1, 3), 16), parseInt(h.slice(3, 5), 16), parseInt(h.slice(5, 7), 16)]; }
  function mix(h1, h2, t) {
    var a = hexToRgb(h1), b = hexToRgb(h2);
    return "#" + [0, 1, 2].map(function (i) { return ("0" + Math.round(a[i] + (b[i] - a[i]) * t).toString(16)).slice(-2); }).join("");
  }
  function hash(a, b, c) { var n = (a * 73856093) ^ (b * 19349663) ^ (c * 83492791); n = (n ^ (n >>> 13)) * 1274126177; return ((n ^ (n >>> 16)) >>> 0) % 1000; }

  /* ---------- sprites: the art arrives as data (js/desk-sprites.js) and is baked to small canvases once ---------- */
  // A layer's pixels: one character per pixel (0-9a-z = palette index, "." = clear), row after row, with runs
  // written as the character followed by its length in capital letters (base 26, A = 0).
  function bake(layer, pal) {
    var c = document.createElement("canvas"); c.width = layer.w; c.height = layer.h;
    var k = c.getContext("2d"), img = k.createImageData(layer.w, layer.h), d = img.data, s = layer.d, i = 0, at = 0;
    while (i < s.length) {
      var code = s.charCodeAt(i++), n = 0, counted = false;
      while (i < s.length) { var u = s.charCodeAt(i); if (u < 65 || u > 90) { break; } n = n * 26 + (u - 65); counted = true; i++; }
      if (!counted) { n = 1; }
      if (code !== 46) {
        var rgb = hexToRgb(pal[code < 58 ? code - 48 : code - 87]);
        for (var q = 0; q < n; q++) { var j = (at + q) * 4; d[j] = rgb[0]; d[j + 1] = rgb[1]; d[j + 2] = rgb[2]; d[j + 3] = 255; }
      }
      at += n;
    }
    k.putImageData(img, 0, 0);
    return { c: c, x: layer.x, y: layer.y, w: layer.w, h: layer.h };
  }
  function blit(s, ox, oy) { g.drawImage(s.c, (ox + s.x) | 0, (oy + s.y) | 0); }
  function blitFlip(s, ox, oy) { g.save(); g.translate(((ox + s.x) | 0) + s.w, (oy + s.y) | 0); g.scale(-1, 1); g.drawImage(s.c, 0, 0); g.restore(); }
  function pixels(list, ox, oy, pal) { for (var i = 0; i < list.length; i += 3) { if (list[i + 2] >= 0) { px(ox + list[i], oy + list[i + 1], pal[list[i + 2]]); } } }

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
  // How much of the night look applies (0 by day, 1 at night) and how much of the low warm sun (around sunrise and sunset).
  function nightAmount(h) { if (h >= 20.5 || h < 5) { return 1; } if (h >= 7 && h < 18) { return 0; } return h >= 18 ? (h - 18) / 2.5 : 1 - (h - 5) / 2; }
  function duskAmount(h) { return Math.max(0, 1 - Math.abs(h - 18.8) / 1.7, 1 - Math.abs(h - 6.2) / 1.2); }

  /* ---------- the room: ceiling, wall, poster, clock, pendant ---------- */
  var NU = ["wwwww.ww.ww", "ww.ww.ww.ww", "ww.ww.ww.ww", "ww.ww.ww.ww", "ww.ww.wwwww"];
  function drawPoster(P) {
    rect(P.x + 2, P.y + 3, P.w, P.h, "rgba(0,0,0,0.20)");                                        // drop shadow
    rect(P.x, P.y, P.w, P.h, C.ink); rect(P.x + 3, P.y + 3, P.w - 6, P.h - 6, "#f4f2ec");
    var mx = P.x + ((P.w - 22) / 2 | 0), my = P.y + (P.h > 55 ? 13 : 9);
    for (var r = 0; r < NU.length; r++) { for (var i = 0; i < NU[r].length; i++) { if (NU[r][i] === "w") { rect(mx + i * 2, my + r * 2, 2, 2, C.ink); } } }
    hline(P.x + 9, my + 16, P.w - 18, C.ink);
    drawText("NUTRIMATIC", P.x + ((P.w - 39) / 2 | 0), my + 22, C.ink);
    hline(P.x + ((P.w - 18) / 2 | 0), my + 31, 18, C.greyLight);
  }
  function drawClock(cx, cy, h) {
    rect(cx - 7, cy - 6, 17, 17, "rgba(0,0,0,0.18)");
    rect(cx - 8, cy - 8, 17, 17, "#f6f4ee"); outline(cx - 8, cy - 8, 17, 17, C.ink);
    px(cx, cy - 6, C.ink); px(cx, cy + 6, C.ink); px(cx - 6, cy, C.ink); px(cx + 6, cy, C.ink);
    var hr = (h % 12) / 12 * Math.PI * 2, mn = (h % 1) * Math.PI * 2;
    for (var i = 1; i <= 3; i++) { px(cx + Math.round(Math.sin(hr) * i), cy - Math.round(Math.cos(hr) * i), C.ink); }
    for (var j = 1; j <= 5; j++) { px(cx + Math.round(Math.sin(mn) * j), cy - Math.round(Math.cos(mn) * j), C.red); }
    px(cx, cy, C.ink);
  }
  function wallColours(h) {
    var n = nightAmount(h), d = duskAmount(h) * (1 - n * 0.6);
    var a = mix(mix(C.wall, C.wallDusk, 0.2 * d), C.wallNight, 0.62 * n), b = mix(mix(C.wallD, C.wallDusk, 0.24 * d), "#141830", 0.66 * n);
    return [a, b];
  }
  function drawRoom(h) {
    var wc = wallColours(h), band = Math.ceil((DESK_Y - CEIL) / 6);
    for (var i = 0; i < 6; i++) { rect(0, CEIL + i * band, W, band, mix(wc[0], wc[1], i / 5)); }
    rect(0, 0, W, CEIL - 2, C.ceil); hline(0, CEIL - 2, W, C.ceilL); hline(0, CEIL - 1, W, mix(C.ceilL, wc[0], 0.5));
    hline(0, DESK_Y - 22, W, mix(wc[1], C.rail, 0.5)); hline(0, DESK_Y - 21, W, mix(wc[0], C.white, 0.25));   // chair rail
    rect(0, DESK_Y - 8, W, 8, mix(wc[1], "#000000", 0.22));
    drawPoster(L.poster); drawClock(L.clock.x, L.clock.y, h);
  }
  function drawPendant(on) {
    var x = L.pendant;
    vline(x, CEIL - 2, 16, C.cord); vline(x + 1, CEIL - 2, 16, C.ink3);
    for (var r = 0; r < 8; r++) { hline(x - 3 - r, 20 + r, 8 + r * 2, C.pendant); }
    hline(x - 11, 28, 24, "#0e0e10");
    hline(x - 9, 27, 20, on ? C.pendantIn : C.pendantOff); rect(x - 2, 29, 6, 2, on ? C.bulb : C.grey);
    px(x - 7, 22, C.ink3); px(x - 6, 23, C.ink3);
  }

  /* ---------- the generated room (assets/desk): the poster's mark and the clock's hands are drawn on it ---------- */
  function applyArt() { if (layoutName) { WIN = ENV.ready ? L.art.win : L.win; makeStars(); } }
  function drawPosterArt() {
    var P = L.art.poster, mx = P.x + ((P.w - 22) / 2 | 0), my = P.y + (P.h > 55 ? 13 : 9);
    for (var r = 0; r < NU.length; r++) { for (var i = 0; i < NU[r].length; i++) { if (NU[r][i] === "w") { rect(mx + i * 2, my + r * 2, 2, 2, C.ink); } } }
    if (P.mark) { hline(mx, my + 16, 22, C.ink); return; }                // on the phone his hair would cut the word: the mark alone
    hline(P.x + 8, my + 16, P.w - 16, C.ink);
    drawText("NUTRIMATIC", P.x + ((P.w - 39) / 2 | 0), my + 22, C.ink);
    hline(P.x + ((P.w - 18) / 2 | 0), my + 31, 18, C.greyLight);
  }
  function drawClockArt(h) {
    var K = L.art.clock, cx = K.x, cy = K.y, r = K.r - 1;
    for (var dy = -r; dy <= r; dy++) { var half = Math.floor(Math.sqrt(r * r - dy * dy)); hline(cx - half, cy + dy, half * 2 + 1, "#f6f4ee"); }
    px(cx, cy - r + 1, C.ink); px(cx, cy + r - 1, C.ink); px(cx - r + 1, cy, C.ink); px(cx + r - 1, cy, C.ink);
    var hr = (h % 12) / 12 * Math.PI * 2, mn = (h % 1) * Math.PI * 2;
    for (var i = 1; i <= 3; i++) { px(cx + Math.round(Math.sin(hr) * i), cy - Math.round(Math.cos(hr) * i), C.ink); }
    for (var j = 1; j <= r - 1; j++) { px(cx + Math.round(Math.sin(mn) * j), cy - Math.round(Math.cos(mn) * j), C.red); }
    px(cx, cy, C.ink);
  }
  // Midtown through the window: the generated skyline by day, its lit-up twin by night (crossfaded at dusk), and the
  // red aircraft lights on the tallest tops, blinking (Empire State, Chrysler, One Vanderbilt and two more; in the
  // skyline picture's own pixels).
  var AIRCRAFT = [[16, 36], [80, 33], [94, 24], [123, 38], [110, 47]];
  function drawSkylineArt(h, f) {
    var A = L.art, n = clamp(nightAmount(h) * 1.25, 0, 1);
    g.save(); g.beginPath(); g.rect(WIN.x, WIN.y, WIN.w, WIN.h); g.clip();
    if (n < 1) { g.drawImage(ENV.img["sky-day"], A.sky.x, A.sky.y); }
    if (n > 0) { g.globalAlpha = n; g.drawImage(ENV.img["sky-night"], A.sky.x, A.sky.y); g.globalAlpha = 1; }
    if (n > 0.4 && (f % 18) < 9) { for (var i = 0; i < AIRCRAFT.length; i++) { px(A.sky.x + AIRCRAFT[i][0], A.sky.y + AIRCRAFT[i][1], C.beacon); } }
    g.restore();
  }
  // The anglepoise lamps stand on the desk at the outer sides, heads over each one's work: Cole's red on his left,
  // Ilinca's white (the same lamp, mirrored) on her right. On when it is dark, or when the owner solders or writes.
  // The picture is 43x47: base centred at x 9.5, the inside of the shade at (34..36, 10..13), its mouth at (39, 14).
  var BULB = [[36, 10], [35, 11], [36, 11], [35, 12], [36, 12], [34, 13], [35, 13], [36, 13]];
  function lampGeom(i) { var bx = L.art.lamps[i], flip = i === 1; return { x: flip ? bx - 33 : bx - 9, y: DESK_Y - 43, mx: flip ? bx - 30 : bx + 30, my: DESK_Y - 29, flip: flip }; }
  function lampIsOn(i, h) { var p = people[i]; return !p.hidden && (isDark(h) || p.activity === "solder" || p.activity === "write"); }
  function slantCone(q, strength, overlay, w1) {
    var y0 = q.my, y1 = DESK_Y + 6, x1 = q.mx + (q.flip ? -24 : 24);
    if (overlay) { g.save(); g.globalCompositeOperation = "overlay"; }
    for (var y = y0; y < y1; y++) {
      var t = (y - y0) / (y1 - y0), cx = Math.round(lerp(q.mx, x1, t)), half = Math.round(lerp(2, w1 || 24, t));
      rect(cx - half, y, half * 2, 1, "rgba(255,214,150," + ((overlay ? 0.9 - t * 0.25 : 1) * strength).toFixed(3) + ")");
    }
    if (overlay) { g.restore(); }
  }
  function drawLampsArt(h) {
    for (var i = 0; i < 2; i++) {
      var q = lampGeom(i), im = ENV.img[i === 0 ? "lamp-red" : "lamp-white"], on = lampIsOn(i, h);
      if (on && !isDark(h)) { slantCone(q, 0.10, false, 20); }                 // by day a working lamp shows only faintly
      if (q.flip) { g.save(); g.translate(q.x + im.width, q.y); g.scale(-1, 1); g.drawImage(im, 0, 0); g.restore(); } else { g.drawImage(im, q.x, q.y); }
      if (on) { drawBulb(q); }
    }
  }
  function drawBulb(q) { for (var k = 0; k < BULB.length; k++) { px(q.flip ? q.x + 42 - BULB[k][0] : q.x + BULB[k][0], q.y + BULB[k][1], C.bulb); } }

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
  function drawWindowView(h, f) {     // the sky and the skyline, inside the frame
    var sky = skyFor(h), bands = 8, dark = isDark(h);
    for (var i = 0; i < bands; i++) { rect(WIN.x, WIN.y + Math.round(i * WIN.h / bands), WIN.w, Math.ceil(WIN.h / bands) + 1, mix(sky[0], sky[1], i / (bands - 1))); }
    rect(WIN.x, WIN.y + WIN.h, WIN.w, 2, mix(sky[0], sky[1], 1));
    if (dark) {
      for (var s = 0; s < stars.length; s++) { var st = stars[s]; if (((f >> 3) + st.p) % 7 !== 0) { px(WIN.x + st.x, WIN.y + st.y, C.star); } }
      var mx = WIN.x + 8 + Math.round(((h + 3) % 24) / 24 * (WIN.w - 22)), my = WIN.y + 8;
      rect(mx, my, 6, 6, C.moon); px(mx, my, sky[0]); px(mx + 5, my, sky[0]); px(mx, my + 5, sky[0]); px(mx + 5, my + 5, sky[0]); rect(mx + 3, my + 1, 3, 3, mix(C.moon, sky[0], 0.35));
    } else {
      var sx = WIN.x + 4 + Math.round(Math.min(1, Math.max(0, (h - 6) / 13)) * (WIN.w - 14)), sy = WIN.y + 5 + Math.round(Math.abs((h - 12.5) / 6.5) * 20);
      rect(sx, sy, 6, 6, C.sun); px(sx, sy, sky[0]); px(sx + 5, sy, sky[0]); px(sx, sy + 5, sky[0]); px(sx + 5, sy + 5, sky[0]);
      for (var c = 0; c < clouds.length; c++) { var cl = clouds[c]; var cx = WIN.x + ((cl.x + f / 20) % (WIN.w + cl.w)) - cl.w, cw = cl.w; if (cx < WIN.x) { cw -= WIN.x - cx; cx = WIN.x; } if (cx + cw > WIN.x + WIN.w) { cw = WIN.x + WIN.w - cx; } if (cw > 2) { hline(cx + 1, WIN.y + cl.y, cw - 2, C.cloud); hline(cx, WIN.y + cl.y + 1, cw, C.cloud); hline(cx, WIN.y + cl.y + 2, cw, C.cloudS); } }
    }
    if (ENV.ready) { drawSkylineArt(h, f); return; }
    var by = WIN.y + WIN.h - 4;
    for (var a = 0; a < FAR.length; a++) { drawBuilding(FAR[a], WIN.x, by - 2, dark, f, true); }
    for (var b = 0; b < NEAR.length; b++) { drawBuilding(NEAR[b], WIN.x, by, dark, f, false); }
    rect(WIN.x, by, WIN.w, 4, dark ? "#06071a" : mix(sky[1], "#3a4252", 0.7));                 // the river line
    if (dark) { for (var r = 0; r < WIN.w; r += 4) { if (hash(r, 1, f >> 4) % 3 === 0) { px(WIN.x + r + 1, by + 1, mix(C.winLit, "#06071a", 0.5)); } } }
  }
  function drawWindowFrame() {
    rect(WIN.x - 3, WIN.y - 3, WIN.w + 6, 3, C.ink); rect(WIN.x - 3, WIN.y + WIN.h, WIN.w + 6, 3, C.ink); rect(WIN.x - 3, WIN.y, 3, WIN.h, C.ink); rect(WIN.x + WIN.w, WIN.y, 3, WIN.h, C.ink);
    rect(WIN.x + (WIN.w / 2 | 0) - 1, WIN.y, 2, WIN.h, C.ink); rect(WIN.x, WIN.y + (WIN.h * 0.42 | 0), WIN.w, 2, C.ink);
    rect(WIN.x - 6, WIN.y + WIN.h + 3, WIN.w + 12, 3, C.ink2); hline(WIN.x - 6, WIN.y + WIN.h + 3, WIN.w + 12, C.ink3);
    rect(WIN.x - 5, WIN.y + WIN.h + 6, WIN.w + 10, 2, "rgba(0,0,0,0.16)");
  }
  function drawWindow(h, f) { drawWindowView(h, f); drawWindowFrame(); }
  function sillY() { return WIN.y + WIN.h + 3; }

  function drawDesk() {
    rect(0, DESK_Y, W, 5, C.deskTop); hline(0, DESK_Y, W, C.deskTopL); hline(0, DESK_Y + 4, W, C.deskTopD);
    rect(0, DESK_Y + 5, W, H - DESK_Y - 5, C.deskFront); hline(0, DESK_Y + 5, W, C.deskFrontD);
    for (var x = 30; x < W; x += 74) { vline(x, DESK_Y + 7, H - DESK_Y - 7, C.deskFrontD); }
  }
  function drawNamePlate(p) {
    var name = p.name === "cole" ? "COLE" : "ILINCA", w = textWidth(name) + 9, x = p.x - (w / 2 | 0), y = DESK_Y + 11;
    rect(x + 1, y + 2, w, 9, "rgba(0,0,0,0.3)"); rect(x, y, w, 9, C.plate); hline(x, y + 8, w, C.plateS); vline(x + w - 1, y + 1, 8, C.plateS);
    drawText(name, x + 5, y + 2, C.ink);
  }

  /* ---------- the lamp: articulated, swings over whoever is working ---------- */
  var LAMP_JOINT = 44;
  var lamp = { base: 176, hx: 184, hy: 52, tx: 184, ty: 52, on: false };
  function lampIdle() { return { x: lamp.base + 9, y: 52 }; }
  function updateLamp(h) {
    var work = null;
    if (cole.activity === "solder") { work = { x: cole.x + 26, y: DESK_Y - 47 }; }       // from the side, so the shade never hides a face
    else if (ilinca.activity === "write") { work = { x: ilinca.x - 31, y: DESK_Y - 47 }; }
    else if (cole.activity === "write") { work = { x: cole.x + 24, y: DESK_Y - 47 }; }
    var t = work || lampIdle();
    lamp.tx = t.x; lamp.ty = t.y; lamp.on = isDark(h) || !!work;
    lamp.hx += (lamp.tx - lamp.hx) * 0.18; lamp.hy += (lamp.ty - lamp.hy) * 0.18;
  }
  function drawLampCone() {
    if (!lamp.on) { return; }
    var hx = Math.round(lamp.hx), hy = Math.round(lamp.hy), top = hy + 9, bottom = DESK_Y + 5;
    for (var y = top; y < bottom; y++) { var t = (y - top) / (bottom - top), half = Math.round(lerp(9, 26, t)); rect(hx - half, y, half * 2, 1, "rgba(255,214,120,0.20)"); }
    rect(hx - 30, DESK_Y, 60, 5, "rgba(255,224,150,0.16)");
  }
  // Base and arm sit behind the figures (drawn before them); the head hangs in front (drawn after the props).
  function drawLampArm() {
    var bx = lamp.base, hx = Math.round(lamp.hx), hy = Math.round(lamp.hy), jy = LAMP_JOINT;
    limb(bx, DESK_Y - 5, bx, jy, 3, C.lampBody);
    limb(bx, jy, hx, hy, 3, C.lampBody);
    rect(bx - 2, jy - 2, 5, 5, C.lampBody); px(bx, jy, C.ink3);
  }
  function drawLampBase() { var bx = lamp.base; rect(bx - 8, DESK_Y - 4, 17, 4, C.lampBody); hline(bx - 7, DESK_Y - 5, 15, C.lampBody); hline(bx - 6, DESK_Y - 4, 13, C.ink3); }
  function drawLamp() {
    var hx = Math.round(lamp.hx), hy = Math.round(lamp.hy);
    rect(hx - 2, hy - 2, 5, 5, C.lampBody);
    var sh = lamp.on ? C.lampShadeOn : C.lampShade;
    for (var r = 0; r < 8; r++) { hline(hx - 5 - r, hy + r, 10 + r * 2, sh); px(hx - 6 - r, hy + r, C.lampBody); px(hx + 5 + r, hy + r, C.lampBody); }
    for (var k = 0; k < 6; k++) { px(hx - 4 + k, hy + 1 + k, mix(sh, C.white, 0.5)); }
    hline(hx - 5, hy - 1, 10, C.lampBody); hline(hx - 13, hy + 8, 27, C.lampBody);
    if (lamp.on) { hline(hx - 10, hy + 9, 21, C.bulb); }
  }

  /* ---------- props ---------- */
  function propVase(x, kind) {
    rect(x - 4, DESK_Y - 14, 9, 14, C.white); outline(x - 4, DESK_Y - 14, 9, 14, C.ink); hline(x - 5, DESK_Y - 15, 11, C.ink); hline(x - 2, DESK_Y - 9, 5, C.greyLight); vline(x + 2, DESK_Y - 12, 9, C.greyLight);
    vline(x, DESK_Y - 28, 13, C.stem); vline(x - 4, DESK_Y - 24, 9, C.stem); vline(x + 4, DESK_Y - 26, 11, C.stem);
    var p = kind === 0 ? C.petalR : kind === 1 ? C.petalW : C.petalY, ctr = kind === 1 ? C.petalY : C.ink;
    rect(x - 3, DESK_Y - 33, 7, 5, p); rect(x - 7, DESK_Y - 28, 5, 4, p); rect(x + 3, DESK_Y - 30, 5, 4, p); px(x, DESK_Y - 31, ctr); px(x - 5, DESK_Y - 26, ctr); px(x + 5, DESK_Y - 28, ctr);
    if (kind === 1) { outline(x - 3, DESK_Y - 33, 7, 5, C.greyLight); }
  }
  function propPlant(x) {
    rect(x - 7, DESK_Y - 10, 14, 10, C.pot); hline(x - 8, DESK_Y - 11, 16, C.potS); vline(x - 6, DESK_Y - 9, 8, C.potS); rect(x + 4, DESK_Y - 9, 2, 8, mix(C.pot, C.white, 0.3));
    rect(x - 8, DESK_Y - 20, 5, 8, C.leaf); rect(x + 4, DESK_Y - 23, 5, 11, C.greenL); rect(x - 3, DESK_Y - 29, 6, 17, C.green); rect(x - 2, DESK_Y - 32, 3, 3, C.greenL);
    px(x - 7, DESK_Y - 21, C.greenL); vline(x, DESK_Y - 27, 12, C.leaf); px(x + 6, DESK_Y - 24, C.leaf);
  }
  function propPapers(x) {
    rect(x - 14, DESK_Y - 5, 28, 5, C.paper); outline(x - 14, DESK_Y - 5, 28, 5, C.paperLine); rect(x - 13, DESK_Y - 9, 27, 4, C.paper); outline(x - 13, DESK_Y - 9, 27, 4, C.paperLine); hline(x - 9, DESK_Y - 7, 14, C.greyLight);
  }
  function propBottle(x, y) {   // the Nutrimatic shaker; bottom at y
    rect(x - 5, y - 26, 11, 26, C.white); outline(x - 5, y - 26, 11, 26, C.ink); rect(x - 4, y - 31, 9, 5, C.red); hline(x - 3, y - 32, 7, C.redDeep); hline(x - 4, y - 27, 9, C.redDeep);
    rect(x - 3, y - 18, 7, 10, C.greyLight); rect(x - 1, y - 15, 3, 2, C.red); px(x, y - 13, C.red); vline(x + 3, y - 24, 4, C.greyLight);
  }
  function propCartridge(x) {
    rect(x - 8, DESK_Y - 16, 17, 16, C.white); outline(x - 8, DESK_Y - 16, 17, 16, C.ink); rect(x - 7, DESK_Y - 20, 15, 4, C.greyLight); outline(x - 7, DESK_Y - 20, 15, 4, C.ink);
    rect(x - 3, DESK_Y - 11, 7, 6, "#c9a36a"); outline(x - 3, DESK_Y - 11, 7, 6, C.ink3); px(x - 1, DESK_Y - 9, C.ink); px(x + 1, DESK_Y - 9, C.ink);
  }
  function propMug(x, y, steam, f) {   // bottom at y
    rect(x - 5, y - 11, 10, 11, C.mug); hline(x - 5, y - 11, 10, C.mugS); vline(x - 5, y - 10, 10, C.mugS); vline(x + 3, y - 10, 9, C.mugL);
    rect(x + 5, y - 9, 2, 6, C.mug); px(x + 7, y - 8, C.mug); px(x + 7, y - 5, C.mug); vline(x + 7, y - 8, 4, C.mugS);
    if (steam) { var k = (f >> 2) % 3; px(x - 2 + k, y - 14, C.smoke2); px(x + 1 - k, y - 17, C.smoke2); px(x - 1 + k, y - 20, C.smoke2); }
  }
  function steam(x, y, f) { var k = (f >> 2) % 3; px(x - 1 + k, y, C.smoke2); px(x + 2 - k, y - 3, C.smoke2); px(x + k, y - 6, C.smoke2); }
  function propSolderStation(x) {
    rect(x - 10, DESK_Y - 8, 20, 8, C.ink3); outline(x - 10, DESK_Y - 8, 20, 8, C.ink); px(x - 7, DESK_Y - 5, C.red); px(x - 4, DESK_Y - 5, C.greenL); rect(x, DESK_Y - 6, 6, 3, C.greyLight);
    rect(x + 6, DESK_Y - 20, 2, 12, C.grey); hline(x + 3, DESK_Y - 20, 8, C.grey);
  }
  function propPhoneOnDesk(x) { rect(x - 5, DESK_Y - 2, 10, 2, C.phone); hline(x - 4, DESK_Y - 2, 8, C.ink3); }
  function propPlane(x, y, dir) {   // a paper airplane pointing in dir (1 = right)
    var d = dir || 1;
    for (var i = 0; i < 9; i++) { px(x + (i - 4) * d, y, C.plane); } for (var j = 0; j < 6; j++) { px(x + (j - 3) * d, y - 1, C.plane); } for (var k = 0; k < 3; k++) { px(x + (k - 2) * d, y - 2, C.plane); }
    px(x + 4 * d, y, C.planeS); px(x - 4 * d, y + 1, C.planeS); px(x - 3 * d, y + 1, C.planeS); px(x - 2 * d, y + 1, C.planeS);
  }

  /* ---------- the characters ---------- */
  // A figure is a body in one of its poses (the whole torso with arms, hands and whatever they hold, generated as
  // one picture per pose), the head on top of it, the face frames, and for a few poses a front part that covers the
  // face (a mug at the mouth). Nothing about the arms is drawn in code.
  function makeCharacter(name, o) {
    var a = ART[name], poses = {};
    Object.keys(a.poses || {}).forEach(function (k) {
      var q = a.poses[k], props = {};
      Object.keys(q.p || {}).forEach(function (n) { props[n] = bake(q.p[n], a.pal); });
      poses[k] = { body: bake(q.b, a.pal), front: q.f ? bake(q.f, a.pal) : null, pts: q.pts || {}, props: props };
    });
    if (!poses.rest) { poses.rest = { body: bake(a.torso, a.pal), front: null, pts: {} }; }
    return {
      name: name, art: a, poses: poses, head: bake(a.head, a.pal), x: 0, activities: o.activities, restMouth: o.restMouth, headDy: o.headDy, tiltRow: o.tiltRow, workLook: o.workLook,
      tilt: 0, exprUntil: 0, nextExprAt: 60 + Math.random() * 120,
      activity: "rest", actUntil: 0, actFrame: 0, look: { x: 0, y: 0 }, lookTarget: { x: 0, y: 0 }, turn: 0, nod: 0, bob: 0, slide: 0, hidden: false,
      mouth: "neutral", brows: null, blink: 0, nextBlink: 20 + Math.random() * 40, talking: false, gesture: false, react: null, reactUntil: 0,
      phoneOnDesk: false, hold: null, drawn: null, laptopOut: false, catLift: null
    };
  }
  // headDy lowers the head on the body (Ilinca's neck read too long); tiltRow is where the head bends for a nod: rows
  // above it drop a pixel, so the face shortens as it would tipping forward, instead of the whole head moving down.
  var cole = makeCharacter("cole", { restMouth: "neutral", headDy: 0, tiltRow: 28, workLook: { type: [0, 1], write: [0, 1], solder: [0, 1] }, activities: ["type", "solder", "solder", "think", "coffee", "stretch", "rest", "type", "write"] });
  var ilinca = makeCharacter("ilinca", { restMouth: "soft", headDy: 3, tiltRow: 24, workLook: { type: [-1, 1], write: [-1, 1], phone: [0, 1] }, activities: ["type", "type", "phone", "coffee", "think", "write", "write", "stretch", "rest"] });
  var people = [cole, ilinca];
  function other(p) { return p === cole ? ilinca : cole; }
  function who(n) { return n === "cole" ? cole : ilinca; }
  function midX() { return (cole.x + ilinca.x) / 2 | 0; }

  // Where the figure's sprite sits: its centre column on the character's x, its desk row on the desk top.
  function origin(p) { var a = p.art; return { x: p.x - a.centre + Math.round(p.slide), y: DESK_Y - a.desk + p.bob }; }
  function point(p, name, o) { o = o || origin(p); var q = p.art.points[name]; return { x: o.x + q[0], y: o.y + q[1] + p.headDy }; }
  function eyeY(p) { return point(p, "eye").y; }

  // Which pose an activity is drawn with. A pose the art does not have falls back to resting.
  var POSE_OF = {
    rest: "rest", type: "type", write: "write", solder: "solder", think: "think", phone: "phone", call: "call", ds: "ds", dsAway: "hide",
    stretch: "stretch", wave: "wave", highfive: "highfive", fold: "fold", "throw": "throw", shake: "shake", drink: "drink", offer: "offer",
    take: "take", rubEye: "yawn", yawn: "yawn", pet: "pet", fan: "wave", fistpump: "fist", carry: "carry", release: "highfive"
  };
  // Writing: the hand moves along the line in small steps and comes back (write1 and write2 are the write pose with
  // the hand moved one and two pixels on).
  var WRITING = ["write", "write", "write1", "write1", "write2", "write2", "write2", "write1", "write", "write", "write", "write1", "write2", "write", "write", "write"];
  function poseOf(p, f) {
    var a = p.activity, name = POSE_OF[a] || (p.poses[a] ? a : "rest");
    if (a === "coffee") { name = ((p.actFrame % 40) >= 12 && (p.actFrame % 40) < 26) ? "sip" : "mug"; }
    if (p.react === "surprise") { name = "surprise"; }
    else if (p.gesture && (a === "rest" || a === "think")) { name = "talk"; }      // a hand joins in only when it is free
    if (name === "wave" && p.poses.wave2 && ((p.actFrame >> 2) % 2)) { name = "wave2"; }
    if (name === "write" && p.poses.write1) { name = WRITING[(p.actFrame >> 1) % WRITING.length]; }
    return p.poses[name] ? name : "rest";
  }
  function posePoint(p, name) { var d = p.drawn; if (!d || !d.pose.pts[name]) { return null; } var q = d.pose.pts[name]; return { x: d.o.x + q[0], y: d.o.y + q[1] + d.jig }; }

  function drawHead(p, o) {
    var h = p.head, x = (o.x + h.x) | 0, y = (o.y + h.y + p.headDy) | 0, split = Math.max(0, Math.min(h.h, p.tiltRow - h.y)), t = p.tilt;
    if (split > 0) { g.drawImage(h.c, 0, 0, h.w, split, x, y + t, h.w, split); }
    if (split < h.h) { g.drawImage(h.c, 0, split, h.w, h.h - split, x, y + split, h.w, h.h - split); }
  }
  function drawFace(p, o, f) {
    var a = p.art, hy = o.y + p.headDy, t = p.tilt, closed = p.blink > 0 || p.mouth === "laugh" || p.mouth === "yawn";
    var lx = Math.round(p.look.x), ly = Math.round(p.look.y);
    var key = closed ? "closed" : ((ly > 0 || t > 0 ? "down" : "open") + (lx < 0 ? -1 : lx > 0 ? 1 : 0));
    pixels(a.eyes[key] || a.eyes.open0, o.x, hy + t, a.pal);
    pixels(a.brows[p.brows || (ly < 0 ? "up" : "neutral")] || a.brows.neutral, o.x, hy + t, a.pal);
    var m = p.mouth; if (m === "talk") { m = (f % 4 < 2) ? "open" : "neutral"; } if (m === "neutral") { m = p.restMouth; }
    pixels(a.mouth[m] || a.mouth.neutral, o.x, hy, a.pal);
  }

  function drawCharacter(p, f) {
    if (p.hidden) { p.drawn = null; return; }
    var o = origin(p), name = poseOf(p, f), pose = p.poses[name];
    var jig = (p.activity === "shake" && (p.actFrame % 2)) ? 1 : (p.activity === "fistpump" && ((p.actFrame >> 1) % 2)) ? -1 : 0;
    p.drawn = { o: o, pose: pose, name: name, jig: jig };
    blit(pose.body, o.x, o.y + jig);
    drawHead(p, o);
    drawFace(p, o, f);
    if (pose.front) { blit(pose.front, o.x, o.y + jig + p.headDy); }
    if (p.activity === "solder") {                                       // the iron's tip: a glow, a wisp of smoke, now and then a spark
      var tip = posePoint(p, "tip");
      if (tip) { px(tip.x, tip.y, (f % 6 < 3) ? C.ironHot : C.iron); var sm = (f >> 1) % 10; px(tip.x + (sm % 2), tip.y - 2 - sm, sm < 5 ? C.smoke : C.smoke2); if (f % 23 === 0) { px(tip.x - 1, tip.y - 1, C.sun); px(tip.x + 1, tip.y - 2, C.sun); } }
    }
  }
  // Hands, forearms and what they hold lie on the desk: that part of the pose is drawn again once the desk is there.
  function drawOnDesk(p) {
    var d = p.drawn; if (p.hidden || !d) { return; }
    g.save(); g.beginPath(); g.rect(0, DESK_Y, W, H - DESK_Y); g.clip();
    blit(d.pose.body, d.o.x, d.o.y + d.jig); if (d.pose.front) { blit(d.pose.front, d.o.x, d.o.y + d.jig + p.headDy); }
    g.restore();
  }
  // The laptop (or the paper) stays on the desk while the hands are off it: lifted for the cat, or petting her.
  function drawLaptopOut(p) {
    if (p.hidden) { return; }
    var from = p.laptopOut ? "type" : (p.catLift === "type" || p.catLift === "write") ? p.catLift : null, q = from && p.poses[from];
    if (!q || p.activity === from) { return; }
    var o = origin(p); Object.keys(q.props).forEach(function (n) { blit(q.props[n], o.x, o.y); });
  }
  // A hand petting the cat lies on her: that part of the pose (a box in the figure's coordinates) goes on again after her.
  var PET_HAND = { cole: { pet: [60, 72, 86, 100], pethead: [26, 54, 54, 74] }, ilinca: { pet: [-20, 66, 2, 88], pethead: [12, 54, 40, 70] } };
  function drawPetHand(p) {
    var d = p.drawn, box = d && PET_HAND[p.name][d.name]; if (!box || p.hidden || !actors.cat) { return; }
    g.save(); g.beginPath(); g.rect(d.o.x + box[0], d.o.y + box[1], box[2] - box[0], box[3] - box[1]); g.clip();
    blit(d.pose.body, d.o.x, d.o.y + d.jig); g.restore();
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
  function propArt(name, x, y) { var im = ENV.img["prop-" + name]; g.drawImage(im, Math.round(x - im.width / 2), y - im.height); }
  function drawProps(f) {
    var set = SETS[setIndex];
    if (ENV.ready) {
      for (var j = 0; j < L.art.slots.length && j < set.length; j++) {
        var kind = set[j].indexOf("vase") === 0 ? "vase" : set[j] === "cartridge" ? "papers" : set[j];
        propArt(kind, L.art.slots[j], DESK_Y + 2); if (kind === "mug") { steam(L.art.slots[j] - 1, DESK_Y - 10, f); }
      }
      if (cole.activity === "solder" && !cole.hidden) { propSolderStation(cole.x - 32); }
      if (ilinca.phoneOnDesk && !ilinca.hidden) { propPhoneOnDesk(ilinca.x - 28); }
      for (var m = 0; m < extras.length; m++) {
        var e2 = extras[m];
        if (e2.kind === "plane") { propPlane(e2.x, DESK_Y - 2, e2.dir); } else if (e2.kind === "bottle") { propArt("bottle", e2.x, DESK_Y + 2); }
        else if (e2.kind === "mug") { propArt("mug", e2.x, DESK_Y + 2); if (e2.steam) { steam(e2.x - 1, DESK_Y - 10, f); } }
      }
      return;
    }
    for (var i = 0; i < L.slots.length && i < set.length; i++) {
      var k = set[i], x = L.slots[i];
      if (k === "plant") { propPlant(x); } else if (k === "papers") { propPapers(x); } else if (k === "bottle") { propBottle(x, DESK_Y); }
      else if (k === "cartridge") { propCartridge(x); } else if (k === "mug") { propMug(x, DESK_Y, false, f); } else if (k.indexOf("vase") === 0) { propVase(x, +k[4]); }
    }
    if (cole.activity === "solder" && !cole.hidden) { propSolderStation(cole.x - 50); }
    if (ilinca.phoneOnDesk && !ilinca.hidden) { propPhoneOnDesk(ilinca.x - 28); }
    for (var e = 0; e < extras.length; e++) { var ex = extras[e]; if (ex.kind === "plane") { propPlane(ex.x, DESK_Y - 2, ex.dir); } else if (ex.kind === "bottle") { propBottle(ex.x, DESK_Y); } else if (ex.kind === "mug") { propMug(ex.x, DESK_Y, ex.steam, f); } }
  }

  /* ---------- conversation without bubbles: look at each other, talk, gesture, nod ---------- */
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
    if (p === ilinca) { p.phoneOnDesk = a !== "phone" && a !== "call"; }
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
  function faceLevel(p) { return eyeY(p); }

  /* ---------- Maker, the cat ---------- */
  // Drawn from sprites when the art has them (ART.maker: walk0/1, sit, sitside, yawn, loaf, curl, stand, knead0/1, most
  // with a ...Blink twin), otherwise as a simple grey cat. (x, y) = feet centre on the desk. She stands on the desk top,
  // in front of their arms (CAT_Y), and blinks every second or three.
  var MAKER = ART.maker ? (function () { var out = {}; Object.keys(ART.maker).forEach(function (k) { if (k !== "pal") { out[k] = bake(ART.maker[k], ART.maker.pal); } }); return out; })() : null;
  var CAT_Y = DESK_Y + 2;
  function drawMaker(x, y, pose, dir, f, blink) {
    var d = dir || 1;
    var key = pose === "walk" ? "walk" + ((f >> 2) % 2) : pose === "knead" ? "knead" + ((f >> 2) % 2) : pose;
    if (blink && MAKER && MAKER[key + "Blink"]) { key += "Blink"; }
    if (MAKER && MAKER[key]) {
      var s = MAKER[key], ox = x - (s.w / 2 | 0), oy = y - s.h + (ART.maker[key].g || 0) + (pose === "walk" && (f >> 1) % 2 ? 1 : 0);
      if (d > 0) { blit(s, ox - s.x, oy - s.y); } else { blitFlip(s, ox - s.x, oy - s.y); }
      return;
    }
    var body = C.cat, dk = C.catD, lt = C.catL, blinkNow = (f % 46) >= 42;
    if (pose === "sit" || pose === "yawn") {
      rect(x - 7, y - 17, 14, 17, body); rect(x - 8, y - 12, 16, 12, body); rect(x - 5, y - 16, 10, 3, lt); vline(x - 8, y - 11, 10, dk); hline(x - 7, y - 1, 14, dk);
      rect(x - 6, y - 27, 13, 11, body); px(x - 6, y - 29, body); px(x - 5, y - 28, body); px(x - 6, y - 28, body); px(x + 6, y - 29, body); px(x + 5, y - 28, body); px(x + 6, y - 28, body); px(x - 5, y - 27, dk); px(x + 5, y - 27, dk);
      if (pose === "yawn") { rect(x - 2, y - 22, 5, 5, C.catMouth); outline(x - 3, y - 23, 7, 7, dk); hline(x - 4, y - 24, 3, dk); hline(x + 2, y - 24, 3, dk); px(x - 1, y - 21, C.white); px(x + 1, y - 21, C.white); }
      else { rect(x - 4, y - 23, 3, 2, blinkNow ? dk : C.catEye); rect(x + 2, y - 23, 3, 2, blinkNow ? dk : C.catEye); if (!blinkNow) { px(x - 3, y - 23, C.ink); px(x + 3, y - 23, C.ink); } px(x, y - 20, C.catNose); px(x - 1, y - 19, dk); px(x + 1, y - 19, dk); }
      limb(x + 7 * d, y - 3, x + 13 * d, y - 9 + ((f >> 3) % 2), 2, dk);
    } else if (pose === "loaf") {
      rect(x - 14, y - 12, 28, 12, body); rect(x - 12, y - 14, 24, 2, body); hline(x - 10, y - 14, 18, lt); hline(x - 14, y - 1, 28, dk); vline(x - 14 * d - (d > 0 ? 0 : 1), y - 10, 9, dk);
      var hx = x + 10 * d; rect(hx - 6, y - 21, 12, 11, body); px(hx - 6, y - 23, body); px(hx - 5, y - 22, body); px(hx - 6, y - 22, body); px(hx + 5, y - 23, body); px(hx + 4, y - 22, body); px(hx + 5, y - 22, body);
      rect(hx - 4, y - 17, 3, 2, blinkNow ? dk : C.catEye); rect(hx + 1, y - 17, 3, 2, blinkNow ? dk : C.catEye); if (!blinkNow) { px(hx - 3, y - 17, C.ink); px(hx + 2, y - 17, C.ink); } px(hx - 1, y - 14, C.catNose);
      rect(x + 4 * d, y - 2, 5, 6, body); hline(x + 4 * d, y + 3, 5, dk);                              // the paw over the edge
    } else {                           // walk
      var s2 = (f >> 1) % 4;
      rect(x - 13, y - 15, 26, 9, body); hline(x - 11, y - 15, 20, lt); hline(x - 13, y - 7, 26, dk);
      var fx = x + 13 * d; rect(fx - (d > 0 ? 2 : 9), y - 20, 11, 10, body); px(fx + (d > 0 ? -1 : -8), y - 22, body); px(fx + (d > 0 ? 7 : 0), y - 22, body); px(fx + (d > 0 ? 0 : -7), y - 21, body); px(fx + (d > 0 ? 6 : -1), y - 21, body);
      rect(fx + (d > 0 ? 4 : -6), y - 17, 3, 2, C.catEye); px(fx + (d > 0 ? 5 : -5), y - 17, C.ink); px(fx + (d > 0 ? 8 : -9), y - 14, C.catNose);
      var legs = [[-10, s2 === 0 ? -1 : 0], [-6, s2 === 2 ? -1 : 0], [6, s2 === 1 ? -1 : 0], [10, s2 === 3 ? -1 : 0]];
      for (var i = 0; i < 4; i++) { rect(x + legs[i][0] * d - 1, y - 6, 3, 6 + legs[i][1], i % 2 ? dk : body); }
      limb(x - 13 * d, y - 13, x - 19 * d, y - 22 + (s2 % 2), 2, dk);
    }
  }

  /* ---------- scenarios: little scripted scenes ---------- */
  var scenario = null, nextScenarioAt = 22 * FPS, actors = {};
  function startScenario(name) {
    var sc = SCENARIOS[name]; if (!sc || (sc.when && !sc.when())) { return false; }
    if (scenario && scenario.end) { scenario.end(); }                    // (only the test hooks start one over another)
    scenario = { name: name, t0: frame, steps: sc.steps.map(function (s) { return { at: s[0], fn: s[1], done: false }; }), dur: sc.dur, update: sc.update, drawBack: sc.drawBack, drawMid: sc.drawMid, drawFront: sc.drawFront, end: sc.end };
    actors = {}; if (sc.setup) { sc.setup(); }
    people.forEach(function (p) { p.actUntil = frame + 1e6; p.gesture = false; }); convo = null;
    return true;
  }
  function stepScenario(f) {
    if (!scenario) { return; }
    var t = (f - scenario.t0) / FPS;
    scenario.steps.forEach(function (s) { if (!s.done && t >= s.at) { s.done = true; s.fn(t); } });
    if (scenario.update) { scenario.update(t, f); }
    if (t >= scenario.dur) { if (scenario.end) { scenario.end(); } scenario = null; actors = {}; people.forEach(function (p) { p.turn = 0; p.brows = p.activity === "think" ? "down" : null; p.mouth = "neutral"; p.hold = null; nextActivity(p); }); nextScenarioAt = f + (45 + Math.random() * 35) * FPS; }
  }
  function neutral(p) { p.mouth = "neutral"; p.brows = null; p.turn = 0; p.lookTarget = { x: 0, y: 1 }; }
  // Maker in a scenario: her blinks, and hands that come up off the desk while she walks past them.
  var HANDS_DOWN = { rest: 1, type: 1, write: 1, think: 1, coffee: 1 };
  function catTick(c, f) {
    if (!c.nextBlink) { c.nextBlink = f + 12 + Math.random() * 24; }
    if (f >= c.nextBlink) { c.blinkUntil = f + 2; c.nextBlink = f + 14 + Math.random() * 26; }
    c.blink = c.shut || f < (c.blinkUntil || 0);
    people.forEach(function (p) {
      if (p.hidden || p.held) { return; }
      var near = c.state === "walk" && Math.abs(c.x - p.x) < 36;
      if (near && !p.catLift && HANDS_DOWN[p.activity]) { p.catLift = p.activity; setActivity(p, "lift", 99); }
      else if (!near && p.catLift && Math.abs(c.x - p.x) > 42) { setActivity(p, p.catLift, 99); p.catLift = null; }
    });
  }
  function catEnd() { people.forEach(function (p) { if (p.catLift) { setActivity(p, p.catLift, 99); } p.catLift = null; p.held = false; p.laptopOut = false; }); }

  var SCENARIOS = {
    // Cole sneaks a game on a red DS; Ilinca notices; he puts it away.
    ds: {
      dur: 13,
      steps: [
        [0, function () { setActivity(cole, "ds", 99); faceOf(cole, { mouth: "smile", look: { x: 0, y: 1 }, turn: 0 }); }],
        [6.5, function () { faceOf(ilinca, { brows: "down", mouth: "flat" }); lookAt(ilinca, cole.x, faceLevel(cole)); }],
        [8.0, function () { faceOf(cole, { brows: "up", mouth: "o" }); lookAt(cole, ilinca.x, faceLevel(ilinca)); }],
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
      drawFront: function (t, f) {
        if (actors.clap && f - actors.clap < 6) {
          var a = posePoint(cole, "hand"), b = posePoint(ilinca, "hand"), mx = a && b ? ((a.x + b.x) / 2 | 0) : midX(), my = a && b ? ((a.y + b.y) / 2 | 0) : DESK_Y - 44;
          px(mx, my - 5, C.sun); px(mx - 5, my, C.sun); px(mx + 5, my, C.sun); px(mx, my + 5, C.sun); px(mx - 3, my - 3, C.white); px(mx + 3, my + 3, C.white); px(mx + 3, my - 3, C.white); px(mx - 3, my + 3, C.white);
        }
      }
    },
    // Cole folds a paper airplane and throws it; it lands in Ilinca's space and stays on the desk.
    airplane: {
      dur: 7.5,
      steps: [
        [0, function () { setActivity(cole, "fold", 99); faceOf(cole, { look: { x: 0, y: 1 }, turn: 0, mouth: "smile" }); }],
        [2.4, function () { setActivity(cole, "throw", 99); lookAt(cole, ilinca.x, faceLevel(ilinca)); }],
        [3.0, function () { var hand = posePoint(cole, "hand") || { x: cole.x + 32, y: DESK_Y - 44 }; setActivity(cole, "release", 99); actors.plane = { t0: frame, x0: hand.x, y0: hand.y }; }],
        [3.8, function () { faceOf(ilinca, { brows: "down", mouth: "flat" }); lookAt(ilinca, cole.x, faceLevel(cole)); setActivity(ilinca, "rest", 99); }],
        [4.0, function () { faceOf(cole, { brows: "up", mouth: "smile" }); setActivity(cole, "rest", 99); }],
        [5.5, function () { faceOf(ilinca, { brows: null, mouth: "smile" }); }]
      ],
      update: function (t, f) {
        var pl = actors.plane; if (!pl || pl.landed) { return; }
        var k = Math.min(1, (f - pl.t0) / 10), dir = ilinca.x > cole.x ? 1 : -1, x0 = pl.x0, x1 = ilinca.x - 34 * dir;
        pl.x = x0 + (x1 - x0) * k; pl.y = pl.y0 - Math.sin(k * Math.PI) * 22 + k * (DESK_Y - 2 - pl.y0);
        if (k >= 1) { pl.landed = true; extras.push({ kind: "plane", x: x1, dir: dir }); }
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
        var b = actors.bird, target = sillY() - 7;
        if (b.state === "land") { if (b.y < target) { b.y += 2; b.x -= 1; } else { b.y = target; b.state = "walk"; b.t0 = f; } }
        else if (b.state === "walk") { var k = f - b.t0; if (k % 24 < 12) { b.x += (k % 2) ? -1 : 0; } b.peck = (k % 30) >= 22; }
        else if (b.state === "fly") { b.y -= 3; b.x += 2; }
      },
      drawFront: function (t, f) {
        var b = actors.bird, x = Math.round(b.x), y = Math.round(b.y), flap = b.state !== "walk" && (f % 4 < 2), pk = b.peck ? 2 : 0;
        rect(x - 4, y, 9, 5, C.pigeon); rect(x - 6, y + 1, 3, 3, C.pigeonD); hline(x - 3, y + 4, 7, C.pigeonD);
        rect(x + 3, y - 3 + pk, 4, 4, C.pigeonL); px(x + 7, y - 2 + pk, C.sun); px(x + 5, y - 2 + pk, C.ink); hline(x + 3, y + pk, 3, "#5d8f7a");
        if (flap) { hline(x - 3, y - 2, 6, C.pigeonL); hline(x - 2, y - 3, 4, C.pigeonL); } else { hline(x - 3, y + 1, 5, C.pigeonL); }
        if (b.state === "walk") { px(x - 1, y + 5, C.sun); px(x + 2, y + 5, C.sun); }
      }
    },
    // Maker comes along the desk (hands come up as she passes), kneads a spot between them, lies down for a good
    // while and blinks at them; one of them pets her (eyes shut, content); she sits up, looks at each in turn (they
    // look back), and goes. Never while Cole is soldering.
    visit: {
      dur: 34, when: function () { return cole.activity !== "solder"; },
      setup: function () {
        var fromLeft = Math.random() < 0.5;
        actors.cat = { x: fromLeft ? -36 : W + 36, state: "walk", dir: fromLeft ? 1 : -1, spot: midX() + (fromLeft ? 3 : -3), phase: "in" };
        actors.petter = Math.random() < 0.5 ? cole : ilinca;
      },
      steps: [
        [1.5, function () { people.forEach(function (p) { p.mouth = "smile"; }); }],
        [13.0, function () { var p = actors.petter; if (p.catLift) { p.catLift = null; } p.held = true; setActivity(p, "pet", 99); p.mouth = "smile"; actors.cat.shut = true; }],
        [19.0, function () { var p = actors.petter; setActivity(p, "rest", 99); p.held = false; actors.cat.shut = false; }],
        [20.5, function () { var c = actors.cat; c.state = "sitside"; c.dir = cole.x < c.x ? -1 : 1; lookAt(cole, c.x, CAT_Y - 30); cole.mouth = "smile"; }],
        [23.0, function () { var c = actors.cat; c.dir = -c.dir; lookAt(ilinca, c.x, CAT_Y - 30); ilinca.mouth = "smile"; }],
        [25.5, function () { var c = actors.cat; c.state = "walk"; c.phase = "out"; c.dir = c.x < W / 2 ? -1 : 1; }],
        [31.0, function () { people.forEach(function (p) { neutral(p); }); }]
      ],
      update: function (t, f) {
        var c = actors.cat; catTick(c, f);
        if (c.phase === "in" && c.state === "walk") { c.x += 3 * c.dir; if ((c.dir > 0 && c.x >= c.spot) || (c.dir < 0 && c.x <= c.spot)) { c.x = c.spot; c.state = "knead"; c.kneadUntil = f + 3 * FPS; } }
        else if (c.state === "knead" && f >= c.kneadUntil) { c.state = "curl"; }
        else if (c.phase === "out") { c.x += 3 * c.dir; }
        if (t >= 1.5 && t < 30 && c.state !== "sitside") { people.forEach(function (p) { if (!p.held) { p.lookTarget = aimAt(p, c.x, CAT_Y - 14); } }); }
      },
      drawFront: function (t, f) { var c = actors.cat; drawMaker(Math.round(c.x), CAT_Y, c.state, c.dir, f, c.blink); },
      end: catEnd
    },
    // Maker picks whoever is typing or writing and sits on the laptop (on the keyboard, ears over the screen) or on
    // the paper. Hands up, a look; the other one laughs; then a scratch on the head anyway. She leaves, thinks better
    // of it, and comes back once more.
    laptop: {
      dur: 30, when: function () { return cole.activity !== "solder" && people.some(function (p) { return p.activity === "type" || p.activity === "write"; }); },
      setup: function () {
        var cands = people.filter(function (p) { return p.activity === "type" || p.activity === "write"; }), v = cands[(Math.random() * cands.length) | 0];
        var onLaptop = v.activity === "type", o = origin(v), box = onLaptop ? v.poses.type.props.laptop : v.poses.write && v.poses.write.props.paper;
        var sx = box ? o.x + box.x + (box.w / 2 | 0) : v.x, fromLeft = v === cole;
        actors.cat = { x: fromLeft ? -36 : W + 36, state: "walk", dir: fromLeft ? 1 : -1, spot: sx, phase: "in", onLaptop: onLaptop && !!box, home: fromLeft ? -40 : W + 40 };
        actors.victim = v; actors.act = v.activity; v.held = true;
      },
      steps: [],
      update: function (t, f) {
        var c = actors.cat, v = actors.victim, o = other(v); catTick(c, f);
        if (c.phase === "in" && c.state === "walk") {
          c.x += 3 * c.dir; lookAt(v, c.x, CAT_Y - 14);
          if ((c.dir > 0 && c.x >= c.spot) || (c.dir < 0 && c.x <= c.spot)) {
            c.x = c.spot; c.state = "sit"; c.since = f; c.dir = v.x < c.x ? -1 : 1;
            setActivity(v, "lift", 99); v.laptopOut = c.onLaptop; faceOf(v, { brows: "down", mouth: "flat" }); lookAt(v, c.x, DESK_Y - 34);
            lookAt(o, c.x, DESK_Y - 34); o.mouth = "laugh";
          }
        } else if (c.state === "sit") {
          var k = f - c.since;
          if (k === 18) { o.mouth = "smile"; }
          if (k === 36) { setActivity(v, v.poses.pethead ? "pethead" : "petfront", 99); faceOf(v, { brows: null, mouth: "smile" }); c.shut = true; }
          if (k === 84) { c.shut = false; c.state = "walk"; c.phase = "leave"; c.dir = c.home < c.x ? -1 : 1; c.left = f; setActivity(v, actors.act, 99); v.laptopOut = false; faceOf(v, { mouth: "neutral" }); v.lookTarget = { x: 0, y: 1 }; }
        } else if (c.phase === "leave") {
          c.x += 3 * c.dir;
          if (!c.again && f - c.left === 9) { c.again = true; c.dir = -c.dir; c.phase = "in"; faceOf(v, { brows: "up" }); }
        }
      },
      drawMid: function (t, f) { var c = actors.cat; if (c.onLaptop && c.state === "sit") { drawMaker(Math.round(c.x), DESK_Y - 3, "sit", 1, f, c.blink); } },
      drawFront: function (t, f) { var c = actors.cat; if (!(c.onLaptop && c.state === "sit")) { drawMaker(Math.round(c.x), CAT_Y, c.state, c.dir, f, c.blink); } },
      end: catEnd
    },
    // Ilinca rolls off for coffee and comes back with two mugs.
    coffee: {
      dur: 15,
      when: function () { return ilinca.activity !== "coffee" && cole.activity !== "coffee"; },
      steps: [
        [0, function () { setActivity(ilinca, "rest", 99); lookAt(ilinca, cole.x, faceLevel(cole)); ilinca.mouth = "smile"; }],
        [0.8, function () { lookAt(cole, ilinca.x, faceLevel(ilinca)); cole.nodAt = frame + 2; cole.mouth = "smile"; }],
        [1.6, function () { actors.away = { dir: ilinca.x > cole.x ? 1 : -1, phase: "out" }; }],
        [8.5, function () { actors.away.phase = "in"; setActivity(ilinca, "carry", 99); }],
        [11.5, function () { setActivity(cole, "coffee", 99); setActivity(ilinca, "coffee", 99); neutral(cole); cole.mouth = "smile"; }]
      ],
      update: function (t, f) {
        var a = actors.away; if (!a) { return; }
        var gone = (a.dir > 0 ? W - ilinca.x : ilinca.x) + 40;
        if (a.phase === "out") { if (Math.abs(ilinca.slide) < gone) { ilinca.slide += 9 * a.dir; } else { ilinca.hidden = true; } }
        else if (a.phase === "in") { ilinca.hidden = false; ilinca.slide -= 9 * a.dir; if (a.dir * ilinca.slide <= 0) { ilinca.slide = 0; a.phase = "home"; } }
      },
      end: function () { ilinca.slide = 0; ilinca.hidden = false; ilinca.hold = null; extras = extras.filter(function (e) { return e.kind !== "mug"; }); }
    },
    // Shake break: Cole mixes a bottle, drinks, passes it over.
    shake: {
      dur: 12,
      steps: [
        [0, function () { setActivity(cole, "shake", 99); faceOf(cole, { mouth: "smile", look: { x: 0, y: 0 }, turn: 0 }); }],
        [2.6, function () { setActivity(cole, "drink", 99); cole.mouth = "o"; cole.lookTarget = { x: 0, y: -1 }; }],
        // he holds it out across the gap; she reaches over and takes it while his arm is still out; then she drinks
        [4.4, function () { setActivity(cole, "offer", 99); lookAt(cole, ilinca.x, faceLevel(ilinca)); cole.mouth = "smile"; lookAt(ilinca, cole.x, faceLevel(cole)); faceOf(ilinca, { brows: "up", mouth: "smile" }); }],
        [5.5, function () { setActivity(ilinca, "take", 99); setActivity(cole, "offerEmpty", 99); ilinca.brows = null; }],
        [6.3, function () { setActivity(cole, "rest", 99); }],
        [6.9, function () { setActivity(ilinca, "drink", 99); ilinca.mouth = "o"; ilinca.turn = 0; ilinca.lookTarget = { x: 0, y: -1 }; }],
        [9.6, function () { setActivity(ilinca, "rest", 99); ilinca.mouth = "smile"; ilinca.nodAt = frame + 1; ilinca.hold = null; extras.push({ kind: "bottle", x: midX() + 22 }); }]
      ],
      end: function () { extras = extras.filter(function (e) { return e.kind !== "bottle"; }); }
    },
    // Late: a yawn passes between them.
    latenight: {
      dur: 7, when: function () { return isDark(hourNow()); },
      steps: [
        [0, function () { setActivity(cole, "yawn", 99); cole.mouth = "yawn"; cole.lookTarget = { x: 0, y: -1 }; }],
        [1.8, function () { setActivity(cole, "rubEye", 99); cole.mouth = "neutral"; }],
        [2.4, function () { lookAt(ilinca, cole.x, faceLevel(cole)); }],
        [3.2, function () { setActivity(ilinca, "yawn", 99); ilinca.mouth = "yawn"; ilinca.turn = 0; ilinca.lookTarget = { x: 0, y: -1 }; }],
        [5.0, function () { setActivity(ilinca, "stretch", 99); ilinca.mouth = "neutral"; setActivity(cole, "rest", 99); lookAt(cole, ilinca.x, faceLevel(ilinca)); cole.mouth = "smile"; }]
      ]
    },
    // A bigger spark while soldering: a puff of smoke, a startle, a hand fanning the air, then a laugh.
    spark: {
      dur: 6.5, when: function () { return cole.activity === "solder"; },
      steps: [
        [0, function () { actors.puff = { t0: frame }; }],
        [0.25, function () { faceOf(cole, { brows: "up", mouth: "o" }); cole.bob = -2; setActivity(cole, "fan", 99); }],
        [0.8, function () { lookAt(ilinca, cole.x, faceLevel(cole)); faceOf(ilinca, { brows: "down", mouth: "flat" }); }],
        [2.6, function () { lookAt(cole, ilinca.x, faceLevel(ilinca)); faceOf(cole, { brows: "up", mouth: "smile" }); cole.bob = 0; }],
        [3.6, function () { faceOf(ilinca, { brows: null, mouth: "laugh" }); faceOf(cole, { brows: null, mouth: "laugh" }); }],
        [5.2, function () { setActivity(cole, "solder", 99); cole.mouth = "neutral"; ilinca.mouth = "smile"; ilinca.turn = 0; ilinca.lookTarget = { x: 0, y: 1 }; }]
      ],
      drawFront: function (t, f) {
        var pf = actors.puff; if (!pf) { return; }
        var k = f - pf.t0, cx = cole.x + 11, cy = DESK_Y - 12;
        if (k < 3) { px(cx, cy - 3, C.sun); px(cx - 3, cy, C.sun); px(cx + 3, cy - 1, C.sun); px(cx + 1, cy - 5, C.white); px(cx - 2, cy - 4, C.white); }
        if (k < 30) { var col = k < 14 ? C.smoke : C.smoke2, r = 3 + (k >> 2); for (var i = 0; i < 4; i++) { var ox = [-3, 2, -1, 4][i] * (1 + k / 10), oy = -k * 1.5 - [0, 3, 6, 2][i]; rect(cx + Math.round(ox) - r / 2, cy + Math.round(oy) - r / 2, r, r, col); } }
      }
    },
    // The phone buzzes; good news; a fist pump.
    call: {
      dur: 11,
      when: function () { return ilinca.activity !== "phone" && ilinca.activity !== "call"; },
      steps: [
        [0, function () { actors.buzz = { t0: frame }; }],
        [1.4, function () { setActivity(ilinca, "call", 99); actors.buzz = null; ilinca.phoneOnDesk = false; faceOf(ilinca, { mouth: "talk", look: { x: 0, y: 0 }, turn: 0 }); }],
        [5.6, function () { ilinca.mouth = "smile"; ilinca.nodAt = frame + 1; }],
        [7.0, function () { setActivity(ilinca, "rest", 99); lookAt(ilinca, cole.x, faceLevel(cole)); ilinca.gesture = true; ilinca.mouth = "talk"; lookAt(cole, ilinca.x, faceLevel(ilinca)); }],
        [8.6, function () { ilinca.gesture = false; ilinca.mouth = "laugh"; setActivity(cole, "fistpump", 99); cole.mouth = "laugh"; }],
        [10.2, function () { setActivity(cole, "rest", 99); cole.mouth = "smile"; ilinca.mouth = "smile"; }]
      ],
      drawFront: function (t, f) { var b = actors.buzz; if (b && ilinca.phoneOnDesk) { var x = ilinca.x - 28 + ((f % 2) ? 1 : -1); rect(x - 5, DESK_Y - 3, 10, 2, C.phone); px(x - 7, DESK_Y - 6, C.greyLight); px(x + 7, DESK_Y - 6, C.greyLight); px(x - 9, DESK_Y - 9, C.greyLight); px(x + 9, DESK_Y - 9, C.greyLight); } }
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
    for (var i = 0; i < people.length; i++) { if (!people[i].hidden && Math.abs(s.x - people[i].x) < 32 && s.y > DESK_Y - people[i].art.desk - 4 && s.y < DESK_Y + 10) { target = people[i]; } }
    if (target) { react(target); } else { people.forEach(function (p) { p.lookTarget = aimAt(p, s.x, s.y); }); }
  });
  function aimAt(p, x, y) { var dx = x - p.x, dy = y - eyeY(p); return { x: Math.abs(dx) < 14 ? 0 : (dx < 0 ? -1 : 1), y: dy < -22 ? -1 : (dy > 30 ? 1 : 0) }; }

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

  /* ---------- light: a sun patch by day, a warm low sun at dusk, blue dark with warm pools at night ---------- */
  function drawSunPatch(h) {
    var day = (1 - nightAmount(h)) * (h > 6 && h < 19.5 ? 1 : 0); if (day <= 0.05) { return; }
    var dusk = duskAmount(h), col = dusk > 0.3 ? "rgba(255,170,90," + (0.16 * day).toFixed(3) + ")" : "rgba(255,240,200," + (0.20 * day).toFixed(3) + ")", reach = 40 + dusk * 30;
    for (var y = WIN.y + 6; y < DESK_Y; y++) { var t = (y - WIN.y) / (DESK_Y - WIN.y); rect(WIN.x - 10 - Math.round(t * reach), y, WIN.w + 6 - Math.round(t * 8), 1, col); }
  }
  function pool(cx, top, bottom, w0, w1, strength) {
    // light falling in a cone: 'overlay' warms and lifts what is lit and leaves black black; a faint haze on top
    g.save(); g.globalCompositeOperation = "overlay";
    for (var y = top; y < bottom; y++) { var t = (y - top) / (bottom - top), half = Math.round(lerp(w0, w1, t)); rect(cx - half, y, half * 2, 1, "rgba(255,214,150," + ((0.9 - t * 0.25) * strength).toFixed(3) + ")"); }
    g.restore();
    for (var y2 = top; y2 < bottom; y2++) { var t2 = (y2 - top) / (bottom - top), h2 = Math.round(lerp(w0, w1, t2)); rect(cx - h2, y2, h2 * 2, 1, "rgba(255,220,150," + (0.05 * strength).toFixed(3) + ")"); }
  }
  function drawNight(h, f) {
    var n = nightAmount(h), d = duskAmount(h) * (1 - n);
    if (ENV.ready) { drawNightArt(h, f, n, d); return; }
    if (d > 0.02) { rect(0, CEIL, W, H - CEIL, "rgba(255,150,80," + (0.10 * d).toFixed(3) + ")"); }
    if (n <= 0.02) { return; }
    rect(0, CEIL, W, DESK_Y - CEIL, "rgba(14,18,46," + (0.40 * n).toFixed(3) + ")"); rect(0, DESK_Y, W, H - DESK_Y, "rgba(14,18,46," + (0.38 * n).toFixed(3) + ")");
    drawWindow(h, f);                                                    // the city stays bright
    pool(L.pendant, 30, DESK_Y + 10, 44, 160, n * 0.32);                 // the pendant: three nested cones, so its edge is soft
    pool(L.pendant, 30, DESK_Y + 10, 26, 104, n * 0.3);
    pool(L.pendant, 30, DESK_Y + 10, 10, 52, n * 0.26);
    if (lamp.on) { pool(Math.round(lamp.hx), Math.round(lamp.hy) + 9, DESK_Y + 6, 10, 28, n * 0.4); }
    rect(0, DESK_Y, W, 2, "rgba(255,224,160," + (0.07 * n).toFixed(3) + ")");
  }

  // The generated room at night: everything but the window dims to blue (the city stays bright behind the glass);
  // each lamp that is on throws a warm slanting pool on the desk and whoever sits under it.
  function drawNightArt(h, f, n, d) {
    var tint = function (a) { return "rgba(14,18,46," + a.toFixed(3) + ")"; };
    if (d > 0.02) { rect(0, 0, W, H, "rgba(255,150,80," + (0.10 * d).toFixed(3) + ")"); }
    if (n <= 0.02) { return; }
    var a = 0.46 * n, wx = WIN.x, wy = WIN.y, ww = WIN.w, wh = WIN.h;
    rect(0, 0, W, wy, tint(a)); rect(0, wy + wh, W, H - wy - wh, tint(a)); rect(0, wy, wx, wh, tint(a)); rect(wx + ww, wy, W - wx - ww, wh, tint(a));
    rect(wx, wy, ww, wh, tint(0.12 * n));
    for (var i = 0; i < 2; i++) {
      if (!lampIsOn(i, h)) { continue; }
      var q = lampGeom(i);
      slantCone(q, n * 0.34, true, 34); slantCone(q, n * 0.30, true, 22); slantCone(q, n * 0.26, true, 12);
      slantCone(q, n * 0.05, false, 30);
    }
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
      if (p.nodAt && f >= p.nodAt) { var k = f - p.nodAt; p.nod = (k < 10) ? [0, 1, 1, 1, 0, 0, 1, 1, 1, 0][k] : 0; if (k >= 10) { p.nodAt = 0; p.nod = 0; } }
      if (pointerActive && !scenario) { p.lookTarget = aimAt(p, pointer.x, pointer.y); if (!convo && !p.react) { p.turn = p.lookTarget.x; } }
      else if (!convo && !p.react && !scenario) {
        var a = p.activity; p.turn = 0;
        if (p.workLook[a]) { p.lookTarget = { x: p.workLook[a][0], y: p.workLook[a][1] }; }
        else if (a === "think") { p.lookTarget = { x: (f >> 5) % 2 ? -1 : 1, y: -1 }; }
        else if (a === "coffee") { p.lookTarget = { x: 0, y: 0 }; }
        else { p.lookTarget = { x: ((f >> 4) + i) % 3 - 1, y: 0 }; }
      }
      p.look.x += (p.lookTarget.x - p.look.x) * 0.6; p.look.y += (p.lookTarget.y - p.look.y) * 0.6;
      if (p.blink > 0) { p.blink--; } else if (--p.nextBlink <= 0) { p.blink = 2; p.nextBlink = 24 + Math.random() * 48; }
      if (!p.react && !(scenario && scenario.name === "spark")) { p.bob = 0; }
      p.tilt = (p.nod > 0 || (p.workLook[p.activity] && !convo && !p.react && !(pointerActive && !scenario))) ? 1 : 0;
      stepExpression(p, f);
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

  // Small changes of expression between everything else, so neither of them wears one face all the time.
  var EXPRESSIONS = {
    cole: [["smile", null, 2.5, 3], ["smirk", null, 2, 2], [null, "up", 1.2, 1], ["grin", null, 1.6, 1], ["flat", "down", 1.8, 1]],
    ilinca: [["smile", null, 2.5, 3], ["smirk", null, 2, 2], ["purse", "down", 1.8, 2], [null, "up", 1.2, 1], ["grin", null, 1.6, 1], ["neutral", "sad", 1.4, 1]]
  };
  function stepExpression(p, f) {
    if (scenario || convo || p.react || p.talking) { return; }
    if (p.exprUntil && f >= p.exprUntil) { p.exprUntil = 0; p.mouth = "neutral"; p.brows = p.activity === "think" ? "down" : null; p.nextExprAt = f + (5 + Math.random() * 9) * FPS; return; }
    if (!p.exprUntil && f >= p.nextExprAt) {
      var list = EXPRESSIONS[p.name], total = 0, r, e = list[0];
      list.forEach(function (x) { total += x[3]; }); r = Math.random() * total;
      for (var i = 0; i < list.length; i++) { r -= list[i][3]; if (r <= 0) { e = list[i]; break; } }
      if (e[0]) { p.mouth = e[0]; } if (e[1]) { p.brows = e[1]; }
      p.exprUntil = f + Math.round(e[2] * FPS);
    }
  }

  function render(f) {
    var h = hourNow(), t = scenario ? (f - scenario.t0) / FPS : 0, dark = isDark(h), art = ENV.ready;
    if (art) { drawWindowView(h, f); g.drawImage(ENV.img["room-" + layoutName], 0, 0); drawPosterArt(); drawClockArt(h); drawSunPatch(h); }
    else { drawRoom(h); drawWindow(h, f); drawSunPatch(h); drawPendant(dark); drawLampArm(); }
    if (scenario && scenario.drawBack) { scenario.drawBack(t, f); }
    for (var i = 0; i < people.length; i++) { drawCharacter(people[i], f); }
    if (scenario && scenario.drawMid) { scenario.drawMid(t, f); }        // between them and the desk: a cat on a keyboard
    if (art) { g.drawImage(ENV.img["desk-" + layoutName], 0, 0); } else { drawDesk(); }
    people.forEach(drawOnDesk); people.forEach(drawLaptopOut);
    if (art) { drawLampsArt(h); } else { drawLampBase(); }
    drawProps(f);
    if (!art) { drawLampCone(); drawLamp(); }
    people.forEach(drawNamePlate);
    if (scenario && scenario.drawFront) { scenario.drawFront(t, f); }
    people.forEach(drawPetHand);
    drawNight(h, f);
    if (dark) { if (art) { for (var k = 0; k < 2; k++) { if (lampIsOn(k, h)) { drawBulb(lampGeom(k)); } } } else { drawPendant(true); drawLamp(); } }   // the bulbs glow through the dark
    blit2();
  }
  function blit2() { ctx.imageSmoothingEnabled = false; ctx.clearRect(0, 0, canvas.width, canvas.height); ctx.drawImage(off, 0, 0, canvas.width, canvas.height); }

  /* ---------- layout + sizing ---------- */
  function applyLayout(name) {
    if (name === layoutName) { return; }
    layoutName = name; L = LAYOUTS[name]; W = L.W; H = L.H; WIN = ENV.ready ? L.art.win : L.win; off.width = W; off.height = H;
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
    face: function (n, o) { var p = who(n); faceOf(p, o || {}); if (o && o.look) { p.look = { x: o.look.x, y: o.look.y }; } if (o && o.blink) { p.blink = 2; } p.actUntil = frame + 1e6; render(frame); },
    step: function (n) { for (var i = 0; i < (n || 1); i++) { frame++; update(frame); } render(frame); },
    poses: function (n) { return Object.keys(who(n).poses); },
    state: function () { return { layout: layoutName, size: [W, H], cole: cole.activity, ilinca: ilinca.activity, poses: [cole.drawn ? cole.drawn.name : null, ilinca.drawn ? ilinca.drawn.name : null], set: setIndex, hour: hourNow(), running: running, convo: !!convo, scenario: scenario ? scenario.name : null, lamp: { on: lamp.on, x: Math.round(lamp.hx) }, art: ENV.ready, lamps: [lampIsOn(0, hourNow()), lampIsOn(1, hourNow())], cat: actors.cat ? { x: Math.round(actors.cat.x), state: actors.cat.state } : null }; }
  };
})();
