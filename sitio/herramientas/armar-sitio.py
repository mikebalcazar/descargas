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
   vb='83.84 198.74 455 215',
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
        ('04-expediente-completo.png','El expediente completo, listo para el contador')],
   datos=[('Versión','portal 0.10.0 · central 0.4.0'),('Plataforma','Web · celular y computadora'),
          ('Estado','En producción con el primer cliente'),('Modelo','Renta mensual por empresa')]),

 'quell101': dict(
   vb='118 198 418 216', color='#0381c2',
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
   vb='-16 -12 980 465',
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
        ('02-propiedades-en-vivo.png','Las propiedades del objeto, al momento')],
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
   img=[],
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
   img=[],
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
   img=[],
   datos=[('Versión','v0 · 7-sep-2026'),('Plataforma','Web, sin instalar'),
          ('Estado','En producción con clientes de prueba'),('Para entrar','Correo y PIN de seis dígitos')]),
}

# Orden en que se enseñan, el mismo que sigue el mueble por el taller.
ORDEN = ['quote101','nest101','draw101','quell101','roster101','dash101','peek101']

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
.flujo{display:grid;grid-template-columns:repeat(auto-fit,minmax(128px,1fr));gap:14px;margin-top:8px}
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
for app in ORDEN:
    d = APPS[app]
    tarjetas.append(f"""<a class="tarjeta" href="app/{app}.html">{logo(app, d.get('vb'), d.get('color'))}
<p>{html.escape(d['corto'])}</p><span class="sello">{html.escape(d['estado'])}</span></a>""")

pasos = [('quote101','Se cotiza el mueble, componente por componente.'),
         ('nest101','Se despieza: lista de corte y herrajes.'),
         ('draw101','Salen los planos de fabricación.'),
         ('quell101','La obra se sigue sobre el plano, mueble por mueble.'),
         ('roster101','La gente que la hace, con su expediente en regla.'),
         ('dash101','Las cuentas cierran solas.'),
         ('peek101','Y el cliente ve su proyecto y su estado de cuenta.')]

portada = cabeza('Suite 101 — programas para taller de muebles',
                 'Siete programas para el taller que ya trabaja: cotización, despiece, planos, obra, personal, cuentas y cliente.') + f"""
{barra()}
<div class="hero"><div class="env">
<h1>El taller entero, de la cotización a la entrega.</h1>
<p>Suite 101 son <span class="cifra">siete</span> programas que se hablan entre ellos: cotizas, despiezas, dibujas,
sigues la obra, llevas al personal, cierras las cuentas y le enseñas al cliente su proyecto. Cada uno funciona por su cuenta; juntos, el dato se captura
<span class="cifra">una</span> vez.</p>
<a class="btn" href="#apps">Ver los programas</a>
<a class="btn fantasma" href="mailto:{CORREO}">Pedir una demostración</a>
</div></div>

<section id="apps"><div class="env">
<h2>Los programas</h2>
<p class="sub">Hechos en un taller que fabrica todos los días, no en un escritorio. Lo que nadie usaba, no se quedó.</p>
<div class="rejilla">{''.join(tarjetas)}</div>
</div></section>

<section id="flujo" class="cierre"><div class="env">
<h2>Cómo encajan</h2>
<p class="sub">El mismo mueble recorre los siete programas sin volver a capturarse.</p>
<div class="flujo">{''.join(f'<div class="paso"><b>{a}</b>{html.escape(t)}</div>' for a, t in pasos)}</div>
</div></section>

<section><div class="env">
<h2>¿Le sirve a tu taller?</h2>
<p class="sub">Se instala por partes: se empieza por el programa que más duele y los demás entran después.
Escríbenos y te enseñamos el que necesites, con datos de una obra de verdad.</p>
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
    # Sin capturas no se deja la sección vacía: se salta y ya.
    vista = f'<section><div class="env">{figs}</div></section>\n' if figs else ''
    # «Qué no hace» sólo donde se decidió decirlo. Vender lo que no existe sale caro.
    nohace = ''
    if d.get('no'):
        puntos = ''.join(f'<div>{html.escape(x)}</div>' for x in d['no'])
        nohace = (f'<section><div class="env"><h2>Qué no hace</h2>'
                  f'<p class="sub">Se dice de una vez, porque vender lo que no existe sale caro.</p>'
                  f'<div class="dos fn">{puntos}</div></div></section>\n')
    pag = cabeza(f'{app} — Suite 101', d['corto'], css='../estilo.css') + f"""
{barra('../')}
<div class="tapa"><div class="env">
{logo(app, d.get('vb'), d.get('color'))}
<div class="lema">{html.escape(d['lema'])}</div>
<p class="entrada">{html.escape(d['entrada'])}</p>
<a class="btn" href="mailto:{CORREO}?subject={app}">Pedir una demostración</a>
</div></div>

{vista}
<section class="cierre"><div class="env">
<h2>Por qué sirve</h2><div class="dos ben">{ben}</div>
</div></section>

<section><div class="env">
<h2>Qué trae</h2><div class="dos fn">{fn}</div>
<div style="height:36px"></div>
<div class="datos">{dat}</div>
</div></section>
{nohace}{pie()}</body></html>"""
    (S / 'app' / f'{app}.html').write_text(pag)

(S / 'estilo.css').write_text(CSS)
print('portada + ', len(APPS), 'páginas')
