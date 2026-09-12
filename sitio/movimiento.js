(() => {
  // Qué equipo y qué entrada le toca a la pantalla principal de cada app. El
  // equipo es el de verdad: monitor de escritorio para las que se instalan en
  // Windows, tableta para la que se usa de pie en la obra, laptop para las de
  // web. 'arranca' es la pantalla de arranque del programa.
  const EQUIPOS = {
    quote101:  ['laptop',     'e-sube'],
    nest101:   ['escritorio', 'e-zoom',     'arranca'],
    draw101:   ['escritorio', 'e-izq',      'arranca'],
    quell101:  ['tableta',    'e-endereza'],
    roster101: ['laptop',     'e-der'],
    dash101:   ['laptop',     'e-izq'],
    peek101:   ['laptop',     'e-zoom'],
  };
  // Las demás pantallas de cada página rotan entrada, para que bajar por una
  // página no se sienta siempre igual.
  const ROTA = ['e-der', 'e-zoom', 'e-izq', 'e-sube'];

  const piezas = [...document.querySelectorAll('[data-mueve]')];
  const cuenta = {};
  for (const el of piezas) {
    const img = el.querySelector('img');
    const app = img && (img.getAttribute('src').match(/([a-z]+101)\//) || [])[1];
    if (!app || !EQUIPOS[app]) { el.classList.add('e-sube'); continue; }
    const [equipo, entrada, arranca] = EQUIPOS[app];
    const n = cuenta[app] = (cuenta[app] || 0) + 1;
    if (!el.classList.contains('suelta')) {
      if (equipo !== 'laptop') el.classList.add(equipo);
      if (equipo === 'escritorio') el.insertAdjacentHTML('beforeend', '<div class="raton"></div>');
    }
    el.classList.add(n === 1 ? entrada : ROTA[(n - 2) % ROTA.length]);
    // El arranque y el encendido, sólo en la primera pantalla de cada app.
    const marca = document.querySelector(`.nombre use[href*="#${app}"], .subbarra use[href*="#${app}"]`);
    if (n === 1 && el.querySelector('.pantalla')) {
      if (arranca && marca) {
        el.classList.add('arranca');
        el.querySelector('.pantalla').insertAdjacentHTML('beforeend',
          `<div class="splash" aria-hidden="true"><svg viewBox="${marca.closest('svg').getAttribute('viewBox')}">` +
          `<use href="${marca.getAttribute('href')}"/></svg><div class="carga"><i></i></div></div>`);
      } else if (el.classList.contains('enciende') === false) {
        el.classList.add('enciende');
      }
    }
  }

  if (!('IntersectionObserver' in window)) return;
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  // Los planos del fondo, sección por sección. Van en las claras y en las
  // oscuras; no en la portada, que ya tiene el montaje de los tres programas.
  const fondos = [...document.querySelectorAll('.mosaico,.vista,.encajan,.cierre,.bloque,.intro')];
  for (const s of fondos) s.insertAdjacentHTML('afterbegin', '<div class="planos" aria-hidden="true"></div>');

  const activas = new Set();
  let pendiente = false;
  const pinta = () => {
    pendiente = false;
    const alto = innerHeight;
    for (const el of activas) {
      const r = el.getBoundingClientRect();
      if (el.classList.contains('planos')) {
        // -1 cuando la sección viene subiendo, +1 cuando ya se fue: mueve las
        // tres capas a distinta velocidad.
        const centro = (r.top + r.height / 2) - alto / 2;      // 0 = la sección está centrada
        const y = Math.max(-1, Math.min(1, -centro / (alto / 2 + r.height / 2)));
        el.style.setProperty('--y', y.toFixed(3));
        continue;
      }
      const p = Math.min(1, Math.max(0, (alto - r.top) / (alto * 0.45)));
      el.style.setProperty('--p', p.toFixed(3));
      if (el.classList.contains('arranca')) {
        const barra = el.querySelector('.carga i');
        if (barra) barra.style.setProperty('--carga', Math.min(1, p / 0.55).toFixed(3));
      }
    }
  };
  const pide = () => { if (!pendiente) { pendiente = true; requestAnimationFrame(pinta); } };
  const vigia = new IntersectionObserver(entradas => {
    for (const e of entradas) e.isIntersecting ? activas.add(e.target) : activas.delete(e.target);
    pide();
  }, { rootMargin: '25% 0px' });
  [...piezas, ...document.querySelectorAll('.planos')].forEach(el => vigia.observe(el));
  document.documentElement.classList.add('mueve');
  addEventListener('scroll', pide, { passive: true });
  addEventListener('resize', pide);
})();
