# Sztuczna Inteligencja - Raport 3

**Członkowie zespołu:** Marcin Kwapisz, Kamila Matysiak, Piotr Rychlicki, Justyna Zarzycka

**Temat podprojektu:** Szukanie najkrótszej trasy za pomocą algorytmu genetycznego

**Autor podprojektu:** Piotr Rychlicki


### Algorytm genetyczny

**Algorytm genetyczny** jest jednym z algorytmów służących do optymalizacji rozwiązania pewnego problemu. Sprawdza się on najlepiej wówczas, gdy nie jest znany lub ściśle określony prosty sposób rozwiązania problemu, a także gdy stosunkowo trudno otrzymać najlepsze rozwiązanie, lecz gdy łatwo można ocenić jakość otrzymanego rozwiązania i je zaakceptować. 
Ogólna zasada działania algorytmu (który w kolejnej części zostanie dokładniej omówiony) polega na wygenerowaniu zbioru potencjalnych rozwiązań, które następnie podlegają ocenie. Spośród nich wybierane są te najlepsze, by potem za pomocą operacji genetycznych stworzyć nową grupę, które ponownie przejdzie przez ten cykl. Wynikiem działania takiego algorytmu powinno być otrzymanie optymalnego rozwiązania, spełniającego warunek zakończenia działania algorytmu.

### Problem

W tym podprojekcie algorytm genetyczny został użyty do szukania optymalnej trasy przejazdu agenta (dalej zwanego traktorem) przez wszystkie pola danego typu począwszy i skończywszy na polu startowym (o współrzędnych **(0,0)**). 
Po uruchomieniu programu, w swoim środowisku traktor zastaje określoną konfigurację pól, z których każde (pole nienawodnione, zachwaszczone, niezasadzone, gotowe do zbiorów) występuje określoną liczbę razy. Naturalnym jest, by traktor wykonując określone zadanie (np. zebranie plonu z pola), przemieszczając się między różnymi polami, zrobił to jak najmniejszym kosztem. Stąd też idea i potrzeba właśnie takiego zastosowania algorytmu genetycznego. 
Ten problem, nazywany problemem komiwojażera, należy do problemów NP-zupełnych, czyli takich, które pomimo prostego ich zdefiniowania, są bardzo czasochłonne do rozwiązania. Dla liczby pól z warzywami, na których testowałem swój algorytm i których jest w środowisku testowym 13, liczba potencjalnych rozwiązań wynosi 12!, czyli 479001600 możliwych tras. 
Algorytm genetyczny, z powodów wymienionych na początku raportu, jako rodzaj algorytmu heurystycznego (oferującego rozwiązanie przybliżone do idealnego), sprawdza się przy problemie komiwojażera bardzo dobrze. 

### Pojęcia 

* Osobnik - pojedyncze rozwiązanie problemu
* Populacja - zbiór osobników, którymi operuje algorytm 
* Pokolenie - populacja przetwarzana w jednej iteracji algorytmu 
* Genotyp - to informacja dziedziczna, którą zawiera pojedynczy osobnik 
* Gen - to najmniejszy element informacji zawarty w genotypie

### Algorytm 

```
def main(self):
	self.algorytm_genetyczny()
	self.wykonanie_trasy()
```

Cały algorytm jest wykonywany w funckji self.algorytm_genetyczny, natomiast funkcja self.wykonanie_trasy odpowiada integrację podprojektu w projekcie, realizując wyznaczoną przez algorytm trasę wraz z odpowiednią akcją agenta. 

```
self.znalezione_pola = self.wspolrzedne()
```

Pierwszy krokiem całego programu jest wyznaczenie współrzędnych pól, przez które będziemy chcieli przejść w najkrótszej trasie. Współrzedne te są reprezentowane macierzą zawierającą liczby dwucyfrową [0,99]: np. pole 32 oznacza współrzędne [2,3].

```
self.koszt_trasy = self.koszt_przejazdu(self.znalezione_pola)
```

Następnie wyznaczany jest pierwotny koszt trasy wiodącej przez wszystkie pola danego typu w porządku rosnącym (z góry na dół i z prawa na lewo).

Poniżej przestawiony został już właściwy algorytm: 

