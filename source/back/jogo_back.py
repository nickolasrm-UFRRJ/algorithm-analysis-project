import os
import json
from source.back.auxiliar import SUN_TIMER
from source.constants import GRID_Y_LEN
from .. import constants as c
from .componentes.map import Map
from .componentes import plant_back as plant
from . import auxiliar as aux


class JogoBack():
    def __init__(self):
        # mapa = instancia do mapa, em /source/component/map.py
        # mapa comeca zerado a cada insercao ele vai olhar no mapa pra ver se da pra fazer ou nao
        self.m = Map(c.GRID_X_LEN, c.GRID_Y_LEN)
        self.state = None
        self.current_time = 0
        self.state = aux.SHOW_MAP
        self.freezing = [ 0 for i in range(5)]

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

    def setupBullets(self):
        self.bullet_list = [[] for y in range(5)]

    def initJogo(self):
        #inicia o jogo, carrega zumbis, os tipos de planta disponiveis, sois iniciais, etc. Chamado pela main
        self.setupPlants()
        self.setupBullets()
        self.setupZombies()
        self.sun_value = self.m.map_data[c.INIT_SUN_NAME]
        self.sun_timer = 0
        pass

    def addPlant(self, name, x, y):
        if name == c.SUNFLOWER:
            self.plants_list[y].append(plant.SunFlower(x, y))
            self.m.map[y][x] = 1
        elif name == c.PEASHOOTER:
            self.plants_list[y].append(plant.PeaShooter(x, y))
            self.m.map[y][x] = 1
        elif name == c.WALLNUT:
            self.plants_list[y].append(plant.WallNut(x, y))
            self.m.map[y][x] = 1

    def play(self):
        # Aqui a Ia vai fazer a play, mas por enquanto usarei um sistema de pausa pra testar insercao
        # Pausa o cronometro. e insere. depois retorna
        print(aux.BREAK_LINE)
        print(aux.PLAY)
        opcao = 0
        print("Escolha uma planta")
        opcao = int(input())

        if opcao == 1:
            print(aux.BREAK_LINE)
            print("Digite a posição que deseja inserir ( y e depois x ): ")
            label = "y = "
            y = int(input(label))
            label = "x = "
            x = int(input(label))
            if self.sun_value >= aux.plant_sun_list[opcao-1] and self.freezing[opcao-1] <= 0:
                if self.m.isEmpty(x, y):
                    self.sun_value -= aux.plant_sun_list[opcao-1]
                    self.freezing[opcao-1] = aux.plant_frozen_time_list[opcao-1]
                    self.addPlant(c.SUNFLOWER, x, y)
                    pass
                else:
                    print(aux.BREAK_LINE + "Posição não disponível!")
                    print(aux.BREAK_LINE + "Aperte enter para continuar")
                    input()
            elif self.freezing[opcao-1] > 0:
                print(aux.BREAK_LINE + "A planta está em cooldown")
                print(aux.BREAK_LINE + "Aperte enter para continuar")
                input()
            else:
                print(aux.BREAK_LINE + "Não possui sol o bastante!")
                print(aux.BREAK_LINE + "Aperte enter para continuar")
                input()


        elif opcao == 2:
            print(aux.BREAK_LINE)
            print("Digite a posição que deseja inserir ( y e depois x ): ")
            label = "y = "
            y = int(input(label))
            label = "x = "
            x = int(input(label))
            if self.sun_value >= aux.plant_sun_list[opcao-1] and self.freezing[opcao-1] <= 0:
                if self.m.isEmpty(x, y):
                    self.sun_value -= aux.plant_sun_list[opcao-1]
                    self.freezing[opcao-1] = aux.plant_frozen_time_list[opcao-1]
                    self.addPlant(c.PEASHOOTER, x, y)
                    pass
                else:
                    print(aux.BREAK_LINE + "Posição não disponível!")
                    print(aux.BREAK_LINE + "Aperte enter para continuar")
                    input()
            elif self.freezing[opcao-1] > 0:
                print(aux.BREAK_LINE + "A planta está em cooldown")
                print(aux.BREAK_LINE + "Aperte enter para continuar")
                input()
            else:
                print(aux.BREAK_LINE + "Não possui sol o bastante!")
                print(aux.BREAK_LINE + "Aperte enter para continuar")
                input()
            pass


        elif opcao == 3:
            print(aux.BREAK_LINE)
            print("Digite a posição que deseja inserir ( y e depois x ): ")
            label = "y = "
            y = int(input(label))
            label = "x = "
            x = int(input(label))
            if self.sun_value >= aux.plant_sun_list[opcao-1] and self.freezing[opcao-1] <= 0:
                if self.m.isEmpty(x, y):
                    self.sun_value -= aux.plant_sun_list[opcao-1]
                    self.freezing[opcao-1] = aux.plant_frozen_time_list[opcao-1]
                    self.addPlant(c.WALLNUT, x, y)
                    pass
                else:
                    print(aux.BREAK_LINE + "Posição não disponível!")
                    print(aux.BREAK_LINE + "Aperte enter para continuar")
                    input()
            elif self.freezing[opcao-1] > 0:
                print(aux.BREAK_LINE + "A planta está em cooldown")
                print(aux.BREAK_LINE + "Aperte enter para continuar")
                input()
            else:
                print(aux.BREAK_LINE + "Não possui sol o bastante!")
                print(aux.BREAK_LINE + "Aperte enter para continuar")
                input()
            pass
        elif opcao == 4:
            pass
        elif opcao == 5:
            pass
        else:
            pass
    
    def showState(self):
        print(aux.FLIP_STATE)
        print("Total de sois = " + str(self.sun_value))
        print("Sun timer: " + str(self.sun_timer))
        print(aux.BREAK_LINE)
        for i in range(self.m.alt):
            print(self.m.map[i])
        
        print(aux.BREAK_LINE)
        print("Plants alive")
        for i in range(self.m.alt):
            string = ""
            for plant in self.plants_list[i]:
                string += str(plant.name) + " " + str(plant.y) + " " + str(plant.x) + "/ "
                if plant.name == c.SUNFLOWER:
                    string += "sun timer = " + str(plant.sun_timer) + " / "
            print(string)
        
        print(aux.BREAK_LINE)
        print("Zombies alive")
        for i in range(self.m.alt):
            print(self.zombies_alive[i])

        print(aux.BREAK_LINE)
        print("Zombies list")
        for zombie in self.zombie_list:
            print(zombie)

        print(aux.BREAK_LINE)
        print("Bullet list")
        for i in range(5):
            # print(self.bullet_list[i])
            string = ""
            for bullet in self.bullet_list[i]:
                string += str(bullet.name) + " - x = " + str(bullet.x_pos) + ", y = " + str(bullet.y_pos) + " // "
            print(string)
        
        print(aux.BREAK_LINE)
        print(aux.BREAK_LINE)
        
        print("Digite qualquer elemento e aperte enter para continuar:")
        input()

    # SESSAO DAS COLISOES

    def checkBulletColision(self):
        for i in range(5):
            for bullet in self.bullet_list[i]:
                if bullet.x_pos > (c.GRID_X_LEN + 1) * c.GRID_X_SIZE:
                    self.bullet_list[i].remove(bullet)
                    

    # SESSAO DOS UPDATES

    def updateFreeze(self):
        # self.freezing eh um vetor de 5 posicoes em que cada posicao corresponde a um tipo de carta.
        for i in range(5):
            if self.freezing[i] > 0:
                self.freezing[i] -= 1

    def updateBullet(self):
        for i in range(5):
            for bullet in self.bullet_list[i]:
                bullet.update()
        pass

    def updatePlant(self):
        for i in range(c.GRID_Y_LEN):
            for plant in self.plants_list[i]:
                if plant.name == c.SUNFLOWER:
                    # print("Sunflower_timer " + str(plant.sun_timer))
                    self.sun_value += plant.update()
                elif plant.name == c.PEASHOOTER:
                    bullet = plant.update()
                    if bullet != None:
                        print("Adicionando bala!!!!!!!")
                        self.bullet_list[i].append(bullet)
                else:
                    continue
    def updateEstados(self):
        # Update nas variaveis
        self.updatePlant()
        self.updateBullet()

        self.checkBulletColision()
        if self.sun_timer >= aux.SUN_TIMER:
            self.sun_value += 25 * int(self.sun_timer / aux.SUN_TIMER)
            self.sun_timer = int(self.sun_timer % aux.SUN_TIMER)

    def updateFrame(self, n_frames):
        for i in range (n_frames):
            self.sun_timer += 1
            # Da update em todos os frames
            self.updateFreeze()
            self.updateEstados()
            # self.play()

    def gameLoop(self):
        opcao = 0
        print(aux.FLIP_STATE)
        print(aux.DECISAO)
        opcao = int(input())
        if opcao == 1:
            self.updateFrame(1)
        elif opcao == 2:
            print(aux.DECISAO_2)
            self.updateFrame(int(input()))
        elif opcao == 3:
            self.updateFrame( (aux.SUN_TIMER - int(self.sun_timer % aux.SUN_TIMER) ) )
            pass
        elif opcao == 4:
            self.play()
        elif opcao == 5:
            self.rodando = False
        else:
            pass
        self.showState()

    def main(self):
        self.rodando = True
        self.initJogo()
        while self.rodando:
            self.gameLoop()
        pass