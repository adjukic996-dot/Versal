#!/usr/bin/env python3
"""
Versal — Seiten bauen.

    python3 _werkzeug/seiten-bauen.py

Zwei Auslieferungen aus einer Quelle, ueber Umgebungsvariablen:
    VERSAL_BASIS=/referenzen/versal VERSAL_ZIEL=... python3 ...
"""
import os
from html import escape as e
from pathlib import Path

BASIS = os.environ.get("VERSAL_BASIS", "/Versal")
HIER  = Path(__file__).resolve().parent.parent
ZIEL  = Path(os.environ.get("VERSAL_ZIEL", HIER))

def u(pfad: str) -> str:
    return BASIS + pfad

# ---------------------------------------------------------------------------
# Die vier Familien. Jede traegt genau eine Farbe — nie eine fremde.
# ---------------------------------------------------------------------------
FAMILIEN = [
    {"pfad": "/werkgrotesk/", "name": "Werkgrotesk", "klasse": "Grotesk",
     "farbe": "grotesk", "probe": "grotesk", "schnitte": 6,
     "kurz": "Der Arbeitsschnitt.",
     "satz": "Gezeichnet für Oberflächen und Tabellen. Offene Punzen, kurze "
             "Oberlängen, eindeutige Ziffern — damit sie auch bei 13 Pixeln "
             "noch auseinanderzuhalten sind.",
     "detail": ["Sechs Schnitte von Light bis Black", "Dicktengleiche Ziffern für Tabellen",
                "Eindeutige 1, l und I", "Kyrillisch und Griechisch in Vorbereitung"]},
    {"pfad": "/isaria/", "name": "Isaria", "klasse": "Antiqua",
     "farbe": "antiqua", "probe": "antiqua", "schnitte": 4,
     "kurz": "Für lange Strecken.",
     "satz": "Eine Antiqua für Fliesstext, der wirklich gelesen wird. Ruhige "
             "Serifen, mittlerer Kontrast, grosszügige Mittellänge. Hält auf "
             "Papier und am Bildschirm gleichermassen.",
     "detail": ["Vier Schnitte, je mit Kursive", "Mediävalziffern und Versalziffern",
                "Kapitälchen in allen Schnitten", "Gezeichnet für 9 bis 14 Punkt"]},
    {"pfad": "/versal-mono/", "name": "Versal Mono", "klasse": "Dicktengleich",
     "farbe": "mono", "probe": "mono", "schnitte": 5,
     "kurz": "Alles steht untereinander.",
     "satz": "Für Code, Zahlenkolonnen und Belege. Gleiche Dickte für jedes "
             "Zeichen, deutlich unterschiedene Klammerpaare, eine Null mit "
             "Schrägstrich.",
     "detail": ["Fünf Schnitte", "Null mit Schrägstrich, abschaltbar",
                "Ligaturen für Pfeile und Vergleiche", "Geprüft in acht Editoren"]},
    {"pfad": "/foehn/", "name": "Föhn", "klasse": "Auszeichnung",
     "farbe": "display", "probe": "display", "schnitte": 3,
     "kurz": "Ab achtundvierzig Punkt.",
     "satz": "Eine Auszeichnungsschrift für grosse Grade. Enge Laufweite, "
             "starke Kontraste, feine Anschlüsse. Unter 48 Punkt verliert sie "
             "ihre Form — das ist Absicht, nicht ein Mangel.",
     "detail": ["Drei Schnitte", "Enge Vorgabe-Laufweite für Schauzeilen",
                "Alternativformen für R, K und Q", "Nicht für Fliesstext gedacht"]},
]

HAUPT = [("/schaufenster/", "Schaufenster"), ("/massschrift/", "Massschrift"),
         ("/lizenzen/", "Lizenzen"), ("/ueber-uns/", "Über uns")]


def klammer(text: str) -> str:
    """Die Signatur des Systems: geschweifte Klammern vor jedem Abschnitt."""
    return f'<p class="klammer" data-ein>{e(text)}</p>'


def knopf(text: str, ziel: str, haupt: bool = False) -> str:
    k = "knopf knopf--haupt" if haupt else "knopf"
    return f'<a class="{k}" href="{u(ziel)}"><span class="knopf__text">{e(text)}</span></a>'


