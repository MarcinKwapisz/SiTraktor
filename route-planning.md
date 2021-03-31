# Sztuczna Inteligencja - Raport Route Planning

**Członkowie zespołu:** Marcin Kwapisz, Kamila Matysiak, Piotr Rychlicki, Justyna Zarzycka

**Temat projektu:** Inteligentny Traktor

**klawisz B** - uruchomienie automatycznego znajdowania ścieżki dla jednego z trybów pracy: 
* 1 - podlewanie
* 2 - odchwaszczanie
* 3 - sadzenie
* 4 - zbieranie

W celu zaplanowania ruchu agenta na kracie wykorzystano schemat procedury przeszukiwania grafu stanów z uwzględnieniem kosztu. 
Zaimplementowano strategię A*, czyli funkcję wyznaczającą priorytet następników,
uwzględniającą zarówno koszt, jak i odpowiednią heurystykę.
Poniżej przedstawiono poszczególne fragmenty kodu, kluczowe dla działania całej procedury.

## Pętla główna strategii przeszukiwania
 
* sprawdzenie aktualnego trybu pracy traktora:

```
if activity == 0:
        avaiable_value = [0,1,2,3]
    elif activity == 1:
        avaiable_value = [1,3,5,7]
    elif activity == 2:
        avaiable_value = [0,1,4,5]
    elif activity == 3:
        avaiable_value = [8]
```

* ustalenie pozycji startowej
* sprawdzenie czy pozycja startowa równa się pożądanej pozyzji końcowej 
* jeżeli nie, ustalenie w którą stronę poruszy się traktor:

```
if start_position == end_point:
        work([int(((config.TRAKTOR_POZ[1]-5)/70)-1), int(((config.TRAKTOR_POZ[0]-5)/70)-1)])
    else:
        route = a_star(start_position,end_point)
        for i in route[::-1]:
            poz = [int(((config.TRAKTOR_POZ[1]-5)/70)-1), int(((config.TRAKTOR_POZ[0]-5)/70)-1)]
            if i[0]> poz[0]:
                move_down()
            elif i[0]< poz[0]:
                move_up()
            elif i[1]> poz[1]:
                move_right()
            elif i[1]< poz[1]:
                move_left()
            pygame.display.update()
            time.sleep(2)
        work([int(((config.TRAKTOR_POZ[1]-5)/70)-1), int(((config.TRAKTOR_POZ[0]-5)/70)-1)])	
```

* funkcja A* - jest to algorytm, którego zadaniem jest znalezienie najkrótszej trasy dla traktora:

```
def a_star(start, end):
    a_queue = PriorityQueue()
    a_queue.put(start,0) 
    cost = {tuple(start): 0}
    path_from = {tuple(start): None}
    finall_path = [tuple(end)]
    found = 0
    while not a_queue.empty():
        current = tuple(a_queue.get())

        if current == tuple(end):
            break

        for next in points(current):
            new_cost = cost[tuple(current)] + int(config.POLE_STAN[next[0],next[1]])
            if tuple(next) not in cost or new_cost < cost[tuple(next)]:
                cost[tuple(next)] = new_cost
                priority = new_cost + heuristic(end, next)
                a_queue.put(next,priority)
                path_from[tuple(next)] = current
                if next == end:
                    found = 1
                    break
        if found:
            break

    pth = path_from[tuple(end)]
    while not pth==tuple(start):
        finall_path.append(pth)
        pth = path_from[pth]

    return finall_path
```

## Funkcja następnika

```
for next in points(current):
            new_cost = cost[tuple(current)] + int(config.POLE_STAN[next[0],next[1]])
            if tuple(next) not in cost or new_cost < cost[tuple(next)]:
                cost[tuple(next)] = new_cost
                priority = new_cost + heuristic(end, next)
                a_queue.put(next,priority)
                path_from[tuple(next)] = current
                if next == end:
                    found = 1
                    break
        if found:
            break		
```

## Heurystyka

Heurystyka to oszacowany dystans między punktem początkowym (aktualnym położeniem agenta na planszy) a punktem końcowym (celem).
Wylicza się ją za pomocą różnic między współrzędnymi (agenta i celu) w pionie i poziomie, 
a następnie podstawienia ich do prostego wzoru Pitagorasa. 
Krótko mówiąc, za pomocą heurystyki można wstępnie szacować koszt dotarcia do celu z akutualnego położenia traktora na planszy.

```
def heuristic(a, b):
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)
```