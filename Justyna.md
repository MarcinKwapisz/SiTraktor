# Drzewa decyzyjne, algorytm ID3

### autor Justyna Zarzycka

## Opis projektu
Projekt implementuje tworzenie drzewa decyzyjnego wykorzystującego algorytm ID3, ktióre pomaga określić chęci do pracy agenta na podstawie warunków panujących na planszy.

### Tworzenie drzewa decyzyjnego 

Funkcja budująca drzewo za pomocą algorymu ID3:

```py
def ID3(data, original_data, attributes, target, parent_node_class=None):

    if len(np.unique(data[target])) <= 1:
        return np.unique(data[target])[0]
    elif len(data) == 0:
        return np.unique(original_data[target])[
            np.argmax(np.unique(original_data[target], return_counts=True)[1])]
    elif len(attributes) == 0:
        return parent_node_class
    else:
        parent_node_class = np.unique(data[target])[
            np.argmax(np.unique(data[target], return_counts=True)[1])]

        item_values = [info_gain(data, i, target) for i in
                       attributes]

        best_attribute_index = np.argmax(item_values)
        best_attribute = attributes[best_attribute_index]

        tree = {best_attribute: {}}
        
        attributes = [i for i in attributes if i != best_attribute]
        for value in np.unique(data[best_attribute]):
            sub_data = data.where(data[best_attribute] == value).dropna()
            subtree = ID3(sub_data, data, attributes, target, parent_node_class)
            tree[best_attribute][value] = subtree

        return (tree)
```
Cechą charakterystyczną algorytmu jest wybór atrybutów dla których kolejno przeprowadzane są testy taki, aby końcowe drzewo było jak najprostsze i jak najefektywniejsze. Wybór atrybutów opiera się na liczeniu entropii, co pozwala obliczyć, wybór którego z atrybutów da największy przyrost informacji. 

Obliczanie wartości przyrostu informacji:

Funkcja oblicza który atrybut najlepiej rozdziela zbiór danych (dzieli zbiór przykładów na jak najbardziej równe podzbiory).

```py
def info_gain(data, split_attribute, target):
   
   _entropy = entropy(data[target])
    vals, counts = np.unique(data[split_attribute], return_counts=True)
    weighted_entropy = np.sum(
        [(counts[i] / np.sum(counts)) * entropy(data.where(data[split_attribute] == vals[i]).dropna()[target])
         for i in range(len(vals))])
    information_gain = _entropy - weighted_entropy

    return information_gain
```

Entropia:

Entropia jest miarą ilości informacji - im mniejsza entropia, tym więcej informacji. W przypadku problemu klasyfikacji przykładów do dwóch odrębnych klas, wzór na entropię przedstawia się następująco:

Entropy(S) = - ∑ pᵢ * log₂(pᵢ) ; i = 1 to n
gdzie:
Z - źródło informacji
p - prawdopodobieństwo wystąpienia przykładu pozytywnego w zbiorze trenującym
(1-p) - prawdopodobieństwo wystąpienia przykładu negatywnego w zbiorze trenującym

```py
def entropy(attribute):
    values, counts = np.unique(target_col, return_counts=True)
    entropy = np.sum(
        [(-counts[i] / np.sum(counts)) * np.log2(counts[i] / np.sum(counts)) for i in range(len(values))])
    return entropy
```

### Zestaw uczący

Zestaw budujący drzewo to lista zawierająca 24 przykładów waruków panujących na polu. Atrybyty zapisane są w formacie ['pogoda', 'ile_chwastow', 'ile_burakow', 'czy_chce_pracowac']. Przykłady ze zbioru:

```py
    ['slonecznie', 'duzo', 'bardzo_malo', 'srednio'],
    ['deszcz', 'bardzo_duzo', 'malo', 'nie'],
    ['grad', 'bardzo_duzo', 'bardzo_malo', 'nie'],
    ['zachmurzenie', 'srednio', 'srednio', 'tak']
```

### Implementacja w projekcie
Podprojet uruchamiany jest za pomocą klawisza *F5*. Pobierane są inforamcje o warunkach panujących na polu, na podstawie których oceniana jest chęć do pracy.

