import pygame as pg
vec = pg.math.Vector2

DIRECT_DICT = {"UP": (0, -1), "RIGHT": (1, 0), "DOWN": (0, 1), "LEFT": (-1, 0)}


DIRECTIONS = ("UP", "RIGHT", "DOWN", "LEFT")


CONTROLS = {pg.K_UP: "UP", pg.K_RIGHT: "RIGHT", pg.K_DOWN: "DOWN", pg.K_LEFT: "LEFT"}

NME_DICT = {"UP": (0, -1), "RIGHT": (1, 0), "DOWN": (0, 1), "LEFT": (-1, 0)}


# Game settings
WIDTH = 1024
HEIGHT = 768
FPS = 30
TITLE = "wor"


TILESIZE = 128
GRIDWIDTH = WIDTH // TILESIZE
GRIDHEIGHT = HEIGHT // TILESIZE



# Player settings
PLAYER_HEALTH = 100
PLAYER_SPEED = 300
PLAYER_ROT_SPEED = 200
PLAYER_IMG = "img/count.png"
PLAYER_HIT_RECT = pg.Rect(0, 0, 35, 35)


# 
# Mob settings
NME_IMG = 'img/g.png'
NME_SPEED = 50
NME_HIT_RECT = pg.Rect(0, 0, 35, 35)
NME_HEALTH = 100
