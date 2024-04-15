import pygame

from settings import *


class Button(pygame.sprite.Sprite):
    def __init__(self, pos: tuple, main_color: str, second_color: str, text_color: str, border_color: str, text: str, font: pygame.font.FontType, size: tuple, group, func):
        """
        Creating a Button.
        Inheritance from pygame.sprite.Sprite


        :param pos: position of top left point of button -> (x, y)
        :param main_color: HEX of background color of a button
        :param second_color: HEX of background second color of a button (When mouse on a button)
        :param text_color: HEX of text color on a button
        :param border_color: HEX of border color of a button
        :param text: Text that button will show to a user
        :param font: Font of a Text -> pygame.font.SysFont
        :param size: Size of a button -> (Width, Height)
        :param group: Groups to add a Sprite to -> Pygame.sprite.Group or list of Pygame.sprite.Group
        :param func: Function that button will call on a function "call_function" -> function reference
        """

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
        self.text_image = self.font.render(str(self.text), True, self.text_color)
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
        """
            calling a function that saved in self.func
        """
        self.func()

    def update(self, mouse_pos: tuple):
        """
        Updating the View of Button if mouse on a button or not.

        :param mouse_pos: Mouse pos on screen -> tuple (x, y)
        """

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


class ImageButton(pygame.sprite.Sprite):
    def __init__(self, pos: tuple, main_color: str, second_color: str, border_color: str, image_path: str, size: tuple,
                 group, func):
        """
        Creating a ImageButton.
        Inheritance from pygame.sprite.Sprite


        :param pos: position of top left point of button -> (x, y)
        :param main_color: HEX of background color of a button
        :param second_color: HEX of background second color of a button (When mouse on a button)
        :param border_color: HEX of border color of a button
        :param image_path: Path of image that button represent
        :param size: Size of a button -> (Width, Height)
        :param group: Groups to add a Sprite to -> Pygame.sprite.Group or list of Pygame.sprite.Group
        :param func: Function that button will call on a function "call_function" -> function reference
        """

        super().__init__(group)
        self.status = False

        self.main_color = main_color
        self.second_color = second_color
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

        # image
        self.img = pygame.image.load(image_path).convert_alpha()
        self.img = pygame.transform.scale(self.img, (self.size[0] - 6, self.size[1] - 6))
        self.img_rect = self.img.get_rect(center=(self.size[0] / 2, self.size[1] / 2))

        # ------- Draw Button ----------
        self.image.fill(self.border_color)  # border
        self.image.blit(self.background_image, self.background_rect)  # background
        self.image.blit(self.img, self.img_rect)  # text

        # ----- For Update -----
        self.background_second_image = pygame.Surface((self.size[0] - 6, self.size[1] - 6))
        self.background_second_image.fill(self.second_color)
        self.background_second_rect = self.background_second_image.get_rect(topleft=(3, 3))

    def call_function(self):
        """
            calling a function that saved in self.func
        """
        self.func()

    def update(self, mouse_pos: tuple):
        """
        Updating the View of Button if mouse on a button or not.

        :param mouse_pos: Mouse pos on screen -> tuple (x, y)
        """
        if not self.status and self.rect.collidepoint(mouse_pos):
            self.image.fill(self.border_color)  # border
            self.image.blit(self.background_second_image, self.background_second_rect)  # background
            self.image.blit(self.img, self.img_rect)  # text
            self.status = True
        elif self.status and not self.rect.collidepoint(mouse_pos):
            self.image.fill(self.border_color)  # border
            self.image.blit(self.background_image, self.background_rect)  # background
            self.image.blit(self.img, self.img_rect)  # text
            self.status = False


class SelectButton(Button):
    def __init__(self, pos: tuple, main_color: str, second_color: str, text_color: str, border_color: str, text: str, font: pygame.font.FontType, size: tuple, group, func):
        """
        Creating a SelectButton.
        Inheritance from Button


        :param pos: position of top left point of button -> (x, y)
        :param main_color: HEX of background color of a button
        :param second_color: HEX of background second color of a button (When mouse on a button)
        :param text_color: HEX of text color on a button
        :param border_color: HEX of border color of a button
        :param text: Text that button will show to a user
        :param font: Font of a Text -> pygame.font.SysFont
        :param size: Size of a button -> (Width, Height)
        :param group: Groups to add a Sprite to -> Pygame.sprite.Group or list of Pygame.sprite.Group
        :param func: Function that button will call on a function "call_function" -> function reference
        """
        super().__init__(pos, main_color, second_color, text_color, border_color, text, font, size, group, func)

        self.selected = False

    def select(self):
        """
            Selecting a button and change the View of a button
        """
        self.selected = True
        self.image.fill(self.border_color)  # border
        self.image.blit(self.background_second_image, self.background_second_rect)  # background
        self.image.blit(self.text_image, self.text_rect)  # text

    def unselect(self):
        """
            Unselecting a button and change the View of a button
        """
        self.selected = False
        self.image.fill(self.border_color)  # border
        self.image.blit(self.background_image, self.background_rect)  # background
        self.image.blit(self.text_image, self.text_rect)  # text

    def call_function(self):
        """
            calling a function that saved in self.func and like param give self
        """
        self.func(self)

    def update(self, mouse_pos: tuple):
        """
        Updating the View of Button if mouse on a button or not.

        :param mouse_pos: Mouse pos on screen -> tuple (x, y)
        """
        if not self.selected:
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
