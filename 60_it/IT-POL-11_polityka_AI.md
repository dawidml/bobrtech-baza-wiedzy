---
id: IT-POL-11
typ: dokument
rodzaj: polityka
tytul: Polityka korzystania z narzędzi AI i klasyfikacji informacji
opis: "jakich narzędzi AI wolno używać do jakich danych, klasy informacji, zgłaszanie incydentów"
slowa_kluczowe: [AI, ChatGPT, Claude, Bóbr, klasyfikacja, POUFNE, polityka AI, incydent]
wersja: "1.2"
status: obowiązujący
obowiazuje_od: 2026-05-01
nastepny_przeglad: 2027-05-01
wlasciciel: Dział IT i Bezpieczeństwa (Kamil Sadowski)
dzial: IT
klasyfikacja: WEWNĘTRZNE
wzorzec: md
oryginal: zalaczniki/oryginaly/IT-POL-11.pdf
zrodlo_prawdy_dla: [dozwolone narzędzia AI, klasy informacji]
---
# Polityka korzystania z narzędzi AI (IT-POL-11)

## 1. Klasy informacji
| Klasa | Przykłady |
|---|---|
| PUBLICZNE | katalog produktów, strona www, ogłoszenia o pracę |
| WEWNĘTRZNE | procedury, regulaminy, instrukcje stanowiskowe |
| POUFNE | ceny i umowy klientów strategicznych, rysunki techniczne klientów, dane osobowe pracowników, wyniki finansowe przed publikacją |
| ŚCIŚLE POUFNE | dane płacowe, informacje o przejęciach, hasła i klucze dostępowe |

## 2. Dozwolone narzędzia
| Narzędzie | Dozwolone klasy informacji |
|---|---|
| Claude Team (konto firmowe) | PUBLICZNE, WEWNĘTRZNE |
| ChatGPT Business (konto firmowe) | PUBLICZNE, WEWNĘTRZNE |
| Asystent **Bóbr** (on-premise, serwerownia Białystok) | PUBLICZNE, WEWNĘTRZNE, POUFNE |
| Jakiekolwiek narzędzie AI | ŚCIŚLE POUFNE: **zakaz** |

Korzystanie z prywatnych kont narzędzi AI do celów służbowych jest zabronione.

## 3. Zasady pracy z AI
1. Za wynik pracy odpowiada człowiek, nie narzędzie. Liczby, nazwy, terminy i cytowane przepisy należy zweryfikować w źródle.
2. Treści wysyłane do klientów, przygotowane z pomocą AI, muszą zostać sprawdzone przez osobę odpowiedzialną za relację z klientem.
3. Nie wolno wklejać do narzędzi AI treści otrzymanych od klientów z klauzulą poufności, chyba że narzędzie jest dozwolone dla klasy POUFNE.
4. Automatyzacje i agenci AI z dostępem do systemów firmowych (ERP, Reklamator, poczta) wymagają zgody Działu IT i wpisu do rejestru automatyzacji.

## 4. Incydenty
Podejrzenie wycieku danych lub nietypowe zachowanie narzędzia AI (np. prośba o hasło, polecenia ukryte w dokumentach) należy zgłosić w ciągu **24 godzin** na security@bobrtech.example.
