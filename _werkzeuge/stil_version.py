#!/usr/bin/env python3
"""Pflege der Kopfzeilen aller Seiten. Aufruf im Hauptordner:  python3 _werkzeuge/stil_version.py

1. Hängt an jeden Verweis auf /stil/basis.css eine Kennung aus dem Inhalt der Datei an
   (z. B. /stil/basis.css?v=3f9a2c1d). Ändert sich basis.css, ändert sich die Kennung, und die
   Browser laden die Gestaltung sofort neu statt aus dem Zwischenspeicher.
2. Ergänzt in jeder Seite die Verweise auf das Symbol (favicon.ico, stil/icon-32.png,
   apple-touch-icon.png), falls sie fehlen, direkt nach dem <title>.
3. Hängt an diese Verweise im Kopf der Seite ebenso eine Kennung aus dem Inhalt der Bilddatei an
   (z. B. /favicon.ico?v=1a2b3c4d). Ändert sich das Symbol, ändert sich die Adresse, und die
   Browser holen es neu, statt das alte aus ihrem Symbolspeicher zu zeigen (Anlass 11.11.2026:
   Safari auf dem iPad zeigte nach dem Wechsel zum Smiley weiter das alte „hm“).

Ordner mit _ veröffentlicht GitHub Pages nicht."""
import hashlib, pathlib, re

wurzel = pathlib.Path(__file__).resolve().parent.parent
kennung = hashlib.sha256((wurzel / 'stil' / 'basis.css').read_bytes()).hexdigest()[:8]
muster = re.compile(r'/stil/basis\.css(\?v=[0-9a-f]+)?')
symbol = ('<link rel="icon" href="/favicon.ico" sizes="any">\n'
          '<link rel="icon" type="image/png" sizes="32x32" href="/stil/icon-32.png">\n'
          '<link rel="apple-touch-icon" href="/apple-touch-icon.png">\n')
# Verweise auf das Symbol im Kopf der Seite (nur <link …>, nicht das Logo-Bild im Text)
bilder = ('favicon.ico', 'stil/icon-32.png', 'apple-touch-icon.png')
bildkennung = {b: hashlib.sha256((wurzel / b).read_bytes()).hexdigest()[:8] for b in bilder}
bildmuster = re.compile(r'(<link\b[^>]*\bhref="/)(' + '|'.join(re.escape(b) for b in bilder)
                        + r')(?:\?v=[0-9a-f]+)?(")')
geaendert = 0
for datei in wurzel.rglob('*.html'):
    if any(teil.startswith(('.', '_')) for teil in datei.relative_to(wurzel).parts):
        continue
    alt = datei.read_text(encoding='utf-8')
    neu = muster.sub(f'/stil/basis.css?v={kennung}', alt)
    if 'apple-touch-icon' not in neu:
        neu = re.sub(r'</title>\n?', lambda m: '</title>\n' + symbol, neu, count=1)
    neu = bildmuster.sub(lambda m: f'{m.group(1)}{m.group(2)}?v={bildkennung[m.group(2)]}{m.group(3)}', neu)
    if neu != alt:
        datei.write_text(neu, encoding='utf-8')
        geaendert += 1
print(f'Kennung {kennung}, {geaendert} Seiten angepasst')
