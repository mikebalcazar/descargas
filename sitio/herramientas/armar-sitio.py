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
CORREO = "info@forespot.com"

def logo(app, viewbox=None, color=None):
    s = (S / 'marca' / f'{app}.svg').read_text()
    if viewbox:
        s = re.sub(r'viewBox="[^"]*"', f'viewBox="{viewbox}"', s, count=1)
    # El width y el height se le quitan a la etiqueta <svg> para que mande el
    # CSS. Antes se borraba el primer width y el primer height del archivo,
    # cayera donde cayera: en roster101 el <svg> no los trae y el recorte se
    # comía los del <rect> siguiente, que es el «1» del «101». Por eso el
    # logotipo de roster101 salía «01» en el sitio publicado.
    s = re.sub(r'<svg\b[^>]*>',
               lambda m: re.sub(r'\s(?:width|height)="[^"]*"', '', m.group(0)),
               s, count=1)
    # Fuera la placa de fondo. quell101.svg viene del programa de dibujo con un
    # rect blanco del tamaño del lienzo debajo de todo; incrustado en la página
    # sería un cuadro blanco tapando lo que hubiera atrás. Antes desaparecía de
    # rebote, porque el recorte de width y height le tocaba a él.
    s = re.sub(r'<rect(?![^>]*\sx=)[^>]*\swidth="[\d.]+"[^>]*/>', '', s, count=1)
    if color:
        s = s.replace(color, '#0080C1')
    s = re.sub(r'<\?xml[^>]*\?>', '', s)
    s = re.sub(r'<!--.*?-->', '', s, flags=re.S)
    return s.strip()

