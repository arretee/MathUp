from settings import *


class MovingText(pygame.sprite.Sprite):
    def __init__(self, text, text_size, start_pos, y_change, text_color, groups):
        super().__init__(groups)

        self.y_change = y_change

        self.image = pygame.font.SysFont(FONT_NAME, text_size).render(text, True, text_color)
        self.rect = self.image.get_rect(topleft = start_pos)


    def update(self):
        self.rect.y = self.rect.y + self.y_change

