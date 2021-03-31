import numpy
import random

class field():
    def __init__(self,training=0):
        self.training = training
        self.weather = self.pogoda()
        if self.training == 1:
            #Macierz treningowa
            self.field_matrix = numpy.array([[8,0,1,3,0,6,4,3,2,3],
                                 [1,4,8,3,7,7,8,5,1,5],
                                 [8,7,6,0,4,0,7,7,5,0],
                                 [5,4,8,0,5,3,8,1,7,7],
                                 [6,0,2,3,2,0,6,6,2,2],
                                 [5,8,8,5,4,3,3,1,5,8],
                                 [7,8,7,1,5,7,8,0,4,8],
                                 [7,3,6,6,0,0,5,6,1,2],
                                 [7,2,8,7,1,2,5,3,2,4],
                                 [2,4,6,7,6,7,3,5,4,6]])
        else:
            self.field_matrix = numpy.random.randint(0, 9, (10, 10))
        print("Reprezentacja pola jako macierz:")
        print("###################")
        for i in self.field_matrix:
            for j in i:
                print(j, end=" ")
            print("")
        print("###################")

    def get_matrix(self):
        return self.field_matrix

    def change_value(self, position, value):
        self.field_matrix[position[1],position[0]] += value

    def get_value(self,position):
        return self.field_matrix[position[1],position[0]]

    def if_value(self,value):
        for i in value:
            if i in self.field_matrix:
                return 1
        return 0

    def pogoda(self):
        number = random.randrange(0, 4)
        return number

    def get_pogoda_value(self):
        return self.weather

    def get_pogoda_name(self):
        if self.weather==0:
            return 'slonecznie'
        elif self.weather==1:
            return 'deszcz'
        elif self.weather==2:
            return 'grad'
        elif self.weather==3:
            return 'zachmurzenie'

    def change_weather(self):
        self.weather = self.pogoda()