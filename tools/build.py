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
NAV = [('index.html', 'Home'), ('aboutus.html', 'About'), ('products.html', 'Products'), ('principals.html', 'Principals'), ('gallery.html', 'Gallery'), ('careers.html', 'Careers')]


def tel(s):
    return s.replace(' ', '')


import hashlib
# cache-busting stamp: changes whenever site.css or site.js changes, so browsers always fetch the latest files
ASSET_V = hashlib.md5(open(R + '/css/site.css', 'rb').read() + open(R + '/js/site.js', 'rb').read()).hexdigest()[:8]

def page(fname, title, desc, body, og='images/industries/plant.jpg'):
    cur = 'products.html' if fname.startswith('products') else fname
    links = ''.join(f'<a href="{h}"{" aria-current=\"page\"" if h == cur else ""}>{l}</a>' for h, l in NAV)
    foot_links = ''.join(f'<li><a href="{h}">{l}</a></li>' for h, l in NAV + [('contact.html', 'Contact')])
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
<link href="https://fonts.googleapis.com/css2?family=Carlito:ital,wght@0,400;0,700;1,400;1,700&amp;display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/site.css?v={ASSET_V}">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="nav-pill">
<a class="brand" href="index.html" aria-label="A T Solvochem — home"><img src="images/mark.png" alt="" width="38" height="34"><span><b>A T Solvochem</b><small>A Chemicals &amp; Solvents Hub</small></span></a>
<nav class="nav-links" aria-label="Main">{links}</nav>
<div class="nav-right"><a class="nav-cta" href="contact.html">Contact us</a><button class="nav-toggle" aria-expanded="false" aria-label="Open menu"><span></span><span></span><span></span></button></div>
</header>
<main id="main">
{body}
</main>
<footer class="site-footer">
<div class="wrap fgrid4">
<div class="foot-brand"><a class="brand" href="index.html"><img src="images/mark.png" alt="" width="38" height="34"><span><b>A T Solvochem</b><small>A Chemicals &amp; Solvents Hub</small></span></a><p>A chemical &amp; solvent hub — one stop spot for all your chemical and solvent requirements, for over two decades.</p></div>
<div><h4>Explore</h4><ul>{foot_links}</ul></div>
<div><h4>Visit</h4><address>{E(ADDR)}</address></div>
<div><h4>Contact</h4><ul>
<li><a href="tel:{tel(PHONE_O1)}">{PHONE_O1}</a></li>
<li><a href="tel:{tel(PHONE_O2)}">{PHONE_O2}</a></li>
<li><a href="tel:{tel(MOB1)}">{MOB1}</a></li>
<li><a href="mailto:{MAIL1}">{MAIL1}</a></li>
<li><a href="mailto:{MAIL2}">{MAIL2}</a></li></ul></div>
</div>
<div class="foot-mega" aria-hidden="true">A T Solvochem</div>
<div class="foot-bottom"><div class="wrap"><span>&copy; <span id="year">2026</span> A.T. Solvochem. All rights reserved.</span><span>Mumbai, India</span></div></div>
</footer>
<a class="wa" href="https://wa.me/{WA}" target="_blank" rel="noopener" aria-label="Chat on WhatsApp">{WAICON}</a>
<script src="js/vendor/gsap.min.js"></script>
<script src="js/vendor/ScrollTrigger.min.js"></script>
<script src="js/vendor/lenis.min.js"></script>
<script src="js/site.js?v={ASSET_V}"></script>
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
    return '<div class="str-grid">' + ''.join(f'<div class="str" data-r><div class="str-top"><span class="str-n">0{i}</span><div class="hx">{ICONS[k]}</div></div><div class="str-txt"><h3>{t}</h3><p>{d}</p></div></div>' for i, (k, t, d) in enumerate(STR, 1)) + '</div>'


def write(name, content):
    open(f'{R}/{name}', 'w', encoding='utf-8').write(content)


# ---------------- HOME ----------------
acc_items = ''
for i, (cid, title, _long, desc, img, short) in enumerate(CATS, 1):
    chips = ''.join(f'<span>{E(c)}</span>' for c in cats[cid][:6])
    acc_items += f"""<details{' open' if i == 1 else ''} data-i="{i-1}"><summary><span class="no">00{i}</span><span class="tt">{title}</span><span class="pl" aria-hidden="true"></span></summary>
<div class="bd"><div class="bd-in"><p>{desc}</p><div class="chips">{chips}<span>+ {len(cats[cid]) - 6} more</span></div><a class="btn btn--dark" href="products-{cid}.html">View all {len(cats[cid])} chemicals {ARROW}</a></div></div></details>"""
acc_art = ''.join(f'<img src="images/industries/{c[4]}" alt="" loading="lazy">' for c in CATS)

