import os
import json
from source.back.componentes.plant_back import CherryBomb
from source.back.auxiliar import SUN_TIMER
from source.constants import ATTACK, GRID_Y_LEN, POTATOMINE
from .. import constants as c
from .componentes.map import Map
from .componentes import plant_back as plant
from .componentes import zombie_back as zombie
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
            self.zombie_list.append((aux.timeToFrame(data['time']), data['name'], data['map_y']))
        self.zombie_start_time = 0
        self.zombie_list.sort(key=takeTime)

    def setupBullets(self):
        self.bullet_list = [[] for y in range(5)]
    
    def setupCars(self):
        self.cars = [1 for i in range(5)]

    def initJogo(self):
        #inicia o jogo, carrega zumbis, os tipos de planta disponiveis, sois iniciais, etc. Chamado pela main
        self.setupPlants()
        self.setupBullets()
        self.setupZombies()
        self.setupCars()
        self.sun_value = self.m.map_data[c.INIT_SUN_NAME]
        self.sun_timer = 0
        self.zombie_timer = 0
        self.result = aux.GANHOU
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
        elif name == c.POTATOMINE:
            self.plants_list[y].append(plant.PotatoMine(x, y))
            self.m.map[y][x] = 1
        elif name == c.CHERRYBOMB:
            self.plants_list[y].append(plant.CherryBomb(x, y))
            self.m.map[y][x] = 1
        

    def addZombie(self, name, y):
        self.zombies_alive[y].append(zombie.Zombie(name, y, c.NORMAL_HEALTH))

    def sortPlants(self):
        def takePosX(plant):
            return plant.x
        for i in range(c.GRID_Y_LEN):
            self.plants_list[i].sort(key=takePosX, reverse=True)

    def play(self):
        # Aqui a Ia vai fazer a play, mas por enquanto usarei um sistema de pausa pra testar insercao
        # Pausa o cronometro. e insere. depois retorna
        print(aux.BREAK_LINE)
        print(aux.PLAY)
        opcao = 0
        print("Escolha uma planta")
        opcao = input()

        if opcao >= '0' and opcao <= '9':
            opcao = int(opcao)
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
                        self.sortPlants()
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
                        self.sortPlants()
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
                        self.sortPlants()
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
                        self.addPlant(c.CHERRYBOMB, x, y)
                        self.sortPlants()
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
            elif opcao == 5:
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
                        self.addPlant(c.POTATOMINE, x, y)
                        self.sortPlants()
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
        else:
            print(aux.BREAK_LINE)
            print("Digite um número válido! Aperte qualquer coisa para avançar")
            input()
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
                string += str(plant.name) + " " + str(plant.y) + " " + str(plant.x) + " REAL_X_POS :: " + str(self.m.realXPos(plant.x)) + " :: VIDA: " + str(plant.health) + " :: "
            print(string)
        
        print(aux.BREAK_LINE)
        print("Zombies alive")
        for i in range(self.m.alt):
            for zombie in self.zombies_alive[i]:
                print("Nome: " + str(zombie.name) + " :: MAP_Y: " + str(zombie.y)  + " :: MAP_X: " + str(zombie.x) + " :: VIDA: " + str(zombie.health) + " :: STATE: " + ("ATTACKING" if zombie.state == c.ATTACK else "WALKING") + " :: ")
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

    def checkPlantColision(self, zombie):
        if len(self.plants_list[zombie.y]) > 0:
            if self.m.realXPos(self.plants_list[zombie.y][0].x) >= zombie.x and zombie.state == c.WALK:
                zombie.setAttack()
            if self.plants_list[zombie.y][0].health <= 0:
                self.plants_list[zombie.y].pop()
                zombie.setWalk()


    def checkBulletColision(self):
        for i in range(5):
            for bullet in self.bullet_list[i]:
                if bullet.x_pos > (c.GRID_X_LEN + 1) * c.GRID_X_SIZE:
                    self.bullet_list[i].remove(bullet)
                if len(self.zombies_alive[i]) > 0:
                    if bullet.x_pos >= self.zombies_alive[i][0].x:
                        self.zombies_alive[i][0].health -= bullet.damage
                        self.bullet_list[i].remove(bullet)
                    if self.zombies_alive[i][0].health <= 0:
                        self.zombies_alive[i].pop()

    def checkZombieColision(self):
         for i in range(c.GRID_Y_LEN):
            for zombie in self.zombies_alive[i]:
                self.checkPlantColision(zombie)
                if self.cars[zombie.y] == 1 and zombie.x <= 0:
                    y = zombie.y
                    self.zombies_alive[y].clear()
                    self.cars[y] = 0
                    print("Carro ativado!!!")
                if zombie.x + 90 <= 0:
                    self.zombies_alive[zombie.y].pop()
                    self.result = aux.PERDEU
                

    # ADICIONANDO ZUMBIS NO DEVIDO TEMPO
    def checkStartTime(self):
        if len(self.zombie_list) > 0:
            self.zombie_timer += 1
            for zombie in self.zombie_list:
                if self.zombie_timer >= zombie[0]:
                    print("adding")
                    self.addZombie(zombie[1], zombie[2])
                    self.zombie_list.pop(0)
                    return  

    # EXPLODA MISERAVEL!
    def checkBoom(self, plant):
        did_boom = False
        if plant.name == c.POTATOMINE or plant.name == c.CHERRYBOMB:
            if plant.name == c.POTATOMINE and plant.is_init == False:
                return 
            for i in range(c.GRID_Y_LEN):
                if abs( i - plant.y) > plant.explode_y_range:
                    continue
                else:
                    # print("TRY BOOM: " + str(i))
                    for zombie in self.zombies_alive[i]:
                        real_x = self.m.realXPos(plant.x)
                        if abs( ( zombie.x + 14) - ( real_x - 40 ) ) <= plant.explode_x_range:
                            print("BOOMMM???")
                            self.zombies_alive[i].remove(zombie)
                            did_boom = True
            if did_boom:
                self.m.map[plant.y][plant.x] = 0
                self.plants_list[plant.y].remove(plant)
                            
    # CHECANDO SE O JOGO ACABOU
    def checkIsOver(self):
        empty = 1
        for i in range(c.GRID_Y_LEN):
            if len(self.zombies_alive[i]) > 0:
                empty = 0
        if empty and len(self.zombie_list) > 0:
            empty = 0
        return empty

    def checkGameResult(self):
        print(aux.FLIP_STATE)
        if self.result == aux.GANHOU:
            print("Você ganhou!!! Parabéns.")
        else:
            print("Voce perdeu!!! Tente Novamente...")

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
                elif plant.name == c.POTATOMINE:
                    plant.update()
                    self.checkBoom(plant)
                elif plant.name == c.CHERRYBOMB:
                    self.checkBoom(plant)

            if  len(self.plants_list[i]) > 0 and self.plants_list[i][0].health <= 0:
                self.plants_list[i].pop()

    def updateZombie(self):
        for i in range(c.GRID_Y_LEN):
            for zombie in self.zombies_alive[i]:
                if zombie.state == c.ATTACK:
                    zombie.update(self.plants_list[zombie.y][0])
                else:
                    zombie.update()
        pass

    def updateEstados(self):
        self.checkBulletColision()
        self.checkZombieColision()

    # Update nas variaveis
        self.updatePlant()
        self.updateBullet()
        self.updateZombie()

        if self.checkIsOver():
            self.rodando = False

        if self.sun_timer >= aux.SUN_TIMER:
            self.sun_value += 25 * int(self.sun_timer / aux.SUN_TIMER)
            self.sun_timer = int(self.sun_timer % aux.SUN_TIMER)

    def updateFrame(self, n_frames):
        for i in range (n_frames):
            self.sun_timer += 1
            
            # Da update em todos os frames
            self.checkStartTime()
            self.updateFreeze()
            self.updateEstados()

    def gameLoop(self):
        opcao = 0
        print(aux.FLIP_STATE)
        print(aux.DECISAO)
        opcao = input()
        if opcao >= '0' and opcao <= '9':
            opcao = int(opcao)
            if opcao == 1:
                self.updateFrame(1)
                self.showState()
            elif opcao == 2:
                print(aux.DECISAO_2)
                self.updateFrame(int(input()))
                self.showState()
            elif opcao == 3:
                self.updateFrame( (aux.SUN_TIMER - int(self.sun_timer % aux.SUN_TIMER) ) )
                self.showState()
                pass
            elif opcao == 4:
                self.play()
                self.showState()
            elif opcao == 5:
                self.rodando = False
            else:
                print(aux.BREAK_LINE)
                print("Opção não existe! Aperte qualquer tecla para voltar")
                input()
        else:
            print(aux.BREAK_LINE)
            print("Digite um número válido! Aperte qualquer tecla para voltar")
            input()
            print(aux.FLIP_STATE)

    def main(self):
        self.rodando = True
        self.initJogo()
        while self.rodando:
            self.gameLoop()
        self.checkGameResult()