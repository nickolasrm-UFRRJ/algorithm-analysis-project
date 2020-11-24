
SHOW_MAP = "show map"
JOGADA = "jogada"
PAUSE = "pause"
GAME_LOOP = "game loop"
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


IS_FROZEN = 0
IS_ACTIVE = 1


SUNFLOWER = 'SunFlower'
PEASHOOTER = 'Peashooter'
SNOWPEASHOOTER = 'SnowPea'
WALLNUT = 'WallNut'
CHERRYBOMB = 'CherryBomb'
THREEPEASHOOTER = 'Threepeater'
REPEATERPEA = 'RepeaterPea'
CHOMPER = 'Chomper'
CHERRY_BOOM_IMAGE = 'Boom'
PUFFSHROOM = 'PuffShroom'
POTATOMINE = 'PotatoMine'
SQUASH = 'Squash'
SPIKEWEED = 'Spikeweed'
JALAPENO = 'Jalapeno'
SCAREDYSHROOM = 'ScaredyShroom'
SUNSHROOM = 'SunShroom'
ICESHROOM = 'IceShroom'
HYPNOSHROOM = 'HypnoShroom'
WALLNUTBOWLING = 'WallNutBowling'
REDWALLNUTBOWLING = 'RedWallNutBowling'

PLANT_HEALTH = 5
WALLNUT_HEALTH = 30

ZOMBIE_ATTACK_TIMER = 60
ZOMBIE_WALK_TIMER = 4

plant_name_list = [SUNFLOWER, PEASHOOTER, WALLNUT,
                   CHERRYBOMB, POTATOMINE]
plant_sun_list = [50, 100, 50, 150, 25]
plant_frozen_time_list = [450, 450, 1800, 3000, 1800]
all_card_list = [0, 1, 2, 3, 4]

def timeToFrame(m_seconds):
    return (int(m_seconds/1000)*60)