APPS = {
 'roster101': dict(
   lema='El expediente laboral lo arma el propio trabajador, desde su celular.',
   corto='Expedientes del personal, capturados desde el celular.',
   estado='En producción', plataforma='Web · celular y computadora',
   entrada='Cada persona captura sus datos —NSS, CURP, RFC, cuenta bancaria, contacto de emergencia— y '
           'escanea sus documentos con la cámara del teléfono. La empresa los ve completos en su panel, en el '
           'orden que los pide el IMSS, el banco o el contador, y los baja en PDF, CSV o ZIP. Sin contraseñas: '
           'se entra con un código que llega al correo.',
   ben=[('Cero papeles perdidos','Todo lo que se escribe se guarda solo. Se cierra y se retoma días después.'),
        ('Alta en minutos','Un código QR en la pared y la persona llena su expediente sola.'),
        ('Datos correctos desde el principio','CURP, RFC, NSS y CLABE se revisan mientras se escriben. No se cuelan dos personas con el mismo NSS.'),
        ('Documentos legibles','El escáner recorta, endereza y quita sombras. Entrega PDF por documento.'),
        ('Cada empresa, su propia base','Los datos de cada cliente viven aparte, y queda bitácora de cada acceso.'),
        ('Sirve hasta en teléfono prestado','El expediente completo se llena desde cualquier celular.')],
   fn=[('Entrar con código','sin contraseña; a los tres intentos se bloquea'),
       ('Expediente por partes','se guarda solo y un semáforo dice qué falta'),
       ('Escáner','credencial 85.6 × 54 mm y hoja carta, PDF multipágina'),
       ('Revisión al escribir','CURP, RFC, NSS, CLABE, celular y correo'),
       ('Panel de empresa','tabla, búsqueda y faltantes por persona'),
       ('Fichas en PDF','por trabajador, con los campos que elijas, y se mandan desde el celular'),
       ('Exportar todo','ZIP con carpeta por trabajador + CSV + bitácora'),
       ('Papelera de 30 días','lo borrado se puede recuperar, con clave de administrador')],
   img=[('07-panel-empresa.png','El panel de la empresa: quién está completo y a quién le falta qué'),
        ('09-celular.png','La captura, desde el celular del trabajador'),
        ('05-documentos.png','Documentos escaneados con la cámara'),
        ('04-expediente-completo.png','El expediente completo, listo para el contador'),
        ('01-acceso-correo.png','Se entra con un código que llega al correo, sin contraseña')],
   datos=[('Versión','portal 0.10.0 · central 0.4.0'),('Plataforma','Web · celular y computadora'),
          ('Estado','En producción con el primer cliente'),('Modelo','Renta mensual por empresa')]),

 'quell101': dict(
   lema='La obra, mueble por mueble, sobre el plano.',
   corto='El avance de la obra, pin por pin, sobre el plano.',
   estado='En uso', plataforma='Web · Windows · Android en preparación',
   entrada='Se sube el plano —PDF o foto— y se le ponen pines: uno por cada mueble, puerta o acabado. Cada pin '
           'lleva su propio camino: compras, fabricación, flete, instalación, entrega. Un toque por etapa y el '
           'plano entero se lee de una mirada. Al entregar se abre la lista de pendientes, con quién responde y para cuándo. '
           'En obra sin señal no se cae: lo que escribes se va guardando y se sube solo cuando regresa la red.',
   ben=[('Se acaba el «¿cómo va la obra?»','Quien abre el plano ve el avance, sin pedirle el reporte a nadie.'),
        ('Nada se entrega dos veces','La lista de pendientes vive pegada al mueble. Lo que se vence se marca solo.'),
        ('El contratista ve lo suyo','Entra, cierra sus pendientes con foto. No ve precios ni el resto.'),
        ('Sirve donde se usa','Sin señal guarda y sincroniza sola.'),
        ('Queda el historial','Cada acuerdo y cada foto, pegados al mueble, no perdidos en un chat.'),
        ('Sin contraseñas','Correo y PIN de seis dígitos. Nada que reponer.')],
   fn=[('Plano con pines','varios planos por obra, PDF nítido, pan y zoom'),
       ('Piezas','mueble, puerta o acabado, con su código y con quién responde'),
       ('Proceso por etapas','compras → fabricación → flete → instalación → entrega'),
       ('Bitácora','notas con foto, pegadas a cada pieza'),
       ('Lista de pendientes','a quién le toca, foto de prueba y cierre del supervisor'),
       ('Dudas','buzón con foto en la pregunta y en la respuesta'),
       ('Roles','dueño, supervisor, contratista y trabajador'),
       ('Sin señal','en el sitio y en la app de Windows')],
   img=[('1-plano.png','El plano de la obra: cada pin es una pieza y el color dice de qué tipo'),
        ('2-item.png','La bitácora de la pieza, con lo que se acordó y cuándo'),
        ('3-lista.png','La obra entera en lista, cuando el plano ya no basta'),
        ('4-dudas.png','Las dudas de quien está en obra y no le toca decidir')],
   datos=[('Versión','Publicación continua'),('Plataforma','Web · Windows · Android en preparación'),
          ('Estado','En uso, primera obra'),('Sin señal','Sí, lectura y escritura')]),

 'draw101': dict(
   lema='CAD 2D para taller de muebles y despachos: abre el DWG, dibuja, acota e imprime.',
   corto='CAD 2D que abre el DWG del arquitecto y saca el plano de fabricación.',
   estado='Uso interno · v1 en curso', plataforma='Windows · macOS en preparación',
   entrada='Abre el plano del arquitecto tal cual —capas, bloques, atributos y hojas— y saca de ahí los planos '
           'de fabricación del taller. Comandos de AutoCAD, menú radial para lo de todos los días, cotas asociativas, hojas A4 a A0 con pie de plano '
           'propio e impresión a PDF a tamaño real. Sin suscripción: se instala y se usa.',
   ben=[('Abre el DWG del cliente','De R2000 a R2018. Lo que no reconoce lo conserva y lo devuelve igual que entró.'),
        ('Flujo de uso familiar','Los comandos de AutoCAD que ya usas, y un menú radial con clic derecho: lo de todos los días queda donde está el cursor.'),
        ('Aguanta el plano de obra','El plano del arquitecto entra entero; pan y zoom navegan sobre él sin redibujarlo.'),
        ('Del modelo al plano','Hojas con pie de plano, escala de lista y vista previa antes de mandar a imprimir.'),
        ('Conectado al taller','Importa las cocinas de nest101, las acota solas y las actualiza.'),
        ('Se mantiene solo','Avisa y se actualiza. Guarda solo y recupera el trabajo si se cierra de golpe.')],
   fn=[('Trazo completo','línea, arco, spline, texto y achurado con galería de patrones'),
       ('Edición con el ratón','recortar, extender, redondeo, chaflán, arreglos y puntos de agarre'),
       ('Referencias a objetos','extremo, medio, centro, perpendicular, tangente'),
       ('Cotas asociativas','lineal, angular, radio y línea de referencia; salen como DIMENSION'),
       ('Capas y bloques','color, grosor, tipo de línea; bloques con atributos'),
       ('Hojas de plano','de A4 a A0, con ventanas que se ajustan con el ratón, varias por hoja'),
       ('Importar y exportar','DWG, DXF R2013, PDF a tamaño real, SVG, .t101x'),
       ('Tema claro y oscuro','deshacer ilimitado y autoguardado')],
   img=[('01-modelo-cocina.png','Alzado de cocina acotado, con las capas del taller'),
        ('04-hoja-pie-de-plano.png','La hoja con pie de plano, lista para imprimir'),
        ('03-galeria-rayado.png','La galería de achurados, con vista previa al momento'),
        ('02-propiedades-en-vivo.png','Las propiedades del objeto, al momento'),
        ('06-vista-previa.png','La vista previa antes de mandar a imprimir')],
   datos=[('Versión','0.20.1 · 9-sep-2026'),('Plataforma','Windows · macOS en preparación'),
          ('Estado','En uso interno, v1 comercial en curso'),('Entrega','Instalador con actualizador')]),

 'quote101': dict(
   lema='Del levantamiento de medidas a la propuesta firmada.',
   corto='La cotización del mueble, desglosada por componente.',
   estado='En producción', plataforma='Web, sin instalar',
   entrada='Armas el mueble por partes —gabinetes, cajones, entrepaños, postes, cubiertas, laminados— y las '
           'cuentas salen solas: indirectos, ingeniería, embalaje, flete, comisiones e IVA. De ahí sale el PDF '
           'para el cliente, con firma y condiciones, y el Excel para el arquitecto. Los precios viven en una '
           'sola tabla: se corrige ahí y toda cotización nueva ya sale con el precio bueno.',
   ben=[('La propuesta sale en minutos','Los indirectos, la ingeniería, el embalaje, el flete y el IVA se calculan solos. Tú metes las piezas.'),
        ('Se ve como se tiene que ver','El PDF lleva logotipo, firma, especificación de materiales y las condiciones con su fecha de vigencia.'),
        ('Los precios, en un solo lugar','Más de 200 valores en una tabla central. Se cambia una vez y vale para todas.'),
        ('No se pierde ninguna versión','Cada versión guardada queda en el historial y se puede volver a abrir tal como estaba.'),
        ('Conectado al taller','Lee el archivo de nest101: los gabinetes, cajones y entrepaños entran como renglones de la cotización.')],
   fn=[('Clientes y proyectos','cotizaciones anidadas, búsqueda al escribir, renombrar y archivar'),
       ('El mueble por partes','gabinetes, cajones, entrepaños, postes, cubiertas, laminados, luz, puertas y especiales'),
       ('Tabla de precios','más de 200 valores por material, tipo y acabado; se puede regresar a los de fábrica'),
       ('PDF para el cliente','desglose por mueble, resumen de cargos, materiales, diez cláusulas y bloque de firma'),
       ('Excel para el arquitecto','una hoja por mueble, con sus partes, sus precios y la marca aplicada'),
       ('Recibos','folio consecutivo, firma incluida y el monto con letra'),
       ('Materiales del proyecto','marca y modelo de formaica, superficie sólida, chapas y laca; salen en el PDF'),
       ('Importar de nest101','abre el .t101x, enseña los gabinetes con sus medidas y tú escoges cuáles entran')],
   img=[('01-clientes.png','Los clientes, con sus proyectos y sus cotizaciones'),
        ('02-cotizacion.png','La cotización armada, mueble por mueble')],
   datos=[('Versión','G80'),('Plataforma','Web, sin instalar'),
          ('Estado','En producción, uso diario'),('Se conecta con','nest101, por archivo .t101x')]),

 'nest101': dict(
   lema='Del mueble a la lista de corte.',
   corto='El despiece: del mueble a la lista de corte.',
   estado='En producción', plataforma='Windows',
   entrada='Toma el mueble y saca lo que el taller necesita para cortarlo: lista de corte, herrajes, fichas, '
           'planos acotados y Excel. Lo mismo sale como archivo .t101x, que draw101 abre para acotar los planos '
           'y quote101 lee para armar la cotización, así que el mueble no se vuelve a capturar en ninguno de los dos.',
   ben=[('Lo que despiezas ya no se recaptura','El archivo .t101x pasa el mueble a draw101 y a quote101 tal como quedó.'),
        ('Alcanza la pantalla y el papel','Cotas, lista de corte, fichas, planos y Excel salen todos del mismo despiece.'),
        ('Los números se leen de un golpe','Medidas, cantidades, precios y fechas van en cifras de la misma altura, con las columnas alineadas. Un número mal leído es una pieza mal cortada.'),
        ('draw101 acota lo que sale de aquí','Las cocinas entran a draw101, se acotan solas y se actualizan cuando cambia el mueble.'),
        ('quote101 lo cotiza sin volver a teclear','Los gabinetes, cajones y entrepaños se vuelven renglones de la cotización.')],
   fn=[('Lista de corte','las piezas del mueble, listas para quien corta'),
       ('Herrajes','la cuenta de lo que hay que pedir'),
       ('Fichas de mueble','para quien arma en el taller'),
       ('Planos acotados','del despiece, para la pantalla y para el papel'),
       ('Salida a Excel','las tablas, con las columnas de números alineadas'),
       ('Archivo .t101x','el puente hacia draw101 y quote101'),
       ('Cifras legibles','medidas, cantidades, precios y fechas con cifras de una sola altura'),
       ('Instalador de Windows','con actualizador')],
   img=[('maqueta-lista-de-corte.png','La lista de corte del mueble, pieza por pieza, con material y canto'),
        ('maqueta-plano-acotado.png','El plano acotado del despiece, listo para imprimir'),
        ('maqueta-herrajes.png','Los herrajes del proyecto, con lo que hay y lo que falta pedir'),
        ('maqueta-ficha-mueble.png','La ficha del mueble, la que se lleva quien lo arma'),
        ('maqueta-proyectos.png','Los proyectos del taller y en qué va el despiece de cada uno')],
   datos=[('Versión','0.15.6 · 8-sep-2026'),('Plataforma','Windows'),
          ('Estado','En producción'),('Entrega','Instalador con actualizador')]),

 'dash101': dict(
   lema='El dinero del taller, en una sola pantalla.',
   corto='Las cuentas del taller: proyectos, gastos y flujo.',
   estado='En producción', plataforma='Web, sin instalar',
   entrada='Lleva las cuentas de un negocio que trabaja por proyecto: cuánto entró, cuánto salió, a qué '
           'proyecto pertenece cada peso y cuánto queda. No sustituye al contador ni factura: es el tablero '
           'donde el dueño ve, sin abrir una hoja de cálculo, si el proyecto que está fabricando ya se pagó '
           'solo o todavía va perdiendo. Maneja varios negocios con la misma cuenta y separa lo que cada quien '
           'alcanza a ver.',
   ben=[('Sabe qué proyecto deja y cuál no','Cada ingreso y cada gasto se amarra a un proyecto, así que el margen no se saca a fin de mes: está a la vista.'),
        ('Dice cuánto va a haber, no nada más cuánto hay','La proyección a 52 semanas toma los gastos fijos y avisa en qué semana el saldo cruza el cero, con tiempo para moverle.'),
        ('Varios negocios, una sola cuenta','Cambiar de empresa es un clic, y los catálogos, saldos y proyectos de cada una no se mezclan.'),
        ('Se reparte sin dar todo','Se invita por correo con un puesto y un alcance: quien lleva un proyecto ve ese proyecto, no los márgenes de los demás.'),
        ('Se captura en segundos','Un movimiento son cinco campos, y si el proyecto, el cliente o el proveedor todavía no existen, se crean sin salir de la pantalla.')],
   fn=[('Movimientos','ingresos y gastos con proyecto, cuenta y con quién; los saldos se recalculan solos'),
       ('Proyectos','precio de venta, compromisos con proveedores, cobrado, pagado y disponible por obra'),
       ('Flujo a 52 semanas','gráfica y tabla de lo que viene, con aviso cuando el saldo se va a cero'),
       ('Gastos fijos','renta, nómina y servicios, semanales, mensuales o anuales, que alimentan la proyección'),
       ('Cuentas','bancos y caja, cada una con su saldo al día y su moneda'),
       ('Clientes y proveedores','directorio con RFC y datos de contacto; los proveedores se comparten entre negocios'),
       ('Equipo','invitación por correo, puestos y alcance por proyecto'),
       ('Portal del cliente','el cliente entra con correo y PIN y ve lo suyo; nunca ve proveedores ni márgenes')],
   no=['No factura ni timbra ante el SAT.',
       'No hace contabilidad electrónica ni pólizas.',
       'No se conecta al banco: los movimientos se capturan a mano.',
       'No maneja inventario ni nómina.'],
   img=[('maqueta-tablero.png','El tablero: saldos, flujo a 52 semanas y el margen de cada proyecto'),
        ('maqueta-movimientos.png','Los movimientos del mes, cada uno amarrado a su proyecto'),
        ('maqueta-proyectos.png','Cada obra con lo cobrado, lo pagado y su margen'),
        ('maqueta-gastos-fijos.png','Los gastos fijos y las cuentas que alimentan la proyección'),
        ('maqueta-equipo.png','Quién entra y hasta dónde ve: se invita por correo, con puesto y alcance'),
        ('maqueta-flujo.png','Las 52 semanas por delante, semana por semana, con el aviso de cuándo se va a cero')],
   datos=[('Versión','0.1.0'),('Plataforma','Web, sin instalar'),
          ('Estado','En producción, uso interno'),('Alcance','Varios negocios en una cuenta')]),

 'peek101': dict(
   lema='Lo que el cliente pregunta por teléfono, contestado sin llamada.',
   corto='El portal del cliente: su proyecto y su estado de cuenta.',
   estado='En producción', plataforma='Web, sin instalar',
   entrada='Es la ventana que el taller le abre a su cliente para que vea su estado de cuenta: qué le están '
           'fabricando, cuánto lleva pagado, cuánto debe y en qué etapa va cada mueble. Entra con su correo y '
           'un PIN de seis dígitos, y no puede hacer nada más que mirar. Del otro lado no hay trabajo extra: '
           'son los mismos datos que el taller ya captura en dash101.',
   ben=[('Deja de sonar el teléfono','«¿Cómo va lo mío?» y «¿cuánto llevo pagado?» ya tienen respuesta a cualquier hora, sin que nadie del taller conteste.'),
        ('El cliente ve el avance, no promesas','Las siete etapas de fabricación en una barra: del diseño autorizado a la instalación y el cierre.'),
        ('Las cuentas claras','Cada pago recibido, con su fecha y su referencia, y el saldo que queda. No hay discusión sobre lo que se abonó.'),
        ('Enseña lo justo','El cliente ve sus muebles y sus pagos. Nunca ve a qué proveedor se le compró, a cuánto, ni cuánto gana el taller.'),
        ('Entrar es fácil','Correo y seis dígitos. Sin instalar nada, sin registrarse y sin otra contraseña que recordar.')],
   fn=[('Entrar con correo y PIN','seis dígitos, sin instalar nada; si se olvida, se repone por correo'),
       ('Estado de cuenta','total en proceso, total pagado y saldo pendiente de todos sus proyectos juntos'),
       ('Avance del pago','qué parte lleva cubierta, en general y por proyecto'),
       ('Lista por proyecto','cada obra con su monto, lo pagado y lo que resta'),
       ('Los muebles del proyecto','uno por uno: concepto, monto, pagado y la entrega acordada'),
       ('Etapa de fabricación','las siete etapas en una barra: diseño, anticipo, materiales, ensamble, entrega, instalación y cierre'),
       ('Pagos recibidos','fecha, referencia y monto de cada abono'),
       ('Corte al día','la fecha del corte a la vista, para que se sepa a cuándo están los números')],
   no=['No cobra ni recibe pagos en línea.',
       'No sirve para pedir cambios, autorizar diseños ni levantar aclaraciones: es solo de lectura.',
       'No manda avisos cuando algo avanza; el cliente entra a ver.',
       'No enseña facturas: los montos son los del control interno del taller.'],
   img=[('maqueta-estado-de-cuenta.png','Lo que ve el cliente: sus totales y la etapa de cada proyecto'),
        ('maqueta-pagos.png','Sus muebles y cada pago recibido, con fecha y referencia'),
        ('maqueta-proyecto.png','Un proyecto por dentro: monto, saldo y en qué etapa va cada mueble'),
        ('maqueta-entrar.png','Se entra con el correo y un PIN de seis dígitos'),
        ('maqueta-celular.png','En el teléfono del cliente, que es donde se consulta'),
        ('maqueta-lista.png','Sus proyectos, con lo pagado y lo que resta de cada uno')],
   datos=[('Versión','v0 · 7-sep-2026'),('Plataforma','Web, sin instalar'),
          ('Estado','En producción con clientes de prueba'),('Para entrar','Correo y PIN de seis dígitos')]),
}

