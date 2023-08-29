import pygame as pg
import sys
from os import path

from config import *
from player import *
from enemy import *
from enemy2 import *
from tilemap import *
from other_sprites import *



from tilemap2 import TiledMap, Camera
from other_sprites import Health


def load_data(self):
    game_folder = path.dirname(__file__)
    img_folder = path.join(game_folder, "img")
    map_folder = path.join(game_folder, "map")
    self.map = TiledMap(path.join(map_folder, "map.tmx"))  # Replace "map.tmx" with your actual map file
    self.map_img = self.map.make_map()
    self.map_rect = self.map_img.get_rect()
    self.enemies = pg.sprite.Group()
    self.health = pg.sprite.Group()


def new(self):
    # initialize all variables and do all the setup for a new game
    self.all_sprites = pg.sprite.Group()
    self.walls = pg.sprite.Group()
    self.health.empty()
    for tile_object in self.map.tmxdata.objects:
        # ...
        if tile_object.name == "health":
            self.health = Health(
                self,
                tile_object.x,
                tile_object.y,
                tile_object.width,
                tile_object.height,
            )
            self.all_sprites.add(self.health)
        # ...


def draw(self):
    pg.display.set_caption(
        "Player Position: ({0}, {1})".format(
            int(self.player.pos[0]), int(self.player.pos[1])
        )
    )

    self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))

    for sprite in self.all_sprites:
        self.screen.blit(sprite.image, self.camera.apply(sprite))
        # ...

    score_text = self.score_font.render(
        "Score: {}".format((self.player.score)), True, CYAN
    )
    score_rect = score_text.get_rect()
    score_rect.topright = SCORE_POSITION
    self.screen.blit(score_text, score_rect)
    self.player.health_bar.draw(self.screen)
    pg.display.flip()


g = Game()
while True:
    g.new()
    g.run()
