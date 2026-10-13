# Robocze ustalenia dotyczące context skills

Stan na 2026-10-13. Notatka do kontynuowania pracy po długiej sesji lub zmianie rozmowy. Zapisuje decyzje użytkownika, bieżący zakres i pomysły do dalszego omówienia; nie ustanawia nowych reguł projektu.

## Bieżący zakres

* Repozytorium: `LeszekKantorek/context-skills`.
* Lokalna gałąź: `codex/context-v-proposal`, utworzona z bieżącego checkoutu na `c5014a9`.
* Zgłoszenie #6 jest propozycją do dyskusji, nie zatwierdzoną specyfikacją całej przebudowy. Użytkownik wyraźnie skorygował początkową interpretację jako zadania wdrożeniowego.
* Użytkownik zatwierdził `context-map` dobierający punkty wejścia i strukturę map do potrzeb projektu. Zastępuje to wcześniejsze wymaganie dwóch map. Definicje i przykłady pozostają w jednym `SKILL.md`.
* Pozostałe skills i integracje mają na razie pozostać bez zmian.
* Stan sprzed ponownego ustalenia celu zapisano lokalnym commitem `62434ff`. Nie publikowano zmian ani nie migrowano innych repozytoriów.
* Dobór map do potrzeb projektu zapisano lokalnym commitem `a5539f6`. Nawigację po rozbudowanym projekcie zapisano lokalnym commitem `5231369`. Usunięcie osobnego etapu analizy i nową tabelę pytań zapisano lokalnym commitem `bed4700`. Obecna rewizja tabeli ról wiedzy pozostaje zmianą roboczą.
* `.local/` i `.agents/` są ignorowane.

## Cel skilla po doprecyzowaniu

Użytkownik zatwierdził cel: zrozumieć znaczenie wiedzy projektu, warunki jej zastosowania oraz wpływ na decyzje lub działania agenta. Dobór punktów wejścia i struktury map wynika z tego rozpoznania. Samo formatowanie tabel i sprawdzanie linków nie realizuje celu.

* Kolejność pracy: zrozumienie źródła, rozpoznanie ról i zastosowań wiedzy, dobór punktów wejścia, struktury i miejsca, zapis tras, sprawdzenie.
* Punkt 2 zawiera jedną tabelę decyzyjną `Term / Meaning / Recognize when / Routing use`, zastępującą przykład zastosowań i osobny słownik.
* Tabela rozpoznaje role: Knowledge area, Task, Explanation, Requirement or constraint, Decision, Procedure, Evidence i Open question. Łączy rozpoznaną treść z jej zastosowaniem w nawigacji.
* Klasyfikacja dotyczy istotnych fragmentów, dopuszcza kilka ról i nie wymaga kopiowania treści, nowych folderów ani osobnych map. Niedopasowanie kategorii nie jest powodem odrzucenia przydatnej wiedzy.
* Definicje Read first, Additional i Extend when znajdują się w punkcie 4. Ich przypisanie zależy od potrzeb konkretnej trasy, nie od kategorii źródła.
* Użytkownik zatwierdził usunięcie osobnego etapu 5 Whys i pytań sokratejskich. Zastępuje to wcześniejsze wymaganie stosowania tych metod.
* Użytkownik uznał tabelę trzech pytań za zbyt ubogą. Zatwierdził tabelę siedmiu pytań o przeznaczenie źródła, rodzaj treści, potrzebę odczytu, wymagany kontekst, podstawy i ograniczenia, relacje z inną wiedzą oraz wynik odczytu.
* Pytania wspomagają zrozumienie źródła. Nie wymagają osobnej odpowiedzi na każde z nich ani nie przywracają osobnego etapu analizy.
* Jasne odpowiedzi pozwalają przejść dalej. Przy niejasności agent doczytuje odpowiedni fragment albo zachowuje lukę, zamiast wymyślać zastosowanie.
* Pozostaje rozróżnienie między treścią źródła, wnioskiem agenta i przyjętą zasadą projektu.
* Przy artykule trzeba odróżnić zalecenie autora od zaakceptowanej reguły projektu. Brak lokalnego uzasadnienia pozostaje brakiem, nie nową regułą.
* Map nie tworzy raportów. Jego wynikiem są mapy, a nie dokument opisujący przebieg pracy.
* Wymagania dotyczące sposobu napisania skilla nie są poleceniami dla agenta wykonującego skill. Usunięto instrukcję nakazującą trzymanie definicji i przykładów w tym dokumencie.
* Cała treść skilla nadal pozostaje w jednym `SKILL.md`, z jawnym `Goal` i uzgodnionym układem `Steps`.
* Użytkownik wyraźnie zachował linki do `docs/`. Przykłady łączą je z wpisami w `.context/`.

