import pygame

from settings import *


class MovingAnswer(pygame.sprite.Sprite):
    def __init__(self, answer: int, text_size: int, start_pos: tuple, start_y_speed: int, y_speed_change: int, text_color: str, main_color:str, border_color, background_color: int, radius:int, groups):
        super().__init__(groups)

        self.answer = answer

        self.speed = start_y_speed
        self.y_speed_change = y_speed_change

        self.image = pygame.Surface((radius*2, radius*2)).convert_alpha()
        self.image.fill(background_color)
        pygame.draw.circle(self.image, main_color, (radius, radius), radius)
        pygame.draw.circle(self.image, border_color, (radius, radius), radius , 2)


        txt = pygame.font.SysFont(FONT_NAME, text_size).render(str(answer), True, text_color)
        txt_rect = txt.get_rect(center=(radius, radius))
        self.image.blit(txt, txt_rect)


        self.rect = self.image.get_rect(center = start_pos)

    def update(self):
        self.rect.y += self.speed

        if self.speed < 60 * self.y_speed_change:
            self.speed += self.y_speed_change




    def get_collide(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)
