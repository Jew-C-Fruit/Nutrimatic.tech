/*
 * Nutrimatic Website - config.js
 * Version 1.0.2
 *
 * Created: 2026-09-13 - Site configuration (v1.0.0)
 * Modified: 2026-09-15 - contactEmail documented as fallback-only, not displayed (v1.0.1)
 * Modified: 2026-09-21 - contactEmail blank by default; forms point to LinkedIn until an endpoint is set (v1.0.2)
 *   - Edit THIS file to wire up forms and the hero media; site.js reads it.
 */

window.NUTRIMATIC_CONFIG = {
  // Where form submissions go. Any endpoint that accepts a JSON POST works
  // (Formspree, Basin, Getform, a Google Apps Script web app, your own API).
  // While this is empty (""), submitting a form shows a note pointing people
  // to the LinkedIn page instead of pretending to send.
  formEndpoint: "",

  // Optional fallback: if formEndpoint is empty but this is set, the forms
  // open the visitor's email app with the details pre-filled, addressed here.
  // Every visitor's browser downloads this file, so an address put here can
  // be scraped. Left blank on purpose; public contact is the LinkedIn link.
  contactEmail: "",

  // Real machine rendering for the splash page. Drop the still into
  // assets/renders/ and it replaces the animated SVG placeholder
  // automatically (if the file is missing, the placeholder stays).
  heroImage: "assets/renders/machine-front.jpg",

  // Rendering animation (optional). When set, the splash page plays it muted
  // and looping, with heroImage as the poster and static fallback.
  heroVideo: {
    mp4: "",   // e.g. "assets/renders/machine.mp4"
    webm: ""   // e.g. "assets/renders/machine.webm"
  },

  // Scroll-driven story on the How it works page (the apple.com-style section).
  // Export the rendering as a numbered JPEG sequence into assets/sequence/
  // (see assets/sequence/README.md), then set `count` to the number of frames.
  // With count 0, or if the frames fail to load, the section scrubs the
  // animated SVG placeholder instead.
  scrollSequence: {
    path: "assets/sequence/frame-{index}.jpg",  // {index} is replaced by the frame number
    count: 0,                                    // e.g. 120
    pad: 4,                                      // zero-padding: 4 -> frame-0001.jpg
    fit: "cover"                                 // "cover" (full-bleed) or "contain"
  },

  // Analytics. Leave both empty for none. Plausible is cookie-free (no banner
  // needed); GA4 is free but you'll want a cookie notice in the EU/UK.
  analytics: {
    plausibleDomain: "",   // e.g. "nutrimatic.tech"
    ga4Id: ""              // e.g. "G-XXXXXXXXXX"
  }
};
