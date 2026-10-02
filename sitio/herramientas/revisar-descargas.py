#!/usr/bin/env python3
# ¿El botón de descarga del sitio apunta a la versión que hay publicada?
#
#     python3 sitio/herramientas/revisar-descargas.py
#
# POR QUÉ EXISTE
#
# El botón lleva la versión en la liga (…/draw101-0.22.2/draw101-0.22.2-setup.exe),
# porque el archivo publicado se llama así. Eso significa que cada entrega nueva
# deja el sitio apuntando a la anterior hasta que alguien lo vuelve a armar. Y la
# liga vieja SIGUE FUNCIONANDO —baja un instalador de verdad—, así que el error no
# se ve: el cliente se lleva una versión atrasada creyendo que es la última.
#
# Mike escogió este camino el 1-oct-2026 sabiendo el riesgo, sobre las otras dos
# opciones (un nombre fijo en el tag «ultima», o una liga propia que reenvíe).
# Esto es lo que vuelve el riesgo RUIDOSO: una orden que lo dice en un segundo.
#
# Se corre después de publicar una entrega, antes de dar por bueno el sitio. Si
# algo no cuadra, la salida dice qué y se arregla volviendo a armar el sitio:
#
#     python3 sitio/herramientas/armar-sitio.py

import json
import pathlib
import re
import signal
import sys

# Sin esto, cortar la salida con `| head` deja un traceback de BrokenPipeError
# que parece que la revisión falló cuando no falló.
signal.signal(signal.SIGPIPE, signal.SIG_DFL)

S = pathlib.Path(__file__).resolve().parent.parent
RAIZ = S.parent

mal = 0
revisadas = 0

for json_app in sorted(RAIZ.glob('*.json')):
    app = json_app.stem
    if app == 'avisos':
        continue
    pagina = S / 'app' / f'{app}.html'
    if not pagina.exists():
        continue

    d = json.loads(json_app.read_text(encoding='utf-8')).get(app)
    if not d or 'windows' not in d:
        continue
    url = d['windows']['url']

    html = pagina.read_text(encoding='utf-8')
    ligas = re.findall(r'href="(https://github\.com/[^"]*/releases/[^"]*)"', html)

    if not ligas:
        # No todas las apps tienen botón de descarga, y eso está bien. Lo que no
        # puede pasar es que tenga uno y apunte a otro lado.
        print(f'  ·  {app}: la página no trae liga de descarga (no se revisa)')
        continue

    revisadas += 1
    for liga in ligas:
        if liga == url:
            print(f'  ok  {app}: la página baja la {d["version"]}, que es la publicada')
        elif '/releases/tag/' in liga:
            mal += 1
            print(f'  MAL {app}: la liga abre la PÁGINA del portal, no baja el archivo')
            print(f'        es:    {liga}')
            print(f'        debe:  {url}')
        else:
            mal += 1
            print(f'  MAL {app}: la página apunta a otra versión que la publicada ({d["version"]})')
            print(f'        es:    {liga}')
            print(f'        debe:  {url}')

if not revisadas:
    print('ninguna página con liga de descarga: no se midió nada')
    sys.exit(1)

print(f'\n{revisadas} página(s) con descarga · {mal} problema(s)')
sys.exit(1 if mal else 0)
