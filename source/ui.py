from source.game import jogo_back as back
from source.game.componentes import constants as const
from source.game.componentes import plant_back as Plant
import math
import emoji

def menu():
    print(emoji.emojize(":sunflower: Bem vindo ao Plants vs Zombies AI :zombie:"))
    print('Nesta aplicação utilizamos o algoritmo de busca \nem árvore Monte Carlo para',
          'a IA decidir qual \nserá o melhor movimento no jogo!')
    print('-----------------------------------------')
    complexidade = input('Primeiro, informe o nível de esperteza da IA, \n' +\
        'isto significa a quantidade expansões feita \npelo algoritmo (5 é um bom nivel): ')
    print('-----------------------------------------')
    nivel = input('Agora informe qual fase você \nquer testar, de 1 a 5: ')
    return (int(complexidade), int(nivel))


def getSunEmoji():
    return emoji.emojize(':sun:')

def getZombieEmoji():
    return emoji.emojize(':zombie:')

def getCarEmoji():
    return emoji.emojize(':tractor:')

def getPlantEmoji(plant):
    out = '  '
    if isinstance(plant, Plant.SunFlower):
        out = ':sunflower:'
    elif isinstance(plant, Plant.PeaShooter):
        out = ':peanuts:'
    elif isinstance(plant, Plant.PotatoMine):
        out = ':potato:'
    elif isinstance(plant, Plant.WallNut):
        out = ':coconut:'
    return emoji.emojize(out)


def printGame(game):
    map = [['  ' for i in range(const.GRID_X_LEN)] \
        for j in range(const.GRID_Y_LEN)]
    for plantRow in game.getPlantsList():
        for plant in plantRow:
            map[plant.y][plant.x] = getPlantEmoji(plant)
    for zombieRow in game.getZombiesAliveList():
        for zombie in zombieRow:
            xPos = math.floor(zombie.x / 80)
            if xPos < 9 and xPos > -1:
                if game.isThereAPlant(game.getMap().getZombieXPosInMap(zombie), zombie.y):
                    if xPos+1 < 9:
                        map[zombie.y][xPos+1] = getZombieEmoji()
                else:
                    map[zombie.y][xPos] = getZombieEmoji()
    print('-----------------------------------------')
    print(getSunEmoji(), "Sun: ", game.getSunValue())
    print('-----------------------------------------')
    for i, row in enumerate(map):
        if game.cars[i] == 1:
            print(getCarEmoji(),' |', end='')
        else:
            print('    |', end='')
        for block in row:
            print(block, '|', end='')
        print('')