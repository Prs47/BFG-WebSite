// static/js/navbar.js
document.addEventListener('DOMContentLoaded', function () {
  const toggle = document.getElementById('nav-toggle');
  const mobileMenu = document.getElementById('mobile-menu');
  const searchToggle = document.getElementById('search-toggle');
  const mobileSearch = document.getElementById('mobile-search');
  const searchInput = document.getElementById('mobile-search-input');

  function show(el) { el.classList.remove('hidden'); el.setAttribute('aria-hidden', 'false'); }
  function hide(el) { el.classList.add('hidden'); el.setAttribute('aria-hidden', 'true'); }

  toggle && toggle.addEventListener('click', function () {
    const expanded = this.getAttribute('aria-expanded') === 'true';
    this.setAttribute('aria-expanded', String(!expanded));
    if (mobileMenu.classList.contains('hidden')) show(mobileMenu); else hide(mobileMenu);
    // Close search if open
    if (!mobileSearch.classList.contains('hidden')) hide(mobileSearch);
  });

  searchToggle && searchToggle.addEventListener('click', function () {
    const expanded = this.getAttribute('aria-expanded') === 'true';
    this.setAttribute('aria-expanded', String(!expanded));
    if (mobileSearch.classList.contains('hidden')) {
      show(mobileSearch);
      if (searchInput) { searchInput.focus(); }
    } else hide(mobileSearch);
    // Close menu if open
    if (!mobileMenu.classList.contains('hidden')) hide(mobileMenu);
  });

  // close on outside click (optional)
  document.addEventListener('click', function (e) {
    if (!e.target.closest('.site-nav')) {
      hide(mobileMenu); hide(mobileSearch);
    }
  });
});
