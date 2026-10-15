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
  if (toggle) toggle.addEventListener('click', function () {
    var open = pill.classList.toggle('open');
    toggle.setAttribute('aria-expanded', open);
    toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
  });

  // product search + category filter
  var blocks = $$('.catblock');
  if (blocks.length) {
    var q = $('#q'), tabs = $$('.tab'), empty = $('.empty'), cat = 'all';
    var apply = function () {
      var term = q.value.trim().toLowerCase(), shown = 0;
      blocks.forEach(function (b) {
        var inCat = cat === 'all' || b.id === cat, n = 0;
        $$('li', b).forEach(function (li) {
          var hit = !term || li.textContent.toLowerCase().indexOf(term) > -1;
          li.hidden = !hit; if (hit) n++;
        });
        b.hidden = !inCat || n === 0; if (!b.hidden) shown += n;
        var c = $('.count', b); if (c) c.textContent = n;
      });
      empty.classList.toggle('show', shown === 0);
      var t = $('#term'); if (t) t.textContent = q.value.trim();
      if (hasGsap) ScrollTrigger.refresh();
    };
    var setCat = function (c) {
      cat = c;
      tabs.forEach(function (t) { t.setAttribute('aria-pressed', t.dataset.cat === c); });
      apply();
    };
    tabs.forEach(function (t) { t.addEventListener('click', function () {
      setCat(t.dataset.cat); history.replaceState(null, '', t.dataset.cat === 'all' ? location.pathname : '#' + t.dataset.cat);
    }); });
    q.addEventListener('input', apply);
    var qp = new URLSearchParams(location.search).get('q'); if (qp) q.value = qp;
    var h = location.hash.slice(1);
    if (h && blocks.some(function (b) { return b.id === h; })) setCat(h); else apply();
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

  // gallery lightbox
  var lb = $('dialog.lb');
  if (lb) {
    var big = $('img', lb);
    $$('.shot').forEach(function (b) { b.addEventListener('click', function () {
      big.src = b.dataset.full; big.alt = b.querySelector('img').alt; lb.showModal();
    }); });
    lb.addEventListener('click', function (e) { if (e.target === lb || e.target.tagName === 'FIGURE' || e.target.tagName === 'BUTTON') lb.close(); });
  }

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

  /* nav hides on scroll down, returns on scroll up */
  if (pill) {
    var last = 0;
    ScrollTrigger.create({ start: 0, end: 'max', onUpdate: function (s) {
      var y = s.scroll();
      pill.classList.toggle('hide', y > 240 && y > last + 2 && !pill.classList.contains('open'));
      if (y < last - 2 || y < 120) pill.classList.remove('hide');
      last = y;
    } });
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
    var items = $$('details', acc), art = $$('.ind-art img');
    var show = function (i) { if (!art.length) return; art.forEach(function (im, k) { gsap.to(im, { opacity: k === i ? 1 : 0, scale: k === i ? 1 : 1.08, duration: 0.8, ease: 'power2.out', overwrite: true }); }); };
    var close = function (d) {
      var bd = $('.bd', d);
      if (reduce) { d.open = false; return; }
      gsap.to(bd, { height: 0, duration: 0.55, ease: 'power3.inOut', onComplete: function () { d.open = false; bd.style.height = ''; } });
    };
    var open = function (d) {
      d.open = true; var bd = $('.bd', d);
      if (!reduce) gsap.fromTo(bd, { height: 0 }, { height: 'auto', duration: 0.7, ease: 'power3.out', onComplete: function () { ScrollTrigger.refresh(); } });
    };
    items.forEach(function (d, i) {
      $('summary', d).addEventListener('click', function (e) {
        e.preventDefault();
        if (d.open) { close(d); return; }
        items.forEach(function (o) { if (o !== d && o.open) close(o); });
        open(d); show(i);
      });
    });
  });

  /* ---------- counters ---------- */
  $$('[data-count]').forEach(function (el) {
    var to = parseFloat(el.dataset.count), obj = { v: 0 };
    var suffix = el.querySelector('i'); var sfx = suffix ? suffix.outerHTML : '';
    var write = function () { el.innerHTML = Math.round(obj.v) + sfx; };
    if (reduce) { obj.v = to; write(); return; }
    write();
    whenIn(el, 'top 88%', function () { gsap.to(obj, { v: to, duration: 2.2, ease: 'power3.out', onUpdate: write }); });
  });

  /* ---------- marquees ---------- */
  if (!reduce) $$('.mq-track').forEach(function (tr, i) {
    var dir = tr.dataset.dir === 'r' ? 1 : -1;
    var t = gsap.fromTo(tr, { xPercent: dir === -1 ? 0 : -50 }, { xPercent: dir === -1 ? -50 : 0, duration: 70, ease: 'none', repeat: -1 });
    if (lenis) lenis.on('scroll', function (e) { t.timeScale(1 + Math.min(Math.abs(e.velocity) * 0.35, 5)); gsap.to(t, { timeScale: 1, duration: 1.2, overwrite: true }); });
  });

  /* ---------- desktop-only pinned / stacked experiences ---------- */
  mm.add('(min-width: 1021px) and (prefers-reduced-motion: no-preference)', function () {
    // horizontal "how we supply"
    var hs = $('.hs'), tr = hs && $('.hs-track');
    if (hs && tr) {
      var dist = function () { return Math.max(0, tr.scrollWidth - window.innerWidth); };
      gsap.to(tr, { x: function () { return -dist(); }, ease: 'none',
        scrollTrigger: { trigger: hs, start: 'top top', end: function () { return '+=' + dist(); }, pin: true, scrub: 0.8, invalidateOnRefresh: true, anticipatePin: 1 } });
    }

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
      return function () { document.documentElement.classList.remove('fx-footer'); m.style.marginBottom = ''; window.removeEventListener('resize', setH); };
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
