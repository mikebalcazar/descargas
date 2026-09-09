#!/usr/bin/env python3
"""Arma el logotipo de una app de la suite como SVG de contornos de verdad.

Por que no se calca el PNG: un calco arrastra los bordes suaves del original y
los vuelve dientes, y ademas se despega de la fuente -- si manana Sansation
cambia de version, el calco se queda con la forma vieja y nadie se entera. Esto
saca los contornos directamente de sansation-700.woff2, que es LA fuente de la
marca, asi que el vector y el texto de la app no pueden discrepar.

Sale sin <text> y sin font-family, igual que el de draw101: puros <path>. Asi se
ve igual en cualquier maquina aunque no tenga Sansation instalada, que es justo
lo que le pasaria a un cliente.

Uso:
    python3 marca-svg.py nest101 /ruta/de/salida
"""
import sys, pathlib
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen

AZUL = '#0080C1'
BLANCO = '#FFFFFF'
FUENTE = '/home/claude/paquete-fuentes/sansation-700.woff2'
MARGEN = 40  # unidades de em alrededor del texto


def contornos(texto, ruta_fuente=FUENTE):
    """Devuelve (path_d, ancho, alto, desplazamiento_y) del texto ya trazado."""
    f = TTFont(ruta_fuente)
    glifos = f.getGlyphSet()
    cmap = f.getBestCmap()
    upm = f['head'].unitsPerEm
    hmtx = f['hmtx']

    faltan = [c for c in texto if ord(c) not in cmap]
    if faltan:
        raise SystemExit(f'el subconjunto de Sansation no trae: {faltan!r}')

    piezas, x = [], 0
    for c in texto:
        g = cmap[ord(c)]
        pluma = SVGPathPen(glifos)
        glifos[g].draw(pluma)
        d = pluma.getCommands()
        if d:
            piezas.append(f'<path transform="translate({x} 0)" d="{d}"/>')
        x += hmtx[g][0]

    ancho = x
    alto = f['head'].yMax - f['head'].yMin
    return piezas, ancho, alto, f['head'].yMax, upm


def svg(texto, color, fondo=None):
    piezas, ancho, alto, ymax, upm = contornos(texto)
    W = ancho + MARGEN * 2
    H = alto + MARGEN * 2
    # El eje Y de una fuente sube y el de SVG baja: se voltea con scale(1,-1) y
    # se recoloca el origen en la linea base.
    cuerpo = '\n  '.join(piezas)
    rect = f'<rect width="{W}" height="{H}" fill="{fondo}"/>\n  ' if fondo else ''
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
            f'width="{W}" height="{H}">\n  {rect}'
            f'<g fill="{color}" fill-rule="nonzero" '
            f'transform="translate({MARGEN} {MARGEN + ymax}) scale(1 -1)">\n  '
            f'{cuerpo}\n  </g>\n</svg>\n')


if __name__ == '__main__':
    nombre = sys.argv[1] if len(sys.argv) > 1 else 'nest101'
    salida = pathlib.Path(sys.argv[2] if len(sys.argv) > 2 else '.')
    salida.mkdir(parents=True, exist_ok=True)
    hechos = []
    for sufijo, color, fondo in (('azul', AZUL, None), ('blanco', BLANCO, None)):
        p = salida / f'{nombre}-{sufijo}.svg'
        p.write_text(svg(nombre, color, fondo))
        hechos.append((p.name, p.stat().st_size))
    for n, b in hechos:
        print(f'  {n}  {b} bytes')
