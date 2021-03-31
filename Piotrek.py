import field, pathfinding_tractorless, pathfinding_tractor
import random

class main():

    def __init__(self,traktor,field,ui,path):
        self.traktor = traktor
        self.field = field
        self.ui = ui
        self.path = path
        self.pathfinding_tractorless = pathfinding_tractorless.pathfinding_tractorless()
        self.pathfinding_tractor = pathfinding_tractor.pathfinding_tractor()

    # def wspolrzedne(self):                                  #wyznacza wspolrzedne pol danego rodzaju na planszy
    #     znalezione_pola = []
    #     k = 0
    #     ktore_pole = self.traktor.get_modes_values()        #rodzaj pól zależy od ustawionego trybu pracy agenta
    #     for i in self.field.field_matrix:
    #         l = 0
    #         for j in i:
    #             if j in ktore_pole:
    #                 znalezione_pola.append(k*10+l)
    #             l = l + 1
    #         k = k + 1
    #     pierwsze_szukane_pole = znalezione_pola[0]           #początkowa współrzędna, w każdym przypadku pole startowe [0,0]
    #     znalezione_pola.append(pierwsze_szukane_pole)
    #     print("Współrzędne szukanych pól: " + str(znalezione_pola))
    #     return znalezione_pola

    def koszt_przejazdu(self,znalezione_pola):               #wyznacza koszt trasy przez pola danego rodzaju w zadanej kolejnosci
        self.liczba_pol = len(znalezione_pola)
        total_cost = 0
        i = 0
        while i < (self.liczba_pol - 1):
            # print(str(self.pathfinding_tractorless.pathfinding_tractorless(self.field,znalezione_pola,i)))
            total_cost = total_cost + self.pathfinding_tractorless.pathfinding_tractorless(self.field,znalezione_pola,i)
            # print(str(total_cost))
            i = i + 1
        # print("Koszt przejścia przez pola w zadanej kolejności: " + str(total_cost))
        # print("###################")
        return total_cost

    def tworzenie_pokolenia(self,znalezione_pola,i):
        first_coord = znalezione_pola[0]
        x = len(znalezione_pola) - 2
        wspolrzedne_shuffle = []
        while x > 0:
            wspolrzedne_shuffle.append(znalezione_pola[x])
            x = x - 1
        x = len(znalezione_pola) - 1
        lista_osobnikow = []
        while i > 0:                    #liczebność pierwszego pokolenia (domyślnie 10)
            nowy_osobnik = random.sample(wspolrzedne_shuffle, len(wspolrzedne_shuffle))
            nowy_osobnik.insert(0,first_coord)    #dodanie na początek listy 0, jako współrzenej startowej
            nowy_osobnik.insert(x,first_coord)    #dodanie na koniec listy 0, jako współrzenej końcowej
            lista_osobnikow.append(nowy_osobnik)
            i = i - 1
        # print("Lista osobników: " + str(lista_osobnikow))
        return lista_osobnikow

    def ocena_przystosowania(self,pokolenia):
        suma_kosztow_tras = 0
        ile_osobnikow = 0
        koszty_tras_osobnikow = []
        y = 0
        pierwszy_koszt = self.koszt_przejazdu(pokolenia[y])
        najtanszy_osobnik = pokolenia[y]
        najnizszy_koszt = pierwszy_koszt
        najwyzszy_koszt = pierwszy_koszt
        for i in pokolenia:
            koszty_tras_osobnikow.append(self.koszt_przejazdu(i))
            suma_kosztow_tras = suma_kosztow_tras + self.koszt_przejazdu(i)
            ile_osobnikow = ile_osobnikow + 1
            if self.koszt_przejazdu(i) < najnizszy_koszt:
                najnizszy_koszt = self.koszt_przejazdu(i)
                najtanszy_osobnik = i
            if self.koszt_przejazdu(i) > najwyzszy_koszt:
                najwyzszy_koszt = self.koszt_przejazdu(i)
        # print("Najtansza trasa w danym pokoleniu: " + str(najnizszy_koszt))
        # print("Najdrozsza trasa w danym pokoleniu: " + str(najwyzszy_koszt))
        srednie_przystosowanie = suma_kosztow_tras/ile_osobnikow #parametr potrzebny do oceny przystosowania osobnikow
        przystosowanie_osobnikow = []
        sumaryczne_przystosowanie_osobnikow = 0
        l = 0
        for i in koszty_tras_osobnikow:
            przystosowanie_osobnikow.append(round(((srednie_przystosowanie/koszty_tras_osobnikow[l])*10),2))
            sumaryczne_przystosowanie_osobnikow += round(((srednie_przystosowanie/koszty_tras_osobnikow[l])*10),2)
            l = l + 1
        # print(str(round(sumaryczne_przystosowanie_osobnikow,2)))
        # print("Ocena przystosowania każdego z osobników: " + str(przystosowanie_osobnikow))
        # print("Koszty tras każdego z osobników: " + str(koszty_tras_osobnikow))
        # print("Średnie przystosowanie wszystkich osobników: " + str(srednie_przystosowanie))
        return(przystosowanie_osobnikow, najnizszy_koszt, najwyzszy_koszt, srednie_przystosowanie, najtanszy_osobnik)

    def wybor_populacji_posredniej(self,pierwsze_pokolenie,przystosowanie_osobnikow):
        x = len(przystosowanie_osobnikow)
        tabela_ruletki = []
        populacja_posrednia = []
        i = 0
        przedzial = 0
        while x > 0:                            #stworzenie "koła ruletki" do selecji osobników populacji pośredniej
            przedzial = przedzial + przystosowanie_osobnikow[i]
            tabela_ruletki.append(round(przedzial,2))
            x = x - 1
            i = i + 1
        #print("Tabela ruletki do losowania z przedziałami dla każdego osobnika: " + str(tabela_ruletki))
        x = len(przystosowanie_osobnikow)/2     #losowanie połowy liczby osobników populacji początkowej do populacji pośredniej
        maks = tabela_ruletki[i-1]
        while x > 0:
            i = 0
            n = random.uniform(0, maks)         #losowanie przedziału
            while n > tabela_ruletki[i]:
                i = i + 1
            populacja_posrednia.append(pierwsze_pokolenie[i])
            x = x - 1
        # print("Populacja pośrednia (rodziców): " + str(populacja_posrednia)) #populacja posrednia, z której zostanie utworzona populacja potomków
        return populacja_posrednia

    def krzyzowanie(self,populacja_posrednia):
        populacja_po_krzyzowaniu = []
        x = len(populacja_posrednia) - 1
        while x > 0:
            rodzic_1 = populacja_posrednia[x]
            #print("Rodzic nr 1: " + str(rodzic_1))
            rodzic_2 = populacja_posrednia[x-1]
            #print("Rodzic nr 2: " + str(rodzic_2))
            dziecko_1 = []
            dziecko_2 = []
            czy_krzyzowac = random.randint(1,100)       #losowanie czy krzyzowac rodzicow, czy nie (szanse 10%)
            if (czy_krzyzowac < 11) and (rodzic_1 != rodzic_2):                      #jesli krzyzowanie nastepuje
                miejsce_krzyzowania = random.randint(1,(len(populacja_posrednia[x])-3))     #wybor miejsca krzyzowania
                l = 0
                k = miejsce_krzyzowania
                while k >= 0:                            #dodawanie do dziecka pierwszej połowy z pierwszego rodzica
                    dziecko_1.append(rodzic_1[l])
                    l = l + 1
                    k = k - 1
                k = miejsce_krzyzowania
                while k < (len(rodzic_1)-2):       #dodawanie do dziecka drugiej połowy z drugiego rodzica
                    for i in rodzic_2:
                        if i not in dziecko_1:
                            dziecko_1.append(i)
                            k = k + 1
                l = 0
                k = miejsce_krzyzowania
                while k >= 0:                               #dodawanie do dziecka pierwszej połowy z pierwszego rodzica
                    dziecko_2.append(rodzic_2[l])
                    l = l + 1
                    k = k - 1
                k = miejsce_krzyzowania
                while k < (len(rodzic_1)-2):       #dodawanie do dziecka drugiej połowy z drugiego rodzica
                    for i in rodzic_1:
                        if i not in dziecko_2:
                            dziecko_2.append(i)
                            k = k + 1
                dziecko_1.append(0)
                dziecko_2.append(0)
            else:                                           #jesli krzyzowanie nie nastepuje, wowczas potencjalni rodzice staja sie dziecmi
                dziecko_1 = rodzic_1
                dziecko_2 = rodzic_2
            populacja_po_krzyzowaniu.append(dziecko_1)
            populacja_po_krzyzowaniu.append(dziecko_2)
            # print("Dziecko nr 1: " + str(dziecko_1))
            # print("Dziecko nr 2: " + str(dziecko_2))
            x = x - 1

        #ostatnie krzyżowanie, pomiędzy pierwszym a ostatnim rodzicem z listy osobnikow nalezacych do populacji posredniej

        rodzic_1 = populacja_posrednia[0]
        #print("Rodzic nr 1: " + str(rodzic_1))
        rodzic_2 = populacja_posrednia[(len(populacja_posrednia)-1)]
        #print("Rodzic nr 2: " + str(rodzic_2))
        dziecko_1 = []
        dziecko_2 = []
        czy_krzyzowac = random.randint(1,100)       #losowanie czy krzyzowac rodzicow, czy nie (szanse 10%)
        if (czy_krzyzowac < 11) and (rodzic_1 != rodzic_2):                      #jesli krzyzowanie nastepuje
            miejsce_krzyzowania = random.randint(1,(len(populacja_posrednia[x])-3))     #wybor miejsca krzyzowania
            l = 0
            k = miejsce_krzyzowania
            while k >= 0:                            #dodawanie do dziecka pierwszej połowy z pierwszego rodzica
                dziecko_1.append(rodzic_1[l])
                l = l + 1
                k = k - 1
            k = miejsce_krzyzowania
            while k < (len(rodzic_1)-2):       #dodawanie do dziecka drugiej połowy z drugiego rodzica
                for i in rodzic_2:
                    if i not in dziecko_1:
                        dziecko_1.append(i)
                        k = k + 1
            l = 0
            k = miejsce_krzyzowania
            while k >= 0:                               #dodawanie do dziecka pierwszej połowy z pierwszego rodzica
                dziecko_2.append(rodzic_2[l])
                l = l + 1
                k = k - 1
            k = miejsce_krzyzowania
            while k < (len(rodzic_1)-2):       #dodawanie do dziecka drugiej połowy z drugiego rodzica
                for i in rodzic_1:
                    if i not in dziecko_2:
                        dziecko_2.append(i)
                        k = k + 1
            dziecko_1.append(0)
            dziecko_2.append(0)
        else:                                           #jesli krzyzowanie nie nastepuje, wowczas potencjalni rodzice staja sie dziecmi
            dziecko_1 = rodzic_1
            dziecko_2 = rodzic_2
        populacja_po_krzyzowaniu.append(dziecko_1)
        populacja_po_krzyzowaniu.append(dziecko_2)
        # print("Dziecko nr 1: " + str(dziecko_1))
        # print("Dziecko nr 2: " + str(dziecko_2))
        return populacja_po_krzyzowaniu

    def mutacja(self,populacja_po_krzyzowaniu):
        k = len(populacja_po_krzyzowaniu) - 1
        while k >= 0:
            czy_mutacja = random.randint(0,100) 
            if czy_mutacja < 3:                     # Szanse 2%
                kogo_mutujemy = populacja_po_krzyzowaniu[k]
                populacja_po_krzyzowaniu.remove(kogo_mutujemy)
                l = len(kogo_mutujemy) - 1
                # print("Osobnik przed mutacją: " + str(kogo_mutujemy))
                x = random.randint(1,l)
                y = random.randint(1,l)
                while x == y:
                    y = random.randint(1,l)
                zamiennik = kogo_mutujemy[x]
                kogo_mutujemy[x] = kogo_mutujemy[y]
                kogo_mutujemy[y] = zamiennik
                # print("Osobnik po mutacji: " + str(kogo_mutujemy))
                populacja_po_krzyzowaniu.insert(k,kogo_mutujemy)
            else:
                pass
            k = k - 1
        populacja_po_mutacji = populacja_po_krzyzowaniu
        # print("Populacja po mutacji: " + str(populacja_po_mutacji))
        return populacja_po_mutacji

    def optymalizacja(self,populacja_po_mutacji,znalezione_pola):        #polega na eliminacji powtarzających się tras
        populacja_po_optymalizacji = populacja_po_mutacji
        i = len(populacja_po_mutacji)
        l = 1
        while l < i:
            k = l
            while k >= 0:
                if populacja_po_mutacji[l] == populacja_po_mutacji[k-1]:
                    populacja_po_optymalizacji.remove(populacja_po_mutacji[k-1])
                    x = len(znalezione_pola) - 2
                    wspolrzedne_shuffle = []
                    while x > 0:
                        wspolrzedne_shuffle.append(znalezione_pola[x])
                        x = x - 1
                    x = len(znalezione_pola) - 1
                    nowy_osobnik = random.sample(wspolrzedne_shuffle, len(wspolrzedne_shuffle))
                    nowy_osobnik.insert(0,znalezione_pola[0])    #dodanie na początek listy 0, jako współrzenej startowej
                    nowy_osobnik.insert(x,znalezione_pola[0])
                    populacja_po_optymalizacji.append(nowy_osobnik)
                    # print("Nastąpiła optymalizacja")
                else:
                    pass
                k = k - 1
            l = l + 1
        # print("Populacja po optymalizacji: " + str(populacja_po_optymalizacji))
        return populacja_po_optymalizacji

    def algorytm_genetyczny(self,coords):
        self.koszt_trasy = self.koszt_przejazdu(coords)
        # Utworzenie pokolenia 
        self.pierwsze_pokolenie = self.tworzenie_pokolenia(coords,10)
        # Funkcja przystosowania
        self.przystosowanie, self.najnizszy_koszt, self.najwyzszy_koszt, self.srednie_przystosowanie_pierwszego_pokolenia, self.najtanszy_osobnik = self.ocena_przystosowania(self.pierwsze_pokolenie)
        # Populacja pośrednia wybrana metodą ruletki
        self.populacja_posrednia = self.wybor_populacji_posredniej(self.pierwsze_pokolenie, self.przystosowanie)
        # Krzyżowanie populacji pośredniej
        self.populacja_po_krzyzowaniu = self.krzyzowanie(self.populacja_posrednia)
        # Mutacja populacji pośredniej 
        self.populacja_po_mutacji = self.mutacja(self.populacja_po_krzyzowaniu)
        # Optymalizacja populacji pośredniej 
        self.populacja_po_optymalizacji = self.optymalizacja(self.populacja_po_mutacji,coords)
        self.maks_koszt = self.najwyzszy_koszt
        self.min_koszt = self.najnizszy_koszt
        self.najtansza_trasa = self.najtanszy_osobnik
        i = 2
        self.ktore_pokolenie = 1
        while i < 41:
            print(" ")
            print("*********************")
            print("Pokolenie " + str(i))
            print("*********************")
            print(" ")
            # Funkcja przystosowania
            self.przystosowanie, self.najnizszy_koszt, self.najwyzszy_koszt, self.srednie_przystosowanie, self.najtanszy_osobnik = self.ocena_przystosowania(self.populacja_po_optymalizacji)
            if self.najwyzszy_koszt > self.maks_koszt:
                self.maks_koszt = self.najwyzszy_koszt
            if self.najnizszy_koszt < self.min_koszt:
                self.min_koszt = self.najnizszy_koszt
                self.najtansza_trasa = self.najtanszy_osobnik                
                self.ktore_pokolenie = i
                print("Nowy najnizszy koszt: " + str(self.min_koszt))
                print("Nowa najtansza trasa: " + str(self.najtansza_trasa))
            # Populacja pośrednia wybrana metodą ruletki
            self.populacja_posrednia = self.wybor_populacji_posredniej(self.populacja_po_mutacji, self.przystosowanie)
            # Krzyżowanie populacji pośredniej
            self.populacja_po_krzyzowaniu = self.krzyzowanie(self.populacja_posrednia)
            # Mutacja populacji pośredniej
            self.populacja_po_mutacji = self.mutacja(self.populacja_po_krzyzowaniu)
            # Optymalizacja populacji pośredniej
            self.populacja_po_optymalizacji = self.optymalizacja(self.populacja_po_mutacji,coords)
            i = i + 1
            if (self.min_koszt)/(self.srednie_przystosowanie_pierwszego_pokolenia) < (0.69):
                print("Zakończono wykonywanie algorytmu po " + str(i) + " pokoleniach")
                break 
        print("Średnie przygotowanie pierwszego pokolenia: " + str(self.srednie_przystosowanie_pierwszego_pokolenia))
        print("Stosunek poprawienia kosztu trasy względem początku: " + str((self.min_koszt)/(self.srednie_przystosowanie_pierwszego_pokolenia)))
        print("Najnizszy znaleziony koszt to " + str(self.min_koszt) + " znaleziony w pokoleniu nr " + str(self.ktore_pokolenie))
        print("Najtansza znaleziona trasa to " + str(self.najtansza_trasa))
        # print("Najwyzszy znaleziony koszt: " + str(self.maks_koszt))

    def wykonanie_trasy(self):
        i = len(self.najtansza_trasa) - 1
        l = 0
        while l < i:
            self.pathfinding_tractor.pathfinding_tractor(self.field, self.traktor, self.ui, self.najtansza_trasa, l)
            l = l + 1

    def main(self,coords):
        self.algorytm_genetyczny(coords)
        self.wykonanie_trasy()