---
id: JK-DANE-01
typ: dane
tytul: Reklamacje 2024-2026 (eksport z Reklamatora)
opis: "liczba, koszty i przyczyny reklamacji według produktu, klienta, kraju i okresu"
plik: dane/reklamacje_2024_2026.csv
zrodlo: "system Reklamator, eksport co tydzień"
ostatnia_aktualizacja: 2026-01-05
czestotliwosc: co tydzień
wlasciciel: Dział Jakości
klasyfikacja: WEWNĘTRZNE
---
- 317 wierszy, separator `;`, kodowanie UTF-8, daty RRRR-MM-DD, `koszt_zl` w złotych netto.
- Kolumny: id, data_zgloszenia, klient, kraj, produkt, klasa (A/B/C), kategoria_wady, opis (PL/EN/DE/SV/NO),
  ilosc_reklamowana, przyczyna_zrodlowa, dzialanie_korygujace, status, koszt_zl, dni_do_pierwszej_odpowiedzi.
- `kategoria_wady`: korozja, wymiar, certyfikat, twardosc, transport, powloka, ilosc, zadziory, spoina, halas.
- Znane problemy: opisy w kilku językach; nazwy klientów pełne (z formą prawną).
- Sprawdzone pytanie: reklamacje BT-WSP-300 w 2025 = 40.
