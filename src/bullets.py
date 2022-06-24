from constants import WIDTH, HEIGHT
from vector import Vector as v2
from base import Image, Sprite, Updatable, Drawable, Layer


class Bullet(Sprite, Updatable, Drawable):
    # From the player's ship...
    bullets = []

    @classmethod
    def clear_all(cls):
        for bullet in cls.bullets:
            bullet.stop_draw()
            bullet.stop_update()
        cls.bullets.clear()

    def __init__(self, pos):
        super().__init__(pos, Image(10, 0, 9, 8))
        self.speed = -120
        self.vel = v2(0, self.speed)
        self.start_update()
        self.set_draw_layer(Layer.fore)
        self.bullets.append(self)

    def update(self, dt, t):
        self.pos += self.vel * dt
        if self.pos[1] <= -self.img.h:
            self.remove()

    def remove(self):
        self.stop_draw()
        self.stop_update()
        self.bullets.remove(self)


class EnBullet(Sprite, Updatable, Drawable):
    # From ennemies ...
    bullets = []

    @classmethod
    def clear_all(cls):
        for bullet in cls.bullets:
            bullet.stop_draw()
            bullet.stop_update()
        cls.bullets.clear()

    def __init__(self, pos, vel, col=0):  # col : 0 = red, 1 = blue, 2 = green
        super().__init__(pos, Image(96, 6 * col, 5, 5))
        self.vel = vel
        self.start_update()
        self.set_draw_layer(Layer.fore)
        self.bullets.append(self)

    def out_of_bounds(self):
        return (
            self.pos[0] <= -5
            or self.pos[0] >= WIDTH + 5
            or self.pos[1] <= -5
            or self.pos[1] >= HEIGHT + 5
        )

    def update(self, dt, t):
        self.pos += self.vel * dt
        if self.out_of_bounds():
            self.remove()

    def remove(self):
        self.stop_draw()
        self.stop_update()
        self.bullets.remove(self)
