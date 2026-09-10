#!/usr/bin/env python3
# Arma las imágenes de nest101, dash101 y peek101 para el escaparate.
#
#     python3 sitio/herramientas/armar-maquetas.py
#
# ESTO NO SON CAPTURAS. Son maquetas: dibujos de la pantalla hechos aquí,
# porque de esas tres aplicaciones no hay captura y no se les puede tomar una
# —el repositorio de nest101 está vacío, y dash101 y peek101 piden cuenta y
# hoy sólo tienen datos de clientes de verdad—. Se pintan con la identidad de
# la suite y con datos inventados.
#
# Sirven para que el escaparate no salga cojo mientras tanto. Se van en cuanto
# haya capturas de verdad: se borran los PNG de sitio/img/<app>/maqueta-*.png,
# se ponen las capturas con su nombre y se corrige la lista de img= en
# armar-sitio.py. La regla de venta/LEEME.md manda: nada de prometer lo que la
# aplicación no hace, y ninguna de estas pantallas enseña una función que no
# esté documentada en la ficha de su aplicación.
#
# Todo lo que se ve es falso: los nombres de clientes, los proyectos, los
# montos y las fechas. Ningún dato real de Taller 101 ni de sus clientes.

import pathlib, base64
from playwright.sync_api import sync_playwright

S = pathlib.Path(__file__).resolve().parent.parent
CHROME = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'
ANCHO, ALTO = 1600, 900


def fuentes():
    """Las fuentes de la casa, incrustadas: el navegador no sale a la red."""
    caras = [('Cifras', 'fira-cifras-400.woff2', 400), ('Cifras', 'fira-cifras-600.woff2', 600),
             ('Raleway', 'raleway-400.woff2', 400), ('Raleway', 'raleway-600.woff2', 600),
             ('Raleway', 'raleway-700.woff2', 700), ('Sansation', 'sansation-700.woff2', 700)]
    fuera = []
    for fam, arch, peso in caras:
        b64 = base64.b64encode((S / 'fuentes' / arch).read_bytes()).decode()
        rango = ('unicode-range:U+0030-0039,U+0024,U+002C,U+002E,U+0025,U+00B0;'
                 if fam == 'Cifras' else '')
        fuera.append(f"@font-face{{font-family:'{fam}';src:url(data:font/woff2;base64,{b64}) "
                     f"format('woff2');font-weight:{peso};{rango}}}")
    return '\n'.join(fuera)


BASE = """
*{box-sizing:border-box;margin:0;padding:0}
:root{--azul:#0080C1;--claro:#3AA3DC;--tinta:#122733;--gris:#5b6b76;--linea:#e3eaee;--fondo:#f4f7f9}
body{width:1600px;height:900px;overflow:hidden;font-family:'Cifras','Raleway',sans-serif;
  font-variant-numeric:tabular-nums;color:var(--tinta);background:#fff;font-size:15px}
.ventana{display:flex;height:900px}
.lado{width:210px;background:var(--tinta);color:#c8d8e2;padding:22px 0;flex:none}
.lado .marca{font-family:'Sansation',sans-serif;font-size:21px;color:#fff;padding:0 22px 24px;letter-spacing:.02em}
.lado a{display:block;padding:11px 22px;color:#9fb6c4;text-decoration:none;font-size:14.5px}
.lado a.hoy{background:var(--azul);color:#fff;font-weight:600}
.cuerpo{flex:1;display:flex;flex-direction:column;min-width:0}
.cinta{height:64px;border-bottom:1px solid var(--linea);display:flex;align-items:center;
  justify-content:space-between;padding:0 30px;flex:none}
.cinta h1{font-size:20px;font-weight:700;letter-spacing:-.01em}
.cinta .quien{font-size:13.5px;color:var(--gris)}
.hoja{padding:26px 30px;overflow:hidden;flex:1;background:var(--fondo);display:flex;flex-direction:column}
.hoja>*{min-height:0}
.btn{background:var(--azul);color:#fff;border-radius:6px;padding:9px 16px;font-size:14px;font-weight:700}
.caja{background:#fff;border:1px solid var(--linea);border-radius:10px}
table{width:100%;border-collapse:collapse;font-size:14px}
th{text-align:left;font-size:11px;letter-spacing:.09em;text-transform:uppercase;color:var(--gris);
  padding:11px 14px;border-bottom:1px solid var(--linea);font-weight:700}
td{padding:11px 14px;border-bottom:1px solid #eef3f6}
td.n,th.n{text-align:right}
tr:last-child td{border-bottom:none}
.tot{font-weight:700;background:#f7fafc}
.pill{display:inline-block;font-size:11.5px;font-weight:700;padding:3px 9px;border-radius:99px}
.ok{background:#e6f4ea;color:#1e7a3c}.va{background:#eaf5fb;color:var(--azul)}.al{background:#fdf0e3;color:#a8621a}
"""


def envoltura(css, cuerpo):
    return (f"<!doctype html><meta charset='utf-8'><style>{fuentes()}{BASE}{css}</style>"
            f"<body>{cuerpo}</body>")


def lado(marca, items, activo):
    enl = ''.join(f"<a class='{'hoy' if t == activo else ''}'>{t}</a>" for t in items)
    return f"<div class='lado'><div class='marca'>{marca}</div>{enl}</div>"


