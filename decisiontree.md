# Sztuczna Inteligencja - Raport

**Członkowie zespołu:** Marcin Kwapisz, Kamila Matysiak, Piotr Rychlicki, Justyna Zarzycka

**Autor podprojektu:** Kamila Matysiak


### Drzewo Decyzyjne

Projekt wykorzystuje drzewo decyzyjne do wybrania czynności dla każdego pola, a następnie wysłania traktora do pól zgodnych z obecnie wybranym trybem.

Projekt używa metody CART (Classification and Regression Tree). Tworzy on drzewo binarne, w którym rozpatruje wszystkie możliwe podziały zbioru wartości cech na dwa rozłączne i uzupełniające się podzbiory dla cech dyskretnych.

Uruchamia się go za pomocą klawisza **F6**.

#### Zbiór uczący:

Zbiorem uczącym jest zestaw danych informujących drzewo jak postępować z polem o danych parametrach.
Kolejne cyfry odpowiadają za: nawodnienie pola, obecność chwastów, czy pole jest puste, czy jest do zbioru.

```
training_data = [[0, 0, 1, 0, "Zasadzic"],
                 [0, 1, 1, 0, "Odchwascic"],
                 [0, 0, 0, 0, "Podlac"],
                 [0, 1, 0, 0, "Odchwascic"],
                 [1, 0, 1, 0, "Zasadzic"],
                 [1, 1, 1, 0, "Odchwascic"],
                 [1, 0, 0, 0, "Czekac"],
                 [1, 1, 0, 0, "Odchwascic"],
                 [0, 0, 0, 1, "Zebrac"]]
        self.tree = build_tree(training_data)
        print_tree(self.tree)
```

#### Algotytm tworzenia drzewa:

Budowanie drzewa zaczynamy od stworzenia klasy **Question**, w której będziemy tworzyć zapytanie, na podstawie którego będziemy dzielić nasze dane. Następnie tworzymy funkcję **partition**, która na podstawie zapytania dzieli nam dane na spełnione i niespełnione wiersze:

```
# podział danych na spełnione i niespełnione wiersze
def partition(rows, question):
    true_rows, false_rows = [], []
    for row in rows:
        if question.match(row):
            true_rows.append(row)
        else:
            false_rows.append(row)
    return true_rows, false_rows
```

Następnie wyokrzystujemy **Index Gini**, który mierzy jak często losowo wybrany element będzie źle zindentyfikowany. Gdy jest równy 0, oznacza to, że element zostanie właściwie oznaczony.

   
    
```
# funkcja implementująca indeks gini
def gini(rows):
    counts = class_counts(rows)
    impurity = 1
    for lbl in counts:
        prob_of_lbl = counts[lbl] / float(len(rows))
        impurity -= prob_of_lbl ** 2
    return impurity

def info_gain(left, right, current_uncertainty):
    p = float(len(left)) / (len(left) + len(right))
    return current_uncertainty - p * gini(left) - (1 - p) * gini(right)
    
```

Następnie na podstawie uzykanych informacji, znajdujemy najlepsze miejsce na podział danych:

```
# znalezienie najlepszego "miejsca" na podział danych
def find_best_split(rows):
    best_gain = 0
    best_question = None
    current_uncertainty = gini(rows)
    n_features = len(rows[0]) - 1
    for col in range(n_features):
        values = set([row[col] for row in rows])
        for val in values:
            question = Question(col, val)
            true_rows, false_rows = partition(rows, question)
            if len(true_rows) == 0 or len(false_rows) == 0:
                continue
            gain = info_gain(true_rows, false_rows, current_uncertainty)
            if gain >= best_gain:
                best_gain, best_question = gain, question
    return best_gain, best_question
```

Po stworzeniu klas definiujących liść i węzęł deycyzyjny przechodzimy do właściwej funkcji **build_tree*:
```
# funkcja budująca drzewo
def build_tree(rows):
    gain, question = find_best_split(rows)                 # znalezienie najlepszego podziału
    if gain == 0:
        return Leaf(rows)
    true_rows, false_rows = partition(rows, question)      # podział danych

    true_branch = build_tree(true_rows)
    false_branch = build_tree(false_rows)                  #stworzenie gałęzi prawdy i fałszu

    return DecisionNode(question, true_branch, false_branch)
```

#### Integracja:

Program sczytuje dane z głównego projektu, następnie interpretuje je za pomocą prostej funkcji **translate**, która zwraca informacje o stanie pola. Następnie za pomocą drzewa określamy czynność, jaka powinna zostać wykonana na tym polu. Wykonanie pracy zlecamy klasie **pathfinding**, która za pomocą algorytmu A* wysyła traktor na pola odpowiadające wybranemu trybowi.

```
   def search_field(self):
        matrix = self.field.get_matrix()
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                print("Pole (%d,%d) Przewidziania czynnosc: %s"
                      % (i, j, print_leaf(classify(translate(matrix[i][j]), self.tree))))
                if work[self.traktor.get_mode()] in self.work_field(classify(translate(matrix[i][j]), self.tree)):
                    print("Zgodna z aktualnym trybem, czynnosc wykonywana")
                    self.path.find_path(self.traktor, self.field, self.ui, [j, i])
                    self.ui.update()
                    time.sleep(0.5)
```


