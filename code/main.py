import pygame.mixer_music

from settings import *
from sys import exit

from support_functions import import_images

from window_minigame import MiniGame
from window_menu import Menu
from window_level import Level


class Game:
    def __init__(self):
        """
        Creating the Game
        """

        pygame.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption("Math Up!")
        self.clock = pygame.time.Clock()

        self.music_status = True
        pygame.mixer.music.load("../sound/main_music.mp3")
        pygame.mixer.music.set_volume(0.5)

        self.textures = import_images()
        self.running = True


        self.current_data = {
            "Difficulty": 1,
            "Speed": 1
        }
        self.window = Menu(self)

        self.level_save = None



    def run(self):
        """
        Running the game
        """

        while self.running:
            self.window.event_loop()
            self.window.run()


            self.clock.tick(60)
            pygame.display.update()


        pygame.quit()
        exit()

    def play_music(self):
        """
        Starting to play a Music
        """
        pygame.mixer.music.play(-1)
        self.music_status = True

    def stop_music(self):
        """
        Stopping to play a Music
        """
        pygame.mixer.music.stop()
        self.music_status = False


    def go_to_level(self):
        """
        Changing window to Level
        """
        self.window = Level(self)

    def go_to_menu(self):
        """
        Changing window to Menu
        """
        self.window = Menu(self)

    def restart_level(self):
        """
        Changing window to Level
        """
        self.window = Level(self)

    def go_to_minigame(self):
        """
        Changing window to MiniGame and saving to Level
        """

        self.level_save = self.window
        self.window = MiniGame(self)

    def back_to_level(self, score):
        self.window = self.level_save
        if score > 0:
            self.window.score += score
        else:
            self.window.score += 1
            self.window.lives -= 1

        self.window.score_view.change_text(f"Score : {self.window.score}")
        self.window.lives_view.change_text(f"Lives : {self.window.lives}")

        self.window.reset_minigame()

    def exit(self):
        """
        Closing The Game
        """
        self.running = False


if __name__ == "__main__":
    Game().run()
