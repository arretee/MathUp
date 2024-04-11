import pygame.mixer_music

from settings import *
from sys import exit

from support_functions import import_images

from window_menu import Menu
from window_level import Level


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption("Math Up!")
        self.clock = pygame.time.Clock()

        self.music_status = True
        pygame.mixer.music.load("../sound/main_music.mp3")
        pygame.mixer.music.set_volume(0.1)

        self.textures = import_images()
        self.running = True
        self.window = Menu(self)


    def run(self):
        while self.running:
            self.window.event_loop()
            self.window.run()


            self.clock.tick(60)
            pygame.display.update()


        pygame.quit()
        exit()

    def play_music(self):
        pygame.mixer.music.play(-1)
        self.music_status = True

    def stop_music(self):
        pygame.mixer.music.stop()
        self.music_status = False


    def go_to_level(self):
        self.window = Level(self)

    def go_to_menu(self):
        self.window = Menu(self)

    def restart_level(self):
        self.window = Level(self)

    def exit(self):
        self.running = False


if __name__ == "__main__":
    Game().run()
