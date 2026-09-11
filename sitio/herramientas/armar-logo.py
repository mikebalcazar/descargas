#!/usr/bin/env python3
# Arma el logotipo de una app de la suite: el de taller101 con la palabra
# cambiada. No es un dibujo nuevo, es el mismo con otra palabra.
#
#     python3 sitio/herramientas/armar-logo.py quote nest dash peek
#
# La geometría no se estimó: se midió sobre roster101.svg y quell101.svg, que
# ya venían del original. Lo que se conserva:
#
#   · Sansation Bold, en trazos —no depende de que la fuente esté instalada—.
#   · Apretón entre letras de -0.05 em.
#   · Línea base en y=351.34 y escala 0.047783 (unidades de fuente directas).
#   · La palabra se alinea a la DERECHA por su avance, que termina en 319.51.
#     Así el aire hacia el aro es el mismo aunque la palabra sea más corta o
#     más larga. Medido: roster acaba en 319.51 y quell en 319.73.
#   · El subrayado va de la tinta izquierda de la palabra hasta el aro, y se
#     corta bajo los descendentes (q, p, g, j, y) con 8.01 de holgura a cada
#     lado. Medido en la q de quell101: 8.01 exactos de los dos lados.
#   · El aro y el «101» no se tocan nunca: van en coordenadas fijas.
#
# El de la suite (suite101) es el mismo dibujo con una diferencia, dicha por
# Mike el 10-sep: el aro es un círculo relleno y el «101» va calado,
# transparente. Se hace con un solo trazo y fill-rule evenodd: el disco con su
# subrayado, menos el «0» y los dos «1», más el hueco del «0», que vuelve a
# quedar relleno. Así el «101» deja ver lo que haya detrás.

import pathlib, sys
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.recordingPen import RecordingPen

S = pathlib.Path(__file__).resolve().parent.parent
FUENTE = S / 'fuentes' / 'sansation-700.woff2'
AZUL = '#0080C1'

ESC        = 0.047783    # unidades de fuente -> unidades del dibujo
BASE       = 351.34      # línea base
AVANCE_FIN = 319.51      # dónde termina el avance de la palabra
ARO_ARRIBA = 208.74      # borde superior del aro
ARO_ABAJO  = 403.25
ARO_DER    = 528.75      # borde derecho del aro
SUB_Y      = 360.72      # subrayado: borde superior
SUB_ALTO   = 6.52
SUB_CODO   = 351.14      # donde el subrayado se encuentra con el arco del aro
SUB_FIN    = 356.01      # extremo derecho del borde inferior del subrayado
HOLGURA    = 8.01        # aire a cada lado del descendente

_f = TTFont(FUENTE)
_gs = _f.getGlyphSet(); _cm = _f.getBestCmap(); _hm = _f['hmtx']
TRACK = -0.05 * _f['head'].unitsPerEm


def _glifo(ch):
    return _cm[ord(ch)]


def _colocar(palabra):
    """Devuelve el origen de cada letra, alineando el avance final."""
    ancho = 0
    for ch in palabra:
        ancho += _hm[_glifo(ch)][0] + TRACK
    ancho -= TRACK                                   # sin apretón tras la última
    origen = AVANCE_FIN / ESC - ancho
    puestos, x = [], origen
    for ch in palabra:
        puestos.append((ch, x))
        x += _hm[_glifo(ch)][0] + TRACK
    return puestos


def _trazo(puestos):
    sp = SVGPathPen(_gs)
    for ch, x in puestos:
        _gs[_glifo(ch)].draw(TransformPen(sp, (1, 0, 0, 1, x, 0)))
    return sp.getCommands()


def _tinta_izq(puestos):
    for ch, x in puestos:
        b = BoundsPen(_gs); _gs[_glifo(ch)].draw(b)
        if b.bounds:
            return (x + b.bounds[0]) * ESC
    raise ValueError('la palabra no tiene tinta')


