# INDEX: mapa bazy wiedzy BOBRTECH (baza_wiedzy)
<!-- Plik generowany skryptem zbuduj_indeks.py (skill kb-indeks). Nie edytuj ręcznie. Stan: 2026-11-12 -->

Zacznij tutaj, potem otwórz `INDEX.md` w folderze tematycznym.

## Gdzie szukać
| Pytanie dotyczy | Folder | Właściciel obszaru |
|---|---|---|
| skróty i nazwy systemów, struktura organizacyjna, kto komu podlega | `00_ogolne/` | Biuro Zarządu |
| delegacje, praca zdalna i hybrydowa, onboarding, urlopy, benefity | `10_hr/` | Dział HR (Anna Kowalczyk) |
| reklamacje: procedura, terminy, noty kredytowe, zdjęcia wad | `20_jakosc/` | Dział Jakości (Marta Zielińska) |
| ceny, rabaty, warunki płatności, produkty, MOQ, czasy realizacji | `30_sprzedaz/` | Dyrektor Handlowy (Tomasz Wróbel) |
| maszyny, kody błędów, BHP, magazyn i składowanie | `40_produkcja/` | Utrzymanie Ruchu (Łukasz Mazur) |
| dostawcy: karty, oceny, kategorie | `50_zakupy/` | Dział Zakupów |
| narzędzia AI, klasy informacji, incydenty bezpieczeństwa | `60_it/` | Dział IT i Bezpieczeństwa (Kamil Sadowski) |
| liczby: reklamacje, zamówienia, oceny dostawców (licz skryptem) | `dane/` | właściciel w karcie danych |

## Źródła prawdy
| Informacja | Jedyne źródło |
|---|---|
| MOQ i czasy realizacji | SP-KAT |
| ceny wyrobów | SP-CEN |
| dopłaty | SP-CEN |
| dozwolone narzędzia AI | IT-POL-11 |
| klasy informacji | IT-POL-11 |
| limity noclegów | HR-POL-03 |
| parametry produktów | SP-KAT |
| podległość służbowa | OG-ORG |
| rabaty | SP-CEN |
| terminy i klasy reklamacji | JK-PR-07 |
| warunki płatności | SP-CEN |
| zasady pracy zdalnej i ryczałt | HR-REG-05 |
| zasady rozliczania delegacji | HR-POL-03 |
| zatwierdzanie not kredytowych | JK-PR-07 |
| znaczenie skrótów i nazw systemów | OG-SL-01 |

## Dane do liczenia (licz skryptem, nie szacuj)
- JK-DANE-01: liczba, koszty i przyczyny reklamacji według produktu, klienta, kraju i okresu (karta: `dane/reklamacje_2024_2026.md`, plik: `dane/reklamacje_2024_2026.csv`)
- SP-DANE-01: zamówienia klientów: klient, kod wyrobu, ilość, wartość netto, data, status (karta: `dane/zamowienia_2026-10.md`, plik: `dane/zamowienia_2026-10.json`)
- ZK-OC-2025: ranking i kategorie dostawców (A, B, C), ocena punktowa, OTD, liczba reklamacji, status (karta: `dane/dostawcy_ocena_2025.md`, plik: `dane/dostawcy_ocena_2025.csv`)

## Obrazy i oryginały
Obrazy: `zalaczniki/obrazy/`, oryginały: `zalaczniki/oryginaly/`. Każdy obraz ma opis w pliku `.md` (pole `obraz:`).

## Archiwum
Stare wersje są w historii Git tego repozytorium (`git log`, tag `dzien-1`). Nie używaj ich do odpowiedzi.
