import pygame
from random import choice, randint

from class_player import Player
from class_text import MovingText, Text
from class_tile import Tile, MovingTile
from class_button import Button, ImageButton

from settings import *


class Level:
    def __init__(self, game):
        """
        Creating the Level Window and setup all the Variables


        :param game: Main object Reference ( Game Object )
        """
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

        # Particles
        self.particles = []

        # Exercises
        self.exercises_diff = self.game.current_data["Difficulty"]
        self.exercises = []
        self.wrong_answers = []
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


        # MiniGame
        self.minigame_status = False
        self.minigame_circle_data = {
            "Center": self.player.rect.center,
            "Radius": SCREEN_WIDTH
        }


    def setup(self):
        """
        Set up the View of Level
        """
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
        plat_size = (TILE_SIZE, TILE_SIZE/8)
        for i in [0, 6, 12, 18]:
            MovingTile(
                image=self.game.textures["Textures"]["platforms"][0],
                pos=[TILE_SIZE * 7, i * TILE_SIZE],
                y_change=self.blocks_speed,
                groups=[self.collide_sprites, self.visible_sprites, self.sprite_to_move],
                size=plat_size
            )

            MovingTile(
                image=self.game.textures["Textures"]["platforms"][2],
                pos=[TILE_SIZE * 19, i * TILE_SIZE],
                y_change=self.blocks_speed,
                groups=[self.collide_sprites, self.visible_sprites, self.sprite_to_move],
                size=plat_size
            )

            for j in [8, 9, 10, 16, 17, 18]:
                MovingTile(
                    image=self.game.textures["Textures"]["platforms"][1],
                    pos=[TILE_SIZE * j, i * TILE_SIZE],
                    y_change=self.blocks_speed,
                    groups=[self.collide_sprites, self.visible_sprites, self.sprite_to_move],
                    size=plat_size
                )

        # Start Platform
        for i in range(11, 16):
            MovingTile(
                image=self.game.textures["Textures"]["platforms"][1],
                pos=[TILE_SIZE * i, SCREEN_SIZE_IN_TILES[1] * TILE_SIZE - TILE_SIZE * 6],
                y_change=self.blocks_speed,
                groups=[self.collide_sprites, self.visible_sprites, self.sprite_to_move, self.start_platform_sprites],
                size=plat_size

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
                    groups=[self.visible_sprites, self.sprite_to_move] if i < 12 else [self.sprite_to_move]
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
                    groups=[self.visible_sprites, self.sprite_to_move] if i < 12 else [self.sprite_to_move]
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
                    groups=[self.visible_sprites, self.sprite_to_move] if i < 12 else [self.sprite_to_move]
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
        """
        Switching the Music by it current status.
        Turning on if it was off and conversely.


        """
        if self.game.music_status:
            self.game.stop_music()
        else:
            self.game.play_music()

    def set_answer_and_score(self, txt_class, status: bool):
        """
        Changing the score and lives by status.
        Changing the color of Text or MovingText class by stats


        :param txt_class: MovingText or Text to change color by status (Status = True -> Green, Status = False -> Red)
        :param status: Status of Player answer (True -> Correct, False -> Error)
        """

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
        """
        Creating exercises by difficulty.

        :return: List that represent exercises, only one of answers is correct. Structure -> [First_num, Second_num, math_operation, first_answer, second_answer]
        """

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
        """
        Adding new Exercises in self.exercises

        Exercises is list of MovingText Views. Structure -> [MovingText(5+5=), MovingText(10), MovingText(15)]
        """
        exersice = self.create_ex_basic()
        ex = []

        pos1 = [TILE_SIZE, -2 * TILE_SIZE - 1] if len(f"{exersice[0]} {exersice[2]} {exersice[1]} =") <= 8 else [TILE_SIZE * 0.25, -2 * TILE_SIZE - 1]
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
                start_pos=[TILE_SIZE * 8, -2 * TILE_SIZE - 1],
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
                start_pos=[TILE_SIZE * 16, -2 * TILE_SIZE - 1],
                y_change=self.blocks_speed,
                text_color=COLORS["Text"],
                groups=[self.visible_sprites, self.sprite_to_move]
            )
        )

        self.exercises.append(ex)

    def create_particles(self, sprite, color: str):
        """
        Adding in to self.particles new particles next to sprite.


        :param sprite: pygame.sprite.Sprite object.
        :param color: Color of particles.
        """
        for i in range(sprite.rect.left, sprite.rect.right, 3):
            self.particles.append([[i, sprite.rect.centery], [randint(0, 20) / 10 - 1, -2], randint(4, 12), color])

    def event_loop(self):
        """
        Get all player input on the level and update everything that depends on player input
        """
        events = pygame.event.get()

        # Level
        if not self.game_over_status and not self.minigame_status:
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

        elif self.minigame_status:
            for event in events:
                if event.type == pygame.QUIT:
                    self.game.running = False

        # Game over
        else:
            for event in events:
                if event.type == pygame.QUIT:
                    self.game.running = False

                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    self.game.restart_level()

    def game_over(self):
        """
        Set up screen for Game Over in self.game_over_screen and setting game_over_status to True.
        """
        self.game_over_status = True
        self.game_over_screen = self.screen.copy()

        # dark background
        darken_percent = 0.75
        dark = pygame.Surface(self.game_over_screen.get_size()).convert_alpha()
        dark.fill((0, 0, 0, darken_percent * 255))
        self.game_over_screen.blit(dark, (0, 0))

        # Text
        group = pygame.sprite.Group()
        Text(
            text="Press any button to restart",
            text_size=30,
            start_pos=(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 1.5 * TILE_SIZE),
            text_color=COLORS["Text"],
            groups=group,
            center_pos=True
        )

        txt = Text(
            text=f"Your Score: {self.score}!",
            text_size=80,
            start_pos=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 6 * TILE_SIZE),
            text_color=COLORS["Text"],
            groups=group,
            center_pos=True
        )


        if len(self.wrong_answers):
            ex_text_pos = (SCREEN_WIDTH / 2 - 8 * TILE_SIZE, SCREEN_HEIGHT / 2 - 4 * TILE_SIZE)
            ex_txt = Text(
                text="Exercise",
                text_size=50,
                start_pos=ex_text_pos,
                text_color=COLORS["Text"],
                groups=group,
            )
            pygame.draw.line(self.game_over_screen, COLORS["Text"], ex_txt.rect.bottomleft, ex_txt.rect.bottomright, 3)

            wrong_text_pos = (SCREEN_WIDTH / 2 - TILE_SIZE, SCREEN_HEIGHT / 2 - 4 * TILE_SIZE)
            wrong_txt = Text(
                text="Wrong",
                text_size=50,
                start_pos=[wrong_text_pos[0], wrong_text_pos[1]],
                text_color=COLORS["Text"],
                groups=group,
            )
            pygame.draw.line(self.game_over_screen, COLORS["Text"], wrong_txt.rect.bottomleft, wrong_txt.rect.bottomright, 3)


            correct_txt_pos = (SCREEN_WIDTH / 2 + 4 * TILE_SIZE, SCREEN_HEIGHT / 2 - 4 * TILE_SIZE)
            wrong_txt = Text(
                text="Correct",
                text_size=50,
                start_pos=[correct_txt_pos[0], correct_txt_pos[1]],
                text_color=COLORS["Text"],
                groups=group,
            )
            pygame.draw.line(self.game_over_screen, COLORS["Text"], wrong_txt.rect.bottomleft,
                             wrong_txt.rect.bottomright, 3)

            for index, wrong in enumerate(self.wrong_answers):
                # Exercises
                Text(
                    text=wrong[0],
                    text_size=50,
                    start_pos= (ex_text_pos[0], ex_text_pos[1] + 2.5 * TILE_SIZE + 1.5 * TILE_SIZE * index),
                    text_color=COLORS["Text"],
                    groups=group,
                )

                # Wrong Answers
                Text(
                    text=wrong[1].strip(),
                    text_size=50,
                    start_pos=[wrong_text_pos[0], wrong_text_pos[1] + 2.5 * TILE_SIZE + 1.5 * TILE_SIZE * index],
                    text_color=COLORS["TextError"],
                    groups=group,
                )

                # Wrong Answers
                t = Text(
                    text=wrong[2].strip(),
                    text_size=50,
                    start_pos=[correct_txt_pos[0], correct_txt_pos[1] + 2.5 * TILE_SIZE + 1.5 * TILE_SIZE * index],
                    text_color=COLORS["TextCorrect"],
                    groups=group,
                )



        pygame.draw.line(self.game_over_screen, COLORS["Text"], txt.rect.bottomleft, txt.rect.bottomright, 3)
        group.draw(self.game_over_screen)

    def reset_minigame(self):
        self.minigame_status = False
        self.minigame_circle_data = {
            "Center": self.player.rect.center,
            "Radius": SCREEN_WIDTH
        }


    def run(self):
        """
        Updating everything that not depends on player input and drawing all sprites on screen.
        """
        if not self.game_over_status and not self.minigame_status:
            # Update
            self.buttons.update(pygame.mouse.get_pos())

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

            # Check answer
            if not self.wait_mode:
                for sprite in self.current_ex_to_jump[1:]:
                    if self.player.rect.colliderect(sprite.rect):
                        if int(sprite.text) == eval(self.current_ex_to_jump[0].text[0:-2].replace("x", "*")):
                            self.set_answer_and_score(sprite, True)
                            self.create_particles(sprite, COLORS["Particles Correct"])
                        else:
                            self.wrong_answers.append([
                                self.current_ex_to_jump[0].text,
                                self.current_ex_to_jump[1].text if sprite == self.current_ex_to_jump[1] else self.current_ex_to_jump[2].text,
                                self.current_ex_to_jump[2].text if sprite != self.current_ex_to_jump[2] else self.current_ex_to_jump[1].text,
                            ])
                            self.set_answer_and_score(sprite, False)
                            self.create_particles(sprite, COLORS["Particles Error"])


                        for index, val in enumerate(self.exercises):
                            if val == self.current_ex_to_jump:
                                if len(self.exercises) > index + 1:
                                    if self.exercises[index] == self.current_ex_to_jump:
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

            # particles
            for particle in self.particles:
                particle[0][0] += particle[1][0]
                particle[0][1] += particle[1][1]
                particle[2] -= 0.1
                particle[1][1] += 0.1
                pygame.draw.circle(self.screen, particle[3], [int(particle[0][0]), int(particle[0][1])],
                                   int(particle[2]))
                if particle[2] <= 0:
                    self.particles.remove(particle)

            # Decor
            pygame.draw.line(self.screen, COLORS["Text"], self.score_view.rect.bottomleft,
                             self.score_view.rect.bottomright, 3)

            if not self.game.music_status:
                pygame.draw.line(self.screen, COLORS["Text"], self.sound_button.rect.topright,
                                 self.sound_button.rect.bottomleft, 5)



            # Create MiniGame
            if self.score % 10 == 0 and self.score != 0:
                if self.player.rect.centerx > 13.5 * TILE_SIZE:
                    self.player.rect.centerx = 17 * TILE_SIZE
                else:
                    self.player.rect.centerx = 10 * TILE_SIZE


                self.minigame_status = True

                self.minigame_circle_data = {
                    "Center": self.player.rect.center,
                    "Radius": SCREEN_WIDTH
                }

        elif self.minigame_status:
            if self.minigame_circle_data["Radius"] > 50:
                txt = pygame.font.SysFont(FONT_NAME, 150).render(str("Mini Game !!"), True, COLORS["Text"])
                txt_rect = txt.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
                pygame.draw.circle(self.screen, "Black", self.minigame_circle_data["Center"], self.minigame_circle_data["Radius"], 50)

                self.screen.blit(
                    txt, txt_rect
                )
                self.minigame_circle_data["Radius"] *= 0.98
            else:

                self.game.go_to_minigame()
        else:
            self.screen.blit(self.game_over_screen, (0, 0))