def form(variante: str) -> str:
    return f'<div class="form form--{variante}" aria-hidden="true"></div>'


def kopfzeile(aktiv: str = "") -> str:
    fam = "".join(
        f'<li><a class="navverweis f-{f["farbe"]}" href="{u(f["pfad"])}"'
        + (' aria-current="page"' if f["pfad"] == aktiv else '')
        + f'>{e(f["name"])}</a></li>' for f in FAMILIEN)
    haupt = "".join(
        f'<li><a class="navverweis" href="{u(p)}"'
        + (' aria-current="page"' if p == aktiv else '')
        + f'>{e(t)}</a></li>' for p, t in HAUPT)
    menue = "".join(f'<a class="f-{f["farbe"]}" href="{u(f["pfad"])}">{e(f["name"])}</a>'
                    for f in FAMILIEN)
    menue += "".join(f'<a href="{u(p)}">{e(t)}</a>' for p, t in HAUPT)
    return f'''<header class="kopf">
  <div class="kopf__reihe">
    <a class="marke" href="{u("/")}">Versal</a>
    <nav aria-label="Hauptnavigation"><ul class="kopf__liste">{fam}{haupt}</ul></nav>
    <div class="kopf__rechts">
      {knopf("Testschnitte", "/lizenzen/", haupt=True)}
      <button class="brenner" type="button" aria-expanded="false" aria-label="Menü">
        <span class="brenner__strich"></span><span class="brenner__strich"></span><span class="brenner__strich"></span>
      </button>
    </div>
  </div>
</header>
<div class="menue" data-auf="nein"><nav aria-label="Menü">{menue}
  <a href="{u("/kontakt/")}">Kontakt</a></nav>
  <div class="menue__knopf">{knopf("Testschnitte laden", "/lizenzen/", haupt=True)}</div></div>'''


def fusszeile() -> str:
    spalten = [
        ("Familien", [(f["pfad"], f["name"]) for f in FAMILIEN]),
        ("Haus", [("/ueber-uns/", "Über uns"), ("/massschrift/", "Massschrift"),
                  ("/schaufenster/", "Schaufenster")]),
        ("Kaufen", [("/lizenzen/", "Lizenzen"), ("/kontakt/", "Kontakt")]),
        ("Rechtliches", [("/impressum/", "Impressum"), ("/datenschutz/", "Datenschutz")]),
    ]
    sp = "".join(
        f'<div><p class="fuss__titel">{e(t)}</p><ul class="fuss__liste">'
        + "".join(f'<li><a href="{u(p)}">{e(n)}</a></li>' for p, n in posten)
        + "</ul></div>" for t, posten in spalten)
    return f'''<footer class="fuss">
  <div class="huelle">
    <div class="fuss__spalten">{sp}</div>
    <div class="fuss__unten">
      <span class="klammer" style="margin:0">Schrift aus München, seit 2019</span>
      <span>© 2026 Versal GmbH</span>
    </div>
  </div>
</footer>'''


def seite(titel: str, beschreibung: str, inhalt: str, aktiv: str = "") -> str:
    return f'''<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{e(titel)}</title>
<meta name="description" content="{e(beschreibung)}">
<link rel="preload" href="{u("/fonts/inter-tight.woff2")}" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{u("/stil.css")}">
<script>document.documentElement.className+=" js"</script>
</head>
<body>
<a class="sprungmarke" href="#inhalt">Zum Inhalt springen</a>
{kopfzeile(aktiv)}
<main id="inhalt">
{inhalt}
</main>
{fusszeile()}
<script src="{u("/bewegung.js")}" defer></script>
</body>
</html>
'''


def schreibe(pfad: str, text: str) -> None:
    ziel = ZIEL / pfad
    ziel.parent.mkdir(parents=True, exist_ok=True)
    ziel.write_text(text, encoding="utf-8")
    print(f"  {pfad:<30} {len(text)/1024:>6.1f} kB")

# ===========================================================================
# INHALTE
# Fachlich gilt: Schriftklassen, Lizenzmodelle, Dickte, Laufweite, Hinting und
# OpenType-Funktionen sind echte Begriffe und werden nur so beschrieben, wie
# sie belegbar sind. Firma, Schriften und Preise sind erfunden.
# ===========================================================================

