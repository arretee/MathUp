import pygame

from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, game, pos: tuple, collide_sprites):
        """
        Creating a player.
        Inheritance from pygame.sprite.Sprite


        :param game: Reference to Game object
        :param pos: Player start position on screen -> (x, y)
        :param collide_sprites: pygame.sprite.Group of all sprites to check collision with
        """



        super().__init__()
        # Basic
        self.game = game
        self.screen = game.screen
        self.collide_sprites = collide_sprites

        # Movement
        self.direction = pygame.math.Vector2()
        self.status = "idle"
        self.facing = "left"
        self.onGround = False

        # Animations
        self.animation_index = 0
        self.animation_speed = ANIMATION_SPEED
        self.animation = self.game.textures["Character"][self.status]

        # General
        self.image = self.game.textures["Character"][self.status][0]
        self.rect = self.image.get_rect(center=pos)



    def event_loop(self, events: list):
        """
        Getting all player input


        :param events: list of events from type pygame.Event
        """


        keys = pygame.key.get_pressed()

        for event in events:
            if event.type == pygame.KEYDOWN:
                # Jump
                if (event.key == pygame.K_SPACE or event.key == pygame.K_UP or event.key == pygame.K_w) and self.onGround:
                    self.jump()

        # Movement
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.facing = "left"
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.facing = "right"
        else:
            self.direction.x = 0

        if self.status == "idle" and self.direction.x != 0:
            self.status = "run"
            self.switch_stasuses()
        elif self.status == "run" and self.direction.x == 0:
            self.status = "idle"
            self.switch_stasuses()

    def jump(self):
        """
        Changing player y direction by JUMP_SPEED_BY_SPEED
        """
        if self.onGround:
            self.onGround = False
            self.direction.y = JUMP_SPEED_BY_SPEED[self.game.current_data["Speed"]]

    def gravity(self):
        """
        Changing Gravity by GRAVITY
        """
        if round(self.direction.y) == 0:
            self.direction.y = LEVEL_Y_BLOCKS_SPEED[self.game.current_data["Speed"]]
        self.direction.y += GRAVITY

    def move(self, speed: int):
        """
        Moving a player and checking collision with collide_sprites


        :param speed: player horizontal speed (positive number = moving right)
        """

        self.rect.y += int(self.direction.y)
        self.collision('vertical')
        self.rect.x += int(self.direction.x * speed)
        self.collision('horizontal')


    def collision(self, direction: str):
        """
        Checking collision by direction with collide_sprites and changing player pos if player collide with sprites.


        :param direction: getting direction of movement ( "horizontal" or "vertical" )
        """

        if direction == 'horizontal':
            for sprite in self.collide_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.x > 0:
                        if sprite.rect.left - self.rect.right < 5:
                            self.rect.right = sprite.rect.left
                            self.direction.x = 0

                    elif self.direction.x < 0:
                        if sprite.rect.right - self.rect.left > -5:
                            self.rect.left = sprite.rect.right
                            self.direction.x = 0

        if direction == 'vertical':
            for sprite in self.collide_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.y > 0:
                        self.rect.bottom = sprite.rect.top
                        self.direction.y = 0
                        self.onGround = True

                    elif self.direction.y < 0:
                        self.direction.y = 0
                        self.rect.top = sprite.rect.bottom


    def switch_stasuses(self):
        """
            Switching player View by status
        """
        self.image = self.game.textures["Character"][self.status][0]
        self.rect = self.image.get_rect(center=self.rect.center)

        self.animation = self.game.textures["Character"][self.status]
        self.animation_index = 0

    def animate(self):
        """
            Animating the player
        """


        self.animation_index += self.animation_speed


        if self.animation_index >= len(self.animation):
            self.animation_index = 0

        if self.facing == "right":
            image = self.animation[int(self.animation_index)]
        else:
            image = pygame.transform.flip(self.animation[int(self.animation_index)], True, False)

        self.image = image
        self.rect = self.image.get_rect(center=self.rect.center)


    def update(self, events):
        """
        Updating the player Data

        :param events: list of events from type pygame.Event
        """

        self.event_loop(events)
        self.animate()
        self.gravity()
        self.move(PLAYER_SPEED)

    def draw(self):
        """
        Drawing player on screen
        """

        self.screen.blit(self.image, (self.rect.x, self.rect.y + 10))