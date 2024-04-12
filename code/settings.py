import pygame

SCREEN_SIZE = [1280, 720]
TILE_SIZE = int(SCREEN_SIZE[0] / 32)
SCREEN_SIZE_IN_TILES = [int(SCREEN_SIZE[0] / TILE_SIZE), int(SCREEN_SIZE[1] / TILE_SIZE)]


SCREEN_WIDTH, SCREEN_HEIGHT = SCREEN_SIZE

COLORS = {
    "BackGround": '#281d2f',
    "LogoText": '#bf8f30',

    "ButtonMain": '#281d2f',
    "ButtonSecond": '#33233C',
    "ButtonText": '#bf8f30',
    "ButtonBorder": '#241A2A',


    "Text": '#bf8f30',
    "TextCorrect": '#43F623',
    "TextError": '#FF0000',


    "Particles Correct": "#6DFF2F",
    "Particles Error": "#F01010",
}

PATHS = {
    "Character": {
        "idle": "../graphics/character/basic/idle",
        "jump": "../graphics/character/basic/jump",
        "run": "../graphics/character/basic/run",
    },

    "Textures": {
        "platforms": "../graphics/platforms",
        "blocks": "../graphics/blocks/blocks.png",
        "grass": "../graphics/grass",
    },

    "Icons": {
        "sound": "../graphics/icons/sound_icon.png"
    }
}



# Menu
MENU_Y_BLOCKS_SPEED = 1
FONT_NAME = 'cambria'

# Level
LEVEL_Y_BLOCKS_SPEED = {
    1: 1,
    2: 2,
    3: 3,
}

PLAYER_SPEED = 5
GRAVITY = 0.2
JUMP_SPEED_BY_SPEED = {
    1: -10,
    2: -9,
    3: -8.5
}
ANIMATION_SPEED = 0.08