SCHAU = [
    ("Isarmetall", "Werkgrotesk", "grotesk", "Oberfläche und Datenblätter"),
    ("Hofgarten Verlag", "Isaria", "antiqua", "Buchreihe und Zeitschrift"),
    ("Taktbau", "Versal Mono", "mono", "Entwicklerhandbuch"),
    ("Nordlicht Festival", "Föhn", "display", "Plakate und Programm"),
    ("Kreissparkasse Lech", "Werkgrotesk", "grotesk", "Formularwesen"),
    ("Studio Grau", "Isaria", "antiqua", "Eigenauftritt"),
]


def start() -> str:
    bloecke = []
    for i, f in enumerate(FAMILIEN):
        links = f'<div data-ein>{form(f["farbe"])}</div>'
        rechts = f'''<div class="stapeln" data-ein style="--verzug:{(i%2)*100}ms">
        <p class="familie__klasse f-{f["farbe"]}">{e(f["klasse"])}</p>
        <h3 class="t-heading-sm familie__name">{e(f["name"])}</h3>
        <p class="t-body-lg familie__text">{e(f["satz"])}</p>
        <div class="knopfreihe">{knopf(f["name"] + " ansehen", f["pfad"])}</div>
      </div>'''
        bloecke.append(f'''<hr class="linie">
<section class="familie">
  <div class="huelle gitter gitter--seite">{links}{rechts}</div>
</section>''')

    schau = "".join(f'''<li class="karte" data-ein style="--verzug:{(i%3)*100}ms">
      <div class="schau__bild">
        <span class="schau__wort probe--{p} f-{p}">{e(n.split()[0])}</span>
      </div>
      <p class="t-body">{e(n)}</p>
      <p class="t-caption gedaempft">{e(fam)} · {e(zweck)}</p></li>'''
      for i, (n, fam, p, zweck) in enumerate(SCHAU[:3]))

    return f'''<section class="aufmacher">
  <div class="huelle">
    {klammer("Schriftgiesserei, München")}
    <h1 class="t-display" data-ein>
      <span class="aufmacher__zeile">Schrift für</span>
      <span class="aufmacher__zeile">Arbeit.</span>
    </h1>
    <div class="stapeln" style="margin-top:var(--s32);max-width:54ch">
      <p class="t-body-lg" data-ein style="--verzug:100ms">Vier Familien aus München,
        gezeichnet für Fliesstext, Tabellen und Bildschirme. Lizenzen ohne Abonnement,
        Testschnitte ohne Anmeldung.</p>
      <div class="knopfreihe" data-ein style="--verzug:200ms">
        {knopf("Testschnitte laden", "/lizenzen/", haupt=True)}
        {knopf("Alle vier Familien", "/schaufenster/")}
      </div>
    </div>
  </div>
</section>

<section class="abschnitt">
  <div class="huelle">{klammer("Die Familien")}</div>
</section>
{"".join(bloecke)}
<hr class="linie">

<section class="abschnitt">
  <div class="huelle stapeln stapeln--weit">
    {klammer("Im Einsatz")}
    <ul class="gitter gitter--3">{schau}</ul>
    <div class="knopfreihe">{knopf("Ganzes Schaufenster", "/schaufenster/")}</div>
  </div>
</section>
<hr class="linie">

<section class="abschnitt">
  <div class="huelle gitter gitter--seite">
    <div class="stapeln">
      {klammer("Haltung")}
      <h2 class="t-heading" data-ein>Einmal kaufen.<br>Dann gehört sie Ihnen.</h2>
    </div>
    <div class="stapeln" data-ein style="--verzug:100ms">
      <p class="t-body-lg">Keine Abonnements, keine Zählung von Seitenaufrufen, keine
        Nachlizenzierung, wenn Ihr Unternehmen wächst.</p>
      <p class="t-body gedaempft">Eine Schrift ist Werkzeug, kein Mietgegenstand. Wer sie
        einmal lizenziert, kann damit arbeiten, solange es das Produkt gibt — auch wenn es
        uns irgendwann nicht mehr gibt.</p>
      <div class="knopfreihe">{knopf("Lizenzen ansehen", "/lizenzen/")}</div>
    </div>
  </div>
</section>'''