# 12 product categories shown as a tile table (from the original site). Each tile links to the closest
# category on products.html (#id), or to the full searchable list where there is no dedicated category.
PT = [('Ff', 'Fragrances &amp; flavours', 'products-fragrance.html'),
      ('Ch', 'Cosmetic, healthcare &amp; aerosol', 'products-care.html'),
      ('Ap', 'API, formulation &amp; speciality chemicals', 'products-pharma.html'),
      ('Pr', 'Paints, polymers, resins &amp; dyestuff', 'products-paint.html'),
      ('Fd', 'Food &amp; fertilizer', 'products.html'),
      ('Tx', 'Textile auxiliaries, monomers &amp; adhesives', 'products-paint.html'),
      ('Mt', 'Plant &amp; machine maintenance', 'products.html'),
      ('Wt', 'Water treatment', 'products.html'),
      ('Mc', 'Miscellaneous chemicals', 'products.html'),
      ('Rb', 'PVC &amp; rubber', 'products-paint.html'),
      ('Eo', 'Essential oils', 'products-fragrance.html'),
      ('Gl', 'General imported &amp; Indian product list', 'products.html')]
PT_ARROW = '<svg class="ar" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M4 12 12 4M5 4h7v7"/></svg>'
pt_tiles = ''.join(f'<a class="pt" href="{h}" data-r><span class="n">{i:02d}</span><span class="s">{s}</span><span class="t">{t}</span>{PT_ARROW}</a>' for i, (s, t, h) in enumerate(PT, 1))

SECT = ['Pharmaceutical, API &amp; formulation', 'Personal care, cosmetics &amp; homecare', 'Fragrance &amp; flavours', 'Speciality chemicals &amp; Grignard reagents', 'Water treatment', 'Paint, resin, adhesives &amp; polyol', 'Construction chemicals', 'Lubricants', 'Textile auxiliaries', 'Rubber &amp; PVC']
sect_html = ''.join(f'<li data-r>{x}</li>' for x in SECT)
CHK = '<svg viewBox="0 0 12 12"><path d="M2 6.5l2.5 2.5L10 3"/></svg>'
CRS = '<svg viewBox="0 0 12 12"><path d="M3 3l6 6M9 3l-6 6"/></svg>'
NO = ['Stock-outs and uncertain availability', 'Unverified grades, no paperwork', 'Material packed in whatever is to hand', 'Small trial quantities refused', 'One supplier for one chemical at a time', 'Logistics left for you to arrange']
YES = ['Regular stock held at Bhiwandi', 'Lab analysis report with each dispatch', 'Quality drums, tanker, FCL or bags', 'Small packs available on request', f'{TOTAL}+ chemicals from one supplier', 'Pan-India logistics support']
vs_html = '<div class="vsp no" data-r><h3>Without a dependable supplier</h3><ul>' + ''.join(f'<li><i>{CRS}</i>{x}</li>' for x in NO) + '</ul></div><div class="vsp yes" data-r><h3>With A T Solvochem</h3><ul>' + ''.join(f'<li><i>{CHK}</i>{x}</li>' for x in YES) + '</ul></div>'

BUY = [('Ready stock', 'Material held at our Bhiwandi warehouse for quick dispatch.', ['Barrels and bags', 'Small packs on request', 'Lab analysis report with each dispatch'], False),
       ('Indent deals', 'Bulk requirements sourced to order, planned around your schedule.', ['Tanker or FCL loads', 'Supplied via Kandla, Mundra, Hazira, JNPT, Aegis', 'Pan-India delivery'], True),
       ('High-seas sales', 'Cargo bought while in transit — ask for current offers.', ['Imported grades', 'Bulk quantities', 'Quoted per shipment'], False)]
buy_html = '<div class="buy2">' + ''.join(f'<div class="bp{" on" if n == 1 else ""}" tabindex="0"><div class="bp-head"><span class="bp-n">0{n}</span><h3>{t}</h3></div><div class="bp-more"><p>{d}</p><ul>' + ''.join(f'<li>{x}</li>' for x in li) + f'</ul><a class="btn btn--red" href="contact.html">Request a quote {ARROW}</a></div></div>' for n, (t, d, li, h) in enumerate(BUY, 1)) + '</div>'