# --------------------------------------------------------------- nest101
def nest_corte():
    filas = [('01','Costado izq.','Melamina blanca 18','720 × 580',2,'Canto 2 mm · 4 lados'),
             ('02','Costado der.','Melamina blanca 18','720 × 580',2,'Canto 2 mm · 4 lados'),
             ('03','Piso','Melamina blanca 18','864 × 580',1,'Canto 2 mm · frente'),
             ('04','Techo','Melamina blanca 18','864 × 580',1,'Canto 2 mm · frente'),
             ('05','Entrepaño','Melamina blanca 18','860 × 560',3,'Canto 2 mm · frente'),
             ('06','Trasera','Fibracel 3','870 × 726',1,'Sin canto'),
             ('07','Frente cajón','Formaica nogal 18','896 × 178',4,'Canto 2 mm · 4 lados'),
             ('08','Zócalo','Melamina blanca 18','864 × 100',1,'Canto 2 mm · frente'),
             ('09','Costado cajonera','Melamina blanca 18','520 × 160',8,'Canto 2 mm · frente'),
             ('10','Fondo cajón','Fibracel 3','836 × 496',4,'Sin canto'),
             ('11','Trasera cajón','Melamina blanca 18','836 × 160',4,'Canto 2 mm · sup.'),
             ('12','Puerta abatible','Formaica nogal 18','446 × 712',2,'Canto 2 mm · 4 lados'),
             ('13','Repisa alacena','Melamina blanca 18','860 × 320',2,'Canto 2 mm · frente'),
             ('14','Costado alacena','Melamina blanca 18','900 × 340',2,'Canto 2 mm · 4 lados'),
             ('15','Tapa nicho TV','Formaica nogal 18','1200 × 380',1,'Canto 2 mm · 4 lados'),
             ('16','Refuerzo trasero','Pino 20 × 40','864 × 40',3,'Sin canto')]
    tr = ''.join(f"<tr><td class='n'>{a}</td><td>{b}</td><td>{c}</td><td class='n'>{d}</td>"
                 f"<td class='n'>{e}</td><td>{f}</td></tr>" for a,b,c,d,e,f in filas)
    css = """
    .rej{display:grid;grid-template-columns:1fr 340px;gap:20px;flex:1;min-height:0}
    .arbol{font-size:14px}.arbol div{padding:7px 10px;border-radius:6px}
    .arbol .sel{background:#eaf5fb;color:var(--azul);font-weight:600}
    .arbol .hijo{padding-left:26px;color:var(--gris)}
    .tit{font-size:12px;letter-spacing:.09em;text-transform:uppercase;color:var(--gris);
      font-weight:700;padding:14px 16px 8px}
    .dato{display:flex;justify-content:space-between;padding:9px 16px;font-size:14px;border-top:1px solid #eef3f6}
    .dato b{font-weight:700}
    """
    cuerpo = f"""
    {lado('nest101', ['Proyectos','Muebles','Lista de corte','Herrajes','Planos','Ajustes'], 'Lista de corte')}
    <div class='cuerpo'>
      <div class='cinta'><h1>Cocina Reyes · Módulo base 900</h1>
        <div><span class='pill va'>16 piezas · 39 cortes</span> &nbsp; <span class='btn'>Exportar a Excel</span></div></div>
      <div class='hoja'><div class='rej'>
        <div class='caja' style='overflow:hidden'>
          <table><thead><tr><th class='n'>#</th><th>Pieza</th><th>Material</th>
            <th class='n'>Medida (mm)</th><th class='n'>Cant.</th><th>Canto</th></tr></thead>
            <tbody>{tr}<tr class='tot'><td></td><td>Total</td><td></td><td></td><td class='n'>39</td><td></td></tr></tbody></table>
        </div>
        <div>
          <div class='caja' style='margin-bottom:16px'>
            <div class='tit'>Muebles del proyecto</div>
            <div class='arbol' style='padding:0 8px 12px'>
              <div class='sel'>Módulo base 900</div>
              <div class='hijo'>Cuerpo · 6 piezas</div>
              <div class='hijo'>Cajonera · 4 piezas</div>
              <div class='hijo'>Zócalo · 1 pieza</div>
              <div>Alacena 900</div><div>Mueble de TV</div>
            </div></div>
          <div class='caja'>
            <div class='tit'>Resumen del despiece</div>
            <div class='dato'><span>Tableros de 18 mm</span><b>3</b></div>
            <div class='dato'><span>Aprovechamiento</span><b>82 %</b></div>
            <div class='dato'><span>Canto de 2 mm</span><b>14.6 m</b></div>
            <div class='dato'><span>Herrajes</span><b>28 piezas</b></div>
            <div class='dato'><span>Archivo</span><b>.t101x</b></div>
          </div></div>
      </div></div></div>"""
    return css, cuerpo


def nest_plano():
    css = """
    .lienzo{background:#fff;border:1px solid var(--linea);border-radius:10px;height:100%;
      position:relative;overflow:hidden}
    .cota{position:absolute;font-size:12px;color:var(--azul);font-weight:600;background:#fff;padding:0 4px}
    """
    # el dibujo: un alzado acotado, en SVG
    svg = """
    <svg viewBox="0 0 1180 600" style="width:100%;height:100%">
      <g stroke="#122733" fill="none" stroke-width="2">
        <rect x="300" y="90" width="520" height="400"/>
        <line x1="300" y1="230" x2="820" y2="230"/>
        <line x1="300" y1="350" x2="820" y2="350"/>
        <rect x="316" y="106" width="488" height="108" fill="#f4f7f9"/>
        <rect x="316" y="246" width="488" height="88" fill="#f4f7f9"/>
        <rect x="316" y="366" width="488" height="108" fill="#f4f7f9"/>
      </g>
      <g stroke="#0080C1" fill="none" stroke-width="1.2">
        <line x1="300" y1="530" x2="820" y2="530"/>
        <line x1="300" y1="500" x2="300" y2="540"/><line x1="820" y1="500" x2="820" y2="540"/>
        <line x1="880" y1="90" x2="880" y2="490"/>
        <line x1="850" y1="90" x2="890" y2="90"/><line x1="850" y1="490" x2="890" y2="490"/>
        <line x1="940" y1="90" x2="940" y2="230"/>
        <line x1="910" y1="90" x2="950" y2="90"/><line x1="910" y1="230" x2="950" y2="230"/>
      </g>
      <g fill="#0080C1" font-family="Cifras,Raleway" font-size="19" font-weight="600">
        <text x="536" y="524" text-anchor="middle">900</text>
        <text x="898" y="296" >720</text>
        <text x="958" y="166" >178</text>
      </g>
      <g fill="#5b6b76" font-family="Raleway" font-size="15">
        <text x="330" y="168">Frente cajón · nogal</text>
        <text x="330" y="298">Entrepaño</text>
        <text x="330" y="428">Puerta abatible</text>
      </g>
      <g stroke="#dfe6ea" stroke-width="1">
        <line x1="60" y1="560" x2="1120" y2="560"/>
      </g>
      <g fill="#5b6b76" font-family="Raleway" font-size="13">
        <text x="60" y="584">Cocina Reyes · Módulo base 900 · Escala 1:10 · Medidas en mm</text>
      </g>
    </svg>"""
    cuerpo = f"""
    {lado('nest101', ['Proyectos','Muebles','Lista de corte','Herrajes','Planos','Ajustes'], 'Planos')}
    <div class='cuerpo'>
      <div class='cinta'><h1>Plano acotado del despiece</h1>
        <div><span class='pill va'>Escala 1:10</span> &nbsp; <span class='btn'>Imprimir a PDF</span></div></div>
      <div class='hoja'><div class='lienzo'>{svg}</div></div></div>"""
    return css, cuerpo