def familienseite(f: dict) -> str:
    detail = "".join(f'<li class="t-body" style="padding:var(--s12) 0;'
                     f'border-bottom:1px solid var(--creme25)">{e(x)}</li>'
                     for x in f["detail"])
    probe = f.get("probe")
    return f'''<section class="aufmacher">
  <div class="huelle">
    {klammer(f["klasse"])}
    <h1 class="t-heading-lg f-{f["farbe"]}" data-ein>{e(f["name"])}</h1>
    <p class="t-heading-sm" data-ein style="--verzug:100ms;margin-top:var(--s16)">{e(f["kurz"])}</p>
    <p class="t-body-lg" data-ein style="--verzug:200ms;margin-top:var(--s24);max-width:50ch">{e(f["satz"])}</p>
    <div class="knopfreihe" data-ein style="--verzug:300ms;margin-top:var(--s32)">
      {knopf("Testschnitt laden", "/lizenzen/", haupt=True)}
      {knopf("Lizenz kaufen", "/lizenzen/")}
    </div>
  </div>
</section>
<hr class="linie">

<section class="abschnitt">
  <div class="huelle stapeln stapeln--weit">
    {klammer("Probe")}
    <div class="probe--{probe}" data-ein>
      <p class="probe__zeile f-{f["farbe"]}">Hamburgefonstiv</p>
      <p class="probe__satz">Der Föhn drückt über die Alpen, und in München
        steigt das Quecksilber.</p>
      <p class="t-body" style="margin-top:var(--s24);max-width:60ch">
        Eine Schrift zeigt sich nicht in der Schauzeile, sondern im Satz. Hier steht sie in
        der Grösse, in der sie später wirklich arbeitet: dicht gesetzt, über mehrere Zeilen,
        mit Ziffern und Satzzeichen. 0123456789 — ()[]{{}} — «Anführung» — 1 l I 0 O</p>
    </div>
  </div>
</section>
<hr class="linie">

<section class="abschnitt">
  <div class="huelle gitter gitter--seite">
    <div data-ein>{form(f["farbe"])}</div>
    <div class="stapeln">
      {klammer("Umfang")}
      <p class="t-heading-sm" data-ein>{f["schnitte"]} Schnitte</p>
      <ul data-ein style="--verzug:100ms">{detail}</ul>
    </div>
  </div>
</section>'''


def schaufenster() -> str:
    karten = "".join(f'''<li class="karte" data-ein style="--verzug:{(i%3)*100}ms">
      <div class="schau__bild">
        <span class="schau__wort probe--{p} f-{p}">{e(n.split()[0])}</span>
      </div>
      <p class="t-body">{e(n)}</p>
      <p class="t-caption gedaempft">{e(fam)} · {e(zweck)}</p></li>'''
      for i, (n, fam, p, zweck) in enumerate(SCHAU))
    return f'''<section class="aufmacher">
  <div class="huelle">
    {klammer("Schaufenster")}
    <h1 class="t-heading-lg" data-ein>Wo sie arbeiten.</h1>
    <p class="t-body-lg" data-ein style="--verzug:100ms;margin-top:var(--s24);max-width:54ch">
      Sechs Häuser, die mit einer unserer Familien setzen. Die Auswahl zeigt den Satz,
      nicht das Logo.</p>
  </div>
</section>
<hr class="linie">
<section class="abschnitt">
  <div class="huelle"><ul class="gitter gitter--3">{karten}</ul></div>
</section>'''


