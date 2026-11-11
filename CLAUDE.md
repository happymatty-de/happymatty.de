# happymatty.de

Dieses Repository ist die Website `happymatty.de`. Sie wird über GitHub Pages ausgeliefert.
Hier liegen Arbeitsblätter (PDF) und interaktive Seiten für den Unterricht.
Sie sind ohne Login per Link erreichbar und hängen nicht an Claude.

## Rückmeldung im Chat

Nach erledigter Arbeit nur eine kurze Statusmeldung („Alles umgesetzt.“). Details nur, wenn etwas
nicht funktioniert hat, wenn Claude deutlich vom Auftrag abgewichen ist oder wenn Patrick etwas
entscheiden oder tun muss. Kleine Verbesserungen, die Claude selbst vornimmt, werden nicht
gemeldet (Entscheidung 10.11.2026: Viel Text lässt Wichtiges untergehen).

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
  alle Links darauf, die Schriften, und dass kein `.tex` und keine Lösung im Repository liegt,
  die nicht in „Veröffentlichtes Material“ als freigegeben steht.
- Nach dem Hochladen wartet Claude mit `python3 _werkzeuge/warten_bis_online.py`, bis GitHub
  Pages fertig ist, und meldet erst dann „online“. Die Veröffentlichung dauert mal unter einer
  Minute, mal mehrere Minuten (Anlass 10.11.2026: Patrick beurteilte Farben, bevor sie online
  waren). Danach genügt in Safari Wahltaste + Cmd + R.
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
- **Text unter dem Kartentitel** sagt, wozu die Schüler die Datei nutzen, nicht was man technisch
  damit tun kann; dahinter in Klammern Dateiart und Seitenzahl (Entscheidung 10.11.2026: Kaum ein
  Schüler druckt selbst aus, sie laden die PDFs aufs iPad):

  | Karte | Text |
  |---|---|
  | Aufgabenblatt | „Zum Arbeiten und Lernen (PDF, n Seiten)“ |
  | Musterlösung, Lösungen zu Tests | „Zum Vergleichen (PDF, n Seiten)“ |
  | Probetest | „Zum Üben vor dem Kurztest (PDF, n Seiten)“ |
  | Probeklassenarbeit | „Zum Üben vor der Klassenarbeit (PDF, n Seiten)“ |
  | Kurztest-Fassung | „Zum Üben (PDF, n Seiten)“ |
  | Notentabelle | „Welche Note zu deinen Punkten gehört (PDF, 1 Seite)“ |

  Die Seitenzahl prüft Claude bei jedem neuen oder ersetzten PDF gegen die Datei.

## Tests: Probetest, Kurztest, Klassenarbeit

In BF1 und BF2 gehört jeder Test zu genau einer Themeneinheit. Er steht auf ihrer Übersicht
unter den drei Karten, je Testart in einem eigenen Abschnitt (Überschrift `themenkopf` mit `id`).
Keine eigene Seite, keine Nummer: „Kurztest 1“ verwechselt man mit Fassung 1.

- **Probetest: wird immer veröffentlicht**, zusammen mit Lösung und Notentabelle, sobald
  Patrick ihn schickt (Entscheidung 10.11.2026: Der Probetest dient der Selbstkontrolle).
- **Kurztest: wird normalerweise nicht veröffentlicht**, weil Patrick ihn wieder einsetzt.
  Es gibt dann keinen Abschnitt und keine graue Karte. Nur wenn Patrick Fassungen ausdrücklich
  freigibt, entsteht der Abschnitt „Kurztest“ mit diesen Fassungen, ihren Lösungen und der
  Notentabelle. **Fassungen, die noch eine Klasse schreibt, kommen nie auf die Website.**
- **Klassenarbeiten** (z. B. BGY) decken meist mehrere Themeneinheiten ab und stehen auf der
  Ebene des Themas (Entscheidung 10.11.2026, erste: Quadratische Funktionen):
  - Veröffentlicht wird nur die **Probeklassenarbeit**, immer mit Lösung und Notentabelle
    (wie der Probetest). Die Klassenarbeit selbst kommt nie auf die Website.
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