# --------------------------------------------------------------- dash101
def dash_tablero():
    barras = [(52,108),(62,142),(46,98),(78,170),(67,124),(88,186),(57,103),(72,150),(93,206),(77,160),
              (64,118),(98,222),(82,175),(70,134),(103,237),(90,191),(75,155),(108,248),(85,180),(80,165)]
    ancho = 34
    b = ''.join(f"<div class='par'><div class='sal' style='height:{s}px'></div>"
                f"<div class='ent' style='height:{e}px'></div></div>" for s, e in barras)
    filas = [('Cocina Reyes','420,000','310,000','168,000','26 %','ok'),
             ('Clóset Peralta','185,000','185,000','98,400','24 %','ok'),
             ('Oficinas Lomas','960,000','480,000','612,000','12 %','al'),
             ('Recámara Nava','240,000','120,000','88,000','31 %','ok'),
             ('Barra Coyoacán','315,000','94,500','142,000','19 %','va'),
             ('Cocina Santa Fe','680,000','340,000','401,000','22 %','ok'),
             ('Vestidor Del Valle','295,000','295,000','181,000','28 %','ok'),
             ('Mostrador Roma','148,000','44,400','71,000','14 %','al'),
             ('Librero Condesa','210,000','105,000','119,000','23 %','ok'),
             ('Cocina Nápoles','530,000','159,000','248,000','17 %','va')]
    tr = ''.join(f"<tr><td>{a}</td><td class='n'>${b_}</td><td class='n'>${c}</td><td class='n'>${d}</td>"
                 f"<td class='n'><span class='pill {g}'>{e}</span></td></tr>" for a,b_,c,d,e,g in filas)
    css = """
    .kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-bottom:18px}
    .kpi{background:#fff;border:1px solid var(--linea);border-radius:10px;padding:16px 18px}
    .kpi b{display:block;font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--gris);margin-bottom:7px}
    .kpi .v{font-size:27px;font-weight:700;letter-spacing:-.01em}
    .kpi .v.rojo{color:#b3261e}.kpi .v.azul{color:var(--azul)}
    .rej{display:grid;grid-template-columns:1fr 520px;gap:18px;flex:1;min-height:0}
    .graf{background:#fff;border:1px solid var(--linea);border-radius:10px;padding:18px 20px}
    .graf h3{font-size:14px;margin-bottom:4px}
    .graf p{font-size:12.5px;color:var(--gris);margin-bottom:14px}
    .barras{display:flex;align-items:flex-end;gap:7px;height:330px;border-bottom:1px solid var(--linea);padding-bottom:0}
    .par{display:flex;flex-direction:column-reverse;gap:2px;flex:1}
    .ent{background:var(--azul);border-radius:2px 2px 0 0}
    .sal{background:#f0c9c4;border-radius:0 0 2px 2px}
    .ley{display:flex;gap:16px;font-size:12px;color:var(--gris);margin-top:10px}
    .ley i{display:inline-block;width:10px;height:10px;border-radius:2px;margin-right:5px}
    .aviso{margin-top:12px;background:#fdf0e3;color:#a8621a;font-size:13px;padding:9px 12px;border-radius:7px}
    """
    cuerpo = f"""
    {lado('dash101', ['Tablero','Movimientos','Proyectos','Flujo','Gastos fijos','Cuentas','Equipo'], 'Tablero')}
    <div class='cuerpo'>
      <div class='cinta'><h1>Muebles Bravo · Tablero</h1>
        <div class='quien'>Corte al 10 de septiembre · 3 usuarios</div></div>
      <div class='hoja'>
        <div class='kpis'>
          <div class='kpi'><b>En bancos y caja</b><div class='v'>$486,300</div></div>
          <div class='kpi'><b>Por cobrar</b><div class='v azul'>$1,182,500</div></div>
          <div class='kpi'><b>Comprometido</b><div class='v'>$742,900</div></div>
          <div class='kpi'><b>Saldo mínimo previsto</b><div class='v rojo'>−$38,400</div></div>
        </div>
        <div class='rej'>
          <div class='graf'>
            <h3>Flujo a 52 semanas</h3>
            <p>Lo que entra y lo que sale, con los gastos fijos ya contados.</p>
            <div class='barras'>{b}</div>
            <div class='ley'><span><i style='background:#0080C1'></i>Entradas</span>
              <span><i style='background:#f0c9c4'></i>Salidas</span></div>
            <div class='aviso'>El saldo cruza el cero en la semana 18 (26 de enero). Faltan $38,400.</div>
          </div>
          <div class='caja' style='overflow:hidden'>
            <table><thead><tr><th>Proyecto</th><th class='n'>Venta</th><th class='n'>Cobrado</th>
              <th class='n'>Pagado</th><th class='n'>Margen</th></tr></thead><tbody>{tr}</tbody></table>
          </div>
        </div></div></div>"""
    return css, cuerpo


def dash_movimientos():
    filas = [('10 sep','Anticipo Cocina Reyes','Cocina Reyes','Santander','Ingreso','+168,000'),
             ('09 sep','Melamina y cantos','Cocina Reyes','Santander','Egreso','−54,320'),
             ('09 sep','Nómina semana 36','—','Caja','Egreso','−96,800'),
             ('08 sep','Segundo pago Oficinas','Oficinas Lomas','BBVA','Ingreso','+240,000'),
             ('08 sep','Herrajes Hafele','Oficinas Lomas','BBVA','Egreso','−38,150'),
             ('06 sep','Renta del taller','—','Santander','Egreso','−45,000'),
             ('05 sep','Liquidación Clóset Peralta','Clóset Peralta','Santander','Ingreso','+92,500'),
             ('04 sep','Flete a Coyoacán','Barra Coyoacán','Caja','Egreso','−4,800'),
             ('03 sep','Formaica nogal','Barra Coyoacán','BBVA','Egreso','−27,600'),
             ('02 sep','Anticipo Cocina Santa Fe','Cocina Santa Fe','BBVA','Ingreso','+340,000'),
             ('02 sep','Tableros de melamina','Cocina Santa Fe','BBVA','Egreso','−118,400'),
             ('01 sep','Luz y agua del taller','—','Santander','Egreso','−12,300'),
             ('30 ago','Liquidación Vestidor','Vestidor Del Valle','Santander','Ingreso','+147,500'),
             ('29 ago','Nómina semana 34','—','Caja','Egreso','−94,200'),
             ('28 ago','Avance Oficinas Lomas','Oficinas Lomas','BBVA','Ingreso','+142,000'),
             ('27 ago','Herrajes y correderas','Vestidor Del Valle','Caja','Egreso','−31,900'),
             ('26 ago','Barniz y consumibles','—','Caja','Egreso','−8,650')]
    tr = ''
    for f, c, p, cu, t, m in filas:
        color = '#1e7a3c' if m.startswith('+') else '#b3261e'
        tr += (f"<tr><td>{f}</td><td>{c}</td><td>{p}</td><td>{cu}</td>"
               f"<td><span class='pill {'ok' if t=='Ingreso' else 'al'}'>{t}</span></td>"
               f"<td class='n' style='color:{color};font-weight:700'>${m[1:]}</td></tr>")
    css = ".caja{overflow:hidden;flex:1}"
    cuerpo = f"""
    {lado('dash101', ['Tablero','Movimientos','Proyectos','Flujo','Gastos fijos','Cuentas','Equipo'], 'Movimientos')}
    <div class='cuerpo'>
      <div class='cinta'><h1>Movimientos</h1>
        <div><span class='pill va'>Septiembre</span> &nbsp; <span class='btn'>+ Registrar movimiento</span></div></div>
      <div class='hoja'>
        <div class='caja'>
          <table><thead><tr><th>Fecha</th><th>Concepto</th><th>Proyecto</th><th>Cuenta</th>
            <th>Tipo</th><th class='n'>Monto</th></tr></thead><tbody>{tr}</tbody></table>
        </div></div></div>"""
    return css, cuerpo


# --------------------------------------------------------------- peek101
ETAPAS = ['Diseño','Anticipo','Materiales','Ensamble','Entrega','Instalación','Cierre']


def barra_etapas(hecho):
    p = ''
    for i, e in enumerate(ETAPAS):
        cl = 'hecho' if i < hecho else ('hoy' if i == hecho else '')
        p += f"<div class='et {cl}'><span></span><b>{e}</b></div>"
    return f"<div class='etapas'>{p}</div>"