def massschrift() -> str:
    schritte = [
        ("Gespräch", "Wir sehen uns an, was Sie setzen und womit. Oft stellt sich dabei "
         "heraus, dass eine vorhandene Familie reicht. Dann sagen wir das."),
        ("Entwurf", "Drei Richtungen als Probe, jeweils ein Alphabet und ein Satz im "
         "Zielgrad. Keine Renderings, keine Stimmungsbilder."),
        ("Ausbau", "Die gewählte Richtung wird zur Familie: Schnitte, Kursive, Ziffernsätze, "
         "Sprachabdeckung. Dauer je nach Umfang vier bis zehn Monate."),
        ("Übergabe", "Dateien, Hinting, Testseiten und ein Satzhandbuch. Die Rechte liegen "
         "danach bei Ihnen, exklusiv und unbefristet."),
    ]
    liste = "".join(f'''<li class="karte karte--offen" data-ein style="--verzug:{i*100}ms">
      <p class="t-caption gedaempft">Schritt {i+1}</p>
      <h3 class="t-subheading">{e(t)}</h3>
      <p class="t-body">{e(x)}</p></li>''' for i, (t, x) in enumerate(schritte))
    return f'''<section class="aufmacher">
  <div class="huelle">
    {klammer("Massschrift")}
    <h1 class="t-heading-lg" data-ein>Eine eigene.</h1>
    <p class="t-body-lg" data-ein style="--verzug:100ms;margin-top:var(--s24);max-width:54ch">
      Wenn keine vorhandene Familie passt, zeichnen wir eine. Vier bis zehn Monate,
      danach gehört sie Ihnen allein.</p>
  </div>
</section>
<hr class="linie">
<section class="abschnitt">
  <div class="huelle stapeln stapeln--weit">
    {klammer("Ablauf")}
    <ul class="gitter gitter--2">{liste}</ul>
  </div>
</section>
<hr class="linie">
<section class="abschnitt">
  <div class="huelle gitter gitter--seite">
    <div data-ein>{form("haus")}</div>
    <div class="stapeln" data-ein style="--verzug:100ms">
      {klammer("Wann nicht")}
      <h2 class="t-heading-sm">Meistens reicht eine fertige.</h2>
      <p class="t-body-lg">Massschrift lohnt sich, wenn Sie viel setzen, lange setzen und
        wiedererkannt werden wollen. Für ein Logo und drei Broschüren lohnt sie sich nicht.</p>
      <p class="t-body gedaempft">Wir sagen Ihnen das im ersten Gespräch, nicht im dritten.</p>
    </div>
  </div>
</section>'''


def lizenzen() -> str:
    stufen = [
        ("Testschnitt", "0 €", "ohne Anmeldung",
         ["Ein Schnitt je Familie", "Für Entwurf und Präsentation",
          "Nicht für Veröffentlichung", "Kein Konto nötig"], True),
        ("Einzelplatz", "ab 90 €", "je Schnitt, einmalig",
         ["Ein Arbeitsplatz", "Druck und Bildschirm", "Unbefristet",
          "Aktualisierungen enthalten"], False),
        ("Haus", "ab 540 €", "je Familie, einmalig",
         ["Bis 50 Arbeitsplätze", "Einbettung in Software und Apps",
          "Webschnitte ohne Zählung von Aufrufen", "Unbefristet"], False),
    ]
    karten = []
    for i, (n, preis, takt, posten, haupt) in enumerate(stufen):
        liste = "".join(f'<li class="t-body-sm" style="padding:var(--s8) 0">{e(x)}</li>'
                        for x in posten)
        karten.append(f'''<li class="karte karte--offen" data-ein style="--verzug:{i*100}ms">
      <h2 class="t-subheading">{e(n)}</h2>
      <p class="t-heading-sm">{e(preis)}</p>
      <p class="t-caption gedaempft">{e(takt)}</p>
      <ul style="margin:var(--s16) 0">{liste}</ul>
      <div style="margin-top:auto">{knopf("Auswählen", "/kontakt/", haupt=haupt)}</div>
    </li>''')
    return f'''<section class="aufmacher">
  <div class="huelle">
    {klammer("Lizenzen")}
    <h1 class="t-heading-lg" data-ein>Einmal kaufen.</h1>
    <p class="t-body-lg" data-ein style="--verzug:100ms;margin-top:var(--s24);max-width:54ch">
      Keine Abonnements, keine Zählung von Seitenaufrufen, keine Nachlizenzierung beim
      Wachsen. Alle Preise netto.</p>
  </div>
</section>
<hr class="linie">
<section class="abschnitt">
  <div class="huelle"><ul class="gitter gitter--3" style="align-items:stretch">{"".join(karten)}</ul></div>
</section>
<hr class="linie">
<section class="abschnitt">
  <div class="huelle stapeln stapeln--weit" style="max-width:56ch">
    {klammer("Was das heisst")}
    <p class="t-body-lg" data-ein>Eine Lizenz gilt für das, wofür Sie sie gekauft haben,
      und zwar dauerhaft. Wenn Ihr Unternehmen wächst, wächst die Rechnung nicht mit.</p>
    <p class="t-body gedaempft" data-ein style="--verzug:100ms">Webschnitte liefern wir als
      woff2 zum Selbsthosten. Wir zählen keine Aufrufe und betreiben keinen Dienst, der
      ausfallen könnte. Was auf Ihrem Server liegt, liegt auf Ihrem Server.</p>
  </div>
</section>'''


