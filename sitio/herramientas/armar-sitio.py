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
for _app, _d in APPS.items():
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

CSS = """*{box-sizing:border-box;margin:0;padding:0}
/* Paleta. --azul es el de la marca (logotipos y acentos); --azul-texto es el
   mismo tono un punto más hondo para letra y botones: el #0080C1 da 4.3 de
   contraste sobre blanco y la norma pide 4.5 para texto normal. */
:root{--azul:#0080C1;--azul-texto:#0074ad;--claro:#3AA3DC;--tinta:#122733;--gris:#5b6b76;
  --nube:#f4f7f9;--linea:#dfe6ea;--en-oscuro:#a9c0ce}
@font-face{font-family:"Cifras";src:url(../fuentes/fira-cifras-400.woff2) format("woff2");font-weight:400;
  font-display:swap;unicode-range:U+0030-0039,U+00B0,U+00B1,U+00D7,U+0025}
@font-face{font-family:"Cifras";src:url(../fuentes/fira-cifras-600.woff2) format("woff2");font-weight:600 700;
  font-display:swap;unicode-range:U+0030-0039,U+00B0,U+00B1,U+00D7,U+0025}
@font-face{font-family:"Raleway";src:url(../fuentes/raleway-400.woff2) format("woff2");font-weight:400;font-display:swap}
@font-face{font-family:"Raleway";src:url(../fuentes/raleway-600.woff2) format("woff2");font-weight:600;font-display:swap}
@font-face{font-family:"Raleway";src:url(../fuentes/raleway-700.woff2) format("woff2");font-weight:700;font-display:swap}
@font-face{font-family:"Sansation";src:url(../fuentes/sansation-700.woff2) format("woff2");font-weight:700;font-display:swap}
html{-webkit-text-size-adjust:100%}
@media(prefers-reduced-motion:no-preference){html{scroll-behavior:smooth}}
body{font-family:"Cifras","Raleway",system-ui,sans-serif;font-variant-numeric:tabular-nums;
  font-feature-settings:"tnum";color:var(--tinta);background:#fff;font-size:17px;line-height:1.5;
  -webkit-font-smoothing:antialiased}
/* Ninguna imagen se estira: manda el ancho y la altura sale de su proporción.
   Antes la del montaje traía height="1020" en el HTML y width:100% en el CSS,
   y en el celular se pintaba de 390 × 1020. */
img{display:block;max-width:100%;height:auto}
a{color:inherit}
:focus-visible{outline:2px solid var(--azul-texto);outline-offset:3px;border-radius:6px}
.vh{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
.env{max-width:1024px;margin:0 auto;padding:0 22px}
.estrecho{max-width:760px}

/* Barras: la de la suite y, en cada app, la de la app debajo, como en Apple. */
.barra,.subbarra{position:sticky;z-index:20;background:rgba(255,255,255,.84);
  -webkit-backdrop-filter:saturate(180%) blur(20px);backdrop-filter:saturate(180%) blur(20px);
  border-bottom:1px solid rgba(18,39,51,.09)}
.barra{top:0}
.barra .env,.subbarra .env{display:flex;align-items:center;justify-content:space-between;height:52px}
.marca{font-family:"Cifras","Sansation",sans-serif;font-size:19px;color:var(--azul);text-decoration:none}
.barra nav{display:flex;gap:24px}
.barra nav a{font-size:13px;text-decoration:none;color:rgba(18,39,51,.78)}
.barra nav a:hover{color:var(--azul-texto)}
.subbarra{top:52px;z-index:19}
.subbarra svg{height:24px;width:auto;display:block}
/* Los logotipos salen de marca/logos.svg; el color lo pone esta regla. El azul
   de la marca sobre la tinta da 3.2 de contraste; el claro, 5.5. */
.logo{fill:var(--azul)}
.oscuro .logo{fill:var(--claro)}
.subbarra .chica{font-size:12.5px;padding:5px 13px}

/* Botones: píldora llena para la acción principal, de contorno para la otra. */
.acciones{display:flex;flex-wrap:wrap;gap:12px 14px;justify-content:center;margin-top:24px}
.btn{display:inline-block;padding:11px 22px;border-radius:980px;font-size:16px;font-weight:600;
  text-decoration:none;background:var(--azul-texto);color:#fff;border:1px solid var(--azul-texto)}
.btn:hover{background:#005f8e;border-color:#005f8e}
.btn.contorno{background:transparent;color:var(--azul-texto)}
.btn.contorno:hover{background:var(--azul-texto);color:#fff}
.oscuro .btn.contorno{color:var(--claro);border-color:var(--claro)}
.oscuro .btn.contorno:hover{background:var(--claro);color:var(--tinta)}

/* Portada */
.hero{background:var(--tinta);color:#fff;text-align:center;padding:72px 0 0;overflow:hidden}
.hero h1{font-size:clamp(40px,6.4vw,76px);line-height:1.04;letter-spacing:-.022em;font-weight:700;
  max-width:19ch;margin:0 auto}
.baja{font-size:clamp(19px,2.2vw,25px);line-height:1.35;max-width:34ch;margin:18px auto 0;color:var(--gris)}
.hero .baja,.oscuro .baja{color:var(--en-oscuro)}
.montaje{max-width:1600px;margin:44px auto 0}
/* En el celular el montaje entero queda de 200 px de alto y no se lee nada:
   se recorta al centro, que es donde se enciman las tres pantallas. */
@media(max-width:640px){.montaje img{aspect-ratio:1/1;object-fit:cover;object-position:56% 50%}}

/* Mosaicos: cada programa, a todo lo ancho o de a dos, con su pantalla asomando por abajo. */
.mosaico{text-align:center;padding:48px 3vw 0;overflow:hidden;background:#fff}
.mosaico.nube{background:var(--nube)}
.mosaico.oscuro{background:var(--tinta);color:#fff}
.nombre svg{height:clamp(44px,4.4vw,58px);width:auto;margin:0 auto;display:block}
.lema{font-size:clamp(28px,3.5vw,44px);line-height:1.1;letter-spacing:-.015em;font-weight:700;
  max-width:28ch;margin:14px auto 0}
.estado{font-size:14px;color:var(--gris);margin-top:12px}
.oscuro .estado{color:var(--en-oscuro)}
.asoma{max-width:1180px;margin:34px auto 0;padding-bottom:56px}
.pares{display:grid;grid-template-columns:1fr 1fr;gap:12px;padding:12px;background:#fff}
.pares .mosaico{padding-top:52px}
.pares .nombre svg{height:clamp(36px,3.4vw,44px)}
.pares .lema{font-size:clamp(24px,2.5vw,32px);max-width:19ch}
.pares .asoma{margin-top:30px;padding-bottom:3vw}
.pares .mosaico{padding-left:3vw;padding-right:3vw}
@media(max-width:820px){.pares{grid-template-columns:1fr;padding:12px 0}}
/* La laptop. Hecha con CSS, sin imagen: la tapa con su marco oscuro y la
   cámara, la captura dentro, y la base más ancha que la tapa, como una
   MacBook vista de frente. La captura conserva su proporción. */
.laptop{position:relative;max-width:1180px;margin:0 auto;padding:0 6.5%;
  filter:drop-shadow(0 28px 36px rgba(18,39,51,.20))}
.oscuro .laptop{filter:drop-shadow(0 28px 40px rgba(0,0,0,.45))}
.pantalla{position:relative;background:#0c1116;border-radius:clamp(10px,1.6vw,20px) clamp(10px,1.6vw,20px) 4px 4px;
  padding:clamp(6px,1.4%,16px) clamp(6px,1.4%,16px) clamp(8px,2%,22px);box-shadow:inset 0 0 0 1px #2b3842}
.pantalla::before{content:"";position:absolute;top:clamp(2px,.55%,6px);left:50%;width:clamp(3px,.45%,6px);
  aspect-ratio:1;border-radius:50%;background:#2a3640;transform:translateX(-50%)}
.pantalla img{width:100%;border-radius:3px}
.base{position:relative;height:clamp(8px,1.5vw,20px);margin:0 -6.9%;border-radius:0 0 45% 45%/0 0 100% 100%;
  background:linear-gradient(#e4e8eb,#b7bfc6 60%,#98a1a9)}
.base::before{content:"";position:absolute;top:0;left:50%;width:15%;height:45%;transform:translateX(-50%);
  border-radius:0 0 10px 10px;background:linear-gradient(#aab2b9,#c9cfd4)}
/* Las altas van sueltas: angostas y con esquina redonda. */
.suelta{max-width:520px;margin:0 auto}
.suelta img{border-radius:14px;box-shadow:0 0 0 1px rgba(18,39,51,.07),0 22px 60px rgba(18,39,51,.14)}
/* En el celular la laptop se deja un poco más ancha que la pantalla: la tapa
   se ve entera y sólo se cortan las puntas de la base, así se lee mejor y
   sigue viéndose como laptop. Nunca se estira. */
@media(max-width:640px){.mosaico .laptop,.principal .laptop,.vista .laptop{width:114%;max-width:none;margin-left:-7%}}

/* Movimiento: sólo si movimiento.js corrió (pone .mueve) y el sistema no pide
   menos movimiento. --p va de 0 a 1 mientras la pieza entra a la pantalla. */
@media(prefers-reduced-motion:no-preference){
  .mueve [data-mueve]{transform:translateY(calc((1 - var(--p,1)) * 64px)) scale(calc(.9 + .1 * var(--p,1)));
    opacity:calc(.25 + .75 * var(--p,1));will-change:transform,opacity}
  .mueve .laptop.enciende .pantalla img{opacity:clamp(0,calc((var(--p,1) - .4) * 1.7),1)}
}

/* Cómo encajan: es una secuencia de verdad (el orden en que el mueble pasa por
   el taller), por eso va unida por una línea. */
.encajan{background:var(--nube);text-align:center;padding:80px 0}
.grande{font-size:clamp(32px,4.6vw,56px);line-height:1.06;letter-spacing:-.02em;font-weight:700;
  max-width:17ch;margin:0 auto}
.cadena{display:grid;grid-template-columns:repeat(7,1fr);margin-top:56px;text-align:left}
.eslabon{border-top:2px solid var(--azul);padding:16px 12px 0 0;font-size:14px;color:var(--gris);line-height:1.4}
.eslabon svg{display:block;height:22px;width:auto;margin-bottom:8px}
@media(max-width:820px){.cadena{grid-template-columns:1fr;max-width:420px;margin-left:auto;margin-right:auto}
  .eslabon{border-top:0;border-left:2px solid var(--azul);padding:0 0 22px 18px}}

/* Cierre y pie */
.cierre{text-align:center;padding:80px 0}
.cierre.nube{background:var(--nube)}
.cierre .baja{max-width:40ch}
footer{background:var(--nube);border-top:1px solid var(--linea);font-size:12.5px;color:var(--gris);padding:30px 0 34px}
footer .cols{display:flex;flex-wrap:wrap;gap:22px 64px}
footer h3{font-size:12.5px;font-weight:700;color:var(--tinta);margin-bottom:8px}
footer ul{list-style:none}
footer li{margin:5px 0}
footer a{text-decoration:none}
footer a:hover{text-decoration:underline;color:var(--tinta)}
footer .firma{margin-top:24px;padding-top:14px;border-top:1px solid var(--linea);display:flex;
  flex-wrap:wrap;justify-content:space-between;gap:8px}

/* Página de cada programa */
.tapa{text-align:center;padding:72px 0 0}
.tapa .nombre svg{height:clamp(52px,6vw,72px)}
.tapa h1{font-size:clamp(36px,5.4vw,64px);line-height:1.06;letter-spacing:-.02em;font-weight:700;
  max-width:17ch;margin:20px auto 0}
.principal{max-width:1280px;margin:48px auto 0;padding:0 3vw;overflow:hidden}
.principal figcaption{font-size:14px;color:var(--gris);margin-top:14px}
.intro{padding:64px 0 60px}
.intro p{font-size:clamp(21px,2.3vw,27px);line-height:1.42;font-weight:600;color:var(--tinta)}
.bloque{padding:72px 0}
.bloque.nube{background:var(--nube)}
.bloque h2{font-size:clamp(30px,4vw,48px);line-height:1.08;letter-spacing:-.018em;font-weight:700;text-align:center}
.ventajas{display:grid;grid-template-columns:repeat(3,1fr);gap:40px 36px;margin-top:52px}
.ventajas b{display:block;font-size:20px;line-height:1.25;margin-bottom:8px}
.ventajas p{color:var(--gris);font-size:16px;line-height:1.5}
@media(max-width:900px){.ventajas{grid-template-columns:1fr 1fr}}
@media(max-width:600px){.ventajas{grid-template-columns:1fr;gap:30px}}
/* Una pantalla por sección, grande, con su frase encima: así recorre Apple
   una página de producto. Fondo alterno para que se sienta el paso. */
.vista{text-align:center;padding:56px 3vw 64px;overflow:hidden}
.vista.nube{background:var(--nube)}
.vista h2{font-size:clamp(24px,3vw,38px);line-height:1.15;letter-spacing:-.015em;font-weight:700;max-width:26ch;margin:0 auto}
.vista .laptop,.vista .suelta{margin-top:30px}
.funciones{display:grid;grid-template-columns:repeat(3,1fr);gap:0 36px;margin-top:44px}
.funciones div{border-top:1px solid var(--linea);padding:14px 0 16px;font-size:15px;color:var(--gris);line-height:1.45}
.funciones b{display:block;color:var(--tinta);font-size:16px;margin-bottom:2px}
@media(max-width:900px){.funciones{grid-template-columns:1fr 1fr}}
@media(max-width:600px){.funciones{grid-template-columns:1fr}}
.ficha{display:grid;grid-template-columns:repeat(4,1fr);gap:22px 30px;margin-top:56px;padding-top:26px;
  border-top:1px solid var(--tinta)}
.ficha span{display:block;font-size:13px;color:var(--gris);margin-bottom:4px}
.ficha b{font-size:16px;font-weight:600;line-height:1.35}
@media(max-width:760px){.ficha{grid-template-columns:1fr 1fr}}
.nohace{margin-top:64px}
.nohace h3{font-size:21px}
.nohace p.nota{color:var(--gris);font-size:15px;margin-top:4px}
.nohace .funciones{margin-top:18px;grid-template-columns:repeat(4,1fr)}
@media(max-width:900px){.nohace .funciones{grid-template-columns:1fr 1fr}}
@media(max-width:600px){.nohace .funciones{grid-template-columns:1fr}}
/* En el celular las dos píldoras caben lado a lado, como en Apple. */
@media(max-width:600px){.hero .btn,.mosaico .btn{font-size:15px;padding:9px 16px}.acciones{gap:10px}}
@media(max-width:600px){.hero,.tapa{padding-top:52px}.mosaico{padding-top:48px}
  .intro,.bloque,.encajan,.cierre{padding:64px 0}.barra nav{gap:15px}.barra nav a{font-size:12.5px}}
"""

