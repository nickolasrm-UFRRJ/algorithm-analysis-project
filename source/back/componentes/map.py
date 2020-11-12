import os
import json
import pygame as pg
from ... import constants as c

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
        file_path = os.path.join('source', 'back', 'data', 'map', map_file)
        f = open(file_path)
        self.map_data = json.load(f)
        f.close()

    # Isso sera usando para retornar a posicao da planta no mapa para ver colisao
    def realXPos(self, x_index):
        return c.GRID_X_SIZE * (x_index+1)