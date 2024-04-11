from settings import *


class MovingText(pygame.sprite.Sprite):
    def __init__(self, text, text_size, start_pos, y_change, text_color, groups):
        super().__init__(groups)
        self.text = text
        self.text_size = text_size


        self.y_change = y_change

        self.image = pygame.font.SysFont(FONT_NAME, text_size).render(text, True, text_color)
        self.rect = self.image.get_rect(topleft = start_pos)


    def update(self):
        self.rect.y = self.rect.y + self.y_change

    def change_color_to(self, color):
        self.image = pygame.font.SysFont(FONT_NAME, self.text_size).render(self.text, True, color)



class Text(pygame.sprite.Sprite):
    def __init__(self, text, text_size, start_pos, text_color, groups, center_pos = False):
        super().__init__(groups)
        self.text = text
        self.text_size = text_size
        self.text_color = text_color

        self.image = pygame.font.SysFont(FONT_NAME, text_size).render(text, True, text_color)
        if not center_pos:
            self.rect = self.image.get_rect(topleft=start_pos)
        else:
            self.rect = self.image.get_rect(center=start_pos)

    def change_text(self, text):
        self.text = text
        self.image = pygame.font.SysFont(FONT_NAME, self.text_size).render(self.text, True, self.text_color)
        self.rect = self.image.get_rect(topleft=self.rect.topleft)