# Orden en que se enseñan, el mismo que sigue el mueble por el taller.
ORDEN = ['quote101','nest101','draw101','quell101','roster101','dash101','peek101']

# Los siete logotipos van en un solo archivo, marca/logos.svg, y cada página los
# llama con <use>. Antes cada página traía el dibujo completo de cada logotipo
# (la portada, catorce veces): 45 KB de trazos repetidos. El color lo pone el CSS
# (fill), así que el mismo logotipo sale azul sobre claro y claro sobre oscuro.
MEDIDA = {}
simbolos = []
# El de la suite va primero: aro relleno y «101» calado (lo arma armar-logo.py).
for _app, _d in [('suite101', {})] + list(APPS.items()):
    _s = logo(_app, _d.get('vb'), _d.get('color'))
    _vb = re.search(r'viewBox="([^"]*)"', _s).group(1).split()
    MEDIDA[_app] = (_vb[2], _vb[3])
    _dentro = _s[_s.index('>') + 1:_s.rindex('</svg>')].strip()
    simbolos.append(f'<symbol id="{_app}" viewBox="{" ".join(_vb)}">\n{_dentro}\n</symbol>')
(S / 'marca' / 'logos.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg">\n' + '\n'.join(simbolos) + '\n</svg>\n')

def marca(app, pref='', nombre_visible=False):
    w, h = MEDIDA[app]
    rol = f'role="img" aria-label="{app}"' if nombre_visible else 'aria-hidden="true"'
    return f'<svg class="logo" viewBox="0 0 {w} {h}" {rol}><use href="{pref}marca/logos.svg#{app}"/></svg>'

