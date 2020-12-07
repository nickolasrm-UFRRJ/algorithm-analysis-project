from source.game import jogo_back as back
from source import ai
from source import ui
import time

complexity, level = ui.menu()

game = back.JogoBack(lvl=level)
while game.isRunning():
    ui.printGame(game)
    time.sleep(0.4)
    game.runUntilNewSun()
    out = ai.doNextMovement(game, complexity)
print('-----------------------------------------')
print('Resultado do jogo:', ('derrota' if game.isLost() is True else 'vitória'))