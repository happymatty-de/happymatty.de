# happymatty.de

Dieses Repository ist die Website `happymatty.de`. Sie wird über GitHub Pages ausgeliefert.
Hier liegen Arbeitsblätter (PDF) und interaktive Seiten für den Unterricht.
Sie sind ohne Login per Link erreichbar und hängen nicht an Claude.

Die Übersichten (Startseite, Einstiegsseiten der Bildungsgänge, Themenseiten, Übersicht jeder
Themeneinheit, Probeklassenarbeit, Klassenarbeit) schreibt niemand von Hand: Das Skript
`_werkzeuge/bauen.py` baut sie aus den Beschreibungsdateien (Entscheidung 14.11.2026).
Wie das geht: Abschnitt „Beschreibungsdateien und Bauskript“.

## Rückmeldung im Chat

Ist eine Arbeit so erledigt wie besprochen, auch mit kleinen Abweichungen, schreibt Claude nur
„Alles umgesetzt.“, ohne Liste von Dateien, Commits, Versionen oder Schritten. Das gilt auch, wenn
ein Auftrag am Ende eine Zusammenfassung verlangt, etwa ein Prompt, den Claude Code vorbereitet hat.
Mehr schreibt Claude nur, wenn etwas nicht funktioniert hat, wenn Claude deutlich vom Auftrag
abgewichen ist oder wenn Patrick etwas entscheiden oder tun muss, und dann nur diesen Punkt. Ein
Protokoll oder einen Bericht liefert Claude nur, wenn Patrick ihn ausdrücklich als eigenes Ergebnis
verlangt, etwa ein Testprotokoll zum Weitergeben. Schreibt Claude einen Auftrag für einen
Projektchat oder eine andere Sitzung, verlangt Claude darin keine Schlussmeldung. Kleine
Verbesserungen, die Claude selbst vornimmt, werden nicht gemeldet (Entscheidung 14.11.2026,
verschärft die Regel vom 10.11.2026: Viel Text lässt Wichtiges untergehen).

## Wer schreibt was

In dieses Repository schreiben zwei Arten von Chats (Entscheidung 14.11.2026):

- **Projektchats aus claude.ai** (Patricks Claude-Projekte, in denen das Material entsteht; in
  Erprobung: erster Lauf am 14.11.2026 mit neuen Versionen von LF1 und LF2, ohne Fehler; eine ganz
  neue Themeneinheit hat noch kein Projektchat angelegt). Sie halten sich an diese CLAUDE.md und
  schreiben **nur in den Ordner ihrer Themeneinheit**: die PDFs, `interaktiv/` und die
  Beschreibungsdatei `_einheit.json`. Dann lassen sie `python3 _werkzeuge/bauen.py` laufen und
  laden hoch; die Seiten, die das Skript dabei außerhalb ihres Ordners neu baut (Themenseite,
  Startseite …), gehören mit dazu. Von Hand ändern sie außerhalb ihres Ordners nichts.
  Quelldateien und alle PDFs sichern sie selbst im privaten Backup
  `happymatty-de/unterrichtsmaterial` (Regeln dort in der `CLAUDE.md`).
- **Claude Code** (lokal bei Patrick) darf alles. Nur Claude Code ändert: das Skript und alles in
  `_werkzeuge/`, `stil/`, die Seitentypen (Aufbau der gebauten Seiten), neue Bereiche, neue
  Themen und Bildungsgänge, die Beschreibungsdateien der Themen (`_thema.json`, also auch
  Probeklassenarbeit und Klassenarbeit), Datenschutzerklärung, Impressum und diese CLAUDE.md.
- Braucht ein Projektchat etwas davon (ein neues Thema, einen neuen Bildungsgang oder Bereich,
  eine andere Gestaltung), hält er an und sagt Patrick, dass Claude Code das übernimmt.
- Der Weg über den Eingang bleibt daneben gültig: Patrick legt eine ZIP-Datei oder Dateien in den
  Ordner `Eingang` neben diesem Repository (`Schreibtisch/Claude/Eingang`) oder hängt sie in einer
  Sitzung an, und Claude Code übernimmt alles (Ablauf in der `CLAUDE.md` von
  `unterrichtsmaterial`).

## Begriffe

- **Thema**: das Gebiet einer Lernreihe, z. B. Lineare Funktionen (`/lineare-funktionen`).
- **Themeneinheit**: ein Abschnitt der Reihe mit genau einem Aufgabenblatt, z. B. LF1
  „Wie steil ist das?“ (`/lineare-funktionen/wie-steil-ist-das`). Zu ihr gehören Aufgabenblatt,
  Lösung, interaktive Seite, Probetest mit Lösung und Notentabelle. Auf Startseite und
  Themenseite werden Themeneinheiten gezählt und aufgelistet (Entscheidung 10.11.2026).
- **Teilthema**: der Fachbegriff des Abschnitts, um den es in einer Themeneinheit geht, wie in der
  Kopfzeile des Blatts (Skill `mathe`, Gestaltung, Kopf- und Fußzeile), z. B. „Addition und
  Subtraktion“ für „Zahlenjagd“. Es steht in der Kopfzeile der Übersicht und am Anfang ihrer
  Beschreibung auf der Themenseite. Fehlt es für eine Themeneinheit, fragt Claude nach.
- **Aufgabenblatt** (Mehrzahl Aufgabenblätter): das PDF für die Schüler, in Karten, Seitentiteln
  und Dateinamen. Sagt Patrick „Arbeitsblatt“ oder „Übungsblatt“, meint er dasselbe; Claude
  schreibt trotzdem „Aufgabenblatt“ (Entscheidung 10.11.2026). „Arbeitsblatt“ in diesen Regeln
  meint die Themeneinheit und kommt auf öffentlichen Seiten nicht vor.
- **Beschreibungsdatei**: `_einheit.json` im Ordner jeder Themeneinheit, `_thema.json` im Ordner
  jedes Themas. Sie sind die einzige Stelle, an der steht, was es gibt und was veröffentlicht ist.
- **Bereich**: eine weitere Zusammenstellung neben Themen und Bildungsgängen, vorgesehen ist
  „Grundlagen“. Noch ohne eigene Seite; eine Einheit kann ihn schon in ihrer Beschreibungsdatei
  nennen.

## Grundsatz: Links bleiben dauerhaft gültig

Ein Link, der einmal an Schüler verschickt wurde, muss auf Dauer funktionieren,
auch über mehrere Schuljahre und für mehrere Klassen.

- Eine veröffentlichte Seite wird nie gelöscht oder umbenannt, ohne dass an der alten Adresse
  eine Weiterleitung auf die neue Adresse bleibt. Ausnahmen: PDF-Adressen (siehe „Aufbau pro
  Arbeitsblatt“) und Seiten, für die Patrick ausdrücklich keine Weiterleitung will, etwa weil ihr
  Link nirgends weitergegeben wurde (Liste unter „Was veröffentlicht ist“).
- Vor jeder Umbenennung oder Verschiebung fragt Claude nach.
- Die Adresse einer Themeneinheit ist ihr Ordnername, nicht ihr Titel: Ein neuer Titel in
  `_einheit.json` ändert die Adresse nicht.

## Ablauf bei Änderungen

- Online ist, was auf `main` liegt; GitHub Pages veröffentlicht es etwa eine Minute nach dem Hochladen.
- Claude speichert Änderungen direkt auf `main` und lädt sie hoch. Kein Pull Request, kein Merge
  durch Patrick (Entscheidung 10.11.2026: Jeder Klick kostet Aufmerksamkeit).
- Commits tragen die Identität `happymatty-de <353878744+happymatty-de@users.noreply.github.com>`
  (im Repository mit `git config user.name` und `git config user.email` setzen), nie eine private
  Adresse: Das Repository ist öffentlich, jede Adresse im Verlauf bleibt dort sichtbar.
- Vor der Arbeit `git pull`, vor dem Hochladen `git pull --rebase`. Gibt es dabei Konflikte in
  gebauten Seiten (`index.html`), nimmt Claude den Stand von `main` und lässt das Skript neu
  laufen; die Beschreibungsdateien sind maßgeblich, nicht die Seiten.
