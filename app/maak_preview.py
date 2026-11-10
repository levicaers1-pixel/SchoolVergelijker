#!/usr/bin/env python3
"""Maakt de pagina plus alle data in één bestand, met een kleine nabootsing van
de dash-runtime. Openen kan zonder server.

    python3 app/maak_preview.py              # app/preview.html, lokaal bekijken
    python3 app/maak_preview.py --site _site # _site/index.html, voor GitHub Pages
"""
import json, pathlib, sys
A = pathlib.Path(__file__).parent
D = A.parent / 'data'
site = '--site' in sys.argv
data = {p.stem: json.loads(p.read_text(encoding='utf8')) for p in D.glob('*.json')}
stub = (A / 'dash-stub.js').read_text(encoding='utf8')
tokens = (A / 'tokens.css').read_text(encoding='utf8')
pagina = (A / 'index.html').read_text(encoding='utf8')
blob = json.dumps(data, ensure_ascii=False).replace('</', '<\\/')
titel = 'SchoolVergelijker: basisscholen in Antwerpen' if site else 'Basisscholen Antwerpen (preview)'
# Alleen de website krijgt de stratenkaart (MapLibre + OpenFreeMap). De preview blijft zonder netwerk.
MAPLIBRE = 'https://unpkg.com/maplibre-gl@4.7.1/dist/'
webkaart = f'''<link rel="stylesheet" href="{MAPLIBRE}maplibre-gl.css">
<style>{(A / 'webkaart.css').read_text(encoding='utf8')}</style>
<script src="{MAPLIBRE}maplibre-gl.js"></script>
<script>{(A / 'webkaart.js').read_text(encoding='utf8')}</script>''' if site else ''
html = f'''<!doctype html><html lang="nl-BE"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="Zoek je straat en bekijk de basisscholen in de buurt, met wat de onderwijsinspectie erover schreef. Geen ranking of totaalscore.">
<title>{titel}</title><style>{tokens}</style>
<script>window.__DATA__={blob};</script><script>{stub}</script>{webkaart}</head>
<body><div id="dash-root">{pagina}</div></body></html>'''
if site:
    uit = pathlib.Path(sys.argv[sys.argv.index('--site') + 1]) / 'index.html'
    uit.parent.mkdir(parents=True, exist_ok=True)
else:
    uit = A / 'preview.html'
uit.write_text(html, encoding='utf8')
print(uit, len(html) // 1024, 'KB')
