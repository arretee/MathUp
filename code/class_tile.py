from settings import *


class Tile(pygame.sprite.Sprite):
    def __init__(self, image, pos, groups, name = None):
        super().__init__(groups)

        self.name = name

        self.image = image
        self.rect = self.image.get_rect(topleft=pos)



class MovingTile(Tile):
    def __init__(self,  image, pos, y_change, groups):
        super().__init__(image, pos, groups)

        self.y_change = y_change


    def update(self):
        self.rect.y = self.rect.y + self.y_change