- `git commit`, `git pull --rebase` und `git push` als einzelne Befehle ausführen, nicht mit `&&`
  verkettet (Anlass 14.11.2026: In einer Cloud-Sitzung lehnte die Rechteprüfung die Kette ab,
  einzeln gingen sie durch).
- Vor dem Hochladen läuft `python3 _werkzeuge/bauen.py` ohne Fehler. Das Skript prüft, dass kein
  `.tex` und kein PDF im Repository liegt, das nicht als freigegeben eingetragen ist (Abschnitt
  „Beschreibungsdateien und Bauskript“). Claude Code sieht sich zusätzlich geänderte Seitentypen
  und Gestaltung im Browser an (Handy-Ansicht, Links, Schriften).
- Nach dem Hochladen wartet Claude mit `python3 _werkzeuge/warten_bis_online.py`, bis GitHub
  Pages fertig ist, und meldet erst dann „online“ (braucht `gh`; ohne `gh` meldet Claude
  „hochgeladen, in wenigen Minuten online“). Die Veröffentlichung dauert mal unter einer
  Minute, mal mehrere Minuten (Anlass 10.11.2026: Patrick beurteilte Farben, bevor sie online
  waren). Danach genügt in Safari Wahltaste + Cmd + R.
- Claude fragt vorher nach, bevor ein veröffentlichter Link umbenannt oder verschoben wird,
  bevor eine Lösung veröffentlicht wird und bevor etwas gelöscht wird.

## Beschreibungsdateien und Bauskript

### Aufruf

Im Hauptordner des Repositorys (einmal je Sitzung vorher `pip install pikepdf`):

```bash
python3 _werkzeuge/bauen.py
```

prüft alles und baut dann die Übersichten. Es nennt jede Datei, die es geändert hat; diese
Dateien gehören in denselben Commit. Bei einem Fehler bricht es ab, schreibt nichts und nennt
Datei und Stelle.

- `python3 _werkzeuge/bauen.py --pruefen` prüft nur und nennt, was sich beim Bauen ändern würde
  (Rückgabe 1, wenn etwas nicht aktuell ist); es schreibt nichts.
- `python3 _werkzeuge/bauen.py --bestand` listet, was veröffentlicht ist (mit Quelle und Stand),
  und darunter, was vorhanden oder vorgemerkt, aber nicht veröffentlicht ist.

### Was das Skript prüft

Es bricht ab, ohne etwas zu schreiben, wenn

- irgendwo im Repository eine `.tex` liegt (sie enthält immer die Lösung),
- ein PDF im Repository liegt, das in keiner Beschreibungsdatei als freigegeben steht,
- ein als freigegeben eingetragenes PDF oder eine freigegebene interaktive Seite fehlt, oder ein
  Ordner `interaktiv/` liegt, der nicht freigegeben ist,
- eine Beschreibungsdatei kein gültiges JSON ist, ein Pflichteintrag fehlt oder ein Eintrag
  unbekannt ist (Tippfehler), ein Datum nicht wie `14.11.2026` aussieht, die Quelle eines PDFs
  keine Versionsnummer trägt oder die Quelle einer freigegebenen interaktiven Seite keine Version,
- ein Bildungsgang oder Bereich genannt ist, den es nicht gibt oder der noch keine Seite hat,
- ein Probetest, eine Probeklassenarbeit oder Klassenarbeit nicht zusammen mit Lösung und
  Notentabelle freigegeben ist, eine Kurztest-Fassung nicht zusammen mit ihrer Lösung, oder
  freigegebene Fassungen ohne die Notentabelle,
- das Aufgabenblatt einer Themeneinheit nicht freigegeben ist (eine Einheit erscheint erst mit
  ihrem Aufgabenblatt),
- zwei Einheiten eines Themas denselben `platz` haben oder zwei Themen eines Bildungsgangs dieselbe
  `reihenfolge`,
- ein Ordner ohne Beschreibungsdatei auftaucht (außer den reservierten und Weiterleitungen, also
  Seiten mit `rel="canonical"`) oder im Ordner einer Einheit eine unbekannte Datei liegt.

### Was das Skript baut und was nicht

- Es baut: Startseite, Einstiegsseiten der Bildungsgänge, Themenseiten, die Übersicht jeder
  Themeneinheit und die Seiten `/<thema>/probeklassenarbeit` und `/<thema>/klassenarbeit`,
  genau so, wie die Abschnitte unten sie beschreiben. Kennzeichen, Zahl der Themeneinheiten,
  Reihenfolge, Seitenzahlen der PDFs („PDF, 5 Seiten“, aus der Datei gelesen) und der Zusatz
  „· mit Test“ ergeben sich aus den Beschreibungsdateien.
- Es baut nicht und ändert nicht: interaktive Seiten, Datenschutzerklärung, Impressum,
  Weiterleitungen. Bei ihnen erneuert es nur die Kennungen `?v=…` im Kopf (siehe „Startseite,
  Themenseiten und Bildungsgänge“, letzter Absatz) und ergänzt dort fehlende Verweise auf das
  Symbol der Website.
- PDFs erzeugt es nie. Fehlt einem freigegebenen PDF der Titel (siehe „Gestaltung“,
  Seitentitel), trägt es ihn ein; Inhalt und Aussehen bleiben gleich.
- Es ersetzt die früheren Werkzeuge `stil_version.py` und `pdf_titel.py`.

### `_einheit.json`

Liegt im Ordner der Themeneinheit, z. B. `rechnen-mit-zahlen/zahlenjagd/_einheit.json`.
Vollständiges Beispiel:

```json
{
  "titel": "Zahlenjagd",
  "kennung": null,
  "teilthema": "Addition und Subtraktion",
  "beschreibung": "Zahlenkarten, Wege und Zahlenmauern",
  "bildungsgaenge": ["BF1"],
  "bereiche": [],
  "platz": 2,
  "aufgabenblatt": { "vorhanden": true, "freigegeben": true, "quelle": "Zahlenjagd_Aufgabenblatt_v2.pdf", "stand": "10.11.2026" },
  "musterloesung": { "vorhanden": true, "freigegeben": true, "quelle": "Zahlenjagd_Loesung_v2.pdf", "stand": "10.11.2026" },
  "interaktiv": { "vorhanden": false, "freigegeben": false },
  "probetest": {
    "test": { "vorhanden": true, "freigegeben": true, "quelle": "Zahlenjagd_Probetest_v2.pdf", "stand": "10.11.2026" },
    "loesung": { "vorhanden": true, "freigegeben": true, "quelle": "Zahlenjagd_Probetest_Loesung_v2.pdf", "stand": "10.11.2026" },
    "notentabelle": { "vorhanden": true, "freigegeben": true, "quelle": "Zahlenjagd_Probetest_Notentabelle_v2.pdf", "stand": "10.11.2026" }
  },
  "kurztest": {
    "fassungen": [
      {
        "fassung": 1,
        "test": { "vorhanden": true, "freigegeben": false, "quelle": "Zahlenjagd_Kurztest_F1_v2.pdf", "stand": "10.11.2026" },
        "loesung": { "vorhanden": true, "freigegeben": false, "quelle": "Zahlenjagd_Kurztest_F1_Loesung_v2.pdf", "stand": "10.11.2026" }
      },
      {
        "fassung": 2,
        "test": { "vorhanden": true, "freigegeben": false, "quelle": "Zahlenjagd_Kurztest_F2_v2.pdf", "stand": "10.11.2026" },
        "loesung": { "vorhanden": true, "freigegeben": false, "quelle": "Zahlenjagd_Kurztest_F2_Loesung_v2.pdf", "stand": "10.11.2026" }
      }
    ],
    "notentabelle": { "vorhanden": true, "freigegeben": false, "quelle": "Zahlenjagd_Kurztest_Notentabelle_v2.pdf", "stand": "10.11.2026" }
  }
}
```