def peek_estado():
    css = """
    .top{display:flex;justify-content:space-between;align-items:center;margin-bottom:20px}
    .kpis{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-bottom:20px}
    .kpi{background:#fff;border:1px solid var(--linea);border-radius:10px;padding:18px 20px}
    .kpi b{display:block;font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--gris);margin-bottom:8px}
    .kpi .v{font-size:30px;font-weight:700;letter-spacing:-.01em}
    .kpi .v.azul{color:var(--azul)}
    .avance{height:9px;background:#e6eef3;border-radius:99px;overflow:hidden;margin-top:14px}
    .avance i{display:block;height:100%;background:var(--azul);border-radius:99px}
    .proy{background:#fff;border:1px solid var(--linea);border-radius:10px;padding:20px 22px;margin-bottom:14px}
    .proy .cab{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:16px}
    .proy h3{font-size:17px}
    .proy .mto{font-size:14px;color:var(--gris)}
    .proy .mto b{color:var(--tinta);font-size:16px}
    .etapas{display:grid;grid-template-columns:repeat(7,1fr);gap:8px}
    .et{text-align:center;font-size:12px;color:#9fb0ba}
    .et span{display:block;height:6px;border-radius:99px;background:#e6eef3;margin-bottom:7px}
    .et.hecho span{background:var(--azul)}.et.hecho b{color:var(--tinta);font-weight:600}
    .et.hoy span{background:var(--claro)}.et.hoy b{color:var(--azul);font-weight:700}
    .abajo{display:grid;grid-template-columns:1fr 1fr;gap:18px;flex:1;min-height:0;margin-top:6px}
    .rot{font-size:12px;letter-spacing:.09em;text-transform:uppercase;color:var(--gris);
      font-weight:700;padding:15px 18px 6px}
    """
    cuerpo = f"""
    <div class='cuerpo' style='width:1600px'>
      <div class='cinta'><h1 style="font-family:'Sansation',sans-serif;color:var(--azul)">peek101</h1>
        <div class='quien'>Sofía Reyes · Corte al 10 de septiembre de 2026</div></div>
      <div class='hoja' style='padding:28px 60px'>
        <div class='kpis'>
          <div class='kpi'><b>En proceso</b><div class='v'>$735,000</div></div>
          <div class='kpi'><b>Pagado</b><div class='v azul'>$478,000</div>
            <div class='avance'><i style='width:65%'></i></div></div>
          <div class='kpi'><b>Saldo pendiente</b><div class='v'>$257,000</div></div>
        </div>
        <div class='proy'>
          <div class='cab'><h3>Cocina integral + Área TV</h3>
            <div class='mto'>Pagado <b>$310,000</b> de <b>$420,000</b></div></div>
          {barra_etapas(4)}
        </div>
        <div class='proy'>
          <div class='cab'><h3>Clóset de recámara principal</h3>
            <div class='mto'>Pagado <b>$168,000</b> de <b>$315,000</b></div></div>
          {barra_etapas(2)}
        </div>
        <div class='abajo'>
          <div class='caja' style='overflow:hidden'>
            <div class='rot'>Sus muebles</div>
            <table><tbody>
              <tr><td>Cocina módulo base izquierdo</td><td><span class='pill ok'>Entregado</span></td><td class='n'>$69,936</td></tr>
              <tr><td>Cocina módulo base derecho</td><td><span class='pill ok'>Entregado</span></td><td class='n'>$28,450</td></tr>
              <tr><td>Alacena despensero</td><td><span class='pill va'>En ensamble</span></td><td class='n'>$42,100</td></tr>
              <tr><td>Mueble de TV con nicho</td><td><span class='pill va'>En materiales</span></td><td class='n'>$31,200</td></tr>
              <tr><td>Clóset · cuerpo principal</td><td><span class='pill va'>En materiales</span></td><td class='n'>$96,400</td></tr>
            </tbody></table>
          </div>
          <div class='caja' style='overflow:hidden'>
            <div class='rot'>Pagos recibidos</div>
            <table><tbody>
              <tr><td>12 ago 2026</td><td>Transferencia · ref. 884120</td><td class='n'>$168,000</td></tr>
              <tr><td>28 ago 2026</td><td>Transferencia · ref. 891455</td><td class='n'>$142,000</td></tr>
              <tr><td>05 sep 2026</td><td>Depósito en ventanilla</td><td class='n'>$98,000</td></tr>
              <tr><td>09 sep 2026</td><td>Transferencia · ref. 903781</td><td class='n'>$70,000</td></tr>
              <tr class='tot'><td colspan='2'>Total pagado</td><td class='n'>$478,000</td></tr>
            </tbody></table>
          </div>
        </div>
      </div></div>"""
    return css, cuerpo


def peek_pagos():
    pagos = [('12 ago 2026','Transferencia · ref. 884120','Anticipo 40 %','168,000'),
             ('28 ago 2026','Transferencia · ref. 891455','Avance de fabricación','142,000'),
             ('05 sep 2026','Depósito en ventanilla','Materiales de clóset','98,000'),
             ('09 sep 2026','Transferencia · ref. 903781','Avance de instalación','70,000')]
    tr = ''.join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td><td class='n' style='font-weight:700'>${d}</td></tr>"
                 for a,b,c,d in pagos)
    muebles = [('Cocina módulo base izquierdo','2 pzas','Entregado','$69,936','ok'),
               ('Cocina módulo base derecho','1 pza','Entregado','$28,450','ok'),
               ('Alacena despensero','1 pza','En ensamble','$42,100','va'),
               ('Mueble de TV con nicho','1 pza','En materiales','$31,200','va')]
    tm = ''.join(f"<tr><td>{a}</td><td>{b}</td><td><span class='pill {e}'>{c}</span></td>"
                 f"<td class='n'>{d}</td></tr>" for a,b,c,d,e in muebles)
    css = """
    .rej{display:grid;grid-template-columns:1fr 1fr;gap:20px}
    .tit{font-size:15px;font-weight:700;padding:16px 18px 0}
    .sub{font-size:12.5px;color:var(--gris);padding:3px 18px 12px}
    """
    cuerpo = f"""
    <div class='cuerpo' style='width:1600px'>
      <div class='cinta'><h1 style="font-family:'Sansation',sans-serif;color:var(--azul)">peek101</h1>
        <div class='quien'>Sofía Reyes · Corte al 10 de septiembre de 2026</div></div>
      <div class='hoja' style='padding:28px 60px'>
        <div class='rej'>
          <div class='caja' style='overflow:hidden'>
            <div class='tit'>Sus muebles</div>
            <div class='sub'>Cocina integral + Área TV</div>
            <table><thead><tr><th>Concepto</th><th>Cant.</th><th>Etapa</th><th class='n'>Monto</th></tr></thead>
              <tbody>{tm}</tbody></table>
          </div>
          <div class='caja' style='overflow:hidden'>
            <div class='tit'>Pagos recibidos</div>
            <div class='sub'>Cuatro abonos · $478,000 en total</div>
            <table><thead><tr><th>Fecha</th><th>Referencia</th><th>Concepto</th><th class='n'>Monto</th></tr></thead>
              <tbody>{tr}<tr class='tot'><td colspan='3'>Total pagado</td><td class='n'>$478,000</td></tr></tbody></table>
          </div>
        </div></div></div>"""
    return css, cuerpo


# --------------------------------------------- pantallas de refuerzo
def nest_herrajes():
    filas = [('Bisagra recta 110°','Blum Clip Top','Módulo base 900',4,'Existencia'),
             ('Corredera oculta 500 mm','Blum Tandem','Cajonera',8,'Pedir'),
             ('Jaladera tubular 160 mm','Nogal cepillado','Frentes',6,'Existencia'),
             ('Patín nivelador 100 mm','Häfele','Zócalo',6,'Existencia'),
             ('Tornillo 4 × 30','Cabeza plana','Cuerpo',120,'Existencia'),
             ('Tarugo 8 × 30','Haya','Cuerpo',48,'Pedir'),
             ('Minifix 15 mm','Häfele','Cuerpo',32,'Existencia'),
             ('Amortiguador de puerta','Blum Blumotion','Puertas',4,'Pedir'),
             ('Perfil LED empotrado','Aluminio 1 m','Alacena',2,'Pedir'),
             ('Tapa cubretornillo','Blanco','Cuerpo',64,'Existencia')]
    tr = ''.join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td><td class='n'>{d}</td>"
                 f"<td><span class='pill {'ok' if e=='Existencia' else 'al'}'>{e}</span></td></tr>"
                 for a,b,c,d,e in filas)
    css = ".caja{overflow:hidden;flex:1}"
    cuerpo = f"""
    {lado('nest101', ['Proyectos','Muebles','Lista de corte','Herrajes','Planos','Ajustes'], 'Herrajes')}
    <div class='cuerpo'>
      <div class='cinta'><h1>Herrajes · Cocina Reyes</h1>
        <div><span class='pill al'>4 por pedir</span> &nbsp; <span class='btn'>Exportar lista</span></div></div>
      <div class='hoja'><div class='caja'>
        <table><thead><tr><th>Herraje</th><th>Marca y modelo</th><th>Mueble</th>
          <th class='n'>Cant.</th><th>Estado</th></tr></thead><tbody>{tr}</tbody></table>
      </div></div></div>"""
    return css, cuerpo