FAQ = [('How do I place an order or get a quote?', 'Send us the chemical name, grade and quantity through the enquiry form, WhatsApp or phone. We confirm availability and pricing from current stock, or source it for you.'),
       ('What packing do you offer?', 'Tanker, FCL, barrels and bags, packed in quality drums to protect the material. Small packs are available on request.'),
       ('Can I order small quantities?', 'Yes — small packs are available on request alongside bulk and indent deals.'),
       ('Do you provide a lab analysis report?', 'Yes. Our quality controllers provide a lab analysis report with each dispatch to assure quality.'),
       ('Where does bulk material ship from?', 'Bulk orders are supplied from Kandla, Mundra, Hazira, JNPT and Aegis ports. Warehouse stock is held in Bhiwandi.'),
       ('Can you source a chemical that is not on your list?', 'Very likely. We import and source on request through our network of leading manufacturers — send us the name and grade.')]
faq_html = '<div class="acc faq">' + ''.join(f'<details><summary><span class="tt">{q}</span><span class="pl" aria-hidden="true"></span></summary><div class="bd"><div class="bd-in"><p>{a}</p></div></div></details>' for q, a in FAQ) + '</div>'

STEPS = [
    ('s1', 'Enquire', 'Tell us the chemical, grade and quantity. We reply with availability and pricing from live stock — or source it for you.', ['Phone', 'WhatsApp', 'Email']),
    ('s2', 'Source', 'Long-standing links with leading manufacturers in India and overseas, so every grade comes from a name you can trust.', ['BASF', 'Clariant', 'Arkema', 'Godrej']),
    ('s3', 'Store', 'Material is held at our Bhiwandi warehouse in barrels and bags — ready for quick dispatch and indent deals.', ['Bhiwandi warehouse', 'Large inventory']),
    ('s4', 'Pack', 'Supplied your way, with a lab analysis report with each dispatch and quality drums to protect the material.', ['Tanker', 'FCL', 'Barrels', 'Bags', 'Small packs']),
    ('s5', 'Deliver', 'Bulk orders move through major ports, then on by road with pan-India logistics support.', ['Kandla', 'Mundra', 'Hazira', 'JNPT', 'Aegis']),
]
STEP_IC = {
    1: '<svg viewBox="0 0 24 24"><path d="M4 5h16v11H8l-4 4z"/></svg>',
    2: '<svg viewBox="0 0 24 24"><circle cx="12" cy="6" r="2.5"/><circle cx="5.5" cy="18" r="2.5"/><circle cx="18.5" cy="18" r="2.5"/><path d="M11 8.3L6.6 15.7M13 8.3l4.4 7.4M8 18h8"/></svg>',
    3: '<svg viewBox="0 0 24 24"><path d="M3 9l1-5h16l1 5M3 9v11h18V9M3 9h18M9 20v-6h6v6"/></svg>',
    4: '<svg viewBox="0 0 24 24"><path d="M21 8l-9-5-9 5v8l9 5 9-5zM3 8l9 5 9-5M12 13v8"/></svg>',
    5: '<svg viewBox="0 0 24 24"><path d="M1 6h13v10H1zM14 10h5l3 3v3h-8"/><circle cx="6" cy="18" r="2"/><circle cx="18" cy="18" r="2"/></svg>'}
steps = ''.join(f'<div class="step"><div class="st-top"><span class="st-n">0{i}</span><span class="st-ic">{STEP_IC[i]}</span></div><div><h3>{t}</h3><p>{d}</p></div><div class="tags">{"".join(f"<span>{x}</span>" for x in tg)}</div></div>' for i, (c, t, d, tg) in enumerate(STEPS, 1))

