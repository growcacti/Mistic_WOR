class Projectile(pg.sprite.Sprite):
    def __init__(self, game, x, y, facing, direction, angle):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.surf = pg.Surface((32, 36)).convert_alpha()
        self.sheet = pg.image.load("img/acid.png").convert_alpha()
        self.size = (32, 36)
        self.frames_down = self.strip(self.sheet, (0, 72), self.size, 3)
        self.frames_up = self.strip(self.sheet, (0, 0), self.size, 3)
        self.frames_left = self.strip(self.sheet, (0, 106), self.size, 3)
        self.frames_right = self.strip(self.sheet, (0, 37), self.size, 3)
        self.frame_iter = cycle(
            self.get_frames(angle)
        )  # Create an iterator for cycling frames
        self.image = next(self.frame_iter)  # Get the first frame
        self.rect = pg.Rect(self.image.get_rect())
        self.last_update = 0
        self.rect.center = (x, y)
        self.pos = vec(x, y)
        self.animation_speed = 2
        self.direction = direction
        self.facing = facing
        self.angle = angle

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
            # Up
            self.rect.centery -= SPELL_SPEED
        elif self.angle == 270:
            # Down
            self.rect.centery += SPELL_SPEED
        elif self.angle == 180:
            # Left
            self.rect.centerx -= SPELL_SPEED
        elif self.angle == 0:
            # Right
            self.rect.centerx += SPELL_SPEED
        # Remove the spell when it goes off the screen
        if (
            self.rect.left < 0
            or self.rect.right > self.game.map.width
            or self.rect.top < 0
            or self.rect.bottom > self.game.map.height
        ):
            self.kill()

    def draw(self):
        pass
