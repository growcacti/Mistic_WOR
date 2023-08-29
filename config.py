import pygame as pg

vec = pg.math.Vector2


WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
DIRECT_DICT = {"UP": (0, -1), "RIGHT": (1, 0), "DOWN": (0, 1), "LEFT": (-1, 0)}


DIRECTIONS = ("UP", "RIGHT", "DOWN", "LEFT","UPRIGHT","UPLEFT","DOWNRIGHT", "DOWNLEFT")


CONTROLS = {pg.K_UP: "UP", pg.K_RIGHT: "RIGHT", pg.K_DOWN: "DOWN", pg.K_LEFT: "LEFT"}

NME_DICT = {"UP": (0, -1), "RIGHT": (1, 0), "DOWN": (0, 1), "LEFT": (-1, 0), "UPRIGHT" :(1,-1),
            "DOWNRIGHT": (1, 1), "UPLEFT" : (-1,-1), "DOWNLEFT": (-1,1)}


# Game settings
WIDTH = 1024
HEIGHT = 768
FPS = 30
TITLE = "wor"


TILESIZE = 128
GRIDWIDTH = WIDTH // TILESIZE
GRIDHEIGHT = HEIGHT // TILESIZE
ACID_SPEED = 20
SPELL_SPEED = 20

# Player settings
PLAYER_HEALTH = 100
PLAYER_SPEED = 300
PLAYER_ROT_SPEED = 200
PLAYER_IMG = "img/count.png"
PLAYER_HIT_RECT = pg.Rect(0, 0, 35, 35)
SCORE_POSITION = (WIDTH - 10, 10)  # Position of the score text (top right corner)


#
# Mob settings
NME_IMG = "img/g.png"
NME2_IMG = "img/llore.png"
NME_SPEED = 50
NME_HIT_RECT = pg.Rect(0, 0, 35, 35)
NME_HEALTH = 100
NME2_SPEED = 120
NME2_HIT_RECT = pg.Rect(0, 0, 35, 35)
NME2_HEALTH = 100
