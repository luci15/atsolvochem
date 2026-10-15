"""Generates the static HTML pages. Run from anywhere:  python tools/build.py
Data lives in tools/cats.json (chemical lists per category). Output goes to the repo root."""
import os, json, html, re
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(HERE)
cats = json.load(open(HERE + '/cats.json', encoding='utf-8'))
E = html.escape

# white glyph version of the mark (used on red hexagons)
if not os.path.exists(R + '/images/mark-white.png'):
    m = Image.open(R + '/images/mark.png').convert('RGBA'); px = m.load()
    for y in range(m.height):
        for x in range(m.width):
            r, g, b, a = px[x, y]
            px[x, y] = (255, 255, 255, max(0, min(255, int((min(r, g, b) - 60) * 255 / 150))) if a else 0)
    m.save(R + '/images/mark-white.png', optimize=True)

CATS = [
    ('fragrance', 'Fragrance, <em>flavours</em> &amp; aerosol', 'Fragrance, Flavours & Aerosol', 'Aroma chemicals, aldehydes, esters, solvents and intermediates for fragrance, flavour and aerosol makers.', 'fragrance.jpg', 'Fragrance & flavours'),
    ('care', 'Cosmetics &amp; <em>personal care</em>', 'Cosmetics, Personal Care & Homecare', 'Surfactants, emollients, preservatives, thickeners and actives for cosmetic, personal care and home-care formulations.', 'care.jpg', 'Personal care'),
    ('uv', 'UV <em>filters</em>', 'UV Filters', 'Organic UV filters and solubilisers for sunscreens and sun-care formulations.', 'lab.jpg', 'UV filters'),
    ('pharma', 'Pharma &amp; <em>API</em>', 'Pharma, API & Formulations', 'Solvents, reagents and intermediates for pharmaceutical, API and speciality-chemical manufacturing.', 'pharma.jpg', 'Pharma & API'),
    ('paint', 'Paints, resins &amp; <em>adhesives</em>', 'Paints, Resins, Adhesives & Dyestuff', 'Monomers, resins, solvents, plasticizers and intermediates for paint, coating, adhesive, rubber and construction industries.', 'plant.jpg', 'Paints & resins'),
]
TOTAL = sum(len(v) for v in cats.values())

PHONE_O1, PHONE_O2 = '+91 22 4924 9199', '+91 22 2580 5200'
MOB1, MOB2 = '+91 75206 62615', '+91 92235 32512'
WA = '919820662615'
MAIL1, MAIL2 = 'sales.atsolvochem@gmail.com', 'atsolvochem@gmail.com'
ADDR = '412, 4th Floor, Jaydeep Emphasis, Plot No. A-9, MIDC, Wagle Ind. Estate, near Mulund Checknaka Toll Plaza, Thane (W) 400604'
ARROW = '<i><svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M2 8h11M9 4l4 4-4 4"/></svg></i>'
WAICON = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17.5 14.4c-.3-.15-1.75-.86-2.02-.96-.27-.1-.47-.15-.67.15-.2.3-.77.96-.94 1.16-.17.2-.35.22-.64.07-.3-.15-1.25-.46-2.38-1.47-.88-.78-1.47-1.75-1.64-2.05-.17-.3-.02-.46.13-.6.13-.13.3-.35.45-.52.15-.17.2-.3.3-.5.1-.2.05-.37-.03-.52-.07-.15-.67-1.6-.92-2.2-.24-.58-.48-.5-.67-.51h-.57c-.2 0-.52.07-.8.37-.27.3-1.04 1.02-1.04 2.48s1.07 2.88 1.22 3.08c.15.2 2.1 3.2 5.08 4.49.71.3 1.26.49 1.7.63.71.23 1.36.2 1.87.12.57-.08 1.75-.72 2-1.41.25-.7.25-1.29.17-1.41-.07-.12-.27-.2-.57-.35M12.04 21.5a9.4 9.4 0 0 1-4.8-1.31l-.34-.2-3.55.93.95-3.46-.22-.36a9.4 9.4 0 0 1-1.44-5.01c0-5.2 4.24-9.44 9.45-9.44 2.52 0 4.9.98 6.68 2.77a9.37 9.37 0 0 1 2.76 6.68c0 5.2-4.24 9.4-9.45 9.4M20.5 3.5A11.3 11.3 0 0 0 12.04.1C5.8.1.73 5.17.73 11.4c0 2 .52 3.94 1.52 5.66L.62 23.4l6.5-1.7a11.3 11.3 0 0 0 5.4 1.38h.01c6.24 0 11.3-5.07 11.3-11.3 0-3.02-1.18-5.86-3.33-8"/></svg>'
NAV = [('index.html', 'Home'), ('aboutus.html', 'About'), ('products.html', 'Products'), ('principals.html', 'Principals'), ('gallery.html', 'Gallery'), ('contact.html', 'Contact')]