mq = ''.join(logo(s, n) for s, n in PR)
mq2 = ''.join(logo(s, n) for s, n in reversed(PR))
cols = [[1, 4], [2, 5], [3, 6]]
alts = {1: 'Team members at the A T Solvochem exhibition stall', 2: 'Visitors at the stall beside the product lists', 3: 'Meeting customers at the exhibition', 4: 'Team and visitor at the stall', 5: 'A T Solvochem at the exhibition', 6: 'A T Solvochem at the exhibition'}
G3 = [  # (photo, css anchor, width px, aspect, start x, start y, z)
    (6, 'top:55%;left:14%', 'c', 201, '16/9', 325, 0, 0),
    (2, 'bottom:94px;right:631px', 'n', 193, '16/9', 246, -109, -20),
    (4, 'top:74%;left:701px', 'y', 186, '16/9', -329, -109, -26),
    (5, 'top:35%;left:85%', 'c', 155, '4/3', -325, 35, -19),
    (3, 'top:26%;left:73%', 'c', 150, '3/4', -241, 120, 20),
    (1, 'top:35%;left:27%', 'c', 136, '3/4', 234, 56, 45),
    (4, 'top:71%;left:68%', 'c', 199, '3/4', -153, -110, 39)]
# frames keep the reference shapes; each photo is aimed so the faces stay inside the crop
G3_FACE = {1: .30, 2: .20, 3: .32, 4: .20, 5: .33, 6: .28}            # where the faces sit (fraction of photo height)
G3_SIZE = {1: (1203, 1400), 2: (1050, 1400), 3: (1050, 1400), 4: (1050, 1400), 5: (900, 900), 6: (900, 900)}
def _g3_focus(n, ar):
    fw, fh = (float(v) for v in ar.split('/'))
    pw, ph = G3_SIZE[n]
    vis = (fh / fw) / (ph / pw)                                          # share of the photo height that fits
    if vis >= 1: return 50
    return round(max(0, min(1, (G3_FACE[n] - vis / 2) / (1 - vis))) * 100)
def _g3_face(n, ar):
    return f'<img src="images/gallery/expo-{n}.webp" alt="" loading="lazy" style="object-position:50% {_g3_focus(n, ar)}%">'
g3_frames = ''.join(f'<figure class="g3-img" data-a="{a}" data-x="{x}" data-y="{y}" data-z="{z}" style="{pos};width:{w}px;aspect-ratio:{ar}"><span class="g3-face">{_g3_face(n, ar)}</span><span class="g3-face g3-back">{_g3_face(n, ar)}</span></figure>' for n, pos, a, w, ar, x, y, z in G3)
g3_main = f'<figure class="g3-main"><span class="g3-face">{_g3_face(1, "16/10")}</span><span class="g3-face g3-back">{_g3_face(1, "16/10")}</span></figure>'
galcols = ''.join('<div class="gal-col">' + ''.join(f'<div class="shot"><img src="images/gallery/expo-{n}.webp" alt="{E(alts[n])}" loading="lazy"></div>' for n in c) + '</div>' for c in cols)

SHOW_CATEGORY_TABLE = False  # the twelve-category tile table is hidden for now
CAT_TABLE_SECTION = (f'''<section class="sec sec--w"><div class="wrap">
<div class="sec-head"><div><p class="label" data-r>Product categories</p><h2 data-r>Twelve categories, <em>one supplier.</em></h2></div><p data-r>Pick the industry you work in to see the full product list. Can&rsquo;t find a grade? Ask the sales desk &mdash; we source imported and Indian material on request.</p></div>
<div class="ptable">{pt_tiles}</div>
</div></section>''' if SHOW_CATEGORY_TABLE else '')

WWO = [('fragrance', 'Fragrance &amp; flavours', 'products-fragrance.html'),
       ('care', 'Personal care', 'products-care.html'),
       ('uv', 'UV filters', 'products-uv.html'),
       ('pharma', 'Pharma &amp; API', 'products-pharma.html'),
       ('paint', 'Paints &amp; resins', 'products-paint.html')]
wwo_imgs = ''.join(f'<img{" class=\"on\"" if n == 0 else ""} data-k="{k}" src="images/who/{k}.jpg" alt="" loading="lazy">' for n, (k, _t, _h) in enumerate(WWO))
wwo_items = ''.join(f'<li data-r><a href="{h}" data-k="{k}">{t}</a></li>' for k, t, h in WWO)