def nest_ficha():
    css = """
    .rej{display:grid;grid-template-columns:1fr 380px;gap:20px;flex:1;min-height:0}
    .hoja2{background:#fff;border:1px solid var(--linea);border-radius:10px;padding:26px 30px;overflow:hidden}
    .hoja2 h2{font-size:22px;margin-bottom:4px}
    .hoja2 .pie{font-size:13px;color:var(--gris);margin-bottom:20px}
    .tit{font-size:12px;letter-spacing:.09em;text-transform:uppercase;color:var(--gris);font-weight:700;padding:14px 16px 8px}
    .dato{display:flex;justify-content:space-between;padding:9px 16px;font-size:14px;border-top:1px solid #eef3f6}
    .dato b{font-weight:700}
    """
    svg = """<svg viewBox="0 0 700 420" style="width:100%;height:auto">
      <g stroke="#122733" fill="none" stroke-width="2">
        <rect x="120" y="40" width="420" height="330"/>
        <line x1="120" y1="150" x2="540" y2="150"/><line x1="120" y1="260" x2="540" y2="260"/>
        <rect x="134" y="54" width="392" height="82" fill="#f4f7f9"/>
        <rect x="134" y="164" width="392" height="82" fill="#f4f7f9"/>
        <rect x="134" y="274" width="392" height="82" fill="#f4f7f9"/></g>
      <g stroke="#0080C1" stroke-width="1.2" fill="none">
        <line x1="120" y1="396" x2="540" y2="396"/>
        <line x1="120" y1="384" x2="120" y2="408"/><line x1="540" y1="384" x2="540" y2="408"/></g>
      <text x="330" y="392" text-anchor="middle" fill="#0080C1"
        font-family="Cifras,Raleway" font-size="17" font-weight="600">900</text></svg>"""
    cuerpo = f"""
    {lado('nest101', ['Proyectos','Muebles','Lista de corte','Herrajes','Planos','Ajustes'], 'Muebles')}
    <div class='cuerpo'>
      <div class='cinta'><h1>Ficha de mueble</h1>
        <div><span class='pill va'>Para el taller</span> &nbsp; <span class='btn'>Imprimir ficha</span></div></div>
      <div class='hoja'><div class='rej'>
        <div class='hoja2'>
          <h2>Módulo base 900 · cajonera</h2>
          <div class='pie'>Cocina Reyes · 900 × 720 × 580 mm · Melamina blanca 18 y formaica nogal</div>
          {svg}
        </div>
        <div>
          <div class='caja' style='margin-bottom:16px'>
            <div class='tit'>Medidas</div>
            <div class='dato'><span>Ancho</span><b>900 mm</b></div>
            <div class='dato'><span>Alto</span><b>720 mm</b></div>
            <div class='dato'><span>Fondo</span><b>580 mm</b></div>
            <div class='dato'><span>Cajones</span><b>4</b></div></div>
          <div class='caja'>
            <div class='tit'>Materiales</div>
            <div class='dato'><span>Cuerpo</span><b>Melamina 18</b></div>
            <div class='dato'><span>Frentes</span><b>Formaica nogal</b></div>
            <div class='dato'><span>Trasera</span><b>Fibracel 3</b></div>
            <div class='dato'><span>Canto</span><b>2 mm</b></div>
            <div class='dato'><span>Piezas</span><b>16</b></div></div>
        </div></div></div></div>"""
    return css, cuerpo


def dash_proyectos():
    filas = [('Cocina Reyes','Sofía Reyes','420,000','310,000','168,000','84,000','26 %','ok'),
             ('Clóset Peralta','Ana Peralta','185,000','185,000','98,400','52,000','24 %','ok'),
             ('Oficinas Lomas','Grupo Lomas','960,000','480,000','612,000','230,000','12 %','al'),
             ('Recámara Nava','Luis Nava','240,000','120,000','88,000','74,000','31 %','ok'),
             ('Barra Coyoacán','Café Aurora','315,000','94,500','142,000','60,000','19 %','va'),
             ('Cocina Santa Fe','Torre Poniente','680,000','340,000','401,000','150,000','22 %','ok'),
             ('Vestidor Del Valle','Marta Ruiz','295,000','295,000','181,000','82,000','28 %','ok'),
             ('Mostrador Roma','Panadería Roma','148,000','44,400','71,000','56,000','14 %','al'),
             ('Librero Condesa','Estudio Condesa','210,000','105,000','119,000','43,000','23 %','ok'),
             ('Cocina Nápoles','Familia Ibarra','530,000','159,000','248,000','198,000','17 %','va')]
    tr = ''.join(f"<tr><td>{a}</td><td>{b}</td><td class='n'>${c}</td><td class='n'>${d}</td>"
                 f"<td class='n'>${e}</td><td class='n'>${f}</td>"
                 f"<td class='n'><span class='pill {h}'>{g}</span></td></tr>"
                 for a,b,c,d,e,f,g,h in filas)
    css = ".caja{overflow:hidden;flex:1}"
    cuerpo = f"""
    {lado('dash101', ['Tablero','Movimientos','Proyectos','Flujo','Gastos fijos','Cuentas','Equipo'], 'Proyectos')}
    <div class='cuerpo'>
      <div class='cinta'><h1>Proyectos</h1>
        <div><span class='pill va'>10 abiertos</span> &nbsp; <span class='btn'>+ Nuevo proyecto</span></div></div>
      <div class='hoja'><div class='caja'>
        <table><thead><tr><th>Proyecto</th><th>Cliente</th><th class='n'>Venta</th><th class='n'>Cobrado</th>
          <th class='n'>Pagado</th><th class='n'>Comprometido</th><th class='n'>Margen</th></tr></thead>
          <tbody>{tr}</tbody></table>
      </div></div></div>"""
    return css, cuerpo