def tel(s):
    return s.replace(' ', '')


def page(fname, title, desc, body, og='images/industries/plant.jpg'):
    links = ''.join(f'<a href="{h}"{" aria-current=\"page\"" if h == fname else ""}>{l}</a>' for h, l in NAV)
    foot_links = ''.join(f'<li><a href="{h}">{l}</a></li>' for h, l in NAV)
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<meta name="theme-color" content="#0D0C0A">
<meta property="og:type" content="website">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:image" content="{og}">
<link rel="canonical" href="https://www.atsolvochem.com/{'' if fname == 'index.html' else fname}">
<link rel="icon" type="image/png" href="images/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Hanken+Grotesk:wght@400;500;600;700&amp;family=Instrument+Serif:ital@0;1&amp;display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/site.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="nav-pill">
<a class="brand" href="index.html" aria-label="A T Solvochem — home"><img src="images/mark.png" alt="" width="38" height="34"><b>A T Solvochem</b></a>
<nav class="nav-links" aria-label="Main">{links}</nav>
<div class="nav-right"><a class="nav-cta" href="contact.html">Get a quote</a><button class="nav-toggle" aria-expanded="false" aria-label="Open menu"><span></span><span></span><span></span></button></div>
</header>
<main id="main">
{body}
</main>
<footer class="site-footer">
<div class="wrap fgrid4">
<div class="foot-brand"><a class="brand" href="index.html"><img src="images/mark.png" alt="" width="38" height="34"><b>A T Solvochem</b></a><p>A chemical &amp; solvent hub — one stop spot for all your chemical and solvent requirements, for over two decades.</p></div>
<div><h4>Explore</h4><ul>{foot_links}</ul></div>
<div><h4>Visit</h4><address>{E(ADDR)}</address></div>
<div><h4>Contact</h4><ul>
<li><a href="tel:{tel(PHONE_O1)}">{PHONE_O1}</a></li>
<li><a href="tel:{tel(PHONE_O2)}">{PHONE_O2}</a></li>
<li><a href="tel:{tel(MOB1)}">{MOB1}</a></li>
<li><a href="mailto:{MAIL1}">{MAIL1}</a></li>
<li><a href="mailto:{MAIL2}">{MAIL2}</a></li></ul></div>
</div>
<div class="foot-mega" aria-hidden="true">Solvochem</div>
<div class="foot-bottom"><div class="wrap"><span>&copy; <span id="year">2026</span> A.T. Solvochem. All rights reserved.</span><span>Thane, Maharashtra, India</span></div></div>
</footer>
<a class="wa" href="https://wa.me/{WA}" target="_blank" rel="noopener" aria-label="Chat on WhatsApp">{WAICON}</a>
<script src="js/vendor/gsap.min.js"></script>
<script src="js/vendor/ScrollTrigger.min.js"></script>
<script src="js/vendor/lenis.min.js"></script>
<script src="js/site.js"></script>
</body>
</html>
'''


def lines(*ls):
    return ''.join(f'<span class="ln"><span>{l}</span></span>' for l in ls)


def phead(label, h1_lines, sub):
    return f'<section class="phead"><div class="wrap"><p class="label" data-r>{label}</p><h1 class="ph-line">{lines(*h1_lines)}</h1><p class="sub" data-r>{sub}</p></div></section>'


def closer(h='Let&rsquo;s talk <em>chemistry.</em>', p='Send us the chemical name, grade and quantity — we confirm availability and pricing from current stock, or source it for you.'):
    return f'''<section class="closer"><div class="hxbg" style="width:420px;left:-120px;top:-60px"></div><div class="hxbg" style="width:300px;right:-60px;bottom:-60px"></div>
