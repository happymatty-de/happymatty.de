#!/usr/bin/env python3
"""Baut alle Übersichten von happymatty.de aus den Beschreibungsdateien und prüft das Repository.

Aufruf im Hauptordner des Repositorys:
    python3 _werkzeuge/bauen.py             prüfen, dann bauen
    python3 _werkzeuge/bauen.py --pruefen   nur prüfen und sagen, was sich ändern würde; schreibt nichts
    python3 _werkzeuge/bauen.py --bestand   prüfen, dann auflisten, was veröffentlicht ist

Braucht pikepdf (einmal je Sitzung: pip install pikepdf).

Beschreibungsdateien (Format: CLAUDE.md, Abschnitt „Beschreibungsdateien“):
    <thema>/_thema.json              Titel, Unterzeile, Reihenfolge, Probeklassenarbeit, Klassenarbeit
    <thema>/<einheit>/_einheit.json  alles über eine Themeneinheit und ihre Dokumente
Dateien und Ordner mit _ am Anfang liefert GitHub Pages nicht aus.

Gebaut werden: Startseite, Einstiegsseiten der Bildungsgänge, Themenseiten, die Übersicht jeder
Themeneinheit, die Seiten /<thema>/probeklassenarbeit und /<thema>/klassenarbeit.
Nicht gebaut und nicht angefasst werden interaktive Seiten, Datenschutzerklärung, Impressum und
Weiterleitungen; bei ihnen erneuert das Skript nur die Kennungen ?v=… im Kopf (siehe unten).
PDFs werden nie neu erzeugt; fehlt einem freigegebenen PDF der Titel, trägt das Skript ihn ein.

Das Skript bricht ab, ohne etwas zu schreiben, wenn
  - irgendwo im Repository eine .tex liegt,
  - ein PDF im Repository liegt, das in keiner Beschreibungsdatei als freigegeben steht,
  - ein als freigegeben eingetragenes PDF oder eine interaktive Seite fehlt
    oder eine interaktive Seite liegt, die nicht freigegeben ist,
  - eine Beschreibungsdatei fehlt, unvollständig ist oder unbekannte Einträge hat,
  - ein Test ohne seine Lösung oder Notentabelle freigegeben ist,
  - ein Ordner oder eine Datei auftaucht, die das Skript nicht kennt.

Kennungen im Kopf jeder Seite (früher stil_version.py): An jeden Verweis auf /stil/basis.css und
auf das Symbol der Website (favicon.ico, stil/icon-32.png, apple-touch-icon.png) kommt eine
Kennung aus dem Inhalt der Datei (?v=…). Ändert sich die Datei, ändert sich die Adresse, und die
Browser laden sie neu, statt die alte aus dem Zwischenspeicher zu zeigen (Anlässe 10. und
11.11.2026: Safari zeigte alte Abstände und das alte Symbol)."""
import datetime
import hashlib
import html
import json
import pathlib
import re
import sys

WURZEL = pathlib.Path(__file__).resolve().parent.parent

# ------------------------------------------------------------------ feste Angaben (ändert nur Claude Code)

# Reihenfolge = Reihenfolge auf der Startseite. „seite“: Einstiegsseite /<kürzel> wird gebaut.
BILDUNGSGAENGE = {
    'BF1': {'name': 'Berufsfachschule I', 'kachel': 'Berufs&shy;fachschule&nbsp;I', 'seite': True},
    'BF2': {'name': 'Berufsfachschule II', 'kachel': 'Berufs&shy;fachschule&nbsp;II', 'seite': True},
    'BGY': {'name': 'Berufliches Gymnasium', 'kachel': 'Berufliches Gymnasium', 'seite': True},
    'FSTM': {'name': 'Techniker-Abendschule', 'kachel': None, 'seite': False},   # ab Januar 2027
    'DBOS': {'name': 'Duale Berufsoberschule', 'kachel': None, 'seite': False},  # ab Schuljahr 2027/28
}
BEREICHE = ['Grundlagen']        # vorgesehen, noch ohne eigene Seite
FAECHER = ['Mathematik', 'BWL']  # Reihenfolge der Überschriften auf den Einstiegsseiten
RESERVIERT = {'stil', 'bf1', 'bf2', 'bgy', 'fstm', 'dbos', 'datenschutz', 'impressum'}

KOPF = '''<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titel}</title>
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/stil/icon-32.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="stylesheet" href="/stil/basis.css">
</head>
<body>
<main class="seite">

'''
FUSS = ('  <footer>CC BY-NC-SA 4.0 · <span class="name">Patrick Saul</span> · '
        '<a href="/datenschutz/">Datenschutzerklärung</a> · <a href="/impressum/">Impressum</a></footer>\n'
        '\n</main>\n</body>\n</html>\n')
LOGO = '<img src="/stil/icon-192.png" alt=""><span>happymatty.de</span>'

ZWECK = {  # Text unter dem Kartentitel, vor „(PDF, n Seiten)“
    'aufgabenblatt': 'Zum Arbeiten und Lernen',
    'loesung': 'Zum Vergleichen',
    'probetest': 'Zum Üben vor dem Kurztest',
    'probeklassenarbeit': 'Zum Üben vor der Klassenarbeit',
    'ueben': 'Zum Üben',
    'notentabelle': 'Welche Note zu deinen Punkten gehört',
}
GESPERRT_LOESUNG = 'Noch nicht freigeschaltet'
GESPERRT_INTERAKTIV = 'Noch nicht vorhanden'
GESPERRT_KLASSENARBEIT = 'Wird am Freitag nach der Klassenarbeit veröffentlicht'

# ------------------------------------------------------------------ Fehler sammeln

