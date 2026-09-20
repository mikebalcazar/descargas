# sitio — escaparate de Suite 101

Estático puro: HTML y una hoja de estilo. **Sin marco, sin build, sin
peticiones a internet.** Las fuentes viven en `fuentes/` y las capturas en
`img/`, así que el sitio se ve igual con la red caída y no le avisa a Google
quién lo visitó.

| Ruta | Qué es |
|---|---|
| `index.html` | portada: los siete programas y cómo encajan |
| `app/<app>.html` | una página por programa |
| `estilo.css` · `fuentes/` · `img/` · `marca/` | lo demás |
| `herramientas/armar-sitio.py` | el guion que arma todo |

## Cómo se cambia

No se edita el HTML a mano: **se edita `herramientas/armar-sitio.py` y se vuelve
a correr** desde la raíz del repositorio.

    python3 sitio/herramientas/armar-sitio.py

**`estilo.css` y `movimiento.js` sí se editan directamente.** Antes vivían
dentro del guion como cadenas, y retocar un color obligaba a mover 56 KB. El
guion arma el HTML y `marca/logos.svg`; el estilo y el movimiento son suyos.

El texto de cada programa está en el diccionario `APPS`. Cuando una app entrega
su material en `claude/venta/` de su repositorio, se copian sus capturas a
`sitio/img/<app>/`, su logotipo a `sitio/marca/<app>.svg`, se pasa la app de
`PENDIENTES` a `APPS` y se vuelve a correr el guion.

## Cómo se publica

Push a `main` → GitHub Actions → **Cloudflare Pages** (gratis, sin límite de
tráfico) → https://suite101.pages.dev

El secreto `CLOUDFLARE_API_TOKEN` está puesto desde el 10-sep y trae
**Cloudflare Pages: Edit**. Cada publicación mide lo servido contra el commit,
archivo por archivo, y deja el resultado como comentario del commit.

## Logotipos

`sitio/marca/<app>.svg`. Los arma `sitio/herramientas/armar-logo.py`, que toma
el logotipo de taller101 y le cambia la palabra:

```bash
python3 sitio/herramientas/armar-logo.py quote nest dash peek
```

La geometría se midió sobre `roster101.svg` y `quell101.svg`, que ya venían del
original: Sansation Bold en trazos, apretón de -0.05 em, la palabra alineada a
la derecha por su avance y el aro y el «101» en coordenadas fijas. El guion
reproduce `roster` con 0.01 de diferencia.

Están los **nueve**: los siete del sitio, `shape101` —que todavía no sale en el
sitio pero ya se descarga y ya necesita su logotipo— y `suite101`, el de la
suite, que es el mismo dibujo con el aro relleno y el «101» calado. El 19-sep se
volvieron a generar los nueve de un tiro y los ocho que ya existían salieron
**idénticos byte a byte**: la prueba de que el guion no se ha movido.

Copia de los nueve en Drive, en `suite101/marca/`, para las otras apps y para
quien no clona el repositorio. El manual de imagen los documenta hoja por hoja.

El recorte va **pegado al aro**, sin aire: el aro es lo más alto del dibujo, así
que puesto en la página con una altura fija sale del mismo tamaño en los siete
—entre 52 y 72 px en la tapa de cada programa y entre 44 y 58 px en los
mosaicos de la portada, según el ancho de la pantalla—. Es la
pieza que los une, y por eso no se toca. El aire va en el CSS, nunca dentro del
SVG. Los siete se arman con el mismo guion, `draw101` incluido: antes era un
dibujo aparte y su aro no medía igual que el de los demás.

**El de la suite, `suite101.svg`**, sale del mismo guion con una diferencia que
dijo Mike el 10-sep: el aro es un círculo relleno y el «101» va calado,
transparente. Es un solo trazo con `fill-rule="evenodd"`, así que el «101» deja
ver el fondo de verdad, no se pinta de blanco. El aro lleno es sólo de la
suite; los programas llevan el aro abierto. Desde el 11-sep va en la barra
del sitio, a 26 px de alto, en lugar de la palabra escrita.

