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

- Online ist, was auf `main` liegt; GitHub Pages veröffentlicht es etwa eine Minute nach dem Hochladen.
- Claude speichert Änderungen direkt auf `main` und lädt sie hoch. Kein Pull Request, kein Merge
  durch Patrick (Entscheidung 10.11.2026: Jeder Klick kostet Aufmerksamkeit).
- Vor dem Hochladen prüft Claude lokal: die geänderten Seiten im Browser (Handy-Ansicht),
  alle Links darauf, die Schriften, und dass keine Lösung und kein `.tex` im Repository liegt.
- Danach nennt Claude im Chat kurz, welche Links neu sind oder sich geändert haben.
- Claude fragt vorher nach, bevor ein veröffentlichter Link umbenannt oder verschoben wird,
  bevor eine Lösung veröffentlicht wird und bevor etwas gelöscht wird.

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

Ausnahme: die Einstiegsseiten der Bildungsgänge (`happymatty.de/bf2` usw., siehe unten).
Sie sind Übersichten, deren Inhalt sich jedes Jahr ändern darf; die Blätter selbst bleiben
unter ihrem Thema.

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
- Die Übersicht zeigt immer drei Karten in dieser Reihenfolge: Aufgabenblatt, Musterlösung,
  Interaktiv. Was es noch nicht gibt, steht als graue Karte ohne Link (Klasse `gesperrt`):
  Musterlösung „Noch nicht freigeschaltet“, Interaktiv „Noch nicht vorhanden“.
  So sehen die Schüler, dass eine Lösung kommt (Entscheidung 10.11.2026).
- Kommt etwas hinzu, wird die graue Karte zur aktiven Karte; die freigeschaltete Musterlösung
  bekommt die Klasse `loesung` (orange).

## Lösungen

- Das Repository ist öffentlich: Alles, was darin liegt, kann jeder finden, auch ohne Link.
  Lösungen kommen deshalb erst ins Repository, wenn Patrick sie ausdrücklich freigibt.
  Bis dahin liegen sie nur im privaten Backup `happymatty-de/unterrichtsmaterial`.
  Ein ausgegrauter Link schützt nicht: Die Adresse `…/loesung.pdf` ist erratbar, und das
  Repository ist öffentlich einsehbar.
- Freischalten: Patrick schreibt z. B. „Lösung LF2 freigeben“. Claude kopiert die Lösung
  aus dem Backup als `loesung.pdf`, macht die Karte aktiv und orange und trägt sie in
  „Veröffentlichtes Material“ ein.
- Ein passwortgeschützter Bereich für Lehrkräfte ist geplant, aber noch nicht gebaut.

## Startseite, Themenseiten und Bildungsgänge

Zwei Wege zum Material (Entscheidung 10.11.2026): nach Thema für alle, nach Bildungsgang für die Schüler.

- **Startseite** `index.html` (`happymatty.de`): oben „Meine Klasse“ mit einer Kachel je
  Bildungsgang, darunter unter „Themenbereiche“ die **Themen** als grüne Karten (Klasse `thema-karte`) mit
  Kennzeichen der Bildungsgänge und Zahl der Arbeitsblätter. Keine Titel einzelner Arbeitsblätter
  auf der Startseite. Auch ältere Themen bleiben stehen, damit jedes Material auffindbar bleibt.
- **Themenseite** `<thema>/index.html` (z. B. `happymatty.de/lineare-funktionen`): alle
  Arbeitsblätter des Themas in der Reihenfolge der Lernreihe, je mit Titel, Kennzeichen der
  Bildungsgänge und einer kurzen Beschreibung. Laufen in einem Thema mehrere Bildungsgänge mit
  eigenen Blättern (etwa BGY als Wiederholung auf höherem Niveau), stehen sie hier nebeneinander.
- **Einstiegsseite je Bildungsgang** `<kürzel>/index.html` (z. B. `happymatty.de/bf2`): nur die
  Arbeitsblätter, die dieser Bildungsgang bearbeitet, je Fach und Thema in der Reihenfolge der
  Reihe. Ohne Material eine graue Karte „Noch kein Material“. Die Schüler speichern sich diesen
  einen Link.
- **Übersicht des Arbeitsblatts**: unter der Überschrift die Kennzeichen der Bildungsgänge.
- **Kennzeichen** (Klasse `badge`) wie die Badges auf den Blättern: grüner Rahmen, hellgrün
  gefüllt, Indie Flower.
