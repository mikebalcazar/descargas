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

// El arranque de nest101, tal como lo dibuja el programa en
// electron/splash.html: su gabinete en isométrico, gris claro mate con las
// aristas oscuras, que se despieza. Las diez piezas y su vector de despiece
// (ex, ey, ez) son los suyos, que a su vez salen de iso.solidos_gabinete().
// La proyección, el reparto de tonos y el orden de pintado son los de allá,
// incluidas sus dos correcciones (#080): la profundidad es z−x−y y el costado
// que se ve es el de −X. Lo único que cambia: el despiece avanza con el
// scroll y no con el reloj.
const PIEZAS = [{"x":0,"y":75,"z":0,"dx":900,"dy":18,"dz":100,"ex":0,"ey":-594,"ez":-54},
{"x":0,"y":41,"z":100,"dx":18,"dy":559,"dz":760,"ex":-310.5,"ey":0,"ez":0},
{"x":882,"y":41,"z":100,"dx":18,"dy":559,"dz":760,"ex":310.5,"ey":0,"ez":0},
{"x":18,"y":41,"z":100,"dx":864,"dy":559,"dz":18,"ex":0,"ey":0,"ez":-270},
{"x":18,"y":41,"z":842,"dx":864,"dy":559,"dz":18,"ex":0,"ey":0,"ez":310.5},
{"x":10,"y":594,"z":110,"dx":880,"dy":6,"dz":740,"ex":0,"ey":405,"ez":0},
{"x":19,"y":41,"z":484,"dx":862,"dy":533,"dz":18,"ex":0,"ey":-94.5,"ez":-121.5},
{"x":18,"y":41,"z":810,"dx":864,"dy":18,"dz":50,"ex":0,"ey":-324,"ez":67.5},
{"x":1.5,"y":20,"z":101.5,"dx":447,"dy":18,"dz":728.5,"ex":0,"ey":-405,"ez":0},
{"x":451.5,"y":20,"z":101.5,"dx":447,"dy":18,"dz":728.5,"ex":0,"ey":-405,"ez":0}];

const C30 = Math.cos(Math.PI / 6), S30 = Math.sin(Math.PI / 6);
const proy = (x, y, z) => [(x - y) * C30, (x + y) * S30 + z];
const hondo = (x, y, z) => z - x - y;
const TONO = { arriba: '#f1f1f1', frente: '#d7d7d7', lado: '#b6b6b6' }, TINTA = '#101317';
const mover = (p, f) => ({ x: p.x + p.ex * f, y: p.y + p.ey * f, z: p.z + p.ez * f,
                           dx: p.dx, dy: p.dy, dz: p.dz });

