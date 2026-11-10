# happymatty.de

Dieses Repository ist die Website `happymatty.de`. Sie wird über GitHub Pages ausgeliefert.
Hier liegen dynamische Inhalte für den Unterricht (interaktive Webseiten zu Arbeitsblättern).
Sie sind ohne Login per Link erreichbar und hängen nicht an Claude.

## Grundsatz: Links bleiben dauerhaft gültig

Ein Link, der einmal an Schüler verschickt wurde, muss auf Dauer funktionieren,
auch über mehrere Schuljahre und für mehrere Klassen.

- Eine veröffentlichte Seite wird nie gelöscht oder umbenannt, ohne dass an der alten Adresse
  eine Weiterleitung auf die neue Adresse bleibt.
- Vor jeder Umbenennung oder Verschiebung fragt Claude nach.

## Ablauf bei Änderungen

- Online ist nur, was auf `main` liegt. Claude schreibt nie direkt auf `main`.
- Claude arbeitet auf einem eigenen Zweig, lädt ihn hoch und legt selbst einen Pull Request an.
- Patrick gibt frei, indem er den Pull Request auf GitHub mergt. Erst dann geht die Änderung online.
- Im Pull Request steht kurz, welche Links neu sind oder sich ändern.

## Aufbau der Links

`happymatty.de/<thema>/<titel-des-arbeitsblatts>`

Beispiel: `happymatty.de/lineare-funktionen/mehr-als-nur-steil`

- `<thema>` ist das übergeordnete Thema der Lernreihe, z. B. `lineare-funktionen`.
- `<titel-des-arbeitsblatts>` ist der Titel des Arbeitsblatts, zu dem die Seite gehört.
- Jede Seite ist ein Ordner mit einer `index.html`, z. B. `lineare-funktionen/mehr-als-nur-steil/index.html`.

Schreibweise:
- nur Kleinbuchstaben
- Wörter mit Bindestrich trennen, keine Unterstriche, keine Leerzeichen
- ä → ae, ö → oe, ü → ue, ß → ss
- keine Sonderzeichen

Nicht in den Link gehören, weil sie sich ändern:
- Nummern aus der Reihenplanung (`LF1`, `LF2` …)
- Versionsnummern
- Klassen, Bildungsgänge oder Schuljahre

Die Dateinamen der Arbeitsblätter (z. B. `LF2_Mehr_als_nur_steil_Aufgabenblatt_v12.14.pdf`)
folgen eigenen Regeln und sind davon unabhängig.

## Startseite und Themenseiten

- `index.html` im Hauptordner ist die Startseite (`happymatty.de`). Sie listet alle Seiten auf,
  gruppiert nach Fach und Thema, auch ältere, damit Schüler jedes Material wiederfinden.
- Jedes Thema hat eine Themenseite `<thema>/index.html` (z. B. `happymatty.de/lineare-funktionen`)
  mit allen Seiten des Themas.
- Wird eine Seite neu veröffentlicht, umbenannt oder bekommt sie einen neuen Titel, trägt Claude das
  im selben Pull Request auf der Startseite und auf der Themenseite ein. Ein neues Thema bekommt
  eine neue Themenseite.
- Innerhalb eines Themas stehen die Seiten in der Reihenfolge der Lernreihe. Jeder Eintrag hat
  Titel und eine kurze Beschreibung in einer Zeile.
- Gemeinsame Gestaltung liegt in `stil/` (`basis.css`, Schrift Libertinus Sans, Farben wie in den
  Unterrichtsseiten). `stil` ist kein Thema und wird nie als Link-Ordner vergeben.

## Inhalte auf den öffentlichen Seiten

- Patrick Saul darf als Autor genannt werden.
- Kein Impressum, keine Anschrift, keine Kontaktdaten.
- Nichts über Claude oder darüber, wie die Seiten entstehen.

## Herkunft der Seiten

Die Seiten entstehen meist als Artifact in einem Claude-Projekt auf claude.ai und werden von hier
übernommen. Jede Seite muss ohne Claude laufen: kein `window.claude`, keine Artifact-Datenbank.
Möglichst keine Inhalte von fremden Servern laden (Datenschutz der Schüler).

## Veröffentlichte Seiten

| Link | Quelle | übernommen |
|---|---|---|
| `/lineare-funktionen/mehr-als-nur-steil` | Artifact „Mehr als nur steil – Lineare Funktionen (LF2)“ | 10.11.2026 |
