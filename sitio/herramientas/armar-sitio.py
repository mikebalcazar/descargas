#!/usr/bin/env python3
# Arma el sitio de suite101: portada + una página por app.
#
# Estático puro: sin marco, sin build, sin peticiones a internet. Las fuentes
# viven en sitio/fuentes/ y las capturas en sitio/img/. Se corre desde la raíz
# del repositorio y escribe dentro de sitio/.
#
#     python3 sitio/herramientas/armar-sitio.py
#
# El texto es el que se le enseña a un cliente; la fuente técnica es el
# ficha.md de cada repositorio.

import pathlib, re, html

S = pathlib.Path(__file__).resolve().parent.parent
CORREO = "mike@forespot.com"   # ← cambiar cuando haya correo de la suite

def logo(app, viewbox=None, color=None):
    s = (S / 'marca' / f'{app}.svg').read_text()
    if viewbox:
        s = re.sub(r'viewBox="[^"]*"', f'viewBox="{viewbox}"', s, count=1)
    s = re.sub(r'\swidth="[\d.]+"', '', s, count=1)
    s = re.sub(r'\sheight="[\d.]+"', '', s, count=1)
    if color:
        s = s.replace(color, '#0080C1')
    s = re.sub(r'<\?xml[^>]*\?>', '', s)
    s = re.sub(r'<!--.*?-->', '', s, flags=re.S)
    return s.strip()

