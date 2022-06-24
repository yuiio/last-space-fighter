from random import uniform, randint
from time import time

import pyxel as px

from constants import *
from vector import Vector as v2
from base import Entity, Updatable, Drawable, Layer


class Background:
    color = BLACK


class Shaker(Updatable):
    """class to shake the screen"""

    def __init__(self, amount=2, duration=0.15):
        self.start_update()
        self.amount = amount
        self.duration = duration
        self.birth = time()

    def update(self, dt, t):
        if t - self.birth < self.duration:
            Entity.offset = v2(
                uniform(-1, 1) * self.amount, uniform(-1, 1) * self.amount
            )
        else:
            Entity.offset = v2(0, 0)
            self.stop_update()


class Particle(Entity):

    sizes = {1: v2(0, 0), 2: v2(0, 1), 3: v2(1, 1)}

    def __init__(self, pos, size, vel, acc, duration, color):
        super().__init__(pos, radius=size)
        self.vel = vel
        self.acc = acc
        self.lifespan = self.duration = duration
        self.color = color

    @property
    def is_dead(self):
        return True if self.lifespan <= 0 else False

    def update(self, dt):
        self.lifespan -= dt
        self.vel += self.acc
        self.pos += self.vel * dt

    def draw(self):
        pos = self.pos + Entity.offset
        # dim = pos + Particle.sizes[self.radius]
        dim = Particle.sizes[self.radius]
        px.rect(*pos, *dim, self.color)


class ParticleStarField(Updatable, Drawable):

    color = BLUE

    def __init__(self):

        self.start_update()
        self.set_draw_layer(Layer.back)
        self.particles = []
        self.never_ending = True

        for _ in range(50):
            self.add_particle()

    def stop(self):
        acc = v2(0, -4)
        for p in self.particles:
            p.acc = acc
        self.never_ending = False

    def start(self):
        self.particles.clear()
        self.never_ending = True
        for _ in range(50):
            self.add_particle()

    def remove(self):
        self.stop_draw()
        self.stop_update()

    def _add_particle(self, pos):
        size = randint(1, 3)
        pos = pos
        vel = v2(0, randint(100, 200))
        acc = v2()

        self.particles.append(Particle(pos, size, vel, acc, 2, self.color))

    def add_particle(self):
        pos = v2(randint(0, WIDTH), randint(0, HEIGHT))
        self._add_particle(pos)

    def add_top_particle(self):
        pos = v2(randint(0, WIDTH), -3)
        self._add_particle(pos)

    def p_is_dead(self, p):
        return True if p.pos.y > HEIGHT + 3 or p.pos.y < -3 else False

    def update(self, dt, t):
        if len(self.particles):
            for p in self.particles.copy():
                p.update(dt)
                p.color = self.color
                if self.p_is_dead(p):
                    self.particles.remove(p)
                    del p
                    if self.never_ending:
                        self.add_top_particle()
        else:
            self.remove()

    def draw(self):
        for p in self.particles:
            p.draw()


class ParticlesExplosion(Updatable, Drawable):
    def __init__(self, pos, color=GREEN, duration=0.5, acceleration=-0.5):

        self.start_update()
        self.set_draw_layer(Layer.fore)

        self.particles = []
        for _ in range(40):
            size = randint(1, 3)
            dist = randint(60, 80)  # distance per seconds
            vel = v2(dist, 0)
            vel = vel.rotate(uniform(0, 360))
            acc = vel.normalize() * acceleration  # deceleration
            self.particles.append(Particle(pos, size, vel, acc, duration, color))

    def remove(self):
        self.stop_draw()
        self.stop_update()

    def update(self, dt, t=None):
        if len(self.particles):
            for p in self.particles:
                p.update(dt)
                if p.is_dead:
                    self.particles.remove(p)
                    del p
        else:
            self.remove()

    def draw(self):
        for p in self.particles:
            p.draw()


class HitFlash(Entity, Updatable, Drawable):

    color_stars = ParticleStarField.color
    color_sky = Background.color

    def __init__(self, pos, color=WHITE):

        super().__init__(pos, radius=12)
        self.start_update()
        self.set_draw_layer(Layer.back)

        self.birth = time()
        self.has_started = False
        self.visible = False
        self.color = color

        Shaker()
        # Start flash
        Background.color = self.color
        ParticleStarField.color = WHITE

    def remove(self):
        self.stop_draw()
        self.stop_update()

    def update(self, dt, t):

        if not self.has_started:
            # Stop flash
            Background.color = self.color = self.color_sky
            ParticleStarField.color = self.color_stars
            self.has_started = True

        if t > self.birth + 0.1:  # duration
            self.remove()

    def draw(self):
        pos = self.pos + Entity.offset

        offx = uniform(-1, 1) * 3
        offy = uniform(-1, 1) * 3
        p1 = pos - v2(self.radius * offx / 2, self.radius * offy / 2)
        p2 = pos + v2(offx, offy)
        px.circ(*pos, self.radius, WHITE)
        px.circ(*p2, self.radius - 2, Background.color)
        px.line(*pos, *p1, WHITE)


class BigExplosion(Updatable, Drawable):
    def __init__(self, pos):

        self.start_update()
        self.set_draw_layer(Layer.fore)

        self.explosions = [
            ParticlesExplosion(pos, duration=1, acceleration=2, color=PURPLE),
            ParticlesExplosion(pos, duration=1, acceleration=2, color=BLUE),
            ParticlesExplosion(pos, duration=3, acceleration=-0.35, color=WHITE),
            ParticlesExplosion(pos, duration=3, acceleration=-0.35, color=CYAN),
        ]

    def remove(self):
        self.stop_draw()
        self.stop_update()

    def update(self, dt, t):
        for e in self.explosions.copy():
            e.update(dt)
            if len(e.particles) == 0:
                self.explosions.remove(e)
        if len(self.explosions) == 0:
            self.remove()

    def draw(self):
        for e in self.explosions:
            e.draw()


class HitEffect(Updatable):

    explosions = []

    def __init__(self, pos, color=WHITE):

        explosion = ParticlesExplosion(pos, color=color)
        explosion.stop_update()
        explosion.stop_draw()
        self.explosions.append(explosion)
        HitFlash(pos, color)
        self.start_update()

    def update(self, dt, t):
        # Fire only the last explosions
        if len(self.explosions):
            last_explosion = self.explosions[-1]
            last_explosion.start_update()
            last_explosion.start_draw()
            self.explosions.clear()
        self.stop_update()
