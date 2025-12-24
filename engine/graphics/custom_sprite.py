import pygame


class CustomSprite(pygame.sprite.Sprite):
    draw_collision: bool

    def __init__(self, sprite_group) -> None:
        super().__init__(sprite_group)

        self.draw_collision = True

    def set_draw_collision(self, value: bool) -> None:
        self.draw_collision = value
