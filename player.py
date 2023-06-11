


import pygame as pg
from pygame import font
from random import uniform, choice, randint, random
from config import *
from itertools import cycle, repeat
vec = pg.math.Vector2




class Player(pg.sprite.Sprite):
    def __init__(self, game, px, py):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.sheet = pg.image.load("img/count.png").convert_alpha()
        self.size = (32, 36)
        self.frames = self.strip(self.sheet, (0, 72), self.size, 3)
        self.frame_index = 0
        self.animation_speed = 200  # Milliseconds per frame
        self.last_update = 0
        self.last_direction = None
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.topleft = (px, py)
        self.pos = vec(px, py)
        self.vel = vec(0, 0)
        self.hit_rect = self.rect
        self.game = game
        self.font = pg.font.Font
        self.rot = 0
        self.last_shot = 0
        self.health = PLAYER_HEALTH
        self.facing = None
        self.size = (32, 36)
        self.start = (0, 0)
    def strip(self, sheet, start, size, columns, rows=1):
        self.frames = []
        for j in range(rows):
            for i in range(columns):
                location = (start[0] + size[0] * i, start[1] + size[1] * j)
                self.frames.append(sheet.subsurface(pg.Rect(location, size)))
        return self.frames

    def animate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > self.animation_speed:
            self.last_update = now
            if self.vel == vec(0, 0):
                self.frame_index = 0
                self.last_direction = self.facing
            else:
                self.frame_index = (self.frame_index + 1) % len(self.frames)
                self.last_direction = self.get_direction()
        self.image = self.frames[self.frame_index]


    def get_keys(self):
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.start =(0,106)
            self.strip(self.sheet, self.start, self.size, 3)
            self.facing = DIRECT_DICT["LEFT"]
           
            self.vel.x = -PLAYER_SPEED
        elif keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.start =(0, 37)
            self.strip(self.sheet, self.start, self.size, 3)
            self.facing = DIRECT_DICT["RIGHT"]
            self.vel.x = PLAYER_SPEED
        elif keys[pg.K_UP] or keys[pg.K_w]:
            self.start = (0, 0)
            self.strip(self.sheet,self.start, self.size, 3)
            self.facing = DIRECT_DICT["UP"]
            self.vel.y = -PLAYER_SPEED
        elif keys[pg.K_DOWN] or keys[pg.K_s]:
            self.start=(0, 72)
            self.strip(self.sheet, self.start, self.size, 3)
            self.facing = DIRECT_DICT["DOWN"]
            self.vel.y = PLAYER_SPEED

        if self.vel != vec(0, 0):
            self.last_direction = self.facing  # Update the last direction

    def get_direction(self):
        if self.vel.x > 0:
            return DIRECT_DICT["RIGHT"]
        elif self.vel.x < 0:
            return DIRECT_DICT["LEFT"]
        elif self.vel.y < 0:
            return DIRECT_DICT["UP"]
        elif self.vel.y > 0:
            return DIRECT_DICT["DOWN"]
        else:
            return self.facing

    def update(self):
        self.get_keys()
        self.animate()
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos

        self.rect.center = self.pos

        self.hit_rect.center = self.rect.center

    def draw(self):
        self.game.screen.blit(self.image, self.game.camera.apply(self))

