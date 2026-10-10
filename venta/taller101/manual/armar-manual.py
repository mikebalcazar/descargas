#!/usr/bin/env python3
# Arma el manual de imagen de taller101: una hoja A4 por tema, HTML
# autocontenido (las cuatro fuentes van en base64) y PDF desde ese mismo HTML.
# Cero peticiones a internet: se ve igual en cualquier máquina.
import base64, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import marca, rasters

AQUI    = pathlib.Path(__file__).parent
FUENTES = AQUI.parents[2] / 'sitio' / 'fuentes'   # descargas/sitio/fuentes
FECHA   = '9 de octubre de 2026'

AZUL, AZUL_TXT, CLARO = '#0080C1', '#0074AD', '#3AA3DC'
TINTA, GRIS, NUBE, LINEA, EN_OSC = '#122733', '#5B6B76', '#F4F7F9', '#DFE6EA', '#A9C0CE'


# ----------------------------------------------------------------- contraste
def _lin(c):
    c /= 255
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

def luz(hexa):
    r, g, b = (int(hexa[i:i+2], 16) for i in (1, 3, 5))
    return 0.2126*_lin(r) + 0.7152*_lin(g) + 0.0722*_lin(b)

def contraste(a, b):
    la, lb = sorted((luz(a), luz(b)))
    return (lb + 0.05) / (la + 0.05)

def rgb(hexa):
    return ', '.join(str(int(hexa[i:i+2], 16)) for i in (1, 3, 5))

def cmyk(hexa):
    r, g, b = (int(hexa[i:i+2], 16)/255 for i in (1, 3, 5))
    k = 1 - max(r, g, b)
    if k >= 1: return '0 · 0 · 0 · 100'
    c, m, y = ((1-r-k)/(1-k), (1-g-k)/(1-k), (1-b-k)/(1-k))
    return ' · '.join(f'{v*100:.0f}' for v in (c, m, y, k))


# ------------------------------------------------------------------- fuentes
def b64(p):
    return base64.b64encode(pathlib.Path(p).read_bytes()).decode()

def caras():
    f = {n: b64(FUENTES / f'{n}.woff2') for n in
         ('fira-cifras-400', 'fira-cifras-600', 'raleway-400', 'raleway-600',
          'raleway-700', 'sansation-700')}
    rango = 'U+0030-0039,U+00B0,U+00B1,U+00D7,U+0025'
    css = []
    for peso, arch in (('400', 'fira-cifras-400'), ('600 700', 'fira-cifras-600')):
        css.append(f'@font-face{{font-family:"Cifras";src:url(data:font/woff2;base64,{f[arch]})'
                   f' format("woff2");font-weight:{peso};unicode-range:{rango}}}')
    for peso in ('400', '600', '700'):
        css.append(f'@font-face{{font-family:"Raleway";src:url(data:font/woff2;base64,'
                   f'{f["raleway-"+peso]}) format("woff2");font-weight:{peso}}}')
    css.append(f'@font-face{{font-family:"Sansation";src:url(data:font/woff2;base64,'
               f'{f["sansation-700"]}) format("woff2");font-weight:700}}')
    return '\n'.join(css)


# ------------------------------------------------------------------- piezas
def hoja(num, titulo, cuerpo, portada=False):
    if portada:
        return f'<section class="hoja portada">{cuerpo}</section>'
    return (f'<section class="hoja">'
            f'<header class="cabeza"><span>taller101 · manual de imagen</span>'
            f'<span class="fol">{num}</span></header>'
            f'<h2 class="titulo"><i>{num}</i>{titulo}</h2>{cuerpo}</section>')


def cota(x1, y1, x2, y2, texto, lado='arriba', sep=16):
    """Una cota con sus dos topes y su número, en unidades del dibujo."""
    if y1 == y2:                                           # horizontal
        ty, anc = y1 - 4, 'middle'
        t = (f'<line class="c" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"/>'
             f'<line class="c" x1="{x1}" y1="{y1-5}" x2="{x1}" y2="{y1+5}"/>'
             f'<line class="c" x1="{x2}" y1="{y2-5}" x2="{x2}" y2="{y2+5}"/>'
             f'<text class="n" x="{(x1+x2)/2}" y="{ty}" text-anchor="{anc}">{texto}</text>')
    else:                                                  # vertical
        t = (f'<line class="c" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"/>'
             f'<line class="c" x1="{x1-5}" y1="{y1}" x2="{x1+5}" y2="{y1}"/>'
             f'<line class="c" x1="{x2-5}" y1="{y2}" x2="{x2+5}" y2="{y2}"/>'
             f'<text class="n" x="{x1+7}" y="{(y1+y2)/2+5}">{texto}</text>')
    return t


def guia(x1, y1, x2, y2):
    return f'<line class="g" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"/>'


# ------------------------------------------------------------------ 0 portada
P0 = f'''
<div class="marcarron">{marca.logo(AZUL)}</div>
<h1>Manual de imagen</h1>
<p class="sub">Qué es la marca del taller, cómo se dibuja, de qué color va y con
qué letra se escriben las palabras y los números.</p>
<div class="datos">
  <div><span>Marca</span><b>taller101</b></div>
  <div><span>Alcance</span><b>Sólo taller101</b></div>
  <div><span>Fecha</span><b>{FECHA}</b></div>
</div>
<p class="pie">Este manual cubre <b>exclusivamente la imagen de taller101</b>, el
taller. No cubre suite101 ni los diez programas: ésos heredan de aquí el aro, el
azul y las letras, pero tienen su propia hoja.</p>
'''

