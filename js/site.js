/* A T Solvochem — scroll experience (GSAP + ScrollTrigger + Lenis, vendored in js/vendor).
   Initial hidden states are set here, never in CSS, so the site stays readable if scripts fail. */
(function () {
  'use strict';
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var hasGsap = typeof gsap !== 'undefined' && typeof ScrollTrigger !== 'undefined';

  /* ---------- basics (no animation dependency) ---------- */
  var yr = $('#year'); if (yr) yr.textContent = new Date().getFullYear();

  var pill = $('.nav-pill'), toggle = $('.nav-toggle');
  // navbar: full-width bar at the top, compresses into a centred pill once the page scrolls (and expands again at the top)
  if (pill) {
    var setCompact = function () { pill.classList.toggle('compact', window.scrollY > 40); };
    setCompact(); window.addEventListener('scroll', setCompact, { passive: true });
  }
  if (toggle) toggle.addEventListener('click', function () {
    var open = pill.classList.toggle('open');
    toggle.setAttribute('aria-expanded', open);
    toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
  });

  // products: old links like products.html#pharma now open that category's page
  if (/\/products\.html$/.test(location.pathname)) {
    var oldCat = location.hash.slice(1);
    if (['fragrance', 'care', 'uv', 'pharma', 'paint'].indexOf(oldCat) > -1) location.replace('products-' + oldCat + '.html');
  }
  // products landing: typing searches every chemical (category cards hide while a search is active)
  var pq = $('#q'), pall = $('.pall'), pgroups = $$('.cgrp');
  if (pq && pall) {   // products landing: typing searches every chemical (cards hide while searching)
    var allItems = $$('li', pall), pempty = $('.empty'), pcards = $('.pcats'), pterm = $('#term'), pn = $('#pall-n');
    var runAll = function () {
      var t = pq.value.trim().toLowerCase(), n = 0;
      allItems.forEach(function (li) { var hit = !t || li.textContent.toLowerCase().indexOf(t) > -1; li.hidden = !hit; if (hit) n++; });
      pall.hidden = !t; if (pcards) pcards.hidden = !!t;
      if (pn) pn.textContent = n; pempty.classList.toggle('show', !!t && n === 0); if (pterm) pterm.textContent = pq.value.trim();
      if (hasGsap) ScrollTrigger.refresh();
    };
    pq.addEventListener('input', runAll);
    var lq = new URLSearchParams(location.search).get('q'); if (lq) pq.value = lq;
    runAll();
  }
  if (pq && pgroups.length) {   // category page: grouped A-Z cards, search, enquiry list
    var cc = $$('.cc'), cn = $('#pcat-n'), cempty = $('.empty'), cterm = $('#term'), azl = $$('.caz a');
    var runCat = function () {
      var t = pq.value.trim().toLowerCase(), n = 0;
      cc.forEach(function (c) { var hit = !t || c.dataset.name.indexOf(t) > -1; c.hidden = !hit; if (hit) n++; });
      pgroups.forEach(function (g) { var any = $$('.cc:not([hidden])', g).length; g.hidden = !any; $('.cgrp-l i', g).textContent = any; });
      azl.forEach(function (a) { var g = document.getElementById('g-' + a.dataset.l); a.classList.toggle('off', g.hidden); });
      cn.textContent = n; cempty.classList.toggle('show', n === 0); cterm.textContent = pq.value.trim();
      if (hasGsap) ScrollTrigger.refresh();
    };
    pq.addEventListener('input', runCat); runCat();
    azl.forEach(function (a) { a.addEventListener('click', function (e) {
      e.preventDefault(); var g = document.getElementById('g-' + a.dataset.l), y = g.getBoundingClientRect().top + window.scrollY - 190;
      if (window.lenis) window.lenis.scrollTo(y); else window.scrollTo({ top: y, behavior: 'smooth' });
    }); });
    var basket = [], bar = $('.pbasket'), bn = $('#pb-n'), send = $('#pb-send');
    try { basket = JSON.parse(sessionStorage.getItem('ats-basket') || '[]'); } catch (e) { basket = []; }
    var save = function () { try { sessionStorage.setItem('ats-basket', JSON.stringify(basket)); } catch (e) {} };
    var paintB = function () {
      bar.hidden = basket.length === 0; bn.textContent = basket.length;
      send.href = 'contact.html?chem=' + encodeURIComponent(basket.join(', '));
      $$('.cc-add').forEach(function (b) { var on = basket.indexOf(b.dataset.name) > -1; b.setAttribute('aria-pressed', on); b.firstChild.textContent = on ? '\u2713' : '+'; b.parentNode.parentNode.classList.toggle('picked', on); });
    };
    $('.pcat-list').addEventListener('click', function (e) {
      var b = e.target.closest('.cc-add'); if (!b) return;
      var i = basket.indexOf(b.dataset.name); if (i > -1) basket.splice(i, 1); else basket.push(b.dataset.name);
      save(); paintB();
    });
    $('.pb-clear').addEventListener('click', function () { basket = []; save(); paintB(); });
    paintB();
  }

  // contact form: prefill from ?chem= and show result
  var form = $('form.enq');
  if (form) {
    var p = new URLSearchParams(location.search), msg = $('#userMsg');
    if (p.get('chem') && msg && !msg.value) msg.value = 'Please share price and availability for: ' + p.get('chem') + '\nGrade / quantity: ';
    var al = $('.alert');
    if (p.get('sent') === '1') { al.className = 'alert ok'; al.textContent = 'Thank you — your enquiry has been sent. We will get back to you shortly.'; }
    else if (p.get('sent') === '0') { al.className = 'alert err'; al.textContent = 'We could not send your enquiry. Please try again or email sales.atsolvochem@gmail.com.'; }
  }

  // ways to buy: hover / focus / tap a panel to open it
  $$('.buy2').forEach(function (row) {
    var ps = $$('.bp', row);
    var pick = function (p) { ps.forEach(function (o) { o.classList.toggle('on', o === p); }); };
    ps.forEach(function (p) {
      p.addEventListener('mouseenter', function () { pick(p); });
      p.addEventListener('focus', function () { pick(p); });
      p.addEventListener('click', function () { pick(p); });
    });
  });

  if (!hasGsap) return;
  gsap.registerPlugin(ScrollTrigger);

  /* ---------- smooth scroll ---------- */
  var lenis = null;
  if (!reduce && typeof Lenis !== 'undefined') {
    lenis = new Lenis({ lerp: 0.09, wheelMultiplier: 0.95 });
    lenis.on('scroll', ScrollTrigger.update);
    gsap.ticker.add(function (t) { lenis.raf(t * 1000); });
    gsap.ticker.lagSmoothing(0);
    $$('a[href^="#"]').forEach(function (a) {
      a.addEventListener('click', function (e) {
        var t = $(a.getAttribute('href')); if (!t) return;
        e.preventDefault(); lenis.scrollTo(t, { offset: -80 });
      });
    });
  }



  /* ---------- helpers ---------- */
  function splitWords(el) {
    var out = [];
    (function walk(node) {
      Array.prototype.slice.call(node.childNodes).forEach(function (n) {
        if (n.nodeType === 3) {
          var frag = document.createDocumentFragment();
          n.textContent.split(/(\s+)/).forEach(function (part) {
            if (!part) return;
            if (/^\s+$/.test(part)) { frag.appendChild(document.createTextNode(' ')); return; }
            var s = document.createElement('span'); s.className = 'w'; s.textContent = part; frag.appendChild(s); out.push(s);
          });
          node.replaceChild(frag, n);
        } else if (n.nodeType === 1) walk(n);
      });
    })(el);
    return out;
  }

  /* run fn once when el reaches `start` — also if the page loads or jumps past it (so nothing stays hidden) */
  function whenIn(el, start, fn) {
    var done = false, run = function () { if (!done) { done = true; fn(); } };
    ScrollTrigger.create({ trigger: el, start: start, end: 'max', onEnter: run, onRefresh: function (self) { if (self.scroll() >= self.start) run(); } });
  }

  var mm = gsap.matchMedia();

  /* ---------- hero: canvas, intro, curtain ---------- */
  var hero = $('.hero');
  if (hero) {
    var canvas = $('.hero-media canvas');
    if (canvas) molecules(canvas, hero);

    if (!reduce) {
      var tl = gsap.timeline({ defaults: { ease: 'expo.out' }, delay: 0.15 });
      tl.from('.hero-media', { scale: 1.25, duration: 2.4, ease: 'power3.out' }, 0)
        .from('.hero h1 .ln>span', { yPercent: 115, duration: 1.5, stagger: 0.12 }, 0.2)
        .from('.hero-line', { scaleX: 0, duration: 1.8 }, 0.4)
        .from('.hero-tag,.hero-side>*,.hero-foot>*', { y: 24, opacity: 0, duration: 1.1, stagger: 0.08 }, 0.9);

      // as the next section rises over the hero: push back, blur, darken
      gsap.timeline({ scrollTrigger: { trigger: '.rise', start: 'top bottom', end: 'top top', scrub: true } })
        .to('.hero-media', { scale: 1.18, yPercent: 9, ease: 'none' }, 0)
        .to('.hero-in', { y: -90, opacity: 0, filter: 'blur(10px)', ease: 'none' }, 0)
        .to('.hero-line,.hero-tag,.hero-foot', { opacity: 0, ease: 'none' }, 0)
        .to('.hero-shade', { backgroundColor: 'rgba(13,12,10,.5)', ease: 'none' }, 0);
    }
    ScrollTrigger.create({ trigger: '.rise', start: 'top top',
      onEnter: function () { hero.classList.add('off'); hero.style.visibility = 'hidden'; },
      onLeaveBack: function () { hero.classList.remove('off'); hero.style.visibility = ''; } });
  }

  /* ---------- scrubbed word reveal ---------- */
  if (!reduce) $$('.scrub').forEach(function (el) {
    var words = splitWords(el);
    gsap.fromTo(words, { opacity: 0.14 }, { opacity: 1, stagger: 0.06, ease: 'none',
      scrollTrigger: { trigger: el, start: 'top 82%', end: 'bottom 48%', scrub: 0.6 } });
  });

  /* ---------- generic reveals ---------- */
  if (!reduce) {
    var rev = $$('[data-r]');
    gsap.set(rev, { opacity: 0, y: 48 });
    rev.forEach(function (el) {
      var idx = Array.prototype.indexOf.call(el.parentNode.children, el);
      whenIn(el, 'top 92%', function () { gsap.to(el, { opacity: 1, y: 0, duration: 1.1, delay: Math.min(idx * 0.08, 0.5), ease: 'power3.out' }); });
    });
    $$('.ph-line').forEach(function (el) {
      gsap.from(el.querySelectorAll('.ln>span'), { yPercent: 115, duration: 1.4, stagger: 0.1, ease: 'expo.out', delay: 0.2 });
    });
  }


  /* ---------- accordions (native <details>; one open at a time, animated height) ---------- */
  $$('.acc').forEach(function (acc) {
    var items = $$('details', acc), art = $$('.ind-art img'), pinSt = null;
    var show = function (i) { if (!art.length) return; art.forEach(function (im, k) { gsap.to(im, { opacity: k === i ? 1 : 0, duration: 0.9, ease: 'power1.inOut', overwrite: true }); }); };
    var close = function (d) {
      var bd = $('.bd', d);
      if (reduce) { d.open = false; return; }
      gsap.to(bd, { height: 0, duration: 0.55, ease: 'power3.inOut', overwrite: true, onComplete: function () { d.open = false; bd.style.height = ''; } });
    };
    var open = function (d) {
      d.open = true; var bd = $('.bd', d);
      if (!reduce) gsap.fromTo(bd, { height: 0 }, { height: 'auto', duration: 0.7, ease: 'power3.out', overwrite: true, onComplete: function () { ScrollTrigger.refresh(); } });
    };
    items.forEach(function (d, i) {
      $('summary', d).addEventListener('click', function (e) {
        e.preventDefault();
        if (pinSt) { // scroll-driven mode: jump to this item's place in the scroll
          var y = pinSt.start + (i + 0.5) / items.length * (pinSt.end - pinSt.start);
          if (lenis) lenis.scrollTo(y); else window.scrollTo({ top: y, behavior: 'smooth' });
          return;
        }
        if (d.open) { close(d); return; }
        items.forEach(function (o) { if (o !== d && o.open) close(o); });
        open(d); show(i);
      });
    });

    // industries (desktop): the section pins; scrolling closes the open item, opens the next and cross-fades the picture
    if (acc.id === 'ind-acc' && !reduce) {
      mm.add('(min-width: 1021px)', function () {
        var sec = acc.closest('.sec'), grid = acc.closest('.ind-grid'), n = items.length, cur = 0, lastP = 0;
        sec.classList.add('ind-pin');
        var go = function (i) {
          if (i === cur) return; cur = i;
          items.forEach(function (o, k) { if (k !== i && o.open) close(o); });
          if (!items[i].open) open(items[i]);
          show(i);
        };
        pinSt = ScrollTrigger.create({
          trigger: grid, start: 'top 96', pin: true, anticipatePin: 1, invalidateOnRefresh: true,
          end: function () { return '+=' + Math.round(window.innerHeight * 0.6 * n); },
          onUpdate: function (st) { if (Math.abs(st.progress - lastP) < 0.0005) return; lastP = st.progress; go(Math.min(n - 1, Math.floor(st.progress * n))); }
        });
        // hovering a row also opens it and swaps the picture (mouse devices)
        var timer = null, hovers = [];
        if (window.matchMedia('(any-hover: hover)').matches) items.forEach(function (d, i) {
          var sm = $('summary', d);
          var enter = function () { clearTimeout(timer); timer = setTimeout(function () { go(i); }, 120); };
          var leave = function () { clearTimeout(timer); };
          sm.addEventListener('mouseenter', enter); sm.addEventListener('mouseleave', leave);
          hovers.push([sm, enter, leave]);
        });
        return function () {
          hovers.forEach(function (h) { h[0].removeEventListener('mouseenter', h[1]); h[0].removeEventListener('mouseleave', h[2]); });
          sec.classList.remove('ind-pin'); if (pinSt) pinSt.kill(); pinSt = null;
        };
      });
    }
  });

  /* ---------- who we work with: hovering a name swaps the background photo ---------- */
  var wwo = $('.wwo');
  if (wwo) {
    var imgs = $$('.wwo-bg img'), links = $$('.wwo-list a'), cur = null;
    var showImg = function (k) {
      if (k === cur) return; cur = k;
      imgs.forEach(function (im) { im.classList.toggle('on', im.dataset.k === k); });
    };
    var list = $('.wwo-list');
    // focus = which name is sharp; the others blur and fade by distance. The first name is focused by default.
    var setFocus = function (idx) {
      list.classList.add('hov');
      links.forEach(function (l, j) { l.style.setProperty('--dist', Math.abs(j - idx)); l.classList.toggle('act', j === idx); });
    };
    var focusOn = function (a) { showImg(a.dataset.k); setFocus(links.indexOf(a)); };
    var firstKey = links[0].dataset.k;
    var focusOff = function () { showImg(firstKey); setFocus(0); };
    cur = firstKey; setFocus(0);
    links.forEach(function (a) {
      a.addEventListener('mouseenter', function () { focusOn(a); });
      a.addEventListener('focus', function () { focusOn(a); });
      a.addEventListener('blur', focusOff);
    });
    list.addEventListener('mouseleave', focusOff);
  }

  /* ---------- counters: odometer digits roll up each time the stats scroll into view ---------- */
  $$('[data-count]').forEach(function (el) {
    if (reduce) return;                         // markup already holds the final number
    var digits = String(parseInt(el.dataset.count, 10)).split('');
    var sfx = el.querySelector('i'); sfx = sfx ? sfx.outerHTML : '';
    el.setAttribute('aria-label', el.textContent);
    el.innerHTML = digits.map(function (d) {
      var strip = '';
      for (var k = 0; k < 20; k++) strip += '<span>' + (k % 10) + '</span>';   // two full turns of the wheel
      for (var m = 0; m <= +d; m++) strip += '<span>' + m + '</span>';           // then stop on the digit
      return '<span class="odo" aria-hidden="true"><span class="odo__strip" data-d="' + d + '">' + strip + '</span></span>';
    }).join('') + sfx;
    var strips = $$('.odo__strip', el);
    var roll = function () {
      strips.forEach(function (s, i) {
        var stop = 20 + (+s.dataset.d);
        gsap.fromTo(s, { yPercent: 0 }, { yPercent: -100 * stop / (stop + 1), duration: 1.6 + (strips.length - 1 - i) * 0.35, ease: 'power3.out', overwrite: true });
      });
    };
    gsap.set(strips, { yPercent: 0 });
    ScrollTrigger.create({ trigger: el, start: 'top 90%', end: 'bottom 10%', onEnter: roll, onEnterBack: roll,
      onRefresh: function (self) { if (self.isActive) roll(); } });
  });

  /* ---------- marquees ---------- */
  if (!reduce) $$('.mq-track').forEach(function (tr, i) {
    var dir = tr.dataset.dir === 'r' ? 1 : -1;
    var t = gsap.fromTo(tr, { xPercent: dir === -1 ? 0 : -50 }, { xPercent: dir === -1 ? -50 : 0, duration: 70, ease: 'none', repeat: -1 });
    if (lenis) lenis.on('scroll', function (e) { t.timeScale(1 + Math.min(Math.abs(e.velocity) * 0.35, 5)); gsap.to(t, { timeScale: 1, duration: 1.2, overwrite: true }); });
  });

  // supply section: pin it and sweep the tilted cards across with scroll (driven by --sup-x)
  mm.add('(min-width: 900px) and (prefers-reduced-motion: no-preference)', function () {
    var sec = $('.sup'), track = sec && $('.sup__track', sec);
    if (!sec || !track) return;
    var total = function () { return track.scrollWidth + 0.9 * window.innerWidth; };
    var measure = function () {
      var card = track.querySelector('.sup__card'), cw = card ? card.offsetWidth : 320;
      var gap = parseFloat(getComputedStyle(track).columnGap || '0') || 0;
      track.style.setProperty('--sup-cw', String(cw));
      track.style.setProperty('--sup-step', String(cw + gap));
      track.style.setProperty('--sup-vw', String(window.innerWidth));
    };
    measure();
    var st = ScrollTrigger.create({ trigger: sec, start: 'top top', end: function () { return '+=' + 0.85 * total(); }, pin: true, anticipatePin: 1, scrub: 0.7,
      invalidateOnRefresh: true, onRefresh: measure,
      onUpdate: function (self) { track.style.setProperty('--sup-x', String(0.9 * window.innerWidth - total() * self.progress)); } });
    track.style.setProperty('--sup-x', String(0.9 * window.innerWidth));
    return function () { ['--sup-x', '--sup-cw', '--sup-step', '--sup-vw'].forEach(function (k) { track.style.removeProperty(k); }); st.kill(); };
  });

  // gallery 3D: stage slides in from top-left and zooms (x2), then the photo cluster spreads out while the whole
  // plane flips 180deg on X and settles at x1.5 - scroll-linked with scrub smoothing
  mm.add('(min-width: 1021px) and (prefers-reduced-motion: no-preference)', function () {
    var gal = $('.gal'), sc = gal && $('.g3-scroll', gal);
    if (!sc) return;
    gal.classList.add('g3-on');
    var sticky = $('.g3-sticky', sc), space = $('.g3-space', sc), content = $('.g3-content', sc), main = $('.g3-main', sc), frames = $$('.g3-img', sc);
    gsap.set(space, { transformPerspective: 800, scale: 1 });
    gsap.set(main, { xPercent: -50, yPercent: -50, z: 150, scale: 0.5 });
    frames.forEach(function (f) {
      var a = f.dataset.a;
      gsap.set(f, { xPercent: a === 'c' ? -50 : 0, yPercent: a === 'n' ? 0 : -50, x: +f.dataset.x, y: +f.dataset.y, z: +f.dataset.z });
    });
    gsap.set(sticky, { scale: 0.7, x: -300, y: -400 });
    var tl = gsap.timeline({ scrollTrigger: { trigger: sc, start: 'top bottom', end: 'bottom bottom', scrub: 1, invalidateOnRefresh: true } });
    tl.to(sticky, { scale: 1, x: 0, y: 0, ease: 'none', duration: 1 }, 0)
      .to(space, { scale: 2, ease: 'none', duration: 1 }, 0)
      .to(content, { rotateX: 180, ease: 'none', duration: 1.8 }, 1)
      .to(space, { scale: 1.5, ease: 'none', duration: 1.8 }, 1)
      .to(frames, { x: 0, y: 0, ease: 'none', duration: 1.8 }, 1);
    return function () { gal.classList.remove('g3-on'); tl.scrollTrigger && tl.scrollTrigger.kill(); tl.kill(); gsap.set([sticky, space, content, main].concat(frames), { clearProps: 'all' }); };
  });

  /* ---------- desktop-only pinned / stacked experiences ---------- */
  mm.add('(min-width: 1021px) and (prefers-reduced-motion: no-preference)', function () {
    // parallax gallery columns
    $$('.gal-col').forEach(function (c, i) {
      gsap.to(c, { y: [-90, 70, -150][i] || -60, ease: 'none', scrollTrigger: { trigger: '.gal', start: 'top bottom', end: 'bottom top', scrub: true } });
    });

    // footer uncovered beneath the page
    var ft = $('.site-footer');
    if (ft && $('.closer')) {
      document.documentElement.classList.add('fx-footer');
      var m = $('main'); var setH = function () { m.style.marginBottom = ft.offsetHeight + 'px'; };
      setH(); window.addEventListener('resize', setH);
      // keep the fixed footer hidden until the closing banner is on screen (nothing can bleed through pinned sections)
      ft.style.visibility = 'hidden';
      var ftSt = ScrollTrigger.create({ trigger: '.closer', start: 'top bottom', end: 'max',
        onEnter: function () { ft.style.visibility = ''; }, onLeaveBack: function () { ft.style.visibility = 'hidden'; },
        onRefresh: function (self) { ft.style.visibility = self.scroll() >= self.start ? '' : 'hidden'; } });
      return function () { document.documentElement.classList.remove('fx-footer'); m.style.marginBottom = ''; ft.style.visibility = ''; ftSt.kill(); window.removeEventListener('resize', setH); };
    }
  });

  /* ---------- all sizes: emerging dark card, closer ---------- */
  if (!reduce) {
    var em = $('.emerge');
    if (em) {
      var small = window.matchMedia('(max-width: 700px)').matches;
      gsap.fromTo(em, { clipPath: small ? 'inset(6% 4% round 28px)' : 'inset(14% 7% round 44px)' },
        { clipPath: 'inset(0% 0% round 0px)', ease: 'none', scrollTrigger: { trigger: '.emerge-wrap', start: 'top 80%', end: 'top 0%', scrub: true } });
      splitWords($('.emerge h2'));
      gsap.set('.emerge h2 .w', { yPercent: 100, opacity: 0 });
      whenIn($('.emerge h2'), 'top 80%', function () { gsap.to('.emerge h2 .w', { yPercent: 0, opacity: 1, stagger: 0.04, duration: 1, ease: 'power3.out' }); });
    }
    var cl = $('.closer');
    if (cl) {
      var words = splitWords($('.closer h2'));
      gsap.set(words, { yPercent: 70, opacity: 0, rotate: 4 });
      whenIn(cl, 'top 70%', function () { gsap.to(words, { yPercent: 0, opacity: 1, rotate: 0, stagger: 0.07, duration: 1.3, ease: 'expo.out' }); });
      $$('.closer .hxbg').forEach(function (h, i) {
        gsap.to(h, { y: (i ? 80 : -80), rotate: i ? -25 : 25, ease: 'none', scrollTrigger: { trigger: cl, start: 'top bottom', end: 'bottom top', scrub: true } });
      });
    }
  }

  window.addEventListener('load', function () { ScrollTrigger.refresh(); });

  /* ---------- hero molecule field ---------- */
  function molecules(cv, host) {
    var ctx = cv.getContext('2d'), w = 0, h = 0, dpr = 1, nodes = [], mx = -9999, my = -9999, t = 0, visible = true;
    function resize() {
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      w = cv.clientWidth; h = cv.clientHeight; cv.width = w * dpr; cv.height = h * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      var n = Math.round(Math.min(120, w * h / 15000));
      nodes = [];
      for (var i = 0; i < n; i++) nodes.push({ x: Math.random() * w, y: Math.random() * h, vx: (Math.random() - 0.5) * 0.28, vy: (Math.random() - 0.5) * 0.28,
        r: 1 + Math.random() * 2, hex: Math.random() < 0.2, a: Math.random() * 6.28, s: (Math.random() - 0.5) * 0.004 });
    }
    function hexPath(x, y, r, a) {
      ctx.beginPath();
      for (var k = 0; k < 6; k++) { var an = a + k * Math.PI / 3 + Math.PI / 6; ctx[k ? 'lineTo' : 'moveTo'](x + Math.cos(an) * r, y + Math.sin(an) * r); }
      ctx.closePath();
    }
    function frame() {
      requestAnimationFrame(frame);
      if (!visible || host.classList.contains('off') || document.hidden) return;
      ctx.clearRect(0, 0, w, h); t += 1;
      var i, j, a, b, dx, dy, d;
      for (i = 0; i < nodes.length; i++) {
        a = nodes[i];
        if (!reduce) { a.x += a.vx; a.y += a.vy; a.a += a.s; }
        if (a.x < -20) a.x = w + 20; if (a.x > w + 20) a.x = -20; if (a.y < -20) a.y = h + 20; if (a.y > h + 20) a.y = -20;
        dx = mx - a.x; dy = my - a.y; d = Math.sqrt(dx * dx + dy * dy);
        if (d < 190 && !reduce) { a.x += dx * 0.012; a.y += dy * 0.012; }
      }
      for (i = 0; i < nodes.length; i++) {
        a = nodes[i];
        for (j = i + 1; j < nodes.length; j++) {
          b = nodes[j]; dx = a.x - b.x; dy = a.y - b.y; d = dx * dx + dy * dy;
          if (d < 19600) { ctx.strokeStyle = 'rgba(255,255,255,' + (0.24 * (1 - Math.sqrt(d) / 140)).toFixed(3) + ')'; ctx.lineWidth = 0.8; ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y); ctx.stroke(); }
        }
        dx = mx - a.x; dy = my - a.y; d = Math.sqrt(dx * dx + dy * dy);
        if (d < 190) { ctx.strokeStyle = 'rgba(227,32,43,' + (0.75 * (1 - d / 190)).toFixed(3) + ')'; ctx.lineWidth = 1.1; ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(mx, my); ctx.stroke(); }
      }
      for (i = 0; i < nodes.length; i++) {
        a = nodes[i];
        if (a.hex) { hexPath(a.x, a.y, a.r * 5, a.a); ctx.strokeStyle = 'rgba(227,32,43,.7)'; ctx.lineWidth = 1.2; ctx.stroke(); }
        else { ctx.beginPath(); ctx.arc(a.x, a.y, a.r, 0, 6.283); ctx.fillStyle = 'rgba(255,255,255,.75)'; ctx.fill(); }
      }
    }
    resize(); window.addEventListener('resize', resize);
    host.addEventListener('pointermove', function (e) { var r = cv.getBoundingClientRect(); mx = e.clientX - r.left; my = e.clientY - r.top; });
    host.addEventListener('pointerleave', function () { mx = my = -9999; });
    if ('IntersectionObserver' in window) new IntersectionObserver(function (es) { visible = es[0].isIntersecting; }).observe(host);
    gsap.from(cv, { opacity: 0, duration: 2, ease: 'power2.out' });
    frame();
  }
})();
