from time import time
import random
import math

import pyxel as px

from vector import Vector as v2
from utils import center_txt

from gfx import Particle
from base import Image, Sprite, ASprite, Entity
from constants import (
    WIDTH,
    HEIGHT,
    BLUE,
    PURPLE,
    BROWN,
    BLACK,
    WHITE,
    LIGHT_GREY,
    GREY,
    RED,
    GREEN,
    CYAN,
)
from scores import ScoresHandler


GRAD1 = HEIGHT - 42  # BLUE
GRAD2 = HEIGHT - 31  # PURPLE
GRAD3 = HEIGHT - 4  # BROWN


class BigStar(ASprite):
    def __init__(self, pos, freq=0.5):
        super().__init__(pos, [Image(44, 16, 11, 11), Image(56, 16, 7, 11)], freq)


class Star:
    def __init__(self, pos):
        self.pos = pos
        self.set_color()

    def set_color(self):
        if self.pos.y < GRAD1:
            self.color = GREY
        elif self.pos.y < GRAD2:
            self.color = PURPLE
        elif self.pos.y < GRAD3:
            self.color = BROWN
        else:
            self.color = LIGHT_GREY

    def draw(self):
        pos = self.pos + Entity.offset
        # px.pix(*pos, self.color)
        px.pset(*pos, self.color)


class PulseStar(ASprite):
    def __init__(self, pos, freq=0.5):
        super().__init__(pos, [Image(64, 16, 3, 3), Image(68, 16, 3, 3)], freq)
        self.set_frames()

    def set_frames(self):
        if self.pos.y < GRAD2:
            self.frames = [Image(64, 16, 3, 3), Image(68, 16, 3, 3)]
        else:
            self.frames = [Image(64, 20, 3, 3), Image(68, 20, 3, 3)]


class ShootingStar:
    def __init__(self, pos):
        self.pos = pos
        y = random.uniform(-1, -4)
        self.dir = v2(3, y).normalize()
        self.duration = 0.8
        self.speed = 90
        self.vel = self.dir * self.speed
        self.particles = []

    def add_particle(self, pos):
        pos = pos
        vel = v2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize() * 3
        acc = v2()

        self.particles.append(Particle(pos, 1, vel, acc, self.duration, WHITE))

    def is_out(self):
        margin = WIDTH
        if self.pos.x > WIDTH + margin or self.pos.y < -margin:
            return True
        return False

    def update(self, dt, t):
        self.pos += self.vel * dt
        if len(self.particles) < 150:
            for _ in range(3):
                self.add_particle(self.pos)

        for p in self.particles:
            p.update(dt)
            if p.pos.y < GRAD1:
                p.color = BLUE
            elif p.pos.y < GRAD2:
                p.color = PURPLE
            elif p.pos.y < GRAD3:
                p.color = BROWN
            else:
                p.color = LIGHT_GREY

            if p.is_dead:
                self.particles.remove(p)
                del p

    def draw(self):
        for p in self.particles:
            p.draw()
        pos = self.pos + Entity.offset
        # px.pix(*pos, WHITE)
        px.pset(*pos, WHITE)