# ------------------------------------------------------------------ 1 la marca
P1 = f'''
<p class="entrada">taller101 es el taller: quien fabrica el mueble, lo instala y
responde por él. Todo lo demás —los programas, el sitio, las fichas— nace de
esta marca y se le parece, pero la marca es ésta.</p>

<h3>El nombre</h3>
<table class="reglas">
<tr><td class="si">Así</td><td><b class="mono">taller101</b></td><td>Todo junto, todo en minúsculas, sin espacio.</td></tr>
<tr><td class="no">Así no</td><td class="mono tachado">Taller101 · TALLER101 · taller 101 · Taller&nbsp;101</td><td>Ni mayúscula inicial, ni versales, ni espacio.</td></tr>
</table>
<p class="nota">La única excepción viva es la firma de pie de página del sitio,
que dice «Taller 101» en texto corrido. Se corrige cuando se toque esa línea.</p>

<h3>Las tres piezas del logotipo</h3>
<div class="anatomia">
  <div class="dib">{marca.logo(AZUL)}</div>
  <ol class="piezas">
    <li><b>La palabra</b> — <span class="mono">taller</span> en Sansation Bold, trazada
        como contorno. Nunca como texto: así se ve igual en una máquina que no
        tenga la fuente instalada.</li>
    <li><b>El subrayado</b> — nace en el filo izquierdo de la palabra y muere en el
        aro. Es lo que amarra las dos mitades.</li>
    <li><b>El aro con el 101</b> — el único elemento que no cambia nunca. Es la
        pieza que hace familia con los diez programas.</li>
  </ol>
</div>
<p class="nota">De este dibujo salen los logotipos de los programas: se cambia la
palabra y <b>el aro y el 101 se quedan donde están</b>. Por eso el aro debe
medir siempre lo mismo cuando dos logotipos van juntos.</p>
'''

# ------------------------------------------------- 2 construcción del logotipo
x0, y0, W, H = marca.CAJA
cx, cy = marca.CENTRO
dib = f'''
<svg class="plano" viewBox="78 165 520 285">
  <g class="trama">
    {guia(x0, 175, x0, 436)}{guia(528.75, 175, 528.75, 436)}
    {guia(85, marca.BASE, 575, marca.BASE)}
    {guia(85, 208.73, 575, 208.73)}{guia(85, 403.25, 575, 403.25)}
    {guia(85, 283.01, 340, 283.01)}{guia(85, 301.17, 340, 301.17)}
    {guia(334.23, 175, 334.23, 436)}
    {guia(cx, 190, cx, 425)}
  </g>
  {marca.logo(AZUL).replace('<svg class="" viewBox="128.0 208.73 400.75 194.52" fill="#0080C1" role="img" aria-label="taller101">', '<g fill="#0080C1">').replace('</svg>', '</g>')}
  <g class="cotas">
    {cota(x0, 193, 528.75, 193, '400,75 de ancho · 2,06 veces el alto')}
    {cota(x0, 428, 318.32, 428, 'palabra  190,31')}
    {cota(345, 428, 528.75, 428, 'aro  194,52')}
    {cota(556, 208.73, 556, 403.25, '194,52')}
    <text class="n" x="88" y="{marca.BASE - 6}">base</text>
    <text class="n" x="88" y="{marca.SUB_Y + 26}">subrayado · 6,52 de grueso</text>
    <text class="n" x="{cx + 8}" y="{403.25 + 46}">centro del aro</text>
    <text class="n" x="88" y="{283.01 - 5}">«l»</text>
    <text class="n" x="88" y="{301.17 + 13}">«a»</text>
  </g>
</svg>'''

P2 = f'''
<p class="entrada">El logotipo no se redibuja ni se recompone: se usa el archivo.
Estas medidas sirven para <b>comprobar</b> que lo que llegó es el bueno, y para
colocarlo en una página. Van en unidades del dibujo; lo que importa son las
proporciones, no el número.</p>
{dib}
<h3>Lo que hay que saber de memoria</h3>
<table class="medidas">
<tr><th>Medida</th><th>Valor</th><th>En proporción</th></tr>
<tr><td>Alto del logotipo = diámetro del aro</td><td class="v">194,52</td><td>el aro manda: es la pieza más alta</td></tr>
<tr><td>Ancho total</td><td class="v">400,75</td><td>2,06 veces el alto</td></tr>
<tr><td>Grueso del aro</td><td class="v">6,52</td><td>el alto ÷ 29,8  (casi ÷ 30)</td></tr>
<tr><td>Grueso del subrayado</td><td class="v">6,52</td><td><b>el mismo que el aro</b></td></tr>
<tr><td>Alto del «101»</td><td class="v">89,61</td><td>0,46 del alto</td></tr>
<tr><td>Asta del «1»</td><td class="v">16,27</td><td>2,5 veces el grueso del aro</td></tr>
<tr><td>Alto de la «l»</td><td class="v">68,33</td><td>0,35 del alto</td></tr>
<tr><td>Alto de la «a»</td><td class="v">50,17</td><td>0,26 del alto</td></tr>
<tr><td>Aire entre la palabra y el aro</td><td class="v">15,91</td><td>2,4 veces el grueso del aro</td></tr>
</table>
<p class="nota"><b>La que más cuesta si se pierde:</b> el subrayado y el aro tienen
el mismo grueso. Si alguien reescala el logotipo sólo a lo ancho, dejan de
coincidir y se nota a primera vista.</p>
'''

