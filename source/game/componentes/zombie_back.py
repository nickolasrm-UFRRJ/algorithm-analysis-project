import random
import math
from source.game.componentes import constants as c
from source.game.componentes import auxiliar as a
from source.game.componentes import plant_back

class Zombie():
    def __init__(self, name, x, map_y, health, damage=1):
        self.name = name
        self.y = map_y
        self.x = x
        self.health = health
        self.damage = damage
        self.speed = 1
        self.attack_timer = 0
        self.walk_timer = 0
        self.state = c.WALK

    def getDamage(self):
        return self.damage

    def update(self, plant=None):
        if self.state == c.WALK:
            self.walk()
        elif self.state == c.ATTACK:
            return self.attack(plant)

    def walk(self, frames = 1):
        if frames == 1:
            self.walk_timer += 1
            if self.walk_timer >= a.ZOMBIE_WALK_TIMER:
                # print("WALKING!")
                self.x -= self.speed
                self.walk_timer = 0
        else:
            self.walk_timer += frames
            self.x -= math.floor(self.walk_timer / a.ZOMBIE_WALK_TIMER) * self.speed
            self.walk_timer = self.walk_timer % a.ZOMBIE_WALK_TIMER

    def attack(self, plant):
        if plant != None:
            self.attack_timer += 1
            if self.attack_timer >= a.ZOMBIE_ATTACK_TIMER:
                # print("ATTACKING")
                plant.receiveDamage(self.damage)
                self.attack_timer = 0
                return plant.health