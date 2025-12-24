import pygame
import sys
import os
from abc import ABC, abstractmethod
from engine.core.input_manager import Input


class Game(ABC):
    screen: pygame.Surface
    clock: pygame.time.Clock
    running: bool
    dt: float

    game_dir: str

    def __init__(
        self,
        game_file_path: str,
        caption: str,
        width: int,
        height: int,
        target_fps: int = 60,
    ):
        pygame.init()

        # 1. Setup Display
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(caption)
        self.clock = pygame.time.Clock()
        self.running = True
        self.target_fps = target_fps

        # 2. Setup Paths
        # We use the path passed from the child class to know where assets are
        self.game_dir = os.path.dirname(os.path.abspath(game_file_path))

    def run(self) -> None:
        """The Master Game Loop. Every game uses this."""
        while self.running:
            # 1. Calculate Delta Time
            self.dt = self.clock.tick(self.target_fps) / 1000.0

            # 2. Handle Inputs (Quit, etc.)
            Input.update()
            self._handle_global_events()

            if Input.get_key_down(pygame.K_SPACE):
                print("uga buga")

            # 3. Game Specific Logic
            self.update(self.dt)
            self.draw()

            # 4. Refresh Screen
            pygame.display.update()

        pygame.quit()
        sys.exit()

    def _handle_global_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # Hook for games to handle their own specific events if needed
            self.on_event(event)

    # --- Methods the Child Game MUST implement ---
    @abstractmethod
    def update(self, dt: float) -> None:
        pass

    @abstractmethod
    def draw(self) -> None:
        pass

    # --- Optional Override ---
    def on_event(self, event: pygame.event.Event) -> None:
        pass
