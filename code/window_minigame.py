import pygame.event

from class_text import Text
from class_moving_answer import MovingAnswer

from random import randint, choice, shuffle

from settings import *


class MiniGame:
    def __init__(self, game):
        self.game = game
        self.level = self.game.level_save

        self.screen = self.game.screen
        self.visible_sprites = pygame.sprite.Group()

        # Create first ex
        self.exercise = None
        self.exercises_diff = self.game.current_data["Difficulty"]
        self.answers = pygame.sprite.Group()

        self.set_new_ex()

        # ComeBackToLevel
        self.status = None
        self.comeback_circle_data = {
            "Center": (SCREEN_WIDTH/2, SCREEN_HEIGHT/2),
            "Radius": SCREEN_WIDTH
        }

    def set_new_ex(self):
        ex = self.create_ex()

        self.exercise = Text(
            text=f"{ex[0]} {ex[2]} {ex[1]} = ?",
            text_size=80,
            start_pos=(SCREEN_WIDTH / 2, TILE_SIZE * 2),
            text_color=COLORS["Text"],
            groups=[self.visible_sprites],
            center_pos=True
        )

        shuffle(ex[-1])

        for index, ans in enumerate(ex[-1]):
            MovingAnswer(
                answer=ans,
                text_size=100,
                start_pos=(SCREEN_WIDTH/2 - 10 * TILE_SIZE + index * TILE_SIZE * 5, SCREEN_HEIGHT + 75),
                start_y_speed=-10,
                y_speed_change=0.1,
                text_color=COLORS["Text"],
                main_color=COLORS["Circle Main"],
                border_color=COLORS["Circle Border"],
                background_color=COLORS["BackGround"],
                radius=75,
                groups=[self.visible_sprites, self.answers]
            )

    def create_ex(self):
        """
                Creating exercises by difficulty.

                :return: List that represent exercises, only one of answers is correct. Structure -> [First_num, Second_num, math_operation, [answer_variants]]
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

            if action == 1:
                answer = x + y
            if action == 2:
                answer = x - y

            wrong_ans = [answer]
            for i in range(2):
                wrong_ans.append(answer + randint(1, 10))
            for i in range(2):
                wrong_ans.append(answer + randint(-10, -1))

            return [x, y, action_txt, wrong_ans]

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

            if action == 1:
                answer = x + y
            if action == 2:
                answer = x - y
            if action >= 3:
                answer = x * y

            wrong_ans = [answer]
            for i in range(2):
                wrong_ans.append(answer + randint(1, 10))
            for i in range(2):
                wrong_ans.append(answer + randint(-10, -1))

            return [x, y, action_txt, wrong_ans]

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

            if action == 1:
                answer = x + y
            if action == 2:
                answer = x - y
            if action >= 3:
                answer = x * y

            wrong_ans = [answer]
            for i in range(2):
                wrong_ans.append(answer + randint(1, 10))
            for i in range(2):
                wrong_ans.append(answer + randint(-10, -1))

            return [x, y, action_txt, wrong_ans]

    def event_loop(self):
        events = pygame.event.get()
        if self.status is None:
            self.answers.update()

        for event in events:
            if event.type == pygame.QUIT:
                self.game.running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                for sprite in self.answers.sprites():
                    if sprite.rect.collidepoint(mouse_pos):
                        self.check_answer(sprite)
                        break

        for sprite in self.answers.sprites():
            if sprite.rect.y > SCREEN_HEIGHT:
                self.status = False
                break

    def check_answer(self, sprite):
        if sprite.answer == eval(self.exercise.text[:-3]):
            self.status = True
        else:
            self.status = False

    def run(self):
        if self.status is None:
            # Draw
            self.screen.fill(COLORS["BackGround"])

            self.visible_sprites.draw(self.screen)
        else:
            if self.comeback_circle_data["Radius"] > 50:
                txt = pygame.font.SysFont(FONT_NAME, 60).render(str("Good Job, Back To Level, Be Ready!!" if self.status else "Wrong answer, Back To Level, Be Ready!!"), True, COLORS["Text"])
                txt_rect = txt.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
                pygame.draw.circle(self.screen, "Black", self.comeback_circle_data["Center"], self.comeback_circle_data["Radius"], 50)

                self.screen.blit(
                    txt, txt_rect
                )
                self.comeback_circle_data["Radius"] *= 0.98
            else:
                # Correct
                if self.status:
                    self.game.back_to_level(1)
                # InCorrect
                else:
                    self.game.back_to_level(-1)