# ---------------------------------------------------- 3 aire y tamaño mínimo
P3 = f'''
<p class="entrada">Dos reglas, las dos medidas sobre el dibujo de verdad.</p>

<h3>Aire alrededor</h3>
<div class="aire">
  <div class="caja-aire"><div class="dentro">{marca.logo(AZUL)}</div></div>
  <div class="texto">
    <p>El aire mínimo a los cuatro lados es <b>un sexto del alto del logotipo</b>.
    Ahí no entra nada: ni texto, ni una orilla, ni otro logotipo.</p>
    <p class="formula">aire = alto ÷ 6</p>
    <p>En la barra del sitio se le da <b>un tercio</b> arriba y abajo. Ése es el
    aire cómodo; un sexto es el piso.</p>
    <p class="chiquita">La línea punteada marca el límite del aire; la línea fina,
    la caja del logotipo.</p>
  </div>
</div>

<h3>Tamaño mínimo</h3>
<p>Se midió rasterizando a los píxeles de verdad, no reimprimiendo el vector:
por debajo de cierto tamaño la palabra se cierra y el subrayado desaparece.</p>
<div class="escalera">
  <div><img src="{rasters.logo_a(24)}" style="height:{24*4}px"><span>24 px</span></div>
  <div><img src="{rasters.logo_a(18)}" style="height:{18*4}px"><span>18 px · mínimo</span></div>
  <div class="mal"><img src="{rasters.logo_a(14)}" style="height:{14*4}px"><span>14 px · ya no</span></div>
  <div class="mal"><img src="{rasters.logo_a(12)}" style="height:{12*4}px"><span>12 px · no</span></div>
</div>
<p class="chiquita">Ampliados cuatro veces. Cada cuadro es un píxel de pantalla.</p>
<table class="medidas">
<tr><th>Dónde</th><th>Mínimo</th><th>Por qué ahí</th></tr>
<tr><td>Pantalla</td><td class="v">18 px de alto</td><td>a 16 px la «a» se empieza a cerrar; a 14 px el subrayado se pierde</td></tr>
<tr><td>Impresión</td><td class="v">8 mm de alto</td><td>a esa altura el aro y el subrayado miden 0,27 mm, que es lo que aguanta el papel</td></tr>
</table>
<p class="nota">Si no cabe en 18 px o en 8 mm, <b>no se encoge el logotipo: se usa
el aro solo</b> (hoja 5).</p>
'''

# ------------------------------------------------------------ 4 versiones
P4 = f'''
<p class="entrada">Cuatro versiones y ninguna más. Se elige por el fondo, no por
el gusto.</p>
<div class="versiones">
  <figure class="v-blanco"><div>{marca.logo(AZUL)}</div>
    <figcaption><b>Azul sobre blanco</b><span>La principal. Papel, pantalla clara, documentos.</span></figcaption></figure>
  <figure class="v-azul"><div>{marca.logo('#FFFFFF')}</div>
    <figcaption><b>Blanco sobre el azul</b><span>Placas, portadas, lonas. Es la del archivo maestro.</span></figcaption></figure>
  <figure class="v-tinta"><div>{marca.logo(CLARO)}</div>
    <figcaption><b>Claro sobre fondo oscuro</b><span>Sobre la tinta, el azul de marca se apaga; el claro aguanta.</span></figcaption></figure>
  <figure class="v-blanco"><div>{marca.logo(TINTA)}</div>
    <figcaption><b>Una sola tinta</b><span>Sellos, fax, grabado, fotocopia. En negro o en tinta.</span></figcaption></figure>
</div>
<h3>Sobre qué fondo sí</h3>
<div class="fondos">
  <div class="f ok" style="background:#fff">{marca.logo(AZUL)}<span>blanco</span></div>
  <div class="f ok" style="background:{NUBE}">{marca.logo(AZUL)}<span>nube</span></div>
  <div class="f ok" style="background:{AZUL}">{marca.logo('#FFFFFF')}<span>azul</span></div>
  <div class="f ok" style="background:{TINTA}">{marca.logo(CLARO)}<span>tinta</span></div>
  <div class="f no" style="background:{CLARO}">{marca.logo('#FFFFFF')}<span>claro — se funde</span></div>
  <div class="f no foto">{marca.logo('#FFFFFF')}<span>foto suelta</span></div>
</div>
<p class="nota">Sobre una foto, el logotipo va en blanco y sólo si debajo hay una
zona lisa y oscura. Si la foto tiene detalle, se pone una placa azul y el
logotipo en blanco encima.</p>
'''

# ---------------------------------------------------------------- 5 el aro
P5 = f'''
<p class="entrada">Cuando el logotipo completo no cabe o no se leería, se usa
<b>el aro con el 101</b>. Es la marca abreviada: la misma familia, sin la palabra.</p>
<div class="aro-fila">
  <figure><div class="cuadro blanco">{marca.aro(AZUL)}</div><figcaption>azul sobre blanco</figcaption></figure>
  <figure><div class="cuadro azul">{marca.aro('#FFFFFF')}</div><figcaption>blanco sobre azul</figcaption></figure>
  <figure><div class="cuadro placa">{marca.aro('#FFFFFF')}</div><figcaption>placa de ícono</figcaption></figure>
</div>
<h3>Cuándo se usa</h3>
<ul class="lista">
  <li>Ícono de la aplicación, favicon, foto de perfil.</li>
  <li>Sello en una esquina, marca de agua, grabado pequeño.</li>
  <li>Cualquier hueco cuadrado, o más angosto que dos veces su alto.</li>
</ul>
<h3>Cómo se dibuja</h3>
<p>Es el aro del logotipo <b>sin el subrayado</b>, con el 101 en su sitio. El
círculo va de <span class="mono">6,52</span> de grueso sobre un diámetro exterior
de <span class="mono">194,52</span>: el mismo aro, no uno nuevo.</p>
<p class="nota">La placa del ícono es un cuadrado con las esquinas redondeadas a
<span class="mono">0,22</span> del lado, el aro centrado ocupando
<span class="mono">0,70</span> del lado.</p>
<div class="prueba32">
  <div><img src="{rasters.placa_a(32)}" style="height:128px"><span>32 px</span></div>
  <div><img src="{rasters.placa_a(24)}" style="height:96px"><span>24 px</span></div>
  <div class="mal"><img src="{rasters.placa_a(16)}" style="height:64px"><span>16 px · no</span></div>
  <p class="chiquita"><b>Ampliados cuatro veces.</b> A 32 px el aro y los tres
  trazos del 101 se separan, aunque el trazo ya va delgado. A 24 px apenas.
  A 16 px se cierran: para un favicon de ese tamaño hace falta un dibujo aparte,
  con el aro más grueso. <b>Está pendiente.</b></p>
</div>
'''

