from settings import *


class Button(pygame.sprite.Sprite):
    def __init__(self, pos, main_color, second_color, text_color, border_color, text, font, size, group, func):
        super().__init__(group)
        self.status = False

        self.text = text
        self.font = font

        self.main_color = main_color
        self.second_color = second_color
        self.text_color = text_color
        self.border_color = border_color

        self.size = size

        # Press func
        self.func = func

        # --------- Sprite General ---------
        self.image = pygame.Surface(self.size)
        self.rect = self.image.get_rect(center=pos)

        # --------- Setup ---------
        # BackGround
        self.background_image = pygame.Surface((self.size[0] - 6, self.size[1] - 6))
        self.background_image.fill(self.main_color)
        self.background_rect = self.background_image.get_rect(topleft=(3, 3))

        # text
        self.text_image = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_image.get_rect(center=(self.size[0] / 2, self.size[1] / 2))

        # ------- Draw Button ----------
        self.image.fill(self.border_color)  # border
        self.image.blit(self.background_image, self.background_rect)  # background
        self.image.blit(self.text_image, self.text_rect)  # text

        # ----- For Update -----
        self.background_second_image = pygame.Surface((self.size[0] - 6, self.size[1] - 6))
        self.background_second_image.fill(self.second_color)
        self.background_second_rect = self.background_second_image.get_rect(topleft=(3, 3))

    def call_function(self):
        self.func()

    def update(self, mouse_pos):
        if not self.status and self.rect.collidepoint(mouse_pos):
            self.image.fill(self.border_color)  # border
            self.image.blit(self.background_second_image, self.background_second_rect)  # background
            self.image.blit(self.text_image, self.text_rect)  # text
            self.status = True
        elif self.status and not self.rect.collidepoint(mouse_pos):
            self.image.fill(self.border_color)  # border
            self.image.blit(self.background_image, self.background_rect)  # background
            self.image.blit(self.text_image, self.text_rect)  # text
            self.status = False
