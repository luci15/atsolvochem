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

- 2026-10-21: Home page 'Product families' (6 cards) replaced with the 12-tile product category table (Ff, Ch, Ap...). Source of truth: tools/build.py (PT list); styles in css/site.css (.ptable/.pt). Tiles link to closest products.html#category (fragrance/care/pharma/paint) or the full searchable list. Archivo + IBM Plex Mono fonts loaded on index.html only. Pulled 12 newer commits (Vercel build) from origin/main first. Not pushed.

- 2026-10-21: Removed 'All' tab on Products (first category shows by default; searching still spans all categories). Calibri (Carlito fallback) site-wide incl. headings, bold headings, body 18px; old fonts removed. Navbar: Careers page added (careers.html, in build.py + sitemap), Contact removed from navbar (kept in footer; 'Get a quote' button -> contact.html). Not pushed.
- 2026-10-21: 'Ways to buy' cards: Request a quote pills sized to content and centred at card bottom (css .bcard .btn). Not pushed.
- 2026-10-21: Home hero footer 'Thane, Mumbai' -> 'Mumbai'; rewrote the philosophy paragraph (build.py, .phil). Not pushed.
- 2026-10-21: Industries ('What we do') accordion is now scroll-driven on desktop: section pins, each scroll step closes the open item, opens the next, picture cross-fades (js/site.js accordion block + .ind-pin css). Click on a row scrolls to its step. Mobile/tablet/reduced-motion keep plain click accordion. Not pushed.
- 2026-10-21: Closer 'or WhatsApp us' link: hover no longer turns red-on-red (stays white + underline). Click opens wa.me in a new tab (verified). Not pushed.

- 2026-10-22: industries preview is a plain rounded rectangle (no hexagon); hovering a row opens it + swaps picture on top of the scroll-driven pin (scroll updates ignored unless progress actually changes, so hover and refresh do not fight).

- 2026-10-22: tagline "A Chemicals & Solvents Hub" under brand (nav+footer); hero/footer location -> Mumbai, India; removed "Five ways we supply" heading; polished Who we are (statement + sub paragraph + About button). "The chemistry we move" section was already replaced by the 12-category table.

- 2026-10-22: no hexagon pictures anywhere (trust logos, About image, Products category thumbnails now rounded rectangles; industries already). Twelve-category tile section hidden via SHOW_CATEGORY_TABLE=False in tools/build.py.

- 2026-10-22: navbar rebuilt after Evermind: full-width bar (32px margins, 60px high, radius 16, solid cream) at top; compresses to a centred 900px pill with shadow after 40px scroll, expands again at top (width transition .75s). Links centred in a 3-column grid; no more hide-on-scroll. Below 1021px: hamburger + dropdown.

- 2026-10-22: industries accordion replaced by "Who we work with" (Bailey Hart reference): full-bleed photo (images/who, upscaled+softened from low-res brochure crops), big centred white names, hover swaps photo + dims others, mouseleave returns to default. Needs real high-res photos to look sharp.
