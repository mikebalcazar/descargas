# Los trazos del logotipo taller101, tal cual salen del archivo maestro
# «Logo taller101 - NEW.svg» (repo bitacora-obra). No se redibujan: se copian.
# Medidos con svgpathtools; las medidas van en el manual.

ARO_SUB = ('M431.49,208.74c-53.63,0-97.26,43.63-97.26,97.26,0,20.28,6.25,39.12,'
           '16.91,54.72h-223.14v6.52h228.01c17.85,21.95,45.05,36.01,75.48,36.01,'
           '53.63,0,97.26-43.63,97.26-97.26s-43.63-97.26-97.26-97.26ZM431.49,'
           '396.74c-29.48,0-55.72-14.14-72.3-35.99v-.02h-.01c-11.55-15.22-18.42'
           '-34.18-18.42-54.72,0-50.03,40.7-90.74,90.74-90.74s90.73,40.7,90.73,'
           '90.74-40.7,90.74-90.73,90.74Z')

PALABRA = [
 ('t','M140.62,351.34h11.28v-10.03h-5.16c-4.04,0-6.07-2.34-6.07-7.02v-23.08h11.23'
      'v-10.04h-12.61l-1.91-8.12h-9.37v44.77c0,9.02,4.2,13.52,12.61,13.52Z'),
 ('a','M176.63,320.76c-14.53,0-21.79,4.99-21.79,14.95s6.13,15.63,18.4,15.63c5.26,0,'
      '10.06-1.5,14.43-4.49l4.49,4.49h7.36v-33.64c0-11.02-7.45-16.53-22.36-16.53-5.48,0'
      '-11.56.8-18.25,2.39v10.03c6.69-1.59,12.77-2.39,18.25-2.39,6.47,0,9.7,2.25,9.7,'
      '6.74v3.78c-3.41-.64-6.82-.96-10.23-.96ZM186.86,338.34c-3.6,2.61-7.5,3.92-11.71,'
      '3.92-5.1,0-7.65-2.23-7.65-6.69,0-4.14,3.04-6.21,9.13-6.21,3.63,0,7.04.32,10.23.96v8.03Z'),
 ('e','M269.27,351.34c6.34,0,11.72-.48,16.15-1.43v-10.03c-5.06.96-10.13,1.43-15.19,1.43'
      '-10.39,0-15.58-3.54-15.58-10.61h33.31c.29-2.07.43-4.14.43-6.21,0-15.55-7.62-23.32'
      '-22.84-23.32s-23.56,8.17-23.56,24.51,9.09,25.66,27.29,25.66ZM265.54,311.11c7.01,0,'
      '10.51,3.47,10.51,10.42v.38h-21.41c.57-7.2,4.2-10.8,10.9-10.8Z'),
 ('r','M305.66,317.27c3.73-3.92,7.95-5.88,12.66-5.88v-10.23c-4.9,0-9.56,2.14-13.95,6.4'
      'l-1.58-6.4h-9.8v50.17h12.66v-34.07Z'),
]
PALABRA_RECT = [(204.94, 283.01, 12.66, 68.33), (224.66, 283.01, 12.66, 68.33)]

CERO = ('M431.81,262.73c-26.11,0-39.16,14.87-39.16,44.62s13.05,44.38,39.16,44.38,38.48'
        '-14.79,38.48-44.38-12.83-44.62-38.48-44.62ZM431.81,337.61c-14.85,0-22.28-10.21'
        '-22.28-30.63s7.43-30.14,22.28-30.14,21.61,10.05,21.61,30.14-7.2,30.63-21.61,30.63Z')
UNOS = [(366.40, 261.50, 16.27, 89.61), (479.98, 261.19, 16.27, 89.61)]

CAJA   = (128.00, 208.73, 400.75, 194.52)   # x, y, ancho, alto del logotipo
CENTRO = (431.49, 306.00)                   # centro del aro
R_EXT, R_INT, GROSOR = 97.26, 90.74, 6.52
BASE, SUB_Y = 351.34, 360.72


def _rect(r):
    return f'<rect x="{r[0]}" y="{r[1]}" width="{r[2]}" height="{r[3]}"/>'


def logo(fill='#0080C1', alto=None, clase='', extra=''):
    """El logotipo completo: palabra + subrayado + aro + 101."""
    x, y, w, h = CAJA
    piezas = [f'<path d="{ARO_SUB}"/>']
    piezas += [f'<path d="{d}"/>' for _, d in PALABRA]
    piezas += [_rect(r) for r in PALABRA_RECT]
    piezas += [f'<path d="{CERO}"/>'] + [_rect(r) for r in UNOS]
    est = f' style="height:{alto}"' if alto else ''
    return (f'<svg class="{clase}" viewBox="{x} {y} {w} {h}" fill="{fill}" '
            f'role="img" aria-label="taller101"{est}>{extra}{"".join(piezas)}</svg>')


def aro(fill='#0080C1', alto=None, clase=''):
    """Sólo el aro con el 101: la marca abreviada."""
    cx, cy = CENTRO
    d = R_EXT * 2
    piezas = [f'<circle cx="{cx}" cy="{cy}" r="{(R_EXT+R_INT)/2}" fill="none" '
              f'stroke="{fill}" stroke-width="{GROSOR}"/>',
              f'<path d="{CERO}"/>'] + [_rect(r) for r in UNOS]
    est = f' style="height:{alto}"' if alto else ''
    return (f'<svg class="{clase}" viewBox="{cx-R_EXT} {cy-R_EXT} {d} {d}" fill="{fill}" '
            f'role="img" aria-label="taller101"{est}>{"".join(piezas)}</svg>')