```
# Utworzenie pokolenia 
self.pierwsze_pokolenie = self.tworzenie_pokolenia(self.znalezione_pola,10)

# Funkcja przystosowania
self.przystosowanie, self.najnizszy_koszt, self.najwyzszy_koszt, self.srednie_przystosowanie_pierwszego_pokolenia, self.najtanszy_osobnik = self.ocena_przystosowania(self.pierwsze_pokolenie)

# Populacja pośrednia wybrana metodą ruletki
self.populacja_posrednia = self.wybor_populacji_posredniej(self.pierwsze_pokolenie, self.przystosowanie)

# Krzyżowanie populacji pośredniej
self.populacja_po_krzyzowaniu = self.krzyzowanie(self.populacja_posrednia)

# Mutacja populacji pośredniej 
self.populacja_po_mutacji = self.mutacja(self.populacja_po_krzyzowaniu)

# Optymalizacja populacji pośredniej 
self.populacja_po_optymalizacji = self.optymalizacja(self.populacja_po_mutacji,self.znalezione_pola)

if (self.min_koszt)/(self.srednie_przystosowanie_pierwszego_pokolenia) < (0.69):
	print("Zakończono wykonywanie algorytmu po " + str(i) + " pokoleniach")
	break 
```

Pierwszym krokiem każdego algorytmu genetycznego jest utworzenie pierwszego pokolenia osobników. Każde pokolenie w podprojekcie liczy sobie 10 osobników, z których każdy jest permutacją bez powtórzeń współrzędnych zawartych w tablicy self.znalezione_pola wraz z dodaną na koniec współrzędną 0, jako polem, do którego agent ma powrócić na końcu. 
Następnie wykonywana jest tzw. funkcja przystosowania, której zadaniem jest ocenić jakość każdego osobnika (czyli potencjalnego rozwiazania):

```
przystosowanie_osobnikow.append(round(((srednie_przystosowanie/koszty_tras_osobnikow[l])*10),2))
```

Przystosowanie każdego z osobników przechowywane jest w tablicy przystosowanie_osobnikow i wyliczane za pomocą ilorazu średniego przystosowania wszystkich osobników w danym pokoleniu i kosztu konkretnego osobnika. Im lepsza jakość osobnika (czyli im niższy koszt proponowanej przez niego trasy), tym wyższy wynik funkcji przystosowania. 
Po ocenie przystosowania dokonuje się wyboru osobników do populacji pośredniej, z której otrzymamy potomków osobników obecnego pokolenia. Tutaj zdecydowano się na wybór tzw. metodą ruletki, w której każdemu osobnikowi przydziela się zakres należący do przedziału [1,100], proporcjonalny do jego przystosowania. Im większe przystosowanie, tym większy przedział zostanie danemu osobnikowy przydzielony. Następnie losowane jest pięć liczb, właśnie z przedziału [1,100] i do populacji pośredniej trafiają osobnicy, w których zakresach mieszczą się wylosowane liczby. Grupa takich pięciu osobników (do której osobnik może trafić więcej niż raz) staje się populacją pośrednią, która przystąpi do operacji genetycznych w celu poprawienia genotypu. 
Tymi operacjami genetycznymi są krzyżowanie, mutacja i dodatkowa optymalizacja.

```
czy_krzyzowac = random.randint(1,100)
	if (czy_krzyzowac < 11) and (rodzic_1 != rodzic_2):
```

Prawdopodobieństwo krzyżowania dwóch kolejnych osobników populacji pośredniej wyznaczono na 10%. Jeśli krzyżowanie nie nastąpi lub osobnicy są identyczni, wówczas przechodzą oni do kolejnego etapu w niezmienionej postaci. 
Jeśli krzyżowanie dojdzie do skutki, wówczas dla obu osobników wykonuje się następującą operację: wybiera się losowe miejsce krzyżowania w tablicy zawierającej genotyp, sprzed którego wszystkie geny przechodzą w niezmienionej kolejności do potomka. Następnie brakujące geny potomka uzupełnia się genami drugiego osobnika, których jeszcze nie zawiera potomek (tak by geny, czyli współrzędne, się nie powtórzyły w genotypie)

```
k = len(populacja_po_krzyzowaniu) - 1
	while k >= 0:
		czy_mutacja = random.randint(0,100) 
        if czy_mutacja < 3:
			kogo_mutujemy = populacja_po_krzyzowaniu[k]
```