def medida_png(ruta):
    # Ancho y alto del PNG leídos de su cabecera, sin librerías.
    with open(ruta, 'rb') as f:
        cab = f.read(24)
    return int.from_bytes(cab[16:20], 'big'), int.from_bytes(cab[20:24], 'big')

def equipo(app, archivo, alt, pref='', perezosa=True, enciende=False):
    # Las capturas de computadora van montadas en una laptop; las que son más
    # altas que anchas (un expediente completo, por ejemplo) van sueltas y
    # angostas, porque en una laptop quedarían como una tira.
    w, h = medida_png(S / 'img' / app / archivo)
    perez = ' loading="lazy"' if perezosa else ''
    img = f'<img src="{pref}img/{app}/{archivo}" alt="{html.escape(alt)}" width="{w}" height="{h}"{perez}>'
    if w / h < 1.2:
        return f'<div class="suelta" data-mueve>{img}</div>'
    return (f'<div class="laptop{" enciende" if enciende else ""}" data-mueve><div class="pantalla">{img}</div>'
            f'<div class="base"></div></div>')

# El estilo y el movimiento ya no viven aquí dentro: son sitio/estilo.css y
# sitio/movimiento.js, y se editan directamente. Este guion arma el HTML y el
# archivo de logotipos, que es lo que sí se genera. Antes iban como cadenas
# dentro de este archivo, y cualquier retoque de estilo obligaba a mover 56 KB.

