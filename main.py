import pygame as pg
import sys
from os import path

from config import *
from player import *
from enemy import *
from tilemap import *
from other_sprites import *

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.load_data()

    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        map_folder = path.join(game_folder, 'maps')
        self.map = TiledMap(path.join(map_folder, 'm.tmx'))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
     

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
       
        for tile_object in self.map.tmxdata.objects:
            if tile_object.name == 'player':
                self.player = Player(self, tile_object.x, tile_object.y)
            if tile_object.name == 'nme':
                self.nme = Enemy(self, tile_object.x, tile_object.y)
            if tile_object.name == 'wall':
                Obstacle(self, tile_object.x, tile_object.y,
                         tile_object.width, tile_object.height)
                self.wall_img = tile_object.name
        self.camera = Camera(self.map.width, self.map.height)
        self.draw_debug = False

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000.0  # fix for Python 2.x
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        
        self.all_sprites.update()
        self.camera.update(self.player)
        
      
       
    def draw(self):
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
   
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
   
        for sprite in self.all_sprites:
            
            self.screen.blit(sprite.image, self.camera.apply(sprite))
            if self.draw_debug:
                pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(sprite.hit_rect), 1)
        if self.draw_debug:
            for wall in self.walls:
                pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(wall.rect), 1)

      

        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_h:
                    self.draw_debug = not self.draw_debug


# create the game object
g = Game()

while True:
    g.new()
    g.run()
  
