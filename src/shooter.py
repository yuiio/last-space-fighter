#
# Space shooter
#
# Author : yuiio@sotodesign.org

from os.path import join as path_join
from time import time

import pyxel as px

from constants import *
from game import Game


class App:
    def __init__(self):
        px.init(WIDTH, HEIGHT, title="The last space fighter", capture_sec=0)
        px.load(path_join("assets", "shooter.pyxres"))
        px.fullscreen(True)

        self.pt = time()  # Buffer previous time
        self.game = Game()
        self.paused = False

        px.mouse(SHOW_CURSOR)
        px.run(self.update, self.draw)

    def update(self):

        if px.btnp(px.KEY_Q):
            px.quit()
        if px.btnp(px.KEY_P):
            if not self.paused:
                px.stop()
            else:
                self.pt = time()
                px.playm(3, loop=True)
            self.paused = not self.paused

        if not self.paused:
            t = time()
            dt = t - self.pt
            self.pt = t

            self.game.state.update(dt, t)
            self.game.state = self.game.state.get_next_state()

    def draw(self):
        if not self.paused:
            self.game.state.draw()


App()
