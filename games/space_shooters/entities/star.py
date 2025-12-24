import random
from pygame import Surface, FRect
from pygame.sprite import Group
from engine.graphics.custom_sprite import CustomSprite


class Star(CustomSprite):
    image: Surface
    rect: FRect

    def __init__(self, sprite_group: Group, image: Surface) -> None:
        super().__init__(sprite_group)
        self.image = image
        self.rect = self.image.get_frect(
            center=(random.randint(0, 1280), random.randint(0, 720))
        )
        self.set_draw_collision(False)
