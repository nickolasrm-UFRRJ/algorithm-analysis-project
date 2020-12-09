from source.game import jogo_back as back
from source import ai
from source import ui
import time
import numpy as np

complexity, level = 5, 1
derrotas = 0
vitorias = 0

times = []
for i in range(10):
    st = time.time()
    game = back.JogoBack(lvl=level)
    while game.isRunning():
        game.runUntilNewSun()
        out = ai.doNextMovement(game, complexity)
    end = time.time()
    times.append(end - st)
    print(end-st)
print(np.average(times), np.std(times))