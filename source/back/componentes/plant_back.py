import random
from ... import constants as c
from .. import auxiliar as a

class Cars():
    def __init__ (self):
        return

class Bullet():
    def __init__ (self, y, damage, start_x):
        self.name = "bullet"
        self.y_pos = y
        self.damage = damage
        self.speed = 4
        self.x_pos = start_x
    
    def update(self):
        self.x_pos += self.speed

class Plant():
    def __init__ (self, x, y, name, health, bullet_group=None):
        self.name = name
        self.health = health
        self.current_time = 0
        self.state = 0

        # x, y sao os indices do mapa
        self.x = x
        self.y = y

    def update(self):
        pass


class SunFlower(Plant):
    def __init__ (self, x, y):
        Plant.__init__(self, x, y, c.SUNFLOWER, c.PLANT_HEALTH)
        self.sun_timer = -a.SUNFLOWER_1CHARGE
    
    def producedSun(self):
        if self.sun_timer % a.SUNFLOWER_TIMER == 0:
            if self.sun_timer == 0:
                return 25
            else:
                result = 25 * int(self.sun_timer / a.SUNFLOWER_TIMER)
                print("Aumentou " + str(result))
                self.sun_timer = 0
                return result
        return 0

    def update(self):
        self.sun_timer += 1
        return self.producedSun()


class PeaShooter(Plant):
    def __init__ (self, x, y):
        Plant.__init__(self, x, y, c.PEASHOOTER, c.PLANT_HEALTH)
        self.hit_timer = -1

    def attack(self):
        if self.hit_timer % a.PEASHOOTER_TIMER == 0:
            self.hit_timer = 0
            centerx = ( ((self.x+1) * c.GRID_X_SIZE) - (c.GRID_X_SIZE/2) )
            return Bullet(self.y, c.BULLET_DAMAGE_NORMAL, centerx)
        return None

    def update(self):
        self.hit_timer += 1
        return self.attack()

class WallNut(Plant):
    def __init__ (self, x, y):
        Plant.__init__(self, x, y, c.WALLNUT, c.WALLNUT_HEALTH)
        return

class CherryBomb(Plant):
    def __init__ (self,x , y):
        Plant.__init__(self, x, y, c.CHERRYBOMB, c.PLANT_HEALTH)
        self.explode_x_range = int(c.GRID_X_SIZE)
        self.explode_y_range = 1
        return

class PotatoMine(Plant):
    def __init__ (self, x, y):
        Plant.__init__(self, x, y, c.POTATOMINE, c.PLANT_HEALTH)
        self.init_timer = 0
        self.explode_x_range = int(c.GRID_X_SIZE//3 * 2)+10
        self.explode_y_range = 0
        self.is_init = False

    def update(self):
        if self.is_init == False:
            self.init_timer += 1
            if self.init_timer > 900:
                self.is_init = True