## Diseño (10-sep, inspirado en apple.com)

Mike pidió tomar apple.com como referencia. Lo que se tomó de ahí:

- **Mosaicos.** Cada programa es un bloque a lo ancho de la pantalla: logotipo
  como título, su frase, dos píldoras («Más información» y «Pedir
  demostración»), su estado y su pantalla grande. Los tres que tocan el mueble
  antes de fabricarlo van a todo lo ancho; los otros cuatro, de a dos, en damero
  claro y oscuro.
- **Píldoras.** Llena para la acción principal, de contorno para la otra.
- **Barra de la app.** En cada programa, debajo de la barra de la suite, otra
  con su logotipo y «Pedir demostración», que se queda arriba al bajar.
- **Una pantalla por sección** en la página de cada programa, con su frase
  encima y el fondo alterno, en vez de capturas apiladas.
- **Ficha técnica** al final de «Qué trae», con etiquetas en letra normal, no en
  mayúsculas.
- **Tres equipos, dibujados con CSS, sin imagen** (11-sep). Cada programa sale
  en el equipo donde se usa de verdad: **monitor de escritorio con ratón** para
  nest101 y draw101, que se instalan en Windows; **tableta** para quell101, que
  se usa de pie en la obra; **laptop** para las de web. Las capturas más altas
  que anchas van sueltas y angostas, fuera de marco (lo decide `equipo()` en el
  guion, con la medida del PNG).

  En el HTML todas nacen como laptop; `movimiento.js` le pone a cada una su
  equipo al cargar, leyendo a qué app pertenece la imagen (tabla `EQUIPOS`). Así
  el marcado no cambia al cambiar de equipo y, sin JavaScript, todas se ven como
  laptop, que es lo que ya estaba publicado.
- **Cinco entradas distintas** (`e-sube`, `e-izq`, `e-der`, `e-zoom`,
  `e-endereza`). La primera pantalla de cada app tiene la suya; las demás de esa
  página rotan, para que bajar no se sienta repetido. Se probó levantar la tapa
  de la laptop y se quitó: de frente, la tapa inclinada se veía más grande en
  vez de cerrada.
- **Pantalla de arranque** en nest101 y draw101, que son programas que se
  instalan: al entrar se ve el arranque y al seguir bajando funde a la captura.
  - **draw101 es el de verdad** (12-sep). Su arranque no es una imagen: es
    `electron/cargando.html` en su repositorio, un plano de cocina en planta,
    en perspectiva, que el programa traza solo mientras arranca el motor de
    Python. Aquí está recreado con los mismos trazos, las mismas cotas, el
    mismo rótulo y los colores de su `core/config.py`; lo único que cambia es
    que **se traza con el scroll y no con el reloj**. El fondo es claro porque
    en el programa la ventana es transparente y se ve el escritorio.
  - **nest101 todavía no.** Su arranque existe —`electron/splash.html`, 61 KB—
    pero no se ha abierto; mientras tanto lleva el genérico: logotipo sobre la
    tinta de la marca con una barra de carga. Se cambia en cuanto se lea.
- **Planos de fondo con parallax.** Tres capas de trazos en azul claro
  —retícula, cotas y el alzado de un mueble— que se mueven a distinta velocidad
  con el scroll. Van dibujadas en el propio `estilo.css` como SVG en
  `background-image`: no son archivos ni peticiones. El JS pone un `.planos` por
  sección y le lleva el avance `--y`.
- **Movimiento al bajar** (`movimiento.js`). El avance `--p` va de 0 a 1
  mientras cada pieza entra a la pantalla, y con él corren la entrada, el
  arranque y el encendido. Si el sistema pide menos movimiento, los equipos se
  arman igual pero no se mueve nada ni hay planos; sin JavaScript todo se ve
  quieto y completo.