SHOW_SECTORS = False  # "The industries we know" list is hidden for now
SECTORS_SECTION = (f'''<section class="sec"><div class="wrap">
<div class="sec-head"><div><p class="label" data-r>Where we work</p><h2 data-r>The industries we <em>know.</em></h2></div><p data-r>Ten sectors where long experience lets us contribute from the first call.</p></div>
<ul class="sect">{sect_html}</ul>
</div></section>''' if SHOW_SECTORS else '')
sup_cards = ''.join(f'<article class="sup__card" style="--sup-i:{i - 1}"><div class="sup__top"><span class="sup__cardNum">0{i}</span><span class="sup__ic" aria-hidden="true">{STEP_IC[i]}</span></div><div class="sup__main"><h3 class="sup__cardTitle">{t}</h3><p class="sup__cardBody">{d}</p></div><div class="sup__tags">{"".join(f"<span>{x}</span>" for x in tg)}</div></article>' for i, (c, t, d, tg) in enumerate(STEPS, 1))
hz_steps = ''.join(f'<li class="hz-step"><span class="hz-node" aria-hidden="true"></span><div class="hz-body"><span class="hz-n">0{i}</span><h3>{t}</h3><p>{d}</p><div class="tags">{"".join(f"<span>{x}</span>" for x in tg)}</div>' + (f'<a class="btn btn--red hz-cta" href="contact.html">Start an enquiry {ARROW}</a>' if i == len(STEPS) else '') + '</div></li>' for i, (c, t, d, tg) in enumerate(STEPS, 1))
tl_steps = ''.join(f'<li class="tl-step"><span class="tl-node" aria-hidden="true"></span><span class="tl-n">0{i}</span><div class="tl-body"><h3>{t}</h3><p>{d}</p><div class="tags">{"".join(f"<span>{x}</span>" for x in tg)}</div></div></li>' for i, (c, t, d, tg) in enumerate(STEPS, 1))

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
<div class="hero-foot"><span>Est. 20+ years<br>Mumbai, India</span><span class="scroll-cue"><i></i>Scroll</span><span>Chemicals &amp; solvents<br>Pan-India supply</span></div>
</section>

<div class="rise">
<section class="phil"><div class="wrap">
<p class="label" data-r>Who we are</p>
<p class="big scrub">For over two decades, A T Solvochem has been the dependable chemicals &amp; solvents partner behind manufacturers across India &mdash; <em>ready stock, transparent pricing</em> and logistics you can rely on.</p>
<p class="phil-sub" data-r>Led by Mr. Parag Shah, we import, distribute and supply chemicals, petrochemicals and industrial polymers &mdash; from a single enquiry to a drum, tanker or container at your gate.</p>
<div class="trust" data-r><span class="tlogo"><img src="images/principals/basf.webp" alt=""></span><span class="tlogo"><img src="images/principals/clariant.webp" alt=""></span><span class="tlogo"><img src="images/principals/arkema.webp" alt=""></span><span class="tlogo"><img src="images/principals/godrej-industries.webp" alt=""></span><span style="margin-left:18px">Backed by 20+ leading principals</span></div>
<a class="btn btn--out phil-btn" href="aboutus.html" data-r>About us {ARROW}</a>
</div></section>

<section class="wwo" id="industries" aria-label="Who we work with">
<div class="wwo-bg" aria-hidden="true">{wwo_imgs}<span class="wwo-shade"></span></div>
<div class="wwo-in"><p class="label l" data-r>Who we work with</p>
<ul class="wwo-list">{wwo_items}</ul>
<p class="wwo-note" data-r>Five industries, one dependable supplier &mdash; and we source beyond the lists on request.</p></div>
</section>

{CAT_TABLE_SECTION}

<div class="emerge-wrap"><section class="emerge on-dark"><div class="emerge-in">
<p class="label">Why A T Solvochem</p>
<h2 style="margin-top:26px">Built on <em>stock,</em> storage and straight dealing.</h2>
<p class="lead">Our network of leading manufacturers across the country lets us serve every industry on the spectrum &mdash; on time, at the right price.</p>
<div class="tick"><span>Lab analysis report with each dispatch</span><span>Regular stock</span><span>Indent deals for bulk</span><span>Small packs on request</span></div>
<div class="stats">
<div class="stat"><b data-count="20">20<i>+</i></b><span>Years supplying chemicals &amp; solvents</span></div>
<div class="stat"><b data-count="{TOTAL}">{TOTAL}<i>+</i></b><span>Chemicals across five product lists</span></div>
<div class="stat"><b data-count="5">5</b><span>Ports serving bulk orders</span></div>
<div class="stat"><b class="sm">Pan<i>-</i>India</b><span>Logistics from our Bhiwandi warehouse</span></div>
</div>
{str_grid()}
</div></section></div>

{SECTORS_SECTION}

