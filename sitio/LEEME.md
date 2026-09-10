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
reproduce `roster` con 0.01 de diferencia. `draw101.svg` no sale de ahí: es un
dibujo aparte, anterior.

## Identidad

Azul `#0080C1` · Sansation en la marca · Raleway en el texto · **Fira Sans en
todas las cifras**, con `unicode-range` para que los dígitos caigan solos en
Fira sin tocar el marcado. Ver `claude/tipografia-cifras-suite101.md`.

## Qué falta

- Capturas de nest101, dash101 y peek101. Sus páginas ya están, pero sin
  imagen: el repositorio de nest101 está vacío, y de dash101 y peek101 nadie ha
  tomado capturas todavía (`conta-master/claude/venta/*/capturas/README.md`
  dice cómo: 1600 px, tema claro, datos falsos). Mientras no lleguen, esas
  páginas se arman sin la sección de imágenes; el guion la salta solo.
- La ficha de nest101 es la más corta de las siete: se armó con lo que consta
  en `nest101.json` y con lo que draw101 y quote101 documentan del `.t101x`,
  porque el repositorio `nest101` no tiene material de venta.
- Dominio propio. Cloudflare Pages lo conecta gratis cuando lo haya.
- Precios: **no van en el sitio**. Decidido por Mike el 9-sep: la única
  llamada a la acción es pedir una demostración. Si alguien pide número, se
  contesta por correo.
