# Material de venta — Suite 101

Aquí vive lo que se le enseña a un cliente. Cada app deja su materia prima en
**su propio repositorio**, en `claude/venta/`; las apps de escritorio, que no
tienen repositorio, la dejan aquí en `venta/<app>/`.

| Carpeta | Qué es |
|---|---|
| `venta/<app>/` | materia prima: `ficha.md`, `datos.md`, `capturas/`, `marca/` |
| `venta/fichas/` | la ficha comercial armada — una hoja A4, en HTML y en PDF |
| `venta/herramientas/armar-fichas.py` | el guion que arma esas hojas |

## Cómo se arma una ficha

`armar-fichas.py` junta la materia prima y escupe un HTML **autocontenido**: las
tres fuentes y las capturas van dentro del archivo en base64. **Cero peticiones
a internet** — se ve igual en la computadora del cliente, sin señal y sin
Google Fonts. El PDF sale del mismo HTML.

La identidad es la de siempre: azul `#0080C1`, Sansation en la marca, Raleway en
el texto y **Fira Sans en todas las cifras**, con `unicode-range` para que los
dígitos caigan solos en Fira sin tocar el marcado. Ver
`claude/tipografia-cifras-suite101.md` en el proyecto.

## Regla

Si cambia lo que hace la app, cambian `ficha.md`, `datos.md` y las capturas
afectadas **en el mismo PR**, y se vuelve a armar la hoja. Una ficha que
promete lo que la app ya no hace es peor que no tener ficha.

## Estado

| App | materia prima | hoja armada |
|---|---|---|
| roster101 | `t101-portal-trabajadores/claude/venta/` | ✅ |
| quell101 | `bitacora-obra/claude/venta/` | ✅ |
| draw101 | `venta/draw101/` | ✅ |
| quote101 | `cotizador-t101/claude/venta/` | falta: capturas en tema claro |
| dash101 · peek101 | `conta-master/claude/venta/` | pendiente |
| nest101 | `venta/nest101/` | pendiente |
