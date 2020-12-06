from .jogo_back import JogoBack
import numpy.random as r
from ... import constants as c
from . import auxiliar as a
from .mcts import *
import copy

class IA():
    def __init__(self):
        self.game = JogoBack()
        self.game.initJogo()
    
    def runGame(self):
        self.game.main()
    

    def testingSimulate(self):
        game_copy = copy.deepcopy(self.game)
        game_copy.showState()
        self.simulation(game_copy)

    def simulation(self, game_copy):
        print(game_copy.sun_timer)
        while game_copy.rodando:
            #do random move if possible and increase sun
            moves = [None]
            if not game_copy.m.isFull():
                for i in range(5):
                    if a.plant_sun_list[i] <= game_copy.sun_value and game_copy.freezing[i] <= 0:
                        moves.append(a.plant_name_list[i])

                print("LIST OF MOVES: " + str(moves))
                if len(moves) > 1:
                    random_move = r.randint(len(moves))
                    if moves[random_move] == c.SUNFLOWER:
                        rand_y = r.randint(5)
                        x = game_copy.m.getFirstLeftFree(rand_y)
                        while not game_copy.m.isEmpty(x, rand_y):
                            rand_y = r.randint(5)
                            x = game_copy.m.getFirstLeftFree(rand_y)
                        game_copy.sun_value -= a.plant_sun_list[0]
                        game_copy.freezing[0] = a.plant_frozen_time_list[0]
                        game_copy.addPlant(c.SUNFLOWER, x, rand_y)
                        game_copy.sortPlants()

                    elif moves[random_move] == c.PEASHOOTER:
                        rand_y = r.randint(5)
                        rand_x = r.randint(9)
                        while not game_copy.m.isEmpty(rand_x, rand_y):
                            rand_y = r.randint(5)
                            rand_x = r.randint(9)
                        game_copy.sun_value -= a.plant_sun_list[1]
                        game_copy.freezing[1] = a.plant_frozen_time_list[1]
                        game_copy.addPlant(c.PEASHOOTER, rand_x, rand_y)
                        game_copy.sortPlants()
                    elif moves[random_move] == c.WALLNUT:
                        rand_y = r.randint(5)
                        rand_x = r.randint(9)
                        while not game_copy.m.isEmpty(rand_x, rand_y):
                            rand_y = r.randint(5)
                            rand_x = r.randint(9)
                        game_copy.sun_value -= a.plant_sun_list[2]
                        game_copy.freezing[2] = a.plant_frozen_time_list[2]
                        game_copy.addPlant(c.WALLNUT, rand_x, rand_y)
                        game_copy.sortPlants()
                        
                    elif moves[random_move] == c.CHERRYBOMB:
                        rand_y = r.randint(5)
                        rand_x = r.randint(9)
                        while not game_copy.m.isEmpty(rand_x, rand_y):
                            rand_y = r.randint(5)
                            rand_x = r.randint(9)
                        game_copy.sun_value -= a.plant_sun_list[3]
                        game_copy.freezing[3] = a.plant_frozen_time_list[3]
                        game_copy.addPlant(c.CHERRYBOMB, rand_x, rand_y)
                        game_copy.sortPlants()

                    elif moves[random_move] == c.POTATOMINE:
                        rand_y = r.randint(5)
                        rand_x = r.randint(9)
                        while not game_copy.m.isEmpty(rand_x, rand_y):
                            rand_y = r.randint(5)
                            rand_x = r.randint(9)
                        game_copy.sun_value -= a.plant_sun_list[4]
                        game_copy.freezing[4] = a.plant_frozen_time_list[4]
                        game_copy.addPlant(c.POTATOMINE, rand_x, rand_y)
                        game_copy.sortPlants()
                        
            game_copy.updateFrame( (a.SUN_TIMER - int(game_copy.sun_timer % a.SUN_TIMER) ) )
            game_copy.showState()