fehler = []
unlesbar = set()  # Ordner, deren Beschreibungsdatei nicht lesbar ist: keine Folgefehler zu ihren PDFs


def rel(pfad):
    return pfad.relative_to(WURZEL).as_posix()


def melde(ort, text):
    fehler.append(f'{ort}: {text}')


def esc(text):
    return html.escape(text, quote=False)


# ------------------------------------------------------------------ Beschreibungsdateien lesen und prüfen

DATUM = re.compile(r'^\d{2}\.\d{2}\.\d{4}$')
QUELLE_PDF = re.compile(r'^[^/\\\s]+_v\d+(?:\.\d+)*\.pdf$')
KENNUNG = re.compile(r'^[A-Z]+\d*$')
ORDNERNAME = re.compile(r'^[a-z0-9]+(?:-[a-z0-9]+)*$')


def lies_json(pfad):
    try:
        return json.loads(pfad.read_text(encoding='utf-8'))
    except json.JSONDecodeError as e:
        melde(rel(pfad), f'kein gültiges JSON (Zeile {e.lineno}, Spalte {e.colno}: {e.msg})')
    return None


def schluessel(ort, obj, pflicht, frei=()):
    """Prüft, dass obj ein Objekt mit allen Pflichteinträgen und keinen unbekannten ist."""
    if not isinstance(obj, dict):
        melde(ort, 'muss ein Objekt { … } sein')
        return False
    for k in pflicht:
        if k not in obj:
            melde(ort, f'„{k}“ fehlt')
    for k in obj:
        if k not in pflicht and k not in frei:
            melde(ort, f'unbekannter Eintrag „{k}“ (Tippfehler?)')
    return True


def wert(ort, obj, k, art, leer=False):
    """Liest obj[k] und prüft den Typ: 'text', 'zahl', 'janein', 'liste' (Liste von Texten)."""
    v = obj.get(k)
    if v is None:
        if not leer and k in obj:
            melde(ort, f'„{k}“ darf nicht null sein')
        return None
    ok = {'text': isinstance(v, str) and v.strip() != '',
          'zahl': isinstance(v, int) and not isinstance(v, bool) and v >= 1,
          'janein': isinstance(v, bool),
          'liste': isinstance(v, list) and all(isinstance(x, str) for x in v)}[art]
    if not ok:
        soll = {'text': 'ein nicht leerer Text', 'zahl': 'eine ganze Zahl ab 1',
                'janein': 'true oder false', 'liste': 'eine Liste von Texten'}[art]
        melde(ort, f'„{k}“ muss {soll} sein')
        return None
    return v


def bildungsgaenge(ort, obj, k='bildungsgaenge'):
    liste = wert(ort, obj, k, 'liste') or []
    if k in obj and not liste:
        melde(ort, f'„{k}“ braucht mindestens einen Bildungsgang')
    for b in liste:
        if b not in BILDUNGSGAENGE:
            melde(ort, f'unbekannter Bildungsgang „{b}“ (bekannt: {", ".join(BILDUNGSGAENGE)})')
        elif not BILDUNGSGAENGE[b]['seite']:
            melde(ort, f'Bildungsgang „{b}“ hat noch keine Seite; die legt nur Claude Code an')
    if len(set(liste)) != len(liste):
        melde(ort, f'„{k}“ nennt einen Bildungsgang doppelt')
    return sorted(set(liste) & set(BILDUNGSGAENGE), key=list(BILDUNGSGAENGE).index)


class Dok:
    """Ein Dokument: vorhanden, freigegeben, Quelle (mit Versionsnummer), Stand, Hinweis."""

    def __init__(self, ort, d, ordner, interaktiv=False):
        self.ort, self.ordner, self.interaktiv = ort, ordner, interaktiv
        self.vorhanden = self.freigegeben = False
        self.quelle = self.stand = self.hinweis = self.text = None
        frei = ('quelle', 'stand', 'hinweis') + (('text',) if interaktiv else ())
        if d is None or not schluessel(ort, d, ('vorhanden', 'freigegeben'), frei):
            return
        self.vorhanden = bool(wert(ort, d, 'vorhanden', 'janein'))
        self.freigegeben = bool(wert(ort, d, 'freigegeben', 'janein'))
        self.quelle = wert(ort, d, 'quelle', 'text', leer=True)
        self.stand = wert(ort, d, 'stand', 'text', leer=True)
        self.hinweis = wert(ort, d, 'hinweis', 'text', leer=True)
        if interaktiv:
            self.text = wert(ort, d, 'text', 'text', leer=True)
        if self.freigegeben and not self.vorhanden:
            melde(ort, 'freigegeben, aber nicht vorhanden')
        if self.vorhanden and not self.quelle:
            melde(ort, 'vorhanden, aber „quelle“ fehlt')
        if self.quelle and not interaktiv and not QUELLE_PDF.match(self.quelle):
            melde(ort, f'„quelle“ muss der Dateiname mit Versionsnummer sein, z. B. '
                       f'„LF1_Probetest_v14.pdf“, nicht „{self.quelle}“')
        if self.freigegeben and not self.stand:
            melde(ort, 'freigegeben, aber „stand“ (Datum der Veröffentlichung) fehlt')
        if self.stand:
            try:
                if not DATUM.match(self.stand):
                    raise ValueError
                datetime.datetime.strptime(self.stand, '%d.%m.%Y')
            except ValueError:
                melde(ort, f'„stand“ muss ein Datum wie 14.11.2026 sein, nicht „{self.stand}“')
        if interaktiv and self.freigegeben and not self.text:
            melde(ort, 'freigegeben, aber „text“ (Zeile unter dem Kartentitel) fehlt')

    @property
    def pfad(self):
        """Ort auf der Website: PDF unter dem Namen aus „quelle“ ohne _v…, interaktiv/ als Ordner."""
        if self.interaktiv:
            return self.ordner / 'interaktiv'
        if self.quelle and QUELLE_PDF.match(self.quelle):
            return self.ordner / re.sub(r'_v\d+(?:\.\d+)*\.pdf$', '.pdf', self.quelle)
        return None


