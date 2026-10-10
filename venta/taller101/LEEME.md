# taller101 — marca y manual de imagen

La imagen de **taller101**, el taller. No la de suite101 ni la de los diez
programas: ésos heredan de aquí el aro, el azul y las letras, pero tienen su
propia hoja.

**La autoridad es `Logo taller101 - NEW.svg`**, en la raíz del repositorio
`bitacora-obra`. Todo lo de aquí sale de ese archivo copiando sus trazos. Nada
se redibuja, nada se calca de un PNG.

## `manual/`

| Archivo | Qué es | Cómo se generó |
| --- | --- | --- |
| `manual-imagen-taller101.pdf` | el manual: 11 hojas A4, con las cuatro fuentes adentro | `python3 armar-manual.py && node imprimir.mjs` |
| `armar-manual.py` | arma el HTML autocontenido del manual | — |
| `imprimir.mjs` | lo pasa a PDF con Playwright, A4 sin márgenes | — |
| `rasters.py` | rasteriza el logotipo a píxeles de verdad para las pruebas de tamaño mínimo | — |
| `marca.py` | los trazos del maestro, copiados | — |

## `marca/`

| Archivo | Para qué |
| --- | --- |
| `taller101-azul.svg` · `.png` (1024 px) | logotipo sobre fondo claro |
| `taller101-blanco.svg` · `.png` | sobre fondo oscuro o sobre el azul |
| `taller101-negro.svg` | una sola tinta: impresión, sellos, grabado |
| `taller101-placa.svg` · `.png` | blanco sobre placa azul |
| `taller101-icono.svg` · `-512.png` · `-192.png` · `-180.png` | ícono de app y pantalla de inicio del celular |
| `taller101-icono-chico.svg` · `-32.png` | el de 32 px: el aro 1,8 veces más grueso |
| `taller101-icono-minimo.svg` · `-16.png` | el de 16 px: sólo el «101», sin aro |
| `taller101.ico` | favicon, con 16, 32, 48 y 64 adentro |
| `taller101-og-1200x630.svg` · `.png` | tarjeta para redes y WhatsApp |

Se arma todo con un comando:

```bash
python3 venta/taller101/marca/armar-marca.py venta/taller101/marca
```

### Lo que hay que saber

- **Los SVG del logotipo traen adentro el aire mínimo** (el alto entre 6), para
  que nadie los pegue a ras de una orilla. El dibujo a caja justa —donde el alto
  del aro es el alto del logotipo— vive en `sitio/marca/logos.svg`, que es el
  que usa el sitio.
- **El ícono va en tres dibujos, no en uno.** Se midió: el aro normal se cierra
  en chico. A 32 px hace falta engrosarlo 1,8 veces; a 16 px no cabe de ninguna
  manera y se queda sólo el «101», que es la pieza que de verdad identifica.
- **El `.ico` se arma a mano**, no con Pillow: su `append_images` se come los
  tamaños extra y dejaba un favicon de un solo tamaño. Se comprueba abriéndolo
  y pidiéndole los cuatro.
- **Azul `#0080C1`.** El maestro de Illustrator trae `#0381C2`, un pelo
  distinto; la diferencia no se ve, pero son dos valores y está pendiente
  unificarlos. El manual declara `#0080C1`.
- Sansation Bold en la marca, Raleway en el texto, **Fira Sans en todas las
  cifras**. Las razones, medidas, están en las hojas 7 y 8 del manual.

### Lo generado no vive en el repositorio

Aquí viven **`marca.py` (los trazos del maestro) y los guiones**. Los SVG, los
PNG, el `.ico` y el PDF salen de ahí con un comando, así que no se guardan:
sería guardar dos veces lo mismo y arriesgarse a que la copia se despegue de su
fuente sin que nadie se entere. Para tenerlos en la mano:

```bash
python3 venta/taller101/marca/armar-marca.py venta/taller101/marca
cd venta/taller101/manual && python3 armar-manual.py && node imprimir.mjs
```
