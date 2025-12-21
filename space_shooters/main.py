import pygame
import random
from pygame.sprite import Group
from pygame import Surface, FRect, Vector2
from os.path import join


class Player(pygame.sprite.Sprite):
    image: Surface
    rect: FRect

    direction: Vector2
    speed: float

    can_shoot: bool
    laser_shoot_time: float
    cooldown_duration: int

    def __init__(self, sprite_group: Group):
        super().__init__(sprite_group)

        self.image: Surface = pygame.image.load(
            join("assets", "images", "player.png")
        ).convert_alpha()

        self.rect: FRect = self.image.get_frect(
            center=(WINDOW_WIDTH * 0.5, WINDOW_HEIGHT * 0.5)
        )

        self.direction = Vector2()
        self.speed = 200.0

        self.can_shoot = True
        self.laser_shoot_time = 0.0
        self.cooldown_duration = 400

    def update(self, dt: float):
        keys = pygame.key.get_pressed()
        just_pressed = pygame.key.get_just_pressed()

        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])

        if self.direction:
            self.direction = self.direction.normalize() * self.speed * dt

        self.rect.center += self.direction

        if just_pressed[pygame.K_SPACE] and self.can_shoot:
            Laser(laser_surface, self.rect.midtop, all_sprites)
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()

        self.laser_timer()

    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_shoot_time >= self.cooldown_duration:
                self.can_shoot = True


class Star(pygame.sprite.Sprite):
    image: Surface
    rect: FRect

    def __init__(self, sprite_group: Group, star_surface: Surface):
        super().__init__(sprite_group)

        self.image = star_surface

        self.rect = self.image.get_frect(
            center=(
                random.randint(0, WINDOW_WIDTH),
                random.randint(0, WINDOW_HEIGHT),
            )
        )


class Laser(pygame.sprite.Sprite):
    image: Surface
    rect: FRect

    def __init__(self, laser_surface: Surface, pos, sprite_group: Group):
        super().__init__(sprite_group)
        self.image = laser_surface
        self.rect = self.image.get_frect(midbottom=pos)

    def update(self, dt: float):
        self.rect.centery -= 400 * dt

        if self.rect.bottom < -20.0:
            self.kill()


class Meteor(pygame.sprite.Sprite):
    image: Surface
    rect: FRect

    start_time: int
    life_time: int

    direction: Vector2
    speed: int

    def __init__(self, sprite_group: Group, meteor_surface: Surface):
        super().__init__(sprite_group)
        self.image = meteor_surface
        self.rect = self.image.get_frect(
            center=(random.randint(0, WINDOW_WIDTH), random.randint(-200, -100))
        )

        self.start_time = pygame.time.get_ticks()
        self.life_time = 5000

        self.direction = Vector2(random.uniform(-0.5, 0.5), 1)
        self.speed = random.randint(50, 350)

    def update(self, dt: float):
        self.rect.center += self.direction * self.speed * dt
        if pygame.time.get_ticks() - self.start_time >= self.life_time:
            self.kill()


# ------------ GENERAL SETUP --------------

pygame.init()

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720

display_surface: Surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Space Shooter")
running = True
clock = pygame.time.Clock()
dt: float = 1 / 60

# ------------- IMPORTS ----------------
star_surface = pygame.image.load(join("assets", "images", "star.png")).convert_alpha()
meteor_surface: Surface = pygame.image.load(
    join("assets", "images", "meteor.png")
).convert_alpha()
laser_surface: Surface = pygame.image.load(
    join("assets", "images", "laser.png")
).convert_alpha()


all_sprites = pygame.sprite.Group()
stars: list[Star] = [Star(all_sprites, star_surface) for _ in range(20)]
player = Player(all_sprites)


# ------------------- CUSTOM EVENTS ---------------------
# ********** METEOR EVENT **********
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 1500)

while running:
    dt: float = clock.tick(165) / 1000

    # ----------------- UPDATE -----------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

        if event.type == meteor_event:
            Meteor(all_sprites, meteor_surface)

    all_sprites.update(dt)

    # ----------------- DRAWING -----------------
    display_surface.fill("darkgray")

    all_sprites.draw(display_surface)

    pygame.display.update()

pygame.quit()