class Eintrag:
    """Ein Dokument mit allem, was die Übersichten und die Prüfung über es wissen müssen."""

    def __init__(self, dok, inhalt, karte, zweck, klasse, pdf_titel, bg):
        self.dok, self.inhalt, self.karte, self.zweck, self.klasse = dok, inhalt, karte, zweck, klasse
        self.pdf_titel, self.bildungsgaenge = pdf_titel, bg


def testgruppe(ort, d, ordner, frei=()):
    """Probetest, Probeklassenarbeit oder Klassenarbeit: test, loesung, notentabelle."""
    if not schluessel(ort, d, ('test', 'loesung', 'notentabelle'), frei):
        return None
    g = {k: Dok(f'{ort} › {k}', d.get(k), ordner) for k in ('test', 'loesung', 'notentabelle')}
    frei_ = [g[k].freigegeben for k in g]
    if any(frei_) and not all(frei_):
        melde(ort, 'Test, Lösung und Notentabelle gehen nur zusammen online '
                   '(alle drei „freigegeben“: true oder alle false)')
    return g


class Einheit:
    def __init__(self, thema, ordner):
        self.thema, self.ordner = thema, ordner
        self.slug = ordner.name
        datei = ordner / '_einheit.json'
        ort = rel(datei)
        d = lies_json(datei)
        self.eintraege = []
        self.ok = d is not None and schluessel(ort, d, (
            'titel', 'kennung', 'teilthema', 'beschreibung', 'bildungsgaenge', 'bereiche', 'platz',
            'aufgabenblatt', 'musterloesung', 'interaktiv'), ('probetest', 'kurztest'))
        if not self.ok:
            unlesbar.add(ordner)
            return
        self.titel = wert(ort, d, 'titel', 'text') or self.slug
        self.kennung = wert(ort, d, 'kennung', 'text', leer=True)
        if self.kennung and not KENNUNG.match(self.kennung):
            melde(ort, f'„kennung“ sieht aus wie LF1 oder QF5, nicht „{self.kennung}“')
        self.teilthema = wert(ort, d, 'teilthema', 'text', leer=True)
        if 'teilthema' in d and not self.teilthema:
            melde(ort, '„teilthema“ fehlt; Patrick fragen (siehe CLAUDE.md, Begriffe)')
        self.beschreibung = wert(ort, d, 'beschreibung', 'text') or ''
        self.bildungsgaenge = bildungsgaenge(ort, d)
        self.bereiche = wert(ort, d, 'bereiche', 'liste') or []
        for b in self.bereiche:
            if b not in BEREICHE:
                melde(ort, f'unbekannter Bereich „{b}“ (vorgesehen: {", ".join(BEREICHE)}; '
                           f'neue Bereiche legt nur Claude Code an)')
        self.platz = wert(ort, d, 'platz', 'zahl') or 0

        t, bg = self.titel, self.bildungsgaenge
        self.aufgabenblatt = Dok(f'{ort} › aufgabenblatt', d.get('aufgabenblatt'), ordner)
        self.musterloesung = Dok(f'{ort} › musterloesung', d.get('musterloesung'), ordner)
        self.interaktiv = Dok(f'{ort} › interaktiv', d.get('interaktiv'), ordner, interaktiv=True)
        if not self.aufgabenblatt.freigegeben:
            melde(ort, 'eine Themeneinheit erscheint erst mit ihrem Aufgabenblatt '
                       '(aufgabenblatt › „freigegeben“: true)')
        self.eintraege += [
            Eintrag(self.aufgabenblatt, 'Aufgabenblatt', 'Aufgabenblatt', ZWECK['aufgabenblatt'], None,
                    f'happymatty/{t}/Aufgabenblatt', bg),
            Eintrag(self.musterloesung, 'Musterlösung', 'Musterlösung', ZWECK['loesung'], 'loesung',
                    f'happymatty/{t}/Lösung', bg),
            Eintrag(self.interaktiv, 'interaktiv', 'Interaktiv', None, 'interaktiv', None, bg),
        ]

        self.probetest = None
        if 'probetest' in d:
            self.probetest = testgruppe(f'{ort} › probetest', d['probetest'], ordner)
        if self.probetest:
            p = self.probetest
            self.eintraege += [
                Eintrag(p['test'], 'Probetest', 'Probetest', ZWECK['probetest'], 'test',
                        f'happymatty/{t}/Probetest', bg),
                Eintrag(p['loesung'], 'Lösung zum Probetest', 'Lösung zum Probetest', ZWECK['loesung'],
                        'loesung', f'happymatty/{t}/Lösung Probetest', bg),
                Eintrag(p['notentabelle'], 'Notentabelle zum Probetest', 'Notentabelle zum Probetest',
                        ZWECK['notentabelle'], 'notentabelle', f'happymatty/{t}/Notentabelle Probetest', bg),
            ]

        self.fassungen, self.kurztest_notentabelle = [], None
        if 'kurztest' in d:
            self.lies_kurztest(f'{ort} › kurztest', d['kurztest'], ordner)

    def lies_kurztest(self, ort, d, ordner):
        if not schluessel(ort, d, ('fassungen', 'notentabelle')):
            return
        t, bg = self.titel, self.bildungsgaenge
        if not isinstance(d.get('fassungen'), list):
            melde(ort, '„fassungen“ muss eine Liste [ … ] sein')
            return
        nummern = []
        for i, f in enumerate(d['fassungen']):
            o = f'{ort} › fassungen[{i}]'
            if not schluessel(o, f, ('fassung', 'test', 'loesung')):
                continue
            n = wert(o, f, 'fassung', 'zahl')
            if n is None:
                continue
            nummern.append(n)
            o = f'{ort} › Fassung {n}'
            test, loesung = Dok(f'{o} › test', f['test'], ordner), Dok(f'{o} › loesung', f['loesung'], ordner)
            if test.freigegeben != loesung.freigegeben:
                melde(o, 'Fassung und Lösung gehen nur zusammen online')
            self.fassungen.append((n, test, loesung))
            self.eintraege += [
                Eintrag(test, f'Kurztest Fassung {n}', f'Kurztest Fassung {n}', ZWECK['ueben'], 'test',
                        f'happymatty/{t}/Kurztest Fassung {n}', bg),
                Eintrag(loesung, f'Lösung zu Fassung {n}', f'Lösung zu Fassung {n}', ZWECK['loesung'],
                        'loesung', f'happymatty/{t}/Lösung Kurztest Fassung {n}', bg),
            ]
        if len(set(nummern)) != len(nummern):
            melde(ort, 'eine Fassung ist doppelt eingetragen')
        self.fassungen.sort(key=lambda x: x[0])
        nt = self.kurztest_notentabelle = Dok(f'{ort} › notentabelle', d.get('notentabelle'), ordner)
        frei = any(test.freigegeben for _, test, _ in self.fassungen)
        if frei and not nt.freigegeben:
            melde(ort, 'freigegebene Fassungen gehen nur mit der Notentabelle online')
        if nt.freigegeben and not frei:
            melde(ort, 'Notentabelle freigegeben, aber keine Fassung')
        self.eintraege.append(Eintrag(nt, 'Notentabelle zum Kurztest', 'Notentabelle zum Kurztest',
                                      ZWECK['notentabelle'], 'notentabelle',
                                      f'happymatty/{t}/Notentabelle Kurztest', bg))

    @property
    def probetest_online(self):
        return bool(self.probetest and self.probetest['test'].freigegeben)

    @property
    def fassungen_online(self):
        return [(n, t, l) for n, t, l in self.fassungen if t.freigegeben]


