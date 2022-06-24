from time import time
from abc import ABC, abstractmethod

import pyxel as px

from constants import BLACK
from vector import Vector as v2


class Updatable(ABC):

    updatables = []

    @abstractmethod
    def update(self, dt, t):
        pass

    def start_update(self):
        self.updatables.append(self)

    def stop_update(self):
        self.updatables.remove(self)


class Layer:
    back = []  # Starfield, Hit flash
    main = []  # Ship, Enemies
    fore = []  # Bullets, Explosions


class Drawable(ABC):
    @abstractmethod
    def draw(self):
        pass

    def set_draw_layer(self, layer: Layer):
        if hasattr(self, "layer") and self in self.layer:
            self.stop_draw()
        self.layer = layer
        self.start_draw()

    def start_draw(self):
        self.layer.append(self)

    def stop_draw(self):
        self.layer.remove(self)


class Image:
    def __init__(self, u, v, w, h, bank=0):
        self.bank = bank
        self.u = u
        self.v = v
        self.w = w
        self.h = h

    def __iter__(self):
        return (self.bank, self.u, self.v, self.w, self.h).__iter__()


class Entity:
    offset = v2(0, 0)

    def __init__(self, pos, radius=None):
        self.pos = pos
        self.center = pos
        self.radius = radius

    def collide_with(self, entity):
        # return self.pos.dist_between(entity.pos) < self.radius + entity.radius
        # Refactor without dist_between that use math.sqrt
        dist = entity.pos - self.pos
        dist_square = dist.x * dist.x + dist.y * dist.y
        return (self.radius + entity.radius) * (
            self.radius + entity.radius
        ) >= dist_square


class Sprite(Entity):
    def __init__(self, pos, img, colkey=BLACK):
        self.img = img
        self.colkey = colkey
        radius = (self.img.w + self.img.h) / 4
        super().__init__(pos, radius=radius)

    def draw(self):
        pos = self.pos - v2(self.img.w / 2, self.img.h / 2)  # pos = center of image
        pos += Entity.offset
        px.blt(*pos, *self.img, colkey=self.colkey)


class ASprite(Sprite):
    def __init__(self, pos, frames, freq, colkey=BLACK):
        self.frames = frames
        self.frame_count = 0
        self.freq = freq
        self.pt = time()
        self.img = frames[self.frame_count]
        super().__init__(pos, self.img, colkey=colkey)

    def update(self, dt, t):
        if t - self.pt >= self.freq:
            self.frame_count += 1
            self.pt = t
        if self.frame_count >= 2:  # 2 -> len(self.frames) hardcoded
            self.frame_count = 0
        self.img = self.frames[self.frame_count]