## Przyjęty kierunek routingu

Aktualna decyzja zastępuje wymaganie dwóch map. Skill rozpoznaje, z czym agent zaczyna pracę, i dobiera strukturę pozwalającą dotrzeć do potrzebnej wiedzy.

| Punkt wejścia | Przykładowa struktura |
| --- | --- |
| Pytanie | Pytanie → źródło odpowiedzi |
| Zadanie | Task → Read first → Extend when |
| Objaw | Objaw → pierwsze sprawdzenie → źródło zależne od wyniku |
| Decyzja | Decyzja → ograniczenia → kryteria → dowody |
| Obszar zmiany | Obszar → kontrakty → zależności → właściwe sprawdzenia |
| Odkrywanie wiedzy | Source → Use when |

* To przykłady do wyboru, nie komplet obowiązkowych map ani zamknięta lista typów.
* Jedna mapa wystarcza, gdy wpisy potrzebują podobnych pól i reguł wyboru. Osobne mapy mają sens przy różnych potrzebach nawigacji.
* Rozgałęzienie ma sens, gdy dalsze źródło zależy od odpowiedzi lub obserwacji. Brak uzasadnienia gałęzi to luka w wiedzy.
* Zachowujemy skuteczną istniejącą nawigację. Zwięzły routing trafia do właściwego `AGENTS.md`; obszerniejsza mapa może mieć osobne miejsce i odnośnik.
* Skill nie wymaga utworzenia indeksu ani osobnej mapy zadań. Nie tworzy nowego pliku tylko dla zgodności z przykładem.
* `Task` oznacza oczekiwany wynik lub powtarzalny rodzaj pracy.
* `Procedure` oznacza ustaloną sekwencję działań z warunkami i oczekiwanym rezultatem.
* `Read first` wskazuje źródło potrzebne do zrozumienia ograniczeń zadania lub wyboru procedury. Może to być procedura, kontrakt, decyzja albo dostępny skill.
* `Extend when` wiąże dodatkowe źródło z konkretnym warunkiem.
* Znana trasa zadania prowadzi bezpośrednio do źródeł. Agent nie musi najpierw czytać indeksu.
* Indeks służy do odkrywania wiedzy, gdy trasa zadania nie istnieje lub nie wystarcza.
* Jeżeli istnieje kilka map, mogą wskazywać to samo źródło. Nie powinny wymuszać powtarzanego przechodzenia między nimi.
* Mapy obejmują źródła poza `.context/`. Nie są obowiązkowym katalogiem każdego pliku.
* Procedury i wiedza pozostają w źródłach. W tabelach zapisujemy warunki i odnośniki.
* Przed zmianą formatu indeksu trzeba sprawdzić zarówno jego czytelników, jak i narzędzia, które go zapisują.
* Istniejące Apply, Gather i hook pozostają bez zmian. Ich zależności mogą ograniczać migrację indeksu.

## Rola context-map

### Nawigacja po rozbudowanym projekcie

Użytkownik odrzucił szczegółowy przykład diagnozowania wieku danych jako zbyt bliski konkretnej procedurze. Potrzebuje sposobu przechodzenia przez rozbudowaną, różnorodną wiedzę: od kompilacji i programowania, przez architekturę i przypadki użycia, po odpowiadanie na zgłoszenia.

* Map ma pomagać zawężać szeroką potrzebę do właściwego źródła, także przez lokalny indeks obszaru.
* Orientacja w zbiorze, zawężanie i bezpośrednie wejścia to możliwe mechanizmy nawigacji. Nie są trzema wymaganymi mapami ani obowiązkową kolejnością czytania.
* Nazwa obszaru lub katalogu nie wystarcza. Trasa ma mówić, kiedy wiedza z danego obszaru jest potrzebna i jak zawęzić wybór.
* Kolejny poziom nawigacji ma sens tylko wtedy, gdy pomaga wybrać źródło lub uniknąć zbędnych odczytów.
* Zadanie może wymagać wiedzy z kilku obszarów. Przejście do kolejnego wynika z potrzeby, nie z obowiązku przeczytania całości na początku.
* Znany cel pozwala ominąć ogólną mapę. Przykładowo kompilacja może prowadzić bezpośrednio do instrukcji dla danego środowiska.
* Wiedza i procedury pozostają w źródłach. Mapa nie przejmuje szczegółowych kroków diagnostycznych.
* Weryfikacja obejmuje całą drogę od rzeczywistego pytania do konkretnego źródła, a nie tylko poprawność pojedynczych linków.
* Nowy przykład w `SKILL.md` obejmuje różne obszary projektu oraz warunkowe przechodzenie między nimi. Zachowano Goal. Późniejsza decyzja usuwa osobny etap 5 Whys i pytań sokratejskich.

