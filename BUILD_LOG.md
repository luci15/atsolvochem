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

- 2026-10-22: Who we work with: focus blur (others blur by distance + fade, hovered name sharp and scaled), section height cut ~1069px -> ~700px, photos re-processed (denoise halftone, two-step upscale, unsharp, grain; 1920x1000). Source crops are still ~400px: real/stock photos needed for true sharpness.

## 2026-10-22 — Stock photos for "Who we work with"
Downloaded (Unsplash licence: free to use, attribution not required) and processed to 1920x1000 in images/who/:
- fragrance  — https://unsplash.com/photos/c8cdede054de (photo-1615634260167-c8cdede054de, perfume bottle)
- care       — https://unsplash.com/photos/ae84f705fc2e (photo-1636740599648-ae84f705fc2e, cosmetic bottles)
- pharma     — https://unsplash.com/photos/24d5c474f2ae (photo-1584308666744-24d5c474f2ae, blister packs)
- paint      — https://unsplash.com/photos/cdc6777db8cc (photo-1670689334799-cdc6777db8cc, industrial plant at night)
- uv         — https://unsplash.com/photos/7871176f1a7e (photo-1594055103006-7871176f1a7e, sunscreen tube)
Placeholders until the client supplies real photos.

- 2026-10-22: focus blur softened (max 2.2px, others fade to 40% and stay readable) to match the reference.

- 2026-10-22: Who we work with trimmed to the five product tabs only (Fragrance & flavours, Personal care, UV filters, Pharma & API, Paints & resins); lubricants photo/entry removed.

- 2026-10-22: card redesign. Supply steps: uniform white cards with red step number + line icon (replaces random red/black/white blocks). Strengths: ruled columns with outlined circle icons instead of boxed hex-icon cards. Stat "Pan-India" no longer wraps.

- 2026-10-22: with/without section: heading row on top, the two panels side by side (stack on <=760px).

- 2026-10-22: gallery photos are display-only: removed lightbox/click, zoom cursor and hover zoom.

- 2026-10-23: navbar button "Get a quote" -> "Contact us".

- 2026-10-23: Who we work with: focus blur is the resting state (first name sharp, others blur/fade by distance); hover moves the focus and swaps the photo; leaving returns to the first name + default photo.

- 2026-10-23: hid "The industries we know" (SHOW_SECTORS=False in tools/build.py). Replaced the horizontal step cards with a scroll-driven supply timeline: sticky intro on the left, rail on the right that fills red as you scroll, a truck rides it, each step lights up (node glows, big outlined number turns red, text fades in) when the truck reaches it. Falls back to a plain readable list without JS / reduced motion.

- 2026-10-23: Who we work with background always matches the sharp (focused) name: fragrance photo at rest, follows hover, returns to fragrance. Removed the separate default refinery photo.

- 2026-10-23: vertical timeline replaced by a horizontal parallax supply journey: section pins, a dashed road scrolls sideways under a fixed truck, red line fills behind it, nodes light as it passes; layers at different speeds (giant outlined ENQUIRE-SOURCE-STORE word 0.35x, step numbers drift 0.2x, heading fades/rises); steps alternate below/above the road; HUD counter 01/05. <=1020px and reduced motion: plain stacked list. Fixed footer hidden until closing banner (prevents bleed-through).

- 2026-10-23: supply section now replicates the reference site "What sets the reference site apart" (read from its live CSS/JS): pinned dark section, uppercase light heading with italic accent, italic lead top-right, five tilted frosted-glass cards sweeping across with scroll (--xn driven, scrub .7, 0.85x distance, 3D rotate/scale/fade by distance from centre); stacked cards below 900px / reduced motion. Font: Jost 300/400 for this section only. Replaced the neon/outlined timeline, horizontal step cards and vertical timeline (all rejected).

- 2026-10-23: supply "ask" section recoloured to the site palette: cream paper background, ink heading, brand-red accents (italic words, lead, card labels), white cards with ink-tinted shadows. Motion unchanged.

- 2026-10-23: supply "ask" section uses site typography/components (Calibri, bold headings with red italic accent, dot label, muted body, rounded white cards); Jost removed. Only the pinned sweeping tilted-card animation is borrowed from the reference site.

- 2026-10-23: fixed principal logo tiles under "Who we are" stretching tall (class clash with the old .tl timeline CSS): renamed to .tlogo, removed leftover timeline CSS, tiles 150x88.

- 2026-10-23: removed every trace of the inspiration site from the code: supply section classes/variables/comments renamed to our own (.sup, --sup-*), no reference-site naming left in HTML, CSS, JS or generator. Behaviour unchanged.

- 2026-10-23: supply sweeping cards now carry the original step content (number, line icon, title, description, tag pills) and the original intro line; only the animation is the borrowed one.

- 2026-10-24: supply section no longer vertically centred: heading starts right under the nav, cards sit just below it (track positioned against the section, top ~36%), removing the empty band above.