| Datei | Inhalt | PDF-Titel |
|---|---|---|
| `probetest.pdf` | Probetest (es gibt nur eine Fassung) | `happymatty/<Titel>/Probetest` |
| `probetest-loesung.pdf` | Lösung zum Probetest | `happymatty/<Titel>/Lösung Probetest` |
| `probetest-notentabelle.pdf` | Notentabelle zum Probetest | `happymatty/<Titel>/Notentabelle Probetest` |
| `kurztest-fassung-<n>.pdf` | freigegebene Fassung des Kurztests | `happymatty/<Titel>/Kurztest Fassung <n>` |
| `kurztest-fassung-<n>-loesung.pdf` | Lösung dazu | `happymatty/<Titel>/Lösung Kurztest Fassung <n>` |
| `kurztest-notentabelle.pdf` | Notentabelle zum Kurztest | `happymatty/<Titel>/Notentabelle Kurztest` |
| `probeklassenarbeit/probeklassenarbeit.pdf` | Probeklassenarbeit (im Ordner des Themas) | `happymatty/<Thema>/Probeklassenarbeit` |
| `probeklassenarbeit/probeklassenarbeit-loesung.pdf` | Lösung zur Probeklassenarbeit | `happymatty/<Thema>/Lösung Probeklassenarbeit` |
| `probeklassenarbeit/probeklassenarbeit-notentabelle.pdf` | Notentabelle zur Probeklassenarbeit | `happymatty/<Thema>/Notentabelle Probeklassenarbeit` |

- **Notentabellen werden immer mit veröffentlicht**, wenn der zugehörige Test online geht.
  Karte „Notentabelle zum …“, Text „Welche Note zu deinen Punkten gehört (PDF, 1 Seite)“.
  Zwischen Zahl und „Seite(n)“ steht immer ein geschütztes Leerzeichen (`&nbsp;`).
- Karten je Abschnitt: Test (violett, Klasse `test`), Lösung (orange), Notentabelle (hellblau, Klasse `notentabelle`); beim Kurztest je
  Fassung Test und Lösung, danach die Notentabelle.
- Themenseite: in der Beschreibung der Themeneinheit
  „· mit Probetest“ bzw. „· mit Probetest und Kurztest“.

Alte Adresse: `/lineare-funktionen/kurztest-1` war am 10.11.2026 kurz online und leitet auf
`/lineare-funktionen/wie-steil-ist-das/#probetest` weiter.

## Lösungen

- Das Repository ist öffentlich: Alles, was darin liegt, kann jeder finden, auch ohne Link.
  Lösungen kommen deshalb erst ins Repository, wenn Patrick sie ausdrücklich freigibt.
  Bis dahin liegen sie nur im privaten Backup `happymatty-de/unterrichtsmaterial`.
  Ein ausgegrauter Link schützt nicht: Die Adresse `…/loesung.pdf` ist erratbar, und das
  Repository ist öffentlich einsehbar.
- Freischalten: Patrick schreibt z. B. „Lösung LF2 freigeben“. Claude kopiert die Lösung
  aus dem Backup als `loesung.pdf`, trägt den PDF-Titel ein, macht die Karte aktiv und orange
  („Zum Vergleichen (PDF, n Seiten)“) und trägt sie in „Veröffentlichtes Material“ ein.
  Kommt später eine neue Version des Blatts, ersetzt Claude eine freigegebene Lösung mit.
- Ein passwortgeschützter Bereich für Lehrkräfte ist geplant, aber noch nicht gebaut.

## Startseite, Themenseiten und Bildungsgänge

Zwei Wege zum Material (Entscheidung 10.11.2026): nach Thema für alle, nach Bildungsgang für die Schüler.

