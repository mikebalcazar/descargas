# Rasteriza el logotipo y la placa de ícono a tamaños de pantalla de verdad.
# En el manual se enseñan ampliados: lo que se ve es el pixel real, no el
# vector reimpreso a 600 dpi, que mentiría sobre la legibilidad.
import base64, io, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import cairosvg, marca

AZUL = '#0080C1'

def _png(svg, alto):
    buf = io.BytesIO()
    cairosvg.svg2png(bytestring=svg.encode(), write_to=buf, output_height=alto,
                     background_color='white')
    return 'data:image/png;base64,' + base64.b64encode(buf.getvalue()).decode()

def logo_a(alto):
    return _png(f'<svg xmlns="http://www.w3.org/2000/svg" '
                f'{marca.logo(AZUL)[4:]}', alto)

def placa_a(alto):
    cx, cy = marca.CENTRO
    d = marca.R_EXT * 2
    lado = d / 0.70
    r = lado * 0.22
    x, y = cx - lado/2, cy - lado/2
    aro = marca.aro('#FFFFFF')
    aro = aro[aro.index('>')+1:aro.rindex('</svg>')]
    return _png(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x} {y} {lado} {lado}" '
        f'fill="#FFFFFF">'
        f'<rect x="{x}" y="{y}" width="{lado}" height="{lado}" rx="{r}" fill="{AZUL}"/>'
        f'{aro}</svg>', alto)