APPS = {
 'roster101': dict(
   vb='83.84 198.74 455 215',
   lema='El expediente laboral lo arma el propio trabajador, desde su celular.',
   corto='Expedientes del personal, capturados desde el celular.',
   estado='En producción', plataforma='Web · celular y computadora',
   entrada='Cada persona captura sus datos —NSS, CURP, RFC, cuenta bancaria, contacto de emergencia— y '
           'escanea sus documentos con la cámara del teléfono. La empresa los ve completos en su panel, en el '
           'orden que los pide el IMSS, el banco o el contador, y los baja en PDF, CSV o ZIP. Sin contraseñas: '
           'se entra con un código que llega al correo.',
   ben=[('Cero papeles perdidos','Todo lo que se escribe se guarda solo. Se cierra y se vuelve días después.'),
        ('Alta en minutos','Un QR en la pared y la persona captura su expediente sola.'),
        ('Datos limpios de origen','CURP, RFC, NSS y CLABE se validan al escribir. No hay dos con el mismo NSS.'),
        ('Documentos legibles','El escáner recorta, endereza y quita sombras. Entrega PDF por documento.'),
        ('Cada empresa, su base','Worker, base y almacén separados por cliente. Bitácora de cada acceso.'),
        ('Para quien no usa correo','Todo el expediente cabe en un celular prestado.')],
   fn=[('Acceso por código','sin contraseña, tres intentos y se frena'),
       ('Expediente por partes','autoguardado y semáforo de avance'),
       ('Escáner','credencial 85.6 × 54 mm y hoja carta, PDF multipágina'),
       ('Validación en vivo','CURP, RFC, NSS, CLABE, celular, correo'),
       ('Panel de empresa','tabla, búsqueda y faltantes por persona'),
       ('Fichas PDF','por trabajador, campos a elegir, envío desde el celular'),
       ('Exportar todo','ZIP con carpeta por trabajador + CSV + bitácora'),
       ('Papelera 30 días','restauración y clave de administración')],
   img=[('07-panel-empresa.png','El panel de la empresa: quién está completo y a quién le falta qué'),
        ('09-celular.png','La captura, desde el celular del trabajador'),
        ('05-documentos.png','Documentos escaneados con la cámara'),
        ('04-expediente-completo.png','El expediente completo, listo para el contador')],
   datos=[('Versión','portal 0.10.0 · central 0.4.0'),('Plataforma','Web · celular y computadora'),
          ('Estado','En producción con el primer cliente'),('Modelo','Renta mensual por empresa')]),

 'quell101': dict(
   vb='118 198 418 216', color='#0381c2',
   lema='La obra, ítem por ítem, sobre el plano.',
   corto='El avance de la obra, pin por pin, sobre el plano.',
   estado='En uso', plataforma='Web · Android · Windows',
   entrada='Se sube el plano —PDF o foto— y se le ponen pines: uno por cada mueble, puerta o acabado. Cada pin '
           'lleva su propio camino: compras, fabricación, flete, instalación, entrega. Un tap por etapa y el '
           'plano entero se lee de un vistazo. Al entregar se abre el punchlist, con responsable, fecha y foto. '
           'En obra sin señal no se cae: lo que se escribe se forma en fila y se vacía solo al volver la red.',
   ben=[('Se acaba el «¿cómo va la obra?»','Quien ve el plano ve el avance, sin pedirle el reporte a nadie.'),
        ('Nada se entrega dos veces','El punchlist vive pegado al ítem. Lo vencido se marca solo.'),
        ('El contratista ve lo suyo','Entra, cierra sus pendientes con foto. No ve precios ni el resto.'),
        ('Sirve donde se usa','Sin señal guarda y sincroniza sola.'),
        ('Queda el historial','Cada acuerdo y cada foto, pegados al mueble, no perdidos en un chat.'),
        ('Sin contraseñas','Correo y PIN de seis dígitos. Nada que reponer.')],
   fn=[('Plano con pines','varios planos por obra, PDF nítido, pan y zoom'),
       ('Ítems','mueble, puerta o acabado, con código y responsable'),
       ('Proceso por etapas','compras → fabricación → flete → instalación → entrega'),
       ('Bitácora','muro de notas con fotos por ítem'),
       ('Punchlist','asignación, evidencia, cierre del supervisor'),
       ('Dudas','buzón con foto en la pregunta y en la respuesta'),
       ('Roles','dueño, supervisor, contratista y trabajador'),
       ('Sin señal','apps de Android y Windows, además del sitio')],
   img=[('1-plano.png','El plano de la obra: cada pin es un ítem y su color dice el tipo'),
        ('2-item.png','La bitácora del ítem, con lo acordado y cuándo'),
        ('3-lista.png','La obra entera en lista, cuando el plano ya no basta'),
        ('4-dudas.png','Las dudas que levanta quien está en obra y no decide')],
   datos=[('Versión','Publicación continua'),('Plataforma','Web · Android · Windows'),
          ('Estado','En uso, primera obra'),('Sin señal','Sí, lectura y escritura')]),

 'draw101': dict(
   vb='-16 -12 980 465',
   lema='CAD 2D para taller de muebles y despachos: abre el DWG, dibuja, acota e imprime.',
   corto='CAD 2D que abre el DWG del arquitecto y saca el plano de fabricación.',
   estado='Uso interno · v1 en curso', plataforma='Windows · macOS en preparación',
   entrada='Abre el plano del arquitecto tal cual —capas, bloques, atributos y hojas— y saca de ahí los planos '
           'de fabricación del taller. Comandos de AutoCAD, cotas asociativas, hojas A4 a A0 con pie de plano '
           'propio e impresión a PDF a tamaño real. Sin suscripción: se instala y se usa.',
   ben=[('Abre el DWG del cliente','R2000 a R2018. Lo que no se entiende se conserva y vuelve a salir intacto.'),
        ('Se aprende en una tarde','Comandos de AutoCAD en inglés o español, menú radial con clic derecho.'),
        ('Rápido con planos pesados','130 000 trazos se pintan en 35 ms. Cuesta lo que cambió, no lo que mide.'),
        ('Del modelo al plano','Hojas con pie de plano, escala por lista y vista previa antes de imprimir.'),
        ('Conectado al taller','Importa las cocinas del despiezador, las acota solas y las actualiza.'),
        ('Se mantiene solo','Avisa y se actualiza. Autoguardado y recuperación tras un cierre inesperado.')],
   fn=[('Trazo completo','línea, arco, spline, texto, rayado con galería de patrones'),
       ('Edición con el ratón','recortar, extender, empalme, chaflán, arreglos, grips'),
       ('Referencias a objetos','extremo, medio, centro, perpendicular, tangente'),
       ('Cotas asociativas','lineal, angular, radio, directriz; salen como DIMENSION'),
       ('Capas y bloques','color, grosor, tipo de línea; bloques con atributos'),
       ('Hojas de plano','A4–A0, ventanas con handles, varias por hoja'),
       ('Importar y exportar','DWG, DXF R2013, PDF a tamaño real, SVG, .t101x'),
       ('Tema claro y oscuro','deshacer ilimitado y autoguardado')],
   img=[('01-modelo-cocina.png','Alzado de cocina acotado, con las capas del taller'),
        ('04-hoja-pie-de-plano.png','La hoja con pie de plano, lista para imprimir'),
        ('03-galeria-rayado.png','Galería de rayados, con previa en vivo'),
        ('02-propiedades-en-vivo.png','Propiedades del objeto, en vivo')],
   datos=[('Versión','0.20.1 · 9-sep-2026'),('Plataforma','Windows · macOS en preparación'),
          ('Estado','En uso interno, v1 comercial en curso'),('Entrega','Instalador con actualizador')]),
}