### Zakres odpowiedzialności

Użytkownik zmienił wcześniejszą koncepcję Apply: agent potrafi już stosować wiedzę, a potrzebny skill ma zarządzać jej routingiem. Dla tej odpowiedzialności przyjęto nazwę `context-map` i przygotowano osobny skill. Dotychczasowy `context-apply` nie został usunięty ani przemianowany.

Map rozpoznaje zastosowania wiedzy i organizuje dostęp do dokumentów oraz procedur przez dobrane punkty wejścia. Uruchamia się przy tworzeniu lub poprawianiu routingu, nie przed każdym zadaniem projektowym. Dla lokalnej poprawki bada odpowiednie trasy; przy budowie pierwszej mapy rozpoznaje szerszy zbiór źródeł.

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
* Definicje, przykłady indeksu, tras zadań i nawigacji po rozbudowanym projekcie oraz scenariusze wyboru znajdują się bezpośrednio w `SKILL.md`. Osobny materiał referencyjny usunięto.
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
| `actionable-skill-example-1.md` — execute-plan | Cel, konkretny wynik, rozdzielenie obserwacji i decyzji, dowody przy wyniku sprawdzenia | Jasny wynik pracy i odróżnienie obserwacji od założeń. Wymaganie raportu zostało odrzucone jako obce celowi Map. |
| `actionable-skill-example-2.md` — write-briefing | Numerowane kroki, mapowanie treści wejściowej na wynik, instrukcje przy polach, dobre i złe przykłady | Przekształcenie treści źródła w przypadek użycia, cel i zastosowanie oraz przykłady poprawiania wierszy. |
| `actionable-skill-example-3.md` — review-plan | Porównanie punkt po punkcie, kryteria klasyfikacji i działanie wynikające z oceny | Porównanie potrzeb sytuacji z wybranymi źródłami: braki, zbędne odczyty, objazdy i niesprawdzone cele. |

Wspólny wzorzec to polecenie z konkretnym obiektem, umieszczone w kroku, który prowadzi do sprawdzalnego wyniku. Tabele pomagają wybrać działanie. Przykłady pokazują, co zmienia sens, zamiast jedynie deklarować ogólną zasadę.

Nie przenosimy automatycznie szczegółowych reguł innych procesów, takich jak obowiązkowe commity, zakaz pytań czy niezmienność planu. Przykład review-plan ma też niespójne wskazanie numeru kroku odczytu briefingu. Wzorce wymagają interpretacji, a nie kopiowania wszystkich poleceń.

Poprzednia rewizja miała sześć etapów z osobnymi nagłówkami. Użytkownik doprecyzował docelowy układ: krótki wstęp, jedna sekcja `Steps`, numerowane kroki oraz punkty i tabele pod krokami. Nie tworzymy osobnych nagłówków dla każdego kroku.

Wersja zapisana w commicie miała siedem kroków i kończyła się raportem. Użytkownik odrzucił ten kierunek jako odejście od celu. Aktualna wersja ma pięć kroków, rozpoczyna się od rozumienia wiedzy i nie wymaga raportu. Całość stanowi jeden skill bez plików `references` i bez nazw oraz linków do konkretnego projektu przykładowego. Przykłady używają fikcyjnych dokumentów i wymagają zastąpienia ich rzeczywistymi źródłami.

W rewizji zapisanej jako `a5539f6` sprawdzono strukturę skilla i język instrukcji, również wewnątrz przykładów. Zastąpiono stały podział na dwie mapy doborem punktów wejścia i struktury. Obecna rewizja rozszerza ten kierunek o nawigację po całym zbiorze. Folder `skills/context-map/` nadal zawiera wyłącznie `SKILL.md`.

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