<section class="sup" id="supply" aria-label="How we supply"><div class="sup__bloom" aria-hidden="true"></div><div class="sup__stage">
<div class="sup__fixed"><p class="sup__eyebrow">How we supply</p><h2 class="sup__mega">From enquiry to <em>your plant.</em></h2><p class="sup__lead">Five steps, one accountable partner &mdash; scroll sideways through how an order moves.</p></div>
<div class="sup__track">{sup_cards}</div></div></section>

<section class="sec"><div class="wrap vs2">
<div class="vs-l"><div><p class="label" data-r>The difference</p><h2 data-r>The same order, <em>handled twice.</em></h2></div><div><p data-r>Six things that go wrong with an unreliable supplier &mdash; and what we do instead.</p><a class="btn btn--dark" href="contact.html" data-r>Work with us {ARROW}</a></div></div>
<div class="vs-r">{vs_html}</div>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head"><div><p class="label" data-r>Ways to buy</p><h2 data-r>Supplied to <em>suit the order.</em></h2></div><p data-r>Three routes, one sales desk. Tell us the quantity and timeline and we&rsquo;ll recommend the right one.</p></div>
{buy_html}
</div></section>

<section class="prin">
<div class="prin-head"><p class="label" data-r>Our principals</p><h2 data-r>Sourced from <em>respected</em> manufacturers.</h2></div>
<div class="mq"><div class="mq-track" data-dir="l">{mq}{mq}</div></div>
<div class="mq"><div class="mq-track" data-dir="r">{mq2}{mq2}</div></div>
<div class="wrap" style="text-align:center;margin-top:46px"><a class="btn btn--out" href="principals.html">All principals {ARROW}</a></div>
</section>

<section class="gal on-dark">
<div class="gal-head"><div><p class="label">On the ground</p><h2 style="margin-top:22px">Meeting our <em>customers</em> &amp; partners.</h2></div></div>
<div class="gal-cols">{galcols}</div>
<div class="g3-scroll" aria-hidden="true"><div class="g3-sticky"><div class="g3-space"><div class="g3-content">{g3_frames}{g3_main}</div></div></div></div>
<div class="gal-foot"><a class="btn btn--cream" href="gallery.html">View gallery {ARROW}</a></div>

</section>

<section class="sec"><div class="wrap faq-grid">
<div><p class="label" data-r>Questions</p><h2 data-r>Asked before <em>you ask.</em></h2><p data-r>Still not answered? Ask the sales desk &mdash; a straight answer either way.</p><a class="btn btn--dark" href="contact.html" data-r>Ask a question {ARROW}</a></div>
{faq_html}
</div></section>

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
<div data-r><div class="figure-rect"><img src="images/industries/plant.jpg" alt="Chemical plant at dusk" loading="lazy"></div></div>
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
# products.html shows only the five categories (plus a search across everything);
# each category has its own page, products-<id>.html, listing its chemicals.
SEARCH_ICON = '<svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/></svg>'
def chem_li(n, cid=None):
    tag = f'<span class="pall-cat">{E(next(c[5] for c in CATS if c[0] == cid))}</span>' if cid else ''
    return f'<li><a href="contact.html?chem={E(re.sub(r"[^A-Za-z0-9]+", "+", n).strip("+"))}">{E(n)}{tag}</a></li>'
NOTE = f'''<div class="note"><p>Available in <strong>tanker, FCL, barrels and bag packing</strong>. Bulk orders are supplied from Kandla, Mundra, Hazira, JNPT and Aegis ports; warehouse stock is held at Bhiwandi. Don&rsquo;t see your grade? We import and source on request.</p><a class="btn btn--dark" href="contact.html">Ask the sales desk {ARROW}</a></div>'''

