---
id: SP-DANE-01
typ: dane
tytul: Zamówienia z października 2026 (eksport z ERP)
opis: "zamówienia klientów: klient, kod wyrobu, ilość, wartość netto, data, status"
plik: dane/zamowienia_2026-10.json
zrodlo: "ERP, eksport miesięczny"
ostatnia_aktualizacja: 2026-11-02
czestotliwosc: co miesiąc
wlasciciel: Dział Sprzedaży
klasyfikacja: WEWNĘTRZNE
---
- JSON: obiekt z polami `eksport`, `data`, `zamowienia` (lista 48 zamówień).
- Pola zamówienia: nr_zamowienia, klient, kod, ilosc, wartosc_netto_pln (złote netto), data_zamowienia, status.
- Źródłem prawdy jest ERP; plik to kopia z datą eksportu.
