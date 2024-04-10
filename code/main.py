from settings import *
from sys import exit

from support_functions import import_images

from window_menu import Menu
from window_level import Level


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption("Math Up!")
        self.clock = pygame.time.Clock()

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


    def go_to_level(self):
        self.window = Level(self)


if __name__ == "__main__":
    Game().run()
