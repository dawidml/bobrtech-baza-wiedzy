"""Raport przeglądów: dokumenty po terminie i z terminem w ciągu N dni, według właścicieli.

  python raport_przegladow.py            # domyślnie 30 dni
  python raport_przegladow.py --dni 60 --baza ../baza_wiedzy_poufna
"""
import sys
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from kb_wspolne import czytaj, parser, pliki_wiedzy, znajdz_baze

p = parser("Raport przeglądów według właścicieli")
p.add_argument("--dni", type=int, default=30, help="ile dni naprzód (domyślnie 30)")
a = p.parse_args()
root = znajdz_baze(a.baza or a.sciezka)
dzis = date.today()
granica = (dzis + timedelta(days=a.dni)).isoformat()
wg = defaultdict(list)
for plik in pliki_wiedzy(root):
    meta, _ = czytaj(plik)
    if not meta or meta.get("typ") != "dokument" or not meta.get("nastepny_przeglad"):
        continue
    t = str(meta["nastepny_przeglad"])
    if t <= granica:
        stan = "PO TERMINIE" if t < dzis.isoformat() else "wkrótce"
        wg[meta.get("wlasciciel") or "brak właściciela"].append(f"{stan:12} {t}  {meta.get('id')} {meta.get('wersja', '')}: {meta.get('tytul')}")
print(f"Raport przeglądów {root.name}, {dzis.isoformat()} (termin do {granica})\n")
for w, lista in sorted(wg.items()):
    print(w)
    for x in sorted(lista):
        print("  " + x)
if not wg:
    print("Brak dokumentów do przeglądu.")
