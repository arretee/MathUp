import pygame
from random import choice, randint

from class_player import Player
from class_text import MovingText
from class_tile import Tile, MovingTile

from settings import *


class Level:
    def __init__(self, game):
        self.game = game
        self.screen = self.game.screen

        self.started = False

        self.player = Player()

        self.collide_sprites = pygame.sprite.Group()
        self.visible_sprites = pygame.sprite.Group()

        self.sprite_to_move = pygame.sprite.Group()
        self.start_platform_sprites = pygame.sprite.Group()

        self.exercises = []

        self.setup()

    def setup(self):
        # ----------------------- Decor --------------------------
        for i in range(21, SCREEN_SIZE_IN_TILES[0]):
            Tile(
                image=choice(self.game.textures["Textures"]["blocks"][1:]),
                pos=[TILE_SIZE * i, 0],
                groups=self.visible_sprites
            )

            if randint(1, 5) == 3:
                Tile(
                    image=choice(self.game.textures["Textures"]["grass"]),
                    pos=[TILE_SIZE * i, TILE_SIZE],
                    groups=self.visible_sprites
                )
        for i in range(21, SCREEN_SIZE_IN_TILES[0]):
            Tile(
                image=choice(self.game.textures["Textures"]["blocks"][1:]),
                pos=[TILE_SIZE * i, SCREEN_HEIGHT - TILE_SIZE],
                groups=self.visible_sprites
            )
        for i in range(1, SCREEN_SIZE_IN_TILES[1]):
            Tile(
                image=choice(self.game.textures["Textures"]["blocks"][1:]),
                pos=[TILE_SIZE * 21, TILE_SIZE * i],
                groups=self.visible_sprites
            )

            Tile(
                image=choice(self.game.textures["Textures"]["blocks"][1:]),
                pos=[TILE_SIZE * int(SCREEN_WIDTH / TILE_SIZE - 1), TILE_SIZE * i],
                groups=self.visible_sprites
            )

        # Tiles For Game
        # ------------------------- Moving -------------------------
        # Blocks
        for i in range(int(SCREEN_SIZE_IN_TILES[1] + SCREEN_SIZE_IN_TILES[1] / 3)):
            MovingTile(
                image=choice(self.game.textures["Textures"]["blocks"][1:]),
                pos=[TILE_SIZE * 6, TILE_SIZE * i],
                y_change=LEVEL_Y_BLOCKS_SPEED,
                groups=[self.collide_sprites, self.visible_sprites, self.sprite_to_move]
            )

            MovingTile(
                image=choice(self.game.textures["Textures"]["blocks"][1:]),
                pos=[TILE_SIZE * 20, TILE_SIZE * i],
                y_change=LEVEL_Y_BLOCKS_SPEED,
                groups=[self.collide_sprites, self.visible_sprites, self.sprite_to_move]
            )

        # Platforms
        for i in [0, 6, 12, 18]:
            MovingTile(
                image=self.game.textures["Textures"]["platforms"][0],
                pos=[TILE_SIZE * 7, i * TILE_SIZE],
                y_change=LEVEL_Y_BLOCKS_SPEED,
                groups=[self.collide_sprites, self.visible_sprites, self.sprite_to_move]
            )

            MovingTile(
                image=self.game.textures["Textures"]["platforms"][2],
                pos=[TILE_SIZE * 19, i * TILE_SIZE],
                y_change=LEVEL_Y_BLOCKS_SPEED,
                groups=[self.collide_sprites, self.visible_sprites, self.sprite_to_move]
            )

            for j in [8, 9, 10, 16, 17, 18]:
                MovingTile(
                    image=self.game.textures["Textures"]["platforms"][1],
                    pos=[TILE_SIZE * j, i * TILE_SIZE],
                    y_change=LEVEL_Y_BLOCKS_SPEED,
                    groups=[self.collide_sprites, self.visible_sprites, self.sprite_to_move]
                )

        # Start Platform
        for i in range(11, 16):
            MovingTile(
                image=self.game.textures["Textures"]["platforms"][1],
                pos=[TILE_SIZE * i, SCREEN_SIZE_IN_TILES[1] * TILE_SIZE - TILE_SIZE * 6],
                y_change=LEVEL_Y_BLOCKS_SPEED,
                groups=[self.collide_sprites, self.visible_sprites, self.sprite_to_move, self.start_platform_sprites]
            )

        # Exercises
        for i in [18, 12, 6, 0]:
            exersice = self.create_ex_basic()
            ex = []

            ex.append(
                MovingText(
                    text=f"{exersice[0]} {exersice[2]} {exersice[1]} = ",
                    text_size=60,
                    start_pos=[TILE_SIZE, -2 * TILE_SIZE + TILE_SIZE * i],
                    y_change=MENU_Y_BLOCKS_SPEED,
                    text_color=COLORS["Text"],
                    groups=[self.visible_sprites, self.sprite_to_move]
                )
            )
            ex.append(
                MovingText(
                    text=str(exersice[3]),
                    text_size=60,
                    start_pos=[TILE_SIZE * 8, -2 * TILE_SIZE + TILE_SIZE * i],
                    y_change=MENU_Y_BLOCKS_SPEED,
                    text_color=COLORS["Text"],
                    groups=[self.visible_sprites, self.sprite_to_move]
                )
            )

            ex.append(
                MovingText(
                    text=str(exersice[4]),
                    text_size=60,
                    start_pos=[TILE_SIZE * 17, -2 * TILE_SIZE + TILE_SIZE * i],
                    y_change=MENU_Y_BLOCKS_SPEED,
                    text_color=COLORS["Text"],
                    groups=[self.visible_sprites, self.sprite_to_move]
                )
            )

            self.exercises.append(ex)

    def create_ex_basic(self):
        x = randint(1, 10)
        y = randint(1, 10)

        action = randint(1, 3)
        action_txt = ""
        if action == 1:
            action_txt = "+"
        if action == 2:
            action_txt = "-"
        if action == 3:
            action_txt = "x"

        if action == 2:
            if y > x:
                x, y = y, x

        if randint(1, 2) == 2:
            if action == 1:
                first = x + y
            elif action == 2:
                first = x - y
            else:
                first = x * y

            incorrect = first + randint(-20, 20)
            if incorrect == first:
                second = first + randint(1, 20)
            else:
                second = first + randint(-20, 20)
        else:
            if action == 1:
                second = x + y
            elif action == 2:
                second = x - y
            else:
                second = x * y

            incorrect = second + randint(-20, 20)
            if incorrect == second:
                first = second + randint(1, 20)
            else:
                first = second + randint(-20, 20)

        return [x, y, action_txt, first, second]


    def add_new_ex(self):
        exersice = self.create_ex_basic()
        ex = []

        ex.append(
            MovingText(
                text=f"{exersice[0]} {exersice[2]} {exersice[1]} = ",
                text_size=60,
                start_pos=[TILE_SIZE, -2 * TILE_SIZE],
                y_change=MENU_Y_BLOCKS_SPEED,
                text_color=COLORS["Text"],
                groups=[self.visible_sprites, self.sprite_to_move]
            )
        )
        ex.append(
            MovingText(
                text=str(exersice[3]),
                text_size=60,
                start_pos=[TILE_SIZE * 8, -2 * TILE_SIZE],
                y_change=MENU_Y_BLOCKS_SPEED,
                text_color=COLORS["Text"],
                groups=[self.visible_sprites, self.sprite_to_move]
            )
        )

        ex.append(
            MovingText(
                text=str(exersice[4]),
                text_size=60,
                start_pos=[TILE_SIZE * 17, -2 * TILE_SIZE],
                y_change=MENU_Y_BLOCKS_SPEED,
                text_color=COLORS["Text"],
                groups=[self.visible_sprites, self.sprite_to_move]
            )
        )

        self.exercises.append(ex)


    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False

            if event.type == pygame.KEYDOWN:
                self.started = True

    def run(self):
        # Update
        if self.started:
            self.sprite_to_move.update()

            for sprite in self.sprite_to_move.sprites():
                if type(sprite) != MovingText:
                    if TILE_SIZE * (SCREEN_SIZE_IN_TILES[1] + int(SCREEN_SIZE_IN_TILES[1] / 3) - 1) < sprite.rect.y:
                        sprite.rect.y = -TILE_SIZE

                else:
                    if TILE_SIZE * (SCREEN_SIZE_IN_TILES[1] + int(SCREEN_SIZE_IN_TILES[1] / 3) - 1) - TILE_SIZE * 1 <= sprite.rect.y:
                        sprite.kill()
                        self.exercises[0].remove(sprite)


                    if self.exercises[0] == []:
                        self.exercises.pop(0)
                        self.add_new_ex()




            for sprite in self.start_platform_sprites.sprites():
                if sprite.rect.y > SCREEN_HEIGHT:
                    sprite.kill()
                else:
                    break

        # Draw
        self.screen.fill(COLORS["BackGround"])

        self.visible_sprites.draw(self.screen)