<div class="wrap"><h2>{h}</h2><p>{p}</p><div class="row"><a class="btn btn--cream" href="contact.html">Send an enquiry {ARROW}</a><a class="btn btn--text" href="https://wa.me/{WA}" target="_blank" rel="noopener">or WhatsApp us &rarr;</a></div></div></section>'''


PR = [('esteem-industries', 'Esteem Industries'), ('basf', 'BASF'), ('clariant', 'Clariant'), ('godrej-industries', 'Godrej Industries'), ('arkema', 'Arkema'), ('sarex', 'Sarex'), ('galaxy-surfactants', 'Galaxy Surfactants'), ('deepak-phenolics', 'Deepak Phenolics'), ('sk-picglobal', 'SK picglobal'), ('nan-ya-plastics', 'Nan Ya Plastics'), ('dairen-chemical', 'Dairen Chemical Corp'), ('ercros', 'Ercros'), ('gacl', 'GACL'), ('luxi', 'Luxi'), ('ensign', 'Ensign'), ('kcil', 'Kairav Chemofarbe (KCIL)'), ('subhash-chemical', 'Subhash Chemical Industries'), ('samrat-pharmachem', 'Samrat Pharmachem'), ('mek', 'Mehk'), ('alg-chemicals', 'ALG Chemicals'), ('vital-group', 'Vital Group'), ('al', 'AL')]


def logo(slug, name, lazy=True):
    ext = 'svg' if slug == 'galaxy-surfactants' else 'webp'
    return f'<div class="logo-tile"><img src="images/principals/{slug}.{ext}" alt="{E(name)}"{" loading=\"lazy\"" if lazy else ""}></div>'


ICONS = {
    'truck': '<svg viewBox="0 0 24 24"><path d="M1 6h13v10H1zM14 10h5l3 3v3h-8"/><circle cx="6" cy="18" r="2"/><circle cx="18" cy="18" r="2"/></svg>',
    'store': '<svg viewBox="0 0 24 24"><path d="M3 9l1-5h16l1 5M3 9v11h18V9M3 9h18M9 20v-6h6v6"/></svg>',
    'coin': '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M15 9.5c-.6-1-1.7-1.5-3-1.5-1.7 0-3 .9-3 2.2 0 3 6 1.5 6 4.5 0 1.3-1.3 2.3-3 2.3-1.4 0-2.5-.6-3.1-1.6M12 6v2M12 16v2"/></svg>',
    'box': '<svg viewBox="0 0 24 24"><path d="M21 8l-9-5-9 5v8l9 5 9-5zM3 8l9 5 9-5M12 13v8"/></svg>',
}
STR = [('truck', 'Pan-India logistics', 'Excellent logistical support — material reaches you wherever your plant is.'),
       ('store', 'Proper storage', 'Chemicals and solvents stored safely in barrels and bags at our Bhiwandi warehouse.'),
       ('coin', 'Cost efficient', 'Direct links to leading manufacturers keep pricing sharp on every order.'),
       ('box', 'Large inventory', 'Regular stock and indent deals for bulk requirements, delivered on schedule.')]


def str_grid():
    return '<div class="str-grid">' + ''.join(f'<div class="str" data-r><div class="hx">{ICONS[k]}</div><h3>{t}</h3><p>{d}</p></div>' for k, t, d in STR) + '</div>'


def write(name, content):
    open(f'{R}/{name}', 'w', encoding='utf-8').write(content)


# ---------------- HOME ----------------
panels = ''
for i, (cid, title, _long, desc, img, short) in enumerate(CATS, 1):
    chips = ''.join(f'<span>{E(c)}</span>' for c in cats[cid][:5])
    btn_cls = 'btn--cream' if i in (3, 4) else 'btn--dark'
    panels += f'''<article class="panel p{i}" id="ind-{cid}"><div class="num" aria-hidden="true">0{i}</div>