(Die echte Datei nennt alle vier Kurztest-Fassungen; hier gekürzt.) Daraus entstehen die
Übersicht `/rechnen-mit-zahlen/zahlenjagd` mit Aufgabenblatt, Musterlösung, grauer Karte
„Interaktiv“ und dem Abschnitt „Probetest“, auf der Themenseite der Eintrag „Zahlenjagd“ mit
Kennzeichen BF1 und „Addition und Subtraktion – Zahlenkarten, Wege und Zahlenmauern · mit
Test“, und die Zählung auf Startseite und `/bf1`. Der Kurztest erscheint nirgends, weil
keine Fassung freigegeben ist.

**Dateinamen der Kurztests:** Die Reihe Rechnen mit Zahlen (BF1) heißt noch nach altem Muster,
wie im Beispiel (`Zahlenjagd_Kurztest_F1_v2.pdf`, `Zahlenjagd_Kurztest_F1_Loesung_v2.pdf`).
Alles Neue heißt nach Skill `mathe` (Dateinamen), wie LF1: `LF1_Kurztest_1_v19.1.pdf`,
`LF1_Kurztest_Loesung_1_v19.1.pdf`, `LF1_Kurztest_Notentabelle_v19.1.pdf`; auf der Website ohne
`_v…` (Tabelle unter „Tests“).

| Eintrag | Inhalt |
|---|---|
| `titel` | Titel wie auf dem Blatt: Überschrift der Übersicht, Eintrag auf der Themenseite, Seitentitel, PDF-Titel |
| `kennung` | Kürzel aus der Reihenplanung (`LF1`, `QF5`); `null`, wenn das Blatt keins trägt (die BF1-Blätter von Rechnen mit Zahlen) |
| `teilthema` | siehe „Begriffe“; Kopfzeile der Übersicht und Anfang der Beschreibung. Pflicht: Steht es nicht auf dem Blatt oder im Reihenplan, fragt der Chat Patrick |
| `beschreibung` | kurzer Text auf der Themenseite hinter „Teilthema – “; „· mit Test“ hängt das Skript an, wenn ein Probetest oder Kurztest-Fassungen veröffentlicht sind |
| `bildungsgaenge` | Liste der Bildungsgänge, die die Einheit bearbeiten (Kennzeichen, Einstiegsseiten, Zählung). Ein weiterer Eintrag zeigt die Einheit auch unter diesem Bildungsgang |
| `bereiche` | Liste weiterer Bereiche, vorgesehen: `"Grundlagen"`. Noch ohne Seite; das Skript prüft nur den Namen. Sonst `[]` |
| `platz` | Platz in der Reihe (1, 2, 3 …): Reihenfolge auf der Themenseite |
| `aufgabenblatt`, `musterloesung`, `interaktiv` | je ein Dokument (Pflicht) |
| `probetest` | `test`, `loesung`, `notentabelle`, je ein Dokument. Weglassen, wenn es keinen Probetest gibt |
| `kurztest` | `fassungen` (Liste, je `fassung` als Zahl, `test`, `loesung`) und `notentabelle`. Weglassen, wenn es keinen Kurztest gibt |

Jedes **Dokument** hat diese Einträge:

| Eintrag | Inhalt |
|---|---|
| `vorhanden` | `true`, wenn es die Datei gibt (bei Patrick, im Backup oder als Artifact) |
| `freigegeben` | `true`, wenn sie auf die Website darf. Nur dann liegt sie in diesem Repository |
| `quelle` | Pflicht, wenn vorhanden: der Dateiname mit Versionsnummer wie im Backup, z. B. `Zahlenjagd_Probetest_v2.pdf`. Auf der Website heißt die Datei genauso ohne `_v…` (`Zahlenjagd_Probetest.pdf`) und liegt im Ordner der Einheit. Bei `interaktiv` der Name des Artifacts mit Version, z. B. `Artifact „Mehr als nur steil – Lineare Funktionen (LF2)“ v1.22`; die Version ist Pflicht, sobald die Seite freigegeben ist, vorher genügt der Name |
| `stand` | Datum `TT.MM.JJJJ`; Pflicht, wenn freigegeben: der Tag, an dem diese Version online ging. Sonst, wenn bekannt, der Tag der Sicherung |
| `hinweis` | freiwillig: kurze Notiz, die nirgends auf der Website erscheint, z. B. „im Einsatz ab 11.11.2026, nicht veröffentlichen“. Stimmt ein Hinweis nicht mehr („folgt“, obwohl die Datei da ist; „im Einsatz“, obwohl geschrieben), passt ihn der Chat beim Nachführen an; was er verbietet („nicht veröffentlichen“), bleibt |
| `text` | nur bei `interaktiv`, Pflicht, wenn freigegeben: die Zeile unter dem Kartentitel, z. B. „Lineare Funktionen erkunden, zeichnen und ablesen – mit Spezialfällen“ |

Was es nicht gibt, steht als `{ "vorhanden": false, "freigegeben": false }`.

**Öffentlich lesbar:** Die Beschreibungsdateien liegen im öffentlichen Repository. GitHub Pages
liefert sie nicht aus (Name beginnt mit `_`), auf GitHub kann sie aber jeder lesen. Sie enthalten
deshalb nur Titel, Dateinamen, Versionen, Daten und kurze Hinweise, nie Aufgaben, Lösungen,
Punktzahlen oder etwas über einzelne Schüler.

### `_thema.json`

Liegt im Ordner des Themas, z. B. `quadratische-funktionen/_thema.json`; nur Claude Code legt
sie an und ändert sie.

```json
{
  "titel": "Quadratische Funktionen",
  "kennung": "QF",
  "fach": "Mathematik",
  "unterzeile": null,
  "bildungsgang": "BGY",
  "reihenfolge": 1,
  "probeklassenarbeit": {
    "bildungsgaenge": ["BGY"],
    "test": { "vorhanden": true, "freigegeben": true, "quelle": "QF_Probeklassenarbeit_v6.pdf", "stand": "10.11.2026" },
    "loesung": { "vorhanden": true, "freigegeben": true, "quelle": "QF_Probeklassenarbeit_Loesung_v6.pdf", "stand": "10.11.2026" },
    "notentabelle": { "vorhanden": true, "freigegeben": true, "quelle": "QF_Probeklassenarbeit_Notentabelle_v6.pdf", "stand": "10.11.2026" }
  },
  "klassenarbeit": {
    "bildungsgaenge": ["BGY"],
    "test": { "vorhanden": true, "freigegeben": true, "quelle": "QF_Klassenarbeit_v1.4.pdf", "stand": "13.11.2026", "hinweis": "geschrieben am 13.11.2026; eine Nachschreib-Fassung käme nur ins Backup" },
    "loesung": { "vorhanden": true, "freigegeben": true, "quelle": "QF_Klassenarbeit_Loesung_v1.4.pdf", "stand": "13.11.2026" },
    "notentabelle": { "vorhanden": true, "freigegeben": true, "quelle": "QF_Klassenarbeit_Notentabelle_v1.4.pdf", "stand": "13.11.2026" }
  }
}
```

| Eintrag | Inhalt |
|---|---|
| `titel` | Name des Themas: Überschrift der Themenseite, Kopfzeilen, Karten |
| `kennung` | Kürzel der Reihe (`LF`, `QF`) oder `null` |
| `fach` | `Mathematik` (später `BWL`): Kopfzeile, Überschrift auf den Einstiegsseiten |
| `unterzeile` | die Teile des Themas, so wie Patrick sie vorgibt, oder `null` |
| `bildungsgang` | der Bildungsgang, zu dem das Thema gehört: Zurück-Link der Themenseite, Gruppe auf der Startseite |
| `reihenfolge` | Platz unter den Themen dieses Bildungsgangs, in der Reihenfolge des Unterrichts |
| `probeklassenarbeit`, `klassenarbeit` | freiwillig: `bildungsgaenge` (Kennzeichen) und `test`, `loesung`, `notentabelle`; die PDFs liegen in `<thema>/probeklassenarbeit/` bzw. `<thema>/klassenarbeit/` |

