import random
import pygame as pg
from ... import tool
from ... import constants as c

class Cars():
    def __init__ (self):
        return

class Bullet():
    def __init__ (self):
        return

class Plant():
    def __init__ (self, x, y, name, health, bullet_group=None):
        self.name = name
        self.health = health
        self.state = c.IDLE
        self.bullet_group = bullet_group
        self.can_sleep = False
        self.hit_timer= 0
        self.current_time = 0

        # x, y sao os indices do mapa
        self.x = x
        self.y = y

    def update(self, current_time):
        self.current_time = current_time
        return self.action()

    def action(self):
        pass

    def setAttack(self):
        self.state = c.ATTACK

    def setIdle(self):
        self.state = c.IDLE

    def setSleep(self):
        self.state = c.SLEEP

class SunFlower(Plant):
    def __init__ (self, x, y):
        Plant.__init__(self, x, y, c.SUNFLOWER, c.PLANT_HEALTH)
        self.sun_timer = 0
    
    def action(self):
        if self.sun_timer == 0:
            self.sun_timer = self.current_time - (c.FLOWER_SUN_INTERVAL - 6000)
        elif (self.current_time - self.sun_timer) > c.FLOWER_SUN_INTERVAL:
            self.sun_timer = self.current_time
            return 1
        return 0


class PeaShooter(Plant):
    def __init__ (self):
        return

class WallNut(Plant):
    def __init__ (self):
        return

class CherryBomb(Plant):
    def __init__ (self):
        return

class PotatoMine(Plant):
    def __init__ (self):
        return

