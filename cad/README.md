# cad/: pliki konstrukcyjne w Git (przykład)

Aktualna rewizja: **A**

## BT-TUL-35 Tuleja ślizgowa Ø35 (CuSn12)

| Plik | Do czego | Jak GitHub go pokazuje |
|---|---|---|
| `BT-TUL-35/BT-TUL-35.stl` | model 3D (format neutralny) | podgląd 3D w przeglądarce: obracanie, przybliżanie (pliki do 10 MB) |
| `BT-TUL-35/BT-TUL-35_rysunek.png` | rysunek eksportowany z CAD | porównanie obrazów: 2-up, swipe, onion skin |
| model natywny, np. `.sldprt`, `.ipt`, `.FCStd` | praca konstruktora | przez Git LFS i blokadę (`lockable` w `.gitattributes`), bez podglądu |

| Rew. | Data | Zmiana | Autor |
|---|---|---|---|
| A | 2026-05-18 | pierwsze wydanie, L = 40 mm | Biuro Konstrukcyjne |

## Zasady
1. Model natywny i jego eksport (STL lub STEP + rysunek PDF/PNG) zawsze w tym samym commicie.
2. Przed edycją pliku natywnego: `git lfs lock <plik>`; po wysłaniu zmian: `git lfs unlock <plik>`.
   Plików binarnych CAD nie da się scalić: blokada zapobiega dwóm równoległym wersjom.
3. Opis commita: numer części, rewizja, numer zlecenia zmiany.
4. Wydanie rewizji = tag, np. `BT-TUL-35-revB`.