Die Probeklassenarbeit erscheint, sobald sie freigegeben ist. Die Klassenarbeit erscheint, sobald
sie vorhanden ist, bis zur Freigabe mit grauen Karten (siehe „Tests“).

### Neue Themeneinheit anlegen

1. `git pull`. Das Thema muss es schon geben (`<thema>/_thema.json`); ein neues Thema legt
   Claude Code an.
2. Ordner `<thema>/<titel-der-einheit>/` anlegen; Schreibweise wie unter „Aufbau der Links“
   (z. B. „Mal, geteilt – und das Minus?“ → `mal-geteilt-und-das-minus`).
3. Die freigegebenen PDFs hineinlegen, jeweils unter dem Namen aus `quelle` ohne `_v…`:
   das Aufgabenblatt immer; den Probetest mit Lösung und Notentabelle, sobald es ihn gibt; die
   Musterlösung und Kurztest-Fassungen nur, wenn Patrick sie ausdrücklich freigibt (Abschnitte
   „Lösungen“ und „Tests“). Nie eine `.tex`.
4. Ist eine interaktive Seite freigegeben: als `interaktiv/index.html` ablegen und dabei die
   Regeln unter „Gestaltung“ einsetzen (Seitentitel, Zurück-Knopf, „Datenschutz · Impressum“).
5. `_einheit.json` schreiben wie im Beispiel oben: alles, was es gibt, auch Nicht-Freigegebenes
   (dann `"freigegeben": false`). `platz` ist die Nummer in der Reihe.
6. `python3 _werkzeuge/bauen.py`; bei Fehlern die Meldung lesen, beheben, erneut laufen lassen.
7. Den Ordner der Einheit und alle Dateien, die das Skript nennt, in einem Commit hochladen
   (Commit-Nachricht wie „LF3 Titel v2 veröffentlicht“), dann `warten_bis_online.py`.
8. Im Backup `unterrichtsmaterial` sichern: alle Dateien mit Versionsnummer, auch `.tex` und
   Lösungen (Regeln dort).

**Neue Version eines Dokuments:** PDF unter demselben Namen ersetzen, in `_einheit.json` `quelle`
und `stand` anpassen, Skript laufen lassen. Ist die Lösung freigegeben, kommt sie mit.
**Freigabe:** PDF hineinlegen, `"freigegeben": true` und `stand` setzen, Skript laufen lassen.
**Freigabe zurücknehmen** (nur auf Patricks Wort): PDFs löschen, `"freigegeben": false`, im
`hinweis` Datum und Grund („bis 14.11.2026 online; nicht mehr veröffentlichen, der Probetest
reicht“), Skript laufen lassen. Die PDF-Adressen entfallen ohne Weiterleitung; sie kommen unter
„Frühere Adressen und Namen“ (Abschnitt „Was veröffentlicht ist“).
**Weiterer Bildungsgang:** in `bildungsgaenge` ergänzen, Skript laufen lassen. Den ersten
zweiten Bildungsgang überhaupt trägt Claude Code ein (siehe „Startseite, Themenseiten und
Bildungsgänge“).

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

Die Dateinamen der Arbeitsblätter im Material (z. B. `LF2_Mehr_als_nur_steil_Aufgabenblatt_v12.14.pdf`)
folgen eigenen Regeln. Auf der Website heißen die PDFs wie im Material, nur ohne Versionsnummer
(Abschnitt „Aufbau pro Arbeitsblatt“).

## Aufbau pro Arbeitsblatt

Jedes Arbeitsblatt (jede Themeneinheit) hat einen Ordner. Darin liegt alles, was dazugehört:

| Datei | Link | Inhalt |
|---|---|---|
| `_einheit.json` | – (wird nicht ausgeliefert) | Beschreibungsdatei |
| `index.html` | `…/<titel>` | Übersicht des Arbeitsblatts, vom Skript gebaut: listet alles auf, was es dazu gibt |
| `interaktiv/index.html` | `…/<titel>/interaktiv` | interaktive Seite |
| `<Kürzel>_<Titel>_Aufgabenblatt.pdf` | `…/<titel>/<Kürzel>_<Titel>_Aufgabenblatt.pdf` | Arbeitsblatt |
| `<Kürzel>_<Titel>_Loesung.pdf` | `…/<titel>/<Kürzel>_<Titel>_Loesung.pdf` | Musterlösung, nur nach Freigabe (siehe unten) |

- **PDF-Namen** (Entscheidung 12.11.2026): Der Name ist der aus `quelle` in der
  Beschreibungsdatei ohne `_v…`, z. B. `QF5_Der_Korbwurf_Aufgabenblatt.pdf`. Grund: Beim
  Herunterladen soll die Datei so heißen wie bei Patrick, und das Kürzel (QF5, LF1 …) ordnet die
  Dateien bei den Schülern.
- Die Dateinamen tragen keine Version. Eine neue Version ersetzt die alte unter demselben Namen;
  ältere Stände bleiben im Git-Verlauf. Die Versionsnummer steht nur in `quelle`.
- Die Kennung (Kürzel) im Dateinamen steht damit auch in der Adresse; das ist die Ausnahme von der
  Regel, dass Adressen keine Kennung tragen. Die Adressen der Seiten bleiben ohne Kennung.
- Die früheren PDF-Adressen (`aufgabenblatt.pdf`, `loesung.pdf`, `probetest.pdf` usw.) entfielen
  am 12.11.2026 ersatzlos, ohne Weiterleitung: Patrick hatte sie nirgends weitergegeben. Das gilt
  nur für PDFs; Seitenadressen bekommen weiter eine Weiterleitung (Grundsatz oben).
- Die Übersicht zeigt immer drei Karten in dieser Reihenfolge: Aufgabenblatt, Musterlösung,
  Interaktiv. Was nicht freigegeben ist, steht als graue Karte ohne Link (Klasse `gesperrt`):
  Musterlösung „Noch nicht freigeschaltet“, Interaktiv „Noch nicht vorhanden“.
  So sehen die Schüler, dass eine Lösung kommt (Entscheidung 10.11.2026).
- Wird etwas freigegeben, wird die graue Karte zur aktiven Karte; die freigeschaltete Musterlösung
  bekommt die Klasse `loesung` (orange).
- **Text unter dem Kartentitel** sagt, wozu die Schüler die Datei nutzen, nicht was man technisch
  damit tun kann; dahinter in Klammern Dateiart und Seitenzahl (Entscheidung 10.11.2026: Kaum ein
  Schüler druckt selbst aus, sie laden die PDFs aufs iPad). Das Skript setzt ihn so:

  | Karte | Text |
  |---|---|
  | Aufgabenblatt | „Zum Arbeiten und Lernen (PDF, n Seiten)“ |
  | Musterlösung, Lösungen zu Tests | „Zum Vergleichen (PDF, n Seiten)“ |
  | Probetest | „Zum Üben vor dem Kurztest (PDF, n Seiten)“ |
  | Probeklassenarbeit | „Zum Üben vor der Klassenarbeit (PDF, n Seiten)“ |
  | Kurztest-Fassung, Klassenarbeit | „Zum Üben (PDF, n Seiten)“ |
  | Notentabelle | „Welche Note zu deinen Punkten gehört (PDF, 1 Seite)“ |
  | Interaktiv | `text` aus der Beschreibungsdatei |

  Die Seitenzahl liest das Skript aus der Datei.

## Tests: Probetest, Kurztest, Klassenarbeit

In BF1 und BF2 gehört jeder Test zu genau einer Themeneinheit. Er steht auf ihrer Übersicht
unter den drei Karten, je Testart in einem eigenen Abschnitt (Überschrift `themenkopf` mit `id`).
Keine eigene Seite, keine Nummer: „Kurztest 1“ verwechselt man mit Fassung 1.

- **Probetest: wird immer veröffentlicht**, zusammen mit Lösung und Notentabelle, sobald
  Patrick ihn schickt (Entscheidung 10.11.2026: Der Probetest dient der Selbstkontrolle).