def _contorno(glifo):
    """Puntos del contorno real, con las curvas aplanadas.

    Hace falta aplanar: los puntos de control de una curva caen fuera del
    trazo, y el desbordamiento de la o y la s los pone bajo la línea base sin
    que la letra baje de verdad. Midiendo sólo los puntos se detectaban
    descendentes que no existen.
    """
    rp = RecordingPen(); _gs[glifo].draw(rp)
    pts, actual = [], (0.0, 0.0)
    def bezier(p, n=24):
        for i in range(n + 1):
            t = i / n; u = 1 - t
            if len(p) == 3:                      # cuadrática
                yield (u*u*p[0][0] + 2*u*t*p[1][0] + t*t*p[2][0],
                       u*u*p[0][1] + 2*u*t*p[1][1] + t*t*p[2][1])
            else:                                # cúbica
                yield (u**3*p[0][0] + 3*u*u*t*p[1][0] + 3*u*t*t*p[2][0] + t**3*p[3][0],
                       u**3*p[0][1] + 3*u*u*t*p[1][1] + 3*u*t*t*p[2][1] + t**3*p[3][1])
    for op, args in rp.value:
        if op == 'moveTo':
            actual = args[0]; pts.append(actual)
        elif op == 'lineTo':
            actual = args[0]; pts.append(actual)
        elif op == 'qCurveTo':
            prev = actual
            puntos = list(args)
            implicito = puntos[-1] is None
            if implicito:                        # TrueType: el último se deduce
                puntos = puntos[:-1]
                for a, b in zip(puntos, puntos[1:]):
                    medio = ((a[0]+b[0])/2, (a[1]+b[1])/2)
                    pts += list(bezier([prev, a, medio])); prev = medio
                pts.append(prev)
            else:
                for a, b in zip(puntos, puntos[1:]):
                    medio = b if b is puntos[-1] else ((a[0]+b[0])/2, (a[1]+b[1])/2)
                    pts += list(bezier([prev, a, medio])); prev = medio
            actual = prev
        elif op == 'curveTo':
            pts += list(bezier([actual] + list(args))); actual = args[-1]
    return pts


def _descendentes(puestos):
    """Tramos en x (unidades del dibujo) que bajan de la línea base."""
    tramos = []
    for ch, x in puestos:
        pts = _contorno(_glifo(ch))
        bajos = [px for px, py in pts if py < -50]   # -50: por debajo del desbordamiento
        if bajos:
            tramos.append(((x + min(bajos)) * ESC - HOLGURA,
                           (x + max(bajos)) * ESC + HOLGURA))
    return tramos


def _disco(izq):
    """El borde de afuera del aro con su subrayado, que arranca en `izq`."""
    l1 = SUB_CODO - izq
    l2 = SUB_FIN - izq
    return (f'M431.49,{ARO_ARRIBA}c-53.63,0-97.26,43.63-97.26,97.26,0,20.28,'
            f'6.25,39.12,16.91,54.72h-{l1:.2f}v{SUB_ALTO}h{l2:.2f}'
            'c17.85,21.95,45.05,36.01,75.48,36.01,53.63,0,97.26-43.63,97.26-97.26'
            's-43.63-97.26-97.26-97.26Z')


def _aro(izq):
    """El aro con su subrayado: el disco menos el hueco de adentro."""
    return (_disco(izq) + 'M431.49,396.74c-29.48,0-55.72-14.14-72.3-35.99'
            'v-.02h-.01c-11.55-15.22-18.42-34.18-18.42-54.72,0-50.03,40.7-90.74,'
            '90.74-90.74s90.73,40.7,90.73,90.74-40.7,90.74-90.73,90.74Z')


# el «101»: nunca cambia
CIENTOUNO = (
 '<path d="M431.81,262.73c-26.11,0-39.16,14.87-39.16,44.62s13.05,44.38,39.16,'
 '44.38,38.48-14.79,38.48-44.38-12.83-44.62-38.48-44.62ZM431.81,337.61c-14.85,'
 '0-22.28-10.21-22.28-30.63s7.43-30.14,22.28-30.14,21.61,10.05,21.61,30.14'
 '-7.2,30.63-21.61,30.63Z"/>\n'
 '<rect x="366.4" y="261.5" width="16.27" height="89.61"/>\n'
 '<rect x="479.98" y="261.19" width="16.27" height="89.61"/>')