def barra(pref=''):
    return f"""<header class="barra"><div class="env">
<a class="marca" href="{pref}index.html" aria-label="Suite 101, inicio">{marca('suite101', pref)}</a>
<nav aria-label="Principal"><a href="{pref}index.html#programas">Programas</a><a href="{pref}index.html#encajan">Cómo encajan</a>
<a href="mailto:{CORREO}">Contacto</a></nav></div></header>"""

def pie(pref=''):
    enlaces = ''.join(f'<li><a href="{pref}app/{a}.html">{a}</a></li>' for a in ORDEN)
    return f"""<footer><div class="env"><div class="cols">
<div><h3>Programas</h3><ul>{enlaces}</ul></div>
<div><h3>Contacto</h3><ul><li><a href="mailto:{CORREO}">{CORREO}</a></li>
<li><a href="mailto:{CORREO}?subject=Demostración">Pedir una demostración</a></li></ul></div></div>
<div class="firma"><span>Taller 101 · Suite 101 · Hecho en el taller, probado en obra</span></div></div></footer>"""

def cabeza(titulo, desc, pref=''):
    return f"""<!doctype html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(titulo)}</title><meta name="description" content="{html.escape(desc)}">
<link rel="stylesheet" href="{pref}estilo.css"><script src="{pref}movimiento.js" defer></script></head><body>"""