- **Kurztest: wird normalerweise nicht veröffentlicht**, weil Patrick ihn wieder einsetzt.
  Es gibt dann keinen Abschnitt und keine graue Karte; in der Beschreibungsdatei stehen die
  Fassungen mit `"freigegeben": false`. Nur wenn Patrick Fassungen ausdrücklich freigibt, entsteht
  der Abschnitt „Kurztest“ mit diesen Fassungen, ihren Lösungen und der Notentabelle.
  **Fassungen, die noch eine Klasse schreibt, kommen nie auf die Website**, ebenso wenig
  Nachschreib-Fassungen.
- **Klassenarbeiten** (z. B. BGY) decken meist mehrere Themeneinheiten ab und stehen auf der
  Ebene des Themas, in `_thema.json` (Entscheidung 10.11.2026, erste: Quadratische Funktionen):
  - Veröffentlicht wird die **Probeklassenarbeit**, immer mit Lösung und Notentabelle
    (wie der Probetest). Die Klassenarbeit selbst kommt erst auf die Website, wenn Patrick sie
    nach dem Schreiben freigibt (Entscheidung 12.11.2026, erste: Quadratische Funktionen, geschrieben
    Freitag 13.11.2026; vorher hieß es „nie“).
  - **Grundsatz** (Patrick, 12.11.2026): Themenseiten verlinken nie direkt auf PDFs. Jede Karte dort
    führt eine Ebene tiefer auf eine Übersicht; erst dort liegen die einzelnen Dokumente.
  - Die Klassenarbeit ist aufgebaut wie die Probeklassenarbeit: Auf der Themenseite unter der
    Probeklassenarbeit der Abschnitt „Klassenarbeit“ (`themenkopf` mit `id="klassenarbeit"`) mit
    **einer** violetten Karte (`test`), von Anfang an aktiv: „Klassenarbeit“ mit Kennzeichen – „Die
    Klassenarbeit zur ganzen Reihe · mit Lösung und Notentabelle“, Link `/<thema>/klassenarbeit`.
    Diese Seite (`<thema>/klassenarbeit/index.html`, Titel `happymatty/<Thema>/Klassenarbeit`,
    Überschrift „Klassenarbeit“, Kennzeichen, zurück zum Thema) zeigt drei Karten: „Klassenarbeit“,
    „Lösung zur Klassenarbeit“, „Notentabelle zur Klassenarbeit“. Sobald die Klassenarbeit in
    `_thema.json` vorhanden ist, gibt es Abschnitt und Seite; bis zur Freigabe sind die Karten
    grau (`gesperrt`) mit dem Hinweis „Wird am Freitag nach der Klassenarbeit veröffentlicht“.
    Auch die Gesamtpunktzahl bleibt bis dahin verborgen, deshalb geht alles zusammen online
    (Entscheidung 12.11.2026).
  - Freigabe: Patrick schreibt nur „Klassenarbeit freigeben“. Die Dateien liegen schon im Backup
    (`unterrichtsmaterial/mathematik/<thema>/QF_Klassenarbeit_…_v….pdf`, neueste Version); Claude
    Code kopiert die drei PDFs ohne `_v…` nach `<thema>/klassenarbeit/`, setzt in `_thema.json`
    bei allen dreien `"freigegeben": true` und `stand` und lässt das Skript laufen. Die `.tex`
    bleibt im Backup. Vor der Freigabe liegt keines dieser PDFs in diesem Repository.
  - Eigene Seite wie die Übersicht einer Themeneinheit (Entscheidung 10.11.2026, geändert am
    selben Tag: einheitlich mit den Themeneinheiten): `<thema>/probeklassenarbeit/index.html`,
    Link `/<thema>/probeklassenarbeit`. Kopfzeile Fach · Thema, Überschrift „Probeklassenarbeit“,
    Kennzeichen, drei Karten: Probeklassenarbeit (violett, `test`), Lösung zur Probeklassenarbeit
    (orange), Notentabelle zur Probeklassenarbeit (hellblau). Die PDFs liegen im selben Ordner.
  - Auf der Themenseite unter den Themeneinheiten der Abschnitt „Probeklassenarbeit“
    (`themenkopf` mit `id="probeklassenarbeit"`) mit **einer** violetten Karte (`test`) auf diese
    Seite: „Probeklassenarbeit“ mit Kennzeichen – „Die ganze Reihe zum Üben vor der Klassenarbeit ·
    mit Lösung und Notentabelle“.
  - Startseite, Einstiegsseiten der Bildungsgänge und Beschreibungen der Themeneinheiten nennen
    sie nicht.

| Datei (Name wie in `quelle`, ohne `_v…`) | Inhalt | PDF-Titel |
|---|---|---|
| `<Kürzel>_Probetest.pdf` | Probetest (es gibt nur eine Fassung) | `happymatty/<Titel>/Probetest` |
| `<Kürzel>_Probetest_Loesung.pdf` | Lösung zum Probetest | `happymatty/<Titel>/Lösung Probetest` |
| `<Kürzel>_Probetest_Notentabelle.pdf` | Notentabelle zum Probetest | `happymatty/<Titel>/Notentabelle Probetest` |
| `<Kürzel>_Kurztest_<n>.pdf` | freigegebene Fassung des Kurztests | `happymatty/<Titel>/Kurztest Fassung <n>` |
| `<Kürzel>_Kurztest_Loesung_<n>.pdf` | Lösung dazu | `happymatty/<Titel>/Lösung Kurztest Fassung <n>` |
| `<Kürzel>_Kurztest_Notentabelle.pdf` | Notentabelle zum Kurztest | `happymatty/<Titel>/Notentabelle Kurztest` |
| `probeklassenarbeit/QF_Probeklassenarbeit.pdf` | Probeklassenarbeit (im Ordner des Themas) | `happymatty/<Thema>/Probeklassenarbeit` |
| `probeklassenarbeit/QF_Probeklassenarbeit_Loesung.pdf` | Lösung zur Probeklassenarbeit | `happymatty/<Thema>/Lösung Probeklassenarbeit` |
| `probeklassenarbeit/QF_Probeklassenarbeit_Notentabelle.pdf` | Notentabelle zur Probeklassenarbeit | `happymatty/<Thema>/Notentabelle Probeklassenarbeit` |
| `klassenarbeit/QF_Klassenarbeit.pdf` usw. | Klassenarbeit, Lösung, Notentabelle | `happymatty/<Thema>/Klassenarbeit`, `…/Lösung Klassenarbeit`, `…/Notentabelle Klassenarbeit` |

- **Notentabellen werden immer mit veröffentlicht**, wenn der zugehörige Test online geht.
  Karte „Notentabelle zum …“, Text „Welche Note zu deinen Punkten gehört (PDF, 1 Seite)“.
  Zwischen Zahl und „Seite(n)“ steht immer ein geschütztes Leerzeichen (`&nbsp;`).
- Karten je Abschnitt: Test (violett, Klasse `test`), Lösung (orange), Notentabelle (hellblau, Klasse `notentabelle`); beim Kurztest je
  Fassung Test und Lösung, danach die Notentabelle.
- Themenseite: in der Beschreibung der Themeneinheit „· mit Test“, sobald ein Probetest oder
  Kurztest-Fassungen veröffentlicht sind, gleich welche (Entscheidung 14.11.2026; vorher
  „· mit Probetest“ bzw. „· mit Probetest und Kurztest“).

## Lösungen

- Das Repository ist öffentlich: Alles, was darin liegt, kann jeder finden, auch ohne Link.
  Lösungen kommen deshalb erst ins Repository, wenn Patrick sie ausdrücklich freigibt.
  Bis dahin liegen sie nur im privaten Backup `happymatty-de/unterrichtsmaterial`.
  Ein ausgegrauter Link schützt nicht: Die Adresse `…/<Kürzel>_<Titel>_Loesung.pdf` ist erratbar, und das
  Repository ist öffentlich einsehbar.
