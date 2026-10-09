/* La guía de las demostraciones de Suite 101.

   Lleva al visitante por el camino feliz en cuatro pasos y se puede saltar en
   cualquiera. Cada paso espera a que el visitante HAGA la cosa, no a que le dé
   «siguiente»: así aprende la app usándola.

   La página define window.GUIA (los pasos) y window.DEMO (datos de la app) y
   avisa lo que va pasando con eventos propios:

       document.dispatchEvent(new CustomEvent('demo:abrir', {detail:'M01'}))

   Un paso se declara así:

       {t:   'texto del cartelito, con <b> si hace falta',
        espera: 'demo:abrir',      // el evento que lo cierra
        solo:   'M01',             // sólo avanza si detail === esto
        regaño: 'texto si pican otra cosa',
        requiere:'M01',            // si se salen de aquí, de vuelta al paso 1
        marca:  '.selector',       // qué parpadea
        svg:    true,              // si lo que parpadea es un trazo de SVG
        boton:  'Siguiente',       // avanza con botón en vez de evento
        fin:    true}              // la última tarjeta

   Si la página vuelve a dibujar su contenido, lo que parpadeaba se pierde con
   el HTML viejo: llamar guia.remarcar() al terminar de pintar. */

(function () {
  const $ = s => document.querySelector(s);
  const PASOS = window.GUIA || [];
  const APP = window.DEMO_APP || '/';        // adónde va «Conocer <app>»
  const NOMBRE = window.DEMO_NOMBRE || 'la app';

  let paso = 0, viva = PASOS.length > 0, soltar = null;

  function remarcar() {
    document.querySelectorAll('.late,.late-svg').forEach(e =>
      e.classList.remove('late', 'late-svg'));
    if (!viva) return;
    const g = PASOS[paso];
    if (!g || !g.marca) return;
    const el = document.querySelector(g.marca);
    if (!el) return;
    el.classList.add(g.svg ? 'late-svg' : 'late');
    acercar(el);
  }

  // El cartelito está fijo abajo a la izquierda, así que puede quedar encima de
  // lo que la guía está pidiendo picar. Si se encima, o si el objetivo no se ve,
  // se lleva al centro de la pantalla. Sin esto el visitante ve «pícale aquí»
  // sobre un botón que el propio cartelito tapa.
  function acercar(el) {
    const caja = $('#guia');
    if (!caja || caja.hidden) return;
    const r = el.getBoundingClientRect(), c = caja.getBoundingClientRect();
    if (!r.width && !r.height) return;
    const fuera = r.top < 60 || r.bottom > innerHeight - 10;
    const encima = r.left < c.right && r.right > c.left &&
                   r.top < c.bottom && r.bottom > c.top;
    if (fuera || encima) {
      try { el.scrollIntoView({block:'center', inline:'nearest', behavior:'smooth'}); }
      catch (e) { el.scrollIntoView(); }
    }
  }

  function saltarse() {
    const b = document.createElement('button');
    b.className = 'saltar';
    b.textContent = 'Saltar';
    b.onclick = cerrar;
    b.style.marginLeft = 'auto';
    return b;
  }

  function regañar(g) { $('#g-txt').innerHTML = g.regaño || g.t; }

  function pintar() {
    const caja = $('#guia');
    if (!caja) return;
    if (!viva) { caja.hidden = true; remarcar(); return; }
    const g = PASOS[paso];
    caja.hidden = false;
    $('#g-paso').textContent = g.fin ? 'LISTO' : 'PASO ' + (paso + 1) + ' DE ' + (PASOS.length - 1);
    $('#g-txt').innerHTML = g.t;

    const pie = $('#g-pie');
    pie.innerHTML = '';
    if (g.fin) {
      const b = document.createElement('button');
      b.className = 'seguir';
      b.textContent = 'Seguir explorando';
      b.onclick = cerrar;
      pie.appendChild(b);
      const a = document.createElement('a');
      a.className = 'saltar';
      a.href = APP;
      a.textContent = 'Conocer ' + NOMBRE;
      pie.appendChild(a);
    } else if (g.boton) {
      const b = document.createElement('button');
      b.className = 'seguir';
      b.textContent = g.boton;
      b.onclick = avanzar;
      pie.appendChild(b);
      pie.appendChild(saltarse());
    } else {
      const s = document.createElement('span');
      s.className = 'espera';
      s.textContent = 'Te toca a ti';
      pie.appendChild(s);
      pie.appendChild(saltarse());
    }

    if (soltar) { document.removeEventListener(soltar.ev, soltar.fn); soltar = null; }
    if (g.espera) {
      const fn = e => {
        // Si el paso pide una cosa concreta y el visitante abrió otra, no se
        // avanza: el camino feliz tiene que llegar hasta el final.
        if (g.solo && e.detail !== g.solo) { regañar(g); return; }
        document.removeEventListener(g.espera, fn);
        soltar = null;
        avanzar();
      };
      document.addEventListener(g.espera, fn);
      soltar = { ev: g.espera, fn };
    }
    remarcar();
  }

  function avanzar() { if (paso < PASOS.length - 1) { paso++; pintar(); } }

  function cerrar() {
    viva = false;
    if (soltar) { document.removeEventListener(soltar.ev, soltar.fn); soltar = null; }
    pintar();
  }

  /* Si en pleno paso se salen a otra cosa, el camino se rompe: de vuelta al 1. */
  document.addEventListener('demo:abrir', e => {
    const g = PASOS[paso];
    if (viva && g && g.requiere && e.detail !== g.requiere) {
      paso = 0; pintar(); regañar(PASOS[0]);
    }
  });

  /* El aviso de abajo, que usan todas las demostraciones. */
  let reloj;
  window.avisar = function (t) {
    const a = $('#aviso');
    if (!a) return;
    a.textContent = t;
    a.classList.add('ver');
    clearTimeout(reloj);
    reloj = setTimeout(() => a.classList.remove('ver'), 2600);
  };

  window.guia = { remarcar, pintar, cerrar };
  document.addEventListener('DOMContentLoaded', pintar);
  if (document.readyState !== 'loading') pintar();
})();
