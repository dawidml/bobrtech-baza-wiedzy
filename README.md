# Baza wiedzy BOBRTECH w Git (klasy PUBLICZNE i WEWNĘTRZNE)

> **Materiał szkoleniowy.** BOBRTECH sp. z o.o. to firma fikcyjna. Osoby, ceny, klienci i dokumenty są zmyślone.

Start: `INDEX.md`. Zasady dla agentów: `AGENTS.md` (Claude Code czyta `CLAUDE.md`, który importuje `AGENTS.md`).

## Jak ta baza korzysta z Git
- Jeden plik `.md` na dokument. Oryginały (docx, xlsx, pptx, pdf) w `zalaczniki/oryginaly/` ze **stałą nazwą**,
  np. `SP-CEN.xlsx`. Wersje są w historii Git, nie w nazwie pliku (koniec z `cennik_v2_FINAL.xlsx`).
- Stare wersje nie leżą w osobnym folderze archiwum: `git log`, `git show <commit>:<plik>`, tag `dzien-1`.
- `zalaczniki/podglad/` to tekstowy podgląd plików Office, generowany automatycznie. Dzięki niemu GitHub
  pokazuje w przeglądarce, co zmieniło się w xlsx, docx i pptx (sam oryginał GitHub widzi jako plik binarny).
- Zmiana dokumentu: gałąź, commit `ID wersja: co się zmieniło`, pull request, przegląd właściciela, scalenie.
- Folder `cad/`: przykład pracy z modelem 3D i rysunkiem.
- Baza POUFNE (umowy, protokoły zarządu) to **osobne, prywatne repozytorium** z innymi uprawnieniami.

## Narzędzia
```bash
pip install -r narzedzia/requirements.txt
python narzedzia/sprawdz_baze.py          # kontrola nagłówków, ID, ścieżek, przeglądów, cen
python narzedzia/zbuduj_indeks.py         # INDEX.md, INDEX.md w folderach, index.jsonl
python narzedzia/podglad_tekstowy.py --wszystkie   # zalaczniki/podglad/*.md z plików Office
python narzedzia/raport_przegladow.py     # przeglądy po terminie i w ciągu 30 dni
git config core.hooksPath .githooks       # kontrola, indeks i podgląd przy każdym commicie
git config diff.dokument.textconv "python narzedzia/podglad_tekstowy.py"   # git diff dla docx/xlsx/pptx
```

Blokady dla agentów: `.claude/settings.json` (Claude Code, z sandboxem) i `.codex/config.toml` (Codex, tylko odczyt).
Kontrola przy każdym pull requeście: `.github/workflows/kontrola-bazy.yml`.