- Freischalten: Patrick schreibt z. B. „Lösung LF2 freigeben“. Claude kopiert die Lösung
  aus dem Backup (ohne `_v…` im Namen) in den Ordner der Einheit, setzt in `_einheit.json` bei
  `musterloesung` `"freigegeben": true` und `stand` und lässt das Skript laufen; es macht die
  Karte aktiv und orange und trägt den PDF-Titel ein.
  Kommt später eine neue Version des Blatts, ersetzt Claude eine freigegebene Lösung mit.
- Ein passwortgeschützter Bereich für Lehrkräfte ist geplant, aber noch nicht gebaut.

## Startseite, Themenseiten und Bildungsgänge

Zwei Wege zum Material (Entscheidung 10.11.2026): nach Thema für alle, nach Bildungsgang für die
Schüler. Alle diese Seiten baut das Skript; was hier steht, ist der Aufbau, den es erzeugt.

- **Startseite** `index.html` (`happymatty.de`): unter der Überschrift „Unterrichtsmaterial“ die Zeile
  „von Patrick Saul“ in Indie Flower grün (Klasse `unterzeile autor`, Entscheidung 11.11.2026). Darunter „Klassen“ mit einer Kachel je
  Bildungsgang (Entscheidung 11.11.2026: knapp wie „Themen“, vorher „Meine Klasse“; „Themenbereiche“ hieß der Abschnitt bis 14.11.2026), darunter unter „Themen“ die **Themen** als grüne Karten (Klasse `thema-karte`) mit
  Kennzeichen der Bildungsgänge und Zahl der Themeneinheiten („2 Themeneinheiten“). Keine Titel
  einzelner Arbeitsblätter auf der Startseite. Auch ältere Themen bleiben stehen, damit jedes
  Material auffindbar bleibt.
  **Reihenfolge** (Entscheidung 10.11.2026): erst alle Themen der BF1, dann der BF2, dann des BGY
  (danach FSTM, DBOS); innerhalb eines Bildungsgangs in der Reihenfolge, in der die Reihen
  unterrichtet werden (`reihenfolge` in `_thema.json`), nicht alphabetisch. Zwischen den
  Bildungsgängen eine gestrichelte Linie in Akzentlila (`<hr class="trenner">`, je Bildungsgang
  eine eigene `<ul class="liste">`), zwischen Themen desselben Bildungsgangs keine.
  Zwischen Titel und Kennzeichen kann eine **Unterzeile** (Klasse `unterzeile`, im Standardgrau
  wie der Text darunter) stehen: die Teile des Themas, mit Mittelpunkt getrennt, so wie Patrick sie vorgibt
  (Rechnen mit Zahlen: „Rationale Zahlen · Rechenregeln · Überschlagen und Schätzen“).
- **Themenseite** `<thema>/index.html` (z. B. `happymatty.de/lineare-funktionen`): Kopfzeile nur
  „Mathematik“, Überschrift das Thema groß in Grün (`<h1 class="thema">`, Entscheidung 10.11.2026:
  der Haupttitel soll sofort ins Auge fallen). Darunter der Abschnitt „Themeneinheiten“
  (`themenkopf`, grau; nicht „Arbeitsblätter“, weil auch interaktive Seiten dazugehören):
  alle Themeneinheiten des Themas in der Reihenfolge der Lernreihe (`platz`), je mit Titel,
  Kennzeichen der Bildungsgänge und einer kurzen Beschreibung. Laufen in einem Thema mehrere
  Bildungsgänge mit eigenen Blättern (etwa BGY als Wiederholung auf höherem Niveau), stehen sie
  hier nebeneinander. Die Beschreibung beginnt mit dem Teilthema, danach ein Gedankenstrich:
  „Addition und Subtraktion – Zahlenkarten, Wege und Zahlenmauern“. Danach gegebenenfalls die
  Abschnitte „Probeklassenarbeit“ und „Klassenarbeit“ (siehe Tests).
- **Einstiegsseite je Bildungsgang** `<kürzel>/index.html` (z. B. `happymatty.de/bf2`): nur die
  **Themen**, die dieser Bildungsgang bearbeitet, keine einzelnen Themeneinheiten (Entscheidung
  10.11.2026: sonst wird es zu viel). Je Fach eine Überschrift (`themenkopf`, „Mathematik“), darunter
  die Themen als grüne Karten wie auf der Startseite (mit Unterzeile und Zahl der Themeneinheiten,
  ohne Kennzeichen), in der Reihenfolge, in der sie unterrichtet werden. Ohne Material eine graue
  Karte „Noch kein Material“ mit „Hier erscheinen die Themen, sobald Material online ist.“
  (Entscheidung 14.11.2026). Die Schüler speichern sich diesen einen Link.
- **Übersicht des Arbeitsblatts**: unter der Überschrift die Kennzeichen der Bildungsgänge.
- **Kennzeichen** (Klasse `badge`) in der Form der Badges auf den Blättern, aber in Akzentlila:
  Rahmen und Schrift `#85609E`, gefüllt `#EBE5EF`, Indie Flower (Skill `mathe`, Stand 10.11.2026).
- **Eine Themeneinheit in mehreren Bildungsgängen** (Eintrag in `bildungsgaenge`): Sie trägt alle
  Kennzeichen (Übersicht, Themenseite), und ihr Thema trägt auf der Startseite alle Kennzeichen
  seiner Einheiten. Auf der Startseite steht das Thema nur einmal, in der Gruppe seines
  `bildungsgang`; die Zahl dort zählt alle Einheiten. Auf der Einstiegsseite jedes beteiligten
  Bildungsgangs steht das Thema mit der Zahl der Einheiten dieses Bildungsgangs. Die Themenseite
  führt zurück zum `bildungsgang` des Themas (Entscheidung 14.11.2026). Zwei Kennzeichen
  hintereinander stehen auf der Themenseite noch mit dem großen Abstand hinter dem Titel; beim
  ersten Fall ergänzt Claude Code in `basis.css` den Abstand zwischen zwei Kennzeichen und prüft
  im Browser (Entscheidung 14.11.2026). Bis dahin trägt nur Claude Code einen zweiten
  Bildungsgang ein.
- Welcher Bildungsgang ein Blatt bearbeitet, steht im Namen des Reihenplans
  (`BF2_Reihenplan_…`); im Zweifel fragt Claude.

Bildungsgänge (maßgeblich ist `BILDUNGSGAENGE` in `_werkzeuge/bauen.py`):

| Kürzel | Link | Name | Stand |
|---|---|---|---|
| BF1 | `/bf1` | Berufsfachschule I | aktiv |
| BF2 | `/bf2` | Berufsfachschule II | aktiv |
| BGY | `/bgy` | Berufliches Gymnasium | aktiv, ein Jahrgang |
| FSTM | `/fstm` | Techniker-Abendschule (BWL) | ab Januar 2027; dann trägt Claude Code ihn im Skript ein |
| DBOS | `/dbos` | Duale Berufsoberschule | ab Schuljahr 2027/28; dann trägt Claude Code ihn im Skript ein |

Bereiche: vorgesehen „Grundlagen“ (`BEREICHE` im Skript), noch ohne Seite. Bekommt ein Bereich
eine Seite, baut Claude Code den Seitentyp ins Skript ein und fragt vorher nach Adresse und
Aufbau.

Reservierte Ordner, nie als Thema: `stil`, `bf1`, `bf2`, `bgy`, `fstm`, `dbos`, `datenschutz`,
`impressum`. Gemeinsame Gestaltung liegt in `stil/` (`basis.css` und die Schriften).