class Thema:
    def __init__(self, ordner):
        self.ordner, self.slug = ordner, ordner.name
        datei = ordner / '_thema.json'
        ort = rel(datei)
        d = lies_json(datei)
        self.eintraege, self.einheiten = [], []
        self.probeklassenarbeit = self.klassenarbeit = None
        self.ok = d is not None and schluessel(ort, d, (
            'titel', 'kennung', 'fach', 'unterzeile', 'bildungsgang', 'reihenfolge'),
            ('probeklassenarbeit', 'klassenarbeit'))
        if not self.ok:
            unlesbar.add(ordner)
            return
        self.titel = wert(ort, d, 'titel', 'text') or self.slug
        self.kennung = wert(ort, d, 'kennung', 'text', leer=True)
        if self.kennung and not KENNUNG.match(self.kennung):
            melde(ort, f'„kennung“ sieht aus wie LF oder QF, nicht „{self.kennung}“')
        self.fach = wert(ort, d, 'fach', 'text') or ''
        if self.fach and self.fach not in FAECHER:
            melde(ort, f'unbekanntes Fach „{self.fach}“ (bekannt: {", ".join(FAECHER)})')
        self.unterzeile = wert(ort, d, 'unterzeile', 'text', leer=True)
        self.bildungsgang = wert(ort, d, 'bildungsgang', 'text')
        if self.bildungsgang and self.bildungsgang not in BILDUNGSGAENGE:
            melde(ort, f'unbekannter Bildungsgang „{self.bildungsgang}“')
        self.reihenfolge = wert(ort, d, 'reihenfolge', 'zahl') or 0
        t = self.titel
        for art, name in (('probeklassenarbeit', 'Probeklassenarbeit'), ('klassenarbeit', 'Klassenarbeit')):
            if art not in d:
                continue
            o = f'{ort} › {art}'
            g = testgruppe(o, d[art], ordner / art, frei=('bildungsgaenge',))
            if g is None:
                continue
            if 'bildungsgaenge' not in d[art]:
                melde(o, '„bildungsgaenge“ fehlt')
            g['bildungsgaenge'] = bildungsgaenge(o, d[art])
            setattr(self, art, g)
            bg = g['bildungsgaenge']
            zweck = ZWECK['probeklassenarbeit'] if art == 'probeklassenarbeit' else ZWECK['ueben']
            self.eintraege += [
                Eintrag(g['test'], name, name, zweck, 'test', f'happymatty/{t}/{name}', bg),
                Eintrag(g['loesung'], f'Lösung zur {name}', f'Lösung zur {name}', ZWECK['loesung'],
                        'loesung', f'happymatty/{t}/Lösung {name}', bg),
                Eintrag(g['notentabelle'], f'Notentabelle zur {name}', f'Notentabelle zur {name}',
                        ZWECK['notentabelle'], 'notentabelle', f'happymatty/{t}/Notentabelle {name}', bg),
            ]

    @property
    def bildungsgaenge(self):
        alle = {b for e in self.einheiten for b in e.bildungsgaenge}
        return [b for b in BILDUNGSGAENGE if b in alle]

    def einheiten_in(self, bg):
        return [e for e in self.einheiten if bg in e.bildungsgaenge]

    @property
    def probeklassenarbeit_online(self):
        return bool(self.probeklassenarbeit and self.probeklassenarbeit['test'].freigegeben)

    @property
    def klassenarbeit_angekuendigt(self):
        """Die Klassenarbeit hat Seite und Karte, sobald sie vorhanden ist; grau bis zur Freigabe."""
        return bool(self.klassenarbeit and self.klassenarbeit['test'].vorhanden)


