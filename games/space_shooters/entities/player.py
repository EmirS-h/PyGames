from engine.core.globals import Globals
import pygame
from pygame import Surface, Vector2, FRect
from pygame.sprite import Group

from engine.graphics.custom_sprite import CustomSprite

# Import Laser so Player can spawn it
from games.space_shooters.entities.laser import Laser


class Player(CustomSprite):
    image: Surface
    rect: FRect

    def __init__(
        self,
        sprite_group: Group,
        image: Surface,
        laser_surf: Surface,
        laser_groups: list[Group],
    ) -> None:
        super().__init__(sprite_group)

        self.image = image
        self.rect = self.image.get_frect(center=(1280 / 2, 720 / 2))

        # Store these so we can spawn lasers later
        self.laser_surf = laser_surf
        self.laser_groups = laser_groups

        self.direction = Vector2()
        self.speed = 400.0

        self.can_shoot = True
        self.laser_shoot_time = 0.0
        self.cooldown_duration = 200

        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt: float) -> None:
        # --- MOVEMENT (Fixed the bracket bug) ---
        keys = pygame.key.get_pressed()

        # Check keys separately!
        right = keys[pygame.K_RIGHT] or keys[pygame.K_d]
        left = keys[pygame.K_LEFT] or keys[pygame.K_a]
        down = keys[pygame.K_DOWN] or keys[pygame.K_s]
        up = keys[pygame.K_UP] or keys[pygame.K_w]

        self.direction.x = int(right) - int(left)
        self.direction.y = int(down) - int(up)

        if self.direction:
            self.direction = self.direction.normalize() * self.speed * dt
        self.rect.center += self.direction
        # --- CLAMP TO SCREEN (Using Globals!) ---
        # No need to pass screen_width to Player anymore!
        win_width = Globals.get("window_width")
        win_height = Globals.get("window_height")

        if win_width and win_height:
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.right > win_width:
                self.rect.right = win_width
            if self.rect.top < 0:
                self.rect.top = 0
            if self.rect.bottom > win_height:
                self.rect.bottom = win_height
        # --- SHOOTING ---
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0] and self.can_shoot:
            Laser(self.laser_groups, self.laser_surf, self.rect.midtop)
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()

        self.laser_timer()

    def laser_timer(self) -> None:
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_shoot_time >= self.cooldown_duration:
                self.can_shoot = True
