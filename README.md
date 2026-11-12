# Baza wiedzy BOBRTECH w Git (klasy PUBLICZNE i WEWNĘTRZNE)

> **Materiał szkoleniowy.** BOBRTECH sp. z o.o. to firma fikcyjna. Osoby, ceny, klienci i dokumenty są zmyślone.
> Historię sprzed 12.11.2026 odtworzono na potrzeby szkolenia: daty i autorów commitów ustawiono ręcznie.

## Dla uczestników: co obejrzeć w przeglądarce (bez logowania)

| Co zobaczysz | Gdzie kliknąć | Na co zwrócić uwagę |
|---|---|---|
| Cała historia bazy | [Commits](https://github.com/dawidml/bobrtech-baza-wiedzy/commits/main) | kto, kiedy, opis zmiany w jednym zdaniu |
| Zmiana cen w cenniku Excel | [commit SP-CEN 2026-H2](https://github.com/dawidml/bobrtech-baza-wiedzy/commit/04d15cd643c0921a3b907135d6b47f83cda71b92) | `SP-CEN.xlsx`: „Binary file not shown”; podgląd `zalaczniki/podglad/SP-CEN.xlsx.md`: dwa zmienione wiersze |
| Duża zmiana polityki | [commit HR-POL-03 v3.0](https://github.com/dawidml/bobrtech-baza-wiedzy/commit/6ad541b95ac4f8f797f51070064461b0dd23c323) | przełącz widok **Split**; limit hotelu 320 zł → 450/520 zł |
| Historia jednego dokumentu | [HR-POL-03: historia](https://github.com/dawidml/bobrtech-baza-wiedzy/commits/main/10_hr/HR-POL-03_polityka_podrozy_sluzbowych.md) | każda wersja polityki to jeden commit |
| Kto zmienił który wiersz | [Blame cennika](https://github.com/dawidml/bobrtech-baza-wiedzy/blame/main/30_sprzedaz/SP-CEN_cennik_i_rabaty.md) | autor i data przy każdej linii |
| Stan z dnia 1 szkolenia → dziś | [porównanie dzien-1...main](https://github.com/dawidml/bobrtech-baza-wiedzy/compare/dzien-1...main) | zakładka **Files changed** |
| Zmiana w pliku Word | [pull request #2, pliki](https://github.com/dawidml/bobrtech-baza-wiedzy/pull/2/files) | `.md` i podgląd `HR-REG-05.docx.md` mówią to samo |
| Zmiana przygotowana przez agenta AI | [pull request #1](https://github.com/dawidml/bobrtech-baza-wiedzy/pull/1) | agent przygotował, człowiek sprawdził i scalił |
| Projekt dokumentu (jeszcze nie obowiązuje) | [pull request #3, pliki](https://github.com/dawidml/bobrtech-baza-wiedzy/pull/3/files) | otwarty PR = status „projekt”; `main` = wersja obowiązująca |
| Błędna zmiana i jej cofnięcie | [zmiana](https://github.com/dawidml/bobrtech-baza-wiedzy/commit/25b4af05437286d30a193b0f75f3347cbbec440c) → [revert](https://github.com/dawidml/bobrtech-baza-wiedzy/commit/53dd0f8a596865cdd8d1393d2b7780fb3edd8b85) | `git revert` nie usuwa historii, dodaje zmianę odwrotną |
| Zmiana obrazu (schemat organizacyjny) | [commit OG-ORG 2026-11](https://github.com/dawidml/bobrtech-baza-wiedzy/commit/ddf60e9c91a9e6a8452e65533eebafeaedcc58d0) | tryby porównania obrazów: 2-up, Swipe, Onion skin |
| Rysunek i model 3D (CAD) | [commit BT-TUL-35 rew. B](https://github.com/dawidml/bobrtech-baza-wiedzy/commit/8437d2c7d13192f9ad9a346255120a9f1b016c31), [model STL](https://github.com/dawidml/bobrtech-baza-wiedzy/blob/main/cad/BT-TUL-35/BT-TUL-35.stl) | rysunek: Swipe; model: obracanie myszą |
| Automatyczna kontrola | [Actions](https://github.com/dawidml/bobrtech-baza-wiedzy/actions) | pierwszy przebieg czerwony, poprawka w [tym commicie](https://github.com/dawidml/bobrtech-baza-wiedzy/commit/60c73ac883baf333b3ffff2b31b5c278546de8cf) |

Dowolne dwie wersje: `https://github.com/dawidml/bobrtech-baza-wiedzy/compare/STARSZA...NOWSZA` (tag, gałąź albo początek numeru commita).

## Te same informacje lokalnie
```bash
git clone https://github.com/dawidml/bobrtech-baza-wiedzy.git
cd bobrtech-baza-wiedzy
git log --oneline --follow -- 10_hr/HR-POL-03_polityka_podrozy_sluzbowych.md   # historia dokumentu
git show dzien-1:30_sprzedaz/SP-CEN_cennik_i_rabaty.md                        # cennik ze stanu z dnia 1
git diff dzien-1 main --word-diff -- 10_hr/                                   # zmiany słowo po słowie
git blame 30_sprzedaz/SP-CEN_cennik_i_rabaty.md                               # kto zmienił który wiersz
git config diff.dokument.textconv "python narzedzia/podglad_tekstowy.py"      # od teraz git diff czyta docx/xlsx/pptx
git log -p -- zalaczniki/oryginaly/SP-CEN.xlsx
```

## O tej bazie
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
