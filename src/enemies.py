import math
import random
from time import time

import pyxel as px

from utils import Delay, map_range
from base import ASprite, Entity, Image, Updatable, Drawable, Layer
from constants import *
from gfx import (
    Background,
    HitEffect,
    HitFlash,
    ParticlesExplosion,
    BigExplosion,
    ParticleStarField,
)
from bullets import EnBullet
from ship import Ship
from vector import Vector as v2


class Enemy(ASprite, Updatable, Drawable):

    enemies = []

    @classmethod
    def clear_all(cls):
        for enemy in cls.enemies:
            enemy.stop_update()
            enemy.stop_draw()
        cls.enemies.clear()

    def __init__(self, pos, frame, freq, colkey=BLACK):
        super().__init__(pos, frame, freq, colkey=colkey)
        self.init_pos()
        self.life = 1
        self.birth = time()
        self.destroy_sound = 1
        self.enemies.append(self)
        self.start_update()
        self.set_draw_layer(Layer.main)

    def init_pos(self):
        # Make sure enemy are out of screen when it start on bound
        if self.pos.y == 0:  # means enemy starts on top of screen
            self.pos.y -= self.frames[0].h / 2 + 1  # so make sure is out of screen
        elif self.pos.y == HEIGHT:
            self.pos.y += self.frames[0].h / 2 + 1
        if self.pos.x == 0:
            self.pos.x -= self.frames[0].w / 2 + 1
        elif self.pos.x == WIDTH:
            self.pos.x += self.frames[0].w / 2 + 1

    def set_target(self, target: Entity):
        # What do enemy have to shoot (-> the ship in our case)
        self.target = target

    def remove(self):
        # Remove enemy from the game
        if self in self.enemies:
            self.enemies.remove(self)
            self.stop_update()
            self.stop_draw()

    def destroy(self):
        px.play(CHAN_DESTROY, self.destroy_sound)
        self.remove()

    def hit_by(self, entity):
        self.life -= 1
        if self.life > 0:
            px.play(CHAN_DESTROY, self.hit_sound)
        # HitFlash(entity.pos, color=self.color)
        HitEffect(entity.pos, color=self.color)

    def update(self, dt, t):
        super().update(dt, t)


class En1(Enemy):
    def __init__(self, pos):
        super().__init__(pos, [Image(19, 0, 11, 11), Image(32, 0, 11, 11)], 0.5)
        self.points = 200
        self.target = None  # What do i have to shoot
        self.color_back = DARK_GREEN
        self.color = GREEN
        self.destroy_sound = 2
        self.previous_shoot = self.birth
        px.play(CHAN_SPAWN, 8)

    def update(self, dt, t):
        super().update(dt, t)

        vx = math.cos((t - self.birth) * 3) * 10
        vy = 20
        self.center += v2(0, vy) * dt
        self.pos = self.center + v2(vx, 0)

        # Enemy shoot
        if t - self.previous_shoot >= 1 and self.target.alive:
            vel = self.target.pos - self.pos
            vel = vel.normalize() * 45
            EnBullet(self.pos, vel)
            self.previous_shoot = t

        # Out of bounds
        if self.pos[1] >= HEIGHT + self.img.h:
            self.remove()


class En2(Enemy):

    # To track a common frame count
    prev_t = 0  #  previous time
    frame_count = 0

    def __init__(self, pos, direc=1):
        super().__init__(
            pos, [Image(76, 0, 9, 9), Image(86, 0, 9, 9)], 0.5, colkey=GREEN
        )
        self.points = 100
        self.color = CYAN
        self.color_back = BLUE
        self.dir = direc
        self.play_spawn_sound()

    def play_spawn_sound(self):
        note = "abcdefg"[random.randint(0, 6)] + "0"
        px.sound(9).set(note, "S", "7", "F", 15)
        px.play(CHAN_SPAWN, 9)

    def update(self, dt, t):

        if t - En2.prev_t >= self.freq:
            En2.frame_count += 1
            En2.prev_t = t
        if En2.frame_count >= 2:  # 2 -> len(self.frames) hardcoded
            En2.frame_count = 0
        self.img = self.frames[En2.frame_count]

        vel = v2(8 * self.dir, 20)
        self.center += vel * dt
        mov = v2(
            math.cos((t - self.birth) * 4) * 16 * self.dir,
            math.sin((t - self.birth) * 4) * 16,
        )
        self.pos = self.center + mov

        # Out of bounds
        if self.pos[1] > HEIGHT + 64:
            self.remove()