def nombre(app, d, etiqueta='div', pref=''):
    # El logotipo es el título; el nombre en texto va oculto para lectores de pantalla.
    return f'<{etiqueta} class="nombre"><span class="vh">{app}</span>{marca(app, pref)}</{etiqueta}>'

def acciones(app, pref=''):
    return (f'<div class="acciones"><a class="btn" href="{pref}app/{app}.html">Más información</a>'
            f'<a class="btn contorno" href="mailto:{CORREO}?subject={app}">Pedir demostración</a></div>')

def mosaico(app, fondo):
    d = APPS[app]
    img = ''
    if d['img']:
        f, c = d['img'][0]
        # La primera laptop de la portada enciende su pantalla al llegar: es el
        # único gesto grande del sitio. Las demás sólo suben y crecen un poco.
        img = f'<div class="asoma">{equipo(app, f, c, enciende=(app == ORDEN[0]))}</div>'
    return (f'<section class="mosaico {fondo}" aria-label="{app}">{nombre(app, d, "h2")}'
            f'<p class="lema">{html.escape(d["lema"])}</p>{acciones(app)}'
            f'<p class="estado">{html.escape(d["estado"])}</p>{img}</section>')

# ------------------------------------------------------------------ portada
# Tres a todo lo ancho —los que tocan el mueble antes de fabricarlo— y los
# otros cuatro de a dos, en damero claro y oscuro, como la portada de Apple.
anchos = [('quote101', ''), ('nest101', 'nube'), ('draw101', 'oscuro')]
de_a_dos = [('quell101', 'nube'), ('roster101', 'oscuro'), ('dash101', 'oscuro'), ('peek101', 'nube')]