pcards = ''.join(f'''<a class="pcard" href="products-{cid}.html" data-r><div class="pcard-img"><img src="images/who/{cid}.jpg" alt="" loading="lazy"></div><div class="pcard-body"><span class="pcard-n">0{i}</span><h2>{E(long)}</h2><p>{desc}</p><div class="pcard-foot"><span><b>{len(cats[cid])}</b> chemicals</span><span class="pcard-go">View products <i><svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M2 8h11M9 4l4 4-4 4"/></svg></i></span></div></div></a>''' for i, (cid, _t, long, desc, img, short) in enumerate(CATS, 1))
all_items = ''.join(chem_li(n, cid) for cid, *_ in CATS for n in cats[cid])
prod = phead('Products', [f'{TOTAL}+ chemicals,', '<em>five industries.</em>'], 'Choose an industry to see its full product list, or search everything at once. Select any chemical to send us an enquiry for it.') + f'''
<div class="page-body">
<div class="toolbar"><div class="wrap"><div class="search search--wide">{SEARCH_ICON}<input id="q" type="search" placeholder="Search all {TOTAL}+ chemicals…" aria-label="Search all chemicals" autocomplete="off"></div><p class="search-hint">or pick an industry below</p></div></div>
<div class="wrap">
<div class="pcats">{pcards}</div>
<div class="pall" hidden><p class="pall-count"><b id="pall-n">0</b> matching chemicals</p><ul class="chem">{all_items}</ul></div>
<div class="empty"><p>No chemical matching &ldquo;<strong id="term"></strong>&rdquo; in our lists.</p><p style="margin-top:8px">We source many more grades on request &mdash; <a href="contact.html">send us an enquiry</a>.</p></div>
{NOTE}</div>
</div>
'''
write('products.html', page('products.html', f'Products | {TOTAL}+ Chemicals & Solvents — A T Solvochem', 'Chemicals and solvents for fragrance & flavours, personal care, UV filters, pharma & API and paints & resins. Choose an industry or search all products.', prod))

for cid, _t, long, desc, img, short in CATS:
    others = ''.join(f'<a class="pother" href="products-{c[0]}.html"><img src="images/who/{c[0]}.jpg" alt="" loading="lazy"><span>{E(c[5])}</span><i>{len(cats[c[0]])}</i></a>' for c in CATS if c[0] != cid)
    groups = {}
    for n in sorted(cats[cid], key=lambda x: x.lower()):
        key = (re.sub(r'^[^A-Za-z]+', '', n)[:1] or '#').upper()
        groups.setdefault(key, []).append(n)
    letters = sorted(groups)
    def chem_card(n):
        q = E(re.sub(r"[^A-Za-z0-9]+", "+", n).strip("+"))
        return f'<li class="cc" data-name="{E(n.lower())}"><h3>{E(n)}</h3><div class="cc-act"><a class="cc-enq" href="contact.html?chem={q}">Enquire <i>&rarr;</i></a><button type="button" class="cc-add" data-name="{E(n)}" aria-pressed="false" aria-label="Add {E(n)} to enquiry list"><span>+</span></button></div></li>'
    items = ''.join(f'<section class="cgrp" id="g-{l}" data-l="{l}"><h2 class="cgrp-l"><span>{l}</span><i>{len(groups[l])}</i></h2><ul class="cgrid">{"".join(chem_card(n) for n in groups[l])}</ul></section>' for l in letters)
    az_bar = ''.join(f'<a href="#g-{l}" data-l="{l}">{l}</a>' for l in letters)
    body = f'''<section class="phead pcat-head"><div class="wrap">
<nav class="crumbs" aria-label="Breadcrumb"><a href="products.html">Products</a><span>/</span><span aria-current="page">{E(short)}</span></nav>
<div class="pcat-top"><div><h1 class="ph-line"><span class="ln"><span>{E(long)}</span></span></h1><p class="sub" data-r>{desc}</p><p class="pcat-count" data-r><b>{len(cats[cid])}</b> chemicals listed</p></div>
<div class="pcat-img" data-r><img src="images/who/{cid}.jpg" alt=""></div></div>
</div></section>
<div class="page-body">
<div class="toolbar"><div class="wrap"><div class="search search--wide">{SEARCH_ICON}<input id="q" type="search" placeholder="Search {E(short.lower())}…" aria-label="Search {E(short)}" autocomplete="off"></div><nav class="caz" aria-label="Jump to letter">{az_bar}</nav><p class="search-hint"><b id="pcat-n">{len(cats[cid])}</b> shown</p></div></div>
<div class="wrap">
<div class="pcat-list">{items}</div>
<div class="empty"><p>No chemical matching &ldquo;<strong id="term"></strong>&rdquo; in this list.</p><p style="margin-top:8px">Try <a href="products.html">searching all products</a>, or <a href="contact.html">send us an enquiry</a> &mdash; we source on request.</p></div>
<div class="pothers"><p class="label">Other industries</p><div class="pothers-row">{others}</div></div>
{NOTE}</div>
</div>
<div class="pbasket" hidden><div class="pbasket-in"><span><b id="pb-n">0</b> products in your enquiry list</span><button type="button" class="pb-clear">Clear</button><a class="btn btn--red" id="pb-send" href="contact.html">Send enquiry {ARROW}</a></div></div>
'''
    write(f'products-{cid}.html', page(f'products-{cid}.html', f'{long} | A T Solvochem', f'{desc} {len(cats[cid])} chemicals from A T Solvochem — enquire online.', body, f'images/who/{cid}.jpg'))