<div class="inner"><div class="txt"><p class="label">{short}</p><h3>{title}</h3><p class="desc">{desc}</p>
<div class="meta"><div class="count">{len(cats[cid])}<small>chemicals listed</small></div><a class="btn {btn_cls}" href="products.html#{cid}">View the list {ARROW}</a></div>
<div class="chips">{chips}</div></div>
<div class="art"><div class="ring"></div><div class="hx"><img src="images/industries/{img}" alt="" loading="lazy"></div></div></div></article>'''

STEPS = [
    ('s1', 'Enquire', 'Tell us the chemical, grade and quantity. We reply with availability and pricing from live stock — or source it for you.', ['Phone', 'WhatsApp', 'Email']),
    ('s2', 'Source', 'Long-standing links with leading manufacturers in India and overseas, so every grade comes from a name you can trust.', ['BASF', 'Clariant', 'Arkema', 'Godrej']),
    ('s3', 'Store', 'Material is held at our Bhiwandi warehouse in barrels and bags — ready for quick dispatch and indent deals.', ['Bhiwandi warehouse', 'Large inventory']),
    ('s4', 'Pack', 'Supplied your way, with a lab analysis report with each dispatch and quality drums to protect the material.', ['Tanker', 'FCL', 'Barrels', 'Bags', 'Small packs']),
    ('s5', 'Deliver', 'Bulk orders move through major ports, then on by road with pan-India logistics support.', ['Kandla', 'Mundra', 'Hazira', 'JNPT', 'Aegis']),
]
steps = ''.join(f'<div class="step {c}"><div class="hxbg"></div><div><span class="n">0{i}</span><h3>{t}</h3><p>{d}</p></div><div class="tags">{"".join(f"<span>{x}</span>" for x in tg)}</div></div>' for i, (c, t, d, tg) in enumerate(STEPS, 1))

mq = ''.join(logo(s, n) for s, n in PR)
mq2 = ''.join(logo(s, n) for s, n in reversed(PR))
cols = [[1, 4], [2, 5], [3, 6]]
alts = {1: 'Team members at the A T Solvochem exhibition stall', 2: 'Visitors at the stall beside the product lists', 3: 'Meeting customers at the exhibition', 4: 'Team and visitor at the stall', 5: 'A T Solvochem at the exhibition', 6: 'A T Solvochem at the exhibition'}
galcols = ''.join('<div class="gal-col">' + ''.join(f'<button class="shot" data-full="images/gallery/expo-{n}.webp"><img src="images/gallery/expo-{n}.webp" alt="{E(alts[n])}" loading="lazy"></button>' for n in c) + '</div>' for c in cols)

home = f'''
<section class="hero" id="top">
<div class="hero-media"><canvas aria-hidden="true"></canvas></div>
<div class="hero-shade"></div>
<div class="hero-line"></div>
<div class="hero-tag">Importer · Distributor · Supplier</div>
<div class="hero-in">
<h1>{lines('One stop for', '<em><b>chemicals</b> &amp;</em>', 'solvents.')}</h1>
<div class="hero-side"><p>For over two decades A T Solvochem has supplied imported and Indian chemicals to fragrance, cosmetic, pharma, paint and resin manufacturers — large stock, safe storage, pan-India delivery.</p>
<div class="hero-cta"><a class="btn btn--red" href="products.html">Browse {TOTAL}+ chemicals {ARROW}</a><a class="btn btn--text" href="contact.html">Request a quote &rarr;</a></div></div>
</div>
<div class="hero-foot"><span>Est. 20+ years<br>Thane, Mumbai</span><span class="scroll-cue"><i></i>Scroll</span><span>Chemicals &amp; solvents<br>Pan-India supply</span></div>
</section>

<div class="rise">
<section class="phil"><div class="wrap">
<p class="label" data-r>Who we are</p>
<p class="big scrub">A.T. Solvochem isn&rsquo;t just a trading house &mdash; it&rsquo;s two decades of <em>reliable supply.</em> We help manufacturers across India source the right chemicals and solvents, with honest pricing, large stock and logistics that simply work.</p>
<div class="trust" data-r><span class="hx"><img src="images/principals/basf.webp" alt=""></span><span class="hx"><img src="images/principals/clariant.webp" alt=""></span><span class="hx"><img src="images/principals/arkema.webp" alt=""></span><span class="hx"><img src="images/principals/godrej-industries.webp" alt=""></span><span style="margin-left:18px">Backed by 20+ leading principals</span></div>
</div></section>

<section class="stack" aria-label="Industries we supply">{panels}</section>

