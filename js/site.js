(function () {
  'use strict';
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };

  // header: scrolled state + mobile menu
  var header = $('.site-header');
  var onScroll = function () { header.classList.toggle('scrolled', window.scrollY > 8); };
  onScroll(); window.addEventListener('scroll', onScroll, { passive: true });
  var toggle = $('.nav-toggle'), nav = $('#site-nav');
  if (toggle) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open);
      toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    });
  }

  // reveal on scroll
  var items = $$('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
    items.forEach(function (el) { io.observe(el); });
  } else { items.forEach(function (el) { el.classList.add('in'); }); }

  var yr = $('#year'); if (yr) yr.textContent = new Date().getFullYear();

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
    var h = location.hash.slice(1);
    if (h && document.getElementById(h) && blocks.some(function (b) { return b.id === h; })) setCat(h); else apply();
    window.addEventListener('hashchange', function () {
      var x = location.hash.slice(1); if (blocks.some(function (b) { return b.id === x; })) setCat(x);
    });
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
    var img = $('img', lb);
    $$('.shot').forEach(function (b) { b.addEventListener('click', function () {
      img.src = b.dataset.full; img.alt = b.querySelector('img').alt; lb.showModal();
    }); });
    lb.addEventListener('click', function (e) { if (e.target === lb || e.target.tagName === 'FIGURE' || e.target.tagName === 'BUTTON') lb.close(); });
  }
})();