# ----------------------------------------------------------------- 6 color
def muestra(nombre, hexa, uso, sobre='#FFFFFF', etiqueta='sobre blanco'):
    c = contraste(hexa, sobre)
    return f'''<div class="color">
  <div class="tono" style="background:{hexa}"></div>
  <div class="dat"><b>{nombre}</b>
    <span class="mono">{hexa.upper()}</span>
    <span>RGB {rgb(hexa)}</span>
    <span>CMYK {cmyk(hexa)}</span>
    <span class="uso">{uso}</span>
    <span class="con">contraste {c:.2f} : 1 {etiqueta}</span>
  </div></div>'''

P6 = f'''
<p class="entrada">Un azul y una tinta. Lo demás son grises de apoyo, y están
aquí para que nadie invente uno.</p>
<h3>Los dos que son la marca</h3>
<div class="colores dos">
  {muestra('Azul taller101', AZUL, 'El logotipo, los trazos, los planos. Es <b>el</b> color.')}
  {muestra('Tinta', TINTA, 'Todo el texto, y el fondo de las secciones oscuras.')}
</div>
<h3>Los de apoyo</h3>
<div class="colores">
  {muestra('Azul de texto', AZUL_TXT, 'El azul para letra y enlaces sobre blanco.')}
  {muestra('Claro', CLARO, 'El logotipo sobre fondo oscuro.', TINTA, 'sobre tinta')}
  {muestra('Gris', GRIS, 'Texto secundario, pies de foto.')}
  {muestra('Nube', NUBE, 'Fondo suave para separar bloques.', TINTA, 'con tinta encima')}
  {muestra('Línea', LINEA, 'Reglas, bordes de tabla.', '#FFFFFF', 'sobre blanco')}
  {muestra('En oscuro', EN_OSC, 'Texto secundario sobre la tinta.', TINTA, 'sobre tinta')}
</div>
<p class="nota"><b>Por qué hay dos azules.</b> El azul de marca da
{contraste(AZUL, '#FFFFFF'):.2f} de contraste sobre blanco y la norma pide 4,5 para
texto normal. Para letra se usa el de texto, que da {contraste(AZUL_TXT, '#FFFFFF'):.2f}.
Para el logotipo y los trazos manda siempre el de marca.</p>
<p class="nota">El CMYK es una conversión directa, para arrancar. En una
impresión que importe se ajusta contra prueba de color: el que manda es el
hexadecimal.</p>
<p class="nota aviso">El archivo maestro de Illustrator trae el azul como
<span class="mono">#0381C2</span>, un pelo distinto del
<span class="mono">#0080C1</span> que usan el sitio, las apps y las fichas. La
diferencia no se ve, pero conviene dejar uno solo: <b>este manual declara
#0080C1</b> y el maestro se corrige cuando se vuelva a abrir.</p>
'''

# ------------------------------------------------------- 7 tipografía: texto
P7 = f'''
<p class="entrada">Dos letras para el texto, y cada una tiene su trabajo. Nunca
se bajan de Google Fonts: viven en el proyecto como archivo
<span class="mono">.woff2</span>, así nada se ve distinto sin señal.</p>

<h3>Sansation Bold — la marca y los rótulos</h3>
<div class="espec sansation">
  <p class="muestra">taller101</p>
  <p class="abc">ABCDEFGHIJKLMNÑOPQRSTUVWXYZ<br>abcdefghijklmnñopqrstuvwxyz</p>
</div>
<table class="medidas">
<tr><th>Dónde</th><th>Ajuste</th></tr>
<tr><td>El logotipo</td><td>contorno trazado, apretón <span class="v">−0,05 em</span> — nunca texto vivo</td></tr>
<tr><td>Rótulos de sección</td><td>versales, separación <span class="v">0,14 em</span>, tamaño chico</td></tr>
</table>
<p class="nota">Sansation <b>no</b> se usa para párrafos. Sólo marca y rótulos cortos.</p>

<h3>Raleway — todo el texto</h3>
<div class="espec raleway">
  <p class="muestra">Hecho en el taller, probado en obra</p>
  <p class="abc">ABCDEFGHIJKLMNÑOPQRSTUVWXYZ abcdefghijklmnñopqrstuvwxyz</p>
  <p class="pesos"><span style="font-weight:400">400 Regular</span> ·
     <span style="font-weight:600">600 SemiBold</span> ·
     <span style="font-weight:700">700 Bold</span></p>
</div>
<h3>La escala en uso</h3>
<table class="medidas escala">
<tr><th>Para qué</th><th>Tamaño</th><th>Interlínea</th><th>Peso</th><th>Separación</th></tr>
<tr><td>Título de portada</td><td class="v">40 – 76 px</td><td class="v">1,04</td><td class="v">700</td><td class="v">−0,022 em</td></tr>
<tr><td>Título de sección</td><td class="v">30 – 48 px</td><td class="v">1,08</td><td class="v">700</td><td class="v">−0,018 em</td></tr>
<tr><td>Lema</td><td class="v">28 – 44 px</td><td class="v">1,10</td><td class="v">700</td><td class="v">−0,015 em</td></tr>
<tr><td>Entrada</td><td class="v">21 – 27 px</td><td class="v">1,42</td><td class="v">600</td><td class="v">0</td></tr>
<tr><td>Texto corrido</td><td class="v">17 px</td><td class="v">1,50</td><td class="v">400</td><td class="v">0</td></tr>
<tr><td>Secundario</td><td class="v">14 – 15 px</td><td class="v">1,45</td><td class="v">400</td><td class="v">0</td></tr>
<tr><td>Botón</td><td class="v">14 px</td><td class="v">1</td><td class="v">700</td><td class="v">0,14 em · versales</td></tr>
</table>
<p class="nota">Los títulos van con el apretón en negativo porque a tamaño grande
la letra se abre sola. El texto corrido nunca se aprieta.</p>
'''

