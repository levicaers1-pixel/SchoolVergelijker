#!/usr/bin/env python3
"""Maakt app/preview.html: de pagina plus alle data in één bestand, met een
kleine nabootsing van de dash-runtime. Openen kan zonder server."""
import json, pathlib
A = pathlib.Path(__file__).parent
D = A.parent / 'data'
data = {p.stem: json.loads(p.read_text(encoding='utf8')) for p in D.glob('*.json')}
stub = (A / 'dash-stub.js').read_text(encoding='utf8')
tokens = (A / 'tokens.css').read_text(encoding='utf8')
pagina = (A / 'index.html').read_text(encoding='utf8')
blob = json.dumps(data, ensure_ascii=False).replace('</', '<\\/')
html = f'''<!doctype html><html lang="nl"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Basisscholen Antwerpen (preview)</title><style>{tokens}</style>
<script>window.__DATA__={blob};</script><script>{stub}</script></head>
<body><div id="dash-root">{pagina}</div></body></html>'''
(A / 'preview.html').write_text(html, encoding='utf8')
print('app/preview.html', len(html) // 1024, 'KB')
