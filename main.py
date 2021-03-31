import pygame, sys
import tractor, pathfinding, field, ui, Justyna, Kamila, Marcin, Piotrek, pathfinding_decision, collective
from pygame.locals import *

pole = field.field()
path = pathfinding.pathfinding()
traktor = tractor.tractor(pole)
UI = ui.game_ui(traktor,pole)
j = Justyna.main(traktor,pole,UI,path)
k = Kamila.main(traktor,pole,UI,pathfinding_decision.pathfinding_dec())
neuro = Marcin.main(traktor,pole,UI,path)
p = Piotrek.main(traktor,pole,UI,path)
c = collective.main(neuro,j,k,p,traktor,pole,UI,path)
pygame.init()
UI.update()
UI.update()
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            print("Zamykanie...")
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            key = pygame.key.get_pressed()
            if key[K_d]:
                traktor.move_right()
            if key[K_s]:
                traktor.move_down()
            if key[K_a]:
                traktor.move_left()
            if key[K_w]:
                traktor.move_up()
            if key[K_SPACE]:
                traktor.work()
            if key[K_1]:
                traktor.set_mode(0)
            if key[K_2]:
                traktor.set_mode(1)
            if key[K_3]:
                traktor.set_mode(2)
            if key[K_4]:
                traktor.set_mode(3)
            if key[K_p]:
                path.pathfinding(traktor,pole,UI)
            if key[K_F4]:
                #Zmiana pogody
                pole.change_weather()
                UI.pogoda()
            if key[K_F5]:
                #Dla projektu Justyny
                j.main()
            if key[K_F6]:
                # Dla projektu Kamili
                k.main()
            if key[K_F7]:
                # Dla projektu Marcina
                neuro.main()
            if key[K_F8]:
                # Dla projektu Piotrka
                p.main()
            if key[K_F9]:
                print(pole.if_value(traktor.get_modes_values()))
            if key[K_F10]:
                print(traktor.get_poz())
            if key[K_F11]:
                print(traktor.get_field_value())
            if key[K_F12]:
                c.main()

            UI.update()
            UI.update()

