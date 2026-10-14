---
id: UR-INS-08
typ: dokument
rodzaj: instrukcja
tytul: "Instrukcja eksploatacji i BHP: prasa hydrauliczna PH-250"
opis: "obsługa i BHP prasy PH-250, kody błędów E01-E07, kto może restartować szafę sterowniczą"
slowa_kluczowe: [prasa, PH-250, BHP, kod błędu, E01, E07, restart, SEP, Fehlercode]
wersja: "2.3"
status: obowiązujący
obowiazuje_od: 2025-11-10
nastepny_przeglad: 2027-11-10
wlasciciel: Utrzymanie Ruchu (Łukasz Mazur)
dzial: Utrzymanie Ruchu
klasyfikacja: WEWNĘTRZNE
wzorzec: oryginal
oryginal: zalaczniki/oryginaly/UR-INS-08.pdf
powiazane: [UR-ZAL-08A]
---
# Prasa hydrauliczna PH-250: instrukcja eksploatacji i BHP

## 1. Zasady bezpieczeństwa
- Prasę obsługują wyłącznie osoby przeszkolone i wpisane do rejestru operatorów.
- Praca tylko przy sprawnym **sterowaniu oburęcznym** i **kurtynie świetlnej**.
- Przed każdą pracą serwisową obowiązuje procedura **LOTO** (odłączenie i zablokowanie energii).
- Zakaz wkładania rąk w strefę roboczą podczas cyklu.

## 2. Przeglądy
| Częstotliwość | Kto | Zakres |
|---|---|---|
| codziennie, przed zmianą | operator | poziom oleju, wycieki, test kurtyny świetlnej |
| co tydzień | mechanik UR | połączenia hydrauliczne, stan węży |
| co 500 motogodzin | mechanik UR | wymiana filtra oleju |
| co 2 000 motogodzin | mechanik UR | wymiana oleju HLP 46 (180 l) |

## 3. Kody błędów
| Kod | Znaczenie | Działanie |
|---|---|---|
| E01 | Przegrzanie oleju (> 65°C) | zatrzymać prasę, sprawdzić chłodnicę i wentylator |
| E02 | Za niskie ciśnienie w układzie (< 180 bar) | sprawdzić filtr ssawny i pompę; wezwać UR |
| E03 | Przerwana kurtyna świetlna | usunąć przeszkodę, zresetować przyciskiem RESET |
| E04 | Brak sygnału czujnika górnego położenia | wezwać UR: nie kontynuować pracy |
| E05 | Przekroczenie siły nacisku 250 t | sprawdzić narzędzie i ustawienia receptury |
| E06 | Niski poziom oleju | uzupełnić olej HLP 46, sprawdzić wycieki |
| E07 | Błąd komunikacji PLC | restart szafy sterowniczej **wyłącznie przez elektryka z uprawnieniami SEP** |

## 4. Kontakt
Dyżur Utrzymania Ruchu Łomża: wewn. 455 (24/7).

> Uwaga: od firmware 3.2 (09.2026) panel pokazuje także kod **E08**, opis w UR-ZAL-08A (transkrypcja naklejki z panelu).
