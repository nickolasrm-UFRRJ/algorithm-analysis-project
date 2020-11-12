import sys
import os
import json
import pygame as pg
from . import jogo_back
from .componentes import plant_back as plants
from .componentes import zombie_back as zombie
from .componentes import map 
from .. import constants as c


def main():
    game = jogo_back.JogoBack()
    game.main()

if __name__=='__main__':
   main()