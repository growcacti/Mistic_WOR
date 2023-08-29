import pygame as pg
from pygame import font
from random import choice, randint
from config import *
from itertools import cycle

vec = pg.math.Vector2
MAX_ACID_SHOTS = 100
FIRE_COOLDOWN = 1

class Nme2(pg.sprite.Sprite):
    def __init__(self, game, px, py):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.sheet = pg.image.load("img/llore.png").convert_alpha()
        self.size = (32, 36)
        self.frames_down = self.strip(self.sheet, (0, 72), self.size, 3)
        self.frames_up = self.strip(self.sheet, (0, 0), self.size, 3)
        self.frames_left = self.strip(self.sheet, (0, 108), self.size, 3)
        self.frames_right = self.strip(self.sheet, (0, 36), self.size, 3)
        self.frame_index = 0
        self.image = self.frames_down[self.frame_index]
        self.rect = self.image.get_rect()
        self.animation_speed = 200  # Milliseconds per frame
        self.last_update = 0
        self.pos = vec(px, py)
        self.vel = vec(0, 0)
        self.hit_rect = self.rect
        self.fire_cooldown = 0
        self.game = game
        self.health = NME_HEALTH
        self.direction = vec(0, 0)
        self.angle = 270
        self.acidlist = []
        self.acid = None

    def strip(self, sheet, start, size, columns, rows=1):
        frames = []
        for j in range(rows):
            for i in range(columns):
                location = (start[0] + size[0] * i, start[1] + size[1] * j)
                frames.append(sheet.subsurface(pg.Rect(location, size)))
        return frames

    def animate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > self.animation_speed:
            self.last_update = now
            self.frame_index = (self.frame_index + 1) % len(self.frames_down)
            self.image = self.get_frame()

    def get_frame(self):
        if self.last_direction == NME_DICT["DOWN"]:
            return self.frames_down[self.frame_index]
        elif self.last_direction == NME_DICT["UP"]:
            return self.frames_up[self.frame_index]
        elif self.last_direction == NME_DICT["LEFT"]:
            return self.frames_left[self.frame_index]
        elif self.last_direction == NME_DICT["RIGHT"]:
            return self.frames_right[self.frame_index]

    def move_towards_player(self):
        player_pos = self.game.player.pos
        self.direction = player_pos - self.pos
        if self.direction.length_squared() > 0:
            self.direction.normalize_ip()

        self.vel = self.direction * NME_SPEED

        # Update last_direction based on movement direction
        if abs(self.direction.x) > abs(self.direction.y):
            if self.direction.x > 0:
                self.angle = 0
                self.last_direction = NME_DICT["RIGHT"]
            else:
                self.last_direction = NME_DICT["LEFT"]
                self.angle = 180
        elif abs(self.direction.x) < abs(self.direction.y):
            if self.direction.y > 0:
                self.last_direction = NME_DICT["DOWN"]
                self.angle = 270
            else:
                self.last_direction = NME_DICT["UP"]
                self.angle = 90

    def fire_acid(self):
        self.fire_cooldown -= self.game.dt
        if self.fire_cooldown <= 0:
            self.acid = Acid(self.game, self.rect.centerx, self.rect.centery, self.direction)
            self.acidlist.append(self.acid)
            self.game.all_sprites.add(self.acid)
            self.game.screen.blit(self.acid.image, self.game.camera.apply(self))
            self.fire_cooldown = FIRE_COOLDOWN 

    def update(self):
        self.rect.center = self.pos
        self.move_towards_player()
        self.animate()
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        self.hit_rect.center = self.rect.center
        self.fire_cooldown -= self.game.dt  # Decrease the fire cooldown

        # Check if enough time has passed to fire again
        if self.fire_cooldown <= 0 and len(self.acidlist) < MAX_ACID_SHOTS:
            self.fire_acid()  # Call the fire_acid method
            self.fire_cooldown = FIRE_COOLDOWN

    def draw(self):
        self.game.screen.blit(self.image, self.game.camera.apply(self))


class Acid(pg.sprite.Sprite):
    def __init__(self, game, x, y, direction):
        pg.sprite.Sprite.__init__(self, game.all_sprites)
        self.game = game
        self.surf = pg.Surface((32, 36)).convert_alpha()
        self.sheet = pg.image.load("img/acid.png").convert_alpha()
        self.size = (32, 36)
        self.frames_down = self.strip(self.sheet, (0, 72), self.size, 3)
        self.frames_up = self.strip(self.sheet, (0, 0), self.size, 3)
        self.frames_left = self.strip(self.sheet, (0, 106), self.size, 3)
        self.frames_right = self.strip(self.sheet, (0, 37), self.size, 3)
        self.anglelist = [0, 90, 180, 270]
        self.angle = choice(self.anglelist)
        self.frame_iter = cycle(self.get_frames(self.angle))
        self.image = next(self.frame_iter)
        self.rect = pg.Rect(self.image.get_rect())
        self.last_update = 0
        self.rect.center = (x, y)
        self.pos = vec(x, y)
        self.animation_speed = 100
        self.direction = direction

    def strip(self, sheet, start, size, columns, rows=1):
        frames = []
        for j in range(rows):
            for i in range(columns):
                location = (start[0] + size[0] * i, start[1] + size[1] * j)
                frames.append(sheet.subsurface(pg.Rect(location, size)))
        return frames

    def get_frames(self, angle):
        if angle == 90:
            return self.frames_up
        elif angle == 270:
            return self.frames_down
        elif angle == 180:
            return self.frames_left
        elif angle == 0:
            return self.frames_right

    def animate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > self.animation_speed:
            self.last_update = now
            self.image = next(self.frame_iter)

    def update(self):
        self.animate()
        if self.angle == 90:
            self.rect.centery -= ACID_SPEED
        elif self.angle == 270:
            self.rect.centery += ACID_SPEED
        elif self.angle == 180:
            self.rect.centerx -= ACID_SPEED
        elif self.angle == 0:
            self.rect.centerx += ACID_SPEED

        if (
            self.rect.left < 0
            or self.rect.right > self.game.map.width * 2
            or self.rect.top < -100
            or self.rect.bottom > self.game.map.height * 2
        ):
            self.kill()  # Remove the acid shot when it goes off-screen

    def draw(self):
        self.game.screen.blit(self.image, self.rect)
