from settings import *


class Tile(pygame.sprite.Sprite):
    def __init__(self, image, pos: tuple, groups, name=None, size=None):
        """
        Creating a Tile View.
        Inheritance from pygame.sprite.Sprite


        :param image: pygame.image variable that sprite will represent
        :param pos: Top left position of image -> (x, y)
        :param groups: Groups to add a Sprite to -> Pygame.sprite.Group or list of Pygame.sprite.Group
        :param name: name of a Tile, does not affect
        :param size: Size of Tile -> (width, height)
        """
        super().__init__(groups)

        self.name = name

        self.image = image
        self.rect = self.image.get_rect(topleft=pos)
        if size is not None:
            self.rect.width = size[0]
            self.rect.height = size[1]





class MovingTile(Tile):
    def __init__(self,  image, pos: tuple, y_change: int, groups, size=None):
        """
        Creating a MovingTile View.
        Inheritance Tile


        :param image: pygame.image variable that sprite will represent
        :param pos: Top left position of image -> (x, y)
        :param y_change: y coordinate change per one frame
        :param groups: Groups to add a Sprite to -> Pygame.sprite.Group or list of Pygame.sprite.Group
        :param size: Size of Tile -> (width, height)

        """
        super().__init__(image, pos, groups, size=size)


        self.y_change = y_change


    def update(self):
        """
        Moving Tile to y_change value
        """

        self.rect.y = self.rect.y + self.y_change