**Kennungen im Kopf:** Das Skript hängt an jeden Verweis auf `/stil/basis.css` eine Kennung aus dem
Inhalt der Datei an (`?v=…`) und ergänzt fehlende Verweise auf das Symbol der Website. Sonst
zeigen Browser bis zu einigen Stunden die alte Gestaltung aus dem Zwischenspeicher (Anlass
10.11.2026: Safari zeigte den alten Abstand am Kennzeichen noch nach mehreren Minuten).
Die Verweise auf das Symbol im Kopf der Seite (`favicon.ico`, `stil/icon-32.png`,
`apple-touch-icon.png`) bekommen ebenso eine Kennung aus dem Inhalt der Bilddatei
(Anlass 11.11.2026: Safari auf dem iPad zeigte nach dem Wechsel zum Smiley weiter das alte „hm“,
auch nach dem Löschen des Verlaufs). Nach jeder Änderung an `basis.css` oder am Symbol und bei
jeder neuen Seite (auch jeder Übernahme eines Artifacts) läuft deshalb das Skript.
Ordner und Dateien, die mit `_` beginnen, veröffentlicht GitHub Pages nicht.

## Gestaltung

Startseite, Themenseiten und Übersichten sehen aus wie die Arbeitsblätter
(Skill `mathe`, Gestaltung: Schriften, Farben, Kopf- und Fußzeile, Überschrift). Ihr HTML steht im
Skript; eine Änderung daran macht nur Claude Code und prüft sie im Browser:

- Kopfzeile mittig in Indie Flower: immer erst das Fach, dann das Thema, getrennt durch
  einen Mittelpunkt: „Mathematik · Lineare Funktionen“. Fach grau, Thema grün `#26870C`.
  Auf der Übersicht einer Themeneinheit folgt das Teilthema in Akzentlila `#85609E`:
  „Mathematik · Rechnen mit Zahlen · Addition und Subtraktion“ (Klasse `teilthema`).
  Die Themenseite zeigt in der Kopfzeile nur das Fach; das Thema ist dort die grüne Überschrift.
- **Ein Grau** `#6E6E6E` überall, wo Text grau ist (Kopf- und Fußzeile, Beschreibungen,
  Unterzeilen), wie im Skill `mathe` (Variable `--grau`). Das frühere `#767676` war heller als
  Blau, Grün und Lila und wirkte daneben am schwächsten (Skill `mathe`, 10.11.2026).
- **Akzentlila** `#85609E`, Füllung `#EBE5EF` (Variablen `--lila`, `--lilahell`): trägt die
  genauere Einordnung: Grün nennt das Thema, Lila den Teil davon. Auf der Website trägt es das
  Teilthema, Kennzeichen und Kacheln der Bildungsgänge und die Karten der Tests.
  Darunter eine dünne Linie in Blau `#0072B2`.
- **Logo oben links** (Entscheidung 11.11.2026): Auf jeder Seite steht ganz
  oben links das Symbol der Website mit „happymatty.de“ daneben (Libertinus Sans fett, schwarz,
  Textfarbe `#1F2933`), als Link auf die Startseite (Klasse `logo`, Bild `/stil/icon-192.png`).
  Das ist der Standard für jede Seite, auch für jede neue: erst der Smiley, rechts daneben der
  Name; „happymatty.de“ steht nirgends mehr mittig oder an anderer Stelle (Patrick, 11.11.2026).
  Rechts in derselben Zeile steht der Link eine Ebene höher (Klasse `zurueck`, Logo und Link
  zusammen in `<div class="kopfleiste">`), aber nie ein zweiter Link auf die Startseite
  (Entscheidung 11.11.2026: spart auf dem Handy eine Zeile; vorher stand er unter dem Logo).
  Ist er zu lang („← Quadratische Funktionen“ auf iPhone SE/mini), bricht er rechtsbündig neben
  dem Logo um:
  - Startseite: dasselbe Logo an derselben Stelle, aber ohne Link (`<div class="logo">`); die
    Kopfzeile bleibt leer (nur die blaue Linie), weil der Name schon im Logo steht (Entscheidung
    11.11.2026: Das Logo gehört auch auf die Startseite; vorher stand dort nur „happymatty.de“
    mittig in der Kopfzeile).
  - Einstiegsseite eines Bildungsgangs (`/bf1` …): nur das Logo, kein Zurück-Link.
  - Themenseite: zurück zu ihrem Bildungsgang („← BF1“ auf `/bf1/`, `bildungsgang` in
    `_thema.json`), nicht zur Startseite (Entscheidung 11.11.2026).
  - Übersicht einer Themeneinheit, Probeklassenarbeit, Klassenarbeit: zurück zum Thema („← Lineare Funktionen“).
  - Datenschutzerklärung: nur das Logo; die Kopfzeile bleibt leer (nur die blaue Linie), weil der
    Name schon im Logo steht.
- Auf den Einstiegsseiten der Bildungsgänge steht in der Kopfzeile der volle Name (grau),
  die Überschrift ist das Kürzel („BF2“). Kacheln der Bildungsgänge auf der Startseite in
  Akzentlila: Rand oben, Kürzel fett, Füllung `#EBE5EF`.
- Überschrift mittig in Indie Flower, Blau `#0072B2`; auf der Themenseite Grün `#26870C` (das Thema).
- **Seitentitel** (`<title>`, erscheint im Tab und als Name von Lesezeichen), immer mit
  „happymatty“ klein und zusammen vorn, getrennt durch Schrägstriche ohne Leerzeichen:

  | Seite | Seitentitel |
  |---|---|
  | Startseite | `happymatty` |
  | Datenschutzerklärung | `happymatty/Datenschutzerklärung` |
  | Bildungsgang | `happymatty/bf2` |
  | Thema | `happymatty/Lineare Funktionen` |
  | Probeklassenarbeit | `happymatty/Quadratische Funktionen/Probeklassenarbeit` |
  | Klassenarbeit | `happymatty/Quadratische Funktionen/Klassenarbeit` |
  | Übersicht des Arbeitsblatts | `happymatty/Mehr als nur steil` |
  | interaktive Seite | `happymatty/Mehr als nur steil/interaktiv` |
  | `…_Aufgabenblatt.pdf` | `happymatty/Mehr als nur steil/Aufgabenblatt` |
  | `…_Loesung.pdf` | `happymatty/Mehr als nur steil/Lösung` |
  | Tests | siehe Abschnitt „Tests“ |

  Bei der interaktiven Seite ersetzt Claude bei jeder Übernahme eines Artifacts den `<title>`.
  In die freigegebenen PDFs auf der Website (nicht ins Backup) trägt das Skript den Titel ein,
  wenn er fehlt oder nicht stimmt; Inhalt und Aussehen bleiben dabei gleich. Ohne Titel zeigen
  Browser nur den Dateinamen.
- Fußzeile mittig in Indie Flower: „CC BY-NC-SA 4.0 · Patrick Saul · Datenschutzerklärung · Impressum“, Name grün,
  Rest grau, darüber eine dünne blaue Linie. „Datenschutzerklärung“ im Standardgrau als Link auf
  `/datenschutz`, ohne Unterstreichung, beim Darüberfahren unterstrichen. Die interaktiven Seiten
  haben keine solche Fußzeile. Dort steht hinter der Versionsnummer ein kleines „Datenschutz“,
  durch „ · “ getrennt und so zurückhaltend wie die Versionsnummer (gleiche Größe und Farbe, ohne
  Unterstreichung, beim Darüberfahren unterstrichen); es öffnet `/datenschutz/` in einem neuen Tab
  (`target="_blank" rel="noopener"`). Claude setzt es bei jeder Übernahme eines Artifacts ein
  (Entscheidung 11.11.2026).
- **Zurück-Knopf der interaktiven Seiten** (Entscheidung 11.11.2026): Links vor dem Titel steht ein
  Pfeil „‹“ mit dem Symbol der Website, beides ein Link (`<a class="heim" id="heim" href="/">`).
  Ein Tipp darauf führt dorthin zurück, wo man herkam (`history.back()`, wenn die vorige Seite auf
  happymatty.de lag); bei einem Direktlink führt er zur Startseite. Nicht „Zurück“ beschriften:
  Unten gibt es meist schon einen Zurück-Knopf für die Schritte. Damit die Kopfleiste auch auf
  einem iPad im 4:3-Format passt, stehen Versionsnummer und „Datenschutz“ in der kleinen Zeile
  unter dem Titel, hinter dem Thema („Lineare Funktionen v1.22 · Datenschutz“); eine Formel o. Ä.
  fällt aus dieser Zeile weg. Claude setzt Knopf, Stil und Skript bei jeder Übernahme eines
  Artifacts ein, wie in `/lineare-funktionen/mehr-als-nur-steil/interaktiv` (Kommentar
  „happymatty: Zurück-Knopf“), und prüft die Kopfleiste bei 1024 × 768.
