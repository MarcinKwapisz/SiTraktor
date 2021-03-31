import time

header = ["hydration", "weeds", "empty", "ready", "TODO"]
work = ["Podlac", "Odchwascic", "Zasadzic", "Zebrac"]

# ustawienie kolejnosci trybow na podstawie pogody
# 3 - zebranie
# 1 - odchwaszczenie
# 2 - zasadzenie
# 0 - podlanie



# przetłumaczenie numerka (0-8)
# nawodnienie, chwasty, puste_pole, gotowe_do_zbioru
def translate(field):
    if field == 0:
        return [0, 0, 1, 0]
    elif field == 1:
        return [0, 1, 1, 0]
    elif field == 2:
        return [0, 0, 0, 0]
    elif field == 3:
        return [0, 1, 0, 0]
    elif field == 4:
        return [1, 0, 1, 0]
    elif field == 5:
        return [1, 1, 1, 0]
    elif field == 6:
        return [1, 0, 0, 0]
    elif field == 7:
        return [1, 1, 0, 0]
    elif field == 8:
        return [0, 0, 0, 1]
    else:
        print("Błąd: Zły numer pola.")


# TWORZENIE DRZEWA


# liczenie ilości prac do wykonania
def class_counts(rows):
    counts = {}
    for row in rows:
        label = row[-1]
        if label not in counts:
            counts[label] = 0
        counts[label] += 1
    return counts


# sprawdzenie czy wartość jest liczbą
def is_numeric(value):
    return isinstance(value, int) or isinstance(value, float)


# klasa tworząca zapytanie do podziału danych
class Question():
    def __init__(self, column, value):
        self.column = column
        self.value = value

    def match(self, example):
        val = example[self.column]
        if is_numeric(val):
            return val >= self.value
        else:
            return val == self.value

    # wyświetlenie pytania
    def __repr__(self):
        if is_numeric(self.value):
            condition = "=="
        return "Czy %s %s %s?" % (
            header[self.column], condition, str(self.value)
        )


# podział danych na spełnione i niespełnione wiersze
def partition(rows, question):
    true_rows, false_rows = [], []
    for row in rows:
        if question.match(row):
            true_rows.append(row)
        else:
            false_rows.append(row)
    return true_rows, false_rows


# funkcja implementująca indeks gini
def gini(rows):
    counts = class_counts(rows)
    impurity = 1
    for label in counts:
        prob_of_label = counts[label] / float(len(rows))
        impurity -= prob_of_label ** 2
    return impurity


def info_gain(true, false, current_uncertainty):
    p = float(len(true)) / (len(true) + len(false))
    return current_uncertainty - p * gini(true) - (1 - p) * gini(false)


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


class Leaf:
    def __init__(self, rows):
        self.predictions = class_counts(rows)


class DecisionNode:
    def __init__(self, question, true_branch, false_branch):
        self.question = question
        self.true_branch = true_branch
        self.false_branch = false_branch


# funkcja budująca drzewo
def build_tree(rows):
    gain, question = find_best_split(rows)
    if gain == 0:
        return Leaf(rows)
    true_rows, false_rows = partition(rows, question)

    true_branch = build_tree(true_rows)
    false_branch = build_tree(false_rows)

    return DecisionNode(question, true_branch, false_branch)


# funkcja wypisująca drzewo
def print_tree(node, spacing=""):
    if isinstance(node, Leaf):
        print(spacing + "Przewidywana czynność:", node.predictions)
        return

    print(spacing + str(node.question))

    print(spacing + '--> Prawda: ')
    print_tree(node.true_branch, spacing + " ")

    print(spacing + '--> Fałsz: ')
    print_tree(node.false_branch, spacing + " ")


def classify(field, node):
    if isinstance(node, Leaf):
        return node.predictions
    if node.question.match(field):
        return classify(field, node.true_branch)
    else:
        return classify(field, node.false_branch)


def print_leaf(counts):
    total = sum(counts.values()) * 1.0
    probs = {}
    for label in counts.keys():
        probs[label] = str(int(counts[label] / total * 100)) + "%"
    return probs


def set_order(self):
    if self.field.get_pogoda_value() == 1:
        order = [3, 1, 2]
    else:
        order = [3, 1, 2, 0]
    return order


class main():
    def __init__(self, traktor, field, ui, path):
        self.traktor = traktor
        self.field = field
        self.ui = ui
        self.path = path
        self.best_action = 0


    def main(self):
        self.learn_tree()
        # ustalamy kolejnosc
        order = set_order(self.field.get_pogoda_value())
        for action in order:
            self.traktor.set_mode(action)                                                                              # ustawiamy tryb traktorowi
            self.search_field()                                                                                        # szukamy pól
        print("Koniec roboty")

    def main_collective(self, pole):
        pola = []
        for i in range(len(pole)):
            for j in range(len(pole[i])):
                coords = i * 10 + j
                print("Pole (%d,%d) Przewidziania czynnosc: %s"
                      % (i, j, print_leaf(
                    classify(translate(pole[i][j]), self.tree))))  # przewidujemy czynność za pomocą drzewa
                if work[self.traktor.get_mode()] in self.work_field(
                        classify(translate(pole[i][j]), self.tree)):  # jezeli zgadza sie z aktualnym trybem:
                    print("Zgodne z wykonywanym trybem")
                    pola.append(coords)
        print("Koordynaty:", pola)
        return pola

    def learn_tree(self):

        # tworzymy zbior uczacy, w ktorym podajemy wszystkie mozliwe pola i czynnosci
        training_data = [[0, 0, 1, 0, "Zasadzic"],
                         [0, 1, 1, 0, "Odchwascic"],
                         [0, 0, 0, 0, "Podlac"],
                         [0, 1, 0, 0, "Odchwascic"],
                         # [1, 0, 1, 0, "Zasadzic"],
                         # [1, 1, 1, 0, "Odchwascic"],
                         [1, 0, 0, 0, "Czekac"],
                         # [1, 1, 0, 0, "Odchwascic"],
                         [0, 0, 0, 1, "Zebrac"]]
        self.tree = build_tree(training_data)
        print_tree(self.tree)

    #        print("TEST:")
    #        print("Przewidziania czynnosc: %s Czynnosc: Zasadzic"
    #              % print_leaf(classify(translate(4), self.tree)))
    #        print("Przewidziania czynnosc: %s Czynnosc: Odchwascic"
    #              % print_leaf(classify(translate(5), self.tree)))
    #        print("Przewidziania czynnosc: %s Czynnosc: Odchwascic"
    #              % print_leaf(classify(translate(7), self.tree)))

    def work_field(self, labels):
        works = []

        for label in labels:
            if labels[label] > 0:
                works.append(label)
        return works

    def search_field(self):

        pola = []
        pole = 0
        order = set_order(self.field.get_pogoda_value())
        matrix = self.field.get_matrix()                                                                               # pobieramy pole
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                pole = i * 10 + j
                print("Pole (%d,%d) Przewidziania czynnosc: %s"
                      % (i, j, print_leaf(classify(translate(matrix[i][j]), self.tree))))                              # przewidujemy czynność za pomocą drzewa
                if work[self.traktor.get_mode()] in self.work_field(classify(translate(matrix[i][j]), self.tree)):     # jezeli zgadza sie z aktualnym trybem:
                    print("Zgodne z wykonywanym trybem")
                    pola.append(pole)
                    self.path.find_path(self.traktor, self.field, self.ui, [j, i])                                     # szukamy sciezki
                    self.ui.update()                                                                                   # update'ujemy UI
                    time.sleep(0.5)