# ------------------------------------------------------------------ Repository durchgehen

def einlesen():
    themen = []
    for ordner in sorted(p for p in WURZEL.iterdir() if p.is_dir()):
        name = ordner.name
        if name.startswith(('.', '_')) or name in RESERVIERT:
            continue
        if not (ordner / '_thema.json').is_file():
            melde(name + '/', 'Ordner ohne _thema.json; ein neues Thema legt nur Claude Code an')
            continue
        if not ORDNERNAME.match(name):
            melde(name + '/', 'Ordnernamen nur aus Kleinbuchstaben, Ziffern und Bindestrichen')
        thema = Thema(ordner)
        themen.append(thema)
        if not thema.ok:
            continue
        for unter in sorted(p for p in ordner.iterdir() if p.is_dir()):
            u = unter.name
            if u.startswith(('.', '_')):
                continue
            if (unter / '_einheit.json').is_file():
                if not ORDNERNAME.match(u):
                    melde(rel(unter) + '/', 'Ordnernamen nur aus Kleinbuchstaben, Ziffern und Bindestrichen')
                e = Einheit(thema, unter)
                if e.ok:
                    thema.einheiten.append(e)
            elif u == 'probeklassenarbeit' and thema.probeklassenarbeit_online:
                pass
            elif u == 'klassenarbeit' and thema.klassenarbeit_angekuendigt:
                pass
            elif u in ('probeklassenarbeit', 'klassenarbeit'):
                melde(rel(unter) + '/', f'Ordner liegt, aber laut _thema.json gibt es keine {u.capitalize()}')
            elif weiterleitung(unter):
                pass
            else:
                melde(rel(unter) + '/', 'Ordner ohne _einheit.json (neue Themeneinheit? Beschreibungsdatei anlegen)')
                unlesbar.add(unter)
        thema.einheiten.sort(key=lambda e: e.platz)
        if not thema.einheiten:
            melde(rel(ordner) + '/', 'Thema ohne Themeneinheit')
        plaetze = [e.platz for e in thema.einheiten]
        if len(set(plaetze)) != len(plaetze):
            melde(rel(ordner) + '/', f'zwei Themeneinheiten haben denselben „platz“ ({plaetze})')
        if thema.bildungsgang and thema.einheiten and thema.bildungsgang not in thema.bildungsgaenge:
            melde(rel(ordner / '_thema.json'), f'„bildungsgang“ {thema.bildungsgang} kommt in keiner '
                                               f'Themeneinheit vor ({", ".join(thema.bildungsgaenge)})')
    for bg in BILDUNGSGAENGE:
        r = [t.reihenfolge for t in themen if t.ok and t.bildungsgang == bg]
        if len(set(r)) != len(r):
            melde('_thema.json', f'zwei Themen im {bg} haben dieselbe „reihenfolge“ ({sorted(r)})')
    return themen


def weiterleitung(ordner):
    """Handgeschriebene Weiterleitung auf eine neue Adresse (Seite mit rel="canonical")."""
    seite = ordner / 'index.html'
    return seite.is_file() and 'rel="canonical"' in seite.read_text(encoding='utf-8')


def alle_eintraege(themen):
    for t in themen:
        for e in t.einheiten:
            yield from e.eintraege
        yield from t.eintraege


def pruefe_dateien(themen):
    """.tex verboten; jedes PDF muss freigegeben sein; Freigegebenes muss da sein."""
    erwartet = {}
    for e in alle_eintraege(themen):
        d = e.dok
        if d.interaktiv:
            da = (d.pfad / 'index.html').is_file()
            if d.freigegeben and not da:
                melde(d.ort, f'freigegeben, aber {rel(d.pfad)}/index.html fehlt')
            if da and not d.freigegeben:
                melde(d.ort, f'{rel(d.pfad)}/ liegt im Repository, ist aber nicht freigegeben')
        elif d.freigegeben and d.pfad:
            if d.pfad in erwartet:
                melde(d.ort, f'{rel(d.pfad)} ist zweimal eingetragen')
            erwartet[d.pfad] = e
    for pfad in sorted(WURZEL.rglob('*')):
        teile = pfad.relative_to(WURZEL).parts
        if teile[0] == '.git' or not pfad.is_file():
            continue
        endung = pfad.suffix.lower()
        if endung == '.tex':
            melde(rel(pfad), '.tex gehört nie ins Repository (enthält immer die Lösung); '
                             'sie liegt nur im Backup unterrichtsmaterial')
        elif endung == '.pdf' and pfad not in erwartet and not unlesbar.intersection(pfad.parents):
            melde(rel(pfad), 'PDF steht in keiner Beschreibungsdatei als freigegeben')
    for pfad, e in erwartet.items():
        if not pfad.is_file():
            melde(e.dok.ort, f'freigegeben, aber {rel(pfad)} fehlt')
    return erwartet


