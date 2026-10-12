# Robocze ustalenia dotyczące context skills

Stan na 2026-10-12. Notatka do kontynuowania pracy po długiej sesji lub zmianie rozmowy. Zapisuje decyzje użytkownika, bieżący zakres i pomysły do dalszego omówienia; nie ustanawia nowych reguł projektu.

## Bieżący zakres

* Repozytorium: `LeszekKantorek/context-skills`.
* Lokalna gałąź: `codex/context-v-proposal`, utworzona z bieżącego checkoutu na `c5014a9`.
* Zgłoszenie #6 jest propozycją do dyskusji, nie zatwierdzoną specyfikacją całej przebudowy. Użytkownik wyraźnie skorygował początkową interpretację jako zadania wdrożeniowego.
* Użytkownik zatwierdził przygotowanie `context-map`, a następnie doprecyzował zakres: dwie mapy, definicje i przykłady w jednym `SKILL.md`.
* Pozostałe skills i integracje mają na razie pozostać bez zmian.
* Zmiany pozostają lokalne, bez commita i publikacji. Nie wykonano migracji innych repozytoriów.

## Przyjęty kierunek routingu

Aktualna decyzja zastępuje wcześniejsze założenie jednej wspólnej tabeli. `context-map` zarządza dwiema mapami o różnych funkcjach.

| Mapa | Pytanie | Format | Miejsce |
| --- | --- | --- | --- |
| Mapa źródeł | Gdzie znajdę wiedzę przydatną w tej sytuacji? | `Source / Use when`, z zachowaniem istniejących nazw kolumn potrzebnych odbiorcom | Istniejący indeks projektu, a przy jego braku domyślnie `.context/index.md` |
| Mapa zadań | Od czego zacząć dane zadanie i kiedy potrzebuję dodatkowych źródeł? | `Task / Read first / Extend when` | Nowa mapa w AGENTS lub istniejący plik task guidance, bez drugiej kopii tabeli |

* `Task` oznacza oczekiwany wynik lub powtarzalny rodzaj pracy.
* `Procedure` oznacza ustaloną sekwencję działań z warunkami i oczekiwanym rezultatem.
* `Read first` wskazuje źródło potrzebne do zrozumienia ograniczeń zadania lub wyboru procedury. Może to być procedura, kontrakt, decyzja albo dostępny skill.
* `Extend when` wiąże dodatkowe źródło z konkretnym warunkiem.
* Znana trasa zadania prowadzi bezpośrednio do źródeł. Agent nie musi najpierw czytać indeksu.
* Indeks służy do odkrywania wiedzy, gdy trasa zadania nie istnieje lub nie wystarcza.
* Obie mapy mogą wskazywać to samo źródło, ale nie powinny wymuszać przechodzenia od jednej mapy do drugiej i z powrotem.
* Mapy obejmują źródła poza `.context/`. Nie są obowiązkowym katalogiem każdego pliku.
* Procedury i wiedza pozostają w źródłach. W tabelach zapisujemy warunki i odnośniki.
* Przed zmianą formatu indeksu trzeba sprawdzić zarówno jego czytelników, jak i narzędzia, które go zapisują.
* Istniejące Apply, Gather i hook pozostają bez zmian. Ich zależności mogą ograniczać migrację indeksu.

## Rola context-map

Użytkownik zmienił wcześniejszą koncepcję Apply: agent potrafi już stosować wiedzę, a potrzebny skill ma zarządzać jej routingiem. Dla tej odpowiedzialności przyjęto nazwę `context-map` i przygotowano osobny skill. Dotychczasowy `context-apply` nie został usunięty ani przemianowany.

Map przekształca dokumenty i procedury w mapę źródeł oraz mapę zadań. Uruchamia się przy tworzeniu lub poprawianiu routingu, nie przed każdym zadaniem projektowym. Dla lokalnej poprawki bada odpowiednie trasy; przy budowie pierwszej mapy rozpoznaje szerszy zbiór źródeł.

Weryfikacja obejmuje trafność warunków, poprawność celów, pominięte potrzebne źródła, zbędne odczyty i zapętlenia nawigacji. Sprawdzanie tras nie oznacza wykonywania wskazanych procedur.