def ueber_uns() -> str:
    leute = [
        ("Henrike Baumgartl", "Schriftentwurf",
         "Zeichnet seit elf Jahren Schrift, davor Buchgestaltung. Verantwortet Isaria."),
        ("Milan Prohaska", "Schriftentwurf",
         "Kommt aus der Oberflächengestaltung. Verantwortet Werkgrotesk und Versal Mono."),
        ("Eleni Sarantou", "Schriftproduktion",
         "Hinting, Kerning, Auslieferung. Die Arbeit, die niemand sieht und ohne die nichts funktioniert."),
        ("Jost Weidinger", "Massschrift",
         "Begleitet Unternehmen, die eine eigene Schrift brauchen — und sagt ab, wenn sie keine brauchen."),
        ("Carla Neunteufel", "Lizenzen",
         "Erklärt Lizenzmodelle so, dass Einkauf und Rechtsabteilung dasselbe verstehen."),
    ]
    liste = "".join(f'''<li class="karte karte--offen" data-ein style="--verzug:{(i%3)*100}ms">
      <h3 class="t-subheading">{e(n)}</h3>
      <p class="t-body f-haus">{e(r)}</p>
      <p class="t-body-sm gedaempft">{e(s)}</p></li>''' for i, (n, r, s) in enumerate(leute))
    return f'''<section class="aufmacher">
  <div class="huelle">
    {klammer("Über uns")}
    <h1 class="t-heading-lg" data-ein>Sieben Leute,<br>vier Familien.</h1>
    <p class="t-body-lg" data-ein style="--verzug:100ms;margin-top:var(--s24);max-width:54ch">
      Versal ist 2019 im Westend entstanden, in einem Gewerbehaus an der Ganghoferstrasse.
      Seitdem haben wir vier Familien gezeichnet und keine davon wieder eingestellt.</p>
  </div>
</section>
<hr class="linie">
<section class="abschnitt">
  <div class="huelle stapeln stapeln--weit">
    {klammer("Die Mannschaft")}
    <ul class="gitter gitter--3">{liste}</ul>
  </div>
</section>
<hr class="linie">
<section class="abschnitt">
  <div class="huelle gitter gitter--seite">
    <div class="stapeln">
      {klammer("Woran wir uns halten")}
      <h2 class="t-heading" data-ein>Keine Schrift,<br>die wir nicht selbst setzen würden.</h2>
    </div>
    <div class="stapeln" data-ein style="--verzug:100ms">
      <p class="t-body-lg">Jede Familie wird vor der Auslieferung in echter Arbeit gesetzt —
        ein Geschäftsbericht, ein Handbuch, eine Oberfläche.</p>
      <p class="t-body gedaempft">Was dabei auffällt, kommt zurück in die Zeichnung. Das ist
        der Grund, warum es bei uns vier Familien gibt und nicht vierzig.</p>
    </div>
  </div>
</section>'''