function caras(p) {
  const { x, y, z, dx, dy, dz } = p;
  return [['arriba', [[x, y, z + dz], [x + dx, y, z + dz], [x + dx, y + dy, z + dz], [x, y + dy, z + dz]]],
          ['frente', [[x, y, z], [x + dx, y, z], [x + dx, y, z + dz], [x, y, z + dz]]],
          ['lado',   [[x, y, z], [x, y + dy, z], [x, y + dy, z + dz], [x, y, z + dz]]]];
}
// Contorno grueso por fuera y línea fina adentro: es lo que hace que la tabla
// se lea como sólido y no como papel doblado.
function silueta(p) {
  const { x, y, z, dx, dy, dz } = p, v = [];
  for (const a of [x, x + dx]) for (const b of [y, y + dy]) for (const c of [z, z + dz]) v.push(proy(a, b, c));
  v.sort((m, n) => m[0] - n[0] || m[1] - n[1]);
  const giro = (o, a, b) => (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0]);
  const media = pts => { const r = []; for (const q of pts) {
    while (r.length >= 2 && giro(r[r.length - 2], r[r.length - 1], q) <= 0) r.pop(); r.push(q); } r.pop(); return r; };
  return media(v).concat(media(v.slice().reverse()));
}
// Para cajas alineadas, el eje que decide cuál tapa a cuál es el que NO
// comparten. Preguntar eje por eje sin esa condición rompía el orden.
const enc2 = (a0, a1, b0, b1) => a0 < b1 - 0.01 && b0 < a1 - 0.01;
const cercaP = p => p.z - (p.x + p.dx) - (p.y + p.dy);
const lejosP = p => (p.z + p.dz) - p.x - p.y;
function tapa(a, b) {
  const ox = enc2(a.x, a.x + a.dx, b.x, b.x + b.dx), oy = enc2(a.y, a.y + a.dy, b.y, b.y + b.dy),
        oz = enc2(a.z, a.z + a.dz, b.z, b.z + b.dz);
  if (oy && oz) return a.x + a.dx <= b.x + 0.01;
  if (ox && oz) return a.y + a.dy <= b.y + 0.01;
  if (ox && oy) return a.z >= b.z + b.dz - 0.01;
  return cercaP(a) >= lejosP(b) - 0.01;
}
function ordenar(cajas) {
  const n = cajas.length, c = cajas.map(p => hondo(p.x + p.dx / 2, p.y + p.dy / 2, p.z + p.dz / 2));
  const grado = new Array(n).fill(0), despues = Array.from({ length: n }, () => []);
  for (let i = 0; i < n; i++) for (let j = 0; j < n; j++)
    if (i !== j && tapa(cajas[i], cajas[j])) { despues[j].push(i); grado[i]++; }
  const listo = new Array(n).fill(false), orden = [];
  for (let k = 0; k < n; k++) {
    let e = -1;
    for (let i = 0; i < n; i++) if (!listo[i] && grado[i] === 0 && (e < 0 || c[i] < c[e])) e = i;
    if (e < 0) for (let i = 0; i < n; i++) if (!listo[i] && (e < 0 || c[i] < c[e])) e = i;
    listo[e] = true; orden.push(e);
    for (const s of despues[e]) grado[s]--;
  }
  return orden.map(i => cajas[i]);
}
// El encuadre se calcula con el despiece abierto del todo, así el mueble no
// cambia de tamaño mientras se abre.
function encuadre(cv) {
  let x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9;
  for (const f of [0, 1]) for (const p of PIEZAS) for (const [, pts] of caras(mover(p, f))) for (const v of pts) {
    const [a, b] = proy(v[0], v[1], v[2]);
    x0 = Math.min(x0, a); x1 = Math.max(x1, a); y0 = Math.min(y0, b); y1 = Math.max(y1, b);
  }
  const m = 18, k = Math.min((cv.width - 2 * m) / (x1 - x0), (cv.height - 2 * m) / (y1 - y0));
  return { k, ox: (cv.width - (x1 - x0) * k) / 2 - x0 * k, oy: (cv.height + (y1 - y0) * k) / 2 + y0 * k };
}
function despiezar(cv, enc, f) {
  const cx = cv.getContext('2d');
  const pant = ([a, b]) => [enc.ox + a * enc.k, enc.oy - b * enc.k];
  const trazo = (pts, tresD) => { cx.beginPath(); pts.forEach((v, i) => {
    const [px, py] = tresD ? pant(proy(v[0], v[1], v[2])) : pant(v);
    i ? cx.lineTo(px, py) : cx.moveTo(px, py); }); cx.closePath(); };
  cx.clearRect(0, 0, cv.width, cv.height);
  cx.lineJoin = cx.lineCap = 'round'; cx.strokeStyle = TINTA;
  for (const p of ordenar(PIEZAS.map(q => mover(q, f)))) {
    for (const [cara, pts] of caras(p)) { trazo(pts, true); cx.fillStyle = TONO[cara]; cx.fill(); }
    cx.lineWidth = 1; for (const [, pts] of caras(p)) { trazo(pts, true); cx.stroke(); }
    cx.lineWidth = 2; trazo(silueta(p), false); cx.stroke();
  }
}

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
          : app === 'nest101'
          ? `<div class="splash despiece" aria-hidden="true"><canvas width="1200" height="820"></canvas>` +
            `<div class="marca-arr">${logo}<div class="carga"><i></i></div>` +
            `<div class="estado">Iniciando…</div></div></div>`
          : `<div class="splash" aria-hidden="true">${logo}<div class="carga"><i></i></div></div>`);
        const cv = el.querySelector('.despiece canvas');
        if (cv) { el.__enc = encuadre(cv); despiezar(cv, el.__enc, 0); }
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
        const cv = el.querySelector('.despiece canvas');
        // El mueble se abre entre 0.10 y 0.60 del avance; después ya está el
        // despiece completo y lo que corre es el fundido a la captura.
        if (cv) despiezar(cv, el.__enc, Math.min(1, Math.max(0, (p - 0.10) / 0.50)));
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