def dash_gastos():
    fijos = [('Renta del taller','Mensual','45,000'),('Nómina de planta','Semanal','96,800'),
             ('Luz y agua','Mensual','12,300'),('Internet y telefonía','Mensual','2,400'),
             ('Contador','Mensual','8,500'),('Seguro del taller','Anual','38,000'),
             ('Mantenimiento de máquinas','Mensual','6,200'),('Camioneta y combustible','Mensual','9,800')]
    tf = ''.join(f"<tr><td>{a}</td><td><span class='pill va'>{b}</span></td>"
                 f"<td class='n' style='font-weight:700'>${c}</td></tr>" for a,b,c in fijos)
    cuentas = [('Santander · 4821','Banco','$312,400'),('BBVA · 7730','Banco','$158,900'),
               ('Caja del taller','Efectivo','$15,000')]
    tc = ''.join(f"<tr><td>{a}</td><td>{b}</td><td class='n' style='font-weight:700'>{c}</td></tr>"
                 for a,b,c in cuentas)
    css = """
    .rej{display:grid;grid-template-columns:1fr 480px;gap:18px;flex:1;min-height:0}
    .tit{font-size:12px;letter-spacing:.09em;text-transform:uppercase;color:var(--gris);font-weight:700;padding:15px 18px 6px}
    """
    cuerpo = f"""
    {lado('dash101', ['Tablero','Movimientos','Proyectos','Flujo','Gastos fijos','Cuentas','Equipo'], 'Gastos fijos')}
    <div class='cuerpo'>
      <div class='cinta'><h1>Gastos fijos y cuentas</h1>
        <div class='quien'>Alimentan la proyección a 52 semanas</div></div>
      <div class='hoja'><div class='rej'>
        <div class='caja' style='overflow:hidden'>
          <div class='tit'>Gastos fijos</div>
          <table><thead><tr><th>Concepto</th><th>Cada</th><th class='n'>Monto</th></tr></thead>
            <tbody>{tf}<tr class='tot'><td colspan='2'>Al mes, aproximado</td><td class='n'>$471,900</td></tr></tbody></table>
        </div>
        <div class='caja' style='overflow:hidden'>
          <div class='tit'>Cuentas</div>
          <table><thead><tr><th>Cuenta</th><th>Tipo</th><th class='n'>Saldo al día</th></tr></thead>
            <tbody>{tc}<tr class='tot'><td colspan='2'>Total disponible</td><td class='n'>$486,300</td></tr></tbody></table>
        </div>
      </div></div></div>"""
    return css, cuerpo


def peek_entrar():
    css = """
    .centro{flex:1;display:flex;align-items:center;justify-content:center;background:var(--tinta)}
    .tarj{background:#fff;border-radius:14px;padding:44px 48px;width:520px;text-align:center}
    .tarj .mk{font-family:'Sansation',sans-serif;font-size:34px;color:var(--azul);margin-bottom:10px}
    .tarj p{font-size:15px;color:var(--gris);margin-bottom:28px}
    .campo{text-align:left;font-size:12px;letter-spacing:.08em;text-transform:uppercase;
      color:var(--gris);font-weight:700;margin-bottom:7px}
    .caj{border:1px solid var(--linea);border-radius:8px;padding:13px 15px;font-size:15px;
      text-align:left;margin-bottom:20px;color:var(--tinta)}
    .pin{display:flex;gap:10px;justify-content:space-between;margin-bottom:26px}
    .pin div{flex:1;border:1px solid var(--linea);border-radius:8px;padding:14px 0;font-size:24px;font-weight:700}
    .pin div.lleno{border-color:var(--azul);color:var(--azul)}
    .accion{background:var(--azul);color:#fff;border-radius:8px;padding:14px;font-weight:700;font-size:15px}
    .nota{font-size:13px;color:var(--gris);margin-top:18px}
    """
    cuerpo = f"""
    <div class='cuerpo' style='width:1600px'>
      <div class='centro'><div class='tarj'>
        <div class='mk'>peek101</div>
        <p>Consulte su proyecto y su estado de cuenta.</p>
        <div class='campo'>Su correo</div>
        <div class='caj'>sofia.reyes@ejemplo.mx</div>
        <div class='campo'>PIN de seis dígitos</div>
        <div class='pin'><div class='lleno'>4</div><div class='lleno'>8</div><div class='lleno'>1</div>
          <div class='lleno'>2</div><div>·</div><div>·</div></div>
        <div class='accion'>Entrar</div>
        <div class='nota'>¿Olvidó su PIN? Se le manda uno nuevo a su correo.</div>
      </div></div></div>"""
    return css, cuerpo


def peek_proyecto():
    css = """
    .cab2{background:#fff;border:1px solid var(--linea);border-radius:10px;padding:22px 24px;margin-bottom:18px}
    .cab2 h2{font-size:21px;margin-bottom:6px}
    .cab2 .l{font-size:14px;color:var(--gris)}
    .cifras{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin:18px 0 0}
    .cifras div b{display:block;font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--gris);margin-bottom:6px}
    .cifras div span{font-size:24px;font-weight:700}
    .etapas{display:grid;grid-template-columns:repeat(7,1fr);gap:8px;margin-top:22px}
    .et{text-align:center;font-size:12px;color:#9fb0ba}
    .et span{display:block;height:6px;border-radius:99px;background:#e6eef3;margin-bottom:7px}
    .et.hecho span{background:var(--azul)}.et.hecho b{color:var(--tinta);font-weight:600}
    .et.hoy span{background:var(--claro)}.et.hoy b{color:var(--azul);font-weight:700}
    .caja{overflow:hidden;flex:1}
    """
    muebles = [('CO-01','Cocina módulo base izquierdo','2 pzas','Entregado','$69,936','ok'),
               ('CO-02','Cocina módulo base derecho','1 pza','Entregado','$28,450','ok'),
               ('CO-03','Alacena despensero','1 pza','En ensamble','$42,100','va'),
               ('MU-TV','Mueble de TV con nicho','1 pza','En materiales','$31,200','va'),
               ('CO-04','Isla con cubierta de cuarzo','1 pza','En ensamble','$118,400','va'),
               ('CO-05','Alacena esquinera','1 pza','Entregado','$36,800','ok'),
               ('CO-06','Cajonera de servicio','2 pzas','En materiales','$44,600','va')]
    tm = ''.join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td><td><span class='pill {f}'>{d}</span></td>"
                 f"<td class='n' style='font-weight:700'>{e}</td></tr>" for a,b,c,d,e,f in muebles)
    cuerpo = f"""
    <div class='cuerpo' style='width:1600px'>
      <div class='cinta'><h1 style="font-family:'Sansation',sans-serif;color:var(--azul)">peek101</h1>
        <div class='quien'>Sofía Reyes · Corte al 10 de septiembre de 2026</div></div>
      <div class='hoja' style='padding:26px 60px'>
        <div class='cab2'>
          <h2>Cocina integral + Área TV</h2>
          <div class='l'>Entrega acordada: 30 de octubre de 2026</div>
          <div class='cifras'>
            <div><b>Monto del proyecto</b><span>$420,000</span></div>
            <div><b>Pagado</b><span style='color:var(--azul)'>$310,000</span></div>
            <div><b>Saldo</b><span>$110,000</span></div></div>
          {barra_etapas(4)}
        </div>
        <div class='caja'>
          <table><thead><tr><th>Clave</th><th>Concepto</th><th>Cant.</th><th>Etapa</th>
            <th class='n'>Monto</th></tr></thead><tbody>{tm}</tbody></table>
        </div></div></div>"""
    return css, cuerpo


def nest_proyectos():
    filas = [('Cocina Reyes','Sofía Reyes','6 muebles',39,'En corte','va'),
             ('Clóset Peralta','Ana Peralta','3 muebles',22,'Cortado','ok'),
             ('Oficinas Lomas','Grupo Lomas','18 muebles',146,'En corte','va'),
             ('Recámara Nava','Luis Nava','4 muebles',31,'Cortado','ok'),
             ('Barra Coyoacán','Café Aurora','2 muebles',14,'Por despiezar','al'),
             ('Cocina Santa Fe','Torre Poniente','9 muebles',78,'En corte','va'),
             ('Vestidor Del Valle','Marta Ruiz','5 muebles',44,'Cortado','ok'),
             ('Mostrador Roma','Panadería Roma','3 muebles',19,'Por despiezar','al'),
             ('Librero Condesa','Estudio Condesa','2 muebles',16,'Cortado','ok')]
    tr = ''.join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td><td class='n'>{d}</td>"
                 f"<td><span class='pill {f}'>{e}</span></td></tr>" for a,b,c,d,e,f in filas)
    css = ".caja{overflow:hidden;flex:1}"
    cuerpo = f"""
    {lado('nest101', ['Proyectos','Muebles','Lista de corte','Herrajes','Planos','Ajustes'], 'Proyectos')}
    <div class='cuerpo'>
      <div class='cinta'><h1>Proyectos</h1>
        <div><span class='pill va'>9 abiertos</span> &nbsp; <span class='btn'>+ Nuevo proyecto</span></div></div>
      <div class='hoja'><div class='caja'>
        <table><thead><tr><th>Proyecto</th><th>Cliente</th><th>Contenido</th>
          <th class='n'>Piezas</th><th>Estado</th></tr></thead><tbody>{tr}</tbody></table>
      </div></div></div>"""
    return css, cuerpo