PENDIENTES = [
 ('quote101','La cotización del mueble, desglosada por componente.','Producción'),
 ('nest101','El despiece: del mueble a la lista de corte.','Producción'),
 ('dash101','Las cuentas del taller: proyectos, gastos y flujo.','Producción'),
 ('peek101','El portal del cliente: su proyecto y su estado de cuenta.','Producción'),
]

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
:root{--azul:#0080C1;--claro:#3AA3DC;--tinta:#122733;--gris:#5b6b76;--linea:#dfe6ea}
@font-face{font-family:"Cifras";src:url(../fuentes/fira-cifras-400.woff2) format("woff2");font-weight:400;
  font-display:swap;unicode-range:U+0030-0039,U+00B0,U+00B1,U+00D7,U+0025}
@font-face{font-family:"Cifras";src:url(../fuentes/fira-cifras-600.woff2) format("woff2");font-weight:600 700;
  font-display:swap;unicode-range:U+0030-0039,U+00B0,U+00B1,U+00D7,U+0025}
@font-face{font-family:"Raleway";src:url(../fuentes/raleway-400.woff2) format("woff2");font-weight:400;font-display:swap}
@font-face{font-family:"Raleway";src:url(../fuentes/raleway-600.woff2) format("woff2");font-weight:600;font-display:swap}
@font-face{font-family:"Raleway";src:url(../fuentes/raleway-700.woff2) format("woff2");font-weight:700;font-display:swap}
@font-face{font-family:"Sansation";src:url(../fuentes/sansation-700.woff2) format("woff2");font-weight:700;font-display:swap}
html{scroll-behavior:smooth}
body{font-family:"Cifras","Raleway",system-ui,sans-serif;font-variant-numeric:tabular-nums;
  font-feature-settings:"tnum";color:var(--tinta);background:#fff;line-height:1.55;-webkit-font-smoothing:antialiased}
a{color:inherit}
.env{max-width:1120px;margin:0 auto;padding:0 24px}
.barra{position:sticky;top:0;z-index:9;background:rgba(255,255,255,.93);backdrop-filter:blur(8px);
  border-bottom:1px solid var(--linea)}
.barra .env{display:flex;align-items:center;justify-content:space-between;height:64px}
.marca{font-family:"Cifras","Sansation",sans-serif;font-size:20px;color:var(--azul);text-decoration:none;letter-spacing:.02em}
.barra nav a{margin-left:22px;text-decoration:none;font-size:14px;font-weight:600;color:var(--gris)}
.barra nav a:hover{color:var(--azul)}
.hero{background:var(--tinta);color:#eaf2f7;padding:86px 0 78px}
.hero h1{font-size:clamp(30px,5vw,50px);line-height:1.12;font-weight:700;letter-spacing:-.015em;max-width:16ch}
.hero p{margin-top:20px;font-size:clamp(16px,2.2vw,19px);color:#a9c0ce;max-width:60ch}
.hero .cifra{color:var(--claro);font-weight:700}
.btn{display:inline-block;margin-top:28px;background:var(--azul);color:#fff;text-decoration:none;
  padding:13px 24px;border-radius:6px;font-weight:700;font-size:15px}
.btn:hover{background:var(--claro)}
.btn.fantasma{background:transparent;border:1px solid rgba(255,255,255,.35);margin-left:10px}
section{padding:64px 0}
h2{font-size:clamp(22px,3vw,30px);letter-spacing:-.01em;margin-bottom:10px}
.sub{color:var(--gris);max-width:62ch;margin-bottom:32px}
.rejilla{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:20px}
.tarjeta{border:1px solid var(--linea);border-radius:10px;padding:24px;text-decoration:none;display:block;
  transition:border-color .15s,transform .15s;background:#fff}
.tarjeta:hover{border-color:var(--azul);transform:translateY(-2px)}
.tarjeta svg{height:26px;width:auto;display:block;margin-bottom:14px}
.tarjeta p{font-size:15px;color:var(--gris);min-height:48px}
.tarjeta.pronto{opacity:.62;pointer-events:none}
.sello{display:inline-block;margin-top:14px;font-size:11px;font-weight:700;letter-spacing:.1em;
  text-transform:uppercase;color:var(--azul);background:#eaf5fb;padding:4px 9px;border-radius:99px}
.flujo{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:14px;margin-top:8px}
.paso{border-top:3px solid var(--azul);padding-top:12px;font-size:14px;color:var(--gris)}
.paso b{display:block;font-family:"Cifras","Sansation",sans-serif;color:var(--tinta);font-size:15px;margin-bottom:3px}
.cierre{background:#f4f7f9;border-top:1px solid var(--linea)}
footer{padding:28px 0;font-size:13px;color:var(--gris);border-top:1px solid var(--linea)}
footer .env{display:flex;justify-content:space-between;flex-wrap:wrap;gap:10px}
/* página de app */
.tapa{padding:64px 0 44px;border-bottom:1px solid var(--linea)}
.tapa svg{height:40px;width:auto;display:block;margin-bottom:22px}
.tapa .lema{font-size:clamp(21px,3.2vw,30px);font-weight:700;letter-spacing:-.01em;max-width:22ch;color:var(--azul)}
.tapa .entrada{margin-top:18px;font-size:17px;color:#31434f;max-width:66ch}
.tapa .btn{background:var(--azul)}
figure{margin:0 0 38px}
figure img{width:100%;border:1px solid var(--linea);border-radius:8px;display:block}
figcaption{font-size:13px;color:var(--gris);margin-top:9px}
.dos{display:grid;grid-template-columns:1fr 1fr;gap:22px 46px}
.ben b{display:block}
.ben>div{padding-left:34px;position:relative;margin-bottom:18px;color:var(--gris);font-size:15px}
.ben>div span{position:absolute;left:0;top:-2px;font-size:19px;font-weight:700;color:var(--azul)}
.fn>div{border-top:1px solid var(--linea);padding:10px 0;font-size:14.5px;color:var(--gris)}
.fn b{color:var(--tinta)}
.datos{background:var(--tinta);color:#dfe8ee;border-radius:10px;padding:26px 30px;display:grid;
  grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:22px;font-size:14.5px}
.datos b{display:block;font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--claro);margin-bottom:4px}
@media(max-width:720px){.dos{grid-template-columns:1fr}.hero{padding:60px 0 54px}section{padding:46px 0}}
"""

def barra(pref=''):
    return f"""<header class="barra"><div class="env">
<a class="marca" href="{pref}index.html">suite101</a>
<nav><a href="{pref}index.html#apps">Programas</a><a href="{pref}index.html#flujo">Cómo encajan</a>
<a href="mailto:{CORREO}">Contacto</a></nav></div></header>"""

def pie():
    return f"""<footer><div class="env"><span>Taller 101 · Suite 101 · Hecho en el taller, probado en obra</span>
<a href="mailto:{CORREO}">{CORREO}</a></div></footer>"""

def cabeza(titulo, desc, css='estilo.css'):
    return f"""<!doctype html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(titulo)}</title><meta name="description" content="{html.escape(desc)}">
<link rel="stylesheet" href="{css}"></head><body>"""

# ------------------------------------------------------------------ portada
tarjetas = []
for app, d in APPS.items():
    tarjetas.append(f"""<a class="tarjeta" href="app/{app}.html">{logo(app, d.get('vb'), d.get('color'))}
<p>{html.escape(d['corto'])}</p><span class="sello">{html.escape(d['estado'])}</span></a>""")
for app, corto, estado in PENDIENTES:
    tarjetas.append(f"""<div class="tarjeta pronto"><div class="marca" style="font-size:22px;margin-bottom:14px">{app}</div>
<p>{html.escape(corto)}</p><span class="sello">Ficha en preparación</span></div>""")

pasos = [('quote101','Se cotiza el mueble, componente por componente.'),
         ('nest101','Se despieza: lista de corte y herrajes.'),
         ('draw101','Salen los planos de fabricación.'),
         ('quell101','La obra se sigue sobre el plano, ítem por ítem.'),
         ('roster101','La gente que la hace, con su expediente en regla.'),
         ('dash101','Y las cuentas cierran solas.')]

portada = cabeza('Suite 101 — programas para taller de muebles',
                 'Seis programas para el taller que ya trabaja: cotización, despiece, planos, obra, personal y cuentas.') + f"""
{barra()}
<div class="hero"><div class="env">
<h1>El taller entero, de la cotización a la entrega.</h1>
<p>Suite 101 son <span class="cifra">seis</span> programas que se hablan entre ellos: cotizas, despiezas, dibujas,
sigues la obra, llevas al personal y cierras las cuentas. Cada uno se usa solo; juntos, el dato se captura
<span class="cifra">una</span> vez.</p>
<a class="btn" href="#apps">Ver los programas</a>
<a class="btn fantasma" href="mailto:{CORREO}">Pedir una demostración</a>
</div></div>

<section id="apps"><div class="env">
<h2>Los programas</h2>
<p class="sub">Hechos en un taller que fabrica todos los días, no en un escritorio. Lo que no se usaba, no se quedó.</p>
<div class="rejilla">{''.join(tarjetas)}</div>
</div></section>

<section id="flujo" class="cierre"><div class="env">
<h2>Cómo encajan</h2>
<p class="sub">El mismo mueble recorre los seis programas sin volver a capturarse.</p>
<div class="flujo">{''.join(f'<div class="paso"><b>{a}</b>{html.escape(t)}</div>' for a, t in pasos)}</div>
</div></section>

<section><div class="env">
<h2>¿Le sirve a tu taller?</h2>
<p class="sub">Se instala por partes: se empieza por el programa que más duele y los demás entran después.
Escríbenos y te enseñamos el que te toque, con datos de una obra de verdad.</p>
<a class="btn" href="mailto:{CORREO}">Escríbenos</a>
</div></section>
{pie()}</body></html>"""
(S / 'index.html').write_text(portada)

# --------------------------------------------------------- páginas por app
for app, d in APPS.items():
    ben = ''.join(f'<div><span>{i+1}</span><b>{html.escape(t)}</b>{html.escape(x)}</div>'
                  for i, (t, x) in enumerate(d['ben']))
    fn = ''.join(f'<div><b>{html.escape(t)}</b> · {html.escape(x)}</div>' for t, x in d['fn'])
    dat = ''.join(f'<div><b>{html.escape(k)}</b>{html.escape(v)}</div>' for k, v in d['datos'])
    figs = ''.join(f'<figure><img src="../img/{app}/{f}" alt="{html.escape(c)}" loading="lazy">'
                   f'<figcaption>{html.escape(c)}</figcaption></figure>' for f, c in d['img'])
    pag = cabeza(f'{app} — Suite 101', d['corto'], css='../estilo.css') + f"""
{barra('../')}
<div class="tapa"><div class="env">
{logo(app, d.get('vb'), d.get('color'))}
<div class="lema">{html.escape(d['lema'])}</div>
<p class="entrada">{html.escape(d['entrada'])}</p>
<a class="btn" href="mailto:{CORREO}?subject={app}">Pedir una demostración</a>
</div></div>

<section><div class="env">{figs}</div></section>

<section class="cierre"><div class="env">
<h2>Por qué sirve</h2><div class="dos ben">{ben}</div>
</div></section>

<section><div class="env">
<h2>Qué trae</h2><div class="dos fn">{fn}</div>
<div style="height:36px"></div>
<div class="datos">{dat}</div>
</div></section>
{pie()}</body></html>"""
    (S / 'app' / f'{app}.html').write_text(pag)

(S / 'estilo.css').write_text(CSS)
print('portada + ', len(APPS), 'páginas')
