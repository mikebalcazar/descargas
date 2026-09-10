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

El texto de cada programa está en el diccionario `APPS`. Cuando una app entrega
su material en `claude/venta/` de su repositorio, se copian sus capturas a
`sitio/img/<app>/`, su logotipo a `sitio/marca/<app>.svg`, se pasa la app de
`PENDIENTES` a `APPS` y se vuelve a correr el guion.

## Cómo se publica

Push a `main` → GitHub Actions → **Cloudflare Pages** (gratis, sin límite de
tráfico) → https://suite101.pages.dev

Falta una sola cosa, y la tiene que hacer Mike una vez: pegar el secreto
`CLOUDFLARE_API_TOKEN` en Settings → Secrets → Actions de este repositorio
—el mismo valor que ya usan `bitacora-obra` y el portal— y comprobar que ese
token traiga el permiso **Cloudflare Pages: Edit**.

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

El recorte va **pegado al aro**, sin aire: el aro es lo más alto del dibujo, así
que puesto en la página con una altura fija sale del mismo tamaño en los siete
—72 px en la tapa de cada ficha, 34 px en las tarjetas de la portada—. Es la
pieza que los une, y por eso no se toca. El aire va en el CSS, nunca dentro del
SVG. Los siete se arman con el mismo guion, `draw101` incluido: antes era un
dibujo aparte y su aro no medía igual que el de los demás.

## Identidad

Azul `#0080C1` · Sansation en la marca · Raleway en el texto · **Fira Sans en
todas las cifras**, con `unicode-range` para que los dígitos caigan solos en
Fira sin tocar el marcado. Ver `claude/tipografia-cifras-suite101.md`.

## Qué falta

- **Capturas de verdad de nest101, dash101 y peek101.** Hoy el escaparate las
  enseña con **maquetas**, no con capturas: ver más abajo.
- **Dos capturas más de quote101.** Sólo tiene dos, y por eso su página es la
  única que no llega al 70 % de imagen (se queda en 51 %). Las demás van entre
  70 % y 81 %.
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
claro y con datos falsos (`conta-master/claude/venta/*/capturas/README.md`).

## La imagen manda

Se pidió que la imagen ocupara el 70 % de la página. Medido con Chromium a
1440 px, sumando el área de cada `img` y `svg` contra el área total de la
página: portada 72 %, nest101 72 %, draw101 75 %, quell101 70 %, roster101
81 %, dash101 72 %, peek101 72 % y **quote101 51 %**, que es la excepción y se
arregla con dos capturas más. En conjunto, 72 %.
- Dominio propio. Cloudflare Pages lo conecta gratis cuando lo haya.
- Precios: **no van en el sitio**. Decidido por Mike el 9-sep: la única
  llamada a la acción es pedir una demostración. Si alguien pide número, se
  contesta por correo.