class En3(Enemy):
    def __init__(self, pos):
        super().__init__(pos, [Image(44, 0, 15, 15), Image(60, 0, 15, 15)], 0.5)
        self.points = 500
        self.life = 3
        self.target = None
        self.color = RED
        self.color_back = PURPLE
        self.destroy_sound = 3
        self.hit_sound = 4
        self.speed_shoot = 1
        self.previous_shoot = self.birth
        self.speed = 50
        px.play(CHAN_SPAWN, 10)

    def update(self, dt, t):
        super().update(dt, t)

        change = int((t - self.birth) * 1.25) % 4
        if change == 0:
            di = v2(1, 0)
        elif change == 2:
            di = v2(-1, 0)
        else:
            di = v2(0, 1)

        vel = di * self.speed
        self.pos += vel * dt

        # Enemy shoot
        if t - self.previous_shoot >= self.speed_shoot and self.target.alive:
            vel = self.target.pos - self.pos
            vel = vel.normalize() * 45
            EnBullet(self.pos, vel)
            self.previous_shoot = t

        # Out of bounds
        if self.pos[1] > HEIGHT + self.img.h:
            self.remove()


class Boss(Enemy):
    def __init__(self, pos):
        super().__init__(pos, [Image(102, 0, 48, 44), Image(151, 0, 48, 44)], 0.5)
        self.target = None
        self.radius = 7
        self.life = self.max_life = 50
        self.points = self.max_life * 1000
        self.color = GREY
        self.color_back = RED
        self.hit_sound = 7
        self.speed_shoot = 1
        self.previous_shoot = self.birth
        self.speed = 50
        self.show_lifebar = True
        HitFlash.color_sky = PURPLE
        HitFlash.color_stars = FLESH
        Background.color = PURPLE
        ParticleStarField.color = FLESH
        # timing
        self.dying = False
        self.starting = True
        self.death_time = None
        px.stop()
        px.playm(1, loop=True)

    def destroy(self):
        self.dying = True
        self.death_time = time()

    def _destroy(self):
        HitFlash.color_sky = BLACK
        Background.color = BLACK
        HitFlash.color_stars = BLUE
        ParticleStarField.color = BLUE
        super().remove()
        # music again after boss death
        Delay(lambda: px.playm(3, loop=True), delay=5)

    def collide_with(self, entity):
        if not self.starting and not self.dying:
            hit_ship = isinstance(entity, Ship)
            self.radius = 22 if hit_ship else 7
            result = super().collide_with(entity)
            if result and not hit_ship:
                self.pos += v2(0, -5)
            return result
        return False

    def update(self, dt, t):
        super().update(dt, t)

        since_birth = t - self.birth
        vx = 0
        vy = 0
        max_height = HEIGHT * 0.4

        if self.starting:
            EnBullet.clear_all()
            if since_birth <= 3:  # Waiting boss
                if not int(round(since_birth % 0.3, 2) * 10):
                    Background.color = PURPLE
                    ParticleStarField.color = FLESH
                else:
                    Background.color = BLACK
                    ParticleStarField.color = BLUE
            else:  # boss is here
                px.play(CHAN_SPAWN, 11)  #  spawn sound
                Background.color = PURPLE
                ParticleStarField.color = FLESH
                self.starting = False
                self.birth = t
                self.previous_shoot = t
        else:
            if self.pos[1] < max_height:
                vy = max_height if since_birth <= 3 else 15

            phase = int(since_birth) % 8
            if phase == 0 or phase == 6:  # go left
                vx = 50
            elif phase == 2 or phase == 4:  # go right
                vx = -50
            else:  # pause
                vx = 0

        if self.dying:  # Boss is dying
            vx = 2
            vy = 20 if self.pos[1] < 44 else 4
            Background.color = RED
            since_death = t - self.death_time
            if since_death >= 3.6:  #  final explosion
                px.playm(0)
                Delay(lambda: HitFlash(self.pos), delay=1.25)
                Delay(lambda: BigExplosion(self.pos), delay=1.25)
                self._destroy()
            elif not int(round(since_death % 0.4, 2) * 10):  # boss is imploding
                x = random.uniform(-20, 20)
                y = random.uniform(-20, 20)
                pos = self.pos + v2(x, y)
                col = random.randint(0, 3)
                ParticlesExplosion(pos, color=(6, 7, 10, 15)[col])
                px.play(CHAN_DESTROY, max(3, col + 1))

                HitFlash(pos, color=WHITE)
                Background.color = WHITE

        vel = v2(vx, vy)
        self.pos += vel * dt

        if (
            t - self.previous_shoot >= self.speed_shoot
            and not self.starting
            and not self.dying
            and self.target.alive
        ):
            for a in range(16):
                vel_b = v2(0, 1)
                vel_b = vel_b.rotate(a * 22.5)  # 22.5 = 360 / 16
                vel_b *= 40
                EnBullet(self.pos, vel_b, col=1)
            self.previous_shoot = t

        if not self.target.alive:
            self.show_lifebar = False

    def draw(self):
        super().draw()
        # Life bar
        if self.show_lifebar:
            p1 = v2((WIDTH - 102) // 2, 3) + Entity.offset
            p2 = v2(101, 3)
            px.rect(*p1, *p2, BLUE)
            p3 = p1 + v2(1, 1)
            p4 = v2(100 * self.life // self.max_life - 1, 1)
            px.rect(*p3, *p4, RED)


# Wave 2


class XRotator(Enemy):
    def __init__(self, pos, destination):
        super().__init__(pos, [Image(20, 12, 11, 11), Image(32, 12, 11, 11)], 0.5)
        self.points = 500
        self.life = 3
        self.color_back = ORANGE
        self.color = YELLOW
        self.destroy_sound = 1
        self.hit_sound = 4
        self.previous_shoot = self.birth

        self.start = self.pos = pos
        self.destination = destination
        self.speed = 40
        px.play(CHAN_SPAWN, 8)  # spawn sound

    def update(self, dt, t):
        super().update(dt, t)

        self.target = self.destination - self.pos
        dist = self.target.norm()
        if dist < 1:
            self.vel = v2(0, 0)
            self.destination, self.start = self.start, self.destination
        else:
            self.vel = self.target.normalize() * self.speed
        self.pos += self.vel * dt

        # Fire
        if t - self.previous_shoot >= 1:  # and not game.end_game:
            for a in range(4):
                vel_b = v2(0, 1)
                vel_b = vel_b.rotate(a * 90 + 45)  # 22.5 = 360 / 16
                vel_b *= 40
                EnBullet(self.pos, vel_b)
            self.previous_shoot = t


class Sider(Enemy):

    # To track a common frame count
    prev_t = 0  #  previous time
    frame_count = 0

    def __init__(self, direc=1):

        gx = WIDTH / 16  # one unit of grid
        self.speed = 64
        self.tc = self.speed / gx  # time to travel one unit of our grid
        self.direc = direc
        self.pos = v2(MID_W + gx * 7 * -direc, -10)
        super().__init__(self.pos, [Image(76, 10, 9, 9), Image(86, 10, 9, 9)], 0.5)

        self.points = 800
        self.life = 4
        self.color_back = PURPLE
        self.color = PINK
        self.destroy_sound = 2
        self.hit_sound = 4
        self.previous_shoot = self.birth

        px.play(CHAN_SPAWN, 9)  # spawn sound

    def update(self, dt, t):
        # Synchronised frame accross all instances
        if t - Sider.prev_t >= self.freq:
            Sider.frame_count += 1
            Sider.prev_t = t
            if Sider.frame_count >= 2:  # 2 -> len(self.frames) hardcoded
                Sider.frame_count = 0
        self.img = self.frames[Sider.frame_count]

        # move
        c = (t - self.birth) * self.tc % 32
        if c >= 0 and c < 2 or c >= 16 and c < 18:
            di = v2(0, 1)
        elif c >= 2 and c < 16:
            di = v2(1 * self.direc, 0)
        else:
            di = v2(-1 * self.direc, 0)
        vel = di * self.speed
        self.pos += vel * dt

        # shoot
        bls = 16  # Bullets per second
        if t - self.previous_shoot >= 1 / bls:  # and not game.end_game:
            # 360° spiral
            change = (t - self.birth) * bls % 16

            vel_b = v2(0, 1)
            vel_b = vel_b.rotate(22.5 * change)  # 22.5 = 360 / 16
            vel_b *= 45
            EnBullet(self.pos, vel_b)
            self.previous_shoot = t

        # Out of bounds
        if self.pos.y > HEIGHT + self.img.h:
            self.remove()


class Pendulum(Enemy):
    def __init__(self, pos):
        super().__init__(
            pos, [Image(0, 9, 9, 9), Image(10, 9, 9, 9)], 0.5, colkey=GREEN
        )
        self.points = 1000
        self.life = 10
        self.color_back = GREY
        self.color = LIGHT_GREY
        self.hit_sound = 7
        self.destroy_sound = 3
        self.speed = 5

        self.birth += math.pi / 2  # add time to start on top of pendulum move
        self.count = -1  #  count each half pi period used for shooting period
        self.hwp = 40  # half width of pendulum move distance in pixels
        self.hhp = 20  # half height of ...
        self.f = 1.25  #  frequence of the move

        px.play(CHAN_SPAWN, 10)  # spawn sound

    def update(self, dt, t):
        super().update(dt, t)

        # Move
        ti = t - self.birth
        vx = math.sin(ti * self.f) * self.hwp
        vy = math.cos(ti * (self.f * 2)) * self.hhp
        self.center += v2(0, self.speed) * dt
        self.hhp -= 2 * dt
        self.pos = self.center + v2(vx, vy)

        c = ti // (1.5708 / self.f)  # 1.5708 -> pi / 2
        if c > self.count:  # and not game.end_game:
            if self.count % 2:
                for a in range(16):
                    vel_b = v2(0, 1)
                    vel_b = vel_b.rotate(22.5 * a)  # 22.5 = 360 / 16
                    vel_b *= 45
                    EnBullet(self.pos, vel_b)
            self.count += 1

        # Out of bounds
        if self.pos.y > HEIGHT + self.img.h:
            self.remove()


class TowerGun(Enemy):
    def __init__(self, n_id, base):
        self.id = n_id
        self.base = base  #  ref to core BigBoss
        self.pos = self.get_pos(time())
        super().__init__(self.pos, [Image(44, 0, 15, 15), Image(60, 0, 15, 15)], 0.5)
        self.life = 5
        self.points = self.life * 200
        self.color = RED
        self.color_back = PURPLE
        self.destroy_sound = 3
        self.hit_sound = 4
        self.speed_shoot = 1
        self.previous_shoot = self.birth
        self.speed = 50
        px.play(CHAN_SPAWN, 10)

        self.pos_target = None

    def collide_with(self, entity):
        # Test prevents being touch during the waiting boss phase
        if self.base.starting:
            return False
        return super().collide_with(entity)

    def hit_by(self, entity):
        super().hit_by(entity)
        self.base.life -= 1

    def destroy(self):
        self.base.towerguns.remove(self)
        super().destroy()

    def get_pos(self, t):
        p = v2(math.cos(-t), math.sin(-t)).normalize() * 30
        return self.base.pos + p.rotate(90 * self.id)

    def update(self, dt, t):
        super().update(dt, t)
        self.pos = self.get_pos(t)
        # shoot
        if (
            t - self.previous_shoot >= 0.5 and self.pos_target is not None
        ):  # and not game.end_game
            vel = self.pos_target - self.pos
            n = max(vel.norm(), 25)
            vel = vel.normalize() * n
            EnBullet(self.pos, vel * 0.7, col=1)
            self.previous_shoot = t

    def draw(self):
        px.pal(PURPLE, BLUE)
        super().draw()
        px.pal()


class BigBoss(Enemy):

    imgs_close = [Image(0, 73, 30, 30), Image(31, 73, 30, 30)]
    imgs_open = [Image(0, 104, 30, 30), Image(31, 104, 30, 30)]

    def __init__(self, pos):
        super().__init__(pos, BigBoss.imgs_close, 0.5, colkey=GREEN)
        self.radius = 5
        self.life = self.max_life = 50
        self.points = self.max_life * 2000
        self.color = GREY
        self.color_back = RED
        self.hit_sound = 7
        # game.fg_gfx.clear() -------------------> TODO
        HitFlash.color_sky = PURPLE
        HitFlash.color_stars = FLESH
        Background.color = PURPLE
        ParticleStarField.color = FLESH

        self.show_lifebar = True

        self.target = None
        self.towerguns = [
            TowerGun(0, self),
            TowerGun(1, self),
            TowerGun(2, self),
            TowerGun(3, self),
        ]
        # Add towerguns lives to BigBoss
        for tg in self.towerguns:
            self.life += tg.life
            self.max_life = self.life

        # Time buffers
        self.delay_shoot = None
        self.delay_enemy = None
        self.death_time = None

        # self.pos = v2(40, 40)
        self.pos = v2(MID_W, -40)  #  overwrite init pos because of towerguns
        self.eye_is_open = False
        self.is_winking = False

        # States
        self.starting = True  # Init phase waiting for BigBoss
        self.phase0 = False  # BigBoss arrive from top of the screen
        self.phase1 = False  # BigBoss with towerguns
        self.phase2 = False  # BigBoss alone launching enemy with 360° Bullet
        self.dying = False

        px.stop()
        px.playm(1, loop=True)

    def destroy(self):
        self.phase2 = False
        self.dying = True
        self.death_time = time()

    def _destroy(self):
        HitFlash.color_sky = BLACK
        Background.color = BLACK
        HitFlash.color_stars = BLUE
        ParticleStarField.color = BLUE
        self.remove()

    def collide_with(self, entity):
        if not self.starting and not self.dying:
            hit_ship = isinstance(entity, Ship)
            self.radius = 15 if hit_ship else 5
            if not self.phase2 and not hit_ship:
                return False
            result = super().collide_with(entity)
            return result
        return False

    def get_targets(self, num):
        targets = []
        v = v2(
            self.pos.x - self.target.pos.x, self.pos.y - self.target.pos.y
        ).normalize()
        c = v * self.target.radius + self.target.pos
        if num == 1:
            return [c]
        else:
            size = 3
            vstart = v2(v.y, -v.x) * self.target.radius * size
            dst = self.target.radius * size * 2 / (num - 1)
            for i in range(num):
                pt = c + vstart + v2(-v.y, v.x) * dst * i
                targets.append(pt)
            return targets

    def open_eye(self):
        self.eye_is_open = True
        self.frames = BigBoss.imgs_open

    def close_eye(self):
        self.eye_is_open = False
        if not self.is_winking:
            self.frames = BigBoss.imgs_close

    def start_wink(self, delay=0.5):
        self.is_winking = True
        self.frames = BigBoss.imgs_open
        Delay(self.stop_wink, delay=delay)

    def stop_wink(self):
        self.is_winking = False
        if not self.eye_is_open:
            self.frames = BigBoss.imgs_close

    def update(self, dt, t):
        super().update(dt, t)
        since_birth = t - self.birth

        if self.starting:
            EnBullet.clear_all()
            if since_birth <= 5:  # Waiting boss
                if not int(round(since_birth % 0.3, 2) * 10):
                    Background.color = PURPLE
                    ParticleStarField.color = FLESH
                else:
                    Background.color = BLACK
                    ParticleStarField.color = BLUE
            else:  # boss is here
                px.play(CHAN_SPAWN, 11)  #  spawn sound
                Background.color = PURPLE
                ParticleStarField.color = FLESH
                self.starting = False
                self.phase0 = True
                self.birth = t
                self.delay_shoot = t

        elif self.dying:
            vx = 2
            vy = 20 if self.pos[1] < 44 else 4
            Background.color = RED
            since_death = t - self.death_time
            if since_death >= 3.6:  #  final explosion
                px.playm(0)
                Delay(lambda: HitFlash(self.pos), delay=1.25)
                Delay(lambda: BigExplosion(self.pos), delay=1.25)
                self._destroy()
            elif not int(round(since_death % 0.4, 2) * 10):  # boss is imploding
                x = random.uniform(-20, 20)
                y = random.uniform(-20, 20)
                pos = self.pos + v2(x, y)
                col = random.randint(0, 3)
                ParticlesExplosion(pos, color=(6, 7, 10, 15)[col])
                px.play(CHAN_DESTROY, max(3, col + 1))

                HitFlash(pos, color=WHITE)
                Background.color = WHITE

            vel = v2(vx, vy)
            self.pos += vel * dt
        else:  # phase0 to phase2

            if self.phase0 or self.phase1:
                # Targets for towergun -> shoot
                num_tower = len(self.towerguns)
                if num_tower:
                    for towg, targ in zip(self.towerguns, self.get_targets(num_tower)):
                        towg.pos_target = targ
                else:
                    self.phase1 = False
                    self.phase2 = True
                    self.delay_shoot = t
                    self.delay_enemy = t

            if self.phase2:
                if (
                    t - self.delay_shoot >= 2 and self.target.alive
                ):  # not game.end_game:
                    self.start_wink()
                    for a in range(16):
                        vel_b = v2(0, 1)
                        vel_b = vel_b.rotate(a * 22.5)  # 22.5 = 360 / 16
                        vel_b *= 40
                        EnBullet(self.pos, vel_b, col=1)
                    self.delay_shoot = t

            # Move
            s = 20
            vx = 0
            vy = 0
            period = int(since_birth * 0.5) % 8
            if self.phase0:
                if period == 0 or period == 1:
                    vy = s
                if period == 2:
                    self.phase0 = False
                    self.phase1 = True
            else:
                if period == 3 or period == 7:
                    if self.phase2:
                        self.close_eye()
                    vy = s
                elif period == 4 or period == 6:
                    vx = s
                elif period == 5 or period == 1:
                    vy = -s
                elif period == 0 or period == 2:
                    vx = -s
                if period == 2 or period == 6:
                    delay = (
                        map_range(self.life, 20, 50, 0.4, 2) if self.life > 20 else 0.2
                    )
                    if self.phase2 and t - self.delay_enemy >= delay:
                        self.open_eye()
                        direc = (period - 4) // -2
                        if self.life > 20:
                            child_enemy = En1(self.pos - v2(10, 0))
                            child_enemy.set_target(self.target)
                        else:
                            En2(
                                self.pos - v2(16 * direc, 0), direc=direc
                            )  # delay = 0.2
                        self.delay_enemy = t

            vel = v2(vx, vy)
            self.pos += vel * dt

        if not self.target.alive:
            self.show_lifebar = False

    def draw(self):
        super().draw()

        # Life bar
        if self.show_lifebar:
            p1 = v2((WIDTH - 102) // 2, 3) + Entity.offset
            p2 = v2(101, 3)
            px.rect(*p1, *p2, BLUE)
            p3 = p1 + v2(1, 1)
            p4 = v2(100 * self.life // self.max_life - 1, 1)
            px.rect(*p3, *p4, RED)
