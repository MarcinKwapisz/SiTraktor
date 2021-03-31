import pandas as pd
import numpy as np
from pprint import pprint
import dataset
import random

# obliczenie entropii dla wskazanej kolumny
def entropy(attribute):
    values, counts = np.unique(attribute, return_counts=True)
    entropy = np.sum(
        [(-counts[i] / np.sum(counts)) * np.log2(counts[i] / np.sum(counts)) for i in range(len(values))])
    return entropy

#obliczanie wartości przyrostu informacji
def info_gain(data, split_attribute, target):

    # Wartość entropii zbioru
    _entropy = entropy(data[target])

    # Wyodrębnienie poszczególnych podzbiorów
    vals, counts = np.unique(data[split_attribute], return_counts=True)

    # Średnia ważona entropii każdego podzbioru
    weighted_entropy = np.sum(
        [(counts[i] / np.sum(counts)) * entropy(data.where(data[split_attribute] == vals[i]).dropna()[target])
         for i in range(len(vals))])

    # Przyrost informacji
    information_gain = _entropy - weighted_entropy

    return information_gain


def ID3(data, original_data, attributes, target, parent_node_class=None):


    # Jeżeli wszystkie atrybuty są takie same, zwracamy liść z pierwszą napotkaną wartością

    if len(np.unique(data[target])) <= 1:
        return np.unique(data[target])[0]

    elif len(data) == 0:
        return np.unique(original_data[target])[
            np.argmax(np.unique(original_data[target], return_counts=True)[1])]

    elif len(attributes) == 0:
        return parent_node_class

    else:

        # nadrzędna wartość
        parent_node_class = np.unique(data[target])[
            np.argmax(np.unique(data[target], return_counts=True)[1])]

        # obliczenie przyrostu informacji dla każdego atrybutu
        item_values = [info_gain(data, i, target) for i in
                       attributes]

        # Wybór najlepszego atrybutu
        best_attribute_index = np.argmax(item_values)
        best_attribute = attributes[best_attribute_index]

        # Struktura drzewa
        tree = {best_attribute: {}}

        # Aktualizacja zbioru atrybutów
        attributes = [i for i in attributes if i != best_attribute]

        # Budowa poddrzewa dla każdej wartości wybranego atrybutu
        for value in np.unique(data[best_attribute]):

            sub_data = data.where(data[best_attribute] == value).dropna()
            subtree = ID3(sub_data, data, attributes, target, parent_node_class)

            tree[best_attribute][value] = subtree

        return (tree)

#tesownie drzewa
def test(data, tree):
    queries = data.iloc[:, :-1].to_dict(orient="records")

    predicted = pd.DataFrame(columns=["predicted"])

    for i in range(len(data)):
        predicted.loc[i, "predicted"] = search(queries[i], tree, 'nie')
    print('Precyzja przewidywań: ', (np.sum(predicted["predicted"] == data['czy_chce_pracowac']) / len(data)) * 100, '%')

#dostowanie danych (lista na słownik) i wywolanie na nich funkcji serach
def data_to_dict(data, tree):

    queries = pd.DataFrame(data=data, columns=dataset.header)
    predicted = pd.DataFrame(columns=["predicted"])
    dict = queries.iloc[:, :-1].to_dict(orient="records")

    for i in range(len(data)):
        predicted.loc[i, "predicted"] = search(dict[i], tree, 'nie')

    predicted_list = predicted.values.tolist()
    return predicted_list[0][0]

#przeszukwianie drzewa
def search(query, tree, default='nie'):

    for key in list(query.keys()):
        if key in list(tree.keys()):
            try:
                result = tree[key][query[key]]
            except:
                return default
            result = tree[key][query[key]]
            if isinstance(result, dict):
                return search(query, result)

            else:
                return result

class main():
    def __init__(self,traktor,field,ui,path):
        self.traktor = traktor
        self.field = field
        self.ui = ui
        self.path = path
        self.result = 0

    def main(self):
        training_data = pd.DataFrame(data=dataset.training_data, columns=dataset.header)
        testing_data = pd.DataFrame(data=dataset.testing_data, columns=dataset.header)

        # Utworzenie drzewa
        tree = ID3(training_data, training_data, training_data.columns[:-1], 'czy_chce_pracowac')
        pprint(tree)

        # Testowanie drzewa
        #print(test(testing_data, tree))

        # Uzyskanie danych od agenta
        ocena_burakow = self.ocen_ile_burakow()
        ocena_chwastow = self.ocen_ile_chwastow()
        pogoda = self.field.get_pogoda_name()
        print('chwasty: ' + ocena_chwastow)
        print('buraki: ' + ocena_burakow)
        print('pogoda: ' + pogoda)
        data = [[pogoda, ocena_chwastow, ocena_burakow, '']]

        #podjecie decyzji
        self.result = data_to_dict(data, tree)
        print('czy oplaca sie pracowac: ' + self.result)
    
    def get_result(self):
        return self.result

    def licz_chwasty_buraki(self):
        chwasty = 0
        buraki = 0

        for i in self.field.field_matrix:
            for j in i:
                if(j==8):
                    buraki = buraki + 1
                elif(j%2==1):
                    chwasty = chwasty + 1
        return chwasty, buraki

    def ocen_ile_burakow(self):
        chwasty, buraki = self.licz_chwasty_buraki()
        if buraki < 5:
            return 'bardzo_malo'
        elif buraki >= 5 and buraki<10:
            return 'malo'
        elif buraki >=10 and buraki<15:
            return 'srednio'
        elif buraki >=15 and buraki<20:
            return 'duzo'
        elif buraki >=20:
            return 'bardzo_duzo'

    def ocen_ile_chwastow(self):
        chwasty, buraki = self.licz_chwasty_buraki()
        if chwasty < 40:
            return 'bardzo_malo'
        elif chwasty >= 40 and chwasty<42:
            return 'malo'
        elif chwasty >=42 and chwasty<45:
            return 'srednio'
        elif chwasty >=45 and chwasty<48:
            return 'duzo'
        elif chwasty >=48:
            return 'bardzo_duzo'