# El mismo «101» como trazos, para calarlo en el disco de la suite.
CIENTOUNO_TRAZO = ('M431.81,262.73c-26.11,0-39.16,14.87-39.16,44.62s13.05,44.38,39.16,'
                   '44.38,38.48-14.79,38.48-44.38-12.83-44.62-38.48-44.62ZM431.81,337.61c-14.85,'
                   '0-22.28-10.21-22.28-30.63s7.43-30.14,22.28-30.14,21.61,10.05,21.61,30.14'
                   '-7.2,30.63-21.61,30.63Z'
                   'M366.4,261.5h16.27v89.61h-16.27Z'
                   'M479.98,261.19h16.27v89.61h-16.27Z')

# Las palabras que llevan el aro relleno y el «101» calado.
SOLIDOS = {'suite'}


def armar(palabra):
    puestos = _colocar(palabra)
    izq = _tinta_izq(puestos)
    cortes = _descendentes(puestos)

    # El subrayado nace en la tinta izquierda. Donde hay descendente se parte:
    # el aro se queda con el tramo de la derecha y los demás van como rect.
    inicio_aro = izq
    trozos = []
    if cortes:
        bordes = [izq]
        for a, b in cortes:
            bordes += [a, b]
        bordes.append(SUB_CODO)
        pares = [(bordes[i], bordes[i + 1]) for i in range(0, len(bordes) - 1, 2)]
        pares = [(a, b) for a, b in pares if b - a > 0.5]   # sin astillas
        inicio_aro = pares[-1][0]
        trozos = pares[:-1]

    partes = [f'<g transform="translate(0,{BASE}) scale({ESC},-{ESC})">'
              f'<path d="{_trazo(puestos)}"/></g>']
    for a, b in trozos:
        partes.append(f'<rect x="{a:.2f}" y="{SUB_Y}" '
                      f'width="{b - a:.2f}" height="{SUB_ALTO}"/>')
    if palabra in SOLIDOS:
        partes.append(f'<path fill-rule="evenodd" d="{_disco(inicio_aro)}{CIENTOUNO_TRAZO}"/>')
    else:
        partes.append(f'<path d="{_aro(inicio_aro)}"/>')
        partes.append(CIENTOUNO)

    # El recorte va pegado al aro, sin aire. El aro es lo más alto del dibujo
    # —la palabra no le llega arriba ni con ascendentes, ni abajo con
    # descendentes—, así que al recortar así el aro mide exactamente el alto
    # del logotipo. Puesto en la página con una altura fija, el aro sale del
    # mismo tamaño en los siete: es la pieza que los une. El aire se pone en
    # el CSS, no aquí dentro.
    vx, vy = izq, ARO_ARRIBA
    vw, vh = ARO_DER - vx, ARO_ABAJO - vy
    cuerpo = '\n'.join(partes)
    return (f'<!-- {palabra}101: el logotipo de taller101 con la palabra cambiada.\n'
            f'     Lo arma sitio/herramientas/armar-logo.py; no se edita a mano.\n'
            f'     Sansation Bold en trazos, apretón -0.05 em, avance alineado a\n'
            f'     la derecha y aro y «101» en las coordenadas del original. -->\n'
            f'<svg xmlns="http://www.w3.org/2000/svg" '
            f'viewBox="{vx:.2f} {vy:.2f} {vw:.2f} {vh:.2f}" '
            f'role="img" aria-label="{palabra}101" fill="{AZUL}">\n{cuerpo}\n</svg>\n')


if __name__ == '__main__':
    for palabra in sys.argv[1:]:
        destino = S / 'marca' / f'{palabra}101.svg'
        destino.write_text(armar(palabra))
        print(f'{destino.relative_to(S.parent)}')
