import copy
import random
import numpy as np
import sys
from collections import namedtuple
from source.game import jogo_back as back
from source.game.componentes import plant_back as Plant
from source.game.componentes import auxiliar as aux
from source.game.componentes import constants as const
from source.montecarlo import mcts as mcts

Move = namedtuple('Move', 'plant x y')

class AITree(mcts.Tree):
    def __init__(self, game, move = None, p=None, c=None):
        super().__init__(parent = p, children = c)
        self.game = game
        self.move = move

    def getMove(self):
        return self.move

    def getGame(self):
        return self.game

    def randomPlacer(self, st, end, plant):
        map = self.getGame().getMap()
        game = self.getGame()

        pos = []
        for i in range(map.getHeight()):
            for j in range(st, end):
                if not game.isThereAPlant(j,i):
                    pos.append((i,j))
        if len(pos) > 0:
            p = pos[np.random.randint(0, len(pos))]
            game.addPlant(plant, p[1], p[0])

    def getRandomPlacerStEnd(self, plant):
        if plant == const.SUNFLOWER:
            return (0, 2)
        elif plant == const.PEASHOOTER:
            return (2, 5)
        elif plant == const.POTATOMINE:
            return (4,9)
        elif plant == const.WALLNUT:
            return (4,6)
        elif plant == const.CHERRYBOMB:
            return (7,9)
        else:
            return None

    def evaluate(self, game, oldStats):            
        stats = game.getStats()
        grade = 0
        if game.isLost():
            grade = -sys.float_info.max
        else:
            grade = -10 * (stats.plantsKilled - oldStats.plantsKilled) +\
                    -100 * (stats.lostCars) +\
                    10 * (stats.zombiesKilled - oldStats.zombiesKilled) +\
                    (stats.givenDamage - oldStats.givenDamage)
        self.score = grade

    def simulate(self):
        game_copy = copy.deepcopy(self.getGame())
        stats = self.getGame().getStats()

        while game_copy.isRunning():
            game_copy.runUntilNewSun()
            sunValue = game_copy.getSunValue()
            plantToPlace = const.SUNFLOWER

            if len(self.getGame().getPlantsList()) < \
                        self.getGame().getMap().getWidth() * \
                        self.getGame().getMap().getHeight():
                while plantToPlace != None:
                    plantToPlace = None
                    for i, cost in enumerate(aux.plant_sun_list):
                        if cost < sunValue and np.random.uniform(0,1) < 0.5 and\
                                not self.getGame().isFrozen(i):
                            plantToPlace = aux.plant_name_list[i]
                            break
                    if np.random.uniform(0,1) < 0.5: #increasing do nothing probability
                        plantToPlace = None

                    if plantToPlace is not None:
                        stend = self.getRandomPlacerStEnd(plantToPlace)
                        self.randomPlacer(stend[0], stend[1], plantToPlace)
        return self.evaluate(game_copy, stats)

    def expand(self):
        game = self.getGame()
        sunValue = game.getSunValue()
        availablePlants = []

        for i, cost in enumerate(aux.plant_sun_list):
            if cost < sunValue and not game.isFrozen(i) and\
                    np.random.uniform(0,1) < 0.5:
                availablePlants.append(aux.plant_name_list[i])
        
        possibleMoves = []
        for plant in availablePlants:
            stend = self.getRandomPlacerStEnd(plant)
            for i in range(game.getMap().getHeight()):
                for j in range(stend[0], stend[1]):
                    if not game.isThereAPlant(j, i):
                        cop = copy.deepcopy(game)
                        cop.addPlant(plant, j, i)
                        possibleMoves.append(AITree(cop, move=Move(plant, j, i), p=self))
        possibleMoves.append(AITree(copy.deepcopy(game), p=self))
        return possibleMoves

def doNextMovement(game, complexity):
    tree = AITree(game)
    for i in range(complexity):
        tree = mcts.MCTS(tree)

    move = max(tree.children, key= lambda x:x.score).getMove()
    if move is not None:
        game.addPlant(move.plant, move.x, move.y)

    return tree