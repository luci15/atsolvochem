# Build log

## 2026-10-15 — Full redesign and rebuild (pushed to main)
- Replaced Bootstrap-era template (css/, js/, old/backup pages, stock images, product.json) with a new design system and 7 pages.
- New: Principals (22 logos, home marquee), Gallery (6 exhibition photos, lightbox), searchable Products page (557 chemicals, per-chemical enquiry link), About with mission/vision from brochure, 404, robots.txt, sitemap.xml.
- email1.php: POST-only, header-injection safe, honeypot, validated email, Reply-To, redirects with ?sent=1/0.
- .htaccess: 404 doc, gzip, cache headers, .md files denied.
- Verified in headless Chrome (desktop 1360 + 390px no horizontal overflow); product filter/search tested; no console errors. Mail sending untested locally (needs server).

## 2026-10-15 — Immersive v2 (scroll-driven)
- Reference: evermind.framer.website. Rebuilt CSS/JS/generator: floating pill nav, sticky hero + curtain, Lenis smooth scroll, GSAP ScrollTrigger sections (see memory.md).
- Generator moved into repo: tools/build.py + tools/cats.json. Vendored GSAP/ScrollTrigger/Lenis.
- Verified in browser: hero curtain, stacked panels, emerge, horizontal pin, footer reveal, product search; no console errors; no horizontal overflow at 390px on all 6 pages.
- Not done: real hero footage; per-section reference matching (awaiting references).

## 2026-10-15 — v3 sections from Palladio + Bailey Hart references
- Added: industries accordion (native details, GSAP height, hex image crossfade), product-family cards (?q= prefilled product search), sectors list, with/without comparison, ways-to-buy cards, FAQ accordion, tick chips in dark section. Removed stacked panels.
- Fixed: scroll-reveal items staying hidden when page loaded/jumped past them (whenIn helper).
- Verified with real scroll harness: all new sections render; accordion open/close + image swap; no console errors.

- 2026-10-15: type scale reduced (~25-30% on display sizes), trust-row hex logos enlarged (96px).

- 2026-10-15: fixed pinned horizontal section cropping on short viewports (min-height removed, compact head/steps).

- 2026-10-15: industries accordion opens on hover (desktop mouse) with picture swap; click still works; touch/mobile click only.
