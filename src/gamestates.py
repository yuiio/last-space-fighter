from time import time
from abc import ABC, abstractmethod

import pyxel as px

from vector import Vector as v2
from constants import *

from ship import Ship
from bullets import Bullet, EnBullet
from enemies import Enemy, Boss
from scores import ScoresHandler
from utils import center_txt, Delay
from gfx import (
    Background,
    ParticleStarField,
    HitFlash,
    HitEffect,
    ParticlesExplosion,
    BigExplosion,
)
from base import Updatable, Layer, Entity
from ending import RewardAnim


class GameState(ABC):
    def __init__(self, game):
        self.game = game
        self._next_state = self
        self.on_enter()

    @abstractmethod
    def on_enter(self):
        pass

    @abstractmethod
    def update(self, dt, t):
        pass

    @abstractmethod
    def draw(self):
        pass

    def get_next_state(self):
        return self._next_state

    def draw_layers(self):
        px.cls(Background.color)
        for item in Layer.back:
            item.draw()
        for item in reversed(Layer.main):
            item.draw()
        for item in Layer.fore:
            item.draw()

    def draw_hud(self):
        # Score on top right
        score = str(self.game.score)
        x = WIDTH - len(score) * 4 - 1
        pos_txt = v2(x, 2) + Entity.offset
        px.text(*pos_txt, score, WHITE)

        # Lives on top left
        for i in range(self.game.lives):
            pos_txt = v2(2 + i * 8, 2) + Entity.offset
            px.blt(*pos_txt, 0, 0, 19, 7, 5, colkey=BLACK)


class GameStateIntro(GameState):
    def on_enter(self):
        self.game.star_field.start()
        px.playm(2, loop=True)

    def update(self, dt, t):
        if px.btnp(px.KEY_X):
            self._next_state = GameStateStart(self.game)

        for item in Updatable.updatables:
            item.update(dt, t)

    def draw(self):
        px.cls(Background.color)
        for item in Layer.back:
            item.draw()

        # Title
        h = HEIGHT / 32
        px.blt((WIDTH - 84) // 2, h, 0, 0, 32, 84, 40, colkey=BLACK)
        author = "by Yuiio"
        px.text((WIDTH - len(author) * 4) // 2, h + 38, author, CYAN)

        # Hi-score
        ScoresHandler.draw(v2(60, HEIGHT * 9 / 20))

        # Instructions
        lines = [f"'Arrows' to move - 'X' to fire", f"Press 'X' to start"]
        for n, l in enumerate(lines):
            posx = center_txt(l)
            posy = HEIGHT - 2 - (n + 1) * 6
            px.text(posx, posy, l, GREY)


class GameStateStart(GameState):
    def on_enter(self):
        px.stop()
        px.playm(3, loop=True)
        self.game.start()

    def hit_ship(self):
        if not self.game.ship.shield:
            self.game.ship.hit()
            if self.game.lives:
                self.game.lives -= 1
                self.game.ship.protect()

    def hit_enemy_with(self, enemy, entity):
        if not (self.game.ship.shield and isinstance(entity, Ship)):
            enemy.hit_by(entity)

        if enemy.life <= 0:
            self.game.score += enemy.points
            enemy.destroy()

    def update(self, dt, t):
        for item in Updatable.updatables:
            item.update(dt, t)

        # Handle collisions
        # for bullet in EnBullet.bullets.copy():
        for bullet in reversed(EnBullet.bullets):
            if bullet.collide_with(self.game.ship):
                bullet.remove()
                self.hit_ship()
                break

        # for enemy in Enemy.enemies.copy():
        for enemy in reversed(Enemy.enemies):
            # for bullet in Bullet.bullets.copy():
            for bullet in reversed(Bullet.bullets):
                # Memo : sometime enemy has its own collide_with function
                if enemy.collide_with(bullet):
                    self.hit_enemy_with(enemy, bullet)
                    bullet.remove()
                    break
            if enemy.collide_with(self.game.ship):
                # Make sure enemy has not been killed by "the" previous bullet
                if enemy in Enemy.enemies:
                    self.hit_enemy_with(enemy, self.game.ship)
                    self.hit_ship()
                break

        # Loose ?
        if not self.game.lives:
            self.game.ship.alive = False
            self._next_state = GameStateShipDestroyed(self.game)

        # Win ?
        if self.game.army.end_war and not len(Enemy.enemies):
            self._next_state = GameStateShipExiting(self.game)

        self.game.spawn(t)

    def draw(self):
        self.draw_layers()
        self.draw_hud()


class GameStateShipDestroyed(GameState):
    def on_enter(self):
        self.start_time = time()
        self.game.ship.destroy()
        px.playm(0)

        # reset
        HitFlash.color_sky = BLACK
        HitFlash.color_stars = BLUE
        Background.color = BLACK
        ParticleStarField.color = BLUE

        # Scores
        ScoresHandler.update(self.game.score)
        ScoresHandler.save()

    def update(self, dt, t):

        for item in Updatable.updatables:
            item.update(dt, t)

        # Wait explosions end before cleaning
        if t - self.start_time >= 5:  # 3.6 -> end exploxion
            Enemy.clear_all()
            EnBullet.clear_all()
            Bullet.clear_all()
            self._next_state = GameStateIntro(self.game)

    def draw(self):
        self.draw_layers()
        self.draw_hud()
        msg = "GAME OVER"
        posx = center_txt(msg)
        px.text(posx, 60, msg, WHITE)


class GameStateShipExiting(GameState):
    def on_enter(self):

        self.game.star_field.stop()
        self.game.ship.acc = v2(0, -4)
        self.game.ship.vel = v2(0, -1)
        self.game.ship.stop_update()

    def is_exit_over(self):
        return not (len(self.game.star_field.particles) or self.game.ship.pos.y > -7)

    def update(self, dt, t):

        for item in Updatable.updatables:
            item.update(dt, t)
        self.game.ship.exiting(dt)

        if self.is_exit_over():
            self.game.ship.stop_draw()
            self._next_state = GameStateEndLivesBonus(self.game)

    def draw(self):
        self.draw_layers()


class GameStateEndLivesBonus(GameState):
    # Bonus for extra lives
    def on_enter(self):
        self.game.score += self.game.lives * 10000
        ScoresHandler.update(self.game.score)
        ScoresHandler.save()
        self.bonus_start = time()

    def update(self, dt, t):
        if t - self.bonus_start >= 3:
            self._next_state = GameStateVictory(self.game)

    def draw(self):
        title = "LIVES BONUS"
        x = (WIDTH - len(title) * 4) / 2
        y = 50
        px.text(x, y, title, WHITE)
        t = " x 10000 = "
        bonus = str(self.game.lives * 10000)
        x = (WIDTH - (self.game.lives * 8 + len(t) * 4 + len(bonus) * 4)) / 2
        for i in range(self.game.lives):
            px.blt(x + i * 8, y + 8, 0, 0, 19, 7, 5, colkey=BLACK)
        txt = t + bonus
        px.text(x + 8 * self.game.lives, y + 8, txt, WHITE)


class GameStateVictory(GameState):
    def on_enter(self):
        Entity.offset = v2(0, HEIGHT)
        self.end_anim = RewardAnim()
        self.end_anim.start()

    def update(self, dt, t):

        if Entity.offset.y > 0:
            Entity.offset += v2(0, -100) * dt
        else:
            Entity.offset = v2()
            if px.btnp(px.KEY_X):
                self._next_state = GameStateIntro(self.game)
        self.end_anim.update(dt, t)

    def draw(self):
        px.cls(BLACK)
        self.end_anim.draw()
