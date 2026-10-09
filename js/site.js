(function () {
	var toggle = document.querySelector('.nav-toggle');
	var nav = document.getElementById('site-nav');
	if (toggle && nav) {
		toggle.addEventListener('click', function () {
			var open = toggle.getAttribute('aria-expanded') === 'true';
			toggle.setAttribute('aria-expanded', String(!open));
			toggle.setAttribute('aria-label', open ? 'Open menu' : 'Close menu');
			nav.classList.toggle('open', !open);
		});
	}

	var year = document.getElementById('year');
	if (year) year.textContent = new Date().getFullYear();

	var items = document.querySelectorAll('.reveal');
	if (!('IntersectionObserver' in window)) {
		items.forEach(function (el) { el.classList.add('in'); });
		return;
	}
	var io = new IntersectionObserver(function (entries) {
		entries.forEach(function (e) {
			if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
		});
	}, { rootMargin: '0px 0px -8% 0px' });
	items.forEach(function (el) { io.observe(el); });
})();
