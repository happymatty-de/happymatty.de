#!/usr/bin/env python3
"""Trägt den Seitentitel in ein PDF ein, damit Browser und Lesezeichen ihn statt des
Dateinamens zeigen. Inhalt und Aussehen bleiben unverändert.

Braucht pikepdf (einmal je Sitzung: pip install pikepdf).
Aufruf:  python3 _werkzeuge/pdf_titel.py <datei.pdf> "<Titel>"
Beispiel: python3 _werkzeuge/pdf_titel.py lineare-funktionen/mehr-als-nur-steil/aufgabenblatt.pdf "happymatty/Mehr als nur steil/Arbeitsblatt"
"""
import sys, pikepdf

datei, titel = sys.argv[1], sys.argv[2]
with pikepdf.open(datei, allow_overwriting_input=True) as pdf:
    with pdf.open_metadata(set_pikepdf_as_editor=False) as meta:
        meta['dc:title'] = titel
    pdf.docinfo['/Title'] = titel
    pdf.Root.ViewerPreferences = pikepdf.Dictionary(DisplayDocTitle=True)
    pdf.save(datei)
print(f'{datei}: Titel „{titel}“')
