# Material de venta — Suite 101

Aquí vive lo que se le enseña a un cliente. Cada app deja su materia prima en
**su propio repositorio**, en `claude/venta/`; las apps de escritorio, que no
tienen repositorio, la dejan aquí en `venta/<app>/`.

**En este repositorio todo lo de venta vive en `venta/`, no en `claude/venta/`.**
`claude/` es para las notas y el semáforo de los chats; `venta/` es producto: lo
mismo la materia prima que las hojas armadas y el guion que las arma. El 9-sep
la sesión de draw101 subió su material a `claude/venta/draw101/` en la rama
`claude/venta-draw101`; se integró el contenido y se dejó en `venta/draw101/`.

| Carpeta | Qué es |
|---|---|
| `venta/<app>/` | materia prima: `ficha.md`, `datos.md`, `capturas/`, `marca/` |
| `venta/fichas/` | la ficha comercial armada — una hoja A4, en HTML y en PDF |
| `venta/herramientas/armar-fichas.py` | el guion que arma esas hojas |
| `venta/herramientas/marca-svg.py` | saca el logotipo en SVG de los contornos de Sansation |

## El logotipo en vector

`armar-fichas.py` espera `<app>/marca/logo.svg` ya hecho, y no todas las apps
tienen uno: el de nest101 estaba compuesto sobre un PNG. Para esos casos está
`marca-svg.py`, que saca los contornos directamente de `sansation-700.woff2`:

```bash
python3 venta/herramientas/marca-svg.py nest101 venta/nest101/marca/
```

Sale sin `<text>` y sin `font-family`, puros `<path>`, igual que el de draw101.
Así se ve igual en la computadora de un cliente que no tenga Sansation
instalada, que es exactamente el caso que importa.

Calcar el PNG habría sido lo obvio y es peor por dos razones: arrastra los
bordes suaves del original y los vuelve dientes, y se despega de la fuente —si
Sansation cambia de versión, el calco se queda con la forma vieja y nadie se
entera. Esto no puede discrepar de la marca porque sale de la marca.

## Cómo se arma una ficha

`armar-fichas.py` junta la materia prima y escupe un HTML **autocontenido**: las
tres fuentes y las capturas van dentro del archivo en base64. **Cero peticiones
a internet** — se ve igual en la computadora del cliente, sin señal y sin
Google Fonts. El PDF sale del mismo HTML.

La identidad es la de siempre: azul `#0080C1`, Sansation en la marca, Raleway en
el texto y **Fira Sans en todas las cifras**, con `unicode-range` para que los
dígitos caigan solos en Fira sin tocar el marcado. Ver
`claude/tipografia-cifras-suite101.md` en el proyecto.

## Decisiones de Mike (9-sep-2026)

- **Se vende como Suite 101**, marca propia. Taller 101 es el taller que la usa
  y la probó, no el nombre del producto.
- **Sin precios públicos.** La única llamada a la acción es pedir una
  demostración, a `info@forespot.com`.
- **macOS de draw101 se anuncia** como «en preparación».
- **Nada de números medidos en una sola máquina.** El claim de «130 000 trazos
  en 35 ms» sale del material: la medición se queda adentro, para el chat que
  optimiza. En su lugar se dice qué se siente, no cuánto marcó el cronómetro.
- «Se aprende en una tarde» se cambia por **flujo de uso familiar**: los
  comandos de AutoCAD que el dibujante ya trae, más el menú radial para lo
  frecuente.

## Decisiones de Mike (10-sep-2026)

- **La integración se vende como parte de la suite**: «el dato se captura una
  vez» y «el mismo mueble recorre los siete programas» se quedan. Se preguntó
  sabiendo que hoy draw101 y nest101 todavía no hablan con la base unificada
  (el puente real es el `.t101x`, por archivo). No es un descuido que corregir:
  es una decisión. Lo que sí se corrigió el mismo día: son **siete** programas;
  quell101 en Android va «en preparación» (el APK no se ha probado en un
  teléfono); draw101 ya no promete fluidez al editar (es su objetivo 1
  abierto); y «el despiezador» se llama nest101.

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
