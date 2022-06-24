from time import time

import pyxel as px

from constants import (
    WIDTH,
    HEIGHT,
    CHAN_FIRE,
    CHAN_DESTROY,
    WHITE,
    CYAN,
    BLACK,
    PURPLE,
    BLUE,
    YELLOW,
)
from vector import Vector as v2
from base import Image, Sprite, Entity, Updatable, Drawable, Layer
from bullets import Bullet
from gfx import HitEffect, HitFlash, BigExplosion
from utils import Delay


class Ship(Sprite, Updatable, Drawable):

    shield_colors = {0: WHITE, 1: CYAN, 2: PURPLE}
    STARTING_POS = v2(WIDTH / 2, HEIGHT - 8)

    def __init__(self, pos=STARTING_POS):
        image = Image(0, 0, 9, 7)
        super().__init__(pos, image)
        self.shield = False
        self.shield_start = 0
        self.shield_duration = self.shield_remaining = 3
        self.vec_bounce = v2(-2, 0)
        self.speed = 80
        self.acc = 0
        self.vel = 0
        self.last_time_shoot = time()
        self.alive = True

    def activate(self):
        # Activation of the ship at the beginning of a game
        self.pos = self.STARTING_POS
        self.alive = True
        self.set_draw_layer(Layer.main)
        self.start_update()

    def deactivate(self):
        # Deactivation of the ship after winning or loosing
        self.stop_update()
        self.stop_draw()

    def protect(self):
        self.shield = True
        self.shield_start = time()

    def exiting(self, dt):
        self.vel += self.acc
        self.pos += self.vel * dt

    def hit(self):
        HitEffect(self.pos)
        px.play(CHAN_DESTROY, 4)

    def destroy(self):
        self.deactivate()
        hit_pos = self.pos
        HitEffect(hit_pos, color=YELLOW)
        Delay(lambda: HitFlash(hit_pos, color=YELLOW), delay=1.25)
        Delay(lambda: BigExplosion(hit_pos), delay=1.25)

    def update(self, dt, t):
        # Move directions
        dir_x = dir_y = 0
        if px.btnp(px.KEY_LEFT, 1, 1):
            dir_x = -1
        elif px.btnp(px.KEY_RIGHT, 1, 1):
            dir_x = 1
        if px.btnp(px.KEY_UP, 1, 1):
            dir_y = -1
        elif px.btnp(px.KEY_DOWN, 1, 1):
            dir_y = 1
        # Fire
        if px.btnp(px.KEY_X, 1, 1):
            if t >= self.last_time_shoot + 0.15:
                Bullet(self.pos)
                px.play(CHAN_FIRE, 0)
                self.last_time_shoot = t

        # Normal move
        if dir_x != 0 or dir_y != 0:
            self.vel = v2(dir_x, dir_y).normalize() * self.speed
            self.pos += self.vel * dt
            self.pos = self.pos.clamp(v2(4, 4), v2(WIDTH - 4, HEIGHT - 4))

        # Protection
        if self.shield:
            self.shield_remaining = t - self.shield_start
            if self.shield_remaining >= self.shield_duration:
                self.shield = False

    def draw(self):
        super().draw()
        if self.shield:
            # shield
            pos = self.pos + v2(-0.5, -0.5) + Entity.offset
            phase = int(time() * 10 % 3)
            px.circb(*pos, self.radius + 2 + phase, Ship.shield_colors[phase])
            # remaining countdown
            pos = pos + v2(0, -(self.radius + 10))
            remaining = str(int(self.shield_duration - self.shield_remaining + 1))
            px.text(*pos, remaining, WHITE)
