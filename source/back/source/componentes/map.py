import os
import json
from .... import constants as c

class Map():
    def __init__(self, x, y):
        self.larg = x
        self.alt = y
        self.larg_cell = c.GRID_X_SIZE
        self.alt_cell = c.GRID_Y_SIZE
        self.map = [[0 for x in range(self.larg)] for y in range(self.alt)]
        self.loadMap()

    def loadMap(self):
        map_file = 'level_' + str(0) + '.json'
        file_path = os.path.join('source', 'back', 'source' , 'data', 'map', map_file)
        f = open(file_path)
        self.map_data = json.load(f)
        f.close()

    # Isso sera usando para retornar a posicao da planta no mapa para ver colisao
    def realXPos(self, x_index):
        return c.GRID_X_SIZE * (x_index+1)

    def isEmpty(self, x, y):
        if self.map[y][x] == 0:
            return True
        return False

    def getFirstLeftFree(self, y):
        counter = 0
        while not self.isEmpty(counter, y) and counter < 9:
            counter+=1
        return counter
    
    def isFull(self):
        for i in range(5):
            for j in range(9):
                if self.isEmpty(j, i):
                    return 0
        return 1