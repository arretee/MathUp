import pygame
from random import choice, randint

from class_player import Player
from class_text import MovingText, Text
from class_tile import Tile, MovingTile
from class_button import Button, ImageButton

from settings import *


class Level:
    def __init__(self, game):
        # Basic
        self.game = game
        self.screen = self.game.screen

        self.started = False
        self.blocks_speed = LEVEL_Y_BLOCKS_SPEED[self.game.current_data["Speed"]]

        # Groups
        self.buttons = pygame.sprite.Group()

        self.collide_sprites = pygame.sprite.Group()
        self.visible_sprites = pygame.sprite.Group()

        self.sprite_to_move = pygame.sprite.Group()
        self.start_platform_sprites = pygame.sprite.Group()

        # Sounds
        self.sound_button = None


        # Exercises
        self.exercises_diff = self.game.current_data["Difficulty"]
        self.exercises = []
        self.setup()

        self.current_ex_to_jump = self.exercises[2]
        self.wait_mode = False

        # Game Over
        self.game_over_status = False
        self.game_over_screen = None


        # Statistic
        self.score = 0
        self.score_view = Text(f"Score : {self.score}", 70, (TILE_SIZE * 23.5, TILE_SIZE * 2), COLORS["Text"],
                               self.visible_sprites)
        self.lives = 3
        self.lives_view = Text(f"Lives : {self.lives}", 40, (TILE_SIZE * 23.5, TILE_SIZE * 6), COLORS["Text"],
                               self.visible_sprites)


        # Player
        self.player = Player(self.game, (TILE_SIZE * 13.5, TILE_SIZE * 11), self.collide_sprites)


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
                y_change=self.blocks_speed,
                groups=[self.collide_sprites, self.visible_sprites, self.sprite_to_move]
            )

            MovingTile(
                image=choice(self.game.textures["Textures"]["blocks"][1:]),
                pos=[TILE_SIZE * 20, TILE_SIZE * i],
                y_change=self.blocks_speed,
                groups=[self.collide_sprites, self.visible_sprites, self.sprite_to_move]
            )

        # Platforms
        for i in [0, 6, 12, 18]:
            MovingTile(
                image=self.game.textures["Textures"]["platforms"][0],
                pos=[TILE_SIZE * 7, i * TILE_SIZE],
                y_change=self.blocks_speed,
                groups=[self.collide_sprites, self.visible_sprites, self.sprite_to_move]
            )

            MovingTile(
                image=self.game.textures["Textures"]["platforms"][2],
                pos=[TILE_SIZE * 19, i * TILE_SIZE],
                y_change=self.blocks_speed,
                groups=[self.collide_sprites, self.visible_sprites, self.sprite_to_move]
            )

            for j in [8, 9, 10, 16, 17, 18]:
                MovingTile(
                    image=self.game.textures["Textures"]["platforms"][1],
                    pos=[TILE_SIZE * j, i * TILE_SIZE],
                    y_change=self.blocks_speed,
                    groups=[self.collide_sprites, self.visible_sprites, self.sprite_to_move]
                )

        # Start Platform
        for i in range(11, 16):
            MovingTile(
                image=self.game.textures["Textures"]["platforms"][1],
                pos=[TILE_SIZE * i, SCREEN_SIZE_IN_TILES[1] * TILE_SIZE - TILE_SIZE * 6],
                y_change=self.blocks_speed,
                groups=[self.collide_sprites, self.visible_sprites, self.sprite_to_move, self.start_platform_sprites]
            )

        # Exercises
        for i in [18, 12, 6, 0]:
            exersice = self.create_ex_basic()
            ex = []
            pos1 = [TILE_SIZE, -2 * TILE_SIZE + TILE_SIZE * i] if len(f"{exersice[0]} {exersice[2]} {exersice[1]} =") <= 8 else [
                TILE_SIZE * 0.25, -2 * TILE_SIZE + TILE_SIZE * i]
            ex.append(
                MovingText(
                    text=f"{exersice[0]} {exersice[2]} {exersice[1]} = ",
                    text_size=60,
                    start_pos=pos1,
                    y_change=self.blocks_speed,
                    text_color=COLORS["Text"],
                    groups=[self.visible_sprites, self.sprite_to_move]
                )
            )

            if len(str(exersice[3])) == 1:
                st = "     "
            elif len(str(exersice[3])) == 2:
                st = "   "
            elif len(str(exersice[3])) == 3:
                st = " "
            else:
                st = ""
            ex.append(
                MovingText(
                    text=str(exersice[3]) + st,
                    text_size=60,
                    start_pos=[TILE_SIZE * 8, -2 * TILE_SIZE + TILE_SIZE * i],
                    y_change=self.blocks_speed,
                    text_color=COLORS["Text"],
                    groups=[self.visible_sprites, self.sprite_to_move]
                )
            )

            if len(str(exersice[4])) == 1:
                st = "     "
            elif len(str(exersice[4])) == 2:
                st = "   "
            elif len(str(exersice[4])) == 3:
                st = " "
            else:
                st = ""
            ex.append(
                MovingText(
                    text=st + str(exersice[4]),
                    text_size=60,
                    start_pos=[TILE_SIZE * 16, -2 * TILE_SIZE + TILE_SIZE * i],
                    y_change=self.blocks_speed,
                    text_color=COLORS["Text"],
                    groups=[self.visible_sprites, self.sprite_to_move]
                )
            )

            self.exercises.append(ex)

        # ------------------------ Buttons ------------------------
        # Back
        Button(
            pos=(TILE_SIZE * 25, TILE_SIZE * 15.5)
            , main_color=COLORS["ButtonMain"]
            , second_color=COLORS["ButtonSecond"]
            , text_color=COLORS["ButtonText"]
            , border_color=COLORS["ButtonBorder"]
            , text="Back"
            , font=pygame.font.SysFont('cambria', int(TILE_SIZE * 1.4))
            , size=(TILE_SIZE * 5.3, TILE_SIZE * 2)
            , group=self.buttons
            , func=self.game.go_to_menu
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

    def switch_music(self):
        if self.game.music_status:
            self.game.stop_music()
        else:
            self.game.play_music()

    def set_answer_and_score(self, txt_class, status):
        if status:
            self.score += 1
        else:
            self.lives -= 1
            if self.lives == -1:
                self.game_over()

        self.score_view.change_text(f"Score : {self.score}")
        self.lives_view.change_text(f"Lives : {self.lives}")
        txt_class.change_color_to(COLORS["TextCorrect"] if status else COLORS["TextError"])

    def create_ex_basic(self):
        if self.exercises_diff == 1:
            x = randint(1, 10)
            y = randint(1, 10)

            action = randint(1, 2)
            action_txt = ""
            if action == 1:
                action_txt = "+"
            if action == 2:
                action_txt = "-"

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

                incorrect = first + randint(-5, 5)
                if incorrect == first or incorrect < 0:
                    second = first + randint(1, 5)
                else:
                    second = incorrect
            else:
                if action == 1:
                    second = x + y
                elif action == 2:
                    second = x - y
                else:
                    second = x * y

                incorrect = second + randint(-5, 5)
                if incorrect == second or incorrect < 0:
                    first = second + randint(1, 5)
                else:
                    first = incorrect

            return [x, y, action_txt, first, second]

        elif self.exercises_diff == 2:
            x = randint(1, 10)
            y = randint(1, 10)

            action = randint(1, 7)
            action_txt = ""
            if action == 1:
                action_txt = "+"
            if action == 2:
                action_txt = "-"
            if action >= 3:
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
                if incorrect == first or incorrect < 0:
                    second = first + randint(1, 20)
                else:
                    second = incorrect
            else:
                if action == 1:
                    second = x + y
                elif action == 2:
                    second = x - y
                else:
                    second = x * y

                incorrect = second + randint(-20, 20)
                if incorrect == second or incorrect < 0:
                    first = second + randint(1, 20)
                else:
                    first = incorrect

            return [x, y, action_txt, first, second]

        else:
            x = randint(1, 50)
            y = randint(1, 30)

            action = randint(1, 6)
            action_txt = ""
            if action == 1:
                action_txt = "+"
            if action == 2:
                action_txt = "-"
            if action >= 3:
                action_txt = "x"

            if randint(1, 2) == 2:
                if action == 1:
                    first = x + y
                elif action == 2:
                    first = x - y
                else:
                    first = x * y

                incorrect = first + randint(-50, 50)
                if incorrect == first:
                    second = first + randint(1, 50)
                else:
                    second = incorrect
            else:
                if action == 1:
                    second = x + y
                elif action == 2:
                    second = x - y
                else:
                    second = x * y

                incorrect = second + randint(-50, 50)
                if incorrect == second:
                    first = second + randint(1, 50)
                else:
                    first = incorrect

            return [x, y, action_txt, first, second]

    def add_new_ex(self):
        exersice = self.create_ex_basic()
        ex = []

        pos1 = [TILE_SIZE, -2 * TILE_SIZE] if len(f"{exersice[0]} {exersice[2]} {exersice[1]} =") <= 8 else [TILE_SIZE * 0.25, -2 * TILE_SIZE]
        ex.append(
            MovingText(
                text=f"{exersice[0]} {exersice[2]} {exersice[1]} = ",
                text_size=60,
                start_pos=pos1,
                y_change=self.blocks_speed,
                text_color=COLORS["Text"],
                groups=[self.visible_sprites, self.sprite_to_move]
            )
        )

        if len(str(exersice[3])) == 1:
            st = "     "
        elif len(str(exersice[3])) == 2:
            st = "   "
        elif len(str(exersice[3])) == 3:
            st = " "
        else:
            st = ""
        ex.append(
            MovingText(
                text=str(exersice[3]) + st,
                text_size=60,
                start_pos=[TILE_SIZE * 8, -2 * TILE_SIZE],
                y_change=self.blocks_speed,
                text_color=COLORS["Text"],
                groups=[self.visible_sprites, self.sprite_to_move]
            )
        )

        if len(str(exersice[4])) == 1:
            st = "     "
        elif len(str(exersice[4])) == 2:
            st = "   "
        elif len(str(exersice[4])) == 3:
            st = " "
        else:
            st = ""
        ex.append(
            MovingText(
                text=st + str(exersice[4]),
                text_size=60,
                start_pos=[TILE_SIZE * 16, -2 * TILE_SIZE],
                y_change=self.blocks_speed,
                text_color=COLORS["Text"],
                groups=[self.visible_sprites, self.sprite_to_move]
            )
        )

        self.exercises.append(ex)

    def event_loop(self):
        events = pygame.event.get()

        if not self.game_over_status:
            self.player.update(events)

            for event in events:
                if event.type == pygame.QUIT:
                    self.game.running = False

                if event.type == pygame.KEYDOWN:
                    self.started = True

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    for sprite in self.buttons.sprites():
                        if sprite.rect.collidepoint(mouse_pos):
                            sprite.call_function()

        else:
            for event in events:
                if event.type == pygame.QUIT:
                    self.game.running = False

                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    self.game.restart_level()

    def game_over(self):
        self.game_over_status = True
        self.game_over_screen = self.screen.copy()

        # dark background
        darken_percent = 0.50
        dark = pygame.Surface(self.game_over_screen.get_size()).convert_alpha()
        dark.fill((0, 0, 0, darken_percent * 255))
        self.game_over_screen.blit(dark, (0, 0))

        # Text
        group = pygame.sprite.Group()
        txt = Text(
            text="Press any button to restart",
            text_size=80,
            start_pos=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2),
            text_color=COLORS["Text"],
            groups=group,
            center_pos=True
        )

        group.draw(self.game_over_screen)

    def run(self):

        if not self.game_over_status:
            # Update
            self.buttons.update(pygame.mouse.get_pos())

            if self.started:
                self.sprite_to_move.update()

                for sprite in self.sprite_to_move.sprites():
                    if type(sprite) != MovingText:
                        if TILE_SIZE * (SCREEN_SIZE_IN_TILES[1] + int(SCREEN_SIZE_IN_TILES[1] / 3) - 1) < sprite.rect.y:
                            sprite.rect.y = -TILE_SIZE

                    else:
                        if TILE_SIZE * (SCREEN_SIZE_IN_TILES[1] + int(
                                SCREEN_SIZE_IN_TILES[1] / 3) - 1) - TILE_SIZE * 1 <= sprite.rect.y:
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

            # Check answer
            if not self.wait_mode:
                for sprite in self.current_ex_to_jump[1:]:
                    if self.player.rect.colliderect(sprite.rect):
                        if int(sprite.text) == eval(self.current_ex_to_jump[0].text[0:-2].replace("x", "*")):
                            self.set_answer_and_score(sprite, True)
                        else:
                            self.set_answer_and_score(sprite, False)

                        for index, val in enumerate(self.exercises):
                            if val == self.current_ex_to_jump:
                                if len(self.exercises) < index + 1:
                                    self.current_ex_to_jump = self.exercises[index + 1]
                                    break

                                else:
                                    self.wait_mode = True
                                    break

            # Check if player in wait mode and update the ex
            if self.wait_mode and self.current_ex_to_jump != self.exercises[-1]:
                self.wait_mode = False
                self.current_ex_to_jump = self.exercises[-1]

            # Game Over
            if self.player.rect.top > SCREEN_HEIGHT:
                self.game_over()

            # Draw
            self.screen.fill(COLORS["BackGround"])
            self.buttons.draw(self.screen)

            # Level
            self.visible_sprites.draw(self.screen)
            self.player.draw()

            # Decor
            pygame.draw.line(self.screen, COLORS["Text"], self.score_view.rect.bottomleft,
                             self.score_view.rect.bottomright, 3)

            if not self.game.music_status:
                pygame.draw.line(self.screen, COLORS["Text"], self.sound_button.rect.topright,
                                 self.sound_button.rect.bottomleft, 5)


        else:
            self.screen.blit(self.game_over_screen, (0, 0))
