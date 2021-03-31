from queue import PriorityQueue
import time

class pathfinding_tractorless():
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

    def pathfinding_tractorless(self,field,pola_buraczane,i):
        self.pola = pola_buraczane
        self.start_position = [int(self.pola[i])%10,int(self.pola[i])//10]
        # print(str(self.start_position))
        self.field = field
        self.end_point = [int(self.pola[i+1])%10,int(self.pola[i+1])//10]
        # print(str(self.end_point))           

        if self.start_position == self.end_point:
            return 0 
        else:
            self.route = self.a_star(self.start_position,self.end_point)
            return self.route


    def a_star(self,start,end):
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
        while not self.pth == tuple(start):
            self.finall_path.append(self.pth)
            self.pth = self.path_from[self.pth]

        return self.new_cost