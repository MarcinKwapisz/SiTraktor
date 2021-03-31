# Sztuczna Inteligencja 

**Członkowie zespołu:** Marcin Kwapisz, Kamila Matysiak, Piotr Rychlicki, Justyna Zarzycka

**Temat projektu:** Inteligentny Traktor

Agent w toku działania programu na samym początku wykorzystuje moduł "Justyna", aby sprawdzić, na podstawie warunków panujących na polu, czy opłaca się pracować. W przypadku pozytywnego wyniku, za pomocą modułu "Marcin", sprawdza co znajduje się na każdym polu. Następnie "Kamila" dla każdego trybu pracy zbiera informacje o koordynatach pól i dodaje je do listy postaci tablicy ze współrzędnymi, gdzie współrzędna danego pola to k*10+l, gdzie k to rząd, a l to kolumna.
"Piotrek" na podstawie tych danych wyznacza najlepszą trasę. 

```py
def main(self):

        self.justyna.main() 

        if(self.justyna.result != 'nie'): 
            order = self.set_order()  
            self.kamila.learn_tree() 
            for action in order:
                self.traktor.set_mode(action)                   
                field = self.neuro_check_field()                
                coords = self.kamila.main_collective(field)     
                                self.piotrek.main(coords)
                
            pass
```