Jeśli chodzi o mutację, tu prawdopodobieństwo jej zajścia dla każdego osobnika ustalono na 2%. Mutacja polega na wylosowaniu dwóch różnych genów osobnika i zamienieniu ich miejscami. 
Na koniec procesu tworzenia potomków dochodzi do opcjonalnej operacji optymalizacji. Jest to nieobowiązkowa funkcja zaimplemetowana w celu dywersyfikacji potomków. Polega ona na usunięciu z populacji pośredniej potwórzeń wśród osobników i uzupełnienie braku nowym, losowym osobnikiem. Po optymalizacji, pokolenie nadal będzie liczyło 10 osobników, lecz każdy z nich z pewnością będzie różny od pozostałych. 
Te 10 osobników storzy nową populację potomków. Tę populację poddaje się ocenie, czyli sprawdzeniu warunku końca działania algorytmu. 

```
if (self.min_koszt)/(self.srednie_przystosowanie_pierwszego_pokolenia) < (0.69):
	print("Zakończono wykonywanie algorytmu po " + str(i) + " pokoleniach")
	break 
```

Jeśli zostanie spełniony warunek znacznego poprawienia kosztu najtańszej trasy najnowszego pokolenia względem średniej długości tras pierwszego pokolenia, wówczas można uznać, że znalezione rozwiazanie jest zadowalające i algorytm zostaje przerwany. 
Jeśli jednak warunek nie jest spełniony, wtedy algorytm wykonuje się na nowo, (zaczynając od etapu oceny przystosowania nowego pokolenia), aż do momentu przejścia przez x zadanych pokoleń (w mojej iplementacji jest to 40 pokoleń)

```
def wykonanie_trasy(self):
	i = len(self.najtansza_trasa) - 1
	l = 0
	while l < i:
		self.pathfinding_tractor.pathfinding_tractor(self.field, self.traktor, self.ui, self.najtansza_trasa, l)
		l = l + 1
```

Ostatnim elementem mojego programu jest ,,wcielenie w życie" znalezionej trasy za pomocą powyższej funkcji wykonanie_trasy. Taką trasę podaje się funkcji pathfinding_tractor, która następnie egzekwuje agentem wykonanie konkretnej akcji na polach danego typu w zadanej kolejności. 


### Dobrane parametry 

Na sprawność działania algorytmu i jakość zwracanych rozwiązań wpływ mają dobrane parametry. Do najważniejszych należą: 

* Liczba pokoleń
* Liczebność pokolenia
* Prawdopodobieństwo zajścia krzyzowania
* Prawdopodobieństwo zajścia mutacji
* Warunek zatrzymania algorytmu 

Na początek ustalono prawdopodobieństwa zajścia operacji genetycznych: 
Prawdopodobieństwo krzyżowania to 10%. Zazwyczaj jest ono większe, lecz dla klasycznego wariantu ułożenia genów, gdzie geny nie zmieniają pozycji w genotypie, lecz wartość. Tutaj użyto permutacyjnego wariantu ułożenia genów, a zatem krzyżowanie nie prowadzi do satysfakcjonujących wyników z dużą częstotliwością. 
Prawdopodobieństwo mutacji dla każdego osobnika to 2%, ponieważ przy permutacjnym ułożeniu genów nie mamy pewności co do korzystności takiego zabiegu. Ma on na celu jedynie dywersyfikację genotypu w celu hipotetycznego znalezienia lepszych rozwiazań.

Liczba pokoleń - tu jej wartość ustawiono na 40. Wartość tę otrzymano wywołując algorytm 10 razy dla każdej z trzech różnych wartości liczby pokoleń: 20, 50 oraz 100 i sprawdzaniu, w którym pokoleniu otrzymano najkrótszą trasę. Okazało się, że dla 50 i 100 pokoleń wartość ta była zbliżona i wynosiła odpowiednio 34 i 27. Zdecydowano zatem o doborze 40 pokoleń. 
Liczebność pokolenia - ta została dobrana losowo na wartość 10, choć oczywiście nie ostatecznie. Jednak rezultaty przy tej konkretnej wartości okazały się na tyle zadowalające, że postanowiono jej nie zmieniać. 
Warunek zatrzymania algorytmu - ten ustalono na 69% wartości średniej długości wszystkich tras z pierwszego pokolenia. Wybrano taką wartość ponownie, na podstawie wywoływanych wcześniej algorytmów dla 20, 50, 100 i ostatecznych 40 pokoleń. Za każdym razem iloraz najlepszego rozwiazania ze średnim kosztem tras pierwszego pokolenia oscylował między 0,67 a 0,7. 