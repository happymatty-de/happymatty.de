#!/usr/bin/env python3
"""Pflege der Kopfzeilen aller Seiten. Aufruf im Hauptordner:  python3 _werkzeuge/stil_version.py

1. Hängt an jeden Verweis auf /stil/basis.css eine Kennung aus dem Inhalt der Datei an
   (z. B. /stil/basis.css?v=3f9a2c1d). Ändert sich basis.css, ändert sich die Kennung, und die
   Browser laden die Gestaltung sofort neu statt aus dem Zwischenspeicher.
2. Ergänzt in jeder Seite die Verweise auf das Symbol (favicon.ico, stil/icon-32.png,
   apple-touch-icon.png), falls sie fehlen, direkt nach dem <title>.

Ordner mit _ veröffentlicht GitHub Pages nicht."""
import hashlib, pathlib, re

wurzel = pathlib.Path(__file__).resolve().parent.parent
kennung = hashlib.sha256((wurzel / 'stil' / 'basis.css').read_bytes()).hexdigest()[:8]
muster = re.compile(r'/stil/basis\.css(\?v=[0-9a-f]+)?')
symbol = ('<link rel="icon" href="/favicon.ico" sizes="any">\n'
          '<link rel="icon" type="image/png" sizes="32x32" href="/stil/icon-32.png">\n'
          '<link rel="apple-touch-icon" href="/apple-touch-icon.png">\n')
geaendert = 0
for datei in wurzel.rglob('*.html'):
    if any(teil.startswith(('.', '_')) for teil in datei.relative_to(wurzel).parts):
        continue
    alt = datei.read_text(encoding='utf-8')
    neu = muster.sub(f'/stil/basis.css?v={kennung}', alt)
    if 'apple-touch-icon' not in neu:
        neu = re.sub(r'</title>\n?', lambda m: '</title>\n' + symbol, neu, count=1)
    if neu != alt:
        datei.write_text(neu, encoding='utf-8')
        geaendert += 1
print(f'Kennung {kennung}, {geaendert} Seiten angepasst')
