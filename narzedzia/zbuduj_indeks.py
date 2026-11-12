"""Generuje INDEX.md (główny i w każdym folderze tematycznym) oraz index.jsonl z nagłówków plików .md.

  python zbuduj_indeks.py                      # baza w bieżącym folderze albo wyżej
  python zbuduj_indeks.py --baza ../baza_wiedzy_poufna

Nie edytuj INDEX.md ręcznie poza opisem folderu (tekst nad znacznikiem INDEKS:START).
Plik bez wymaganych pól: błąd z nazwą pliku i kod wyjścia 1, indeks się nie zmienia.
"""
import json
import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from kb_wspolne import czytaj, parser, pliki_wiedzy, schemat, znajdz_baze

a = parser("Buduje INDEX.md i index.jsonl z nagłówków plików").parse_args()
root = znajdz_baze(a.baza or a.sciezka)
SCH = schemat(root)
DZIS = date.today().isoformat()
START, END = "<!-- INDEKS:START (generowany, nie edytuj) -->", "<!-- INDEKS:END -->"

docs, bledy = [], []
for p in pliki_wiedzy(root):
    meta, _ = czytaj(p)
    rel = p.relative_to(root).as_posix()
    if meta is None:
        bledy.append(f"{rel}: brak nagłówka YAML")
        continue
    if "_blad_yaml" in meta:
        bledy.append(f"{rel}: nagłówek YAML z błędem składni ({meta['_blad_yaml']})")
        continue
    typ = meta.get("typ")
    brak = [f for f in SCH["wymagane"].get(typ, SCH["wymagane"]["dokument"]) if not meta.get(f)]
    if brak:
        bledy.append(f"{rel}: brak pól {', '.join(brak)}")
        continue
    docs.append(dict(meta, sciezka=rel))

if bledy:
    print("Indeks NIE został zbudowany:\n  " + "\n  ".join(bledy))
    sys.exit(1)

docs.sort(key=lambda d: d["id"])
with open(root / "index.jsonl", "w", encoding="utf-8", newline="\n") as f:
    for d in docs:
        f.write(json.dumps({k: d.get(k) for k in ("id", "typ", "rodzaj", "tytul", "opis", "wersja", "status", "klasyfikacja", "wlasciciel",
                                                    "nastepny_przeglad", "zrodlo_prawdy_dla", "slowa_kluczowe", "sciezka")}, ensure_ascii=False) + "\n")


def linia(d, folder):
    wer = f" {d['wersja']}" if d.get("wersja") else (f" ({d['data']})" if d.get("data") else "")
    rel = Path(d["sciezka"]).relative_to(folder).as_posix() if folder != "." else d["sciezka"]
    prz = f", przegląd {d['nastepny_przeglad']}" if d.get("nastepny_przeglad") else ""
    return f"- {d['id']}{wer}: {d['opis']} (`{rel}`{prz})"


# INDEX.md w folderach tematycznych (pierwszy poziom)
foldery = sorted({Path(d["sciezka"]).parts[0] for d in docs if len(Path(d["sciezka"]).parts) > 1})
gdzie = []
for fol in foldery:
    idx = root / fol / "INDEX.md"
    opis_folderu = f"---\nopis: \"\"\nwlasciciel: \"\"\n---\n# {fol}\n\n"
    if idx.exists():
        opis_folderu = idx.read_text(encoding="utf-8").split(START)[0].rstrip() + "\n\n"
    meta, _ = czytaj(idx) if idx.exists() else ({}, "")
    lista = "\n".join(linia(d, fol) for d in docs if d["sciezka"].startswith(fol + "/"))
    idx.write_text(f"{opis_folderu}{START}\n{lista}\n{END}\n", encoding="utf-8", newline="\n")
    gdzie.append((fol, (meta or {}).get("opis", ""), (meta or {}).get("wlasciciel", "")))

zrodla = [(z, d["id"]) for d in docs for z in (d.get("zrodlo_prawdy_dla") or [])]
dane = [d for d in docs if d.get("typ") == "dane"]
firma = f" {SCH['firma']}" if SCH.get("firma") else ""
if (root.parent / f"{root.name}_archiwum").is_dir():
    archiwum = f"poza tym folderem (`{root.name}_archiwum/`)"
elif (root / ".git").exists():
    archiwum = "w historii Git tego repozytorium (`git log`, tag `dzien-1`)"
else:
    archiwum = "poza tym folderem (osobne archiwum)"
nazwa = SCH.get("nazwa_bazy") or root.name  # stała nazwa: indeks nie zależy od folderu, do którego sklonowano repozytorium
tekst = [f"# INDEX: mapa bazy wiedzy{firma} ({nazwa})",
         f"<!-- Plik generowany skryptem zbuduj_indeks.py (skill kb-indeks). Nie edytuj ręcznie. Stan: {DZIS} -->", "",
         "Zacznij tutaj, potem otwórz `INDEX.md` w folderze tematycznym.", "", "## Gdzie szukać", "| Pytanie dotyczy | Folder | Właściciel obszaru |", "|---|---|---|"]
tekst += [f"| {o or '-'} | `{f}/` | {w or '-'} |" for f, o, w in gdzie]
tekst += ["", "## Źródła prawdy", "| Informacja | Jedyne źródło |", "|---|---|"] + [f"| {z} | {i} |" for z, i in sorted(zrodla)]
if dane:
    tekst += ["", "## Dane do liczenia (licz skryptem, nie szacuj)"] + [f"- {d['id']}: {d['opis']} (karta: `{d['sciezka']}`, plik: `{d.get('plik', '')}`)" for d in dane]
tekst += ["", "## Obrazy i oryginały", "Obrazy: `zalaczniki/obrazy/`, oryginały: `zalaczniki/oryginaly/`. Każdy obraz ma opis w pliku `.md` (pole `obraz:`).",
          "", "## Archiwum", f"Stare wersje są {archiwum}. Nie używaj ich do odpowiedzi.", ""]
# Data „Stan” zmienia się tylko razem z treścią: bez tego każdy commit zmieniałby INDEX.md (szum w historii Git).
nowy = "\n".join(tekst)
stary = (root / "INDEX.md").read_text(encoding="utf-8") if (root / "INDEX.md").exists() else ""
bez_daty = lambda t: re.sub(r"Stan: \d{4}-\d{2}-\d{2}", "Stan: -", t)
if bez_daty(stary) != bez_daty(nowy):
    (root / "INDEX.md").write_text(nowy, encoding="utf-8", newline="\n")
print(f"Indeks {root.name}: pliki {len(docs)}, foldery {len(foldery)}, źródła prawdy {len(zrodla)}. Zapisano INDEX.md i index.jsonl.")
