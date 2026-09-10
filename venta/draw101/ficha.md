# draw101

**CAD 2D para taller de muebles y despachos de arquitectura.** Abre DWG/DXF, dibuja, acota, arma la hoja con pie de plano e imprime a PDF. Lo que un taller usa todos los días, con los comandos que el dibujante ya sabe.

## Para quién
- Talleres de carpintería y mobiliario que reciben planos DWG de arquitectos y deben producir sus propios planos de fabricación.
- Despachos chicos de arquitectura e interiorismo que dibujan en 2D y entregan PDF.
- Quien paga AutoCAD para usar el 10 % (o lo usa sin licencia).

## 5 beneficios
1. **Abre el DWG del cliente tal cual** — R2000 a R2018, capas, bloques, atributos y hojas de otros despachos; lo que no se entiende se conserva y vuelve a salir intacto al guardar.
2. **Flujo de uso familiar** — los comandos que el dibujante ya trae de AutoCAD (L, C, TR, DIM…), en inglés o español, y un menú radial con clic derecho para lo que se usa a cada rato: línea, círculo, cotas, mover, recortar. Espacio = Enter; barra por bloques de herramientas.
3. **Aguanta el plano de obra completo** — el plano del arquitecto entra entero; pan y zoom navegan sobre él sin redibujarlo.
4. **Del modelo al plano en minutos** — hojas A4–A0 con el pie de plano del despacho, escala por lista, cotas con tamaño propio por hoja, vista previa e impresión a PDF a tamaño real.
5. **Conectado al taller** — importa las cocinas de nest101 (.t101x), las acota solas y se actualizan cuando cambia el mueble; el DXF que sale va directo al que corta.

## 8 funciones
1. **Trazo completo** — línea, polilínea, arco, círculo, elipse, spline, rectángulo, polígono, texto de párrafo, rayado con galería de patrones (ANSI, ladrillo, concreto, madera…) y previa en vivo.
2. **Edición con el ratón** — mover, copiar, girar, escalar por 3 puntos, espejo, recortar, extender, empalme, chaflán, arreglos, grips en extremos y puntos medios.
3. **Referencias a objetos** — extremo, medio, centro, intersección, perpendicular, tangente, cercano, proyección con línea de rastreo; rejilla y ortho.
4. **Cotas asociativas** — lineal, alineada, angular, radio, diámetro, directriz; estilo del documento y tamaño por hoja; salen como DIMENSION en el DXF.
5. **Capas y bloques** — capas con color, grosor y tipo de línea; bloques con atributos; referencias externas; bloques pesados como sprites de lejos.
6. **Hojas de plano** — formatos A4–A0, pie de plano lateral editable con doble clic, ventanas con handles (tamaño, posición, encuadre en vivo), varias ventanas por hoja, escala por lista.
7. **Importar / exportar** — DWG (lectura y escritura), DXF R2013, PDF a tamaño real, PDF de fondo para calcar, SVG de la hoja, .t101x de Taller 101.
8. **Se mantiene solo** — actualizador integrado con aviso al arrancar, avisos del fabricante, deshacer/rehacer ilimitado, autoguardado y recuperación tras un cierre inesperado, tema claro y oscuro.

## Capturas

Tomadas del render local en el runner (`build/capturas_venta.py` en el código de draw101: arranca el motor, abre la interfaz en Chromium a **1600 × 1100 px** —y a **1600 × 900** para la portada—, tema claro, idioma español, datos ficticios «Cocina Ramírez / Familia Ramírez»). Ninguna sale de un plano de cliente. Para retomarlas a mano en Windows: ventana de draw101 maximizada en un monitor a 1600 px de ancho (o recorte a 1600), tema claro (Ayuda → Configuración), mismo dibujo.

| Archivo | Qué enseña |
|---|---|
| [01-modelo-cocina.png](capturas/01-modelo-cocina.png) | Modelo: alzado y planta de una cocina importada de Taller 101, acotada sola, nota a mano, capas a la derecha |
| [02-propiedades-en-vivo.png](capturas/02-propiedades-en-vivo.png) | Clic derecho sobre un mueble: propiedades flotantes editables en vivo |
| [03-galeria-rayado.png](capturas/03-galeria-rayado.png) | RAYADO: galería de patrones con previa sobre la cubierta |
| [04-hoja-pie-de-plano.png](capturas/04-hoja-pie-de-plano.png) | Hoja A2 con el pie de plano lateral de Taller 101, escala 1:20 |
| [05-ventana-handles.png](capturas/05-ventana-handles.png) | EDITARVENTANA: la ventana de la hoja con sus handles |
| [06-vista-previa.png](capturas/06-vista-previa.png) | Vista previa de impresión, centrada en el papel |
| [07-tema-oscuro.png](capturas/07-tema-oscuro.png) | El mismo modelo en tema oscuro |
| [08-menu-radial.png](capturas/08-menu-radial.png) | El menú radial abierto sobre el dibujo: clic derecho sostenido y los ocho gajos alrededor del cursor |
| [09-portada-16-9.png](capturas/09-portada-16-9.png) | **Portada 16:9** (1600 × 900) — la pantalla completa, sin recortes |

## Marca

`marca/draw101-azul.{png,svg}` (logo sobre claro), `marca/draw101-blanco.{png,svg}` (sobre oscuro), `marca/draw101-icono.{png,svg,ico}` (el disco «101»). Los SVG son trazado vectorial del PNG original (Sansation Bold); el PNG es el de la app.

## Cómo se pide

Se vende dentro de **Suite 101**. Sin precios en el material: la única llamada a la acción es **pedir una demostración a info@forespot.com**. Sitio: **suite101.pages.dev**.