def kontakt() -> str:
    return f'''<section class="aufmacher">
  <div class="huelle">
    {klammer("Kontakt")}
    <h1 class="t-heading-lg" data-ein>Schreiben Sie uns.</h1>
  </div>
</section>
<hr class="linie">
<section class="abschnitt">
  <div class="huelle gitter gitter--seite">
    <form class="stapeln" method="post" action="#" novalidate data-ein>
      <p class="feld"><label for="name">Name</label>
        <input id="name" name="name" type="text" autocomplete="name" required></p>
      <p class="feld"><label for="haus">Unternehmen</label>
        <input id="haus" name="haus" type="text" autocomplete="organization"></p>
      <p class="feld"><label for="post">E-Mail</label>
        <input id="post" name="post" type="email" autocomplete="email" required></p>
      <p class="feld"><label for="anlass">Worum geht es?</label>
        <select id="anlass" name="anlass">
          <option>Lizenz kaufen</option>
          <option>Testschnitte</option>
          <option>Massschrift</option>
          <option>Etwas anderes</option>
        </select></p>
      <p class="feld"><label for="text">Nachricht</label>
        <textarea id="text" name="text" rows="6"></textarea></p>
      <div class="knopfreihe">
        <button class="knopf knopf--haupt" type="submit"><span class="knopf__text">Absenden</span></button>
      </div>
    </form>
    <div class="stapeln stapeln--weit" data-ein style="--verzug:100ms">
      <div class="karte karte--offen">
        <h2 class="t-subheading">Direkt</h2>
        <p class="t-body">post@versal.type</p>
        <p class="t-body">+49 89 411 907 30</p>
      </div>
      <div class="karte karte--offen">
        <h2 class="t-subheading">Anschrift</h2>
        <p class="t-body">Versal GmbH<br>Ganghoferstraße 68<br>80339 München</p>
      </div>
    </div>
  </div>
</section>'''


def impressum() -> str:
    probe_nachweis = "".join(
        f'<li class="t-body-sm" style="padding:var(--s8) 0">{e(x)}</li>' for x in [
            "Space Grotesk (SIL Open Font License) — Probe für Werkgrotesk",
            "Source Serif 4 (SIL Open Font License) — Probe für Isaria",
            "JetBrains Mono (SIL Open Font License) — Probe für Versal Mono",
            "Archivo Black (SIL Open Font License) — Probe für Föhn",
            "Inter Tight (SIL Open Font License) — Oberfläche",
        ])
    return f'''<section class="aufmacher">
  <div class="huelle">{klammer("Impressum")}<h1 class="t-heading-lg" data-ein>Impressum</h1></div>
</section>
<hr class="linie">
<section class="abschnitt">
  <div class="huelle stapeln stapeln--weit" style="max-width:56ch" data-ein>
    <div><h2 class="t-subheading">Anbieter</h2>
      <p class="t-body">Versal GmbH<br>Ganghoferstraße 68, 80339 München</p>
      <p class="t-body">Geschäftsführung: Henrike Baumgartl, Milan Prohaska<br>
        Amtsgericht München, HRB 263118<br>Umsatzsteuer-ID: DE341206877</p></div>
    <div><h2 class="t-subheading">Kontakt</h2>
      <p class="t-body">post@versal.type · +49 89 411 907 30</p></div>
    <div><h2 class="t-subheading">Verantwortlich für den Inhalt</h2>
      <p class="t-body">Henrike Baumgartl, Anschrift wie oben.</p></div>
    <div><h2 class="t-subheading">Schriftnachweis</h2>
      <p class="t-body gedaempft">Die Schriftproben auf dieser Seite werden mit frei
        lizenzierten Schriften gesetzt:</p>
      <ul>{probe_nachweis}</ul></div>
  </div>
</section>'''


def datenschutz() -> str:
    teile = [
        ("Verantwortlicher", "Versal GmbH, Ganghoferstraße 68, 80339 München, "
         "post@versal.type, +49 89 411 907 30."),
        ("Aufruf dieser Seite", "Beim Aufruf werden die technisch notwendigen Daten "
         "verarbeitet, die Ihr Browser übermittelt: gekürzte IP-Adresse, Zeitpunkt, "
         "aufgerufene Adresse und Browserkennung. Rechtsgrundlage ist Artikel 6 Absatz 1 "
         "Buchstabe f DSGVO. Die Protokolle werden nach sieben Tagen gelöscht."),
        ("Keine Einwilligung nötig", "Diese Seite setzt keine Cookies, bindet keine Dienste "
         "Dritter ein, lädt keine Schriften von fremden Servern und erhebt keine Statistik. "
         "Deshalb gibt es hier kein Einwilligungsbanner."),
        ("Testschnitte", "Testschnitte laden Sie ohne Anmeldung herunter. Wir erheben dabei "
         "keine Daten über die reinen Serverprotokolle hinaus und zählen keine Aufrufe."),
        ("Kontaktformular", "Die Angaben aus dem Formular verwenden wir ausschliesslich zur "
         "Bearbeitung Ihrer Anfrage, Rechtsgrundlage Artikel 6 Absatz 1 Buchstabe b "
         "beziehungsweise f DSGVO."),
        ("Ihre Rechte", "Auskunft, Berichtigung, Löschung, Einschränkung, "
         "Datenübertragbarkeit und Widerspruch. Beschwerden nimmt das Bayerische Landesamt "
         "für Datenschutzaufsicht entgegen."),
    ]
    inhalt = "".join(f'<div><h2 class="t-subheading">{e(t)}</h2>'
                     f'<p class="t-body gedaempft">{e(x)}</p></div>' for t, x in teile)
    return f'''<section class="aufmacher">
  <div class="huelle">{klammer("Datenschutz")}<h1 class="t-heading-lg" data-ein>Datenschutz</h1></div>
</section>
<hr class="linie">
<section class="abschnitt">
  <div class="huelle stapeln stapeln--weit" style="max-width:56ch" data-ein>{inhalt}
    <p class="t-caption gedaempft">Stand: Oktober 2026</p>
  </div>
</section>'''