- **Startseite** `index.html` (`happymatty.de`): unter der Überschrift „Unterrichtsmaterial“ die Zeile
  „von Patrick Saul“ in Indie Flower grün (Klasse `unterzeile autor`, Entscheidung 11.11.2026). Darunter „Klassen“ mit einer Kachel je
  Bildungsgang (Entscheidung 11.11.2026: knapp wie „Themenbereiche“, vorher „Meine Klasse“), darunter unter „Themenbereiche“ die **Themen** als grüne Karten (Klasse `thema-karte`) mit
  Kennzeichen der Bildungsgänge und Zahl der Themeneinheiten („2 Themeneinheiten“). Keine Titel
  einzelner Arbeitsblätter auf der Startseite. Auch ältere Themen bleiben stehen, damit jedes
  Material auffindbar bleibt.
  **Reihenfolge** (Entscheidung 10.11.2026): erst alle Themen der BF1, dann der BF2, dann des BGY
  (danach FSTM, DBOS); innerhalb eines Bildungsgangs in der Reihenfolge, in der die Reihen
  unterrichtet werden, nicht alphabetisch. Zwischen den Bildungsgängen eine gestrichelte Linie
  in Akzentlila (`<hr class="trenner">`, je Bildungsgang eine eigene `<ul class="liste">`),
  zwischen Themen desselben Bildungsgangs keine. Ein Thema für mehrere Bildungsgänge: Claude fragt.
  Zwischen Titel und Kennzeichen kann eine **Unterzeile** (Klasse `unterzeile`, im Standardgrau
  wie der Text darunter) stehen: die Teile des Themas, mit Mittelpunkt getrennt, so wie Patrick sie vorgibt
  (Rechnen mit Zahlen: „Rationale Zahlen · Rechenregeln · Überschlagen und Schätzen“).
- **Themenseite** `<thema>/index.html` (z. B. `happymatty.de/lineare-funktionen`): Kopfzeile nur
  „Mathematik“, Überschrift das Thema groß in Grün (`<h1 class="thema">`, Entscheidung 10.11.2026:
  der Haupttitel soll sofort ins Auge fallen). Darunter der Abschnitt „Themeneinheiten“
  (`themenkopf`, grau; nicht „Arbeitsblätter“, weil auch interaktive Seiten dazugehören):
  alle Themeneinheiten des Themas in der Reihenfolge der Lernreihe, je mit Titel, Kennzeichen der
  Bildungsgänge und einer kurzen Beschreibung. Laufen in einem Thema mehrere Bildungsgänge mit
  eigenen Blättern (etwa BGY als Wiederholung auf höherem Niveau), stehen sie hier nebeneinander.
  Die Beschreibung beginnt mit dem Teilthema, danach ein Gedankenstrich: „Addition und
  Subtraktion – Zahlenkarten, Wege und Zahlenmauern“. Danach gegebenenfalls der Abschnitt
  „Probeklassenarbeit“ (siehe Tests).
- **Einstiegsseite je Bildungsgang** `<kürzel>/index.html` (z. B. `happymatty.de/bf2`): nur die
  **Themen**, die dieser Bildungsgang bearbeitet, keine einzelnen Themeneinheiten (Entscheidung
  10.11.2026: sonst wird es zu viel). Je Fach eine Überschrift (`themenkopf`, „Mathematik“), darunter
  die Themen als grüne Karten wie auf der Startseite (mit Unterzeile und Zahl der Themeneinheiten,
  ohne Kennzeichen), in der Reihenfolge, in der sie unterrichtet werden. Ohne Material eine graue Karte „Noch kein Material“. Die Schüler speichern sich diesen
  einen Link.
- **Übersicht des Arbeitsblatts**: unter der Überschrift die Kennzeichen der Bildungsgänge.
- **Kennzeichen** (Klasse `badge`) in der Form der Badges auf den Blättern, aber in Akzentlila:
  Rahmen und Schrift `#85609E`, gefüllt `#EBE5EF`, Indie Flower (Skill `mathe`, Stand 10.11.2026).
