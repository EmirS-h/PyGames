import pygame
from pygame import Surface, FRect
from pygame.sprite import Group
from engine.graphics.custom_sprite import CustomSprite


class Laser(CustomSprite):
    image: Surface
    rect: FRect

    def __init__(self, sprite_groups: list[Group], image: Surface, pos) -> None:
        super().__init__(sprite_groups)
        self.image = image
        self.rect = self.image.get_frect(midbottom=pos)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt: float) -> None:
        self.rect.centery -= 800 * dt
        if self.rect.bottom < -20.0:
            self.kill()
