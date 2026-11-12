# Schemat nagłówków bazy wiedzy BOBRTECH

Jedno źródło zamkniętych list i pól wymaganych. Czytają go skrypty w `narzedzia/` i w skillach (blok YAML poniżej) oraz ludzie.
Jedna pisownia: „obowiązujący” i „obowiazujacy” to dla skryptu dwie różne wartości.

## Identyfikatory
- `DZIAŁ-RODZAJ-NUMER`. Działy: OG, HR, JK, SP, UR, MAG, ZK, IT, ZR, KOR, UM.
  Rodzaje: POL, REG, PR, INS, FAQ, CEN, KAT, SL, ORG, ZAL, DOS, OC, ZDJ, DANE, PROT.
- Dokumenty aktualizowane mają stałe ID bez roku (`SP-CEN`, wersja w nagłówku: `2026-H2`).
- Zapisy mają datę w ID (`KOR-2026-031`, `ZR-PROT-2026-Q3`).
- Plik: `ID_temat.md`; załącznik: to samo ID (`zalaczniki/obrazy/UR-ZAL-08A_panel_bledow.png`).
- Oryginał w repozytorium Git ma stałą nazwę bez wersji: `zalaczniki/oryginaly/SP-CEN.xlsx`. Wersje są w historii Git, nie w nazwie pliku.
- Cytat w odpowiedzi: `[ID wersja §sekcja]`, np. `[HR-POL-03 v3.0 §3]`.

```yaml
typ: [dokument, zapis, dane]
status: [projekt, obowiązujący, archiwalny]
klasyfikacja: [PUBLICZNE, WEWNĘTRZNE, POUFNE, ŚCIŚLE POUFNE]
wzorzec: [md, oryginal]
rodzaj: [polityka, regulamin, procedura, instrukcja, FAQ, słownik, struktura, cennik, katalog, karta, umowa, notatka,
         protokół, ustalenie, zdjęcie, dane]
wymagane:
  dokument: [id, typ, rodzaj, tytul, opis, wersja, status, obowiazuje_od, nastepny_przeglad, wlasciciel, dzial, klasyfikacja, wzorzec]
  zapis: [id, typ, rodzaj, tytul, opis, data, status, wlasciciel, dzial, klasyfikacja]
  dane: [id, typ, tytul, opis, plik, zrodlo, ostatnia_aktualizacja, wlasciciel, klasyfikacja]
ranga: [polityka, regulamin, procedura, instrukcja, FAQ, notatka]
firma: BOBRTECH
nazwa_bazy: baza_wiedzy
wzor_kodu_produktu: 'BT-[A-Z]+-\d+'
```

## Kolejność pierwszeństwa (ta sama w AGENTS.md)
1. Tylko dokumenty `obowiązujący`, których okres obowiązywania obejmuje dzisiejszą datę.
2. Zobowiązania wobec klienta (umowa, potwierdzone ustalenie) przed dokumentami wewnętrznymi; ustalenie dla zamówienia przed umową ramową.
3. Dokumenty wewnętrzne według `rodzaj`: polityka i regulamin, procedura, instrukcja, FAQ i notatka.
4. Ta sama ranga: późniejsza data `obowiazuje_od`.
5. Liczby: dane z systemu przed liczbą przepisaną do dokumentu.
6. Uzupełnienie (`powiazane`) to nie sprzeczność.
7. Nadal niejasne: obie wersje z ID i właściciel.