def pruefe_ordnerinhalt(themen):
    """In den Ordnern der Einheiten, Probeklassenarbeit und Klassenarbeit liegt nur, was dahin gehört."""
    ordner = [(e.ordner, {'index.html', '_einheit.json', 'interaktiv'}) for t in themen for e in t.einheiten]
    for t in themen:
        if t.probeklassenarbeit_online:
            ordner.append((t.ordner / 'probeklassenarbeit', {'index.html'}))
        if t.klassenarbeit_angekuendigt:
            ordner.append((t.ordner / 'klassenarbeit', {'index.html'}))
    for o, erlaubt in ordner:
        if not o.is_dir():
            continue
        for p in o.iterdir():
            if p.name.startswith('.') or p.name in erlaubt or p.suffix.lower() in ('.pdf', '.tex'):
                continue
            melde(rel(p), 'unerwartete Datei; hier liegen nur index.html, die Beschreibungsdatei, '
                          'freigegebene PDFs und interaktiv/')


# ------------------------------------------------------------------ PDFs: Seitenzahl und Titel

def pikepdf_laden():
    try:
        import pikepdf
        return pikepdf
    except ImportError:
        sys.exit('pikepdf fehlt: einmal „pip install pikepdf“ ausführen, dann neu starten.')


_seiten = {}


def seitenzahl(pfad):
    if pfad not in _seiten:
        with pikepdf_laden().open(pfad) as pdf:
            _seiten[pfad] = len(pdf.pages)
    return _seiten[pfad]


def titel_stimmt(pfad, titel):
    pikepdf = pikepdf_laden()
    with pikepdf.open(pfad) as pdf:
        info = str(pdf.docinfo.get('/Title', ''))  # vor open_metadata lesen: das gleicht die Info an
        with pdf.open_metadata(set_pikepdf_as_editor=False, update_docinfo=False) as meta:
            xmp = meta.get('dc:title')
        vp = pdf.Root.get('/ViewerPreferences')
        anzeigen = vp is not None and bool(vp.get('/DisplayDocTitle', False))
        return info == titel and xmp == titel and anzeigen


def titel_setzen(pfad, titel):
    """Wie früher pdf_titel.py: Titel in Info und XMP, Anzeige des Titels statt des Dateinamens."""
    pikepdf = pikepdf_laden()
    with pikepdf.open(pfad, allow_overwriting_input=True) as pdf:
        with pdf.open_metadata(set_pikepdf_as_editor=False) as meta:
            meta['dc:title'] = titel
        pdf.docinfo['/Title'] = titel
        pdf.Root.ViewerPreferences = pikepdf.Dictionary(DisplayDocTitle=True)
        pdf.save(pfad)


# ------------------------------------------------------------------ Seiten bauen

def url(pfad):
    s = '/' + rel(pfad)
    return s + '/' if pfad.is_dir() or pfad.suffix == '' else s


def seiten_text(n):
    return f'{n}&nbsp;Seite' if n == 1 else f'{n}&nbsp;Seiten'


def anzahl(n):
    return f'{n} Themeneinheit' if n == 1 else f'{n} Themeneinheiten'


def badges(liste):
    return ''.join(f'<span class="badge">{b}</span>' for b in liste)


def karte(klasse, href, titel, text):
    k = f' class="{klasse}"' if klasse else ''
    return (f'    <li><a{k} href="{href}">\n'
            f'      <span class="titel">{titel}</span>\n'
            f'      <span class="text">{text}</span>\n'
            f'    </a></li>\n')


def graue_karte(titel, text):
    return ('    <li><div class="gesperrt" aria-disabled="true">\n'
            f'      <span class="titel">{titel}</span>\n'
            f'      <span class="text">{text}</span>\n'
            '    </div></li>\n')


def liste(karten, klasse='liste'):
    return f'  <ul class="{klasse}">\n' + ''.join(karten) + '  </ul>\n'


def pdf_karte(e):
    return karte(e.klasse, url(e.dok.pfad), e.karte,
                 f'{e.zweck} (PDF, {seiten_text(seitenzahl(e.dok.pfad))})')


def thema_karte(t, text):
    unter = f'      <span class="unterzeile">{esc(t.unterzeile)}</span>\n' if t.unterzeile else ''
    return (f'    <li><a class="thema-karte" href="/{t.slug}/">\n'
            f'      <span class="titel">{esc(t.titel)}</span>\n'
            f'{unter}'
            f'      <span class="text">{text}</span>\n'
            f'    </a></li>\n')


def kopfleiste(zurueck_href, zurueck_text):
    return ('  <div class="kopfleiste">\n'
            f'    <a class="logo" href="/">{LOGO}</a>\n'
            f'    <a class="zurueck" href="{zurueck_href}">← {esc(zurueck_text)}</a>\n'
            '  </div>\n')


def seite(titel, bloecke):
    return KOPF.format(titel=esc(titel)) + '\n'.join(bloecke + [FUSS])


def kopf_thema(t, teilthema=None):
    s = f'{esc(t.fach)} · <span class="thema">{esc(t.titel)}</span>'
    if teilthema:
        s += f' · <span class="teilthema">{esc(teilthema)}</span>'
    return f'  <p class="kopf">{s}</p>\n'


def baue_einheit(e):
    t = e.thema
    by = {x.dok: x for x in e.eintraege}
    kopf = (kopfleiste(f'/{t.slug}/', t.titel) + kopf_thema(t, e.teilthema)
            + f'  <h1>{esc(e.titel)}</h1>\n'
            + f'  <p class="badges">{badges(e.bildungsgaenge)}</p>\n')
    karten = [pdf_karte(by[e.aufgabenblatt])]
    karten.append(pdf_karte(by[e.musterloesung]) if e.musterloesung.freigegeben
                  else graue_karte('Musterlösung', GESPERRT_LOESUNG))
    karten.append(karte('interaktiv', url(e.interaktiv.pfad), 'Interaktiv', esc(e.interaktiv.text))
                  if e.interaktiv.freigegeben else graue_karte('Interaktiv', GESPERRT_INTERAKTIV))
    bloecke = [kopf, liste(karten)]
    if e.probetest_online:
        p = e.probetest
        bloecke.append('  <h2 class="themenkopf" id="probetest">Probetest</h2>\n'
                       + liste([pdf_karte(by[p[k]]) for k in ('test', 'loesung', 'notentabelle')]))
    if e.fassungen_online:
        k = []
        for _, test, loesung in e.fassungen_online:
            k += [pdf_karte(by[test]), pdf_karte(by[loesung])]
        k.append(pdf_karte(by[e.kurztest_notentabelle]))
        bloecke.append('  <h2 class="themenkopf" id="kurztest">Kurztest</h2>\n' + liste(k))
    return seite(f'happymatty/{e.titel}', bloecke)


