from random import choice, randint
from settings import *

from class_button import Button, ImageButton, SelectButton
from class_tile import Tile, MovingTile
from class_text import MovingText, Text


class Menu:
    def __init__(self, game):
        # Basic
        self.game = game
        self.screen = self.game.screen

        if self.game.music_status:
            self.game.play_music()

        # Groups
        self.texts = pygame.sprite.Group()
        self.tiles = pygame.sprite.Group()
        self.buttons = pygame.sprite.Group()

        self.difficulty_buttons = pygame.sprite.Group()
        self.speed_buttons = pygame.sprite.Group()

        self.sound_button = None

        # Text Variables
        self.logo_text = None
        self.diff_text = None
        self.speed_text = None

        self.setup()

    def setup(self):
        # -------------------------- Logo --------------------------
        self.logo_text = Text(
            text="Math Up!",
            text_size=72,
            start_pos=(TILE_SIZE * 26.5, TILE_SIZE * 2.5),
            text_color=COLORS["LogoText"],
            groups=self.texts,
            center_pos=True
        )

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
            pos=(TILE_SIZE * 26.5, TILE_SIZE * 5)
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

        # Sound Button
        self.sound_button = ImageButton(
            pos=(TILE_SIZE * 29.5, TILE_SIZE * 15.5)
            , main_color=COLORS["ButtonMain"]
            , second_color=COLORS["ButtonSecond"]
            , border_color=COLORS["ButtonBorder"]
            , image_path=PATHS["Icons"]["sound"]
            , size=(TILE_SIZE * 2, TILE_SIZE * 2)
            , group=self.buttons
            , func=self.switch_music
        )

        # Exit
        Button(
            pos=(TILE_SIZE * 25, TILE_SIZE * 15.5)
            , main_color=COLORS["ButtonMain"]
            , second_color=COLORS["ButtonSecond"]
            , text_color=COLORS["ButtonText"]
            , border_color=COLORS["ButtonBorder"]
            , text="EXIT"
            , font=pygame.font.SysFont('cambria', int(TILE_SIZE * 1.4))
            , size=(TILE_SIZE * 5.3, TILE_SIZE * 2)
            , group=self.buttons
            , func=self.game.exit
        )

        # ------------------------ Difficulty Text -------------------------------
        self.diff_text = Text(
            text="Difficulty",
            text_size=40,
            start_pos=(TILE_SIZE * 26.5, TILE_SIZE * 7),
            text_color=COLORS["LogoText"],
            groups=self.texts,
            center_pos=True
        )

        # ----------------------- Difficulty Buttons -----------------------------
        b1 = SelectButton(
            pos=(TILE_SIZE * 23.5, TILE_SIZE * 9)
            , main_color=COLORS["ButtonMain"]
            , second_color=COLORS["ButtonSecond"]
            , text_color=COLORS["ButtonText"]
            , border_color=COLORS["ButtonBorder"]
            , text="Easy"
            , font=pygame.font.SysFont('cambria', int(TILE_SIZE * 1.2))
            , size=(TILE_SIZE * 2.75, TILE_SIZE * 2)
            , group=(self.buttons, self.difficulty_buttons)
            , func=self.switch_difficulty
        )

        if self.game.current_data["Difficulty"] == 1:
            b1.select()

        b2 = SelectButton(
            pos=(TILE_SIZE * 26.5, TILE_SIZE * 9)
            , main_color=COLORS["ButtonMain"]
            , second_color=COLORS["ButtonSecond"]
            , text_color=COLORS["ButtonText"]
            , border_color=COLORS["ButtonBorder"]
            , text="Mid"
            , font=pygame.font.SysFont('cambria', int(TILE_SIZE * 1.2))
            , size=(TILE_SIZE * 2.75, TILE_SIZE * 2)
            , group=(self.buttons, self.difficulty_buttons)
            , func=self.switch_difficulty
        )
        if self.game.current_data["Difficulty"] == 2:
            b2.select()

        b3 = SelectButton(
            pos=(TILE_SIZE * 29.5, TILE_SIZE * 9)
            , main_color=COLORS["ButtonMain"]
            , second_color=COLORS["ButtonSecond"]
            , text_color=COLORS["ButtonText"]
            , border_color=COLORS["ButtonBorder"]
            , text="Hard"
            , font=pygame.font.SysFont('cambria', int(TILE_SIZE * 1.2))
            , size=(TILE_SIZE * 2.75, TILE_SIZE * 2)
            , group=(self.buttons, self.difficulty_buttons)
            , func=self.switch_difficulty
        )

        if self.game.current_data["Difficulty"] == 3:
            b3.select()

        # ------------------------ Speed Text -------------------------------
        self.speed_text = Text(
            text="Speed",
            text_size=40,
            start_pos=(TILE_SIZE * 26.5, TILE_SIZE * 11),
            text_color=COLORS["LogoText"],
            groups=self.texts,
            center_pos=True
        )

        # ----------------------- Speed Buttons -----------------------------
        b1 = SelectButton(
            pos=(TILE_SIZE * 23.5, TILE_SIZE * 13)
            , main_color=COLORS["ButtonMain"]
            , second_color=COLORS["ButtonSecond"]
            , text_color=COLORS["ButtonText"]
            , border_color=COLORS["ButtonBorder"]
            , text="Slow"
            , font=pygame.font.SysFont('cambria', int(TILE_SIZE * 1.2))
            , size=(TILE_SIZE * 2.75, TILE_SIZE * 2)
            , group=(self.buttons, self.speed_buttons)
            , func=self.switch_speed
        )
        if self.game.current_data["Speed"] == 1:
            b1.select()

        b2 = SelectButton(
            pos=(TILE_SIZE * 26.5, TILE_SIZE * 13)
            , main_color=COLORS["ButtonMain"]
            , second_color=COLORS["ButtonSecond"]
            , text_color=COLORS["ButtonText"]
            , border_color=COLORS["ButtonBorder"]
            , text="Mid"
            , font=pygame.font.SysFont('cambria', int(TILE_SIZE * 1.2))
            , size=(TILE_SIZE * 2.75, TILE_SIZE * 2)
            , group=(self.buttons, self.speed_buttons)
            , func=self.switch_speed
        )
        if self.game.current_data["Speed"] == 2:
            b2.select()

        b3 = SelectButton(
            pos=(TILE_SIZE * 29.5, TILE_SIZE * 13)
            , main_color=COLORS["ButtonMain"]
            , second_color=COLORS["ButtonSecond"]
            , text_color=COLORS["ButtonText"]
            , border_color=COLORS["ButtonBorder"]
            , text="Fast"
            , font=pygame.font.SysFont('cambria', int(TILE_SIZE * 1.2))
            , size=(TILE_SIZE * 2.75, TILE_SIZE * 2)
            , group=(self.buttons, self.speed_buttons)
            , func=self.switch_speed
        )
        if self.game.current_data["Speed"] == 3:
            b3.select()

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

    def switch_music(self):
        if self.game.music_status:
            self.game.stop_music()
        else:
            self.game.play_music()

    def switch_difficulty(self, select_button):
        if select_button.text == "Easy":
            diff = 1
        elif select_button.text == "Mid":
            diff = 2
        else:
            diff = 3

        for sprite in self.difficulty_buttons:
            if sprite.text != select_button.text:
                sprite.unselect()
            else:
                sprite.select()

        self.game.current_data["Difficulty"] = diff

    def switch_speed(self, select_button):
        if select_button.text == "Slow":
            speed = 1
        elif select_button.text == "Mid":
            speed = 2
        else:
            speed = 3

        for sprite in self.speed_buttons:
            if sprite.text != select_button.text:
                sprite.unselect()
            else:
                sprite.select()

        self.game.current_data["Speed"] = speed

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
            if TILE_SIZE * (
                    SCREEN_SIZE_IN_TILES[1] + int(SCREEN_SIZE_IN_TILES[1] / 3) - 1) - TILE_SIZE * 1 <= sprite.rect.y:
                sprite.rect.y = -TILE_SIZE * 2

        self.buttons.update(pygame.mouse.get_pos())

    def run(self):
        self.screen.fill(COLORS["BackGround"])

        # Line Under The logo
        pygame.draw.line(self.screen, '#bf8f30', self.logo_text.rect.bottomleft, self.logo_text.rect.bottomright, 2)
        # Line Under The Difficulty text
        pygame.draw.line(self.screen, '#bf8f30', self.diff_text.rect.bottomleft, self.diff_text.rect.bottomright, 2)
        # Line Under The Speed text
        pygame.draw.line(self.screen, '#bf8f30', self.speed_text.rect.bottomleft, self.speed_text.rect.bottomright, 2)

        # Groups
        self.tiles.draw(self.screen)
        self.texts.draw(self.screen)
        self.buttons.draw(self.screen)

        # Music line (Off / On)
        if not self.game.music_status:
            pygame.draw.line(self.screen, COLORS["Text"], self.sound_button.rect.topright,
                             self.sound_button.rect.bottomleft, 5)