## Problem rozproszonej nawigacji

* `AGENTS.md` kieruje do `.context/index.md` i warunkowo do `.context/task-guidance.md`.
* Indeks zawiera task guidance, a task guidance dla części pracy nad interfejsem odsyła z powrotem do indeksu.
* Task guidance obejmuje także sekcje dokumentów poza `.context/`, czego nie robi sam indeks wpisów.
* Zasady selektywnego odczytu i zatrzymania poszukiwania powtarzają się w AGENTS i task guidance.
* Nie oznacza to, że każda praca zawsze czyta wszystkie routery; problemem jest rozproszona odpowiedzialność za nawigację.
* Gotowa procedura akceptacji w CONTRIBUTING jest przykładem celu, do którego można prowadzić bezpośrednio.

## Kierunek pozostałych skills

Poniższe punkty zapisują oczekiwania użytkownika dotyczące kolejnych iteracji. Nie są upoważnieniem do ich wdrożenia w obecnym kroku.

### context-gather

* Zapisuje trwałe informacje z dostępnej sesji lub dostarczonych sesji, uwzględniając szerszy przebieg zadania.
* Priorytetem jest dobre zachowanie treści, zakresu, źródeł, uzasadnienia i niepewności.
* Może tworzyć nowe wpisy bez szerokiego poszukiwania idealnego miejsca w dokumentacji.
* Nie powinien przy okazji ładować i analizować całego zbioru ani prowadzić szerokiej deduplikacji.
* Wcześniejsza sugestia asystenta, aby Gather zachował rozbudowane porządkowanie, została skorygowana przez użytkownika. Nie przywracać jej jako przyjętej decyzji.

### context-maintain

* Na życzenie użytkownika analizuje większy zbiór dokumentów i jego architekturę informacji.
* Główne zadanie to wykrywanie powtarzających się reguł i znaczeń, także w różnych katalogach.
* Rozważa wspólne źródło, zastąpienie kopii odsyłaczami, usunięcie zbędnych fragmentów oraz podział nadmiernie rozrośniętych dokumentów.
* Podobne sformułowania mogą mieć różny zakres; scalenie nie może usuwać istotnych różnic ani uzasadnienia.
* Ma mieć inny przebieg pracy niż Gather, dopasowany do całościowego przeglądu.

### Przegląd sesji

* Importer pozostaje osobną odpowiedzialnością; użytkownik rozważa nazwę `context-review-sessions`.
* Przy 10–15 sesjach użytkownik oczekuje pracy na osobnych agentach, zamiast ładowania wszystkich transkryptów do jednego kontekstu.
* Do zaprojektowania pozostają podział materiału, zwracane wyniki, koordynacja zapisów i oznaczanie checkpointów.
* Nie wdrożono zmiany nazwy ani delegowania. Istniejący `context-import-sessions` pozostaje bez zmian.

### context-compile

* Użytkownik popiera kierunek przenoszenia ustalonych procedur do bezpośrednio wybieranych `SKILL.md`.
* Motywacja jest szersza niż skrócenie indeksu: agent ma trafiać od razu do wykonywalnej instrukcji zamiast przechodzić przez kilka routerów i duży dokument.
* Asystent wskazał potrzebę jednego źródła procedury: skill może stać się jej właścicielem albo być generowany z dokumentu z kontrolą aktualności.
* Wybór między przenoszeniem a generowaniem nie jest jeszcze rozstrzygnięty. Nie tworzyć dwóch niezależnie edytowanych kopii.
* Wcześniejsze stanowisko asystenta, aby odkładać Compile wyłącznie do pomiarów indeksu, nie oddaje późniejszego doprecyzowania użytkownika.

### Diagnozowanie zachowania agenta

* Użytkownik rozważa `context-diagnose-and-improve`; asystent zaproponował krótsze `context-diagnose`. Nazwa nie została zatwierdzona.
* Punktem wejścia jest konkretne złe zachowanie lub korekta użytkownika, a nie ogólne zebranie wiedzy z długiego zadania.
* Skill ma porównać oczekiwane i rzeczywiste zachowanie oraz zbadać dostępne instrukcje i ślady ich użycia.
* Możliwe problemy obejmują brak informacji, nietrafny routing, niejasną lub nadmierną instrukcję i zignorowanie istniejącej reguły.
* Poprawką może być usunięcie lub zawężenie instrukcji, nie tylko dopisanie kolejnej.
* Może analizować także skills wytworzone przez Compile. Przyczyna niepotwierdzona dowodami pozostaje hipotezą.

