"""Pytania testowe przez agenta w trybie tylko do odczytu: claude -p albo codex exec.

  python pytania_testowe.py --agent claude          # albo --agent codex
  python pytania_testowe.py --agent codex --nr 1 4 7 --baza ../baza_wiedzy

Pytania: testy/pytania_testowe.csv w bazie (separator ;, kolumny nr, pytanie, oczekiwana_odpowiedz, zrodlo, typ).
Ocena: czy odpowiedź zawiera oczekiwaną wartość i ID źródła. Wynik: testy/wyniki_RRRR-MM-DD_agent.csv
"""
import csv
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from kb_wspolne import parser, znajdz_baze

p = parser("Pytania testowe bazy wiedzy przez claude -p albo codex exec")
p.add_argument("--agent", choices=["claude", "codex"], default="claude")
p.add_argument("--nr", nargs="*", help="tylko wybrane numery pytań")
p.add_argument("--pytania", help="inny plik CSV z pytaniami (domyślnie testy/pytania_testowe.csv)")
a = p.parse_args()
root = znajdz_baze(a.baza or a.sciezka)
cmd = {"claude": ["claude", "-p", "--permission-mode", "plan"], "codex": ["codex", "exec", "--sandbox", "read-only"]}[a.agent]
if not shutil.which(cmd[0]):
    sys.exit(f"Nie znaleziono polecenia {cmd[0]}.")
plik_pytan = Path(a.pytania) if a.pytania else root / "testy" / "pytania_testowe.csv"
if not plik_pytan.exists():
    sys.exit(f"Brak pliku z pytaniami: {plik_pytan}")
rows = list(csv.DictReader(open(plik_pytan, encoding="utf-8"), delimiter=";"))
wyniki, ok = [], 0
for r in rows:
    if a.nr and r["nr"] not in a.nr:
        continue
    out = subprocess.run(cmd + [r["pytanie"]], cwd=root, capture_output=True, text=True, timeout=600).stdout
    wartosc = r["oczekiwana_odpowiedz"].lower() in out.lower()
    zrodla = [z.strip() for z in r.get("zrodlo", "").split("+") if z.strip() not in ("-", "")]
    zrodlo = not zrodla or any(z.split()[0] in out for z in zrodla)
    ok += wartosc and zrodlo
    wyniki.append([r["nr"], r.get("typ", ""), wartosc, zrodlo, out.strip().replace("\n", " ")[:500]])
    print(f"{r['nr']:>3} {'OK ' if wartosc and zrodlo else 'BŁĄD'} {r['pytanie'][:70]}")
(root / "testy").mkdir(exist_ok=True)
plik = root / "testy" / f"wyniki_{date.today().isoformat()}_{a.agent}.csv"
with open(plik, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(["nr", "typ", "wartosc_ok", "zrodlo_ok", "odpowiedz"])
    w.writerows(wyniki)
print(f"Wynik: {ok}/{len(wyniki)}. Szczegóły: {plik}. Pytania POUFNE oceniaj ręcznie (oczekiwana odmowa).")