def dash_equipo():
    gente = [('Mike Balcázar','mike@ejemplo.mx','Dueño','Todo','ok'),
             ('Laura Méndez','laura@ejemplo.mx','Oficina','Todos los proyectos','ok'),
             ('Jorge Rangel','jorge@ejemplo.mx','Producción','Cocina Reyes · Oficinas Lomas','va'),
             ('Paty Solís','paty@ejemplo.mx','Oficina','Cocina Santa Fe','va'),
             ('Invitación enviada','carlos@ejemplo.mx','Producción','Barra Coyoacán','al')]
    tr = ''.join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td>"
                 f"<td><span class='pill {f}'>{'Activo' if f!='al' else 'Pendiente'}</span></td></tr>"
                 for a,b,c,d,f in gente)
    css = """
    .caja{overflow:hidden}
    .aviso{background:#eaf5fb;color:var(--azul);font-size:13.5px;padding:12px 16px;
      border-radius:8px;margin-top:16px}
    """
    cuerpo = f"""
    {lado('dash101', ['Tablero','Movimientos','Proyectos','Flujo','Gastos fijos','Cuentas','Equipo'], 'Equipo')}
    <div class='cuerpo'>
      <div class='cinta'><h1>Equipo · Muebles Bravo</h1>
        <div><span class='btn'>Invitar por correo</span></div></div>
      <div class='hoja'>
        <div class='caja'>
          <table><thead><tr><th>Quién</th><th>Correo</th><th>Puesto</th><th>Alcance</th>
            <th>Estado</th></tr></thead><tbody>{tr}</tbody></table></div>
        <div class='aviso'>Quien lleva un proyecto ve ese proyecto. Los márgenes de los demás no le aparecen.</div>
      </div></div>"""
    return css, cuerpo


def peek_celular():
    css = """
    .centro{flex:1;display:flex;align-items:center;justify-content:center;background:var(--tinta);gap:60px}
    .tel{width:390px;height:780px;background:#fff;border-radius:34px;overflow:hidden;
      border:9px solid #0a1a24;display:flex;flex-direction:column}
    .tel .cab{padding:20px 22px 14px;border-bottom:1px solid var(--linea)}
    .tel .mk{font-family:'Sansation',sans-serif;font-size:22px;color:var(--azul)}
    .tel .qn{font-size:12.5px;color:var(--gris);margin-top:3px}
    .tel .in{padding:18px 22px;overflow:hidden}
    .tarj{border:1px solid var(--linea);border-radius:10px;padding:14px 16px;margin-bottom:12px}
    .tarj b{display:block;font-size:11px;letter-spacing:.09em;text-transform:uppercase;
      color:var(--gris);margin-bottom:5px}
    .tarj .v{font-size:25px;font-weight:700}
    .tarj .v.azul{color:var(--azul)}
    .barra{height:8px;background:#e6eef3;border-radius:99px;margin-top:11px;overflow:hidden}
    .barra i{display:block;height:100%;background:var(--azul)}
    .pr{border:1px solid var(--linea);border-radius:10px;padding:13px 15px;margin-bottom:11px}
    .pr h4{font-size:14.5px;margin-bottom:9px}
    .pasos{display:flex;gap:4px}
    .pasos span{flex:1;height:5px;border-radius:99px;background:#e6eef3}
    .pasos span.on{background:var(--azul)}
    .pr .l{font-size:12px;color:var(--gris);margin-top:8px}
    .dice{color:#eaf2f7;max-width:430px}
    .dice h2{font-size:34px;line-height:1.15;font-weight:700;letter-spacing:-.015em;margin-bottom:16px}
    .dice p{font-size:16.5px;color:#a9c0ce;line-height:1.55}
    """
    cuerpo = f"""
    <div class='cuerpo' style='width:1600px'>
      <div class='centro'>
        <div class='dice'>
          <h2>El cliente lo abre en su teléfono.</h2>
          <p>Sin instalar nada y sin registrarse: su correo, seis dígitos y ve lo suyo.
             Cuánto lleva pagado, cuánto debe y en qué etapa va cada mueble.</p>
        </div>
        <div class='tel'>
          <div class='cab'><div class='mk'>peek101</div>
            <div class='qn'>Sofía Reyes · corte al 10 de septiembre</div></div>
          <div class='in'>
            <div class='tarj'><b>Saldo pendiente</b><div class='v'>$257,000</div></div>
            <div class='tarj'><b>Pagado</b><div class='v azul'>$478,000</div>
              <div class='barra'><i style='width:65%'></i></div></div>
            <div class='pr'><h4>Cocina integral + Área TV</h4>
              <div class='pasos'><span class='on'></span><span class='on'></span><span class='on'></span>
                <span class='on'></span><span class='on'></span><span></span><span></span></div>
              <div class='l'>En entrega · pagado $310,000 de $420,000</div></div>
            <div class='pr'><h4>Clóset de recámara principal</h4>
              <div class='pasos'><span class='on'></span><span class='on'></span><span class='on'></span>
                <span></span><span></span><span></span><span></span></div>
              <div class='l'>En materiales · pagado $168,000 de $315,000</div></div>
          </div></div>
      </div></div>"""
    return css, cuerpo


