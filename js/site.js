/*
 * Nutrimatic Website - site.js
 * Version 1.4.0
 *
 * Created: 2026-09-13 - Site behaviour (v1.0.0)
 * Modified: 2026-09-15 - Scroll story takes its SVG, scrub length and still from data attributes (v1.1.0)
 * Modified: 2026-09-21 - Forms with no endpoint and no fallback address show a LinkedIn note (v1.2.2)
 * Modified: 2026-09-21 - Per-form endpoints (formEndpoints.contact / .waitlist); brand sign-ups get their own subject line (v1.3.0)
 * Modified: 2026-09-21 - Web3Forms support: access key and field names adapted per endpoint; JSON error replies count as failures (v1.4.0)
 *   - Mobile nav toggle
 *   - Hero media: swaps the SVG placeholder for a real render / video when present
 *   - Optional figures that only appear when their image exists
 *   - Scroll-driven story (About page): scrubs a frame sequence (canvas) or the SVG placeholder's
 *     animations with scroll position, crossfading captions (apple.com style)
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
    var perForm = cfg.formEndpoints && cfg.formEndpoints[data.form];
    var endpoint = String(perForm || cfg.formEndpoint || "").trim();
    var payload = endpoint ? adaptPayload(endpoint, data) : null;
    if (!endpoint || !payload) {
      if (!endpoint && String(cfg.contactEmail || "").trim()) { mailtoFallback(form, data); } else { notConnected(form); }
      return;
    }

    setBusy(form, true);
    setStatus(form, "Sending…", false);
    fetch(endpoint, {
      method: "POST",
      headers: { "Content-Type": "application/json", "Accept": "application/json" },
      body: JSON.stringify(payload)
    }).then(function (res) {
      return res.json().catch(function () { return {}; }).then(function (json) {
        // Formspree answers {ok:true}; Web3Forms {success:true}. Either flag false = not delivered.
        if (!res.ok || json.ok === false || json.success === false) { throw new Error(json.message || ("HTTP " + res.status)); }
        setStatus(form, "", false);
        showSuccess(form, data);
      });
    }).catch(function () {
      setStatus(form, "That didn’t send. Try again, or reach us at linkedin.com/in/maisonpierre.", true);
    }).then(function () {
      setBusy(form, false);
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

  // Shape the payload for the service behind the endpoint. Returns null when
  // that service needs something that isn't configured (a Web3Forms key).
  function adaptPayload(endpoint, data) {
    var out = {};
    Object.keys(data).forEach(function (key) { out[key] = data[key]; });
    if (/(^|\/\/|\.)web3forms\.com\//i.test(endpoint)) {
      var keyCfg = cfg.formAccessKey;
      var key = String((keyCfg && typeof keyCfg === "object") ? keyCfg[data.form] : keyCfg || "").trim();
      if (!key) { return null; }
      out.access_key = key;
      out.subject = data._subject;          // Web3Forms' name for the subject line
      out.from_name = "Nutrimatic website";
      delete out._subject;
    }
    return out;
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
