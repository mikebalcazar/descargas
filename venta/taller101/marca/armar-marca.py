#!/usr/bin/env python3
# Saca el juego de archivos de marca de taller101 desde el maestro
# «Logo taller101 - NEW.svg» (repo bitacora-obra). Los trazos se copian; aquí
# no se redibuja nada. Puros <path>: sin <text> ni font-family, para que se vea
# igual en una máquina que no tenga Sansation instalada.
#
#     python3 armar-marca.py venta/taller101/marca
#
# Los archivos del logotipo llevan dentro el aire mínimo del manual —el alto
# entre 6— para que nadie los pegue a ras de una orilla.
#
# El ícono va en tres dibujos, no en uno, porque se midió que el aro normal se
# cierra en chico:
#   · normal  (512, 192, 180 px)  el aro tal cual
#   · chico   (32 px)             el aro 1,8 veces más grueso y más grande
#   · mínimo  (16 px)             sin aro: sólo el «101», que es lo único que
#                                 a ese tamaño todavía se lee
import io, pathlib, struct, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import cairosvg, marca
from PIL import Image

AZUL, BLANCO, TINTA = '#0080C1', '#FFFFFF', '#122733'
AIRE = marca.CAJA[3] / 6            # el aire mínimo del manual

CAB = ('<!-- taller101 · {q}\n'
       '     Sale de «Logo taller101 - NEW.svg» con armar-marca.py.\n'
       '     No se edita a mano. Puros <path>, sin <text> ni font-family. -->\n')


def _svg(cuerpo, vb, q):
    return (CAB.format(q=q) +
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" '
            f'role="img" aria-label="taller101">\n{cuerpo}\n</svg>\n')


def _dentro(s):
    return s[s.index('>') + 1:s.rindex('</svg>')]


def _ciento(esc=1.0):
    cx, cy = marca.CENTRO
    t = (f' transform="translate({cx},{cy}) scale({esc}) translate({-cx},{-cy})"'
         if esc != 1.0 else '')
    return (f'<g{t} fill="{BLANCO}"><path d="{marca.CERO}"/>'
            + ''.join(f'<rect x="{a}" y="{b}" width="{c}" height="{e}"/>'
                      for a, b, c, e in marca.UNOS) + '</g>')


def logotipo(tinta, q, placa=None):
    x, y, w, h = marca.CAJA
    vb = f'{x-AIRE:.2f} {y-AIRE:.2f} {w+2*AIRE:.2f} {h+2*AIRE:.2f}'
    fondo = (f'<rect x="{x-AIRE:.2f}" y="{y-AIRE:.2f}" width="{w+2*AIRE:.2f}" '
             f'height="{h+2*AIRE:.2f}" fill="{placa}"/>\n') if placa else ''
    return _svg(fondo + f'<g fill="{tinta}">{_dentro(marca.logo(tinta))}</g>', vb, q)


def icono(porcion=0.70, grueso=1.0, esc=1.0, aro=True, q='ícono'):
    cx, cy = marca.CENTRO
    lado = marca.R_EXT * 2 / porcion
    x, y = cx - lado/2, cy - lado/2
    g = marca.GROSOR * grueso
    anillo = (f'<circle cx="{cx}" cy="{cy}" r="{marca.R_EXT-g/2:.2f}" fill="none" '
              f'stroke="{BLANCO}" stroke-width="{g:.2f}"/>\n') if aro else ''
    return _svg(f'<rect x="{x:.2f}" y="{y:.2f}" width="{lado:.2f}" height="{lado:.2f}" '
                f'rx="{lado*0.22:.2f}" fill="{AZUL}"/>\n{anillo}{_ciento(esc)}',
                f'{x:.2f} {y:.2f} {lado:.2f} {lado:.2f}', q)