def dash_flujo():
    sem = [('Sem 37','12 sep','486,300','168,000','−142,900','511,400'),
           ('Sem 38','19 sep','511,400','0','−96,800','414,600'),
           ('Sem 39','26 sep','414,600','240,000','−188,300','466,300'),
           ('Sem 40','03 oct','466,300','0','−96,800','369,500'),
           ('Sem 41','10 oct','369,500','94,500','−151,200','312,800'),
           ('Sem 42','17 oct','312,800','0','−96,800','216,000'),
           ('Sem 43','24 oct','216,000','120,000','−174,600','161,400'),
           ('Sem 44','31 oct','161,400','0','−141,800','19,600'),
           ('Sem 45','07 nov','19,600','0','−96,800','−77,200')]
    tr = ''
    for a,b,c,d,e,f in sem:
        rojo = f.startswith('−')
        tr += (f"<tr><td>{a}</td><td>{b}</td><td class='n'>${c}</td>"
               f"<td class='n' style='color:#1e7a3c'>{'$'+d if d!='0' else '—'}</td>"
               f"<td class='n' style='color:#b3261e'>${e[1:]}</td>"
               f"<td class='n' style='font-weight:700;color:{'#b3261e' if rojo else 'inherit'}'>"
               f"{'−$'+f[1:] if rojo else '$'+f}</td></tr>")
    barras = ''.join(f"<div class='par'><div class='sal' style='height:{x}px'></div>"
                     f"<div class='ent' style='height:{y}px'></div></div>"
                     for x, y in [(58,120),(70,158),(52,108),(88,188),(75,138),(98,206),
                                  (64,114),(80,166),(104,228),(86,178),(72,130),(110,246)])
    css = """
    .graf{background:#fff;border:1px solid var(--linea);border-radius:10px;padding:18px 22px;margin-bottom:16px}
    .graf h3{font-size:15px;margin-bottom:3px}
    .graf p{font-size:12.5px;color:var(--gris);margin-bottom:14px}
    .barras{display:flex;align-items:flex-end;gap:12px;height:250px;border-bottom:1px solid var(--linea)}
    .par{display:flex;flex-direction:column-reverse;gap:2px;flex:1}
    .ent{background:var(--azul);border-radius:2px 2px 0 0}
    .sal{background:#f0c9c4;border-radius:0 0 2px 2px}
    .aviso{background:#fdf0e3;color:#a8621a;font-size:13.5px;padding:10px 14px;border-radius:7px;margin-top:12px}
    .caja{overflow:hidden;flex:1}
    """
    cuerpo = f"""
    {lado('dash101', ['Tablero','Movimientos','Proyectos','Flujo','Gastos fijos','Cuentas','Equipo'], 'Flujo')}
    <div class='cuerpo'>
      <div class='cinta'><h1>Flujo a 52 semanas</h1>
        <div class='quien'>Con los gastos fijos y lo comprometido ya contados</div></div>
      <div class='hoja'>
        <div class='graf'><h3>Lo que entra y lo que sale</h3>
          <p>Primeras doce semanas.</p>
          <div class='barras'>{barras}</div>
          <div class='aviso'>El saldo cruza el cero en la semana 45 (7 de noviembre). Faltan $77,200.</div></div>
        <div class='caja'>
          <table><thead><tr><th>Semana</th><th>Inicia</th><th class='n'>Saldo inicial</th>
            <th class='n'>Entradas</th><th class='n'>Salidas</th><th class='n'>Saldo final</th></tr></thead>
            <tbody>{tr}</tbody></table></div>
      </div></div>"""
    return css, cuerpo


def peek_lista():
    proy = [('Cocina integral + Área TV','30 oct 2026','420,000','310,000','110,000','74%'),
            ('Clóset de recámara principal','22 nov 2026','315,000','168,000','147,000','53%')]
    filas = ''
    for a,b,c,d,e,f in proy:
        filas += f"""
        <div class='pr'>
          <div class='cab'><h3>{a}</h3><span class='ent'>Entrega acordada: {b}</span></div>
          <div class='nums'>
            <div><b>Monto</b><span>${c}</span></div>
            <div><b>Pagado</b><span class='azul'>${d}</span></div>
            <div><b>Saldo</b><span>${e}</span></div>
            <div><b>Va cubierto</b><span class='azul'>{f}</span></div></div>
          <div class='barra'><i style='width:{f}'></i></div>
        </div>"""
    css = """
    .pr{background:#fff;border:1px solid var(--linea);border-radius:10px;padding:24px 26px;margin-bottom:18px}
    .pr .cab{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:18px}
    .pr h3{font-size:19px}
    .pr .ent{font-size:13.5px;color:var(--gris)}
    .nums{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}
    .nums b{display:block;font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--gris);margin-bottom:6px}
    .nums span{font-size:25px;font-weight:700}
    .nums .azul{color:var(--azul)}
    .barra{height:9px;background:#e6eef3;border-radius:99px;overflow:hidden;margin-top:18px}
    .barra i{display:block;height:100%;background:var(--azul);border-radius:99px}
    .cierre{background:#fff;border:1px solid var(--linea);border-radius:10px;padding:22px 26px;
      display:flex;justify-content:space-between;align-items:center}
    .cierre .t{font-size:14px;color:var(--gris)}
    .cierre .g{font-size:27px;font-weight:700}
    """
    cuerpo = f"""
    <div class='cuerpo' style='width:1600px'>
      <div class='cinta'><h1 style="font-family:'Sansation',sans-serif;color:var(--azul)">peek101</h1>
        <div class='quien'>Sofía Reyes · Corte al 10 de septiembre de 2026</div></div>
      <div class='hoja' style='padding:28px 60px'>
        {filas}
        <div class='cierre'>
          <div class='t'>Dos proyectos abiertos · saldo pendiente en total</div>
          <div class='g'>$257,000</div></div>
      </div></div>"""
    return css, cuerpo


MAQUETAS = {
 'nest101': [('maqueta-lista-de-corte.png', nest_corte), ('maqueta-plano-acotado.png', nest_plano),
             ('maqueta-herrajes.png', nest_herrajes), ('maqueta-ficha-mueble.png', nest_ficha), ('maqueta-proyectos.png', nest_proyectos)],
 'dash101': [('maqueta-tablero.png', dash_tablero), ('maqueta-movimientos.png', dash_movimientos),
             ('maqueta-proyectos.png', dash_proyectos), ('maqueta-gastos-fijos.png', dash_gastos), ('maqueta-equipo.png', dash_equipo), ('maqueta-flujo.png', dash_flujo)],
 'peek101': [('maqueta-estado-de-cuenta.png', peek_estado), ('maqueta-pagos.png', peek_pagos),
             ('maqueta-proyecto.png', peek_proyecto), ('maqueta-entrar.png', peek_entrar), ('maqueta-celular.png', peek_celular), ('maqueta-lista.png', peek_lista)],
}


def main():
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=CHROME, args=['--no-sandbox'])
        pg = b.new_page(viewport={'width': ANCHO, 'height': ALTO}, device_scale_factor=1)
        for app, pantallas in MAQUETAS.items():
            destino = S / 'img' / app
            destino.mkdir(parents=True, exist_ok=True)
            for nombre, hacer in pantallas:
                css, cuerpo = hacer()
                envuelto = envoltura(css, f"<div class='ventana'>{cuerpo}</div>")
                pg.set_content(envuelto, wait_until='load')
                pg.wait_for_timeout(250)
                pg.screenshot(path=str(destino / nombre))
                print(f"img/{app}/{nombre}")
        b.close()


if __name__ == '__main__':
    main()


# ------------------------------------------------------- portada del sitio
# Un montaje con tres pantallas, para que la portada abra con imagen y no con
# texto. Se arma con PIL a partir de los PNG que ya están en sitio/img/.
def portada():
    from PIL import Image, ImageDraw, ImageFilter
    W, H = 2000, 1020
    fondo = Image.new('RGB', (W, H), '#122733')
    piezas = [('quote101/02-cotizacion.png', 40, 250, 1000),
              ('dash101/maqueta-tablero.png', 470, 130, 1180),
              ('nest101/maqueta-lista-de-corte.png', 1010, 400, 940)]
    for arch, x, y, ancho in piezas:
        im = Image.open(S / 'img' / arch).convert('RGB')
        alto = round(im.height * ancho / im.width)
        im = im.resize((ancho, alto), Image.LANCZOS)
        # esquinas redondeadas
        mascara = Image.new('L', (ancho, alto), 0)
        ImageDraw.Draw(mascara).rounded_rectangle([0, 0, ancho - 1, alto - 1], 14, fill=255)
        # sombra, para que se despeguen del fondo
        sombra = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(sombra).rounded_rectangle([x + 6, y + 14, x + ancho + 6, y + alto + 14],
                                                 14, fill=(0, 0, 0, 150))
        fondo = Image.alpha_composite(fondo.convert('RGBA'),
                                      sombra.filter(ImageFilter.GaussianBlur(18))).convert('RGB')
        fondo.paste(im, (x, y), mascara)
    destino = S / 'img' / 'portada.png'
    fondo.save(destino, optimize=True)
    print('img/portada.png', fondo.size)