pasos = [('quote101','Se cotiza el mueble, componente por componente.'),
         ('nest101','Se despieza: lista de corte y herrajes.'),
         ('draw101','Salen los planos de fabricación.'),
         ('quell101','La obra se sigue sobre el plano, mueble por mueble.'),
         ('roster101','La gente que la hace, con su expediente en regla.'),
         ('dash101','Las cuentas cierran solas.'),
         ('peek101','Y el cliente ve su proyecto y su estado de cuenta.')]
eslabones = [f'<div class="eslabon">{marca(a, nombre_visible=True)}{html.escape(t)}</div>' for a, t in pasos]
cadena = ''.join(eslabones)

portada = cabeza('Suite 101 — programas para taller de muebles',
                 'Siete programas para el taller que ya trabaja: cotización, despiece, planos, obra, personal, cuentas y cliente.', '') + f"""
{barra()}
<main>
<section class="hero">
<div class="env">
<h1>El taller entero, de la cotización a la entrega.</h1>
<p class="baja">Siete programas que se hablan entre ellos. Cada uno funciona por su cuenta; juntos, el dato se captura una vez.</p>
<div class="acciones oscuro"><a class="btn" href="#programas">Ver los programas</a>
<a class="btn contorno" href="mailto:{CORREO}?subject=Demostración">Pedir demostración</a></div>
</div>
<div class="montaje"><img src="img/portada.png" alt="Tres programas de Suite 101 sobre el mismo proyecto: la cotización, el tablero de cuentas y la lista de corte" width="2000" height="1020"></div>
</section>
<div id="programas">
{''.join(mosaico(a, f) for a, f in anchos)}
<div class="pares">{''.join(mosaico(a, f) for a, f in de_a_dos)}</div>
</div>
<section id="encajan" class="encajan"><div class="env">
<h2 class="grande">El mismo mueble recorre los siete programas.</h2>
<p class="baja">Sin volver a capturarse.</p>
<div class="cadena">{cadena}</div>
</div></section>
<section class="cierre"><div class="env">
<h2 class="grande">¿Le sirve a tu taller?</h2>
<p class="baja">Se instala por partes: se empieza por el programa que más duele y los demás entran después.
Escríbenos y te enseñamos el que necesites, con datos de una obra de verdad.</p>
<div class="acciones"><a class="btn" href="mailto:{CORREO}?subject=Demostración">Pedir una demostración</a></div>
</div></section>
</main>
{pie()}</body></html>"""
(S / 'index.html').write_text(portada)