- **Logotipos en un solo archivo**, `marca/logos.svg`, que arma el guion a partir
  de `marca/<app>.svg`. Las páginas los llaman con `<use>` y el color lo pone el
  CSS. La portada bajó de 45 KB a 10 KB.

Reglas que no se rompen:

- **Ninguna imagen se estira.** `img{height:auto}`: manda el ancho y la altura
  sale de la proporción. El 10-sep el montaje de la portada salía de 390 × 1020
  en el celular porque traía `height="1020"` en el HTML sin `height:auto`.
- **En el celular.** El montaje de la portada se corta en cuadrado con
  `object-fit:cover` para que se lea. Las laptops se dejan un poco más anchas que
  la pantalla; el monitor y la tableta no, porque su marco se vería cortado.
- **Dos azules.** `--azul` (#0080C1) es el de la marca, para logotipos y
  acentos. Para letra y botones va `--azul-texto` (#0074ad): el de la marca da
  4.3 de contraste sobre blanco y la norma pide 4.5. Sobre fondo oscuro los
  logotipos pasan al `--claro` (#3AA3DC), que da 5.5.

## Identidad

Azul `#0080C1` · Sansation en la marca · Raleway en el texto · **Fira Sans en
todas las cifras**, con `unicode-range` para que los dígitos caigan solos en
Fira sin tocar el marcado. Ver `claude/tipografia-cifras-suite101.md`.

## Qué falta

- **Capturas de verdad de nest101, dash101 y peek101.** Hoy el escaparate las
  enseña con **maquetas**, no con capturas: ver más abajo.
- **Dos capturas más de quote101.** Sólo tiene dos, y es la página con menos
  imagen de las siete. Las dos que hay traen un ícono roto en el buscador y los
  filtros encimados: hay que volver a tomarlas.
- La ficha de nest101 es la más corta de las siete: se armó con lo que consta
  en `nest101.json` y con lo que draw101 y quote101 documentan del `.t101x`,
  porque el repositorio `nest101` no tiene material de venta.

## Maquetas, no capturas

De nest101, dash101 y peek101 no hay captura y no se les puede tomar una: el
repositorio de nest101 está vacío, y dash101 y peek101 piden cuenta y hoy sólo
tienen datos de clientes de verdad. Para que el escaparate no saliera cojo se
armaron **maquetas** con `sitio/herramientas/armar-maquetas.py`:

```bash
python3 sitio/herramientas/armar-maquetas.py
```

Son dibujos de la pantalla, hechos con la identidad de la suite y con datos
inventados. **Ninguna enseña una función que no esté en la ficha de su
aplicación**, pero no son la aplicación: son un cómo se vería. Se llaman
`maqueta-*.png` para que se distingan de un vistazo.

**Se van en cuanto haya capturas de verdad.** Se borran los `maqueta-*.png` de
la carpeta, se ponen las capturas con su nombre y se corrige la lista `img=`
de esa aplicación en `armar-sitio.py`. Las capturas se toman a 1600 px, tema
claro y con datos falsos (`dash101/claude/venta/*/capturas/README.md`).

## La imagen manda

Se pidió que la imagen ocupara el 70 % de la página. Medido con Chromium a
1440 px, sumando el área visible de cada `img` y `svg` contra el área total de
la página, el diseño del 10-sep por la mañana daba 72 % en conjunto.

**El rediseño inspirado en apple.com lo bajó**, medido igual: portada 45 %,
conjunto 44 % a 1440; a 390, 23 %. Apple alterna una pantalla grande con aire y
titulares; el diseño anterior apilaba capturas. **Pendiente de que Mike diga
cuál manda.**
- Dominio propio. Cloudflare Pages lo conecta gratis cuando lo haya.
- Precios: **no van en el sitio**. Decidido por Mike el 9-sep: la única
  llamada a la acción es pedir una demostración. Si alguien pide número, se
  contesta por correo.
