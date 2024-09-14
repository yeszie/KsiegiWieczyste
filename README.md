# Projekt: Pobieranie Ksiąg Wieczystych na Dysk Lokalny

Ten projekt umożliwia pobranie ksiąg wieczystych na dysk lokalny. Ze względów prawnych — pomimo że dostęp do KW jest jawny — istnieją pewne wątpliwości dotyczące tej kwestii.

Z tego powodu nie zamieszczam pełnej wersji skryptu, choć oczywiście taki posiadam. Każdy z odrobiną wysiłku może uzupełnić brakujące elementy, aby uzyskać pełną funkcjonalność.

## Zastrzeżenie

Zawartość tego repozytorium ma charakter edukacyjny. Materiał został celowo skrócony — osoby bardziej zaznajomione z tematem nie powinny mieć problemów z dalszym rozwijaniem projektu.

## Opis Skryptu

W pełnej wersji skryptu, proces został podzielony na kilka etapów, realizowanych przez oddzielne pliki:

1. **Wygenerowanie numerów ksiąg wieczystych**: Tworzenie listy wszystkich możliwych numerów ksiąg wieczystych dla każdego województwa, łącznie z cyfrą kontrolną.
2. **Pobieranie danych**: Pobieranie ksiąg wieczystych na dysk lokalny w formacie HTML oraz oczyszczanie pobranych plików z nadmiarowych danych.
3. **Analiza i eksport**: Przesyłanie plików HTML do modelu AI w celu wygenerowania zbiorczego pliku Excel z uporządkowanymi danymi.

## Ograniczenia

Ze względu na timeouty oraz limity nałożone przez API, konieczne jest stosowanie przerw między zapytaniami, aby uniknąć zbanowania adresu IP (np. przerwy co 10 sekund).

### Cyfra kontrolna

Obliczanie cyfry kontrolnej zostało opisane w dokumentacji, ale temat ten może być trudny dla osób bez doświadczenia w tej dziedzinie. W moim skrypcie wykorzystałem dwie metody weryfikacji prawidłowych numerów ksiąg wieczystych:

1. **Metoda wolna**: Polega na odpytywaniu kolejnych numerów i weryfikacji ich poprawności na podstawie odpowiedzi zwróconej przez system (brak błędu oznacza prawidłowy numer).
2. **Metoda szybka**: Jest znacznie szybsza, ale z przyczyn prawnych nie opisuję jej szczegółowo ani nie zamieszczam kodu.

## Wydajność

Średnia prędkość pobierania danych na jednym komputerze (jednym adresie IP) wynosi od kilku do kilkunastu tysięcy ksiąg na dobę. W Polsce istnieje ponad 20 milionów ksiąg wieczystych. Ponieważ każdy sąd rejonowy ma swoją unikalną numerację, można ograniczyć pobieranie danych tylko do wybranego zakresu.

Zauważyłem, że numeracja ksiąg wieczystych jest rosnąca, co oznacza, że jeśli dla danej jednostki sądowej istnieje 150 tysięcy ksiąg, to numery wyższe niż 150 tysięcy nie będą zawierały danych. Może się jednak zdarzyć, że w pewnych przedziałach występują "dziury", czyli niektóre numery nie mają przypisanej księgi, mimo że inne numery z tego zakresu są poprawne.
