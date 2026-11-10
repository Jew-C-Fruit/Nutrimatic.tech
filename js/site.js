/*
 * Nutrimatic Website - site.js
 * Version 1.7.1
 *
 * Created: 2026-09-13 - Site behaviour (v1.0.0)
 * Modified: 2026-09-15 - Scroll story takes its SVG, scrub length and still from data attributes (v1.1.0)
 * Modified: 2026-09-21 - Forms with no endpoint and no fallback address show a LinkedIn note (v1.2.2)
 * Modified: 2026-09-21 - Per-form endpoints (formEndpoints.contact / .waitlist); brand sign-ups get their own subject line (v1.3.0)
 * Modified: 2026-09-21 - Web3Forms support: access key and field names adapted per endpoint; JSON error replies count as failures (v1.4.0)
 * Modified: 2026-09-21 - sheetEndpoint: submissions also go to the Google Apps Script that fills the sheet; Web3Forms gets only the human fields, labelled (v1.5.0)
 * Modified: 2026-11-09 - App section (How it works): the scrolling Coachbot chat is scroll-linked; its row pins, the phones rise and shrink to make room for the captions, then the chat scrolls with the page (v1.6.0)
 * Modified: 2026-11-09 - App screens: also pins when the caption sits above its screen (phones); where caption and phone can't both fit, the caption rises under the nav and fades as the phone comes into view (v1.6.1)
 * Modified: 2026-11-09 - Product reveal film (splash page): silent loop; a click plays it from the start with sound, full screen (v1.7.0)
 * Modified: 2026-11-10 - Reveal film sits below the fold now: it starts loading when it comes near the screen (v1.7.1)
 *   - Mobile nav toggle
 *   - Hero media: swaps the SVG placeholder for a real render / video when present
 *   - Product reveal film (splash page): silent loop; a click plays it with sound, full screen
 *   - Optional figures that only appear when their image exists
 *   - Scroll-driven story (About page): scrubs a frame sequence (canvas) or the SVG placeholder's
 *     animations with scroll position, crossfading captions (apple.com style)
 *   - App screens that scroll (How it works): the row pins, the phones rise and shrink, the screen scrolls with the page
 *   - Waitlist role switch (owner / member / brand) synced with ?type= in the URL
 *   - Form validation + submission (JSON POST to config endpoint; mailto fallback if contactEmail is set;
 *     otherwise a note pointing to LinkedIn)
 *   - Optional analytics (Plausible or GA4) loaded from config, with a lead event on form success
 */

