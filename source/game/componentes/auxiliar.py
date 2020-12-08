PLANTS_NUMBER = 5

SHOW_MAP = "show map"
JOGADA = "jogada"
PAUSE = "pause"
GAME_LOOP = "game loop"
SIMULATION = "simulation"
EVENT_HANDLE = "tratando eventos"

QUIT = "Kitou troxa"

FLIP_STATE = "\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
BREAK_LINE = "\n\n"

SUN_TIMER = 420
SUNFLOWER_TIMER = 1320
SUNFLOWER_1CHARGE = 360
PEASHOOTER_TIMER = 120

PLAY = "Iserir Planta:\n1 - Sunflower (50)\n2 - Peashooter (100)\n3 - Noz (50)\n4 - Cereja (150)\n5 - Batata mina (25)\n0 - Descartar inserção"

DECISAO = "DECISAO:\n1- AVANCAR PARA PROXIMO FRAME\n2- AVANCAR MAIS DE 1 FRAME\n3- AVANCAR ATE PROXIMO SOL\n4- INICIAR JOGADA\n5- SAIR DO JOGO\nESCOLHA UMA OPCAO:"
DECISAO_2 = "DIGITE A QUANTIDADE DE FRAMES PARA AVANCAR: "
TYPE_GAME = "QUAL A OPCAO DE JOGO:\n1- NORMAL GAME\n2- IA\n3- IA SIMULATION(NAO INCLUIDO)\n0- SAIR\n"


IS_FROZEN = 0
IS_ACTIVE = 1


SUNFLOWER = 'SunFlower'
PEASHOOTER = 'Peashooter'
WALLNUT = 'WallNut'
POTATOMINE = 'PotatoMine'

PLANT_HEALTH = 5
WALLNUT_HEALTH = 30

ZOMBIE_ATTACK_TIMER = 60
ZOMBIE_WALK_TIMER = 4

plant_name_list = [SUNFLOWER, PEASHOOTER, WALLNUT, POTATOMINE]
plant_sun_list = [50, 100, 50, 25]
plant_frozen_time_list = [450, 450, 1800, 1800]
all_card_list = [0, 1, 2, 3]

def timeToFrame(m_seconds):
    return (int(m_seconds/1000)*60)

PERDEU = "perdeu"
GANHOU = "ganhou"