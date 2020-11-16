import random
from ... import constants as c
from .. import auxiliar as a
from .plant_back import *

class Zombie():
    def __init__(self, name, map_y, health, damage):
        self.name = name
        self.y = map_y
        self.x = (c.GRID_X_LEN + 1) * c.GRID_X_SIZE
        self.health = health
        self.damage = damage
        self.speed = 1

    def update(self, state):
        if state == c.WALK:
            self.walk()

    def walk(self):

        pass

    def attack(self, plant):
        plant.health -= 1
        return plant