# ---------------- PRINCIPALS ----------------
pr = phead('Principals', ['Partners behind', '<em>our supply.</em>'], 'We work with leading manufacturers in India and overseas, so the material we supply is backed by names the industry trusts.') + f'''
<div class="page-body"><section class="section"><div class="wrap"><div class="logos">{''.join(logo(s, n) for s, n in PR)}</div></div></section>
{closer('Looking for a <em>specific make?</em>', 'Tell us the manufacturer and grade — we will confirm availability.')}</div>
'''
write('principals.html', page('principals.html', 'Our Principals | A T Solvochem', 'Manufacturers and principals associated with A T Solvochem — BASF, Clariant, Godrej, Arkema, Galaxy Surfactants, Deepak Phenolics and more.', pr))

# ---------------- GALLERY ----------------
shots = ''.join(f'<div class="shot"><img src="images/gallery/expo-{n}.webp" alt="{E(alts[n])}" loading="lazy"></div>' for n in range(1, 7))
gal = phead('Gallery', ['Out and about with', '<em>our customers.</em>'], 'Moments from our exhibition stall &mdash; meeting customers, principals and partners from across the industry.') + f'''
<div class="page-body"><section class="section"><div class="wrap"><div class="masonry">{shots}</div></div>
</section>
{closer()}</div>
'''
write('gallery.html', page('gallery.html', 'Gallery | A T Solvochem', 'Photos from A T Solvochem’s exhibition stall — meeting customers, principals and partners.', gal, 'images/gallery/expo-1.webp'))

# ---------------- CAREERS ----------------
CAREER_MAIL = MAIL2
car = phead('Careers', ['Build your career', 'in <em>chemicals.</em>'], 'A T Solvochem has supplied chemicals and solvents across India for over two decades. If you want to grow with a supply business that values straight dealing, we would like to hear from you.') + f"""
<div class="page-body">
<section class="section"><div class="wrap">
<div class="shead"><div><p class="label" data-r>Why join us</p><h2 data-r>Work that keeps <em>industry moving.</em></h2></div></div>
<ul class="feat feat--2">
<li data-r>Two decades in the chemical and solvent trade</li>
<li data-r>{TOTAL}+ chemicals supplied to fragrance, cosmetic, pharma, paint and resin makers</li>
<li data-r>Partnerships with leading principals such as BASF, Clariant, Arkema and Godrej</li>
<li data-r>Head office in Thane, warehouse at Bhiwandi, pan-India logistics</li>
</ul>
</div></section>
<section class="section section--w"><div class="wrap">
<div class="mv">
<div data-r><p class="label">How to apply</p><h3>Send us your <em>CV</em></h3><p>We do not list fixed openings online. Email your CV with the role you are interested in, and we will get back to you when a position matches your profile.</p><p style="margin-top:22px"><a class="btn btn--dark" href="mailto:{CAREER_MAIL}?subject=Career%20enquiry%20%E2%80%94%20A%20T%20Solvochem">Email your CV {ARROW}</a></p></div>
<div data-r><p class="label">Prefer to talk?</p><h3>Call or <em>WhatsApp</em></h3><p>Reach the office on <a href="tel:{tel(PHONE_O2)}">{PHONE_O2}</a>, or message us on WhatsApp and we will point you to the right person.</p><p style="margin-top:22px"><a class="btn btn--text" href="https://wa.me/{WA}" target="_blank" rel="noopener">WhatsApp us &rarr;</a></p></div>
</div></div></section>
</div>
"""
write('careers.html', page('careers.html', 'Careers | A T Solvochem, Thane', 'Careers at A T Solvochem — a chemical and solvent importer and distributor in Thane, Mumbai. Send your CV to join our team.', car))

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
urls = ['', 'aboutus.html', 'products.html'] + [f'products-{c[0]}.html' for c in CATS] + [ 'principals.html', 'gallery.html', 'careers.html', 'contact.html']
write('sitemap.xml', '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'<url><loc>https://www.atsolvochem.com/{u}</loc></url>\n' for u in urls) + '</urlset>\n')
print('built', TOTAL)
