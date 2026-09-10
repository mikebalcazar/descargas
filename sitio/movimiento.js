(() => {
  if (!('IntersectionObserver' in window)) return;
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  const piezas = [...document.querySelectorAll('[data-mueve]')];
  if (!piezas.length) return;
  const activas = new Set();
  let pendiente = false;
  const pinta = () => {
    pendiente = false;
    const alto = innerHeight;
    for (const el of activas) {
      const arriba = el.getBoundingClientRect().top;
      const p = Math.min(1, Math.max(0, (alto - arriba) / (alto * 0.45)));
      el.style.setProperty('--p', p.toFixed(3));
    }
  };
  const pide = () => { if (!pendiente) { pendiente = true; requestAnimationFrame(pinta); } };
  const vigia = new IntersectionObserver(entradas => {
    for (const e of entradas) e.isIntersecting ? activas.add(e.target) : activas.delete(e.target);
    pide();
  }, { rootMargin: '25% 0px' });
  piezas.forEach(el => vigia.observe(el));
  document.documentElement.classList.add('mueve');
  addEventListener('scroll', pide, { passive: true });
  addEventListener('resize', pide);
})();