class RewardAnim:
    def __init__(self):
        self.planet = Sprite(v2(WIDTH * 3 / 10, HEIGHT - 47), Image(195, 39, 61, 61))
        mfw = 37  # moon front width
        self.moon_front = Sprite(v2(-mfw / 2, HEIGHT - 40), Image(218, 0, mfw, mfw))
        mbw = 16  # moon back width
        self.moon_back = Sprite(
            v2(WIDTH + mbw / 2, HEIGHT - 45), Image(200, 0, mbw, mbw)
        )
        self.big_stars = [
            BigStar(v2(WIDTH * 7 / 80, HEIGHT * 1 / 2), freq=0.05),
            BigStar(v2(WIDTH * 19 / 20, HEIGHT * 3 / 20), freq=0.075),
            BigStar(v2(WIDTH * 17 / 32, HEIGHT * 37 / 60), freq=0.5),
            PulseStar(v2(WIDTH * 17 / 32, HEIGHT * 19 / 40), freq=0.075),
            PulseStar(v2(WIDTH * 149 / 160, HEIGHT * 17 / 20), freq=0.075),
            PulseStar(v2(WIDTH * 1 / 10, HEIGHT * 47 / 60), freq=0.075),
            PulseStar(v2(WIDTH * 41 / 80, HEIGHT * 2 / 15), freq=0.075),
            PulseStar(v2(WIDTH * 41 / 80, HEIGHT * 3 / 20), freq=0.075),
            BigStar(v2(WIDTH * 39 / 160, HEIGHT * 11 / 40), freq=0.045),
            PulseStar(v2(WIDTH * 11 / 16, HEIGHT * 13 / 30), freq=0.045),
            PulseStar(v2(WIDTH * 79 / 80, HEIGHT * 23 / 120), freq=0.045),
        ]
        self.stars = [
            Star(v2(WIDTH * 1 / 20, HEIGHT * 71 / 120)),
            Star(v2(WIDTH * 1 / 32, HEIGHT * 11 / 20)),
            Star(v2(WIDTH * 1 / 16, HEIGHT * 83 / 120)),
            Star(v2(WIDTH * 9 / 80, HEIGHT * 31 / 40)),
            Star(v2(WIDTH * 1 / 10, HEIGHT * 91 / 120)),
            Star(v2(WIDTH * 3 / 40, HEIGHT * 17 / 20)),
            Star(v2(WIDTH * 37 / 80, HEIGHT * 39 / 40)),
            Star(v2(WIDTH * 71 / 160, HEIGHT * 19 / 20)),
            Star(v2(WIDTH * 73 / 160, HEIGHT * 37 / 40)),
            Star(v2(WIDTH * 7 / 16, HEIGHT * 14 / 15)),
            Star(v2(WIDTH * 2 / 5, HEIGHT * 107 / 120)),
            Star(v2(WIDTH * 9 / 20, HEIGHT * 49 / 60)),
            Star(v2(WIDTH * 1 / 2, HEIGHT * 11 / 24)),
            Star(v2(WIDTH * 19 / 20, HEIGHT * 29 / 60)),
            Star(v2(WIDTH * 39 / 40, HEIGHT * 3 / 8)),
            Star(v2(WIDTH * 77 / 80, HEIGHT * 47 / 120)),
            Star(v2(WIDTH * 19 / 20, HEIGHT * 1 / 3)),
            Star(v2(WIDTH * 27 / 32, HEIGHT * 17 / 40)),
            Star(v2(WIDTH * 143 / 160, HEIGHT * 5 / 8)),
            Star(v2(WIDTH * 151 / 160, HEIGHT * 27 / 40)),
            Star(v2(WIDTH * 149 / 160, HEIGHT * 41 / 60)),
            Star(v2(WIDTH * 153 / 160, HEIGHT * 91 / 120)),
            Star(v2(WIDTH * 29 / 32, HEIGHT * 107 / 120)),
            Star(v2(WIDTH * 1 / 20, HEIGHT * 17 / 24)),
            Star(v2(WIDTH * 1 / 32, HEIGHT * 29 / 30)),
            Star(v2(WIDTH * 1 / 20, HEIGHT * 19 / 20)),
            Star(v2(WIDTH * 7 / 160, HEIGHT * 113 / 120)),
            Star(v2(WIDTH * 3 / 32, HEIGHT * 109 / 120)),
            Star(v2(WIDTH * 1 / 20, HEIGHT * 13 / 15)),
            Star(v2(WIDTH * 1 / 20, HEIGHT * 101 / 120)),
            Star(v2(WIDTH * 7 / 32, HEIGHT * 103 / 120)),
            Star(v2(WIDTH * 91 / 160, HEIGHT * 91 / 120)),
            Star(v2(WIDTH * 21 / 32, HEIGHT * 41 / 60)),
            Star(v2(WIDTH * 123 / 160, HEIGHT * 103 / 120)),
            Star(v2(WIDTH * 111 / 160, HEIGHT * 49 / 120)),
            Star(v2(WIDTH * 113 / 160, HEIGHT * 17 / 40)),
            Star(v2(WIDTH * 19 / 32, HEIGHT * 1 / 6)),
            Star(v2(WIDTH * 93 / 160, HEIGHT * 17 / 120)),
            Star(v2(WIDTH * 89 / 160, HEIGHT * 9 / 20)),
            Star(v2(WIDTH * 99 / 160, HEIGHT * 17 / 40)),
            Star(v2(WIDTH * 1 / 2, HEIGHT * 31 / 60)),
            Star(v2(WIDTH * 153 / 160, HEIGHT * 17 / 60)),
            Star(v2(WIDTH * 79 / 80, HEIGHT * 9 / 40)),
            Star(v2(WIDTH * 31 / 32, HEIGHT * 13 / 60)),
            Star(v2(WIDTH * 29 / 32, HEIGHT * 21 / 40)),
        ]
        self.shooting_stars = []
        self.last_shooting = 0
        self.birth = 0
        self.t = 0.5

    def start(self):
        self.birth = time()

    def destroy(self):
        del self

    def update(self, dt, t):

        time_since_birth = t - self.birth

        # Shooting stars
        if t - self.last_shooting >= 3:
            posx = random.uniform(-WIDTH / 2, WIDTH / 2)
            self.shooting_stars.append(ShootingStar(v2(posx, HEIGHT + 5)))
            self.last_shooting = t
        for star in self.shooting_stars:
            star.update(dt, t)
            if star.is_out():
                self.shooting_stars.remove(star)
                del star

        # stars
        for star in self.big_stars:
            star.update(dt, t)

        # Moon
        phase = int(time_since_birth % 32)
        vel_mf = v2()
        vel_mb = v2()

        if phase < 8:
            vel_mf = v2((WIDTH + self.moon_front.img.w) / 8, 0)
        elif phase >= 8 and phase < 12:
            self.moon_front.pos.x = 0 - self.moon_front.img.w / 2
        elif phase >= 12 and phase < 28:
            vel_mb = v2(-(WIDTH + self.moon_back.img.w) / 16, 0)
        else:
            self.moon_back.pos.x = WIDTH + self.moon_back.img.w / 2

        self.moon_back.pos += vel_mb * dt
        self.moon_front.pos += vel_mf * dt

    def draw(self):

        # Background gradient
        p1 = v2(0, GRAD1) + Entity.offset
        p2 = v2(WIDTH, GRAD2) + Entity.offset
        px.rect(*p1, *p2, BLUE)
        p1 = v2(0, GRAD2) + Entity.offset
        p2 = v2(WIDTH, GRAD3) + Entity.offset
        px.rect(*p1, *p2, PURPLE)
        p1 = v2(0, GRAD3) + Entity.offset
        p2 = v2(WIDTH, HEIGHT) + Entity.offset
        px.rect(*p1, *p2, BROWN)

        # Shooting stars
        for star in self.shooting_stars:
            star.draw()

        # Title
        p = v2(WIDTH * 3 / 80, HEIGHT * 1 / 20) + Entity.offset
        px.blt(*p, 0, 0, 32, 84, 40, colkey=BLACK)

        # stars
        for star in self.big_stars:
            star.draw()
        for star in self.stars:
            star.draw()

        # Planet
        self.moon_back.draw()
        self.planet.draw()

        # Congratulations
        for n, c in enumerate("CONGRATULATIONS"):
            px.text(
                18 + n * 4,
                88 + math.sin(time() * 4 + n * self.t) * 3 + Entity.offset.y,
                c,
                CYAN,
            )

        # Texts
        lines = [
            f"You defeated",
            f"the ennemies",
            f"     ...    ",
            f"All humanity",
            f"will remember",
            f"you as one of",
            f"the bravest.",
        ]
        posx = WIDTH * 3 / 5

        y = HEIGHT * 1 / 20
        for n, l in enumerate(lines):
            posy = y + n * 6
            p = v2(posx, posy) + Entity.offset
            px.text(*p, l, LIGHT_GREY)

        p = v2(posx, HEIGHT * 29 / 60) + Entity.offset
        ScoresHandler.draw(p, for_end=True)

        # Planet front
        self.moon_front.draw()
