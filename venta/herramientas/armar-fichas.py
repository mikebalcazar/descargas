#!/usr/bin/env python3
# Arma un one-pager HTML autocontenido por app. Cero peticiones externas.
#
# Antes de correrlo hay que juntar la materia prima en /home/claude/venta/:
#   fonts/            los seis .woff2 (de t101-portal-trabajadores/public/fonts/)
#   <app>/capturas/   las capturas de claude/venta/capturas/ de cada repo
#   <app>/marca/logo.svg
# El texto de cada hoja está escrito aquí abajo a mano, no se saca de ficha.md:
# la ficha del repo es la fuente, esto es la versión editada para el cliente.
import base64, pathlib, re, html

B = pathlib.Path('/home/claude/venta')
OUT = pathlib.Path('/mnt/user-data/outputs')
OUT.mkdir(parents=True, exist_ok=True)

def b64(p):
    return base64.b64encode(pathlib.Path(p).read_bytes()).decode()

def fuentes():
    f = {n: b64(B / 'fonts' / f'{n}.woff2') for n in
         ['fira-cifras-400', 'fira-cifras-600', 'raleway-400', 'raleway-600', 'raleway-700', 'sansation-700']}
    rango = 'U+0030-0039,U+00B0,U+00B1,U+00D7,U+0025'
    css = []
    for peso, arch in [('400', 'fira-cifras-400'), ('600 700', 'fira-cifras-600')]:
        css.append(f'@font-face{{font-family:"Cifras";src:url(data:font/woff2;base64,{f[arch]}) format("woff2");'
                   f'font-weight:{peso};font-display:swap;unicode-range:{rango}}}')
    for peso in ['400', '600', '700']:
        css.append(f'@font-face{{font-family:"Raleway";src:url(data:font/woff2;base64,{f["raleway-" + peso]}) '
                   f'format("woff2");font-weight:{peso};font-display:swap}}')
    css.append(f'@font-face{{font-family:"Sansation";src:url(data:font/woff2;base64,{f["sansation-700"]}) '
               f'format("woff2");font-weight:700;font-display:swap}}')
    return '\n'.join(css)

def logo(app, viewbox=None, color=None):
    s = (B / app / 'marca' / 'logo.svg').read_text()
    if viewbox:
        s = re.sub(r'viewBox="[^"]*"', f'viewBox="{viewbox}"', s, count=1)
    s = re.sub(r'\swidth="[\d.]+"', '', s, count=1)
    s = re.sub(r'\sheight="[\d.]+"', '', s, count=1)
    if color:
        s = s.replace(color, '#0080C1').replace(color.upper(), '#0080C1')
    s = re.sub(r'<\?xml[^>]*\?>', '', s)
    s = re.sub(r'<!--.*?-->', '', s, flags=re.S)
    return s.strip()

def img(p):
    return f'data:image/png;base64,{b64(p)}'

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:"Cifras","Raleway",system-ui,sans-serif;font-variant-numeric:tabular-nums;
  -webkit-font-feature-settings:"tnum";font-feature-settings:"tnum";color:#122733;background:#e8ecef}
.hoja{width:210mm;background:#fff;margin:0 auto 8mm;padding:12mm 12mm 0;
  display:flex;flex-direction:column}
