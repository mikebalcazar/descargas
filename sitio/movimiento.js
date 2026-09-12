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


// El arranque de draw101, tal como lo dibuja el programa en
// electron/cargando.html: la planta de una cocina en L con su isla, sus cotas
// y su rótulo. Mismos trazos y mismos colores (core/config.py); lo único que
// cambia es que aquí se traza con el scroll y no con el reloj.
const PLANO = `<svg viewBox="0 0 620 420" xmlns="http://www.w3.org/2000/svg">
<rect x="0" y="0" width="620" height="420" rx="3" fill="rgba(255,255,255,.92)" stroke="rgba(0,128,193,.35)"/>
<g stroke="rgba(0,128,193,.14)" stroke-width=".6"><path d="M60 0V420M120 0V420M180 0V420M240 0V420M300 0V420M360 0V420M420 0V420M480 0V420M540 0V420M0 60H620M0 120H620M0 180H620M0 240H620M0 300H620M0 360H620"/></g>
<g stroke="#122733" stroke-width="5" opacity=".85" stroke-linejoin="miter">
<path class="traza t1" d="M70 60H550V340H70Z"/><path class="traza t1" d="M300 60V150"/></g>
<g stroke="#0080C1" stroke-width=".9" stroke-linecap="round">
<path class="traza t2" d="M420 340H500"/><path class="traza t2" d="M420 340A80 80 0 0 1 500 260"/>
<path class="traza t2" d="M360 56H480M360 64H480"/>
<path class="traza t2" d="M76 96H120"/><path class="traza t2" d="M106 126V334"/>
<path class="traza t3" d="M136 66V126M196 66V126M246 66V126M76 176H136M76 226H136M76 276H136"/>
<circle class="traza t3" cx="183" cy="96" r="5"/><path class="traza t3" d="M183 78v-8"/>
<circle class="traza t3" cx="95" cy="199" r="7"/><circle class="traza t3" cx="117" cy="199" r="7"/>
<circle class="traza t3" cx="95" cy="223" r="7"/><circle class="traza t3" cx="117" cy="223" r="7"/>
<path class="traza t3" d="M310 103h64M368 72v26"/>
<path class="traza t3" d="M230 214h180M320 190v70"/>
<circle class="traza t4" cx="260" cy="282" r="10"/><circle class="traza t4" cx="320" cy="282" r="10"/>
<circle class="traza t4" cx="380" cy="282" r="10"/></g>
<g stroke="#0080C1" stroke-width="1.6" stroke-linejoin="round" stroke-linecap="round">
<path class="traza t2" d="M76 66H294V126H136V334H76Z"/>
<path class="traza t3" d="M148 78h70a6 6 0 0 1 6 6v26a6 6 0 0 1-6 6h-70a6 6 0 0 1-6-6V84a6 6 0 0 1 6-6z"/>
<path class="traza t3" d="M82 186h48v50H82z"/><path class="traza t3" d="M310 66h64v74h-64z"/>
<path class="traza t3" d="M230 190h180v70H230z"/></g>
<g class="aparece" stroke="#C8813A" stroke-width=".9">
<path d="M70 372V386M550 372V386M70 380H550"/><path d="M74 376l-4 4 4 4M546 376l4 4-4 4"/>
<path d="M578 60H592M578 340H592M586 60V340"/><path d="M582 64l4-4 4 4M582 336l4 4 4-4"/>
<path d="M230 166V178M410 166V178M230 172H410"/>
<path d="M40 66H52M40 334H52M46 66V334"/></g>
<g class="aparece" fill="#C8813A" font-family="Cifras,Raleway,sans-serif" font-size="9" text-anchor="middle" stroke="none">
<text x="310" y="394">4800</text><text x="606" y="204" transform="rotate(90 606 204)">2800</text>
<text x="320" y="166">1800</text><text x="30" y="204" transform="rotate(-90 30 204)">2680</text></g>
<g class="aparece"><path d="M470 356H612V412H470Z M470 376H612 M540 376V412" stroke="#0080C1" stroke-width=".9"/>
<g fill="#0080C1" font-family="Cifras,Raleway,sans-serif" font-size="9" text-anchor="middle" stroke="none">
<text x="505" y="369">COCINA · PLANTA</text><text x="505" y="396">ESC 1:20</text><text x="576" y="396">A-01</text></g></g>
</svg>`;

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
        const vb = marca.closest('svg').getAttribute('viewBox');
        const logo = `<svg viewBox="${vb}"><use href="${marca.getAttribute('href')}"/></svg>`;
        el.querySelector('.pantalla').insertAdjacentHTML('beforeend', app === 'draw101'
          ? `<div class="splash plano" aria-hidden="true"><div class="escena"><div class="hoja3d">${PLANO}</div></div>` +
            `<div class="marca-arr">${logo}<div class="sub">Dibujo 2D · Taller 101</div>` +
            `<div class="estado">Cargando aplicación</div></div></div>`
          : `<div class="splash" aria-hidden="true">${logo}<div class="carga"><i></i></div></div>`);
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