def baue_arbeit(t, art):
    """Seite /<thema>/probeklassenarbeit oder /<thema>/klassenarbeit."""
    g = getattr(t, art)
    name = 'Probeklassenarbeit' if art == 'probeklassenarbeit' else 'Klassenarbeit'
    by = {x.dok: x for x in t.eintraege}
    kopf = (kopfleiste(f'/{t.slug}/', t.titel) + kopf_thema(t)
            + f'  <h1>{name}</h1>\n'
            + f'  <p class="badges">{badges(g["bildungsgaenge"])}</p>\n')
    karten = []
    for k in ('test', 'loesung', 'notentabelle'):
        x = by[g[k]]
        karten.append(pdf_karte(x) if g[k].freigegeben else graue_karte(x.karte, GESPERRT_KLASSENARBEIT))
    return seite(f'happymatty/{t.titel}/{name}', [kopf, liste(karten)])


def baue_thema(t):
    heim = t.bildungsgang
    kopf = (kopfleiste(f'/{heim.lower()}/', heim) + f'  <p class="kopf">{esc(t.fach)}</p>\n'
            + f'  <h1 class="thema">{esc(t.titel)}</h1>\n')
    karten = []
    for e in t.einheiten:
        text = f'{esc(e.teilthema)} – {esc(e.beschreibung)}'
        if e.probetest_online or e.fassungen_online:  # Entscheidung 14.11.2026: nur „mit Test“
            text += ' · mit Test'
        karten.append(karte(None, url(e.ordner), f'{esc(e.titel)}{badges(e.bildungsgaenge)}', text))
    bloecke = [kopf, '  <h2 class="themenkopf">Themeneinheiten</h2>\n' + liste(karten)]
    if t.probeklassenarbeit_online:
        bloecke.append(
            '  <h2 class="themenkopf" id="probeklassenarbeit">Probeklassenarbeit</h2>\n'
            + liste([karte('test', f'/{t.slug}/probeklassenarbeit/',
                           f'Probeklassenarbeit{badges(t.probeklassenarbeit["bildungsgaenge"])}',
                           'Die ganze Reihe zum Üben vor der Klassenarbeit · mit Lösung und Notentabelle')]))
    if t.klassenarbeit_angekuendigt:
        bloecke.append(
            '  <h2 class="themenkopf" id="klassenarbeit">Klassenarbeit</h2>\n'
            + liste([karte('test', f'/{t.slug}/klassenarbeit/',
                           f'Klassenarbeit{badges(t.klassenarbeit["bildungsgaenge"])}',
                           'Die Klassenarbeit zur ganzen Reihe · mit Lösung und Notentabelle')]))
    return seite(f'happymatty/{t.titel}', bloecke)


def sortiert(themen):
    return sorted(themen, key=lambda t: t.reihenfolge)


def baue_bildungsgang(bg, themen):
    kopf = (f'  <a class="logo" href="/">{LOGO}</a>\n'
            f'  <p class="kopf">{BILDUNGSGAENGE[bg]["name"]}</p>\n'
            f'  <h1>{bg}</h1>\n')
    bloecke = [kopf]
    for fach in FAECHER:
        hier = sortiert(t for t in themen if t.fach == fach and t.einheiten_in(bg))
        if hier:
            bloecke.append(f'  <h2 class="themenkopf">{esc(fach)}</h2>\n'
                           + liste([thema_karte(t, anzahl(len(t.einheiten_in(bg)))) for t in hier]))
    if len(bloecke) == 1:
        bloecke.append(liste([graue_karte('Noch kein Material',
                                          'Hier erscheinen die Themen, sobald Material online ist.')]))
    return seite(f'happymatty/{bg.lower()}', bloecke)


def baue_startseite(themen):
    kopf = (f'  <div class="logo">{LOGO}</div>\n'
            '  <p class="kopf"></p>\n'
            '  <h1>Unterrichtsmaterial</h1>\n'
            '  <p class="unterzeile autor">von Patrick Saul</p>\n')
    kacheln = [f'    <li><a href="/{bg.lower()}/"><span class="kuerzel">{bg}</span>'
               f'<span class="name">{d["kachel"]}</span></a></li>\n'
               for bg, d in BILDUNGSGAENGE.items() if d['seite']]
    gruppen = []
    for bg in BILDUNGSGAENGE:
        hier = sortiert(t for t in themen if t.bildungsgang == bg)
        if hier:
            gruppen.append(liste([thema_karte(t, f'{badges(t.bildungsgaenge)} {anzahl(len(t.einheiten))}')
                                  for t in hier]))
    return seite('happymatty', [
        kopf,
        '  <h2 class="themenkopf">Klassen</h2>\n' + liste(kacheln, 'klassen'),
        '  <h2 class="themenkopf">Themen</h2>\n' + '  <hr class="trenner">\n'.join(gruppen),
    ])


