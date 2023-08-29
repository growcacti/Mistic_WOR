import pygame as pg
import os
import pytmx
from config import *
class Map:
    def __init__(self, filename):
        self.current_map = filename
        self.load_map(filename)
        tm = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm
        self.camera = Camera(self.width, self.height)

        ti = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
         if isinstance(layer, pytmx.TiledTileLayer):
             for x, y, gid in layer:
                 tile = ti(gid)
                 if tile:
                     surface.blit(tile, (x * self.tmxdata.tilewidth, y * self.tmxdata.tileheight), area=self.camera.apply_rect(tile.get_rect()))

    def make_map(self):
        temp_surface = pg.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface









class TiledMap:
    def __init__(self, filename):
        tm = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm
        self.camera = Camera(self.width, self.height)
    def render(self, surface):
        ti = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = ti(gid)
                    if tile:
                        surface.blit(tile, (x * self.tmxdata.tilewidth,
                                            y * self.tmxdata.tileheight),
                                     area=self.camera.apply_rect(tile.get_rect()))

    def make_map(self):
        temp_surface = pg.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface





class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.centerx + int(WIDTH / 2)
        y = -target.rect.centery + int(HEIGHT / 2)

        # limit scrolling to map size
##        x = min(0, x)  # left
##        y = min(0, y)  # top
##        x = max(-(self.width - WIDTH), x)  # right
##        y = max(-(self.height - HEIGHT), y)  # bottom
        self.camera = pg.Rect(x, y, self.width, self.height)

    def update_map(self, player):
        player_pos = player.rect.center
        map_width = self.width / TILESIZE
        map_height = self.height / TILESIZE

        # Check if the player is near the edge of the current map
        if player_pos[0] < self.width:
            # Load the map to the left
            new_map = Map("left.tmx")
            new_x = new_map.width - TILESIZE
            new_y = player_pos[1]
        elif player_pos[0] > self.width:
            # Load the map to the right
            new_map = Map("right.tmx")
            new_x = TILESIZE
            new_y = player_pos[1]
        elif player_pos[1] < self.height:
            # Load the map above
            new_map = Map("top.tmx")
            new_x = player_pos[0]
            new_y = new_map.height - TILESIZE
        elif player_pos[1] > self.height:
            # Load the map below
            new_map = Map("bottom.tmx")
            new_x = player_pos[0]
            new_y = TILESIZE
        else:
            # The player is not near the edge of the current map
            return

        # Update the camera and the current map
        self.camera.topleft = (new_x - int(self.width / 2), new_y - int(self.height / 2))
        self.width = new_map.width
        self.height = new_map.height
        self.current_map = new_map.current_map

