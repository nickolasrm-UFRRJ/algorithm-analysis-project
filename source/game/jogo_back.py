import os
import json
import math
import time

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
        self.freezing = [ 0 for i in range(4)]
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

    def setupCars(self):
        self.cars = [1 for i in range(5)]

    def setupStats(self):
        self.givenDamage = 0
        self.zombiesKilled = 0
        self.plantsKilled = 0

    def initJogo(self):
        #inicia o jogo, carrega zumbis, os tipos de planta disponiveis, sois iniciais, etc. Chamado pela main
        self.setupPlants()
        self.setupZombies()
        self.setupCars()
        self.setupStats()
        self.sun_value = 2*c.SUN_VALUE#self.m.map_data[c.INIT_SUN_NAME]
        self.sun_timer = 0
        self.zombie_timer = 0
        self.lost = False
        self.rodando = True


    def removePlant(self, pl):
        self.removePlantInMap(pl.x, pl.y)
        self.plants_list[pl.y].remove(pl)
        if not isinstance(pl, plant.PotatoMine):
            self.increasePlantsKilledCounter()

    def removeZombieAlive(self, zombie):
        self.zombies_alive[zombie.y].remove(zombie)
        self.increaseZombiesKilledCounter()

    def removeZombieFirstZombieAliveInRow(self, row):
        self.zombies_alive.pop()
        self.increaseZombiesKilledCounter()

    def getStats(self):
        return Stats(self.plantsKilled,
                    self.zombiesKilled,
                    self.givenDamage)

    def getAddingPlantDataByName(self, name, x, y):
        if name == c.SUNFLOWER:
            return (plant.SunFlower(x, y), 0)
        elif name == c.PEASHOOTER:
            return (plant.PeaShooter(x, y), 1)
        elif name == c.WALLNUT:
            return (plant.WallNut(x, y), 2)
        elif name == c.POTATOMINE:
            return (plant.PotatoMine(x, y), 3)
        return None

    def isPlantFrozenByCode(self, plantCode):
        if plantCode == c.SUNFLOWER:
            self.isPlantFrozen(0)
        elif plantCode == c.PEASHOOTER:
            self.isPlantFrozen(1)
        elif plantCode == c.WALLNUT:
            self.isPlantFrozen(2)
        elif plantCode == c.POTATOMINE:
            self.isPlantFrozen(3)
        return None

    def isPlantFrozen(self, plantId):
        return self.freezing[plantId] > 0

    def addPlant(self, name, x, y):
        plant = self.getAddingPlantDataByName(name, x, y)
        if self.getPlantInMap(x, y) is None and not self.isPlantFrozen(plant[1]):
            self.plants_list[y].append(plant[0])
            self.setPlantInMap(plant[0], x, y)
            self.setFrozenTimer(plant[1], aux.plant_frozen_time_list[plant[1]])
            self.decreaseSunValue(aux.plant_sun_list[plant[1]])
            return True
        return False
        
    def addZombie(self, name, y, x=(c.GRID_X_LEN*c.GRID_X_SIZE+50)):
        z = zombie.Zombie(name, x, y, c.NORMAL_HEALTH)
        self.zombies_alive[y].append(z)
        return z

    def sortPlants(self):
        def takePosX(plant):
            return plant.x
        for i in range(c.GRID_Y_LEN):
            self.plants_list[i].sort(key=takePosX, reverse=True)

    def checkBoom(self, pl):
        boom = False
        realX = self.getMap().realXPos(pl.x)
        for zombie in self.zombies_alive[pl.y]:
            if zombie.x >= (realX - 2*c.GRID_X_SIZE) and\
                zombie.x <= (realX + c.GRID_X_SIZE):
                boom = True
                self.removeZombieAlive(zombie)
        if boom:
            self.removePlant(pl)


    def getPeashooterTimeToShoot(self):
        peashooterTimes = [[0 for i in range(c.GRID_Y_LEN)] for j in range(c.GRID_X_LEN)]
        for row in self.plants_list:
            for p in row:
                if isinstance(p, plant.PeaShooter):
                    peashooterTimes.append(aux.PEASHOOTER_TIMER - p.hit_timer)
        return peashooterTimes

    def getPeashooterTimesInRowBeforeZombie(self, zombie):
        times = []
        posX = self.getMap().getZombieXPosInMap(zombie)
        for pl in self.plants_list[zombie.y]:
            if pl.x <= posX:
                times.append(pl)
        return pl

    def framesToKillZombieByPeashooter(self, zombie, peashooterTimes = None):
        if peashooterTimes is None:
            peashooterTimes=self.getPeashooterTimesInRowBeforeZombie(zombie)

        if len(peashooterTimes) > 0:
            attacksToKillZombie = math.ceil(zombie.health / c.BULLET_DAMAGE_NORMAL)
            framesToKillZombie = 0

            iterat = min(attacksToKillZombie, len(peashooterTimes))
            for i in range(iterat):
                framesToKillZombie += peashooterTimes[i]
                attacksToKillZombie -= 1
            framesToKillZombie += aux.PEASHOOTER_TIMER * attacksToKillZombie
            return framesToKillZombie
        return math.inf

    def framesToKillPlant(self, pl, zombie):
        attacksToKillPlant = math.ceil(pl.health / zombie.damage)
        framesToKillPlant = (aux.ZOMBIE_ATTACK_TIMER - zombie.attack_timer) + \
                            (aux.ZOMBIE_ATTACK_TIMER * (attacksToKillPlant-1))
        return framesToKillPlant
    
    def numberOfZombieAttacks(self, z, frames):
        framesToFirstAttack = aux.ZOMBIE_ATTACK_TIMER - z.attack_timer
        zFr = 0
        if framesToFirstAttack < frames:
            frames -= framesToFirstAttack
            zFr = 1 + math.floor(frames / aux.ZOMBIE_ATTACK_TIMER)
        return zFr

    def numberOfPeashooterAttacksBeforeZombie(self, zombie, maxFrames, \
            peashooterTimes = None):
        if peashooterTimes is None:
            peashooterTimes=self.getPeashooterTimesInRowBeforeZombie(zombie)
        framesToFirstAttack = 0
        psAttacks = 0

        for time in peashooterTimes:
            framesToFirstAttack = aux.PEASHOOTER_TIMER - time
            if framesToFirstAttack < frames:
                psAttacks += 1
                frames -= framesToFirstAttack
            else:
                break
        else:
            return psAttacks
        return psAttacks + math.floor(frames / (len(peashooterTimes) * aux.PEASHOOTER_TIMER))

    def damageByZombieAttacks(self, att, z):
        return att * z.damage
    def damageByPeashooterAttacks(self, att):
        return att * c.BULLET_DAMAGE_NORMAL

    def getFirstPlantBeforeZombie(self, zombie):
        posX = self.getMap().getZombieXPosInMap(zombie)
        for plant in self.plants_list[zombie.y]:
            if plant.x < posX:
                return plant
        return None

    def framesUntilNewSun(self):
        framesToSun = aux.SUN_TIMER - self.sun_timer
        for row in self.plants_list:
            for pl in row:
                if isinstance(pl, plant.SunFlower):
                    min(framesToSun, pl.sun_timer)
        return framesToSun

    def framesUntilReachTheBoard(self, zombie):
        border = self.getMap().realXPos(8)-1
        if zombie.x > border:
            return math.ceil((zombie.x - border) / zombie.speed)
        return 0

    def updateZombiesAdding(self, frames):
        last = [0 for i in range(len(frames))]
        for timeZombieRow in self.zombie_list:
            limit = frames[timeZombieRow[2]]+self.zombie_timer
            if timeZombieRow[0] < limit:
                last[timeZombieRow[2]] = timeZombieRow[0] - self.zombie_timer
                self.addZombie(timeZombieRow[1], timeZombieRow[2], x=\
                    c.GRID_X_SIZE*c.GRID_X_LEN+50+last[timeZombieRow[2]])

        for i in range(len(last)):
            frames[i] -= last[i]

    def updateCars(self):
        for i, row in enumerate(self.zombies_alive):
            if len(row) > 0 and row[0].x <= 0:
                if self.isThereACar(i):
                    self.removeZombiesAliveInLine(i)
                    self.removeCar(i)
                else:
                    self.setLost()

    def updateUntilLostOrCar(self, i, frames):
        row = self.zombies_alive[i]
        for zombie in row:
            pl = self.getFirstPlantBeforeZombie(zombie)
            if pl is None:
                zombie.x = zombie.x - frames[i]
                frames[i] = 0
                if zombie.x <= 0:
                    break
        self.updateCars()
                

    def updateZombiesUntilCollision(self, i, frames):
        zombiesRow = self.zombies_alive[i]
        timeSpent = 0
        while len(zombiesRow) > 0 and len(self.plants_list[i]) > 0\
                and frames[i] > timeSpent:
            firstZ = zombiesRow[0]
            if self.getMap().getZombieXPosInMap(firstZ.x) >= 9:
                steps = self.framesUntilReachTheBoard(firstZ)
                walked = timeSpent + steps
                if walked > frames[i]:
                    rest = frames[i] - timeSpent
                    firstZ.walk(rest)
                    timeSpent += rest
                    break
                else:
                    firstZ.walk(steps)
                    timeSpent += steps

            if self.getMap().getZombieXPosInMap(firstZ.x) < 9:
                firstP = self.getFirstPlantBeforeZombie(firstZ)
                if firstP is not None:
                    timeToCol = (firstZ.x - \
                        self.getMap().realXPos(firstP)) / firstZ.speed
                    timeToCol = min(timeToCol, frames[i]-timeSpent)

                    framesToKillZombie = min(self.framesToKillZombieByPeashooter(zombie),\
                                            timeToCol)
                    attacks = self.numberOfPeashooterAttacksBeforeZombie(framesToKillZombie, \
                            framesToKillZombie)

                    firstZ.health -= self.damageByPeashooterAttacks(attacks)
                    timeSpent += framesToKillZombie
                    
                    if firstZ.health <= 0:
                        self.removeZombieFirstZombieAliveInRow(i)
                        zombiesRow[0].walk(timeSpent)
                    else:
                        firstZ.x = self.getMap().realXPos(firstP.x)-1
                        break
        frames[i] -= timeSpent

        for j in range(1, len(zombiesRow)):
            zombiesRow[j].walk(timeSpent)


    def updateZombiesOnCollision(self, i, frames):
        row = self.zombies_alive[i]
        timeSpent = 0
        if len(self.plants_list[i]) > 0:
            for zombie in row:
                if self.getMap().getZombieXPosInMap(zombie) < 9:
                    pl = self.getPlantInMap(self.getMap().getZombieXPosInMap(zombie),\
                                    zombie.y)
                    if isinstance(pl, plant.PotatoMine):
                        time = min(1, frames[i])
                        if time > 0:
                            self.checkBoom(pl)
                            timeSpent = max(timeSpent, time)
                    elif pl is not None:
                        if isinstance(pl, plant.PeaShooter):
                            framesToKillZombie = self.framesToKillZombieByPeashooter(zombie)
                            framesToKillPlant = self.framesToKillPlant(pl, zombie)

                            time = min(framesToKillZombie, framesToKillPlant, frames[i])

                            pl.health -= self.damageByZombieAttacks(\
                                self.numberOfZombieAttacks(zombie, time), zombie)
                            zombie.health -= self.damageByPeashooterAttacks(
                                    self.numberOfPeashooterAttacksBeforeZombie(\
                                        pl,zombie,time))
                            if pl.health <= 0:
                                self.removePlant(plant)
                            if zombie.health <= 0:
                                self.removeZombieAlive(zombie)

                            timeSpent = max(timeSpent, time)
                    else:
                        continue
        frames[i] -= timeSpent


    def updateSunflowers(self, frames):
        sun = 0
        for row in self.plants_list:
            for pl in row:
                if isinstance(plant, plant.SunFlower):
                    sun += pl.update(frames)
        self.sun_value += sun

    def updateSun(self, frames):
        self.sun_timer += frames
        if self.sun_timer >= aux.SUN_TIMER:
            self.sun_timer = 0
            self.sun_value += 25

    def checkFinished(self):
        for z in self.zombies_alive:
            if len(z) > 0:
                return False
        return (len(self.zombie_list) == 0) or self.isLost()

    def updateStates(self, frames):
        self.zombie_timer += frames
        self.updateSunflowers(frames)
        self.updateSun(frames)
        self.rodando = not self.checkFinished()

    def updateUntilNewSun(self):
        frames = self.framesUntilNewSun()
        framesPerRow = [frames for i in range(c.GRID_Y_LEN)]
        self.sortPlants()

        self.updateZombiesAdding(framesPerRow)
        for i in range(len(framesPerRow)):
            while framesPerRow[i] > 0 and len(self.zombies_alive[i]) > 0:
                self.updateUntilLostOrCar(i, framesPerRow)
                self.updateZombiesUntilCollision(i, framesPerRow)
                self.updateZombiesOnCollision(i, framesPerRow)

        self.updateStates(frames)

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
        return self.getPlantInMap(x, y) is not None
    def getPlantsKilledCounter(self):
        return self.plantsKilled
    def getZombiesKilledCounter(self):
        return self.zombiesKilled
    def getGivenDamageCounter(self):
        return self.givenDamage
    def isLost(self):
        return self.lost
    def isThereACar(self, line):
        return self.cars[line]
    #setters
    def setFrozenTimer(self, plantIndex, time):
        self.freezing[plantIndex] = time
    def removeZombiesAliveInLine(self, line):
        self.increaseZombiesKilledCounter(len(self.zombies_alive[line]))
        self.zombies_alive[line].clear()
    def removeCar(self, line):
        self.cars[line] = 0
    def increasePlantsKilledCounter(self):
        self.plantsKilled += 1
    def increaseZombiesKilledCounter(self, n = 1):
        self.zombiesKilled += n
    def increaseGivenDamage(self, dmg):
        self.givenDamage += dmg
    def setPlantInMap(self, plant, x, y):
        self.getMap().getBoard()[y][x] = plant
    def removePlantInMap(self, x, y):
        self.getMap().getBoard()[y][x] = None
    def setLost(self):
        self.lost = True
    def decreaseSunValue(self, val):
        self.sun_value -= val