def og():
    """Tarjeta para redes y WhatsApp: 1200 × 630, logotipo blanco sobre azul."""
    w, h = 1200, 630
    lw = 680
    lh = lw / (marca.CAJA[2] / marca.CAJA[3])
    esc = lw / marca.CAJA[2]
    return _svg(
        f'<rect width="{w}" height="{h}" fill="{AZUL}"/>\n'
        f'<g transform="translate({(w-lw)/2:.2f},{(h-lh)/2:.2f}) scale({esc:.5f}) '
        f'translate({-marca.CAJA[0]},{-marca.CAJA[1]})" fill="{BLANCO}">'
        f'{_dentro(marca.logo(BLANCO))}</g>',
        f'0 0 {w} {h}', 'tarjeta para redes')


def rast(svg, destino, ancho):
    d = destino if hasattr(destino, 'write') else str(destino)
    cairosvg.svg2png(bytestring=svg.encode(), write_to=d, output_width=ancho)
    return destino


def imagen(svg, ancho):
    b = io.BytesIO(); rast(svg, b, ancho); b.seek(0)
    return Image.open(b).convert('RGBA')


if __name__ == '__main__':
    D = pathlib.Path(sys.argv[1]); D.mkdir(parents=True, exist_ok=True)

    SVG = {
      'taller101-azul.svg':        logotipo(AZUL,   'azul sobre fondo claro'),
      'taller101-blanco.svg':      logotipo(BLANCO, 'blanco sobre fondo oscuro o sobre el azul'),
      'taller101-negro.svg':       logotipo(TINTA,  'una sola tinta: impresión, sellos, grabado'),
      'taller101-placa.svg':       logotipo(BLANCO, 'blanco sobre placa azul', placa=AZUL),
      'taller101-icono.svg':       icono(),
      'taller101-icono-chico.svg': icono(0.80, 1.8, 1.00, True,  'ícono chico · 32 px'),
      'taller101-icono-minimo.svg':icono(0.70, 1.0, 1.55, False, 'ícono mínimo · 16 px'),
      'taller101-og-1200x630.svg': og(),
    }
    for n, s in SVG.items():
        (D / n).write_text(s)

    PNG = [('taller101-azul.png',        'taller101-azul.svg',        1024),
           ('taller101-blanco.png',      'taller101-blanco.svg',      1024),
           ('taller101-placa.png',       'taller101-placa.svg',       1024),
           ('taller101-og-1200x630.png', 'taller101-og-1200x630.svg', 1200),
           ('taller101-icono-512.png',   'taller101-icono.svg',        512),
           ('taller101-icono-192.png',   'taller101-icono.svg',        192),
           ('taller101-icono-180.png',   'taller101-icono.svg',        180),
           ('taller101-icono-32.png',    'taller101-icono-chico.svg',   32),
           ('taller101-icono-16.png',    'taller101-icono-minimo.svg',  16)]
    for n, fuente, px in PNG:
        rast(SVG[fuente], D / n, px)

    # El .ico lleva cada tamaño con SU dibujo, no uno reescalado. Pillow no
    # sabe hacer eso (su append_images para .ico se come los extras), así que
    # el archivo se arma a mano: cabecera, un renglón por tamaño y los PNG
    # pegados atrás. Un .ico con PNG adentro lo entiende cualquier navegador.
    trozos = [(16, SVG['taller101-icono-minimo.svg']),
              (32, SVG['taller101-icono-chico.svg']),
              (48, SVG['taller101-icono-chico.svg']),
              (64, SVG['taller101-icono-chico.svg'])]
    datos = []
    for px, s in trozos:
        b = io.BytesIO(); rast(s, b, px); datos.append((px, b.getvalue()))
    ico = struct.pack('<HHH', 0, 1, len(datos))
    desp = 6 + 16 * len(datos)
    for px, d in datos:
        ico += struct.pack('<BBBBHHII', px, px, 0, 0, 1, 32, len(d), desp)
        desp += len(d)
    (D / 'taller101.ico').write_bytes(ico + b''.join(d for _, d in datos))

    total = 0
    for n in list(SVG) + [n for n, _, _ in PNG] + ['taller101.ico']:
        b = (D / n).stat().st_size; total += b
        print(f'  {n:30s} {b:>8,} bytes')
    print(f'\n{len(SVG)+len(PNG)+1} archivos · {total:,} bytes · {D}')