- Wird ein Arbeitsblatt neu veröffentlicht, umbenannt oder bekommt es einen neuen Titel oder
  Bildungsgang, trägt Claude das im selben Schritt überall ein: Übersicht, Themenseite,
  Einstiegsseiten der Bildungsgänge (Zahl) und Startseite (Zahl, Kennzeichen). Ein neues Thema bekommt
  eine Themenseite und eine Karte auf der Startseite.
- Welcher Bildungsgang ein Blatt bearbeitet, steht im Namen des Reihenplans
  (`BF2_Reihenplan_…`); im Zweifel fragt Claude.

Bildungsgänge:

| Kürzel | Link | Name | Stand |
|---|---|---|---|
| BF1 | `/bf1` | Berufsfachschule I | aktiv |
| BF2 | `/bf2` | Berufsfachschule II | aktiv |
| BGY | `/bgy` | Berufliches Gymnasium | aktiv, ein Jahrgang |
| FSTM | `/fstm` | Techniker-Abendschule (BWL) | ab Januar 2027, Seite dann anlegen |
| DBOS | `/dbos` | Duale Berufsoberschule | ab Schuljahr 2027/28, Seite dann anlegen |

Reservierte Ordner, nie als Thema: `stil`, `bf1`, `bf2`, `bgy`, `fstm`, `dbos`, `datenschutz`.
Gemeinsame Gestaltung liegt in `stil/` (`basis.css` und die Schriften).

**Nach jeder Änderung an `basis.css` oder am Symbol der Website** und bei jeder neuen Seite
(auch bei jeder Übernahme eines Artifacts) führt Claude `python3 _werkzeuge/stil_version.py` aus. Das Skript hängt an
jeden Verweis auf `/stil/basis.css` eine Kennung aus dem Inhalt der Datei an (`?v=…`) und
ergänzt fehlende Verweise auf das Symbol der Website. Sonst zeigen Browser
bis zu einigen Stunden die alte Gestaltung aus dem Zwischenspeicher (Anlass 10.11.2026:
Safari zeigte den alten Abstand am Kennzeichen noch nach mehreren Minuten).
Die Verweise auf das Symbol im Kopf der Seite (`favicon.ico`, `stil/icon-32.png`,
`apple-touch-icon.png`) bekommen ebenso eine Kennung aus dem Inhalt der Bilddatei
(Anlass 11.11.2026: Safari auf dem iPad zeigte nach dem Wechsel zum Smiley weiter das alte „hm“,
auch nach dem Löschen des Verlaufs).
Ordner, die mit `_` beginnen, veröffentlicht GitHub Pages nicht.

## Gestaltung

Startseite, Themenseiten und Übersichten sehen aus wie die Arbeitsblätter
(Skill `mathe`, Gestaltung: Schriften, Farben, Kopf- und Fußzeile, Überschrift):

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
  - Themenseite: zurück zu ihrem Bildungsgang („← BF1“ auf `/bf1/`), nicht zur Startseite
    (Entscheidung 11.11.2026). Gehört ein Thema zu mehreren Bildungsgängen, fragt Claude nach.
  - Übersicht einer Themeneinheit, Probeklassenarbeit: zurück zum Thema („← Lineare Funktionen“).
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
  | Übersicht des Arbeitsblatts | `happymatty/Mehr als nur steil` |
  | interaktive Seite | `happymatty/Mehr als nur steil/interaktiv` |
  | `aufgabenblatt.pdf` | `happymatty/Mehr als nur steil/Aufgabenblatt` |
  | `loesung.pdf` | `happymatty/Mehr als nur steil/Lösung` |
  | Tests | siehe Abschnitt „Tests“ |

  Bei der interaktiven Seite ersetzt Claude bei jeder Übernahme eines Artifacts den `<title>`.
  In die PDFs auf der Website (nicht ins Backup) trägt Claude den Titel mit
  `python3 _werkzeuge/pdf_titel.py <datei.pdf> "<Titel>"` ein, bei jedem neuen oder ersetzten
  PDF; Inhalt und Aussehen bleiben dabei gleich. Ohne Titel zeigen Browser nur den Dateinamen.
