from engine.core.globals import Globals
import pygame
import random
from pygame import Surface, Vector2, FRect
from pygame.sprite import Group
from engine.graphics.custom_sprite import CustomSprite


class Meteor(CustomSprite):
    image: Surface
    rect: FRect

    def __init__(self, sprite_groups: list[Group], image: Surface) -> None:
        super().__init__(sprite_groups)
        self.image = image
        self.rect = self.image.get_frect(
            center=(
                random.randint(0, Globals.get("window_width")),
                random.randint(-200, -100),
            )
        )
        self.start_time = pygame.time.get_ticks()
        self.life_time = 5000
        self.direction = Vector2(random.uniform(-0.5, 0.5), 1)
        self.speed = random.randint(50, 350)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt: float) -> None:
        self.rect.center += self.direction * self.speed * dt
        if pygame.time.get_ticks() - self.start_time >= self.life_time:
            self.kill()