<div class="emerge-wrap"><section class="emerge on-dark"><div class="emerge-in">
<p class="label">Why A T Solvochem</p>
<h2 style="margin-top:26px">Built on <em>stock,</em> storage and straight dealing.</h2>
<p class="lead">Our network of leading manufacturers across the country lets us serve every industry on the spectrum &mdash; on time, at the right price.</p>
<div class="stats">
<div class="stat"><b data-count="20">0<i>+</i></b><span>Years supplying chemicals &amp; solvents</span></div>
<div class="stat"><b data-count="{TOTAL}">0<i>+</i></b><span>Chemicals across five product lists</span></div>
<div class="stat"><b data-count="5">0</b><span>Ports serving bulk orders</span></div>
<div class="stat"><b>Pan<i>-</i>India</b><span>Logistics from our Bhiwandi warehouse</span></div>
</div>
{str_grid()}
</div></section></div>

<section class="hs" aria-label="How we supply">
<div class="hs-head"><div><p class="label">How we supply</p><h2 style="margin-top:22px">From enquiry to <em>your plant.</em></h2></div><p>Five steps, one accountable partner &mdash; scroll sideways through how an order moves.</p></div>
<div class="hs-track">{steps}</div>
</section>

<section class="prin">
<div class="prin-head"><p class="label" data-r>Our principals</p><h2 data-r>Sourced from <em>respected</em> manufacturers.</h2></div>
<div class="mq"><div class="mq-track" data-dir="l">{mq}{mq}</div></div>
<div class="mq"><div class="mq-track" data-dir="r">{mq2}{mq2}</div></div>
<div class="wrap" style="text-align:center;margin-top:46px"><a class="btn btn--out" href="principals.html">All principals {ARROW}</a></div>
</section>

<section class="gal on-dark">
<div class="gal-head"><div><p class="label">On the ground</p><h2 style="margin-top:22px">Meeting our <em>customers</em> &amp; partners.</h2></div><a class="btn btn--cream" href="gallery.html">View gallery {ARROW}</a></div>
<div class="gal-cols">{galcols}</div>
<dialog class="lb" aria-label="Photo viewer"><figure><img alt=""></figure><button aria-label="Close">&times;</button></dialog>
</section>

{closer()}
</div>
'''
write('index.html', page('index.html', 'A T Solvochem | Chemical & solvent importer, distributor — Thane, Mumbai', 'A T Solvochem — a chemical & solvent hub. Importer, distributor and supplier of 550+ chemicals for fragrance, cosmetic, pharma, paint, resin and rubber industries. Thane, Mumbai.', home))

# ---------------- ABOUT ----------------
feats = ['Top-notch quality', 'Regular availability of stock', 'Indent deals for bulk requirements', 'High seas sales', 'Lab analysis report with each dispatch', 'Quality drums to protect material', 'Small packs on request']
about = phead('About us', ['Two decades of', '<em>chemicals</em> &amp; solvents.'], 'One stop spot for all your chemical &amp; solvent requirements.') + f'''
<div class="page-body">
<section class="section"><div class="wrap split">
<div class="prose"><p class="label" data-r>Who we are</p><h2 data-r>Trusted by manufacturers across <em>India.</em></h2>
<p data-r>A.T. Solvochem is a leading importer, distributor and supplier of chemicals, petrochemicals and industrial polymers. Under the leadership of <strong>Mr. Parag Shah</strong>, the firm has completed two decades supplying chemicals and solvents &mdash; beginning by trading solvents and chemicals in a single market.</p>
<p data-r>Years of dedication and hard work have made us a trusted supplier. We value our customer relationships and our work ethic: we strengthen old bonds and create new ones. Active networking has built relationships with leading manufacturers across the country, so we can be a one-stop shop for every industry.</p>
<p data-r>We offer hydrocarbons, alcohols, glycols, ketones, esters, chlorinated solvents, fragrance chemicals, monomers and more.</p></div>
<div data-r><div class="figure-hex"><img src="images/industries/plant.jpg" alt="Chemical plant at dusk" loading="lazy"></div></div>
</div></section>

<section class="section section--w"><div class="wrap">
<div class="mv">
<div data-r><p class="label">Our mission</p><h3>What we <em>believe</em></h3><p>To predict and meet the rising needs of our clients in the chemicals marketplace through high and consistent manoeuvrability and quality &mdash; enabling every client requirement with efficiency, backed by customer and logistical support that puts us at the forefront of this competitive business.</p></div>
<div data-r><p class="label">Our vision</p><h3>Where we want to <em>reach</em></h3><p>To be the most trustworthy and reliable chemical vendor in India &mdash; serving the maximum number of customers with quality products and efficient services all over the country.</p></div>
</div></div></section>

