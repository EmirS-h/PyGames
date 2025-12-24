from engine.core.globals import Globals
import pygame
from os.path import join
from typing import override

# --- ENGINE IMPORTS ---
from engine.core.game import Game

# --- ENTITY IMPORTS ---
# Notice how clean these look now!
from games.space_shooters.entities.player import Player
from games.space_shooters.entities.meteor import Meteor
from games.space_shooters.entities.star import Star


class SpaceShooter(Game):
    def __init__(self):
        Globals.set("window_width", 1280)
        Globals.set("window_height", 720)

        super().__init__(
            game_file_path=__file__,
            caption="Space Shooter",
            width=Globals.get("window_width"),
            height=Globals.get("window_height"),
        )

        # 1. Load Assets
        self.font = pygame.font.Font(
            join(self.game_dir, "assets", "images", "Oxanium-Bold.ttf"), 32
        )
        self.player_surf = pygame.image.load(
            join(self.game_dir, "assets", "images", "player.png")
        ).convert_alpha()
        self.star_surf = pygame.image.load(
            join(self.game_dir, "assets", "images", "star.png")
        ).convert_alpha()
        self.meteor_surf = pygame.image.load(
            join(self.game_dir, "assets", "images", "meteor.png")
        ).convert_alpha()
        self.laser_surf = pygame.image.load(
            join(self.game_dir, "assets", "images", "laser.png")
        ).convert_alpha()

        # 2. Setup Groups
        self.all_sprites = pygame.sprite.Group()
        self.meteor_sprites = pygame.sprite.Group()
        self.laser_sprites = pygame.sprite.Group()

        # 3. Spawn Objects
        self.stars = [Star(self.all_sprites, self.star_surf) for _ in range(20)]

        # We pass the laser surface and groups to the Player now
        self.player = Player(
            sprite_group=self.all_sprites,
            image=self.player_surf,
            laser_surf=self.laser_surf,
            laser_groups=[self.all_sprites, self.laser_sprites],
        )

        # 4. Events
        self.meteor_event = pygame.event.custom_type()
        pygame.time.set_timer(self.meteor_event, 500)

        self.show_collision = False

    @override
    def update(self, dt: float) -> None:
        self.all_sprites.update(dt)
        self.check_collisions()

    @override
    def draw(self) -> None:
        self.screen.fill((22, 22, 22))
        self.display_score()
        self.all_sprites.draw(self.screen)

        if self.show_collision:
            for sprite in self.all_sprites:
                if hasattr(sprite, "draw_collision") and sprite.draw_collision:
                    pygame.draw.rect(self.screen, (0, 255, 0), sprite.rect, width=1)

    @override
    def on_event(self, event: pygame.event.Event) -> None:
        if event.type == self.meteor_event:
            Meteor([self.all_sprites, self.meteor_sprites], self.meteor_surf)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_QUOTEDBL:
            self.show_collision = not self.show_collision

    def check_collisions(self) -> None:
        if pygame.sprite.spritecollide(
            self.player,
            self.meteor_sprites,
            True,
            pygame.sprite.collide_mask,  # ty:ignore[invalid-argument-type]
        ):
            self.running = False

        for laser in self.laser_sprites:
            if pygame.sprite.spritecollide(
                laser,
                self.meteor_sprites,
                True,
                pygame.sprite.collide_mask,  # ty:ignore[invalid-argument-type]
            ):
                laser.kill()

    def display_score(self) -> None:
        current_time = pygame.time.get_ticks() // 100
        text_surface = self.font.render(str(current_time), True, (240, 240, 240))
        text_rect = text_surface.get_frect(midbottom=(1280 * 0.5, 720 - 50))
        self.screen.blit(text_surface, text_rect)
        pygame.draw.rect(
            self.screen,
            (240, 240, 240),
            text_rect.inflate(20, 10).move(0, -5),
            width=4,
            border_radius=4,
        )