.cab{display:flex;align-items:flex-end;justify-content:space-between;gap:8mm;
  border-bottom:2px solid #0080C1;padding-bottom:5mm}
.cab svg{height:13mm;width:auto;display:block}
.lema{font-size:10.5pt;font-weight:600;color:#0080C1;text-align:right;line-height:1.35;max-width:88mm}
.que{margin:3mm 0 3mm;font-size:9.6pt;line-height:1.45;color:#2b3d48}
.que b{color:#122733;font-weight:700}
.hero{width:100%;height:38mm;object-fit:cover;object-position:top center;border:1px solid #cfd8de;border-radius:2mm;display:block}
.pie-img{font-size:7.2pt;color:#7b8a94;margin:1mm 0 4mm}
h2{font-family:"Cifras","Sansation",sans-serif;font-size:8.2pt;letter-spacing:.14em;text-transform:uppercase;
  color:#0080C1;margin:0 0 2.2mm}
.ben{display:grid;grid-template-columns:1fr 1fr;gap:1.8mm 6mm;margin-bottom:3.5mm}
.ben div{font-size:8.4pt;line-height:1.3;padding-left:8mm;position:relative;color:#2b3d48}
.ben div b{display:block;color:#122733}
.ben span{position:absolute;left:0;top:-.3mm;font-size:13pt;font-weight:700;color:#0080C1}
.fn{display:grid;grid-template-columns:1fr 1fr;gap:1.1mm 6mm;margin-bottom:4mm;font-size:8pt;color:#2b3d48}
.fn div{border-top:1px solid #e2e8ec;padding-top:1mm;line-height:1.28}
.fn b{color:#122733}
.tiras{display:grid;grid-template-columns:repeat(3,1fr);gap:2.5mm;margin-bottom:4mm}
.tiras figure{margin:0}
.tiras img{width:100%;height:18mm;object-fit:cover;object-position:top center;border:1px solid #cfd8de;border-radius:1.5mm;display:block}
.tiras figcaption{font-size:7.5pt;color:#7b8a94;margin-top:1.2mm}
.datos{margin-top:auto;background:#122733;color:#dfe8ee;border-radius:2mm;padding:4mm 5mm;
  display:grid;grid-template-columns:repeat(4,1fr);gap:3mm;font-size:8pt;line-height:1.35}
.datos b{display:block;font-size:7pt;letter-spacing:.12em;text-transform:uppercase;color:#3AA3DC;
  margin-bottom:1mm;font-weight:700}
.firma{display:flex;justify-content:space-between;align-items:center;font-size:7.2pt;color:#7b8a94;
  padding:2mm 0 3mm}
.firma b{font-family:"Cifras","Sansation",sans-serif;color:#0080C1;letter-spacing:.05em}
@media print{body{background:#fff}.hoja{margin:0;box-shadow:none}@page{size:A4;margin:0}}
"""

def hoja(app, svg, lema, que, beneficios, funciones, hero, hero_pie, tiras, datos):
    ben = ''.join(f'<div><span>{i+1}</span><b>{html.escape(t)}</b>{html.escape(d)}</div>'
                  for i, (t, d) in enumerate(beneficios))
    fns = ''.join(f'<div><b>{html.escape(t)}</b> · {html.escape(d)}</div>' for t, d in funciones)
    tir = ''.join(f'<figure><img src="{img(p)}"><figcaption>{html.escape(c)}</figcaption></figure>'
                  for p, c in tiras)
    dat = ''.join(f'<div><b>{html.escape(k)}</b>{html.escape(v)}</div>' for k, v in datos)
    return f"""<!doctype html><html lang="es"><meta charset="utf-8">
<title>{app} — Suite 101</title><style>{fuentes()}{CSS}</style>
<div class="hoja">
  <div class="cab">{svg}<div class="lema">{html.escape(lema)}</div></div>
  <p class="que">{que}</p>
  <img class="hero" src="{img(hero)}">
  <div class="pie-img">{html.escape(hero_pie)}</div>
  <h2>Por qué sirve</h2>
  <div class="ben">{ben}</div>
  <h2>Qué trae</h2>
  <div class="fn">{fns}</div>
  <div class="tiras">{tir}</div>
  <div class="datos">{dat}</div>
  <div class="firma"><span>Taller 101 · Suite 101</span><b>suite101</b></div>
</div></html>"""

# ---------------------------------------------------------------- roster101
r = B / 'roster101' / 'capturas'
pathlib.Path(OUT / 'roster101-ficha.html').write_text(hoja(
    'roster101',
    logo('roster101', viewbox='83.84 198.74 455 215'),
    'El expediente laboral lo arma el propio trabajador, desde su celular.',
    'Cada persona captura sus datos —NSS, CURP, RFC, cuenta bancaria, contacto de emergencia— y escanea '
    'sus documentos con la cámara del teléfono. La empresa los ve completos en su panel, en el orden que '
    'los pide el IMSS, el banco o el contador, y los baja en <b>PDF, CSV o ZIP</b>. Sin contraseñas: se entra '
    'con un código que llega al correo.',
    [('Cero papeles perdidos', 'Todo lo que se escribe se guarda solo. Se cierra y se vuelve días después.'),
     ('Alta en minutos', 'Un QR en la pared y la persona captura su expediente sola.'),
     ('Datos limpios de origen', 'CURP, RFC, NSS y CLABE se validan al escribir. No hay dos con el mismo NSS.'),
     ('Documentos legibles', 'El escáner recorta, endereza y quita sombras. Entrega PDF por documento.'),
     ('Cada empresa, su base', 'Worker, base y almacén separados por cliente. Bitácora de cada acceso.'),
     ('Hecho para quien no usa correo', 'Todo el expediente cabe en un celular prestado.')],
    [('Acceso por código', 'sin contraseña, tres intentos y se frena'),
     ('Expediente por partes', 'autoguardado y semáforo de avance'),
     ('Escáner', 'credencial 85.6 × 54 mm y hoja carta, PDF multipágina'),
     ('Validación en vivo', 'CURP, RFC, NSS, CLABE, celular, correo'),
     ('Panel de empresa', 'tabla, búsqueda y faltantes por persona'),
     ('Fichas PDF', 'por trabajador, campos a elegir, envío desde el celular'),
     ('Exportar todo', 'ZIP con carpeta por trabajador + CSV + bitácora'),
     ('Papelera 30 días', 'restauración y clave de administración')],
    r / '07-panel-empresa.png', 'Panel de la empresa: quién está completo y a quién le falta qué.',
    [(r / '09-celular.png', 'Captura desde el celular'),
     (r / '05-documentos.png', 'Documentos escaneados'),
     (r / '04-expediente-completo.png', 'Expediente completo')],
    [('Versión', 'portal 0.10.0 · central 0.4.0'), ('Plataforma', 'Web · celular y computadora'),
     ('Estado', 'En producción con el primer cliente'), ('Modelo', 'Renta mensual por empresa')]))

# ----------------------------------------------------------------- quell101
q = B / 'quell101' / 'capturas'
pathlib.Path(OUT / 'quell101-ficha.html').write_text(hoja(
    'quell101',
    logo('quell101', color='#0381c2'),
    'La obra, ítem por ítem, sobre el plano.',
    'Se sube el plano —PDF o foto— y se le ponen pines: uno por cada mueble, puerta o acabado. Cada pin lleva '
    'su propio camino: <b>compras, fabricación, flete, instalación, entrega</b>. Un tap por etapa y el plano '
    'entero se lee de un vistazo. Al entregar se abre el punchlist, con responsable, fecha y foto. '
    'Funciona en obra sin señal: lo que se escribe se forma en fila y se vacía solo al volver la red.',
    [('Se acaba el «¿cómo va la obra?»', 'Quien ve el plano ve el avance, sin pedirle el reporte a nadie.'),
     ('Nada se entrega dos veces', 'El punchlist vive pegado al ítem. Lo vencido se marca solo.'),
     ('El contratista ve lo suyo', 'Entra, cierra sus pendientes con foto. No ve precios ni el resto.'),
     ('Sirve donde de verdad se usa', 'Sin señal no se cae: guarda y sincroniza sola.'),
     ('Queda el historial', 'Cada acuerdo y cada foto, pegados al mueble, no perdidos en un chat.'),
     ('Sin contraseñas', 'Correo y PIN de seis dígitos. Nada que reponer.')],
    [('Plano con pines', 'varios planos por obra, PDF nítido, pan y zoom'),
     ('Ítems', 'mueble, puerta o acabado, con código y responsable'),
     ('Proceso por etapas', 'compras → fabricación → flete → instalación → entrega'),
     ('Bitácora', 'muro de notas con fotos por ítem'),
     ('Punchlist', 'asignación, evidencia, cierre del supervisor'),
     ('Dudas', 'buzón con foto en la pregunta y en la respuesta'),
     ('Roles', 'dueño, supervisor, contratista y trabajador'),
     ('Sin señal', 'en el sitio y en la app de Windows')],
    q / '1-plano.png', 'El plano de la obra: cada pin es un ítem y su color dice el tipo.',
    [(q / '2-item.png', 'Bitácora del ítem'), (q / '3-lista.png', 'La obra en lista'),
     (q / '4-dudas.png', 'Dudas desde la obra')],
    [('Versión', 'Publicación continua'), ('Plataforma', 'Web · Windows · Android en preparación'),
     ('Estado', 'En uso, primera obra'), ('Sin señal', 'Sí, lectura y escritura')]))

# ------------------------------------------------------------------ draw101
d = B / 'draw101' / 'capturas'
pathlib.Path(OUT / 'draw101-ficha.html').write_text(hoja(
    'draw101',
    logo('draw101', viewbox='-16 -12 980 465'),
    'CAD 2D para taller de muebles y despachos: abre el DWG, dibuja, acota e imprime.',
    'Abre el plano del arquitecto tal cual —capas, bloques, atributos y hojas— y saca de ahí los planos de '
    'fabricación del taller. Comandos de AutoCAD, cotas asociativas, hojas <b>A4 a A0</b> con pie de plano '
    'propio e impresión a PDF a tamaño real. <b>Sin suscripción</b>: se instala y se usa.',
    [('Abre el DWG del cliente', 'R2000 a R2018. Lo que no se entiende se conserva y vuelve a salir intacto.'),
     ('Flujo de uso familiar','Los comandos de AutoCAD que ya usas, y un menú radial con clic derecho: lo de todos los días queda donde está el cursor.'),
     ('Aguanta el plano de obra','El plano del arquitecto entra entero; pan y zoom navegan sobre él sin redibujarlo.'),
     ('Del modelo al plano', 'Hojas con pie de plano, escala por lista y vista previa antes de imprimir.'),
     ('Conectado al taller', 'Importa las cocinas de nest101, las acota solas y las actualiza.'),
     ('Se mantiene solo', 'Avisa y se actualiza. Autoguardado y recuperación tras un cierre inesperado.')],
    [('Trazo completo', 'línea, arco, spline, texto, rayado con galería de patrones'),
     ('Edición con el ratón', 'recortar, extender, empalme, chaflán, arreglos, grips'),
     ('Referencias a objetos', 'extremo, medio, centro, perpendicular, tangente'),
     ('Cotas asociativas', 'lineal, angular, radio, directriz; salen como DIMENSION'),
     ('Capas y bloques', 'color, grosor, tipo de línea; bloques con atributos'),
     ('Hojas de plano', 'A4–A0, ventanas con handles, varias por hoja'),
     ('Importar y exportar', 'DWG, DXF R2013, PDF a tamaño real, SVG, .t101x'),
     ('Tema claro y oscuro', 'deshacer ilimitado y autoguardado')],
    d / '01-modelo-cocina.png', 'Alzado de cocina acotado, con capas del taller.',
    [(d / '04-hoja-pie-de-plano.png', 'Hoja con pie de plano'),
     (d / '03-galeria-rayado.png', 'Galería de rayados'),
     (d / '06-vista-previa.png', 'Vista previa de impresión')],
    [('Versión', '0.20.1 · 9-sep-2026'), ('Plataforma', 'Windows · macOS en preparación'),
     ('Estado', 'En uso interno, v1 comercial en curso'), ('Entrega', 'Instalador con actualizador')]))

print('listo')
