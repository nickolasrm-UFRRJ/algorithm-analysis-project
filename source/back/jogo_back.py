import os
import json
from source.constants import GRID_Y_LEN
import pygame as pg
from .. import constants as c
from . import frame
from .componentes.map import Map
from .componentes import plant_back as plant
from . import auxiliar as aux


class JogoBack():
    def __init__(self):
        # mapa = instancia do mapa, em /source/component/map.py
        # mapa comeca zerado a cada insercao ele vai olhar no mapa pra ver se da pra fazer ou nao
        self.m = Map(c.GRID_X_LEN, c.GRID_Y_LEN)
        self.surface = pg.display.get_surface()
        self.surface.fill((255,255,255))
        self.state = None
        self.clock = pg.time.Clock()
        self.current_time = 0
        self.stateTimer = 0
        self.state = aux.SHOW_MAP

    def setupPlants(self):
        self.plants_list = [[] for y in range(5)]

    def setupZombies(self):
        def takeTime(element):
            return element[0]

        self.zombie_list = []
        self.zombies_alive = [[] for y in range(5)]
        for data in self.m.map_data[c.ZOMBIE_LIST]:
            self.zombie_list.append((data['time'], data['name'], data['map_y']))
        self.zombie_start_time = 0
        self.zombie_list.sort(key=takeTime)

    def initJogo(self):
        #inicia o jogo, carrega zumbis, os tipos de planta disponiveis, sois iniciais, etc. Chamado pela main
        self.setupPlants()
        self.setupZombies()
        self.sun_value = self.m.map_data[c.INIT_SUN_NAME]
        self.sun_timer = self.current_time
        pass

    def addPlant(self, name, x, y):
        if name == c.SUNFLOWER:
            self.plants_list[y].append(plant.SunFlower(x, y))
            self.m.map[y][x] = 1

    def play(self):
        # Aqui a Ia vai fazer a play, mas por enquanto usarei um sistema de pausa pra testar insercao
        # Pausa o cronometro. e insere. depois retorna
        print(aux.PLAY)
        opcao = 0
        print("Escolha uma planta")
        opcao = int(input())
        if input == 1:
            pass
        elif input == 2:
            pass
        elif input == 3:
            pass
        elif input == 4:
            pass
        elif input == 5:
            pass
        else:
            pass
        
    def handleEvents(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                print(aux.QUIT)
                self.rodando = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    print(aux.QUIT)
                    self.rodando = False
                elif event.key == pg.K_j:
                    if self.state != aux.JOGADA:
                        self.state = aux.JOGADA
                    print(aux.JOGADA)
            pass    
    
    def showState(self):
        print(aux.FLIP_STATE)
        print("Total de sois = " + str(self.sun_value))
        print(aux.BREAK_LINE)
        for i in range(self.m.alt):
            print(self.m.map[i])
        
        print(aux.BREAK_LINE)
        print("Plants alive")
        for i in range(self.m.alt):
            string = ""
            for plant in self.plants_list[i]:
                string += str(plant.name) + " " + str(plant.y) + " " + str(plant.x) + "/ "
            print(string)
        
        print(aux.BREAK_LINE)
        print("Zombies alive")
        for i in range(self.m.alt):
            print(self.zombies_alive[i])

        print(aux.BREAK_LINE)
        print("Zombies list")
        for zombie in self.zombie_list:
            print(zombie)

    def updatePlant(self):
        for i in range(c.GRID_Y_LEN):
            for plant in self.plants_list[i]:
                if plant.name == c.SUNFLOWER:
                    if plant.update(self.current_time) == 1:
                        self.sun_value += 25
                        print("opaaa")
                else:
                    continue

    def updateEstados(self):
        # Update nas variaveis
        self.updatePlant()

        if (self.current_time - self.sun_timer) >= c.PRODUCE_SUN_INTERVAL:
            self.sun_timer = self.current_time
            self.sun_value += c.SUN_VALUE

    def updateFrame(self):
        self.current_time = pg.time.get_ticks()
        # Da update em todos os frames
        self.handleEvents()
        self.updateEstados()
        # self.play()
        pass

    def gameLoop(self):

        if (self.current_time - self.stateTimer) >= 1000 and self.state == aux.SHOW_MAP:
            self.stateTimer = self.current_time
            self.showState()
        elif self.state == aux.JOGADA:
            self.play()
            self.state = aux.SHOW_MAP
            pass
        self.updateFrame()
        pass

    def main(self):
        self.rodando = True
        self.pause = False
        self.initJogo()
        self.addPlant(c.SUNFLOWER, 0, 0)
        self.sun_value -= 50
        while self.rodando:
            self.gameLoop()
            pg.display.update()
            self.clock.tick(60)
        pass