<section class="section section--dark"><div class="wrap"><div class="shead"><div><p class="label l" data-r>Our strength</p><h2 data-r>What you can <em>count on.</em></h2></div></div>{str_grid()}</div></section>

<section class="section"><div class="wrap">
<div class="shead"><div><p class="label" data-r>Our features</p><h2 data-r>Service that goes with <em>every drum.</em></h2></div></div>
<ul class="feat">{''.join(f'<li data-r>{f}</li>' for f in feats)}</ul>
</div></section>
{closer('Let&rsquo;s talk about <em>your requirement.</em>', 'Tell us what you need — we&rsquo;ll respond with availability and pricing.')}
</div>
'''
write('aboutus.html', page('aboutus.html', 'About A T Solvochem | Chemical & solvent supplier, Thane', 'Two decades of supplying chemicals and solvents across India. Mission, vision and strengths of A T Solvochem, led by Mr. Parag Shah.', about))

# ---------------- PRODUCTS ----------------
tabs = f'<button class="tab" data-cat="all" aria-pressed="true">All<span>{TOTAL}</span></button>' + ''.join(f'<button class="tab" data-cat="{c[0]}" aria-pressed="false">{c[5]}<span>{len(cats[c[0]])}</span></button>' for c in CATS)
blocks = ''
for cid, _t, long, desc, img, short in CATS:
    lis = ''.join(f'<li><a href="contact.html?chem={E(re.sub(r"[^A-Za-z0-9]+", "+", n).strip("+"))}">{E(n)}</a></li>' for n in cats[cid])
    blocks += f'<section class="catblock" id="{cid}"><div class="cathead"><div class="hx"><img src="images/industries/{img}" alt="" loading="lazy"></div><div><h2>{E(long)}</h2><p>{desc} <strong class="count">{len(cats[cid])}</strong> chemicals listed.</p></div></div><ul class="chem">{lis}</ul></section>'
prod = phead('Products', [f'{TOTAL}+ chemicals,', '<em>ready to enquire.</em>'], 'Search the list or browse by industry. Select any chemical to send us an enquiry for it.') + f'''
<div class="page-body">
<div class="toolbar"><div class="wrap"><div class="search"><svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/></svg><input id="q" type="search" placeholder="Search chemicals…" aria-label="Search chemicals" autocomplete="off"></div><div class="tabs" role="group" aria-label="Filter by industry">{tabs}</div></div></div>
<div class="wrap">{blocks}
<div class="empty"><p>No chemical matching &ldquo;<strong id="term"></strong>&rdquo; in our lists.</p><p style="margin-top:8px">We source many more grades on request &mdash; <a href="contact.html">send us an enquiry</a>.</p></div>
<div class="note"><p>Available in <strong>tanker, FCL, barrels and bag packing</strong>. Bulk orders are supplied from Kandla, Mundra, Hazira, JNPT and Aegis ports; warehouse stock is held at Bhiwandi. Don&rsquo;t see your grade? We import and source on request.</p><a class="btn btn--dark" href="contact.html">Ask the sales desk {ARROW}</a></div></div>
</div>
'''
write('products.html', page('products.html', f'Products | {TOTAL}+ Chemicals & Solvents — A T Solvochem', 'Browse chemicals and solvents for fragrance, cosmetics, UV filters, pharma/API, paints, resins, adhesives and dyestuff. Enquire online with A T Solvochem, Thane.', prod))

# ---------------- PRINCIPALS ----------------
pr = phead('Principals', ['Partners behind', '<em>our supply.</em>'], 'We work with leading manufacturers in India and overseas, so the material we supply is backed by names the industry trusts.') + f'''
<div class="page-body"><section class="section"><div class="wrap"><div class="logos">{''.join(logo(s, n) for s, n in PR)}</div></div></section>
{closer('Looking for a <em>specific make?</em>', 'Tell us the manufacturer and grade — we will confirm availability.')}</div>
'''
write('principals.html', page('principals.html', 'Our Principals | A T Solvochem', 'Manufacturers and principals associated with A T Solvochem — BASF, Clariant, Godrej, Arkema, Galaxy Surfactants, Deepak Phenolics and more.', pr))

# ---------------- GALLERY ----------------
shots = ''.join(f'<button class="shot" data-full="images/gallery/expo-{n}.webp"><img src="images/gallery/expo-{n}.webp" alt="{E(alts[n])}" loading="lazy"></button>' for n in range(1, 7))
gal = phead('Gallery', ['Out and about with', '<em>our customers.</em>'], 'Moments from our exhibition stall &mdash; meeting customers, principals and partners from across the industry.') + f'''
<div class="page-body"><section class="section"><div class="wrap"><div class="masonry">{shots}</div></div>
<dialog class="lb" aria-label="Photo viewer"><figure><img alt=""></figure><button aria-label="Close">&times;</button></dialog></section>
{closer()}</div>
'''
write('gallery.html', page('gallery.html', 'Gallery | A T Solvochem', 'Photos from A T Solvochem’s exhibition stall — meeting customers, principals and partners.', gal, 'images/gallery/expo-1.webp'))

# ---------------- CONTACT ----------------
con = phead('Contact', ['Talk to the', '<em>sales desk.</em>'], 'Share the chemical, grade and quantity &mdash; we will respond with availability and pricing.') + f'''
<div class="page-body"><section class="section" style="padding-top:20px"><div class="wrap">
<div class="contact">
<div class="info">
<div class="info-item" data-r><h3>Call</h3><a href="tel:{tel(PHONE_O1)}">{PHONE_O1}</a><a href="tel:{tel(PHONE_O2)}">{PHONE_O2}</a><a href="tel:{tel(MOB1)}">{MOB1}</a><a href="tel:{tel(MOB2)}">{MOB2}</a></div>
<div class="info-item" data-r><h3>Email</h3><a href="mailto:{MAIL1}">{MAIL1}</a><a href="mailto:{MAIL2}">{MAIL2}</a></div>
<div class="info-item" data-r><h3>WhatsApp</h3><a href="https://wa.me/{WA}" target="_blank" rel="noopener">+91 98206 62615</a><small>Quick quotes and availability</small></div>
<div class="info-item" data-r><h3>Address</h3><p>{E(ADDR)}</p></div>
</div>
<form class="enq" action="email1.php" method="post" data-r>
<h2>Send an <em>enquiry</em></h2><p>We usually reply the same working day.</p>
<div class="alert" role="status" aria-live="polite"></div>
<div class="fgrid">
<div class="field"><label for="userName">Name *</label><input id="userName" name="userName" required autocomplete="name"></div>
<div class="field"><label for="userPhone">Mobile</label><input id="userPhone" name="userPhone" type="tel" autocomplete="tel"></div>
<div class="field full"><label for="userEmail">Email *</label><input id="userEmail" name="userEmail" type="email" required autocomplete="email"></div>
<div class="field full"><label for="userMsg">Message *</label><textarea id="userMsg" name="userMsg" required placeholder="Chemical, grade, quantity, delivery location…"></textarea></div>
</div>
<div class="hp" aria-hidden="true"><label>Leave empty<input name="website" tabindex="-1" autocomplete="off"></label></div>
<button class="btn btn--red" type="submit">Send enquiry {ARROW}</button>
</form>
</div>
<div class="map" data-r><iframe title="A T Solvochem on the map" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://www.google.com/maps?q=Jaydeep+Emphasis+Wagle+Industrial+Estate+Thane&amp;output=embed"></iframe></div>
</div></section></div>
'''
write('contact.html', page('contact.html', 'Contact A T Solvochem | Thane, Mumbai', 'Contact A T Solvochem — call, email or send an enquiry for chemicals and solvents. 412 Jaydeep Emphasis, MIDC Wagle Estate, Thane (W).', con))

write('404.html', page('404.html', 'Page not found | A T Solvochem', 'Page not found.', phead('404', ['Page', '<em>not found.</em>'], 'The page you are looking for has moved or does not exist.') + f'<div class="page-body"><section class="section" style="padding-top:0"><div class="wrap"><a class="btn btn--red" href="index.html">Back to home {ARROW}</a></div></section></div>'))
write('robots.txt', 'User-agent: *\nAllow: /\nSitemap: https://www.atsolvochem.com/sitemap.xml\n')
urls = ['', 'aboutus.html', 'products.html', 'principals.html', 'gallery.html', 'contact.html']
write('sitemap.xml', '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'<url><loc>https://www.atsolvochem.com/{u}</loc></url>\n' for u in urls) + '</urlset>\n')
print('built', TOTAL)