# --------------------------------------------------------- páginas por app
for app, d in APPS.items():
    ven = ''.join(f'<div><b>{html.escape(t)}</b><p>{html.escape(x)}</p></div>' for t, x in d['ben'])
    fn = ''.join(f'<div><b>{html.escape(t)}</b>{html.escape(x)}</div>' for t, x in d['fn'])
    ficha = ''.join(f'<div><span>{html.escape(k)}</span><b>{html.escape(v)}</b></div>' for k, v in d['datos'])
    principal, galeria = '', ''
    if d['img']:
        f0, c0 = d['img'][0]
        principal = (f'<figure class="principal">{equipo(app, f0, c0, "../", perezosa=False, enciende=True)}'
                     f'<figcaption>{html.escape(c0)}</figcaption></figure>')
        # Después de «Por qué sirve» (en nube) los fondos se alternan de uno en
        # uno hasta el cierre, para que nunca queden dos iguales pegados.
        galeria = ''.join(f'<section class="vista{" nube" if i % 2 else ""}"><h2>{html.escape(c)}</h2>'
                          f'{equipo(app, f, "", "../")}</section>'
                          for i, (f, c) in enumerate(d['img'][1:]))
    n_vistas = max(len(d['img']) - 1, 0)
    trae_nube = n_vistas % 2 == 1          # si la última vista quedó en blanco, «Qué trae» va en nube
    cierre_nube = not trae_nube
    # «Qué no hace» sólo donde se decidió decirlo. Vender lo que no existe sale caro.
    nohace = ''
    if d.get('no'):
        puntos = ''.join(f'<div>{html.escape(x)}</div>' for x in d['no'])
        nohace = (f'<div class="nohace"><h3>Qué no hace</h3>'
                  f'<p class="nota">Se dice de una vez, porque vender lo que no existe sale caro.</p>'
                  f'<div class="funciones">{puntos}</div></div>')
    pag = cabeza(f'{app} — Suite 101', d['corto'], '../') + f"""
{barra('../')}
<div class="subbarra"><div class="env">
<a href="{app}.html" aria-label="{app}">{marca(app, '../')}</a>
<a class="btn chica" href="mailto:{CORREO}?subject={app}">Pedir demostración</a>
</div></div>
<main>
<section class="tapa"><div class="env">
{nombre(app, d, pref='../')}
<h1>{html.escape(d['lema'])}</h1>
<div class="acciones"><a class="btn" href="mailto:{CORREO}?subject={app}">Pedir una demostración</a></div>
<p class="estado">{html.escape(d['estado'])} · {html.escape(d['plataforma'])}</p>
</div>{principal}</section>
<section class="intro"><div class="env estrecho"><p>{html.escape(d['entrada'])}</p></div></section>
<section class="bloque nube"><div class="env">
<h2>Por qué sirve</h2><div class="ventajas">{ven}</div>
</div></section>
{galeria}
<section class="bloque{' nube' if trae_nube else ''}"><div class="env">
<h2>Qué trae</h2><div class="funciones">{fn}</div>
<div class="ficha">{ficha}</div>
{nohace}</div></section>
<section class="cierre{' nube' if cierre_nube else ''}"><div class="env">
<h2 class="grande">¿Le sirve a tu taller?</h2>
<p class="baja">Te enseñamos {app} con datos de una obra de verdad.</p>
<div class="acciones"><a class="btn" href="mailto:{CORREO}?subject={app}">Pedir una demostración</a>
<a class="btn contorno" href="../index.html#programas">Ver los siete programas</a></div>
</div></section>
</main>
{pie('../')}</body></html>"""
    (S / 'app' / f'{app}.html').write_text(pag)

print('portada + ', len(APPS), 'páginas')