- Wird ein Arbeitsblatt neu veröffentlicht, umbenannt oder bekommt es einen neuen Titel oder
  Bildungsgang, trägt Claude das im selben Schritt überall ein: Übersicht, Themenseite,
  Einstiegsseiten der Bildungsgänge und Startseite (Zahl, Kennzeichen). Ein neues Thema bekommt
  eine Themenseite und eine Karte auf der Startseite.
- Welcher Bildungsgang ein Blatt bearbeitet, steht im Namen des Reihenplans
  (`BF2_Reihenplan_…`); im Zweifel fragt Claude.

Bildungsgänge:

| Kürzel | Link | Name | Stand |
|---|---|---|---|
| BF1 | `/bf1` | Berufsfachschule I | aktiv, noch kein Material |
| BF2 | `/bf2` | Berufsfachschule II | aktiv |
| BGY | `/bgy` | Berufliches Gymnasium | aktiv, ein Jahrgang, noch kein Material |
| FSTM | `/fstm` | Techniker-Abendschule (BWL) | ab Januar 2027, Seite dann anlegen |
| DBOS | `/dbos` | Duale Berufsoberschule | ab Schuljahr 2027/28, Seite dann anlegen |

Reservierte Ordner, nie als Thema: `stil`, `bf1`, `bf2`, `bgy`, `fstm`, `dbos`.
Gemeinsame Gestaltung liegt in `stil/` (`basis.css` und die Schriften).

**Nach jeder Änderung an `basis.css`** und bei jeder neuen Seite führt Claude
`python3 _werkzeuge/stil_version.py` aus. Das Skript hängt an jeden Verweis auf
`/stil/basis.css` eine Kennung aus dem Inhalt der Datei an (`?v=…`). Sonst zeigen Browser
bis zu einigen Stunden die alte Gestaltung aus dem Zwischenspeicher (Anlass 10.11.2026:
Safari zeigte den alten Abstand am Kennzeichen noch nach mehreren Minuten).
Ordner, die mit `_` beginnen, veröffentlicht GitHub Pages nicht.

## Gestaltung

Startseite, Themenseiten und Übersichten sehen aus wie die Arbeitsblätter
(Skill `mathe`, Gestaltung: Schriften, Farben, Kopf- und Fußzeile, Überschrift):

- Kopfzeile mittig in Indie Flower: immer erst das Fach, dann das Thema, getrennt durch
  einen Mittelpunkt: „Mathematik · Lineare Funktionen“. Fach grau `#767676`, Thema grün `#26870C`.
  Darunter eine dünne Linie in Blau `#0072B2`.
- Auf der Startseite steht in der Kopfzeile nur „happymatty.de“, in Libertinus Sans fett, schwarz (Textfarbe `#1F2933`).
- Auf den Einstiegsseiten der Bildungsgänge steht in der Kopfzeile der volle Name (grau),
  die Überschrift ist das Kürzel („BF2“). Kacheln der Bildungsgänge auf der Startseite: Kürzel grün fett.
- Überschrift mittig in Indie Flower, Blau `#0072B2`.
- **Seitentitel** (`<title>`, erscheint im Tab und als Name von Lesezeichen), immer mit
  „happymatty“ klein und zusammen vorn: Startseite `happymatty`, Bildungsgang `happymatty/bf2`,
  Thema `happymatty/Lineare Funktionen`, Arbeitsblatt `happymatty/Mehr als nur steil`.
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
Alle Dateien (auch `.tex` und Lösungen) sichert Claude im selben Schritt im privaten Repository
`happymatty-de/unterrichtsmaterial`; Ablauf dort in `CLAUDE.md`.

## Veröffentlichtes Material

| Link | Inhalt | Bildungsgang | Quelle | Stand |
|---|---|---|---|---|
| `/lineare-funktionen/mehr-als-nur-steil/aufgabenblatt.pdf` | Aufgabenblatt | BF2 | `LF2_Mehr_als_nur_steil_Aufgabenblatt_v12.14.pdf` | 10.11.2026 |
| `/lineare-funktionen/mehr-als-nur-steil/interaktiv` | interaktiv | BF2 | Artifact „Mehr als nur steil – Lineare Funktionen (LF2)“ | 10.11.2026 |

Die ganze Reihe Lineare Funktionen läuft derzeit nur in der BF2.

Lösung zu „Mehr als nur steil“ (`LF2_Mehr_als_nur_steil_Loesung_v12.14.pdf`): noch nicht freigegeben.
