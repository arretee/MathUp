from random import choice, randint
from settings import *

from class_button import Button
from class_tile import Tile, MovingTile
from class_text import MovingText


class Menu:
    def __init__(self, game):
        # Basic
        self.game = game
        self.screen = self.game.screen

        # Groups
        self.texts = pygame.sprite.Group()
        self.tiles = pygame.sprite.Group()
        self.buttons = pygame.sprite.Group()

        self.setup()

    def setup(self):
        # -------------------------- Logo --------------------------
        self.logo_image = pygame.font.SysFont(FONT_NAME, int(TILE_SIZE * 1.8)).render("Math Up!", True,
                                                                                      COLORS['LogoText'])
        self.logo_rect = self.logo_image.get_rect(center=(TILE_SIZE * 26.5, TILE_SIZE * 4))

        # ----------------------- Decor --------------------------
        for i in range(21, SCREEN_SIZE_IN_TILES[0]):
            Tile(
                image=choice(self.game.textures["Textures"]["blocks"][1:]),
                pos=[TILE_SIZE * i, 0],
                groups=self.tiles
            )

            if randint(1, 5) == 3:
                Tile(
                    image=choice(self.game.textures["Textures"]["grass"]),
                    pos=[TILE_SIZE * i, TILE_SIZE],
                    groups=self.tiles
                )
        for i in range(21, SCREEN_SIZE_IN_TILES[0]):
            Tile(
                image=choice(self.game.textures["Textures"]["blocks"][1:]),
                pos=[TILE_SIZE * i, SCREEN_HEIGHT - TILE_SIZE],
                groups=self.tiles
            )
        for i in range(1, SCREEN_SIZE_IN_TILES[1]):
            Tile(
                image=choice(self.game.textures["Textures"]["blocks"][1:]),
                pos=[TILE_SIZE * 21, TILE_SIZE * i],
                groups=self.tiles
            )

            Tile(
                image=choice(self.game.textures["Textures"]["blocks"][1:]),
                pos=[TILE_SIZE * int(SCREEN_WIDTH / TILE_SIZE - 1), TILE_SIZE * i],
                groups=self.tiles
            )


        # ------------------------- Moving -------------------------
        # Tiles
        for i in range(int(SCREEN_SIZE_IN_TILES[1] + SCREEN_SIZE_IN_TILES[1] / 3)):
            MovingTile(
                image=choice(self.game.textures["Textures"]["blocks"][1:]),
                pos=[TILE_SIZE * 6, TILE_SIZE * i],
                y_change=MENU_Y_BLOCKS_SPEED,
                groups=self.tiles
            )

            MovingTile(
                image=choice(self.game.textures["Textures"]["blocks"][1:]),
                pos=[TILE_SIZE * 20, TILE_SIZE * i],
                y_change=MENU_Y_BLOCKS_SPEED,
                groups=self.tiles
            )

        for i in [0, 6, 12, 18]:
            MovingTile(
                image=self.game.textures["Textures"]["platforms"][0],
                pos=[TILE_SIZE * 7, TILE_SIZE * i],
                y_change=MENU_Y_BLOCKS_SPEED,
                groups=self.tiles
            )
            for j in [0, 1, 2, 8, 9, 10]:
                MovingTile(
                    image=self.game.textures["Textures"]["platforms"][1],
                    pos=[TILE_SIZE * (8 + j), TILE_SIZE * i],
                    y_change=MENU_Y_BLOCKS_SPEED,
                    groups=self.tiles
                )

            MovingTile(
                image=self.game.textures["Textures"]["platforms"][2],
                pos=[TILE_SIZE * 19, TILE_SIZE * i],
                y_change=MENU_Y_BLOCKS_SPEED,
                groups=self.tiles
            )

        # Text
        for i in [0, 6, 12, 18]:
            exersice = self.create_ex()

            MovingText(
                text=f"{exersice[0]} {exersice[2]} {exersice[1]} = ",
                text_size=60,
                start_pos=[TILE_SIZE, -2 * TILE_SIZE + TILE_SIZE * i],
                y_change=MENU_Y_BLOCKS_SPEED,
                text_color=COLORS["Text"],
                groups=self.texts
            )


            MovingText(
                text=str(exersice[3]),
                text_size=60,
                start_pos=[TILE_SIZE * 8, -2 * TILE_SIZE + TILE_SIZE * i],
                y_change=MENU_Y_BLOCKS_SPEED,
                text_color=COLORS["Text"],
                groups=self.texts
                )
            MovingText(
                text=str(exersice[4]),
                text_size=60,
                start_pos=[TILE_SIZE * 17, -2 * TILE_SIZE + TILE_SIZE * i],
                y_change=MENU_Y_BLOCKS_SPEED,
                text_color=COLORS["Text"],
                groups=self.texts
            )


        # -------------------------- Buttons --------------------------
        # Play
        Button(
            pos=(TILE_SIZE * 26.5, TILE_SIZE * 7)
            , main_color=COLORS["ButtonMain"]
            , second_color=COLORS["ButtonSecond"]
            , text_color=COLORS["ButtonText"]
            , border_color=COLORS["ButtonBorder"]
            , text="Play"
            , font=pygame.font.SysFont('cambria', int(TILE_SIZE * 1.4))
            , size=(TILE_SIZE * 5.3, TILE_SIZE * 2)
            , group=self.buttons
            , func=self.game.go_to_level
        )

        # Settings
        Button(
            pos=(TILE_SIZE * 26.5, TILE_SIZE * 9.5)
            , main_color=COLORS["ButtonMain"]
            , second_color=COLORS["ButtonSecond"]
            , text_color=COLORS["ButtonText"]
            , border_color=COLORS["ButtonBorder"]
            , text="Settings"
            , font=pygame.font.SysFont('cambria', int(TILE_SIZE * 1.4))
            , size=(TILE_SIZE * 5.3, TILE_SIZE * 2)
            , group=self.buttons
            , func=None
        )

        # Exit
        Button(
            pos=(TILE_SIZE * 26.5, TILE_SIZE * 12)
            , main_color=COLORS["ButtonMain"]
            , second_color=COLORS["ButtonSecond"]
            , text_color=COLORS["ButtonText"]
            , border_color=COLORS["ButtonBorder"]
            , text="EXIT"
            , font=pygame.font.SysFont('cambria', int(TILE_SIZE * 1.4))
            , size=(TILE_SIZE * 5.3, TILE_SIZE * 2)
            , group=self.buttons
            , func=None
        )

    def create_ex(self):
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

    def event_loop(self):
        self.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for sprite in self.buttons.sprites():
                    if sprite.rect.collidepoint(mouse_pos):
                        sprite.call_function()

    def update(self):
        self.tiles.update()
        for sprite in self.tiles.sprites():
            if TILE_SIZE * (SCREEN_SIZE_IN_TILES[1] + int(SCREEN_SIZE_IN_TILES[1] / 3) - 1) < sprite.rect.y:
                sprite.rect.y = -TILE_SIZE


        self.texts.update()
        for sprite in self.texts.sprites():
            if TILE_SIZE * (SCREEN_SIZE_IN_TILES[1] + int(SCREEN_SIZE_IN_TILES[1] / 3) - 1) - TILE_SIZE * 1 <= sprite.rect.y:
                sprite.rect.y = -TILE_SIZE * 2

        self.buttons.update(pygame.mouse.get_pos())

    def run(self):
        self.screen.fill(COLORS["BackGround"])


        self.screen.blit(self.logo_image, self.logo_rect)
        pygame.draw.line(self.screen, '#bf8f30', self.logo_rect.bottomleft, self.logo_rect.bottomright, 2)

        self.tiles.draw(self.screen)
        self.texts.draw(self.screen)
        self.buttons.draw(self.screen)
