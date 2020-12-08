import random
from source.game.componentes import constants as c
from source.game.componentes import auxiliar as a

class Cars():
    def __init__ (self):
        return

class Plant():
    def __init__ (self, x, y, name, health, bullet_group=None):
        self.name = name
        self.health = health
        self.current_time = 0
        self.state = 0

        # x, y sao os indices do mapa
        self.x = x
        self.y = y

    def attack(self, zombie):
        pass

    def update(self):
        pass

    def receiveDamage(self, dmg):
        self.health -= dmg


class SunFlower(Plant):
    def __init__ (self, x, y):
        Plant.__init__(self, x, y, c.SUNFLOWER, c.PLANT_HEALTH)
        self.sun_timer = 0#-a.SUNFLOWER_1CHARGE
    
    def producedSun(self):
        if self.sun_timer >= a.SUNFLOWER_TIMER:
            self.sun_timer = 0
            return 25
        return 0
    #    if self.sun_timer % a.SUNFLOWER_TIMER == 0:
    #        if self.sun_timer == 0:
    #            return 25
    #        else:
    #            result = 25 * int(self.sun_timer / a.SUNFLOWER_TIMER)
    #            self.sun_timer = 0
    #            return result
    #    return 0

    def update(self, n=1):
        self.sun_timer += n
        return self.producedSun()


class PeaShooter(Plant):
    def __init__ (self, x, y):
        Plant.__init__(self, x, y, c.PEASHOOTER, c.PLANT_HEALTH)
        self.hit_timer = 0

    def attack(self, zombie):
        if self.hit_timer >= a.PEASHOOTER_TIMER:
            self.hit_timer = 0
            zombie.health -= c.BULLET_DAMAGE_NORMAL

    def update(self):
        self.hit_timer += 1

class WallNut(Plant):
    def __init__ (self, x, y):
        Plant.__init__(self, x, y, c.WALLNUT, c.WALLNUT_HEALTH)
        return

class PotatoMine(Plant):
    def __init__ (self, x, y):
        Plant.__init__(self, x, y, c.POTATOMINE, c.PLANT_HEALTH)