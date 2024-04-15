from settings import *


class MovingText(pygame.sprite.Sprite):
    def __init__(self, text: str, text_size: int, start_pos: tuple, y_change: int, text_color: str, groups):
        """
        Creating a MovingText View.
        Inheritance from pygame.sprite.Sprite


        :param text: Text that user will see on the screen
        :param text_size: Size of a text that user will see
        :param start_pos: top left position where object will start -> tuple (x, y)
        :param y_change: y coordinate change per one frame
        :param text_color: HEX of text color
        :param groups:Groups to add a Sprite to -> Pygame.sprite.Group or list of Pygame.sprite.Group
        """

        super().__init__(groups)
        self.text = text
        self.text_size = text_size

        self.y_change = y_change

        self.image = pygame.font.SysFont(FONT_NAME, text_size).render(text, True, text_color)
        self.rect = self.image.get_rect(topleft=start_pos)

    def update(self):
        """
        Moving text to y_change value
        """

        self.rect.y = self.rect.y + self.y_change

    def change_color_to(self, color: str):
        """

        :param color: HEX of text color will change on -> String
        """

        self.image = pygame.font.SysFont(FONT_NAME, self.text_size).render(self.text, True, color)


class Text(pygame.sprite.Sprite):
    def __init__(self, text: str, text_size: int, start_pos: tuple, text_color: str, groups, center_pos=False):

        """
        Creating a Text View.
        Inheritance from pygame.sprite.Sprite



        :param text: Text that user will see on the screen
        :param text_size: Size of a text that user will see
        :param start_pos: top left position where object will start -> tuple (x, y)
        :param text_color: HEX of text color
        :param groups:Groups to add a Sprite to -> Pygame.sprite.Group or list of Pygame.sprite.Group
        """
        super().__init__(groups)
        self.text = text
        self.text_size = text_size
        self.text_color = text_color

        self.image = pygame.font.SysFont(FONT_NAME, text_size).render(text, True, text_color)
        if not center_pos:
            self.rect = self.image.get_rect(topleft=start_pos)
        else:
            self.rect = self.image.get_rect(center=start_pos)

    def change_text(self, text: str):
        """
        Changing text on View.

        :param text: text that View will change on
        """


        self.text = text
        self.image = pygame.font.SysFont(FONT_NAME, self.text_size).render(self.text, True, self.text_color)
        self.rect = self.image.get_rect(topleft=self.rect.topleft)
