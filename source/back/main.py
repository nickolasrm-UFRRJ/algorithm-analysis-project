import sys
import os
import json
from .source import jogo_back
from .. import constants as c
from .source.ia import IA
from .source import auxiliar as  a


def main():
    print(a.FLIP_STATE)
    print(a.TYPE_GAME)
    opcao = input()
    while opcao < '0' and opcao > '3':
        print(a.FLIP_STATE)
        print(a.TYPE_GAME)
        opcao = input()
    opcao = int(opcao)
    if opcao == 0:
        pass
    elif opcao == 1:
        game = jogo_back.JogoBack()
        game.main()
    elif opcao == 2:
        ia = IA()
        ia.runGame()
    elif opcao == 3:
        ia = IA()
        ia.testingSimulate()

