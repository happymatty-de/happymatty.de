# happymatty.de

Dieses Repository ist die Website `happymatty.de`. Sie wird über GitHub Pages ausgeliefert.
Hier liegen Arbeitsblätter (PDF) und interaktive Seiten für den Unterricht.
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
- Jede Adresse ist ein Ordner mit einer `index.html`.

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

## Aufbau pro Arbeitsblatt

Jedes Arbeitsblatt hat einen Ordner. Darin liegt alles, was dazugehört, unter festen Namen:

| Datei | Link | Inhalt |
|---|---|---|
| `index.html` | `…/<titel>` | Übersicht des Arbeitsblatts: listet alles auf, was es dazu gibt |
| `interaktiv/index.html` | `…/<titel>/interaktiv` | interaktive Seite |
| `aufgabenblatt.pdf` | `…/<titel>/aufgabenblatt.pdf` | Arbeitsblatt |
| `loesung.pdf` | `…/<titel>/loesung.pdf` | Musterlösung, nur nach Freigabe (siehe unten) |

- Die Dateinamen tragen keine Version. Eine neue Version ersetzt die alte unter demselben Namen;
  ältere Stände bleiben im Git-Verlauf.
- Kommt etwas hinzu, wird es auf der Übersicht des Arbeitsblatts eingetragen.

## Lösungen

- Das Repository ist öffentlich: Alles, was darin liegt, kann jeder finden, auch ohne Link.
  Lösungen kommen deshalb erst ins Repository, wenn Patrick sie ausdrücklich freigibt,
  jeweils in einem eigenen Pull Request.
- Ein passwortgeschützter Bereich für Lehrkräfte ist geplant, aber noch nicht gebaut.

## Startseite und Themenseiten

- `index.html` im Hauptordner ist die Startseite (`happymatty.de`). Sie listet alle Arbeitsblätter auf,
  gruppiert nach Fach und Thema, auch ältere, damit Schüler jedes Material wiederfinden.
- Jedes Thema hat eine Themenseite `<thema>/index.html` (z. B. `happymatty.de/lineare-funktionen`)
  mit allen Arbeitsblättern des Themas.
- Wird ein Arbeitsblatt neu veröffentlicht, umbenannt oder bekommt es einen neuen Titel, trägt Claude das
  im selben Pull Request auf der Startseite und auf der Themenseite ein. Ein neues Thema bekommt
  eine neue Themenseite.
- Innerhalb eines Themas stehen die Arbeitsblätter in der Reihenfolge der Lernreihe. Jeder Eintrag hat
  Titel und eine kurze Beschreibung in einer Zeile.
- Gemeinsame Gestaltung liegt in `stil/` (`basis.css` und die Schriften). `stil` ist kein Thema
  und wird nie als Link-Ordner vergeben.

## Gestaltung

Startseite, Themenseiten und Übersichten sehen aus wie die Arbeitsblätter
(Skill `mathe`, Gestaltung: Schriften, Farben, Kopf- und Fußzeile, Überschrift):

- Kopfzeile mittig in Indie Flower: immer erst das Fach, dann das Thema, getrennt durch
  einen Mittelpunkt: „Mathematik · Lineare Funktionen“. Fach grau `#767676`, Thema grün `#26870C`.
  Darunter eine dünne Linie in Blau `#0072B2`.
- Auf der Startseite steht in der Kopfzeile nur „happymatty.de“, in Libertinus Sans fett, Blau `#0072B2`.
- Überschrift mittig in Indie Flower, Blau `#0072B2`.
- Fußzeile mittig in Indie Flower: „CC BY-NC-SA 4.0 · Patrick Saul“, Name grün, Rest grau,
  darüber eine dünne blaue Linie.
- Fließtext Libertinus Sans. Einträge als Karten mit blauem Rand links, Titel in Indie Flower blau.
- Die Musterlösung bekommt die Lösungsfarbe `#D55E00` (Klasse `loesung` in `basis.css`).
- Ändern sich die Farben oder die Kopfzeile im Skill `mathe`, zieht die Website nach.

## Inhalte auf den öffentlichen Seiten

- Patrick Saul darf als Autor genannt werden.
- Kein Impressum, keine Anschrift, keine Kontaktdaten.
- Nichts über Claude oder darüber, wie die Seiten entstehen.

## Herkunft der Seiten

Die interaktiven Seiten entstehen meist als Artifact in einem Claude-Projekt auf claude.ai und werden von hier
übernommen. Jede Seite muss ohne Claude laufen: kein `window.claude`, keine Artifact-Datenbank.
Möglichst keine Inhalte von fremden Servern laden (Datenschutz der Schüler).

Die PDFs entstehen in Patricks Claude-Projekten; Claude Code sieht diese Dateien nicht.
Patrick lädt sie hier im Chat oder auf GitHub hoch, Claude legt sie unter dem festen Namen ab.

## Veröffentlichtes Material

| Link | Inhalt | Quelle | seit |
|---|---|---|---|
| `/lineare-funktionen/mehr-als-nur-steil/interaktiv` | interaktiv | Artifact „Mehr als nur steil – Lineare Funktionen (LF2)“ | 10.11.2026 |