# ------------------------------------------------------ 8 tipografía: cifras
P8 = f'''
<p class="entrada">Ésta es la regla que más barato sale y más caro cuesta
olvidar: <b>los números no se escriben con la letra del texto</b>. Van en Fira
Sans, y se cambian solos.</p>

<h3>El problema, medido</h3>
<table class="medidas">
<tr><th></th><th>Raleway</th><th>Fira Sans</th></tr>
<tr><td>Alto de las cifras</td><td class="v mal">0,571 – 0,715 em</td><td class="v bien">0,669 – 0,679 em</td></tr>
<tr><td>Cifras que bajan de la línea</td><td class="v mal">hasta −0,154 em</td><td class="v bien">−0,022 em</td></tr>
<tr><td>Ancho tabular</td><td class="v mal">no lo trae</td><td class="v bien">0,560 em, todas iguales</td></tr>
</table>
<div class="comparacion">
  <div><span class="rot">Raleway</span><p class="num ral">1 234 567<br>890,05</p>
       <small>las cifras bailan: unas altas, otras bajas, una colgando</small></div>
  <div><span class="rot">Fira Sans</span><p class="num fir">1 234 567<br>890,05</p>
       <small>una sola altura, todas apoyadas, todas del mismo ancho</small></div>
</div>
<p class="nota">En una lista de corte o en una cotización las columnas tienen que
cuadrar a la vista. <b>Un número mal leído es una pieza mal cortada.</b></p>

<h3>Cómo se aplica — se copia tal cual</h3>
<pre class="codigo">@font-face{{font-family:"Cifras";
  src:url(fira-cifras-400.woff2) format("woff2");
  font-weight:400;
  unicode-range:U+0030-0039,U+00B0,U+00B1,U+00D7,U+0025}}

body{{font-family:"Cifras","Raleway",system-ui,sans-serif;
  font-variant-numeric:tabular-nums;
  font-feature-settings:"tnum"}}</pre>
<p>«Cifras» va <b>primero</b> en la lista y sólo cubre
<span class="mono">0–9 ° ± × %</span>. El navegador toma de ahí esos signos y
todo lo demás de Raleway. <b>No hay que marcar nada en el HTML:</b> los números
caen solos donde estén.</p>
<table class="medidas">
<tr><th>Signo</th><th>Código</th><th>Por qué entra</th></tr>
<tr><td class="v">0 – 9</td><td class="mono">U+0030-0039</td><td>las cifras</td></tr>
<tr><td class="v">°</td><td class="mono">U+00B0</td><td>grados de un corte o un ángulo</td></tr>
<tr><td class="v">±</td><td class="mono">U+00B1</td><td>tolerancias</td></tr>
<tr><td class="v">×</td><td class="mono">U+00D7</td><td>medidas: 600 × 350</td></tr>
<tr><td class="v">%</td><td class="mono">U+0025</td><td>desperdicio, avance, utilidad</td></tr>
</table>
<p class="nota"><b>Dónde manda esta regla:</b> medidas, cantidades, precios,
fechas, versiones, folios, teléfonos. En pantalla y en papel. En las columnas de
números, alineadas a la derecha.</p>
'''

# ------------------------------------------------------------ 9 usos malos
def mal(estilo, titulo, por):
    return (f'<figure class="malo"><div class="m"><div class="t" style="{estilo}">'
            f'{marca.logo(AZUL)}</div></div>'
            f'<figcaption><b>{titulo}</b><span>{por}</span></figcaption></figure>')

P9 = f'''
<p class="entrada">Todo lo de esta hoja está prohibido. No son opiniones: cada
una rompe algo que el logotipo necesita para leerse.</p>
<div class="malos">
  {mal('transform:scaleX(1.22)', 'Estirado', 'el subrayado y el aro dejan de medir lo mismo')}
  {mal('transform:scaleY(1.45)', 'Aplastado', 'igual, al revés')}
  {mal('transform:rotate(-9deg) scale(.92)', 'Girado', 'el subrayado deja de ser una línea de piso')}
  {mal('filter:hue-rotate(115deg) saturate(1.5)', 'Otro color', 'el azul es la marca; no se cambia por gusto')}
  {mal('filter:drop-shadow(3px 4px 2px rgba(0,0,0,.5))', 'Con sombra', 'el logotipo es plano, siempre')}
  {mal('opacity:.32', 'Desvanecido', 'si estorba, se quita; no se apaga')}
</div>
<h3>Y tampoco</h3>
<ul class="lista nono">
  <li>Rehacer la palabra escribiéndola con la fuente. <b>Se usa el archivo.</b></li>
  <li>Cambiar el 101 de sitio, de tamaño o de forma.</li>
  <li>Separar la palabra del aro, o quitar el subrayado del logotipo completo.</li>
  <li>Meter el logotipo en una caja, un círculo o una pastilla que no sea la placa de ícono.</li>
  <li>Ponerle un contorno, un degradado o una textura.</li>
  <li>Escribir «taller101» con la letra del texto y hacerlo pasar por el logotipo.</li>
  <li>Dejar que algo entre en el aire mínimo.</li>
</ul>
'''