## Context V i ograniczanie instrukcji

Context V z #6 pozostaje propozycją powiązania intencji, wymagań, architektury, kontraktów i implementacji z odpowiednimi dowodami. Nie został wdrożony ani przyjęty jako obowiązkowy przebieg pracy. Późniejsza decyzja o Map przesunęła bieżący zakres na routing.

Artykuł OpenAI wniósł dodatkowe kryterium: oceniać potrzebę instrukcji, zamiast zakładać, że ich dokładanie poprawi pracę. Wnioski dla projektu to warunkowe odczyty, krótkie opisy aktywacji, unikanie obowiązkowych sekwencji bez uzasadnienia i uwzględnienie różnic między modelami. Samo przeniesienie nadmiernych instrukcji ze skilla do `.context/` nie zmniejszy ich kosztu, jeśli agent nadal musi wszystko czytać.

Asystent zaproponował porównanie wariantu obecnego, uproszczonego i rozbudowanego na podobnych zadaniach. Eksperyment nie został jeszcze wykonany. Większa szczegółowość planu sama w sobie nie stanowi dowodu poprawy jakości.

## Przygotowane pliki i sprawdzenia

* [Nowy skill](skills/context-map/SKILL.md) zawiera zakres, selekcję źródeł, budowanie tabeli, zasady migracji i sprawdzanie tras.
* Definicje, dwa ogólne przykłady map i scenariusze wyboru znajdują się bezpośrednio w `SKILL.md`. Osobny materiał referencyjny usunięto.
* [README](README.md) opisuje pierwszą wersję i współistnienie ze starym przepływem indeksu.
* [Katalog skills](skills.sh.json) zawiera `context-map`.
* Standardowy `quick_validate.py` przeszedł. Brakujący PyYAML pobrano do katalogu tymczasowego, bez dodawania zależności projektu.
* Sprawdzono lokalne linki dokumentacji, katalog skills, formatowanie zmian oraz brak zmian w pozostałych skills i integracjach.
* Scenariusze w przykładzie są oczekiwanymi wyborami, nie wynikami niezależnych uruchomień agentów. Nie wykonano jeszcze oceny skuteczności routingu na rzeczywistych zadaniach.

## Zależności i następne kroki

### Rewizja na podstawie actionable skills

Użytkownik dostarczył trzy przykłady w `.local/` oraz skill `asd-ste100` w `.agents/skills/`. Polecił oprzeć konstrukcję `context-map` na tych przykładach zamiast na stylu proponowanym przez `skill-creator`. Reguły STE mają dopracować język, a nie zastąpić projektowanie procedury.

| Przykład | Mechanizm pisania | Zastosowanie w Map |
| --- | --- | --- |
| `actionable-skill-example-1.md` — execute-plan | Cel, konkretny wynik, rozdzielenie obserwacji i decyzji, dowody przy wyniku sprawdzenia | Jawny wynik pracy oraz raport z zadaniem, wybranymi celami, wynikiem i dowodem lub ograniczeniem. |
| `actionable-skill-example-2.md` — write-briefing | Numerowane kroki, mapowanie treści wejściowej na wynik, instrukcje przy polach, dobre i złe przykłady | Przekształcenie treści źródła w przypadek użycia, cel i zastosowanie oraz przykłady poprawiania wierszy. |
| `actionable-skill-example-3.md` — review-plan | Porównanie punkt po punkcie, kryteria klasyfikacji i działanie wynikające z oceny | Porównanie informacji wymaganych przez zadanie z wybranymi celami oraz klasy Match, Missing, Excess, Detour i Unchecked. |

Wspólny wzorzec to polecenie z konkretnym obiektem, umieszczone w kroku, który prowadzi do sprawdzalnego wyniku. Tabele pomagają wybrać działanie. Przykłady pokazują, co zmienia sens, zamiast jedynie deklarować ogólną zasadę.