(function () {
  "use strict";

  var cfg = window.NUTRIMATIC_CONFIG || {};
  var reduceMotion = !!(window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches);

  /* ---------- Navigation ---------- */
  var nav = document.querySelector(".nav");
  var toggle = nav ? nav.querySelector(".nav__toggle") : null;
  if (nav && toggle) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && nav.classList.contains("is-open")) {
        nav.classList.remove("is-open");
        toggle.setAttribute("aria-expanded", "false");
        toggle.focus();
      }
    });
  }

  /* ---------- Analytics (optional, off until configured) ---------- */
  var analytics = cfg.analytics || {};
  if (analytics.plausibleDomain) {
    var pl = document.createElement("script");
    pl.defer = true;
    pl.setAttribute("data-domain", analytics.plausibleDomain);
    pl.src = "https://plausible.io/js/script.js";
    document.head.appendChild(pl);
  }
  if (analytics.ga4Id) {
    var ga = document.createElement("script");
    ga.async = true;
    ga.src = "https://www.googletagmanager.com/gtag/js?id=" + encodeURIComponent(analytics.ga4Id);
    document.head.appendChild(ga);
    window.dataLayer = window.dataLayer || [];
    window.gtag = window.gtag || function () { window.dataLayer.push(arguments); };
    window.gtag("js", new Date());
    window.gtag("config", analytics.ga4Id, { anonymize_ip: true });
  }
  function trackLead(data) {
    var props = { form: data.form, role: data.role || "" };
    try {
      if (typeof window.plausible === "function") { window.plausible("Lead", { props: props }); }
      if (typeof window.gtag === "function" && analytics.ga4Id) { window.gtag("event", "generate_lead", props); }
    } catch (err) { /* analytics must never break the form */ }
  }

  /* ---------- Small text substitutions ---------- */
  document.querySelectorAll("[data-year]").forEach(function (el) {
    el.textContent = String(new Date().getFullYear());
  });
  /* ---------- Hero media ---------- */
  var hero = document.querySelector("[data-hero-media]");
  if (hero) { setupHeroMedia(hero); }

  function setupHeroMedia(container) {
    var still = String(cfg.heroImage || "").trim();
    var video = cfg.heroVideo || {};
    var sources = [];
    if (video.webm) { sources.push({ src: String(video.webm).trim(), type: "video/webm" }); }
    if (video.mp4) { sources.push({ src: String(video.mp4).trim(), type: "video/mp4" }); }
    var img = container.querySelector("img");
    var picture = container.querySelector("picture");

    /* Placeholder: inline the SVG so its text uses the site font (an <img> can't). */
    function inlineSvg() {
      if (reduceMotion || !img || container.classList.contains("has-render") || container.classList.contains("has-video")) { return; }
      var src = img.getAttribute("src") || "";
      if (!/\.svg(\?|$)/i.test(src)) { return; }
      fetch(src).then(function (r) { return r.ok ? r.text() : Promise.reject(r.status); }).then(function (text) {
        var doc = new DOMParser().parseFromString(text, "image/svg+xml");
        var svg = document.importNode(doc.documentElement, true);
        svg.removeAttribute("width");
        svg.removeAttribute("height");
        svg.setAttribute("role", "img");
        if (img.alt) { svg.setAttribute("aria-label", img.alt); }
        var media = container.querySelector(".hero__media") || container;
        media.appendChild(svg);
        if (picture) { picture.hidden = true; }
        container.classList.add("has-inline-svg");
      }).catch(function () { /* keep the <img> */ });
    }

    function useStill() {
      if (!still || !img) { inlineSvg(); return; }
      var probe = new Image();
      probe.onerror = inlineSvg;
      probe.onload = function () {
        if (picture) {
          picture.querySelectorAll("source").forEach(function (s) { s.setAttribute("srcset", still); });
        }
        img.removeAttribute("width");
        img.removeAttribute("height");
        img.src = still;
        container.classList.add("has-render");
      };
      probe.src = still;
    }

    if (sources.length && !reduceMotion) {
      var v = document.createElement("video");
      v.muted = true;
      v.loop = true;
      v.autoplay = true;
      v.playsInline = true;
      v.setAttribute("muted", "");
      v.setAttribute("playsinline", "");
      v.setAttribute("aria-hidden", "true");
      v.hidden = true;
      if (still) { v.poster = still; }
      var failures = 0;
      sources.forEach(function (s) {
        var el = document.createElement("source");
        el.src = s.src;
        el.type = s.type;
        el.addEventListener("error", function () {
          failures += 1;
          if (failures >= sources.length) {
            v.remove();
            useStill();
          }
        });
        v.appendChild(el);
      });
      v.addEventListener("loadeddata", function () {
        v.hidden = false;
        if (picture) { picture.hidden = true; }
        container.classList.add("has-video");
        var p = v.play();
        if (p && typeof p.catch === "function") { p.catch(function () {}); }
      });
      var media = container.querySelector(".hero__media") || container;
      media.appendChild(v);
      v.load();
    } else {
      useStill();
    }
  }

  /* ---------- Product reveal film (splash page) ---------- */
  // Plays muted on a loop while it's on screen. A click on the film or its button plays it from the start with sound,
  // full screen; the end of the film or leaving full screen brings back the silent loop. With reduced motion it waits
  // for the click. Without the script the native controls stay.
  var reveal = document.querySelector("[data-reveal]");
  if (reveal) { setupReveal(reveal); }

  function setupReveal(section) {
    var video = section.querySelector("video");
    var button = section.querySelector("[data-reveal-play]");
    if (!video) { return; }
    var watching = false;
    var onScreen = true;
    video.controls = false;
    if (button) { button.hidden = false; }

    function play() {
      var p = video.play();
      if (p && typeof p.catch === "function") { p.catch(function () { /* autoplay refused: the poster and button stay */ }); }
    }
    function loop() {
      if (reduceMotion || !onScreen) { video.pause(); return; }
      video.muted = true;
      play();
    }
    function fullscreenElement() { return document.fullscreenElement || document.webkitFullscreenElement || null; }
    function enterFullscreen() {
      if (video.requestFullscreen) {
        var r = video.requestFullscreen();
        if (r && typeof r.catch === "function") { r.catch(function () {}); }
      } else if (video.webkitRequestFullscreen) {
        video.webkitRequestFullscreen();
      } else if (video.webkitEnterFullscreen) {
        video.webkitEnterFullscreen(); // iPhone: the native player
      }
    }
    function exitFullscreen() {
      if (fullscreenElement()) {
        if (document.exitFullscreen) { document.exitFullscreen().catch(function () {}); } else if (document.webkitExitFullscreen) { document.webkitExitFullscreen(); }
      } else if (video.webkitDisplayingFullscreen && video.webkitExitFullscreen) {
        video.webkitExitFullscreen();
      } else {
        stopWatching();
      }
    }
    function watch() {
      if (watching) { return; }
      watching = true;
      video.loop = false;
      video.muted = false;
      video.controls = true;
      try { video.currentTime = 0; } catch (e) { /* not seekable yet */ }
      play();
      enterFullscreen();
    }
    function stopWatching() {
      if (!watching) { return; }
      watching = false;
      video.controls = false;
      video.loop = true;
      loop();
    }

    video.addEventListener("click", function (e) {
      if (watching) { return; }
      e.preventDefault();
      watch();
    });
    if (button) { button.addEventListener("click", watch); }
    video.addEventListener("ended", function () { if (watching) { exitFullscreen(); } });
    document.addEventListener("fullscreenchange", function () { if (!fullscreenElement()) { stopWatching(); } });
    document.addEventListener("webkitfullscreenchange", function () { if (!fullscreenElement()) { stopWatching(); } });
    video.addEventListener("webkitendfullscreen", stopWatching); // iPhone
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (entries) {
        onScreen = entries[0].isIntersecting;
        if (!watching) { loop(); }
      }).observe(video);
    }
    if (!reduceMotion) {
      if ("IntersectionObserver" in window) { // the film sits below the fold: load it as it comes near
        var near = new IntersectionObserver(function (entries) {
          if (entries[0].isIntersecting) { video.preload = "auto"; near.disconnect(); }
        }, { rootMargin: "100% 0px" });
        near.observe(video);
      } else {
        video.preload = "auto";
      }
    }
    loop();
  }

  /* ---------- Optional figures (only shown if the image exists) ---------- */
  document.querySelectorAll("[data-optional-figure]").forEach(function (fig) {
    var img = fig.querySelector("img[data-src]");
    if (!img) { return; }
    var probe = new Image();
    probe.onload = function () {
      img.src = img.getAttribute("data-src");
      fig.hidden = false;
    };
    probe.src = img.getAttribute("data-src");
  });

  /* ---------- Scroll-driven story ---------- */
  var story = document.querySelector("[data-scrolly]");
  if (story) { setupScrolly(story); }

  function setupScrolly(section) {
    var visual = section.querySelector("[data-scrolly-visual]");
    var bar = section.querySelector("[data-scrolly-bar]");
    var fallback = section.querySelector(".scrolly__fallback");
    var chapters = Array.prototype.slice.call(section.querySelectorAll("[data-chapter]"));
    var seq = cfg.scrollSequence || {};
    var count = parseInt(seq.count, 10) || 0;
    var progress = 0;
    var mode = "static";
    var animations = [];
    var svgSrc = section.getAttribute("data-scrolly-src") || "assets/machine.svg";
    var SCRUB_MS = parseInt(section.getAttribute("data-scrolly-ms"), 10) || 12600; // how far into the SVG loop the scroll reaches
    var frames = [];
    var canvas = null;
    var context = null;
    var lastDrawn = -1;
    var FADE = 0.04;

    function clamp01(v) { return Math.max(0, Math.min(1, v)); }

    function renderCaptions() {
      chapters.forEach(function (el, i) {
        var start = parseFloat(el.getAttribute("data-start"));
        var end = parseFloat(el.getAttribute("data-end"));
        if (i === 0) { start -= FADE; }
        if (i === chapters.length - 1) { end += FADE; }
        var o = clamp01(Math.min((progress - start) / FADE, (end - progress) / FADE));
        el.style.opacity = o.toFixed(3);
        el.style.transform = reduceMotion ? "none" : "translateY(" + ((1 - o) * 14).toFixed(1) + "px)";
        el.classList.toggle("is-active", o > 0.5);
        el.setAttribute("aria-hidden", o > 0.5 ? "false" : "true");
      });
      if (bar) { bar.style.transform = "scaleX(" + progress.toFixed(4) + ")"; }
    }

    function renderVisual() {
      if (mode === "svg") {
        var t = progress * SCRUB_MS;
        animations.forEach(function (a) { a.currentTime = t; });
      } else if (mode === "frames") {
        drawFrame(Math.round(progress * (count - 1)));
      }
    }

    function update() {
      var rect = section.getBoundingClientRect();
      var vh = window.innerHeight || document.documentElement.clientHeight;
      if (rect.bottom < 0 || rect.top > vh) { return; }
      var total = section.offsetHeight - vh;
      progress = total > 0 ? clamp01(-rect.top / total) : 0;
      renderCaptions();
      renderVisual();
    }

    var ticking = false;
    function schedule() {
      if (ticking) { return; }
      ticking = true;
      window.requestAnimationFrame(function () { ticking = false; update(); });
    }
    window.addEventListener("scroll", schedule, { passive: true });
    window.addEventListener("resize", function () { sizeCanvas(); lastDrawn = -1; schedule(); });

    /* Placeholder: fetch the machine SVG, inline it, pause its CSS animations and scrub them. */
    function useSvg() {
      if (mode === "svg") { return; }
      fetch(svgSrc).then(function (r) { return r.ok ? r.text() : Promise.reject(r.status); }).then(function (text) {
        var doc = new DOMParser().parseFromString(text, "image/svg+xml");
        var svg = document.importNode(doc.documentElement, true);
        svg.removeAttribute("width");
        svg.removeAttribute("height");
        svg.setAttribute("aria-hidden", "true");
        svg.classList.add("scrolly__svg");
        visual.appendChild(svg);
        if (fallback) { fallback.hidden = true; }
        animations = (svg.getAnimations ? svg.getAnimations({ subtree: true }) : []).filter(function (a) {
          return !a.effect || !a.effect.getTiming || a.effect.getTiming().duration >= 1000; // leave the fast spin / dash loops running
        });
        animations.forEach(function (a) { a.pause(); });
        mode = "svg";
        update();
      }).catch(function () { /* keep the static image */ });
    }

    /* Real thing: a numbered frame sequence drawn onto a canvas. */
    function sizeCanvas() {
      if (!canvas) { return; }
      var dpr = Math.min(window.devicePixelRatio || 1, 2);
      var w = visual.clientWidth, h = visual.clientHeight;
      if (canvas.width !== Math.round(w * dpr) || canvas.height !== Math.round(h * dpr)) {
        canvas.width = Math.round(w * dpr);
        canvas.height = Math.round(h * dpr);
      }
    }

    function drawFrame(index) {
      if (!context) { return; }
      var img = frames[index];
      var probe = index;
      while (!img && probe > 0) { probe -= 1; img = frames[probe]; }   // nearest loaded earlier frame
      if (!img || probe === lastDrawn) { return; }
      lastDrawn = probe;
      var cw = canvas.width, ch = canvas.height, iw = img.naturalWidth, ih = img.naturalHeight;
      var cover = (seq.fit || "cover") !== "contain";
      var scale = cover ? Math.max(cw / iw, ch / ih) : Math.min(cw / iw, ch / ih);
      var dw = iw * scale, dh = ih * scale;
      context.clearRect(0, 0, cw, ch);
      context.drawImage(img, (cw - dw) / 2, (ch - dh) / 2, dw, dh);
    }

    function framePath(i) {
      var n = String(i);
      var pad = parseInt(seq.pad, 10) || 0;
      while (n.length < pad) { n = "0" + n; }
      return String(seq.path || "").replace("{index}", n);
    }

    function useFrames() {
      var failed = false;
      var loaded = 0;
      for (var i = 1; i <= count; i++) {
        (function (i) {
          var img = new Image();
          img.decoding = "async";
          img.onload = function () {
            frames[i - 1] = img;
            loaded += 1;
            if (mode !== "frames") {
              canvas = document.createElement("canvas");
              canvas.setAttribute("aria-hidden", "true");
              context = canvas.getContext("2d");
              visual.appendChild(canvas);
              section.classList.add("is-frames");
              if (fallback) { fallback.hidden = true; }
              mode = "frames";
              sizeCanvas();
            }
            lastDrawn = -1;
            update();
          };
          img.onerror = function () {
            if (failed) { return; }
            failed = true;
            if (mode !== "frames") { useSvg(); }
          };
          img.src = framePath(i);
        })(i);
      }
    }

    if (count > 0 && seq.path) { useFrames(); } else { useSvg(); }
    renderCaptions();
  }

  /* ---------- App section: screens that scroll with the page ---------- */
  // A column whose screen scrolls ([data-app-scroll]) pins under the nav together with the rest of its grid row.
  // While pinned, the phones rise and shrink a little so the captions fit below them, then the screen scrolls with
  // the page, then the row lets go. With reduced motion or a short window the chat scrolls by hand, as before.
  var appRow = document.querySelector("[data-app-row]");
  if (appRow && !reduceMotion) { setupAppScroll(appRow); }

  function setupAppScroll(row) {
    var GAP = 16;                         // px between the nav and the risen phone, and under the caption
    var MIN_SCALE = 0.78, MAX_SCALE = 0.92;
    var RISE = 0.35, HOLD = 0.15;         // scroll spent rising, and holding at the end, in viewport heights
    var nav = document.querySelector(".nav");
    var probe = document.createElement("div"); // 100svh: the window with the browser bars showing, so it doesn't jump
    probe.setAttribute("aria-hidden", "true");
    probe.style.cssText = "position:fixed;left:0;top:0;width:0;height:100vh;height:100svh;visibility:hidden;pointer-events:none";
    document.body.appendChild(probe);
    var cols = Array.prototype.slice.call(row.querySelectorAll(".app-col")).map(function (col) {
      var stick = col.querySelector(".app-col__stick");
      var art = stick.querySelector(".app-col__art");
      return {
        col: col, stick: stick, art: art,
        copy: Array.prototype.slice.call(stick.children).filter(function (el) { return el !== art; }),
        scroller: stick.querySelector("[data-app-scroll]")
      };
    });
    var groups = [];
    var lastW = -1, lastH = -1;

    function clamp01(v) { return Math.max(0, Math.min(1, v)); }
    function clamp(lo, hi, v) { return Math.max(lo, Math.min(hi, v)); }
    function ease(t) { return t * t * (3 - 2 * t); }
    function overflowOf(c) { return c.scroller.scrollHeight - c.scroller.clientHeight; }

    function measure() {
      // Natural sizes first: only the wrapper heights and transforms are cleared, so the page keeps its height meanwhile
      cols.forEach(function (c) {
        c.stick.style.minHeight = "";
        c.art.style.transform = "";
        c.copy.forEach(function (el) { el.style.transform = el.style.opacity = ""; });
        c.plan = null;
      });
      var vh = probe.offsetHeight || window.innerHeight;
      var navH = nav ? nav.offsetHeight : 0;
      var avail = vh - navH;
      lastW = window.innerWidth; lastH = vh;
      groups = [];
      var rows = []; // grid rows: the columns that share a top
      cols.forEach(function (c) {
        var top = c.col.offsetTop;
        var r = rows.filter(function (g) { return Math.abs(g.top - top) < 2; })[0];
        if (!r) { r = { top: top, cols: [] }; rows.push(r); }
        r.cols.push(c);
      });
      rows.forEach(function (r) {
        var driven = r.cols.filter(function (c) { return c.scroller && overflowOf(c) > 8; });
        if (avail < 420 || !driven.length) { return; }
        var c0 = r.cols[0];
        var artH = c0.art.offsetHeight;
        var stickH = Math.max.apply(null, r.cols.map(function (c) { return c.stick.offsetHeight; }));
        var room = avail - 2 * GAP;
        var g = {
          cols: r.cols, driven: driven, fade: false,
          above: c0.copy.length > 0 && c0.copy[0].offsetTop < c0.art.offsetTop,
          rise: RISE * vh, run: Math.max.apply(null, driven.map(overflowOf)), hold: HOLD * vh
        };
        if (!g.above) {
          // Caption under the screen (wide layouts): pin with the full-size phone centred, then raise and shrink it
          // until the caption fits underneath
          var copyH = Math.max.apply(null, driven.map(function (c) { return c.stick.offsetHeight - c.art.offsetHeight; }));
          g.scale = clamp(MIN_SCALE, MAX_SCALE, (room - copyH) / artH);
          g.top = navH + Math.max(GAP, (avail - artH) / 2);
          g.lift = g.top - navH - GAP;
        } else {
          // Caption above the screen (phones): pin with the heading under the nav (the rule above it tucks under). If
          // caption and phone can't both fit, the caption, read on the way in, rises under the nav and fades while the
          // phone comes fully into view, only slightly smaller
          var inset = c0.copy[0].getBoundingClientRect().top - c0.stick.getBoundingClientRect().top;
          var capH = Math.max.apply(null, driven.map(function (c) { return c.art.getBoundingClientRect().top - c.copy[0].getBoundingClientRect().top; }));
          var fit = (room - capH) / artH;
          g.top = navH + GAP - inset;
          if (fit >= MIN_SCALE) {
            g.scale = Math.min(MAX_SCALE, fit);
            g.lift = 0;
          } else {
            g.scale = clamp(MIN_SCALE, MAX_SCALE, room / artH);
            g.lift = Math.max(0, capH + g.scale * artH - room);
            g.fade = true;
          }
        }
        g.shrink = (1 - g.scale) * artH;
        g.pin = g.rise + g.run + g.hold;
        r.cols.forEach(function (c) { c.plan = { stickH: stickH, top: g.top, colH: stickH + g.pin, margin: -(g.lift + g.shrink) }; });
        groups.push(g);
      });
      cols.forEach(function (c) {
        var p = c.plan;
        c.col.classList.toggle("is-pinned", !!p);
        c.stick.style.minHeight = p ? p.stickH + "px" : "";
        c.stick.style.top = p ? p.top + "px" : "";
        c.col.style.minHeight = p ? p.colH + "px" : "";
        c.col.style.marginBottom = p ? p.margin.toFixed(1) + "px" : ""; // no empty band once the row lets go
        if (c.scroller) {
          c.scroller.setAttribute("tabindex", p ? "-1" : "0");
          if (!p) { c.scroller.scrollTop = 0; }
        }
      });
      row.classList.toggle("has-pins", groups.length > 0);
      update();
    }

    function update() {
      groups.forEach(function (g) {
        var d = Math.max(0, Math.min(g.pin, g.top - g.cols[0].col.getBoundingClientRect().top));
        var a = ease(clamp01(d / g.rise));
        var b = clamp01((d - g.rise) / g.run);
        var art = "translateY(" + (-g.lift * a).toFixed(1) + "px) scale(" + (1 - (1 - g.scale) * a).toFixed(4) + ")";
        var copy = "translateY(" + (-(g.lift + (g.above ? 0 : g.shrink)) * a).toFixed(1) + "px)";
        g.cols.forEach(function (c) {
          c.art.style.transform = art;
          c.copy.forEach(function (el) { el.style.transform = copy; el.style.opacity = g.fade ? (1 - a).toFixed(3) : ""; });
        });
        g.driven.forEach(function (c) { c.scroller.scrollTop = Math.round(b * overflowOf(c)); });
      });
    }

    var ticking = false;
    function schedule() {
      if (ticking) { return; }
      ticking = true;
      window.requestAnimationFrame(function () { ticking = false; update(); });
    }
    window.addEventListener("scroll", schedule, { passive: true });
    window.addEventListener("resize", function () {
      // phone browsers resize as their bars slide; only re-measure when the width or the small viewport changes
      if (window.innerWidth !== lastW || (probe.offsetHeight || window.innerHeight) !== lastH) { measure(); }
    });
    window.addEventListener("load", measure);
    if (document.fonts && document.fonts.ready) { document.fonts.ready.then(measure); }
    measure();
  }

  /* ---------- Waitlist role switch ---------- */
  var waitlist = document.querySelector('form[data-form="waitlist"]');
  if (waitlist) {
    var roleInputs = waitlist.querySelectorAll('input[name="role"]');
    var aliases = { owner: "owner", gym: "owner", manager: "owner", operator: "owner", member: "member", athlete: "member", brand: "brand", brands: "brand", sponsor: "brand", advertiser: "brand" };
    var wanted = aliases[String(new URLSearchParams(window.location.search).get("type") || "").toLowerCase()];
    if (wanted) {
      var pre = waitlist.querySelector('input[name="role"][value="' + wanted + '"]');
      if (pre) { pre.checked = true; }
    }
    var applyRole = function () {
      var checked = waitlist.querySelector('input[name="role"]:checked');
      var role = checked ? checked.value : "owner";
      waitlist.querySelectorAll("[data-role-copy]").forEach(function (el) {
        el.hidden = el.getAttribute("data-role-copy") !== role;
      });
      document.querySelectorAll("[data-role-only]").forEach(function (el) {
        var show = el.getAttribute("data-role-only").split(/\s+/).indexOf(role) !== -1;
        el.hidden = !show;
        el.querySelectorAll("input, textarea, select").forEach(function (input) {
          input.disabled = !show;
          if (!show) { clearError(input); }
        });
      });
      waitlist.querySelectorAll("[data-required-for]").forEach(function (input) {
        var need = input.getAttribute("data-required-for").split(/\s+/).indexOf(role) !== -1;
        if (need) { input.setAttribute("required", ""); } else { input.removeAttribute("required"); clearError(input); }
      });
      waitlist.querySelectorAll("[data-role-text]").forEach(function (el) {
        var text = el.getAttribute("data-" + role);
        if (text) { el.textContent = text; }
      });
      waitlist.querySelectorAll("[data-role-placeholder]").forEach(function (el) {
        var text = el.getAttribute("data-" + role + "-placeholder");
        if (text) { el.setAttribute("placeholder", text); }
      });
      try {
        var url = new URL(window.location.href);
        url.searchParams.set("type", role);
        window.history.replaceState(null, "", url.toString());
      } catch (err) { /* ignore */ }
    };
    roleInputs.forEach(function (r) { r.addEventListener("change", applyRole); });
    applyRole();
  }

  /* ---------- Forms ---------- */
  document.querySelectorAll("form[data-form]").forEach(function (form) {
    form.setAttribute("novalidate", "");
    form.addEventListener("submit", onSubmit);
    form.querySelectorAll(".input, .textarea").forEach(function (input) {
      input.addEventListener("input", function () { clearError(input); });
    });
  });

  function onSubmit(e) {
    e.preventDefault();
    var form = e.currentTarget;
    if (!validate(form)) { return; }

    var trap = form.querySelector('[name="_gotcha"]');
    if (trap && trap.value) { showSuccess(form, collect(form)); return; } // bots get a fake success

    var data = collect(form);
    var deliveries = plan(data);
    if (deliveries === null) { notConnected(form); return; }
    if (!deliveries.length) {
      if (String(cfg.contactEmail || "").trim()) { mailtoFallback(form, data); } else { notConnected(form); }
      return;
    }

    setBusy(form, true);
    setStatus(form, "Sending…", false);
    Promise.all(deliveries.map(function (d) {
      return send(d).then(function () { return true; }, function () { return false; });
    })).then(function (landed) {
      // The email service and the sheet are independent copies; one landing is enough.
      if (!landed.some(Boolean)) { throw new Error("nothing delivered"); }
      setStatus(form, "", false);
      showSuccess(form, data);
    }).catch(function () {
      setStatus(form, "That didn’t send. Try again, or reach us at linkedin.com/in/maisonpierre.", true);
    }).then(function () {
      setBusy(form, false);
    });
  }

  // Where a submission goes: the email service (Formspree / Web3Forms) if configured,
  // and the Google Apps Script that fills the sheet if configured. [] = nothing set up;
  // null = a configured service is missing something it needs (a Web3Forms key).
  function plan(data) {
    var list = [];
    var perForm = cfg.formEndpoints && cfg.formEndpoints[data.form];
    var endpoint = String(perForm || cfg.formEndpoint || "").trim();
    if (endpoint) {
      var payload = adaptPayload(endpoint, data);
      if (!payload) { return null; }
      list.push({ url: endpoint, body: payload, contentType: "application/json" });
    }
    var sheet = String(cfg.sheetEndpoint || "").trim();
    if (sheet) {
      // text/plain keeps the request "simple" (no preflight), which is what an Apps Script web app can answer cross-origin.
      list.push({ url: sheet, body: data, contentType: "text/plain;charset=utf-8" });
    }
    return list;
  }

  function send(d) {
    return fetch(d.url, {
      method: "POST",
      headers: { "Content-Type": d.contentType, "Accept": "application/json" },
      body: JSON.stringify(d.body)
    }).then(function (res) {
      return res.json().catch(function () { return {}; }).then(function (json) {
        // Formspree answers {ok:true}, Web3Forms {success:true}, the sheet script {ok:true}. A false flag = not delivered.
        if (!res.ok || json.ok === false || json.success === false) { throw new Error(json.message || ("HTTP " + res.status)); }
      });
    });
  }

  function validate(form) {
    var ok = true;
    var first = null;
    form.querySelectorAll("[required]").forEach(function (input) {
      if (input.disabled) { return; }
      var value = String(input.value || "").trim();
      var bad = !value;
      if (!bad && input.type === "email") {
        bad = !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(value);
      }
      if (!bad && input.type === "url") {
        if (!/^https?:\/\//i.test(value)) { value = "https://" + value; input.value = value; }
        bad = !/^https?:\/\/[^\s/]+\.[^\s/]{2,}/i.test(value);
      }
      if (bad) {
        ok = false;
        markError(input);
        if (!first) { first = input; }
      } else {
        clearError(input);
      }
    });
    if (first) { first.focus(); }
    return ok;
  }

  function markError(input) {
    var field = input.closest(".field");
    if (field) { field.classList.add("has-error"); }
    input.setAttribute("aria-invalid", "true");
  }

  function clearError(input) {
    var field = input.closest(".field");
    if (field) { field.classList.remove("has-error"); }
    input.removeAttribute("aria-invalid");
  }

  function collect(form) {
    var data = {};
    new FormData(form).forEach(function (value, key) {
      if (key === "_gotcha") { return; }
      data[key] = String(value).trim();
    });
    data.form = form.getAttribute("data-form");
    data.page = window.location.href;
    data.submitted_at = new Date().toISOString();
    if (data.form === "waitlist") {
      if (data.role === "brand") {
        data._subject = "Nutrimatic waitlist: Nutrition brand — " + (data.name || data.brand_website || "");
      } else {
        var who = data.role === "member" ? "Gym member" : "Gym owner / manager";
        data._subject = "Nutrimatic waitlist: " + who + " — " + (data.gym_name || "");
      }
    } else {
      data._subject = "Nutrimatic contact: " + (data.name || data.email || "");
    }
    return data;
  }

  function mailtoFallback(form, data) {
    var lines = [];
    Object.keys(data).forEach(function (key) {
      if (key === "_subject" || key === "form" || key === "page" || key === "submitted_at" || !data[key]) { return; }
      lines.push(key.replace(/_/g, " ") + ": " + data[key]);
    });
    var href = "mailto:" + encodeURIComponent(cfg.contactEmail || "") +
      "?subject=" + encodeURIComponent(data._subject) +
      "&body=" + encodeURIComponent(lines.join("\n"));
    showSuccess(form, data, true);
    window.location.href = href;
  }

  // Field labels for the Web3Forms notification email, in the order they should appear.
  // `email` keeps its name so Web3Forms uses it as the reply-to address.
  var EMAIL_LABELS = [
    ["name", "Name"], ["email", "email"], ["gym_name", "Gym"], ["gym_location", "Location"],
    ["brand_website", "Brand website"], ["product", "Product"], ["target_customer", "Target customer"],
    ["message", "Message"]
  ];

  // Shape the payload for the service behind the endpoint. Returns null when
  // that service needs something that isn't configured (a Web3Forms key).
  function adaptPayload(endpoint, data) {
    if (/(^|\/\/|\.)web3forms\.com\//i.test(endpoint)) {
      var keyCfg = cfg.formAccessKey;
      var key = String((keyCfg && typeof keyCfg === "object") ? keyCfg[data.form] : keyCfg || "").trim();
      if (!key) { return null; }
      // Only the human fields, labelled, so the notification email is short; the
      // subject line already says which form and which role.
      var out = { access_key: key, subject: data._subject, from_name: "Nutrimatic website" };
      EMAIL_LABELS.forEach(function (pair) { if (data[pair[0]]) { out[pair[1]] = data[pair[0]]; } });
      return out;
    }
    var copy = {};
    Object.keys(data).forEach(function (key) { copy[key] = data[key]; });
    return copy;
  }

  // Nothing configured to receive the form: say so rather than fake a send.
  function notConnected(form) {
    var status = form.querySelector(".form__status");
    if (!status) { return; }
    status.textContent = "This form isn’t connected yet. Message us on LinkedIn and we’ll add you by hand: ";
    var link = document.createElement("a");
    link.href = "https://www.linkedin.com/in/maisonpierre";
    link.rel = "noopener noreferrer";
    link.target = "_blank";
    link.textContent = "linkedin.com/in/maisonpierre";
    status.appendChild(link);
    status.classList.add("is-error");
  }

  function showSuccess(form, data, viaEmail) {
    trackLead(data);
    var fields = form.querySelector(".form__fields");
    var success = form.querySelector(".form__success");
    if (fields) { fields.hidden = true; }
    if (success) {
      success.querySelectorAll("[data-success-email]").forEach(function (el) { el.textContent = data.email || ""; });
      success.querySelectorAll("[data-success-mailto]").forEach(function (el) { el.hidden = !viaEmail; });
      success.setAttribute("data-show", "");
      success.setAttribute("tabindex", "-1");
      success.focus({ preventScroll: true });
      success.scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth", block: "center" });
    }
    form.classList.add("is-done");
  }

  function setBusy(form, busy) {
    form.classList.toggle("is-busy", busy);
    var button = form.querySelector('button[type="submit"]');
    if (button) { button.disabled = busy; }
  }

  function setStatus(form, text, isError) {
    var status = form.querySelector(".form__status");
    if (!status) { return; }
    status.textContent = text;
    status.classList.toggle("is-error", !!isError);
  }
})();