# Movimiento al bajar, como en apple.com: cada equipo sube y crece un poco al
# entrar a la pantalla, y en la laptop marcada con .enciende se prende la
# pantalla. (Se probó levantar la tapa: de frente, la tapa inclinada se veía
# más grande en vez de cerrada, así que se quitó.) El avance
# va de 0 (asoma por abajo) a 1 (su borde de arriba ya pasó el 70 % de la
# pantalla) y se le pasa al CSS en --p. Si el sistema pide menos movimiento no
# se mueve nada, y sin JavaScript todo se ve quieto y completo.
MOVIMIENTO = """(() => {
  if (!('IntersectionObserver' in window)) return;
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  const piezas = [...document.querySelectorAll('[data-mueve]')];
  if (!piezas.length) return;
  const activas = new Set();
  let pendiente = false;
  const pinta = () => {
    pendiente = false;
    const alto = innerHeight;
    for (const el of activas) {
      const arriba = el.getBoundingClientRect().top;
      const p = Math.min(1, Math.max(0, (alto - arriba) / (alto * 0.45)));
      el.style.setProperty('--p', p.toFixed(3));
    }
  };
  const pide = () => { if (!pendiente) { pendiente = true; requestAnimationFrame(pinta); } };
  const vigia = new IntersectionObserver(entradas => {
    for (const e of entradas) e.isIntersecting ? activas.add(e.target) : activas.delete(e.target);
    pide();
  }, { rootMargin: '25% 0px' });
  piezas.forEach(el => vigia.observe(el));
  document.documentElement.classList.add('mueve');
  addEventListener('scroll', pide, { passive: true });
  addEventListener('resize', pide);
})();
"""

def barra(pref=''):
    return f"""<header class="barra"><div class="env">
<a class="marca" href="{pref}index.html">suite101</a>
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

(S / 'estilo.css').write_text(CSS)
(S / 'movimiento.js').write_text(MOVIMIENTO)
print('portada + ', len(APPS), 'páginas')
