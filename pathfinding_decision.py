from queue import PriorityQueue
import time

class pathfinding_dec():
    def __init__(self):
        pass

    def heuristic(self,a, b):
        (x1, y1) = a
        (x2, y2) = b
        return abs(x1 - x2) + abs(y1 - y2)

    def points(self, point):
        self.point = []
        for i in [[point[0],point[1]-1],[point[0]-1,point[1]],[point[0],point[1]+1],[point[0]+1,point[1]]]:
            if i[0] in [-1,10] or i[1] in [-1,10]:
                pass
            else:
                self.point.append(i)
        return self.point

    def find_path(self, traktor, field, ui, destination):
        self.ui = ui
        self.traktor = traktor
        self.activity = self.traktor.get_mode()
        self.start_position = self.traktor.get_poz()
        self.field = field
        self.end_point = destination

        if self.start_position == self.end_point:
            self.traktor.work()
        else:
            self.route = self.a_star(self.start_position,self.end_point)
            for i in self.route[::-1]:
                self.poz = self.traktor.get_poz()
                if i[1]> self.poz[1]:
                    self.traktor.move_down()
                elif i[1]< self.poz[1]:
                    self.traktor.move_up()
                elif i[0]> self.poz[0]:
                    self.traktor.move_right()
                elif i[0]< self.poz[0]:
                    self.traktor.move_left()
                self.ui.update()
                time.sleep(0.1)
            self.traktor.work()


    def a_star(self,start, end):
        self.a_queue = PriorityQueue()
        self.a_queue.put(start,0)
        self.cost = {tuple(start): 0}
        self.path_from = {tuple(start): None}
        self.finall_path = [tuple(end)]
        self.found = 0
        while not self.a_queue.empty():
            self.current = tuple(self.a_queue.get())

            if self.current == tuple(end):
                break

            for self.next in self.points(self.current):
                self.new_cost = self.cost[tuple(self.current)] + self.field.get_value(self.next)
                if tuple(self.next) not in self.cost or self.new_cost < self.cost[tuple(self.next)]:
                    self.cost[tuple(self.next)] = self.new_cost
                    self.priority = self.new_cost + self.heuristic(end, self.next)
                    self.a_queue.put(self.next,self.priority)
                    self.path_from[tuple(self.next)] = self.current
                    if self.next == end:
                        self.found = 1
                        break
            if self.found:
                break

        self.pth = self.path_from[tuple(end)]
        while not self.pth==tuple(start):
            self.finall_path.append(self.pth)
            self.pth = self.path_from[self.pth]

        return self.finall_path


    def search(self,start,value):
        self.checked = []
        self.visited = [start]
        while self.visited:
            if self.field.get_value(self.visited[0]) in value:
                # print("Znaleziono pole: "+str(self.visited[0]))
                return self.visited[0]
            else:
                self.p = self.points(self.visited[0])
                for i in self.p:
                    if i not in self.checked:
                        self.visited.append(i)
                self.checked.append(self.visited[0])
                del self.visited[0]


