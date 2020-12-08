import copy
import random
import sys
import numpy as np
from collections import namedtuple
from source.game import jogo_back as back
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

    def evaluate(self, game, oldStats):            
        stats = game.getStats()
        grade = 0
        if game.isLost():
            grade = -sys.float_info.max
        else:
            grade = -10 * (stats.plantsKilled - oldStats.plantsKilled) +\
                    10 * (stats.zombiesKilled - oldStats.zombiesKilled) +\
                    (stats.givenDamage - oldStats.givenDamage)
        return grade

    def simulate(self):
        game_copy = copy.deepcopy(self.getGame())
        stats = self.getGame().getStats()

        while game_copy.isRunning():
            game_copy.updateUntilNewSun()
            sunValue = game_copy.getSunValue()
            plantToPlace = const.SUNFLOWER

            if len(self.getGame().getPlantsList()) < \
                        self.getGame().getMap().getWidth() * \
                        self.getGame().getMap().getHeight():
                while plantToPlace != None:
                    plantToPlace = None
                    for i, cost in enumerate(aux.plant_sun_list):
                        if cost < sunValue and random.uniform(0,1) < 0.5 and \
                                not self.getGame().isPlantFrozen(i):
                            plantToPlace = aux.plant_name_list[i]
                            break
                    if random.uniform(0,1) < 0.5: #increasing do nothing probability
                        plantToPlace = None

                    if plantToPlace is not None:
                        for i in range(self.getGame().getMap().getWidth()):
                            for j in range(self.getGame().getMap().getHeight()):
                                if self.getGame().isThereAPlant(i,j) == 0 \
                                        and random.uniform(0,1) < 0.5:
                                    game_copy.addPlant(plantToPlace, i,j)
        return self.evaluate(game_copy, stats)

    def expand(self):
        game = self.getGame()
        sunValue = game.getSunValue()
        availablePlants = []

        for i, cost in enumerate(aux.plant_sun_list):
            if cost < sunValue and random.uniform(0,1) < 0.5 and\
                    not game.isPlantFrozen(i):
                availablePlants.append(aux.plant_name_list[i])
        
        possibleMoves = []
        for plant in availablePlants:
            for i in range(self.getGame().getMap().getWidth()):
                for j in range(self.getGame().getMap().getHeight()):
                    if not game.isThereAPlant(i, j):
                        cop = copy.deepcopy(game)
                        cop.addPlant(plant, i, j)
                        possibleMoves.append(AITree(cop, move=Move(plant, i, j), p=self))
        possibleMoves.append(AITree(copy.deepcopy(game), p=self))
        return possibleMoves

def doNextMovement(game, complexity):
    tree = AITree(game)
    for i in range(complexity):
        tree = mcts.MCTS(tree)

    #move = max(tree.children, key= lambda x:x.score).getMove()
    move = tree.get_best_child_by_visits().getMove()

    if move is not None:
        game.addPlant(move.plant, move.x, move.y)

    return tree