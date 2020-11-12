import os
import json
import pygame as pg
from .. import tool
from .. import constants as c
from ..component import map, plant, zombie


class Frame():
    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura
        self.map = [[0 for x in range(self.largura)] for y in range(self.altura)]
    
    def setupGroups(self):
        self.sun_group = pg.sprite.Group()
        self.head_group = pg.sprite.Group()

        self.plant_groups = []
        self.zombie_groups = []
        self.hypno_zombie_groups = [] #zombies who are hypno after eating hypnoshroom
        self.bullet_groups = []
        for i in range(self.map_y_len):
            self.plant_groups.append(pg.sprite.Group())
            self.zombie_groups.append(pg.sprite.Group())
            self.hypno_zombie_groups.append(pg.sprite.Group())
            self.bullet_groups.append(pg.sprite.Group())
        