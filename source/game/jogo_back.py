import os
import json

from source.game.componentes import constants as c
from source.game.componentes.map import Map
from source.game.componentes import plant_back as plant
from source.game.componentes import zombie_back as zombie
from source.game.componentes import auxiliar as aux
from collections import namedtuple
import numpy.random as r

Stats = namedtuple('Stats', 'plantsKilled zombiesKilled givenDamage')

class JogoBack():
    def __init__(self, lvl=1):
        # mapa = instancia do mapa, em /source/component/map.py
        # mapa comeca zerado a cada insercao ele vai olhar no mapa pra ver se da pra fazer ou nao
        self.m = Map(c.GRID_X_LEN, c.GRID_Y_LEN, lvl=lvl)
        self.state = None
        self.current_time = 0
        self.state = aux.SHOW_MAP
        self.freezing = [ 0 for i in range(5)]
        self.initJogo()

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

    def setupStats(self):
        self.givenDamage = 0
        self.zombiesKilled = 0
        self.plantsKilled = 0

    def initJogo(self):
        #inicia o jogo, carrega zumbis, os tipos de planta disponiveis, sois iniciais, etc. Chamado pela main
        self.setupPlants()
        self.setupBullets()
        self.setupZombies()
        self.setupCars()
        self.setupStats()
        self.sun_value = 2*c.SUN_VALUE#self.m.map_data[c.INIT_SUN_NAME]
        self.sun_timer = 0
        self.zombie_timer = 0
        self.lost = False
        self.rodando = True

    #getters
    def getPlantsList(self):
        return self.plants_list
    def getZombiesAliveList(self):
        return self.zombies_alive
    def isRunning(self):
        return self.rodando
    def getSunValue(self):
        return self.sun_value
    def getMap(self):
        return self.m
    def getPlantInMap(self, x, y):
        return self.getMap().getBoard()[y][x]
    def isThereAPlant(self, x, y):
        return self.getPlantInMap(x, y)
    def getPlantsKilledCounter(self):
        return self.plantsKilled
    def getZombiesKilledCounter(self):
        return self.zombiesKilled
    def getGivenDamageCounter(self):
        return self.givenDamage
    def isLost(self):
        return self.lost
    #setters
    def increasePlantsKilledCounter(self):
        self.plantsKilled += 1
    def increaseZombiesKilledCounter(self):
        self.zombiesKilled += 1
    def increaseGivenDamage(self, dmg):
        self.givenDamage += dmg
    def setPlantInMap(self, x, y):
        self.getMap().getBoard()[y][x] = 1
    def removePlantInMap(self, x, y):
        self.getMap().getBoard()[y][x] = 0
    def setLost(self):
        self.lost = True
    def decreaseSunValue(self, val):
        self.sun_value -= val

    def getStats(self):
        return Stats(self.plantsKilled,
                    self.zombiesKilled,
                    self.givenDamage)

    def getAddingPlantDataByName(self, name, x, y):
        if name == c.SUNFLOWER:
            return (plant.SunFlower(x, y), aux.plant_sun_list[0])
        elif name == c.PEASHOOTER:
            return (plant.PeaShooter(x, y), aux.plant_sun_list[1])
        elif name == c.WALLNUT:
            return (plant.WallNut(x, y), aux.plant_sun_list[2])
        elif name == c.CHERRYBOMB:
            return (plant.CherryBomb(x, y), aux.plant_sun_list[3])
        elif name == c.POTATOMINE:
            return (plant.PotatoMine(x, y), aux.plant_sun_list[4])
        return None

    def addPlant(self, name, x, y):
        if not self.isThereAPlant(x, y):
            plant = self.getAddingPlantDataByName(name, x, y)
            if plant is not None:
                self.plants_list[y].append(plant[0])
                self.setPlantInMap(x,y)
                self.decreaseSunValue(plant[1])
                return True
        return False
        
    def addZombie(self, name, y):
        self.zombies_alive[y].append(zombie.Zombie(name, y, c.NORMAL_HEALTH))

    def sortPlants(self):
        def takePosX(plant):
            return plant.x
        for i in range(c.GRID_Y_LEN):
            self.plants_list[i].sort(key=takePosX, reverse=True)

    # SESSAO DAS COLISOES

    def checkPlantColision(self, zombie):
        if len(self.plants_list[zombie.y]) > 0:
            front_pos = self.m.realXPos(self.plants_list[zombie.y][0].x)
            if front_pos >= zombie.x and front_pos-80 <= zombie.x and zombie.state == c.WALK:
                zombie.setAttack()
            if self.plants_list[zombie.y][0].health <= 0:
                #print(str(self.plants_list[zombie.y][0].name) + " x " + str(self.plants_list[zombie.y][0].x) + " y " + str(self.plants_list[zombie.y][0].y)) 
                plant = self.plants_list[zombie.y][0]
                self.plants_list[zombie.y].remove(plant)
                zombie.setWalk()


    def checkBulletColision(self):
        for i in range(5):
            for bullet in self.bullet_list[i]:
                if bullet.x_pos > (c.GRID_X_LEN + 1) * c.GRID_X_SIZE:
                    self.bullet_list[i].remove(bullet)
                if len(self.zombies_alive[i]) > 0:
                    if bullet.x_pos >= self.zombies_alive[i][0].x:
                        self.zombies_alive[i][0].health -= bullet.damage
                        self.increaseGivenDamage(bullet.damage)
                        self.bullet_list[i].remove(bullet)
                    if self.zombies_alive[i][0].health <= 0:
                        self.increaseZombiesKilledCounter()
                        self.zombies_alive[i].pop()

    def checkZombieColision(self):
         for i in range(c.GRID_Y_LEN):
            for zombie in self.zombies_alive[i]:
                self.checkPlantColision(zombie)
                if self.cars[i] == 1:
                    if zombie.x <= 0:
                        self.zombies_alive[i].clear()
                        self.cars[i] = 0
                        break
                elif zombie.x <= 0:
                    self.setLost()

    # ADICIONANDO ZUMBIS NO DEVIDO TEMPO
    def checkStartTime(self):
        if len(self.zombie_list) > 0:
            self.zombie_timer += 1
            for zombie in self.zombie_list:
                if self.zombie_timer >= zombie[0]:
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
        return empty or self.isLost()

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
                        #print("Adicionando bala!!!!!!!")
                        self.bullet_list[i].append(bullet)
                elif plant.name == c.POTATOMINE:
                    plant.update()
                    self.checkBoom(plant)
                elif plant.name == c.CHERRYBOMB:
                    self.checkBoom(plant)

            if  len(self.plants_list[i]) > 0 and self.plants_list[i][0].health <= 0:
                self.increasePlantsKilledCounter()
                self.plants_list[i].pop()

    def updateZombie(self):
        for i in range(c.GRID_Y_LEN):
            for zombie in self.zombies_alive[i]:
                if zombie.state == c.ATTACK:
                    if len(self.plants_list[zombie.y]) > 0:
                        zombie.update(self.plants_list[zombie.y][0])
                    else:
                        zombie.setWalk()
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

    def runUntilNewSun(self):
        old = self.sun_value
        while old == self.getSunValue():
            self.updateFrame(1)
            