- Fußzeile mittig in Indie Flower: „CC BY-NC-SA 4.0 · Patrick Saul · Datenschutzerklärung“, Name grün,
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
  Geräte runden selbst.
- Ändern sich die Farben oder die Kopfzeile im Skill `mathe`, zieht die Website nach.

## Inhalte auf den öffentlichen Seiten

- Patrick Saul darf als Autor genannt werden.
- Kein Impressum und keine Anschrift, bis Patrick das Impressum klärt. Einzige Kontaktangabe ist
  die E-Mail-Adresse happymatty.de@gmail.com in der Datenschutzerklärung.
- Nichts über Claude oder darüber, wie die Seiten entstehen.

## Herkunft der Seiten

Die interaktiven Seiten entstehen meist als Artifact in einem Claude-Projekt auf claude.ai und werden von hier
übernommen. Jede Seite muss ohne Claude laufen: kein `window.claude`, keine Artifact-Datenbank.
Möglichst keine Inhalte von fremden Servern laden (Datenschutz der Schüler).
Lädt eine Seite etwas von fremden Servern, setzt sie Cookies, speichert sie weitere Daten im
Browser oder kommt eine Statistik hinzu, passt Claude die Datenschutzerklärung im selben Schritt
an oder fragt vorher.

Die PDFs entstehen in Patricks Claude-Projekten; Claude Code sieht diese Dateien nicht.
Patrick lädt sie hier im Chat oder auf GitHub hoch, Claude legt sie unter dem festen Namen ab.
Alle Dateien (auch `.tex` und Lösungen) sichert Claude im selben Schritt im privaten Repository
`happymatty-de/unterrichtsmaterial`; Ablauf dort in `CLAUDE.md`.

## Veröffentlichtes Material