def alle_seiten(themen):
    seiten = {WURZEL / 'index.html': baue_startseite(themen)}
    for bg, d in BILDUNGSGAENGE.items():
        if d['seite']:
            seiten[WURZEL / bg.lower() / 'index.html'] = baue_bildungsgang(bg, themen)
    for t in themen:
        seiten[t.ordner / 'index.html'] = baue_thema(t)
        for e in t.einheiten:
            seiten[e.ordner / 'index.html'] = baue_einheit(e)
        if t.probeklassenarbeit_online:
            seiten[t.ordner / 'probeklassenarbeit' / 'index.html'] = baue_arbeit(t, 'probeklassenarbeit')
        if t.klassenarbeit_angekuendigt:
            seiten[t.ordner / 'klassenarbeit' / 'index.html'] = baue_arbeit(t, 'klassenarbeit')
    return seiten


# ------------------------------------------------------------------ Kennungen ?v=… im Kopf

SYMBOL = ('<link rel="icon" href="/favicon.ico" sizes="any">\n'
          '<link rel="icon" type="image/png" sizes="32x32" href="/stil/icon-32.png">\n'
          '<link rel="apple-touch-icon" href="/apple-touch-icon.png">\n')
BILDER = ('favicon.ico', 'stil/icon-32.png', 'apple-touch-icon.png')


def kennung(datei):
    return hashlib.sha256((WURZEL / datei).read_bytes()).hexdigest()[:8]


def kennungen(text):
    """Hängt an basis.css und die Symbol-Verweise im Kopf die Kennung aus dem Dateiinhalt an und
    ergänzt fehlende Symbol-Verweise direkt nach dem <title>."""
    text = re.sub(r'/stil/basis\.css(\?v=[0-9a-f]+)?', f'/stil/basis.css?v={kennung("stil/basis.css")}', text)
    if 'apple-touch-icon' not in text:
        text = re.sub(r'</title>\n?', lambda m: '</title>\n' + SYMBOL, text, count=1)
    muster = re.compile(r'(<link\b[^>]*\bhref="/)(' + '|'.join(re.escape(b) for b in BILDER)
                        + r')(?:\?v=[0-9a-f]+)?(")')
    return muster.sub(lambda m: f'{m.group(1)}{m.group(2)}?v={kennung(m.group(2))}{m.group(3)}', text)


# ------------------------------------------------------------------ Bestand

def bestand(themen):
    zeilen = ['| Link | Inhalt | Bildungsgang | Quelle | Stand |', '|---|---|---|---|---|']
    offen = []
    for e in alle_eintraege(themen):
        d = e.dok
        if d.freigegeben:
            link = url(d.pfad).rstrip('/') if d.interaktiv else url(d.pfad)
            quelle = d.quelle if d.interaktiv else f'`{d.quelle}`'
            zeilen.append(f'| `{link}` | {e.inhalt} | {", ".join(e.bildungsgaenge)} | {quelle} | {d.stand} |')
        elif d.vorhanden or d.hinweis:
            wo = rel(d.ordner)
            was = f'vorhanden ({d.quelle})' if d.vorhanden else 'nicht vorhanden'
            offen.append(f'- {wo} › {e.inhalt}: {was}' + (f' – {d.hinweis}' if d.hinweis else ''))
    print('Veröffentlicht:\n')
    print('\n'.join(zeilen))
    if offen:
        print('\nVorhanden oder vorgemerkt, nicht veröffentlicht:\n')
        print('\n'.join(offen))


# ------------------------------------------------------------------ Ablauf

def main():
    args = set(sys.argv[1:])
    if args - {'--pruefen', '--bestand'}:
        sys.exit(__doc__)
    nur_pruefen = '--pruefen' in args
    themen = einlesen()
    erwartet = pruefe_dateien(themen)
    pruefe_ordnerinhalt(themen)
    if fehler:
        print(f'Abgebrochen, nichts geschrieben. {len(fehler)} Fehler:')
        for f in fehler:
            print('  - ' + f)
        sys.exit(2)

    if '--bestand' in args:
        bestand(themen)
        return

    neu = {p: kennungen(s) for p, s in alle_seiten(themen).items()}
    for p in sorted(WURZEL.rglob('*.html')):  # nicht gebaute Seiten: nur die Kennungen im Kopf
        if p not in neu and not any(x.startswith(('.', '_')) for x in p.relative_to(WURZEL).parts):
            neu[p] = kennungen(p.read_text(encoding='utf-8'))
    geaendert = [p for p, s in neu.items() if not p.is_file() or p.read_text(encoding='utf-8') != s]
    titel = [(e.dok.pfad, e.pdf_titel) for e in erwartet.values() if not titel_stimmt(e.dok.pfad, e.pdf_titel)]

    if nur_pruefen:
        if not geaendert and not titel:
            print(f'Geprüft: alles in Ordnung, {len(neu)} Seiten aktuell.')
            return
        print('Geprüft: in Ordnung, aber nicht aktuell. Beim Bauen ändern sich:')
        for p in geaendert:
            print('  - ' + rel(p))
        for p, t in titel:
            print(f'  - {rel(p)} (PDF-Titel „{t}“)')
        sys.exit(1)

    for p in geaendert:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(neu[p], encoding='utf-8')
    for p, t in titel:
        titel_setzen(p, t)
    if not geaendert and not titel:
        print(f'Geprüft und gebaut: nichts geändert, {len(neu)} Seiten aktuell.')
        return
    print(f'Geprüft und gebaut. Geändert:')
    for p in geaendert:
        print('  - ' + rel(p))
    for p, t in titel:
        print(f'  - {rel(p)} (PDF-Titel „{t}“ eingetragen)')


if __name__ == '__main__':
    main()