# ------------------------------------------------------------ 10 archivos
P10 = f'''
<p class="entrada">Dónde está cada cosa y de dónde sale. Nada de esto se dibuja a
mano otra vez.</p>
<h3>El maestro</h3>
<table class="medidas archivos">
<tr><th>Archivo</th><th>Qué es</th></tr>
<tr><td class="mono">Logo taller101 - NEW.svg</td><td>el original de Illustrator: el logotipo en blanco sobre placa azul. Repositorio <span class="mono">bitacora-obra</span>, en la raíz. <b>Es la autoridad.</b></td></tr>
<tr><td class="mono">sitio/fuentes/*.woff2</td><td>las cuatro letras: Sansation Bold, Raleway 400/600/700, Fira Sans 400/600 recortada a las cifras</td></tr>
<tr><td class="mono">sitio/herramientas/armar-logo.py</td><td>arma el logotipo de cada programa cambiando la palabra, con el aro y el 101 fijos</td></tr>
</table>
<h3>Las reglas que no se negocian</h3>
<ul class="lista">
  <li><b>El logotipo se usa, no se redibuja.</b> Si hace falta en otro formato, se exporta del maestro.</li>
  <li><b>Nada de calcar un PNG.</b> Arrastra los bordes suaves y se despega de la fuente.</li>
  <li><b>El vector va en trazos:</b> puro <span class="mono">&lt;path&gt;</span>, sin <span class="mono">&lt;text&gt;</span> ni <span class="mono">font-family</span>. Así se ve igual en la máquina de un cliente que no tenga Sansation.</li>
  <li><b>Fuentes propias, cero Google Fonts.</b> Van dentro del archivo o junto a él.</li>
  <li><b>Lo que no se midió, se dice.</b> Nunca se supone.</li>
</ul>
<h3>Lo que falta</h3>
<table class="medidas archivos">
<tr><td class="pend">Pendiente</td><td>Sacar del maestro el juego de taller101: azul, blanco, una tinta, placa de ícono y las medidas de redes, como ya lo tienen los programas.</td></tr>
<tr><td class="pend">Pendiente</td><td>Unificar el azul del maestro en <span class="mono">#0080C1</span>.</td></tr>
<tr><td class="pend">Pendiente</td><td>Corregir la firma del pie del sitio: dice «Taller 101», debe decir «taller101».</td></tr>
<tr><td class="pend">Pendiente</td><td>Dibujar el ícono chico (16 y 32 px) con el aro más grueso: el aro normal se cierra a ese tamaño.</td></tr>
</table>
<p class="firma-final">{marca.logo(AZUL, alto='42px')}</p>
'''

PAGINAS = [
    (None, None, P0, True),
    ('1', 'La marca', P1, False),
    ('2', 'El logotipo', P2, False),
    ('3', 'Aire y tamaño mínimo', P3, False),
    ('4', 'Versiones y fondos', P4, False),
    ('5', 'El aro', P5, False),
    ('6', 'Color', P6, False),
    ('7', 'Tipografía · el texto', P7, False),
    ('8', 'Tipografía · las cifras', P8, False),
    ('9', 'Usos incorrectos', P9, False),
    ('10', 'Archivos y reglas', P10, False),
]