Nie przenosimy automatycznie szczegółowych reguł innych procesów, takich jak obowiązkowe commity, zakaz pytań czy niezmienność planu. Przykład review-plan ma też niespójne wskazanie numeru kroku odczytu briefingu. Wzorce wymagają interpretacji, a nie kopiowania wszystkich poleceń.

Poprzednia rewizja miała sześć etapów z osobnymi nagłówkami. Użytkownik doprecyzował docelowy układ: krótki wstęp, jedna sekcja `Steps`, numerowane kroki oraz punkty i tabele pod krokami. Nie tworzymy osobnych nagłówków dla każdego kroku.

Obecna wersja ma siedem kroków: wybór map i lokalizacji, definicje oraz identyfikację wejścia, mapę źródeł, mapę zadań, zapis z obsługą zależności, sprawdzenie wyboru i raport. Całość stanowi jeden skill bez plików `references` i bez nazw oraz linków do konkretnego projektu przykładowego. Przykłady używają fikcyjnych dokumentów i wymagają zastąpienia ich rzeczywistymi źródłami.

Po tej zmianie sprawdzono strukturę skilla, lokalne odnośniki oraz język instrukcji z limitem 20 słów, łącznie z oboma szablonami map. Kontrole przeszły bez uwag. Folder `skills/context-map/` zawiera wyłącznie `SKILL.md`. README i ta notatka odzwierciedlają nowy podział.

Scenariusze nadal opisują oczekiwane wybory, nie niezależne uruchomienia agentów.

Zastosowano krótkie polecenia, czynne czasowniki, spójne terminy i osobne zdania dla odrębnych działań. Linter STE początkowo zgłosił 23 uwagi wymagające poprawy i 2 uwagi doradcze w głównym skillu. Po przebudowie głównego skilla i przykładu nie zgłasza uwag. Nie oznacza to certyfikowanej zgodności ze słownikiem ASD-STE100.

Sprawdzono także limit 20 słów na zdanie, łącznie z szablonami AGENTS wewnątrz bloków Markdown. Kontrola nie zgłosiła uwag. Walidator struktury skilla oraz kontrola lokalnych linków i formatowania również przeszły. PyYAML do walidatora znajduje się teraz w ignorowanym `.references/context-map-validation/`, bez zmiany zależności projektu.

Materiały użytkownika w `.local/`, skill STE, plik `skills-lock.json` oraz pozostałe skills pozostają bez zmian w tej rewizji.

### Kolejne kroki

1. Omówić i dopracować pierwszą wersję `context-map`, zwłaszcza zwięzłość instrukcji i szczegółowość tabeli.
2. Sprawdzić zachowanie na małym zadaniu, zadaniu przekraczającym granice modułów i przypadkach, które nie powinny aktywować danej trasy.
3. Osobno ustalić zakres ewentualnej migracji projektu używającego skills. Przykładowe ścieżki w skillu nie są gotową mapą żadnego repozytorium.
4. Przed wycofaniem starych indeksów uwzględnić Apply, Gather i startup hook, które nadal ich wymagają. Obecny zakres nie obejmuje zmiany tych odbiorców.
5. Pozostałe skills rozwijać w kolejnych uzgodnionych iteracjach.

Przy wznowieniu pracy sprawdzić aktualną gałąź i diff; powyższy stan jest zapisem z daty notatki. Aktualizować tę notatkę przy kolejnych istotnych decyzjach, zachowując rozróżnienie między decyzją użytkownika, propozycją i wykonanym działaniem.

## Źródła rozmowy

* [Zgłoszenie #6](https://github.com/LeszekKantorek/context-skills/issues/6).
* [Pełny załącznik do zgłoszenia](https://github.com/user-attachments/files/33313824/context-engineering-framework-feedback-and-proposal.md).
* [Artykuł OpenAI o skills i promptach](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra).

Załącznik do #6 wspominał także niezidentyfikowany artykuł o doborze kontekstu. Użytkownik później podał powyższy artykuł OpenAI jako dodatkowy materiał; nie ustalono, że to ta sama publikacja.