- **Datenschutzerklärung** (`/datenschutz`): Die Stand-Zeile trägt das Datum der Veröffentlichung.
  Der Abschnitt „Dein Recht auf Widerspruch“ steht abgesetzt im Kasten mit blauem Rand links
  (Klasse `kasten`), weil Art. 21 Abs. 4 DSGVO für diesen Hinweis eine getrennte Form verlangt.
- Fließtext Libertinus Sans. Einträge als Karten mit blauem Rand links, Titel in Indie Flower blau.
- Farben der Karten (Entscheidung 10.11.2026): Aufgabenblatt blau `#0072B2`; Probetest und
  Kurztest-Fassungen Akzentlila `#85609E` (Violett `#7A5195` aus dem Skill `mathe`, auf die Helligkeit
  des Akzentblaus angehoben), Füllung `#EBE5EF` (Klasse `test`);
  Lösungen orange `#D55E00` (Klasse `loesung`); interaktive Seiten grün `#26870C` (Klasse
  `interaktiv`); Notentabellen als Zusatz hellblau `#59A3CD` (Akzentblau 35 % aufgehellt), Titel etwas kleiner (Klasse
  `notentabelle`); nicht Veröffentlichtes grau gestrichelt (Klasse `gesperrt`): Titel in hellerem
  Grau `#9A9A9A`, deutlich heller als das Standardgrau, damit die Karte als „noch nicht da“ zurücktritt;
  der Hinweis darunter („Noch nicht freigeschaltet“) im Standardgrau (Entscheidung 10.11.2026: so lassen).
  Füllungen im Farbton ihrer Schrift und gleich hell wie die Füllungen zu
  Orange und Grün aus dem Skill (Aufgabenblatt `#E0EDF8`); die Notentabelle heller (`#F3F8FB`).
  Die Kacheln (Karten und Bildungsgang-Kacheln) tragen ihre Füllung immer; beim Darüberfahren
  mit der Maus und beim Antippen werden sie weiß (Entscheidung 11.11.2026: Auf iPad und Handy
  gibt es kein Darüberfahren, die Farben waren dort nur beim Tippen kurz zu sehen).
  Beim Aufhellen in OKLCH rechnen, nicht mit Weiß mischen: Gemischtes Blau kippt ins Türkis.
- **Symbol der Website** (Tab, Lesezeichen, Home-Bildschirm, Logo oben links): weißer Smiley auf
  Akzentblau, wie von Hand gezeichnet: zwei ovale Augen, darunter ein Lächeln mit dickem, leicht
  unregelmäßigem Strich; der Kopf ist um 17° gegen den Uhrzeigersinn gekippt (rechts höher), das
  Ganze steht waagerecht und senkrecht mittig (Entscheidung 11.11.2026, löst das „hm“ mit Lächeln
  vom 10.11.2026 ab; Patrick wollte einen echten Smiley, nicht glatt und nicht Standard).
  Vorlage als Vektorgrafik: `_werkzeuge/symbol.svg`. Dateien:
  `favicon.ico` (16, 32, 48 px) und `apple-touch-icon.png` (180 px) im Hauptordner,
  `stil/icon-32.png`, `stil/icon-192.png`; alle quadratisch ohne runde Ecken, die Seiten und
  Geräte runden selbst. Nach dem Ersetzen läuft das Skript (Kennungen im Kopf).
- Ändern sich die Farben oder die Kopfzeile im Skill `mathe`, zieht die Website nach.

## Inhalte auf den öffentlichen Seiten

- Patrick Saul darf als Autor genannt werden.
- Das Impressum ist geklärt und online (`/impressum`, Entscheidung 14.11.2026). Als Anschrift gilt
  ausschließlich die berufliche Anschrift „Patrick Saul, c/o BBS Betzdorf-Kirchen, Auf dem
  Molzberg 14, 57548 Kirchen“. Die private Anschrift kommt nie auf die Seite. Kontakt bleibt
  happymatty.de@gmail.com. Neue Seiten bekommen die Fußzeile mit Datenschutzerklärung und
  Impressum (Link `/impressum/`, im selben Grau und mit derselben Gestaltung); die interaktiven
  Seiten tragen hinter „Datenschutz“ ein „Impressum“.
- Nichts über Claude oder darüber, wie die Seiten entstehen.

## Herkunft der Seiten

Die interaktiven Seiten entstehen meist als Artifact in einem Claude-Projekt auf claude.ai.
Jede Seite muss ohne Claude laufen: kein `window.claude`, keine Artifact-Datenbank.
Möglichst keine Inhalte von fremden Servern laden (Datenschutz der Schüler).
Lädt eine Seite etwas von fremden Servern, setzt sie Cookies, speichert sie weitere Daten im
Browser oder kommt eine Statistik hinzu, passt Claude Code die Datenschutzerklärung im selben
Schritt an oder fragt vorher; ein Projektchat legt eine solche Seite nicht selbst ab, sondern
übergibt an Claude Code.

Die PDFs entstehen in Patricks Claude-Projekten. Von dort kommen sie auf zwei Wegen:

- **Direkt aus dem Projektchat** (in Erprobung, erster Lauf 14.11.2026): Der Projektchat legt
  die freigegebenen PDFs, `interaktiv/` und `_einheit.json` in den Ordner seiner Themeneinheit,
  lässt das Skript laufen und lädt hoch (siehe „Wer schreibt was“ und „Neue Themeneinheit
  anlegen“). Alle Dateien mit Versionsnummer, auch `.tex` und Lösungen, sichert er selbst im
  privaten Repository `happymatty-de/unterrichtsmaterial`; Regeln dort in der `CLAUDE.md`.
- **Über Claude Code:** Patrick lädt die Dateien in einer Sitzung hoch oder legt sie (auch als
  ZIP) in den Eingang. Claude Code legt sie unter ihrem Namen ohne Versionsnummer ab, schreibt die
  Beschreibungsdatei, lässt das Skript laufen und sichert alle Dateien im selben Schritt im Backup.

## Was veröffentlicht ist

Das steht nur in den Beschreibungsdateien (Entscheidung 14.11.2026: eine einzige Stelle; die frühere
Tabelle „Veröffentlichtes Material“ in dieser Datei entfiel). Übersicht mit Quelle und Stand:

```bash
python3 _werkzeuge/bauen.py --bestand
```

Frühere Adressen und Namen:
- Rechnen mit Zahlen hieß bis 10.11.2026 „Rationale Zahlen“ (`/rationale-zahlen`); der alte Link
  war nirgends weitergegeben und hat deshalb keine Weiterleitung (Entscheidung 10.11.2026).
- `/lineare-funktionen/kurztest-1` war am 10.11.2026 kurz online (mit zwei älteren Ständen des
  Probetests als PDF, entfallen am 12.11.2026) und leitete danach auf den Probetest von LF1 weiter.
  Die Weiterleitung entfiel am 14.11.2026 (Entscheidung Patrick: nicht nötig).
- `/lineare-funktionen/wie-steil-ist-das/LF1_Kurztest_1.pdf`, `LF1_Kurztest_2.pdf`,
  `LF1_Kurztest_Loesung_1.pdf`, `LF1_Kurztest_Loesung_2.pdf`, `LF1_Kurztest_Notentabelle.pdf`:
  online vom 12. bis 14.11.2026 (Fassungen 1 und 2 als Ausnahme), entfielen ohne Weiterleitung
  (Entscheidung 14.11.2026: Der Probetest reicht). Mit ihnen entfiel der Abschnitt „Kurztest“ auf
  der Übersicht von LF1.