| Link | Inhalt | Bildungsgang | Quelle | Stand |
|---|---|---|---|---|
| `/lineare-funktionen/wie-steil-ist-das/aufgabenblatt.pdf` | Aufgabenblatt | BF2 | `LF1_Wie_steil_ist_das_Aufgabenblatt_v24.pdf` | 10.11.2026 |
| `/lineare-funktionen/wie-steil-ist-das/loesung.pdf` | Musterlösung, freigegeben | BF2 | `LF1_Wie_steil_ist_das_Loesung_v24.pdf` | 10.11.2026 |
| `/lineare-funktionen/wie-steil-ist-das/probetest.pdf` | Probetest | BF2 | `LF1_Probetest_v14.pdf` | 10.11.2026 |
| `/lineare-funktionen/wie-steil-ist-das/probetest-loesung.pdf` | Lösung zum Probetest, freigegeben | BF2 | `LF1_Probetest_Loesung_v14.pdf` | 10.11.2026 |
| `/lineare-funktionen/wie-steil-ist-das/probetest-notentabelle.pdf` | Notentabelle zum Probetest | BF2 | `LF1_Probetest_Notentabelle_v14.pdf` | 10.11.2026 |
| `/lineare-funktionen/wie-steil-ist-das/kurztest-fassung-1.pdf` | Kurztest Fassung 1, freigegeben | BF2 | `LF1_Kurztest_1_v17.pdf` | 10.11.2026 |
| `/lineare-funktionen/wie-steil-ist-das/kurztest-fassung-1-loesung.pdf` | Lösung Fassung 1, freigegeben | BF2 | `LF1_Kurztest_Loesung_1_v17.pdf` | 10.11.2026 |
| `/lineare-funktionen/wie-steil-ist-das/kurztest-fassung-2.pdf` | Kurztest Fassung 2, freigegeben | BF2 | `LF1_Kurztest_2_v17.pdf` | 10.11.2026 |
| `/lineare-funktionen/wie-steil-ist-das/kurztest-fassung-2-loesung.pdf` | Lösung Fassung 2, freigegeben | BF2 | `LF1_Kurztest_Loesung_2_v17.pdf` | 10.11.2026 |
| `/lineare-funktionen/wie-steil-ist-das/kurztest-notentabelle.pdf` | Notentabelle zum Kurztest | BF2 | `LF1_Kurztest_Notentabelle_v17.pdf` | 10.11.2026 |
| `/lineare-funktionen/mehr-als-nur-steil/aufgabenblatt.pdf` | Aufgabenblatt | BF2 | `LF2_Mehr_als_nur_steil_Aufgabenblatt_v12.14.pdf` | 10.11.2026 |
| `/lineare-funktionen/mehr-als-nur-steil/interaktiv` | interaktiv | BF2 | Artifact „Mehr als nur steil – Lineare Funktionen (LF2)“ | 10.11.2026 |
| `/rechnen-mit-zahlen/ausschuss/aufgabenblatt.pdf` | Aufgabenblatt | BF1 | `Ausschuss_Aufgabenblatt_v11.1.pdf` | 10.11.2026 |
| `/rechnen-mit-zahlen/ausschuss/loesung.pdf` | Musterlösung, freigegeben | BF1 | `Ausschuss_Loesung_v11.1.pdf` | 10.11.2026 |
| `/rechnen-mit-zahlen/zahlenjagd/aufgabenblatt.pdf` | Aufgabenblatt | BF1 | `Zahlenjagd_Aufgabenblatt_v2.pdf` | 10.11.2026 |
| `/rechnen-mit-zahlen/zahlenjagd/loesung.pdf` | Musterlösung, freigegeben | BF1 | `Zahlenjagd_Loesung_v2.pdf` | 10.11.2026 |
| `/rechnen-mit-zahlen/zahlenjagd/probetest.pdf` | Probetest | BF1 | `Zahlenjagd_Probetest_v2.pdf` | 10.11.2026 |
| `/rechnen-mit-zahlen/zahlenjagd/probetest-loesung.pdf` | Lösung zum Probetest, freigegeben | BF1 | `Zahlenjagd_Probetest_Loesung_v2.pdf` | 10.11.2026 |
| `/rechnen-mit-zahlen/zahlenjagd/probetest-notentabelle.pdf` | Notentabelle zum Probetest | BF1 | `Zahlenjagd_Probetest_Notentabelle_v2.pdf` | 10.11.2026 |
| `/rechnen-mit-zahlen/mal-geteilt-und-das-minus/aufgabenblatt.pdf` | Aufgabenblatt | BF1 | `Mal_geteilt_und_das_Minus_Aufgabenblatt_v2.pdf` | 10.11.2026 |
| `/rechnen-mit-zahlen/mal-geteilt-und-das-minus/loesung.pdf` | Musterlösung, freigegeben | BF1 | `Mal_geteilt_und_das_Minus_Loesung_v2.pdf` | 10.11.2026 |
| `/rechnen-mit-zahlen/mal-geteilt-und-das-minus/probetest.pdf` | Probetest | BF1 | `Mal_geteilt_und_das_Minus_Probetest_v2.pdf` | 10.11.2026 |
| `/rechnen-mit-zahlen/mal-geteilt-und-das-minus/probetest-loesung.pdf` | Lösung zum Probetest, freigegeben | BF1 | `Mal_geteilt_und_das_Minus_Probetest_Loesung_v2.pdf` | 10.11.2026 |
| `/rechnen-mit-zahlen/mal-geteilt-und-das-minus/probetest-notentabelle.pdf` | Notentabelle zum Probetest | BF1 | `Mal_geteilt_und_das_Minus_Probetest_Notentabelle_v2.pdf` | 10.11.2026 |
| `/quadratische-funktionen/vom-term-zur-parabel/aufgabenblatt.pdf` | Aufgabenblatt | BGY | `QF1_Vom_Term_zur_Parabel_Aufgabenblatt_v13.1.pdf` | 10.11.2026 |
| `/quadratische-funktionen/vom-term-zur-parabel/loesung.pdf` | Musterlösung, freigegeben | BGY | `QF1_Vom_Term_zur_Parabel_Loesung_v13.1.pdf` | 10.11.2026 |
| `/quadratische-funktionen/nullstellen-ohne-formel/aufgabenblatt.pdf` | Aufgabenblatt | BGY | `QF2_Nullstellen_ohne_Formel_Aufgabenblatt_v16.1.pdf` | 10.11.2026 |
| `/quadratische-funktionen/nullstellen-ohne-formel/loesung.pdf` | Musterlösung, freigegeben | BGY | `QF2_Nullstellen_ohne_Formel_Loesung_v16.1.pdf` | 10.11.2026 |
| `/quadratische-funktionen/die-pq-formel/aufgabenblatt.pdf` | Aufgabenblatt | BGY | `QF3_Die_pq-Formel_Aufgabenblatt_v12.pdf` | 10.11.2026 |
| `/quadratische-funktionen/die-pq-formel/loesung.pdf` | Musterlösung, freigegeben | BGY | `QF3_Die_pq-Formel_Loesung_v12.pdf` | 10.11.2026 |
| `/quadratische-funktionen/nullstellen-bestimmen-die-funktion/aufgabenblatt.pdf` | Aufgabenblatt | BGY | `QF4_Nullstellen_bestimmen_die_Funktion_Aufgabenblatt_v26.1.pdf` | 10.11.2026 |
| `/quadratische-funktionen/nullstellen-bestimmen-die-funktion/loesung.pdf` | Musterlösung, freigegeben | BGY | `QF4_Nullstellen_bestimmen_die_Funktion_Loesung_v26.1.pdf` | 10.11.2026 |
| `/quadratische-funktionen/der-korbwurf/aufgabenblatt.pdf` | Aufgabenblatt | BGY | `QF5_Der_Korbwurf_Aufgabenblatt_v47.pdf` | 10.11.2026 |
| `/quadratische-funktionen/der-korbwurf/loesung.pdf` | Musterlösung, freigegeben | BGY | `QF5_Der_Korbwurf_Loesung_v47.pdf` | 10.11.2026 |
| `/quadratische-funktionen/probeklassenarbeit/probeklassenarbeit.pdf` | Probeklassenarbeit | BGY | `QF_Probeklassenarbeit_v6.pdf` | 10.11.2026 |
| `/quadratische-funktionen/probeklassenarbeit/probeklassenarbeit-loesung.pdf` | Lösung zur Probeklassenarbeit, freigegeben | BGY | `QF_Probeklassenarbeit_Loesung_v6.pdf` | 10.11.2026 |
| `/quadratische-funktionen/probeklassenarbeit/probeklassenarbeit-notentabelle.pdf` | Notentabelle zur Probeklassenarbeit | BGY | `QF_Probeklassenarbeit_Notentabelle_v6.pdf` | 10.11.2026 |

