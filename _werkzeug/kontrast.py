#!/usr/bin/env python3
"""Versal — Kontraste rechnen. Aufruf: python3 _werkzeug/kontrast.py"""

F = {
    "schwarz":   "#0e100f",  # Canvas
    "offblack":  "#191919",  # Fusszeile, verschachtelte Flaechen
    "creme":     "#fffce1",  # Hauptschrift
    "creme50":   "#7c7c6f",  # gedaempfte Schrift
    "creme25":   "#42433d",  # Haarlinien
    "gruen":     "#0ae448",  # Haus
    "hellgruen": "#abff84",
    "orange":    "#ff8709",  # Antiqua
    "pink":      "#fec5fb",  # Auszeichnung
    "lila":      "#9d95ff",  # dicktengleich
    "blau":      "#00bae2",  # Grotesk
}

def lum(h: str) -> float:
    h = h.lstrip("#")
    t = []
    for i in (0, 2, 4):
        c = int(h[i:i+2], 16) / 255
        t.append(c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4)
    return 0.2126 * t[0] + 0.7152 * t[1] + 0.0722 * t[2]

def k(a: str, b: str) -> float:
    la, lb = sorted((lum(F[a]), lum(F[b])), reverse=True)
    return (la + 0.05) / (lb + 0.05)

GRUPPEN = [
    ("Schrift auf dem Canvas", 4.5, [
        ("creme", "schwarz"), ("creme50", "schwarz"),
    ]),
    ("Die Farbtaxonomie auf dem Canvas", 4.5, [
        ("gruen", "schwarz"), ("hellgruen", "schwarz"), ("orange", "schwarz"),
        ("pink", "schwarz"), ("lila", "schwarz"), ("blau", "schwarz"),
    ]),
    ("Auf der Fusszeile (Off Black)", 4.5, [
        ("creme", "offblack"), ("creme50", "offblack"), ("gruen", "offblack"),
    ]),
    ("Raender von Bedienelementen", 3.0, [
        ("creme", "schwarz"), ("gruen", "schwarz"), ("creme25", "schwarz"),
    ]),
    ("Grosse Grade ab 24px (Ziel 3,0)", 3.0, [
        ("creme50", "schwarz"), ("orange", "schwarz"), ("blau", "schwarz"),
    ]),
]

def main() -> None:
    print("Versal — Kontraste\n")
    probleme = []
    for titel, ziel, paare in GRUPPEN:
        print(f"{titel}   (Ziel {ziel}:1)")
        for a, b in paare:
            w = k(a, b)
            ok = w >= ziel
            if not ok:
                probleme.append((titel, a, b, w, ziel))
            print(f"  {a:<10} auf {b:<9} {w:6.2f}:1  {'ok' if ok else 'DURCHGEFALLEN'}")
        print()
    if probleme:
        print("ZU KLAEREN:")
        for t, a, b, w, z in probleme:
            print(f"  {a} auf {b}: {w:.2f}:1, gefordert {z} — {t}")
    else:
        print("Alle Pruefungen bestanden.")

if __name__ == "__main__":
    main()
