class main():

    def __init__(self,marcin, justyna, kamila, piotrek, traktor, pole, UI, path):
        self.marcin = marcin
        self.justyna = justyna
        self.kamila = kamila
        self.piotrek = piotrek
        self.traktor = traktor
        self.pole = pole
        self.UI = UI
        self.path = path

    # ustalanie kolejnosci wykonywania dzialam na podstwie pogody
    # 3 - zbieranie, 2 - sadzenie, 1 - odchwaszczanie, 0 - podlewanie
    def set_order(self):
        if self.pole.get_pogoda_value() == 1:  #jak deszcz, to bez podlewania
            order = [3, 1, 2]
        else:
            order = [3, 1, 2, 0]
        return order


    def main(self):

        self.justyna.main() # sprawdzamy czy oplaca sie pracowac

        if(self.justyna.result != 'nie'): 
            order = self.set_order()  #wybieramy kolejnosc prac na polu
            self.kamila.learn_tree()  #uczenie drzewa
            for action in order:
                self.traktor.set_mode(action)                   # ustawiamy tryb traktorowi
                field = self.neuro_check_field()                # sprawdzamy pole
                coords = self.kamila.main_collective(field)     # zwracam koordynaty pol zgodych z wybranym trybem
                first_coord = coords[0]
                coords.append(first_coord)
                self.piotrek.main(coords)
                # tutaj Piotrek tworzy optymalna sciezke
                # traktor wykonuje prace na polu
            pass
        

    def neuro_check_field(self):
        field = []
        row = []
        print("Sprawdzanie siecią neuronową całego pola, proszę czekać...")
        for i in range(0, 10):
            print("Sprawdzam "+str(i+1)+" wiersz")
            for j in range(0, 10):
                row.append(self.marcin.main_collective([j,i]))
            field.append(row)
            row = []
        return field



    # 1. sprawdza czy opłaca się pracować
    # 2. sprawdza pole na którym stoi żeby drzewo podjęło decyzje
    # 3. Uruchamia się drzewo
    # 4. Wojażer leci przez pola i zostaje na ostatnim
    # 5. -> 2.  Jeżeli nie ma na danym polu nic do roboty