Die ganze Reihe Lineare Funktionen läuft derzeit nur in der BF2, die Reihe Rechnen mit Zahlen nur in der BF1, die Reihe
Quadratische Funktionen nur im BGY (alle Musterlösungen freigegeben 10.11.2026).
Rechnen mit Zahlen hieß bis 10.11.2026 „Rationale Zahlen“ (`/rationale-zahlen`); der alte Link war
nirgends weitergegeben und hat deshalb keine Weiterleitung (Entscheidung 10.11.2026).

Noch nicht freigegeben: Lösung zu „Mehr als nur steil“ (`LF2_Mehr_als_nur_steil_Loesung_v12.14.pdf`).
Kurztest LF1 Fassung 3 und 4 (v17) mit Lösungen: nicht veröffentlichen, im Einsatz ab 11.11.2026.
Kurztest LF1 Fassung 5 für Nachschreiber: folgt, nur ins Backup, nie veröffentlichen
(Fassung 1 und 2 sind öffentlich und taugen nicht mehr zum Nachschreiben).
Interaktive Seiten zu LF1 (Artifacts „Steil-Check“, „Steigung ablesen“): vorerst nicht veröffentlichen.
Rechnen mit Zahlen (BF1): Lösungen aller drei Aufgabenblätter freigegeben (10.11.2026). Kurztests aller drei Einheiten nur im
Backup.
