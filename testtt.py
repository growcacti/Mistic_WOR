how could an item like a portal when the player coliides with it a new tmx map  is loaded
like another level



import pygame as pg
from os import path
import sys
from config import *
from player import *
from enemy import *
from enemy2 import *
from tiledmap2 import *
from other_sprites import *


class Game:
    def __init__(self):
        pg.init()
        self.all_sprites = pg.sprite.Group()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))

        self.player = Player(self, 600, 600)
        self.spells = pg.sprite.Group()
    
        self.clock = pg.time.Clock()
        self.load_data()
        self.score_font = pg.font.Font(None, 28)  # Create a font object for the score

    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, "img")
        map_folder = path.join(game_folder, "maps")
        map_filename = path.join(map_folder, "L4.tmx")  # Replace with your map file
        self.map = TiledMap(map_filename)  # Create an instance of TiledMap with the map filename
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.enemies = pg.sprite.Group()
        self.health = pg.sprite.Group()  # Add the health group here


            
    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.portals = pg.sprite.Group()
        self.health.empty()
        self.enemies.empty()
        self.spells.empty()

        self.load_map("maps/L4.tmx")  # Replace with the initial map filename

        self.draw_debug = False
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.health.empty()
        for tile_object in self.map.tmxdata.objects:
            if tile_object.name == "player":
                self.player = Player(self, tile_object.x, tile_object.y)
            if tile_object.name == "nme":
                self.nme = Enemy(self, tile_object.x, tile_object.y)
                self.enemies.add(self.nme)
            if tile_object.name == "nme2":
                self.nme2 = Nme2(self, tile_object.x, tile_object.y)
                self.enemies.add(self.nme2)

            if tile_object.name == "health":
                self.health = Health(
                    self,
                    tile_object.x,
                    tile_object.y,
                    tile_object.width,
                    tile_object.height,
                )
                self.all_sprites.add(self.health)

            if tile_object.name == "wall":
                Obstacle(
                    self,
                    tile_object.x,
                    tile_object.y,
                    tile_object.width,
                    tile_object.height,
                )
                self.wall_img = tile_object.name
            if tile_object.name == "portal":
                Obstacle(
                    self,
                    tile_object.x,
                    tile_object.y,
                    tile_object.width,
                    tile_object.height,
                )
                self.wall_img = tile_object.name
        self.camera = Camera(self.map.width, self.map.height)
        self.draw_debug = False

    def load_map(self, map_filename):
        self.map = TiledMap(map_filename)
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.walls.empty()  # Clear the walls group
        self.portals.empty()  # Clear the portals group
        self.all_sprites.empty()  # Clear all sprites group
        self.player = None  # Clear the player reference

        for tile_object in self.map.tmxdata.objects:
            if tile_object.name == "player":
                self.player = Player(self, tile_object.x, tile_object.y)
            elif tile_object.name == "nme":
                self.nme = Enemy(self, tile_object.x, tile_object.y)
                self.enemies.add(self.nme)
            elif tile_object.name == "nme2":
                self.nme2 = Nme2(self, tile_object.x, tile_object.y)
                self.enemies.add(self.nme2)
            elif tile_object.name == "health":
                self.health = Health(
                    self,
                    tile_object.x,
                    tile_object.y,
                    tile_object.width,
                    tile_object.height,
                )
                self.all_sprites.add(self.health)
            elif tile_object.name == "wall":
                Obstacle(
                    self,
                    tile_object.x,
                    tile_object.y,
                    tile_object.width,
                    tile_object.height,
                )
            elif tile_object.name == "portal":
                portal = Portal(
                    self,
                    tile_object.x,
                    tile_object.y,
                    tile_object.width,
                    tile_object.height,
                    tile_object.properties["map_filename"],
                )
                self.portals.add(portal)
                self.all_sprites.add(portal)

        self.camera = Camera(self.map.width, self.map.height)

    def draw(self):
        pg.display.set_caption(
            "Player Position: ({0}, {1})".format(
                int(self.player.pos[0]), int(self.player.pos[1])
            )
        )

        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))

        for sprite in self.all_sprites:

            self.screen.blit(sprite.image, self.camera.apply(sprite))
            if self.draw_debug:
                pg.draw.rect(
                    self.screen, CYAN, self.camera.apply_rect(sprite.hit_rect), 1
                )
        if self.draw_debug:
            for wall in self.walls:
                pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(wall.rect), 1)

        if self.draw_debug:
            for wall in self.walls:
                pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(wall.rect), 1)

        score_text = self.score_font.render(
            "Score: {}".format((self.player.score)), True, CYAN
        )
        score_rect = score_text.get_rect()
        score_rect.topright = SCORE_POSITION
        self.screen.blit(score_text, score_rect)
        self.player.health_bar.draw(self.screen)
        pg.display.flip()






    def run(self):
        # game loop - set self.playing = False to end the game
        loop = True
        while loop:

            self.dt = self.clock.tick(FPS) / 1000.0  # fix for Python 2.x
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        loop = False
        sys.exit()

    def update(self):
        self.camera.update(self.player)
        self.camera.update(self.player)
        self.nme2.fire_acid()
        self.all_sprites.update()

        # Check for collisions between player and walls
        player_collisions = pg.sprite.spritecollide(self.player, self.walls, False)
        if player_collisions:
            # Adjust player's position to avoid the walls
            self.player.pos -= self.player.vel * self.dt

        # Check for collisions between player and health objects
        player_health_collisions = pg.sprite.spritecollide(
            self.player, self.health, True
        )
        if player_health_collisions:
            self.player.health += (
                10  # Increase the player's health when colliding with a health object
            )

        # Check for collisions between player and enemies
        spell_hits = pg.sprite.spritecollide(self.player, self.enemies, True)
        if spell_hits:
            self.player.score += 1
            self.player.score += len(spell_hits)

        for enemy in self.enemies:
            enemy_collisions = pg.sprite.spritecollide(enemy, self.walls, False)
            if enemy_collisions:
                # Adjust enemy's position to avoid the walls
                enemy.pos -= enemy.vel * self.dt

        self.spells.update()
        ##        self.acid.update()
        spell_hits = pg.sprite.spritecollide(self.player, self.enemies, True)
        if spell_hits:
            self.player.score += 1
            self.player.score += len(nme)

        hits = pg.sprite.groupcollide(self.enemies, self.spells, True, True)
        for self.nme in hits:
            # Increase the player's score
            self.player.score += 1
            # Remove the enemy sprite from groups and kill it
            self.nme.kill()
        if self.nme and pg.sprite.collide_rect(self.player, self.nme):
            self.player.health -= (
                10  # Decrease health by 1 if player collides with the nme
            )
            self.player.health_bar.update()
        nme_collisions = pg.sprite.spritecollide(self.player, self.enemies, False)
        if nme_collisions:
            self.player.health -= 10  # Decrease health by 1 for each nme collision
            self.player.health_bar.update()

        player_health_collisions = pg.sprite.spritecollide(
            self.player, self.health, True
        )
        if player_health_collisions:
            self.player.health += (
                10  # Increase the player's health when colliding with a health object
            )
        portal_collisions = pg.sprite.spritecollide(self.player, self.portals, False)
        if portal_collisions:
            portal_collisions[0].collide_with_player()    
    def draw(self):
        pg.display.set_caption(
            "Player Position: ({0}, {1})".format(
                int(self.player.pos[0]), int(self.player.pos[1])
            )
        )

        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))

        for sprite in self.all_sprites:

            self.screen.blit(sprite.image, self.camera.apply(sprite))
            if self.draw_debug:
                pg.draw.rect(
                    self.screen, CYAN, self.camera.apply_rect(sprite.hit_rect), 1
                )
        if self.draw_debug:
            for wall in self.walls:
                pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(wall.rect), 1)

        if self.draw_debug:
            for wall in self.walls:
                pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(wall.rect), 1)

        ##        for spell in self.spells:
        ##            self.screen.blit(spell.image, self.camera.apply(spell))

        score_text = self.score_font.render(
            "Score: {}".format((self.player.score)), True, CYAN
        )
        score_rect = score_text.get_rect()
        score_rect.topright = SCORE_POSITION
        self.screen.blit(score_text, score_rect)
        self.player.health_bar.draw(self.screen)
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
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        spell = Spell(
                            self,
                            self.player.rect.centerx,
                            self.player.rect.centery,
                            self.player.direction,
                            self.player.facing,
                            self.player.angle,
                        )
                        self.player.fire_spell(self.player.angle)
        
# create the game object
g = Game()

while True:
    g.new()
    g.run()




other sprites code



import pygame as pg

from config import *


class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        self.rect = pg.Rect(x, y, w, h)
        self.hit_rect = self.rect
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y


class Health(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        self.rect = pg.Rect(x, y, w, h)
        self.hit_rect = self.rect
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
class Item(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        self.rect = pg.Rect(x, y, w, h)
        self.hit_rect = self.rect
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y


        
class Portal:
    def __init__(self, game, x, y, w, h):
        self.groups = game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        self.rect = pg.Rect(x, y, w, h)
        self.hit_rect = self.rect
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y