def fehlerseite() -> str:
    return f'''<section class="aufmacher">
  <div class="huelle">
    {klammer("Fehler 404")}
    <h1 class="t-display" data-ein>
      <span class="aufmacher__zeile">Nicht</span>
      <span class="aufmacher__zeile">gesetzt.</span>
    </h1>
    <p class="t-body-lg" data-ein style="--verzug:100ms;margin-top:var(--s32);max-width:48ch">
      Diese Seite gibt es nicht. Von der Startseite aus finden Sie alles.</p>
    <div class="knopfreihe" data-ein style="--verzug:200ms;margin-top:var(--s24)">
      {knopf("Zur Startseite", "/", haupt=True)}
      {knopf("Kontakt", "/kontakt/")}
    </div>
  </div>
</section>'''


SEITEN = [
    ("index.html", "Versal — Schrift für Arbeit",
     "Vier Schriftfamilien aus München für Fliesstext, Tabellen und Bildschirme.", start, "/"),
    ("schaufenster/index.html", "Schaufenster — Versal",
     "Sechs Häuser, die mit einer unserer Familien setzen.", schaufenster, "/schaufenster/"),
    ("massschrift/index.html", "Massschrift — Versal",
     "Eine eigene Schrift für Ihr Unternehmen, in vier bis zehn Monaten.", massschrift, "/massschrift/"),
    ("lizenzen/index.html", "Lizenzen — Versal",
     "Einmal kaufen, dauerhaft nutzen. Keine Abonnements, keine Zählung von Aufrufen.", lizenzen, "/lizenzen/"),
    ("ueber-uns/index.html", "Über uns — Versal",
     "Sieben Leute im Westend, vier Familien seit 2019.", ueber_uns, "/ueber-uns/"),
    ("kontakt/index.html", "Kontakt — Versal", "Schreiben Sie uns.", kontakt, "/kontakt/"),
    ("impressum/index.html", "Impressum — Versal", "Angaben nach § 5 DDG.", impressum, "/impressum/"),
    ("datenschutz/index.html", "Datenschutz — Versal",
     "Was beim Besuch dieser Seite passiert.", datenschutz, "/datenschutz/"),
    ("404.html", "Nicht gesetzt — Versal", "Diese Seite gibt es nicht.", fehlerseite, ""),
]


def main() -> None:
    print("Versal — Seiten bauen\n")
    for pfad, titel, beschr, bauer, aktiv in SEITEN:
        schreibe(pfad, seite(titel, beschr, bauer(), aktiv))
    for f in FAMILIEN:
        schreibe(f["pfad"].strip("/") + "/index.html",
                 seite(f'{f["name"]} — Versal',
                       f'{f["klasse"]}: {f["kurz"]} {f["satz"][:90]}',
                       familienseite(f), f["pfad"]))
    (ZIEL / "robots.txt").write_text("User-agent: *\nDisallow: /\n", encoding="utf-8")
    print("  robots.txt")
    print(f"\n  {len(SEITEN) + len(FAMILIEN)} Seiten gebaut.")


if __name__ == "__main__":
    main()
