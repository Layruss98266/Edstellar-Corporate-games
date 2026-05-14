/* Motion (vanilla JS) animations for Edstellar Engage prototype.
   Loaded after assets/app.js. Requires Motion One global from CDN.
   No-op if window.Motion isn't present.
*/
(function(){
  if(!window.Motion){ console.warn('Motion not loaded - animations disabled.'); return; }
  const { animate, inView, stagger } = window.Motion;
  const easeOut = [0.22, 1, 0.36, 1];
  const spring = [0.34, 1.56, 0.64, 1];

  // Respect reduced-motion users
  const reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if(reduce) return;

  // ---------- 1. Page-load hero entrance ----------
  const heroH1 = document.querySelector('.hero h1, .lib-hero h1, .detail-title');
  const heroEye = document.querySelector('.hero .eyebrow, .lib-hero .eyebrow');
  const heroLead = document.querySelector('.hero .lead, .lib-hero .lead');
  const heroCta = document.querySelector('.hero-cta, .lib-search');
  const heroArt = document.querySelector('.hero-mock, .detail-hero-art');

  if(heroEye)  animate(heroEye,  { opacity:[0,1], y:[12,0] }, { duration:.45, easing:easeOut });
  if(heroH1)   animate(heroH1,   { opacity:[0,1], y:[18,0] }, { duration:.6, delay:.08, easing:easeOut });
  if(heroLead) animate(heroLead, { opacity:[0,1], y:[14,0] }, { duration:.6, delay:.18, easing:easeOut });
  if(heroCta)  animate(heroCta,  { opacity:[0,1], y:[14,0] }, { duration:.55, delay:.28, easing:easeOut });
  if(heroArt)  animate(heroArt,  { opacity:[0,1], scale:[.96,1] }, { duration:.7, delay:.2, easing:easeOut });

  // ---------- 2. Section reveal on scroll ----------
  const sectionsSelector = '.section, .section-tight';
  document.querySelectorAll(sectionsSelector).forEach(s => {
    s.style.opacity = '0';
    s.style.transform = 'translateY(20px)';
    s.style.willChange = 'opacity, transform';
  });
  inView(sectionsSelector, (info) => {
    animate(info.target, { opacity:[0,1], y:[20,0] }, { duration:.55, easing:easeOut });
    return () => {}; // one-shot
  }, { margin: '-60px' });

  // ---------- 3. Card / grid stagger reveal ----------
  function staggerChildren(host, selector){
    const items = host.querySelectorAll(selector);
    if(!items.length) return;
    animate(items, { opacity:[0,1], y:[16,0] }, {
      delay: stagger(0.05),
      duration: .45,
      easing: easeOut
    });
  }

  const STAGGER_TARGETS = [
    ['.cards-grid', ':scope > .card'],
    ['.rich-cat-grid', ':scope > .rich-cat-tile'],
    ['.value-grid', ':scope > .value-card'],
    ['.uc-grid', ':scope > .uc-card'],
    ['.price-grid', ':scope > .price-card'],
    ['.stats-strip', ':scope > .stat-card'],
    ['.quotes', ':scope > .quote'],
    ['.steps', ':scope > .step'],
    ['.timeline', ':scope > .tl-step']
  ];
  STAGGER_TARGETS.forEach(([host, sel])=>{
    document.querySelectorAll(host).forEach(h => {
      const items = h.querySelectorAll(sel);
      items.forEach(i => { i.style.opacity = '0'; });
    });
    inView(host, (info) => {
      staggerChildren(info.target, sel);
    }, { margin: '-40px' });
  });

  // ---------- 4. Game library grid: animate cards on every render (filter / pagination) ----------
  const grid = document.getElementById('grid-results');
  if(grid){
    let lastFirstCard = null;
    const observer = new MutationObserver(() => {
      const cards = grid.querySelectorAll(':scope > .card');
      const firstNow = cards[0];
      if(!cards.length || firstNow === lastFirstCard) return;
      lastFirstCard = firstNow;
      animate(cards, { opacity:[0,1], y:[12,0] }, {
        delay: stagger(0.035, { from: 0 }),
        duration: .35,
        easing: easeOut
      });
    });
    observer.observe(grid, { childList: true });
  }

  // ---------- 5. Stat number count-ups ----------
  const STAT_RX = /^([^\d]*?)(\d[\d,]*)(\.\d+)?(.*)$/;
  inView('.stat-num, .lib-stat strong', (info) => {
    const el = info.target;
    if(el.dataset._counted) return;
    const raw = (el.textContent || '').trim();
    const m = raw.match(STAT_RX);
    if(!m) return;
    const prefix = m[1] || '';
    const intStr = m[2];
    const decStr = m[3] || '';
    const suffix = m[4] || '';
    const n = parseInt(intStr.replace(/,/g,''), 10);
    if(isNaN(n) || n < 3 || n > 1000000000) return;
    el.dataset._counted = '1';
    const start = 0;
    animate(start, n, {
      duration: 1.1,
      easing: easeOut,
      onUpdate: v => {
        el.textContent = prefix + Math.round(v).toLocaleString() + decStr + suffix;
      }
    });
    return () => {};
  });

  // ---------- 6. Modal & walkthrough spring entrance ----------
  document.querySelectorAll('.modal-overlay').forEach(ov => {
    const obs = new MutationObserver(()=>{
      if(ov.classList.contains('open')){
        const modal = ov.querySelector('.modal');
        if(modal){
          animate(modal, { opacity:[0,1], scale:[.94, 1], y:[12, 0] },
            { duration:.32, easing:spring });
        }
      }
    });
    obs.observe(ov, { attributes:true, attributeFilter:['class'] });
  });

  // ---------- 7. Card hover micro-lift (extra polish on top of CSS) ----------
  document.addEventListener('pointerenter', (e) => {
    const card = e.target.closest && e.target.closest('.card, .rich-cat-tile, .uc-card, .price-card');
    if(!card || card.dataset._hovered) return;
    card.dataset._hovered = '1';
    animate(card, { scale: 1.015 }, { duration: .18, easing: easeOut });
  }, true);
  document.addEventListener('pointerleave', (e) => {
    const card = e.target.closest && e.target.closest('.card, .rich-cat-tile, .uc-card, .price-card');
    if(!card || !card.dataset._hovered) return;
    delete card.dataset._hovered;
    animate(card, { scale: 1 }, { duration: .22, easing: easeOut });
  }, true);

  // ---------- 8. Sticky CTA breathing accent (subtle pulse on first viewport) ----------
  const stickyDemo = document.querySelector('.sticky-cta');
  if(stickyDemo){
    setTimeout(() => {
      animate(stickyDemo, { scale:[1, 1.06, 1] }, { duration: .9, easing: easeOut });
    }, 1200);
  }

  // ---------- 9. Pagination buttons: scale on click ----------
  document.addEventListener('click', (e) => {
    const pg = e.target.closest && e.target.closest('.pg-btn, .pg-num');
    if(!pg || pg.disabled) return;
    animate(pg, { scale:[1, .92, 1] }, { duration:.18, easing:easeOut });
  });
})();