- 2026-10-24: supply cards: removed the skewed side edge strips and the ledge shadow; soft shadow only.

- 2026-10-24: buttons: hover animation from the reference waitlist CTA (icon chip slides right-to-left across the button while label paddings swap, size constant, 500ms, darker bg + shadow). Strength cards ("Why A T Solvochem" + About): tall dark tiles with index 01-04, red rounded-square icon top-right, text at bottom; hover fills red from the bottom, icon turns white, card lifts.

- 2026-10-24: stats: odometer counters (each digit wheel spins two full turns and settles, right digit last; replays every time the stats scroll into view); "Pan-India" letters scramble then settle. Final numbers are in the HTML for no-JS/reduced motion. Ways to buy: three panels in a row, hovered/focused/tapped one widens to show text, tags and button, others fold to number + title + plus icon; stacked and all open on <=900px.

- 2026-10-24: home gallery rebuilt as a 3D scroll scene using the reference site's own keyframes (read from its compiled Framer code): stage starts scaled 0.7 offset (-300,-400) and slides in while the 3D space (perspective 800) zooms x2; then the 7 photo frames (each with a back face) spread from a centre cluster to a scattered collage while the whole plane flips 180deg on X and the space settles at x1.5; main photo at z150 scale .5. Scroll-linked, scrub 1 + Lenis. Desktop only (>1020px, motion allowed); photo columns otherwise. Fixed: section overflow:hidden broke position:sticky -> overflow:clip.

- 2026-10-24: gallery 3D frames now use each photo's own shape (3:4 portrait, 1:1 square; main 3:4) with focus near the top, so faces are no longer cropped.

- 2026-10-24: gallery 3D: frames back to the reference shapes (16:9 / 4:3 / 3:4, main 16:10); photos re-assigned (square group shots in landscape slots, portraits in portrait slots) and each crop aimed at where the faces sit (per-photo face height -> computed object-position), so shapes crop but faces stay in.

- 2026-10-24: "View gallery" button moved below the 3D gallery (centred) and made clickable: the 3D stage overlapped it, so the stage now ignores pointer events.

- 2026-10-24: removed the letter scramble on "Pan-India"; only the numeric stats roll.

- 2026-10-24: red closing banner: square bottom corners, removing the light gaps where it meets the footer.

- 2026-10-25: Products split: products.html shows only the five category cards (photo, description, count) plus a search across all 557 chemicals (results tagged by category); each category has its own page products-<id>.html (breadcrumb, hero photo, count, in-page search, full list, links to the other four). All home links point to the category pages; old products.html#cat links redirect. Sitemap updated.

- 2026-10-25: reverted the showcase/explorer products page (user preferred the previous one): back to the 5 category cards + search, with category pages.

- 2026-10-25: products hero text was clipped: the search toolbar used margin-top:-84px, pulling the cream page body over the intro. Toolbar now sticks at top:84px with no negative margin; background only on the bar.

- 2026-10-25: cache-busting: css/js links carry ?v=<md5 of site.css+site.js> (ASSET_V in tools/build.py) so browsers never show stale styles after an update.

- 2026-10-25: navbar links get a 6px gap so hover and active pills do not touch.

- 2026-10-25: category pages revamped: chemicals grouped under big A-Z letter headings as cards (name, Enquire link, + add button); sticky bar with search, A-Z jump strip (letters with no match dimmed); enquiry list - add several chemicals, floating bar sends one enquiry with all names (sessionStorage). Landing page search unchanged.

- 2026-10-25: category page header compacted (title one line ~56px, small 16:9 photo, tighter paddings) so chemical cards start in the first screen.

- 2026-10-25: category header resized to a middle size (title up to 80px two lines, photo 16:10 about 520px wide).

- 2026-10-25: inner page header top padding reduced (about 100-118px, was 130-180px) on products, about, principals, gallery, careers, contact.

- 2026-10-25: About page rebuilt with scroll animation throughout: full-height hero (parallax plant photo, line-reveal headline, text drifts away on scroll); story with sticky heading + word-by-word scrubbed paragraph; odometer stats band; mission/vision stacked cards (vision slides over, mission scales back); strengths cards; two opposite-direction feature marquees (solid + outlined); On the ground photos with clip-path reveals and parallax at different speeds; principals logo marquee; red closer. Content only from brochure facts.

- 2026-10-25: footer v2: big email headline with sliding red underline + rotating arrow, Contact us / WhatsApp, five columns (brand + Facebook, Explore, Products -> category pages, Visit + Open in Maps, Call & write), giant faint wordmark (hidden on short screens), bottom bar with Back to top. Link hover: red dot + slide. Fixed reveal-under-page footer now measures itself with ResizeObserver (it was clipped when fonts changed its height) and is skipped if taller than the screen.

- 2026-10-25: About page vertical padding reduced by about 35-40% on every section.

- 2026-10-25: principal logos: tile boxes removed everywhere (home marquee, about, principals grid); white backgrounds baked out of images/principals/*.webp (alpha) so logos sit straight on the cream page.