CSS = f'''
{caras()}
*{{box-sizing:border-box;margin:0;padding:0}}
:root{{--azul:{AZUL};--azultxt:{AZUL_TXT};--claro:{CLARO};--tinta:{TINTA};
  --gris:{GRIS};--nube:{NUBE};--linea:{LINEA};--enosc:{EN_OSC}}}
@page{{size:A4;margin:0}}
body{{font-family:"Cifras","Raleway",sans-serif;font-variant-numeric:tabular-nums;
  font-feature-settings:"tnum";color:var(--tinta);font-size:9.6pt;line-height:1.5;
  -webkit-font-smoothing:antialiased;background:#fff}}
.hoja{{width:210mm;height:297mm;padding:17mm 17mm 14mm;position:relative;
  page-break-after:always;overflow:hidden;background:#fff}}
.hoja:last-child{{page-break-after:auto}}
svg{{display:block;height:auto;max-width:100%}}

/* ------------------------------------------------------------- portada */
.portada{{display:flex;flex-direction:column;padding-top:38mm;
  border-top:7mm solid var(--azul)}}
.marcarron svg{{width:96mm}}
.portada h1{{font-size:34pt;font-weight:700;letter-spacing:-.022em;line-height:1.04;
  margin:14mm 0 0}}
.portada .sub{{font-size:13pt;font-weight:600;line-height:1.38;color:var(--gris);
  max-width:120mm;margin-top:6mm}}
.datos{{display:flex;gap:14mm;margin-top:16mm;padding-top:5mm;border-top:1px solid var(--linea)}}
.datos span{{display:block;font-size:7.6pt;color:var(--gris);letter-spacing:.06em;
  text-transform:uppercase}}
.datos b{{font-size:11pt;font-weight:600}}
.portada .pie{{margin-top:auto;font-size:9pt;color:var(--gris);max-width:140mm;
  border-left:2px solid var(--azul);padding-left:5mm}}

/* ------------------------------------------------------------- cabeza */
.cabeza{{display:flex;justify-content:space-between;align-items:baseline;
  font-size:7.4pt;letter-spacing:.1em;text-transform:uppercase;color:var(--gris);
  border-bottom:1px solid var(--linea);padding-bottom:2.5mm}}
.fol{{font-weight:700;color:var(--azul)}}
.titulo{{font-size:20pt;font-weight:700;letter-spacing:-.018em;line-height:1.1;
  margin:7mm 0 5mm;display:flex;align-items:baseline;gap:4mm}}
.titulo i{{font-style:normal;font-size:20pt;font-weight:700;color:var(--azul)}}
h3{{font-family:"Cifras","Sansation",sans-serif;font-size:8pt;font-weight:700;
  letter-spacing:.14em;text-transform:uppercase;color:var(--azul);
  margin:7mm 0 3mm;padding-bottom:1.5mm;border-bottom:1px solid var(--linea)}}
.entrada{{font-size:11pt;font-weight:600;line-height:1.42}}
p{{margin-bottom:2.5mm}}
.nota{{font-size:8.4pt;color:var(--gris);line-height:1.45;margin-top:3mm;
  border-left:2px solid var(--linea);padding-left:3.5mm}}
.chiquita{{font-size:7.6pt;color:var(--gris);line-height:1.35;margin-top:2mm}}
.nota.aviso{{border-left-color:var(--azul);color:var(--tinta);background:var(--nube);
  padding:3mm 3.5mm}}
.mono{{font-family:"Cifras",ui-monospace,"Courier New",monospace;font-weight:600;
  letter-spacing:.01em}}
.tachado{{text-decoration:line-through;color:var(--gris)}}

/* ------------------------------------------------------------- tablas */
table{{width:100%;border-collapse:collapse;margin-top:2mm}}
th{{text-align:left;font-size:7.4pt;letter-spacing:.09em;text-transform:uppercase;
  color:var(--gris);font-weight:700;padding:0 3mm 1.5mm 0;border-bottom:1px solid var(--linea)}}
td{{padding:2mm 3mm 2mm 0;border-bottom:1px solid var(--linea);font-size:9pt;
  vertical-align:top;line-height:1.35}}
td.v{{font-weight:600;white-space:nowrap}}
td.mal{{color:#B3341F}} td.bien{{color:var(--azultxt)}}
.reglas td:first-child{{width:19mm;font-size:7.4pt;letter-spacing:.08em;
  text-transform:uppercase;font-weight:700}}
.reglas .si{{color:var(--azul)}} .reglas .no{{color:#B3341F}}
.reglas td:nth-child(2){{width:62mm}}
.escala td,.escala th{{font-size:8.4pt}}
.archivos td:first-child{{width:56mm}}
td.pend{{width:24mm;font-size:7.4pt;letter-spacing:.08em;text-transform:uppercase;
  font-weight:700;color:var(--azul)}}

/* ------------------------------------------------------------- hoja 1 */
.anatomia{{display:flex;gap:8mm;align-items:flex-start;margin-top:3mm}}
.anatomia .dib{{flex:0 0 72mm;background:var(--nube);padding:7mm 6mm}}
.piezas{{list-style:none;counter-reset:p}}
.piezas li{{counter-increment:p;position:relative;padding-left:8mm;margin-bottom:3.5mm;
  font-size:9pt;line-height:1.42}}
.piezas li::before{{content:counter(p);position:absolute;left:0;top:0;width:5mm;height:5mm;
  background:var(--azul);color:#fff;font-size:7.5pt;font-weight:700;text-align:center;
  line-height:5mm}}

/* ------------------------------------------------------------- hoja 2 */
.plano{{width:100%;margin:2mm 0 1mm}}
.plano .g{{stroke:{CLARO};stroke-width:.7;stroke-dasharray:5 4;opacity:.75}}
.plano .c{{stroke:{TINTA};stroke-width:1.1}}
.plano .n{{font-family:"Cifras","Raleway",sans-serif;font-size:11px;font-weight:600;
  fill:{TINTA}}}

/* ------------------------------------------------------------- hoja 3 */
.aire{{display:flex;gap:7mm;align-items:center;margin-top:2mm}}
.caja-aire{{flex:0 0 86mm;border:1px dashed var(--claro);padding:5.99mm;
  background:var(--nube)}}
.caja-aire .dentro{{outline:.6px solid rgba(18,39,51,.45)}}
.aire .texto{{font-size:9pt;line-height:1.42}}
.formula{{font-family:"Cifras","Sansation",sans-serif;font-weight:700;color:var(--azul);
  letter-spacing:.06em;font-size:10pt;margin-top:3mm}}
.escalera{{display:flex;gap:7mm;align-items:flex-end;margin:3mm 0 1mm;
  background:var(--nube);padding:6mm 5mm}}
.escalera>div{{text-align:left}}
.escalera img{{image-rendering:pixelated;display:block;margin-bottom:2.5mm;width:auto}}
.escalera span{{display:block;font-size:7.4pt;color:var(--gris);letter-spacing:.05em}}
.escalera .mal span{{color:#B3341F}}

/* ------------------------------------------------------------- hoja 4 */
.versiones{{display:grid;grid-template-columns:1fr 1fr;gap:4mm;margin-top:2mm}}
.versiones figure>div{{padding:7mm 6mm}}
.v-blanco>div{{background:#fff;border:1px solid var(--linea)}}
.v-azul>div{{background:var(--azul)}}
.v-tinta>div{{background:var(--tinta)}}
figcaption{{margin-top:2mm;font-size:8.4pt;line-height:1.35}}
figcaption b{{display:block}}
figcaption span{{color:var(--gris)}}
.fondos{{display:grid;grid-template-columns:repeat(3,1fr);gap:3mm;margin-top:2mm}}
.f{{padding:5mm 4mm 3mm;border:1px solid var(--linea);position:relative}}
.f span{{display:block;margin-top:3mm;font-size:7.4pt;letter-spacing:.05em;color:var(--gris)}}
.f[style*="0080C1"] span,.f[style*="122733"] span{{color:rgba(255,255,255,.82)}}
.f.no{{border-color:#B3341F}}
.f.no span{{color:#B3341F}}
.f.no::after{{content:"";position:absolute;inset:0;
  background:repeating-linear-gradient(45deg,rgba(179,52,31,.09) 0 6px,transparent 6px 12px)}}
.f.foto{{background:linear-gradient(118deg,#8a7a63 0%,#d8cfc0 28%,#53606b 55%,#c9b79a 78%,#2e3a44 100%)}}
.f.foto span{{color:#fff}}

/* ------------------------------------------------------------- hoja 5 */
.aro-fila{{display:grid;grid-template-columns:repeat(3,1fr);gap:5mm;margin-top:2mm}}
.cuadro{{aspect-ratio:1;display:flex;align-items:center;justify-content:center;padding:9mm}}
.cuadro.blanco{{background:#fff;border:1px solid var(--linea)}}
.cuadro.azul{{background:var(--azul)}}
.cuadro.placa{{background:var(--azul);border-radius:22%}}
.cuadro svg{{width:100%}}
.lista{{list-style:none;font-size:9pt;line-height:1.45}}
.lista li{{padding-left:5mm;position:relative;margin-bottom:1.8mm}}
.lista li::before{{content:"";position:absolute;left:0;top:1.6mm;width:2mm;height:2mm;
  background:var(--azul)}}
.nono li::before{{background:#B3341F}}
.prueba32{{display:flex;gap:7mm;align-items:flex-end;flex-wrap:wrap;margin-top:3mm;
  background:var(--nube);padding:5mm 6mm}}
.prueba32>div{{text-align:center}}
.prueba32 .mal span{{color:#B3341F}}
.prueba32 img{{image-rendering:pixelated;display:block;width:auto}}
.prueba32 .chiquita{{flex:1 1 52mm;margin:0 0 1mm;text-align:left}}
.prueba32 span{{display:block;margin-top:2mm;font-size:7.2pt;color:var(--gris)}}

/* ------------------------------------------------------------- hoja 6 */
.colores{{display:grid;grid-template-columns:1fr 1fr;gap:3mm 5mm;margin-top:2mm}}
.colores.dos{{grid-template-columns:1fr 1fr}}
.color{{display:flex;gap:3.5mm;align-items:stretch}}
.tono{{flex:0 0 17mm;border:1px solid rgba(18,39,51,.12)}}
.dat{{font-size:7.8pt;line-height:1.42}}
.dat>b{{font-size:9.4pt;display:block;margin-bottom:.6mm}}
.dat .uso b{{font-weight:700}}
.dat span{{display:block;color:var(--gris)}}
.dat .mono{{color:var(--tinta)}}
.dat .uso{{margin-top:1mm;color:var(--tinta)}}
.dat .con{{color:var(--azultxt);font-weight:600}}

/* ------------------------------------------------------------- hoja 7 */
.espec{{background:var(--nube);padding:5mm 6mm;margin-top:2mm}}
.espec .muestra{{font-size:27pt;line-height:1.1;margin:0}}
.espec.sansation .muestra{{font-family:"Cifras","Sansation",sans-serif;font-weight:700;
  letter-spacing:-.05em;color:var(--azul)}}
.espec.raleway .muestra{{font-weight:700;letter-spacing:-.02em}}
.espec .abc{{font-size:9pt;color:var(--gris);margin-top:2.5mm;line-height:1.5;
  word-spacing:.1em}}
.espec.sansation .abc{{font-family:"Cifras","Sansation",sans-serif}}
.espec .pesos{{margin-top:2.5mm;font-size:10pt}}

/* ------------------------------------------------------------- hoja 8 */
.comparacion{{display:grid;grid-template-columns:1fr 1fr;gap:5mm;margin-top:3mm}}
.comparacion>div{{background:var(--nube);padding:4mm 5mm}}
.rot{{display:block;font-family:"Cifras","Sansation",sans-serif;font-size:7.4pt;
  font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--gris)}}
.num{{font-size:21pt;line-height:1.2;margin:1.5mm 0 1.5mm;font-weight:600}}
.num.ral{{font-family:"Raleway",sans-serif;font-variant-numeric:normal;
  font-feature-settings:normal}}
.num.fir{{font-family:"Cifras","Raleway",sans-serif}}
.comparacion small{{font-size:7.6pt;color:var(--gris);line-height:1.35;display:block}}
.codigo{{font-family:"Cifras",ui-monospace,"Courier New",monospace;font-size:7.8pt;
  line-height:1.5;background:var(--tinta);color:#dde7ed;padding:4mm 5mm;margin-top:2mm;
  white-space:pre-wrap}}

/* ------------------------------------------------------------- hoja 9 */
.malos{{display:grid;grid-template-columns:repeat(3,1fr);gap:4mm 5mm;margin-top:2mm}}
.malo .m{{background:var(--nube);border:1px solid #B3341F;overflow:hidden;
  display:flex;align-items:center;justify-content:center;height:24mm;padding:4mm}}
.malo .t{{width:100%;display:flex;align-items:center;justify-content:center}}
.malo .t svg{{width:100%}}
.malo figcaption b{{color:#B3341F}}

/* ------------------------------------------------------------- hoja 10 */
.firma-final{{margin-top:9mm;padding-top:4mm;border-top:1px solid var(--linea)}}
.firma-final svg{{height:42px;width:auto}}
'''

HTML = f'''<!doctype html><html lang="es"><head><meta charset="utf-8">
<title>taller101 — manual de imagen</title>
<style>{CSS}</style></head><body>
{''.join(hoja(n, t, c, p) for n, t, c, p in PAGINAS)}
</body></html>'''

destino = AQUI / 'manual-imagen-taller101.html'
destino.write_text(HTML)
print(f'{destino}  {len(HTML):,} bytes  ·  {len(PAGINAS)} hojas')
