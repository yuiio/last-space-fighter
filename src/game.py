import pyxel as px
from time import time

from constants import WIDTH, HEIGHT

from army import Army
from ship import Ship
from enemies import Enemy
from bullets import EnBullet
from gfx import ParticleStarField
from gamestates import GameStateIntro, GameStateStart, GameStateVictory


class Game:
    def __init__(self):

        self.score = 0
        self.lives = 3
        self.ship = Ship()
        self.star_field = ParticleStarField()

        self.won_game = False
        self.army = Army()

        self.state = GameStateIntro(self)
        # self.state = GameStateVictory(self)

    def start(self):
        self.ship.activate()
        self.score = 0
        self.lives = 3
        self.army.start_war()
        self.time_start = time()
        self.time_spawn = self.time_start

    def spawn(self, t):
        time_past = t - self.time_spawn
        if self.army.delay is None:
            if not len(Enemy.enemies):
                self.army.get_troop()
                self.time_spawn = t
        elif time_past >= self.army.delay:
            soldier = self.army.get_soldier()
            if hasattr(soldier, "target"):
                soldier.set_target(self.ship)
            self.time_spawn = t
