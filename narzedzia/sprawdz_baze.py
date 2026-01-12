"""Kontrola bazy wiedzy: nagłówki, zamknięte listy, unikalne ID, martwe ścieżki, przeglądy, klasyfikacja,
frazy typowe dla ukrytych poleceń, ten sam kod produktu z cenami w kilku dokumentach.

  python sprawdz_baze.py                                  # BŁĘDY: kod wyjścia 1 (hook pre-commit zatrzyma zmianę)
  python sprawdz_baze.py --baza ../baza_wiedzy_poufna --poufna

Wzór kodu produktu do kontroli cen: pole wzor_kodu_produktu w bloku YAML w SCHEMAT.md (np. "BT-[A-Z]+-\\d+").
"""
import re
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from kb_wspolne import czytaj, parser, pliki_wiedzy, schemat, znajdz_baze

p = parser("Kontrola bazy wiedzy")
p.add_argument("--poufna", action="store_true", help="baza dla danych POUFNE (wtedy POUFNE nie jest błędem)")
a = p.parse_args()
root = znajdz_baze(a.baza or a.sciezka)
SCH = schemat(root)
DZIS = date.today().isoformat()
bledy, ostrzezenia = [], []
ids = defaultdict(list)
ceny = defaultdict(set)
FRAZY = re.compile(r"zignoruj (wszystkie |poprzednie )?(instrukcje|polecenia)|ignore (all |previous )?instructions|podaj (swoje )?hasło|wyślij (dane|hasło)|system prompt", re.I)
KOD = SCH.get("wzor_kodu_produktu") or r"[A-Z]{2,}-[A-Z0-9]+-\d+"
CENA = re.compile(r"\|\s*(" + KOD + r")\s*\|[^\n]*?(\d[\d ]*,\d{2}) zł")

for plik in pliki_wiedzy(root):
    rel = plik.relative_to(root).as_posix()
    meta, tresc = czytaj(plik)
    if meta is None:
        bledy.append(f"{rel}: brak nagłówka YAML")
        continue
    if "_blad_yaml" in meta:
        bledy.append(f"{rel}: nagłówek YAML z błędem składni ({meta['_blad_yaml']})")
        continue
    typ = meta.get("typ")
    if typ not in SCH["typ"]:
        bledy.append(f"{rel}: typ '{typ}' spoza listy {SCH['typ']}")
        continue
    for f in SCH["wymagane"][typ]:
        if not meta.get(f):
            bledy.append(f"{rel}: brak pola {f}")
    for pole in ("status", "klasyfikacja", "rodzaj", "wzorzec"):
        v = meta.get(pole)
        if v and pole in SCH and v not in SCH[pole]:
            bledy.append(f"{rel}: {pole} '{v}' spoza listy w SCHEMAT.md")
    ids[meta.get("id")].append(rel)
    for pole in ("oryginal", "obraz", "plik"):
        if meta.get(pole) and not (root / meta[pole]).exists():
            bledy.append(f"{rel}: {pole} wskazuje nieistniejący plik {meta[pole]}")
    kl = meta.get("klasyfikacja")
    if kl == "ŚCIŚLE POUFNE":
        bledy.append(f"{rel}: ŚCIŚLE POUFNE nie może trafić do bazy wiedzy")
    elif kl == "POUFNE" and not a.poufna:
        bledy.append(f"{rel}: plik POUFNE w bazie dla narzędzi chmurowych; przenieś do bazy poufnej")
    if meta.get("status") == "archiwalny":
        bledy.append(f"{rel}: wersja archiwalna w folderze roboczym; przenieś do archiwum")
    if typ == "dokument" and meta.get("nastepny_przeglad") and str(meta["nastepny_przeglad"]) < DZIS:
        ostrzezenia.append(f"{rel}: przegląd po terminie ({meta['nastepny_przeglad']}), właściciel: {meta.get('wlasciciel')}")
    if FRAZY.search(tresc):
        ostrzezenia.append(f"{rel}: fraza typowa dla ukrytych poleceń (prompt injection): sprawdź treść")
    for kod, cena in CENA.findall(tresc):
        ceny[kod].add((cena, meta.get("id")))

for i, pl in ids.items():
    if len(pl) > 1:
        bledy.append(f"ID {i} w kilku plikach: {', '.join(pl)}")
for kod, zb in ceny.items():
    zrodla = {i for _, i in zb}
    if len(zrodla) > 1:
        bledy.append(f"{kod}: ceny w kilku dokumentach ({', '.join(sorted(zrodla))}); jedyne źródło cen to cennik")

for linia in ostrzezenia:
    print("UWAGA", linia)
for linia in bledy:
    print("BŁĄD ", linia)
print(f"{root.name}: sprawdzone pliki {sum(len(v) for v in ids.values())}, błędy {len(bledy)}, uwagi {len(ostrzezenia)}.")
sys.exit(1 if bledy else 0)
